# CRUD upskilling batch 06 — 2026-09-21

**10 of 10 projects delivered.** Remaining entries are pending, not accepted changes.

Luna implements most projects in isolated stages; Astra reviews correctness, meaningful test evidence and teaching quality before applying finite manifests. Protected project families and every applybot/applyboy variant are excluded.

| Project | Status | Accepted test cases | Learning guide |
|---|---|---:|---|
| _Organized Desktop/05 Numbered Experiments/ww26 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww26/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww28 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww28/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww29 | Delivered | 6 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww29/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww3 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww3/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww30 | Delivered | 3 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww30/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww31 | Delivered | 6 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww31/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww32 | Delivered | 6 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww32/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww4 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww4/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww40 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww40/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/ww45 | Delivered | 6 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww45/astraupskill/README.md) |

**Accepted runtime tests:** 51. **Changed/added files:** 142. [Complete file-name list](CRUD_UPSKILL_BATCH_06_CHANGED_FILES_2026-09-21.txt).


## ww26

- Reviewed lock coordinator behavior and found no production defect warranting a patch.
- Added an actual coordinator lab for ownership, expiry, status rereads, holder cleanup, and stale sweeps.
- Captured five executed Node VM cases with explicit provider limits.

**Teaching:** 9 source-based chapters; 1,686 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/runtime-lock-coordinator-lab.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/evidence/crud-b06-astra-runtime.log`
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
- No live provider, FOR UPDATE, route, concurrent worker, or rollback execution.
- Normal project typecheck and provider-backed tests remain follow-up checks.
- Authorization and ApiError execute from actual source; repository/transaction adapters do not establish row locking or isolation.

[Delivery manifest](../astra-remaining-improvements/deliveries/971a7c784720.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/971a7c784720-astra-review.json)


## ww28

- Reject multipart part numbers below one as well as above expectedParts.
- Prevent malformed chunk storage and metadata writes while preserving valid retry writes.
- Execute the real UploadService through five dependency-free runtime cases.

**Teaching:** 9 source-based chapters; 1,747 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/services/uploadService.ts`
- `tests/runtime-upload-bounds.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src/services/uploadService.ts`
- `astraupskill/evidence/crud-b06-astra-runtime.log`
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

- No live Next, Prisma, replica filesystem, completion, quota, or concurrent retry execution.
- Historical malformed chunks are not migrated or deleted by this bounded fix.
- Actual guards, permission rules, base64 utility and error classes execute. Repository/storage adapters do not verify durable storage or atomic retry replacement; delete precedes replacement write.

[Delivery manifest](../astra-remaining-improvements/deliveries/5528ac452b91.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/5528ac452b91-astra-review.json)


## ww29

- Reviewed notification open path and found no production defect warranting a patch.
- Added an actual service lab for recipient isolation, SENT eligibility, aggregate refresh, audit, and admin visibility.
- Captured six executed Node VM cases using the production permission matrix.

**Teaching:** 9 source-based chapters; 1,821 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/runtime-notification-open-lab.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/evidence/crud-b06-astra-runtime.log`
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
- No live Prisma transaction, Next route, worker, or repeated-open execution.
- Normal project typecheck and provider-backed tests remain follow-up checks.
- Real service, permissions, ApiError and repository aggregate functions execute. Prisma enum exports and unused rendering/Zod imports are adapted. Open tracking has no encompassing transaction; aggregate failure can follow earlier open writes.

[Delivery manifest](../astra-remaining-improvements/deliveries/4e19ba5b5028.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/4e19ba5b5028-astra-review.json)


## ww3

- Replaced the country-rule repository create call with a composite-key Prisma upsert matching the schema unique constraint.
- Added actual repository runtime coverage for first-write and repeat-write payloads.

**Teaching:** 9 source-based chapters; 1,789 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/repositories/prisma/complianceRepository.ts`
- `tests/runtime-country-rule-upsert.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-repositories-prisma-complianceRepository.ts.before`
- `astraupskill/evidence/crud-b06-astra-runtime.log`
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

- Actual repository TypeScript executed with explicit Prisma-shaped double; no live database or generated-client typecheck.
- No route, auth, audit, migration, or concurrent transaction test.
- Upsert preserves composite identity and updates mutable fields; audit action semantics remain unchanged.

[Delivery manifest](../astra-remaining-improvements/deliveries/5c252a248ab8.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/5c252a248ab8-astra-review.json)


## ww30

- Changed cache expiry comparison from strict greater-than to greater-than-or-equal so entries expire at the declared TTL boundary.
- Added actual QueryResultCache runtime coverage with deterministic before, exact, and after expiry cases.

**Teaching:** 9 source-based chapters; 1,664 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/lib/cache/queryCache.ts`
- `tests/runtime-cache-expiry.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-lib-cache-queryCache.ts.before`
- `astraupskill/evidence/crud-b06-astra-runtime.log`
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

- Actual cache TypeScript executed with explicit type-export stubs and deterministic Date; no full service or live DB.
- No HTTP, auth, query execution, distributed cache, or concurrency check.
- Fix covers TTL exact-boundary semantics; maxEntries and row-level cache authorization remain separate concerns.

[Delivery manifest](../astra-remaining-improvements/deliveries/41ea8dcef618.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/41ea8dcef618-astra-review.json)


## ww31

- Added an explicit bounded capacity policy to InMemoryCache with default size, disabled zero-capacity behavior, and oldest-key eviction.
- Added actual cache runtime coverage for disabled storage, capacity eviction, and prefix invalidation.
- Reject non-finite, fractional and unsafe capacity values so configured bounds cannot silently become unbounded.

**Teaching:** 9 source-based chapters; 1,765 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/lib/cache/inMemoryCache.ts`
- `tests/runtime-cache-capacity.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-lib-cache-inMemoryCache.ts.before`
- `astraupskill/evidence/crud-b06-astra-runtime.log`
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

- Actual cache class with local VM helper; no flag evaluator, route, database, distributed process, memory profiler, or concurrency run.
- Capacity bound is per process and does not address TTL freshness or authorization key design.

[Delivery manifest](../astra-remaining-improvements/deliveries/ed24cac9b9f3.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/ed24cac9b9f3-astra-review.json)


## ww32

- Provide a runnable source lab for workspace-scoped message posting and guest refusal.
- Verify successful transaction orchestration with created message and sync event adapters.

**Teaching:** 9 source-based chapters; 1,663 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/message-post-runtime.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/messageService.ts.original.txt`
- `astraupskill/evidence/crud-b06-astra-runtime.log`
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

- Six actual message-service cases load real role policy and errors, with channel-access, repository, transaction and realtime adapters. No Next, Prisma rollback/isolation or network delivery execution.
- Private notification filtering and attachment query arguments execute in the service; the adapters do not prove repository scoping or live transport confidentiality. Publishing follows the transaction response; persisted event does not prove delivery.

[Delivery manifest](../astra-remaining-improvements/deliveries/829e8e7b8605.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/829e8e7b8605-astra-review.json)


## ww4

- Provide a runnable source lab for issue creation orchestration and project-member refusal.
- Verify transaction ordering with issue, activity, and automation adapters.

**Teaching:** 9 source-based chapters; 1,058 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/issue-service-runtime.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/issueService.ts.original.txt`
- `astraupskill/evidence/crud-b06-astra-runtime.log`
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

- Five cases execute actual issue creation, permission mapping, workflow helpers, custom-field validator and errors. Repository, transaction and automation persistence are adapted; no Prisma rollback, sequence concurrency, route or automation delivery execution.
- Same-client checks establish argument discipline, not commit durability. Project setup/member reads precede the transaction; visibility or membership races are not addressed. No production source change.

[Delivery manifest](../astra-remaining-improvements/deliveries/7dde79c7a4c0.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/7dde79c7a4c0-astra-review.json)


## ww40

- Provide a runnable source lab for job submission, approval, rejection, and audit sequencing.
- Verify review-state guards through injected repository and audit adapters.

**Teaching:** 9 source-based chapters; 1,027 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/job-posting-service-runtime.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/jobPostingService.ts.original.txt`
- `astraupskill/evidence/crud-b06-astra-runtime.log`
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

- Five actual service cases use real ApiError and repository/audit adapters. No route authentication, generated Prisma, SQL scoping or concurrency run.
- Service review reads state before separate update and audit calls; no enclosing transaction or expected-status predicate is proved. The service does not itself assert reviewer role. No production code changed.

[Delivery manifest](../astra-remaining-improvements/deliveries/7a06d436fe48.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/7a06d436fe48-astra-review.json)


## ww45

- Add six actual-service runtime cases using real knowledge publishing permissions and domain errors.
- Add source-grounded decision tables, call tracing, failure injection and review exercises.

**Teaching:** 9 source-based chapters; 1,029 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/knowledge-entry-service-runtime.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/knowledgeEntryService.ts.original.txt`
- `astraupskill/evidence/crud-b06-astra-runtime.log`
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

- Database repositories and transaction are adapters; no Next authentication, SQL filtering, rollback or isolation execution.
- Production source unchanged. Equal-status writes and audit behavior documented, not changed.

[Delivery manifest](../astra-remaining-improvements/deliveries/5bbaa8521f2b.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/5bbaa8521f2b-astra-review.json)


Canonical file hashes were checked when this report was generated. Passing counts refer only to the accepted suites; they are not a claim that every upstream or external-service check ran.
