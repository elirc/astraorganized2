from pathlib import Path

B = Path(__file__).resolve().parents[2]
S = B / 'stage/44013f102ff1'
C = S / 'astraupskill'
C.mkdir(exist_ok=True)

(S/'README.md').write_text('''# Practice Journal and AI Call Assistant

Start with **Practice Journal**, a local CRUD web app for deliberate interview and engineering practice. Manage profiles, questions, sessions and scored attempts. It runs without Electron, external accounts, recording, provider keys or third-party runtime packages.

## Quick start — PowerShell

Install Node.js 22 or later, open this project directory, then run:

```powershell
node --version
npm test
npm run practice:setup -- "Your name"
npm run practice
```

Setup creates `data/practice.json` and prints a random access token once. Keep it privately. Open `http://127.0.0.1:4310`, enter that token, and create a profile. Setup refuses to overwrite an existing workspace. The server never automatically initializes or repairs data. You do not need `npm install` for this learning app or its Node tests.

For a separate disposable workspace, set an absolute file path before both setup and startup:

```powershell
$env:PRACTICE_DATA_FILE = 'C:\\your-training-folder\\practice.json'
$env:PRACTICE_PORT = '4311'
npm run practice:setup -- "Practice learner"
npm run practice
```

Use a directory you own. Stop the server with Ctrl+C. Clear those task-specific environment variables when you finish using the alternate workspace.

## A first complete session

1. Create a profile with your target role and learning goals.
2. Create a question; choose that profile or make it shared.
3. Create a session, then change its status from `planned` to `in_progress`.
4. Create an attempt for that session and question. Write your own answer, review it, and assign a score from 0 through 5.
5. Complete the session. Reopen it to revise its attempts.
6. Export a copy. Archive questions you no longer want offered. Delete referenced records in child-first order.

The editor keeps unsaved drafts after rejected writes. If another writer changes the workspace, choose **Review latest while keeping my draft**, compare accepted values, and explicitly retain your changed fields. A lost response may still represent an accepted write; review before retrying a creation.

## Learn the implementation

The [nine-part course](astraupskill/README.md) explains source files, request traces, worked fixes, exercises, solutions and verification. Start there before adding features. [Verification details](astraupskill/VERIFICATION.md) distinguish Node tests, real HTTP/browser checks, and a separately mocked desktop renderer.

## Optional legacy desktop assistant

The existing Electron app remains a separate entry point: `npm ci`, then `npm start`. Its pinned dependency tree remains in `package-lock.json`; this change does not claim that its Electron release is current or that the Windows installer was tested. Review the desktop dependencies before distributing it. `npm run dist` is the existing Windows packaging command.

The desktop workflow records system audio on explicit action, transcribes through SiliconFlow, and streams a DeepSeek answer. It requires provider credentials and desktop OS support. Native capture, provider compatibility, OS encryption and packaging were not exercised in the isolated checks. No real credentials, audio or provider requests were used during this improvement. The legacy app's content-protection setting remains; the separate Practice Journal has no recording feature.

Desktop settings now use write-only credential fields, revision checks, explicit clear controls and protected IPC. Existing plaintext keys are read without rewriting the file; a subsequent explicit save encrypts nonempty keys only when OS encryption is available. If encryption or parsing fails, preserve the file and use the recovery instructions in the course. Blank key inputs mean keep the saved key; the separate removal checkbox clears it.

## Scope and recovery

This is a single-owner, loopback learning app using a bounded JSON store. It has no account recovery, import, team authorization, durable operation receipts or distributed database. Export omits the credential and is a portable record copy, not an automatic restore format. A full private data-file backup includes the token hash; protect it. A stale `.lock` is never stolen automatically. Stop all writers, preserve files, establish which operation stopped, and repair only a disposable copy first.

Original source snapshots live under `docs/original/` with `.txt` suffixes. `docs/ALTERNATIVE_APP_SPEC.md` remains a historical proposal, not a statement that all of its features were implemented.
''',encoding='utf-8')

docs = {}
docs['README.md'] = '''# Learn CRUD engineering through Practice Journal

This course takes a junior developer from reading a working application to explaining the consistency and failure behavior expected of a mid-level engineer. The project now contains two related systems: a new local web journal and the existing desktop audio assistant. Use the journal first. Its four linked resources make relationships, validation, update semantics, and state transitions visible without external dependencies.

## What you will build understanding of

A profile describes a learning context. A question belongs to one profile or is shared. A session belongs to one profile and moves through planned, in-progress and completed states. An attempt belongs to a session and preserves the question wording used during that attempt. This is enough structure to learn genuine CRUD decisions: whether a reference may change, which records can be removed, and how historical information survives edits.

Start with the [root setup instructions](../README.md). The Node tests and journal need no package installation. Setup creates an empty, explicitly owned workspace and shows its access token once. The browser keeps that token in memory. Refreshing the tab requires another sign-in. Use synthetic descriptions and practice answers while learning failure scenarios.

## Five learning stages

1. **Run and read.** Follow [the codebase map](01-CODEBASE-MAP.md). Create a profile, question, session and attempt. Find the source responsible for each screen action. Explain why a new session cannot immediately accept an attempt.
2. **Understand contracts.** Study [the concepts](02-CONCEPTS.md). Predict the result of a missing field, `false`, zero, `null`, an unknown field, and an outdated revision. Confirm your predictions with tests.
3. **Repair a concrete defect.** Follow [the worked change](03-WORKED-CHANGE.md). Compare the original settings store with the repaired implementation. Explain the difference between accepted disk state and an in-memory draft.
4. **Practice failure handling.** Use [testing and debugging](04-TESTING-AND-DEBUGGING.md) and [the exercises](05-PRACTICE.md). Simulate another writer, failed replacement, and a lost response. Keep the failing test focused on observable behavior.
5. **Review like a maintainer.** Compare your answer with [solutions and review](06-SOLUTIONS-AND-REVIEW.md), then narrate [the trace lab](07-TRACE-LAB.md) without looking at the guide. Check [verification](VERIFICATION.md) before describing a guarantee to another developer.

## A small worked practice example

Create profile “API developer”, question “Why use a revision on PATCH?”, and session “Concurrency rehearsal”. Start the session. Record the answer: “The client sends the revision it edited; the server compares it while holding the writer lease. A mismatch prevents a stale overwrite.” Score the answer zero initially if it needs work. Zero is a real score; leaving the field blank means no score. Complete the session only after writing and scoring every attempt.

Now edit the question wording. Reopen the old attempt. Its snapshot should still describe the question actually practiced. This distinction introduces historical modeling: a foreign key identifies a current object, while a snapshot preserves selected facts at an earlier time. Neither is a universal substitute for the other.

## How to study each chapter

Read a small source function, write a prediction, perform one action, and compare the result. Keep a learning note containing the exact input, expected output, observed output, and file responsible. For example, “`score: 0` was accepted; `score: '0'` was rejected; the HTML form converts its string input before sending JSON.” That note is more useful than copying the entire function.

When you finish an exercise, show a teammate the normal case and one failure case. Explain what remains unchanged after failure. Include whether the evidence came from a pure function, real file, HTTP request, browser interaction, or mocked bridge. The distinction is part of engineering accuracy, not paperwork.

This course does not require activating the desktop recorder. Its settings and IPC changes provide a second example of the same boundary principles. Native Electron, actual OS encryption, audio capture, and live providers remain separate verification work. The journal is intentionally bounded to one owner on one machine; a future database or team system needs additional design.
'''
docs['01-CODEBASE-MAP.md'] = '''# Codebase map: follow one write

Begin with [package.json](../package.json). `practice:setup` creates an empty journal; `practice` starts the loopback server; `test` runs the Node suite; `syntax` parses JavaScript across source, tests and verification. `start` still launches the separate Electron assistant. These commands enter different workflows, so identify the process you are debugging before setting a breakpoint.

## Web application responsibilities

| File | Responsibility | Useful question |
| --- | --- | --- |
| [setup.js](../src/practice/setup.js) | Generate a random token and initialize once | What stops setup replacing existing work? |
| [server.js](../src/practice/server.js) | HTTP envelope, authentication, routing and responses | Which checks happen before domain mutation? |
| [domain.js](../src/practice/domain.js) | Resource contracts, relationships, lifecycle, listing, export helpers | What makes an attempt valid? |
| [json-file.js](../src/shared/json-file.js) | Read, validate, revise and replace accepted JSON | When does the write become accepted? |
| [ui/app.js](../src/practice/ui/app.js) | Browser state, dynamic forms, draft comparison and requests | What survives an uncertain response? |
| [ui/index.html](../src/practice/ui/index.html) | Semantic page and accessible form regions | Where does feedback appear? |
| [ui/styles.css](../src/practice/ui/styles.css) | Desktop and narrow-screen layout | Can every action remain reachable? |

Read `payload` in the domain before reading all the HTTP handlers. It distinguishes create defaults from PATCH omissions. Then read the reference and lifecycle checks. Finally follow the service methods into `disk.commit`. This reading order gives the transport code meaning: routes are useful because they enforce a domain operation, not merely because a URL returns JSON.

## Trace: creating a profile

The browser renders fields from `definitions`. `values` produces typed data: a checkbox becomes a boolean, a number input becomes a number or `null`, and a nullable reference becomes `null` when blank. `changes` returns a full create body or only changed edit fields. The submit handler supplies the editor's accepted revision, not whichever revision another background request happened to fetch most recently.

The server validates request host, origin, method, body type and size. Authentication compares the provided token hash with the stored hash. The create route supplies the body and quoted `If-Match` revision to the service. The service validates fields, then executes the operation inside the file store's mutation callback. The callback sees current accepted data under the writer lease. It checks uniqueness and relationships, creates the record, and appends a content-free activity entry.

The file store serializes and validates the complete draft, writes a private temporary file, flushes it, and replaces the accepted file. Only then does the service return the accepted record and revision. The browser reloads bootstrap, list and detail state. If this follow-up read fails, it says the write was accepted but the refresh failed; it does not quietly declare the old editor current.

## Desktop responsibilities

[main.js](../src/main/main.js) creates the Electron window and configures existing capture/navigation behavior. [preload.js](../src/preload.js) exposes six narrow bridge operations. [ipc-controller.js](../src/main/ipc-controller.js) validates the window, sender frame, message shape and recording request lifecycle. [settings-store.js](../src/main/settings-store.js) keeps credentials behind the main-process boundary and delegates replacement to the same JSON storage primitive.

The original `store.js` is now a small Electron adapter. Provider modules `stt.js` and `llm.js` still handle transcription and streaming; their tests use synthetic network responses. The renderer settings form sends `{revision, changes}` and receives public settings with credential presence flags. It never needs the stored secret merely to show that a secret exists.

## Test map and original reference

[practice.test.js](../test/practice.test.js) exercises domain behavior against disposable files. [practice-http.test.js](../test/practice-http.test.js) makes real loopback requests. [json-file.test.js](../test/json-file.test.js) isolates persistence faults. [ipc.test.js](../test/ipc.test.js) supplies synthetic Electron-like senders. [verify_browser.py](../verification/verify_browser.py) operates the actual web UI. [verify_renderer.py](../verification/verify_renderer.py) operates the desktop HTML with a mocked preload bridge.

Original implementation snapshots are preserved under [docs/original](../docs/original). Their `.txt` suffixes keep archived tests out of discovery. Use them to study before/after behavior, not as runnable alternate entry points. The historical alternative specification describes a larger possible rewrite; the implemented behavior is defined by current source, this course, and the explicit evidence.
'''
docs['02-CONCEPTS.md'] = '''# Concepts: contracts, history and accepted state

CRUD is more than four route names. A useful implementation defines which inputs are allowed, what references mean, which transitions make sense, and how a user learns whether an operation succeeded. This project makes those contracts small enough to inspect in [domain.js](../src/practice/domain.js) and [server.js](../src/practice/server.js).

## Omission is different from a value

```json
{"targetRole":"Backend developer"}
```

On profile PATCH, this changes only the role. It does not erase the background or unarchive the profile. Compare explicit values:

```json
{"background":"","archived":false}
```

The empty string clears an optional field and `false` unarchives. Neither should disappear through a truthiness check. Similarly, `score: 0` is a valid assessed score, while `score: null` means unscored. A string `"0"` is not the same JSON type as the number `0`. The browser converts form strings; the server still validates independently because callers can bypass the browser.

Create operations apply documented defaults. PATCH applies only supplied editable fields. Unknown fields and immutable references are rejected so a misspelled field cannot appear to save successfully. A session's profile and an attempt's session/question identities are immutable after creation. To represent a different association, create a different record deliberately.

## Relationships and historical snapshots

A question can be shared (`profileId: null`) or assigned to one profile. A new attempt may use only an active question matching its session's profile or a shared question. A session stores the profile name and target role at creation; an attempt stores question title, prompt and topic. Later edits to the current question do not rewrite the question that was answered historically.

Archiving controls future availability while preserving references. Deletion removes a record and is blocked when children still depend on it. The explicit removal order is attempts, sessions, questions, then profiles, subject to session state. This is a domain choice, not a universal CRUD rule. A billing system might forbid deletion entirely; a disposable draft editor might choose an explicit cascade. The important skill is making the choice visible and testing it.

## State transitions

New sessions start `planned`. Starting changes status to `in_progress`, which permits attempt creation and editing. Completion requires at least one attempt and an answer plus score on every attempt. Reopening returns to `in_progress`. Returning to `planned` is allowed only when there are no attempts. These rules prevent contradictory state such as a supposedly completed session containing unassessed practice.

## Revision and writer lease solve different problems

The file revision is SHA-256 of accepted bytes. The browser sends it as a quoted `If-Match` header. A revision comparison detects a stale edit. An exclusive `.lock` lease prevents two cooperating writers from both checking and replacing concurrently. The comparison must happen while holding the lease; checking first and acquiring later leaves a race.

```text
Tab A reads revision R1
Tab B accepts a write, producing R2
Tab A submits its draft with R1
Server holds lease, reads R2, rejects R1
Tab A retains draft and asks for explicit review
```

The revision is global to this small file, so an unrelated record edit also conflicts. That is conservative and easy to reason about, but less convenient than per-record versions in a database. JSON replacement is bounded local persistence, not a claim of distributed transactions or power-loss certification.

## An error response does not always mean nothing happened

A network failure after replacement can hide a successful write. A cleanup error after replacement can also make the outcome uncertain. The editor therefore blocks automatic retries and loads current state for review. It does not have durable operation receipts. In particular, retrying an uncertain creation can duplicate work; inspect or search existing records first.

## Credentials cross only necessary boundaries

The journal stores a hash of a high-entropy bearer token; the browser retains the token only in memory. Export excludes authentication internals. Desktop settings use a different mechanism: Electron OS-backed encryption and write-only form fields. Availability and protections depend on the platform; see Electron's [safeStorage API](https://www.electronjs.org/docs/latest/api/safe-storage). The local tests inject a synthetic encryption adapter and do not establish native OS behavior.

Electron also recommends validating the sender of privileged messages; read its [security guidance](https://www.electronjs.org/docs/latest/tutorial/security). This project's controller checks exact live window, main frame and page URL before operating. The lesson applies equally to HTTP: knowing which operation was requested is insufficient without establishing who may request it.
'''
docs['03-WORKED-CHANGE.md'] = '''# Worked change: publish settings only after acceptance

The original settings store made several assumptions that were convenient for a prototype but dangerous to learning correct update behavior. It could mutate an in-memory cache before persistence succeeded, turn read failures into defaults, implicitly recover damaged JSON, expose nested aliases, and tolerate encryption failures by changing meaning. Eight new behavioral regressions failed against that original implementation. They passed after the storage repair.

Compare [the original store snapshot](../docs/original/src/main/store.js.txt), [the new adapter](../src/main/store.js), [the settings service](../src/main/settings-store.js), and [the regression tests](../test/settings-safety.test.js). The key change is the order of events, not the length of the helper functions.

## Reproduce the original defect conceptually

Suppose the accepted resume is “Built inventory APIs”. A save attempts to replace it with “Built billing APIs”, but the filesystem rejects replacement. If code first does `Object.assign(cache, changes)` and later writes the file, the UI or next provider call can observe the new resume even though disk still contains the old one. Restarting reverses the apparent save. Two representations now disagree about accepted state.

The regression injects a replacement failure into a disposable settings path. It does not make your real filesystem fail and never opens real Electron user data. Its assertions are behavioral:

```javascript
assert.throws(() => store.set({ resume: 'Rejected resume' }));
assert.equal(store.get('resume'), 'Accepted resume');
assert.deepEqual(fs.readFileSync(file), before);
```

Those assertions establish both memory and disk behavior. Merely checking that `renameSync` was called would not establish that the user still has a consistent accepted value.

## Implement the acceptance boundary

The new store obtains the accepted revision, then calls `JsonFile.commit`. Inside the exclusive writer lease, it reads and decodes current accepted settings, merges the supplied changes into a detached object, validates it, and prepares its encrypted representation. Nonempty secrets require available encryption. An encryption failure aborts before replacement; there is no fallback that silently writes plaintext.

The shared file layer validates the draft, serializes bounded JSON, exclusively creates a unique temporary file beside the target, writes and flushes it, and replaces the accepted path. Only after this call returns does the settings service publish its new cache. Returned objects are detached so a caller cannot mutate storage simply by retaining an array reference.

The ordering can be summarized as:

```text
read accepted revision → lease → reread and compare → private draft
→ validate and encrypt → write temporary → replace → publish cache
```

Do not move publication earlier “for responsiveness.” The renderer can show a saving state without pretending the draft has already become accepted state.

## Explain the additional regressions

Nested read tests mutate values returned from `get` and `all`; accepted settings must remain unchanged. Corruption tests compare exact bytes before and after a read error; no implicit rename or reset is allowed. An unreadable existing file must not become empty writable defaults. A decryption failure preserves the stored encrypted value and reports a recovery problem. A stale writer cannot overwrite a newer accepted file. Finally, simply reading a legacy plaintext key never rewrites that file; migration occurs only on a subsequent explicit successful save.

The later temporary-file regression in [json-file.test.js](../test/json-file.test.js) checks another ownership boundary. If exclusive creation fails, cleanup must not unlink the candidate path because this operation never acquired it. The implementation assigns its cleanup-owned `temporary` variable only after `openSync(..., 'wx')` succeeds. It also preserves the original creation error rather than replacing it with a cleanup error for a nonexistent path.

## Carry the fix into the interface

The renderer now sends a revision and changed fields. It displays credential presence, keeps password inputs blank, preserves omitted keys, and uses explicit clear checkboxes. Failed saves retain the draft and disable another save until accepted settings are reloaded. The main window can still open with a temporary display preference when settings cannot be read, allowing the renderer to show the storage error instead of silently quitting or presenting a ready state.

This worked change stops short of claiming every possible filesystem failure is solved. A failure after replacement may produce an uncertain result, and manual recovery remains deliberate. That limitation is exactly why interface state and storage state must be designed together.
'''
docs['04-TESTING-AND-DEBUGGING.md'] = '''# Testing and debugging observable behavior

Run `npm test` from the project root. The [test launcher](../verification/run-tests.js) enumerates only current `test/*.test.js` files; original snapshots cannot accidentally run because they end in `.txt`. The suite uses Node's built-in test runner and temporary directories. No npm install, API key, microphone, Electron installation or provider account is required for these checks.

Run `npm run syntax` separately to parse source and verification JavaScript. Syntax checks catch malformed code but do not establish a lifecycle rule, successful write, accessible form or safe retry behavior. Keep those claims tied to behavioral evidence.

## Choose the smallest useful test layer

| Layer | Example in this repository | What it establishes |
| --- | --- | --- |
| Domain with real temporary file | [practice.test.js](../test/practice.test.js) | Resource rules and persisted results |
| File fault injection | [json-file.test.js](../test/json-file.test.js) | Accepted bytes survive tested failures |
| Actual HTTP | [practice-http.test.js](../test/practice-http.test.js) | Headers, body limits, auth and response behavior |
| Mocked Electron sender | [ipc.test.js](../test/ipc.test.js) | Controller rejects untrusted frames and handles cancellation |
| Real journal browser | [verify_browser.py](../verification/verify_browser.py) | Forms, navigation, drafts and visible accepted state |
| Mocked desktop bridge browser | [verify_renderer.py](../verification/verify_renderer.py) | Settings form and error/cancel wiring |

Use fault injection when real failure would be unreliable or risky. Replacing one fixture's `renameSync` with a throwing function lets a test assert that disk bytes and accepted state remain unchanged. Restore any patched global in `finally`, and use dedicated fixture state. Never point a corruption exercise at an actual learning journal you want to keep.

## Run optional browser checks

Use a separate Python environment if needed. Install [the optional browser requirement](../verification/requirements-browser.txt), provide an installed Chromium executable or install Playwright's Chromium, and pass a new evidence directory:

```powershell
python -m pip install -r verification/requirements-browser.txt
python -m playwright install chromium
python verification/verify_browser.py verification/browser-evidence-01
python verification/verify_renderer.py verification/browser-evidence-renderer-01
```

An existing evidence directory is refused so a failed run remains inspectable. `ASTRA_BROWSER_EXECUTABLE` can select an already available Chromium binary. The journal fixture creates a temporary workspace, communicates its synthetic token directly to the harness, and closes its server before removing owned files. Its token is not a usable credential for a real journal.

## Debug a stale edit

Open the journal in two tabs, sign in to both, and edit the same profile. Save the second tab first. Saving the first tab should produce a conflict and retain the typed value. Inspect the first request's `If-Match` header and compare it with the revision returned by a new detail read. The important question is not “why did fetch fail?” but “which accepted state did this draft assume?”

Choose review, examine accepted fields and your changed fields, and retain your changes deliberately. An untouched role should adopt the other tab's updated role while your edited name remains a draft. The browser regression checks this precise distinction. Automatically replacing every field with the stale form would silently lose another user's change even if the subsequent HTTP response succeeded.

## Debug an uncertain response

The browser harness can let a real PATCH finish, then abort delivery of its response. The correct visible result is a retained draft, blocked retry and review action. After review, the editor recognizes when its changed value is already accepted and reports no changed fields instead of submitting again. This tests a realistic distributed-systems boundary even on localhost: server completion and client knowledge are different events.

## Capture evidence carefully

Record the failing input, expected invariant, actual state, and smallest reproduction. Include accepted file bytes or revision when relevant, but avoid printing bearer tokens, provider credentials, resumes or private answers. Screenshots in [verification](VERIFICATION.md) use synthetic data. A passing mock encryption test means the application handles adapter success and failure; it does not prove Windows encryption works on a user's profile. Likewise, a Chromium renderer fixture does not prove native capture, Electron packaging or provider compatibility.
'''
docs['05-PRACTICE.md'] = '''# Practice: build mid-level CRUD judgment

Do these exercises in order using a disposable journal. Each asks for a concrete artifact and a failure case. Keep your implementation small enough to explain. Consult [the solution guide](06-SOLUTIONS-AND-REVIEW.md) after writing a prediction or first attempt, and use [the source map](01-CODEBASE-MAP.md) to find the correct boundary.

## Exercise 1 — Explain an entire practice session

Create profile “Inventory developer”, a shared question about input validation, and a planned session. Try to create an attempt before starting the session through the API or a domain test. Predict the rejection. Start the session, create an attempt, leave its score blank, and try completion. Then score it zero and complete it. Deliver a short trace containing the resource IDs, transition, relevant rule and observed result. Use synthetic IDs in anything you share.

Acceptance: you can distinguish a missing assessment from a low assessment. You can explain why a disabled or filtered UI control is insufficient protection and point to the service rule that handles a direct HTTP caller.

## Exercise 2 — Add an optional practice question hint

Propose a `hint` field with a bounded length and default empty string. Before editing code, identify every affected contract: create default, PATCH allowed fields, persisted-state validation, browser field, tests, and possibly question snapshots. Decide whether historical attempts should preserve the hint used at the time. Write your decision before adding it to the snapshot.

Acceptance: an omitted PATCH preserves the hint, an empty string clears it, an overlong value is rejected without changing accepted bytes, and an old file without the new optional field has an explicit compatibility policy. This is an exercise, not a feature already implemented in the delivered app.

## Exercise 3 — Test reference changes deliberately

Create two profiles, a question assigned to the first, and a session assigned to the second. Attempt to use that question in the second session. Then create a shared question and repeat. After a question has an attempt, try moving it to a different profile. Explain why preserving the attempt snapshot alone does not automatically make every relationship change acceptable.

Acceptance: add a focused test for one forbidden association and one allowed association. Assert that rejected operations leave both the resource collections and the activity history unchanged. Avoid a test that merely repeats the same validator expression with different syntax.

## Exercise 4 — Reconcile two writers

Use two tabs to edit different fields of the same profile. Save one, then the other. Before choosing review, record which values belong to the accepted record and which belong to the local draft. After choosing “Use this version and keep my changes,” verify that only your changed fields overlay the newly accepted record. Save, reload, and inspect the final result.

Acceptance: explain the conservative consequence of a global file revision when the other tab changes an unrelated question. Propose per-record revisions as a future design, then explain how deleting a referenced record still requires a transaction across related data. Faster conflict handling must not weaken referential integrity.

## Exercise 5 — Design recovery before implementing import

Export the journal and separately copy its private data file while the server is stopped. Compare their top-level fields without revealing tokens or answers. The export intentionally excludes authentication internals and activity. It is not an automatic replacement for the private store. Write a recovery plan for malformed JSON, an unreadable file, a lost token, and an orphaned lock.

Acceptance: the plan never silently resets a workspace or blindly deletes a lock. It identifies the file owner, stops writers, preserves evidence, validates a repaired copy, and explains how a new token or import would need an explicit new feature. Do not invent an existing reset command.

## Exercise 6 — Propose a database migration

Sketch tables for profiles, questions, sessions, attempts and activity. Mark nullable references and snapshot fields. Explain where unique profile names, immutable associations and session completion rules would run. Write one transaction sequence for creating an attempt and one for deleting a question. Include the stale revision policy and the user-visible error.

Acceptance: your proposal handles foreign keys and business rules together, includes migration and backup planning, and does not claim that changing JSON calls to SQL automatically solves retries. Add a separate design for durable operation IDs if you want safe creation retries after lost responses.

Finish with a short review demonstration: one normal action, one rejected action, one concurrency conflict, and a statement of what your evidence does not cover. That combination is a stronger mid-level signal than adding many untested form fields.
'''
docs['06-SOLUTIONS-AND-REVIEW.md'] = '''# Solutions and review reasoning

Use these explanations to assess your reasoning, not as a script to memorize. A good review ties a rule to its user consequence and then to evidence. Reference [domain.js](../src/practice/domain.js), [the browser editor](../src/practice/ui/app.js), and [the domain tests](../test/practice.test.js) while comparing your work.

## Session and assessment solution

A new session is planned because creating its metadata is different from starting practice. Attempt creation requires `in_progress`. Completion requires at least one attempt with a nonempty answer and a non-null score on every attempt. Zero passes the assessment requirement because it means “assessed at the lowest score”; null means “not assessed.” A reviewer should reject `if (!score)` because it collapses those meanings.

Completed sessions protect their attempts from edits and deletion. Reopen the session before revising work. This deliberate transition makes historical changes visible in activity rather than allowing records to drift beneath an apparently finished session. The existing code is still a local learning model, not a regulated audit system; its activity buffer retains only the latest 1,000 entries.

## Optional hint solution outline

Add the proposed field to the question whitelist and create defaults. Validate type and size on direct calls, not just through an HTML maxlength. Add the form definition so it participates in `values`, `changes` and draft comparison. Decide whether a hint is part of the historical question experience. If yes, extend snapshot construction and its persisted validation with an explicit compatibility strategy for old attempts.

Tests should cover create omission, PATCH omission, explicit clearing, oversized rejection with unchanged state, and reading an existing file. A test that merely checks a new input element exists is insufficient. This guide describes an exercise; the current app does not already provide hints or a migration system.

## Reference solution

The first profile's question cannot be attached to the second profile's session. A shared question can. Once a question has been used, its profile association cannot be changed even though wording snapshots remain stable. A snapshot preserves selected historical content, while the association still determines current domain meaning and filtering. Keep these responsibilities separate in your explanation.

For deletion, remove attempts while their sessions are in progress, then remove sessions and questions before removing the profile. The application rejects references instead of quietly cascading. A future cascade design would need a preview, explicit scope, transactional implementation, and tests that count every removed record. Removing only the visible parent from a list is not proof that related state remains coherent.

## Concurrent edit solution

Suppose the original profile is `{name: 'A', targetRole: 'Junior'}`. Tab one changes the name to B; tab two changes the role to Mid and saves. Tab one's old revision fails. The review UI retains the delta `{name: 'B'}`, reads the latest accepted record, and presents `{name: 'A', targetRole: 'Mid'}` for comparison. After explicit acceptance, the editor becomes `{name: 'B', targetRole: 'Mid'}` with the latest revision, still unsaved.

The important property is the delta. Overlaying the entire stale form would restore the obsolete Junior role. A reviewer should trace both typed values and raw form values: the code uses typed values for API changes and raw values to detect unsaved edits. This prevents blank numeric inputs and checkboxes from being compared carelessly.

## Recovery and database solution

Export is a sharing copy of practice records, not a complete operational backup. A private backup preserves the complete data file but must be protected. Corruption and lock failures require stopping writers and investigating ownership. The app provides no token-reset or import command, so your recovery plan must acknowledge that limitation rather than suggesting an undocumented action.

In a relational redesign, use foreign keys for existence and transactions for multi-record invariants. Attempt creation reads the session state, validates the question scope, inserts the snapshot, and records activity in one transaction. Session completion checks all attempts under a concurrency policy that prevents a competing edit from invalidating the result. Per-record versions reduce false conflicts, while transaction isolation handles related writes. Durable operation receipts are a separate concern from database atomicity.

## Review checklist in prose

Ask the author to demonstrate an accepted write, invalid input, a stale revision and an uncertain response. Check that unknown fields fail visibly, booleans and zero survive correctly, and rejected operations preserve accepted state. Confirm that credentials are absent from public settings and export. Read the tests' fixture setup before trusting the scope of their evidence. Finally ask which behavior remains untested on the actual desktop runtime. A precise limitation is more useful than an unsupported claim of production readiness.
'''
docs['07-TRACE-LAB.md'] = '''# Trace lab: explain the boundary at every step

This lab turns source reading into a repeatable debugging skill. Use [the server](../src/practice/server.js), [domain service](../src/practice/domain.js), [file store](../src/shared/json-file.js) and [browser state](../src/practice/ui/app.js). Keep a trace table with columns for input, accepted revision, rule, output and side effect. Do not record actual access tokens in the table.

## Trace A — A successful attempt

First create a profile, a matching question and an in-progress session through the UI. Read `/api/bootstrap` in browser developer tools and identify the session and question IDs. Its compact references support form choices; it does not return the entire authentication object or every answer. The attempt form chooses a session and filters active questions to the matching profile plus shared questions.

Submit an answer and numeric score. The browser serializes the form into JSON and sends POST with authorization and the quoted accepted revision. The server checks the request envelope and bounded body, authenticates the caller, recognizes the resource route and passes the operation to the service. The service holds the writer lease while checking current session state and question scope. It creates an ID, timestamps, a question snapshot and an activity entry containing action and field names.

After the file replacement succeeds, the response contains the accepted attempt. The browser then reloads list, bootstrap and detail state. Locate the moment `baseRaw` changes: that determines whether leaving the page is treated as abandoning an unsaved draft. Explain why an accepted response followed by failed refresh must not be labeled a rejected write.

## Trace B — A rejected completion

Leave an attempt's score blank and try completing its session. The browser may submit valid JSON with a valid revision; the operation still fails because the domain transition is invalid. Follow the exception back through HTTP error mapping and the notice area. Check accepted file bytes and activity count with a disposable fixture or focused test. Neither should change.

Now set score to zero and complete the session. The difference is domain meaning, not truthiness. State the exact invariant: each attempt must have a written answer and an assessed score. Avoid an explanation such as “the score must be positive,” because that is false for this implementation.

## Trace C — Lost acknowledgement

The [browser harness](../verification/verify_browser.py) forwards an actual PATCH to the server, waits for the accepted response, then aborts delivery to the page. Draw two timelines. On the server timeline, replacement completed. On the client timeline, fetch failed before the application received a readable response. Both timelines are true.

The editor marks the outcome uncertain, retains the draft and requires review. A new GET can show the submitted value already accepted. For an update, accepting that version may leave no changed fields. For a creation, there is no durable operation receipt; the user must inspect/search current records before deliberately retrying. Explain why a generic retry loop would be unsafe for the latter case.

## Trace D — Desktop settings and cancellation

Read [the preload bridge](../src/preload.js) and [IPC controller](../src/main/ipc-controller.js). `settings:get` returns public settings and credential presence. `settings:set` requires a revision plus allowed changes. Trace an explicit `alwaysOnTop: false` through validation, accepted persistence, then the window effect. If that final effect fails, persistence may already have happened; the renderer requires reload rather than guessing.

For a recording request, identify the exact trusted window/frame checks and WAV envelope checks. An AbortController spans transcription and answer generation. Cancel, renderer destruction, process loss or navigation abort the active request. The controller rechecks current ownership before publishing text or chunks. Provider retry code also checks cancellation after its backoff, preventing a cancelled operation from starting another upload simply because a timer ended.

The renderer-only test exercises the cancel button with a synthetic bridge. It does not capture media. The IPC test exercises a synthetic sender and providers. Neither establishes that native Windows capture or actual provider cancellation works end to end.

## Your final explanation

Give a five-minute demonstration with one trace from each family: domain rejection, stale writer, uncertain response and privileged desktop boundary. For each, state what was accepted, what the user knows, and what evidence supports the statement. Finish by naming one future improvement, such as durable creation receipts, and identify the additional tests needed before claiming it works.
'''
docs['VERIFICATION.md'] = '''# Verification, boundaries and recovery

This project was improved in an isolated staged copy before applying a finite set of changes to its original folder. Original code snapshots are retained in [docs/original](../docs/original). Tests use synthetic data and disposable files. No real Electron user settings, provider credentials, live audio, external accounts or provider calls were used.

## What the evidence means

The original baseline had 73 passing Node tests. Eight added settings regressions all failed against the original implementation; they then passed after repair. The final suite contains 120 passing tests, covering original audio/prompt/provider behavior with fixtures, settings safety, trusted IPC, shared file persistence, journal domain rules and real loopback HTTP behavior. Repeated clean-copy runs are repeated verification of these tests, not additional distinct test cases.

Browser and fresh-setup results are recorded in [verification-results.json](verification-results.json). The real journal browser harness exercises sign-in, pagination, CRUD, snapshots, stale edits, accepted writes with lost responses, lifecycle restrictions, export, deletion order and narrow-screen layout. The separate desktop renderer harness uses a mocked preload bridge and is labeled accordingly. Screenshots, when linked in the results, contain synthetic learning data.

Run `npm test` and `npm run syntax` for local checks. Optional browser instructions are in [testing and debugging](04-TESTING-AND-DEBUGGING.md). The browser scripts require a new evidence directory and close only their own server/browser fixture. A failure artifact is retained rather than overwritten. The setup check uses a fresh source copy, runs the real setup and server CLI, verifies authenticated access and static assets, and checks that setup refuses replacement of the existing file.

## Accepted changes and remaining limits

The journal implements profiles, questions, sessions and attempts with strict mutation fields, typed validation, reference protection, snapshots, lifecycle rules, server search/pagination and credential-free export. Writes use a global byte revision and exclusive local writer lease. Validated JSON is written to a same-directory temporary file and replaced; the application does not claim distributed storage, power-loss certification, automatic stale-lock recovery or durable operation receipts.

The entire practice file is limited to 8 MiB. Collections are bounded at 200 profiles, 2,000 questions, 2,000 sessions and 5,000 attempts. Activity retains the latest 1,000 entries. HTTP mutation bodies are bounded at 128 KiB. These limits make the local implementation inspectable; they are not a performance benchmark or a scalability promise. Standard JSON parsing accepts duplicate property names using its normal last-value behavior; duplicate-key rejection was not added.

Persisted schema checks cover structure, types and references but are not a comprehensive forensic validator for arbitrary hand-edited history. There is no account management, token reset, import workflow, multi-owner authorization or encrypted practice-answer database. The bearer token is high entropy and stored as a hash; protect the token and private files. The server binds loopback and validates request host/origin. Do not expose it as a public multi-user service without redesign.

Desktop settings now preserve corrupt or undecryptable data, reject silent plaintext fallback, publish the cache after accepted replacement, and require revisions through IPC. Native Electron, Windows encryption, capture, live provider behavior and the Windows installer were not run. Existing Electron dependencies were retained, not advertised as current. The streaming provider parser and response-size behavior have not received a full production hardening pass.

## Recovery is explicit

If a settings or practice file cannot be read, stop its writers and preserve a private copy before investigation. Distinguish malformed bytes, missing file, permission failure and encryption failure. Never replace an unreadable file with empty defaults merely to make the screen load. Test repair on a copy first and validate it before deciding to restore it.

An orphaned `.lock` requires confirming the owning process is gone; this app never steals it by age. A cleanup error after replacement may mean a write was accepted, so review current state before retrying. Export omits authentication and history and is not an automatic restore format. Losing a token is not solved by rerunning setup: setup deliberately refuses to overwrite an existing workspace. A reset/import mechanism is future work requiring its own explicit design and tests.

For the platform rationale behind protected desktop messages and credential storage, consult Electron's [IPC guide](https://www.electronjs.org/docs/latest/tutorial/ipc), [security guidance](https://www.electronjs.org/docs/latest/tutorial/security), and [safeStorage reference](https://www.electronjs.org/docs/latest/api/safe-storage). Those references explain platform APIs; the local results establish only the behavior actually exercised here.
'''
for name, text in docs.items():
    assert len(text.split()) >= 250, name
    (C/name).write_text(text, encoding='utf-8')
print({name:len(text.split()) for name,text in docs.items()})
print('Total course words:',sum(len(text.split()) for text in docs.values()))
