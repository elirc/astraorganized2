# newcodexJS/01-task-manager — Fable review

- **Path:** `newcodexJS/01-task-manager`  ·  **Wave:** 1  ·  **Stack:** Node + Express + Knex + PostgreSQL (server), Vite client  ·  **Batch:** B01
- **Astra's change (one line):** Three small hardening edits in `server/src/services/taskService.js` — id parsing now uses `Number.isSafeInteger` with an int4 upper bound (`> 2147483647`) so an oversized id is a 400 instead of a database error, titles are rejected above 255 characters before hitting the column, and `buildUpdatePayload` lets an overdue task be re-saved with its *existing* due date while still enforcing the future-date rule for a changed one — plus a new real-HTTP/real-Postgres regression suite.
- **Course size:** 5,720 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`server/test/tasks.test.cjs`, plus harness `server/test/database.cjs`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 4 | 5 | 4 | 5 | 4 | 3 | 4.3 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The test suite is the real deliverable and it is the right kind. `server/test/tasks.test.cjs` drives actual HTTP (`api.request('POST','/api/tasks', …)`) through the real Express app and then reads the row back with Knex (`await db('tasks').where({ id }).first()`). It covers the full C-R-U-D arc in one test — create → filter by priority → mark done (asserting `completed_at` is set) → reopen (asserting `completed_at` is back to `null`) → delete → 404 — which is exactly the loop a junior needs to internalise.
- The invalid-input test asserts the row count before and after, so "400 returned" is proved to mean "nothing was written": `assert.equal(Number((await db('tasks').count('* as count').first()).count), before)`.
- The test harness is safety-engineered and worth reading on its own. `server/test/database.cjs:4-9` refuses to run unless `ASTRA_TEST_DATABASE_URL` names a database matching `^astra_test_[a-z0-9_]+$`, then creates a uniquely named schema per run, applies the real migration into it, and drops only that schema. A junior who copies this pattern will never truncate their dev database.
- The overdue-edit fix is a genuinely subtle product rule handled well, and the comment says why: `// An overdue task must remain editable when its existing date is submitted.` (`server/src/services/taskService.js:266-270`). The third test proves both halves — same past date succeeds, a *different* past date is a 400.
- `VERIFICATION.md` is honest: it lists only `tests` and `build`, and correctly **omits** the "Real Chromium browser interaction" row that projects 01–06 carry, matching `implementation/browser-checks.json`, which contains entries for projects 01–06 only.

## Problems found (evidence required)
- **[D2]** The production change is five lines. `diff` of `implementation/backups/07/server/src/services/taskService.js` against the current file shows exactly three hunks: `Number.isInteger` → `Number.isSafeInteger(...) || id > 2147483647`, an inserted `if (title.length > 255) throw …`, and the `due_date` branch. The course README headline ("a complete CRUD boundary") and 5,720 words oversell what is largely a new test suite bolted onto existing code. That is still valuable, but the framing is inflated.
- **[D2]** The `title.length > 255` check is placed *before* the empty check (`taskService.js:115` vs `:117`), so the ordering is fine, but there is no corresponding bound on `description`, which the same course teaches you to look for. An unbounded `description` still reaches the column.
- **[D1/D7]** `04-TESTING-AND-DEBUGGING.md` opens with the README's setup paragraph copy-pasted verbatim, including its forward reference: "The regression tests use a separate database through `ASTRA_TEST_DATABASE_URL`; **see chapter 4**" — printed inside chapter 4. A junior following the pointer goes in a circle.
- **[D8]** `04-TESTING-AND-DEBUGGING.md` also carries a paragraph written for other projects: "For the plain browser projects, jsdom runs the actual app.js against its HTML. The helper supplies browser APIs missing from jsdom and a controllable timer clock." There is no jsdom and no `app.js` in this project. `02-CONCEPTS.md` shares 37 of 41 lines with the other nine B01 courses; `05-PRACTICE.md` shares 42 of 47.
- **[D3]** `03-WORKED-CHANGE.md`'s "Three variations to work through" names no actual variations.
- **[D5]** Running the suite requires a local PostgreSQL 18-class server, a hand-created `astra_test_*` database and a user with `CREATE SCHEMA` rights. Chapter 4 documents this well (including a PowerShell `$env:` line), but there is no `docker run` fallback, no `.env.example` pointer for the test URL, and nothing tells the learner what to do if `createdb` is unavailable — the single biggest drop-off point for a junior on a fresh machine.

## Spot-checks performed
- Course claim (`03-WORKED-CHANGE.md`): excerpt of `buildUpdatePayload` "near line 243". -> `grep -n "function buildUpdatePayload" server/src/services/taskService.js` returns `243`, and the 36-line body matches exactly, including the `// An overdue task must remain editable…` comment. -> **matches.**
- Course claim (`VERIFICATION.md`): "editing its title with that same due date succeeds, but changing it to another past date fails." -> test 3 inserts a `2020-01-01` task, `PUT`s `{title:'Still relevant', due_date:'2020-01-01'}` expecting 200 and asserting the stored title changed, then `PUT`s `{due_date:'2020-01-02'}` expecting 400. Implementation at `taskService.js:266-270`. -> **matches.**
- Course claim (`README.md` Scope): "The API rejects unsafe ids and titles longer than the database column." -> `taskService.js:41` (`!Number.isSafeInteger(id) || id < 1 || id > 2147483647`) and `:115`; test 2 asserts `GET /api/tasks/9007199254740992` is a 400. -> **matches.**
- Course claim (chapter 4): "Each run creates a uniquely named schema, runs the existing migrations there, and drops only its own schema." -> `server/test/database.cjs:24-37`: `CREATE SCHEMA "${schema}"` with a random suffix, `await up(db)`, then `DROP SCHEMA "${schema}" CASCADE` with the comment "Only the unique schema created above is removed". -> **matches.**
- Honesty check: does `VERIFICATION.md` claim a browser check? -> No; the table lists only `tests` and `build`, consistent with `implementation/browser-checks.json` covering projects 01–06 only. -> **matches** (no overclaim).
- Delivery claim: 3 test cases, 5,720 words. -> 3 `test(` blocks; `wc -w astraupskill/*` totals 5,720. -> **matches.**

## Improvements needed (ordered, concrete, actionable)
1. Fix `astraupskill/04-TESTING-AND-DEBUGGING.md`: delete the copy-pasted "Run the checks" paragraph with its circular "see chapter 4" pointer, and delete the jsdom/`app.js` paragraph that belongs to the browser projects. Effort: S.
2. Add a Docker fallback to chapter 4 so a junior without a local Postgres can still run the suite — e.g. `docker run --rm -e POSTGRES_PASSWORD=local-test -p 5432:5432 postgres:18` plus the `createdb astra_test_learning` line — and state the required privilege (`CREATE SCHEMA`) explicitly. This is the course's main reproducibility risk. Effort: S.
3. Add a `description` length bound in `normalizeDescription` mirroring the new title bound, and a test case for it; the course teaches "bound every field that reaches a column" while leaving one unbounded. Effort: S.
4. Re-title the course honestly. "A complete CRUD boundary" describes the *test suite*, not the change; say so in `README.md` and add a short "what actually changed" list (three hunks, five lines) so the learner reads the diff before the prose. Effort: S.
5. Replace "Three variations to work through" with three concrete request bodies and expected status codes — `{title:'x'.repeat(256)}`, `{due_date:'2099-02-30'}`, `{}` (no fields → the `At least one task field must be provided.` branch) — the last of which is currently untested. Effort: S.

## One-paragraph summary for the index
The first of four server-side courses, and the place to start if you want to learn how CRUD APIs are actually tested. The code change itself is small — bounded task ids so an oversized number is a 400 rather than a database error, a title length check, and a rule that lets an already-overdue task be re-saved with its own past due date — but the new regression suite is the real lesson: it drives real HTTP through Express, reads rows back with Knex against a real PostgreSQL database, asserts `completed_at` flips on and off across done/reopen, and proves rejected input leaves the row count unchanged. The test harness refuses to run against anything but an `astra_test_*` database and creates a throwaway schema per run, which is a pattern worth stealing. Expect friction if you do not already have PostgreSQL running locally, because the course gives no container fallback, and ignore chapter 4's copy-pasted paragraph about jsdom, which belongs to a different project.
