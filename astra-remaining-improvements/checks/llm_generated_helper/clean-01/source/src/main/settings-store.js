const { JsonFile, failure } = require("../shared/json-file");
const SECRET_KEYS = ["siliconflowKey", "deepseekKey"];
const PREFIX = "enc:v1:";

function validateSettings(value, encrypted = true) {
  if (!value || typeof value !== "object" || Array.isArray(value))
    throw failure(422, "Settings must be a JSON object");
  for (const key of SECRET_KEYS) {
    if (
      value[key] !== undefined &&
      (typeof value[key] !== "string" ||
        value[key].length > (encrypted ? 16384 : 512))
    )
      throw failure(422, "Invalid credential value");
  }
  for (const key of ["resume", "jobDescription"]) {
    if (
      value[key] !== undefined &&
      (typeof value[key] !== "string" || value[key].length > 200000)
    )
      throw failure(422, `Invalid ${key}; maximum 200000 characters`);
  }
  if (value.alwaysOnTop !== undefined && typeof value.alwaysOnTop !== "boolean")
    throw failure(422, "alwaysOnTop must be a boolean");
}

function createSettingsStore({ file, encryption, fsImpl }) {
  const disk = new JsonFile(file, {
    fsImpl,
    allowMissing: true,
    validate: validateSettings,
  });
  let accepted = null;
  function decode(stored) {
    const result = structuredClone(stored);
    for (const key of SECRET_KEYS) {
      const value = result[key];
      if (typeof value !== "string" || !value.startsWith("enc:")) continue;
      if (!value.startsWith(PREFIX))
        throw failure(
          503,
          "Unsupported encrypted credential format; the file was preserved",
        );
      try {
        result[key] = encryption.decryptString(
          Buffer.from(value.slice(PREFIX.length), "base64"),
        );
      } catch {
        throw failure(
          503,
          "A saved credential could not be decrypted. Restore access to the original OS profile or recover a backup; no key was cleared",
        );
      }
    }
    validateSettings(result, false);
    return result;
  }
  function refresh() {
    const snapshot = disk.read();
    if (
      accepted &&
      accepted.revision !== "missing" &&
      snapshot.revision === "missing"
    )
      throw failure(
        503,
        "The settings file disappeared. Restore it before editing this session",
      );
    const value = decode(snapshot.value);
    accepted = { value, revision: snapshot.revision };
    return accepted;
  }
  function load() {
    return accepted || refresh();
  }
  function publicSnapshot(refreshFirst = true) {
    const snapshot = refreshFirst ? refresh() : load();
    return {
      revision: snapshot.revision,
      resume: snapshot.value.resume ?? "",
      jobDescription: snapshot.value.jobDescription ?? "",
      alwaysOnTop: snapshot.value.alwaysOnTop !== false,
      credentials: Object.fromEntries(
        SECRET_KEYS.map((key) => [key, Boolean(snapshot.value[key]?.trim())]),
      ),
    };
  }
  return {
    get(key, fallback) {
      const value = load().value[key];
      return structuredClone(value === undefined ? fallback : value);
    },
    all() {
      return structuredClone(load().value);
    },
    public: publicSnapshot,
    reload() {
      refresh();
      return this.all();
    },
    set(changes, { expectedRevision } = {}) {
      validateSettings(changes, false);
      const snapshot = load();
      let next;
      const committed = disk.commit(
        expectedRevision ?? snapshot.revision,
        (draft) => {
          next = { ...decode(draft), ...structuredClone(changes) };
          validateSettings(next, false);
          const stored = structuredClone(next);
          for (const key of SECRET_KEYS) {
            if (!stored[key]) continue;
            let available = false;
            try {
              available = encryption?.isEncryptionAvailable() === true;
            } catch {}
            if (!available)
              throw failure(
                503,
                "OS credential encryption is unavailable. No plaintext credential was saved",
              );
            try {
              stored[key] =
                PREFIX +
                encryption.encryptString(stored[key]).toString("base64");
            } catch {
              throw failure(
                503,
                "Credential encryption failed; settings were not saved",
              );
            }
          }
          for (const key of Object.keys(draft)) delete draft[key];
          Object.assign(draft, stored);
        },
      );
      // Publishing after commit preserves the old in-memory snapshot on pre-replacement failure.
      accepted = { value: next, revision: committed.revision };
      return publicSnapshot(false);
    },
  };
}
module.exports = { createSettingsStore, validateSettings, SECRET_KEYS };
