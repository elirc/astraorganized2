from pathlib import Path
B=Path('astrafinalplan/implementation/batch03/stage')
p=B/'28/server/src/index.ts';s=p.read_text(encoding='utf-8');a=s.index('    const { id } = req.params;',s.index('app.patch("/api/nodes/:id/move"'));b=s.index('\n  } catch',a)
s=s[:a]+'''    const id = req.params.id;
    const newParentId = req.body?.newParentId;
    if (newParentId !== null && !validId(newParentId)) throw new ValidationError("Choose a valid parent id or null for a root.");
    const client = await pool.connect();
    try {
      await client.query("BEGIN");
      // All structural writers conflict with this lock; readers can continue.
      await client.query("LOCK TABLE nodes IN SHARE ROW EXCLUSIVE MODE");
      const node = await client.query("SELECT id FROM nodes WHERE id=$1",[id]);
      if (!node.rows.length) { await client.query("ROLLBACK"); return res.status(404).json({ error: "Node not found." }); }
      if (newParentId !== null) {
        const parent = await client.query("SELECT id FROM nodes WHERE id=$1",[newParentId]);
        if (!parent.rows.length) throw new ValidationError("Parent does not exist.");
        const descendants = await client.query(`WITH RECURSIVE sub AS (
          SELECT id FROM nodes WHERE id=$1 UNION SELECT n.id FROM nodes n JOIN sub s ON n.parent_id=s.id
        ) SELECT id FROM sub WHERE id=$2`,[id,newParentId]);
        if (descendants.rows.length) throw new ValidationError("Cannot move a node beneath itself or a descendant.");
      }
      await client.query("UPDATE nodes SET parent_id=$2 WHERE id=$1",[id,newParentId]);
      await client.query("COMMIT"); res.json({ ok: true });
    } catch (error) { await client.query("ROLLBACK"); throw error; }
    finally { client.release(); }'''+s[b:]
s=s.replace('  const data = body as Partial<NewNode>;','''  if (!body || typeof body !== "object" || Array.isArray(body)) throw new ValidationError("Send a node object.");
  const data = body as Partial<NewNode>;
  if (typeof data.name !== "string" || data.name.length > 200 || data.title !== undefined && (typeof data.title !== "string" || data.title.length > 200) || data.parentId != null && !validId(data.parentId))
    throw new ValidationError("Use bounded names/titles and a valid parent id.");''')
s=s.replace('    const name = String(req.body.name ?? "").trim();','''    if (typeof req.body?.name !== "string" || req.body.name.length > 200 || req.body.title !== undefined && (typeof req.body.title !== "string" || req.body.title.length > 200))
      throw new ValidationError("Use bounded text for name and title.");
    const name = req.body.name.trim();''')
s=s.replace('app.use(express.json());','''app.use(express.json());
app.param("id",(_req,res,next,value) => { if (!validId(value)) return res.status(400).json({ error: "Use a valid node id." }); next(); });''')
s+='\nfunction validId(value: unknown): value is string { return typeof value === "string" && /^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$/i.test(value); }\n';p.write_text(s,encoding='utf-8')
p=B/'30/server/src/index.ts';s=p.read_text(encoding='utf-8');a=s.index('    `SELECT to_char(day,');b=s.index('`,\n    [days]',a)
s=s[:a]+'''    `WITH calendar AS (
       SELECT generated::date AS day FROM generate_series(CURRENT_DATE - ($1::int - 1), CURRENT_DATE, interval '1 day') generated
     ), filled AS (
       SELECT c.day, COALESCE(m.views,0) AS views, COALESCE(m.carts,0) AS carts,
         COALESCE(m.orders,0) AS orders, COALESCE(m.revenue,0) AS revenue
       FROM calendar c LEFT JOIN daily_metrics m ON m.day=c.day
     )
     SELECT to_char(day,'YYYY-MM-DD') AS day, views, carts, orders, revenue,
       ROUND(AVG(revenue) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW),2) AS revenue_ma7,
       SUM(revenue) OVER (ORDER BY day) AS revenue_cumulative,
       revenue - LAG(revenue) OVER (ORDER BY day) AS revenue_delta
     FROM filled ORDER BY day'''+s[b:]
s=s.replace('WHERE day >= CURRENT_DATE - $1::int','WHERE day >= CURRENT_DATE - ($1::int - 1) AND day <= CURRENT_DATE')
s=s.replace('Math.min(20, Math.max(1, Number(req.query.limit) || 5))','Math.min(20, Math.max(1, Math.trunc(Number(req.query.limit)) || 5))')
s=s.replace('  const data = body as Partial<NewEvent>;','''  if (!body || typeof body !== "object" || Array.isArray(body)) throw new ValidationError("Send an event object.");
  const data = body as Partial<NewEvent>;
  if (typeof data.product !== "string" || data.product.length > 200) throw new ValidationError("Use a product name of at most 200 characters.");
  if (data.name === "purchase" && (typeof data.amount !== "number" && typeof data.amount !== "string" || String(data.amount).trim() === "")) throw new ValidationError("Purchase amount must be a number.");''')
s=s.replace('if (!(amount >= 0))','if (!Number.isFinite(amount) || amount < 0 || amount > 9999999999.99)');p.write_text(s,encoding='utf-8')
print('Implemented concurrent cycle prevention and gap-filled daily analytics.')
