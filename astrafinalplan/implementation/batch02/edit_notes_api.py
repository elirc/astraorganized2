from pathlib import Path
import json
B=Path('astrafinalplan/implementation/batch02/stage');R=B/'19'
(R/'server/src/services/service.js').write_text('''const model = require("../models/model");
const { NotFoundError, ValidationError } = require("../utils/errors");
function parseId(value) {
  const id = Number(value);
  if (!Number.isInteger(id) || id < 1 || id > 2147483647) throw new ValidationError("Id must be a positive 32-bit integer.");
  return id;
}
function sanitizePayload(payload, partial = false) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) throw new ValidationError("Supply a note object.");
  const clean = {};
  for (const key of ["title", "folder", "status", "body"]) {
    if (partial && payload[key] === undefined) continue;
    const value = key === "body" && payload[key] === undefined ? "" : payload[key];
    if (typeof value !== "string" || (key !== "body" && !value.trim()) || value.length > (key === "body" ? 100000 : 255)) throw new ValidationError(`${key} must be valid bounded text.`);
    clean[key] = key === "body" ? value : value.trim();
  }
  if (!partial || payload.tags !== undefined) {
    const tags = payload.tags === undefined ? [] : payload.tags;
    if (!Array.isArray(tags) || tags.length > 30 || tags.some((tag) => typeof tag !== "string" || !tag.trim() || tag.length > 50)) throw new ValidationError("Use up to 30 nonempty text tags, each at most 50 characters.");
    clean.tags = [...new Set(tags.map((tag) => tag.trim()))];
  }
  if (!Object.keys(clean).length) throw new ValidationError("At least one note field is required.");
  return clean;
}
function list(query = {}) {
  const clean = {};
  for (const key of ["search", "status", "folder"]) {
    if (query[key] === undefined) continue;
    if (typeof query[key] !== "string" || query[key].length > 255) throw new ValidationError(`${key} must be text up to 255 characters.`);
    clean[key] = query[key].trim();
  }
  return model.listRecords(clean);
}
async function get(value) {
  const record = await model.findRecord(parseId(value));
  if (!record) throw new NotFoundError("note not found.");
  return record;
}
function create(payload) { return model.createRecord(sanitizePayload(payload)); }
async function update(value, payload) { await get(value); return model.updateRecord(parseId(value), sanitizePayload(payload, true)); }
async function remove(value) { await get(value); return model.deleteRecord(parseId(value)); }
function getStats() { return model.stats(); }
module.exports = { list, get, create, update, remove, getStats };
''',encoding='utf-8')
p=R/'server/src/models/model.js';s=p.read_text();a=s.index('function listRecords');b=s.index('/** Finds',a)
s=s[:a]+'''function listRecords(query) {
  const builder = db("notes").select("*").orderBy("created_at", "desc").orderBy("id", "desc");
  if (query.status) builder.where("status", query.status);
  if (query.folder) builder.where("folder", query.folder);
  // Search document content, not ids, timestamps or serialized row metadata.
  if (query.search) builder.whereRaw("to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, '')) @@ plainto_tsquery('english', ?)", [query.search]);
  return builder;
}
function databasePayload(payload) {
  return payload.tags === undefined ? payload : { ...payload, tags: JSON.stringify(payload.tags) };
}
'''+s[b:];s=s.replace('.insert(payload)', '.insert(databasePayload(payload))').replace('.update({ ...payload, updated_at:', '.update({ ...databasePayload(payload), updated_at:');p.write_text(s,encoding='utf-8')
p=R/'client/src/App.jsx';s=p.read_text().replace('useEffect, useMemo, useState','useEffect, useRef, useState');a=s.index('  const filteredRecords =');b=s.index('  /** Updates form state',a)
s=s[:a]+'''  const [searching, setSearching] = useState(false);
  const requestVersion = useRef(0);
  async function refresh() {
    const version = ++requestVersion.current;
    setSearching(true);
    try {
      const [nextRecords, nextStats] = await Promise.all([listRecords({ search }), loadStats()]);
      if (version !== requestVersion.current) return;
      setRecords(nextRecords); setStats(nextStats); setError("");
    } catch (requestError) {
      if (version === requestVersion.current) setError(requestError instanceof Error ? requestError.message : "Could not load notes");
    } finally {
      if (version === requestVersion.current) setSearching(false);
    }
  }
  useEffect(() => {
    setSearching(true);
    const timer = setTimeout(refresh, 250);
    return () => { clearTimeout(timer); requestVersion.current += 1; };
  }, [search]);

'''+s[b:];s=s.replace('placeholder="Search"','aria-label="Search note content" placeholder="Search words in title or body"').replace('{filteredRecords.map','{records.map');s=s.replace('      {error &&', '      <p role="status">{searching ? "Searching…" : `${records.length} matching notes`}</p>\n      {error &&');s=s.replace('    await deleteRecord(id);\n    await refresh();','    try { await deleteRecord(id); await refresh(); }\n    catch (requestError) { setError(requestError instanceof Error ? requestError.message : "Could not delete note"); }');p.write_text(s,encoding='utf-8')
p=R/'server/package.json';d=json.loads(p.read_text());d['scripts']['test']='node --test test/*.test.cjs';p.write_text(json.dumps(d,indent=2)+'\n')
print('Notes API content search, validation, JSON tags, and debounced client search implemented.')
