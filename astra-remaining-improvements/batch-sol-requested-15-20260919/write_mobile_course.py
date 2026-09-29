from pathlib import Path
import json
from course_writer import write_course

P = Path(__file__).resolve().parent.parent/'stage/1bf7dd59f47b'
chapters = {}
def add(name, title, body, file, anchor, count):
    chapters[name] = (title, body, [(file, anchor, count)])

add('README.md', 'Mobiletagalog: synchronize without losing local progress', '''
The mobile app combines a server progress baseline with a local outbox. A learner may complete another activity while an earlier batch is being synchronized. A safe response handler must acknowledge only the sent events, preserve newly added events, and publish the resulting baseline and remainder together. It must also reject a response belonging to a session that has already ended.

This course follows those requirements through ProgressSyncCoordinator, device persistence, and ProgressProvider. The coordinator serializes sync requests and associates each with an authentication generation. Device storage commits the returned baseline and acknowledged identifiers in one synchronous transaction. The provider rereads remaining events after that commit, so a closure captured before the network request cannot discard later work.

Begin with the map and concepts chapters, then trace the deferred-response examples. The tests use controlled promises for network interleavings and a mock SQLite adapter for transaction-contract assertions. They do not run an Expo device or certify native SQLite durability. The verification chapter retains that distinction alongside actual command results.

The change also handles authentication transitions. Guest events survive initial sign-in, but a direct switch between different signed-in users clears the previous account's progress. Logout invalidates in-flight responses. A delayed timezone profile update cannot restore old credentials or overwrite a refreshed access token. Each of these behaviors is part of keeping progress attached to the correct session.
''', 'src/lib/sync.ts', '/** Serial sync', 42)

add('01-CODEBASE-MAP.md', 'Map baseline, outbox, and authentication state', '''
storage.ts owns the device SQLite connection, key-value records, and outbox rows. commitSyncedProgress writes the server baseline and deletes only acknowledged identifiers inside withTransactionSync. outboxAdd preserves first-write-wins event identity through INSERT OR IGNORE. outboxAll provides the accepted local remainder used for display.

sync.ts contains the framework-independent coordinator. Its dependencies describe the boundaries needed for a sync attempt: read the outbox, push a batch, refresh credentials, commit acknowledgement, and publish tokens or progress. This interface makes delayed network responses testable without mounting the entire mobile app.

progress.tsx connects the coordinator to React and the actual API/storage functions. addEvents persists then rereads the outbox. syncNow delegates to the coordinator. adoptAuth distinguishes guest adoption from a true account switch; logout advances the session generation before clearing account state. The timezone effect captures a session snapshot and applies a returned user profile only if that snapshot still belongs to the active generation.

The core reducer combines the baseline and unsent events into visible progress. It does not decide whether a remote response is current. That decision belongs in the coordinator before storage mutation. When diagnosing a mismatch, inspect the sent batch, acknowledged IDs, active generation, and persisted remainder before changing the reducer. Each boundary answers a different question: what was sent, what was accepted, who owns the response, and what remains local.
''', 'src/lib/progress.tsx', '  const adoptAuth', 33)

add('02-CONCEPTS.md', 'A response belongs to a generation', '''
User identity alone is not a sufficient stale-response guard. A user can log out and later sign into the same account while an old request is still pending. The identifier matches again, but the old request belongs to a different session. The coordinator increments a generation on every setSession call and captures that generation when sync is requested.

Queued operations check the captured generation before reading the outbox or making a request. In-flight operations check again before committing a result. The refresh branch checks before requesting new credentials and after refresh completes. These checks prevent a late unauthorized response from initiating a refresh for an abandoned account and prevent returned credentials from restoring a logged-out session.

The acknowledgement boundary is narrower than clearing the outbox. Only identifiers present in the sent batch may be removed. A server response containing an unrelated identifier is intersected with that batch. Events added while the request was pending remain in storage and are included in the next derived view.

Profile updates have a related but distinct rule. A returned user profile may be current while its captured access token is outdated because refresh occurred in the meantime. applyUserUpdate checks the generation and account, then combines the returned user with the coordinator's current tokens. This preserves newer credentials instead of rebuilding authentication from an old closure. The tests exercise both logout rejection and refreshed-token preservation.
''', 'src/lib/sync.ts', '  applyUserUpdate(', 20)

add('03-WORKED-CHANGE.md', 'Commit the baseline with its acknowledgement', '''
Follow one sync attempt from queue to publication. The coordinator captures the active generation when sync is called, chains the operation after the previous attempt, and catches rejection only on its internal tail. The caller still receives the operation promise. A failed attempt therefore does not poison all future sync requests.

When the operation starts, it reads at most five hundred outbox events and sends that batch with the active credentials. A 401 can trigger one refresh if the generation is still current. Other failures propagate without pretending progress was committed. After a successful push, the final generation and user checks run before any local acknowledgement.

The returned identifiers are intersected with the sent batch. commitSyncedProgress writes the new baseline and deletes those identifiers in one SQLite transaction. Publishing reads the remaining outbox after the commit, so newly recorded events are preserved in the displayed state.

The provider's adoption and logout paths invalidate old work before replacing account data. Guest-to-account adoption keeps guest events for synchronization; account A to account B wipes A's baseline and outbox. The delayed timezone response goes through applyUserUpdate instead of assigning captured credentials directly. These changes address different races with the same ownership principle: asynchronous results may mutate local account state only while their issuing session remains active.
''', 'src/lib/sync.ts', '  private async runOnce', 31)

add('04-TESTING-AND-DEBUGGING.md', 'Make the late response deterministic', '''
The synchronization tests hold a push response on a promise, add an event while the request is pending, then release the response. The expected acknowledgement contains only the original sent identifier, while the new event remains in the outbox. This reproduces the race directly instead of relying on network timing or a fixed sleep.

A second test starts overlapping sync calls and tracks active requests. The maximum must remain one, and the queued pass must read the remainder after the earlier commit. Account-change tests replace the session before releasing a response and assert that no baseline or acknowledgement is committed. Another case rejects the stale push with 401 and verifies that refresh is never called.

Profile-update tests capture a session, log out, and attempt to apply a delayed user response. The result must be null. They then establish an active session, update its access token, and apply a profile response captured before that refresh. The new token must survive.

Storage tests use a mock Expo SQLite adapter to verify the transaction contract and rollback behavior modeled by that fixture. That is useful regression evidence, but a real device restart or native database failure needs its own verification. When debugging, distinguish a coordinator rejection, an API failure, and a storage commit failure; they occur at different points and support different conclusions about whether progress changed.
''', 'src/lib/sync.test.ts', '  it("serializes overlaps', 35)

add('05-PRACTICE.md', 'Exercises across the asynchronous boundary', '''
First, start with outbox A and a baseline of zero. Block the push, append event B, then acknowledge A. Predict the persisted baseline, remaining outbox, and the event list supplied to the derived-state calculation. Explain why publishing a captured copy of the original outbox is wrong.

Second, return acknowledgements for A and C even though only A was sent. Predict which identifiers the coordinator passes to commit. Describe a test that would fail if the sent-batch intersection were removed.

Third, issue a sync for account A, switch to account B, and then release A's successful response. Repeat with a 401 response instead. State which callbacks may run in each case, including refresh and onTokens. Do not treat matching user identifiers after a later re-login as proof that the original session is still valid.

Fourth, capture a timezone update, refresh the account's access token, and release the timezone response. Explain which user fields and credentials should survive. Then repeat with logout before the response and predict the result.

Finally, compare guest adoption with a direct signed-in account switch. Which path preserves pending guest activity, and which path clears the previous user's baseline and outbox? Write assertions at both the coordinator and provider boundaries. A pure adoption-mode test describes the decision; verifying the provider's actual clearing behavior is a separate integration concern.
''', 'src/lib/sync.test.ts', '  it("does not refresh a stale', 24)

add('06-SOLUTIONS-AND-REVIEW.md', 'Answers and review criteria', '''
After acknowledging A, the new server baseline is stored and B remains local. The publication callback receives a fresh read of the remainder. Clearing all outbox rows or publishing the pre-request array would lose B or make its display inconsistent with storage.

For an acknowledgement containing A and C, only A is passed to commit because the sent batch defines the permitted deletion set. The server response cannot authorize removal of an event this request never sent. The fake provider test should include an unrelated acknowledgement to protect that condition explicitly.

After account replacement, both the successful response and stale 401 are discarded before local mutation. The stale 401 must not call refresh. Generation checking also protects logout followed by login to the same user identifier, because identity equality alone would accept that abandoned request.

For a delayed timezone response within the active session, the returned user profile is combined with current credentials. A refreshed access token remains intact. After logout, applyUserUpdate returns null and the provider does not persist or publish the old authentication object.

Guest adoption preserves the outbox so local learning can be synchronized. A direct account switch clears the prior account's outbox and baseline. Review solutions for the ordering of session invalidation and clearing, and for transaction scope around baseline-plus-acknowledgement. Also inspect claims in reports: a mock SQLite contract test is not a native device durability test, and a fake provider does not prove the production server's acceptance semantics.
''', 'src/lib/sync.test.ts', '  it("rejects a delayed profile', 29)

add('07-TRACE-LAB.md', 'Trace A, B, and a logout', '''
Draw columns for the UI, coordinator, server, and device database. Begin with event A in the outbox and a sync request at generation zero. The coordinator reads A and waits for the server. While it waits, the UI records B and rereads the persisted outbox. The screen can now derive progress from A and B using the existing baseline.

Release the server response for A. The coordinator confirms generation zero, intersects acknowledgements with the sent batch, and commits the new baseline with deletion of A. It then rereads storage and publishes B as the remainder. A second queued sync starts only after that sequence, so its batch reflects current storage rather than the state at the time the second call was originally queued.

Restart the trace but insert logout before the response. setSession advances the generation and clears active credentials; account storage is wiped. The old response reaches the final guard and exits without commit. No baseline callback may restore A's progress. Repeat with a stale 401 to observe the earlier guard before refresh.

Finally, add a timezone request to the active-session trace and refresh credentials while it waits. The profile response may update the current user, but it must retain the newly refreshed access token. These timelines let you identify exactly which guard protects each callback and what state a failed assertion would implicate.
''', 'src/lib/progress.tsx', '  useEffect(() => {\n    if (!auth) return;', 19)

add('VERIFICATION.md', 'Verification and device boundaries', '''
The accepted command records below provide exact arguments, terminal results, and logs. They distinguish dependency setup from tests and type checking. A successful installation does not establish synchronization correctness; the deferred-response and storage-contract assertions supply that evidence at their stated boundaries.

The coordinator tests execute the actual framework-independent class with injected storage and provider functions. They control interleavings through promises rather than contacting the production service. The storage fixture models the Expo SQLite API used by commitSyncedProgress. It checks that baseline adoption and acknowledgement belong to one transaction, but it cannot verify the native implementation on Android or iOS.

The provider integration was reviewed for generation invalidation, account-switch clearing, fresh outbox reads, and guarded timezone updates. A device UI run remains a distinct verification activity and is not inferred from those source checks. Guest adoption behavior and direct account switching should be exercised together when such an environment is available.

Read the logs with the changed-source snapshots. Existing project material is preserved, while this course focuses on one progress synchronization contract. Future work may add device restart tests or server acceptance integration, but those claims require their own controlled environments. Do not run test cleanup against the user's original device database. The temporary test fixtures in this delivery use their own state and do not contact external accounts or providers.
''', 'src/lib/storage.ts', '/** Atomically adopt', 30)

write_course('1bf7dd59f47b', chapters, 'Trace session generations, acknowledged event batches, and baseline/outbox transaction boundaries.')
B = P.parent.parent
(B/'specs/1bf7dd59f47b.json').write_text(json.dumps(dict(changedFiles=[], summary=[
    'Added serial, generation-bound synchronization and atomic baseline plus sent-event acknowledgement.',
    'Preserved events recorded during in-flight sync; prevented late responses, stale refreshes and profile updates from restoring prior sessions.',
    'Distinguished guest adoption from signed-in account switching and added regression fixtures and source-based guides.'
], limits=[
    'Provider and Expo SQLite tests use controlled fixtures; no native-device durability or live server integration is claimed.',
    'Source review covers React provider wiring; pure coordinator tests do not constitute a complete device UI run.'
]), indent=2), encoding='utf-8')
