const { randomBytes } = require("node:crypto");
const { createService, createState } = require("./domain");
const { dataFile } = require("./server");

function setup(owner, file = dataFile()) {
  const token = randomBytes(32).toString("hex");
  const service = createService(file);
  service.disk.initialize(createState(owner, token));
  return { token, file };
}
if (require.main === module) {
  try {
    if (process.argv.length !== 3)
      throw new Error('Usage: node src/practice/setup.js "Your name"');
    const result = setup(process.argv[2]);
    console.log(
      `Created a new practice workspace at ${result.file}. Save this access token privately; it is shown once:`,
    );
    console.log(result.token);
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
module.exports = { setup };
