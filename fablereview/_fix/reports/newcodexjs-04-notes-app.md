# newcodexJS/04-notes-app — fix report (B02)

Fable, 2026-09-18.

## Done
- review#1 test split into four named blocks and review#4 tie-break test were completed by the earlier fix agent (verified on disk)
- review#1 VERIFICATION count updated to the four named blocks
- review#2 migration 002_search_index.js (GIN expression index) and an EXPLAIN walkthrough in 04
- review#3 01 diagram replaced with the real request path
- review#5 exercises 2 and 4 made concrete (ts_rank proof; language config with a stemming demonstration)
- 2.2 trace-lab call path section (07)
- 2.3 per-exercise review criteria (06)
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 (05, 06)
- finding: the earlier agent's four-block split stood up a schema per block and destroyed the shared Knex pool after block 1, so blocks 2-4 failed with "Unable to acquire a connection" and the run hung; the suite now sets up one schema and one server in before/after, uses distinct fixture words per block, and passes

## Skipped
- (none)

## Verification
- npm install (server) -> added 214 packages
- node --test test/search.test.cjs with ASTRA_TEST_DATABASE_URL -> # tests 4 / # pass 4 / # fail 0 (a first version of this report was written before the run finished and was wrong; replaced)
- server/node_modules removed

## Course/code consistency check
- 01 diagram, 04 EXPLAIN section and 07 call-path cite model.js 4, service.js 25/27, App.jsx 41-43, migration 002
- VERIFICATION count matches the four named blocks
