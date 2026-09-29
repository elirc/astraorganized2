# newcodexJS/01-task-manager — fix report (B01)

Fable, 2026-09-18.

## Done
- review#1/#2 04 "Run the checks" rewritten: no circular pointer, Docker fallback, CREATE SCHEMA privilege named
- review#5 new test: PUT {} is 400 "At least one task field must be provided." and the row is unchanged
- review#3 description bound (5000 characters) already present in normalizeDescription with a test case; verified, not re-added
- review#4 README title is honest and a "What actually changed" section points at the three hunks
- review#5 three concrete variations
- 2.2 trace-lab call path section (07)
- 2.3 per-exercise review criteria (06)
- 2.5 ownership/authz exercise 7 (05, 06)

## Skipped
- (none)

## Verification
- npm install (server) -> added 110 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 4 / # pass 4 / # fail 0 (3 delivered + empty-body test)
- server/node_modules removed

## Course/code consistency check
- 07 call-path section cites taskRoutes.js 7-13, taskService.js 38/108/131/162/249/281, taskModel.js 58/71
- README "What actually changed" checked against backups/07 diff (service hunks only)
