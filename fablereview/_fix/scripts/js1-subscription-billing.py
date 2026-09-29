import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'js1-subscription-billing'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# --- code: whole-cent rule in parseItem + regression case (review #2)
src = 'server/src/index.ts'
def patch_src(t):
    old = """  if (
    !Number.isFinite(item.amount) ||
    item.amount < 0 ||
    item.amount > 9999999999.99
  )
    throw new ValidationError("Amount must be zero or greater.");
  return item;"""
    new = """  if (
    !Number.isFinite(item.amount) ||
    item.amount < 0 ||
    item.amount > 9999999999.99
  )
    throw new ValidationError("Amount must be zero or greater.");
  // Whole cents only: the numeric(12,2) column would otherwise round 12.345 silently.
  if (Math.abs(item.amount * 100 - Math.round(item.amount * 100)) > 1e-6)
    throw new ValidationError("Amount must be whole cents.");
  return item;"""
    assert old in t, 'parseItem tail not found'
    return t.replace(old, new)
assert fe.rw(src, patch_src)
done.append('review#2: parseItem now rejects fractional cents (server/src/index.ts) — the course claim is now true')

tst = 'test/workflow.test.ts'
def patch_test(t):
    t = t.replace("let h;\n", "let h: Awaited<ReturnType<typeof database>>;\n", 1)
    t = t.replace('const call = (path, method = "GET", body = undefined) =>', 'const call = (path: string, method = "GET", body?: unknown) =>', 1)
    t = t.replace("    { amount: null },\n  ]) {", "    { amount: null },\n    { amount: 12.345 },\n  ]) {", 1)
    return t
assert fe.rw(tst, patch_test)
done.append('review#4: test file typed (h, call) so `npm run typecheck` covers it; new `{ amount: 12.345 } -> 400` case')

# --- 1.3 sentence: now the accurate "rejected" version for this project
for pre in ('02', '03', '07'):
    fe.rw(fe.chapter(S, pre), lambda t: re.sub(r"Amounts must be finite, nonnegative numbers: `server/server\.js` checks .*? This scaffold does not perform real payment processing\.",
        "Amounts must be finite, nonnegative, whole-cent values: `parseItem` in `server/src/index.ts` checks `Number.isFinite`, the range, and that `amount * 100` is a whole number, so 12.345 is rejected with 400 (`Amount must be whole cents.`) instead of being silently rounded by the `numeric(12,2)` column. This scaffold does not perform real payment processing.", t))
done.append('1.3 whole-cent sentence corrected to the implemented behavior (02, 03, 07)')

B = [
("the React form or status button decides what to send",
 "`client/src/App.tsx`: `save` (line 113) sends the whole `form` object through `createItem` or `updateItem` depending on `editingId`; `changeStatus(item, status)` (line 125) sends only the new status. Both wrap the call in `try/catch` and hand failures to `report(error)`, which is where the server's `error` text becomes the message you see. No field is validated in the browser beyond input types; `amount` leaves the form as whatever the number input produced."),
("the client serializes the operation as an HTTP request",
 "`client/src/api.ts`: `updateStatus(id, status)` builds `PATCH /api/subscriptions/:id/status` with body `{ status }`; `updateItem` builds `PUT /api/subscriptions/:id` with the full `NewItem`. The generic `request<T>()` sets `Content-Type: application/json`, returns `null` on 204 and throws `new Error(data.error || \"Request failed.\")` on any non-2xx. The TypeScript types in `shared/types.ts` describe the wire shape, but they are erased at runtime: nothing here guarantees the server receives numbers where it expects them."),
("the route parses and validates runtime input",
 "`server/src/index.ts:30` `app.param(\"id\")` rejects anything that is not a UUID with 400 before any handler runs. The PATCH route (line 186) checks `STATUSES.includes(req.body?.status)` and throws `ValidationError`; create and full edit call `parseItem` (line 326), which type-checks every field, runs `validDate`, applies the priority allowlist, normalizes, then enforces title/owner length, status, category, the finite nonnegative range and the whole-cent rule. `asyncRoute` forwards a thrown `ValidationError` to the error middleware, which maps it to 400; anything else becomes 500."),
("the repository applies the change inside one transaction",
 "The PATCH handler calls `withTransaction` (`server/src/db.ts:22`). Inside it, `SELECT * FROM items WHERE id=$1 FOR UPDATE` (line 195) locks the row, so a second concurrent PATCH waits here. If the locked row already has the requested status the callback returns it unchanged: no `UPDATE`, no activity row. Otherwise `UPDATE items SET status=$1, updated_at=now()` and `INSERT INTO activity_entries (... 'status' ...)` run on the same client. Compare with the PUT route (line 149), which updates every column and always records an `updated` entry."),
("the storage boundary commits or rolls back",
 "`withTransaction` issues `BEGIN`, runs the callback, then `COMMIT`; any throw triggers `ROLLBACK` and re-throws, and the client is released in `finally`. The fourth test proves the boundary: a `BEFORE INSERT` trigger on `activity_entries` makes the audit insert fail, the route answers 500, and the record is byte-for-byte unchanged, because the `UPDATE` in the same transaction was rolled back. The `numeric(12,2)` column and the `CHECK` constraints in `server/db/schema.sql` are the last line of defense if `parseItem` is bypassed."),
("the response tells the client what actually happened",
 "The handler answers `res.json(toItem(updated))` (200), or 404 `{ error: \"Record not found.\" }` when the locked select found nothing. `toItem` converts `due_date` and `numeric` strings back into the wire shape. In the browser `changeStatus` then calls `refresh()` and re-fetches the activity list, so what you see is a fresh read of committed rows, not the PATCH response."),
]
fe.set_boundaries(S, B); done.append('review#3 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the window must be computed in SQL inside the same `REPEATABLE READ READ ONLY` transaction as the count (add it to the `where` string with a parameter), both ends stated as inclusive or exclusive, and a record due exactly on the end date tested; `total` and the page clamp must reflect the filtered rows, which means the filter runs in the `COUNT(*)` query too.",
"the reason must be stored on the `status` activity row only (a new nullable `reason` column or the `body`), written by the same `INSERT` inside `withTransaction`; a repeat with the same status must still return early without writing; a blank reason must be rejected with 400 before `BEGIN`; and your test must reuse the trigger technique from the fourth test to prove that a failed reason insert rolls the status back.",
"after deleting the only row on page 2 of a filtered list, requesting page 2 again must clamp to page 1 with `total` 2 and the remaining ids; a filter that matches nothing must return `total` 0 and `page` 1; assert on ids, and note that the count and the rows come from one snapshot transaction, so a concurrent insert cannot make them disagree.",
"the check must be part of the `UPDATE` itself, `UPDATE items SET ... WHERE id=$1 AND updated_at=$2 RETURNING *`, run under `FOR UPDATE` or as a single statement; zero rows updated means 409 and no activity row; your test sends two sequential `PUT`s with the same stale `updatedAt` and asserts 200 then 409 with the stored record equal to the first result.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')

code = open(src, encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
# PATCH route 186..220 (1-based) and the amount checks (whole-cent rule follows the range check)
i = next(i for i, l in enumerate(code) if 'Amount must be zero or greater' in l)
excerpt = '\n'.join(code[185:220]) + '\n\n// parseItem, server/src/index.ts:' + str(i - 4) + '\n' + '\n'.join(code[i - 5:i + 4])
fe.set_excerpt(S, "The lines below are the ones that changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/52/server/src/index.ts` with `diff --strip-trailing-cr -w`): the PATCH route now locks the row with `FOR UPDATE`, returns early on a no-op status, and writes the update and its audit row in one transaction; `parseItem` gained the finite/range check and, in this course's fix pass, the whole-cent rule. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows the changed PATCH route and amount checks')

fe.set_variations(S, """**Normal variation — a real edit.** `PUT /api/subscriptions/:id` with the full valid fixture but `priority: "High"`. Predict: 200, `priority` is `High`, `updatedAt` moved, and `GET /activity` has one more `updated` row. Then check `SELECT updated_at FROM items WHERE id=...` in `psql` to see that the timestamp is the database's `now()`, not the client's clock.

**Invalid variation — fractional cents.** `PUT` with `amount: 12.345`. Predict: 400 `Amount must be whole cents.` and the stored row unchanged (deep-equal the GET). Then comment out the whole-cent check, run the same request, and read the row: PostgreSQL's `numeric(12,2)` silently stores 12.35. That silent rounding is why the validation belongs before the write.

**Boundary variation — a failing audit insert.** Reuse the fourth test's trigger (`CREATE TRIGGER fail_lesson_audit BEFORE INSERT ON activity_entries ...`) from `psql` against your dev database, then `PATCH /status` to `Active`. Predict: 500, the record still `Trial`, and one activity row (the seed). Drop the trigger and repeat: 200 and exactly two rows. Explain which line in `withTransaction` made the first outcome all-or-nothing."""); done.append('2.4 three concrete variations')

fe.add_exercise(S, 'ownership and authorization',
"""Every subscription row has an `owner` column, but any browser can edit any row. Add an actor and enforce ownership inside the transaction.

1. Read the caller identity from an `X-Actor` header in a small middleware and attach it as `req.actor`; a blank header on `POST`, `PUT`, `PATCH` or `DELETE` answers 401 `{ error: "Sign in to change records." }`. `GET` stays open.
2. In the PUT, PATCH and DELETE handlers, after `SELECT ... FOR UPDATE` (add that select to PUT and DELETE, which currently update blind), compare `row.owner` with `req.actor`; on mismatch throw a new `ForbiddenError` that the error middleware maps to 403, so the transaction rolls back with nothing written.
3. On `POST`, overwrite `owner` with `req.actor` before the `INSERT`.
4. Send the header from `client/src/api.ts` using a small "signed in as" input.

Acceptance, written before coding: cross-owner `PUT` is 403 and the row deep-equals the original; cross-owner `PATCH /status` is 403 with no new activity row; owner `PATCH` is 200; missing header is 401. Extend `request()` in `test/database.ts` with a `headers` parameter to write the test.""",
"""Reference implementation (the important part is that the ownership check happens on the locked row, inside the same transaction as the write):

```typescript
class ForbiddenError extends Error {}
app.use((req, _res, next) => { (req as any).actor = String(req.get("X-Actor") ?? "").trim(); next(); });
function requireActor(req: express.Request, res: express.Response, next: express.NextFunction) {
  if (!(req as any).actor) return res.status(401).json({ error: "Sign in to change records." });
  next();
}
// inside the PATCH transaction, right after the FOR UPDATE select:
if (current.rows[0].owner !== (req as any).actor) throw new ForbiddenError("Only the owner can change this subscription.");
// error middleware:
if (error instanceof ForbiddenError) return res.status(403).json({ error: error.message });
```

Reference test (after adding `headers: Record<string, string> = {}` to `request()` and spreading it into the fetch headers):

```typescript
test("only the owner can change a subscription", async () => {
  const mine = { "X-Actor": "Junior Learner" }, other = { "X-Actor": "Someone Else" };
  const made = await call(route, "POST", valid, mine);
  const path = route + "/" + made.data.id;
  assert.equal((await call(path, "PUT", { ...valid, title: "Hijacked" }, other)).status, 403);
  assert.deepEqual((await call(path)).data, made.data);
  assert.equal((await call(path + "/status", "PATCH", { status: "Active" }, other)).status, 403);
  assert.equal((await call(path + "/activity")).data.length, 1);
  assert.equal((await call(path + "/status", "PATCH", { status: "Active" }, mine)).status, 200);
  assert.equal((await call(path, "PUT", valid)).status, 401);
});
```

Review: the 403 must come from inside `withTransaction` so the lock is released by the rollback; `POST` must ignore a body `owner`; explain why the check is on `current.rows[0].owner` (the locked, committed value) and not on whatever the client sent."""); done.append('2.5 ownership/authz exercise 7 with reference code and test (05, 06)')

fe.append_section(S, '04', "## This project's test harness: `test/database.ts`", """`database()` refuses to run unless `ASTRA_TEST_DATABASE_URL` points at a database whose name starts with `astra_test_`, creates a schema named `astra_<uuid>`, applies `server/db/schema.sql` into it (stripping the `DROP` and `CREATE EXTENSION` lines, which is why `pgcrypto` must already exist in the test database), and only then sets `process.env.DATABASE_URL` and does `await import("../server/src/index.js")`. The order matters: `server/src/db.ts` builds its `Pool` from `DATABASE_URL` at module load, so importing the app first would connect to the wrong database and ignore the schema. Every test file therefore gets its own schema and drops it in `close()`. `request()` returns `{ status, data }` and never throws on 4xx, which is what lets the tests assert a 400 and then re-read the row. Start the run with `$env:ASTRA_TEST_DATABASE_URL = "postgres://user@127.0.0.1:5432/astra_test_yourname"` then `npm test`.""", before='## '); done.append('review#6 database.ts walkthrough with the import-order detail (04)')

pj = json.load(open('package.json', encoding='utf-8'))
pins = {"cors": "^2.8.6", "dotenv": "^16.6.1", "express": "^4.22.2", "pg": "^8.23.0", "react": "^18.3.1", "react-dom": "^18.3.1",
        "@types/cors": "^2.8.19", "@types/express": "^4.17.23", "@types/node": "^22.19.0", "@types/pg": "^8.15.5", "@types/react": "^18.3.27", "@types/react-dom": "^18.3.7",
        "@vitejs/plugin-react": "^6.1.1", "concurrently": "^9.2.1", "tsx": "^4.23.13", "typescript": "^5.9.3", "vite": "^8.2.2"}
for sec in ('dependencies', 'devDependencies'):
    for k in pj.get(sec, {}):
        pj[sec][k] = pins.get(k, pj[sec][k])
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(pj, indent=2) + '\n')
done.append('review#5 / 2.7 dependencies pinned to the versions Astra verified with (react 18.3.1, vite 8.2.2, express 4.22.2, pg 8.23.0, tsx 4.23.13, typescript 5.9.3)')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
