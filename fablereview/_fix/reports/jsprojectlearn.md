# JSProjectLearn — fix report (B15)

Fable, 2026-09-18.

## Done
- review#1 README setup block: Node 22, npm ci, playwright install, the four commands
- review#2 VERIFICATION stamped 2026-09-18 with literal per-file counts (11/12+2 it.each/16)
- review#3 02 names the server-side analogue of each local mechanism
- review#4 01 in-scope/out-of-scope table for src/game/

## Skipped
- (none)

## Verification
- Documentation-only change (no code or tests touched), so no test run; edited files re-read for headings/links after the script; per-file test counts measured with a regex (engine 11 it, storage 12 it + 2 it.each, learning.spec 16 test)

## Course/code consistency check
- README setup block matches package.json scripts; 01 table lists files that exist in src/game/.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md`, before the first existing second-level heading: a prerequisites line naming what a learner should already know (and, where one exists, the sibling course that comes first) plus an 11-term glossary table whose third column names a real file, function, table or header in this project. Every location was checked against the source before it was written: src/game/storage.ts (persistProgress revision/epoch check, browserLock, serializeProgress), src/game/schema.ts (normalizeProgress, validateAgainstCatalog, boundedJson, MAX_SAVE_BYTES), src/game/drafts.ts read/writeMissionDrafts, src/game/notes.ts updateNote and src/App.tsx commitProgress.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `03-WORKED-CHANGE.md` — quoted from `src/game/notes.ts:14-28` (`updateNote`)
- `04-TESTING-AND-DEBUGGING.md` — quoted from `package.json` test/build/test:browser commands
- `06-SOLUTIONS-AND-REVIEW.md` — quoted from `src/game/storage.test.ts:136-157` (reset identity case)
- `07-TRACE-LAB.md` — quoted from `src/game/storage.ts:20-36` (`persistProgress`)
