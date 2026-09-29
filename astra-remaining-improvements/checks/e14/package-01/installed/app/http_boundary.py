"""Bound raw requests before parsing; constrain the local browser workspace."""

import json
import math
from urllib.parse import urlsplit

from starlette.responses import JSONResponse


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON property")
        result[key] = value
    return result


def finite_constant(_value):
    raise ValueError("Non-finite JSON number")


def finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("Non-finite JSON number")
    return number


class LocalHTTPBoundary:
    def __init__(self, app, settings):
        self.app, self.settings = app, settings

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = {}
        duplicates = set()
        for name, value in scope["headers"]:
            key = name.decode("latin1").lower()
            if key in headers:
                duplicates.add(key)
            headers[key] = value.decode("latin1")

        async def reject(code, detail):
            await JSONResponse(
                {"detail": detail}, status_code=code, headers={"Cache-Control": "no-store"}
            )(scope, receive, send)

        if duplicates & {
            "host",
            "origin",
            "authorization",
            "content-length",
            "content-type",
            "if-match",
        }:
            return await reject(400, "Ambiguous repeated request header")
        try:
            host = headers.get("host", "")
            parsed = urlsplit("http://" + host)
            valid_hosts = {"localhost", "127.0.0.1", "::1"}
            if self.settings.testing:
                valid_hosts.add("testserver")
            if (
                parsed.hostname not in valid_hosts
                or parsed.username
                or parsed.password
                or parsed.path
                or parsed.query
                or parsed.fragment
            ):
                return await reject(403, "This application accepts only local hostnames")
            port = parsed.port
            if port is not None and not 1 <= port <= 65535:
                raise ValueError("Invalid port")
            if headers.get("sec-fetch-site") == "cross-site":
                return await reject(403, "Cross-site browser requests are not allowed")
            origin = headers.get("origin")
            if origin and origin != scope.get("scheme", "http") + "://" + host:
                return await reject(403, "Origin must match this local server")
        except ValueError:
            return await reject(400, "Malformed local host header")
        if headers.get("content-encoding", "identity").lower() != "identity":
            return await reject(415, "Compressed request bodies are not supported")
        try:
            declared = int(headers.get("content-length", "0"))
            if declared < 0:
                raise ValueError()
        except ValueError:
            return await reject(400, "Invalid content length")
        if declared > self.settings.request_max_bytes:
            return await reject(413, "Request body exceeds the configured size limit")
        chunks = []
        size = 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            chunk = message.get("body", b"")
            size += len(chunk)
            if size > self.settings.request_max_bytes:
                return await reject(413, "Request body exceeds the configured size limit")
            chunks.append(chunk)
            if not message.get("more_body", False):
                break
        body = b"".join(chunks)
        if body and scope["path"].startswith("/api/"):
            if headers.get("content-type", "").split(";")[0].lower() != "application/json":
                return await reject(415, "Use application/json for API request bodies")
            try:
                json.loads(
                    body.decode("utf-8"),
                    object_pairs_hook=unique_object,
                    parse_constant=finite_constant,
                    parse_float=finite_float,
                )
            except (ValueError, UnicodeError, RecursionError):
                return await reject(
                    400, "Request must contain valid finite UTF-8 JSON without duplicate properties"
                )
        delivered = False

        async def replay():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": body, "more_body": False}
            return await receive()

        async def secured_send(message):
            if message["type"] == "http.response.start":
                extra = [
                    (b"cache-control", b"no-store"),
                    (b"x-content-type-options", b"nosniff"),
                    (b"referrer-policy", b"no-referrer"),
                ]
                if scope["path"] not in {"/docs", "/redoc", "/docs/oauth2-redirect"}:
                    extra.append(
                        (
                            b"content-security-policy",
                            b"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'",
                        )
                    )
                message["headers"] = [
                    (key, value)
                    for key, value in message.get("headers", [])
                    if key.lower() not in {b"cache-control"}
                ] + extra
            await send(message)

        await self.app(scope, replay, secured_send)
