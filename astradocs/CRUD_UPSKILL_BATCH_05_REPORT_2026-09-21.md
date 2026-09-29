# CRUD upskilling batch 05 — 2026-09-21

**10 of 10 projects delivered.** Remaining entries are pending, not accepted changes.

Luna implements most projects in isolated stages; Astra reviews correctness, meaningful test evidence and teaching quality before applying finite manifests. Protected project families and every applybot/applyboy variant are excluded.

| Project | Status | Accepted test cases | Learning guide |
|---|---|---:|---|
| _Organized Desktop/05 Numbered Experiments/w25 | Delivered | 6 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/w25/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww1 | Delivered | 6 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww1/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww10 | Delivered | 8 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww10/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww11 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww11/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww12 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww12/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww13 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww13/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww15 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww15/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww16 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww16/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww18 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww18/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww19 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww19/astraupskill/README.md) |

**Accepted runtime tests:** 53. **Changed/added files:** 144. [Complete file-name list](CRUD_UPSKILL_BATCH_05_CHANGED_FILES_2026-09-21.txt).


## w25

- Preserve the existing LockService production implementation and add a bounded executable learning lab.
- Add an actual-service lab for ownership, expiry, release, and contention boundaries.
- Document runtime evidence and distributed-locking limits.

**Teaching:** 9 source-based chapters; 1,681 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/runtime-lock-service-lab.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/evidence/crud-b05-astra-runtime.log`
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

- Six cases execute actual LockService, state machine, scope-key and time helpers with explicit repository/audit adapters. No Next route, actual repository persistence, expiry scan, multi-process contention or durable audit execution.
- The draft incorrectly replaced canReacquire with always true and used a Date-returning time double. Accepted tests load the real modules and distinguish active-lock refusal from a repository version conflict after an eligible reacquire.
- No production code is changed and this bounded lab is not a complete correctness certification of the lock system.

[Delivery manifest](../astra-remaining-improvements/deliveries/13ccdfb915ff.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/13ccdfb915ff-astra-review.json)


## ww1

- Guard review-item decisions with organization, id, and PENDING at the write boundary.
- Return HTTP 409 on a lost state transition before revocation or audit side effects.
- Verify the real TypeScript service with a dependency-free VM test lab.

**Teaching:** 9 source-based chapters; 1,897 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/repositories/reviewCycleRepository.ts`
- `src/services/reviewCycleService.ts`
- `tests/runtime-review-cycle.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src/repositories/reviewCycleRepository.ts`
- `astraupskill/snapshots/src/services/reviewCycleService.ts`
- `astraupskill/evidence/crud-b05-astra-runtime.log`
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

- Six runtime cases execute actual review service, HttpError and the changed repository predicate builder. Explicit database/transaction/repository adapters verify arguments and ordering; no native Prisma provider or concurrent database run.
- The conditional write guards organization, item id and PENDING, but does not atomically guard review-cycle OPEN status. Native rollback, route authorization and simultaneous reviewer behavior remain unexecuted.
- Normal application typecheck and provider-backed integration were not run after dependency cleanup.

[Delivery manifest](../astra-remaining-improvements/deliveries/5007ac6ecdec.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/5007ac6ecdec-astra-review.json)


## ww10

- Preserve production reconciliation and add an eight-case actual-source decision-table lab.
- Teach lifecycle precedence, verification completeness, condition regression and disbursement gating without claiming persistence guarantees.

**Teaching:** 9 source-based chapters; 1,786 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/runtime-workflow-reconciliation-lab.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/evidence/crud-b05-astra-runtime.log`
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

- Eight Node cases execute actual pure reconciler and disbursement guard without dependency doubles. No Prisma, Next, transaction, authorization or provider callback execution.
- Stage regression to CONDITIONS is domain behavior, not database rollback. Pending and referred decisions explicitly select CREDIT_DECISIONING rather than generic current-stage fallthrough.
- Local Next.js guides absent after cleanup; no framework code was changed. Full application typecheck and command integration remain unexecuted.

[Delivery manifest](../astra-remaining-improvements/deliveries/e3ea1d9f41f1.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/e3ea1d9f41f1-astra-review.json)


## ww11

- Restrict protocol activation to draft versions so ACTIVE rows cannot be redundantly mutated or audited.
- Preserve draft activation and sibling retirement while adding a focused lifecycle boundary.

**Teaching:** 9 source-based chapters; 1,646 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/lib/domain/protocolRules.ts`
- `tests/runtime-protocol-activation.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-lib-domain-protocolRules.ts.before`
- `astraupskill/evidence/crud-b05-astra-runtime2.log`
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

- Four runtime cases execute actual protocol service, rules and repository with mock-state, id, audit and type-only export adapters. Same-code retirement, unrelated protocol preservation and unchanged participant pins are observed in fixture state.
- No route auth, native application, concurrent activation or durable audit was executed. The real repository mutates state before audit; audit failure leaves activation applied. No rollback guarantee is added.

[Delivery manifest](../astra-remaining-improvements/deliveries/1d0b328c6621.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/1d0b328c6621-astra-review.json)


## ww12

- Check updateMany count before auditing a conversation status transition so zero-row persistence cannot report success.
- Preserve tenant-scoped lookup, allowed transitions, and one-row audit behavior.

**Teaching:** 9 source-based chapters; 1,795 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/services/conversationService.ts`
- `tests/runtime-conversation-update-count.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-services-conversationService.ts.before`
- `astraupskill/evidence/crud-b05-astra-runtime.log`
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

- Five runtime cases execute actual conversation service, permission policy and error helpers with transaction/repository/audit adapters. No native Prisma, HTTP, SQL or rollback execution.
- The new count check detects a non-single-row update; repository write predicates do not compare the old status. It does not prevent stale-state transition races or prove concurrent safety.

[Delivery manifest](../astra-remaining-improvements/deliveries/5fd517cae993.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/5fd517cae993-astra-review.json)


## ww13

- Validate reporting-period existence before submission insertion and before approval changes the child report.
- Add actual repository/error-class tests for both orphan paths and successful parent/child transitions.

**Teaching:** 9 source-based chapters; 2,121 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/repositories/reportingRepository.ts`
- `tests/runtime-report-submit-atomicity.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-repositories-reportingRepository.ts.before`
- `astraupskill/evidence/crud-b05-astra-runtime.log`
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

- Five runtime cases execute actual repository and error classes with mutable-store and ID adapters. No live Next, authentication, persistence transaction, concurrency or full typecheck.
- This prevents the known missing-parent partial mutations in submit and approve. It does not add idempotency, service authorization, rollback for arbitrary later failures or atomic audit persistence. IDs and submission timestamps are still allocated before parent lookup.

[Delivery manifest](../astra-remaining-improvements/deliveries/2e356b8f3d9f.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/2e356b8f3d9f-astra-review.json)


## ww15

- Provide a runnable production-source lab for assigned-buyer offer authorization and mutation ordering.
- Verify assigned buyer success, role/identity rejection, and provider failure with zero later status/audit calls.

**Teaching:** 9 source-based chapters; 1,500 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/transaction-offer-policy.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/transaction-service.ts.original.txt`
- `astraupskill/evidence/crud-b05-astra-runtime.log`
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

- Four actual-service cases load real viewer/offer guards, policy and error classes with only repository port adapters. No Next, native persistence, external provider or rollback execution.
- createOffer is a repository operation, not an external provider call in this lab. Status/audit failure can follow earlier attempted writes; there is no service transaction wrapper. submitOffer does not call the workflow-transition validator used by updateStatus.

[Delivery manifest](../astra-remaining-improvements/deliveries/678b11ff9b03.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/678b11ff9b03-astra-review.json)


## ww16

- Provide a runnable production-source lab for deal state transitions, permission checks, and side-effect ordering.
- Verify permitted approval transition and forbidden transition zero writes.

**Teaching:** 9 source-based chapters; 1,772 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/deal-transition-lab.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/dealRegistrationService.ts.original.txt`
- `astraupskill/evidence/crud-b05-astra-runtime.log`
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

- Five cases execute actual service, transition policy, role permissions, error classes and quarter helper. Transaction/repository/audit/job and unused ZodError adapters are explicit.
- No Next, native database, rollback, worker or concurrent transition execution. Current deal is read before transaction and update does not compare prior status; shared client assertions do not prove isolation. No production behavior changed.

[Delivery manifest](../astra-remaining-improvements/deliveries/d851d9ba11a1.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/d851d9ba11a1-astra-review.json)


## ww18

- Add an actual-source quote policy lab covering lifecycle conflicts, integer-cent totals, exact discount thresholds and review routing.
- Preserve production behavior and teach boundary analysis with real money helpers and error classes.

**Teaching:** 9 source-based chapters; 1,680 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/quote-transition-policy.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/quote-policy.ts.original.txt`
- `astraupskill/evidence/crud-b05-astra-runtime.log`
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

- Five Node cases execute actual quote policy, money helpers and error classes without dependency doubles. No quote service, Next, Prisma, transaction, tenant authorization or order conversion execution.
- Pure policy tests use valid typed-like fixtures; request-schema validation, invalid runtime enum values and concurrent approval/price changes are outside this lab. No production code changed.

[Delivery manifest](../astra-remaining-improvements/deliveries/b17f4c546008.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/b17f4c546008-astra-review.json)


## ww19

- Provide a runnable service lab for user-scoped workflow-run idempotency and execution seeding.
- Verify replay zero writes and independent users receive separate idempotency scopes.

**Teaching:** 9 source-based chapters; 1,529 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/workflow-run-idempotency.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/workflow-run-service.ts.original.txt`
- `astraupskill/evidence/crud-b05-astra-runtime.log`
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

- Five cases execute actual start-run service and ApiError, with repository, transaction, schema and engine adapters plus unused Next/auth export stubs. No native Prisma, HTTP, real schema validation, worker or concurrency run.
- The fixture models per-user stored keys, not database uniqueness. Create callback completes before seeding; replay after seed failure returns the existing row without reseeding. Recovery is separate and not added.
- Same user and key return the existing run even if requested payload or definition differs. No payload-binding guarantee or production behavior change is claimed.

[Delivery manifest](../astra-remaining-improvements/deliveries/34942f670f85.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/34942f670f85-astra-review.json)


Canonical file hashes were checked when this report was generated. Passing counts refer only to the accepted suites; they are not a claim that every upstream or external-service check ran.
