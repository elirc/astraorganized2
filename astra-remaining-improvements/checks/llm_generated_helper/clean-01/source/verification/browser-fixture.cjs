// Only an isolated temporary workspace; never reads Electron userData.
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { randomBytes } = require("node:crypto");
const { createState, createService } = require("../src/practice/domain");
const { createServer } = require("../src/practice/server");
const directory = fs.mkdtempSync(path.join(os.tmpdir(), "aihelper-browser-"));
const token = randomBytes(32).toString("hex");
const service = createService(path.join(directory, "practice.json"));
service.disk.initialize(createState("Browser learner", token));
for (let index = 1; index <= 23; index++)
  service.create(
    "profiles",
    {
      name: `Seed profile ${String(index).padStart(2, "0")}`,
      targetRole: "CRUD developer",
    },
    service.read().revision,
  );
const server = createServer({ service });
server.listen(0, "127.0.0.1", () =>
  console.log(
    JSON.stringify({ url: `http://127.0.0.1:${server.address().port}`, token }),
  ),
);
process.stdin.resume();
process.stdin.once("data", () => {
  server.close(() => {
    if (
      path.dirname(path.resolve(directory)) !== path.resolve(os.tmpdir()) ||
      !path.basename(directory).startsWith("aihelper-browser-")
    )
      throw new Error("Unexpected cleanup target");
    for (const name of fs.readdirSync(directory))
      fs.unlinkSync(path.join(directory, name));
    fs.rmdirSync(directory);
    process.exit(0);
  });
  server.closeAllConnections();
});
