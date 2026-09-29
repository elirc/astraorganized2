from pathlib import Path
s=Path('astra-remaining-improvements/stage/a9672affc47e');d=s/'astraupskill';d.mkdir(exist_ok=True)
docs={
'README.md':'''# SkillForge Quest: build reliable CRUD from a learning journal

This course uses the application you are running as the worked example. SkillForge has 334 archived missions, but reading those missions alone does not demonstrate that you can maintain a web application. Here you will follow one feature through forms, domain rules, browser persistence, concurrency, failure recovery, and tests. The feature is a mission-linked learning journal. You can create notes, list and search them, edit their contents without changing their identity, and delete them after confirmation.

Start with Node 22 or newer, then run `npm ci` and `npm run dev` from this project folder. Open the URL printed by Vite. Create a callsign, open **Loadout & saves**, and create a note titled “Why a draft is not a saved record.” In its body, describe what should happen when storage fails. Reload the page and verify that the note survives. Export a backup before experimenting with resets or imports.

## Suggested learning sequence

1. Read [the codebase map](01-CODEBASE-MAP.md), then locate the component, pure domain operation, schema validator, and storage adapter yourself. Explain why each owns a different decision.
2. Work through [the concepts](02-CONCEPTS.md). Draw two tabs reading revision 3 and trying to save revision 4. Predict which proposal must be rejected.
3. Follow [the worked change](03-WORKED-CHANGE.md), changing one note and observing the returned accepted revision. A successful button click is insufficient evidence; inspect the durable value and reload.
4. Run [the debugging checks](04-TESTING-AND-DEBUGGING.md), including a storage quota failure and competing edits. Record the expected state before pressing Save.
5. Complete [the practice tasks](05-PRACTICE.md) before reading [the review guidance](06-SOLUTIONS-AND-REVIEW.md). Finish with [the trace lab](07-TRACE-LAB.md).

Allow several focused sessions. A useful session produces a small diff, a reproducible check, and a short explanation of one tradeoff. For example, “I kept the old accepted record after a failed write because displaying the candidate as saved would mislead the learner.” That explanation is stronger than “I added error handling.”

The current application is a local learning tool. It has no authenticated server, SQL database, shared team workspace, or protected grading service. Mission gates accept self-reported reasoning of a minimum length. They do not establish correctness or prevent cheating. The scratch worker isolates execution from the main UI thread and stops long runs; it is not a security sandbox. Use these limits to identify the next design questions, not to claim production readiness. [Verification](VERIFICATION.md) separates executed checks from future practice.
''',
'01-CODEBASE-MAP.md':'''# Follow the data, not only the folders

The main entry is [App.tsx](../src/App.tsx). It loads the static catalog, reads browser progress, chooses the visible screen, and owns the accepted `GameProgress`. Its `commitProgress` function coordinates saving. Components propose a new value; they receive the accepted value only after persistence succeeds. This is the most useful starting point when investigating a report such as “my note vanished after refreshing.”

[LearningNotes.tsx](../src/components/LearningNotes.tsx) owns the note editor. Opening an editor captures the accepted progress as `base`. The title, body, and linked mission then change independently. Search and pagination operate on accepted notes, so an unsubmitted title does not silently appear as a saved card. The list shows twenty records per page and sorts by update time, then stable identifier. Deletion requires confirmation, while a failed save keeps the editor open.

[notes.ts](../src/game/notes.ts) contains pure create, update, and delete operations. “Pure” means the operation returns a candidate without writing storage or mutating its input. Creation checks identity uniqueness. Updating locates the existing identity rather than deleting and recreating the record. Deletion rejects a missing record. Each operation passes its candidate through the same normalization boundary used by imports.

[schema.ts](../src/game/schema.ts) validates unknown external values. A TypeScript interface disappears at runtime; a JSON import can still contain negative XP, repeated identities, a note with no title, or an unknown mission. Structural normalization checks shape and bounds. `validateAgainstCatalog` then checks relationships against the shipped curriculum, including prerequisites and completed gates. These are separate questions: “is this field a string?” and “does this mission actually exist?”

[storage.ts](../src/game/storage.ts) owns the browser boundary. It reads the original key, coordinates cooperating tabs with Web Locks, compares revision and epoch, writes once, and returns the accepted snapshot. [SavePanel.tsx](../src/components/SavePanel.tsx) exposes recovery actions without automatically replacing damaged data. [engine.ts](../src/game/engine.ts) owns mission completion, XP, unlocks, and spaced review scheduling. [lab.ts](../src/game/lab.ts) owns worker execution and cleanup.

The files in `public/content/` are the preserved curriculum archive. Application improvements do not require rewriting those embedded source files. `scripts/verify-content.mjs` verifies the archive hashes and relationships. Unit tests live beside the game modules; [browser tests](../tests/learning.spec.ts) cross the React and browser boundaries. When changing behavior, identify the smallest owner of the rule first, then find the test that can observe its consequence.
''',
'02-CONCEPTS.md':'''# Five concepts behind trustworthy local CRUD

## Accepted state and draft state

Suppose a saved note says “Validate on the server,” while its editor says “Validate on both client and server.” The second sentence is a proposal. Until storage accepts it, the card and exported accepted progress should still describe the first sentence. This distinction matters when quota is exhausted, another tab has changed the record, or validation rejects the proposal. In this application, note fields and mission responses stay local until an explicit save or checkpoint submission.

```ts
const candidate = updateNote(base, { id, missionId, title, body });
const accepted = await persistProgress(candidate);
// Adopt accepted only after the awaited write succeeds.
```

This abbreviated example omits the catalog validation performed by `App.commitProgress`. In a server application, replace `persistProgress` with a request that returns the committed server representation. Do not assign a new version yourself and call that a successful database update.

## Identity and optimistic concurrency

An identifier answers “which note?” A revision answers “which accepted snapshot did this editor read?” Two tabs can hold the same note identifier and different revisions. SkillForge uses a revision for the entire progress document, so unrelated edits can conflict. This is deliberately simpler than merging notes independently. Web Locks serialize the read-compare-write sequence between cooperating tabs. A lock without a version check would merely serialize two overwrites; a version check without coordination could let both writers observe the same old revision.

An epoch identifies a reset generation. Resetting revision 9 to revision 0 alone could eventually make an old revision-1 tab appear current again. Reset creates a new epoch, so an old-generation proposal remains stale even when its numeric revision matches.

## Runtime boundaries and relationships

JSON is untrusted input even when it came from your own export yesterday. The schema rejects unknown properties, invalid counts, excessive sizes, and inconsistent review records. The catalog check rejects unknown missions and impossible completion relationships. Maximum lengths protect both usability and storage. A four-mebibyte serialized limit is checked in UTF-8 bytes; character count alone differs for emoji and other multibyte text.

## Failure is a state transition

A quota error should produce an unchanged accepted record, a retained candidate, and a visible explanation. It should not become a success toast followed by lost data. Exporting pending data gives the learner an escape route before reloading current progress. Corrupt original data is preserved and can be exported raw before a confirmed reset.

## Transfer to a CRUD API

A SQL equivalent can use `UPDATE notes SET body = ?, version = version + 1 WHERE id = ? AND version = ?`. Zero affected rows requires distinguishing a missing record from a conflict according to your API contract. Authorization must constrain the same query by owner or tenant. Browser revisions teach concurrency, but they provide no authorization: a user can edit their own local storage directly.
''',
'03-WORKED-CHANGE.md':'''# Worked change: update a learning note without losing an edit

Imagine two tabs opened the same learning journal at revision 4. Tab A changes a title to “Atomic audit writes.” Tab B changes the body to explain a rollback. The required behavior is that one accepted save advances the document, while the stale editor keeps its text and asks the learner to reconcile. Automatically merging these whole documents would risk losing mission progress, review scheduling, or other notes.

First open [LearningNotes.tsx](../src/components/LearningNotes.tsx) and find `open`. It captures `progress` as the editor base. This is important: using the newest parent snapshot at submission time could disguise that the user edited an older record. The form fields change independently of that base. React renders text as text; note bodies are not injected as HTML.

Next follow `save` into [updateNote](../src/game/notes.ts). It creates a new collection containing the changed record and keeps the identifier stable. Missing identifiers are rejected. The operation refreshes `updatedAt`, validates the candidate, and leaves the original object untouched. In a debugger, keep references to both objects and compare their bodies after the function returns.

The parent then validates the candidate against the catalog and calls `persistProgress`. Under the Web Lock, the storage adapter reads the current saved document. If Tab A already saved, the current revision is 5 while Tab B still proposes revision 4. The adapter throws before calling `setItem`. Tab B does not close its editor, does not change its accepted list, and exposes **Export pending draft**. Export that draft before choosing **Load current progress**, because loading explicitly discards open drafts.

For the winning tab, storage creates the next revision, serializes the bounded document, and calls `setItem`. Only a successful call returns the accepted snapshot. The parent adopts it, and the editor closes. The distinction is observable: replace `Storage.prototype.setItem` with a function that throws in a disposable test page, then submit. The same candidate must remain recoverable and the original saved value must remain identical.

Now implement a small extension yourself: add a `summary` field limited to 200 characters. Change the type, schema, form, card, import compatibility rule, and tests. Decide whether old saves default the field to an empty string. Test a legacy save, exactly 200 characters, 201 characters, and a stale update containing a valid summary. Do not merely add an HTML `maxLength`; imported JSON bypasses that control. Explain why the schema is the authoritative boundary even though the form helps users avoid invalid input.
''',
'04-TESTING-AND-DEBUGGING.md':'''# Test observable outcomes across the save boundary

Run the model checks with `npm test`. These tests exercise pure progression rules and injected storage/lock adapters. They include malformed saves, legacy defaults, conflicting proposals, quota failures, reset generation changes, note operations, and catalog relationships. Injection makes a difficult failure deterministic: a fake `setItem` can throw every time without actually filling your browser profile.

Run `npm run build` to check TypeScript and production bundling. Compilation does not prove that a delete confirmation works or that a second tab preserves its draft. For those behaviors, install the Playwright Chromium runtime once with `npx playwright install chromium`, then run `npm run test:browser`. The configured server binds loopback port 4287 with strict port selection; it refuses to reuse an unrelated existing server. Tests create isolated browser contexts rather than modifying your ordinary profile.

The browser suite covers onboarding, note CRUD and identity, search, reload persistence, confirmed deletion, competing tabs, pending exports, quota failures, corrupt-data recovery, mission drafts, import replacement, fetch retries, worker assertions and timeouts, and narrow layouts. Download assertions read the actual downloaded bytes. This catches a recovery button that appears functional but exports the wrong snapshot.

## A reproducible conflict investigation

1. Create a note and open the same app URL in a second tab.
2. Begin an edit in each tab before saving either one.
3. Save Tab A, then save Tab B. Expect a conflict in B and unchanged accepted storage.
4. Export B's pending draft. Inspect its title and revision in a text editor.
5. Load current progress in B after confirming the discard. Reapply the intended edit against the new snapshot.

Write down all three representations: A's accepted value, B's draft, and the actual storage value. “The UI looks stale” is too vague to diagnose which boundary failed.

## Other useful fault experiments

Block `/content/catalog.json` in a disposable browser session and verify that Retry catalog works after restoring the response. Block one mission archive and verify Retry mission independently. Run `console.assert(false, "edge case")` in the scratch lab: the result must say ERROR. Run `while(true){}`: the worker must stop after its timeout rather than freezing the page. Log a thousand lines and confirm that output is bounded.

Finally run `npm run verify:content`. It recomputes archive evidence for all 334 missions and 1,839 preserved source files. This protects historical teaching content while the application around it changes. Record exact commands and outcomes; do not describe an unrun browser, deployment, or security audit as verified.
''',
'05-PRACTICE.md':'''# Practice toward mid-level CRUD development

Complete these tasks in order. Keep each change small enough to explain in a code review. Before coding, write the expected success state and at least one failure state. The current implementation is a reference for local boundaries, not a completed backend architecture.

## 1. Improve journal navigation

Add a mission filter beside the text search. Filtering should combine both conditions, reset the displayed page when the filter changes, and show an informative empty state. Test a note that matches the text but belongs to a different mission. Then delete the last note on the final page and verify that pagination stays valid. This exercise teaches derived state and collection boundaries without introducing a server.

## 2. Add an explicit archive operation

Design `archivedAt` for notes. Existing saves should load without the field. Decide whether archived notes appear in search by default and whether editing restores them. Add Restore as a separate action. Preserve note identity and use the existing revision boundary. Verify that an archive operation from a stale editor cannot overwrite another tab's edit. Explain why archive and delete have different user expectations.

## 3. Implement an HTTP note repository

Create a separate practice backend and substitute an adapter behind the UI. Define request and response DTOs for create, list, update, and delete. Include a stable identifier and version in returned records. Use appropriate success statuses and documented validation, missing-record, and conflict responses. Keep the editor open when a request fails. Add an abortable list request so a slow older search cannot replace newer results. Do not hard-code success data into the component.

## 4. Move invariants into SQL transactions

Create users, notes, and note audit tables. An update must change the note and insert an audit row in one transaction. Inject an audit insertion failure and prove that the note remains unchanged. Use a conditional version update and run two competing requests against the same row. Assert one winner and one conflict, not merely two HTTP responses. Add a uniqueness constraint where the business rule actually requires uniqueness; note titles need not be unique just because identifiers are.

## 5. Add ownership and operational evidence

Introduce authenticated users using a deliberate learning setup. Every read and write must constrain ownership server-side. Try another user's identifier and prove that the API does not leak the record. Add request identifiers and structured error logs without recording note bodies or credentials. Document how you would diagnose “Save failed” from the browser to the database.

Finish by reviewing the tradeoffs: whole-document revisions versus row versions, local backups versus server backups, offset pagination versus cursors, and a synchronous audit transaction versus asynchronous notifications. Give a concrete trigger for changing each design. Avoid adding infrastructure only because a tutorial mentions it.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Review guide and solution reasoning

Use this page after attempting the exercises. There is no single correct framework choice. A strong solution keeps business rules explicit, demonstrates failure behavior, and explains which assumptions make the design safe.

For the mission filter, derive one filtered collection from accepted notes, the normalized text query, and the selected mission. Calculate the page count from that collection. Clamp the current page before slicing, and reset the requested page when either filter changes. A common mistake is filtering only the twenty visible records, which hides matching records on later pages and reports an incorrect total. Test at least twenty-one notes to expose that bug.

For note archiving, put compatibility defaults at the runtime boundary. A migration that assumes every imported object already has `archivedAt` is incomplete. Preserve the identifier on archive and restore. The write must still use the editor's captured revision and epoch. If your archive button uses a fresh snapshot while an older editor is open, either disable that competing action or define how the draft is reconciled; silently rebasing the old draft is not a solution.

For an HTTP adapter, a useful update contract is an identifier in the route, a version in the request, and only editable fields in the body. Reject unknown or server-owned fields. The server returns the committed representation with its new version. The UI adopts that response after success. A network timeout creates uncertainty: the server might already have committed. Explain how a reread, operation identifier, or idempotency design resolves that uncertainty before adding automatic retries to mutations.

For SQL, the note update and audit insertion belong in the same transaction if the requirement is “every accepted update has an audit record.” Test rollback using a real database constraint or injected failure after the update but before commit. A mock that always returns success cannot establish rollback. An affected-row count of zero in a versioned update should follow a documented missing-versus-conflict policy. Ownership constraints must be part of the database query, not a hidden button in React.

In review, ask the author to trace one rejected save. Which object changes? Which object stays unchanged? What can the learner export? What happens after reload? Then ask them to trace a reset while an older tab remains open. They should explain why a new epoch prevents an old-generation write even if revision numbers coincide.

Mid-level readiness means handling those questions without depending on happy-path demonstrations. Look for focused tests, readable names, bounded inputs, explicit compatibility decisions, and honest limits. A polished screenshot supports usability review, but it cannot establish authorization, transaction correctness, or recovery from an interrupted deployment.
''',
'07-TRACE-LAB.md':'''# Trace lab: connect a click to an accepted record

Use a disposable browser context and export any progress you want to keep. Open developer tools and locate the `skillforge.quest.progress.v1` local-storage value. Do not edit your main learning profile for this exercise. Keep a short table with columns for action, editor base revision, stored revision, stored epoch, visible accepted title, and draft title.

## Trace A: a normal note update

Create “Boundary notes” and record the saved revision. Open Edit and change the title to “Runtime boundary notes.” Before saving, inspect storage: its title and revision should be unchanged. Place a breakpoint in `LearningNotes.save`, then step through `updateNote`, `App.commitProgress`, and `persistProgress`. Observe that the schema is checked before the lock callback writes anything. Inside the callback, compare the proposal and current revision/epoch. After `setItem` returns, inspect the accepted object returned to the parent. The editor closes only after that acceptance.

## Trace B: a competing writer

Open another tab before editing. Capture a draft in both tabs. Save the first tab and observe the storage event warning in the second. The warning does not replace the second tab's fields. Submit there and follow the conflict exception back through the promise chain. The parent retains a pending proposal; the editor retains its input. Export pending data and compare its revision with current storage. Loading current progress requires an explicit discard confirmation and returns the view to the command deck.

## Trace C: reset generations

Leave an editor open in one tab. In the other, export a backup and reset saved progress. Compare epochs before and after the reset. The numeric revision restarts, but the epoch changes. Try submitting the old draft. It must fail even if its numeric revision happens to match a later revision in the new generation. Explain the difference between a record version and a generation identifier in your own words.

## Trace D: mission progress and evidence

Enter FizzBuzz, type an answer and scratch code, and inspect storage before pressing Save mission drafts. Submit one gate and inspect the response key, completed checkpoint list, XP, and revision together. The gate is self-reported evidence; satisfying minimum length does not prove the explanation correct. Complete a scheduled review when it becomes due and inspect the latest review response alongside its updated schedule. A premature repeat should be rejected by the engine.

Finish with a one-page engineering note: describe the invariant, the observable failure, the smallest owning module, and the test that would catch a regression. Then identify which parts would move to a server in a multi-user CRUD application and which UI draft responsibilities would remain in React.
''',
'VERIFICATION.md':'''# Verification record and practical limits

The implementation is validated in a staged copy before its finite changed-file manifest is delivered to the original project. The central completion report records the actual final check results. The repeatable project commands are `npm test`, `npm run build`, `npm run verify:content`, and `npm run test:browser`. Browser installation is a separate one-time step: `npx playwright install chromium`. The browser configuration starts its own strict loopback server and uses isolated contexts.

The model suite exercises normalization of legacy saves, malformed nested fields, reserved object keys, size bounds, catalog relationships, note identity and immutable operations, accepted-write ordering, quota rejection, queued competing writers, and reset generations. Progression checks exercise prerequisites, challenge membership, canonical XP rewards, due-time constraints, and runtime review ratings. These checks establish the specified local model behavior; they do not assess the educational truth of a learner's written answer.

The browser suite exercises real forms and downloads. It checks that onboarding writes only on submission, note CRUD survives reload, deletion can be cancelled, stale tabs retain pending drafts, quota errors preserve accepted state, corrupt original bytes can be exported, reset requires confirmation, mission drafts save explicitly, imported progress is validated and confirmed, failed content requests can be retried, and the lab reports assertion failures and terminates endless loops. Desktop and narrow journal screenshots are saved under `astraupskill/images/` for visual review.

Archive verification recomputes the preserved content evidence: 334 missions, 1,002 gates, 1,839 source files, and ten worlds. The application changes do not expand that archive or claim to complete its historical expansion plans. Existing handoff and migration documents describe prior work; this course describes the delivered reliability and CRUD changes.

Important boundaries remain. Storage is local to this origin and browser profile. Clearing site data removes it. Web Locks coordinate cooperating copies of this application on localhost or HTTPS; a script that ignores this protocol can still overwrite storage. Whole-document revisions may reject unrelated concurrent edits. Backups are manual, and an oversized pending export may need careful reduction before the bounded importer accepts it. Raw damaged-data exports are recovery material, not automatically valid portable saves.

There is no server authentication, SQL transaction layer, deployment verification, distributed concurrency guarantee, or full accessibility certification. Worker execution is a convenience for local experiments, not a security boundary; code can access worker capabilities, including network APIs. Output is bounded and the worker is terminated after 2.5 seconds, but completion is not proof of correctness. These limitations are explicit starting points for the backend and operational exercises, rather than features the current app claims to provide.
'''
}
for name,text in docs.items():
 (d/name).write_text(text,encoding='utf-8');print(name,len(text.split()))
p=s/'README.md';t=p.read_text(encoding='utf-8').replace('Progress saves automatically in the browser.','Profile submission saves in this browser. Mission answers and scratch code remain drafts until you choose **Save mission drafts** or submit a checkpoint.').replace('a persistent JavaScript scratch lab with isolated execution and a timeout;','a JavaScript scratch lab with explicit draft saving, bounded output, and a worker timeout;').replace('reference and solution files hidden until the prediction gate is cleared;','reference and solution files visually gated until the prediction checkpoint is cleared (the static archive is not access-protected);')
t+='''\n## Reliable saves and learning-note CRUD\n\nOpen **Loadout & saves** to create, read, search, update, and delete mission-linked learning notes. Saves use a captured revision and reset generation under a Web Lock. A competing tab or storage failure keeps the editor and offers a pending export. **Load current progress** discards drafts only after confirmation. Invalid saved data is preserved for raw export before a confirmed reset. Imports validate the complete bounded document and catalog relationships before confirmed replacement. Use localhost or HTTPS in a browser with Web Locks.\n\nProgression gates are self-reported evidence, not automated grading. The lab reports failed assertions and exceptions, caps output, and terminates long runs; it is not a security sandbox. Latest review reasoning is saved when its rating is accepted. There is no backend, account authorization, SQL store, or automatic cross-device synchronization.\n\nRead the detailed [CRUD learning course](astraupskill/README.md), including worked changes, failure experiments, and a path to a real API and SQL database. For browser verification run `npx playwright install chromium` once, then `npm run test:browser`. The tests use an isolated browser profile and loopback port 4287.\n'''
p.write_text(t,encoding='utf-8')
