# JS1/warehouse-ledger — fix report (B06)

Fable, 2026-09-17.

## Done
- review#1 / 2.2 six distinct trace-lab boundaries (07)
- review#3 / 2.3 per-exercise review criteria (06)
- review#2 lock-ordering exercise 7 with deadlock experiment (05, 06)
- 2.5 ownership/authz exercise 8 (05, 06)
- 2.4 excerpt shows the changed movement route and lockProduct
- 2.4 three concrete variations
- review#4 database.ts walkthrough (04)
- review#5 db:setup now `psql -f server/db/schema.sql` (relies on PGDATABASE/PG* env or DATABASE_URL via psql conventions, documented in README)
- review#6 / 2.7 dependencies pinned to the versions Astra verified with
- 07: duplicated "Explain the design tradeoff" section removed (2 -> 1)

## Skipped
- (none)

## Verification
- npm install (pinned) -> added 155 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL (PostgreSQL 18, 127.0.0.1:55439) -> # tests 3 / # pass 3 / # fail 0
- npm run typecheck -> clean
- npm run build -> vite built in 2.02s
- node_modules and dist removed; package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against server/src/index.ts 129-160 and lockProduct 311
- 07 boundaries cite App.tsx 76/98, api.ts, index.ts 233/255/311/219/206, db.ts
- exercises 7 and 8 reference real helpers (lockProduct, requireWarehouse, h.admin)
