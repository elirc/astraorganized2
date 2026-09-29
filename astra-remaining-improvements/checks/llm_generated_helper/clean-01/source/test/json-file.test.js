const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { JsonFile } = require("../src/shared/json-file");

function fixture(t, options = {}) {
  const directory = fs.mkdtempSync(
    path.join(os.tmpdir(), "aihelper-json-file-"),
  );
  t.after(() => {
    assert.equal(
      path.dirname(path.resolve(directory)),
      path.resolve(os.tmpdir()),
    );
    assert.ok(path.basename(directory).startsWith("aihelper-json-file-"));
    for (const item of fs.readdirSync(directory))
      fs.unlinkSync(path.join(directory, item));
    fs.rmdirSync(directory);
  });
  const file = path.join(directory, "state.json");
  return { directory, file, disk: new JsonFile(file, options) };
}
test("explicit initialization refuses missing reads and existing-file overwrite", (t) => {
  const { disk, file } = fixture(t);
  assert.throws(() => disk.read(), /not initialized/);
  disk.initialize({ records: [] });
  const bytes = fs.readFileSync(file);
  assert.throws(
    () => disk.initialize({ records: ["replacement"] }),
    /changed|exists/,
  );
  assert.deepEqual(fs.readFileSync(file), bytes);
});
test("a held writer lease is never stolen or removed by another operation", (t) => {
  const { disk, file } = fixture(t);
  const first = disk.initialize({ value: 1 });
  fs.writeFileSync(file + ".lock", "another owner");
  assert.throws(
    () =>
      disk.commit(first.revision, (draft) => {
        draft.value = 2;
      }),
    /lease/,
  );
  assert.equal(fs.readFileSync(file + ".lock", "utf8"), "another owner");
  assert.equal(disk.read().value.value, 1);
});
test("byte revision detects external edits and retains the newer accepted file", (t) => {
  const { disk, file } = fixture(t);
  const first = disk.initialize({ value: 1 });
  fs.writeFileSync(file, '{"value":2}');
  assert.throws(
    () =>
      disk.commit(first.revision, (draft) => {
        draft.value = 3;
      }),
    /changed/,
  );
  assert.equal(disk.read().value.value, 2);
});
test("invalid Unicode, non-finite values, reserved keys and asynchronous mutations fail without changes", async (t) => {
  const { disk, file, directory } = fixture(t);
  const first = disk.initialize({ value: 1 });
  const before = fs.readFileSync(file);
  for (const value of [
    NaN,
    undefined,
    "\ud800",
    JSON.parse('{"__proto__":{}}'),
  ])
    assert.throws(() =>
      disk.commit(first.revision, (draft) => {
        draft.value = value;
      }),
    );
  assert.throws(
    () =>
      disk.commit(first.revision, async (draft) => {
        await Promise.resolve();
        draft.value = 2;
      }),
    /synchronous/,
  );
  await Promise.resolve();
  assert.deepEqual(fs.readFileSync(file), before);
  assert.deepEqual(fs.readdirSync(directory), ["state.json"]);
});
test("size limits refuse oversized reads and writes without erasing accepted data", (t) => {
  const { disk, file } = fixture(t, { maxBytes: 100 });
  const first = disk.initialize({ value: 1 });
  const before = fs.readFileSync(file);
  assert.throws(
    () =>
      disk.commit(first.revision, (draft) => {
        draft.value = "x".repeat(150);
      }),
    /size limit/,
  );
  assert.deepEqual(fs.readFileSync(file), before);
  fs.writeFileSync(file, "x".repeat(101));
  assert.throws(() => disk.read(), /size limit/);
  assert.equal(fs.readFileSync(file).length, 101);
});
test("corrupt UTF-8 and structurally invalid persisted records are reported without recovery", (t) => {
  const { disk, file } = fixture(t, {
    validate: (value) => {
      if (!Array.isArray(value.records)) throw new Error("Invalid records");
    },
  });
  fs.writeFileSync(file, Buffer.from([0xff]));
  assert.throws(() => disk.read(), /Invalid JSON/);
  assert.deepEqual(fs.readFileSync(file), Buffer.from([0xff]));
  fs.writeFileSync(file, "{}");
  assert.throws(() => disk.read(), /Invalid records/);
  assert.equal(fs.readFileSync(file, "utf8"), "{}");
});
test("returned snapshots and retained mutation drafts cannot alter accepted state", (t) => {
  const { disk } = fixture(t);
  const first = disk.initialize({ values: [] });
  let retained;
  const committed = disk.commit(first.revision, (draft) => {
    retained = draft;
    draft.values.push("accepted");
    return draft.values;
  });
  retained.values.push("late");
  committed.value.values.push("aliased");
  committed.result.push("result alias");
  assert.deepEqual(disk.read().value, { values: ["accepted"] });
});
test("failed exclusive temporary-file creation preserves the original error and never unlinks an unowned path", (t) => {
  const { disk, file } = fixture(t);
  const initial = disk.initialize({ value: 1 });
  const before = fs.readFileSync(file);
  const removed = [];
  const injected = Object.assign(
    new Error("Synthetic temporary-file permission failure"),
    { code: "EACCES" },
  );
  const faulty = new JsonFile(file, {
    fsImpl: {
      ...fs,
      openSync(name, ...args) {
        if (String(name).endsWith(".tmp")) throw injected;
        return fs.openSync(name, ...args);
      },
      unlinkSync(name) {
        removed.push(name);
        return fs.unlinkSync(name);
      },
    },
  });
  assert.throws(
    () =>
      faulty.commit(initial.revision, (draft) => {
        draft.value = 2;
      }),
    (error) => error === injected,
  );
  assert.deepEqual(removed, [file + ".lock"]);
  assert.deepEqual(fs.readFileSync(file), before);
});
