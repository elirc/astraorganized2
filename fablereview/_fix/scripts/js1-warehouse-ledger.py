import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'js1-warehouse-ledger'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

B = [
("the React form decides what to send",
 "`client/src/App.tsx`: `submitAdjust` (line 76) turns the form's `kind` and `quantity` into one signed `delta` (`-Math.abs` for an issue, `+Math.abs` for a receipt) and calls `recordMovement`; `submitTransfer` (line 98) sends the `move` state as-is to `transfer`. Both clear `message`, catch errors and show `error.message`, then call `refreshStock()` and `maybeRefreshLedger()`. The sign convention is decided here, in the browser: the server never sees `kind`."),
("the client serializes the operation as an HTTP request",
 "`client/src/api.ts`: `recordMovement(input)` is `POST /api/movements` with `{ productId, warehouseId, delta, reason }`; `transfer(input)` is `POST /api/transfers` with `{ productId, fromWarehouseId, toWarehouseId, quantity, reason }`. The shared request helper sets the JSON header and throws `Error(data.error)` on non-2xx. The TypeScript types in `shared/types.ts` are erased at runtime, so `delta` can arrive as a string, a float or `null`."),
("the route parses and validates runtime input",
 "`server/src/index.ts`: `parseMovement` (line 233) requires UUIDs for product and warehouse, a non-zero whole-number `delta` (line 245) and a bounded `reason`; `parseTransfer` (line 255) additionally requires two different warehouses and a positive quantity. Every failure throws `ValidationError`, which the error middleware (line 206) maps to 400; anything else becomes 500 `Something went wrong.` Nothing has touched the database yet when a 400 is produced, which is why the first test can assert an unchanged `count(*)`."),
("the transaction locks, reads the balance and decides",
 "Inside `withTransaction`, the first statement is always `lockProduct` (line 311): `SELECT id FROM products WHERE id=$1 FOR UPDATE`. A second request for the same product blocks here until the first commits. Only then does `balanceOf` (line 219) sum `movements`, so the balance it reads already includes the other request's insert. `requireWarehouse` checks existence without a lock. The comment above `lockProduct` states the rule that makes opposing transfers deadlock-free: one lock, always the same one, taken before any read."),
("the storage boundary commits or rolls back",
 "A movement is one `INSERT INTO movements`; a transfer is two inserts (debit then credit) in the same transaction. `withTransaction` (`server/src/db.ts`) wraps them in `BEGIN`/`COMMIT` and issues `ROLLBACK` on any throw. The third test installs a `BEFORE INSERT` trigger that rejects the credit row: the debit insert has already run, the route answers 500, and `count(*)` is unchanged, which proves the rollback. The `CHECK (delta <> 0)` in `server/db/schema.sql` is the database's own last guard."),
("the response tells the client what actually happened",
 "Both routes answer `201 { ok: true }`; they do not return the new balance. The browser therefore calls `refreshStock()` and re-reads `/api/stock`, which is computed by `SUM(delta)` per product and warehouse. That re-read is what turns the `[201, 400]` outcome of two racing issues into the single correct balance you see on screen."),
]
fe.set_boundaries(S, B); done.append('review#1 / 2.2 six distinct trace-lab boundaries (07)')
# remove a duplicated "Explain the design tradeoff" section if present twice
def dedupe_tradeoff(t):
    marker = chr(10) + '## Explain the design tradeoff'
    first = t.find(marker)
    second = t.find(marker, first + 1) if first >= 0 else -1
    if second < 0:
        return t
    nxt = t.find(chr(10) + '## ', second + 1)
    return t[:second] + (t[nxt:] if nxt >= 0 else chr(10))
fe.rw(fe.chapter(S, '07'), dedupe_tradeoff)

R = [
"the running balance must be accumulated in the same order the ledger is displayed (timestamp, then a stable tie-breaker such as `id`), and your test must include two movements with equal `created_at`; if the ledger shows only the latest 100 rows, show where the opening balance comes from and prove it equals `SUM(delta)` of the hidden rows.",
"a reversal must be one opposite-signed movement inserted in a transaction that first takes `lockProduct`; store the original movement id in a new column; a second reversal of the same movement must be rejected (unique index on that column or an explicit check under the lock) and your test must show the balance moved exactly once after two reversal requests.",
"the missing-warehouse case must return 400 from `requireWarehouse` inside the transaction with `count(*)` unchanged (reuse the first test's comparison), the form must keep its values, and the message must name which warehouse reference failed; explain why this check runs after `lockProduct` and what would change if it ran before.",
"your comparison must include the deadlock experiment: replace `lockProduct` with two warehouse row locks taken in payload order, run two opposite transfers concurrently with `Promise.all`, and report the PostgreSQL error code you observe (`40P01`); then fix it by sorting the two warehouse ids before locking and show the same pair now yields `[201, 201]` with conserved stock.",
]
fe.set_reviews(S, R); done.append('review#3 / 2.3 per-exercise review criteria (06)')

fe.add_exercise(S, 'feel the lock ordering rule',
"""The comment above `lockProduct` in `server/src/index.ts` says one product lock serializes opposing transfers without taking warehouse locks in different orders. Make that rule bite before you trust it.

1. Predict: if `lockProduct` were replaced by locking the two warehouse rows in payload order (`FOR UPDATE` on `fromWarehouseId`, then on `toWarehouseId`), what happens when transfer A moves 1 unit main -> other while transfer B moves 1 unit other -> main at the same time? Write the interleaving down with four lines (A locks main, B locks other, A waits for other, B waits for main).
2. On a throwaway branch, implement that variant (`lockWarehouse(client, id)` called twice, no product lock). Add a test that runs the two opposite transfers in a `Promise.all` and records both statuses and, for the failure, `error.code`.
3. Run it several times. You should see at least one run where PostgreSQL aborts one transaction with `40P01 deadlock_detected` after `deadlock_timeout` (1 s by default), and the route answers 500.
4. Fix it without going back to the product lock: lock the warehouse ids in sorted order. Re-run: `[201, 201]` every time and `SUM(delta)` per warehouse is conserved.
5. Return to the shipped `lockProduct` design and explain, in three sentences, what each design buys and costs (throughput for unrelated warehouses of the same product versus simplicity).""",
"""Reference for the deadlocking variant and its repair:

```typescript
async function lockWarehouse(client: PoolClient, id: string) {
  const r = await client.query("SELECT id FROM warehouses WHERE id=$1 FOR UPDATE", [id]);
  if (!r.rowCount) throw new ValidationError("Warehouse not found.");
}
// deadlocking: payload order
await lockWarehouse(client, input.fromWarehouseId);
await lockWarehouse(client, input.toWarehouseId);
// repaired: deterministic order
for (const id of [input.fromWarehouseId, input.toWarehouseId].sort()) await lockWarehouse(client, id);
```

Reference test skeleton:

```typescript
test("opposite transfers under warehouse locks", async () => {
  const [a, b] = await Promise.all([
    api("transfers", { productId: product, fromWarehouseId: main, toWarehouseId: other, quantity: 1 }),
    api("transfers", { productId: product, fromWarehouseId: other, toWarehouseId: main, quantity: 1 }),
  ]);
  console.log(a.status, b.status); // payload order: sometimes [201, 500]; sorted order: always [201, 201]
  const sum = await h.admin.query("SELECT sum(delta) AS n FROM movements WHERE product_id=$1", [product]);
  assert.equal(Number(sum.rows[0].n), 40); // conserved either way: the loser rolled back
});
```

Review: the interesting observation is that stock is conserved even in the deadlock case (the aborted transaction rolled back), so the bug is availability, not integrity. Say which log line or error code proved the deadlock, and why sorting ids is a complete fix for two locks but not obviously for N locks across different tables."""); done.append('review#2 lock-ordering exercise 7 with deadlock experiment (05, 06)')

fe.add_exercise(S, 'ownership and authorization',
"""Movements have no actor. Add one and scope who may issue stock from which warehouse.

1. Read `X-Actor` in a small middleware; blank on `POST` -> 401. Add a `warehouse_operators(warehouse_id, actor)` table to `server/db/schema.sql` with two seed rows.
2. Inside the transaction of `POST /api/movements`, after `lockProduct`, check that `(input.warehouseId, req.actor)` exists in `warehouse_operators` for any negative `delta`; otherwise throw a `ForbiddenError` mapped to 403. Receipts (positive delta) stay open. For transfers, require the actor on the source warehouse only.
3. Record `actor` on the inserted movement row (new column) so the ledger shows who moved stock.

Acceptance: an issue by a non-operator is 403 and `count(*)` is unchanged; the same issue by an operator is 201; a receipt by anyone is 201; a transfer whose actor operates only the destination is 403.""",
"""Reference (the check lives after the lock, inside the transaction, so a concurrent operator change cannot slip through):

```typescript
if (input.delta < 0) {
  const ok = await client.query("SELECT 1 FROM warehouse_operators WHERE warehouse_id=$1 AND actor=$2", [input.warehouseId, actor]);
  if (!ok.rowCount) throw new ForbiddenError("You do not operate this warehouse.");
}
```

Review: explain why this is authorization and not validation (the request is well-formed; the caller is simply not allowed), why the ledger should record the actor from the header rather than from the body, and what the `count(*)` assertion proves that a 403 status alone does not."""
, number=8); done.append('2.5 ownership/authz exercise 8 (05, 06)')

code = open('server/src/index.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
excerpt = '\n'.join(code[128:160]) + '\n\n// server/src/index.ts:311\n' + '\n'.join(code[308:317])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/55/server/src/index.ts` with `diff --strip-trailing-cr -w`): the movement route now runs inside `withTransaction`, takes `lockProduct` before reading `balanceOf`, and rejects an over-issue with a 400 whose message carries the real balance; the transfer route reuses the same lock and inserts both rows in one transaction. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows the changed movement route and lockProduct')

fe.set_variations(S, """**Normal variation — a receipt then an issue.** `POST /api/movements` with `delta: 5` for the seeded product in `main`, then `delta: -3`. Predict the two `SUM(delta)` values you will read from `psql` between the calls and after; then check `/api/stock` shows the same number. Reason: no balance check runs for a positive delta.

**Invalid variation — a fractional issue.** `POST /api/movements` with `delta: -2.5`. Predict: 400 `Quantity must be a non-zero whole number.` and `SELECT count(*) FROM movements` unchanged. Then send `delta: "-2"` (a string): predict whether `parseMovement` coerces or rejects, run it, and read the parser to explain the outcome.

**Boundary variation — the race.** Reproduce the second test by hand: with 40 on hand, fire two `delta: -30` requests with `Promise.all`. Predict `[201, 400]` in some order and a final balance of 10. Then remove the `lockProduct` call on a throwaway branch and repeat until you observe `[201, 201]` and a balance of -20; put the lock back. Explain which statement the second request was waiting on, and why reading the balance before the lock would be wrong."""); done.append('2.4 three concrete variations')

fe.append_section(S, '04', "## This project's test harness: `test/database.ts`", """`database()` refuses any `ASTRA_TEST_DATABASE_URL` whose database name does not start with `astra_test_`, creates a private schema `astra_<uuid>`, loads `server/db/schema.sql` into it after stripping the `DROP ...` and `CREATE EXTENSION` lines (the teaching script is destructive on purpose; the extension must already exist in the test database), and only then assigns `process.env.DATABASE_URL` and does `await import("../server/src/index.js")`. That order is essential: `server/src/db.ts` creates its `Pool` from `DATABASE_URL` when the module loads, so importing the app first would bind it to the wrong database. `close()` drops the schema. The second and third tests use `h.admin` (a superuser connection into the same schema) to read `SUM(delta)` and `count(*)` directly, which is how they check what was committed rather than what the API says. Run with `$env:ASTRA_TEST_DATABASE_URL = "postgres://user@127.0.0.1:5432/astra_test_yourname"` then `npm test`.""", before='## '); done.append('review#4 database.ts walkthrough (04)')

pj = json.load(open('package.json', encoding='utf-8'))
pins = {"cors": "^2.8.6", "dotenv": "^16.6.1", "express": "^4.22.2", "pg": "^8.23.0", "react": "^18.3.1", "react-dom": "^18.3.1",
        "@types/cors": "^2.8.19", "@types/express": "^4.17.23", "@types/node": "^22.19.0", "@types/pg": "^8.15.5", "@types/react": "^18.3.27", "@types/react-dom": "^18.3.7",
        "@vitejs/plugin-react": "^6.1.1", "concurrently": "^9.2.1", "tsx": "^4.23.13", "typescript": "^5.9.3", "vite": "^8.2.2"}
for sec in ('dependencies', 'devDependencies'):
    for k in pj.get(sec, {}):
        pj[sec][k] = pins.get(k, pj[sec][k])
pj['scripts']['db:setup'] = "psql -f server/db/schema.sql"
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(pj, indent=2) + '\n')
done.append('review#5 db:setup now `psql -f server/db/schema.sql` (relies on PGDATABASE/PG* env or DATABASE_URL via psql conventions, documented in README)')
done.append('review#6 / 2.7 dependencies pinned to the versions Astra verified with')
fe.rw(fe.chapter(S, 'README'), lambda t: t.replace("`npm run db:setup`", "`npm run db:setup` (which runs `psql -f server/db/schema.sql`; set `PGHOST`, `PGPORT`, `PGUSER` and `PGDATABASE`, or pass a URL with `psql \"$env:DATABASE_URL\" -f server/db/schema.sql`)", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
