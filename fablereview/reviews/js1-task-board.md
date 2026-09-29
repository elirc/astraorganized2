# JS1/task-board — Fable review

- **Path:** `JS1/task-board`  ·  **Wave:** 1  ·  **Stack:** vanilla JS + localStorage (jsdom tests)  ·  **Batch:** B01
- **Astra's change (one line):** Replaced the bare `tasks` array in localStorage with a versioned `{version, tasks, deleted}` document (with legacy-array upgrade), added a `commitBoard()` write-then-publish helper, and wired a one-level "Undo last deletion" button that survives reload and refuses to consume recovery data when the write fails.
- **Course size:** 5,079 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/undo.test.cjs`, plus harness `test/browser.cjs`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 4 | 4 | 5 | 4 | 4 | 3 | 4.1 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The code change is real and non-cosmetic. `deleteTask` captures `{task, index}` and `commitBoard` persists *before* mutating `state` (`app.js:121-133`), so a quota error leaves both the task and the undo record intact. The legacy-array migration in `loadBoard` (`app.js:62-69`) is a genuine data-migration lesson a junior will meet again.
- The tests exercise behaviour, not calls. `test/undo.test.cjs` reloads the app from a `snapshot()` of localStorage and asserts ids `['a','b','c']` and `deleted === null` afterwards; the third test monkey-patches `Storage.prototype.setItem` to throw and asserts `state.tasks.length === 3` plus the user-facing message.
- `07-TRACE-LAB.md` is genuinely project-specific and good: it separates id from index, shows `filter` is not a deep copy, and explains why two localStorage keys would break atomicity where one does not.
- Test-case count, word count and file list in `astraupskill/VERIFICATION.md` all match `astrafinalplan/implementation/delivery-summary.json` and `checks.json` (stage 01, exit 0). The "Real Chromium browser interaction" row is backed by real Playwright Chromium — `implementation/browser_checks.cjs:26,39-45` launches `chromium` and drives delete → reload → undo.

## Problems found (evidence required)
- **[D2]** The write-before-publish discipline the whole course is about is applied only to delete/undo. `saveTasks()` (`app.js:71-73`) and therefore the add/edit path in `handleSubmit` (`app.js:99-101`) still write unguarded and publish state first. A learner who internalises the lesson will immediately find the inconsistency and have no guidance on it; the course never mentions it.
- **[D8]** `astraupskill/02-CONCEPTS.md` is a shared template. Diffing it against `newcodexJS/03-expense-tracker/astraupskill/02-CONCEPTS.md` yields only 4 changed lines out of 41 — the sections "Invariants: a precise way to describe correctness", "Validation versus normalization", "State transitions and failure boundaries", "Identity, representation and derived values" and "Small design decisions deserve explanations" are byte-identical across the batch. Same for `05-PRACTICE.md` (42 of 47 lines identical; e.g. "Start by locating the current input, handler and output. Write an acceptance example before editing." appears verbatim in all ten projects).
- **[D3]** `03-WORKED-CHANGE.md` promises "Three variations to work through" but supplies no variations — only instructions to invent them ("change one ordinary value in the successful fixture while preserving its shape"). This paragraph is also identical in all ten B01 projects.
- **[D6]** `VERIFICATION.md:20` states "Database suites ran against a fresh, separate PostgreSQL 18.1 instance" in a project that has no database and no database suite. It is harness boilerplate, not a claim about this project, and it dilutes an otherwise honest record.
- **[D1, minor]** `README.md` says "Open index.html directly in a browser for the app." `app.js` reads/writes `localStorage` at module load; over `file://` that is blocked or origin-shared in several browsers. The verified path was a local HTTP server (`browser_checks.cjs:9-23`).

## Spot-checks performed
- Course claim: "The excerpt below comes from [app.js](../app.js) near line 121" for `commitBoard`. -> `grep -n "function commitBoard" app.js` returns `121`. -> **matches.**
- Course claim (`VERIFICATION.md`): "Real Chromium browser interaction | Passed". -> `implementation/browser-checks.json` has `{"project":"01","check":"browser","passed":true}` and `browser_checks.cjs:26` launches a real Chromium executable with Playwright. -> **matches** (not a fabricated browser claim).
- Course claim (`01-CODEBASE-MAP.md`): "The v2 document is {version: 2, tasks: [...], deleted: {task, index} | null}. A legacy array becomes a document with deleted: null." -> `app.js:62-73` `loadBoard`/`saveTasks`. -> **matches.**
- Course claim (`README.md` Scope): "Undo clears old filters so the restored task is visible." -> `app.js:158-159` sets `state.query = ""; state.status = "All"` and resets both inputs after a successful commit. -> **matches.**
- Delivery claim: 3 test cases, 5,079 words. -> `wc -w astraupskill/*` totals 5,079; `test/undo.test.cjs` has exactly 3 `test(` blocks. -> **matches.**

## Improvements needed (ordered, concrete, actionable)
1. Add a short chapter-3 subsection (or exercise 1 rewrite) that names the asymmetry explicitly: "`handleSubmit` still calls the unguarded `saveTasks()` at `app.js:99`. Route add/edit through `commitBoard` and predict which test would have caught the difference." Effort: S (docs only, no code change needed for a read-only follow-up).
2. Replace the generic "Three variations to work through" block in `03-WORKED-CHANGE.md` with three *concrete* task-board variations and their expected stored values (e.g. "delete `b`, add `d`, then undo — predict the resulting id order and why `splice(Math.min(index, tasks.length))` matters"). Effort: S.
3. Cut the two irrelevant boilerplate sentences from `VERIFICATION.md:20` (PostgreSQL, Recipeweb dependency tree) and replace with the one true environment line for this project: Node 22.16.0, jsdom 25, Playwright Chromium. Effort: S.
4. Fix the setup line in `README.md`: tell the learner to run a static server (`npx serve .` or `python -m http.server`) rather than opening `index.html` over `file://`. Effort: S.
5. Make `02-CONCEPTS.md` earn its length: replace at least two of the five shared sections with task-board-specific material (e.g. a state table for the four delete/undo/reload/failed-write transitions). Effort: M.

## One-paragraph summary for the index
A small, well-chosen first lesson: one localStorage value now holds both the visible tasks and the last deleted task, and every write persists before it publishes to memory. The change is real, the three jsdom tests genuinely reload the app and force a storage failure, and every line reference and excerpt in the course checks out against `app.js`. The trace lab on "id versus index" is the best part and worth doing even if you skip the rest. Its weaknesses are shared with the whole batch: the concepts and practice chapters are a cross-project template with four lines swapped, the "three variations" are never actually given, and the course never admits that the add/edit path still writes unguarded. Do it first (about two hours), then move to the Postgres API courses where the CRUD content is much denser.
