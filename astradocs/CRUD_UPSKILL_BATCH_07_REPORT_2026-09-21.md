# CRUD upskilling batch 07 — 2026-09-21

**10 of 10 projects delivered.** Remaining entries are pending, not accepted changes.

Luna implements most projects in isolated stages; Astra reviews correctness, meaningful test evidence and teaching quality before applying finite manifests. Protected project families and every applybot/applyboy variant are excluded.

| Project | Status | Accepted test cases | Learning guide |
|---|---|---:|---|
| _Organized Desktop/05 Numbered Experiments/ww46 | Delivered | 7 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww46/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww47 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww47/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww6 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww6/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww7 | Delivered | 6 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww7/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww8 | Delivered | 3 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww8/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/X1 | Delivered | 2 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/X1/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/z8 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/z8/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/zz1 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz1/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/zz4 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz4/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/zz55 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz55/astraupskill/README.md) |

**Accepted runtime tests:** 44. **Changed/added files:** 146. [Complete file-name list](CRUD_UPSKILL_BATCH_07_CHANGED_FILES_2026-09-21.txt).


## ww46

- Check the tenant-scoped updateMany count before rereading or auditing a project status change.
- Return HTTP 409 when the status write affects zero rows.
- Execute the real project service and policy through seven runtime cases.

**Teaching:** 9 source-based chapters; 1,702 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/services/project-service.ts`
- `tests/runtime-project-status-race.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src/services/project-service.ts`
- `astraupskill/evidence/crud-b07-astra-runtime.log`
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

- No live Prisma SQL, concurrent database, route, or rollback execution.
- No retry policy or status-policy redesign is included.
- The repository predicate includes organization and id, not expected status; count checking is not optimistic concurrency control. Real HttpError and role/status policy execute with generated enum adapters.

[Delivery manifest](../astra-remaining-improvements/deliveries/7ff66e57d973.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/7ff66e57d973-astra-review.json)


## ww47

- Reviewed aggregation worker and state policy; no production fix was warranted in the bounded path.
- Added a production state-machine lab for all legal and representative invalid job transitions.
- Captured four executed Node VM cases with explicit worker and provider limits.

**Teaching:** 9 source-based chapters; 1,616 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/runtime-aggregation-state-lab.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/evidence/crud-b07-astra-runtime.log`
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

- No production fix warranted in reviewed path.
- No Prisma worker, rollup, audit persistence, concurrent claim, or retry execution.
- Provider-backed queue checks remain follow-up work.
- State guard and real AppError execute without behavior doubles. Worker claim and completion transactions were inspected, not executed.

[Delivery manifest](../astra-remaining-improvements/deliveries/ec28c8c40e53.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/ec28c8c40e53-astra-review.json)


## ww6

- Fix an accidentally terminated block comment in the real HTTP error module so TypeScript can parse it.
- Added a production state-machine lab for legal and invalid run transitions.
- Captured four executed Node VM policy cases with explicit worker limits.

**Teaching:** 9 source-based chapters; 1,738 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/runtime-allocation-state-lab.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `src/lib/http/errors.ts`
- `astraupskill/snapshots/errors.ts.original.txt`
- `astraupskill/evidence/crud-b07-astra-runtime2.log`
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

- No Prisma worker, claim, aggregation, rollup, audit, failure recovery, or retry execution.
- Provider-backed queue checks remain follow-up work.
- Real ValidationError is loaded. Unexecuted repository/engine exports and queue registration are adapted. Worker catch directly writes FAILED without transition guard; terminal helper refusal does not certify worker immutability.

[Delivery manifest](../astra-remaining-improvements/deliveries/79c315026b95.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/79c315026b95-astra-review.json)


## ww7

- Made equal workflow status requests idempotent by returning after authorization and transition validation without persistence or change audit.
- Added actual workflow service runtime coverage for no-op, valid transition, and invalid transition behavior.

**Teaching:** 9 source-based chapters; 1,723 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/services/workflow-definition-service.ts`
- `tests/runtime-workflow-same-status.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-services-workflow-definition-service.ts.before`
- `astraupskill/evidence/crud-b07-astra-runtime.log`
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

- Six cases execute actual service, ownership helper, status/readiness policy and AppError with repository/schedule and generated-enum adapters. No HTTP route, live Prisma, cron parsing or concurrency run.
- Equal-status calls retain ownership checks but skip activation-readiness and schedule recalculation. Coarse route permission enforcement is outside this lab. Status update and audit have no enclosing service transaction.

[Delivery manifest](../astra-remaining-improvements/deliveries/671a350f0386.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/671a350f0386-astra-review.json)


## ww8

- Verify actual extraction-job claim predicate, attempt increment, result forwarding and database error propagation without claiming a concurrent worker execution.
- Added actual repository runtime learning-lab coverage without changing already-correct production logic.

**Teaching:** 9 source-based chapters; 1,629 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/runtime-job-claim-contract.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/evidence/crud-b07-astra-runtime.log`
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

- Actual documentRepository function with Prisma-shaped double; no production source mutation.
- No worker, extractor, Prisma SQL lock, transaction, audit, or concurrent process test.

[Delivery manifest](../astra-remaining-improvements/deliveries/4d914b7440f4.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/4d914b7440f4-astra-review.json)


## X1

- Preserved moderator-hidden review state when an author edits existing review content; update SQL no longer resets is_hidden.
- Two actual-data-module runtime cases check content-only UPDATE and visible INSERT with author/shop identity.

**Teaching:** 9 source-based chapters; 1,469 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `bagel-intel-platform/src/lib/data.ts`
- `bagel-intel-platform/tests/runtime-review-moderation.test.mjs`
- `bagel-intel-platform/tests/helpers/load-typescript.mjs`
- `bagel-intel-platform/astraupskill/snapshots/src-lib-data.ts.before`
- `astraupskill/evidence/crud-b07-astra-runtime.log`
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

- Actual data module with SQLite-shaped adapter; no live SQLite or server action.
- No session/admin integration or ranking correctness check.
- New rows remain visible by existing insert behavior; edits preserve current moderation state.

[Delivery manifest](../astra-remaining-improvements/deliveries/1754dbb384b1.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/1754dbb384b1-astra-review.json)


## z8

- Rejects registration requests containing session IDs that are not owned by the selected event.
- Executes five actual-service cases with real permission and AppError code.
- Preserves an exact snapshot and teaches the service-side data boundary and verification limits.

**Teaching:** 9 source-based chapters; 1,979 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/modules/registrations/registration.service.ts`
- `tests/registration-session-selection.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src/modules/registrations/registration.service.ts`
- `astraupskill/evidence/crud-b07-astra-runtime.log`
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

- Persistence, audit and DB singleton adapted; NextResponse and zod exports unused by tested path are stubs.
- No database concurrency or notification delivery proof. Duplicate IDs allowed and deduplicated. Notification failure can follow persistence.

[Delivery manifest](../astra-remaining-improvements/deliveries/482e93488b83.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/482e93488b83-astra-review.json)


## zz1

- Deal stage movement now treats a null update reread as a safe not-found result.
- Four actual-service cases use real errors for null reread, ordinary success, pipeline refusal and won-stage payload.
- Exact source snapshot and source-grounded course explain repository reread limits.

**Teaching:** 9 source-based chapters; 1,758 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/services/dealService.ts`
- `tests/deal-stage-update-result.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src/services/dealService.ts`
- `astraupskill/evidence/crud-b07-astra-runtime.log`
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

- Repository, Prisma transaction, pipeline, and audit are explicit doubles.
- No real provider or concurrency execution.
- Guard proves non-null reread before dependent writes, not transactional race resolution.

[Delivery manifest](../astra-remaining-improvements/deliveries/5f8d9a364788.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/5f8d9a364788-astra-review.json)


## zz4

- Sort pending stages consistently for both current approval and next-stage advancement.
- Four actual-service runtime cases execute real capability/assignment guards and errors with database/session adapters.

**Teaching:** 9 source-based chapters; 1,698 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `zz4/src/services/approvalService.ts`
- `zz4/tests/approval-stage-order.test.mjs`
- `zz4/tests/helpers/load-typescript.mjs`
- `zz4/astraupskill/snapshots/src/services/approvalService.ts`
- `astraupskill/evidence/crud-b07-astra-runtime.log`
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

- No Prisma, Next session, SQL isolation or concurrent approvals executed.
- Duplicate sequence policy unchanged; request read remains before transaction.

[Delivery manifest](../astra-remaining-improvements/deliveries/f1f996eeb9e7.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/f1f996eeb9e7-astra-review.json)


## zz55

- Employee task completion now requires both profile ownership and an EMPLOYEE task assignment before mutation.
- Five actual-service cases execute real permission, transition and error modules, including no-write refusals, stage advance and audit failure.
- The course documents the source map, ownership concepts, worked change, debugging, exercises, answers, trace, and verification limits.

**Teaching:** 9 source-based chapters; 1,768 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/services/onboardingService.ts`
- `tests/onboarding-task-ownership.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/onboardingService.ts.before`
- `astraupskill/evidence/crud-b07-astra-runtime.log`
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

- Persistence, audit and job adapters; no Next, Prisma, database isolation or rollback execution.
- Employee ownerRole restriction only; HR/IT broader existing capability behavior unchanged. No enclosing service transaction.

[Delivery manifest](../astra-remaining-improvements/deliveries/cd5a8a522511.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/cd5a8a522511-astra-review.json)


Canonical file hashes were checked when this report was generated. Passing counts refer only to the accepted suites; they are not a claim that every upstream or external-service check ran.
