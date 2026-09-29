# Subscription Billing — Fable review

- **Path:** `JS1/subscription-billing`  ·  **Wave:** 1  ·  **Stack:** Node/Express + TypeScript + PostgreSQL (`pg`) + React/Vite  ·  **Batch:** B06
- **Astra's change (one line):** Made the list endpoint read count+page inside one `REPEATABLE READ READ ONLY` transaction with an `id ASC` tie-break and a clamped page, made `PATCH /status` take `SELECT … FOR UPDATE` and skip the write + audit row when the status is unchanged, wrapped every route in an `asyncRoute` catcher (previously a rejected promise could hang the request), added a UUID `app.param` guard and full runtime body validation, fixed a `DATE`-to-local-midnight drift with `pg.types.setTypeParser(1082, v => v)`, and fixed a real seed bug in `server/db/schema.sql`.
- **Course size:** 8,391 words across 9 files  ·  **Tests claimed:** 4  ·  **Tests found on disk:** 4 (`test/workflow.test.ts`, harness `test/database.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 3 | 5 | 3 | 5 | 4 | 5 | 4 | 2 | 3.9 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- The pagination fix is the textbook-correct one and rare to see done properly: `SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY`, then `COUNT(*)`, then `Math.min(filters.page, totalPages)`, then the page query with `ORDER BY ${sort} ${direction}, id ASC`. Count and page can no longer disagree under concurrent inserts.
- Idempotent status is enforced at the database, not in JS: `SELECT * FROM items WHERE id=$1 FOR UPDATE` inside `withTransaction`, then `if (current.rows[0].status === status) return current.rows[0];`. The old code was a bare `UPDATE … SET status` plus a second unconditioned `INSERT INTO activity_entries`.
- A genuine pre-existing bug was fixed in `server/db/schema.sql`: the seed selected `due_date::date` from a `json_to_recordset(...) AS x(… due_date text …)` whose JSON key is `dueDate`, so the column was always null. Astra changed both to the quoted `"dueDate"`.
- The 4th test is the best test in the batch: it installs a `BEFORE INSERT` trigger that raises on `kind='status'`, asserts the status PATCH returns 500, then asserts `deepEqual((await call(path)).data, made.data)` and `activity.length === 1` — i.e. it proves the transaction actually rolled back, rather than proving "the code has a BEGIN in it".
- The test harness (`test/database.ts`) refuses any database whose name does not start with `astra_test_`, creates a per-run schema, strips `DROP …`/`CREATE EXTENSION` from the teaching SQL, and drops the schema on close. That is a safe pattern a junior can reuse.
- Verification is honest: `logs/52-tests.log` = `# tests 4 # pass 4 # fail 0`; typecheck, build and browser entries all exist in `checks.json` / `browser-checks.json`; all 20 manifest hashes match disk.

## Problems found (evidence required)
- **[D8]** This course is a noun-swap of `JS1/field-service` and `JS1/research-studies`. Measured with `diff`: `02-CONCEPTS.md` differs by **2 of 45 lines**, `05-PRACTICE.md` by **1 of 47**, `04-TESTING-AND-DEBUGGING.md` by **1 of 69**, `07-TRACE-LAB.md` by **4 of 114**. The three `test/workflow.test.ts` files have identical test names and identical bodies apart from the status/category vocabulary. Only one of the three belongs in a learning path.
- **[D1]** `02-CONCEPTS.md:9` — "Amounts are bounded nonnegative currency values; a **fractional cent is rejected** rather than silently rounded." False, and worse here than elsewhere because this is the *billing* app. `server/src/index.ts:~352` only checks `!Number.isFinite(item.amount) || item.amount < 0 || item.amount > 9999999999.99`. The test fixture itself uses `amount: 12.5`; `12.345` would be accepted.
- **[D3/D1]** `07-TRACE-LAB.md` repeats one identical instruction paragraph under all six "Boundary" headings, each pointing at `server/src/index.ts` and `parseItem` — including the two boundaries that describe the React client. `06-SOLUTIONS-AND-REVIEW.md` repeats one identical **Review:** paragraph under all four exercises.
- **[D8]** `04-TESTING-AND-DEBUGGING.md` contains a paragraph about unrelated projects: "Questboard uses Vitest and simulated browser storage; DevDeck uses Vitest with fake-indexeddb for its actual Dexie methods… Live Chat also tests a real WebSocket and PostgreSQL notification."
- **[D5]** All `dependencies`/`devDependencies` in `package.json` are `"latest"` with no lockfile (pre-existing; VERIFICATION.md does disclose it). Separately, `checks.json` shows the verified commands were `node <impl>/node_modules/typescript/bin/tsc`, `…/tsx/dist/cli.mjs --test <stage>/52/test/workflow.test.ts` and `…/vite/bin/vite.js build` run from Astra's shared workspace — `npm install && npm test` in *this* folder is documented but was never executed.
- **[D2, minor]** `test/workflow.test.ts` is a `.ts` file written as untyped JS (`let h;`, `const call = (path, method = "GET", body = undefined) =>`). `npm run typecheck` runs `tsc --noEmit` over the project; the suite is only green because `tsx --test` strips types rather than checking them.

## Spot-checks performed
- "The excerpt below comes from `server/src/index.ts` near line 326" -> `grep -n "^function parseItem"` returns **326** -> matches exactly.
- "Repeating a status leaves timestamps and history alone" -> read the `PATCH /:id/status` handler: `FOR UPDATE` + `if (current.rows[0].status === status) return current.rows[0]` -> matches.
- "a fractional cent is rejected" -> read `parseItem` and the amount branch -> **does not match**.
- "Count matching records after filters, calculate the last page, clamp the request, then fetch that page" (`02-CONCEPTS.md`) -> read the `GET /api/subscriptions` transaction: `COUNT(*)` -> `totalPages` -> `Math.min(filters.page, totalPages)` -> `LIMIT/OFFSET` -> matches, in that order.
- VERIFICATION "Automated test cases: 4" and "typecheck Passed" -> `logs/52-tests.log` `# tests 4 # pass 4`, `52-typecheck.log` present with `exit_code: 0` in `checks.json` -> matches.
- "The helper refuses a non-test database name" (README) -> `test/database.ts`: `if (!url.pathname.slice(1).startsWith("astra_test_")) throw new Error("Refusing a non-test database.")` -> matches.

## Improvements needed (ordered, concrete, actionable)
1. Pick **one** of subscription-billing / field-service / research-studies for the learning path and either drop the other two courses or rewrite them around a distinct lesson (e.g. make field-service about scheduling-window validation and research-studies about soft-delete/audit). As shipped, a learner doing all three reads the same 8,000 words three times. (effort: L; the decision itself is S)
2. Fix the fractional-cent claim. In a billing app, implement it: in `server/src/index.ts` `parseItem`, add `if (Math.round(item.amount * 100) !== Math.round(item.amount * 1000) / 10) throw new ValidationError("Amount must be whole cents.")` (or a cleaner `Number.isInteger(item.amount * 100)` check with an epsilon), plus a `{amount: 12.345} -> 400` case in `test/workflow.test.ts`. Otherwise strike the sentence from all three chapters. (effort: S)
3. Rewrite `07-TRACE-LAB.md` boundaries 1–6 to name the real code at each step: `client/src/App.tsx` submit handler -> `fetch` -> `app.param("id")`/`parseItem` -> `withTransaction` -> `COMMIT` -> the JSON envelope. Delete the five duplicate paragraphs. (effort: M)
4. Type the test file: add `let h: Awaited<ReturnType<typeof database>>` and parameter types (the sibling `warehouse-ledger/test/ledger.test.ts` already does this) so `npm run typecheck` actually covers the suite. (effort: S)
5. Pin `package.json` from `batch04/dependency-versions.json`, commit a lockfile, and state Node 22.16.0 / PostgreSQL 18.1 in the README setup block rather than only in VERIFICATION.md. (effort: S)
6. Replace the Questboard/DevDeck/Live Chat paragraph in `04-TESTING-AND-DEBUGGING.md` with a walkthrough of `test/database.ts` — specifically why `process.env.DATABASE_URL` must be set *before* `await import("../server/src/index.js")`. That import-order detail is the single most useful thing in this harness and the course never explains it. (effort: S)

## One-paragraph summary for the index
This is the best JS/TS + PostgreSQL CRUD lesson in the batch after `warehouse-ledger`: Astra replaced a naive `COUNT(*) OVER()`-in-one-query list endpoint with a `REPEATABLE READ READ ONLY` transaction that counts, clamps and pages consistently, made the status endpoint idempotent with `SELECT … FOR UPDATE`, added an `asyncRoute` wrapper so a rejected promise becomes a 500 instead of a hung request, and fixed a silent seed bug where every `due_date` was null. The four tests run against a real PostgreSQL schema and one of them injects a failing trigger to prove the status update actually rolls back — that is a pattern worth stealing. The course prose is accurate on the code (line references check out exactly) but it is a noun-swap of two sibling courses, its trace lab repeats one paragraph six times, and it claims a fractional-cent validation that the billing code does not have. Do this one, skip `field-service` and `research-studies`, and read `server/src/index.ts` and `test/database.ts` directly instead of chapter 7.
