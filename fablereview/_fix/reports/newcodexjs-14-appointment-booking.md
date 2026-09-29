# newcodexJS/14-appointment-booking — fix report (B07)

Fable, 2026-09-17.

## Done
- review#1 03 states the confirmed-only slot policy and the coupling to appointmentService.ts:125; new test pins it (a cancelled row does not block, a confirmed one does)
- review#3 02 half-open-interval box with the four worked cases
- review#2 / 2.2 six distinct trace-lab boundaries (07)
- review#4 / 2.3 per-exercise review criteria (06)
- 2.4 excerpt shows the changed model transaction and the overlap check
- 2.4 three concrete variations
- 2.5 ownership/authz exercise 7 across customer and provider roles (05, 06)
- review#4 booking-specific debugging section (04)
- review#5 root package renamed from astra-crud-workspace-65; pg and tsx declared at the root; README carries the Toolchain block
- test 3 (notification trigger) now drops its trigger and function in a finally block, so later tests are not poisoned (found while adding test 4)

## Skipped
- (none)

## Verification
- npm install (workspaces) -> added 251 packages
- cmd /c npm test with ASTRA_TEST_DATABASE_URL -> # tests 4 / # pass 4 / # fail 0 (3 delivered + cancelled-row policy test)
- npm run build -> built in 16.66s
- direct service reproduction (temporary test/_debug.test.ts, removed) used to isolate the trigger pollution
- node_modules and dist removed; root package-lock.json kept

## Course/code consistency check
- 03 excerpt re-read against models/appointmentModel.ts createAppointment (81) and ensureNoConflict (127)
- 07 boundaries cite services/api.ts 33, appointmentRoutes.ts, validate.ts, appointmentService.ts 27-70/125, appointmentModel.ts 81/127, utils/errors.ts 27
- 02 half-open table matches the strict comparisons at appointmentModel.ts 144-145; 03 policy paragraph matches the status CHECK constraint
