from pathlib import Path
import json,shutil
B=Path(__file__).resolve().parent.parent;P=B/'stage/4bda479c4c50'
rel='deskpilot-clean/src/lib/store.ts';f=P/rel
snap=P/'astraupskill/snapshots/store.ts.original.txt';snap.parent.mkdir(parents=True,exist_ok=True);assert not snap.exists();snap.write_bytes(f.read_bytes())
t=f.read_text(encoding='utf-8')
old='  ticket.updatedAt = nowIso();\n\n  if (Object.keys(newValue).length > 0) {'
assert t.count(old)==1
t=t.replace(old,'  if (Object.keys(newValue).length === 0) {\n    return ticket;\n  }\n\n  ticket.updatedAt = nowIso();\n\n  if (Object.keys(newValue).length > 0) {')
f.write_text(t,encoding='utf-8')
T=P/'tests';(T/'helpers').mkdir(parents=True,exist_ok=True)
shutil.copyfile(B/'batch-crud-upskill-20260921/test-tools/load-typescript.mjs',T/'helpers/load-typescript.mjs')
(T/'runtime-ticket-noop.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import * as fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { loadTypeScript } from './helpers/load-typescript.mjs';
const root = fileURLToPath(new URL('..', import.meta.url));
const previous = '2020-01-01T00:00:00.000Z', current = '2026-09-21T12:00:00.000Z';
class Clock extends Date { constructor(...args) { super(...(args.length ? args : [current])); } }
async function fixture(t) {
  const temp = await fs.mkdtemp(path.join(os.tmpdir(), 'deskpilot-noop-'));
  t.after(() => fs.rm(temp, { recursive: true, force: true }));
  await fs.mkdir(path.join(temp, 'data'));
  const file = path.join(temp, 'data/deskpilot.json');
  const ticket = { id: 'ticket-1', orgId: 'org-1', subject: 'Login', priority: 'low', assigneeId: null, tags: ['bug'], updatedAt: previous };
  const original = JSON.stringify({ tickets: [ticket], ticketEvents: [], comments: [], customers: [] });
  await fs.writeFile(file, original);
  let writes = 0;
  const store = await loadTypeScript('deskpilot-clean/src/lib/store.ts', { root,
    aliasRoot: path.join(root, 'deskpilot-clean/src'), globals: { process: { cwd: () => temp }, Date: Clock },
    stubs: { 'node:path': { default: path }, 'node:fs/promises': { ...fs, writeFile: async (...args) => { writes++; return fs.writeFile(...args); } } }
  });
  return { original, raw: () => fs.readFile(file, 'utf8'), writes: () => writes,
    update: input => store.updateTicketFields({ orgId: 'org-1', ticketId: 'ticket-1', ...input }) };
}
test('empty patch preserves timestamp and file bytes without writing', async t => {
  const f = await fixture(t); const ticket = await f.update({});
  assert.equal(ticket.updatedAt, previous); assert.equal(await f.raw(), f.original); assert.equal(f.writes(), 0);
});
test('equivalent fields and normalized tags are a no-op', async t => {
  const f = await fixture(t); const ticket = await f.update({ subject: 'Login', priority: 'low', assigneeId: null, tags: [' bug ', 'bug', ''] });
  assert.equal(ticket.updatedAt, previous); assert.equal(await f.raw(), f.original); assert.equal(f.writes(), 0);
});
test('real changes persist one event with old and new fields and new timestamp', async t => {
  const f = await fixture(t); const ticket = await f.update({ subject: 'Reset login', priority: 'high', actorUserId: 'agent-1' });
  const db = JSON.parse(await f.raw()); assert.equal(f.writes(), 1); assert.equal(ticket.updatedAt, current);
  assert.equal(db.tickets[0].subject, 'Reset login'); assert.equal(db.ticketEvents.length, 1);
  const event = db.ticketEvents[0]; assert.equal(event.eventType, 'ticket.updated'); assert.equal(event.actorUserId, 'agent-1');
  assert.deepEqual(event.oldValue, { subject: 'Login', priority: 'low' });
  assert.deepEqual(event.newValue, { subject: 'Reset login', priority: 'high' }); assert.equal(event.createdAt, current);
});
test('other organization cannot mutate the matching ticket id', async t => {
  const f = await fixture(t); assert.equal(await f.update({ orgId: 'org-2', subject: 'Wrong tenant' }), null);
  assert.equal(await f.raw(), f.original); assert.equal(f.writes(), 0);
});
test('missing ticket returns null without a write', async t => {
  const f = await fixture(t); assert.equal(await f.update({ ticketId: 'missing', subject: 'Missing' }), null);
  assert.equal(await f.raw(), f.original); assert.equal(f.writes(), 0);
});
''',encoding='utf-8')
j={'id':'4bda479c4c50','project':'_Organized Desktop/04 JavaScript Training/jstrain3','summary':['Preserve the timestamp and avoid file writes for empty or equivalent ticket field patches.','Teach no-op semantics using real JSON-file persistence and event assertions.'], 'changedFiles':[rel,'astraupskill/snapshots/store.ts.original.txt','tests/runtime-ticket-noop.test.mjs','tests/helpers/load-typescript.mjs'],'checks':{'format':'json','resultsFile':'checks/4bda479c4c50/results-crud-b03.json'},'limits':['Focused tests execute the actual store with real temporary files, a fixed clock and a write-count wrapper; no Next.js HTTP or UI test was run.','The existing JSON store is not a database transaction or multi-process concurrency solution; this patch does not add locking or crash-safe writes.']}
(B/'specs/4bda479c4c50.json').write_text(json.dumps(j,indent=2))
