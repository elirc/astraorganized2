from pathlib import Path
b=Path(__file__).resolve().parent;s=b/'stage/b415b13a50ee';d=s/'astraupskill';d.mkdir(exist_ok=True)
p=s/'extension/styles.css';p.write_text(p.read_text(encoding='utf-8')+'\n.saved-messages textarea{display:block;width:100%;min-height:130px;resize:vertical;padding:12px;border:1px solid #b8c6b8;border-radius:8px;background:#fff;line-height:1.5;color:inherit}.saved-messages form>.primary,.saved-messages form>.secondary{margin-top:12px}\n',encoding='utf-8')
old=(s/'README.md').read_text(encoding='utf-8');credits=old[old.index('## Artwork and icons'):]
(s/'README.md').write_text('''# Interlude

Local Pomodoro timer, artwork breaks, and a reusable reminder library. Runs as a browser preview or a self-contained Manifest V3 Chrome extension. Start the detailed junior-to-mid-level learning course in [astraupskill](astraupskill/README.md).

## Run and develop

Use Node 22. From this folder:

```powershell
npm.cmd ci
npm.cmd run build
npm.cmd start
```

Open the loopback URL printed by the preview server (normally port 43210). An occupied port selects a free port. The extension folder is already built: enable Developer mode at `chrome://extensions`, choose Load unpacked, and select `extension`. The toolbar action opens its dashboard. After changing source, rebuild and reload the extension. `interlude-extension.zip` contains the same delivered extension files; extract it before loading. Do not edit generated `extension/app.js`; edit `src/app.js`.

## Implemented behavior

Focus defaults to 60 minutes followed by a five-minute art break. Pause, reset, snooze, presets, custom durations, rotation, uploaded art and daily counters remain available. My message now includes create, read, update and confirmed delete for up to 30 saved reminders. Use copies a library message into the active reminder draft; Save message applies it. Deleting a library entry preserves the active reminder.

Settings and library edits carry the revision captured when editing starts. A competing save rejects the stale proposal and keeps its text. Reopen the view to load current values after copying any draft you want to keep. Navigating back to the message view clears the library editor. Timer commands do not consume settings revisions. Uploaded artwork is resized locally and never sent to a service.

Accepted extension data is persisted before alarms/windows are reconciled. A warning can mean the data saved but an external effect failed. A later dashboard read retries that effect. The preview requires its tab to stay open; extension alarms require Chrome to remain running and can be delayed by sleep. Break windows are dismissible. Browser preview storage and extension storage are independent.

Settings offers Export local data. Corrupt preview JSON is preserved for export; Reset browser preview data explicitly confirms replacement and checks that data did not change while confirming. This export is a recovery artifact, not an implemented import format. Extension reset is not provided. There is no server account, SQL database, authentication, shared workspace or durable distributed outbox.

## Verify

```powershell
npx.cmd playwright install chromium
npm.cmd run verify
```

Verification builds the bundle, runs 39 Node tests and ten Chromium scenarios. The browser runner starts its own strict-port server (25431 by default) and an isolated unpacked-extension profile. Set `PLAYWRIGHT_BROWSERS_PATH` when reusing a managed browser installation. Set `INTERLUDE_RESULTS_DIR` to retain four screenshots. `node tests/browser-check.mjs` invokes the same browser suite. Tests use synthetic browser data and never attach to a personal profile. See [verification evidence and limits](astraupskill/VERIFICATION.md).

'''+credits,encoding='utf-8')
docs={
'README.md':'''# Learn CRUD and failure handling through Interlude

Interlude gives you a small, visible application in which a save has consequences beyond changing a label. It stores timer settings, reusable reminders and a deadline; the extension also creates alarms and break windows. Your learning target is to explain how a proposal becomes accepted data, how a stale proposal fails, and how a later read repairs an external effect. Those skills transfer directly to a CRUD web application with a database and background jobs.

Begin with the root [setup guide](../README.md), then open the preview. Create a saved message called Water with text Take a sip. Edit its title to Hydrate, use it, save the active message and delete the library entry. Reload. The active reminder remains because it is a copied value, not a foreign-key reference. Explain this behavior before reading the implementation: the product decision determines the data relationship.

Read these lessons in order:

1. [Codebase map](01-CODEBASE-MAP.md): find the UI, pure model, timer transitions and storage adapters.
2. [Concepts](02-CONCEPTS.md): compare drafts, revisions, validation and committed side effects.
3. [Worked change](03-WORKED-CHANGE.md): trace saved-message creation through both persistence paths.
4. [Testing and debugging](04-TESTING-AND-DEBUGGING.md): distinguish model evidence, simulated worker failures and real browser behavior.
5. [Practice](05-PRACTICE.md): build progressively harder changes with explicit acceptance criteria.
6. [Solutions and review](06-SOLUTIONS-AND-REVIEW.md): compare your reasoning after trying the exercises.
7. [Trace lab](07-TRACE-LAB.md): reproduce a conflict and an interrupted effect deliberately.
8. [Verification](VERIFICATION.md): understand exactly what was tested and what remains unproven.

Allow a first session for running and tracing, a second for model tests, and later sessions for the exercises. Progress depends on the evidence you produce, not elapsed hours. Before advancing, show a reviewer one successful save, one rejected save that preserves its draft, and one saved operation whose external effect needs repair. Use the browser storage inspector only with this isolated learning profile.

The implemented app remains local. The HTTP API, SQL model and authentication described in later exercises are proposed extensions. You are ready to move toward mid-level work when you can describe their transaction boundaries, authorization decisions and failure responses without claiming the current local version already provides them. Keep a short engineering journal containing your prediction, observed result and explanation for each failure experiment.
''',
'01-CODEBASE-MAP.md':'''# Read the code by responsibility

Start at [src/app.js](../src/app.js). It installs the layout, binds controls, keeps the visible settings/state/revision/presets snapshot and chooses a transport. In a normal browser it uses local storage; inside the extension it sends runtime messages to the worker. The shared UI therefore needs the same response shape from two adapters. `src/layout.js` supplies the original timer, artwork, message and settings markup. The new library and recovery controls are appended by the app module with explicitly constructed elements.

[extension/model.js](../extension/model.js) is the data boundary. `normalize` validates a stored snapshot and supplies missing legacy fields. `parsePreview` distinguishes absent storage from malformed stored text. `applyMessage` validates a command and computes a candidate without writing it. Read the allowed keys before following a branch: rejecting unknown fields prevents accidental partial support for a misspelled or future property.

[extension/state.js](../extension/state.js) owns timer arithmetic and phase transitions. It receives a clock value, which makes elapsed-time tests deterministic. A deadline represents the intended finish instant; the displayed countdown is derived from it. Repeated display refreshes should not create new focus sessions. The state tests explain how start, pause, snooze and completion interact with counters.

[extension/background.js](../extension/background.js) serializes worker operations, reads Chrome storage, applies the model, persists the accepted snapshot and reconciles alarms/windows. Follow `synchronize` and then `reconcile`. They deliberately expose a distinction between a failed initial write and a failure after data was accepted. The queue serializes this worker's messages; it is not a cross-device database lock.

The generated `extension/app.js` bundles the UI and dependencies. The manifest starts the background module and points at the options page. `extension/styles.css` and the three bundled artwork files are consumed directly. `server.js` serves the preview; it does not implement a database or CRUD API. The zip is a packaged copy of extension assets, not another implementation.

Read tests in three layers: timer/model tests describe pure rules; worker tests inject storage, alarm and window failures; [browser scenarios](../tests/browser/interlude.spec.js) exercise the actual interface and one unpacked extension. To trace one edit, put breakpoints at the form handler, `applyMessage`, the adapter write and the UI assignment after success. Record the revision at each stop. If the displayed data changes before persistence succeeds, you have crossed the acceptance boundary too early. That ordering is the key relationship to find in this codebase.
''',
'02-CONCEPTS.md':'''# Data invariants, revisions and external effects

A saved reminder contains `id`, `title` and `message`. Identity stays stable when its title changes. Titles are trimmed and bounded at 80 characters, message text at 500, and the library at 30 entries. IDs must be unique. These rules belong in the shared model because browser input attributes can be bypassed by a runtime message or hand-edited storage. Validation also covers durations, boolean settings, artwork choices, image data and timer state.

A draft is a proposal; an accepted snapshot is the last successfully stored value. Suppose two tabs load revision 7. Tab A changes a reminder and saves with `expectedRevision: 7`; the accepted revision becomes 8. Tab B submits its older proposal with 7. The model rejects it. It must not silently retry with 8, because that would turn a detected conflict into an overwrite. The UI retains B's proposal so the learner can copy it, reopen current data and decide how to merge.

The revision covers settings and the saved-message library together. This is intentionally conservative: unrelated edits may conflict. Timer start/pause commands do not increment it, so a running countdown does not continuously invalidate an editor. A future per-reminder version could reduce false conflicts, but would need a separate rule for settings and library limits. There is no single correct version scope independent of the application's invariants.

The browser adapter uses Web Locks to serialize cooperating same-origin tabs while it reads, validates and writes. A lock without a version check would still allow an old form to replace newer data. A version check without serialized read/check/write could let two simultaneous saves both win. Together they protect this local protocol; direct storage manipulation and other origins remain outside it.

The extension has another boundary: persistence versus side effects. Imagine the worker stores a running deadline successfully, then alarm creation fails. Returning only an ordinary save failure would mislead the UI about accepted data. Instead it returns the accepted snapshot with a warning; a later read checks and repairs the alarm. Likewise a saved break state can outlive a failed popup creation. This is reconciliation, not a durable outbox or an atomic transaction across Chrome APIs.

Chrome's [alarm API](https://developer.chrome.com/docs/extensions/reference/api/alarms) supports inspecting scheduled alarms; timing can be delayed, including by sleep. The code compares desired state with observed effects rather than relying on one initial scheduling call. In a server application the analogous design might store an outbox row in the same SQL transaction and process it separately. Implementing that design would require retries, ownership and deduplication beyond this project's current guarantees.
''',
'03-WORKED-CHANGE.md':'''# Worked change: create and revise a reusable reminder

The implemented library adds CRUD to an app that previously stored one active message. Follow [the model](../extension/model.js) and [the app](../src/app.js) while reproducing the following sequence. Start from an isolated preview with an empty library and revision zero. The library form captures the editing revision when a new draft first changes. Editing an existing card captures the revision when Edit is chosen.

The command has this shape:

```js
const request = {
  type: 'preset',
  action: 'create',
  expectedRevision: 0,
  preset: { id: 'water-1', title: 'Water', message: 'Take a sip' }
};
const next = applyMessage(normalize(), request, 1000);
// next.presets has one item; next.revision is 1.
```

The browser UI uses a generated UUID rather than this teaching ID. `applyMessage` first normalizes the current snapshot, checks the command shape, compares the expected revision, validates the reminder and rejects an existing identity. It constructs a new array and returns a candidate. Nothing in this function writes local storage, creates a DOM node or contacts Chrome. You can assert that the input snapshot still has an empty array.

In preview mode the adapter executes the read/check/write sequence inside the same-origin Web Lock. Only after `localStorage.setItem` succeeds does the UI adopt the response. In extension mode the worker serializes messages and saves the whole accepted snapshot to Chrome storage. It then reconciles effects. A storage rejection prevents acceptance; an effect rejection after storage produces a warning alongside the saved response. These are different outcomes and deserve different user messages.

The UI builds each card using `textContent`. A title such as `<b>Water</b>` remains text. Update submits the same identity and a new title/message with the editor's revision. Delete requires confirmation and removes only that saved item. Use copies message text to the active-message editor; a separate Save message performs the settings patch. Therefore deleting Water does not erase a reminder already copied into settings.

Now open two tabs and edit Water in both. Save A first, then B. B keeps its typed text and displays the conflict. Reopening the view refreshes the baseline but clears its library draft, so copy useful text first. Notice why sending the entire settings object would be dangerous: an old message form could also undo an unrelated artwork change. The improved handlers send partial settings patches, and the revision check still guards the fields they intend to change. Partial updates and optimistic concurrency solve different parts of the lost-update problem.
'''}
for name,content in docs.items():(d/name).write_text(content,encoding='utf-8')
print({name:len(content.split()) for name,content in docs.items()})
