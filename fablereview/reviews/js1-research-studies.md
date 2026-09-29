# Research Studies — Fable review

- **Path:** `JS1/research-studies`  ·  **Wave:** 1  ·  **Stack:** Node/Express + TypeScript + PostgreSQL (`pg`) + React/Vite  ·  **Batch:** B06
- **Astra's change (one line):** The same treatment as `subscription-billing`/`field-service` applied to the `/api/studies` resource — count+page inside one `REPEATABLE READ READ ONLY` transaction with `id ASC` tie-break and clamped page, `SELECT … FOR UPDATE` + no-op on unchanged status in `PATCH /:id/status`, `asyncRoute` error forwarding on every route, UUID `app.param` guard, runtime body validation with real calendar-date checking, `pg.types.setTypeParser(1082, v => v)`, and the `"dueDate"` seed-column fix in `server/db/schema.sql`.
- **Course size:** 8,383 words across 9 files  ·  **Tests claimed:** 4  ·  **Tests found on disk:** 4 (`test/workflow.test.ts`, harness `test/database.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 3 | 5 | 3 | 5 | 4 | 5 | 4 | 2 | 3.9 |

**Verdict:** IMPROVE    **Path role:** skip

## What Astra did well
- Same high-quality server change as its two siblings: consistent count/page under one read-only repeatable-read snapshot, stable `ORDER BY ${sort} ${direction}, id ASC`, `page = Math.min(filters.page, totalPages)`, and a status endpoint that compares the locked current row before writing anything.
- Real calendar validation, not a regex alone: `validDate` requires `/^\d{4}-\d{2}-\d{2}$/` **and** round-trips through `new Date(value + "T00:00:00Z").toISOString().slice(0,10) === value`, which is what actually rejects `2027-02-29`. Paired with `setTypeParser(1082, …)` so the stored date does not come back shifted by the server's timezone. This pairing is the genuinely instructive part of the change.
- Activity endpoints now verify the parent study exists (404) instead of returning an empty array or inserting an orphan.
- The course's domain facts are correct for this project: `01-CODEBASE-MAP.md:11` says "Statuses are Design, Recruiting, Running, Analysis, Complete. Categories are Usability, Market, Clinical, Internal", matching `server/src/index.ts:15-16`.
- Verification is honest: `logs/54-tests.log` = `# tests 4 # pass 4 # fail 0`, build/typecheck/browser entries present, and all 20 manifest hashes match the files on disk.

## Problems found (evidence required)
- **[D8]** Duplicate course. Against `JS1/field-service`: `02-CONCEPTS.md` differs by **2 of 45 lines**, `04-TESTING-AND-DEBUGGING.md` by **1 of 69**, `05-PRACTICE.md` by **1 of 47**, `07-TRACE-LAB.md` by **4 of 114**, `README.md` by **2 of 67**. `test/workflow.test.ts` is the same four tests with the status vocabulary swapped. A junior who has done subscription-billing learns nothing new here.
- **[D1]** `02-CONCEPTS.md:9` — "a **fractional cent is rejected** rather than silently rounded." Not implemented: `server/src/index.ts` `parseItem` checks only `!Number.isFinite(item.amount) || item.amount < 0 || item.amount > 9999999999.99`. The same paragraph also promises the scaffold "does not perform external billing, legal work, dispatch integration or research compliance checks" — one sentence written to serve four unrelated projects.
- **[D1/D8]** The data-model sentence says "The main record represents a study, coordinator, research category and **review date**" while the field is literally `dueDate` everywhere in code and JSON (`server/src/index.ts`, `shared/types.ts`, `client/src/App.tsx`). A junior grepping for `reviewDate` finds nothing. The abstraction is a leftover from the shared template's "amount/dueDate" record shape.
- **[D3/D1]** `07-TRACE-LAB.md` repeats one identical paragraph under all six "Boundary" headings, all pointing at `server/src/index.ts` and `parseItem`, including the two boundaries that describe the React client.
- **[D3]** `06-SOLUTIONS-AND-REVIEW.md` uses the same **Review:** paragraph for all four exercises.
- **[D8]** `04-TESTING-AND-DEBUGGING.md` discusses Questboard, DevDeck and Live Chat — none of which exist in this repository.
- **[D5]** Dependencies are all `"latest"` with no lockfile; `checks.json` shows verification ran from Astra's shared `implementation/node_modules` against `stage/54`, so `npm install && npm test` in this folder is documented but unexecuted.
- **[D2, minor]** `test/workflow.test.ts` is untyped JS in a `.ts` file (`let h;`), so `npm run typecheck` does not really cover it.

## Spot-checks performed
- "The excerpt below comes from `server/src/index.ts` near line 323" (`03-WORKED-CHANGE.md:19`) -> `grep -n "^function parseItem" server/src/index.ts` returns **323** -> matches exactly (and note it is 326 in the two siblings, so the numbers were generated per project, not copied).
- "Statuses are Design, Recruiting, Running, Analysis, Complete" -> `server/src/index.ts:15` -> matches.
- "Validate its shape and compare its parsed calendar components; 2027-02-29 has the right shape but is not a real day" (`02-CONCEPTS.md`) -> read `validDate`: regex + `Date.parse` + ISO round-trip equality -> matches, and `test/workflow.test.ts` asserts `{ dueDate: "2027-02-29" } -> 400`.
- "a fractional cent is rejected rather than silently rounded" -> read `parseItem` -> **does not match**.
- "review date" (`01-CODEBASE-MAP.md:11`) -> `grep -rn "reviewDate" .` returns nothing; the field is `dueDate` / `due_date` -> **does not match**.
- VERIFICATION "Automated test cases: 4" -> `batch04/logs/54-tests.log`: `# tests 4 # pass 4 # fail 0` -> matches.

## Improvements needed (ordered, concrete, actionable)
1. Drop this course from the path (keep `subscription-billing` as the trio's representative), or give it a distinct lesson. The natural research-domain one: participant enrolment caps and a soft-delete/withdrawal audit trail — add a `target_participants` column and an enrolment table in `server/db/schema.sql`, enforce the cap inside `withTransaction` with `FOR UPDATE`, and test two concurrent enrolments against the last slot. (effort: L)
2. Fix `01-CODEBASE-MAP.md:11`: replace "review date" with `dueDate` and note the `due_date` -> `dueDate` mapper, so the vocabulary in the course is greppable in the code. (effort: S)
3. Delete the fractional-cent sentence from `02-CONCEPTS.md`, `03-WORKED-CHANGE.md` and `07-TRACE-LAB.md`; this project's `amount` is a study budget with no cent rule. (effort: S)
4. Rewrite `07-TRACE-LAB.md` boundaries 1–6 with real per-boundary targets (`client/src/App.tsx` submit -> `fetch` -> `app.param`/`parseItem` -> `withTransaction` -> `COMMIT` -> `toItem` mapper) and delete the five duplicate paragraphs. (effort: M)
5. Give each exercise in `06-SOLUTIONS-AND-REVIEW.md` its own review criteria. (effort: M)
6. Type `test/workflow.test.ts` and pin `package.json` from `batch04/dependency-versions.json` with a lockfile. (effort: S)

## One-paragraph summary for the index
A PostgreSQL-backed study tracker where Astra applied a solid set of CRUD fixes — consistent count/page inside one repeatable-read transaction, a `FOR UPDATE` status endpoint that writes no history when nothing changed, an `asyncRoute` wrapper so rejected promises become 500s, and the one detail worth the whole lesson: a real calendar-date validator paired with `pg.types.setTypeParser(1082)` so a `DATE` column does not come back shifted by a timezone. The four tests hit a real database, and every verification claim matches the batch logs and file hashes. But the course is a noun-swap of `field-service` and `subscription-billing` (two differing lines out of forty-five in the concepts chapter), it calls the `dueDate` field a "review date" that does not exist in the code, and it claims a fractional-cent rule that is not implemented. Skip the course; if you want the date/timezone lesson, read `validDate` and `server/src/db.ts` directly.
