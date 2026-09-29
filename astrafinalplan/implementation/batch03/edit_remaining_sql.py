from pathlib import Path
B=Path('astrafinalplan/implementation/batch03/stage')
p=B/'33/server/src/index.ts';s=p.read_text(encoding='utf-8');a=s.index('app.get("/api/threads",');b=s.index('\napp.get(',a+1);part=s[a:b]
part=part.replace('const page = Math.max(1, Number(req.query.page) || 1);','let page = pageNumber(req.query.page,1,1000000);').replace('const pageSize = Math.min(20, Math.max(1, Number(req.query.pageSize) || 5));','const pageSize = pageNumber(req.query.pageSize,5,20);')
part=part.replace('  const offset = (page - 1) * pageSize;','''  return withTransaction(async client => {
  await client.query("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY");
  const count = await client.query<{ total: string }>(`SELECT COUNT(*) AS total FROM threads t
    WHERE ($1 = '' OR t.search @@ websearch_to_tsquery('english',$1))
    AND ($2 = '' OR EXISTS (SELECT 1 FROM thread_tags x JOIN tags y ON y.id=x.tag_id WHERE x.thread_id=t.id AND y.name=$2))`,[q,tag]);
  const total = Number(count.rows[0]!.total);
  page = Math.min(page,Math.max(1,Math.ceil(total/pageSize)));
  const offset = (page - 1) * pageSize;''')
part=part.replace('const rows = await query<{','const { rows } = await client.query<{',1).replace('  const total = rows[0] ? Number(rows[0].total) : 0;','').replace('t.created_at DESC\n      LIMIT','t.created_at DESC, t.id ASC\n      LIMIT').replace('  res.json(payload);\n}));','  res.json(payload);\n  });\n}));')
s=s[:a]+part+s[b:]
s=s.replace('  const data = body as Partial<NewThread>;','''  if (!body || typeof body !== "object" || Array.isArray(body)) throw new ValidationError("Send a thread object.");
  const data = body as Partial<NewThread>;
  if (typeof data.title !== "string" || data.title.length > 200 || data.body !== undefined && (typeof data.body !== "string" || data.body.length > 20000) || !validId(data.authorId))
    throw new ValidationError("Use bounded title/body text and a valid author id.");
  if (data.tagNames !== undefined && (!Array.isArray(data.tagNames) || data.tagNames.length > 20 || !data.tagNames.every(tag => typeof tag === "string" && tag.trim().length > 0 && tag.length <= 40)))
    throw new ValidationError("Use at most 20 nonempty tag strings, each at most 40 characters.");''')
s+='\nfunction pageNumber(value: unknown, fallback: number, maximum: number) { const n=Number(value ?? fallback); return Number.isSafeInteger(n) && n>0 ? Math.min(n,maximum) : fallback; }\n';p.write_text(s,encoding='utf-8')
p=B/'31/server/src/index.ts';s=p.read_text(encoding='utf-8')
needle='''    const ok = await withTransaction(async (client) => {
      const { rowCount } = await client.query(
        "UPDATE tickets SET status'''
s=s.replace(needle,'''    const ok = await withTransaction(async (client) => {
      const current = await client.query<{ status: string }>("SELECT status FROM tickets WHERE id=$1 FOR UPDATE",[req.params.id]);
      if (!current.rows.length) return false;
      if (current.rows[0].status === status) return true;
      const { rowCount } = await client.query(
        "UPDATE tickets SET status''')
s=s.replace('    const assigneeId = req.body.assigneeId === null ? null : String(req.body.assigneeId);','''    const assigneeId = req.body?.assigneeId;
    if (assigneeId !== null && !validId(assigneeId)) throw new ValidationError("Choose a valid agent id or null.");''')
needle='''    const ok = await withTransaction(async (client) => {
      const { rowCount } = await client.query(
        "UPDATE tickets SET assignee_id'''
s=s.replace(needle,'''    const ok = await withTransaction(async (client) => {
      const current = await client.query<{ assignee_id: string | null }>("SELECT assignee_id FROM tickets WHERE id=$1 FOR UPDATE",[req.params.id]);
      if (!current.rows.length) return false;
      if (current.rows[0].assignee_id === assigneeId) return true;
      const { rowCount } = await client.query(
        "UPDATE tickets SET assignee_id''')
s=s.replace('  const data = body as Partial<NewTicket>;','''  if (!body || typeof body !== "object" || Array.isArray(body)) throw new ValidationError("Send a ticket object.");
  const data = body as Partial<NewTicket>;
  if (typeof data.subject !== "string" || data.subject.length > 200 || data.body !== undefined && (typeof data.body !== "string" || data.body.length > 20000) || data.assigneeId != null && !validId(data.assigneeId))
    throw new ValidationError("Use bounded subject/body text and a valid agent id.");
  if (data.labelIds !== undefined && (!Array.isArray(data.labelIds) || data.labelIds.length > 30 || !data.labelIds.every(validId)))
    throw new ValidationError("Use at most 30 valid label ids.");''');p.write_text(s,encoding='utf-8')
p=B/'34/server/src/index.ts';s=p.read_text(encoding='utf-8')
s=s.replace('  const tax = Math.round(subtotal * taxRate) / 100;','  const tax = Math.round(subtotal * taxRate) / 100;').replace('    total: subtotal + tax','    total: Math.round((subtotal + tax) * 100) / 100')
s=s.replace('  const data = body as Partial<NewInvoice>;','''  if (!body || typeof body !== "object" || Array.isArray(body)) throw new ValidationError("Send an invoice object.");
  const data = body as Partial<NewInvoice>;
  if (!validId(data.clientId)) throw new ValidationError("Choose a valid client id.");
  if (typeof data.issuedDate !== "string" || !/^\\d{4}-\\d{2}-\\d{2}$/.test(data.issuedDate) || Number.isNaN(Date.parse(data.issuedDate+"T00:00:00Z")) || new Date(data.issuedDate+"T00:00:00Z").toISOString().slice(0,10) !== data.issuedDate)
    throw new ValidationError("Use a real issue date in YYYY-MM-DD format.");
  if (!decimal(data.taxRate,100)) throw new ValidationError("Tax rate must be 0-100 with at most two decimal places.");''')
s=s.replace('if (items.length === 0)','if (items.length === 0 || items.length > 100)')
s=s.replace('    if (!item.description?.trim())','''    if (!item || typeof item !== "object" || Array.isArray(item) || typeof item.description !== "string" || item.description.length > 500) throw new ValidationError("Each line needs text of at most 500 characters.");
    if (!Number.isSafeInteger(Number(item.quantity)) || typeof item.quantity === "boolean" || Number(item.quantity) > 1000000 || !decimal(item.unitPrice,9999999999.99)) throw new ValidationError("Use whole quantities and prices with at most two decimal places.");
    if (!item.description?.trim())''')
s+='\nfunction decimal(value: unknown, maximum: number) { return (typeof value === "number" || typeof value === "string") && /^\\d+(?:\\.\\d{1,2})?$/.test(String(value)) && Number(value) <= maximum; }\n';p.write_text(s,encoding='utf-8')
for n in [31,33,34]:
 p=B/str(n)/'server/src/index.ts';s=p.read_text(encoding='utf-8');s=s.replace('app.use(express.json());','''app.use(express.json());
app.param("id",(_req,res,next,value) => { if (!validId(value)) return res.status(400).json({ error: "Use a valid record id." }); next(); });''')
 s=s.replace('  console.error(error);','''  if (["22P02","23503","23505","23514","22003"].includes((error as { code?: string }).code ?? "")) return res.status(400).json({ error: "Invalid reference or value." });
  console.error(error);''')
 s+='\nfunction validId(value: unknown): value is string { return typeof value === "string" && /^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$/i.test(value); }\n';p.write_text(s,encoding='utf-8')
print('Implemented repeat-safe ticket mutations, reliable forum pages and strict invoice validation.')
