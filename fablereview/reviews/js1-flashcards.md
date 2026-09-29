# JS1/flashcards — Fable review

- **Path:** `JS1/flashcards`  ·  **Wave:** 1  ·  **Stack:** vanilla JS + localStorage (jsdom tests, no framework/server)  ·  **Batch:** B02
- **Astra's change (one line):** Study sessions now snapshot card ids at start, add an "unlearned only" filter, restart when the deck filter changes, require revealing the answer before grading, advance past the last card into an explicit "Session complete" state, and roll back the cursor if the `localStorage` write throws.
- **Course size:** 5,144 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 (`test/study.test.cjs`, ~14 assertions, plus `test/browser.cjs` jsdom harness)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 3 | 3 | 4 | 4 | 4 | 3 | 3.8 |

**Verdict:** IMPROVE    **Path role:** elective

## What Astra did well
- The `grade()` excerpt in `03-WORKED-CHANGE.md` is byte-identical to `app.js:243` and the claimed line number is exact (verified programmatically).
- The change is a genuine state-machine fix, not cosmetic: `app.js:242-259` builds a replacement array, writes it, and only then advances `state.studyIndex`, so a quota failure leaves both the stored card and the cursor untouched. The test asserts exactly that (`test/study.test.cjs`, second test stubs `Storage.prototype.setItem` to throw and checks `state.studyIndex === 0` and the persisted `known === false`).
- The delivered files match the recorded `after_sha256` in `batch02/delivery-manifest.json` (I re-hashed all 171 batch files; 0 mismatches), and `logs/11-tests.log` really shows `# pass 2 / # fail 0`.
- A real Chromium check exists and is not a hand-wave: `batch02/browser_checks.cjs:43-48` drives the built app in Playwright, asserts the grade button is disabled before flip, asserts "Session complete", then **reloads** and re-reads `localStorage` — a genuinely different check from the jsdom suite. `logs/11-browser.png` is retained.

## Problems found (evidence required)
- **[D8]** The course is roughly two-thirds shared template. Measuring substantive lines (>40 chars) across the 10 B02 courses, only **37%** of flashcards' words are unique to this project. `05-PRACTICE.md` is ~95% identical to `JS1/budget-tracker/astraupskill/05-PRACTICE.md` — e.g. Exercise 3's whole body ("Create a failing example in a disposable fixture. Capture the state before the operation and after the failure…") is verbatim in both. Only one prompt sentence per exercise is project-specific.
- **[D8/D3]** `01-CODEBASE-MAP.md` contains the same generic Mermaid flowchart (`A[Input or user action] --> B[Validate and normalize] …`) in all ten B02 courses, with the disclaimer "This diagram names responsibilities, not necessarily separate files" — i.e. the course admits the diagram is not this project's architecture.
- **[D6]** `VERIFICATION.md` "Environment and limits" states "PostgreSQL tests used a separate local PostgreSQL 18.1 instance on port 55439 and uniquely named schemas in a dedicated test database." This project has no database and ran no PostgreSQL test (`checks.json` shows only a `node --test` run). The paragraph is shared boilerplate and reads as an inflated environment claim.
- **[D4]** The project is browser-only localStorage. It teaches write-then-publish ordering and state transitions, which transfer, but it contains no HTTP, no SQL, no ownership/authz, no transactions, and no React/Node — the target stacks of the rubric.
- **[D3]** There is no predict-then-run artifact the learner fills in; the "predict" instruction is prose ("Before running anything, write the exact expected stored values") with no table or answer key to check against beyond the test file itself.
- **[D5]** No `package-lock.json`; `jsdom: ^25.0.1` is a caret range, so `npm install` is not pinned.

## Spot-checks performed
- Claim: excerpt "comes from app.js near line 243" -> `grep -n '^function grade' app.js` returns 243, and the fenced block is a substring of `app.js` -> **matches**.
- Claim: "Grading requires revealing the answer" -> `app.js:244` `if (!card || !state.flipped) return;` plus `app.js:267-268` disabling both grade buttons when `!state.flipped` -> **matches**.
- Claim (README): "run `npm install`, then `npm test`" -> `package.json` has `"test": "node --test test/*.test.cjs"` and `devDependencies.jsdom` -> **matches**.
- Claim (VERIFICATION): "Automated test cases: 2" -> `batch02/logs/11-tests.log` `# tests 2 / # pass 2` -> **matches**.
- Claim (VERIFICATION): "Chromium interaction Passed" -> `browser-checks.json` records `{"project":"11","passed":true}` with no assertion detail, but `browser_checks.cjs:43` contains the actual assertions -> **matches, though the JSON alone would not have proved it**.
- Claim (VERIFICATION): "PostgreSQL tests used a separate local PostgreSQL 18.1 instance" -> no PG check for project 11 in `checks.json` -> **does not match / irrelevant boilerplate**.

## Improvements needed (ordered, concrete, actionable)
1. Delete the PostgreSQL/port-55439 sentence from `astraupskill/VERIFICATION.md` for this project and replace it with "Node 22.16.0, jsdom 25, no database" (effort: S).
2. Rewrite `05-PRACTICE.md` exercises 1-4 so the whole body, not just the first line, is about decks/cards — e.g. "Exercise 3: make `saveCards` fail on the *second* grade of a session and prove the first grade survived a reload" (effort: M).
3. Replace the generic Mermaid diagram in `01-CODEBASE-MAP.md` with a real state diagram of `manage <-> study`, `flipped`, `studyIndex`, `studyOrder` (effort: S).
4. Add a filled-in prediction table to `03-WORKED-CHANGE.md` (columns: action, `studyOrder`, `studyIndex`, `flipped`, stored `known`, visible text) with the answers moved to `06-SOLUTIONS-AND-REVIEW.md` (effort: M).
5. Add a third test covering "shuffle and restart mid-session does not lose an already-graded card's `known` flag", since `startStudy(true)` is reachable from the UI but untested (effort: S).

## One-paragraph summary for the index
A small, honest browser exercise about session state and failed writes. The code change is real and the two tests are good ones — they assert persisted state and cursor position after a simulated `localStorage` quota failure, not just that a message appeared. The weakness is the course itself: about two-thirds of it is a shared template reused across ten projects, so the exercises and the architecture diagram are generic, and the verification page claims a PostgreSQL environment this project never used. Do it if you want a clean drill on "write first, then publish, then advance" and on distinguishing a snapshot from a live filtered list. Skip it if you are short on time and need HTTP, SQL or React practice — the four API projects in this batch teach far more of the target stack.
