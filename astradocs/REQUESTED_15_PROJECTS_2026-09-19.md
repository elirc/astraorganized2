# Requested fifteen-project improvement report

**15 of 15 selected projects delivered.** All selected work is complete.

Delivered work has **643 passing test cases**, **37 successful recorded checks**, and **400 verified delivered file hashes**. Test counts describe the accepted per-project suites, not a claim that every upstream suite was run.

Sol agents contributed initial staged changes. At the user's request, Astra took over the remaining implementation, review, checks and delivery without subagents. Existing Fable work and documentation are preserved. Each delivered project includes nine source-based `astraupskill` chapters, exercises and solutions, verification logs, and original snapshots for changed baseline files.

| Project | Status | Passing tests | Evidence |
|---|---|---:|---|
| [gitjira-app](../../gitjira-app) | Delivered | 147 | [Course](../../gitjira-app/astraupskill/README.md), [checks](../../gitjira-app/astraupskill/VERIFICATION.md) |
| [globehire](../../globehire) | Delivered | 8 | [Course](../../globehire/astraupskill/README.md), [checks](../../globehire/astraupskill/VERIFICATION.md) |
| [mobiletagalog](../../mobiletagalog) | Delivered | 10 | [Course](../../mobiletagalog/astraupskill/README.md), [checks](../../mobiletagalog/astraupskill/VERIFICATION.md) |
| [netairag](../../netairag) | Delivered | 11 | [Course](../../netairag/astraupskill/README.md), [checks](../../netairag/astraupskill/VERIFICATION.md) |
| [netdrop](../../netdrop) | Delivered | 22 | [Course](../../netdrop/astraupskill/README.md), [checks](../../netdrop/astraupskill/VERIFICATION.md) |
| [netopen3](../../netopen3) | Delivered | 4 | [Course](../../netopen3/astraupskill/README.md), [checks](../../netopen3/astraupskill/VERIFICATION.md) |
| [netopen5](../../netopen5) | Delivered | 10 | [Course](../../netopen5/astraupskill/README.md), [checks](../../netopen5/astraupskill/VERIFICATION.md) |
| [skillforgejs](../../skillforgejs) | Delivered | 28 | [Course](../../skillforgejs/astraupskill/README.md), [checks](../../skillforgejs/astraupskill/VERIFICATION.md) |
| [aral](../../aral) | Delivered | 102 | [Course](../../aral/astraupskill/README.md), [checks](../../aral/astraupskill/VERIFICATION.md) |
| [astra1](../../astra1) | Delivered | 49 | [Course](../../astra1/astraupskill/README.md), [checks](../../astra1/astraupskill/VERIFICATION.md) |
| [astra5](../../astra5) | Delivered | 34 | [Course](../../astra5/astraupskill/README.md), [checks](../../astra5/astraupskill/VERIFICATION.md) |
| [buildermentor](../../buildermentor) | Delivered | 38 | [Course](../../buildermentor/astraupskill/README.md), [checks](../../buildermentor/astraupskill/VERIFICATION.md) |
| [buildevent](../../buildevent) | Delivered | 11 | [Course](../../buildevent/astraupskill/README.md), [checks](../../buildevent/astraupskill/VERIFICATION.md) |
| [buildreviewer](../../buildreviewer) | Delivered | 72 | [Course](../../buildreviewer/astraupskill/README.md), [checks](../../buildreviewer/astraupskill/VERIFICATION.md) |
| [.netarchitectureproject](../../.netarchitectureproject) | Delivered | 97 | [Course](../../.netarchitectureproject/astraupskill/README.md), [checks](../../.netarchitectureproject/astraupskill/VERIFICATION.md) |

## Changes and additions delivered

### gitjira-app

- Coordinated sprint assignment, start and completion with bounded serializable transactions and state-qualified writes.
- Validated completion destinations and protected browser assignments with strictly advancing timestamp comparisons.
- Added real PostgreSQL regressions and made socket test synchronization and cleanup deterministic; added nine source-based guide chapters.

**Changed source/configuration files:** `apps/api/src/controllers/sprint.controller.js`, `apps/api/src/services/issue.service.js`, `apps/api/src/services/sprint.service.js`, `apps/api/test/issue-concurrency.test.js`, `apps/api/test/issue.test.js`, `apps/api/test/socket.test.js`, `apps/api/test/sprint.test.js`, `apps/web/src/lib/hooks.js`, `apps/web/src/pages/BacklogPage.jsx`, `packages/shared/src/issue-schemas.js`.

**Added source/test/setup files:** `apps/web/test/backlog-stale-assignment.test.jsx`, `scripts/test-local.py`.

**Verification limits:** API database checks do not certify deployed Redis workers or browser end-to-end behavior.

[Delivery manifest](../astra-remaining-improvements/deliveries/5be7edf43612.json)

### globehire

- Added application-level regressions proving client-scoped hire-case completion and submission cannot mutate another client's aggregate.
- Verified valid owner completion records the injected UTC audit time and increments the optimistic version once.
- Verified a stale owner version preserves the untouched checklist item and reports the stable concurrency business error.
- Added nine source-grounded learning chapters that trace route identity, repository keys, aggregate transitions, testing, and operational limits.

**Added source/test/setup files:** `tests/GlobeHire.Application.Tests/HireCases/HireCaseTenantIsolationTests.cs`.

**Verification limits:** The project uses singleton in-memory repositories and does not prove durable or distributed transaction behavior. ClientId is supplied by the teaching API route; authentication and organization membership are outside this change. The targeted application test project was run; no external providers, databases, or broad solution checks were used.

[Delivery manifest](../astra-remaining-improvements/deliveries/509c3537abdd.json)

### mobiletagalog

- Added serial, generation-bound synchronization and atomic baseline plus sent-event acknowledgement.
- Preserved events recorded during in-flight sync; prevented late responses, stale refreshes and profile updates from restoring prior sessions.
- Distinguished guest adoption from signed-in account switching and added regression fixtures and source-based guides.

**Changed source/configuration files:** `package-lock.json`, `package.json`, `src/lib/progress.tsx`, `src/lib/storage.ts`.

**Added source/test/setup files:** `src/core/events.test.ts`, `src/lib/storage.test.ts`, `src/lib/sync.test.ts`, `src/lib/sync.ts`.

**Verification limits:** Provider and Expo SQLite tests use controlled fixtures; no native-device durability or live server integration is claimed. Source review covers React provider wiring; pure coordinator tests do not constitute a complete device UI run.

[Delivery manifest](../astra-remaining-improvements/deliveries/1bf7dd59f47b.json)

### netairag

- Added deterministic runbook retrieval with weighted fields, stable ties, bounded results and explicit no-match handling.
- Persisted actual log and document evidence using JSON serialization, accurate tool counts and timestamps, and explicit zero model usage.
- Added loaded evaluation fixtures, permission and saved-evidence regressions, and nine source-based course chapters.

**Changed source/configuration files:** `sample-eval-cases/README.md`, `src/Infrastructure/Operations/OperationsService.cs`, `tests/UnitTests/NetAiOps.UnitTests.csproj`.

**Added source/test/setup files:** `sample-eval-cases/retrieval.json`, `src/Application/Retrieval/LexicalRetriever.cs`, `tests/UnitTests/LexicalRetrieverTests.cs`, `tests/UnitTests/OperationsServiceTests.cs`.

**Verification limits:** Service tests use EF InMemory, not PostgreSQL; no relational isolation or deployed end-to-end claim is made. Retrieval uses ASCII lexical tokens and materializes the knowledge corpus; model services are not called.

[Delivery manifest](../astra-remaining-improvements/deliveries/6ee92f3ab313.json)

### netdrop

- Validated SHA-256 declarations, overflow-safe chunk counts, exact chunk boundaries, and terminal upload lifecycle transitions.
- Made accepted chunk files immutable under competing uploads, preserved identical retries, bounded oversized input reads, and isolated assembled-stream temporary files.
- Checked actual assembled length and checksum before blob or database graph writes; added a pure, overflow-safe quota preflight before external storage.
- Repaired the FileNode.Versions EF relationship mapping conflict exposed by actual context-model initialization.
- Added domain, real-filesystem, and fresh-context handler regressions; the final project suite passed all 22 tests.
- Added nine source-based guide chapters with worked traces, exercises, solutions, exact original snapshots, and recorded verification evidence.

**Changed source/configuration files:** `src/NetDropbox.Application/Abstractions/IChunkStorage.cs`, `src/NetDropbox.Application/Common/Hashing.cs`, `src/NetDropbox.Application/Uploads/CompleteUpload.cs`, `src/NetDropbox.Application/Uploads/UploadChunk.cs`, `src/NetDropbox.Domain/UploadSession.cs`, `src/NetDropbox.Domain/UserStorageAccount.cs`, `src/NetDropbox.Infrastructure/Persistence/NetDropboxDbContext.cs`, `src/NetDropbox.Infrastructure/Storage/FileSystemChunkStorage.cs`, `tests/NetDropbox.Tests/Domain/UploadSessionTests.cs`, `tests/NetDropbox.Tests/Domain/UserStorageAccountTests.cs`, `tests/NetDropbox.Tests/NetDropbox.Tests.csproj`.

**Added source/test/setup files:** `tests/NetDropbox.Tests/Uploads/FileSystemChunkStorageTests.cs`, `tests/NetDropbox.Tests/Uploads/UploadHandlerTests.cs`.

**Verification limits:** Handler persistence tests use EF InMemory with fake external storage and queue ports; they do not establish SQL uniqueness, rollback, or concurrent database isolation. Filesystem concurrency tests use real temporary files on this Windows host. API-host, frontend, and deployed end-to-end checks were not part of the accepted test command. Blob persistence, database commit, and subsequent queue notification remain separate resource boundaries. No unsafe shared-blob deletion compensation was added; durable recovery requires its own protocol.

[Delivery manifest](../astra-remaining-improvements/deliveries/8e9229d5d6ef.json)

### netopen3

- Replaced repeated index sorting with first-payload lookup and requested-ID iteration, excluding unrequested and duplicate entities.
- Added template-controller regressions for missing/extra results, duplicate payloads and preserved empty-page metadata.
- Added nine source-based guide chapters with focused verification evidence.

**Changed source/configuration files:** `Umbraco-CMS/src/Umbraco.Cms.Api.Management/Controllers/ManagementApiControllerBase.cs`, `Umbraco-CMS/tests/Umbraco.Tests.UnitTests/Umbraco.Cms.Api.Management/Controllers/Template/Item/SearchTemplateItemControllerTests.cs`.

**Added source/test/setup files:** `scripts/template-order-tests/Directory.Packages.props`, `scripts/template-order-tests/TemplateOrder.Tests.csproj`.

**Verification limits:** Controller tests use service and mapper substitutes; they do not certify production search, database or browser authorization behavior. Focused unit verification does not imply the complete upstream Umbraco test suite passed.

[Delivery manifest](../astra-remaining-improvements/deliveries/b8fb41bd6255.json)

### netopen5

- Rejected nonpositive and integer-doubling-overflow latest-media limits before user or library access.
- Preserved the twenty-item default, valid query forwarding, and the shared legacy-route guard.
- Added focused controller regressions and nine source-based guide chapters.

**Changed source/configuration files:** `jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs`.

**Added source/test/setup files:** `jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs`.

**Verification limits:** Tests use mocked library collaborators, not a running Jellyfin server or real media scan. The arithmetic bound is not a production capacity or rate-limit guarantee; HTTP binding and middleware are outside these focused tests.

[Delivery manifest](../astra-remaining-improvements/deliveries/7115d7be5ffc.json)

### skillforgejs

- Made completion, review seeding, XP, quests, achievements and progress one transaction with a unique completion gate.
- Propagated transaction clients and one captured time through nested award helpers, with selective bounded SQLite contention retries.
- Added guarded temporary-SQLite regressions and nine source-based guide chapters.

**Changed source/configuration files:** `src/server/actions.ts`, `src/server/gamification.ts`, `src/server/quests.ts`, `src/server/review.ts`.

**Added source/test/setup files:** `scripts/test-completion-local.mjs`, `src/server/completion.ts`, `tests/unit/completion.test.ts`.

**Verification limits:** SQLite tests do not exercise browsers or external code runners. Ordinary unit runs skip the destructive completion suite unless the owned-database helper enables it.

[Delivery manifest](../astra-remaining-improvements/deliveries/9d3b119f40a0.json)

### aral

- Deduplicated progress events before ordering with first-arrival payload semantics, preventing retry XP inflation.
- Serialized local records, remote merges, clock corrections and hydration; reconciled live state from persisted events after writes and partial failures.
- Added shared reducer and stateful store regressions, plus nine source-based guide chapters.

**Changed source/configuration files:** `packages/app/src/db/sync/outbox.ts`, `packages/app/src/state/store.ts`, `packages/shared/src/derived.test.ts`, `packages/shared/src/derived.ts`, `packages/shared/src/events.ts`.

**Added source/test/setup files:** `packages/app/src/state/store.test.ts`.

**Verification limits:** Store tests use a Map-backed DAO fixture, not native device SQLite; native persistence durability and rollback are not established. Queue ordering is process-local and preserves the existing DAO replacement semantics.

[Delivery manifest](../astra-remaining-improvements/deliveries/46f416b83060.json)

### astra1

- Added a real PostgreSQL late-postmortem failure regression proving repair effects and command receipt roll back together.
- Verified same-command recovery and replay without rewriting the existing repair implementation.
- Added an owned PostgreSQL/API/browser verification helper and source-based guides, including the repository upskilling location.

**Changed source/configuration files:** `docs/project/current-state.md`, `tests/integration/repair.test.ts`.

**Added source/test/setup files:** `docs/exec-plans/003-repair-rollback-regression.md`, `scripts/test-owned-postgres.py`, `upskilling/repair-rollback/01-CODEBASE-MAP.md`, `upskilling/repair-rollback/02-CONCEPTS.md`, `upskilling/repair-rollback/03-WORKED-CHANGE.md`, `upskilling/repair-rollback/04-TESTING-AND-DEBUGGING.md`, `upskilling/repair-rollback/05-PRACTICE.md`, `upskilling/repair-rollback/06-SOLUTIONS-AND-REVIEW.md`, `upskilling/repair-rollback/07-TRACE-LAB.md`, `upskilling/repair-rollback/README.md`, `upskilling/repair-rollback/VERIFICATION.md`.

**Verification limits:** Local fixture workflows do not certify real physical systems, external model providers or public deployment. Human learning remains unassessed; prior completed program evidence is preserved separately.

[Delivery manifest](../astra-remaining-improvements/deliveries/a8435f7ed53c.json)

### astra5

- Separated pending refunds into retryable and exhausted groups while retaining merchant-scoped totals.
- Displayed distinct operational counts and guidance toward the authorized order recovery action.
- Added a real PostgreSQL merchant/boundary regression, frontend mapping coverage, and nine source-based guide chapters.

**Changed source/configuration files:** `scripts/integration.mjs`, `services/Fulfil/Services/ReadApi.cs`, `src/components/Panels.tsx`.

**Added source/test/setup files:** `scripts/test-refund-health.py`, `src/lib/health.ts`, `tests/Fulfil.Tests/RefundHealthTests.cs`, `tests/health.test.ts`.

**Verification limits:** Health counts are separate reads, not an atomic reporting snapshot. Database tests call the API function directly; frontend tests cover mapping, not browser interaction or provider refunds.

[Delivery manifest](../astra-remaining-improvements/deliveries/37844e1ec56d.json)

### buildermentor

- Separated retrieval dependencies and deterministic ranking while retaining the production parameterized SQL adapter.
- Validated query vectors and returned a safe typed unavailable error for embedding and query failures.
- Added local provenance, ranking, SQL-construction and failure regressions plus nine source-based guide chapters.

**Changed source/configuration files:** `apps/api/src/rag/retrieve.ts`.

**Added source/test/setup files:** `apps/api/test/fixtures/reliability.md`, `apps/api/test/ingest-retrieval.test.ts`.

**Verification limits:** SQL adapter tests compile the query with a mocked executor; they do not prove database-backed tenant isolation. No live embedding/model quality or non-Markdown parsing claim is established.

[Delivery manifest](../astra-remaining-improvements/deliveries/a81b176807e5.json)

### buildevent

- Used stable checkout provider keys, guarded amount validation and conditional payment-intent persistence.
- Made inventory/ticket completion and event-bound check-in choose one winner, and rejected falsely successful cancelled free checkout.
- Added stateful provider/persistence regressions and nine source-based guide chapters.

**Changed source/configuration files:** `apps/api/src/routes/checkin.routes.ts`, `apps/api/src/services/checkin.service.ts`, `apps/api/src/services/order.service.ts`.

**Added source/test/setup files:** `apps/api/tests/order-checkin.test.ts`.

**Verification limits:** Tests simulate Prisma, Stripe and QR verification; they do not establish real database isolation, cryptographic verification or provider exactly-once delivery. QR generation remains post-commit; remote provider effects and QR recovery are separate operational boundaries.

[Delivery manifest](../astra-remaining-improvements/deliveries/af5130b3aad2.json)

### buildreviewer

- Atomically claimed draft reviews before publication and blocked competing callers.
- Preserved ambiguous provider/local-finalization outcomes as a retry gate; made rejection annotations and release transactional.
- Added controlled provider and SQLite rollback regressions plus nine source-based guide chapters.

**Changed source/configuration files:** `apps/api/src/modules/publish/publish.service.ts`, `apps/api/test/api.e2e.spec.ts`, `apps/api/test/fake-provider.ts`, `apps/api/test/global-setup.cjs`, `packages/shared/src/enums.ts`.

**Verification limits:** External publication is simulated with a fake provider; no live GitHub review or exactly-once guarantee is established. Ambiguous or interrupted publications still require manual reconciliation.

[Delivery manifest](../astra-remaining-improvements/deliveries/3b9c30ec3ce2.json)

### .netarchitectureproject

- Preserved requested meeting end dates in create and change handlers.
- Rejected zero or reversed meeting intervals through a shared domain business rule.
- Added actual handler and value-object regressions; passed 97 unit tests and added nine source-based guide chapters.

**Changed source/configuration files:** `modular-monolith-with-ddd/src/Modules/Meetings/Application/Meetings/ChangeMeetingMainAttributes/ChangeMeetingMainAttributesCommandHandler.cs`, `modular-monolith-with-ddd/src/Modules/Meetings/Application/Meetings/CreateMeeting/CreateMeetingCommandHandler.cs`, `modular-monolith-with-ddd/src/Modules/Meetings/Domain/Meetings/MeetingTerm.cs`.

**Added source/test/setup files:** `modular-monolith-with-ddd/src/Modules/Meetings/Domain/Meetings/Rules/MeetingTermMustEndAfterStartRule.cs`, `modular-monolith-with-ddd/src/Modules/Meetings/Tests/UnitTests/Meetings/MeetingTermCommandHandlerTests.cs`, `modular-monolith-with-ddd/src/Modules/Meetings/Tests/UnitTests/Meetings/MeetingTermTests.cs`.

**Verification limits:** Repository substitutes establish handler and aggregate behavior, not SQL transaction rollback or HTTP/browser behavior.

[Delivery manifest](../astra-remaining-improvements/deliveries/209d90f0603b.json)

## Campaign status

The campaign ledger is **107 of 239 complete**; **132 project families remain queued**. See the [remaining list](REMAINING_PROJECTS_TO_DO_2026-09-19.md).

The [earlier fourteen-project completion report](COMPLETED_14_PROJECTS_2026-09-19.md) is preserved as historical evidence. The 153 earlier Astra projects covered by Fable remain outside this campaign queue.

[Verified delivery counts and hashes](../astra-remaining-improvements/batch-sol-requested-15-20260919/delivery-verification.json). Failed or interrupted setup/check attempts remain in the campaign logs; only accepted terminal-zero checks count as passing evidence.
