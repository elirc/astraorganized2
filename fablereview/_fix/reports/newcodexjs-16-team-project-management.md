# newcodexJS/16-team-project-management — fix report (B07)

Fable, 2026-09-17.

## Done
- review#2 dead `status: "active"` argument removed from restoreRecord (server/src/models/model.ts); "active" was never a status of this app
- review#5 bulk cap now applies after de-duplication (150 repeats of one id are accepted); regression test added
- review#4 02-CONCEPTS section on desired-state vs event commands and why version is not optimistic concurrency
- review#3 / 2.2 six distinct trace-lab boundaries (07)
- review#5 / 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows lifecycleUpdate and statusFields
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 (05, 06)
- harness and test-purpose section (04)
- root package renamed from astra-crud-workspace-67; pg and tsx declared at the root; README carries the Toolchain block

## Skipped
- review#1 (drop 17-20 courses) handled by the clone banners (sweep 2.10)

## Verification
- npm install (workspaces) -> added 244 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 5 / # pass 5 / # fail 0 (4 delivered + distinct-cap/restore test)
- npm run build -> built in 11.14s
- node_modules and dist removed; root package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against models/model.ts lifecycleUpdate (173) and statusFields (325)
- 07 boundaries cite App.tsx 100/125, services/api.ts 63-75, service.ts 54/188, model.ts 99/173, response.ts, errorMiddleware.ts
- 02 desired-state section matches the early returns in lifecycleUpdate; restoreRecord call site re-read after the dead-argument removal
