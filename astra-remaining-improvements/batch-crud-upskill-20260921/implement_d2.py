from pathlib import Path
import json,shutil
B=Path(__file__).resolve().parent.parent;P=B/'stage/3c142f8c1521'
assert not list(P.rglob('AGENTS.md'))
rel='src/app/api/reviews/route.ts';f=P/rel
snap=P/'astraupskill/snapshots/reviews-route.ts.original.txt';snap.parent.mkdir(parents=True,exist_ok=True);assert not snap.exists();snap.write_bytes(f.read_bytes())
t=f.read_text();old='  await db\n    .update(reviews)\n    .set({ sourceMetadata: { ...sourceMetadata, template, rules: rules ? { ...rules } : undefined } })'
assert old in t
t=t.replace(old,'''  // Snapshot the rules accepted for this review, after any rules write succeeds.
  const reviewMetadata = {
    ...sourceMetadata,
    template,
    rules: parsedRules?.success ? parsedRules.data : rules ? { ...rules } : undefined
  };

  await db
    .update(reviews)
    .set({ sourceMetadata: reviewMetadata })''')
t=t.replace('sourceMetadata: row.sourceMetadata,','sourceMetadata: reviewMetadata,')
f.write_text(t,encoding='utf-8')
T=P/'tests';(T/'helpers').mkdir(parents=True,exist_ok=True)
shutil.copyfile(B/'batch-crud-upskill-20260921/test-tools/load-typescript.mjs',T/'helpers/load-typescript.mjs')
(T/'runtime-review-metadata.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { loadTypeScript } from './helpers/load-typescript.mjs';
const root = fileURLToPath(new URL('..', import.meta.url));
const oldRules = { id: 'rules-1', projectId: 'project-1', language: 'JavaScript', framework: 'Old', preferredPatterns: ['old'], ignorePatterns: [] };
const newRules = { language: 'TypeScript', framework: 'Next', preferredPatterns: ['new'], ignorePatterns: ['generated'] };
async function fixture(options = {}) {
  const tables = { projects: { id: 'project.id' }, promptTemplates: { id: 'template.id', projectId: 'template.projectId', isActive: 'template.isActive' }, reviews: { id: 'review.id', sourceMetadata: 'review.sourceMetadata' }, projectRules: { projectId: 'rules.projectId' } };
  const calls = []; let storedMetadata, ruleWrite;
  const db = { query: {
    projects: { findFirst: async () => options.missingProject ? undefined : { id: 'project-1' } },
    projectRules: { findFirst: async () => options.noRules ? undefined : oldRules },
    promptTemplates: { findFirst: async () => ({ systemPrompt: 'Review carefully' }) }
  }, insert(table) { return { values(data) {
    if (table === tables.reviews) { calls.push('insert-review'); return { returning: async () => [{ id: 'review-1', sourceMetadata: data.sourceMetadata }] }; }
    assert.equal(table, tables.projectRules); calls.push('insert-rules'); ruleWrite = data;
    return options.rulesError ? Promise.reject(options.rulesError) : Promise.resolve();
  } }; }, update(table) { return { set(data) { return { where: async condition => {
    if (table === tables.projectRules) { calls.push('update-rules'); ruleWrite = data; if(options.rulesError) throw options.rulesError; }
    else { assert.equal(table,tables.reviews); calls.push('update-metadata'); storedMetadata=data.sourceMetadata; assert.deepEqual(condition,['eq','review.id','review-1']); }
  } }; } }; } };
  const route = await loadTypeScript('src/app/api/reviews/route.ts', { root, stubs: {
    'drizzle-orm': { eq: (a,b) => ['eq',a,b], and: (...a) => a, desc: x=>x, gte: ()=>{}, lte: ()=>{}, sql: ()=>{} },
    'next/server': { NextResponse: { json: (data,init) => Response.json(data,init) } },
    '@/lib/db/client': { db }, '@/lib/db/schema': tables,
    '@/lib/validation/schemas': { reviewSourceSchema: { safeParse: data => options.invalid ? { success:false,error:{issues:['invalid']} } : {success:true,data} }, projectRuleSchema: { safeParse: data => ({success:true,data}) } },
    '@/lib/review/ingest': { normalizeReviewSource: async () => 'normalized diff' }
  }});
  return { calls, stored: () => storedMetadata, rules: () => ruleWrite,
    run: input => route.POST({ json: async () => ({ projectId: 'project-1', inputType: 'diff', diff: 'diff', ...input }) }) };
}
const plain = value => JSON.parse(JSON.stringify(value));
test('updated rules are snapshotted and returned instead of old rules', async () => {
  const f = await fixture(); const body = await (await f.run({rules:newRules})).json();
  assert.deepEqual(body.sourceMetadata,plain(f.stored())); assert.deepEqual(body.sourceMetadata.rules,newRules);
  assert.deepEqual(plain(f.rules()),newRules); assert.equal(body.sourceMetadata.template,'Review carefully');
  assert.deepEqual(f.calls,['insert-review','update-rules','update-metadata']); assert.equal(oldRules.language,'JavaScript');
});
test('newly created project rules are included in metadata', async () => {
  const f = await fixture({noRules:true}); const body = await (await f.run({rules:newRules})).json();
  assert.deepEqual(body.sourceMetadata.rules,newRules); assert.deepEqual(body.sourceMetadata,plain(f.stored()));
  assert.equal(f.rules().projectId,'project-1'); assert.deepEqual(f.calls,['insert-review','insert-rules','update-metadata']);
});
test('omitted rules retain existing project snapshot without a rules write', async () => {
  const f = await fixture(); const body = await (await f.run({})).json();
  assert.deepEqual(body.sourceMetadata.rules,oldRules); assert.deepEqual(body.sourceMetadata,plain(f.stored()));
  assert.deepEqual(f.calls,['insert-review','update-metadata']);
});
test('no existing or submitted rules leaves rules absent after JSON serialization', async () => {
  const f = await fixture({noRules:true}); const body = await (await f.run({})).json();
  assert.equal(Object.hasOwn(body.sourceMetadata,'rules'),false); assert.deepEqual(body.sourceMetadata,plain(f.stored()));
});
test('rules persistence failure escapes before metadata update or success response', async () => {
  const sentinel=new Error('rules unavailable'), f=await fixture({rulesError:sentinel});
  await assert.rejects(f.run({rules:newRules}),error=>error===sentinel);
  assert.deepEqual(f.calls,['insert-review','update-rules']); assert.equal(f.stored(),undefined);
});
test('missing project and invalid source do not insert a review', async () => {
  for (const [options,status] of [[{missingProject:true},404],[{invalid:true},400]]) {
    const f=await fixture(options); assert.equal((await f.run({})).status,status); assert.deepEqual(f.calls,[]);
  }
});
''',encoding='utf-8')
j={'id':'3c142f8c1521','project':'_Organized Desktop/05 Numbered Experiments/D2','summary':['Snapshot newly accepted project rules in review metadata instead of stale pre-update rules.','Return the same finalized metadata written to the review, including its template and effective rules.'],'changedFiles':[rel,'astraupskill/snapshots/reviews-route.ts.original.txt','tests/runtime-review-metadata.test.mjs','tests/helpers/load-typescript.mjs'],'checks':{'format':'json','resultsFile':'checks/3c142f8c1521/results-crud-b03.json'},'limits':['Tests execute the actual POST route using explicit ORM, Zod parser, ingestion and NextResponse adapter doubles.','No PostgreSQL, GitHub ingestion, native Next.js or real Zod validation was executed.','The existing review creation and rules writes are separate operations; this bounded metadata correction does not add atomic transactions or prevent an incomplete pending review on a later failure.']}
(B/'specs/3c142f8c1521.json').write_text(json.dumps(j,indent=2))
