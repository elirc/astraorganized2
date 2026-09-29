from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
P=B/'stage/7b18281f562f'
(P/'tests/bulk-enroll-entry.ts').write_text('export { enrollmentService } from "../packages/application/src/services/enrollment-service";\nexport { AppError } from "../packages/application/src/errors";\n')
(P/'tests/runtime-bulk-enroll.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { loadTypeScript } from './helpers/load-typescript.mjs';
const root = fileURLToPath(new URL('..', import.meta.url));
const actor = { id: 'manager-1', role: 'SchoolManager' };
async function fixture() {
  const calls = [], successes = [];
  let outcomes = [];
  const module = await loadTypeScript('tests/bulk-enroll-entry.ts', { root, stubs: {
    '@agentic-edu/domain': { explainPermission: () => 'Denied', decideEnrollment() {}, decideWaitlistPromotion() {} },
    '@agentic-edu/db': { prisma: { $transaction: async () => {
      const index = calls.length; calls.push(index);
      const outcome = outcomes[index];
      if (outcome) throw outcome;
      successes.push(index);
      return { id: `enrollment-${index}`, status: 'Enrolled' };
    } } },
    '../context': { assertCan() {} },
    '../audit': { createAuditEvent: async () => {} },
    '../logging': { withServiceLogging: (_name, methods) => methods }
  }});
  return { ...module, calls, successes, set: values => { outcomes = values; },
    run: ids => module.enrollmentService.bulkEnroll(actor, { classSectionId: 'section-1', studentIds: ids, allowWaitlist: false }) };
}
test('four expected AppError codes become ordered student refusals', async () => {
  const f = await fixture();
  const codes = ['FORBIDDEN', 'VALIDATION_ERROR', 'NOT_FOUND', 'CONFLICT'];
  f.set(codes.map(code => new f.AppError(code, `reason-${code}`)));
  const result = await f.run(codes);
  assert.equal(result.length, 4);
  result.forEach((row, i) => { assert.equal(row.studentId, codes[i]); assert.equal(row.ok, false); assert.equal(row.reason, `reason-${codes[i]}`); });
  assert.equal(f.calls.length, 4);
});
test('unexpected first failure preserves identity and stops later work', async () => {
  const f = await fixture(), failure = new Error('database unavailable'); f.set([failure]);
  await assert.rejects(f.run(['a', 'b']), error => error === failure);
  assert.equal(f.calls.length, 1); assert.equal(f.successes.length, 0);
});
test('success refusal success retains input order and continues', async () => {
  const f = await fixture(); f.set([null, new f.AppError('CONFLICT', 'Section is full.'), null]);
  const result = await f.run(['a', 'b', 'c']);
  assert.equal(result.map(row => row.studentId).join(','), 'a,b,c');
  assert.equal(result.map(row => row.ok).join(','), 'true,false,true');
  assert.equal(result[0].status, 'Enrolled'); assert.equal(result[2].status, 'Enrolled');
  assert.equal(result[1].reason, 'Section is full.'); assert.equal(f.calls.length, 3);
});
test('middle unexpected failure stops later work and does not undo prior success', async () => {
  const f = await fixture(), failure = new Error('connection lost'); f.set([null, failure, null]);
  await assert.rejects(f.run(['a', 'b', 'c']), error => error === failure);
  assert.deepEqual(f.calls, [0, 1]); assert.deepEqual(f.successes, [0]);
});
test('INTERNAL_ERROR AppError propagates and stops later work', async () => {
  const f = await fixture(), failure = new f.AppError('INTERNAL_ERROR', 'Storage unavailable'); f.set([failure]);
  await assert.rejects(f.run(['a', 'b']), error => error === failure);
  assert.equal(f.calls.length, 1);
});
test('empty batch returns no rows and performs no transaction', async () => {
  const f = await fixture(); assert.equal((await f.run([])).length, 0); assert.equal(f.calls.length, 0);
});
''', encoding='utf-8')
s=B/'specs/7b18281f562f.json';j=json.loads(s.read_text())
j['changedFiles']=[f for f in j['changedFiles'] if not f.startswith('checks/')]
j['changedFiles'].append('tests/bulk-enroll-entry.ts')
j['checks']['resultsFile']='checks/7b18281f562f/results-crud-b02.json'
s.write_text(json.dumps(j,indent=2))
