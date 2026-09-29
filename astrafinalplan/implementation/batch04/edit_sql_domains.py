from pathlib import Path
import json,re
B=Path('astrafinalplan/implementation/batch04');R=B/'stage';spec=json.loads((B/'domain-specs.json').read_text(encoding='utf-8'))
for x in spec:
 root=R/x['stage'];p=root/'server/src/index.ts';s=p.read_text(encoding='utf-8');route=x['route']
 a=s.index('app.get("'+route+'",');b=s.index('\napp.get(',a+1)
 s=s[:a]+'''app.get("ROUTE", asyncRoute(async (req,res) => {
  const filters = parseQuery(req.query as Record<string, unknown>);
  const sort = SORT_COLUMNS[filters.sort] ?? "created_at";
  const direction = filters.dir === "asc" ? "ASC" : "DESC";
  const where = `($1 = '' OR to_tsvector('english', title || ' ' || owner || ' ' || category || ' ' || notes) @@ websearch_to_tsquery('english', $1))
    AND ($2 = 'all' OR status = $2) AND ($3 = 'all' OR category = $3)`;
  const payload = await withTransaction(async client => {
    await client.query("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY");
    const params = [filters.search, filters.status, filters.category];
    const count = await client.query<{ total: string }>(`SELECT COUNT(*) AS total FROM items WHERE ${where}`, params);
    const total = Number(count.rows[0]!.total), totalPages = Math.max(1,Math.ceil(total / filters.pageSize));
    const page = Math.min(filters.page,totalPages);
    const result = await client.query<ItemRow>(`SELECT * FROM items WHERE ${where}
      ORDER BY ${sort} ${direction}, id ASC LIMIT $4 OFFSET $5`, [...params,filters.pageSize,(page-1)*filters.pageSize]);
    return { items: result.rows.map(toItem), total, totalPages, page, pageSize: filters.pageSize };
  });
  res.json(payload);
}));
'''.replace('ROUTE',route)+s[b:]
 a=s.index('    const rows = await query<ItemRow>("UPDATE items SET status=');b=s.index('\n  } catch',a)
 s=s[:a]+'''    const updated = await withTransaction(async client => {
      const current = await client.query<ItemRow>("SELECT * FROM items WHERE id=$1 FOR UPDATE",[req.params.id]);
      if (!current.rows[0]) return null;
      if (current.rows[0].status === status) return current.rows[0];
      const result = await client.query<ItemRow>("UPDATE items SET status=$1, updated_at=now() WHERE id=$2 RETURNING *",[status,req.params.id]);
      await client.query("INSERT INTO activity_entries (item_id,kind,body) VALUES ($1,'status',$2)",
        [req.params.id,"Changed status from " + current.rows[0].status + " to " + status]);
      return result.rows[0]!;
    });
    if (!updated) return res.status(404).json({ error: "Record not found." });
    res.json(toItem(updated));'''+s[b:]
 s=s.replace('const status = String(req.body.status || "");','const status = req.body?.status;')
 s=s.replace('function parseItem(body: Partial<NewItem>): NewItem {','''function parseItem(body: Partial<NewItem>): NewItem {
  if (!body || typeof body !== "object" || Array.isArray(body)) throw new ValidationError("Send a record object.");
  if ((["title","owner"] as const).some(key => typeof body[key] !== "string" || body[key].trim().length > 200) ||
      (["category","status","notes","priority","dueDate"] as const).some(key => body[key] !== undefined && typeof body[key] !== "string"))
    throw new ValidationError("Use text fields; title and owner allow at most 200 characters.");
  if (body.amount !== undefined && (typeof body.amount !== "number" && typeof body.amount !== "string" || String(body.amount).trim() === ""))
    throw new ValidationError("Amount must be a number.");
  if (body.dueDate && !validDate(body.dueDate)) throw new ValidationError("Use a real date in YYYY-MM-DD format.");
  if ((body.notes?.length ?? 0) > 10000 || body.priority && !["Low","Medium","High","Critical"].includes(body.priority))
    throw new ValidationError("Choose a valid priority and keep notes under 10000 characters.");''')
 s=s.replace('item.amount < 0','item.amount < 0 || item.amount > 9999999999.99')
 s=s.replace('Math.max(1, Number(query.page) || 1)','pageNumber(query.page, 1, 1000000)').replace('Math.min(25, Math.max(1, Number(query.pageSize) || 6))','pageNumber(query.pageSize, 6, 25)')
 s=s.replace('  const rows = await query<ActivityRow>("SELECT * FROM activity_entries WHERE item_id=$1 ORDER BY created_at DESC", [req.params.id]);','''  const parent = await query("SELECT id FROM items WHERE id=$1",[req.params.id]);
  if (!parent.length) return res.status(404).json({ error: "Record not found." });
  const rows = await query<ActivityRow>("SELECT * FROM activity_entries WHERE item_id=$1 ORDER BY created_at DESC, id ASC", [req.params.id]);''')
 s=s.replace('    const body = String(req.body.body || "").trim();','''    if (typeof req.body?.body !== "string" || req.body.body.length > 2000 ||
        req.body.kind !== undefined && (typeof req.body.kind !== "string" || !req.body.kind.trim() || req.body.kind.length > 40))
      throw new ValidationError("Activity needs text of 1-2000 characters and an optional short kind.");
    const parent = await query("SELECT id FROM items WHERE id=$1",[req.params.id]);
    if (!parent.length) return res.status(404).json({ error: "Record not found." });
    const body = req.body.body.trim();''')
 s=s.replace('app.use(express.json());','''app.use(express.json());
app.param("id", (req,res,next,value) => {
  if (typeof value !== "string" || !/^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$/i.test(value))
    return res.status(400).json({ error: "Use a valid record id." });
  next();
});''')
 s+='''\nfunction validDate(value: string) {
  return /^\\d{4}-\\d{2}-\\d{2}$/.test(value) && !Number.isNaN(Date.parse(value + "T00:00:00Z")) &&
    new Date(value + "T00:00:00Z").toISOString().slice(0,10) === value;
}
function pageNumber(value: unknown, fallback: number, maximum: number) {
  const number = Number(value ?? fallback);
  return Number.isSafeInteger(number) && number > 0 ? Math.min(number,maximum) : fallback;
}
''';p.write_text(s,encoding='utf-8')
 p=root/'server/src/db.ts';s=p.read_text(encoding='utf-8').replace('const { Pool } = pg;','const { Pool } = pg;\n// A calendar date is a label, not a local-midnight timestamp.\npg.types.setTypeParser(1082, value => value);');p.write_text(s,encoding='utf-8')
 p=root/'server/db/schema.sql';s=p.read_text(encoding='utf-8').replace('due_date::date','"dueDate"::date').replace('priority text, due_date text','priority text, "dueDate" text');p.write_text(s,encoding='utf-8')
print('Improved seven SQL domain apps: transactional repeat-safe status audit, snapshot pagination, validation and calendar dates.')
