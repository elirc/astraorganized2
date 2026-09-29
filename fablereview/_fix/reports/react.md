# _Organized Desktop/04 JavaScript Training/react — fix report (B16)

Fable, 2026-09-18.

## Done
- review#2 VERIFICATION command block includes npx playwright install chromium
- review#3 08-HTTP-COMPANION.md: Express + node:sqlite bank API with If-Match/428/409 and a conditional UPDATE, client change, four tests, mapping table; linked from README
- review#4 the batch index note ("not a React course") is recorded in fablereview (LEARNING_PATH/SCOREBOARD update in Phase 3); the root README already says so
- review#1 test/store.test.js, e2e/board.spec.js and server.js reformatted with prettier in the pipeline (see report)

## Skipped
- e2e/board.spec.js was reformatted but the Playwright suite was not run (no browser dependencies installed)

## Verification
- prettier (single quotes, 100 cols) on the three files: 26/50/17 lines became 213/271/44; node --check server.js ok; node --test test/store.test.js: 20/20 passed

## Course/code consistency check
- 08 companion reuses validateState from store.js as the server validator; README links it; VERIFICATION now includes the playwright install line.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md`, before the first existing second-level heading: a prerequisites line naming what a learner should already know (and, where one exists, the sibling course that comes first) plus a 12-term glossary table whose third column names a real file, function, table or header in this project. Every location was checked against the source before it was written: store.js (BoardStore.save with expectedRaw, revision, validateState, migrateLegacy, STORAGE_KEY), edit.js createEditor draft, main.js (current, busy, valid, export-raw) and 08-HTTP-COMPANION.md.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `03-WORKED-CHANGE.md` — quoted from `store.js:48-62` (`BoardStore.save`)
- `04-TESTING-AND-DEBUGGING.md` — quoted from `package.json` test/test:browser/verify
- `06-SOLUTIONS-AND-REVIEW.md` — quoted from `test/store.test.js:106-119` (concurrent-save case)
- `07-TRACE-LAB.md` — quoted from `main.js:65-69` (storage event listener)
