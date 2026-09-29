from pathlib import Path
s=Path('astra-remaining-improvements/stage/6844a7b03c83')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('README.md',r'''
# Quiz board studio

A small vanilla JavaScript CRUD app for editing a question bank and playing quiz rounds. The folder is historically named `react`, but the implementation uses browser ES modules, DOM APIs, localStorage and Web Locks. Start with [the detailed learning course](astraupskill/README.md).

## Run

Prerequisites: Node 22 and a current browser with Web Locks on localhost.

```powershell
npm ci
npm start
```

Open `http://127.0.0.1:4173`. Serve through the local server instead of opening index.html as a file. The server serves only the app's seven assets and binds to loopback. It does not expose a data API or other repository files. `PORT` can select another port; browser storage belongs to the exact origin, so changing the port changes which saved board is visible.

## Use

Choose Edit question bank to create, rename or delete categories and create, update or delete questions. Category deletion removes its questions from the draft. Save bank persists the entire validated candidate; Cancel discards the draft. Each category supports up to 20 questions, with up to 10 categories overall. Questions have a prompt, answer and point value.

Clue tiles show points. Open a clue, reveal its answer and explicitly mark it used. Closing a clue alone does not consume it. New round clears used markers while retaining the question bank. Progress survives reload in this browser. Points label clues; automatic player scoring is not implemented.

Export creates a portable JSON copy. Import validates before requesting replacement confirmation. Existing legacy arrays under `customJeopardy` load without an automatic write and convert to the versioned format on the next successful save. Corrupt saved text is preserved, with export and explicit replacement controls. Storage failures retain the editor draft. Cooperating tabs use Web Locks plus exact saved-text comparison to reject stale writes.

## Verify

```powershell
npm test
npx playwright install chromium
npm run test:browser
```

The Node suite checks storage/domain behavior. Chromium scenarios exercise actual CRUD, reload, cross-tab conflicts, Web Locks, quota failure, import/export and layouts using fresh browser contexts. See [verification](astraupskill/VERIFICATION.md) for evidence and limits.

This is a local learning app. It has no server database, authenticated accounts, shared remote classroom, player score ledger or guaranteed backup. Existing sample question content is retained as supplied. Web-service and SQL extensions are [practice work](astraupskill/05-PRACTICE.md).
''')
w('astraupskill/README.md',r'''
# Learn CRUD through a complete browser workflow

This small application now has a real question-bank editing workflow rather than only a set of clickable tiles. Your goal is to follow a user action through draft state, validation, persistence and rendering, then explain what happens when saving fails or another tab acts first. Those skills transfer directly to larger CRUD web applications.

Start with [the root setup](../README.md). Install the locked development dependency with `npm ci`, start the local server and open its loopback URL. The application itself has no framework or runtime package dependency. Despite the historical folder name, it is vanilla JavaScript. Read the code as browser modules rather than looking for React components that are not present.

## Your first session

Open a clue. Notice that the board initially shows points, then the dialog displays the prompt. Reveal answer shows the answer, while Mark clue used persists its consumed state. Close alone leaves it available. Reload and compare the used count. New round clears progress while retaining the same questions. The app does not calculate a player's score; point values identify clue values only.

Open Edit question bank and add a category called CRUD practice. Add a question, supply a prompt and answer, and save. Reload to see the persisted category. Edit the question, cancel once and verify that the saved version remains. Then save an update, delete the question with confirmation and finally delete the empty category. This sequence exercises the full create/read/update/delete lifecycle.

Read [the code map](01-CODEBASE-MAP.md), [concepts](02-CONCEPTS.md) and [worked change](03-WORKED-CHANGE.md). Use [testing and debugging](04-TESTING-AND-DEBUGGING.md) to connect each guarantee to evidence. Attempt [practice](05-PRACTICE.md) before consulting [review guidance](06-SOLUTIONS-AND-REVIEW.md). Complete [the trace lab](07-TRACE-LAB.md) and read [verification](VERIFICATION.md) before describing the application as reliable.

For every change, write a short note with the user intent, valid input, state owner, save boundary, failure path and test. For example, “An editor opened before another tab marks a clue used must not restore the older round state.” That sentence explains why exact saved-text comparison is needed in addition to a lock.

The app stores data in this browser on this exact origin. Export provides a copy you can move elsewhere. There is no authenticated account, remote database or shared classroom service. The course teaches those as next steps. A mid-level engineer should be able to distinguish a working local workflow from the additional consistency and access-control requirements of a multi-user server application.
''')
w('astraupskill/01-CODEBASE-MAP.md',r'''
# Follow the browser's state owners

[index.html](../index.html) supplies the toolbar, board and two native dialogs. It loads one module entry point and the actual stylesheet paths. The original markup referenced nonexistent subdirectories and duplicated scripts before and after the DOM. The current module entry waits for document parsing and imports its dependencies explicitly, making startup order visible.

[main.js](../main.js) coordinates the application. `current` holds the last loaded or accepted saved board plus its exact raw storage text. The editor owns a separate draft. `valid` distinguishes usable saved data from a corrupt or unavailable storage state, and `busy` prevents overlapping UI save commands. The controller handles clue dialogs, import/export, new rounds and storage events from other tabs.

[store.js](../store.js) defines the data contract and persistence boundary. `validateState` checks schema version, revision, category and question counts, stable IDs, required text, point values and used-question references. `migrateLegacy` converts the earlier category/question array into deterministic IDs without changing the source array. `parseState` distinguishes missing storage, legacy data, valid current data and malformed content. `BoardStore.save` owns locking, stale-data comparison and the actual localStorage write.

[edit.js](../edit.js) builds labeled form controls with DOM methods. It starts from a deep copy of the current state and remembers the raw baseline at editor opening. Input events update only that draft. Adding or deleting categories/questions rerenders the draft form. Submission passes the candidate and original baseline to the save callback. The modal closes only after save succeeds; a failure preserves the draft for correction or export-oriented recovery.

[board.js](../board.js) renders one section per category, keeping its heading and question tiles together. Each tile is a button with an accessible label and a callback carrying the selected question. User-controlled names and text are assigned as text, not inserted as HTML. Used IDs determine disabled tiles. The displayed progress count is derived from the state rather than maintained by a separate counter.

[data.js](../data.js) retains the supplied example content. [server.js](../server.js) is a small local static server with an explicit asset allowlist. It has no database or mutation endpoint. Serving through loopback gives the browser a suitable origin for modules, storage and Web Locks.

Read [store tests](../test/store.test.js) for pure validation and controlled storage behavior, then [browser tests](../e2e/board.spec.js) for real DOM, localStorage and cross-tab coordination. Trace a successful edit across all these files and identify where the visible board becomes authoritative. Then trace a quota error and show why the old board and new draft remain separate.
''')
w('astraupskill/02-CONCEPTS.md',r'''
# Drafts, identity and cooperating browser tabs

A draft is a proposal. The saved board is the accepted state. Mixing them creates a common CRUD bug: the screen changes before persistence succeeds, then a reload loses the apparent update. The editor copies the loaded board, changes the copy and submits it only when the learner saves. `BoardStore.save` validates and writes before the controller replaces `current`. A storage error leaves the proposal visible in the dialog and the accepted board unchanged.

Stable IDs distinguish records from positions. Deleting the first question should not make its used marker refer to the former second question. Categories and questions have unique IDs, while round progress stores question IDs. Delete helpers remove obsolete used markers together with the corresponding records. Validation rejects duplicates and references to missing questions, keeping the relationship explicit.

## Why a lock is not enough

A Web Lock serializes cooperating saves on the same origin. Imagine two tabs both load revision zero. Tab A saves a changed category and releases the lock. Tab B later acquires it, but its draft was still based on revision zero. If it simply writes, it loses A's change. Therefore the save also compares the current stored text with the exact text remembered when that draft began. B conflicts instead of overwriting A.

The app increments revision for display and exported metadata, deriving the next value from current storage. It does not trust a revision number supplied in an import. The actual stale-write condition uses the raw baseline. This is coarse whole-board concurrency: two tabs editing different questions still conflict. Per-record versions in a server database are a later exercise.

## Missing, empty and corrupt data

Missing storage loads examples without automatically writing. An empty category list is a valid user-created board. Malformed JSON or an unsupported schema version is corruption or incompatibility, so the app preserves the raw text and offers recovery. It does not silently replace a broken board with examples. Explicit replacement checks the same raw baseline, preventing an old recovery screen from overwriting a newer repair in another tab.

Input validation and safe rendering solve different problems. A category name containing angle brackets can be valid literal text. The DOM renderer uses textContent and text nodes, so that value does not create an image or execute markup. Import validation checks structure, bounds and relationships before it reaches rendering. Neither local validation nor a content security policy creates authenticated ownership.

The storage guarantee assumes all app tabs use the same lock protocol. DevTools, older scripts or other code can bypass it. localStorage is origin-scoped and is not a remote backup or a database transaction across users. These limits matter when translating the design into a server-backed CRUD application.
''')
print('Quiz board setup and first three course files written')
