# JS1/secure-notes — fix report (B06)

Fable, 2026-09-17.

## Done
- review#1: session expiry implemented in server/server.js (tokens store {userId, expiresAt}; requireAuth deletes an expired token and answers 401; SESSION_TTL_MS env for tests, default 8h)
- review#1: regression test for expiry (test/notes.test.js, 4th test)
- review#2 README scope separates pre-existing behavior from the delivered change
- review#1 02-CONCEPTS explains why expiry belongs to the session store
- review#3 / 2.2 six distinct trace-lab boundaries (07)
- 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows the changed lines
- 2.4 three concrete variations
- review#4 exercise 7: 404-vs-403 with enumeration experiment and test (05, 06)
- review#5 harness description (04)
- review#6 / 2.7 dependencies pinned (kept the glob test script: Node 22 expands it; a bare directory is rejected)

## Skipped
- (none)

## Verification
- npm install (pinned) -> added 117 packages
- cmd /c npm test -> # tests 4 / # pass 4 / # fail 0 (Node 22.16.0; includes the new expiry test with SESSION_TTL_MS=40)
- npm run build -> vite built in 2.07s
- node_modules and dist removed; package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against server/server.js (JSON guard, register, GET /api/notes/:id, validateNote)
- 07 boundaries cite App.jsx 53/134/161, api.js, server.js 16/141/157/187, routes 94-127
- 02 expiry section, README scope and VERIFICATION count match the new code and test
