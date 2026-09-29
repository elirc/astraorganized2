from pathlib import Path
P=Path(__file__).resolve().parent/'stage/092c5e5b7052'
p=P/'server/store.js'
p.write_text(r'''import * as Y from 'yjs';
import { mkdirSync, readdirSync, readFileSync, writeFileSync, renameSync, unlinkSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { randomUUID } from 'node:crypto';

export class DocumentError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}
export function validateId(id) {
  if (typeof id !== 'string' || !/^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$/.test(id))
    throw new DocumentError(400, 'Document ID must be 1–64 letters, numbers, underscores or hyphens.');
  return id;
}
function validateTitle(title) {
  if (typeof title !== 'string' || !title.trim() || title.trim().length > 100)
    throw new DocumentError(400, 'Title must contain 1–100 characters.');
  return title.trim();
}
function checkVersion(record, version) {
  if (!Number.isSafeInteger(version) || version < 1) throw new DocumentError(400, 'A positive metadata version is required.');
  if (record.version !== version) throw new DocumentError(409, 'Document metadata changed. Refresh and retry.');
}

export class DocumentStore {
  constructor(directory, { maxStateBytes = 8 * 1024 * 1024 } = {}) {
    this.directory = resolve(directory);
    this.maxStateBytes = maxStateBytes;
    this.entries = new Map();
    mkdirSync(this.directory, { recursive: true });
    try {
      for (const name of readdirSync(this.directory).filter(name => name.endsWith('.json'))) {
        const record = JSON.parse(readFileSync(join(this.directory, name), 'utf8'));
        validateId(record.id);
        if (name !== `${record.id}.json` || record.format !== 1 || this.entries.has(record.id)) throw new Error('Invalid document identity or format.');
        validateTitle(record.title);
        if (!Number.isSafeInteger(record.version) || record.version < 1 || typeof record.deleted !== 'boolean') throw new Error('Invalid document metadata.');
        if (typeof record.createdAt !== 'string' || typeof record.updatedAt !== 'string' || !Number.isFinite(Date.parse(record.createdAt)) || !Number.isFinite(Date.parse(record.updatedAt))) throw new Error('Invalid document timestamp.');
        if (typeof record.update !== 'string' || !/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(record.update)) throw new Error('Invalid document state encoding.');
        const bytes = Buffer.from(record.update, 'base64');
        if (bytes.length > this.maxStateBytes) throw new Error('Document state exceeds its size limit.');
        const doc = new Y.Doc();
        try { Y.applyUpdate(doc, bytes); } catch (error) { doc.destroy(); throw error; }
        this.entries.set(record.id, { record, doc });
      }
    } catch (error) {
      this.destroy();
      throw new Error(`Stored documents could not be loaded; files were not replaced: ${error.message}`, { cause: error });
    }
  }
  metadata(entry) {
    const { id, title, version, createdAt, updatedAt } = entry.record;
    return { id, title, version, createdAt, updatedAt, characters: entry.doc.getText('markdown-content').length };
  }
  require(id) {
    validateId(id);
    const entry = this.entries.get(id);
    if (!entry || entry.record.deleted) throw new DocumentError(404, 'Document not found.');
    return entry;
  }
  list() {
    return [...this.entries.values()].filter(entry => !entry.record.deleted).map(entry => this.metadata(entry))
      .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt) || a.id.localeCompare(b.id));
  }
  get(id) { return this.metadata(this.require(id)); }
  create(id, title = id) {
    validateId(id); title = validateTitle(title);
    const existing = this.entries.get(id);
    if (existing?.record.deleted) throw new DocumentError(409, 'This document ID was deleted. Choose a new ID.');
    if (existing) return { created: false, document: this.metadata(existing) };
    const doc = new Y.Doc();
    const now = new Date().toISOString();
    const record = { format: 1, id, title, version: 1, createdAt: now, updatedAt: now, deleted: false, update: Buffer.from(Y.encodeStateAsUpdate(doc)).toString('base64') };
    try { this.persist(record); } catch (error) { doc.destroy(); throw error; }
    const entry = { record, doc }; this.entries.set(id, entry);
    return { created: true, document: this.metadata(entry) };
  }
  rename(id, title, version) {
    const entry = this.require(id); title = validateTitle(title); checkVersion(entry.record, version);
    const record = { ...entry.record, title, version: entry.record.version + 1, updatedAt: new Date().toISOString() };
    this.persist(record); entry.record = record;
    return this.metadata(entry);
  }
  delete(id, version) {
    const entry = this.require(id); checkVersion(entry.record, version);
    const empty = new Y.Doc();
    const record = { ...entry.record, deleted: true, version: entry.record.version + 1, updatedAt: new Date().toISOString(), update: Buffer.from(Y.encodeStateAsUpdate(empty)).toString('base64') };
    empty.destroy();
    this.persist(record); entry.record = record;
  }
  applyUpdate(id, update) {
    const entry = this.require(id);
    const candidate = new Y.Doc();
    try {
      Y.applyUpdate(candidate, Y.encodeStateAsUpdate(entry.doc));
      try { Y.applyUpdate(candidate, update); } catch { throw new DocumentError(400, 'Invalid collaborative update.'); }
      const encoded = Y.encodeStateAsUpdate(candidate);
      if (encoded.length > this.maxStateBytes) throw new DocumentError(413, 'Document state exceeds its size limit.');
      const previous = Buffer.from(Y.encodeStateAsUpdate(entry.doc));
      if (previous.equals(Buffer.from(encoded))) return false;
      const record = { ...entry.record, update: Buffer.from(encoded).toString('base64'), updatedAt: new Date().toISOString() };
      // Disk acceptance precedes live state mutation and broadcast by the server.
      this.persist(record);
      Y.applyUpdate(entry.doc, update);
      entry.record = record;
      return true;
    } finally { candidate.destroy(); }
  }
  persist(record) {
    const destination = join(this.directory, `${validateId(record.id)}.json`);
    const temporary = join(this.directory, `.${record.id}-${randomUUID()}.tmp`);
    try {
      writeFileSync(temporary, JSON.stringify(record), { encoding: 'utf8', flag: 'wx' });
      renameSync(temporary, destination);
    } finally { if (existsSync(temporary)) unlinkSync(temporary); }
  }
  destroy() { for (const entry of this.entries.values()) entry.doc.destroy(); this.entries.clear(); }
}
''',encoding='utf-8')
