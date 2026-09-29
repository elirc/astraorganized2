from pathlib import Path
import hashlib
import json

C = Path(__file__).resolve().parent
B = C.parents[1]
S = B / "stage/44013f102ff1"
path = S / "src/main/store.js"
baseline = json.loads((B / "baselines/44013f102ff1.json").read_text(encoding="utf-8"))["files"]
assert hashlib.sha256(path.read_bytes()).hexdigest() == baseline["src/main/store.js"]
assert (S / "docs/original/src/main/store.js.txt").read_bytes() == path.read_bytes()
path.write_text('''const { app, safeStorage } = require('electron');
const path = require('node:path');
const { createSettingsStore } = require('./settings-store');

// Resolve Electron's userData path lazily, after the application is ready.
let store;
function instance() {
  return store ||= createSettingsStore({
    file: path.join(app.getPath('userData'), 'settings.json'),
    encryption: safeStorage,
  });
}
module.exports = {
  get: (...args) => instance().get(...args),
  set: (...args) => instance().set(...args),
  all: () => instance().all(),
  public: () => instance().public(),
  reload: () => instance().reload(),
};
''', encoding="utf-8")
print("Replaced settings adapter; original snapshot preserved")
