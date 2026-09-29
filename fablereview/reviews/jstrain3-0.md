# jstrain3.0 — Fable review

- **Path:** `_Organized Desktop/04 JavaScript Training/jstrain3.0`  ·  **Wave:** 2  ·  **Stack:** Node 22 + Express 4 + better-sqlite3 (server), Vite/React client  ·  **Batch:** B16
- **Astra's change (one line):** Fixed a real oversell TOCTOU in checkout — moved the cart SELECT inside the `better-sqlite3` immediate transaction, replaced `UPDATE products SET stock = stock - ?` with a conditional `... AND stock >= ?` + `changes !== 1` abort, added strict `positiveSafeInteger` validation on cart routes, and introduced `createDatabase`/`createCartRouter`/`createOrderRouter`/`createApp` seams so handlers are testable without a listener.
- **Course size:** 6,027 words across 9 files  ·  **Tests claimed:** 6  ·  **Tests found on disk:** 6 in `server/tests/cart-validation.test.mjs` (lines 74, 83, 107, 124, 141, 192)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 4.9 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The bug fixed is the textbook one a junior must learn. `backups/4c54d18d7d97/server/src/routes/orders.js` checked `item.quantity > item.stock` in a loop **outside** the transaction, then ran an unconditional `UPDATE products SET stock = stock - ? WHERE id = ?`. The new `server/src/services/checkout.js` does the cart read, the validation, the order insert, the conditional decrement and the cart delete inside one `database.transaction(...).immediate(userId)`.
- Defence in depth is taught explicitly: the write route validates input (`cart.js` `positiveSafeInteger`), and checkout **re-validates persisted rows** (`totalForCart` → `validateCartLine`) because a legacy/hostile row may already be in the table. 06-SOLUTIONS §3 states the reason in one sentence.
- The rollback test is a real one, not a mock assertion: test 6 ("unknown persistence errors become safe 500 responses and roll back all checkout writes") drives the actual `createApp` error middleware, and 06-SOLUTIONS §4 openly corrects Astra's own exercise wording — the two-line stock case is a *preflight* rejection and "does not prove rollback of earlier writes", so a SQLite trigger is used for the real rollback proof. That level of self-correction is rare.
- Original bytes are preserved for the worked-change comparison: `astraupskill/snapshots/server__src__routes__cart.js.txt` is byte-identical to the backup copy (verified with `diff`), so a learner can do the before/after read without git.

## Problems found (evidence required)
- **[D2]** Indentation was not repaired after wrapping the routers in factories — inside `createCartRouter`, the handler bodies stay at the old two-space level (`server/src/routes/cart.js`, e.g. `router.get('/', (req, res) => {` at 2 spaces with its body at 2 spaces and the closing `});` at 2 spaces). Functionally irrelevant, but juniors are being asked to read this file closely and the block structure is now visually misleading.
- **[D7]** `server/package.json` has no `test` script; the only way to run the suite is the literal command in VERIFICATION.md (`node --test server/tests/cart-validation.test.mjs`). A junior who types `npm test` in `server/` gets an npm error, not a test run.
- **[D7]** The chapters assume prior comfort with Express routers, JWT middleware and SQLite semantics. `07-TRACE-LAB.md:1` opens straight into "creates a synchronous `db.transaction` callback" with no prior definition of what `immediate` mode does beyond a one-line code comment.
- **[D6, minor]** `deliveries/4c54d18d7d97.json` reports `testResults.total: 6` but then lists nine entries under `checks` (install, client install, client build, five syntax gates plus the test run). It is not an inflated count — the log `astraupskill/evidence/luna-server-final-check-20260912.log` ends with `# tests 6 / # pass 6 / # fail 0` — but the shape invites misreading.

## Spot-checks performed
- VERIFICATION claims "six discovered tests, six passes and zero failures" → `astraupskill/evidence/luna-server-final-check-20260912.log` tail shows `1..6`, `# tests 6`, `# pass 6`, `# fail 0` → **matches**.
- README claims checkout "decrements stock with a `stock >= quantity` predicate" → `server/src/services/checkout.js` `'UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?'` plus `if (changed.changes !== 1) throw new InsufficientStockError(...)` → **matches**.
- README claims `snapshots/` are "byte copies of the original files before the staged edit" → `diff astraupskill/snapshots/server__src__routes__cart.js.txt backups/4c54d18d7d97/server/src/routes/cart.js` → identical → **matches**.
- 07-TRACE-LAB says "the route never accepts a user id from the body" → every statement in `server/src/routes/cart.js` and `orders.js` binds `req.user.id` → **matches**.
- VERIFICATION says "Importing the lazy default database ... does not initialize the canonical `server/data/store.db`" → `server/src/db/connection.js` wraps the default in a `Proxy` whose `get` calls `getDefaultDatabase()` on first property access, and `index.js` only calls `initializeDatabase()` under the `process.argv[1] === fileURLToPath(import.meta.url)` guard → **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Add `"test": "node --test tests/"` to `server/package.json` and reference `npm test --prefix server` in `VERIFICATION.md` and `04-TESTING-AND-DEBUGGING.md`, so the documented command matches the muscle memory a junior will actually use. (effort: S)
2. Re-indent `server/src/routes/cart.js` and `orders.js` after the factory wrap (pure formatting, no behavior change), then regenerate the after-hash in the delivery record. (effort: S)
3. Add a short "SQLite transaction modes" box to `02-CONCEPTS.md`: deferred vs `immediate` vs exclusive, and why `immediate` is what stops the second checkout from reading stale stock — currently that reasoning exists only as a code comment at the bottom of `checkout.js`. (effort: S)
4. Add the missing negative cases named in VERIFICATION as exercises with skeleton tests: the accumulated-total overflow case and the "forced zero-row conditional UPDATE" case. They are the two most instructive holes and Astra already identified them. (effort: M)

## One-paragraph summary for the index
This is the best pure server-side course in the batch and should sit early in the Node/SQL sequence. The original `POST /api/orders` checked stock in a loop outside its transaction and then decremented unconditionally — the classic oversell; Astra moved the read into an immediate transaction, made the decrement conditional on `stock >= quantity`, and added strict input validation plus a second validation pass over already-persisted rows. Six real regression tests drive the production handlers against a disposable SQLite file, including a trigger-induced second-line failure that proves rollback. The course is honest about what it did not prove (no live listener, no JWT parsing, no multi-process contention, no payment), and the solutions chapter even corrects one of its own exercises. Expect to already know Express basics; you will not be hand-held through routers.
