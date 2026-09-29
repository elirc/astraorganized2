# buildsmallplates — fix report (B18)

Fable, 2026-09-18.

## Done
- review#1 the three deleteWorkout/deleteSet call sites branch on the boolean (close on true, "already removed" alert on false); 05 exercise 7 asks the same for updateSet with the repository-must-not-own-the-copy argument
- review#2 updateSet validates while it binds in one pass over the mapping; regression test: a field outside the mapping is neither validated nor bound
- review#3 orienting paragraph first, drill/summary paragraph last in README, 01, 04, 07
- review#4 the "Root observed / Root's successful locked install" sentences are gone; 04 states the locked install plainly
- review#6 VERIFICATION reproduce block uses the vitest command that package.json runs; Jest phrasing dropped
- review#5 08-WEB-TRANSLATION.md: PATCH /sets/:id with 200/404/400/409 mapped onto the boolean contract

## Skipped
- (none)

## Verification
- npx vitest run --maxWorkers=1 --testTimeout=30000 via junctioned stage node_modules: 10 files, 93 passed (92 delivered + 1 mapping test); npx tsc --noEmit exit 0 (the Alert branches and the single-pass updateSet compile); junction removed

## Course/code consistency check
- 05 exercise 7 describes the three call sites as changed; 08 maps the boolean contract the tests pin; VERIFICATION command matches package.json.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md`, before the first existing second-level heading: a prerequisites line naming what a learner should already know (and, where one exists, the sibling course that comes first) plus a 12-term glossary table whose third column names a real file, function, table or header in this project. Every location was checked against the source before it was written: src/db/repos.ts (updateSet, bump, dbVersion, finishWorkout, newId use), src/db/database.ts (withTransactionSync, PRAGMA user_version, the two ON DELETE CASCADE columns), src/core/setValidation.ts assertValidSetNumber and src/state/hooks.ts useDbQuery.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `04-TESTING-AND-DEBUGGING.md` — quoted from `package.json` (`vitest run`, `tsc --noEmit`)
- `07-TRACE-LAB.md` — quoted from `src/db/repos.ts:433-467` (`updateSet`)
