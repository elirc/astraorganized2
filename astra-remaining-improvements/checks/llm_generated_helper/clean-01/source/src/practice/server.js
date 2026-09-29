const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const { randomUUID } = require("node:crypto");
const { createService, authenticate, bootstrap, KINDS } = require("./domain");
const { failure, jsonValue } = require("../shared/json-file");
const UI = path.resolve(__dirname, "ui");
const MAX_BODY = 128 * 1024;

function dataFile() {
  return path.resolve(
    process.env.PRACTICE_DATA_FILE ||
      path.join(__dirname, "../../data/practice.json"),
  );
}
function headers(response) {
  response.setHeader("Cache-Control", "no-store");
  response.setHeader("X-Content-Type-Options", "nosniff");
  response.setHeader("Referrer-Policy", "no-referrer");
  response.setHeader(
    "Content-Security-Policy",
    "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'",
  );
  response.setHeader("X-Request-Id", randomUUID());
}
function boundary(request) {
  const port = request.socket.localPort;
  if (
    ![`127.0.0.1:${port}`, `localhost:${port}`].includes(request.headers.host)
  )
    throw failure(400, "Unexpected local Host header");
  if (
    !request.url ||
    request.url.length > 2048 ||
    !request.url.startsWith("/") ||
    request.url.startsWith("//") ||
    request.url.includes("#")
  )
    throw failure(400, "Invalid request URL");
  const origin = `http://${request.headers.host}`;
  if (request.headers.origin && request.headers.origin !== origin)
    throw failure(403, "Cross-origin requests are not accepted");
  if (request.headers["sec-fetch-site"] === "cross-site")
    throw failure(403, "Cross-site requests are not accepted");
  if (!["GET", "HEAD", "POST", "PATCH", "DELETE"].includes(request.method))
    throw failure(405, "Unsupported method");
  return new URL(request.url, origin);
}
function body(request) {
  if (
    request.headers["content-encoding"] &&
    request.headers["content-encoding"] !== "identity"
  )
    return Promise.reject(failure(415, "Compressed bodies are not accepted"));
  if (
    !/^application\/json(?:\s*;\s*charset=utf-8)?$/i.test(
      request.headers["content-type"] ?? "",
    )
  )
    return Promise.reject(failure(415, "Use application/json"));
  if (
    request.headers["content-length"] &&
    Number(request.headers["content-length"]) > MAX_BODY
  )
    return Promise.reject(
      Object.assign(failure(413, "Request exceeds 128 KiB"), { close: true }),
    );
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    const clean = () => {
      request.removeListener("data", data);
      request.removeListener("end", end);
      request.removeListener("error", error);
      request.removeListener("aborted", aborted);
    };
    const error = (value) => {
      clean();
      reject(value);
    };
    const aborted = () => error(failure(400, "Request aborted"));
    const data = (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY) {
        request.pause();
        error(
          Object.assign(failure(413, "Request exceeds 128 KiB"), {
            close: true,
          }),
        );
        return;
      }
      chunks.push(chunk);
    };
    const end = () => {
      clean();
      try {
        const value = JSON.parse(
          new TextDecoder("utf-8", { fatal: true }).decode(
            Buffer.concat(chunks),
          ),
        );
        if (!value || typeof value !== "object" || Array.isArray(value))
          throw new Error();
        jsonValue(value);
        resolve(value);
      } catch {
        reject(failure(400, "Expected a bounded, valid JSON object"));
      }
    };
    request.on("data", data);
    request.once("end", end);
    request.once("error", error);
    request.once("aborted", aborted);
  });
}
function revision(request) {
  const match = /^"([a-f0-9]{64})"$/.exec(request.headers["if-match"] ?? "");
  if (!match)
    throw failure(
      428,
      "Load the workspace and send its quoted If-Match revision",
    );
  return match[1];
}
function send(response, status, payload, acceptedRevision) {
  if (acceptedRevision) response.setHeader("ETag", `"${acceptedRevision}"`);
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
  });
  response.end(JSON.stringify(payload));
}
function createServer({
  file = dataFile(),
  service = createService(file),
} = {}) {
  service.read(); // Missing/corrupt workspaces do not silently initialize on start.
  const server = http.createServer(async (request, response) => {
    headers(response);
    try {
      const url = boundary(request);
      if (!url.pathname.startsWith("/api/")) {
        if (!["GET", "HEAD"].includes(request.method))
          throw failure(405, "Static pages support GET and HEAD");
        const files = {
          "/": ["index.html", "text/html"],
          "/app.js": ["app.js", "application/javascript"],
          "/styles.css": ["styles.css", "text/css"],
        };
        const entry = files[url.pathname];
        if (!entry) throw failure(404, "Page not found");
        const bytes = fs.readFileSync(path.join(UI, entry[0]));
        response.writeHead(200, {
          "Content-Type": entry[1] + "; charset=utf-8",
        });
        response.end(request.method === "HEAD" ? undefined : bytes);
        return;
      }
      if (request.method === "HEAD")
        throw failure(405, "API resources support GET");
      const write = ["POST", "PATCH", "DELETE"].includes(request.method);
      const input = write ? await body(request) : null;
      // Authenticate against the same accepted snapshot used for this operation.
      const snapshot = service.read();
      authenticate(snapshot.value, request.headers.authorization);
      if (request.method === "GET" && url.pathname === "/api/bootstrap") {
        send(response, 200, bootstrap(snapshot), snapshot.revision);
        return;
      }
      if (request.method === "GET" && url.pathname === "/api/export") {
        response.setHeader(
          "Content-Disposition",
          'attachment; filename="practice-export.json"',
        );
        send(
          response,
          200,
          {
            schemaVersion: 1,
            exportedAt: new Date().toISOString(),
            ...Object.fromEntries(
              KINDS.map((kind) => [kind, snapshot.value[kind]]),
            ),
          },
          snapshot.revision,
        );
        return;
      }
      const match =
        /^\/api\/(profiles|questions|sessions|attempts)(?:\/([a-f0-9-]+))?$/.exec(
          url.pathname,
        );
      if (!match) throw failure(404, "API resource not found");
      const [, kind, id] = match;
      if (request.method === "GET") {
        send(
          response,
          200,
          id
            ? service.get(snapshot, kind, id)
            : service.list(snapshot, kind, url.searchParams),
          snapshot.revision,
        );
        return;
      }
      if (url.search)
        throw failure(422, "Mutation requests do not accept query parameters");
      const expected = revision(request);
      let result;
      if (request.method === "POST" && !id)
        result = service.create(kind, input, expected);
      else if (request.method === "PATCH" && id)
        result = service.update(kind, id, input, expected);
      else if (request.method === "DELETE" && id) {
        if (Object.keys(input).length)
          throw failure(422, "Deletion expects an empty JSON object");
        result = service.delete(kind, id, expected);
      } else throw failure(405, "Method does not match this resource");
      send(
        response,
        request.method === "POST" ? 201 : 200,
        result.result,
        result.revision,
      );
    } catch (error) {
      if (response.headersSent) {
        response.destroy();
        return;
      }
      if (error.close) response.setHeader("Connection", "close");
      send(response, error.status || 500, {
        error: error.status
          ? error.message
          : "The operation could not be completed; review accepted state before retrying",
      });
    }
  });
  server.requestTimeout = 15000;
  server.headersTimeout = 10000;
  server.keepAliveTimeout = 5000;
  server.maxRequestsPerSocket = 100;
  return server;
}
if (require.main === module) {
  const port = Number(process.env.PRACTICE_PORT || 4310);
  if (!Number.isInteger(port) || port < 1 || port > 65535)
    throw new Error("PRACTICE_PORT must be an integer from 1 to 65535");
  createServer().listen(port, "127.0.0.1", () =>
    console.log(`Practice workspace: http://127.0.0.1:${port}`),
  );
}
module.exports = { createServer, dataFile };
