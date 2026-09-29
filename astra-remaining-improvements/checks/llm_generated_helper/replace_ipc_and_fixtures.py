from pathlib import Path
import hashlib
import json

C = Path(__file__).resolve().parent
B = C.parents[1]
S = B / "stage/44013f102ff1"
baseline = json.loads((B / "baselines/44013f102ff1.json").read_text(encoding="utf-8"))["files"]
for relative in ["src/main/ipc.js", "test/store.test.js", "test/stt.test.js", "test/llm.test.js", "package.json"]:
    assert hashlib.sha256((S / relative).read_bytes()).hexdigest() == baseline[relative], relative
(S / "src/main/ipc.js").write_text('''const { ipcMain } = require('electron');
const settings = require('./store');
const { transcribe } = require('./stt');
const { generateAnswer } = require('./llm');
const { createIpcController } = require('./ipc-controller');

function registerIpc(getWin) {
  const handlers = createIpcController({ getWin, settings, transcribe, generateAnswer });
  for (const [channel, handler] of Object.entries(handlers)) ipcMain.handle(channel, handler);
}
module.exports = { registerIpc };
''', encoding="utf-8")
for relative in ["test/store.test.js", "test/stt.test.js", "test/llm.test.js"]:
    path = S / relative
    text = path.read_text(encoding="utf-8")
    text = text.replace("{ app: { getPath: () => userDataDir } }", "{ app: { getPath: () => userDataDir }, safeStorage: require('../verification/test-encryption.cjs') }")
    old = "try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch {}"
    assert old in text
    text = text.replace(old, "assert.equal(path.dirname(path.resolve(userDataDir)), path.resolve(os.tmpdir()));\n  assert.ok(path.basename(userDataDir).startsWith('aihelper-'));\n  for (const name of fs.readdirSync(userDataDir)) fs.unlinkSync(path.join(userDataDir, name));\n  fs.rmdirSync(userDataDir);")
    if relative == "test/store.test.js":
        start = text.index("test('a corrupted settings file falls back")
        end = text.index("\ntest('all()", start)
        text = text[:start] + """test('a corrupted settings file is preserved and requires explicit repair', () => {
  resetDisk('{{{ not json');
  const before = fs.readFileSync(settingsFile);
  const store = freshStore();
  assert.throws(() => store.get('anything', 'safe-default'), /Invalid JSON/);
  assert.throws(() => store.set({ recovered: true }), /Invalid JSON/);
  assert.deepEqual(fs.readFileSync(settingsFile), before);
});
""" + text[end:]
    path.write_text(text, encoding="utf-8")
package = json.loads((S / "package.json").read_text(encoding="utf-8"))
package["scripts"]["test"] = "node verification/run-tests.js"
(S / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
print("Updated IPC adapter and isolated fixtures; original assertions preserved except documented corruption policy change")
