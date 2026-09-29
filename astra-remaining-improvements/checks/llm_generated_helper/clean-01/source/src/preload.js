const { contextBridge, ipcRenderer } = require("electron");

// Minimal, explicit bridge between the page and the main process.
// Only these six functions are reachable from the page; ipcRenderer itself
// (and any Node primitive) is never exposed. Only string event payloads cross
// the bridge; subscriptions return an explicit cleanup function.

contextBridge.exposeInMainWorld("api", {
  getSettings: () => ipcRenderer.invoke("settings:get"),
  saveSettings: (obj) => ipcRenderer.invoke("settings:set", obj),
  ask: (wavArrayBuffer) => ipcRenderer.invoke("ask", wavArrayBuffer),
  cancelAsk: () => ipcRenderer.invoke("ask:cancel"),
  onTranscript: (cb) => {
    if (typeof cb !== "function")
      throw new TypeError("onTranscript expects a function");
    const listener = (_e, text) => {
      if (typeof text === "string") cb(text);
    };
    ipcRenderer.on("transcript", listener);
    return () => ipcRenderer.removeListener("transcript", listener);
  },
  onAnswerChunk: (cb) => {
    if (typeof cb !== "function")
      throw new TypeError("onAnswerChunk expects a function");
    const listener = (_e, chunk) => {
      if (typeof chunk === "string") cb(chunk);
    };
    ipcRenderer.on("answer-chunk", listener);
    return () => ipcRenderer.removeListener("answer-chunk", listener);
  },
});
