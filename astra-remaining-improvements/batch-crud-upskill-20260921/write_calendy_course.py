from pathlib import Path
import re
D=Path(__file__).resolve().parent.parent/'stage/ef1449fa0c77/astraupskill'
chapters={
'README.md':'''# NetCalendy: validate the relationship, not just the identifier

A booking command contains an event-type ID and a host-user ID. Each can be
well formed while their combination is wrong. This lab follows the actual
[booking handler](../src/NetCalendy.Application/Bookings/Commands/CreateBooking/CreateBookingHandler.cs)
and [availability handler](../src/NetCalendy.Application/Schedules/Queries/GetAvailableSlots/GetAvailableSlotsHandler.cs)
to repair that boundary. Before the change, finding the event type was enough
to continue using a caller-supplied host. The corrected handlers require the
event type to belong to both the resolved tenant and requested host.

This is especially useful CRUD practice because the endpoints intentionally
allow anonymous invitees. Requiring a signed-in user would change the booking
product. Instead, the operation must establish which public resource the
request describes. Missing resources and mismatched resource relationships
produce the same EventType.NotFound result. An inactive matching event type
produces EventType.Inactive, and availability now agrees with booking on that
state rule. Legal booking and missing-schedule behavior remain visible in tests.

Study the chapters in order, keeping the source open. First draw the route,
handler, aggregate and repository path. Then predict which downstream calls
are allowed for each input tuple. Compare the original snapshots with the
guard, run the focused harness, and attempt the practice before opening its
separate answers. The trace table provides a review aid rather than a claim
that every component of the web application was exercised.

The [harness](../tests/NetCalendy.ScopeHarness/Program.cs) compiles production
source into a dependency-free .NET 10 executable. The application still targets
.NET 9. Repository and mediator contracts in the harness are explicit test
boundaries; ASP.NET middleware, MediatR pipelines, EF Core and PostgreSQL are
not executed. Read VERIFICATION for the captured result. A senior conclusion
should identify both the relationship now enforced and the scheduling,
concurrency and deployment questions this small change does not answer.
''',
'01-CODEBASE-MAP.md':'''# Map the two public paths

[BookingsController](../src/NetCalendy.Api/Controllers/BookingsController.cs)
accepts CreateBookingCommand on POST api/bookings with AllowAnonymous. It sends
the command through the mediator and converts the handler result into an HTTP
response. The command contains EventTypeId, HostUserId, StartTime and invitee
details. Tenant identity comes from ICurrentTenantService rather than a tenant
field copied from the command. These are distinct sources of input, so write
them in separate columns when tracing a request.

[CreateBookingHandler](../src/NetCalendy.Application/Bookings/Commands/CreateBooking/CreateBookingHandler.cs)
loads the event type, checks scope and active state, calculates the end from
its duration, queries conflicting bookings, validates the invitee, constructs
Booking, adds it and saves the unit of work. EventType carries TenantId and
OwnerId; Booking carries TenantId, HostId and EventTypeId. The new comparison
connects those identities before the handler constructs a new aggregate.

[SchedulesController](../src/NetCalendy.Api/Controllers/SchedulesController.cs)
exposes GET api/schedules/available-slots anonymously. Its existing date-range
checks reject reversed ranges and ranges over sixty days. The query handler
loads the event type before the default host schedule and existing bookings.
It now applies the same scope and active-state policy before those reads.
A matching event with no schedule still returns an empty successful list.

The infrastructure repository inherits GetByIdAsync from RepositoryBase,
which uses EF FindAsync. The handler should not assume that a generic lookup
proves the relationship between independently supplied IDs. Repository query
filters may provide additional protection, but the source-level guard states
the operation's own contract and remains observable in a focused test.

For navigation practice, follow one valid command to bookings.Add and then
repeat with the wrong host. Circle the earliest branch that differs. For the
query path, circle GetDefaultByUserAsync: a wrong host must never reach it.
This map makes read avoidance as reviewable as write avoidance and clarifies
why both public entry points belong in this bounded change.
''',
'02-CONCEPTS.md':'''# Referential consistency and public resource scope

A foreign key can prove that a referenced row exists. It does not necessarily
prove that two referenced rows belong together. A booking may contain a valid
event ID and a valid host ID while the event belongs to someone else. Treat
the request as a relationship tuple: resolved tenant, requested host, selected
event. The event's stored TenantId and OwnerId are the evidence used to validate
that tuple. Caller-provided IDs are assertions to check, not authority.

This is different from authenticating the invitee. The application permits
public booking, so an anonymous visitor can legitimately request a host's
published event type. The handler must preserve that product behavior while
refusing to combine another host with the selected event. Returning the same
not-found result for missing and mismatched resources avoids introducing a
separate response that confirms a resource outside the requested scope.

State is another dimension. An event type can belong to the correct host and
tenant but be inactive. Booking already rejected that case. Availability must
also reject it rather than advertise slots that cannot be booked through the
corresponding create path. Relationship checks come first, so inactive state
is not disclosed for a mismatched resource. Tests should name these as separate
conditions rather than merging every invalid input into a generic failure.

The comparisons use the domain's TenantId and UserId value objects, whose
record equality compares their values. Do not compare display names or slugs
when the aggregate already carries stable identities. Do not trust the client
to disable an invalid combination; direct callers can submit the same command.

Finally, scope validation is not concurrency control. A conflict query followed
by a write can still race with another booking. The new checks do not prove
availability membership, timezone correctness, atomic reservation or delivery
of domain events. Read the [domain booking rules](../src/NetCalendy.Domain/Bookings/Booking.cs)
and separate those concerns when designing the next experiment. One precise
invariant is easier to verify than an unsupported promise of complete safety.
''',
'03-WORKED-CHANGE.md':'''# Worked change: stop a mismatched tuple early

Consider tenant T, host H and event E. E exists but OwnerId is J. Before the
change, the booking handler accepted E, used its duration, searched H's bookings
and constructed a booking connecting E to H. No check established that H owned
E. The availability handler similarly combined E's duration with H's schedule.
Compare the originals in snapshots with the current handlers before reading
the replacement condition below.

```csharp
// Before: existence was the only resource check.
if (eventType is null)
    return Result.Failure<CreateBookingResponse>(Error.NotFound("EventType", cmd.EventTypeId));

// After: the loaded aggregate must match the complete requested scope.
if (eventType is null || eventType.TenantId != tenantId || eventType.OwnerId != hostId)
    return Result.Failure<CreateBookingResponse>(Error.NotFound("EventType", cmd.EventTypeId));
```

The placement is before duration calculation, conflict lookup, invitee creation
and persistence. A repository spy can therefore assert more than a returned
error: no conflict query, Add or SaveChanges call is allowed for the wrong host.
For the query handler, the corresponding assertion is no schedule or booking
read. The same failure code is used when the event is absent or outside scope.

The availability change additionally checks IsActive after scope succeeds.
It returns EventType.Inactive using the same validation message already present
in booking. It does not modify how schedules generate slots, how bookings are
filtered by time or how the controller constrains date ranges. A valid event
without a default schedule continues to return an empty list.

In the [runtime harness](../tests/NetCalendy.ScopeHarness/Program.cs), each invalid
case loads an actual EventType aggregate or null through a repository double.
The real handler executes the guard. Legal create and existing conflict cases
then confirm that the repair did not turn every request into a failure. This
is the central review pattern: demonstrate the prohibited interaction and a
neighboring allowed interaction through the production operation itself.
''',
'04-TESTING-AND-DEBUGGING.md':'''# Observe the first forbidden interaction

Run `dotnet run --project tests/NetCalendy.ScopeHarness --configuration Release`
from this project root with .NET 10 installed. The harness project links the
actual domain source and both application handlers; it does not copy their
conditions into test functions. Its small MediatR interfaces support compilation
only. DispatchProxy implementations provide repository contracts, count calls
and fail if an unexpected method is invoked. The test result is handler evidence,
not a test of dependency injection or mediator dispatch.

For each public path, the fixtures cover a missing event, another host's event,
another tenant's event and an inactive matching event. Assert the exact error
code and zero downstream calls. If the error is correct but a schedule read
already occurred, the guard is too late. If no writes occur only because a
repository double throws, the test has not demonstrated deliberate rejection.
Both the result and the call trace are necessary to distinguish those failures.

The positive booking fixture records the actual Booking supplied to Add and
counts SaveChanges. Verify tenant, host, event ID and derived duration. Another
fixture returns a conflicting booking and verifies the existing conflict result
without Add or SaveChanges. The availability success fixture returns no default
schedule, confirming that an empty list remains a legitimate successful read.

When debugging, first compare the command's host with EventType.OwnerId, then
the current tenant with EventType.TenantId. Check value-object values rather
than assuming separately constructed objects have different identity. Next
inspect active state and the repository call log. Finally inspect result mapping
only if handler behavior is correct and the observed HTTP response differs.

Do not infer PostgreSQL behavior from these doubles. Follow-up integration tests
should exercise tenant resolution, EF tracking and query filters, controller
mapping, MediatR validation and two simultaneous bookings. The application still
targets .NET 9; this isolated .NET 10 compilation verifies a selected source
slice and does not certify the application's original build configuration.
''',
'05-PRACTICE.md':'''# Practice before reading the answers

Use tenant T, requested host H and event E for every prediction. Write the
event's stored TenantId, OwnerId and IsActive beside the command. Then record
the expected result, conflict-query count, schedule-query count, Add count and
SaveChanges count. This worksheet forces you to distinguish input validity from
allowed side effects. Answer from the handlers rather than an imagined framework
policy, and label any answer that requires an integration test.

1. E belongs to T and H and is active. The conflict query returns no rows.
   Predict the persisted Booking identities and a thirty-minute event's end.
2. Change only E.OwnerId to J. Predict booking and availability behavior.
   Explain why checking that H exists would not repair the relationship.
3. Restore OwnerId to H but change E.TenantId to U. Predict the error and
   identify the first downstream call that must not occur in each handler.
4. Keep both identities correct and deactivate E. Predict the result on both
   paths. Then combine inactivity with a wrong host and predict which error wins.
5. Keep the event valid but return no schedule. Explain why this is different
   from a missing event and whether availability should be an error.

For an implementation exercise, extend the harness with a repository that
records the exact cancellation token passed to GetByIdAsync. Determine whether
your new assertion protects application behavior or merely records a current
implementation detail. Next, write a controller integration test that sends
a mismatched public request and verifies response mapping without logging invitee
personal data. State what test infrastructure that exercise requires.

For a senior design exercise, propose a database-level protection against two
simultaneous bookings of the same host and interval. Name the invariant, a
possible constraint or locking strategy, transaction boundaries and retry error.
Explain why the new host/event guard neither solves nor prevents that race.
Keep your concurrency proposal separate from the accepted source change.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Answers and review rubric

Case one succeeds when the remaining invitee and domain validations also pass.
The saved booking carries tenant T, host H and E's actual ID; its end is the
requested start plus E.Duration.Minutes. The harness verifies one Add and one
SaveChanges call. An answer that merely says “201” skips the handler's contract:
the HTTP status belongs to controller mapping and was not executed by this test.

Case two returns EventType.NotFound before conflict or schedule lookup. H's
independent existence would not prove ownership of E. Case three returns the
same result for a tenant mismatch. In both cases the event lookup is allowed,
but operations on the requested host's calendar must not follow. Case four
returns EventType.Inactive only for a matching tuple. A wrong-host inactive event
returns not found because scope is checked before state. Case five succeeds with
an empty slot list after one default-schedule lookup; an absent schedule is an
existing supported empty result, unlike an absent selected event.

The cancellation-token exercise is useful if cancellation propagation is part
of the operation's documented contract. Avoid asserting arbitrary local variable
names or object construction order. A controller integration test adds HTTP
binding, tenant resolution and error translation; it cannot be replaced by a
handler double returning a fabricated status code. Its evidence should remain
separate from the focused source-slice compilation.

Score a review on four dimensions: correct resource relationship, early rejection,
preserved legal behavior and accurate evidence boundaries. Require the author to
show both handlers because availability and booking form a public workflow.
Reject client-only checks and checks performed after Add. Ask which error is
returned for a resource outside scope and whether it reveals more information
than the existing not-found path.

For the concurrency design, there is no single answer proven by this patch.
A credible proposal names a real database mechanism and tests two interleaving
transactions. A pre-write conflict query alone is not an atomic guarantee.
The accepted review should acknowledge that remaining concern without expanding
a small, testable relationship repair into an unverified scheduling redesign.
''',
'07-TRACE-LAB.md':'''# Trace the tuple across both operations

Before executing the harness, fill the empty columns of your own copy of this
table. “Downstream” excludes the initial event lookup and means conflict reads,
schedule reads, booking persistence and unit-of-work save. Counting the first
lookup as a failure would obscure the fact that persisted event attributes are
needed to decide whether the tuple is valid. The guard needs evidence; it does
not need a booking write to obtain that evidence.

| Persisted event | Booking result | Availability result | Allowed downstream work |
|---|---|---|---|
| Missing | EventType.NotFound | EventType.NotFound | None |
| Tenant T, owner J, active | EventType.NotFound | EventType.NotFound | None |
| Tenant U, owner H, active | EventType.NotFound | EventType.NotFound | None |
| Tenant T, owner H, inactive | EventType.Inactive | EventType.Inactive | None |
| Tenant T, owner H, active | Continue existing rules | Continue existing rules | Operation-specific |

For a successful booking, continue the last row: compute end time, query conflicts,
construct Invitee, create Booking, Add, SaveChanges and return the response. Mark
which values come from the command and which come from the event aggregate.
The host is caller supplied but checked against stored ownership. Duration comes
from the selected event; the client cannot independently choose an end time in
this command. Tenant comes from the resolved request context.

For availability, continue with GetDefaultByUserAsync. A null schedule returns
an empty list without reading bookings. A real schedule would lead into timezone,
date and overlap logic, which the new guard does not redesign. The harness's
positive query case intentionally stops at the null-schedule branch; do not
extend its success claim to daylight-saving conversion or slot generation.

Finally, overlay the original source on the wrong-host row. The old code could
continue with E's duration and H's calendar. Explain that mismatch to a peer
without using the word “validation.” If your explanation names both resources,
their owner and the prohibited interaction, you have identified the underlying
CRUD invariant rather than memorized a conditional expression.
''',
'VERIFICATION.md':'''# Verification scope and reproduction

The focused command is `dotnet run --project tests/NetCalendy.ScopeHarness
--configuration Release` from this project root. The harness targets .NET 10,
the SDK installed during this task. The application and its existing test projects
continue targeting .NET 9. No target-framework upgrade is part of the production
change. Accepted execution evidence is attached below after the command completes;
this explanation alone is not a claim that an unfinished command passed.

Read [the harness project](../tests/NetCalendy.ScopeHarness/NetCalendy.ScopeHarness.csproj)
to see the linked production files. It compiles the domain, the two handlers,
their command/query records and the current-tenant/unit-of-work interfaces.
The [mediator contracts](../tests/NetCalendy.ScopeHarness/MediatorContracts.cs)
are minimal test-only signatures. They do not implement MediatR behavior or
its validation pipeline. The [program](../tests/NetCalendy.ScopeHarness/Program.cs)
uses explicit repository and unit-of-work doubles and exits nonzero on an
assertion failure. Its printed totals count runtime cases, not restore or build
steps. Compiler success is useful additional evidence for this selected slice.

Eight negative cases pair missing, foreign-host, foreign-tenant and inactive
events with booking and availability. Three positive or neighboring cases cover
correctly scoped persistence, existing booking conflict handling and empty
availability when a valid event has no schedule. Inspect both the returned error
and downstream call counters. This checks that rejection happens deliberately
before calendar reads or writes instead of relying on a later dependency error.

The check does not execute the original xUnit suites, ASP.NET controllers,
authentication, tenant middleware, FluentValidation, EF Core, PostgreSQL or a
browser. It does not prove booking availability membership or simultaneous-write
safety. The original handler snapshots permit before/after review, and the
captured command record identifies the environment used. A future integration
run should restore the original project's dependencies and use its intended
runtime and disposable database; report those results independently rather
than folding them into these focused handler cases.
'''
}
D.mkdir(exist_ok=True)
for name,text in chapters.items():
    (D/name).write_text(text,encoding='utf-8')
    print(name,len(re.findall(r"\b[\w'-]+\b",text)))
