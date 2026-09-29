# CRUD upskilling batch 01 — 2026-09-21

**10 of 10 projects delivered.** Remaining entries are pending, not accepted changes.

Luna implements most projects in isolated stages; Astra reviews correctness, meaningful test evidence and teaching quality before applying finite manifests. Protected project families and every applybot/applyboy variant are excluded.

| Project | Status | Accepted test cases | Learning guide |
|---|---|---:|---|
| _Organized Desktop/08 App And Product Projects/recipegen-app | Delivered | 46 | [Course](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app/astraupskill/README.md) |
| _Organized Desktop/08 App And Product Projects/HNJOBTRACK | Delivered | 9 | [Course](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK/astraupskill/README.md) |
| _Organized Desktop/08 App And Product Projects/grouphelpdesk | Delivered | 5 | [Course](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/grouphelpdesk/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww36 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww36/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww43 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww43/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww48 | Delivered | 3 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww48/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/zz2 | Delivered | 2 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz2/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/zz3 | Delivered | 7 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz3/astraupskill/README.md) |
| _Organized Desktop/02 Build Projects/buildaffiliate | Delivered | 3 | [Course](../../_Organized%20Desktop/02%20Build%20Projects/buildaffiliate/astraupskill/README.md) |
| _Organized Desktop/02 Build Projects/buildanalytics | Delivered | 8 | [Course](../../_Organized%20Desktop/02%20Build%20Projects/buildanalytics/astraupskill/README.md) |

**Accepted runtime tests:** 92. **Changed/added files:** 185. [Complete file-name list](CRUD_UPSKILL_BATCH_01_CHANGED_FILES_2026-09-21.txt).


## recipegen-app

- Validate recipe requests before provider calls and validate nested provider output before success.
- Recover valid browser history/favorites from mixed or malformed persisted JSON without rewriting data during reads.
- Add 46 production-module regressions and nine source-based teaching chapters with original snapshots, debugging exercises, traces and separate solutions.

**Teaching:** 9 source-based chapters; 3,415 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `app/api/recipes/route.ts`
- `lib/storage.ts`
- `package.json`
- `tsconfig.json`
- `lib/validation.ts`
- `lib/generation.ts`
- `tests/boundaries.test.mjs`
- `astraupskill/snapshots/app__api__recipes__route.ts.original.txt`
- `astraupskill/snapshots/lib__storage.ts.original.txt`
- `astraupskill/snapshots/package.json.original.txt`
- `astraupskill/snapshots/tsconfig.json.original.txt`
- `astraupskill/evidence/crud-b01-boundaries.log`
- `astraupskill/evidence/crud-b01-typecheck-installed.log`
- `astraupskill/evidence/results.json`
- `astraupskill/README.md`
- `astraupskill/01-CODEBASE-MAP.md`
- `astraupskill/02-CONCEPTS.md`
- `astraupskill/03-WORKED-CHANGE.md`
- `astraupskill/04-TESTING-AND-DEBUGGING.md`
- `astraupskill/05-PRACTICE.md`
- `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- `astraupskill/07-TRACE-LAB.md`
- `astraupskill/VERIFICATION.md`

**Verification limits:**

- Focused production-module tests; Next HTTP adapter/browser/provider integration not executed.
- No database exists in this flow. Storage recovery validates and filters on read without rewriting saved collections.
- Changed-file ESLint was stopped after more than ten minutes without diagnostics; no lint pass is claimed.
- Existing process-local rate limiting, session-storage navigation failure, SDK-internal retries and dietary/culinary accuracy are not certified by this change.
- Full production build and browser end-to-end tests were not run; project typecheck passed.

[Delivery manifest](../astra-remaining-improvements/deliveries/e0e5886e8464.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/e0e5886e8464-astra-review.json)


## HNJOBTRACK

- Make HN comment acquisition resumable when a thread parent exists but a prior run stopped before importing children.
- Preserve completed parsed listings by returning early and use duplicate-ignore upsert for incomplete retries.

**Teaching:** 9 source-based chapters; 2,848 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `backend/app/services/scraper.py`
- `supabase/schema.sql`
- `supabase/migrations/20260921_job_comment_unique.sql`
- `backend/tests/test_scraper_resume.py`
- `backend/tests/test_scraper_recovery.py`
- `astraupskill/snapshots/backend/app/services/scraper.py`
- `astraupskill/snapshots/supabase/schema.sql`
- `astraupskill/evidence/astra-crud-b01-all-scraper.log`
- `astraupskill/evidence/results.json`
- `astraupskill/README.md`
- `astraupskill/01-CODEBASE-MAP.md`
- `astraupskill/02-CONCEPTS.md`
- `astraupskill/03-WORKED-CHANGE.md`
- `astraupskill/04-TESTING-AND-DEBUGGING.md`
- `astraupskill/05-PRACTICE.md`
- `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- `astraupskill/07-TRACE-LAB.md`
- `astraupskill/VERIFICATION.md`

**Verification limits:**

- Focused tests use fake database and HTTP module boundaries.
- Live service and migration execution were not performed.

[Delivery manifest](../astra-remaining-improvements/deliveries/fb1267045788.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/fb1267045788-astra-review.json)


## grouphelpdesk

- Protect ticket organization ownership during updates by adding a service-level field authorization decision.
- Reject non-admin cross-organization changes before persistence while preserving same-organization updates.

**Teaching:** 9 source-based chapters; 2,500 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `packages/server/src/modules/tickets/ticket.permissions.ts`
- `packages/server/src/modules/tickets/ticket.service.ts`
- `packages/server/src/modules/tickets/ticket.test.ts`
- `tests/helpers/load-typescript.mjs`
- `tests/runtime-permissions.test.mjs`
- `tests/runtime-ticket-service.test.mjs`
- `astraupskill/snapshots/packages/server/src/modules/tickets/ticket.permissions.ts`
- `astraupskill/snapshots/packages/server/src/modules/tickets/ticket.service.ts`
- `astraupskill/snapshots/packages/server/src/modules/tickets/ticket.test.ts`
- `astraupskill/evidence/astra-crud-b01-services.log`
- `astraupskill/evidence/results.json`
- `astraupskill/README.md`
- `astraupskill/01-CODEBASE-MAP.md`
- `astraupskill/02-CONCEPTS.md`
- `astraupskill/03-WORKED-CHANGE.md`
- `astraupskill/04-TESTING-AND-DEBUGGING.md`
- `astraupskill/05-PRACTICE.md`
- `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- `astraupskill/07-TRACE-LAB.md`
- `astraupskill/VERIFICATION.md`

**Verification limits:**

- Vitest command not run because dependencies were not installed.
- Five Node runtime tests exercise actual service and permission source with explicit persistence/integration doubles; no real HTTP, Prisma or outbox execution.
- Optional missing-viewer trusted internal bypass remains; this is an organization-field update guard, not a complete tenant-security audit.

[Delivery manifest](../astra-remaining-improvements/deliveries/0f37c14f6d60.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/0f37c14f6d60-astra-review.json)


## ww36

- Prevent completion of active reservations at or after expiresAt
- Keep release available as expired-hold cleanup
- Add service regression coverage and CRUD upskill course

**Teaching:** 9 source-based chapters; 2,497 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/services/reservationService.ts`
- `tests/reservation-service-transition.test.ts`
- `tests/runtime-expiry.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-services-reservationService.ts.before`
- `astraupskill/snapshots/tests-reservation-service-transition.test.ts.before`
- `astraupskill/evidence/astra-crud-b01-runtime.log`
- `astraupskill/evidence/results.json`
- `astraupskill/README.md`
- `astraupskill/01-CODEBASE-MAP.md`
- `astraupskill/02-CONCEPTS.md`
- `astraupskill/03-WORKED-CHANGE.md`
- `astraupskill/04-TESTING-AND-DEBUGGING.md`
- `astraupskill/05-PRACTICE.md`
- `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- `astraupskill/07-TRACE-LAB.md`
- `astraupskill/VERIFICATION.md`

**Verification limits:**

- Vitest command is unrun because npm registry tooling did not complete
- Portable VM tests use explicit mocked repository/Prisma contracts and do not claim live PostgreSQL concurrency
- Full typecheck/build, real HTTP authorization and live database concurrency were not executed.

[Delivery manifest](../astra-remaining-improvements/deliveries/7a758c622d3c.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/7a758c622d3c-astra-review.json)


## ww43

- Protect note status transitions with an atomic expected-status predicate
- Return a stable STATUS_CONFLICT before audit on stale writes
- Add project-specific CRUD upskill course

**Teaching:** 9 source-based chapters; 2,655 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/repositories/note-repository.ts`
- `src/services/note-service.ts`
- `tests/services/note-service.test.ts`
- `tests/runtime-status.test.mjs`
- `tests/runtime-note-service.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-repositories-note-repository.ts.before`
- `astraupskill/snapshots/src-services-note-service.ts.before`
- `astraupskill/snapshots/tests-services-note-service.test.ts.before`
- `astraupskill/evidence/astra-crud-b01-services.log`
- `astraupskill/evidence/results.json`
- `astraupskill/README.md`
- `astraupskill/01-CODEBASE-MAP.md`
- `astraupskill/02-CONCEPTS.md`
- `astraupskill/03-WORKED-CHANGE.md`
- `astraupskill/04-TESTING-AND-DEBUGGING.md`
- `astraupskill/05-PRACTICE.md`
- `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- `astraupskill/07-TRACE-LAB.md`
- `astraupskill/VERIFICATION.md`

**Verification limits:**

- Vitest command is unrun because isolated dependency installation was unavailable
- Portable VM tests use explicit repository/database contracts; live PostgreSQL race coverage remains for review
- Full typecheck/build, real HTTP authorization and live database concurrency were not executed.
- Status comparison does not detect ACTIVE-to-ARCHIVED-to-ACTIVE changes, body edits or permission changes between read and write.

[Delivery manifest](../astra-remaining-improvements/deliveries/200c3e641a36.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/200c3e641a36-astra-review.json)


## ww48

- Protect pending follow-up status changes with compare-and-set persistence
- Avoid parent-summary and activity writes after stale update conflicts
- Add project-specific CRUD upskill course

**Teaching:** 9 source-based chapters; 2,867 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/repositories/followUpRepository.ts`
- `src/services/followUpService.ts`
- `src/tests/follow-up-status-conflict.test.ts`
- `src/tests/runtime-followup.test.mjs`
- `src/tests/runtime-followup-service.test.mjs`
- `src/tests/helpers/load-typescript.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-repositories-followUpRepository.ts.before`
- `astraupskill/snapshots/src-services-followUpService.ts.before`
- `astraupskill/snapshots/src-tests-lead-stage-transition.test.ts.before`
- `astraupskill/evidence/astra-crud-b01-services.log`
- `astraupskill/evidence/results.json`
- `astraupskill/README.md`
- `astraupskill/01-CODEBASE-MAP.md`
- `astraupskill/02-CONCEPTS.md`
- `astraupskill/03-WORKED-CHANGE.md`
- `astraupskill/04-TESTING-AND-DEBUGGING.md`
- `astraupskill/05-PRACTICE.md`
- `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- `astraupskill/07-TRACE-LAB.md`
- `astraupskill/VERIFICATION.md`

**Verification limits:**

- Vitest command is unrun because isolated dependency installation was unavailable
- Portable VM tests use explicit repository/database contracts and do not prove two live PostgreSQL transactions race correctly
- Full typecheck/build, real HTTP authorization and live database concurrency were not executed.

[Delivery manifest](../astra-remaining-improvements/deliveries/6e522cf7fdc9.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/6e522cf7fdc9-astra-review.json)


## zz2

- Make ticket references collision-resistant for concurrent creates while preserving the SUP- display prefix.
- Add a production TicketService regression for consecutive creates and nine source-grounded CRUD chapters.

**Teaching:** 9 source-based chapters; 2,730 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/server/modules/tickets/service.ts`
- `src/server/modules/tickets/service.test.ts`
- `tests/ticket-reference.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src__server__modules__tickets__service.ts.original.txt`
- `astraupskill/evidence/astra-crud-b01-identifiers.log`
- `astraupskill/evidence/results.json`
- `astraupskill/snapshots/src__server__modules__tickets__service.test.ts.original.txt`
- `astraupskill/README.md`
- `astraupskill/01-CODEBASE-MAP.md`
- `astraupskill/02-CONCEPTS.md`
- `astraupskill/03-WORKED-CHANGE.md`
- `astraupskill/04-TESTING-AND-DEBUGGING.md`
- `astraupskill/05-PRACTICE.md`
- `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- `astraupskill/07-TRACE-LAB.md`
- `astraupskill/VERIFICATION.md`

**Verification limits:**

- Focused Vitest was blocked by an uncached dependency; no database or HTTP integration was run.
- UUID uniqueness still relies on the database unique constraint for final enforcement.

[Delivery manifest](../astra-remaining-improvements/deliveries/fdad4e87a703.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/fdad4e87a703-astra-review.json)


## zz3

- Reject duplicate tag identities in ticket create and metadata update commands.
- Preserve valid empty and omitted tag semantics while failing before relation writes.

**Teaching:** 9 source-based chapters; 2,853 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/lib/validation/ticket-schemas.ts`
- `src/tests/unit/ticket-schemas.test.ts`
- `tests/helpers/load-typescript.mjs`
- `tests/runtime-schema.test.mjs`
- `astraupskill/snapshots/src/lib/validation/ticket-schemas.ts`
- `astraupskill/snapshots/src/tests/unit/ticket-schemas.test.ts`
- `astraupskill/evidence/astra-crud-b01-schema.log`
- `astraupskill/evidence/results.json`
- `astraupskill/README.md`
- `astraupskill/01-CODEBASE-MAP.md`
- `astraupskill/02-CONCEPTS.md`
- `astraupskill/03-WORKED-CHANGE.md`
- `astraupskill/04-TESTING-AND-DEBUGGING.md`
- `astraupskill/05-PRACTICE.md`
- `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- `astraupskill/07-TRACE-LAB.md`
- `astraupskill/VERIFICATION.md`

**Verification limits:**

- Runtime schema tests used real Zod 4.3.6 through an explicit shared-install override; normal runner resolves project-local zod.
- Vitest, full typecheck/build, HTTP, authorization and Prisma/database integration were not executed.

[Delivery manifest](../astra-remaining-improvements/deliveries/c94cd4bde644.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/c94cd4bde644-astra-review.json)


## buildaffiliate

- Use a full UUID suffix for newly created campaign slugs while preserving readable name normalization and the 60-character prefix bound.
- Add three production helper/service runtime tests and nine source-linked chapters on CRUD identity, uniqueness and request idempotency.

**Teaching:** 9 source-based chapters; 2,559 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `apps/api/src/services/campaign.service.ts`
- `apps/api/src/services/campaign.service.test.ts`
- `tests/campaign-slug.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/apps__api__src__services__campaign.service.ts.original.txt`
- `astraupskill/evidence/astra-crud-b01-identifiers.log`
- `astraupskill/evidence/results.json`
- `astraupskill/README.md`
- `astraupskill/01-CODEBASE-MAP.md`
- `astraupskill/02-CONCEPTS.md`
- `astraupskill/03-WORKED-CHANGE.md`
- `astraupskill/04-TESTING-AND-DEBUGGING.md`
- `astraupskill/05-PRACTICE.md`
- `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- `astraupskill/07-TRACE-LAB.md`
- `astraupskill/VERIFICATION.md`

**Verification limits:**

- Focused Vitest was not run because dependencies were unavailable in the staged workspace.
- Database uniqueness and cross-process behavior remain deployment checks.

[Delivery manifest](../astra-remaining-improvements/deliveries/74faaa8b7040.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/74faaa8b7040-astra-review.json)


## buildanalytics

- Repair default-peer clearing for dashboard configuration PATCHes with omitted role or default fields.
- Add eight runtime regressions plus nine source-linked CRUD chapters with effective-state exercises and solved traces.

**Teaching:** 9 source-based chapters; 2,500 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `backend/src/modules/dashboardConfigs/dashboardConfigs.service.ts`
- `backend/src/modules/dashboardConfigs/dashboardConfigs.service.test.ts`
- `tests/dashboard-default.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/backend__src__modules__dashboardConfigs__dashboardConfigs.service.ts.original.txt`
- `astraupskill/evidence/astra-crud-b01-dashboard.log`
- `astraupskill/evidence/results.json`
- `astraupskill/README.md`
- `astraupskill/01-CODEBASE-MAP.md`
- `astraupskill/02-CONCEPTS.md`
- `astraupskill/03-WORKED-CHANGE.md`
- `astraupskill/04-TESTING-AND-DEBUGGING.md`
- `astraupskill/05-PRACTICE.md`
- `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- `astraupskill/07-TRACE-LAB.md`
- `astraupskill/VERIFICATION.md`

**Verification limits:**

- Focused Node runtime tests use explicit Prisma transaction spies; real SQL rollback, isolation, HTTP authorization and browser behavior were not executed.
- Normal Vitest suite, full typecheck and build were not run. The existing pre-read and create path mean this PATCH repair does not guarantee global or concurrent default uniqueness.

[Delivery manifest](../astra-remaining-improvements/deliveries/54397e702f3f.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/54397e702f3f-astra-review.json)


Canonical file hashes were checked when this report was generated. Passing counts refer only to the accepted suites; they are not a claim that every upstream or external-service check ran.
