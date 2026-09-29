from pathlib import Path
b=Path(__file__).resolve().parent;s=b/'stage/b415b13a50ee';d=s/'astraupskill'
docs={
'04-TESTING-AND-DEBUGGING.md':'''# Choose evidence for the boundary you changed

Run `npm.cmd test` for the 39 Node cases. Six timer cases cover transitions, three original background cases preserve earlier behavior, eighteen model cases cover validation and CRUD rules, and twelve reliability cases inject worker failures. These tests do not require a personal Chrome profile. Read [model tests](../tests/model.test.js) before adding another rule: they show how to provide an explicit clock and construct a minimal valid snapshot.

Use `npm.cmd run test:browser` for ten Chromium scenarios after building. Playwright starts a strict-port preview server; an occupied test port fails instead of accidentally testing a different app. The suite covers timer controls, literal reminder persistence, library CRUD, two-tab conflicts, quota failure, corrupt-data recovery, artwork upload/removal, elapsed deadlines, layouts and a real unpacked extension. The extension case checks actual stored reminders, scheduled deadlines, popup creation and removal after snooze.

A successful UI assertion is strongest when paired with persisted evidence. For example, after a quota error the form should retain its text, the active reminder should remain unchanged and storage should still contain the old value. Checking only the toast would miss a bug that changes accepted state before the write. Similarly, a stale edit test needs both the rejected draft and the other tab's winning value.

To debug a save, classify its last successful boundary. Did validation run? Did the revision match? Did the initial storage write complete? Did alarm creation or popup reconciliation fail afterward? The worker's warning explicitly identifies the latter category. A failure before persistence must not create an alarm. A failure after persistence can leave data accepted while an effect needs repair. The reliability suite injects both cases rather than treating every exception as equivalent.

For a deterministic experiment, copy a reliability test and make `chrome.windows.create` fail once. Issue a break command, inspect the accepted break state and warning, then restore the fake API and read again. Exactly one live window should result. Another test fails saving its newly created window ID; the worker attempts to remove that orphan before later recovery. If both cleanup and persistence fail, the implementation cannot promise perfect cleanup.

Keep logs, the failing assertion and the smallest reproduction together. Do not add arbitrary sleeps to hide a race. Prefer awaiting the visible accepted state or querying the effect being asserted. [Verification](VERIFICATION.md) records the delivered evidence, including the distinction between simulated failures and actual extension integration. No test here proves all browser versions, operating-system fullscreen behavior, power-loss durability or accessibility conformance.
''',
'05-PRACTICE.md':'''# Practice toward a mid-level CRUD application

The following changes are exercises, not delivered features. Start each in a separate working branch or copy, preserve the existing tests and write acceptance criteria before implementation. Use synthetic reminders and a disposable browser profile. Finish a small vertical change before attempting a server rewrite.

## 1. Search the saved-message library

Add a labeled search field that filters cards by title and message without modifying stored data. For example, Water and Walk should both match `wa`, while `sip` matches only Water's text. Decide how whitespace and case are handled. Clearing the query restores every card. An empty result should explain that no reminders match, not claim the library is empty. Evidence: model or small pure-filter tests plus one browser scenario proving that clearing the search restores a hidden card after reload-independent filtering.

## 2. Duplicate a reminder safely

Add Duplicate to each card. Copy the text, choose a new UUID and propose a distinct title in the editor. Require the learner to save rather than silently adding a record. The thirty-entry limit still applies at acceptance time; two tabs cannot bypass it by both seeing twenty-nine records. Evidence: canceled duplication creates nothing, the new item has another identity, editing the copy preserves the original, and a stale save keeps its proposal.

## 3. Improve conflict recovery

Show the current server-equivalent snapshot beside the preserved draft after a conflict. Let the user choose which text to keep and explicitly submit a new command against the freshly displayed revision. Do not automatically change `expectedRevision` and retry. Acceptance: another intervening edit can cause a second conflict without losing either proposal. Include a test where the selected record was deleted elsewhere, since merging an update into a missing identity needs a product decision.

## 4. Design a local HTTP and SQL version

Move reminders into a small service with collection and item routes. Propose tables for reminders and owner settings, row versions, bounded text checks and a migration from browser exports. Describe response bodies and status codes for invalid data, missing IDs and stale versions. Implement transactions around constraints spanning several rows. Keep the timer's clock-driven model separate from transport. Evidence must include real database integration tests for two competing updates and an update after deletion; an in-memory mock cannot demonstrate SQL concurrency.

## 5. Add ownership and a reliable job boundary

Only after the local service works, derive the owner from authenticated server context. Test that one owner cannot read or mutate another owner's reminders even with a known ID. If server-side notifications are added, commit an outbox item with the relevant database change, then deliver with a stable event identity. Explain duplicate delivery and retry policy. This is a larger capstone: do not describe it as a small validation patch or assume Chrome's local worker queue supplies those guarantees.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Review your decisions after the exercises

A good search solution computes visible reminders from the accepted library and query, leaving the stored array untouched. A common mistake is assigning filtered results back to `presets`; the next save can then erase hidden entries. Another mistake is inserting highlighted user text with `innerHTML`. Build text nodes or keep highlighting out of the first implementation. The browser test should search, clear and verify both original identities still exist in storage.

Duplication should create a new identity at the point a new draft is prepared. A copied array reference is not enough: the copied reminder must remain independent when edited. The save still goes through `applyMessage`, where the latest library length and revision are checked. A button disabled at thirty entries is useful feedback but is not the constraint. Review a boundary case in which another tab creates the thirtieth item after your draft begins.

For conflict recovery, distinguish refreshing the accepted snapshot from replacing the user's draft. Display both, capture the displayed revision, and let the user deliberately construct a new proposal. If the reminder was deleted, present an explicit create-as-new action with a new ID or let the user discard the draft. Quietly converting every failed update into a create can resurrect deliberately removed data. A second conflict during review should remain possible and understandable.

A SQL implementation might update one row with a condition on identity, owner and expected version. A zero-row result needs a deliberate response policy: distinguish missing from stale only when doing so does not reveal another owner's data. Unique constraints protect identity independently of the HTTP validator. For a per-owner library limit, checking `COUNT(*)` outside a transaction can race; design an owner-row lock or another database-enforced allocation mechanism before claiming the limit is safe.

A reviewable migration reads and validates the entire export, presents a summary and commits all accepted rows atomically or clearly reports a partial-import policy. Preserve original IDs only if they fit the new ownership model. Uploaded images require separate size and content handling; a browser data URL should not automatically become an unlimited database field or public URL. The current export feature does not implement this import.

Use this review checklist in prose when presenting your change: explain the user-visible result, identify the data invariant, locate the acceptance boundary, show a failure case and state the remaining limit. For the delivered project, the boundary is local persistence and subsequent Chrome-effect reconciliation. For your server capstone, it may be a SQL commit followed by an outbox worker. The names of the layers matter less than proving that the response describes what was actually accepted. [The trace lab](07-TRACE-LAB.md) provides concrete examples you can use as a baseline review demonstration.
''',
'07-TRACE-LAB.md':'''# Trace a stale edit and a repaired break

Use an isolated preview origin and open two tabs, A and B. In both, enter My message. In A, create Water and wait for the saved card. Refresh B and choose Edit Water in both tabs. Write Accepted in A and Proposal in B. Before saving, predict the result and inspect each editor's captured revision in the debugger. The displayed timer can refresh while those editor revisions remain unchanged.

Save A, then B. Record the stored revision and reminder text after each operation. B should show a conflict and retain Proposal in the field. Storage should contain Accepted. Copy B's text somewhere temporary, reopen the message view and observe that the library editor clears. This explicit refresh behavior is why preserving a failed draft and preserving a draft across navigation are different promises. Make a deliberate new edit if you want to apply Proposal against the current revision.

Now inspect [src/app.js](../src/app.js) at `saveSettings` and the preset handler. Write down which variables represent accepted data, which represent draft metadata, and where the asynchronous persistence call returns. Trigger a quota failure through the isolated Playwright test rather than filling your personal browser's storage. The expected path throws before accepted UI assignment. Compare that with a normal save to understand why a try/catch alone is insufficient if state is mutated too early.

For the worker experiment, open [worker reliability tests](../tests/worker-reliability.test.js). Find the case that rejects alarm creation once. Follow this sequence on paper: read snapshot, apply start, persist running deadline, fail alarm creation, return accepted data with warning, read again, inspect missing alarm, create it. The second read must preserve the original deadline. Resetting the deadline during repair would make infrastructure failure extend a focus session accidentally.

Repeat with break-window creation. A successful popup creation followed by a failed ID write is a different failure from creation itself failing. The implementation attempts to remove the newly created orphan. The test then restores the API and observes a later successful repair. Explain which operations are durable and which are only best-effort cleanup. There is no transaction that rolls back Chrome storage, alarms and windows together.

Finally run the unpacked-extension browser case. It starts a fresh Chromium profile, creates a library entry, reloads, starts focus, checks the real alarm deadline, enters a break and snoozes. Compare its evidence with the fake worker tests: integration proves that these actual APIs cooperate in the tested runtime, while injected failures make otherwise rare branches deterministic. Submit a short trace table with operation, revision, stored phase, external effect and visible response for each step. That artifact is more useful than a screenshot of a passing test count alone.
''',
'VERIFICATION.md':'''# Delivered evidence and practical limits

The implementation was verified in an isolated copy using Node 22.16.0, Playwright 1.60.0 and Chromium 148. The source bundle built successfully. All 39 Node tests passed: six timer tests, three existing background tests, eighteen shared-model tests and twelve worker-reliability tests. All ten Chromium scenarios passed without retries or skips. One scenario loaded the actual unpacked extension in a new persistent test profile and checked Chrome storage, an alarm deadline and popup lifecycle.

The browser scenarios also checked timer controls, persistence after reload, reusable-message CRUD, independent active reminders, stale edits across two tabs, storage quota rejection, literal text rendering, corrupt preview export and confirmed replacement, art upload/removal, elapsed focus behavior and narrow/desktop layouts. Four screenshots were inspected; the saved-message textarea was subsequently widened and the affected layout scenario rerun. See the [desktop dashboard](images/dashboard-desktop.png), [desktop messages](images/messages-desktop.png), [narrow dashboard](images/dashboard-narrow.png) and [narrow messages](images/messages-narrow.png). Screenshots demonstrate the captured layouts, not a complete accessibility or cross-device certification.

The extension archive was regenerated from the delivered extension directory, and each archive member was checked against its corresponding file. The generated UI bundle is included so Load unpacked does not require Node at runtime. Development still requires rebuilding after source edits. Test logs and a machine-readable result are retained in the parent workspace's implementation evidence; the central report links this project's delivered learning folder and records the finite file manifest.

No personal extension profile, live account or existing browser storage was used. Model and worker fault tests use simulated Chrome APIs; the one unpacked integration scenario uses real APIs but does not simulate operating-system sleep, browser crashes, power loss or all Chrome releases. The preview stores data under its own origin and is separate from extension storage. Changing the preview port changes the origin and therefore the visible saved data.

This remains a local app with no server database, authentication, multi-user access control or durable distributed outbox. Worker serialization covers cooperating messages in that worker. Preview Web Locks cover cooperating tabs at the same origin. Direct storage writers can bypass the protocol. Alarms can run late; a repaired alarm or break window does not imply exact real-time execution. If popup cleanup itself fails after an ID-save failure, orphan cleanup is best effort. Raw export aids recovery but no general import or extension reset UI was added. The SQL, ownership and outbox work in [practice](05-PRACTICE.md) is proposed follow-on learning, not functionality counted as delivered.
'''}
for name,content in docs.items():(d/name).write_text(content,encoding='utf-8')
print({name:len(content.split()) for name,content in docs.items()})
