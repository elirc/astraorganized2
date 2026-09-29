from pathlib import Path
B=Path(__file__).resolve().parent.parent
names=['README.md','01-CODEBASE-MAP.md','02-CONCEPTS.md','03-WORKED-CHANGE.md','04-TESTING-AND-DEBUGGING.md','05-PRACTICE.md','06-SOLUTIONS-AND-REVIEW.md','07-TRACE-LAB.md','VERIFICATION.md']
courses={
'7ba004a89f06':[
'''# File-backed project storage

The existing [FileProjectStore](../server/services/projectStore.ts) implements get, save and clear for one uploaded project document. The [runtime workshop](../tests/project-store-runtime.test.mjs) uses real temporary filesystem operations, so you can observe serialized bytes as well as returned objects. No production implementation changed.

Study the path from caller data to data/uploaded-project.json, then compare missing, malformed and replaced storage. Exercises combine a call trace, payload prediction and a crash-consistency design review. The implementation provides a small CRUD boundary without a database server, but it does not validate UploadedProject at runtime or coordinate concurrent writers. Keep those absent guarantees separate from successful round-trip evidence.''',
'''# Follow three methods to the filesystem

The constructor combines baseDir with data/uploaded-project.json. save creates the containing directory recursively and writes JSON.stringify(project) as UTF-8. get reads UTF-8, parses JSON and returns the result as UploadedProject; any read or parse exception becomes null. clear removes the file with force:true.

ProjectStore declares the asynchronous interface, while UploadedProject is imported only as a type. That annotation does not validate parsed file contents. The runtime test supplies explicit temporary base directories and imports the actual service through the local loader. Read the physical file assertion to see how it independently checks the path and serialization rather than relying only on get.''',
'''# Replacement, absence and corruption

save replaces the complete JSON document. It does not merge file arrays or retain fields omitted by the caller. Two instances using different base directories address different documents; two instances sharing a directory address the same file.

get intentionally returns the same null result for missing storage and malformed JSON. This simplifies callers but hides the cause of failure. clear is safe to repeat because removal is forced. None of those behaviors establishes atomic writes or crash durability. Before adding retries, logging or temporary-file replacement, define whether callers need to distinguish absence from corruption and how concurrent saves should resolve. The current lab documents existing behavior without making that product decision.''',
'''# Save, inspect, read and clear

Create a temporary directory and instantiate FileProjectStore with it. Save a document named demo containing src/index.ts with content export {}. Predict the created file path, then read its bytes independently and assert that the source path appears. get should return the same name, path and content.

Next call clear and verify that get returns null; repeat clear to exercise idempotent removal. The runtime fixture cleans its own temporary directory after checking that its resolved path belongs to the temporary root. The teaching change is this executable sequence and its evidence. No upload endpoint, archive parser, authentication handler or production data file is involved in the test.''',
'''# Debug the file boundary

Run node --experimental-vm-modules --test tests/project-store-runtime.test.mjs from the project root. The loader executes the actual TypeScript class and permits its Node filesystem/path imports. The test creates isolated directories and removes only the directories it created after verifying their location.

If get returns null after save, compare the two base directories and inspect the physical JSON before assuming parsing is wrong. If malformed storage returns null, that matches the broad catch. If a second save retains old files, inspect whether the caller reused the old document; the store itself only stringifies the supplied object. These tests do not simulate a process crashing halfway through writeFile.''',
'''# Practice before the answer chapter

Predict the stored document after saving files a and b, then saving a replacement document with an empty files array. Explain whether the old array survives. Next put malformed JSON at the expected path and predict whether get rejects or returns a value.

Design a two-instance test where each store has a different base directory, then describe what changes if both receive the same directory. Finally propose a crash-during-write experiment and an observable success criterion. Identify which result needs an operating-system experiment rather than another assertion about JSON.stringify. Keep your proposed implementation changes separate from the existing runtime behavior.''',
'''# Answers and review criteria

The replacement save stores the new empty files array; no merge occurs. Malformed JSON returns null because parsing sits inside get's catch. Separate base directories isolate documents, while shared directories target the same path and need a concurrency policy if callers write simultaneously.

A crash experiment should check whether readers observe a complete previous or new document, rather than truncated bytes. A temporary write followed by rename is a possible design to investigate, not a guarantee supplied by the current class. Review the filesystem's behavior and durability requirements before adopting it. The delivered runtime cases cover ordinary replacement, absence, corruption handling and isolation, with production source preserved in the snapshot.''',
'''# Trace two saves to one path

Start with name old and a single file a. save creates the directory and replaces uploaded-project.json. Save name replacement with no files using the same instance. get reads the same path and returns only the replacement document. A second store rooted in another directory still returns its own document.

Now contrast a missing file with malformed bytes. The first path fails in readFile; the second succeeds in readFile and fails in JSON.parse. Both are caught and return null. Record those separate internal paths even though the public result is identical. This trace explains why application telemetry may need more information than the current interface exposes.''',
'''# Verification scope

Three runtime cases exercise actual filesystem I/O: save/read/physical bytes/clear, missing and malformed storage, and whole-document replacement with separate-directory isolation. Test cleanup checks the generated directory is under the temporary root before recursive removal. The [snapshot](snapshots/projectStore.ts.original.txt) preserves the unchanged service.

The run does not exercise upload routes, project-schema validation, production permissions, concurrent writers, crash consistency or durable flush behavior. Returning a typed UploadedProject after JSON.parse does not establish runtime validation. The evidence records the finite Node command and terminal count. Use those assertions as a reproducible starting point for the design exercises, rather than treating a successful local round trip as a complete storage reliability test.'''
],
'6712d23cf34a':[
'''# Invoice lifecycle and event workshop

Study [createInvoiceService](../services/billing-service/src/services/invoice-service.ts), which accepts a repository and event publisher. The [runtime lab](../tests/invoice-service-runtime.test.mjs) executes the real service with explicit persistence and publisher adapters. Production source is unchanged.

Follow tenant identity from context into invoice payloads, then compare legal and illegal transitions using persisted status. The course combines a state matrix, payload classification, call-order tracing and late-failure injection. Repository calls receive outbox data before publication, but this unit boundary cannot prove transaction durability or broker delivery. The exercises ask you to identify exactly which guarantee belongs to the service, repository and event infrastructure.''',
'''# Map repository and publisher calls

listInvoices forwards context.session.tenantId to listInvoicesByTenant. createInvoice generates invoice and event identifiers, creates billing.invoice.issued metadata and payload, and supplies an outboxEvent to repository.createInvoice. Only after that promise resolves does publish receive billing.invoice-events and the event.

updateInvoiceStatus first calls findTenantInvoiceOrThrow with tenant and invoice id. It checks allowedTransitions against the stored status, builds billing.invoice.status_changed, updates with outbox data, then publishes. The event carries correlationId, traceId and actor identity from context. Read these explicit payloads before assuming input can set tenant ownership. The test uses real service logic while contract schema imports remain inert module dependencies.''',
'''# State eligibility is not commit safety

issued permits paid, failed or void. failed permits paid or void. paid and void are terminal, and equal-status requests are invalid. The guard depends on the repository's returned status, so checking only the requested destination would lose essential lifecycle information.

Reading stored status still leaves a possible stale-read window before update. The service passes no expected prior status as a separate update predicate. Similarly, including an outboxEvent argument suggests a persistence contract but does not prove atomic storage. A publisher rejection happens after the repository resolves. Distinguish these concerns when designing retries: event identifiers, consumer deduplication, repository transactions and broker acknowledgements require their own evidence.''',
'''# Work through invoice creation

Use tenant-1 and user-1 in context, with externalReference order-1, amountCents1200 and currency USD in input. The service generates identifiers, supplies tenant and actor fields to the repository and includes billing.invoice.issued outbox metadata. The publisher runs afterward with billing.invoice-events.

For status change, take a stored failed invoice and request paid. The event payload records previousStatus failed, nextStatus paid and changedByUserId user-1; causationId is the invoice id. The expanded runtime matrix asserts these stable fields and call order while allowing fresh identifiers and timestamps. Contrast issued to issued, which stops immediately after lookup with INVALID_STATUS_TRANSITION and performs neither update nor publication.''',
'''# Debug event payloads and failure timing

Run node --experimental-vm-modules --test tests/invoice-service-runtime.test.mjs. The loader executes invoice-service.ts; repository and EventPublisher objects are injected through its existing factory. Contract imports are stubs because this run targets service behavior, not schema parsing or HTTP authentication.

If a transition fails, inspect the persisted status and destination before changing the matrix. If publication is missing, determine whether the repository rejected first. If publication fails after create, the adapter trace records the completed repository call followed by the error. Avoid interpreting that ordering as proof of committed outbox data. Stable event names, tenant, actor and causation fields are better assertions than whole-event equality with random UUIDs.''',
'''# Practice with concrete lifecycle cases

Classify externalReference, tenantId, issuedByUserId, invoiceId and eventId by whether they come from input, authenticated context or generation. Then draw the complete allowed transition matrix and predict failed to paid, paid to failed and issued to issued.

Next write an expected call trace for a publisher that rejects after createInvoice resolves. Design a second fixture where the repository rejects first and identify which call must be absent. Finally propose a real persistence test for invoice plus outbox atomicity. State the failure injection point and rows to inspect. Do not use a publisher adapter success as evidence that an external broker acknowledged anything.''',
'''# Answers and review criteria

externalReference comes from input; tenantId and issuedByUserId come from context; invoiceId and eventId are generated. failed to paid is valid, while paid to failed and issued to issued are rejected. A publisher failure follows the repository call; a repository failure prevents publication entirely.

An outbox integration test should force a failure while persisting invoice and event data, then inspect both tables through a separate transaction. Review whether the repository guarantees they commit together and whether retry processing duplicates events. The current service test cannot establish those properties. It does verify all five legal edges, terminal/unknown-state refusals, tenant forwarding and stable event fields against the actual implementation.''',
'''# Trace failure across the event boundary

For createInvoice, record identifier generation, repository.createInvoice with outboxEvent, then publish. Make publish throw broker unavailable. The caller receives rejection even though the repository adapter already returned. Now make the repository throw db unavailable and confirm no publish call follows.

Compare those traces with an illegal status transition, which performs only the tenant-scoped lookup. The three paths have different retry implications. The service alone cannot tell whether a real persistence failure happened before or after commit, nor whether an event was externally delivered before acknowledgement failed. Use this trace to formulate integration questions rather than adding a blanket retry around the entire method.''',
'''# Six-case verification

Six runtime cases cover creation ordering, illegal equal-status refusal, all legal transition edges with event metadata, terminal and unknown-state refusals, tenant-scoped listing with late publisher failure, and repository failure suppressing publication. The [snapshot](snapshots/invoice-service.ts.original.txt) preserves unchanged production source.

Repository and publisher adapters are explicit; contract schemas and framework types are not executed. No PostgreSQL transaction, outbox commit, broker acknowledgement, HTTP authentication or concurrent state update is verified. The service reads current state but the lab does not prove stale-write prevention. The finite command in the debugging chapter and saved terminal evidence establish exactly the service-level behaviors exercised by this lesson.'''
],
'c558dc8dae3b':[
'''# TraceVault read and aggregation workshop

The existing [TraceVaultService](../packages/core/src/service.ts) lists projects and sessions, searches session text and aggregates usage across SourceAdapter implementations. This lesson explores the read side of CRUD: filtering available sources, mapping records, resolving identifiers and building derived views. Production source is unchanged.

The [runtime lab](../tests/trace-vault-service-runtime.test.mjs) supplies deterministic adapters while executing the actual service. Exercises combine call tracing, search prediction, aggregation arithmetic and a performance review. Pay attention to the misleading cache name: resolveProjectCache builds a new map on each call. The lab proves orchestration behavior, not provider parsing, filesystem discovery, UI rendering or search-index performance.''',
'''# Follow source, project and session lookup

listSources returns configured source descriptors. sourceStatus also calls detect, even for disabled sources. listProjects instead skips disabled sources before detection and skips undetected sources before listing. It maps adapter project fields and sorts descending by lastActivityAt.

listSessions resolves a project entry and returns an empty array if absent. getSession rebuilds the project map, lists sessions for each project and reads the first matching reference, otherwise returning null. listAllSessions merges references and sorts updatedAt. searchFallback and usageStats call these methods repeatedly. The runtime fixtures adapt provider I/O only; the mapping, filtering, loops and aggregation are actual service code. Keep each method's disabled-source behavior distinct.''',
'''# Reads can hide repeated work

resolveProjectCache creates a fresh Map rather than retaining one between calls. searchFallback first lists all sessions, then calls getSession for each reference, which resolves projects and sessions again. This is correct for the small fixture but deserves measurement for large providers.

Search matches case-insensitively across userText, assistantText and thinkingBlocks, then truncates the returned snippet to400 characters. A match can therefore come from text beyond the visible snippet. usageStats counts session references separately from successfully read sessions. These details affect API expectations and performance. Do not infer redaction, indexing or stable snapshot behavior from a service that repeatedly asks live adapters for data.''',
'''# Work through a one-session fixture

The adapter exposes project p1 and session s1 dated2025-01-01. Its first turn has user text find invoice, assistant text found, prompt tokens2 and completion tokens3. listProjects maps sourceId from the adapter; listSessions returns s1; searching invoice finds that turn.

The expanded aggregation fixture adds another turn without token usage and tools read, read and write. Predict two total turns, prompt2, completion3, read frequency2 and write frequency1, with one activity count for the session's day. The tests assert those exact outputs. No source algorithm was rewritten: the improvement is an executable set of examples showing how record reads become search and usage views.''',
'''# Debug filtering and derived output

Run node --experimental-vm-modules --test tests/trace-vault-service-runtime.test.mjs. The loader executes packages/core/src/service.ts while replacing adapter construction and supplying explicit SourceAdapter instances. It does not load real filesystem or external provider implementations.

When a project disappears, inspect source enablement, detect result and filterSourceId in that order. For missing sessions, inspect project resolution before assuming readSession failed. For search, compare the full combined text with the truncated snippet. For usage, check absent tokenUsage defaults separately from tool-call counts. Provider exceptions propagate rather than being converted to empty results. The failure fixture makes that distinction visible without hiding an outage behind a successful empty list.''',
'''# Practice before reading solutions

Predict whether a disabled adapter's detect method runs in listProjects and in sourceStatus. Then arrange projects with activity dates2024 and2025 and state their returned order. Add an unknown project id and predict listSessions.

For search, place Needle in thinkingBlocks after500 characters of user text. Query NEEDLE with limit1 and predict match count, snippet length and whether the matched word must appear in the snippet. Finally inspect usageStats with one turn missing tokenUsage and two read tool calls. Write exact totals before running the lab. Propose a measurement of repeated adapter reads without replacing the service with a copied algorithm.''',
'''# Answers and review questions

listProjects skips disabled detection, while sourceStatus detects every configured adapter. Projects return2025 before2024. An unknown project gives an empty session array. Case-insensitive search finds Needle in thinkingBlocks, returns one result for positive limit1, and truncates text to400 characters; the matching word may lie outside that snippet.

Missing tokenUsage contributes zero, while every tool-call entry increments its named frequency. To measure repeated reads, count detect, listProjects, listSessions and readSession calls for an increasing number of references. Review caching only after defining freshness and invalidation requirements. Also inspect project-id uniqueness: the temporary map uses project.id as its key, so adapter collisions require a separate contract discussion.''',
'''# Trace a search request

searchFallback lowercases the query and obtains references through listAllSessions. For each reference it calls getSession, which rebuilds project lookup and locates the matching session again. It joins user, assistant and thinking text, checks the lowercase combined string, adds a400-character snippet and stops when its positive limit is reached.

Trace a provider exception separately: a failing listProjects call rejects the operation rather than returning no projects. That matters when distinguishing an empty account from unavailable storage. The lab deliberately tests a positive limit; behavior for zero or negative limits is not established as a validated API contract. Route validation and real provider performance remain separate follow-up work.''',
'''# Verification boundaries

Five runtime cases cover source/project/session reads, baseline search and aggregation, disabled/undetected filtering with sorted mapping and missing records, case-insensitive thinking-text search with snippet truncation and positive limit, and complete usage/tool/day totals plus provider-error propagation. The [snapshot](snapshots/service.ts.original.txt) preserves the unchanged service.

Adapters supply deterministic records. No real provider parser, filesystem detection, MCP transport, UI, index, redaction policy or benchmark executes. The service's temporary map and repeated reads are source observations, not measured performance claims. Tests do not certify project-id uniqueness or nonpositive search limits. Use the concrete fixtures and saved terminal evidence to distinguish executed behavior from the proposed integration and design exercises.'''
]}
for id,chapters in courses.items():
 for name,text in zip(names,chapters):(B/'stage'/id/'astraupskill'/name).write_text(text+'\n',encoding='utf-8')
