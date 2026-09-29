# _Organized Desktop/08 App And Product Projects/job track — fix report (B08)

Fable, 2026-09-18.

## Done
- review#4 02 section on undefined vs null vs absent with the before/after Zod lines
- review#3 fourth test: absent keeps, "" clears to null, invalid value is 400 with the row unchanged, for location and job_url
- review#1 README and VERIFICATION pin Node 22.16 and give the better-sqlite3 rebuild fallback; engines.node added to server/package.json
- review#5 server test script is `node --test ../test/*.test.js` (Node 22 expands the glob; a bare directory is rejected by Node 22.16)
- review#2 / 2.2 six distinct trace-lab boundaries (07)
- 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows the transforms and the merge block
- 2.4 three concrete variations
- harness section (04)
- new test corrected twice against the real contract (POST requires role + applied_date; updates are PUT; responses wrap rows in { item })

## Skipped
- (none)

## Verification
- npm install --prefix server -> added 156 packages
- cmd /c npm test -> # tests 4 / # pass 4 / # fail 0 (3 delivered + three-state test for location/job_url); two earlier runs of this report were written before the test passed and have been replaced
- server/node_modules removed

## Course/code consistency check
- 03 excerpt re-read against server/src/validation.js optional schemas and routes/applications.js merged block (PUT /:id at line 126)
- 07 boundaries cite ApplicationsPage.jsx, middleware/auth.js requireAuth, utils.js parseOrRespond, routes/applications.js 126-175
- 02 three-state section matches the transform lines and the merge block
