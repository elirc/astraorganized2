# JS1/room-booking — fix report (B02)

Fable, 2026-09-18.

## Done
- review#1 00-PREREQS.md, review#3 wrap() on POST, review#4 pins + lockfile, review#5 sequence-diagram timeline and review#2 datetime-local note were completed by the earlier fix agent (verified on disk)
- 2.2 trace-lab call path section (07)
- 2.3 per-exercise review criteria (06)
- 2.4 three concrete variations
- 2.5 exercise 4 (ownership) now has a worked solution with the owner predicate inside the statement (06)

## Skipped
- (none)

## Verification
- npm ci (pinned lockfile from the earlier agent) -> added 144 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 2 / # pass 2 / # fail 0
- npm run typecheck -> clean
- node_modules and dist removed

## Course/code consistency check
- 07 call-path cites App.tsx 68/79-80, api.ts 21/25, validation.ts 12/16, index.ts 73/88, schema.sql 30, error middleware
- 06 worked ownership solution matches the WITH ... RETURNING statement shapes in index.ts
