# CRUD upskilling batch 02 — 2026-09-21

**10 of 10 projects delivered.** Remaining entries are pending, not accepted changes.

Luna implements most projects in isolated stages; Astra reviews correctness, meaningful test evidence and teaching quality before applying finite manifests. Protected project families and every applybot/applyboy variant are excluded.

| Project | Status | Accepted test cases | Learning guide |
|---|---|---:|---|
| _Organized Desktop/01 Net Workspaces/.netcalendy | Delivered | 11 | [Course](../../_Organized%20Desktop/01%20Net%20Workspaces/.netcalendy/astraupskill/README.md) |
| _Organized Desktop/01 Net Workspaces/.netslack | Delivered | 5 | [Course](../../_Organized%20Desktop/01%20Net%20Workspaces/.netslack/astraupskill/README.md) |
| _Organized Desktop/01 Net Workspaces/csbootcamp | Delivered | 13 | [Course](../../_Organized%20Desktop/01%20Net%20Workspaces/csbootcamp/astraupskill/README.md) |
| _Organized Desktop/02 Build Projects/buildagenthelpdesk | Delivered | 4 | [Course](../../_Organized%20Desktop/02%20Build%20Projects/buildagenthelpdesk/astraupskill/README.md) |
| _Organized Desktop/02 Build Projects/buildagentteaching | Delivered | 6 | [Course](../../_Organized%20Desktop/02%20Build%20Projects/buildagentteaching/astraupskill/README.md) |
| _Organized Desktop/02 Build Projects/buildecom | Delivered | 6 | [Course](../../_Organized%20Desktop/02%20Build%20Projects/buildecom/astraupskill/README.md) |
| _Organized Desktop/02 Build Projects/buildScedulingPYJS | Delivered | 5 | [Course](../../_Organized%20Desktop/02%20Build%20Projects/buildScedulingPYJS/astraupskill/README.md) |
| _Organized Desktop/03 Master Projects/master | Delivered | 7 | [Course](../../_Organized%20Desktop/03%20Master%20Projects/master/astraupskill/README.md) |
| _Organized Desktop/03 Master Projects/master1 | Delivered | 3 | [Course](../../_Organized%20Desktop/03%20Master%20Projects/master1/astraupskill/README.md) |
| _Organized Desktop/03 Master Projects/mastermatter | Delivered | 6 | [Course](../../_Organized%20Desktop/03%20Master%20Projects/mastermatter/astraupskill/README.md) |

**Accepted runtime tests:** 66. **Changed/added files:** 168. [Complete file-name list](CRUD_UPSKILL_BATCH_02_CHANGED_FILES_2026-09-21.txt).


## .netcalendy

- Require selected event types to match the resolved tenant and requested host before booking or availability work.
- Reject inactive event types consistently in availability while preserving valid booking, existing conflict and empty-schedule behavior.
- Add eleven executable production-source C# cases and nine linked teaching chapters on resource relationships, early rejection and evidence boundaries.

**Teaching:** 9 source-based chapters; 2,838 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/NetCalendy.Application/Bookings/Commands/CreateBooking/CreateBookingHandler.cs`
- `src/NetCalendy.Application/Schedules/Queries/GetAvailableSlots/GetAvailableSlotsHandler.cs`
- `tests/NetCalendy.ScopeHarness/NetCalendy.ScopeHarness.csproj`
- `tests/NetCalendy.ScopeHarness/MediatorContracts.cs`
- `tests/NetCalendy.ScopeHarness/Program.cs`
- `astraupskill/snapshots/src__NetCalendy.Application__Bookings__Commands__CreateBooking__CreateBookingHandler.cs.original.txt`
- `astraupskill/snapshots/src__NetCalendy.Application__Schedules__Queries__GetAvailableSlots__GetAvailableSlotsHandler.cs.original.txt`
- `astraupskill/evidence/crud-b02-scope-harness.log`
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

- Eleven handler cases compiled and executed actual linked production source on .NET10 with explicit repository and minimal MediatR contract doubles.
- Original .NET9 solution/xUnit suites, ASP.NET/MediatR pipelines, EF Core, PostgreSQL and browser integration were not executed.
- This relationship/state guard does not establish booking availability membership, timezone correctness, atomic double-booking prevention or tenant middleware behavior.

[Delivery manifest](../astra-remaining-improvements/deliveries/ef1449fa0c77.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/ef1449fa0c77-astra-review.json)


## .netslack

- Map a concurrent persisted workspace slug collision to ConflictException.
- Re-query persisted state after a save failure: occupied slug maps to conflict; absent slug preserves the original save exception.
- Verify the actual staged service and domain with a dependency-free .NET10 source-linked harness.

**Teaching:** 9 source-based chapters; 2,619 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/NetSlack.Application/Workspaces/WorkspaceService.cs`
- `tests/NetSlack.Application.Tests/WorkflowTests.cs`
- `tests/NetSlack.ScopeHarness/NetSlack.ScopeHarness.csproj`
- `tests/NetSlack.ScopeHarness/Contracts.cs`
- `tests/NetSlack.ScopeHarness/Program.cs`
- `astraupskill/snapshots/src/NetSlack.Application/Workspaces/WorkspaceService.cs`
- `astraupskill/snapshots/tests/NetSlack.Application.Tests/WorkflowTests.cs`
- `astraupskill/evidence/crud-b02-astra-harness.log`
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

- Native .NET8 test project and EF provider were not executed because only .NET10 is installed.
- Harness contracts model persisted winner state but do not prove SQL translation, unique index creation, transaction isolation, or migration behavior.
- No automatic retry or concurrent worker coordination is claimed.
- If the recovery query fails or is cancelled, its failure propagates instead of the original save error.
- Classification is based on observed slug occupancy, not proof of which database constraint caused the save failure; no automatic retry is performed.

[Delivery manifest](../astra-remaining-improvements/deliveries/7f289bf2abfa.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/7f289bf2abfa-astra-review.json)


## csbootcamp

- Add a standalone .NET10 CRUD web companion with create/list/read/replace/delete, title validation and required version preconditions on writes.
- Demonstrate atomic in-process version checks with actual loopback HTTP regressions and nine chapters covering traces, exercises, solutions and database follow-up design.

**Teaching:** 9 source-based chapters; 3,103 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `README.md`
- `guides/crud-web-lab/CrudWebLab.csproj`
- `guides/crud-web-lab/Program.cs`
- `guides/crud-web-lab/TaskStore.cs`
- `guides/crud-web-lab/HttpChecks.cs`
- `astraupskill/snapshots/README.md.original.txt`
- `astraupskill/evidence/crud-b02-http-lab.log`
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

- This new teaching companion uses in-memory single-process storage; no authentication, durable database, browser UI or deployment is included.
- The If-Match contract supports one strong numeric tag only, not full HTTP conditional request grammar.
- The original bootcamp exercise suites and scoreboard were not rerun or modified.
- One overlapping HTTP writer case checks observed behavior; exhaustive stress testing and multi-instance concurrency are outside this lab.

[Delivery manifest](../astra-remaining-improvements/deliveries/c10fc180fa35.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/c10fc180fa35-astra-review.json)


## buildagenthelpdesk

- Prevent updateTicketAction from overwriting a ticket version read earlier by requiring organization, id, and updatedAt to match in the update where clause.
- Map the known Prisma P2025 compare-and-set conflict to a reload error before audit or notification side effects, while preserving the committed update DTO for existing side-effect logic.
- Add a portable runtime regression that executes the real TypeScript action through a project-local VM loader for stale and successful paths.

**Teaching:** 9 source-based chapters; 2,965 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `apps/web/lib/actions.ts`
- `tests/runtime-ticket-update.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/apps-web-lib-actions.ts.before`
- `astraupskill/evidence/runtime-ticket-update.log`
- `astraupskill/evidence/results-crud-b02.json`
- `astraupskill/evidence/crud-b02-astra-runtime.log`
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

- Vitest, full typecheck, live Prisma/database, HTTP, and production connector timestamp precision were not run.
- The runtime test uses explicit Next, Prisma, audit, and notification doubles while executing the real updateTicketAction source.
- This guard covers the updateTicketAction read-to-write boundary; it does not claim serializable transactions, protection for unrelated unconditional ticket mutations, or detection of edits occurring before the server read.
- Domain capability, transition, normalization and SLA helpers are substituted; status-change notification fan-out is not exercised. Timestamp collisions and edits before the server read are not detected by this guard.

[Delivery manifest](../astra-remaining-improvements/deliveries/707cb3abbb7a.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/707cb3abbb7a-astra-review.json)


## buildagentteaching

- Keep expected AppError enrollment refusals as independent per-student batch results.
- Rethrow unexpected persistence and programming failures so the batch cannot hide infrastructure incidents.
- Execute the actual TypeScript enrollment service through a dependency-free source-linked runtime harness.

**Teaching:** 9 source-based chapters; 2,873 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `packages/application/src/services/enrollment-service.ts`
- `tests/runtime-bulk-enroll.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/packages/application/src/services/enrollment-service.ts`
- `tests/bulk-enroll-entry.ts`
- `astraupskill/evidence/crud-b02-astra-runtime.log`
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

- The runtime harness does not execute Prisma SQL, database rollback, Vitest, or browser actions.
- The batch remains independently transactional per student; no retries or all-or-nothing transaction were added.

[Delivery manifest](../astra-remaining-improvements/deliveries/7b18281f562f.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/7b18281f562f-astra-review.json)


## buildecom

- Protect updateOrderStatus from stale status overwrites by adding the read status to the Prisma update predicate.
- Map only Prisma P2025 to a 409 ORDER_STATUS_CHANGED error before event, audit, and buyer notification side effects while rethrowing unrelated persistence errors.
- Add six production-source runtime cases using the real transition policy and ApiError class, plus a source-specific CRUD course on state, seller scope and side effects.

**Teaching:** 9 source-based chapters; 2,836 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/server/orders/service.ts`
- `tests/runtime-order-status.test.mjs`
- `tests/helpers-load-typescript.mjs`
- `astraupskill/snapshots/src-server-orders-service.ts.before`
- `astraupskill/evidence/runtime-order-status.log`
- `astraupskill/evidence/results-crud-b02.json`
- `astraupskill/evidence/crud-b02-astra-runtime.log`
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

- Vitest, full typecheck, live Prisma, HTTP, Stripe, outbox, transaction isolation, and deployed schema support for extended unique filters were not run.
- Runtime tests execute real service source with explicit persistence and framework contracts.
- The guard covers updateOrderStatus status freshness only; it does not claim checkout inventory, refund idempotency, or unrelated order mutation safety.
- Status equality does not detect unrelated field or seller-split changes, or a status changing away and back. The transaction double does not prove real rollback; HTTP role/session and Zod validation are outside the executed suite.

[Delivery manifest](../astra-remaining-improvements/deliveries/83297bdf668f.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/83297bdf668f-astra-review.json)


## buildScedulingPYJS

- Protect appointment completion from stale status writes by requiring the status read before validation to still match during the update.
- Map only Prisma P2025 to APPOINTMENT_STATUS_CHANGED 409 before activity and audit side effects while preserving unrelated persistence errors.
- Add five production-source runtime cases using the real state machine, AppError and audit helper, with a fixed clock and source-specific course.

**Teaching:** 9 source-based chapters; 2,582 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `backend/src/modules/appointments/appointments.service.ts`
- `tests/runtime-appointment-complete.test.mjs`
- `tests/helpers-load-typescript.mjs`
- `astraupskill/snapshots/backend-appointments-service.ts.before`
- `astraupskill/evidence/runtime-appointment-complete.log`
- `astraupskill/evidence/results-crud-b02.json`
- `astraupskill/evidence/crud-b02-astra-runtime.log`
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

- Vitest, Express, full typecheck, live Prisma, transaction isolation, external notifications, and deployed schema support for extended unique filters were not run.
- Runtime tests execute actual appointmentsService.complete with explicit persistence and framework contracts.
- The guard covers completion status freshness only; cancellation, rescheduling, recurrence, and booking conflict paths remain outside this bounded change.
- Status equality does not detect other field changes or a reschedule/reconfirm cycle. Test transaction contracts do not prove database rollback; HTTP authentication/authorization and missing generated Prisma typing remain outside the executed suite.

[Delivery manifest](../astra-remaining-improvements/deliveries/cb18aae6d81d.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/cb18aae6d81d-astra-review.json)


## master

- Validate destination project ownership before task creation or PATCH reassignment; preserve title-only edits and existing task ownership filtering.
- Return 404 and perform zero task writes when the destination project is outside the user's scope.

**Teaching:** 9 source-based chapters; 3,147 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `src/app/api/tasks/[id]/route.ts`
- `src/app/api/tasks/route.ts`
- `tests/task-project-isolation.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/tasks-[id]-route.ts.original.txt`
- `astraupskill/snapshots/tasks-route.ts.original.txt`
- `astraupskill/evidence/crud-b02-runtime7.log`
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

- The regression uses explicit Prisma and auth doubles; it does not connect to a live database.
- The route's authentication wrapper is stubbed, so middleware and session construction are outside this check.
- The ownership read and task update/create are separate calls; concurrent project deletion or reassignment is outside this bounded fix.
- Schema parsing is stubbed: real Zod validation and Next HTTP handling were not exercised.

[Delivery manifest](../astra-remaining-improvements/deliveries/785c7da790a8.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/785c7da790a8-astra-review.json)


## master1

- Preserve an existing completedAt timestamp when a DONE task is updated to DONE again.
- Stamp completion only when entering DONE, clear it when reopening, and leave it untouched when status is omitted.

**Teaching:** 9 source-based chapters; 3,061 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `apps/api/src/modules/tasks/tasks.service.ts`
- `tests/tasks-service-completion.test.mjs`
- `tests/helpers/load-typescript.mjs`
- `astraupskill/snapshots/tasks.service.ts.original.txt`
- `astraupskill/evidence/crud-b02-runtime2.log`
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

- The regression invokes the real TasksService with explicit Prisma and audit doubles; it does not connect to a live database.
- The local loader removes standalone Nest decorator syntax because Node's dependency-free TypeScript stripper cannot parse it; service method logic remains actual source.
- This checks completion timestamp behavior only; concurrent task updates and database transaction behavior are outside scope.

[Delivery manifest](../astra-remaining-improvements/deliveries/39fabfbc58f5.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/39fabfbc58f5-astra-review.json)


## mastermatter

- Treat a zero-row channel update as a not-found failure instead of continuing as if the channel was updated.
- Preserve the existing multiple-row defensive failure while returning the production store not-found error for a missing channel.

**Teaching:** 9 source-based chapters; 2,752 words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.

**Changed or added files:**

- `mattermost/server/channels/store/sqlstore/channel_store.go`
- `mattermost/server/channels/store/sqlstore/channel_store_update_test.go`
- `mattermost/tests/crud-b02/run_channel_store_harness.py`
- `astraupskill/snapshots/channel_store.go.original.txt`
- `astraupskill/evidence/crud-b02-go-harness-final.log`
- `astraupskill/evidence/results.json`
- `astraupskill/evidence/toolchain-verification.json`
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

- Six Go subtests execute the exact extracted updateChannelT method and row-count helper with explicit SQL, model and error contracts.
- The native Mattermost package test, PostgreSQL integration, model validation and unique-constraint classification were not executed.
- Outer Update transaction finalization and public-channel propagation were reviewed in source only; the harness does not execute them.

[Delivery manifest](../astra-remaining-improvements/deliveries/f5bd710b171f.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/f5bd710b171f-astra-review.json)


Canonical file hashes were checked when this report was generated. Passing counts refer only to the accepted suites; they are not a claim that every upstream or external-service check ran.
