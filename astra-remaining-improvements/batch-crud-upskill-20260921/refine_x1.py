from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/1754dbb384b1'
t=P/'bagel-intel-platform/tests/runtime-review-moderation.test.mjs';s=t.read_text()
s=s.replace('const calls = [];','const calls = [];\nlet existing=true;\nconst lookups=[];')
s=s.replace("if (sql.includes('SELECT id FROM reviews')) return { id: 'review-1' };","if (sql.includes('SELECT id FROM reviews')) {lookups.push(args);return existing?{ id: 'review-1' }:undefined;}")
s=s.replace(", '@/lib/utils': { clamp: (v) => v, createId: () => 'id', normalizePhone: (v) => v, normalizeWebsite: (v) => v, nowIso: () => '2026-01-01T00:00:00.000Z', slugify: (v) => v }",'')
s=s.replace("assert.equal(update.params.id, 'review-1');","assert.equal(update.params.id, 'review-1');assert.deepEqual(lookups[0],['u1','s1']);assert.equal(update.params.title,'Updated title');assert.equal(update.params.rating,5);assert.equal(update.params.visitDate,null);")
s+='''
test('new review uses visible insert default and author/shop identity',()=>{
 existing=false;calls.length=0;mod.upsertReview({userId:'u2',shopId:'s2',rating:4,title:'New',body:'A useful review',visitDate:'2026-01-02'});
 const insert=calls.find(c=>c.sql.includes('INSERT INTO reviews'));assert.ok(insert);assert.match(insert.sql,/@visitDate, 0, 0,/);assert.equal(insert.params.userId,'u2');assert.equal(insert.params.shopId,'s2');assert.equal(insert.params.visitDate,'2026-01-02');assert.match(insert.params.id,/^rev_/);assert.equal(calls.some(c=>c.sql.includes('UPDATE reviews')),false);
});
''';t.write_text(s,encoding='utf-8')
for p in (P/'astraupskill').glob('*.md'):
 s=p.read_text(encoding='utf-8').replace('Result: 1 test passed','Result: 2 tests passed')
 s+='\nThe extended lab also executes INSERT and checks visible initial state, supplied author/shop identity and visit date. Real utility functions generate identifiers and timestamps. Only SQLite, seed inputs and date-fns formatting/ranking helpers are adapted; ranking results remain unverified.\n'
 p.write_text(s,encoding='utf-8')
# Practice should pose questions separately from the answer chapter.
p=P/'astraupskill/05-PRACTICE.md';s=p.read_text();s=s.replace(' Answer: content fields change, `is_hidden` remains 1.','').replace(' Answer: the INSERT explicitly writes zero; this is independent of the UPDATE fix.','').replace(' Reject it. Moderation state is an administrator decision, not an author freshness signal.',' Explain which authority owns this field.').replace(' One author’s review is edited rather than duplicated for a shop, assuming the database and application enforce the intended invariant.',' State the database assumption required.');p.write_text(s,encoding='utf-8')
p=B/'specs/1754dbb384b1.json';s=json.loads(p.read_text(encoding='utf-8-sig'));s['changedFiles']=[x for x in s['changedFiles'] if '/evidence/' not in x];s['summary'][1]='Two actual-data-module runtime cases check content-only UPDATE and visible INSERT with author/shop identity.';p.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
P=B/'stage/482e93488b83'
for p in (P/'astraupskill').glob('*.md'):
 s=p.read_text().replace('three subtests','five subtests').replace('three passing subtests','five passing subtests').replace('Three cases','Five cases').replace('three executable cases','five executable cases')
 s=s.replace('external I/O and permission wiring','external I/O and unused framework imports').replace('repository and permission boundary double','repository boundary double and real permission helper')
 s=s.replace('database singleton, permission function, audit adapter, and `AppError` dependency','database singleton, audit adapter and unused NextResponse/zod exports; the real permission and AppError modules execute')
 p.write_text(s,encoding='utf-8')
