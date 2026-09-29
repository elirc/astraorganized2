# JS1/task-board — fix report (B01)

## Done
- [P4 "JS1/task-board … create branch still uses unguarded `saveTasks()`" / review #1] **Code fix.** `handleSubmit` now builds a replacement array (`[task, ...state.tasks]` on create, `map` on edit) and routes it through `commitBoard(nextTasks, state.deleted)`, so create and edit obey the same persist-then-publish rule as delete/undo; the success message moved after the write. `saveTasks()` is kept (a delivered test calls it) but is now commented as the raw, unguarded write used only by fixtures. Files: `app.js:71-104`.
- [P4 regression test] Added two cases to `test/undo.test.cjs`: "creating a task persists before publishing and keeps the undo record" (asserts stored order `['New task','a','c']` and `deleted.task.id === 'b'`) and "failed storage on create adds no task and does not consume recovery data" (asserts `state.tasks.length === 2`, recovery intact, `/Could not save/`). Suite is now 5 cases.
- [review #1 / backlog 2.4] New `03-WORKED-CHANGE.md` subsection "The changed lines in `handleSubmit`" showing the real before (cited to `implementation/backups/01/app.js:84-92`) and after (`app.js:94-101`) hunks and the three observable consequences. Also added a note on why `saveTasks` survives.
- [backlog 2.4 / review #2] Replaced the generic "Three variations to work through" block with three concrete task-board variations (delete→add→undo ordering; delete-last-then-delete-another under one-level undo; undo into a shrunken array and what `Math.min(index, tasks.length)` buys) each with a stated prediction and what to assert.
- [review #4] `README.md` + `04-TESTING-AND-DEBUGGING.md` setup paragraph rewritten: serve over HTTP (`npx serve .` / `python -m http.server 8000`) instead of opening `index.html` over `file://`, with the reason (module-load `localStorage` read, blocked/shared `file://` origins).
- [review #5] `02-CONCEPTS.md`: two of the five shared template sections replaced with project-specific material — "State transitions and failure boundaries in this board" (a 7-row state table over create/delete/reload/undo/no-op-undo/duplicate-undo/failed-write, plus why the unreachable rows are unreachable) and "Identity, representation and derived values in this board" (id vs index vs derived list vs derived button state, the `T00:00:00` date-parsing trap, JSON as the atomicity carrier).
- [backlog 2.2] `07-TRACE-LAB.md`: added "The six boundaries of one delete-and-undo round trip" — six distinct paragraphs (DOM input surface `app.js:31-58`/`:211`; normalization `:80-88`; action guards `:89-92`,`:136-137`,`:146-151`; intended-change computation `:94-96`,`:138`,`:151-152`; persistence boundary `commitBoard:122-133`; publication/render `:130-131`,`:178-214`) plus a backwards trace from the failure. The old duplicated `filter`-is-not-a-deep-copy snippet was folded into boundary 4 rather than left twice.
- [backlog 2.3 / 3.11] `06-SOLUTIONS-AND-REVIEW.md`: each of the four exercises now has real code (accessible announcement after a successful commit; bounded two-level undo stack with v1/v2/v3 upgrade in `loadBoard`; quarantine-on-unreadable-JSON `loadBoard`; three-option multi-tab policy with a `storage` listener) and a **distinct** review paragraph naming the specific trap, the demonstration, and the invariant that must not move. The identical "Demonstrate an ordinary case…" sentence is gone (grep count 0).
- [backlog 2.3] Added a concrete answer section for the new chapter-5 exercise-0 question.
- [review #1, learner side] `05-PRACTICE.md` exercise 0 now asks the learner to diff `backups/01/app.js:84-92` against `app.js:94-103` and name which of the five tests would have failed against the old create path.
- [backlog 2.7] `npm install --prefer-offline` run; `package-lock.json` now committed to the tree (was absent). No `"latest"` dependency existed here (`jsdom: ^25.0.1`).
- [VERIFICATION] Test count corrected from 3 to 5 with the split stated, the two new scenarios described, and the follow-up run recorded.

## Skipped
- Backlog 2.5 (ownership/authz exercise): not a server project, no user/actor concept, no routes. The cross-tab section of exercise 4 is the nearest analogue and points forward to the API courses.
- Backlog 2.1/2.6/2.8/2.9/2.10/1.15: already applied by the wave-1 sweep; verified present (VERIFICATION.md now carries the Node-only environment line and the diff-reading note, no PostgreSQL sentence) and not redone.
- Review #3 (strip PostgreSQL/Recipeweb sentences from `VERIFICATION.md:20`): already done by the sweep — confirmed by reading the file.

## Verification
- `npm install --prefer-offline --no-audit --no-fund` → `added 60 packages in 3m`
- `node --test test/undo.test.cjs` (before my change, 3 cases) → `# tests 3 / # pass 3 / # fail 0`
- `node --test test/undo.test.cjs` (after code change + 2 new cases) → `# tests 5 / # pass 5 / # fail 0`
- Note: `node --test test/` (directory form) fails on Node 22.16.0 with `Cannot find module …\test` (MODULE_NOT_FOUND). Named file or `npm test` works. Recorded in VERIFICATION.md.
- Line references re-derived after the edit (`grep -n "function …" app.js`): `saveTasks:73`, `handleSubmit:77`, `commitBoard:122`, `deleteTask:135`, `undoDelete:145`, `getVisibleTasks:170`, `render:178`; all citations in the course updated (03's "near line 121" → 122).

## Course/code consistency check
- `03-WORKED-CHANGE.md` re-read against `app.js:94-104` and `:122-133` — excerpt and both hunks match byte-for-byte.
- `02-CONCEPTS.md` state table checked row by row against `handleSubmit`, `deleteTask`, `undoDelete`, `loadBoard` and `commitBoard`; the "failed write publishes nothing" row is the one tests 3 and 5 assert.
- `07-TRACE-LAB.md` line citations checked individually against the post-edit file.
- `README.md` Scope updated to say *every* write path persists before publishing (it previously said only delete and undo do), which is now true.
- `04-TESTING-AND-DEBUGGING.md` "What the test suite proves" extended with cases 4 and 5.
