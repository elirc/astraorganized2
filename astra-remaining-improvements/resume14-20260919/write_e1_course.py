from pathlib import Path
P = Path(__file__).resolve().parent.parent / 'stage/0bfafff7d45f'
chapters = {
'README.md': ('A booking that remains booked', """
The scheduling demo originally returned convincing booking objects without retaining them. A successful create response could be followed by a detail lookup that found nothing, while slot previews continued offering the same time. Cancellation and rescheduling had similar gaps. This course follows the replacement: a shared process-local repository, explicit command validation, organizer-wide availability, guest tokens and atomic replacement of a booking.

Start with the codebase map, then inspect the repository excerpt below. The read method returns a clone rather than the mutable internal arrays. The transaction method makes a working copy, invokes a synchronous callback, clones its result and only then replaces retained state. A callback that throws cannot publish its draft. This gives the demonstration a useful atomicity boundary within one JavaScript process. It does not provide database persistence, crash recovery or synchronization between server instances.

The seed contains illustrative people, calendars, event types and bookings. New booking tokens use random UUIDs. Existing seed tokens and owner-facing information belong to a public simulator; this is not a production authentication system. Registration, login, event editing and integration commands still demonstrate response shapes. No external calendar, email account or OAuth provider participates in these tests.

Use Node with TypeScript stripping support, install the package dependencies and run npm test, npm run typecheck, npm run lint and the production build command recorded in VERIFICATION. Read the failed-request tests as carefully as the success test. The important contract is that a rejected reschedule leaves both the original booking and its attendee linkage unchanged. Later chapters explain how to prove that contract without relying on a screenshot or a returned success message.
""", ('src/lib/booking-repository.ts', 'export function createBookingRepository', 'export type BookingRepository')),
'01-CODEBASE-MAP.md': ('Follow commands and reads to the same state', """
There are four layers in the booking path. Route handlers accept HTTP requests and return correlation-aware responses through http.ts. mock-services.ts now exports the real booking service methods while retaining the other explicit mock actions. booking-service.ts owns validation, authorization and lifecycle decisions. booking-repository.ts owns the cloned process-local state and synchronous transaction boundary.

The data module still defines seed fixtures, but getBookings and getBookingAttendees read the repository. getBookingById and getBookingByToken build on those getters. The dashboard assembles current bookings and attendees with a fresh clock. The public booking page offers only published, nondeleted events and sends the current organizer's bookings to generateSlots. These are not separate copies of booking truth. The root layout uses dynamic rendering so rendered pages consult current state rather than a build-time snapshot.

The global repository reference keeps module reloads or separate server bundles within one Node process pointed at the same demo state. A second process has its own repository. A restart recreates the fixtures. Tests needing isolation should construct a repository directly; the integration-style demo test resets the shared repository in a finally block.

Availability is calculated in availability.ts with local-date helpers from time.ts. That file has no Next request dependency. booking-state.ts contains legal transitions and cancellation-reason handling. The service translates lifecycle failures into BookingError with a specific status. bookingFailure exposes known messages and returns a generic message for unexpected exceptions, avoiding accidental disclosure of internal details.

Trace a new booking by opening create in the service, then getBookingDetail in the mock-service facade, then getBookingById in demo-data. The source excerpt is the concrete bridge between static fixtures and retained data. If a future feature reads the original arrays directly, it can recreate the initial inconsistency even though commands still succeed.
""", ('src/lib/demo-data.ts', '// Shared only within', 'export function getCalendarIntegrations')),
'02-CONCEPTS.md': ('Availability, authority and atomicity are different decisions', """
An available slot is a start and end instant that fits the organizer's local weekly window, overrides, blocked times, active bookings, notice period and booking horizon. The event duration determines its end. The event interval determines candidate starts. Clipping a query range must not shift that grid: a request beginning at 09:07 does not make 09:07 a valid half-hour start. Candidate starts are generated from the original window, then filtered against the requested range.

An organizer may publish several event types. Comparing only eventTypeId would let two different meetings reserve the same person at once. The implementation therefore checks organizerId and active booking status. For each existing booking it resolves that booking's event buffers, then compares the requested meeting including its own buffers. Touching interval edges are allowed; positive overlap is rejected. Canceled and soft-deleted bookings do not block future slots.

Authority is checked separately. Knowing a booking ID does not grant a guest permission to change it. Confirm, cancel and reschedule require the exact confirmation token, and the latter two also enforce guest action flags. These checks protect the command boundary in this simulator. They do not retrofit real owner login or make publicly seeded data secret.

Atomicity describes publication of state. Reschedule first verifies the target against all other bookings, then constructs a canceled predecessor, a fresh replacement and copied attendee links inside one repository transaction. Failure before commit leaves the stored graph unchanged. There is no asynchronous network call inside that callback, so another JavaScript command cannot interleave halfway through it.

These guarantees have different tests. Slot tests examine candidate times; token tests examine rejected callers; rollback tests compare complete state before and after failure. Passing one category is not proof of the other two.
""", ('src/lib/booking-service.ts', '  function authorize', '  function transition')),
'03-WORKED-CHANGE.md': ('Reschedule without losing the original appointment', """
Begin with the original service snapshot in the snapshots directory. It constructed a canceled predecessor before checking an offered target. The replacement spread the old booking, retaining the confirmation token and creation timestamp, and neither object was inserted into the data used by later reads. A caller could receive a successful-looking response without a durable change even within that process.

The completed method accepts a booking ID, requested timestamp and guest token. Inside a repository transaction it locates a live booking, checks token and reschedule permission, and restricts the source to pending or confirmed. It samples the clock once. The offered-slot calculation excludes only this source booking, preserving conflicts with every other event for the organizer. That exclusion also permits a deliberate reschedule to the same still-valid time.

Only after preflight succeeds does the code cancel the original. The replacement gets a distinct ID and token, refreshed createdAt and updatedAt values, a confirmed status and rescheduledFromBookingId pointing to the predecessor. Attendee records are copied with new record IDs and the replacement booking ID. Historical attendee links remain attached to the canceled predecessor for inspection.

The repository publishes all of these changes together. Returning a replacement object cannot bypass that publication, because transaction result cloning occurs before state replacement. An exception in the callback or result cloning leaves the old retained state intact. The original token can still identify the historical canceled booking, but it cannot authorize mutation of the replacement; terminal transition rules prevent reconfirming the canceled predecessor.

The regression test first requests a time outside working hours and compares the entire repository snapshot with its earlier value. It then performs a valid replacement and checks status, linkage, token rotation and timestamp changes. This makes the intended behavior reviewable through observable state rather than through implementation order alone.
""", ('src/lib/booking-service.ts', '    reschedule(id:', None)),
'04-TESTING-AND-DEBUGGING.md': ('Test the booking contract through actual consumers', """
The suite uses Node's built-in test runner and a small loader that resolves the project's TypeScript aliases. It invokes real service functions and actual route handlers; no database container is involved because this application's storage boundary is deliberately in memory. Type checking remains a separate command because runtime type stripping does not verify TypeScript types.

The deterministic fixture uses a fixed Monday morning in UTC and creates two published event types for one organizer. Every day has the same business hours. This removes unrelated seed calendar changes from conflict tests. Individual tests create isolated repositories and service instances, allowing buffers, guest flags and clocks to be varied without affecting other cases.

A separate test exercises the default demo graph: create through mock-services, read by ID and token, inspect detail attendees and dashboard entries, check that the offered slot disappears, cancel, then check that it returns. That test resets the shared repository in finally. It is valuable because isolated service tests cannot discover a forgotten static-array read in a page data helper.

The HTTP test creates NextRequest objects and calls POST exports directly. It checks 400 for malformed command fields, 403 for a missing guest token, 404 for an unknown booking and 409 for confirming a canceled booking. It also verifies a successful 201 response from the create route. This does not substitute for a browser test or a deployed multi-process test, but it proves the route-to-service status mapping.

When debugging, first reproduce the smallest failing assertion. A type error belongs to type checking; a loader failure occurs before assertions; an availability rejection needs the clock, event configuration and organizer blockers inspected together. Keep the recorded unsuccessful command logs as history, and use only terminal passing runs as delivery evidence.
""", ('src/tests/booking-flow.test.ts', 'test("create, detail', 'test("reads and returned')),
'05-PRACTICE.md': ('Exercises with observable outcomes', """
Exercise one: create two event types owned by the same organizer, with a thirty-minute meeting starting at 10:00. Give the first event a thirty-minute trailing buffer and the second a fifteen-minute leading buffer. Predict whether 11:00 and 11:30 should be offered for the second event, then prove the result with the public service. Explain which two occupied intervals overlap. Keep a control case for a different organizer.

Exercise two: extend the command tests with an unknown booking, a valid ID paired with a wrong token, and a correct token paired with guestCanReschedule set to false. Assert the intended status for each case and compare repository state with a snapshot taken before the command. A test that checks only that something threw is insufficient: it can pass for an unrelated configuration error.

Exercise three: inspect the repository transaction callback. Deliberately remove a booking from the draft and then throw. Confirm the stored booking and attendee remain. Next mutate an object returned by read and verify a later read remains unchanged. These are different forms of isolation: rollback protects failed work, while cloning protects the boundary from callers holding references.

Exercise four: query a half-hour schedule with rangeStart at 09:07, then add a duplicate available window. The first start must remain 09:30 and each instant must appear once. Try zero, negative and nonfinite intervals; each must fail quickly instead of entering an unbounded loop. Preserve the distinction between a programming/configuration error and a legitimate empty slot list.

Exercise five: design a persistent implementation on paper. Identify the database constraints and transaction isolation needed to prevent competing organizer bookings, and decide how a provider calendar update would be retried. Do not remove the documented process-local limitation merely because the in-memory tests pass. External side effects need their own recovery model and evidence.
""", None),
'06-SOLUTIONS-AND-REVIEW.md': ('Reason from state and boundary predicates', """
For the buffer exercise, the first appointment occupies 10:00 through 11:00 after adding its trailing buffer. The second candidate at 11:00 occupies time beginning at 10:45 after adding its leading buffer, so it overlaps and must fail. A candidate at 11:30 begins occupying time at 11:15 and can succeed if every other scheduling rule passes. A different organizer's booking must not block either candidate.

For authorization, a missing resource is 404, a known resource without a matching token is 403, and a disabled guest action is also 403. A valid caller attempting an illegal terminal transition receives 409. Missing required fields and a whitespace-only cancellation reason receive 400. The service is responsible for these decisions even when called directly rather than through an HTTP route.

For state isolation, the working draft is discarded when its callback throws. The stored arrays are replaced only after the callback result can be cloned successfully. read returns a separate graph, so changes to its booking objects cannot silently modify retained data. The output of a successful command is likewise detached. This is why asserting a later read is stronger than asserting the returned object alone.

For slot generation, the cursor is anchored to the original local window. The requested date range filters candidates without shifting that anchor. A set of ISO start instants removes duplicates from overlapping windows, and positive finite integer configuration guards execute before the loop. The supplied clock keeps notice and horizon checks deterministic throughout one call.

During review, look for accidental direct access to seed bookings, service defaults that invent required values, token checks performed after mutation, or a reschedule that reuses the old token. Confirm that new attendee rows point to the replacement and historical rows still explain the predecessor. Review the original snapshots alongside these tests, then record actual commands after any further code change.
""", ('src/lib/booking-state.ts', 'export function canTransitionBooking', None)),
'07-TRACE-LAB.md': ('Trace one failed replacement and one successful replacement', """
Choose a fresh deterministic fixture and create a 10:00 appointment. Record its booking ID, confirmation token, status, attendee ID, createdAt and updatedAt. Read the repository immediately afterward; the retained graph should contain one booking and one attendee. Keep that complete graph as the comparison baseline rather than retaining references to mutable objects.

Now request a reschedule to 19:00 with the correct token. Step through authorize, the active-status check and offered. Authorization succeeds, but the target falls outside the configured 09:00 through 18:00 window. offered raises a conflict before the source booking is transitioned. The repository callback exits through the exception path, leaving both arrays equal to the baseline. The route translates the typed error into 409 without exposing an internal stack.

Repeat with an 11:00 target and a later injected clock. The availability input contains all active organizer bookings except the source. After a slot match, transition creates the canceled predecessor. A separate replacement receives a random ID and token, fresh timestamps and the predecessor ID. Each linked attendee is copied with a new ID. The callback updates the predecessor, appends the replacement and appends those copied attendees. Only then does the repository publish the completed draft.

Read by both tokens. The old token should still identify the canceled historical booking; it must not identify or authorize the new appointment. A confirm attempt against the predecessor should fail with a terminal conflict. A cancel attempt against the replacement using the old token should fail with forbidden. These checks distinguish history preservation from authority transfer.

Finally inspect the public slot preview. The new occupied interval should disappear for all events sharing the organizer, while the old interval may return if no other blockers or notice rules exclude it. Explain that final qualification before concluding that a particular missing slot is a repository bug.
""", ('src/lib/booking-service.ts', '  function offered', '  function authorize')),
'VERIFICATION.md': ('Evidence and operating limits', """
The evidence section below records the completed commands accepted for this delivery, their exit codes and project-local logs. The test total counts assertions grouped by the runner as tests; it does not count shell commands as tests. Read the complete test summary and require zero failures, skips and cancellations. A command that is still running is not accepted evidence.

The finite suite exercises direct commands, shared demo consumers, cloned return values, transaction rollback, invalid input, organizer conflicts, both event buffers, notice and horizon rules, terminal states, token permissions, attendee linkage and actual HTTP status mapping. Type checking and linting catch a different class of defects. A production build verifies framework compilation and route generation, while the dynamic root layout prevents a build snapshot from becoming the retained booking view.

These checks do not establish production durability. Storage is process-local and resets with the process. Multiple workers or hosts can disagree because there is no shared database or distributed lock. Login, registration, owner administration and integration actions remain a simulator. Seed tokens are illustrative; new tokens are random. The tests make no claim that a real OAuth connection, notification delivery or external calendar synchronization occurred.

Timezone conversion uses the project's existing local-date helpers. Deterministic regression cases use UTC. This delivery does not certify every daylight-saving gap, fold, timezone database version or overnight availability convention. Such support needs explicit product rules and targeted tests before stronger claims are made.

Keep the original snapshots when experimenting. They provide an exact baseline for reviewing why behavior changed. Run the relevant checks after source edits and replace the recorded evidence only with a terminal passing result. The course and report describe the implemented scope and its remaining operational limits so the next reader can distinguish a complete teaching flow from a deployed scheduling service.
""", None),
}
nav = '\n## Course navigation\n\n' + ' / '.join(f'[{name.removesuffix(".md")}]({name})' for name in chapters) + '\n'
(P/'astraupskill').mkdir(exist_ok=True)
for name,(title,body,excerpt) in chapters.items():
 text='# '+title+'\n\n'+body.strip()+'\n'
 if excerpt:
  file,start,end=excerpt;source=(P/file).read_text();index=source.index(start);sample=source[index:source.index(end,index) if end else len(source)]
  text+=f'\n## Source excerpt\n\nFrom [{file}](../{file}).\n\n```ts\n{sample.rstrip()}\n```\n'
 text+=nav
 assert len(text.split())>=250,(name,len(text.split()))
 (P/'astraupskill'/name).write_text(text,encoding='utf-8');print(name,len(text.split()))
f=P/'README.md';s=f.read_text(encoding='utf-8')
if 'astraupskill/README.md' not in s:s+='\n## Retained booking demo\n\n[Booking service course](astraupskill/README.md): process-local booking state, organizer availability, guest token authorization and atomic rescheduling. State resets on restart and is not shared between workers. Owner login and calendar integrations remain simulations. Guest commands require confirmationToken in the JSON body; cancel also requires reason and reschedule requires startTime. Run npm test, npm run typecheck and npm run lint.\n'
f.write_text(s,encoding='utf-8')
