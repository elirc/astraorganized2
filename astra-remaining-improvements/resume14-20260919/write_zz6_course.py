from pathlib import Path
P = Path(__file__).resolve().parent.parent / 'stage/2f29156b71ed'
chapters = {
'README.md': ('Publish a policy as one completed workflow', """
This compliance portal demonstrates tenant-scoped policies, version publication, required acknowledgments and exemption review. Its repositories operate on a mutable in-memory database. A Prisma schema exists in the project, but the service paths discussed here do not execute SQL. The course teaches how to make this particular demo's compound changes coherent without claiming database durability.

The initial publication sequence archived the current version, appended a new version and updated the policy pointer before calculating each recipient's deadline. An invalid effective date could therefore fail after important state had changed. Creating a policy first introduced another failure boundary: the policy could remain even though its initial publication failed. Exception review had a similar ordering problem, changing the decision before verifying its linked acknowledgment.

The completed services parse their runtime inputs directly and use a synchronous transaction over a cloned working database. Nested policy creation and publication share that working copy. A thrown error restores the predecessor graph. Successful results are cloned before being returned, preventing callers from changing retained roles or other nested values through a response reference. Publication also computes its due date and unique recipients before mutating version history.

You should understand TypeScript objects, arrays, exceptions and simple tenant predicates before starting. Read the map and worked change before attempting the exercises. Run the finite test suite and follow the evidence links in VERIFICATION. The tests compare independent snapshots of the entire database, including audit records, instead of inspecting only the record nearest the failure.

The demo session switcher remains a teaching feature. No external policy service, email delivery or durable database is contacted. A successful local transaction protects this process's workflow, while persistence across restart, cross-process coordination and real authentication remain separate implementation concerns.
""", ('src/lib/mock/mock-db.ts','// Nested service calls',None)),
'01-CODEBASE-MAP.md': ('Find the transaction, tenant predicates and read models', """
Routes under src/app/api parse request envelopes and resolve the active demo session. The services apply permissions and coordinate business workflows. Repository functions in src/repositories obtain the active mock database and include tenant IDs in their record queries. That existing tenant scope remains the foundation; this change does not replace it with broad global lookup followed by a late check.

policy-service.ts contains createPolicyWithInitialVersion and publishPolicyVersion. Both join withMockTransaction. The outer create call owns rollback for the new policy, publication, acknowledgment fan-out and both audit events. publishPolicyVersion can also run alone, in which case it owns its own transaction. policy-repository.ts contains the individual archive, create and pointer writes. acknowledgment-repository.ts stores recipient records, while audit-log-repository.ts appends completed workflow history.

exception-service.ts handles requesting and reviewing exemptions. A request links a pending exception to its acknowledgment. Review verifies that the reciprocal reference, requester, policy and version all match before changing either record. acknowledgment-service.ts enforces self ownership and implements a stable acknowledgment retry. An already acknowledged record returns its original timestamp without adding another completion audit event.

Read models also require careful scope. Employees receive their own acknowledgment and exception records. Policy summaries count only that employee's pending exceptions. dashboard-service.ts now omits the tenant audit feed when the viewer lacks audit:read, and its pending count uses the same employee scope. Managers retain tenant-level counts.

Start a trace at the exported service function, follow its permission check, then inspect where the repository obtains getMockDb. Because the active database changes while a transaction callback runs, all nested repository operations must resolve that active graph. Caching a repository's old database reference outside the callback would bypass the working copy and undermine rollback.
""", ('src/services/dashboard-service.ts','export function getDashboard',None)),
'02-CONCEPTS.md': ('A working copy, a preflight and a stable retry', """
Preflight means validating everything that can be known before the first mutation. For publication this includes a real effective date, a finite whole-day acknowledgment window, known unique target roles, a computable deadline and the selected recipients. Runtime schemas belong in the service as well as the route because tests, jobs or later callers may invoke a service directly.

A transaction supplies a second defense: even valid preflight cannot prevent every later failure. ID generation or audit creation can throw after a version and some acknowledgments have been created. withMockTransaction first saves the existing graph and makes a cloned working graph active. A successful callback returns a cloned result. A thrown error restores the saved graph. All service callbacks here are synchronous, so JavaScript does not suspend them midway through a mutation sequence.

Nested calls join the same transaction rather than publishing an independent inner commit. This matters when creating a policy: publication can finish and append its audit, but the outer policy audit can still fail. The whole create operation must disappear in that case. Tests inject precisely that late failure and compare the complete state with the prior snapshot.

Stable retry is another distinct contract. Repeating an acknowledgment that already succeeded should preserve its original acknowledgedAt and audit count. It is not a new acknowledgment event. An exempted record remains ineligible for acknowledgment. A reviewed exception also remains terminal; a second review cannot reverse the original decision.

The implementation is not a database transaction engine. It does not provide isolation between multiple Node processes, survive a crash or undo a real external message. No asynchronous provider operation belongs inside this synchronous working-copy callback. The explicit scope is enough to make the demo consistent while keeping its operational limits visible.
""", ('src/services/acknowledgment-service.ts','  if (acknowledgment.status === "EXEMPTED")','  const updated = updateAcknowledgment')),
'03-WORKED-CHANGE.md': ('Preflight an exception decision before changing history', """
The original review path found a pending exception, selected a status, updated the exception and only afterward looked for its acknowledgment. A missing linked row therefore produced an error after decision history had already changed. An arbitrary direct-call decision string could also fall through to rejection rather than being rejected as malformed input.

The completed method first requires exception:review and parses reviewExceptionSchema. The schema admits only APPROVED or REJECTED with a bounded decision note. Inside the working-copy transaction, the service finds the exception in the active tenant and checks that it is still pending. It then finds the acknowledgment in that same tenant and compares policy ID, version ID, requester user ID and the reciprocal exception ID.

The eligibility policy is explicit: only PENDING or OVERDUE acknowledgments for the current PUBLISHED policy version can request or receive an exemption decision. Already acknowledged or exempted work is not reinterpreted through a late approval. An archived-version exception may remain historical and pending, but it cannot alter current compliance state. A future archival resolution feature would need a separate, audited command.

Once these checks pass, review updates the exception. Approval also marks the linked acknowledgment EXEMPTED; rejection leaves its existing acknowledgment status unchanged. The audit event belongs to the same transaction. If that final audit fails, neither the decision nor exemption survives. The returned exception is detached from stored state.

The tests corrupt each important relationship independently, verify the expected conflict, and compare a complete before snapshot. Another test injects failure after both approval mutations have happened and proves rollback. The existing repeated-review test remains useful: it confirms the pending-only rule was preserved while the transaction boundary was added.
""", ('src/services/exception-service.ts','  const acknowledgment = findAcknowledgmentById(session.tenant.id, record.acknowledgmentId);','  const nextStatus: ExceptionStatus')),
'04-TESTING-AND-DEBUGGING.md': ('Make late failures observable before proving rollback', """
The new workflow suite invokes actual services and repositories against the mock database. Each test resets the seed, and snapshots use structuredClone so an expected object cannot mutate along with the implementation. This matters because a shallow copy of an array would still share the policy, acknowledgment and audit objects being changed.

Input cases exercise malformed dates, impossible calendar dates, nonfinite or fractional windows, zero days, unknown roles, empty role lists and duplicate roles. Both create and publish must reject these values without leaving any database differences. Success coverage checks the current version pointer, incrementing version numbers, prior version archiving, unique user recipients, exact due date and the ordered publication and creation audit events.

Failure injection uses the existing ID-generation dependency rather than a test-only bypass in the service. The injected function checks that the workflow has already created a recipient or changed an exception before it throws. An additional flag proves the test reached that late point. Without that flag, a setup error could cause an early throw and make a rollback assertion pass without exercising rollback at all.

Other cases cover missing and inconsistent links, wrong tenant, wrong requester, nonreviewer roles, repeated terminal decisions and acknowledgment retries. Employee dashboard tests add a peer's pending request and assert the employee count stays unchanged while the manager count increases. The audit feed must also remain empty for a viewer without permission.

Run npm test for the complete finite suite, typecheck for static contracts and the production build for framework integration. Check runner totals and the saved command exit status separately. A failed dependency installation is not a failing business assertion; preserve its log and repair the install before interpreting test results. VERIFICATION links only completed passing commands accepted for delivery.
""", ('src/tests/workflow-atomicity.test.ts','test("nested creation','test("review preflights')),
'05-PRACTICE.md': ('Publication and exemption exercises', """
Exercise one: add two memberships for the same tenant user with roles targeted by a publication. Predict the acknowledgment count before running the command. The intended unit is one recipient user for one version, not one row per matching membership. Verify the returned version, stored current pointer, archived predecessor and the audit assignee count, then inspect the recipient IDs themselves.

Exercise two: inject a failure after at least one acknowledgment has been appended during publication. Record an independent copy of the entire mock database before starting. Prove that the failure was reached late, then compare policies, versions, acknowledgments, exception requests and audits. Repeat through createPolicyWithInitialVersion so a newly created parent policy also has to roll back.

Exercise three: corrupt an exception's linked acknowledgment one field at a time. Try a missing row, another policy ID, another version ID, another requester and a missing reciprocal exception ID. Each attempt must reject before committing a decision. Explain why matching the acknowledgment ID alone would not prove the relationship is safe.

Exercise four: acknowledge a pending record, save its timestamp and audit count, then repeat the call with a different optional note. The second call must return the original result and leave history unchanged. Contrast that behavior with approving an already decided exception: the latter is a conflict, not an idempotent retry that can rewrite a reviewer note.

Exercise five: add a peer employee's pending exception and inspect both policy and dashboard summaries as the original employee. The count should remain self-scoped and the tenant audit feed should remain unavailable. Then switch to the manager and verify the tenant count includes both requests. Write down which permission check and predicate produce each difference before changing the UI label.
""", None),
'06-SOLUTIONS-AND-REVIEW.md': ('Review the complete committed graph', """
The recipient exercise should produce one acknowledgment per distinct user in the selected tenant whose membership role is targeted. The service removes duplicate user IDs before beginning writes. The deadline is computed once from the effective instant using UTC calendar-day addition, so all recipients of a version receive the same dueAt. The audit records that actual recipient count.

For rollback, the important comparison is a fresh read of getMockDb after the exception. The transaction restores the prior graph, while the discarded working graph may still exist in a test's local reference. Reading a discarded reference is not evidence of committed state. The failure flag and the independent initial snapshot together prove that mutations happened inside the draft and were not published.

For exception relationships, all relevant IDs must agree within the tenant. A pending exception linked to a peer's acknowledgment must not be allowed to exempt that peer simply because the reviewer has tenant permission. Acknowledgment state and current published version eligibility are checked separately from link consistency. Both sets of checks precede decision mutation.

The retry exercise preserves acknowledgedAt and the number of completion audit events. A second optional note is not appended to history because the command represents the same completed action. If notes need later editing, that should be a distinct command with its own permission, state policy and audit trail. Exempted records reject acknowledgment attempts, and reviewed exceptions reject further review.

During code review, locate every mutation in create, publish, request, review and acknowledge. Each belongs inside withMockTransaction. Verify that direct-call parsing remains present even though routes validate their payloads too. Check that no helper caches the mutable store before the transaction begins. Finally inspect employee summaries and the dashboard audit permission rather than assuming repository tenant filters also provide self scope.
""", ('src/services/policy-service.ts','  const dueAt = addDays','  const version = createPolicyVersion')),
'07-TRACE-LAB.md': ('Trace a nested publication that fails at its last audit', """
Start with the compliance-manager demo session and take a complete database snapshot. Call createPolicyWithInitialVersion with a unique key, valid content, two target roles, a ten-day acknowledgment window and a valid effective timestamp. The permission and runtime schema checks run before entering the outer transaction. The transaction activates a cloned database graph.

The service creates the parent policy and calls publishPolicyVersion. That call validates its publication input and joins the already active transaction. It does not create a second independent commit. Publication locates the parent in the working graph, computes its version number, due date and unique recipients, archives any predecessor, appends the version, updates the parent pointer and adds recipient acknowledgments.

Allow the publication audit to succeed. Now inject failure when the final policy-created audit asks for an ID. At this moment the working graph contains a valid-looking policy, version, recipients and publication event. The nested publication has returned, but the outer transaction has not completed. The exception travels out of the callback, and withMockTransaction restores the graph that existed before the parent policy was created.

Inspect a fresh snapshot. No parent, new version, recipient or audit from that failed create may remain. The previous policies and exception records must also be byte-for-byte equivalent at the data level. A test that only checks whether the new policy disappeared could overlook leaked acknowledgments or a misleading publication audit.

Remove the injection and repeat the same request. The successful response should contain a policy whose currentVersionId matches its version. Stored acknowledgments should reference that version and share the expected due date. The event order should be publication followed by policy creation. Explain how this ordering describes one completed workflow without claiming an email was sent or a SQL commit occurred.
""", ('src/services/policy-service.ts','  const version = publishPolicyVersion','export function publishPolicyVersion')),
'VERIFICATION.md': ('Recorded checks and the limits of the demo transaction', """
The command evidence below identifies the finite suite, static checks and production build accepted for this delivery. Each record includes the exact arguments, start and finish times, log path and terminal exit code. Test totals come from the actual runner output. Installation attempts or shell commands are never counted as tests, and an unfinished process is not reported as a passing check.

Regression coverage includes invalid publication input, successful version transitions and recipient output, late fan-out failure, failure at the final outer audit, exception link corruption, malformed decisions, role and tenant rejection, review rollback, acknowledgment rollback and stable retry, historical-version eligibility, employee counts and audit visibility. Existing permission, isolation, validation and terminal-review tests remain part of the suite.

The package lock contained incomplete optional dependency records without versions, which prevented npm from resolving its tree. Those malformed metadata entries were removed before npm rebuilt the lock. This repair concerns repeatable dependency installation; it does not change the application's storage model or imply a security audit of every package.

No original database was reset or migrated. The implementation uses the process-local mock database. The transaction helper clones and restores JavaScript graphs, and nested service calls share the same synchronous boundary. It provides no persistence across restart or coordination between worker processes. The application still uses an explicit demo session selector rather than real identity-provider authentication.

Exception eligibility is intentionally conservative: current published version, uncompleted acknowledgment, matching tenant and reciprocal links. Historical pending exceptions are not silently approved after a newer policy is published. A later archival-resolution feature needs its own command and tests. Keep these rules, the original snapshots and the recorded evidence together when extending the portal, so a future reader can distinguish verified behavior from planned production features.
""", None),
}
nav='\n## Course navigation\n\n'+' / '.join(f'[{name.removesuffix(".md")}]({name})' for name in chapters)+'\n'
(P/'astraupskill').mkdir(exist_ok=True)
for name,(title,body,excerpt) in chapters.items():
 text='# '+title+'\n\n'+body.strip()+'\n'
 if excerpt:
  file,start,end=excerpt;source=(P/file).read_text(encoding='utf-8');index=source.index(start);sample=source[index:source.index(end,index) if end else len(source)]
  text+=f'\n## Source excerpt\n\nFrom [{file}](../{file}).\n\n```ts\n{sample.rstrip()}\n```\n'
 text+=nav;assert len(text.split())>=250,(name,len(text.split()));(P/'astraupskill'/name).write_text(text,encoding='utf-8');print(name,len(text.split()))
f=P/'README.md';s=f.read_text(encoding='utf-8') if f.exists() else '# Compliance policy portal\n'
if 'astraupskill/README.md' not in s:s+='\n## Policy workflow course\n\n[Source-based course](astraupskill/README.md): runtime preflight, atomic process-local publication and exception review, stable acknowledgment retries and employee read scope. This is in-memory demo storage; no SQL durability or real authentication is implied. Exceptions require an uncompleted acknowledgment for the current published version.\n'
f.write_text(s,encoding='utf-8')
