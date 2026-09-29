# grokbuildecommerceproject — fix report (B14)

Fable, 2026-09-18.

## Done
- review#1 8 full-final evidence files copied and linked from VERIFICATION
- review#2 03b-BREAK-IT.md with three predicted failures; review#5 README prerequisites and task 3 flagged as a stretch goal
- review#3 06 worked solution for task 2 (schema, validation, repository with conditional write + receipt, route, concurrency integration test)
- review#4 04 explains the three deliberate 500s and the optional 503 mapping

## Skipped
- review#3 the task 2 solution is a written reference (schema, validation, repository, route, test), not applied code; the integration suite needs the PostgreSQL fixture

## Verification
- Documentation and evidence copies only; no code changed, so no test run. Evidence files verified present under astraupskill/evidence/

## Course/code consistency check
- 03b names the three guards by their actual lines in orderRepository.ts; 04 attributes the three 500 log lines to the auditFailure helper that exists in workflow.integration.test.ts.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `04-TESTING-AND-DEBUGGING.md` — quoted from root `package.json` test scripts
- `07-TRACE-LAB.md` — quoted from `backend/src/repositories/orderRepository.ts:85-102` (checkout advisory lock + receipt lookup)
