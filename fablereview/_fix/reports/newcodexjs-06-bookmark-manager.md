# newcodexJS/06-bookmark-manager — fix report (B02)

Fable, 2026-09-18.

## Done
- review#5 lockfiles for server/ and client/ were committed by the earlier fix agent (verified on disk)
- review#1 listRecords searches title/url/collection with escaped LIKE metacharacters instead of CAST(bookmarks AS TEXT); test proves % is literal and ids/timestamps do not match
- review#3 `declare module "*.module.css"` restored in client/src/vite-env.d.ts
- review#2/#4 README separates the junior lesson from the advanced appendix and gives a safe-host recipe
- 2.2 trace-lab call path section (07)
- 2.3 per-exercise review criteria (06)
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 (05, 06)
- review#5 VERIFICATION records the Zod/Knex/TS versions and the lockfiles
- finding: the delivered bookmarks test stood up its own schema and the harness cleanup destroys the Knex pool, so any second test in the file hung; the file now sets up one schema and server in before/after

## Skipped
- review#2 (full course split) done as a README-level separation of the junior lesson and the advanced appendix rather than moving files

## Verification
- npm ci (server) -> added 130 packages
- npx tsx --test test/bookmarks.test.ts -> # tests 2 / # pass 2
- cmd /c npm test (both files, metadata suite included) with ASTRA_TEST_DATABASE_URL -> # tests 5 / # pass 5 / # fail 0
- server/node_modules removed

## Course/code consistency check
- 07 boundaries cite service.ts 18/23/24/27 and the rewritten model.ts listRecords
- README appendix section checked against the metadata test file names
