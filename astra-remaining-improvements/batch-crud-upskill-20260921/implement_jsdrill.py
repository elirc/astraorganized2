from pathlib import Path
import json,shutil
B=Path(__file__).resolve().parent.parent;P=B/'stage/612cdbaa5aa0'
assert not list(P.rglob('AGENTS.md'))
rels=['src/lib/db/schema.ts','src/lib/db/seed.ts']
for rel in rels:
    f=P/rel;snap=P/'astraupskill/snapshots'/rel;snap.parent.mkdir(parents=True,exist_ok=True);assert not snap.exists();snap.write_bytes(f.read_bytes())
f=P/rels[0];t=f.read_text();t=t.replace('real, primaryKey }','real, primaryKey, uniqueIndex }')
start=t.index('export const userCards =');end=t.index('// ─── User Tier Progress',start);block=t[start:end]
assert block.count('});')==1
block=block.replace('});','}, (table) => [uniqueIndex("user_cards_user_problem_unique").on(table.userId, table.problemId)]);')
f.write_text(t[:start]+block+t[end:],encoding='utf-8')
f=P/rels[1];t=f.read_text();anchor='    CREATE TABLE IF NOT EXISTS user_tier_progress (';assert t.count(anchor)==1
t=t.replace(anchor,'    CREATE UNIQUE INDEX IF NOT EXISTS user_cards_user_problem_unique\n      ON user_cards(user_id, problem_id);\n\n'+anchor)
f.write_text(t,encoding='utf-8')
T=P/'tests';T.mkdir(exist_ok=True)
(T/'user-card-constraint.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
const seed = readFileSync(new URL('../src/lib/db/seed.ts', import.meta.url), 'utf8');
const match = seed.match(/sqlite\\.exec\\(`([\\s\\S]*?)`\\);/);
assert.ok(match, 'seed DDL block must remain discoverable');
const ddl = match[1]; assert.equal(ddl.includes('$' + '{'), false, 'DDL must be static SQL');
const indexSQL = 'CREATE UNIQUE INDEX IF NOT EXISTS user_cards_user_problem_unique\\n      ON user_cards(user_id, problem_id);';
assert.ok(ddl.includes(indexSQL));
function fixture(t, sql = ddl) {
  const db = new DatabaseSync(':memory:'); t.after(() => db.close());
  db.exec('PRAGMA foreign_keys=ON'); db.exec(sql);
  db.exec("INSERT INTO categories(id,name) VALUES ('cat','CRUD'); INSERT INTO users(id,name,email,created_at) VALUES ('u1','One','one@example.test','2026-09-21'),('u2','Two','two@example.test','2026-09-21');");
  const insert = db.prepare('INSERT INTO problems(id,title,description,starter_code,category_id,created_at,updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)');
  for(const id of ['p1','p2']) insert.run(id,id,'Practice','','cat','2026-09-21','2026-09-21');
  return { db, card: (id,user='u1',problem='p1') => db.prepare('INSERT INTO user_cards(id,user_id,problem_id,due) VALUES (?,?,?,?)').run(id,user,problem,'2026-09-22'),
    count: () => db.prepare('SELECT count(*) AS n FROM user_cards').get().n };
}
test('different card ids cannot duplicate one user-problem pair', t => {
  const f=fixture(t); f.card('a'); assert.throws(()=>f.card('b'),/UNIQUE constraint failed: user_cards.user_id, user_cards.problem_id/); assert.equal(f.count(),1);
});
test('one user may own cards for different problems', t => {
  const f=fixture(t); f.card('a'); f.card('b','u1','p2'); assert.equal(f.count(),2);
});
test('different users may review the same problem', t => {
  const f=fixture(t); f.card('a'); f.card('b','u2','p1'); assert.equal(f.count(),2);
});
test('reapplying seed DDL preserves valid cards and the unique index', t => {
  const f=fixture(t); f.card('a'); f.db.exec(ddl); assert.equal(f.count(),1);
  const index=f.db.prepare("PRAGMA index_list('user_cards')").all().find(row=>row.name==='user_cards_user_problem_unique'); assert.equal(index.unique,1);
  assert.throws(()=>f.card('b'),/UNIQUE constraint failed/);
});
test('legacy duplicates reject index creation without deleting either card', t => {
  const f=fixture(t,ddl.replace(indexSQL,'')); f.card('a'); f.card('b');
  assert.throws(()=>f.db.exec(ddl),/UNIQUE constraint failed/); assert.equal(f.count(),2);
  assert.deepEqual(f.db.prepare('SELECT id FROM user_cards ORDER BY id').all().map(row=>row.id),['a','b']);
});
test('updating a card into an occupied pair also fails without changing its pair', t => {
  const f=fixture(t); f.card('a'); f.card('b','u1','p2');
  assert.throws(()=>f.db.prepare('UPDATE user_cards SET problem_id=? WHERE id=?').run('p1','b'),/UNIQUE constraint failed/);
  assert.equal(f.db.prepare('SELECT problem_id FROM user_cards WHERE id=?').get('b').problem_id,'p2'); assert.equal(f.count(),2);
});
''',encoding='utf-8')
j={'id':'612cdbaa5aa0','project':'_Organized Desktop/04 JavaScript Training/jsdrill_sync_20260223_125137','summary':['Enforce the documented one-card-per-user-and-problem invariant with a composite unique index in the Drizzle schema and executable seed DDL.','Teach database identity, cross-user cardinality, constraint failures and nondestructive handling of legacy duplicate rows.'],'changedFiles':rels+['astraupskill/snapshots/'+r for r in rels]+['tests/user-card-constraint.test.mjs'],'checks':{'format':'json','resultsFile':'checks/612cdbaa5aa0/results-crud-b03.json'},'limits':['Tests execute the exact static SQL DDL extracted from the production seed in real in-memory SQLite through Node node:sqlite; the native better-sqlite3/Drizzle/Next.js stack was not run.','No existing project database was opened or migrated. Reapplying seed DDL creates the index on clean existing tables but fails if duplicate pairs already exist; rows are not automatically removed.','The attempts route remains unchanged: a racing duplicate insert may return its existing generic failure, and attempt/card/tier writes remain separate operations. This is a uniqueness constraint, not request idempotency or an atomic workflow.']}
(B/'specs/612cdbaa5aa0.json').write_text(json.dumps(j,indent=2))
