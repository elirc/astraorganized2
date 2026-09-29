# JS1/subscription-billing — fix report (B06)

Fable, 2026-09-17.

## Done
- review#2: parseItem now rejects fractional cents (server/src/index.ts) — the course claim is now true
- review#4: test file typed (h, call) so `npm run typecheck` covers it; new `{ amount: 12.345 } -> 400` case
- 1.3 whole-cent sentence corrected to the implemented behavior (02, 03, 07)
- review#3 / 2.2 six distinct trace-lab boundaries (07)
- 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows the changed PATCH route and amount checks
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 with reference code and test (05, 06)
- review#6 database.ts walkthrough with the import-order detail (04)
- review#5 / 2.7 dependencies pinned to the versions Astra verified with (react 18.3.1, vite 8.2.2, express 4.22.2, pg 8.23.0, tsx 4.23.13, typescript 5.9.3)
- review#5 README already carries the Toolchain block (sweep); package-lock.json generated from the pinned install

## Skipped
- review#1 (drop the two clones) handled by the clone banners on field-service and research-studies (sweep 2.10)

## Verification
- createdb astra_test_fable + pgcrypto/btree_gist on the PostgreSQL 18 cluster at 127.0.0.1:55439
- npm install (pinned) -> added 155 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 4 / # pass 4 / # fail 0 (includes the new 12.345 -> 400 case)
- npm run typecheck -> clean
- npm run build -> vite built in 1.75s
- node_modules and dist removed; package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against server/src/index.ts PATCH route (186-220) and parseItem amount checks
- 07 boundaries cite App.tsx 113/125, api.ts request<T>, index.ts 30/186/326, db.ts 22
- 02/03/07 whole-cent sentence matches the new parseItem check
