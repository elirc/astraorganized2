# JS1/flashcards — fix report (B02)

## Done
- [backlog 2.2] `astraupskill/07-TRACE-LAB.md` — replaced the single repeated boundary paragraph with **six distinct boundaries**, each naming the real file/function/line for this browser app and stating explicitly that the six in-process hand-offs are the analogue of a server request's six: input surface (`index.html:72-74`, listeners `app.js:74-77`) → intent-to-identity (`currentStudyCard`, `app.js:232-235`) → guard (`app.js:245`) → candidate construction (`app.js:246`) → persistence (`app.js:247-253`) → publish/render (`app.js:254-258`, `renderStudy` `app.js:261`). Line numbers checked against `app.js` on disk.
- [backlog 2.3 / review #4] `astraupskill/06-SOLUTIONS-AND-REVIEW.md` — the identical "Review: Demonstrate an ordinary case…" paragraph appeared 4×; replaced with four distinct review criteria naming the specific naive implementation each exercise invites (rebuild-vs-replay in ex.1, reusing `renderStudy`'s persistent count in ex.2, asserting only the final value in ex.3, "handle old data" as a non-decision in ex.4). Added an **answer key** for the new chapter-3 prediction table, including the failure row.
- [backlog 2.4] `astraupskill/03-WORKED-CHANGE.md` — added the pre-change `grade()` body from `backups/11/app.js:235-245` with the four defects annotated, so the excerpt now demonstrably contains changed lines; replaced the three abstract "variations" with **three concrete ones** (flip card `b` to `known:false` and predict the new `studyOrder`; delete the flip click and predict zero writes; a counting `setItem` stub that throws once, with the exact expected `studyIndex`/`flipped`/summary after each click).
- [review #4] `astraupskill/03-WORKED-CHANGE.md` — added the filled-in prediction table skeleton (action, `studyOrder`, `studyIndex`, `flipped`, stored `known`, visible text, button state) with answers moved to chapter 6.
- [review #2] `astraupskill/05-PRACTICE.md` — rewrote the **whole body** of exercises 1-4 (not just the prompt line) in terms of decks/cards/sessions; exercise 3 is now the review's suggested "make the write fail on the *second* grade and prove the first survived a reload".
- [review #3] `astraupskill/01-CODEBASE-MAP.md` — replaced the generic `flowchart LR` (identical across all ten B02 courses) with a real `stateDiagram-v2` of `Manage ↔ Study` and the `Empty / Hidden / Revealed / Complete` states, including the `Revealed --> Revealed` self-loop that represents a failed write, plus three paragraphs on what to read off it.
- [review #5] `test/study.test.cjs` — added a third test: grade card `a`, then `startStudy(true)` mid-session, and assert the cursor resets, the order is still length 2, and **both** persisted `known` flags survive; then tick "unlearned only" and assert the restarted session is empty with the "No matching cards" message. This covers the `startStudy(true)` path the review flagged as reachable-but-untested.
- [backlog 2.7] `package.json` — pinned `jsdom` from `^25.0.1` to `25.0.1` and generated `package-lock.json` by running the install.
- [review #1 — already satisfied by the sweep] the PostgreSQL/port-55439 sentence is gone from `VERIFICATION.md`. I strengthened the replacement to state explicitly "**no database and no server** … Nothing in this course requires PostgreSQL or any network access" and named jsdom 25.0.1.
- [review — honesty] `VERIFICATION.md` "Automated test cases" updated from 2 to 3 with a note to count assertions rather than `test()` blocks.

## Skipped
- [backlog 2.5 ownership/authz] Not applicable: browser-only localStorage project, no server, no actor concept. The plan scopes 2.5 to server projects.

## Verification
- `npm install --prefer-offline --no-audit --no-fund` (PowerShell, project root) → `added 60 packages in 2m`; `package-lock.json` created (`Test-Path` → `True`).
- `node --test test/study.test.cjs` → `# tests 3 / # pass 3 / # fail 0` (exit code 0). The new third test passes; the two delivered tests still pass unchanged.
- Line numbers cited in the new trace lab and diagram were read from `app.js` with `sed -n '218,262p'` before writing.

## Course/code consistency check
- Re-read `03-WORKED-CHANGE.md`, `07-TRACE-LAB.md`, `01-CODEBASE-MAP.md` against `app.js:53-62, 74-77, 222-235, 243-290` and `index.html:72-78` after editing; every cited line matches.
- `VERIFICATION.md` test count now matches the observed `# tests 3`.
- The new test uses only helpers that already exist in `test/browser.cjs` (`evaluate`, `event`, `w.localStorage`); no harness change was needed.
