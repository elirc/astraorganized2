from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/a80284ee08de'
chapters={
'README.md':('Job-board moderation: one terminal decision',"""
This course studies a small administrative job board built with Next.js, Prisma and TypeScript. Its central change is a moderation workflow in which two operators cannot both close the same case and write contradictory terminal audits. The associated improvements make service-level input validation explicit and keep paged lists deterministic when timestamps tie. You will read the real service, repository and tests before proposing another workflow command.

Prerequisites are async functions, object types, HTTP methods and basic relational tables. A case is OPEN or IN_REVIEW before resolution and RESOLVED or DISMISSED afterwards. A conditional write updates a row only while its expected state still matches. A unit of work supplies repositories sharing one transaction client. An audit is a retained record of the accepted command, not an independent best-effort logging message. These terms appear in moderationService.ts, moderationCaseRepository.ts and unitOfWork.ts.

Install using `npm ci` in the project root, generate the Prisma client with `npm run prisma:generate`, then run `npm test`, `npm run typecheck` and `npm run build`. The unit suite does not require a database. Running the full application requires your own local PostgreSQL setup as described in the root documentation. The verification in this course does not initialize or reset an existing database.

Read chapters 01 through 04, do the exercises before reading their solutions, then explain the competing-request trace in chapter 07 aloud. The tests distinguish orchestration with fakes from actual Prisma query arguments. Neither is presented as a live PostgreSQL concurrency run. The signed demo-session mechanism is retained for learning; requesting a role from a demo endpoint does not establish a production identity system. Treat deployment authentication, database provisioning and operational monitoring as separate work, not hidden guarantees of this change.
""",None),
'01-CODEBASE-MAP.md':('From HTTP command to transaction repositories',"""
The moderation route resolves the demo session, parses input and calls resolveModerationCase. The service repeats runtime validation so an internal caller cannot bypass the schema merely because TypeScript accepted its declared type. Permission is checked before parsing or reading the case. The service then enters runInTransaction and obtains the current case through the repositories supplied to that callback.

Read src/services/serviceDeps.ts next. It defines the injectable dependency set. Its production implementation uses withRepositoryTransaction from unitOfWork.ts. That function constructs new repositories around the transaction client. The distinction matters: reading through the module's default repository inside an otherwise transactional function still uses the wrong connection. The regression suite passes distinct outer and transaction repository objects to expose this mistake.

moderationCaseRepository.ts owns the conditional updateMany predicate. Its where clause includes both case ID and expected current status. Zero affected rows throws InvalidStateTransitionError, which errorToResponse maps to HTTP 409. A successful write is followed by a reread using the same transaction client, returning a populated record for the audit and response.

The posting and saved-search services already had useful transactional structure. The new work parses their runtime inputs with strict schemas before entering that structure. Saved-search ownership continues to come from session.userId; a client ownerId is rejected as an unknown field. Posting decisions retain their original conditional state update. Both posting and moderation list queries now end their ordering with a stable ID.

Read tests/unit/boundaries.test.ts after these files. It proves correct dependency use, malformed-input rejection, a controlled competing read, and repository query shapes. The existing focused tests remain part of the full suite rather than being replaced by a standalone demonstration.
""",('src/repositories/unitOfWork.ts','export function createRepositorySet',None)),
'02-CONCEPTS.md':('Why validation and conditional writes both matter',"""
A transaction and a state predicate solve different problems. A transaction groups the accepted row mutation and its audit so an exception can abort the unit of work. A conditional predicate rejects a decision whose expected state has already changed. Reading OPEN earlier and then updating only by ID allows a later request to overwrite RESOLVED even if each request uses a transaction. The predicate must reach the database write.

The service accepts only OPEN or IN_REVIEW as sources for resolution. It then passes that observed state into the repository. If another command wins first, updateMany returns a count other than one. A typed state-transition error carries conflict semantics to the HTTP boundary. A generic Error would become 500 and misleadingly present a normal stale-request outcome as an unexpected server failure.

Type annotations disappear at runtime. Parsing at the service boundary protects direct callers and future transports as well as today's route. Strict objects reject unrecognized fields rather than silently discarding them. The parsed result is used for writes, preserving trimmed strings and validated enums. A discriminated posting decision also prevents moderation-only fields from appearing in an approval command.

Ownership remains server-derived. Saved-search create and update use the session user ID even when repositories are injected. Partial updates retain omitted properties, and an empty patch is rejected by the existing refinement. Validation must not manufacture a filters object when the caller only changes a name.

Finally, deterministic ordering makes page boundaries reproducible when status and timestamp tie. Adding ID as the last sort key improves this property without claiming a snapshot across concurrent list/count reads. The application still needs a separate policy if it must show a perfectly consistent paginated snapshot during concurrent insertion.
""",('src/repositories/moderationCaseRepository.ts','    async resolveCase(input)',None)),
'03-WORKED-CHANGE.md':('Move the read and guard the write',"""
The earlier staged moderation service read the current case through deps.moderationCaseRepository before entering the transaction. It passed an expected status to the repository, which was a useful start, but the source plan required the actual read to share the transaction boundary. The draft repository also threw a generic Error on a stale update, producing an HTTP 500 instead of a conflict.

The completed service checks permission, parses resolveModerationCaseSchema, enters runInTransaction and reads from its supplied repositories. Missing cases produce NotFoundError. Terminal or unknown states produce InvalidStateTransitionError before a write. The accepted source status becomes expectedCurrentStatus. Only after the conditional update succeeds does the service create the audit, using the persisted result's ID and status.

Runtime parsing was added to posting creation/decision, moderation filters/resolution and saved-search create/update. Their schemas use strictObject so client actor or owner properties cannot be silently accepted. Existing role rules, saved-search ownership and posting transaction behavior were preserved. This is an extension of those boundaries, not a claim that they were previously absent.

Read the production function below and compare it with the original snapshot. Run `npm test -- -t "transaction-scoped repositories"` to see a test deliberately supply different repository sets outside and inside the callback. It should fail if you change the read back to deps. Then run the stale-write repository test: removing expectedCurrentStatus from the where clause should fail its argument assertion.

Do not use those temporary mutations as a replacement for reviewing the code. The tests show particular observable contracts; the production transaction helper must still be inspected to establish that the injected callback is actually backed by Prisma's transaction API.
""",('src/services/moderationService.ts','export async function resolveModerationCase',None)),
'04-TESTING-AND-DEBUGGING.md':('Three layers of evidence',"""
The suite uses three kinds of test. Validation tests invoke actual services with malformed inputs and require rejection before runInTransaction. Dependency tests supply distinct transaction repositories and assert that the service uses them for read, write and audit. Repository tests construct the real Prisma adapter with a fake client and inspect the actual where and data arguments sent to updateMany. Each layer catches a different way an apparently correct helper can be disconnected from the application.

The competing-action test synchronizes two reads using a promise barrier. Both calls receive an OPEN snapshot before either writes. The fake conditional write changes its shared state synchronously; the second call observes a mismatch and rejects. The test requires one fulfilled result, one rejected result and one audit. A sequential retry test alone would not establish that the service propagates a stale expected state correctly.

The audit-failure test supplies a rollback-capable fixture. Its transaction runner snapshots the fixture state, restores it when the callback throws, and rethrows the error. This establishes that the service keeps the audit inside the callback and does not swallow its failure. It does not prove PostgreSQL rollback: that requires a disposable database integration run.

When debugging a failed case, first establish which boundary failed. A short resolution note should cause schema rejection rather than reach the concurrency branch. An ANALYST must be forbidden before the transaction. A missing case is 404, an already decided case is 409, and an unexpected provider outage is still 500. Avoid rewriting all failures as conflicts.

After focused tests pass, run the full suite and typecheck. A passing focused test can miss unrelated contract changes in the posting or saved-search services. The production build then checks framework integration. Verification records retain exact commands and explain the absence of a live database race test.
""",('tests/unit/boundaries.test.ts','  it("allows one of two','  it("propagates audit')),
'05-PRACTICE.md':('Practice the boundaries independently',"""
Exercise 1: add a service test for an IN_REVIEW case resolved by a MODERATOR. Use the fake dependency factory but return a detached case snapshot. Assert that expectedCurrentStatus is IN_REVIEW, resolvedById comes from the session, and the audit records the exact previous and next states. Add a negative version using an ANALYST and prove that no transaction begins. The accepted result must contain the intended case ID, not merely be truthy.

Exercise 2: test the successful Prisma repository branch. Supply updateMany returning count one and findUniqueOrThrow returning a realistic row including posting and company. Verify the update predicate, resolution timestamp and actor. Assert that the returned DTO contains companyName and postingTitle from the included relation. Then return count zero and prove that the reread is never called. This exercise tests the production adapter, not a separate reimplementation of it.

Exercise 3: add saved-search update tests for a name-only patch and a filters-only patch. The name should be trimmed without introducing filters. An empty filters object is an intentional accepted replacement; an entirely empty patch is rejected. A foreign ownerId property must be rejected and no write should occur. For accepted writes, the repository's owner argument must always be session.userId.

For each exercise, explain the service boundary, persistence boundary and response boundary. Record one positive case and the failure that protects a meaningful invariant. Use the existing fixture shapes and imports in boundaries.test.ts. Keep the fixtures independent between tests by constructing a fresh dependency set each time. Do not use clearAllMocks as if it replaced an incorrect mock implementation.

An optional later integration exercise is to repeat the competing-action case against a disposable PostgreSQL schema and observe exactly one terminal audit. Do not run it against an existing project database or describe the mocked race test as already completing this extension.
""",None),
'06-SOLUTIONS-AND-REVIEW.md':('Solutions and a review checklist',"""
For exercise 1, create an actor with role MODERATOR and a fresh case record with status IN_REVIEW. Configure the transaction repository to return that record and its resolution method to return the resulting terminal record. The service must use the transaction-scoped read. Its write includes expectedCurrentStatus IN_REVIEW and the server actor ID. The audit metadata contains previousStatus IN_REVIEW and nextStatus RESOLVED. Switch to ANALYST for the denied case and assert runInTransaction was not called.

For exercise 2, use createModerationCaseRepository with a DbClient-shaped mock. The returned row must include posting.id, posting.title and posting.company.name because toRecord reads those fields. A count-one result followed by that row establishes successful mapping. A count-zero result must throw InvalidStateTransitionError and skip findUniqueOrThrow. Pass the caught error through errorToResponse to verify 409. Never change a mock to return a row missing a required relation and then weaken toRecord to accommodate the incomplete fixture.

For exercise 3, call updateSavedSearch with only name and expect exactly that parsed property in updateOwned's third argument. The existing name-only regression is reproduced below. For filters-only input, assert the name key is absent. Empty filters are accepted because the schema permits all filter fields to be omitted; the outer refinement still requires at least one provided patch property. An ownerId key is rejected by strictObject before the repository sees it.

Review any solution for accidental weak assertions. Check that positive results are nonempty, error tests reach their intended branch, and snapshots are detached from mutable state. Verify that the owner originates from the actor and that writes and audits share a transaction repository set. A helper that merely returns a constant conflict can satisfy a negative assertion, so preserve a positive path alongside every failure case. Keep database-specific concurrency claims limited to the evidence actually executed.
""",('tests/unit/boundaries.test.ts','  it("preserves omitted','describe("moderation transaction')),
'07-TRACE-LAB.md':('Follow two competing moderation decisions',"""
Start with one case C in OPEN state. Operator A intends RESOLVED and operator B intends DISMISSED. Both have moderation.resolve permission and valid resolution notes. The HTTP routes establish their sessions and parse their requests. Each service call validates again at its direct boundary, then starts a repository transaction. Pause both traces immediately after reading C as OPEN.

Resume A first. Its repository calls updateMany where id equals C and status equals OPEN. One row matches. The repository writes RESOLVED, the actor, notes and resolvedAt, then rereads the included record. The service writes a MODERATION_CASE_RESOLVED audit with previousStatus OPEN and nextStatus RESOLVED. Both changes remain inside A's transaction callback.

Resume B. Its expected status is still OPEN. The database predicate now matches no row, so the repository throws InvalidStateTransitionError. The service does not catch it and does not write an audit. The transaction aborts, and the HTTP error mapper returns 409. B's UI should refresh before trying another action. Simply repeating the request cannot overwrite A's accepted terminal state.

Now change the scenario: A's audit write fails after its conditional update. Trace the exception through the callback to Prisma's transaction runner. The intended production behavior is rollback of both operations. The local rollback-fixture test proves the callback grouping and exception propagation; it is not a live observation of PostgreSQL. Explain where the real database integration check would be added.

Finally, trace an invalid saved-search patch containing ownerId. The strict service schema rejects it before entering a transaction, so neither the repository nor audit receives the attacker-selected identity. Contrast that with a valid name-only patch, whose repository owner is taken from the established session and whose omitted filters remain omitted. Use this exercise to distinguish authority, validation, concurrency and atomicity rather than calling all four simply a transaction.
""",None),
'VERIFICATION.md':('Verification scope and reproduction',"""
The resumed delivery runs the project's complete Vitest suite, TypeScript check and Next production build. Exact terminal command records and their logs are preserved with the delivery evidence. The tests now include service validation, two competing actions sharing an initial snapshot, transaction-scoped repository usage, typed HTTP conflict mapping and production Prisma argument checks. Earlier staged summaries are historical evidence and are not used as proof of the expanded implementation.

Reproduce with npm ci, npm run prisma:generate, npm test, npm run typecheck and npm run build from the project root. Prisma generation creates the client from the checked-in schema; it does not apply a migration or initialize the application database. The unit tests pass fake repositories or fake Prisma clients, so they do not require a live PostgreSQL service. The build verifies route and client compilation without demonstrating an operational deployed database.

The transaction-aware fixture deliberately snapshots its state before invoking the service callback and restores it when the audit fails. That checks error propagation and write grouping. The competing-read fixture makes both calls observe OPEN before either conditional write. That checks the expected-state contract and one-audit behavior. The real repository test then checks that the expected state actually appears in Prisma's where clause. These are complementary proofs at different boundaries, not substitutes for a database concurrency test.

No original database was reset, migrated or seeded by this verification. No external provider was contacted. The project's existing demo session endpoint remains a local teaching mechanism; the course does not claim production authentication. Paged list ordering is deterministic for equal status and timestamp, but separate list/count operations do not guarantee a single concurrent snapshot.

The delivery manifest lists every source, schema, configuration, test, snapshot and learning file that was applied. Generated caches and dependency trees are excluded. Re-run the relevant checks after later edits and update this record rather than assuming the old results still apply to a changed source tree.
""",None),
}
nav='\n\n## Course navigation\n\n'+' / '.join(f'[{name.removesuffix(".md")}]({name})' for name in chapters)+'\n'
for name,(title,body,excerpt) in chapters.items():
 text='# '+title+'\n\n'+body.strip()+'\n'
 if excerpt:
  filename,start,end=excerpt;source=(P/filename).read_text(encoding='utf-8-sig');index=source.index(start);sample=source[index:source.index(end,index) if end else len(source)].rstrip()
  text+='\n## Source excerpt\n\nFrom ['+filename+'](../'+filename+'). Use the linked file for its imports and fixture setup.\n\n```ts\n'+sample+'\n```\n'
 text+=nav
 assert len(text.split())>=250,(name,len(text.split()))
 (P/'astraupskill'/name).write_text(text,encoding='utf-8')
 print(name,len(text.split()))
readme=P/'README.md';text=readme.read_text(encoding='utf-8') if readme.exists() else '# Job-board administration dashboard\n\nNext.js, Prisma and TypeScript teaching application for posting review, moderation cases and private saved searches.\n\nInstall with `npm ci`, generate the client with `npm run prisma:generate`, then run `npm test`, `npm run typecheck` and `npm run build`. Unit tests do not require a database. For the app, configure a dedicated local PostgreSQL database using `.env.example` and the Prisma schema; migrate and seed only your intended development database. Demo role selection is for local learning.\n\n[Architecture](docs/architecture/README.md) / [Course](astraupskill/README.md)\n'
if 'astraupskill/README.md' not in text:
 readme.write_text(text+'\n## Moderation learning course\n\n[Start the source-based course](astraupskill/README.md) for service validation, conditional resolution, transaction boundaries and the runnable regression suite.\n',encoding='utf-8')
