from pathlib import Path
P = Path(__file__).resolve().parent.parent / 'stage/32d4e2fef457'
chapters = {
'README.md': ('Calendar boundaries and one-winner cancellation', """
This appointment application schedules clients with staff members using local working hours, time-off blocks and PostgreSQL-backed appointment records. The improvement focuses on two boundaries: deciding whether an interval belongs inside a local working day, and canceling an appointment without leaking another caller's state or overwriting an earlier cancellation.

The original working-hours check compared the start weekday and local clock minutes but did not compare the end date. A meeting beginning late at night and ending after midnight could appear to fit a daytime rule because the end minute wrapped back to a small number. The completed calculation checks both local dates, permits an exact next-midnight endpoint only for a rule ending at minute 1440, and rejects other cross-day windows. Invalid ranges, timezones and nonpositive slot steps fail before iteration.

Cancellation originally loaded an unrestricted ID, inspected terminal state and only afterward checked ownership. The completed service performs an actor-scoped read first. Its final write also carries actor scope and BOOKED status. If another request already canceled the row, the conditional write affects zero rows and becomes a conflict rather than replacing the saved reason or timestamp.

The existing initial SQL migration already includes a PostgreSQL half-open exclusion constraint for booked appointments. It is preserved, not presented as a new feature. That database guard is the final protection against concurrent overlapping inserts. Service checks improve feedback, but a read followed by an insert alone cannot establish that guarantee.

Read the map, inspect the local-date algorithm and attempt the exercises before checking the solutions. Tests cover pure calendar behavior, actual service orchestration with repository mocks and actual Prisma query construction with a mocked client. They do not claim that a live PostgreSQL migration or concurrency test ran for this project. VERIFICATION records the exact accepted checks and their scope.
""", None),
'01-CODEBASE-MAP.md': ('Trace preview, booking and cancellation', """
availabilityService.ts assembles working-hour rules, time-off blocks and booked appointments for a staff member. It delegates to buildAvailabilitySlots in src/lib/availability/schedule.ts. The returned slot DTO contains ISO start and end timestamps, isOpen and an optional blocked reason. Direct booking validation calls isSlotOpen from the same module, so preview and command paths share the local-day and overlap policy.

appointmentService.ts coordinates the lifecycle. bookAppointment requires the client role, parses the direct command, loads the staff profile and validates its stored duration before constructing the interval. It checks availability and conflicts, then creates the appointment. Only a recognized Prisma integrity error naming the existing exclusion constraint is translated into a slot conflict. Unrelated errors propagate to the generic route error boundary.

cancelAppointment parses its fields and obtains the appointment through findScopedAppointmentById. appointmentScopes.ts defines the existing role predicates: a client is scoped by clientId, staff by staffProfileId and an administrator can access all appointments. Missing staff profile identity produces an impossible staff scope rather than a broad query. The cancellation repository applies that same scope with BOOKED status to updateMany, then performs a scoped read for the response.

The validation module contains both the HTTP string schema and a Date-based command schema for direct service callers. The distinction matters because routes turn an accepted timestamp string into a Date before calling the service. TypeScript annotations alone cannot prevent an invalid Date or malformed runtime object from reaching that method.

Finally, inspect prisma/migrations/0001_initial/migration.sql. Its btree_gist extension and exclusion constraint encode overlap protection beyond the Prisma model. Applying db push is not equivalent to running this hand-written migration. Keep the SQL file with the schema when preparing a development database, and do not infer migration execution from passing mocked tests.
""", ('src/repositories/appointmentRepository.ts','export async function cancelAppointment','export async function listAppointmentsInWindow')),
'02-CONCEPTS.md': ('Instants, local days and half-open intervals', """
An appointment is stored as two increasing instants. Working hours are local calendar rules: weekday plus start and end minute in a named timezone. Translating an instant to a local clock loses information unless the local date is retained too. The dateKey in getZonedParts prevents a next-day endpoint from being compared as if it belonged to the starting day.

The policy treats ordinary working-hour rules as single-day windows. An appointment may end exactly at the following local midnight if the rule ends at minute 1440. The algorithm checks the instant immediately before the endpoint to prove that this midnight actually closes the starting local day. Any other cross-date interval is closed. Seconds and milliseconds are included in minute comparisons, so a meeting ending just beyond the boundary cannot slip through a truncation.

The formatter uses hourCycle h23 without the conflicting hour12 option. Midnight is therefore represented as 00 rather than 24 in labels and arithmetic. A DST boundary changes the relationship between local clock time and UTC, which is why the tests include a spring-transition local midnight and a folded clock interval. Intervals whose local end clock is not later than the start are rejected by this policy.

Overlap uses half-open semantics: a meeting ending at 10:00 may sit immediately before one starting at 10:00. Positive overlap is blocked. The existing SQL exclusion constraint uses the same interval convention for BOOKED rows; canceled rows do not occupy the calendar.

Validation is separate from availability. An increasing, well-formed interval can legitimately be unavailable. A zero step or invalid timestamp is malformed and should fail promptly, never produce an infinite loop or an apparently valid empty preview. Keeping those outcomes distinct makes both API behavior and tests easier to interpret.
""", ('src/lib/availability/schedule.ts','function isWithinWorkingHours','export function isSlotOpen')),
'03-WORKED-CHANGE.md': ('Scope first, then condition the cancellation write', """
Consider two callers trying to cancel the same appointment. A service can read BOOKED twice before either write finishes. If the repository updates only by ID, both requests succeed and the second replaces the first cancellation reason and timestamp. A prior status check is useful for feedback but is not a concurrency condition on the write.

The repository now uses updateMany with the appointment ID, the actor's access predicate and status BOOKED in one where object. The database decides whether the row still matches when it performs the update. The winning call changes status, reason and cancelledAt. A losing call receives count zero and returns null without performing a fallback update or response read.

The service converts that null into ConflictAppError. A booking already observed as canceled produces the existing InvalidTransitionAppError. Both are 409 outcomes, but they describe different moments: one was terminal at the scoped read, while the other changed between read and write. Neither path changes history again.

Access is also checked in the correct order. The first lookup is findScopedAppointmentById, so a foreign client receives not found without learning whether the appointment was canceled. The conditional update repeats the scope in case access-related data changes after the read. The final response read also retains the same actor predicate.

The tests inspect these real repository arguments for client, assigned staff, missing staff profile and administrator. Service tests separately prove that unrestricted lookup is never called, reasons are normalized, the response comes from the successful repository operation, and a stale loser makes only one write attempt. This combination verifies the actual boundary wiring while remaining honest that no live database race was executed.
""", ('src/services/appointmentService.ts','export async function cancelAppointment','export async function getAppointment')),
'04-TESTING-AND-DEBUGGING.md': ('Separate calendar evidence from persistence evidence', """
The calendar-boundaries suite calls the actual pure scheduling functions. It includes overnight intervals that previously appeared valid, exact midnight endpoints, invalid timezone and rule data, reversed ranges, zero and nonfinite steps, adjacent appointments and a daylight-saving local-date boundary. It also compares each generated preview slot with isSlotOpen to ensure the preview and booking predicate agree.

The appointment-boundaries suite injects repository and availability dependencies using Vitest module mocks. It invokes the actual service and verifies normalization, direct-call validation before reads, bad stored duration, scoped lookup, successful booking and cancellation, and a conditional-write conflict. The provider-error test creates a real PrismaClientKnownRequestError instance with P2004 metadata naming the exclusion constraint. Ordinary errors containing the word conflict must remain ordinary failures.

The appointment-repository suite mocks only the Prisma client. The production repository functions build their real where and data objects. These assertions inspect the actor predicate, BOOKED requirement, expected response scope and the absence of a follow-up read after count zero. This is stronger than testing a separate hand-written query helper that the repository might never call.

The route-boundaries suite invokes the actual cancellation POST handler. It verifies that Next route parameters are awaited, the resolved appointment ID reaches the service, malformed fields return 400, and a missing actor returns 401 before mutation. The shared wrappers accept Promise-based route parameters while passing resolved values to inner handlers.

Existing permission, schema and isolation tests remain in the full suite. The original terminal cancellation test now supplies its canceled record through the scoped lookup mock, matching the production service's corrected path. Its assertion remains a terminal-state rejection.

When debugging, first identify which boundary failed. A malformed Date belongs to validation, a false isOpen may be a valid business result, and a Prisma query shape failure belongs to persistence scope. Inspect the accepted command log and runner total in VERIFICATION. Mocked tests prove orchestration and predicates; they are not evidence that the migration was applied or that PostgreSQL rejected two simultaneous inserts in this environment.
""", ('tests/calendar-boundaries.test.ts',' it("uses local date boundaries',' it("keeps adjacent')),
'05-PRACTICE.md': ('Calendar and cancellation review exercises', """
Exercise one: construct a UTC appointment from 23:30 to 00:30 the following day and a 09:00 through 17:00 working rule. Explain how comparing only clock minutes could accept it, then assert the completed predicate rejects it. Repeat with an endpoint exactly at midnight and a rule ending at 1440. Include one endpoint a millisecond beyond midnight to test the precision boundary.

Exercise two: use America/New_York on the spring daylight-saving transition date. Identify the UTC instant representing the following local midnight and test a half-hour appointment ending there. Then extend it by thirty minutes. The first can fit an all-day rule; the second crosses the permitted local-day boundary. Explain why adding a fixed twenty-four hours is not a general way to find a local midnight.

Exercise three: build two adjacent appointments and one overlapping appointment. Verify the half-open predicate permits the adjacent starts while rejecting positive overlap. Locate the matching bracket convention in the existing SQL migration and explain why canceled rows do not participate in that constraint.

Exercise four: simulate a BOOKED scoped read followed by an updateMany result with count zero. Assert the service returns a conflict and does not retry an unrestricted write. Repeat with a foreign client's scoped lookup returning null. The latter must stop before any write and must not reveal terminal state through a different error.

Exercise five: create a typed Prisma P2004 error for a different constraint and a plain network error containing the word conflict. Neither should become a slot-taken response. Finally write an integration-test plan for a disposable PostgreSQL database that applies the real migration and races overlapping inserts. Keep that proposed evidence separate from the mocked checks already recorded here.
""", None),
'06-SOLUTIONS-AND-REVIEW.md': ('Use the date and the write predicate as proof points', """
The overnight example fails because its local start and end dates differ and the endpoint is not the exact closing midnight of the starting day. A midnight endpoint can be represented as minute 1440 only after checking the immediately preceding instant belongs to the start date. Extending the endpoint even slightly moves it beyond that permitted boundary. Seconds and milliseconds therefore matter in the comparison.

On a spring transition day in New York, the UTC offset changes during the local date. Convert the actual endpoint through the timezone formatter rather than assuming the day has exactly twenty-four elapsed hours. The implementation reasons from formatted local date keys and instants. The regression test demonstrates the selected date-boundary cases; it is not an exhaustive certification of every timezone or historical transition.

For overlap, equality at an edge is allowed because the predicate uses strict less-than and greater-than comparisons. The SQL migration encodes the same half-open range. A cancellation changes the row out of BOOKED, which removes it from the exclusion constraint's predicate without deleting its historical timestamps or reason.

For a stale cancellation, count zero is decisive. There is no successful mutation to return, so the service raises a conflict. Repeating the write by ID alone would undo the protection and recreate the original race. A missing actor-scoped row instead produces not found before status inspection, avoiding a cross-user lifecycle disclosure.

Provider error translation requires both the Prisma error type and the specific known constraint metadata. Arbitrary prose is not a stable domain contract. Unknown failures should reach the existing generic error response rather than being misreported as a booking conflict.

Reviewers should inspect the actual repository call, the service's scoped lookup, the formatter options and the SQL migration together. These pieces implement different parts of the contract. Preserving one while bypassing another can still produce an inconsistent calendar or an unauthorized state change.
""", ('src/lib/data/appointmentErrors.ts','const constraint',None)),
'07-TRACE-LAB.md': ('Follow a cancellation loser through the real service', """
Start with a client actor and a booking that belongs to that client. Supply a valid cancellation reason with surrounding whitespace. The service validates the command and stores the parsed, trimmed reason. It then asks findScopedAppointmentById for the booking using the actor and ID, rather than loading an unrestricted record.

Assume the scoped result is BOOKED. Before the service writes, imagine a second authorized request successfully cancels the same row. The first request still holds its earlier snapshot. Its repository call sends the actor scope and BOOKED status with the ID to updateMany. Because the current row is now CANCELLED, the database reports count zero.

The repository returns null immediately. It does not issue another update, change cancelledAt, replace the winning reason or query an unrestricted row for a response. The service translates the null to ConflictAppError. The caller can refresh the appointment to see its current state, but the failed command has not created another cancellation event.

Now trace the successful path in isolation. updateMany affects one row. The repository performs findScopedAppointmentById again and returns the current included staff and client fields. The service returns that result without fabricating a DTO from stale pre-write values. In the test, the returned cancellation status and normalized reason come from the mocked persistence result.

Finish with a foreign client. The first scoped lookup returns null, so the flow ends with not found before status inspection or mutation. Compare that with an assigned staff actor and an administrator by inspecting their repository where objects. The exercise demonstrates why role permission, resource scope, lifecycle status and conditional mutation are separate checks that all belong in the completed path.
""", ('tests/appointment-repository.test.ts','it.each(',None)),
'VERIFICATION.md': ('Check records, migration requirements and scope', """
The accepted command records below contain the exact arguments, terminal exit codes and logs for the finite tests, TypeScript check, Prisma client generation and production build. Test totals refer to the actual Vitest result, not the number of shell commands. A process still collecting build traces is not counted as complete until its recorded exit status is zero.

Calendar regressions cover invalid intervals and steps, midnight formatting, local date changes, selected DST boundaries, half-open overlaps and agreement between preview and direct availability. Service regressions cover normalized cancellation, scoped lookup before state inspection, direct malformed input, corrupt stored duration, valid creation and narrow provider error translation. Repository regressions inspect the production where clauses and the conditional loser behavior.

Prisma client generation creates application types and query code. It does not apply the schema or migration to a database. The initial migration already contains btree_gist and the BOOKED-only half-open appointment exclusion constraint; this delivery preserves that existing protection. A database created with db push alone may lack the hand-written constraint. Follow the project's migration setup when creating a dedicated development database.

No original appointment database was reset or populated. The tests mock persistence and establish service orchestration and query contracts. They do not prove live PostgreSQL race behavior, migration deployment or browser end-to-end booking. The production build uses an inert database URL only where configuration is needed for compilation. The layout now uses the existing system sans-serif fallback directly, removing a Google-font download that prevented offline builds. This changes the typeface from Space Grotesk to the platform system font without changing page structure.

The scheduling policy is single-local-day working hours with an exact closing-midnight exception. It rejects a folded interval when its local end clock is not after its local start. Overnight working-hour rules and a richer DST ambiguity policy would require explicit product decisions and additional tests. Preserve these limits and the exact original snapshots when extending the scheduling model, and replace verification evidence after any later source changes.
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
f=P/'README.md';s=f.read_text(encoding='utf-8') if f.exists() else '# Appointment booking system\n'
if 'astraupskill/README.md' not in s:s+='\n## Appointment boundary course\n\n[Start the source-based course](astraupskill/README.md) for local-day and midnight rules, conditional actor-scoped cancellation and verification evidence. The existing SQL exclusion constraint requires the hand-written migration; Prisma db push alone does not recreate it. Tests use mocked persistence and do not claim live database concurrency verification.\n'
f.write_text(s,encoding='utf-8')
