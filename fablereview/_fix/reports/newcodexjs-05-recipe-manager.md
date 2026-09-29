# newcodexJS/05-recipe-manager — fix report (B01)

Fable, 2026-09-18.

## Done
- review#2 / P4 isPublic defaults to private when omitted (recipeService.ts:55); test proves a non-owner gets 403 unless isPublic: true was sent
- review#1 03 second excerpt and walkthrough of parseRecipeInput with one worked input per helper
- review#5/#6 04 "Run the checks" rewritten with the Docker fallback, privilege note and the JWT_ACCESS_SECRET note
- review#3 three concrete concurrency/authz variations
- review#4 06 worked example for the version column (exercise 1)
- 2.2 trace-lab call path section (07)
- 2.3 per-exercise review criteria (06)

## Skipped
- (none)

## Verification
- npm install (server) -> added 150 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 4 / # pass 4 / # fail 0 (3 delivered + private-by-default test)
- server/node_modules removed

## Course/code consistency check
- 03 second excerpt cut from recipeService.ts parseRecipeInput at run time
- 07 call-path cites recipeService.ts 17/88 and the ownership test; 06 version worked example matches the FOR UPDATE flow
