from pathlib import Path
P = Path(__file__).resolve().parent.parent / 'stage/27a8a1400c49'
chapters = {
'README.md': ('A cancellation and its replacement belong together', """
This scheduler manages organization-scoped resources, customers, bookings and waitlist requests. A cancellation may release time and immediately promote a compatible request. That makes cancellation a compound workflow: the original booking changes, a replacement may be created, a waitlist entry changes status and audit records explain both actions.

The original service performed those steps through ordinary repository instances without one shared transaction. A later promotion or audit failure could leave the cancellation committed alone. Reschedule and cancel also wrote by ID after reading status, so version increments did not actually prevent a stale writer from changing a booking. The completed workflow runs through transaction-scoped repositories with Serializable isolation and bounded retry of recognized serialization failures.

Waitlist matching now compares UTC intervals constructed from each entry's own timezone. It scans active entries in deterministic creation order, with ID as a tie breaker, and skips malformed or ineligible requests. The replacement uses the request's duration rather than inheriting the entire canceled appointment. Availability, customer scope, lead time and conflicts are checked again before promotion, and the entry must still be ACTIVE when changed.

This course connects the service, transaction helper, repository predicates and time conversion rules. Tests use explicit transaction-aware fixtures and actual repository methods with a mocked Prisma client. They establish orchestration, rollback behavior in the fixture and query construction. They do not claim that a real PostgreSQL concurrency experiment was run for this project.

Read the timezone chapter before changing promotion. A local date in Tokyo can correspond to the previous UTC date, while a New York clock may repeat or skip a time around daylight saving. The helper rejects nonexistent wall times and defines an earlier-instant policy for offset-free ambiguous times. Keep those rules and the verification scope visible when extending the scheduling model.
""", None),
'01-CODEBASE-MAP.md': ('Follow the transaction client through every repository', """
BookingService exposes list, create, reschedule and cancel methods. Permission checks remain at the service boundary. Create and reschedule parse their runtime schemas, while cancellation parses its reason. Mutation calls enter the atomic helper, which obtains transaction-scoped ResourceRepository, CustomerRepository, BookingRepository, WaitlistRepository and AuditLogRepository instances from scheduling-transaction.ts.

The scoped service instance executes the workflow without opening another transaction. Its repositories all use the Prisma transaction client. Reads that decide status, expected version, customer membership, availability and conflicts therefore occur inside the same boundary as the writes they authorize. List operations continue to use their ordinary organization-scoped read repository and validate optional date bounds.

BookingRepository encodes half-open conflict queries using startsAtUtc less than the requested end and endsAtUtc greater than the requested start. Schedule updates and cancellation now use updateMany with organizationId, booking ID, CONFIRMED status and expected version. A zero-row result raises a typed conflict before any follow-up read. WaitlistRepository similarly requires organization and ACTIVE status for promotion.

The transaction helper retries only Prisma P2034 serialization failures, at most three attempts. Each attempt receives newly constructed repository instances over the new transaction client. Unknown errors propagate without retry. The final exhausted conflict becomes a 409 application error. No external calendar, payment or notification operation is included in this retryable callback.

Time conversion lives in timezone.ts; availability rules and preview iteration live in availability.ts. AvailabilityService fetches the resource first so its day query uses the resource timezone rather than the organization timezone. WaitlistService validates the requested local window before creating a row and stores its audit in the same transaction. These paths share primitives without assuming that every caller's local date names the same UTC day.
""", ('src/lib/db/scheduling-transaction.ts','export interface SchedulingRepositories',None)),
'02-CONCEPTS.md': ('Why a version increment is not a concurrency check', """
Incrementing a version tells a later reader that something changed. It does not stop two writers that both read the same earlier version. A concurrency condition requires the expected value in the write predicate. The completed schedule update and cancellation compare the version that was read inside the transaction and require the row to remain CONFIRMED in the same organization.

Serializable isolation addresses a different race: two commands can both observe an empty overlap query and try to insert conflicting bookings. The database may abort a transaction that cannot fit a serial ordering. The helper recognizes Prisma's serialization-conflict code and retries the whole database-only workflow with fresh reads. Retrying just the final insert would reuse decisions from a stale snapshot and would not provide the same contract.

A transaction also controls atomicity. Cancellation, its audit, replacement creation, conditional waitlist promotion and promotion audit are one unit. If a later audit or conditional promotion fails, the cancellation must not remain alone. The in-memory fixture models this by cloning a draft and publishing it only after the callback succeeds; production uses the Prisma transaction client.

Timezones introduce an independent correctness problem. A waitlist date and clock window belong to that request's timezone. They must be converted to UTC before comparison with the released interval. A thirty-minute request fitting inside a sixty-minute cancellation receives thirty minutes. It does not inherit the larger duration just because that time became free.

These guarantees require different evidence. Query-shape assertions verify expected version and tenant predicates. Workflow tests verify that all steps use scoped repositories and that a late failure prevents draft publication. A live database test would be required to measure PostgreSQL's actual behavior under competing transactions. The documentation keeps that final claim separate from the tests completed here.
""", ('src/repositories/bookingRepository.ts','  async cancel(',None)),
'03-WORKED-CHANGE.md': ('Promote a compatible request on the UTC timeline', """
The original promotion logic filtered entries by the canceled booking's resource-local date, compared local clock strings and then copied the entire canceled interval. That could overlook a request whose own timezone named a different date, compare incompatible clocks or give a thirty-minute request a sixty-minute booking.

The completed method obtains active entries for the organization and resource across local dates. The repository orders by createdAt and ID, making the candidate sequence deterministic. For each entry, waitlistUtcWindow converts its desired start and end using its own timezone and verifies that its duration fits the increasing same-day window. Invalid stored entries are skipped rather than causing a valid cancellation to fail.

The candidate start is the later of the released start and the requested window start. Its end is calculated from the entry's duration. Both must fit inside the released interval and the requested window. The service then reloads scheduling context through transaction-scoped repositories to verify the customer, active resource, lead time, availability rules, exceptions and current conflicts.

A compatible candidate becomes a new booking with the entry's timezone and membership attribution. The waitlist update requires that the same organization-owned entry is still ACTIVE. The promotion audit follows inside the same transaction. If that conditional update loses or persistence fails, the whole cancellation workflow rolls back; it does not silently move on after creating an orphan replacement.

No eligible candidate is a normal result: cancellation commits with promotedBooking null and its cancellation audit. Malformed, missing-customer, blocked or stale-window candidates can be skipped during preflight. Database and audit failures are not treated as harmless ineligibility. The regression tests distinguish those outcomes and verify that the replacement duration, timezone and entry linkage are actually retained.
""", ('src/services/bookingService.ts','  private async promoteWaitlistIfPossible',None)),
'04-TESTING-AND-DEBUGGING.md': ('Use transaction-aware fixtures without overstating them', """
The workflow fixture keeps bookings, waitlist entries and audit records in one state object. Each simulated transaction clones that object and gives the service repositories backed by the draft. Only a successful callback publishes the draft. Outer repositories are sentinels that throw if a mutation accidentally uses them, so a passing workflow proves the service switched to the scoped dependencies.

Cancellation tests cover a sixty-minute release promoting a thirty-minute New York request, deterministic FIFO selection, skipped incompatible entries, no eligible candidate and a late promotion-audit failure. The late failure compares the entire retained graph with the original snapshot. A repeated cancellation test issues two concurrent promises through the serialized fixture and verifies one replacement and one pair of audits. This checks orchestration under the fixture's model; it is not a live PostgreSQL concurrency result.

Create and reschedule tests cover adjacent half-open intervals, real conflict rejection, expected-version loss, direct malformed input, wrong organization and audit rollback. Waitlist creation checks that an impossible window fails before transaction entry and that a later audit failure rolls back the new request. A lead-time test injects the system clock and verifies that an otherwise matching request is skipped when its start is already too late.

The repository suite calls actual production repository methods with a mocked Prisma client and inspects their write predicates. It also exercises the real retry helper with recognized serialization errors, verifies three-attempt exhaustion and proves unrelated errors are not retried. Time tests cover DST gaps, both explicit offsets of a fold, date-boundary conversion and invalid slot steps.

When a test fails, inspect whether it concerns validation, time conversion, workflow ordering or query construction before broadening the fixture. TypeScript and lint checks run separately from Vitest. VERIFICATION records the terminal passing commands and actual totals accepted for the delivered source.
""", ('tests/repository-transactions.test.ts','it("bounded serializable retry',None)),
'05-PRACTICE.md': ('Scheduling exercises with explicit invariants', """
Exercise one: cancel a UTC appointment from 10:00 to 11:00 and provide a New York waitlist window from 06:00 to 07:00 on a September date. Request thirty minutes. Predict the replacement's UTC interval, local timezone and duration before invoking the service. Then use a Tokyo window whose local date differs from UTC and explain why filtering candidates by one resource-local date would be unsafe.

Exercise two: create three entries with the same creation timestamp. Make the first too long for the released interval and give the other two compatible windows. Order their IDs deliberately. Verify the first compatible entry in the repository's deterministic ordering is promoted, while the others remain ACTIVE. The test should inspect stored linkage, not only the returned booking.

Exercise three: force the promotion audit to fail after cancellation, replacement creation and waitlist mutation. Compare the entire retained state with an independent before snapshot. Repeat with a conditional promotion failure. Both failures must abort the cancellation rather than leave a canceled source and an unexplained replacement.

Exercise four: inspect the actual updateSchedule where object. Remove expected version in a local experiment and identify the repository assertion that fails. Explain why increasing version in data cannot compensate for the missing predicate. Restore the condition and repeat the exercise for organization scope and CONFIRMED status.

Exercise five: pass an offset-free repeated local clock time around the autumn DST transition, then the two explicit valid offsets. Predict which instant the helper chooses in each case. A nonexistent spring-gap time must reject. Finally propose a disposable PostgreSQL concurrency test for two overlapping creates, keeping that proposed test separate from the in-memory fixture evidence already recorded.
""", None),
'06-SOLUTIONS-AND-REVIEW.md': ('Distinguish ineligibility from a failed transaction', """
The September New York request beginning at 06:00 corresponds to 10:00 UTC. With a thirty-minute duration, its replacement ends at 10:30 UTC even though the released appointment ends at 11:00. The stored booking retains the request timezone and calculated local endpoint. A Tokyo midnight request may correspond to the preceding UTC date, so each candidate's window must be converted before comparing dates or intervals.

FIFO applies among compatible entries. The repository orders creation time first and ID second. A request that is too long, outside the released window, blocked by availability or no longer inside lead-time rules is skipped during preflight. A later compatible entry can then win. Once a replacement is being written, a failed conditional promotion or audit is a transaction failure, not a reason to continue to another candidate.

The rollback comparison must include the source booking, replacement list, waitlist status and audits. Inspecting only the canceled source can miss an orphan replacement or a misleading event. The sentinel outer repositories provide another proof point: mutations must use the repositories created from the transaction client, not dependencies that happen to return similar values outside the boundary.

Expected version belongs in the where clause together with organization, ID and CONFIRMED status. The increment belongs in data after that predicate matches. Count zero is a conflict and must not trigger an unconditional fallback. Waitlist promotion applies the analogous ACTIVE condition.

For ambiguous local times without an offset, the helper selects the earlier possible instant deterministically. An explicit valid offset can select the later occurrence. An offset that disagrees with the supplied timezone's local wall time is rejected. Spring-gap round-trip mismatch is also rejected. Review those rules alongside the tests before changing how clients submit timestamps, and retain the distinction between checked conversion behavior and untested production database concurrency.
""", ('src/lib/time/timezone.ts','export function toUtcInterval','export function waitlistUtcWindow')),
'07-TRACE-LAB.md': ('Trace a serializable retry from fresh reads', """
Start with a create-booking command that passes permission and runtime validation. The service enters atomic, and the transaction helper begins its first Serializable attempt. It constructs all five repositories using the supplied transaction client and gives them to a scoped service instance. That instance reads the resource, customer and overlap set before deciding whether to write.

Assume the first attempt receives a Prisma P2034 error because of a concurrent scheduling operation. The helper catches only that recognized code and starts another complete transaction attempt. It does not reuse the previous repositories, overlap result or tentative booking. The second attempt therefore repeats the business reads against its own transaction snapshot.

Now trace a successful cancellation with a compatible waitlist entry. The scoped service reads the current booking and captures its version, performs a conditional cancellation, appends the cancellation audit, evaluates entries in FIFO order and constructs a candidate interval. The candidate is checked against resource availability and conflicts before creating the replacement. Conditional ACTIVE promotion and its audit complete the workflow.

Inject a failure at the last audit. The production transaction rejects, so the callback cannot return a successful cancellation response. In the test fixture, the draft is discarded and the previously retained graph remains unchanged. Explain why a catch block that merely logged this failure and returned the canceled booking would violate the intended contract.

Finally inspect the retry exhaustion test. Three recognized serialization failures become a typed 409. An unrelated connection or application error is thrown immediately without blind retry. This bounded policy is suitable only because the callback contains local database work. Adding an external notification or provider action requires an idempotency or outbox design before that action can safely participate in retries.
""", ('src/services/bookingService.ts','  private atomic','  async listBookings')),
'VERIFICATION.md': ('Evidence, database scope and time policies', """
The accepted command records below show the finite regression suite, static checks, Prisma client generation and production build used for this delivery. Each record includes exact arguments, terminal status and a project-local log. The test total comes from the actual Vitest summary. Failed or incomplete attempts remain historical evidence and are not counted as successful validation.

Workflow tests exercise scoped transaction wiring, cancellation with and without promotion, requested duration, timezone conversion, FIFO selection, malformed and ineligible candidates, duplicate cancellation, create and reschedule, expected-version loss, wrong organization, lead time and late audit rollback. Repository tests inspect the real conditional predicates and bounded retry implementation. Time helpers have targeted gap, fold, local-date and invalid-step cases.

These tests use explicit mocks and a transaction-aware in-memory fixture. They do not certify live PostgreSQL Serializable behavior, deployment of a database schema or end-to-end browser use. Prisma generation creates client code, not a database. No inherited database connection was used for destructive setup, and no original bookings were changed by the test suite.

The production workflow is configured to retry at most three recognized serialization conflicts. It contains only database operations. A future external calendar, email or webhook action must not be added to this callback without its own idempotency or outbox strategy. Unknown errors remain visible failures rather than being mislabeled as ordinary waitlist ineligibility.

The waitlist query examines active entries across local dates to compare each entry in its own timezone. Large deployments may need a carefully designed indexed UTC search representation. Offset-free folded times choose the earlier instant; explicit valid offsets can disambiguate; nonexistent wall times reject. Preserve these operating rules, the exact source snapshots and the evidence links when extending the scheduling model, and rerun the relevant checks after any source change.
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
f=P/'README.md';s=f.read_text(encoding='utf-8') if f.exists() else '# Organization scheduler\n'
if 'astraupskill/README.md' not in s:s+='\n## Scheduling transaction course\n\n[Source-based course](astraupskill/README.md): Serializable booking workflows, expected-version writes, atomic waitlist promotion and timezone rules. Tests use explicit transaction-aware mocks; they do not establish live PostgreSQL concurrency behavior. No external notification belongs in the retryable transaction without idempotency or an outbox.\n'
f.write_text(s,encoding='utf-8')
