const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { EventEmitter } = require("node:events");
const { createIpcController, PAGE } = require("../src/main/ipc-controller");
const { createSettingsStore } = require("../src/main/settings-store");

function fixture(t, dependencies = {}) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "aihelper-ipc-"));
  t.after(() => {
    assert.equal(
      path.dirname(path.resolve(directory)),
      path.resolve(os.tmpdir()),
    );
    assert.ok(path.basename(directory).startsWith("aihelper-ipc-"));
    for (const item of fs.readdirSync(directory))
      fs.unlinkSync(path.join(directory, item));
    fs.rmdirSync(directory);
  });
  const settings = createSettingsStore({
    file: path.join(directory, "settings.json"),
    encryption: require("../verification/test-encryption.cjs"),
  });
  const sender = new EventEmitter();
  sender.mainFrame = { url: PAGE };
  sender.isDestroyed = () => false;
  const sent = [];
  sender.send = (...args) => sent.push(args);
  const top = [];
  const win = {
    webContents: sender,
    isDestroyed: () => false,
    setAlwaysOnTop: (value) => top.push(value),
  };
  const event = { sender, senderFrame: sender.mainFrame };
  const handlers = createIpcController({
    getWin: () => win,
    settings,
    transcribe: async () => "A practice question",
    generateAnswer: async (_text, emit) => {
      emit("Practice answer");
      return "Practice answer";
    },
    ...dependencies,
  });
  return { settings, sender, sent, win, event, handlers, top };
}
function wav() {
  const bytes = Buffer.alloc(2048);
  bytes.write("RIFF");
  bytes.write("WAVE", 8);
  return bytes;
}
function deferred() {
  let resolve;
  const promise = new Promise((value) => {
    resolve = value;
  });
  return { promise, resolve };
}

test("IPC accepts only the live application main frame for every channel", async (t) => {
  const { handlers, event } = fixture(t);
  for (const untrusted of [
    {},
    { ...event, sender: {} },
    { ...event, senderFrame: { url: PAGE } },
    { ...event, senderFrame: null },
  ]) {
    for (const channel of ["settings:get", "settings:set", "ask:cancel"])
      assert.throws(() => handlers[channel](untrusted, {}), /Untrusted/);
    await assert.rejects(handlers.ask(untrusted, wav()), /Untrusted/);
  }
  event.senderFrame.url = "https://unrelated.example";
  assert.throws(() => handlers["settings:get"](event), /Untrusted/);
});

test("settings reads return credential presence without stored secrets or unknown legacy fields", (t) => {
  const { settings, handlers, event } = fixture(t);
  settings.set({
    deepseekKey: "synthetic-sensitive-value",
    resume: "My resume",
    unknownLegacy: "internal only",
  });
  const publicValue = handlers["settings:get"](event);
  assert.equal(publicValue.credentials.deepseekKey, true);
  assert.equal(publicValue.resume, "My resume");
  assert.equal(publicValue.deepseekKey, undefined);
  assert.equal(publicValue.unknownLegacy, undefined);
  assert.ok(!JSON.stringify(publicValue).includes("synthetic-sensitive-value"));
});

test("settings patch preserves omitted credentials, permits explicit clearing, and applies false", (t) => {
  const { settings, handlers, event, top } = fixture(t);
  settings.set({
    deepseekKey: "synthetic-sensitive-value",
    resume: "Initial",
    alwaysOnTop: true,
  });
  let current = handlers["settings:get"](event);
  current = handlers["settings:set"](event, {
    revision: current.revision,
    changes: { resume: "", alwaysOnTop: false },
  });
  assert.equal(settings.get("deepseekKey"), "synthetic-sensitive-value");
  assert.equal(settings.get("resume"), "");
  assert.deepEqual(top, [false]);
  current = handlers["settings:set"](event, {
    revision: current.revision,
    changes: { deepseekKey: "" },
  });
  assert.equal(current.credentials.deepseekKey, false);
});

test("stale settings revision refuses the complete change including window side effects", (t) => {
  const { settings, handlers, event, top } = fixture(t);
  const old = handlers["settings:get"](event);
  settings.set({ resume: "Other accepted value" });
  assert.throws(
    () =>
      handlers["settings:set"](event, {
        revision: old.revision,
        changes: { resume: "Lost update", alwaysOnTop: false },
      }),
    /changed/,
  );
  assert.equal(settings.get("resume"), "Other accepted value");
  assert.deepEqual(top, []);
});

test("settings contracts reject unknown keys, wrong types, missing revisions and line-break credentials", (t) => {
  const { handlers, event, settings } = fixture(t);
  const revision = handlers["settings:get"](event).revision;
  for (const input of [
    { changes: { resume: "x" } },
    { revision, changes: { unknown: "x" } },
    { revision, changes: { resume: false } },
    { revision, changes: { deepseekKey: "x\ny" } },
    { revision, changes: {} },
    { revision, changes: { resume: "x" }, extra: true },
  ])
    assert.throws(() => handlers["settings:set"](event, input));
  assert.deepEqual(settings.all(), {});
});

test("malformed WAV input never enters the provider pipeline", async (t) => {
  let calls = 0;
  const { handlers, event } = fixture(t, {
    transcribe: async () => {
      calls++;
    },
  });
  for (const payload of [null, "audio", Buffer.alloc(10), Buffer.alloc(2048)])
    await assert.rejects(handlers.ask(event, payload));
  assert.equal(calls, 0);
});

test("a successful request publishes transcript and chunks in order and removes lifetime listeners", async (t) => {
  const { handlers, event, sent, sender } = fixture(t);
  const result = await handlers.ask(event, wav());
  assert.deepEqual(sent, [
    ["transcript", "A practice question"],
    ["answer-chunk", "Practice answer"],
  ]);
  assert.equal(result.answer, "Practice answer");
  assert.equal(sender.listenerCount("destroyed"), 0);
  assert.equal(sender.listenerCount("did-start-navigation"), 0);
});

test("cancellation during transcription suppresses late output and prevents generation", async (t) => {
  const pending = deferred();
  let signal;
  let generations = 0;
  const { handlers, event, sent } = fixture(t, {
    transcribe: async (_wav, options) => {
      signal = options.signal;
      return pending.promise;
    },
    generateAnswer: async () => {
      generations++;
    },
  });
  const request = handlers.ask(event, wav());
  assert.deepEqual(handlers["ask:cancel"](event), { cancelled: true });
  assert.equal(signal.aborted, true);
  pending.resolve("Late transcript");
  await assert.rejects(request, /cancelled/);
  assert.equal(generations, 0);
  assert.deepEqual(sent, []);
});

test("duplicate requests are refused while the first remains active", async (t) => {
  const pending = deferred();
  const { handlers, event } = fixture(t, {
    transcribe: async () => pending.promise,
  });
  const first = handlers.ask(event, wav());
  await assert.rejects(handlers.ask(event, wav()), /already being processed/);
  handlers["ask:cancel"](event);
  pending.resolve("Late");
  await assert.rejects(first, /cancelled/);
});

test("window lifetime cancellation suppresses output even when a provider ignores AbortSignal", async (t) => {
  const pending = deferred();
  let emit;
  let signal;
  const { handlers, event, sender, sent } = fixture(t, {
    generateAnswer: async (_text, callback, options) => {
      emit = callback;
      signal = options.signal;
      return pending.promise;
    },
  });
  const request = handlers.ask(event, wav());
  await Promise.resolve();
  sender.emit("destroyed");
  assert.equal(signal.aborted, true);
  assert.throws(() => emit("Late chunk"), /cancelled/);
  pending.resolve("Late answer");
  await assert.rejects(request, /cancelled/);
  assert.deepEqual(sent, [["transcript", "A practice question"]]);
});

test("pipeline failure releases the busy guard for the next request", async (t) => {
  let attempts = 0;
  const { handlers, event } = fixture(t, {
    transcribe: async () => {
      if (++attempts === 1) throw new Error("Synthetic failure");
      return "Retry question";
    },
  });
  await assert.rejects(handlers.ask(event, wav()), /Synthetic failure/);
  assert.equal((await handlers.ask(event, wav())).answer, "Practice answer");
});
