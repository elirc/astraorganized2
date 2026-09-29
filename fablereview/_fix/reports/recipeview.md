# recipeview — fix report (B08)

Fable, 2026-09-17.

## Done
- review#1 03 documents the fail() change and where the real error goes; VERIFICATION notes it
- review#2/#3 04: duplicated command block removed; harness sentence now describes the temp-directory SQLite harness
- review#4 fourth test: malformed ids rejected on PATCH, a rejected dish rename leaves search_index unchanged, a zero-padded id resolves to the same row
- 2.2 six distinct trace-lab boundaries (07)
- 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows the h() wrapper and validatePayload
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 (05, 06)
- finding: ids were validated but not canonicalized; h() now rewrites validated ids to canonical decimal, documented in 03
- test 4 creates its own dish because test 3 deletes the shared fixture

## Skipped
- review#5 already satisfied after the sweep (VERIFICATION names Node 22.16 and no PostgreSQL)

## Verification
- npm ci -> added 211 packages
- cmd /c npm test -> # tests 4 / # pass 4 / # fail 0 (3 delivered + write-path id and search-index test); an earlier run of this report claimed 4/4 before the fix landed and was corrected here
- npm run typecheck -> clean
- npm run build -> vite built in 7.95s
- node_modules and dist removed

## Course/code consistency check
- 03 excerpt re-read against server/index.ts h() and validatePayload; the new canonicalization line sits inside h()
- 07 boundaries cite src/api.ts 45, index.ts 69/94/600, db.ts 18/39-51
