const { ipcMain } = require("electron");
const settings = require("./store");
const { transcribe } = require("./stt");
const { generateAnswer } = require("./llm");
const { createIpcController } = require("./ipc-controller");

function registerIpc(getWin) {
  const handlers = createIpcController({
    getWin,
    settings,
    transcribe,
    generateAnswer,
  });
  for (const [channel, handler] of Object.entries(handlers))
    ipcMain.handle(channel, handler);
}
module.exports = { registerIpc };
