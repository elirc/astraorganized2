# _Organized Desktop/02 Build Projects/buildsubbox — fix report (B16)

Fable, 2026-09-18.

## Done
- review#4 01 lists 16 exported symbols of src/model.js with line numbers
- review#2 02 glossary of 15 terms each tied to a src/model.js symbol
- review#1 05 rung 0: failing test supplied for a below-cost item rule, with the one-line fix and what a fixture failure means
- review#3 08-SERVER-COMPANION.md: POST /reservations with Idempotency-Key, UNIQUE(subscriberId, cycle), compare-and-set stock update, mapped onto reduce/replay; linked from README

## Skipped
- (none)

## Verification
- rung-0 test written to a temporary file and run: fails as intended ("Missing expected exception"), then removed; node scripts/test.mjs: 36/36 passed (unchanged suite)

## Course/code consistency check
- Glossary symbols and line anchors were generated from src/model.js exports; 08 companion maps to the real function names (reduce, replay, fingerprint, quoteBox, eligible).

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `03-WORKED-CHANGE.md` — quoted from `src/model.js:381-394` (`quoteBox` input contract)
- `06-SOLUTIONS-AND-REVIEW.md` — quoted from `src/repository.js:11-24` (`commit`)
- `07-TRACE-LAB.md` — quoted from `test/model.test.mjs:250-263` (replay / changed-cycle cases)
