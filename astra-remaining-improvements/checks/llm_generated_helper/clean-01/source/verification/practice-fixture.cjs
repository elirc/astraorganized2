const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { randomBytes } = require("node:crypto");
const { createService, createState } = require("../src/practice/domain");
const { createServer } = require("../src/practice/server");

function fixture(t, options = {}) {
  const directory = fs.mkdtempSync(
    path.join(os.tmpdir(), "aihelper-practice-test-"),
  );
  const file = path.join(directory, "practice.json");
  const token = randomBytes(32).toString("hex");
  const service = createService(file, options);
  service.disk.initialize(createState("Practice learner", token));
  const servers = [];
  t.after(async () => {
    for (const server of servers)
      await new Promise((resolve) => {
        server.close(resolve);
        server.closeAllConnections();
      });
    assert.equal(
      path.dirname(path.resolve(directory)),
      path.resolve(os.tmpdir()),
    );
    assert.ok(path.basename(directory).startsWith("aihelper-practice-test-"));
    for (const name of fs.readdirSync(directory))
      fs.unlinkSync(path.join(directory, name));
    fs.rmdirSync(directory);
  });
  const revision = () => service.read().revision;
  const create = (kind, value) =>
    service.create(kind, value, revision()).result;
  const update = (kind, id, value) =>
    service.update(kind, id, value, revision()).result;
  const remove = (kind, id) => service.delete(kind, id, revision()).result;
  async function http() {
    const server = createServer({ service });
    servers.push(server);
    await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
    const url = `http://127.0.0.1:${server.address().port}`;
    const request = (route, { method = "GET", body, headers = {} } = {}) =>
      fetch(url + route, {
        method,
        headers: {
          Authorization: `Bearer ${token}`,
          ...(body !== undefined
            ? {
                "Content-Type": "application/json",
                "If-Match": `"${revision()}"`,
              }
            : {}),
          ...headers,
        },
        ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
      });
    return { url, request };
  }
  return {
    file,
    directory,
    token,
    service,
    create,
    update,
    remove,
    revision,
    http,
  };
}
module.exports = { fixture };
