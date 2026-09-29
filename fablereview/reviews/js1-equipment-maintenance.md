# Equipment Maintenance — Fable review

- **Path:** `JS1/equipment-maintenance`  ·  **Wave:** 1  ·  **Stack:** JavaScript (ESM) + Express (in-memory repository) + React/Vite  ·  **Batch:** B04
- **Astra's change (one line):** `repository.setStatus` stops round-tripping through `update()` and instead returns the existing record untouched when the status already matches, otherwise writes the record and appends exactly one `kind:'status'` activity entry; `validateItem` gains shape/bounds guards and a real-calendar-date check (`new Date(v+"T00:00:00Z").toISOString().slice(0,10) === v`); list sorting gains an `a.id.localeCompare(b.id)` tie-breaker and the page number is clamped to `totalPages`; a JSON-object body guard and an exportable `app` are added.
- **Course size:** 7,306 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/workflow.test.js`, helper `test/http.js`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 4 | 4 | 3 | 4 | 4 | 5 | 3 | 2 | 3.6 |

**Verdict:** IMPROVE    **Path role:** elective

## What Astra did well
- The idempotency fix is the right one and is visible in the diff. The old `setStatus(id, status)` delegated to `this.update(...)`, which unconditionally appended an `"updated"` activity entry; the new version compares `existing.status === status`, returns early, and otherwise writes the record plus one `"status"` entry recording the actual transition ("Changed status from Open to Scheduled"). History now describes transitions, not clicks.
- Test 3 in `test/workflow.test.js` fires two concurrent `PATCH /status` requests with `Promise.all`, asserts both return 200, then asserts `entries.filter(x=>x.kind==='status').length === 1` and that the stored status is the new one — it proves the invariant, not just that the endpoint responds.
- Test 2 is the best-designed test in the in-memory family: it creates three records with the *same* title, sorts by `title` ascending (so ties are guaranteed), asserts the id ordering is identical across two identical requests, then checks `page=999` clamps to page 2 with one item and `total` still 3, an absent search clamps to page 1 with total 0, and `page=1.5&pageSize=Infinity` falls back to 1/6. Those are exactly the four ways naive pagination breaks.
- The date guard is real: `validDate` rejects `2027-02-29` (a string `Date.parse` happily accepts) by requiring the ISO round trip, and the test covers it.

## Problems found (evidence required)
- **[D8]** This project's course is a near-clone of four siblings in the same batch. Against `JS1/library-lending/astraupskill`, the nine files total ~575 lines and differ by only **~40 changed lines** (`README.md` 4, `01-CODEBASE-MAP.md` 4, `02-CONCEPTS.md` 6, `03-WORKED-CHANGE.md` 12, `04-TESTING-AND-DEBUGGING.md` 2, `05-PRACTICE.md` 10, `06-SOLUTIONS-AND-REVIEW.md` 16, `07-TRACE-LAB.md` 24, `VERIFICATION.md` 4) — roughly 93% identical. The same holds for `gym-membership`, `campaign-planner` and `volunteer-coordinator`. Separately, the `02-CONCEPTS.md` paragraph "Validation rejects values the operation cannot accept…" appears in all 48 `JS1/*/astraupskill/02-CONCEPTS.md` files.
- **[D1/D6]** The fixture the course tells you to create does not exist. `astraupskill/VERIFICATION.md:17` says `Create "Inspect west-wing ventilation" in HVAC with status Open, amount 12.50 and dueDate 2028-02-29`; `test/workflow.test.js:7` actually uses `{title:'A lesson record', owner:'Junior Learner', category:"HVAC", ...}`. The described behaviour is genuine, but the domain-flavoured title was written into seven course files and never into the code.
- **[D8/D1]** `04-TESTING-AND-DEBUGGING.md` contains a paragraph about other projects entirely: "For Poll Studio and Kanban Flow, jsdom runs the actual app.js against its HTML and fresh browser storage; the suite can force a storage-write failure." Poll Studio and Kanban Flow are stages 21-22. Nothing in this course explains what they are.
- **[D2]** Mechanical editing artefact: Astra prepended `import { pathToFileURL } from "node:url";` *above* the file's UTF-8 BOM, so `server/server.js` line 2 now begins with the bytes `EF BB BF` (`od -c` shows `357 273 277 i m p o r t   e x p r e s s`). It parses because U+FEFF is whitespace in ES source, which is why the build passed, but a stray BOM mid-file is exactly the kind of thing a junior will be baffled by.
- **[D4]** The persistence layer is a module-level array (`server/server.js:94-130`). There are no transactions, no SQL, no ownership checks and no durability — the CRUD lessons available here are validation, pagination and in-memory state, which is a narrower slice of the target skill set than `support-tickets`, `invoice-studio` or `asset-checkout` in the same batch.
- **[D3]** `05-PRACTICE.md` exercises are single sentences ("Show overdue open work orders"), and `06-SOLUTIONS-AND-REVIEW.md` repeats one identical **Review** paragraph under every exercise.
- **[D7]** `test/workflow.test.js` is minified (each test body is 3-6 physical lines holding 10+ statements), while `03-WORKED-CHANGE.md` instructs the learner to read it as arrange/act/assert. `04-TESTING-AND-DEBUGGING.md` also duplicates the `npm test` / `npm run build` block twice in a row (once as a PowerShell block, once as a bare `text` block).
- **[D5]** All dependencies in `package.json` are `"latest"` and there is no lockfile.

## Spot-checks performed
- Claim "The excerpt below comes from server/server.js near line 37" (`03-WORKED-CHANGE.md:19`) -> read `server/server.js:37` -> quoted block **matches** exactly.
- Claim "Repeating the current status creates no extra status history" -> read `server/server.js:116-124` (`if (existing.status === status) return existing;`) and `test/workflow.test.js` test 3 -> **matches**.
- Claim `Create "Inspect west-wing ventilation"` (`VERIFICATION.md:17`) -> `test/workflow.test.js:7` -> **does not match** (title is `'A lesson record'`).
- Claim VERIFICATION.md "Automated test cases: **3**" -> 3 `test(` blocks on disk; **matches**.
- Claim VERIFICATION.md "Chromium interaction | Passed" -> `batch03/browser-checks.json` project 36 `passed: true` with `"responsive_check": "390px no horizontal overflow; 1280px usable search width"`, and both `batch03/logs/36-browser.png` and `36-mobile.png` exist; `browser_checks.mts:38-52` shows the real domain flow (create via API, edit in the UI, change status, assert one status activity entry, add a note, then check both viewports); **matches** — this is a real browser check, not a claim.
- Independent check: `diff -rq batch03/stage/36 JS1/equipment-maintenance` differs only by `client/dist`; the tree that was tested is the tree that shipped. **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Decide that this project is the one survivor of its five-way clone family (see the `library-lending`, `gym-membership`, `campaign-planner`, `volunteer-coordinator` reviews) and invest the differentiating content here: add a chapter-2 section on why the in-memory repository loses everything on restart, what would have to change to move `createRepository()` behind SQL, and which of the three tests would then start failing. (effort: M)
2. Fix the fabricated fixture: replace `"Inspect west-wing ventilation"` in `astraupskill/VERIFICATION.md:17`, `01-CODEBASE-MAP.md`, `03-WORKED-CHANGE.md:13`, `04-TESTING-AND-DEBUGGING.md`, `05-PRACTICE.md`, `06-SOLUTIONS-AND-REVIEW.md` and `07-TRACE-LAB.md` with the literal fixture from `test/workflow.test.js:7`, or rename the fixture in the test. (effort: S)
3. Re-save `server/server.js` as UTF-8 without a BOM so the `EF BB BF` bytes stop sitting on line 2. (effort: S)
4. Delete the "For Poll Studio and Kanban Flow…" paragraph and the duplicated `npm test` code block from `astraupskill/04-TESTING-AND-DEBUGGING.md`. (effort: S)
5. Reformat `test/workflow.test.js` to one statement per line and re-paste it into `03-WORKED-CHANGE.md`; expand the six `05-PRACTICE.md` prompts with a starting state, an acceptance example and the file to edit, and give each a distinct **Review** paragraph. (effort: M)

## One-paragraph summary for the index
A small Express + React work-order tracker where the lesson is repeat-safe status history and explicit input contracts: a second `PATCH` with the status the record already has now returns the record untouched instead of appending another history row, sorting gets an id tie-breaker, out-of-range page numbers clamp instead of returning an empty page with a bogus total, and dates like `2027-02-29` are rejected. The three tests are well chosen — concurrent duplicate status requests, guaranteed sort ties, and six malformed edits followed by a `deepEqual` against the stored record — and the browser check is a real Playwright run with screenshots at two viewports. Two caveats: persistence is a module-level array, so there are no transactions or SQL to learn here, and this course is about 93% identical to four siblings in the same batch (`library-lending`, `gym-membership`, `campaign-planner`, `volunteer-coordinator`). Do this one and skip the other four.
