from pathlib import Path
import re,json
B=Path('astrafinalplan/implementation/batch04')
for n in range(58,72):
 p=B/'stage'/str(n)/'server/package.json';d=json.loads(p.read_text());d['scripts']['start']='node dist/src/server.js';p.write_text(json.dumps(d,indent=2)+'\n')
for n in range(67,72):
 root=B/'stage'/str(n);sp=root/'server/src/services/service.ts';s=sp.read_text();mp=root/'server/src/models/model.ts';m=mp.read_text()
 statuses=json.loads(re.search(r'const allowedStatuses = (.*);',s)[1]);org=re.search(r'const orgColumn = "(.*?)"',m)[1];table=re.search(r'const table = "(.*?)"',m)[1]
 s=s.replace('!Number.isInteger(id) || id < 1','!/^\\d+$/.test(value) || !Number.isSafeInteger(id) || id < 1')
 start=s.index('  if (!partial && (!clean.title');end=s.index('  if (!partial) {',start)
 s=s[:start]+'''  if (!partial && clean.title === undefined) throw new ValidationError("A title is required.");
  if (partial && !Object.keys(clean).length) throw new ValidationError("Provide at least one editable field.");
  for (const key of ["title", "owner", "risk_level"]) {
    if (clean[key] !== undefined) {
      const value = clean[key];
      if (typeof value !== "string" || !value.trim() || value.trim().length > 255)
        throw new ValidationError(`${key} must contain 1–255 characters.`);
      clean[key] = value.trim();
    }
  }
  if (clean.status !== undefined && !allowedStatuses.includes(clean.status as string))
    throw new ValidationError(`Status must be one of: ${allowedStatuses.join(", ")}.`);
  if (clean.priority !== undefined && !allowedPriorities.includes(clean.priority as string))
    throw new ValidationError(`Priority must be one of: ${allowedPriorities.join(", ")}.`);
  if (clean.metadata !== undefined && (!clean.metadata || typeof clean.metadata !== "object" || Array.isArray(clean.metadata) || JSON.stringify(clean.metadata).length > 20000))
    throw new ValidationError("Metadata must be a JSON object of at most 20,000 characters.");
  if (clean.due_at !== undefined && clean.due_at !== null) {
    const value = clean.due_at;
    if (typeof value !== "string" || !/^\\d{4}-\\d{2}-\\d{2}(?:T.*)?$/.test(value) || !Number.isFinite(Date.parse(value)) || new Date(value.slice(0,10)).toISOString().slice(0,10) !== value.slice(0,10))
      throw new ValidationError("due_at must be a real ISO date or null.");
  }
  if (clean.ORG !== undefined && (typeof clean.ORG !== "number" || !Number.isSafeInteger(clean.ORG) || (clean.ORG as number) < 1))
    throw new ValidationError("ORG must be a positive integer.");

'''.replace('ORG',org)+s[end:]
 s=s.replace('payload.ids.length === 0','payload.ids.length === 0 || payload.ids.length > 100').replace('const ids = payload.ids.map((id) => parseId(String(id)));','const ids = [...new Set(payload.ids.map((id) => parseId(String(id))))];')
 s=s.replace('const body = String(payload.body || "").trim();','const body = typeof payload.body === "string" ? payload.body.trim() : "";').replace('if (!body) throw','if (!body || body.length > 10000) throw')
 sp.write_text(s)
 m='import { NotFoundError } from "../utils/errors.js";\n'+m
 m=m.replace('const before = await baseQuery(trx).where({ id }).first();','const before = await baseQuery(trx).where({ id }).forUpdate().first();\n    if (!before) throw new NotFoundError("Record not found.");')
 m=m.replace('.orderBy(query.sort, query.order)','.orderBy(query.sort, query.order).orderBy("id", query.order)')
 m=m.replace('const [record] = await trx(table).insert(payload)', 'const [record] = await trx(table).insert({ ...payload, ...statusFields(null, payload.status) })')
 m=m.replace('.update({ ...payload, version:', '.update({ ...payload, ...statusFields(before, payload.status), version:')
 start=m.index('    const rows = await trx(table)',m.index('export async function bulkStatus'));end=m.index('    return rows;',start)+len('    return rows;')
 m=m[:start]+'''    const beforeRows = await baseQuery(trx).whereIn("id", ids).orderBy("id").forUpdate();
    if (beforeRows.length !== ids.length) throw new NotFoundError("One or more records were not found; no statuses changed.");
    const rows = [];
    for (const before of beforeRows) {
      if (before.status === status) { rows.push(before); continue; }
      const [record] = await trx(table).where({id: before.id}).update({status, ...statusFields(before, status), version: trx.raw("version + 1"), updated_at: trx.fn.now()}).returning("*");
      await writeActivity(trx, before.id, "bulk_status", `Moved ${before.title} to ${status}`, {status});
      await writeAudit(trx, before.id, context, "bulk_status", before, record);
      rows.push(record);
    }
    return rows;'''+m[end:]
 m=m.replace('    const [record] = await trx(table)\n      .where({ id })\n      .whereNull("deleted_at")\n      .update({ ...updates,', '''    if (action === "archived" && before.archived_at) return before;
    if (action === "restored" && !before.archived_at) return before;
    if (action === "restored") updates = {archived_at: null, status_before_archive: null, status: before.status_before_archive || "FALLBACK"};
    else if (action === "archived") updates = {...updates, ...statusFields(before, "archived")};
    const [record] = await trx(table)
      .where({ id })
      .whereNull("deleted_at")
      .update({ ...updates,'''.replace('FALLBACK',statuses[0]))
 m+='''
// Keep lifecycle flags consistent even when a form or bulk action changes status.
function statusFields(before: any, status: unknown): Record<string, unknown> {
  if (status === undefined) return {};
  if (status === "archived") return {archived_at: before?.archived_at || db.fn.now(), status_before_archive: before?.status === "archived" ? before.status_before_archive : before?.status || "FALLBACK"};
  return {archived_at: null, status_before_archive: null};
}
'''.replace('FALLBACK',statuses[0])
 mp.write_text(m)
 (root/'server/db/migrations/003_archive_status.ts').write_text('''import type { Knex } from "knex";
export async function up(knex: Knex) { await knex.schema.alterTable("TABLE", table => {table.string("status_before_archive").nullable();}); }
export async function down(knex: Knex) { await knex.schema.alterTable("TABLE", table => {table.dropColumn("status_before_archive");}); }
'''.replace('TABLE',table))
 print(n,table,statuses)
