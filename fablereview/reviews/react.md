# Quiz board studio (folder `react`) — Fable review

- **Path:** `_Organized Desktop/04 JavaScript Training/react`  ·  **Wave:** 2  ·  **Stack:** vanilla browser ES modules + localStorage + Web Locks; Node 22 static server; Playwright 1.60 (**no React at all despite the folder name**)  ·  **Batch:** B16
- **Astra's change (one line):** Rebuilt a broken Jeopardy MVP (its `index.html` loaded `scripts/*.js` and `styles/styles.css` paths that do not exist, and duplicated all four script tags) into a working CRUD lab: `store.js` with schema validation/migration/Web-Locks save, `edit.js` draft isolation, `main.js` controller that publishes state only after `setItem` succeeds, `server.js` allowlist static server, 20 node tests and 11 Playwright scenarios.
- **Course size:** 3,921 words across 9 files  ·  **Tests claimed:** 31 (20 node + 11 Chromium) + 6 syntax gates  ·  **Tests found on disk:** 20 in `test/store.test.js`, 11 specs in `e2e/board.spec.js`

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 5 | 3 | 5 | 5 | 4 | 5 | 4.6 |

**Verdict:** KEEP    **Path role:** elective

## What Astra did well
- Every defect the course narrates is real in the backup. `backups/6844a7b03c83/index.html` loads `scripts/data.js`… twice (before and after the DOM) and `styles/styles.css`, none of which exist next to the files; `backups/.../edit.js` `saveEditorChanges` does `data[cIndex].questions = pairs;` **before** `localStorage.setItem`, and `main.js` closes the modal unconditionally after calling it. That is exactly the "state changed before persistence succeeded" story 03-WORKED-CHANGE.md tells.
- The fix teaches the right discipline: draft is a `structuredClone` with a remembered raw baseline; `BoardStore.save` takes a Web Lock, re-reads storage, compares against the baseline, and only returns an accepted snapshot after `setItem` returns. Failure leaves the old board visible and the draft open.
- Astra refuses to let the folder name mislead: README.md:3 and the course README both say "Despite the historical folder name, it is vanilla JavaScript… Read the code as browser modules rather than looking for React components that are not present." Naming the limitation up front is the honest call.
- Browser evidence is genuine, not asserted. `checks/quiz-board/final/browser.json` contains 11 named Playwright specs with `expected: 11, unexpected: 0`, including "actual Web Locks coordinate two simultaneous tab saves" and "static server serves only app assets"; `store.tap` ends `# tests 20 / # pass 20 / # fail 0`.
- The original `section.innerHTML = \`<h3>${cat.category}</h3>\`` injection path was replaced with text assignment, and there is a browser test for it ("import renders hostile-looking names literally").

## Problems found (evidence required)
- **[D4]** This is the weakest fit in the batch for the stated target stacks. There is no React, no Express/Next, no SQL, no auth — `server.js` is a 7-file static allowlist with "no database or mutation endpoint" (01-CODEBASE-MAP.md). All server/HTTP/SQL work is deferred to `05-PRACTICE.md` exercises 3-5 as "proposed extensions". A junior doing only this course learns CRUD *reasoning* but writes zero server code.
- **[D7]** The delivered source is written in an extremely dense one-statement-per-line style that is hard to read or extend. `test/store.test.js` packs 20 tests into 26 lines (7,399 bytes); a single line is `test('legacy data migrates deterministically...', () => { const before=JSON.stringify(defaultData),a=parseState(before),b=parseState(before);assert.deepEqual(a,b);...});`. `server.js` fits its whole request handler into 3 lines. Learners are asked to read these files closely.
- **[D7]** `npm run test:browser` will fail on a fresh machine unless `npx playwright install chromium` is run first. The root `README.md` "Verify" block does include that line, but `astraupskill/VERIFICATION.md` does not repeat it and simply says "The project exposes `npm test` and `npm run test:browser`".
- **[D8, minor]** The course lands on the same vocabulary as other Astra browser-storage courses in this batch ("exact baseline comparison", "retained draft", "explicit confirmed replacement"). Here the content is genuinely project-specific (clue reveal, used-clue references, new round), so it reads as a house style rather than a template, but the phrasing overlap with `buildsubbox` is noticeable.

## Spot-checks performed
- README claims `npm start` serves `http://127.0.0.1:4173` and "only the app's seven assets" → `server.js` has `port = Number(process.env.PORT || 4173)`, binds `'127.0.0.1'`, and `allowed` is a 7-entry Set (`index.html, styles.css, main.js, board.js, edit.js, data.js, store.js`) → **matches**.
- 03-WORKED-CHANGE claims the earlier editor "changed the shared question array before calling localStorage.setItem" and "could also close the editor as though the operation succeeded" → `backups/6844a7b03c83/edit.js:44` then `:47`, and `backups/.../main.js` save handler → **matches**.
- VERIFICATION claims "all 31 tests passed (20 Node and eleven Chromium)" → `checks/quiz-board/final/store.tap` (`# pass 20`) and `browser.json` (`stats.expected: 11, unexpected: 0`) → **matches, not overclaimed**.
- 01-CODEBASE-MAP claims `store.js` `validateState` "checks schema version, revision, category and question counts, stable IDs, required text, point values and used-question references" → `store.js` `validateState` does all seven (`schemaVersion !== 1`, `revision` safe-integer, `categories.length > 10`, `questions.length > 20`, `identity()` regex + duplicate Set, `text()` bounds, points multiple-of-100 range) → **matches**.
- Delivery claims "two reviewed screenshots" → `astraupskill/images/desktop.png`, `narrow.png` present and duplicated in `checks/quiz-board/final/` → **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Reformat `test/store.test.js`, `e2e/board.spec.js` and `server.js` to normal multi-line style (a formatter pass, no behavior change). These are the files the course tells a junior to read line by line; right now they are effectively minified. (effort: S)
2. Add `npx playwright install chromium` to the command block in `astraupskill/VERIFICATION.md` so the reproduce steps stand alone. (effort: S)
3. Promote `05-PRACTICE.md` exercise 3 ("Move the question bank behind HTTP") into a worked companion chapter with a concrete Express + SQLite target and an `If-Match`/version-column conflict rule mapped onto the existing baseline comparison. Without it this course never touches the target stack. (effort: M)
4. Rename or add a note at the repo root (`README.md` already does this well) and in the batch index so nobody sequences this as a React course. (effort: S)

## One-paragraph summary for the index
Do this one for the concurrency and draft-safety lesson, not for React — there is no React in it despite the folder name. The original was a broken Jeopardy demo whose script tags pointed at directories that did not exist and whose editor mutated the live question array before writing to localStorage, closing the modal whether or not the save worked. Astra's rebuild separates draft from accepted state, validates a full candidate before persisting, takes a Web Lock and compares the exact saved text as a baseline so a second tab cannot be silently overwritten, and keeps corrupt saved data until the user explicitly replaces it. Eleven real Chromium scenarios (including two tabs racing through the actual Web Locks API) back the claims. The gap is that everything stays in the browser: budget a follow-up on HTTP and SQL, and expect to reformat some very densely written source before you can comfortably read it.
