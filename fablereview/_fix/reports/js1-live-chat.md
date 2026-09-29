# JS1/live-chat — fix report (B06)

Fable, 2026-09-17.

## Done
- review#1 tests decoupled: the study room is created in before(); test 1 creates "seminar" for its 201 and keeps the duplicate-slug 409
- review#3 two new tests: >16KB frame closes that socket with 1009 while HTTP keeps serving; a 2001-character body is dropped and never persisted
- review#2 02-CONCEPTS teaches LISTEN/NOTIFY with the real trigger before it is used
- review#4 / 2.2 six distinct trace-lab boundaries (07)
- 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows the changed connectSocket guard and listener
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 (05, 06)
- review#5 harness walkthrough (04)
- review#6 / 2.7 dependencies pinned to the versions Astra verified with (ws 8.21.3)

## Skipped
- (none)

## Verification
- npm install (pinned) -> added 157 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL (PostgreSQL 18, 127.0.0.1:55439) -> # tests 4 / # pass 4 / # fail 0 (2 delivered + 2 new)
- npm run typecheck -> clean
- npm run build -> vite built in 3.03s
- node_modules and dist removed; package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against server/src/index.ts 126-157 and 204-216
- 07 boundaries cite App.tsx 30/72/80, api.ts WS_URL, index.ts 95/108/140/150/183/204, schema.sql trigger
- 02 LISTEN/NOTIFY section quotes the real trigger from server/db/schema.sql
