import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_blocks import apply

items = []

items.append(('grokbuildecommerceproject', '04', '## The commands behind each layer',
"""Each suite named below has one script entry at the repository root; the helper that creates and tears down the marked temporary PostgreSQL database is the same in all of them. From the root `package.json`, `scripts`:

```bash
npm run test:api      # node scripts/test-database.mjs api      (backend jest --runInBand)
npm test              # node scripts/test-database.mjs backend  (adds component tests)
npm run verify        # node scripts/test-database.mjs verify    (complete local workflow)
npm run test:browser  # node scripts/test-database.mjs browser   (Playwright checkout suite)
```"""))

items.append(('grokbuildecommerceproject', '07', '## The receipt lock you are tracing',
"""Round 3 depends on the first few statements of the checkout transaction: the advisory lock is taken on `userId + ":" + requestId` *before* the durable receipt is read, so a retry of the same key waits rather than racing. From `backend/src/repositories/orderRepository.ts:85-102`:

```ts
export async function checkout(value: Actor, input: CheckoutInput) {
  orderScope(value);
  const hash = fingerprint(input),
    items = sortedItems(input);
  return prisma.$transaction(
    async (tx) => {
      // Serialize the same customer's key before inspecting its durable receipt.
      const lockKey = value.id + ":" + input.requestId;
      await tx.$queryRaw`SELECT 1 AS locked FROM pg_advisory_xact_lock(hashtextextended(${lockKey},0))`;
      const existing = await tx.order.findUnique({
        where: {
          userId_checkoutKey: {
            userId: value.id,
            checkoutKey: input.requestId,
          },
        },
        include: orderDetails,
      });
```"""))

items.append(('buildsmallplates', '04', '## The commands that produce this evidence',
"""There are exactly two checks in this project, both declared in `package.json`; neither starts a device or the Expo runtime, which is why the repository-level tests above are still described as proposed.

```bash
npm test        # vitest run
npm run typecheck  # tsc --noEmit
```"""))

items.append(('buildsmallplates', '07', '## The write at the end of the trace',
"""This is the repository function the tap reaches, from `src/db/repos.ts:433-467`. The single pass over `mapping` is what keeps the validated fields and the bound columns the same list, and `result.changes === 0` is the missing-id branch that returns `false` without bumping the version.

```ts
export function updateSet(
  setId: string,
  fields: Partial<Pick<SetRecord, 'actualWeightKg' | 'actualReps' | 'rpe' | 'isFailure' | 'completedAt' | 'note' | 'kind'>>,
): boolean {
  const cols: string[] = [];
  const vals: (string | number | null)[] = [];
  const mapping: Record<string, string> = {
    actualWeightKg: 'actual_weight_kg',
    actualReps: 'actual_reps',
    rpe: 'rpe',
    isFailure: 'is_failure',
    completedAt: 'completed_at',
    note: 'note',
    kind: 'kind',
  };
  const nonNumeric = new Set(['note', 'kind', 'isFailure', 'completedAt']);
  for (const [k, col] of Object.entries(mapping)) {
    if (!(k in fields)) continue;
    const v = (fields as Record<string, unknown>)[k];
    if (v === undefined) continue;
    if (v !== null && !nonNumeric.has(k)) {
      if (typeof v !== 'number') throw new Error(`${k} must be a number`);
      assertValidSetNumber(k as SetNumericField, v);
    }
    cols.push(`${col} = ?`);
    vals.push(typeof v === 'boolean' ? (v ? 1 : 0) : (v as string | number | null));
  }
  if (cols.length === 0) return false;
  vals.push(setId);
  const result = getDb().runSync(`UPDATE set_entries SET ${cols.join(', ')} WHERE id = ?`, vals);
  if (result.changes === 0) return false;
  bump();
  return true;
}
```"""))

items.append(('react', '03', '## The save the walkthrough follows',
"""The paragraphs above describe one function. Here it is, from `store.js:48-62`: validation first, then the named Web Lock, then the baseline comparison, and only then `setItem`. The accepted snapshot is the return value, so the controller cannot close the editor on a failed write.

```js
  async save(candidate, expectedRaw, { replaceInvalid = false } = {}) {
    const normalized = validateState(candidate);
    if (!this.locks?.request) throw new Error('Saving needs Web Locks. Open the local server in a supported browser.');
    return this.locks.request(`quiz-board:${STORAGE_KEY}`, async () => {
      let current; try { current = this.storage.getItem(STORAGE_KEY); } catch { throw new Error('Browser storage is unavailable.'); }
      if (current !== expectedRaw) throw new Error('This board changed in another tab. Reload before saving; your draft is preserved.');
      let revision = 0;
      try { revision = parseState(current).revision; } catch (error) { if (!replaceInvalid) throw error; }
      if (revision >= Number.MAX_SAFE_INTEGER) throw new Error('Revision limit reached; export and review the board.');
      const state = { ...normalized, revision: revision + 1 }; const raw = JSON.stringify(state);
      if (new TextEncoder().encode(raw).length > MAX_BYTES) throw new Error('Board exceeds the 2 MiB limit.');
      try { this.storage.setItem(STORAGE_KEY, raw); } catch { throw new Error('Save failed: browser storage is full or unavailable. Your draft is preserved.'); }
      return { raw, state };
    });
  }
```"""))

items.append(('react', '04', '## The three commands',
"""Both layers are declared in `package.json`; `npm run verify` is simply the pair, and it fails if the Node cases fail before Playwright starts.

```bash
npm test          # node --test test/store.test.js
npm run test:browser  # playwright test
npm run verify    # npm test && npm run test:browser
```"""))

items.append(('react', '06', '## The invariant a framework change must not lose',
"""Whatever you later put in front of this store, this case must keep passing: two savers sharing one baseline produce exactly one winner and one revision. From `test/store.test.js:106-119`:

```js
test('two concurrent cooperating saves from one baseline have one winner', async () => {
  const memory = storage(),
    lock = locks(),
    a = new BoardStore(memory, lock),
    b = new BoardStore(memory, lock);
  const first = freshState(),
    second = freshState();
  first.categories[0].name = 'First';
  second.categories[0].name = 'Second';
  const results = await Promise.allSettled([a.save(first, null), b.save(second, null)]);
  assert.equal(results.filter((r) => r.status === 'fulfilled').length, 1);
  assert.equal(results.filter((r) => r.status === 'rejected').length, 1);
  assert.equal(a.load().state.revision, 1);
});
```"""))

items.append(('react', '07', '## What the second tab actually receives',
"""When the first tab saves, the second tab does not poll: it reloads accepted state from a `storage` event and leaves the open draft alone. From `main.js:65-69`:

```js
window.addEventListener('storage', event => {
  if (event.key !== STORAGE_KEY && event.key !== null) return;
  load(); status('Saved board changed in another tab.');
  if (editor.dialog.open) byId('editor-error').textContent = 'Another tab changed the saved board. This draft is preserved; cancel and reload before editing again.';
});
```"""))

items.append(('buildsubbox', '03', '## The input contract in code',
"""The rules described above are enforced in one place before any quote line is built, from `src/model.js:381-394`. Note that the plan's `itemCount` — not the UI — decides how many distinct items a valid draft has.

```js
export function quoteBox(s, subscriberId, itemIds) {
  array(itemIds, 20);
  unique(itemIds);
  const u = s.subscribers.find((u) => u.id === subscriberId);
  ensure(
    u && u.status === "Active",
    "Only an active subscriber can reserve a box.",
  );
  const p = s.plans.find((p) => p.id === u.planId);
  ensure(p?.active, "The subscription plan is unavailable.");
  ensure(
    itemIds.length === p.itemCount,
    `Choose exactly ${p.itemCount} distinct items.`,
  );
```"""))

items.append(('buildsubbox', '06', '## What a server would have to replace',
"""Before sketching a server, read the transaction you already have. `commit` in `src/repository.js:11-24` is lock, replay check, base comparison, reduce, write — a server version needs all five, with the lock and the base comparison moved into the database.

```js
  async function commit(base, command) {
    return lock(() => {
      const current = load();
      if (replay(current.state, command)) return current;
      if (current.raw !== base.raw)
        throw new Error(
          "Workspace changed in another tab. Export your draft and reload before saving.",
        );
      const state = reduce(current.state, command);
      const raw = encode(state);
      storage.setItem(STORAGE_KEY, raw);
      return { state, raw };
    });
  }
```"""))

items.append(('buildsubbox', '07', '## The duplicate-policy case Lab C reproduces',
"""Lab C asks you to resend one reservation. The model test states the expected outcome exactly: replaying the same command returns an identical state object and stock is decremented once. From `test/model.test.mjs:250-263`:

```js
test("same request replays without reserving stock twice", () => {
  const c = reserve(),
    s = reduce(fresh(), c);
  assert.equal(reduce(s, c), s);
  assert.equal(s.items[0].stock, 419);
});
test("changed cycle under an accepted key fails", () => {
  const c = reserve(),
    s = reduce(fresh(), c);
  assert.throws(
    () => reduce(s, { ...c, cycle: "2026-10" }),
    /different reservation/,
  );
});
```"""))

apply(items)
