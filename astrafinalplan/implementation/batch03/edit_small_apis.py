from pathlib import Path
B=Path('astrafinalplan/implementation/batch03/stage')
common='''\nfunction isText(value, min = 0, max = 200) { return typeof value === "string" && value.trim().length >= min && value.length <= max; }
function whole(value, min, max) { return (typeof value === "number" || typeof value === "string" && value.trim() !== "") && Number.isSafeInteger(Number(value)) && Number(value) >= min && Number(value) <= max; }
function realDate(value) { return typeof value === "string" && /^\\d{4}-\\d{2}-\\d{2}$/.test(value) && !Number.isNaN(Date.parse(value+"T00:00:00Z")) && new Date(value+"T00:00:00Z").toISOString().slice(0,10) === value; }
'''
for n in [23,24,25,26,27,29,32]:
 p=B/str(n)/'server/server.js';s=p.read_text(encoding='utf-8')
 if n==23:
  s=s.replace('  const course = normalizeCourse(req.body);','''  if (!["code","title","instructor"].every(key => isText(req.body[key],1)) || !whole(req.body.capacity,1,100000) || !whole(req.body.enrolled,0,100000))
    return res.status(400).json({ error: "Use text fields and whole capacity/enrollment counts." });
  const course = normalizeCourse(req.body);
  if (!["Beginner","Intermediate","Advanced"].includes(course.level)) return res.status(400).json({ error: "Choose a valid level." });
  if (courses.some(existing => existing.id !== req.params.id && existing.code === course.code))
    return res.status(409).json({ error: "A course with this code already exists." });''')
 if n==24:
  s=s.replace('  const event = normalizeEvent(req.body);','''  if (!["name","location"].every(key => isText(req.body[key],1)) || !realDate(req.body.date) || !whole(req.body.capacity,1,100000) || !whole(req.body.registered,0,100000))
    return res.status(400).json({ error: "Use text, a real calendar date and whole capacity/registration counts." });
  const event = normalizeEvent(req.body);''')
 if n==25:
  s=s.replace('  const application = normalizeApplication(req.body);','''  if (!["company","role"].every(key => isText(req.body[key],1)) ||
      req.body.contact !== undefined && !isText(req.body.contact) || req.body.notes !== undefined && !isText(req.body.notes,0,10000) ||
      req.body.nextStepDate !== undefined && req.body.nextStepDate !== "" && !realDate(req.body.nextStepDate))
    return res.status(400).json({ error: "Use text fields and a real next-step date, or leave the date blank." });
  const application = normalizeApplication(req.body);''')
  s=s.replace('  res.json(result);','''  result.sort((a,b) => (a.nextStepDate || "9999-99-99").localeCompare(b.nextStepDate || "9999-99-99") || a.id.localeCompare(b.id));
  res.json(result);''',1)
 if n==26:
  s=s.replace('Math.max(1, Number(req.query.page) || 1)','whole(req.query.page,1,1000000) ? Number(req.query.page) : 1').replace('clamp(Number(req.query.pageSize) || 5, 1, 50)','whole(req.query.pageSize,1,1000000) ? Math.min(Number(req.query.pageSize),50) : 5')
  s=s.replace('  const { name, category, price, stock } = req.body;','''  const { name, category, price, stock } = req.body;
  if (!isText(name,2) || !isText(category,2) || !whole(stock,0,1000000000) ||
      !(typeof price === "number" || typeof price === "string" && price.trim() !== "") || !Number.isFinite(Number(price)) || Number(price) > 9999999999.99)
    return res.status(400).json({ error: "Use bounded names, a finite price and a whole stock count." });''')
  s=s.replace('compare(a, b, sort, dir));','compare(a, b, sort, dir) || a.id.localeCompare(b.id));')
 if n==27:
  s=s.replace('  const recipe = normalizeRecipe(req.body);','''  if (!isText(req.body.name,3) || !whole(req.body.cookTime,1,10080) || !whole(req.body.servings,1,1000) ||
      !Array.isArray(req.body.ingredients) || req.body.ingredients.length > 100 || !req.body.ingredients.every(x => isText(x,1,500)) ||
      req.body.category !== undefined && !isText(req.body.category,1) || req.body.notes !== undefined && !isText(req.body.notes,0,10000))
    return res.status(400).json({ error: "Use whole cooking minutes/servings and 1-100 nonempty ingredient strings." });
  const recipe = normalizeRecipe(req.body);''')
  s=s.replace('input.ingredients.map((item) => String(item).trim()).filter(Boolean)','input.ingredients.map(item => item.trim()).filter((item,index,items) => items.findIndex(other => other.toLowerCase() === item.toLowerCase()) === index)')
 if n==29:
  s=s.replace('  const { title, author, body } = req.body;','''  const { title, author, body } = req.body;
  if (!isText(title,3) || !isText(author,2) || !isText(body,1,20000)) return res.status(400).json({ error: "Use bounded text for title, author and body." });''')
  s=s.replace('  const { author, text } = req.body;','''  const { author, text } = req.body;
  if (!isText(author,2) || !isText(text,1,2000)) return res.status(400).json({ error: "Use an author name and comment text of at most 2000 characters." });''')
 if n==32:
  s=s.replace('const { status = "all", search = "" } = req.query;','''const { status = "all", search = "", priority = "all" } = req.query;
  if (typeof search !== "string" || !["all","Low","Medium","High","Critical"].includes(priority))
    return res.status(400).json({ error: "Use a text search and a valid priority filter." });''').replace('repository.list({ status, search })','repository.list({ status, search, priority })').replace('list({ status, search })','list({ status, search, priority })').replace('return matchesStatus && text.includes(search.toLowerCase());','return matchesStatus && (priority === "all" || issue.priority === priority) && text.includes(search.toLowerCase());')
  s=s.replace('  const { title, status, priority, assignee } = req.body;','''  const { title, status, priority, assignee } = req.body;
  if (!isText(title,3) || !isText(assignee,2) || req.body.description !== undefined && !isText(req.body.description,0,10000))
    return res.status(400).json({ error: "Use bounded text for title, assignee and description." });''')
 p.write_text(s+common,encoding='utf-8')
p=B/'32/client/src/App.jsx';s=p.read_text(encoding='utf-8').replace('useState({ status: "all", search: "" })','useState({ status: "all", search: "", priority: "all" })');s=s.replace('<input placeholder="Search issues"','<input aria-label="Search issues" placeholder="Search issues"');needle='''          <div className="toolbar">''';s=s.replace(needle,needle+'''
            <select aria-label="Filter priority" value={filters.priority} onChange={event => setFilters({ ...filters, priority: event.target.value })}>
              <option value="all">All priorities</option>
              {["Low","Medium","High","Critical"].map(priority => <option key={priority}>{priority}</option>)}
            </select>''');p.write_text(s,encoding='utf-8')
print('Implemented seven distinct API improvements: course codes, event capacity/dates, follow-up ordering, catalog paging, ingredients, comment validation and issue priority filtering.')
