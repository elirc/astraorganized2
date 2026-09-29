const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { SECRET_KEYS } = require("./settings-store");
const { jsonValue, failure } = require("../shared/json-file");
const PAGE = pathToFileURL(
  path.resolve(__dirname, "../renderer/index.html"),
).href;
const LIMITS = {
  siliconflowKey: 512,
  deepseekKey: 512,
  resume: 200000,
  jobDescription: 200000,
};

function settingsInput(input) {
  jsonValue(input);
  if (
    !input ||
    Array.isArray(input) ||
    typeof input !== "object" ||
    Object.keys(input).some((key) => !["revision", "changes"].includes(key))
  )
    throw failure(422, "Expected a settings revision and changes");
  if (
    typeof input.revision !== "string" ||
    !/^(missing|[a-f0-9]{64})$/.test(input.revision)
  )
    throw failure(428, "Reload accepted settings before saving");
  const changes = input.changes;
  if (
    !changes ||
    typeof changes !== "object" ||
    Array.isArray(changes) ||
    !Object.keys(changes).length
  )
    throw failure(422, "Provide at least one settings change");
  for (const [key, value] of Object.entries(changes)) {
    if (key === "alwaysOnTop") {
      if (typeof value !== "boolean")
        throw failure(422, "alwaysOnTop must be a boolean");
    } else if (
      !Object.hasOwn(LIMITS, key) ||
      typeof value !== "string" ||
      value.length > LIMITS[key]
    )
      throw failure(422, "Unknown or invalid settings field");
    if (SECRET_KEYS.includes(key) && /[\r\n]/.test(value))
      throw failure(422, "Credentials cannot contain line breaks");
  }
  return structuredClone(input);
}

function wavBuffer(payload) {
  let source;
  if (payload instanceof ArrayBuffer) source = new Uint8Array(payload);
  else if (ArrayBuffer.isView(payload))
    source = new Uint8Array(
      payload.buffer,
      payload.byteOffset,
      payload.byteLength,
    );
  else throw failure(422, "Expected a WAV byte buffer");
  if (source.length < 1024 || source.length > 25 * 1024 * 1024)
    throw failure(422, "Recording must contain 1024 bytes to 25 MiB");
  const buffer = Buffer.from(source);
  if (
    buffer.toString("ascii", 0, 4) !== "RIFF" ||
    buffer.toString("ascii", 8, 12) !== "WAVE"
  )
    throw failure(422, "Expected a WAV recording");
  return buffer;
}

function createIpcController({ getWin, settings, transcribe, generateAnswer }) {
  let active = null;
  function trusted(event) {
    const win = getWin();
    if (
      !win ||
      win.isDestroyed() ||
      !event?.senderFrame ||
      event.sender !== win.webContents ||
      event.sender.isDestroyed() ||
      event.senderFrame !== win.webContents.mainFrame ||
      event.senderFrame.url !== PAGE
    )
      throw failure(403, "Untrusted application frame");
    return win;
  }
  const cancelled = () =>
    new Error(
      "Request cancelled. No further transcript or answer will be published",
    );
  return {
    "settings:get": (event) => {
      trusted(event);
      return settings.public();
    },
    "settings:set": (event, input) => {
      const win = trusted(event);
      const { revision, changes } = settingsInput(input);
      const result = settings.set(changes, { expectedRevision: revision });
      if (Object.hasOwn(changes, "alwaysOnTop") && !win.isDestroyed())
        win.setAlwaysOnTop(changes.alwaysOnTop);
      return result;
    },
    "ask:cancel": (event) => {
      trusted(event);
      if (active) active.abort();
      return { cancelled: Boolean(active) };
    },
    ask: async (event, payload) => {
      trusted(event);
      if (active) throw failure(409, "A recording is already being processed");
      const wav = wavBuffer(payload);
      const controller = new AbortController();
      active = controller;
      const abort = () => controller.abort();
      const sender = event.sender;
      sender.once("destroyed", abort);
      sender.once("render-process-gone", abort);
      sender.once("did-start-navigation", abort);
      const ensureCurrent = () => {
        if (controller.signal.aborted) throw cancelled();
        trusted(event);
      };
      try {
        const transcript = await transcribe(wav, { signal: controller.signal });
        ensureCurrent();
        if (typeof transcript !== "string" || !transcript.trim())
          throw new Error("No speech detected in the recording");
        if (transcript.length > 200000)
          throw new Error("Transcript exceeds the supported text limit");
        sender.send("transcript", transcript);
        const answer = await generateAnswer(
          transcript,
          (chunk) => {
            ensureCurrent();
            if (typeof chunk !== "string")
              throw new Error("Invalid answer chunk");
            sender.send("answer-chunk", chunk);
          },
          { signal: controller.signal },
        );
        ensureCurrent();
        return { transcript, answer };
      } finally {
        sender.removeListener("destroyed", abort);
        sender.removeListener("render-process-gone", abort);
        sender.removeListener("did-start-navigation", abort);
        if (active === controller) active = null;
      }
    },
  };
}

module.exports = { createIpcController, settingsInput, wavBuffer, PAGE };
