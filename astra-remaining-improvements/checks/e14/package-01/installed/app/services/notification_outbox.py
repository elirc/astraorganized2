"""Explicit operator delivery of one durable outbox item; never called by HTTP."""

import http.client
import ipaddress
import json
import socket
import ssl
from urllib.parse import urlsplit

from sqlalchemy import update

from app.models import AlertDelivery


def validate_destination(url, settings):
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.fragment
        or parsed.port not in (None, 443)
    ):
        raise ValueError("Delivery requires HTTPS on port 443 without credentials or fragments")
    if parsed.hostname.lower() not in settings.webhook_hosts:
        raise ValueError("Destination hostname is not in OBS_WEBHOOK_HOSTS")
    return parsed


def send_https(url, payload, settings):
    parsed = validate_destination(url, settings)
    addresses = socket.getaddrinfo(parsed.hostname, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(item[4][0]).is_global for item in addresses):
        raise ValueError("Webhook DNS must resolve only to public IP addresses")
    # Connect to the checked address itself, retaining the original hostname for
    # TLS certificate validation. A second DNS lookup cannot change the target.
    address = addresses[0][4][0]

    class PinnedHTTPS(http.client.HTTPSConnection):
        def connect(self):
            raw = socket.create_connection((address, 443), timeout=5)
            try:
                self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
            except BaseException:
                raw.close()
                raise

    connection = PinnedHTTPS(parsed.hostname, timeout=5, context=ssl.create_default_context())
    try:
        body = json.dumps(payload, allow_nan=False).encode("utf-8")
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query
        connection.request(
            "POST",
            path,
            body=body,
            headers={"Content-Type": "application/json", "User-Agent": "E14-Explicit-Outbox/1"},
        )
        response = connection.getresponse()
        if len(response.read(4097)) > 4096:
            raise RuntimeError("Response exceeded the delivery response limit")
        if not 200 <= response.status < 300:
            raise RuntimeError("Destination did not acknowledge delivery")
    finally:
        connection.close()


def deliver_one(session_factory, settings, delivery_id, *, sender=send_https):
    if not settings.allow_notifications:
        raise ValueError("Set OBS_ALLOW_NOTIFICATIONS=1 for explicit operator delivery")
    with session_factory() as db:
        item = db.get(AlertDelivery, delivery_id)
        if item is None or item.status != "pending":
            raise ValueError("Only an existing pending delivery may be claimed")
        validate_destination(item.destination, settings)
        changed = db.execute(
            update(AlertDelivery)
            .where(AlertDelivery.id == delivery_id, AlertDelivery.status == "pending")
            .values(status="sending")
        )
        if changed.rowcount != 1:
            raise ValueError("Another worker already claimed this delivery")
        destination, payload = item.destination, {**item.payload, "delivery_id": delivery_id}
        db.commit()
    try:
        sender(destination, payload, settings)
        outcome = "sent"
    except ValueError:
        # Validation failure occurs before a network request is sent.
        outcome = "failed"
    except Exception:
        # The receiver might have accepted the request before the connection
        # failed. Do not automatically send it again.
        outcome = "uncertain"
    with session_factory() as db:
        changed = db.execute(
            update(AlertDelivery)
            .where(AlertDelivery.id == delivery_id, AlertDelivery.status == "sending")
            .values(status=outcome)
        )
        if changed.rowcount != 1:
            raise RuntimeError("Delivery claim changed; operator investigation required")
        db.commit()
    return outcome
