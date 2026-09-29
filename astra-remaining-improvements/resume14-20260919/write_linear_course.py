from pathlib import Path
P = Path(__file__).resolve().parent.parent / 'stage/b2f277b889f9'
chapters = {
'README.md': ('Issue commands, PostgreSQL conflicts and notification boundaries', '''
NetLinear is a .NET 8 issue tracker with a React client. This course follows issue creation and movement through its domain model, command handlers, EF Core persistence and HTTP error boundary. The finished change prevents rejected inputs from consuming a tracked team counter, rejects foreign project and cycle references, preserves PostgreSQL optimistic concurrency, and makes stale writes return a conflict response. It also fixes duplicate EF navigation discovery that previously prevented the production model from initializing.

Begin with basic C# records, async methods, LINQ and relational transactions. An aggregate here is the Issue together with its activity collection. A command handler coordinates reference checks, aggregate mutation, persistence and notification enqueue. A concurrency token identifies the version last read; PostgreSQL supplies the xmin token used by this project. A domain event describes a successful in-memory change but does not itself guarantee durable message delivery.

Restore NetLinear.sln using a .NET 8 SDK. Run dotnet test with Docker available for the default Testcontainers fixture, or use `python scripts/test-local.py --postgres-bin "C:/Program Files/PostgreSQL/18/bin" --dotnet dotnet` with locally installed PostgreSQL binaries. The helper creates its own temporary cluster and the fixture creates a uniquely named test database. It does not reuse the application's configured database. Read VERIFICATION before interpreting the results or changing environment variables.

Read the codebase map, concepts and worked change first. Then reproduce the handler tests, attempt the practice tasks, and compare your reasoning with the solutions. The trace lab separates a stale screen from a concurrent database update. Keep those two failure modes distinct when reviewing a UI retry policy. The source links and excerpts refer to this delivered project, so you can follow each claim without another checkout.
''', None),
'01-CODEBASE-MAP.md': ('Follow a command through the actual layers', '''
The API in src/NetLinear.Api/Program.cs receives requests and routes them through MediatR. FluentValidation provides transport-level checks. CreateIssueCommandHandler adds an independent service boundary by calling the Issue validation helpers directly. This matters because the test suite and future internal callers may invoke the handler without passing through the HTTP pipeline.

The handler looks up the team and default workflow state. It then validates that any referenced project and cycle belong to that same team and that an assignee exists. Only after those checks does Team.ReserveIssueKey increment the next number. The new Issue is assigned its detail values, attached to the EF context and saved. A save conflict is translated narrowly to ConcurrencyConflictException. Notification events are enqueued after that save, and the aggregate's event list is cleared only after enqueue succeeds.

The infrastructure mapping uses PostgreSQL xmin for auditable entities and retains the unique TeamId/Key index. Issue has private collection fields and public read-only collection views. The mapping explicitly uses the fields; ignoring the public views prevents EF conventions from discovering the same navigation twice. The activity table therefore remains part of the aggregate save rather than becoming an unrelated test-only representation.

ChangeIssueStateCommandHandler checks the caller's Version before looking up the destination workflow state. Its destination query binds both state ID and issue team. The domain method independently requires a valid target even when the request only reorders an issue inside its current state. The API mapper converts known validation, missing-resource, authorization and concurrency errors into appropriate status codes. Unexpected errors retain HTTP 500 with a generic public description.
''', ('src/NetLinear.Application/Issues/ChangeIssueStateCommand.cs', '    public async', '        foreach (var domainEvent')),
'02-CONCEPTS.md': ('Preflight, atomic persistence and version ownership', '''
A rejected command should leave the observable aggregate unchanged. Before this change, construction could reject a title after the handler had already incremented the team's tracked next number. A later save through that context could persist the gap. Calling the same domain validation before ReserveIssueKey closes that path without relying on an HTTP validator to have executed. The constructor and mutators still validate because other callers can instantiate the domain directly.

Foreign references are another preflight boundary. A project ID that exists in another team is not an acceptable project for the new issue. The query must combine identity with TeamId. A missing assignee also rejects before number reservation. Domain value checks cover title length, description length, defined priority values and the estimate range. Team guards the integer counter's upper boundary before incrementing, so overflow cannot silently wrap it.

A request Version and a database concurrency token address different times. Version tells the handler whether the client is using an outdated representation. EF also keeps the original xmin read by its context; another connection may update the row after that read. PostgreSQL then causes the conditional save to affect no matching row, and EF throws DbUpdateConcurrencyException. Catching that exception at the handler preserves conflict semantics without treating unrelated persistence errors as ordinary contention.

After a failed save, discard the request's context. Its tracked objects may still contain attempted changes even though the database transaction failed. This implementation does not promise to rewind every tracked field. Likewise, enqueue after commit is not an outbox: a crash can lose a notification, and partial enqueue followed by retry can duplicate one. Those operational limits must remain visible in a design review.
''', ('src/NetLinear.Domain/Organizations/Team.cs', '    public string ReserveIssueKey', None)),
'03-WORKED-CHANGE.md': ('Validate before allocating the issue number', '''
Start with CreateIssueCommandHandler and the original source snapshot. The important ordering is validation, reference lookup, allocation, mutation, persistence and notification. Moving only the title check into an API endpoint would leave direct handler calls vulnerable. The implemented handler calls Issue.ValidateTitle and Issue.ValidateDetails first, using exactly the same rules as the aggregate. It checks related rows before Team.ReserveIssueKey is evaluated as a constructor argument.

The domain helpers reject blank or overlong trimmed titles, descriptions longer than twenty thousand characters, undefined priority enum values and estimates outside zero through one hundred. Rename performs its check before assignment. UpdateDetails performs all checks before assigning any of its properties, so a late invalid estimate does not leave an already changed description. Positive tests still create an issue, normalize its title and verify persisted assignment and activity.

The save boundary catches DbUpdateConcurrencyException and wraps it in the application's typed conflict exception. ChangeIssueStateCommandHandler uses that same type for a stale supplied Version. ApiExceptionMapper hides provider diagnostics in a generic conflict detail and supplies a generic detail for unexpected failures. Domain and validation errors retain useful user-facing explanations.

The first PostgreSQL regression run exposed a separate blocker in the existing EF mapping. Both public Issue collection views and explicit private field navigations were discovered. Ignoring only the duplicate public views keeps the original field navigation names and allows the production model to initialize. A subsequent real save exposed EF interpreting newly discovered child entities as existing rows because their GUIDs were already populated. The production model now declares domain-generated entity IDs with ValueGeneratedNever, so appended activity is inserted correctly. No portable SQLite substitute or test-only mapping switch is used. The tests therefore exercise the same xmin and JSON mapping as the API.
''', ('src/NetLinear.Application/Issues/CreateIssueCommand.cs', '        Issue.ValidateTitle', '        foreach (var domainEvent')),
'04-TESTING-AND-DEBUGGING.md': ('Use a real provider and inspect the failure boundary', '''
IssueDomainTests exercises domain state transitions and invalid values without a database. ApiExceptionTests checks the distinction between a known conflict and an unexpected exception, as well as counter overflow and rejected rename behavior. IssueHandlerRegressionTests uses the production AppDbContext with PostgreSQL. Its fixture creates a unique database on an explicitly selected loopback test server, or starts its own Testcontainers PostgreSQL instance when no server override is supplied.

The handler success test uses real team, project, cycle and assignee rows and rereads the saved issue through another context. Negative input tests check both the tracked team counter and its persisted value. Foreign references must fail before any issue or notification appears. These assertions make a test stronger than simply expecting an exception from a path that might also reject every valid command.

The xmin test keeps two independent contexts alive. The losing context reads first; the winning context saves a state change; then the loser attempts a save using its stale tracked token. The test verifies the winner's stored state and sort key, a single accepted state-change event and no losing notification. This is a real provider concurrency result, not a mock that returns zero on demand.

The health smoke test starts the ASP.NET application through WebApplicationFactory and calls /healthz with the fixture connection. It validates application startup and database health, but it is not a complete authenticated browser workflow. The queue-failure test intentionally throws after persistence and verifies that the issue remains committed and its undelivered events remain on the tracked aggregate. That result documents a delivery gap; it does not establish an automatic retry mechanism.
''', ('tests/NetLinear.Tests/IssueHandlerRegressionTests.cs', '    public async Task Actual_xmin', '    [Fact]\n    public async Task Queue_failure')),
'05-PRACTICE.md': ('Exercises in rejection order and recovery', '''
Exercise one: extend the invalid-values handler test with a title containing only tab and newline characters. Before running it, identify the exact method that should reject the request and the observable state that must remain unchanged. Check both the tracked counter and a new context's persisted counter. Include a valid trimmed title control so an implementation that rejects every title cannot pass your proposed test.

Exercise two: add a valid same-state reorder case. Create an issue, then move it to its current state with a different SortKey and current Version. Assert that the new order persists without a state-change notification. Now pass a target belonging to another team and require rejection before reordering. Explain why the domain method validates the target before its same-state early return, even though today's handler already scopes the destination query.

Exercise three: design a test for two handlers allocating numbers for one team from separate contexts. Make both contexts observe the same team version before either saves. Predict whether the team xmin check or the unique TeamId/Key index wins in your concrete schedule. Assert that the losing handler never enqueues and that the database retains unique issue keys. Do not call every possible provider exception a conflict merely to make the assertion convenient.

Exercise four is a design task rather than an implemented feature: propose a transactional outbox. Identify the table, message identity, worker claim mechanism, retry policy and consumer idempotency rule. Explain which current crash window it closes and which duplicate-delivery window still exists. Include a migration and backward compatibility plan before treating that proposal as deployable code.

Keep each exercise in the appropriate existing test class. Use fresh IDs and fixture-owned databases. Never point a destructive cleanup step at the application's database connection. Record the executed test result separately from the expected answer and preserve a failing run when it reveals a real missing invariant.
''', None),
'06-SOLUTIONS-AND-REVIEW.md': ('Reason through the expected solutions', '''
For exercise one, string.IsNullOrWhiteSpace in Issue.ValidateTitle rejects the whitespace-only title. CreateIssueCommandHandler calls it before loading the team or reserving a key. The test should show no newly tracked Issue or ActivityEvent, no queue item, and the unchanged persisted team counter. A valid title with surrounding spaces should still become its trimmed representation. Testing only the exception type would miss a premature mutation.

For exercise two, MoveToState first checks membership in the valid target set. With the current state present, it changes SortKey and returns without adding a state-change activity or domain event. SaveChanges still persists the reorder and advances xmin. A foreign target fails the handler's scoped query; a separate direct domain test should also reject an invalid target set. The two checks defend different entry points and should not be merged into an assumption about HTTP callers.

For exercise three, inspect the SQL and actual exception rather than predicting solely from C# ordering. Both the team row's xmin and the issue key's unique index protect invariants, but the statement sequence determines the observed failure. The current regression proves an issue update conflict, not every allocation interleaving. If you extend allocation conflict translation, match the exact provider constraint or token failure and retain unexpected storage errors as server failures.

For exercise four, persist an outbox record in the same transaction as the issue and its activity. Give the message a stable ID and make worker retries safe. A worker crash after sending but before marking delivery can still cause duplicates; the consumer must recognize the stable ID or make its effect idempotent. The current code has no durable outbox and no claimed exactly-once guarantee.

A useful review also checks the production model. The duplicate collection fix must not remove the backing-field relationship itself. Preserve the xmin column mapping, team/key uniqueness and activity foreign key while changing discovery behavior. Finally, ensure public errors do not expose a database connection string or provider diagnostic supplied by an unexpected exception.
''', None),
'07-TRACE-LAB.md': ('Trace two contexts and an interrupted notification', '''
Begin with issue I in Todo, SortKey ten and database version V. Context A reads I and retains V as its original concurrency token. Context B independently reads the same row. The browser request to B also supplies V, so the request-level comparison passes. B looks up a Done state in I's team, mutates the aggregate, adds a state-change activity and saves. PostgreSQL accepts its original token and advances the stored xmin.

Now resume A with a request that still supplies V. A's tracked entity still has V, so its manual request comparison can pass even though another connection has already saved. A attempts a same-state reorder using its stale tracked token. EF's conditional update cannot match the current row version and throws DbUpdateConcurrencyException. The handler translates that error into ConcurrencyConflictException. No notification is enqueued, the HTTP layer returns 409, and a fresh read retains B's winning state and SortKey.

Compare a second schedule: A starts after B commits but the browser still sends V. A reads the new token and rejects at the explicit Version comparison, before a domain mutation or database save. Both schedules produce a conflict response, but only the first relies on the provider's concurrency check. Explain why testing only the second schedule would leave the actual xmin mapping unverified.

Finally, trace a successful creation with an assignee. The issue and activity commit; then the queue throws. The database row remains present. The aggregate retains its domain events because ClearDomainEvents follows the enqueue loop. A process crash at this point loses that in-memory recovery information. Retention on a live object is useful evidence about ordering, not durable recovery. The course's queue test demonstrates precisely this limit so a future outbox change has a concrete scenario to improve.
''', ('src/NetLinear.Application/Issues/CreateIssueCommand.cs', '        foreach (var domainEvent', '        return new IssueDto')),
'VERIFICATION.md': ('Reproduce and interpret the recorded checks', '''
Verification uses the complete .NET test project with the production PostgreSQL provider. The solution restore and build use a local .NET 8 SDK because this machine's system SDK alone does not provide the required runtime. Exact commands, exit codes and test counters are retained in the delivery evidence below. Failed attempts are preserved in the campaign checks directory and are not counted as passing validation.

The default fixture starts PostgreSQL through Testcontainers. An alternative Python helper uses installed PostgreSQL binaries, creates a uniquely named temporary data directory, starts a loopback-only server, supplies NETLINEAR_TEST_SERVER to the test process and stops its owned server afterwards. The fixture creates and drops only its generated netlinear_test database. The helper skips synchronization during initialization because its cluster is disposable test data. It does not alter the application's connection settings or migrate an existing user database.

The suite covers domain rejection, handler reference preflight, successful issue creation, a real two-context xmin conflict, HTTP exception classification and the application's health endpoint. The API error mapper is tested directly for typed and provider conflicts and for suppression of unexpected exception details. The health test supplies real database connectivity through WebApplicationFactory; it does not claim end-to-end browser authentication or deployment verification.

Notification enqueue remains in memory and occurs after commit. The failure regression confirms that a committed issue is not rolled back when enqueue fails and that event clearing happens only after success. Crash recovery, durable dispatch and exactly-once processing are outside this implementation. The existing development login and seeded demonstration identities are also not replaced by this work.

Use the before snapshots to review changed source, then rerun the commands after any subsequent edits. A historical passing TRX describes the source tested at that time; it cannot validate later unrecorded changes. Generated binaries, dependency directories and temporary databases are excluded from delivery.
''', None),
}
nav = '\n## Course navigation\n\n' + ' / '.join(f'[{n.removesuffix(".md")}]({n})' for n in chapters) + '\n'
for name, (title, body, excerpt) in chapters.items():
    text = '# ' + title + '\n\n' + body.strip() + '\n'
    if excerpt:
        filename, start, end = excerpt
        source = (P / filename).read_text(encoding='utf-8-sig'); index = source.index(start)
        sample = source[index:source.index(end, index) if end else len(source)].rstrip()
        text += f'\n## Source excerpt\n\nFrom [{filename}](../{filename}).\n\n```csharp\n{sample}\n```\n'
    text += nav
    assert len(text.split()) >= 250, (name, len(text.split()))
    (P / 'astraupskill' / name).write_text(text, encoding='utf-8')
    print(name, len(text.split()))
(P / 'astraupskill/08-REFERENCE.md').write_text('''# Source reference

Use the [course index](README.md) for the ordered reading path and [verification](VERIFICATION.md) for executed evidence.

- [Issue aggregate](../src/NetLinear.Domain/Issues/Issue.cs): preflight rules, state changes, activity and domain events.
- [Team](../src/NetLinear.Domain/Organizations/Team.cs): guarded issue key allocation.
- [Create handler](../src/NetLinear.Application/Issues/CreateIssueCommand.cs): references, allocation, persistence and enqueue.
- [State handler](../src/NetLinear.Application/Issues/ChangeIssueStateCommand.cs): client version and provider conflict handling.
- [Production EF context](../src/NetLinear.Infrastructure/Persistence/AppDbContext.cs): backing fields, unique indexes and xmin.
- [API error mapper](../src/NetLinear.Api/Services/ApiExceptionMapper.cs): public HTTP status and detail policy.
- [PostgreSQL fixture](../tests/NetLinear.Tests/PostgresFixture.cs): isolated database ownership.
- [Handler regressions](../tests/NetLinear.Tests/IssueHandlerRegressionTests.cs): real provider checks and queue failure evidence.
''', encoding='utf-8')
p = P / 'README.md'; text = p.read_text(encoding='utf-8')
text = text.replace('The test project includes domain unit tests and a Testcontainers-backed API health smoke test.', 'The test project includes domain and API error tests, real PostgreSQL handler regressions, and an API health smoke test. Docker is used by default. With local PostgreSQL binaries, run `python scripts/test-local.py --postgres-bin "C:/Program Files/PostgreSQL/18/bin" --dotnet dotnet` after restoring the solution; the helper owns a disposable loopback cluster.')
if 'astraupskill/README.md' not in text: text += '\n## Issue command learning course\n\n[Start the source-based course](astraupskill/README.md) for command preflight, xmin conflicts, EF mappings and notification limits.\n'
p.write_text(text, encoding='utf-8')
