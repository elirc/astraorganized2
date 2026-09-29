# grokbuildhrproject — fix report (B14)

Fable, 2026-09-18.

## Done
- review#1 three before-snapshots and 15 evidence files copied; linked from 03 and VERIFICATION
- review#2 02 names the trade-off of the constant advisory lock; a two-line comment at chartLock points at it
- review#3 04 break-it section for the exclusion constraint and the PENDING guard, naming the existing tests
- review#4 06 worked solution for task 1 (validator, scope intersection, query key, four tests, documented intersect-vs-reject choice)
- review#5 README session boundaries

## Skipped
- review#4 task 1 solution is written in 06, not applied; the jest integration suite needs the PostgreSQL fixture

## Verification
- Only a two-line comment was added to employeeRepository.ts (no behavior change); no test run. Snapshots and evidence verified present under astraupskill/

## Course/code consistency check
- 02 lock paragraph matches the constant key in chartLock; 04 break-it names the two existing test titles from workflow.integration.test.ts.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md`, before the first existing second-level heading: a prerequisites line naming what a learner should already know (and, where one exists, the sibling course that comes first) plus a 12-term glossary table whose third column names a real file, function, table or header in this project. Every location was checked against the source before it was written: middleware/auth.ts (Actor, requireHr), repositories/scope.ts employeeScope, repositories/leaveRepository.ts (stale(), overlap, status guards, audit), repositories/employeeRepository.ts chartLock with pg_advisory_xact_lock, services/leaveService.ts approveLeave, the version columns in the migration SQL and frontend/src/hooks/useWorkspace.ts.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `04-TESTING-AND-DEBUGGING.md` — quoted from root `package.json` test scripts
- `07-TRACE-LAB.md` — quoted from `backend/src/repositories/leaveRepository.ts:239-251` (`decide` guards)
