# Issue Desk — Fable review

- **Path:** `JS1/issue-desk`  ·  **Wave:** 1  ·  **Stack:** JavaScript (ESM) + Express (in-memory repository) + React/Vite  ·  **Batch:** B04
- **Astra's change (one line):** Added a `priority` filter dimension that composes with the existing `status` and `search` filters (client select -> `URLSearchParams` -> `repository.list`), plus a JSON-object body guard, a bounded-text guard in `validateIssue`, a 400 for unknown priority values, an exportable `app` and a `main.jsx`/`vite.config.js` entry so the client can actually be built and tested.
- **Course size:** 5,707 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 (`test/api.test.js`, helper `test/http.js`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 3 | 3 | 4 | 4 | 5 | 3 | 2 | 3.6 |

**Verdict:** IMPROVE    **Path role:** elective

## What Astra did well
- The filter composition is taught correctly and implemented correctly. `server/server.js:110-113` returns `matchesStatus && (priority === "all" || issue.priority === priority) && text.includes(search.toLowerCase())` — three independent predicates ANDed, which is exactly the point `02-CONCEPTS.md:7` makes ("A High issue can be Backlog or Done… OR would return unrelated records").
- The test is a genuine composition matrix, not a smoke test: `test/api.test.js` creates three issues that differ only in priority and status, then asserts `/api/issues?search=Astra&status=Backlog&priority=High` returns exactly one row, and that `?priority=Unknown` returns 400.
- Astra fixed a latent packaging defect while here: `client/index.html` previously loaded `/src/App.jsx` directly (no `createRoot` call, so the app never mounted under a plain build); it now loads the new `client/src/main.jsx`.
- The second test proves data integrity rather than error text: after three malformed PUTs it asserts `deepEqual` of the stored record against the pre-edit snapshot.

## Problems found (evidence required)
- **[D2]** Dead code was introduced. `server/server.js:155-156` declares `function whole(value, min, max)` and `function realDate(value)`; neither is called anywhere in the file (`grep -n "whole(\|realDate("` returns only the declarations). These are leftovers from Astra's shared generator for the date/amount projects and have nothing to do with the priority-filter lesson.
- **[D2]** The change is thin relative to its siblings. Beyond the filter, the only server work is three guard clauses; there is no transaction, ownership or persistence content because the repository is a module-level array (`server/server.js:94-150`). Compared to `JS1/support-tickets` or `JS1/invoice-studio` in the same batch, this is a 45-minute lesson padded to 5,707 words.
- **[D8]** Template smell. `02-CONCEPTS.md` sections "Invariants: a precise way to describe correctness", "Validation versus normalization" and "Small design decisions deserve explanations" are byte-identical across **all 48** `JS1/*/astraupskill/02-CONCEPTS.md` files; only the first section and one data-model paragraph are about issues. `astraupskill/README.md` differs from `JS1/equipment-maintenance/astraupskill/README.md` by 6 lines out of 63.
- **[D8/D1]** `04-TESTING-AND-DEBUGGING.md` contains a paragraph about *other* projects: "For Poll Studio and Kanban Flow, jsdom runs the actual app.js against its HTML and fresh browser storage…". Poll Studio and Kanban Flow are stages 21-22, not this project. A junior reading this course has no idea what that sentence refers to.
- **[D7]** `test/api.test.js` is minified (imports and two statements on line 1; each `test()` body is 3 lines with 5+ statements), while `03-WORKED-CHANGE.md` tells the learner to read it as "arrange → act → assert".
- **[D3]** `05-PRACTICE.md` Exercise 1 is one sentence and every **Review** paragraph in `06-SOLUTIONS-AND-REVIEW.md` repeats the same boilerplate sentence.

## Spot-checks performed
- Claim "The excerpt below comes from server/server.js near line 58" (`03-WORKED-CHANGE.md`) -> read `server/server.js:58` -> **matches** the quoted block exactly.
- Claim "The client sends state via URLSearchParams; the API checks the vocabulary" (`02-CONCEPTS.md:9`) -> `client/src/api.js:4` is `const params = new URLSearchParams(filters);`, called from `App.jsx:33` via `listIssues(filters)`, and the vocabulary check is `server/server.js:22-24`; **matches**.
- Claim VERIFICATION.md "Automated test cases: **2**" -> `test/api.test.js` has 2 `test(` blocks; **matches**.
- Claim VERIFICATION.md "Chromium interaction | Passed" -> `batch03/browser-checks.json` records project 32 passed against an "actual isolated HTTP server"; `batch03/browser_checks.mts:63-77` shows the stage-32 branch really drives the priority select (`getByLabel('Filter priority').selectOption('Low')`) and `batch03/logs/32-browser.png` exists; **matches**.
- Independent check: `diff -rq batch03/stage/32 JS1/issue-desk` differs only by `client/dist`; the checked tree is what shipped. **matches**.
- Claim implied by the "typed and bounded inputs" framing -> searched for callers of the new `whole`/`realDate` helpers -> **does not match**: they are unused.

## Improvements needed (ordered, concrete, actionable)
1. Delete the unused `whole()` and `realDate()` functions at `server/server.js:155-156`, or add the `estimate`/`dueDate` field the project README suggests so they have a purpose. (effort: S)
2. Delete the "For Poll Studio and Kanban Flow…" paragraph from `astraupskill/04-TESTING-AND-DEBUGGING.md` and replace it with one sentence about this project's helper (`test/http.js` starts the exported `app` on port 0). (effort: S)
3. Deepen the lesson so it earns its length: add a guided section on why the in-memory array loses data on restart and what would change if `repository` were backed by SQL, and add a third test covering `search` + `priority` with zero matches and with URL-encoded text. (effort: M)
4. Reformat `test/api.test.js` to one statement per line and re-paste it into `03-WORKED-CHANGE.md`. (effort: S)
5. Rewrite `astraupskill/05-PRACTICE.md` Exercises 1-4 with a starting state, an acceptance example and the file to edit, and give each a distinct **Review** paragraph in `06-SOLUTIONS-AND-REVIEW.md`. (effort: M)

## One-paragraph summary for the index
A short, correct lesson on why filter dimensions must be independent predicates rather than one encoded string, delivered on a small Express + React issue tracker with an in-memory repository. The code change and the two tests are honest — the composition test really does prove that High+Backlog+"Astra" matches exactly one of three near-identical records — and everything the course claims about the code checks out, including the line-58 excerpt. But the lesson is thin (there is no persistence, transaction or authorization content to learn here), Astra left two unused validation helpers behind at `server/server.js:155-156`, and most of the 5,700 words are the same template used by 47 other courses. Take it only if query-parameter validation and filter composition are a specific gap for you; otherwise do `support-tickets` or `invoice-studio` instead.
