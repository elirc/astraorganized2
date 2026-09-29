# Forum Search — Fable review

- **Path:** `JS1/forum-search`  ·  **Wave:** 1  ·  **Stack:** TypeScript + Express + PostgreSQL full-text search (`websearch_to_tsquery`) + React/Vite  ·  **Batch:** B04
- **Astra's change (one line):** `GET /api/threads` now runs the count and the page query inside one `REPEATABLE READ READ ONLY` transaction, clamps the requested page to `ceil(total/pageSize)` before computing the offset, adds `t.id ASC` as a tie-breaker after the `ts_rank`/`created_at` ordering, validates UUID path params via `app.param("id")`, and funnels async route rejections through an `asyncRoute` wrapper.
- **Course size:** 6,696 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 (`test/feature.test.ts`, helper `test/database.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 4 | 5 | 3 | 5 | 4 | 3 | 3 | 2 | 3.6 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- This is the best code change in the batch for teaching pagination. The original derived `total` from `COUNT(*) OVER()` on the returned rows (`const total = rows[0] ? Number(rows[0].total) : 0`), which returns 0 for any page past the end. The replacement runs a separate `COUNT(*)` and the row query in one `REPEATABLE READ READ ONLY` transaction so the two agree on a snapshot, then clamps `page = Math.min(page, Math.max(1, Math.ceil(total/pageSize)))` before the offset. Both the "count and rows disagree" and the "empty page N" failure modes are covered by one coherent fix.
- The ordering tie-breaker is real and necessary: `ORDER BY ts_rank(...) DESC, t.created_at DESC, t.id ASC`. With seeded threads created in the same transaction, `created_at` ties are common, so page boundaries were genuinely unstable before.
- The test proves stability rather than asserting a single call: it issues the same query twice and `deepEqual`s the returned id arrays, then asks for `page=999` and asserts `total` is still 3, `page` is 2 and one item comes back — plus an empty-result case that must clamp to page 1 with `total` 0.
- The second test counts rows in the database before and after five malformed POSTs (`{tagNames:[{}]}`, `{tagNames:['']}`, `{authorId:'bad'}`, a well-formed but nonexistent UUID author, `{title:4}`) and asserts the thread count is unchanged — that proves "no partial thread", not just "got a 400".

## Problems found (evidence required)
- **[D6/D1]** VERIFICATION.md's "Tested behavior" describes a scenario that is **not tested**. It says: "Create six threads matching a unique search, visit page two, delete its only item, then fetch page two again. The response reports the clamped first page with five rows and total five." The actual `test/feature.test.ts` creates **three** threads with `pageSize=2`, never calls `DELETE`, and asserts page 2 with **one** item and total 3. The counts, the delete step and the outcome are all different. The same invented paragraph is repeated in `01-CODEBASE-MAP.md:57`, `03-WORKED-CHANGE.md:13`, `04-TESTING-AND-DEBUGGING.md:44`, `05-PRACTICE.md:9`, `06-SOLUTIONS-AND-REVIEW.md:13` and `07-TRACE-LAB.md:11`, and `07-TRACE-LAB.md:21` even tabulates "Request old page 2 -> Page 1 with five rows" as an expected observation. A junior who follows the course literally will build a six-thread fixture and get results that do not match the stated expectation.
- **[D8]** The generic template again: the "Invariants", "Validation versus normalization" and "Small design decisions deserve explanations" sections of `02-CONCEPTS.md` are byte-identical across all 48 `JS1/*/astraupskill/02-CONCEPTS.md` files. `astraupskill/README.md` differs from `JS1/support-tickets/astraupskill/README.md` by 6 lines out of 72.
- **[D8/D1]** `04-TESTING-AND-DEBUGGING.md` carries the cross-project boilerplate paragraph "For Poll Studio and Kanban Flow, jsdom runs the actual app.js against its HTML…", which is about stages 21-22, not this project.
- **[D7]** `test/feature.test.ts` is minified (line 1 holds three imports; each test body is 3-5 lines containing 10+ statements), yet `03-WORKED-CHANGE.md` tells the learner to read it as arrange/act/assert.
- **[D3]** `05-PRACTICE.md` exercises are one-sentence stubs and each **Review** paragraph in `06-SOLUTIONS-AND-REVIEW.md` is the same boilerplate sentence.
- **[D5]** All dependencies are `"latest"` in `package.json` with no lockfile; the course correctly warns about this but does not pin anything.

## Spot-checks performed
- Claim "The excerpt below comes from server/src/index.ts near line 34" (`03-WORKED-CHANGE.md:19`) -> read `server/src/index.ts:34` -> the quoted block **matches** character-for-character, including `SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY`.
- Claim VERIFICATION.md "Tested behavior: create six threads… delete its only item… five rows and total five" -> read `test/feature.test.ts` -> **does not match** (3 threads, no delete, 1 row, total 3).
- Claim VERIFICATION.md "Automated test cases: **2**" -> 2 `test(` blocks on disk; **matches**.
- Claim VERIFICATION.md "typecheck | Passed" -> `batch03/checks.json` has project 33 `typecheck` `exit_code: 0` (90.76s) and `batch03/logs/33-typecheck.log` exists; **matches**.
- Claim VERIFICATION.md "Chromium interaction | Passed" -> `batch03/browser-checks.json` project 33 passed with "disposable PostgreSQL schema", `batch03/logs/33-browser.png` exists, Playwright launch at `browser_checks.mts:21`; **matches**.
- Independent check: `diff -rq batch03/stage/33 JS1/forum-search` differs only by `client/dist`; the verified tree is what shipped. **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Fix the false fixture narrative. Replace the "six threads / delete / five rows / total five" sentence in `astraupskill/VERIFICATION.md`, `01-CODEBASE-MAP.md:57`, `03-WORKED-CHANGE.md:13`, `04-TESTING-AND-DEBUGGING.md:44`, `05-PRACTICE.md:9`, `06-SOLUTIONS-AND-REVIEW.md:13` and `07-TRACE-LAB.md:11/21` with the scenario the test actually runs (three threads tagged `lesson`, `pageSize=2`, `page=999` -> page 2, one item, total 3, plus the empty-search case). This is the highest-priority fix in the batch. (effort: S)
2. If the delete-then-reread scenario is pedagogically wanted, add it as a third test in `test/feature.test.ts` (create 6, read page 2, `DELETE` that thread, re-read page 2, assert clamp to page 1 with 5 rows) and bump the count in VERIFICATION.md. (effort: M)
3. Add a short section to `astraupskill/02-CONCEPTS.md` explaining what `REPEATABLE READ` does and does not buy here (it is a read-only snapshot, not a lock; concurrent inserts are invisible to this request but visible to the next), replacing one of the generic sections. (effort: M)
4. Reformat `test/feature.test.ts` to one statement per line and re-paste it into `03-WORKED-CHANGE.md`. (effort: S)
5. Delete the "For Poll Studio and Kanban Flow…" paragraph from `04-TESTING-AND-DEBUGGING.md`. (effort: S)

## One-paragraph summary for the index
The code change here is the best pagination lesson in the batch: the original computed the total from `COUNT(*) OVER()` on the returned rows, so any page past the end reported zero matches, and Astra replaced it with a real `COUNT(*)` plus the page query inside one `REPEATABLE READ READ ONLY` transaction, a page clamp, and an `id` tie-breaker so ties in `ts_rank`/`created_at` cannot shuffle page boundaries. The two tests genuinely prove those properties, including counting rows in the database to show that five malformed POSTs create nothing. The serious flaw is honesty: VERIFICATION.md and six other files all describe a "six threads, delete one, five rows, total five" scenario that appears nowhere in `test/feature.test.ts` (which uses three threads and no delete), so fix that before handing this to a junior. Worth doing for the SQL pagination and full-text-search material, with chapter 2 skimmed.
