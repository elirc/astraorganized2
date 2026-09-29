from pathlib import Path
import json,re
B=Path('astrafinalplan/implementation/batch04')
p=B/'stage/75/server/src/validation.js';s=p.read_text();s=s.replace("const optionalDateSchema = z", "const realDate = value => /^\\d{4}-\\d{2}-\\d{2}$/.test(value) && Number.isFinite(Date.parse(value)) && new Date(value).toISOString().slice(0,10) === value;\n\nconst optionalDateSchema = z");s=s.replace('.regex(/^\\d{4}-\\d{2}-\\d{2}$/)',".refine(realDate, 'Use a real calendar date')");s=s.replace("transform(() => undefined)","transform(() => null)");s=s.replace("z.coerce.number().int().nonnegative().optional().or(z.literal('').transform(() => null))","z.preprocess(value => value === '' || value === null ? null : value, z.coerce.number().int().nonnegative().nullable().optional())");s=s.replace('value.salary_min === undefined || value.salary_max === undefined','value.salary_min == null || value.salary_max == null');p.write_text(s)
p=B/'stage/75/server/src/routes/applications.js';s=p.read_text().replace('!Number.isInteger(id) || id <= 0',"!/^\\d+$/.test(req.params.id) || !Number.isSafeInteger(id) || id <= 0").replace('ORDER BY ${sort_by} ${sort_order.toUpperCase()}','ORDER BY ${sort_by} ${sort_order.toUpperCase()}, id ${sort_order.toUpperCase()}');s=s.replace('return res.status(400).json({ message: `Application is already ${nextStatus}` });','return res.json({ item: existing });');p.write_text(s)
p=B/'stage/75/server/src/db.js';s=p.read_text().replace("const dbDir = path.join(__dirname, '..', 'data');","const dbDir = process.env.JOB_TRACK_DATA_DIR || path.join(__dirname, '..', 'data');");p.write_text(s)
p=B/'stage/75/server/src/server.js';s=p.read_text().replace('app.listen(PORT,','if (require.main === module) app.listen(PORT,');s+='\nmodule.exports = {app};\n';p.write_text(s)
p=B/'stage/75/server/package.json';d=json.loads(p.read_text());d['scripts']['test']='node --test ../test/*.test.js';p.write_text(json.dumps(d,indent=2)+'\n')
# Recipe edits reject malformed nested values before any rows or search entries change.
p=B/'stage/72/server/index.ts';s=p.read_text().replace("import { fileURLToPath }", "import { fileURLToPath, pathToFileURL }").replace('const app = express();','export const app = express();').replace('const isDate = (s: string) => /^\\d{4}-\\d{2}-\\d{2}$/.test(s);','const isDate = (s: string) => /^\\d{4}-\\d{2}-\\d{2}$/.test(s) && Number.isFinite(Date.parse(s)) && new Date(s).toISOString().slice(0,10) === s;');s=s.replace('      const out = fn(req, res);','''      for (const [key,value] of Object.entries(req.params)) {
        if (key.toLowerCase().endsWith('id') && (typeof value !== 'string' || !/^\\d+$/.test(value) || !Number.isSafeInteger(Number(value)) || Number(value) < 1)) throw new InputError('Use a positive whole-number id');
      }
      if (['POST','PATCH'].includes(req.method) && !req.path.endsWith('/photos')) validatePayload(req.body);
      const out = fn(req, res);''').replace('res.status(500).json({ error: String((e as Error)?.message ?? e) })','res.status(e instanceof InputError ? 400 : 500).json({ error: e instanceof InputError ? e.message : "Request failed" })');s=s.replace('app.listen(PORT,','if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) app.listen(PORT,')
s+='''
class InputError extends Error {}
function validatePayload(body: unknown) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) throw new InputError('Send a JSON object');
  const b=body as Record<string,unknown>;
  for(const key of ['name','title','notes','source_name','source_url','yield_unit']) {
    if(b[key]===undefined)continue;
    if(typeof b[key]!=='string' || (b[key] as string).length>20000 || (['name','title'].includes(key) && !(b[key] as string).trim()))throw new InputError(`${key} must contain valid text`);
  }
  if(b.tags!==undefined && (!Array.isArray(b.tags)||b.tags.length>50||b.tags.some(t=>typeof t!=='string'||t.length>100)))throw new InputError('Tags must be at most 50 short strings');
  if(b.yield_qty!==undefined && (typeof b.yield_qty!=='number'||!Number.isFinite(b.yield_qty)||b.yield_qty<=0))throw new InputError('Yield must be a positive number');
  if(b.ingredients!==undefined) {
    if(!Array.isArray(b.ingredients)||b.ingredients.length>300)throw new InputError('Ingredients must be an array of at most 300 rows');
    for(const row of b.ingredients) {
      if(!row||typeof row!=='object'||Array.isArray(row))throw new InputError('Invalid ingredient row');
      for(const key of ['item','unit','note','section'])if(row[key]!==undefined&&typeof row[key]!=='string')throw new InputError(`Ingredient ${key} must be text`);
      if(row.qty!==undefined&&row.qty!==null&&row.qty!==''&&(typeof row.qty!=='number'||!Number.isFinite(row.qty)||row.qty<0))throw new InputError('Ingredient quantity must be nonnegative or blank');
    }
  }
  if(b.steps!==undefined && (!Array.isArray(b.steps)||b.steps.length>300||b.steps.some(row=>typeof row!=='string'&&(!row||typeof row.text!=='string'))))throw new InputError('Steps must contain text');
}
''';p.write_text(s)
p=B/'stage/72/package.json';d=json.loads(p.read_text());d['scripts']['test']='tsx --test test/*.test.ts';p.write_text(json.dumps(d,indent=2)+'\n')
