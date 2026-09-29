from pathlib import Path
s=Path('astra-remaining-improvements/stage/6844a7b03c83')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('astraupskill/03-WORKED-CHANGE.md',r'''
# Worked change: preserve a draft when persistence fails

The earlier editor changed the shared question array before calling localStorage.setItem. If storage was full or unavailable, the visible in-memory state had already changed. The save handler could also close the editor as though the operation succeeded. This walkthrough follows the delivered candidate-state approach in [edit.js](../edit.js), [main.js](../main.js) and [store.js](../store.js).

When the editor opens, it copies the currently accepted board with structuredClone and remembers the exact stored text as its baseline. Form input changes this local draft. It does not change the board displayed behind the modal. Adding a category or deleting a question also affects only the draft. Cancel simply closes the modal; the next opening starts from the accepted state again.

Submission first benefits from native required-field checks, then calls the store's full structural validation. The store checks stable IDs, supported counts, nonempty text, point values and used-clue references. Browser form validation improves feedback but is not the authoritative rule: imports and direct module callers also go through the same store validator.

The save acquires a named Web Lock. Inside the lock, it rereads storage and compares it with the editor's baseline. A mismatch reports that another tab changed the board. If the baseline still matches, it computes the next revision from saved state, serializes the normalized candidate and performs setItem. Only after that call succeeds does the store return an accepted snapshot. The controller then replaces current state, rerenders the board, reports success and allows the editor to close.

## Follow a failure

Imagine the learner renames a category to “CRUD practice” and storage throws a quota error. The store throws a readable failure without returning a committed snapshot. The controller reports it inside the editor and leaves the draft open. The old category name remains on the accepted board. The learner can correct the situation or copy the proposal; a reload does not falsely promise that the failed edit was saved.

Now imagine a second tab marks a clue used while the first tab's editor is open. A storage event refreshes the accepted board but leaves the open draft intact. Saving that old draft still uses its original baseline and therefore conflicts. Replacing the baseline automatically would let old used-marker state overwrite the newer round. The explicit recovery is to cancel, reload and reapply intended edits against current data.

The Node tests inject quota failure and serialize competing saves through a controlled lock boundary. Browser tests additionally override the real Storage method, inspect the retained form, and run two tabs through the actual Web Locks API. These layers establish different claims. Neither proves coordination with a script that ignores the lock or persistence after browser data is cleared.
''')
w('astraupskill/04-TESTING-AND-DEBUGGING.md',r'''
# Verify the real state boundary

Run `npm test` for the 20 Node cases and `npm run test:browser` for the Chromium workflows after installing the matching Playwright browser. The [configuration](../playwright.config.js) launches an isolated loopback static server and refuses to reuse an existing listener. Browser tests use new contexts, so personal browser storage is not a fixture and is not cleared.

The [store suite](../test/store.test.js) tests missing data, deterministic legacy migration, invalid JSON, schema versions, IDs, required fields, bounds, used-clue references and empty boards. Persistence cases assert new revision behavior, stale baseline rejection, quota failure, missing Web Locks, explicit corruption replacement and exhausted revisions. Delete cases verify that round-progress references are cleaned without modifying the input snapshot.

The controlled lock in Node serializes callbacks so races can be tested deterministically. It is useful for store logic, but it is not proof that the browser's lock implementation coordinates tabs. The [browser suite](../e2e/board.spec.js) therefore opens two pages in one context, lets both capture the same saved baseline, then starts their saves together. Exactly one succeeds. Another UI case preserves an older open form after a competing tab has saved.

Browser workflows also test category/question CRUD through labeled controls, reload, cancelled editing and deletion, quota failure, corrupt-data preservation, explicit replacement, literal rendering of markup-like text, import/export and new-round behavior. A clue is not consumed merely by opening and closing its dialog. Keyboard Escape dismisses an idle native dialog and returns focus. Desktop and narrow checks capture screenshots and reject document-wide horizontal overflow.

The static-server case checks that only application assets are served, including a successful HEAD request with no body. Repository files such as package metadata, server source and environment paths are not part of the asset allowlist. Response headers supply a content type, nosniff and a restrictive content security policy. This is a local static server, not a general-purpose production hosting service.

When debugging a failed save, ask three questions in order: did validation accept the candidate, did the stored baseline still match, and did setItem succeed? Inspect the editor error instead of assuming any open dialog means a broken click handler. For a missing saved board, compare protocol, hostname and port; changing localhost to 127.0.0.1 changes the origin and its storage.

A passing local suite does not establish authenticated ownership, remote persistence, full accessibility compliance or power-loss durability. Keep [verification](VERIFICATION.md) beside any claims you make about the project.
''')
w('astraupskill/05-PRACTICE.md',r'''
# Exercises toward a server-backed CRUD app

These are proposed extensions. Build on the delivered local workflow and keep each change small enough to review with its test. Start by stating which state belongs to a draft, a saved resource or a derived display value.

## 1. Add search in the editor

Filter questions by prompt or answer while preserving stable IDs and category context. Editing a filtered result must update the intended question, not the record currently occupying an array index. Test two questions with similar text, deleting an earlier question and clearing the filter. Decide how unsaved changes affect search results, and avoid replacing the draft merely because the filter changes.

## 2. Add players and explicit scoring

The current point values do not represent a score ledger. Introduce players and a record of awarded or deducted points for a clue. Define whether a clue may be scored more than once and how undo works. Derive totals from scoring records instead of independently updating a displayed total and history array. Test a corrected award, a deleted question and a new round. Decide whether a historical score refers to an immutable clue snapshot.

## 3. Move the question bank behind HTTP

Create a server with category and question CRUD endpoints. Return readable resource identities after creation, clear errors for invalid input and conflicts for stale updates. Keep the existing store interface or an adapter so the editor can preserve its draft on failed requests. Add an actual HTTP test before connecting the browser. A network response may arrive after the user closes and reopens an editor; use a session or request identity to prevent stale completion from closing the wrong draft.

## 4. Introduce SQL relationships and per-record versions

Model categories, questions and rounds explicitly. Add foreign keys, unique IDs and a version column on editable resources. Deleting a category and its related questions must follow an intentional cascade or restriction policy. A transaction should also handle any associated round references. Test two users editing different questions successfully and two users editing the same version with one winner. Compare that behavior with the current whole-board conflict policy.

## 5. Separate teacher and learner access

Add authenticated teacher ownership and a learner-facing quiz view. The browser currently receives every answer, so hiding a paragraph is not a security boundary. Design separate response models if answers must remain server-side until reveal or scoring. Test copied resource IDs across teachers, unauthorized imports and attempts to edit a question through the learner role. Derive identity from the server's trusted authentication context.

## 6. Add migration and recovery tooling

Design an import preview with counts, validation errors and a downloadable backup of the existing board. Test legacy migration on disposable copies. Add a database backup/restore exercise once the server exists. Keep the distinction between a successful save response, a durable backup and a user-visible recovery workflow. Finish with a short release note stating the tested environment and the remaining storage and access assumptions.
''')
w('astraupskill/06-SOLUTIONS-AND-REVIEW.md',r'''
# Review the invariant, not the framework choice

Use these notes after attempting [practice](05-PRACTICE.md). The current implementation uses plain modules, but the same review questions apply if you later introduce React or a server framework. A framework does not decide which state is authoritative or when a command is safe to call successful.

For filtered editing, keep the draft's canonical collection separate from the visible filtered projection. Event handlers should carry category and question IDs. A deletion should find the record by identity, not by the filtered list's index. Test a filter that hides the first question, then update the visible second one and confirm that the hidden record remains unchanged. Decide whether filter text itself belongs in persistent board data; it usually represents local UI state.

For scoring, model an award as an explicit record with player, clue, round, amount and identity. Derive totals from accepted records. Undo can append a reversal or remove a draft award according to the audit requirements you choose. Do not let both the score total and history mutate independently. A double-click or repeated network request must not award the same event twice. That introduces a useful idempotency exercise once scoring moves behind HTTP.

For the HTTP adapter, preserve the current promise that a failed save leaves the draft open. Parse non-success responses before treating their bodies as data, and handle 204 without JSON parsing. Carry an expected resource version with updates. A request completing for an old editor session should not replace a newer proposal or close its dialog. Test delayed responses and explicit cancellation, not only immediate success.

For SQL persistence, put related writes inside the same transaction and use conditional updates at the write boundary. A transaction around an unconditional update still permits a stale editor to overwrite newer values. Define category-deletion policy and test it with active round references. If historical rounds must remain explainable after question edits, store the relevant prompt/answer snapshot or prohibit destructive changes to referenced records.

For access control, the owner comes from authenticated server identity. A hidden answer element or disabled edit button is only presentation. Learner responses should omit protected fields, and every mutation route must check authorization independently. Test users who know each other's IDs and nested question references. Keep authorization errors consistent with the resource-disclosure policy you select.

For migration and recovery, validate the complete input before writing any replacement. Preserve an existing backup until a restore has actually been verified. A successful import should report what changed and which format version was accepted. During review, ask the author to reproduce one stale save, one storage failure and one incomplete import. The strongest explanation connects each failure to a specific boundary and its test evidence.
''')
w('astraupskill/07-TRACE-LAB.md',r'''
# Trace one edit through two browser tabs

Start the local server at its ordinary loopback URL and open a disposable browser profile or context if you want to keep existing learning data separate. Do not clear a personal browser's site data as a testing shortcut. The automated browser suite already creates isolated contexts for this purpose.

Begin by opening and closing a clue without marking it used. Confirm that the tile remains available. Open it again, reveal the answer and mark it used. Inspect localStorage under `customJeopardy`: the saved object includes schemaVersion, revision, categories and usedQuestionIds. The used marker refers to a question ID rather than its position in the displayed board. Reload and compare the progress count.

Open Edit question bank. Change a category name, but do not save yet. Inspect the board behind the dialog and the stored JSON. Both still contain the accepted name; the proposal lives only in the editor's draft. Save and inspect the revision increment. Explain why an imported revision of 999 would not control the next revision: the store derives it from current saved state.

Now open a second tab on the exact same origin. Open editors in both tabs. Save a name change in the first while retaining a different proposal in the second. The second receives a storage event, refreshes its accepted board and preserves the draft. Its later Save bank uses the baseline captured at editor opening and conflicts. Cancel, reload and deliberately reapply the intended change. Do not merely replace the baseline token on the old draft.

Export the board and inspect the downloaded JSON. Copy it, change one category name to literal markup-like text and import the copy. The name should render as text, not create an element. Then make a malformed copy and attempt import again. Validation must fail before the saved board is replaced. Keep your valid export for recovery rather than editing the only copy you own.

Read the quota-failure browser test. It makes setItem throw, submits a changed category and checks that the editor retains the proposal while storage remains unchanged. Compare that result with a stale-save failure: one means the persistence medium rejected the write; the other means the proposal was based on old data. Their recovery paths differ.

Write a trace table covering input collection, draft change, validation, lock acquisition, baseline comparison, storage write, accepted-state publication and render. Mark which steps can fail and what the user sees. Finish by mapping those stages to a future form component, API route, service and SQL transaction. The current static server serves assets only; those data-service layers remain future work.
''')
w('astraupskill/VERIFICATION.md',r'''
# Verification and practical limits

The final gate runs 20 Node storage/domain cases, eleven Chromium scenarios and six JavaScript syntax checks. Results are recorded in the central implementation workspace with TAP output, browser JSON and screenshots. The project exposes `npm test` and `npm run test:browser` so the learner can reproduce the corresponding suites. The tested environment uses Node 22.16.0 and Playwright 1.60.0 with its matching Chromium build.

Node cases exercise actual validation and migration functions plus controlled storage and lock boundaries. They verify detached defaults, deterministic legacy IDs, malformed input, unknown fields, unique identity, bounded points and collections, valid used-clue references, revision derivation, stale saves, quota errors, unavailable storage, explicit corrupt replacement, deletion cleanup and empty banks. These cases establish the store's behavior without depending on browser UI timing.

Chromium scenarios exercise the real application modules and localStorage. They cover category/question CRUD and reload, cancelled edits and deletes, clue reveal and accepted use, new rounds, retained drafts after quota failure, stale forms in another tab, actual simultaneous Web Locks saves, corrupt-data preservation and explicit replacement, import/export and literal rendering of markup-like names. Layout checks inspect desktop and narrow widths, capture screenshots and exercise keyboard dialog dismissal with focus return. The static-server scenario verifies its asset allowlist, response headers and HEAD behavior.

The first browser run passed ten scenarios. The final recorded run includes the additional server-boundary case. Browser contexts are isolated test data; no personal browser profile or existing localStorage was used. The local server refuses to reuse an existing listener. Dependency installation used the checked-in lockfile outcome, and the application runtime itself requires only built-in browser APIs.

The supplied example question content was retained. Existing legacy saved arrays are read and migrated in memory, then converted on the next successful save. That migration is not a live rewrite performed during this improvement pass. Corrupt saved text remains untouched until the app user explicitly confirms replacement, and its current raw baseline must still match. Export offers a recovery copy but is not an automated backup schedule.

Limits remain: no server-side database, authentication, remote classroom sharing, player scoring history, automatic answer secrecy, full accessibility certification, crash-recovery or power-loss guarantee. Web Locks coordinate cooperating tabs on the same origin; code that bypasses the protocol can still change storage. Browser storage can be cleared or unavailable, and changing protocol, hostname or port changes the origin. The asset server is for local learning, with no production deployment claim. These boundaries are the starting point for the HTTP, SQL and ownership exercises, not hidden unfinished features.
''')
print('All nine quiz board learning documents written')
