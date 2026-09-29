from pathlib import Path
import json,re
B=Path('astrafinalplan/implementation/batch03');R=B/'stage';spec=[]
jsids=[36,37,38,39,40,42,45,46,48]
for n in jsids:
 p=R/str(n)/'server/server.js';s=p.read_text(encoding='utf-8');route=re.search(r'app.get\("([^\"]+)"',s)[1];statuses=json.loads(re.search(r'const STATUSES = (\[.*?\]);',s)[1]);categories=json.loads(re.search(r'const CATEGORIES = (\[.*?\]);',s)[1]);spec.append({'stage':str(n),'route':route,'statuses':statuses,'categories':categories,'purpose':(R/str(n)/'README.md').read_text(encoding='utf-8').splitlines()[2]})
 s=s.replace('function validateItem(req, res, next) {','''function validateItem(req, res, next) {
  const body = req.body;
  if (["title","owner"].some(key => typeof body[key] !== "string" || body[key].trim().length > 200) ||
      ["notes","dueDate","priority","category","status"].some(key => body[key] !== undefined && typeof body[key] !== "string"))
    return res.status(400).json({ error: "Use text for record fields; title and owner allow at most 200 characters." });
  if (body.amount !== undefined && (typeof body.amount !== "number" && typeof body.amount !== "string" || String(body.amount).trim() === ""))
    return res.status(400).json({ error: "Amount must be a number." });
  if (body.dueDate && !validDate(body.dueDate)) return res.status(400).json({ error: "Use a real date in YYYY-MM-DD format." });
  if (body.notes?.length > 10000 || body.priority && !["Low","Medium","High","Critical"].includes(body.priority))
    return res.status(400).json({ error: "Choose a valid priority and keep notes under 10000 characters." });''')
 s=s.replace('const page = Math.max(1, Number(query.page) || 1);','const page = pageNumber(query.page, 1, 1000000);').replace('const pageSize = Math.min(25, Math.max(1, Number(query.pageSize) || 6));','const pageSize = pageNumber(query.pageSize, 6, 25);')
 s=s.replace('compareValues(a[sort], b[sort], dir)','compareValues(a[sort], b[sort], dir) || a.id.localeCompare(b.id)').replace('const start = (page - 1) * pageSize;','page = Math.min(page, totalPages);\n      const start = (page - 1) * pageSize;')
 old='setStatus(id, status) { const existing = this.find(id); if (!existing) return null; return this.update(id, { ...existing, status }); },'
 assert old in s
 s=s.replace(old,'''setStatus(id, status) {
      const existing = this.find(id); if (!existing) return null;
      if (existing.status === status) return existing;
      const updated = { ...existing, status, updatedAt: now() };
      const entry = activityEntry(id, "status", "Changed status from " + existing.status + " to " + status);
      items = items.map(item => item.id === id ? updated : item); activity.unshift(entry);
      return updated;
    },''')
 s=s.replace('const status = String(req.body.status || "");','const status = req.body.status;')
 s=s.replace('  const entry = repository.addActivity(req.params.id, req.body);','''  if (typeof req.body.body !== "string" || !req.body.body.trim() || req.body.body.length > 2000 ||
      req.body.kind !== undefined && (typeof req.body.kind !== "string" || !req.body.kind.trim() || req.body.kind.length > 40))
    return res.status(400).json({ error: "Activity needs text of 1-2000 characters and an optional short kind." });
  const entry = repository.addActivity(req.params.id, req.body);''')
 s+='''\nfunction validDate(value) {
  return typeof value === "string" && /^\\d{4}-\\d{2}-\\d{2}$/.test(value) &&
    !Number.isNaN(Date.parse(value + "T00:00:00Z")) && new Date(value + "T00:00:00Z").toISOString().slice(0,10) === value;
}
function pageNumber(value, fallback, maximum) {
  const number = Number(value ?? fallback);
  return Number.isSafeInteger(number) && number > 0 ? Math.min(number,maximum) : fallback;
}
'''
 p.write_text(s,encoding='utf-8')
(B/'memory-domain-specs.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
print('Improved nine in-memory domain apps: dates/types, repeat-safe status history and stable bounded pagination.')
