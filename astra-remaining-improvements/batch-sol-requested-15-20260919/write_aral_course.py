from pathlib import Path
import json
from course_writer import write_course

store = 'packages/app/src/state/store.ts'
tests = 'packages/app/src/state/store.test.ts'
dao = 'packages/app/src/db/dao/events.ts'
sync = 'packages/app/src/db/sync/outbox.ts'
derived = 'packages/shared/src/derived.ts'
chapters = {}
def add(name, title, body, file, anchor, count):
    chapters[name] = (title, body, [(file, anchor, count)])

add('README.md', 'Aral: one persisted event, one contribution', '''
Aral derives learning progress from an event log. That design makes retries convenient only if every layer agrees about which events exist. SQLite already uses event identifiers to ignore repeated inserts. Before this change, the live store could append the incoming event anyway, so displayed progress and a subsequent reload could disagree. A retry could therefore look like additional XP until hydration rebuilt state from storage.

This course follows the repair through shared reduction, persistence, the app store, and synchronization. Start by locating each boundary in the codebase map. Calculate the conflicting-duplicate example in Concepts, then read the worked change to see why deduplicating an array alone was insufficient. The testing chapter explains the deliberately stateful DAO fixture and its limits. Practice and solutions focus on ordering, authoritative reads, and failure recovery.

The intended contract is first-write-wins for an event identifier. A later payload with the same identifier cannot replace the accepted lesson or XP value. Deduplication occurs before timestamp sorting so an earlier timestamp in a conflicting retry does not become a back door for replacing the original event.

The store also serializes asynchronous mutation-and-refresh operations. Local recording, remote merging, clock correction, and hydration participate in the same queue. After a write, it reads the persisted log and rebuilds the snapshot. This is an application ordering guarantee, not a claim that every DAO operation is a native database transaction. Keep that distinction visible while reading the tests and final verification record.
''', store, '// SQLite writes', 28)

add('01-CODEBASE-MAP.md', 'Map the log, reducer, store, and sync worker', '''
The shared package defines ProgressEvent and rebuildDerivedState. The reducer is used to calculate XP, completed lessons, and other learning state from events. Its new firstEventsById step runs before event ordering. This protects every caller of the shared reducer, not only the visible app store.

The events DAO owns persistent append, remote merge, list, and replacement operations. Append and merge use SQLite INSERT OR IGNORE semantics. listAll returns the actual stored events. The distinction matters when a batch contains an identifier that already exists with a different payload: the caller's proposed payload is not necessarily the one storage retained.

The Zustand store publishes events and derived state to the application. record and mergeRemote queue a DAO write followed by a read and snapshot refresh. replaceEvent uses that same ordering boundary for clock corrections. hydrateStore queues its reads and publication, avoiding a boot or account-reset hydration overtaking an already queued mutation.

The outbox worker pushes unsynced events and pulls remote events. A clock_future rejection replaces the original with a fresh identifier and corrected timestamp. That replacement now passes through the store, so even a subsequent empty pull leaves the screen consistent with the corrected local log. Marking an event synced changes delivery bookkeeping; it does not add a second contribution to learning progress.

Use these boundaries when debugging. A duplicate contribution points first to event identity and reduction. A stale screen after a successful write points to publication ordering. A missing durable event requires inspecting the DAO and its persistence behavior separately from the in-memory store.
''', sync, 'async function pushOnce', 33)

add('02-CONCEPTS.md', 'Identity wins before timestamp ordering', '''
Consider a persisted lesson completion with identifier A and fifteen XP. A network retry carries identifier A again. It represents the same event, so the derived total remains fifteen. Now change the retry to claim nine hundred ninety-nine XP and an earlier occurrence time. The identifier still identifies an already accepted event. Sorting by time before choosing the first duplicate would mistakenly prefer the conflicting retry. Choosing the first arrival before sorting preserves the accepted payload.

This contract differs from last-write-wins state synchronization. A progress event is an immutable contribution, not an editable row whose newest payload should replace the old one. If the application needs a correction, it must express that correction through its explicit replacement path. The clock correction path removes the original identifier and adds a replacement; its store refresh then reflects the actual resulting log.

The queue is a promise chain. Each operation begins after its predecessor settles. The public promise still rejects when an operation fails, while the internal tail catches that rejection so later operations can continue. Without that distinction, one failed write could permanently block all subsequent progress recording.

An authoritative read is equally important. An append may ignore a duplicate or fail after persisting an earlier row. Reconstructing memory from the proposed input would miss those outcomes. Reading listAll after the write attempt lets the store publish what actually survived, then surface the original failure. This does not make partial persistence disappear; it prevents the screen from inventing a different history.
''', store, '  record: (newEvents)', 25)

add('03-WORKED-CHANGE.md', 'Serialize mutation and reconciliation together', '''
The old mental model was append input, append to memory, then reduce. The corrected model is attempt the persistent operation, read the accepted log, publish that log, reduce it, and save the derived snapshot. The queue encloses this entire sequence. Queuing only the DAO call would still allow overlapping readbacks and snapshot publications to finish in the wrong order.

record and mergeRemote capture whether the write failed separately from the error value. JavaScript permits throwing undefined, so checking whether an error variable is truthy would not reliably represent failure. After reconciliation, the operation rethrows the captured value when the explicit failure flag is set. The internal queue tail absorbs rejection only to keep future work runnable; it does not hide the error from the caller.

replaceEvent follows the same sequence. The outbox's clock_future branch calls it through useApp rather than directly invoking the DAO. This repairs a less obvious stale-state case: the server can reject a future event, the client can replace it successfully, and the following pull can contain zero events. The screen must still refresh without waiting for a nonempty remote batch.

hydrateStore also joins the queue. It reads events, cached derived state, and authentication metadata only after prior queued work. The cached snapshot is a convenience, while rederive computes from accepted events. These changes preserve the existing persistence interface and reducer contract without asserting stronger transactional guarantees than the DAO actually provides.
''', store, '  replaceEvent: (oldId, replacement)', 24)

add('04-TESTING-AND-DEBUGGING.md', 'Test ordering with controlled promises', '''
The store tests use a Map-backed DAO fixture that implements first-write-wins insertion. This is more useful than returning an empty array from every mock: the store must read back the payload that the fixture actually retained. Sequential retries and conflicting payloads verify both the event list and the derived XP or completed-lesson state.

The concurrency tests deliberately hold the first append on a promise. They start a second operation while the first is blocked and assert that its DAO method has not run. Releasing the promise lets both finish, after which the test inspects the final authoritative snapshot. This controls the interleaving without relying on a guessed sleep duration.

A partial-failure case inserts one row and then throws. The public record call rejects, but the store still displays the retained row. A subsequent conflicting retry proves that the queue remains usable after rejection and that the original payload still wins.

The correction-and-hydration regression queues a record, a replacement, and hydration. Neither replacement nor readback may overtake the blocked append. After release, the corrected event appears exactly once and contributes fifteen XP, without any remote pull being necessary.

These are store contract tests, not device database tests. They do not prove native SQLite rollback or web persistence durability. When a failure appears only on a device, inspect the real adapter after confirming this ordering contract. Shared reducer tests separately verify duplicate identity handling so store fixtures are not the only protection against double counting.
''', tests, '  it("queues clock correction', 24)

add('05-PRACTICE.md', 'Predict retries, failures, and clock correction', '''
Exercise one: record completion A with fifteen XP, then retry A unchanged, then retry A with a different lesson and nine hundred ninety-nine XP. Predict the stored log, live event list, total XP, and completed lesson identifiers after each call. Explain why the third payload does not become authoritative merely because it arrived later.

Exercise two: give that conflicting retry an earlier occurredAt timestamp. Compare deduplication-before-sort with sort-before-deduplication. Write a minimal input sequence that makes the two algorithms choose different payloads. State which algorithm matches INSERT OR IGNORE semantics.

Exercise three: block a local append after its first row is persisted. While blocked, enqueue a remote merge. Identify which calls may have started and which must remain waiting. Then release the append and predict the final order of operations. Your answer should include the snapshot write, not only the two DAO mutations.

Exercise four: make append throw after retaining one event. Predict the caller's result and the live state. Then enqueue another valid record. Explain the role of the caught internal tail in allowing that later operation to proceed.

Exercise five: a future-clock event is rejected, replaced locally, and followed by an empty remote pull. Trace the path from the outbox worker to replaceEvent and the new snapshot. Describe the stale display that would return if the worker called the DAO directly again. Keep your proposed assertions about application state separate from claims about native transaction atomicity.
''', tests, '  it("reconciles a partially', 23)

add('06-SOLUTIONS-AND-REVIEW.md', 'Solutions and review questions', '''
The first exercise retains A's original payload throughout. The event list has one element, total XP is fifteen, and the original lesson remains completed. The conflicting retry is ignored because identity governs acceptance. A reducer that sums all received payloads would disagree with the database even if the UI appeared correct immediately after the first call.

In the second exercise, deduplicating before sorting retains the first accepted payload. Sorting first can move the conflicting retry ahead of the original and select it instead. The regression should use different payload values as well as different timestamps; two identical duplicates cannot expose the mistake.

For the blocked append, the queued merge does not begin until append, authoritative read, reduction, and snapshot persistence settle. After release, the merge runs and performs its own readback and publication. This ensures the last published snapshot includes both accepted operations.

For partial failure, the record promise rejects while the store reflects the row that survived. The internal tail is replaced with a caught promise, allowing the next operation to start. Catching only at the UI would not repair a permanently rejected internal chain.

For clock correction, the queued replacement refreshes state itself. An empty pull therefore does not prevent the corrected timestamp and identifier from reaching the screen. Calling the DAO directly would bypass this guarantee. During review, ask which public mutation paths join the queue, which state is authoritative, and what happens after a thrown write. Also ask what the tests cannot establish: the Map fixture cannot prove the actual SQLite adapter's transactional or durability behavior.
''', store, 'function enqueueEventWrite', 8)

add('07-TRACE-LAB.md', 'Trace one delayed local event', '''
Draw four columns: caller, queue, DAO, and published store. Put the initial completion A in the caller column and an empty Map in the DAO column. Start record(A), insert A into the fixture, and pause the append before it returns. The published store has not yet been refreshed. That intermediate state is intentional because the queued operation has not reached its reconciliation phase.

Now enqueue replaceEvent(A, B), where B carries the corrected time and a new identifier, followed by hydrateStore. Both requests have promises, but neither may enter its read or write phase yet. Check the fixture spy counts at this exact point. A replacement call or listAll read would demonstrate that the shared ordering boundary had been bypassed.

Release the append. record reads A, reduces it, and persists its snapshot. Replacement then removes A, adds B, reads B, reduces it, and persists the corrected snapshot. Hydration finally reads the accepted log and metadata and publishes B again. The final XP remains fifteen because replacement represents one completion, not a second award.

Repeat the trace with append throwing after inserting A. Its reconciliation still publishes A before rejecting, and the caught tail permits replacement to proceed. Finally, repeat with an empty pull after replacement. Nothing further must happen for the screen to show B. This last trace is why the outbox call site matters as much as the store helper. Keep the native adapter's non-atomic replacement behavior as a separate investigation rather than assuming this timeline proves database rollback.
''', sync, '      const replacement = ProgressEvent.parse', 12)

add('VERIFICATION.md', 'Read the accepted checks and their limits', '''
The recorded commands below define the completed verification scope. Test results are accepted only after a command terminates successfully. Installation output, source inspection, and a still-running process are not test passes. Failed setup attempts remain in the campaign history rather than being rewritten as successful evidence.

Shared reducer tests protect first-arrival event identity before sorting. Store tests protect reconciliation after ignored inserts, competing operations, partial write failure, and queued clock correction followed by hydration. Their Map-backed DAO fixture is intentionally stateful, but it remains a mock of the persistence boundary. Native SQLite transactions, device restarts, and deployed synchronization require separate environments and are not implied by these results.

Type checking provides another useful boundary: the store exposes the replacement operation in its state interface, and the outbox caller must pass a ProgressEvent. It cannot establish runtime persistence semantics, which is why the behavioral tests inspect final events and derived progress as well as method calls.

Reproduction should use the repository scripts and the exact accepted command arguments captured with this delivery. Avoid copying the user's original database into a test workspace. The changed source is staged independently, and original snapshots make review reversible. The course complements the existing Aral documentation and does not claim that reading or passing software checks establishes a learner's mastery.

Known limits include process-local queueing and the DAO's existing replacement semantics. The queue coordinates callers using this store instance; it is not a cross-process lock or a substitute for database constraints. Those distinctions should remain explicit in future fixes and reports.
''', store, '/** Boot hydration', 13)

write_course('46f416b83060', chapters, 'Follow event identity, queued persistence reconciliation, and clock-correction regression tests.')
B = Path(__file__).resolve().parent.parent
(B/'specs/46f416b83060.json').write_text(json.dumps(dict(changedFiles=[], summary=[
    'Deduplicated progress events before ordering with first-arrival payload semantics, preventing retry XP inflation.',
    'Serialized local records, remote merges, clock corrections and hydration; reconciled live state from persisted events after writes and partial failures.',
    'Added shared reducer and stateful store regressions, plus nine source-based guide chapters.'
], limits=[
    'Store tests use a Map-backed DAO fixture, not native device SQLite; native persistence durability and rollback are not established.',
    'Queue ordering is process-local and preserves the existing DAO replacement semantics.'
]), indent=2), encoding='utf-8')
