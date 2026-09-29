const { app, safeStorage } = require("electron");
const path = require("node:path");
const { createSettingsStore } = require("./settings-store");

// Resolve Electron's userData path lazily, after the application is ready.
let store;
function instance() {
  return (store ||= createSettingsStore({
    file: path.join(app.getPath("userData"), "settings.json"),
    encryption: safeStorage,
  }));
}
module.exports = {
  get: (...args) => instance().get(...args),
  set: (...args) => instance().set(...args),
  all: () => instance().all(),
  public: () => instance().public(),
  reload: () => instance().reload(),
};
