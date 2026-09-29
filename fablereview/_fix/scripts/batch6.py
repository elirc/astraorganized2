import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_blocks import apply

items = []

items.append(('astra4-2', '04', '## The commands, including the extension-free run',
"""These are the scripts from `package.json` plus the grep-invert form described above, which is how you run the browser suite on a machine without an extension-capable Chromium channel.

```bash
npm.cmd test                 # node --test tests/*.test.js
npm.cmd run build            # esbuild src/app.js -> extension/app.js
npm.cmd run test:browser     # playwright test
npx.cmd playwright test --grep-invert "unpacked extension"
npm.cmd run verify           # build && test && test:browser
```"""))

items.append(('astra4-2', '06', '## Identity and the revision check, in the code you must reuse',
"""Whatever the duplicate button does in the UI, the accepted write still goes through `applyMessage`, which owns identity and the revision comparison. From `extension/model.js:67-76`:

```js
  let presets = structuredClone(current.presets);
  if (message.action === 'create') {
    const [preset] = validatePresets([message.preset]); if (presets.some(p=>p.id===preset.id)) throw new Error('Saved-message identity already exists.'); presets.push(preset);
  } else if (message.action === 'update') {
    const [preset] = validatePresets([message.preset]); if (preset.id !== message.id) throw new Error('Saved-message identity cannot change.');
    if (!presets.some(p=>p.id===message.id)) throw new Error('Saved message not found.'); presets = presets.map(p=>p.id===message.id?preset:p);
  } else if (message.action === 'delete') {
    if (!presets.some(p=>p.id===message.id)) throw new Error('Saved message not found.'); presets = presets.filter(p=>p.id!==message.id);
  } else throw new Error('Unknown saved-message command.');
  return { ...current, presets: validatePresets(presets), revision: current.revision + 1 };
```"""))

items.append(('astra4-2', '07', '## The function to put a breakpoint in',
"""Here is `saveSettings`, from `src/app.js:128-135`. Everything after `await send(...)` runs only on acceptance — the captured `expectedRevision` is what tab B sends and what the model compares against.

```js
async function saveSettings(patch, confirmation, expectedRevision = revision) {
  try {
    const saved = await send({ type: 'settings', settings: patch, expectedRevision });
    if (currentView === 'message') messageRevision = revision; if (currentView === 'settings') settingsRevision = revision;
    renderArt(); renderTimer(); if (currentView === 'art') renderGallery();
    toast(saved.warning || confirmation);
  } catch (error) { toast(error.message || 'Your changes could not be saved.'); }
}
```"""))

items.append(('grokbuildhrproject', '04', '## The three commands',
"""Each command is one entry in the root `package.json`; all three go through the same helper that owns the temporary PostgreSQL cluster.

```bash
npm run test:api   # node scripts/test-database.mjs api     (backend jest --runInBand)
npm test           # node scripts/test-database.mjs backend (adds frontend component tests)
npm run verify     # node scripts/test-database.mjs verify  (builds + Chromium workflows)
```"""))

items.append(('grokbuildhrproject', '07', '## Round 3, in the repository',
"""Round 3 is decided by these lines from `backend/src/repositories/leaveRepository.ts:239-251`. Note the pairing the break-it exercise in chapter 04 depends on: the pre-check is a read, but `status: "PENDING"` inside the `updateMany` `where` is the guard that makes a second decision lose.

```ts
    if (current.version !== expected) throw stale();
    if (current.status !== "PENDING")
      throw new AppError(409, "Only pending requests can receive a decision.");
    const changed = await tx.leaveRequest.updateMany({
      where: { id, version: expected, status: "PENDING" },
      data: {
        status,
        decidedById: actor.id,
        decisionNote: note,
        version: { increment: 1 },
      },
    });
    if (changed.count !== 1) throw stale();
```"""))

items.append(('andie', '04', '## How the redaction is implemented',
"""The assertion that fixture credential text never reaches a reported message rests on one helper pair, applied to every thrown transport detail. From `scripts/lib/client.js:7-20`:

```js
const SECRET = /shpat_[A-Za-z0-9]+/g;
// Error detail is kept, never headers, and any token-shaped substring is masked before it can reach a log.
function redact(value) {
  if (typeof value === 'string') return value.replace(SECRET, 'shpat_[redacted]');
  if (Array.isArray(value)) return value.map(redact);
  if (value && typeof value === 'object')
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, redact(item)]));
  return value;
}
function detailed(message, details) {
  const error = new Error(message);
  error.details = redact(details);
  return error;
}
```"""))

items.append(('andie', '06', '## What a fingerprint actually covers',
"""Before you put a fingerprint in a report, read how it is produced: keys are sorted recursively, the result is serialized, and that string is hashed. It identifies normalized content and nothing else. From `scripts/lib/planner.js:4-15`:

```js
function stable(value) {
  if (Array.isArray(value)) return value.map(stable);
  if (value && typeof value === 'object')
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, stable(value[key])]),
    );
  return value;
}
const canonical = (value) => JSON.stringify(stable(value));
const hash = (value) => createHash('sha256').update(canonical(value)).digest('hex');
```"""))

items.append(('andie', '07', '## Where the offline plan is built',
"""`buildPlan` takes two snapshots and returns four arrays; no client, token or network call appears on this branch. The app-owned check below is the conflict you will reproduce when you add a `$`-prefixed or `app--` type to the source fixture. From `scripts/lib/planner.js:156-171`:

```js
function buildPlan(sourceRaw, targetRaw) {
  const source = normalizeSnapshot(sourceRaw),
    target = normalizeSnapshot(targetRaw);
  if (source.store === target.store) throw new Error('Source and target stores must differ.');
  const operations = [],
    conflicts = [],
    unchanged = [],
    targetOnly = [];
  for (const definition of source.definitions) {
    const existing = target.definitions.find((d) => d.type === definition.type);
    if (definition.type.startsWith('$') || definition.type.startsWith('app--')) {
      conflicts.push({
        type: definition.type,
        reason: 'App-owned type requires a separate ownership migration.',
      });
      continue;
```"""))

items.append(('j3', '04', '## The competing-withdrawal case',
"""Here is the concurrency case described above, from `test/bankapp/RegressionTests.java:50-57`. The latch is what makes the 64 submissions compete; the three assertions cover balance, success count and history together, because any one of them alone could pass over a broken guard.

```java
        test("competing withdrawals cannot overdraw one service",()->{
            var s=service();var executor=Executors.newFixedThreadPool(8);var gate=new CountDownLatch(1);var futures=new java.util.ArrayList<Future<Boolean>>();
            try {
                for(int i=0;i<64;i++) futures.add(executor.submit(()->{gate.await();try{s.withdraw("A",money("1"),"");return true;}catch(IllegalStateException error){return false;}}));
                gate.countDown();int successful=0;for(var future:futures) if(future.get(10,TimeUnit.SECONDS)) successful++;
                equal(10,successful);equal(money("0.00"),s.getAccountById("A").getBalance());equal(10,s.getAllTransactions().size());
            } finally {gate.countDown();executor.shutdownNow();}
        });
```"""))

items.append(('b1', '03', '## The two repaired projections',
"""This is the "after" state at both relation boundaries, from `src/lib/platform.ts:671-680`. The same `canViewIncident(actor, candidate)` that guards the primary lookup now also filters the parent and the children.

```ts
  const parentIncident = incident.parentIncidentId
    ? store.incidents.find(
        (candidate) =>
          candidate.id === incident.parentIncidentId && canViewIncident(actor, candidate),
      ) ?? null
    : null;
  const childIncidents = store.incidents.filter(
    (candidate) =>
      incident.childIncidentIds.includes(candidate.id) && canViewIncident(actor, candidate),
  );
```"""))

items.append(('b1', '04', '## Running the two harnesses',
"""Both checks are plain Node scripts with no test framework; each compiles `src/lib` into its own temporary directory and imports the compiled service.

```bash
node checks/incident-detail-regression.mjs
node checks/incident-list-pagination.mjs
```"""))

items.append(('b1', '07', '## The first six lines of the trace',
"""These are the lines to break on, from `src/lib/platform.ts:652-665`. The escalation sweep runs before the actor is resolved, and the authorization refusal happens before any projection is built.

```ts
export async function getIncidentDetail(incidentId: string, actorUserId: string): Promise<IncidentDetailView> {
  const store = await readStore();
  const evidenceEvents: EvidenceBufferEvent[] = [];
  const changed = runEscalationSweep(store, evidenceEvents);
  if (changed) {
    await flushStore(store, evidenceEvents);
  }

  const actor = getUserOrThrow(store, actorUserId);
  const incident = getIncidentOrThrow(store, incidentId);
  if (!canViewIncident(actor, incident)) {
    throw new Error("You do not have visibility for this incident.");
  }
```"""))

items.append(('aiapplybot', '04', '## The concurrent-writer case',
"""Here is the store test named above, from `tests/test_store.py:57-71`. Two threads submit the same baseline version; the assertions cover the winner, the 409, the stored version and the audit length together.

```python
    def test_two_concurrent_writers_have_one_winner(self):
        created = self.store.create(draft())

        def update(title):
            try:
                return self.store.update(created["id"], 1, draft(title=title))
            except StoreError as error:
                return error.status

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(update, ["First proposal", "Second proposal"]))
        self.assertEqual(sum(isinstance(value, dict) for value in results), 1)
        self.assertIn(409, results)
        self.assertEqual(self.store.get(created["id"])["version"], 2)
        self.assertEqual(len(self.store.audit(created["id"])), 2)
```"""))

items.append(('aiapplybot', '06', '## The version contract your new field must obey',
"""Every exercise here extends a record that is already guarded twice: a read comparison inside the transaction and a conditional `UPDATE ... WHERE id=? AND version=?`. A new column joins this statement; it does not get its own path. From `applybot/application_store.py:217-241`:

```python
    def update(self, identity: str, version: object, value: object) -> dict:
        expected, data = version_input(version), application_input(value)
        with self.transaction() as db:
            current = self._get(db, identity)
            if current["version"] != expected:
                raise StoreError(
                    "Application changed. Keep your draft and load the current record before retrying.",
                    409,
                )
            changed = db.execute(
                \"\"\"UPDATE applications SET url=?,company=?,title=?,status=?,notes=?,
                                    version=version+1,updated_at=? WHERE id=? AND version=?\"\"\",
                (
                    data["url"],
                    data["company"],
                    data["title"],
                    data["status"],
                    data["notes"],
                    utc_now(),
                    identity,
                    expected,
                ),
            )
            if changed.rowcount != 1:
                raise StoreError("Application changed while saving.", 409)
```"""))

items.append(('aiapplybot', '07', '## The breakpoint for the stale PUT',
"""Set your breakpoint on the comparison in `update`; tab B arrives here with the version it loaded, while `current["version"]` has already advanced. From `applybot/application_store.py:217-225`:

```python
    def update(self, identity: str, version: object, value: object) -> dict:
        expected, data = version_input(version), application_input(value)
        with self.transaction() as db:
            current = self._get(db, identity)
            if current["version"] != expected:
                raise StoreError(
                    "Application changed. Keep your draft and load the current record before retrying.",
                    409,
                )
```"""))

items.append(('job-track-restaurant-kitchen-display-system', '03', '## The repaired query schema',
"""The transport fix is one line: an explicit vocabulary first, then the conversion. Anything outside `'true' | 'false'` now fails validation instead of being coerced. From `server/src/lib/validation.js:22-26`:

```js
const listOrdersSchema = z.object({
  station: z.enum(['grill', 'fryer', 'salad']).optional(),
  status: z.enum(['queued', 'in_progress', 'ready']).optional(),
  includeLateOnly: z.enum(['true', 'false']).transform(value => value === 'true').optional()
});
```"""))

items.append(('job-track-restaurant-kitchen-display-system', '06', '## The multi-item case, as the suite states it',
"""The shipped regression matches the sketch above: affected orders are compared as a set, the already-ready item keeps its status, notifications are counted per event type, and a new order for the unavailable item is refused. From `server/test/kds.test.cjs:92-107`:

```js
test('global menu 86 commits all active orders and preserves ready items', async () => {
  const first = await order(['burger']);
  const second = await order(['burger', 'fries']);
  const ready = await order(['burger']);
  await request(`/order-items/${ready.items[0].id}/status`, 'PATCH', { status: 'ready' });
  notifications.length = 0;
  const result = await request('/menu-items/burger/availability', 'PATCH', { isAvailable: false, reason: 'Sold out' });
  assert.equal(result.status, 200);
  assert.deepEqual(new Set(result.body.affectedOrders), new Set([first.id, second.id]));
  assert.equal((await request(`/orders/${first.id}`)).body.order.status, 'ready');
  assert.equal((await request(`/orders/${second.id}`)).body.order.status, 'in_progress');
  assert.equal((await request(`/orders/${ready.id}`)).body.order.items[0].status, 'ready');
  assert.equal(notifications.filter(x => x.event.type === 'order_updated').length, 2);
  assert.equal(notifications.filter(x => x.event.type === 'menu_item_updated').length, 1);
  assert.equal((await request('/orders', 'POST', { channel: 'phone', items: [{ menuItemId: 'burger' }] })).status, 400);
});
```"""))

items.append(('grokbuildorderproject', '04', '## The three commands',
"""Each layer has its own root script; only `verify` builds and runs the browser gate. From `package.json`, `scripts`:

```bash
npm run test:api   # node scripts/test-database.mjs backend (jest --runInBand)
npm run test:web   # npm test --prefix frontend -- --run    (vitest)
npm run verify     # node scripts/test-database.mjs verify
```"""))

items.append(('missioncontrol', '04', '## The offline test command',
"""This is the command the README documents, and it is the one these API and unit cases run under; it needs no LLM key and no webhook endpoint.

```bash
dotnet test
```"""))

items.append(('missioncontrol', '07', '## Traces A to C in one method',
"""All three traces enter `TaskService.UpdateAsync`. Read the order: transaction, workspace-filtered task lookup, project lookup, validation, then serialization of caller collections before any tracked entity is touched. From `src/FleetCommand.Host/Services/TaskService.cs:87-113`:

```csharp
    public async Task<TaskItem> UpdateAsync(long id, UpdateTaskRequest req, string actor, CancellationToken ct = default)
    {
        await using var transaction = await BeginWriteTransactionAsync(ct);
        var task = await db.Tasks.FirstOrDefaultAsync(t => t.Id == id, ct)
            ?? throw new DomainException($"Task {id} not found");
        Project? targetProject = null;
        if (req.ProjectId is not null && req.ProjectId != task.ProjectId)
        {
            targetProject = await db.Projects.FirstOrDefaultAsync(p => p.Id == req.ProjectId, ct)
                ?? throw new DomainException($"Project {req.ProjectId} not found");
        }

        ValidateUpdateRequest(req, task);
        // Serialize caller-provided collections before touching tracked entities.
        // JsonSerializer can throw for cyclic/unsupported metadata; doing this up
        // front keeps a scoped DbContext clean for a later valid update.
        var serializedTags = req.Tags is null ? null : JsonSerializer.Serialize(req.Tags);
        var serializedMetadata = req.Metadata is null ? null : JsonSerializer.Serialize(req.Metadata);
        var oldStatus = StatusOf(task);
        var statusChanged = false;

        if (req.Title is not null)
        {
            var title = req.Title.Trim();
            if (title.Length == 0) throw new DomainException("Title is required");
            task.Title = title;
        }
```"""))

apply(items)
