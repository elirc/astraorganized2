# newcodexJS/15-api-tester — fix report (B07)

Fable, 2026-09-17.

## Done
- review#1 02-CONCEPTS section on the owner-row lock, its cost and two alternatives (partial unique index, ordered environment locks)
- review#2 / 2.2 six distinct trace-lab boundaries (07)
- review#4 / 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows the changed activation and variable replacement
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 on collections/folders/requests (05, 06)
- review#4 project-specific debugging section (04)
- review#3 README names the transferable skill and positions the course as an elective
- review#5 root package renamed from astra-crud-workspace-66; pg and tsx declared at the root; README carries the Toolchain block

## Skipped
- (none)

## Verification
- npm install (workspaces) -> added 258 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 4 / # pass 4 / # fail 0
- npm run build -> built in 21.58s
- node_modules and dist removed; root package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against models/environmentModel.ts activateEnvironment (73) and replaceVariables (92)
- 07 boundaries cite services/api.ts 58, routes/index.ts, validate.ts, environmentService.ts 38, environmentModel.ts 73/92/135
- 02 lock section matches the users forUpdate() at environmentModel.ts 29/49/75
