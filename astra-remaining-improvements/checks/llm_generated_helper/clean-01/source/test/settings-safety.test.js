const { test, after } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const Module = require("node:module");

const directory = fs.mkdtempSync(
  path.join(os.tmpdir(), "aihelper-settings-safety-"),
);
const file = path.join(directory, "settings.json");
const originalLoad = Module._load;
let available = true;
let decryptFails = false;
const crypto = {
  isEncryptionAvailable: () => available,
  encryptString: (value) => Buffer.from(`synthetic:${value}`),
  decryptString: (value) => {
    if (decryptFails) throw new Error("Synthetic decryption failure");
    return value.toString().slice("synthetic:".length);
  },
};
Module._load = function (request) {
  if (request === "electron")
    return { app: { getPath: () => directory }, safeStorage: crypto };
  return originalLoad.apply(this, arguments);
};
const moduleId = require.resolve("../src/main/store.js");
function fresh() {
  delete require.cache[moduleId];
  return require(moduleId);
}
function reset() {
  available = true;
  decryptFails = false;
  for (const entry of fs.readdirSync(directory))
    fs.unlinkSync(path.join(directory, entry));
}
after(() => {
  Module._load = originalLoad;
  assert.equal(
    path.dirname(path.resolve(directory)),
    path.resolve(os.tmpdir()),
  );
  assert.ok(path.basename(directory).startsWith("aihelper-settings-safety-"));
  for (const entry of fs.readdirSync(directory))
    fs.unlinkSync(path.join(directory, entry));
  fs.rmdirSync(directory);
});

test("failed replacement preserves the accepted settings in memory and on disk", () => {
  reset();
  const store = fresh();
  store.set({ resume: "Accepted resume" });
  const before = fs.readFileSync(file);
  const rename = fs.renameSync;
  fs.renameSync = () => {
    throw new Error("Injected replacement failure");
  };
  try {
    assert.throws(
      () => store.set({ resume: "Rejected resume" }),
      /replacement failure/,
    );
  } finally {
    fs.renameSync = rename;
  }
  assert.equal(store.get("resume"), "Accepted resume");
  assert.deepEqual(fs.readFileSync(file), before);
  assert.deepEqual(fs.readdirSync(directory), ["settings.json"]);
});

test("nested reads cannot mutate settings outside an accepted save", () => {
  reset();
  const store = fresh();
  store.set({ nested: { items: ["accepted"] } });
  store.get("nested").items.push("mutated through get");
  store.all().nested.items.push("mutated through all");
  assert.deepEqual(store.get("nested"), { items: ["accepted"] });
});

test("corrupt settings are reported and left in place without implicit recovery", () => {
  reset();
  const raw = Buffer.from("{broken");
  fs.writeFileSync(file, raw);
  assert.throws(() => fresh().all(), /invalid|corrupt|JSON/i);
  assert.deepEqual(fs.readFileSync(file), raw);
  assert.deepEqual(fs.readdirSync(directory), ["settings.json"]);
});

test("an unreadable existing file cannot turn into writable defaults", () => {
  reset();
  fs.writeFileSync(file, '{"resume":"Keep me"}');
  const store = fresh();
  const read = fs.readFileSync;
  fs.readFileSync = function (target, ...args) {
    if (path.resolve(String(target)) === file)
      throw Object.assign(new Error("Access denied"), { code: "EACCES" });
    return read.call(this, target, ...args);
  };
  try {
    assert.throws(
      () => store.set({ resume: "Would overwrite" }),
      /denied|read/i,
    );
  } finally {
    fs.readFileSync = read;
  }
  assert.equal(JSON.parse(fs.readFileSync(file, "utf8")).resume, "Keep me");
});

test("undecryptable credentials remain an explicit error and are preserved", () => {
  reset();
  const store = fresh();
  store.set({ deepseekKey: "synthetic-key" });
  const before = fs.readFileSync(file);
  decryptFails = true;
  assert.throws(() => fresh().all(), /decrypt|credential/i);
  assert.deepEqual(fs.readFileSync(file), before);
});

test("new credentials are not silently stored as plaintext when encryption is unavailable", () => {
  reset();
  available = false;
  assert.throws(
    () => fresh().set({ deepseekKey: "synthetic-key" }),
    /encrypt/i,
  );
  assert.equal(fs.existsSync(file), false);
});

test("a stale settings writer cannot overwrite another accepted save", () => {
  reset();
  const first = fresh();
  first.set({ resume: "Initial" });
  const second = fresh();
  second.all();
  first.set({ resume: "Other accepted change" });
  assert.throws(
    () => second.set({ jobDescription: "Stale writer" }),
    /changed|conflict|reload/i,
  );
  assert.equal(fresh().get("resume"), "Other accepted change");
  assert.equal(fresh().get("jobDescription"), undefined);
});

test("reading a legacy plaintext credential never rewrites the file", () => {
  reset();
  const raw = Buffer.from('{"deepseekKey":"synthetic-legacy"}');
  fs.writeFileSync(file, raw);
  assert.equal(fresh().get("deepseekKey"), "synthetic-legacy");
  assert.deepEqual(fs.readFileSync(file), raw);
});
