# CRUD upskilling batch 04 — 2026-09-21

**10 of 10 projects delivered.** Remaining entries are pending, not accepted changes.

Luna implements most projects in isolated stages; Astra reviews correctness, meaningful test evidence and teaching quality before applying finite manifests. Protected project families and every applybot/applyboy variant are excluded.

| Project | Status | Accepted test cases | Learning guide |
|---|---|---:|---|
| _Organized Desktop/05 Numbered Experiments/D3 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/D3/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/e11 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/e11/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/e17 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/e17/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/e3 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/e3/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/e4 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/e4/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/g1 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/g1/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/rn1 | Delivered | 4 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/rn1/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/w21 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/w21/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/w22 | Delivered | 5 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/w22/astraupskill/README.md) |
| _Organized Desktop/05 Numbered Experiments/w23 | Delivered | 6 | [Course](../../_Organized%20Desktop/05%20Numbered%20Experiments/w23/astraupskill/README.md) |

**Accepted runtime tests:** 45. **Changed/added files:** 150. [Complete file-name list](CRUD_UPSKILL_BATCH_04_CHANGED_FILES_2026-09-21.txt).


## D3

- Reject API key strings with more than one delimiter before hashing or database access.
- Keep verification consistent with list lifecycle rules by excluding soft-deleted keys while preserving organization and revoked filters.

**Teaching:** 9 source-based chapters; 1,854 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `lib/services/apiKeys.ts`
- `tests/api-key-verify-boundary.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/apiKeys.ts.original.txt`
- `astraupskill/evidence/crud-b04-astra-runtime.log`
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

- Four runtime cases execute actual apiKeys.ts with real Node SHA-256 and explicit Drizzle/schema/database predicate adapters. No Next.js, native ORM or PostgreSQL is executed.
- The sequential verification read and lastUsedAt write are unchanged; concurrent revocation/deletion between them is not made atomic. Key verification does not establish every caller permission or organization lifecycle rule.

[Delivery manifest](../astra-remaining-improvements/deliveries/43d6b6358f56.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/43d6b6358f56-astra-review.json)


## e11

- Require an own room-map entry before share token generation or persistence, rejecting missing and inherited object-property names.
- Preserve existing share shape and JSON persistence for valid room references.

**Teaching:** 9 source-based chapters; 1,923 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `server/store.ts`
- `tests/share-room-integrity.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/store.ts.original.txt`
- `astraupskill/evidence/crud-b04-astra-runtime.log`
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

- Four runtime cases execute actual store source with real Node path and explicit filesystem/nanoid/scene adapters; no Express, auth signing or real filesystem persistence was executed.
- No-share-write assertions assume an initialized store; readDb may create initial directories/database when absent. File read-modify-write remains non-atomic and existing orphan shares are not migrated.
- The existing route has no new explicit mapping of the service error to HTTP404; this fix establishes a store rejection, not a newly verified HTTP error contract.

[Delivery manifest](../astra-remaining-improvements/deliveries/3b0530b090c4.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/3b0530b090c4-astra-review.json)


## e17

- Validate optional reply parent posts belong to the requested topic before opening the create transaction.
- Reject missing and cross-topic parent ids while preserving top-level and same-topic reply workflows.

**Teaching:** 9 source-based chapters; 1,678 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/lib/forum-core.ts`
- `tests/reply-parent-boundary.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/forum-core.ts.original.txt`
- `astraupskill/evidence/crud-b04-astra-runtime.log`
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

- Five Node runtime cases execute the actual forum module with Prisma, schema, enum, permission and external helper adapters. Same-topic/top-level cases run internal notification and trust orchestration against adapters, not real deliveries or persistence.
- No Next.js, native Prisma, Zod schema, actual permission policy, database isolation or durable rollback was executed. Parent validation is a pre-transaction membership check; concurrent parent changes remain outside this correction.
- Local Next.js guides were absent after dependency cleanup. No Next.js API or route was changed.

[Delivery manifest](../astra-remaining-improvements/deliveries/2f59a0d07a85.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/2f59a0d07a85-astra-review.json)


## e3

- Resolve the full project-scoped identifier set before privacy deletion so aliases and canonical IDs are scrubbed together.
- Remove associated alias mappings while preserving unrelated records and unknown-ID audit behavior.

**Teaching:** 9 source-based chapters; 1,937 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `lib/server/privacy.ts`
- `tests/runtime-privacy-alias-delete.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/lib-server-privacy.ts.before`
- `astraupskill/evidence/crud-b04-astra-runtime.log`
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

- Four actual privacy-service runtime cases use explicit store, id and clock adapters; no Next route, real authorization, filesystem durability or concurrent mutation executed.
- This bounded change expands identifier matching and alias cleanup in the existing scrubber. It is not complete erasure: other properties, userProperties, sessions, derived tables and audit metadata are not comprehensively scrubbed.
- No-person deletion still scrubs exact matching event/raw history and aliases; only a completely unmatched id changes audit alone. Export behavior is unchanged.

[Delivery manifest](../astra-remaining-improvements/deliveries/330bb6feda2f.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/330bb6feda2f-astra-review.json)


## e4

- Align development newsletter queue state transitions with the database path by rejecting re-queue attempts from queued state.
- Preserve first-queue recipient scheduling and audit behavior while preventing duplicate retry side effects.

**Teaching:** 9 source-based chapters; 1,859 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/server/newsletters/service.ts`
- `tests/runtime-newsletter-state.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-server-newsletters-service.ts.before`
- `astraupskill/evidence/crud-b04-astra-runtime.log`
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

- Four actual-service runtime cases load the real dedupe-key helper with explicit dev store, queue, audit, database and environment adapters. No native Prisma, Redis, HTTP or worker execution.
- The development branch changes status before awaiting queued jobs. A queue failure leaves queued state and prevents retry through this function; recovery/outbox redesign is not included. No durable delivery, atomicity or concurrency guarantee is claimed.

[Delivery manifest](../astra-remaining-improvements/deliveries/1cf37faa32e8.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/1cf37faa32e8-astra-review.json)


## g1

- Validate parent city existence before creating a shop so the catalog cannot contain orphan city references.
- Preserve valid shop normalization while rejecting unknown city IDs before any serialized store write.

**Teaching:** 9 source-based chapters; 1,631 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/lib/store.ts`
- `tests/runtime-shop-city.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src-lib-store.ts.before`
- `astraupskill/evidence/crud-b04-astra-runtime.log`
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

- Four runtime cases execute actual store and utility source with filesystem, path, slugify, clsx, scoring and schema adapters. Real nullable-text and array normalization execute; third-party slug behavior is not established.
- No native filesystem, SQL, HTTP auth, cascade, locking or concurrent write behavior executed. readStore may call mkdir before rejecting an unknown city; zero writes means zero writeFile calls, not zero filesystem activity.
- The write-failure adapter throws before storing bytes; this does not prove native writeFile is atomic or preserves a file on partial failure. Local Next.js guides absent after cleanup; no framework API was changed.

[Delivery manifest](../astra-remaining-improvements/deliveries/d7c9faad43d9.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/d7c9faad43d9-astra-review.json)


## rn1

- Invalidate the blocked-accounts query after successful unblock so the deletion is reflected in the cached list, matching the existing block path.
- Preserve remote deletion, signed-out rejection and profile feed reset behavior; add a portable Yarn learning test script.

**Teaching:** 9 source-based chapters; 1,907 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `social-app/src/state/queries/profile.ts`
- `social-app/package.json`
- `social-app/tests/crud-upskill/profile-unblock.test.mjs`
- `social-app/tests/crud-upskill/load-typescript.mjs`
- `astraupskill/snapshots/profile.ts.original.txt`
- `astraupskill/snapshots/package.json.original.txt`
- `astraupskill/evidence/crud-b04-astra-runtime3.log`
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

- Four focused cases execute the exact extracted production unblock hook and actual blocked-query key, using session/agent/query-client/AtUri doubles and an explicitly modeled mutation lifecycle.
- No mounted React, TanStack cache engine, real AT Protocol server, native Jest, lint, typecheck, Expo or mobile/browser rendering was executed.
- Invalidation schedules query refresh; this does not prove immediate removal from every list, successful refetch, rollback, request idempotency or session-switch safety.
- Application requires Node >=24.15.0; the focused Yarn script passed on device Node22.16 with explicit --ignore-engines, not a full native application compatibility check.

[Delivery manifest](../astra-remaining-improvements/deliveries/195e77d61335.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/195e77d61335-astra-review.json)


## w21

- Map Prisma P2025 concurrent deletion to the existing route not-found contract.
- Preserve unrelated persistence error identity.
- Execute the actual transition service through a dependency-free VM harness.

**Teaching:** 9 source-based chapters; 1,670 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/services/admin/gateway-route-service.ts`
- `tests/runtime-route-status.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src/services/admin/gateway-route-service.ts`
- `astraupskill/evidence/crud-b04-astra-runtime.log`
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

- Five runtime cases execute actual transition service, AppError and role policy with repository and Prisma transaction adapters. Native Vitest, Prisma/PostgreSQL and Next HTTP middleware were not run.
- P2025 is simulated after a successful pre-read; no real concurrent delete or transaction rollback was executed. Status and policy preconditions remain separate reads and are not made atomic by this error translation.

[Delivery manifest](../astra-remaining-improvements/deliveries/06f66ec88e8d.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/06f66ec88e8d-astra-review.json)


## w22

- Move payment and successful-refund reads into the refund transaction before allowance validation.
- Propagate the transaction client through the repository reads and create.
- Prove client scope and over-refund refusal with the actual service.

**Teaching:** 9 source-based chapters; 1,744 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/services/refundService.ts`
- `tests/runtime-refund-scope.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/src/services/refundService.ts`
- `astraupskill/evidence/crud-b04-astra-runtime.log`
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

- Five runtime cases execute actual refund service, state machine and RouteError with explicit repository/transaction/UUID adapters. No native Prisma, PostgreSQL, HTTP or provider payment operation was executed.
- Passing the transaction client keeps reads and writes in the same transaction, but default isolation does not by itself prevent simultaneous refunds from exceeding the allowance. No locking, serializable retry or durable idempotency was added.
- The existing service simulates provider success with a generated id; tests do not establish real-provider refunds, real database rollback or request authorization.

[Delivery manifest](../astra-remaining-improvements/deliveries/529eba39810c.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/529eba39810c-astra-review.json)


## w23

- Preserve the reviewed ticket status production path and add a runnable six-case fault-injection teaching lab.
- Exercise actual transition policy and error classes, scoped repository arguments, transaction-handle propagation, successful side-effect order and refusal/failure boundaries.

**Teaching:** 9 source-based chapters; 1,833 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `tests/runtime-ticket-boundary-lab.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/evidence/crud-b04-astra-runtime.log`
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

- No production source was changed. The lab executes actual ticket service, status policy and error classes with explicit permission, validation, document-builder, repository and transaction adapters.
- Six runtime cases do not execute native Drizzle/PostgreSQL, HTTP, real authorization policy, indexing worker or transaction rollback. An empty update result is simulated, not proof of concurrent mutation safety.

[Delivery manifest](../astra-remaining-improvements/deliveries/5df5911fc343.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/5df5911fc343-astra-review.json)


Canonical file hashes were checked when this report was generated. Passing counts refer only to the accepted suites; they are not a claim that every upstream or external-service check ran.
