# newcodexJS/11-survey-builder — fix report (B07)

Fable, 2026-09-17.

## Done
- review#3 surveySchema now requires ISO-8601 date-times for start_date/end_date (z.string().datetime({ offset: true }))
- review#3 regression test: "next tuesday" as start_date is 400, an ISO date-time is 201 (test/responses.test.ts; request() gained a headers argument)
- review#2 02-CONCEPTS section on lock granularity with the two failing alternatives
- review#1 / 2.2 six distinct trace-lab boundaries (07)
- review#4 / 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows the changed submitResponse and assertAccepting
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 on the owner-side routes (05, 06)
- harness walkthrough (04)
- review#5 root package renamed from astra-crud-workspace-62; pg and tsx declared at the root; README already carries the Toolchain block

## Skipped
- (none)

## Verification
- npm install (workspaces) -> added 247 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 4 / # pass 4 / # fail 0 (3 delivered + date-window test)
- npm run build -> built in 17.77s
- node_modules and dist removed; root package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against services/surveyService.ts submitResponse and assertAccepting
- 07 boundaries cite PublicSurveyPage.tsx, services/api.ts:42, surveyRoutes.ts:51, validate.ts, surveyService.ts 60/176, surveyModel.ts 170, utils/http.ts, middleware/errors.ts
- 02 lock-granularity section matches the forUpdate() at surveyService.ts:179
