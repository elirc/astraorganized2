from pathlib import Path
import json,shutil
B=Path(__file__).resolve().parent.parent;P=B/'stage/abcd8cc338ec'
rel='src/app/api/workflows/[id]/route.ts';f=P/rel
snap=P/'astraupskill/snapshots/workflow-route.ts.original.txt';snap.parent.mkdir(parents=True,exist_ok=True);assert not snap.exists();snap.write_bytes(f.read_bytes())
t=f.read_text();start=t.index('    const [updated] = await db',t.index('export async function PUT'));end=t.index('    return ok(updated);',start)
block=t[start:end].replace('await db','await tx').replace('return ok(null);','return null;')
block='\n'.join('  '+line if line else line for line in block.splitlines())
t=t[:start]+'    const updated = await db.transaction(async (tx) => {\n'+block+'\n      return updated;\n    });\n\n'+t[end:]
f.write_text(t,encoding='utf-8')
T=P/'tests';(T/'helpers').mkdir(parents=True,exist_ok=True)
shutil.copyfile(B/'batch-crud-upskill-20260921/test-tools/load-typescript.mjs',T/'helpers/load-typescript.mjs')
(T/'runtime-workflow-transaction.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { loadTypeScript } from './helpers/load-typescript.mjs';
const root = fileURLToPath(new URL('..', import.meta.url));
const step = { stepType: 'delay', name: 'Wait', position: 0, config: { ms: 100 }, inputMapping: {}, timeoutMs: 1000, retryConfig: {}, onFailure: 'stop', nextStepId: null };
async function fixture(options = {}) {
  const calls = []; let active = false, updateFields, condition, inserted;
  const workflows = { id: 'workflow.id', tenantId: 'workflow.tenantId', version: 'workflow.version' }, workflowSteps = { workflowId: 'step.workflowId' };
  function record(name, table) { assert.equal(active, true, `${name} outside transaction`); calls.push(name); }
  const tx = {
    update(table) { record('update', table); assert.equal(table, workflows); return { set(fields) { updateFields = fields; return { where(value) { condition = value; return { returning: async () => options.missing ? [] : [{ id: 'workflow-1', tenantId: 'tenant-1', name: fields.name, version: 2 }] }; } }; } }; },
    delete(table) { record('delete', table); assert.equal(table, workflowSteps); return { where: async value => { assert.deepEqual(value, ['eq', 'step.workflowId', 'workflow-1']); if (options.deleteError) throw options.deleteError; } }; },
    insert(table) { record('insert', table); assert.equal(table, workflowSteps); return { values: async values => { inserted = values; if (options.insertError) throw options.insertError; } }; }
  };
  const db = { transaction: async callback => { calls.push('begin'); active = true; try { const result = await callback(tx); calls.push('commit'); return result; } catch(error) { calls.push('reject'); throw error; } finally { active = false; } } };
  const route = await loadTypeScript('src/app/api/workflows/[id]/route.ts', { root, globals: { Error }, stubs: {
    'drizzle-orm': { eq: (a,b) => ['eq',a,b], and: (...args) => ['and',...args], asc: x => x, sql: (parts,...values) => ({ text: parts.join('?'), values }) },
    'next/server': { NextRequest: class {}, NextResponse: { json: (body, init) => Response.json(body, init) } },
    '@/lib/db': { db }, '@/lib/db/schema': { workflows, workflowSteps },
    '@/lib/auth/tenant': { requireTenantContext: async () => ({ tenantId: 'tenant-1' }) },
    '@/lib/validators/workflow.schema': { workflowUpdateSchema: { parse: value => { if(options.parseError) throw options.parseError; return value; } } }
  }});
  return { calls, fields: () => updateFields, condition: () => condition, inserted: () => inserted,
    run: payload => route.PUT({ json: async () => payload }, { params: { id: 'workflow-1' } }) };
}
test('parent update and step replacement use one transaction in order', async () => {
  const f = await fixture(); const response = await f.run({ name: 'Revised', steps: [step] });
  assert.equal(response.status, 200); assert.equal((await response.json()).data.name, 'Revised');
  assert.deepEqual(f.calls, ['begin','update','delete','insert','commit']);
  assert.deepEqual(f.condition(), ['and',['eq','workflow.id','workflow-1'],['eq','workflow.tenantId','tenant-1']]);
  assert.equal(f.fields().version.text, '? + 1'); assert.deepEqual(f.fields().version.values, ['workflow.version']);
  assert.equal(f.inserted().length, 1); assert.equal(f.inserted()[0].workflowId, 'workflow-1');
  assert.equal(f.inserted()[0].name, 'Wait'); assert.equal(f.inserted()[0].conditionBranches, null);
});
test('insert failure rejects transaction callback before API error response', async () => {
  const f = await fixture({ insertError: new Error('step insert failed') }); const response = await f.run({ steps: [step] });
  assert.equal(response.status, 500); assert.equal((await response.json()).error.message, 'step insert failed');
  assert.deepEqual(f.calls, ['begin','update','delete','insert','reject']);
});
test('delete failure prevents insert and commit', async () => {
  const f = await fixture({ deleteError: new Error('step delete failed') }); const response = await f.run({ steps: [step] });
  assert.equal(response.status, 500); assert.deepEqual(f.calls, ['begin','update','delete','reject']);
});
test('omitted steps preserve children', async () => {
  const f = await fixture(); await f.run({ name: 'Rename' }); assert.deepEqual(f.calls, ['begin','update','commit']);
});
test('empty steps delete children without insert', async () => {
  const f = await fixture(); await f.run({ steps: [] }); assert.deepEqual(f.calls, ['begin','update','delete','commit']);
});
test('tenant-scoped missing parent returns null without touching children', async () => {
  const f = await fixture({ missing: true }); const response = await f.run({ steps: [step] });
  assert.equal((await response.json()).data, null); assert.deepEqual(f.calls, ['begin','update','commit']);
  assert.deepEqual(f.condition(), ['and',['eq','workflow.id','workflow-1'],['eq','workflow.tenantId','tenant-1']]);
});
test('payload rejection happens before starting transaction', async () => {
  const f = await fixture({ parseError: new Error('invalid payload') }); const response = await f.run({});
  assert.equal(response.status, 500); assert.deepEqual(f.calls, []);
});
''',encoding='utf-8')
j={'id':'abcd8cc338ec','project':'_Organized Desktop/04 JavaScript Training/jstrain2','summary':['Update workflow metadata, increment version and replace steps within one Drizzle transaction.','Teach aggregate boundaries, omitted-versus-empty child lists, and error propagation before response conversion.'],'changedFiles':[rel,'astraupskill/snapshots/workflow-route.ts.original.txt','tests/runtime-workflow-transaction.test.mjs','tests/helpers/load-typescript.mjs'],'checks':{'format':'json','resultsFile':'checks/abcd8cc338ec/results-crud-b03.json'},'limits':['Tests execute the actual PUT route and API response/error helpers with explicit Drizzle, auth, schema and validation doubles.','The transaction double asserts call scope, order and rejection; it does not prove PostgreSQL rollback, isolation, SQL compilation or real Zod validation.','Native Next.js, database and browser suites were not run. Existing step-id references and authorization policy are unchanged.']}
(B/'specs/abcd8cc338ec.json').write_text(json.dumps(j,indent=2))
