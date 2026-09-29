# Asset Checkout — Fable review

- **Path:** `JS1/asset-checkout`  ·  **Wave:** 1  ·  **Stack:** TypeScript + Express + PostgreSQL (`pg`, full-text search) + React/Vite  ·  **Batch:** B04
- **Astra's change (one line):** The asset list now runs `COUNT(*)` and the page query in one `REPEATABLE READ READ ONLY` transaction with a clamped page and an `id ASC` tie-breaker; `PATCH /:id/status` reads the row `FOR UPDATE`, returns it unchanged when the status already matches and otherwise writes the row plus its activity entry in one transaction; inputs are UUID/date/bounds-validated; a real seed bug is fixed (`json_to_recordset(... "dueDate" text)` instead of `due_date text`, which was silently dropping the seeded due dates); `pg.types.setTypeParser(1082, v => v)` keeps DATE columns as calendar strings; and the toolbar CSS grid becomes two flexible columns.
- **Course size:** 8,151 words across 9 files  ·  **Tests claimed:** 4  ·  **Tests found on disk:** 4 (`test/workflow.test.ts`, helper `test/database.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 4 | 5 | 3 | 5 | 4 | 4 | 3 | 2 | 3.8 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- Astra found and fixed a genuine pre-existing data bug rather than inventing one. `server/db/schema.sql` seeded from `json_to_recordset('[... "dueDate":"2026-07-30" ...]') AS x(..., due_date text, ...)`; PostgreSQL matches record columns to JSON keys by name, so `due_date` never matched `dueDate` and every seeded asset had a NULL due date. The fix quotes the key: `AS x(..., "dueDate" text, ...)` with `SELECT ..., "dueDate"::date`. This is exactly the class of bug a junior should learn to spot.
- `server/src/db.ts:5-6` adds `pg.types.setTypeParser(1082, value => value)` with the comment "A calendar date is a label, not a local-midnight timestamp." That is the single most useful line in the batch for anyone who has ever shipped an off-by-one-day date bug, and the test asserts the round trip (`assert.equal(made.data.dueDate,'2028-02-29')`).
- The status route is now genuinely atomic and idempotent: `SELECT * FROM items WHERE id=$1 FOR UPDATE`, early return when `current.rows[0].status === status`, then the `UPDATE` and the `INSERT INTO activity_entries` on the same client. Test 4 installs a `BEFORE INSERT` trigger on `activity_entries` that raises on `kind='status'`, asserts 500, asserts the item is unchanged and the activity count is still 1, drops the trigger, and then asserts the same request now succeeds — a proper restore-and-reverify.
- The pagination fix mirrors `forum-search` but is proven harder: the test creates three records with the **same** title, sorts by `title` (guaranteed ties), asserts the id order is identical across two identical requests, then `page=999` clamps to page 2 with one item, an absent search clamps to page 1 with total 0, and `page=1.5&pageSize=Infinity` falls back to 1/6.

## Problems found (evidence required)
- **[D6/D1]** The "Tested behavior" fixture in `astraupskill/VERIFICATION.md:18` says: `Create "Camera kit for field interviews" in Laptop with status Available, amount 12.50 and dueDate 2028-02-29`. `test/workflow.test.ts:7` actually uses `{title:'A lesson record', owner:'Junior Learner', category:"Laptop", ...}`; no test anywhere creates "Camera kit for field interviews". The same invented title is repeated in `03-WORKED-CHANGE.md:13`, `04-TESTING-AND-DEBUGGING.md`, `05-PRACTICE.md`, `06-SOLUTIONS-AND-REVIEW.md` and `07-TRACE-LAB.md`. The behaviour described is real; the literal fixture a learner is told to reproduce is not what is on disk.
- **[D8]** `02-CONCEPTS.md` sections "Invariants", "Validation versus normalization", "State transitions and failure boundaries", "Identity, representation and derived values" and "Small design decisions deserve explanations" are byte-identical across **all 48** `JS1/*/astraupskill/02-CONCEPTS.md` files. `astraupskill/README.md` and `JS1/equipment-maintenance/astraupskill/README.md` differ by 25 lines out of 72 — and those 25 are almost entirely the PostgreSQL setup block, not teaching content.
- **[D8/D1]** `04-TESTING-AND-DEBUGGING.md` contains "For Poll Studio and Kanban Flow, jsdom runs the actual app.js against its HTML and fresh browser storage…" — a paragraph about stages 21-22 with no relevance to this project.
- **[D7]** `test/workflow.test.ts` is minified: the six bad-payload cases are one line, and each test body packs 5-10 statements per physical line. This is the 4-test, 8,151-word flagship of the batch and its tests are the hardest to read.
- **[D3]** `05-PRACTICE.md` exercise prompts are single sentences ("Add a checkout/return history view"), and `06-SOLUTIONS-AND-REVIEW.md` repeats one identical **Review** paragraph under each exercise.
- **[D2, minor]** The CSS change (`client/src/styles.css:13`, `.toolbar` from `1fr 160px 160px 160px` to `repeat(2, minmax(0,1fr))`) is presented as a teaching point in the course scope sentence, but it is a cosmetic accommodation for the Playwright assertion `searchBox.width >= 150` at `batch03/browser_checks.mts:48`. Mixing a harness-driven layout tweak into the lesson's headline change dilutes it.
- **[D5]** All dependencies are `"latest"` with no lockfile; VERIFICATION.md discloses this.

## Spot-checks performed
- Claim "The excerpt below comes from server/src/index.ts near line 107" (`03-WORKED-CHANGE.md:19`) -> read `server/src/index.ts:107` -> **matches** exactly.
- Claim "Seed dates map to the intended column" (`03-WORKED-CHANGE.md:9`) -> diffed `batch03/backups/35/server/db/schema.sql` against the shipped `server/db/schema.sql` -> the only change is `due_date text` -> `"dueDate" text` and `due_date::date` -> `"dueDate"::date`; **matches**, and the original really was broken.
- Claim `Create "Camera kit for field interviews"` (`VERIFICATION.md:18`) -> `test/workflow.test.ts:7` uses `title:'A lesson record'` -> **does not match**.
- Claim VERIFICATION.md "Automated test cases: **4**" -> 4 `test(` blocks on disk; **matches** (this is the only 4-test project in the batch).
- Claim VERIFICATION.md "Chromium interaction | Passed" -> `batch03/browser-checks.json` project 35 records `"responsive_check": "390px no horizontal overflow; 1280px usable search width"`, and both `batch03/logs/35-browser.png` and `batch03/logs/35-mobile.png` exist, matching the two viewport assertions in `browser_checks.mts:48-52`; **matches**.
- Independent check: `diff -rq batch03/stage/35 JS1/asset-checkout` differs only by `client/dist`; **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Replace the fabricated fixture title in `astraupskill/VERIFICATION.md:18` and in chapters 03, 04, 05, 06, 07 with the literal fixture from `test/workflow.test.ts:7`, or rename the fixture in the test to "Camera kit for field interviews" so the two agree. (effort: S)
2. Promote the seed bug and the DATE type-parser to their own chapter-2 section: show the broken `json_to_recordset` column list, explain PostgreSQL's case-folding of unquoted identifiers, and show what `SELECT due_date FROM items` returned before and after `setTypeParser(1082, …)`. Replace the generic "Identity, representation and derived values" section with it. (effort: M)
3. Move the `.toolbar` CSS change out of the headline scope sentence into a short "incidental fixes" note in `VERIFICATION.md`, so the lesson's claim is about transactions and pagination. (effort: S)
4. Reformat `test/workflow.test.ts` to one statement per line and re-paste it into `03-WORKED-CHANGE.md`. (effort: S)
5. Delete the "For Poll Studio and Kanban Flow…" paragraph from `04-TESTING-AND-DEBUGGING.md` and expand the `05-PRACTICE.md` exercises with starting state, acceptance example and target file. (effort: M)

## One-paragraph summary for the index
This is the most complete course in the batch and the one with the most real engineering in it: an actual seed bug (`json_to_recordset` matching JSON keys by unquoted lower-cased column name, so every seeded `dueDate` was NULL), a DATE type-parser so calendar dates stop drifting by a timezone, a row-locked idempotent status transition whose audit write shares the transaction, and a count+page query under `REPEATABLE READ` with a clamped page and an id tie-breaker. Four tests back all of it, including one that installs a PostgreSQL trigger to fail the audit insert, checks the rollback, drops the trigger and re-verifies success. The catch is that the fixture the course tells you to reproduce (an asset named "Camera kit for field interviews") does not exist in the test file, and roughly two thirds of the 8,151 words are the same template shared with 47 other courses. Do it after `support-tickets`; it is worth the 8,000 words for the date and transaction material alone.
