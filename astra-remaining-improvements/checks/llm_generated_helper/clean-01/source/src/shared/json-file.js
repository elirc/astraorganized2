const fs = require("node:fs");
const path = require("node:path");
const { createHash, randomUUID } = require("node:crypto");

function failure(status, message) {
  return Object.assign(new Error(message), { status });
}
function jsonValue(value, depth = 0) {
  if (depth > 16) throw failure(422, "JSON nesting exceeds 16 levels");
  if (value === null || typeof value === "boolean") return;
  if (typeof value === "string") {
    if (!value.isWellFormed())
      throw failure(422, "Text contains invalid Unicode");
    return;
  }
  if (typeof value === "number" && Number.isFinite(value)) return;
  if (!value || typeof value !== "object")
    throw failure(422, "Only finite JSON values can be stored");
  if (
    !Array.isArray(value) &&
    Object.getPrototypeOf(value) !== Object.prototype &&
    Object.getPrototypeOf(value) !== null
  )
    throw failure(422, "Expected a plain JSON object");
  for (const key of Object.keys(value)) {
    if (["__proto__", "prototype", "constructor"].includes(key))
      throw failure(422, "Reserved JSON property");
    jsonValue(value[key], depth + 1);
  }
}
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");

class JsonFile {
  constructor(
    file,
    {
      fsImpl = fs,
      validate = () => {},
      maxBytes = 2 * 1024 * 1024,
      allowMissing = false,
    } = {},
  ) {
    if (typeof file !== "string" || !path.isAbsolute(file))
      throw new TypeError("An absolute data file path is required");
    this.file = path.resolve(file);
    this.fs = fsImpl;
    this.validate = validate;
    this.maxBytes = maxBytes;
    this.allowMissing = allowMissing;
  }

  read(allowMissing = this.allowMissing) {
    let bytes;
    try {
      const size = this.fs.statSync(this.file).size;
      if (size > this.maxBytes)
        throw failure(
          413,
          "Data file exceeds its size limit; it was not changed",
        );
      bytes = this.fs.readFileSync(this.file);
    } catch (error) {
      if (error.code === "ENOENT" && allowMissing)
        return { value: {}, revision: "missing" };
      if (error.code === "ENOENT")
        throw failure(503, "Workspace is not initialized; run explicit setup");
      throw error;
    }
    if (bytes.length > this.maxBytes)
      throw failure(
        413,
        "Data file exceeds its size limit; it was not changed",
      );
    let value;
    try {
      value = JSON.parse(
        new TextDecoder("utf-8", { fatal: true }).decode(bytes),
      );
    } catch {
      throw failure(
        503,
        "Invalid JSON data file. Preserve a backup and repair it explicitly; no recovery was performed",
      );
    }
    jsonValue(value);
    this.validate(value);
    return { value, revision: digest(bytes) };
  }

  initialize(value) {
    return this.commit(
      "missing",
      (draft) => {
        for (const key of Object.keys(draft)) delete draft[key];
        Object.assign(draft, structuredClone(value));
      },
      { initialize: true },
    );
  }

  commit(expectedRevision, mutate, { initialize = false } = {}) {
    if (
      typeof expectedRevision !== "string" ||
      !/^(missing|[a-f0-9]{64})$/.test(expectedRevision)
    )
      throw failure(428, "A valid accepted revision is required");
    if (typeof mutate !== "function")
      throw new TypeError("A synchronous mutation function is required");
    const parent = path.dirname(this.file);
    this.fs.mkdirSync(parent, { recursive: true });
    const lock = this.file + ".lock";
    let lease;
    try {
      lease = this.fs.openSync(lock, "wx", 0o600);
    } catch (error) {
      if (error.code === "EEXIST")
        throw failure(
          409,
          "Another writer holds the data lease. Reload after that writer finishes",
        );
      throw error;
    }
    let temporary = null;
    let descriptor = null;
    try {
      this.fs.writeFileSync(
        lease,
        JSON.stringify({
          pid: process.pid,
          createdAt: new Date().toISOString(),
        }),
      );
      const current = this.read(initialize || this.allowMissing);
      if (current.revision !== expectedRevision)
        throw failure(
          409,
          "The accepted data changed. Reload and review your draft before saving",
        );
      if (initialize && current.revision !== "missing")
        throw failure(409, "Workspace already exists");
      const draft = structuredClone(current.value);
      const result = mutate(draft);
      if (result && typeof result.then === "function")
        throw new TypeError("Mutation functions must be synchronous");
      jsonValue(draft);
      this.validate(draft);
      const bytes = Buffer.from(JSON.stringify(draft, null, 2) + "\n");
      if (bytes.length > this.maxBytes)
        throw failure(413, "Data file would exceed its size limit");
      const candidate = path.join(
        parent,
        `${path.basename(this.file)}.${randomUUID()}.tmp`,
      );
      descriptor = this.fs.openSync(candidate, "wx", 0o600);
      temporary = candidate; // Cleanup owns this path only after exclusive creation succeeds.
      this.fs.writeFileSync(descriptor, bytes);
      this.fs.fsyncSync(descriptor);
      this.fs.closeSync(descriptor);
      descriptor = null;
      this.fs.renameSync(temporary, this.file);
      temporary = null;
      // Return the exact representation accepted on disk, never a retained draft alias.
      return {
        value: JSON.parse(bytes.toString("utf8")),
        revision: digest(bytes),
        result: structuredClone(result),
      };
    } finally {
      try {
        if (descriptor !== null) this.fs.closeSync(descriptor);
      } finally {
        try {
          if (temporary !== null) this.fs.unlinkSync(temporary);
        } finally {
          try {
            this.fs.closeSync(lease);
          } finally {
            this.fs.unlinkSync(lock);
          }
        }
      }
    }
  }
}

module.exports = { JsonFile, jsonValue, failure };
