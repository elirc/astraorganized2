from pathlib import Path
P=Path(__file__).resolve().parent/'stage/092c5e5b7052';D=P/'astraupskill';D.mkdir(exist_ok=True)
def doc(name,text): (D/name).write_text(text.strip()+'\n',encoding='utf-8')
doc('README.md',r'''
# Collaborative documents: CRUD metadata meets real-time editing

This course uses the actual React, TypeScript, Node, WebSocket, and Yjs implementation in this folder. You will manage document identity and titles through HTTP while editing document content through a collaborative protocol. These are two different consistency problems, and the project makes that distinction visible instead of calling every update a generic save.

The starting source did not match its README and tests. The server used CommonJS `require` inside an ES-module package and imported a server helper path that the installed client library no longer exposed. The React app had a single fixed room, while the tests expected room selection, presence, tools, and document management. The delivered work implements those paths and adds explicit metadata CRUD, persistence, validation, and failure tests.

## Start locally

Use a Node version compatible with the checked-in lockfiles. Delivery verification used Node 22.16.0 and npm 10.9.2. From the project root:

```powershell
npm.cmd ci
npm.cmd ci --prefix client
npm.cmd ci --prefix server
npm.cmd run dev:server
```

In a second terminal, run `npm.cmd run dev:client` and open `http://127.0.0.1:5173`. The server defaults to loopback port 1234 and stores document records in `server/data`. To use a separate learning directory, set `DATA_DIR` in the server terminal before starting it. The sample environment file is a reference; Node's entrypoint does not automatically load it.

Create or join a room using a short ID such as `learning-notes`. The UI creates a new document if that ID is unused, or opens the existing document. Open a second tab and join the same room. Type in either editor and observe the other tab. Rename the title, cancel a deletion, then use a disposable room to try confirmed deletion. A deleted ID stays reserved so an old reconnecting client cannot recreate it with stale content.

Run `npm.cmd run test:server` for backend cases. Run `npx.cmd playwright install chromium` once for the matching browser, then `npm.cmd run verify` for backend tests, lint, TypeScript/build, and browser tests. Browser tests use separate ports and a test data directory; see the [verification guide](VERIFICATION.md) for evidence and boundaries.

## Learning sequence

Read the [code map](01-CODEBASE-MAP.md), [concepts](02-CONCEPTS.md), and [worked changes](03-WORKED-CHANGE.md). Follow [testing and debugging](04-TESTING-AND-DEBUGGING.md) and the [trace lab](07-TRACE-LAB.md). Attempt the [practice ladder](05-PRACTICE.md), then use [solution guidance](06-SOLUTIONS-AND-REVIEW.md) to review your reasoning.

Your review should explain why metadata versions differ from Yjs updates, why persistence happens before broadcasting accepted content, why presence is temporary, and why a Live connection is not a receipt proving every local keystroke reached disk. This remains a local shared lab with no authenticated ownership or multi-process storage coordination. The next exercises turn those explicit boundaries into a mid-level CRUD web-service design.
''')
doc('01-CODEBASE-MAP.md',r'''
# Trace HTTP commands and WebSocket content separately

[server/index.js](../server/index.js) exports `createCollaborationServer` for tests and starts the production server only when run as the entrypoint. That separation lets tests use ephemeral ports and temporary directories without importing a module that unexpectedly binds port 1234. The factory owns the HTTP server, WebSocket server, document store, active rooms, and shutdown procedure.

The HTTP adapter handles health, document listing, create-or-open, get-by-ID, rename, and deletion. It bounds JSON request bodies, validates fields, checks configured browser origins, and maps known `DocumentError` outcomes to response status. Unexpected storage errors become a generic 500 response while the server logger receives the diagnostic. Origin checks are a browser access policy, not authentication; non-browser clients can still reach this local service.

[server/store.js](../server/store.js) owns persistent document records and live Yjs documents. Each file contains format version, safe ID, title, metadata version, timestamps, deleted flag, and a base64-encoded Yjs state update. Startup validates records and refuses corrupt data without replacing it. `create`, `rename`, `delete`, and `applyUpdate` persist a candidate before publishing it into live state. Temporary sibling files are renamed over their destinations after serialization succeeds.

`applyUpdate` first clones the current collaborative state into a candidate `Y.Doc`, applies the incoming update there, and checks encoded size. Only after persistence succeeds does it apply the update to the live document. The server then broadcasts the accepted update. The sender already has its local edit; this ordering protects the server and other clients from accepting a write that the server could not save.

The WebSocket adapter reads Yjs sync messages through the installed `y-protocols` and `lib0` APIs. Sync step 1 exchanges state vectors; step 2 and update messages carry missing document changes. Rooms are selected by validated path IDs and must already exist. Awareness messages represent temporary presence. Ownership tracking distinguishes new client state from harmless relayed echoes produced by standard providers.

[client/src/App.tsx](../client/src/App.tsx) manages HTTP metadata, room selection, a Yjs session, provider lifecycle, and React display state. One controlled textarea handler computes a prefix/suffix replacement and performs a Yjs transaction. A Y.Text observer updates React state for both local and remote changes. There is no competing native input listener or timer that suppresses a user's next input event.

Room cleanup aborts an unfinished metadata request and destroys the previous provider/document. The generation value supports rejoining the same room deliberately. Metadata actions use the current expected version; conflicts refresh the version while preserving the proposed title for review. Confirmed deletion disconnects clients and disables editing. [client/src/index.css](../client/src/index.css) supplies the existing responsive workspace styles plus command/status feedback.

[server/test/documents.test.js](../server/test/documents.test.js) exercises real HTTP, real WebSocket providers, Yjs convergence, files, failure injection, and separate-process startup. [tests/collaboration.spec.ts](../tests/collaboration.spec.ts) exercises the actual browser interface. [playwright.config.ts](../playwright.config.ts) starts isolated loopback services and refuses to reuse an unrelated running server.
''')
doc('02-CONCEPTS.md',r'''
# Versions, collaborative state, presence, and durable acceptance

A document has metadata and collaborative content. The title is an ordinary CRUD field: two people renaming it can overwrite each other's intent unless the write checks what version they read. The server requires an expected metadata version for rename and deletion. Two writes using version 1 produce one winner and one 409 conflict. Content updates do not increment that metadata version, so typing does not constantly invalidate a title editor.

```json
{"title":"Review notes","version":1}
```

That proposed PATCH body means “apply this title only if metadata is still version 1.” It is not a merge algorithm. On conflict, the browser keeps the proposed title and refreshes its expected version; the user decides whether to retry. A production UI could additionally show both titles side by side rather than relying only on the error message and refreshed document list.

Yjs content uses a different model. Edits carry identities and dependencies so compatible updates can be merged and replayed without treating every edit as a full-document overwrite. A state vector tells another peer which structures it already knows; sync responses send missing state. The two-client test inserts A and B concurrently and verifies convergence without losing either insertion. This does not prove every editing interaction, cursor position, or input method behaves perfectly.

The store validates incoming updates on a candidate document. It serializes that candidate before changing the authoritative live document or broadcasting to peers. If disk persistence fails, the live server state and other clients remain unchanged. The sender may still display its local edit and reconnect later. Consequently, the UI's Live label describes protocol synchronization, not a per-edit durable acknowledgment. Acknowledging committed revisions is a separate exercise.

Presence is ephemeral awareness state. Display names are user-controlled labels, not authenticated identities. The server tracks which connection introduced each awareness client ID so a new state cannot simply take over another active connection's ID. Standard providers also relay received awareness messages. Stale or identical echoes must be ignored before checking ownership of genuinely new state; otherwise ordinary clients can be disconnected merely for participating in the protocol.

Deletion needs a rule for old clients. Removing a file and allowing immediate ID reuse could let a reconnecting client push old content into a newly created room with the same name. The implementation persists a tombstone, hides the document from normal reads, closes active sockets, and permanently reserves that ID. This is a small explicit lifecycle policy. It consumes retained metadata and does not provide a restore feature.

Atomic file replacement keeps one record from being partially overwritten in ordinary tested failures. It does not coordinate two server processes, guarantee power-loss durability, authenticate users, or make the entire directory a transactional database. The synchronous store also blocks the Node event loop while encoding and writing state, which is acceptable for this bounded learning app but an important scaling exercise. Explain each boundary separately before describing the project as ready for a multi-user deployment.
''')
doc('03-WORKED-CHANGE.md',r'''
# Worked changes: restore startup, then make persistence authoritative

The first reproduction was simply starting `server/index.js`. Node reported that `require` was undefined because the package declares `type: module`. Changing a file extension alone would not have completed the repair: the old code also depended on an internal server-helper import that the installed `y-websocket` client package did not expose. The delivered entrypoint uses explicit ES-module imports and the installed sync/awareness protocol APIs.

The server factory separates construction from listening. Tests can import it, choose an ephemeral port, provide a temporary data directory, and close the exact resources they created. Running the file directly still starts the application. This small separation is useful in CRUD services because an import should not unexpectedly launch a production listener or touch a user's dataset.

The persistence change establishes a specific order of operations:

```text
decode incoming collaborative update
copy current Yjs state into a candidate document
apply and validate the candidate update
encode and persist the candidate record
apply the update to the live server document
broadcast the accepted update to connected peers
```

The failed-persistence test deliberately throws from the write boundary. The sender's local document already contains its attempted edit, but the server's live document, another client, and the saved bytes remain unchanged. This is more meaningful than asserting only that an exception occurred. A second test forces a real rename failure by placing a nonempty directory at the destination path inside a temporary fixture, then verifies preservation and cleanup.

Metadata gets an ordinary optimistic-concurrency contract. Rename and delete require the version returned by a metadata read. The store checks the expected value before writing, and increments the metadata version after accepted changes. Two concurrent rename requests using the same version produce one 200 response and one 409 response. Collaborative content edits use Yjs instead of incrementing this metadata version for every keystroke.

Deletion persists a tombstone before closing active room connections. Reads and joins then reject the deleted ID. This prevents stale clients from recreating the room after reconnecting. The file keeps lifecycle metadata with an empty persisted Yjs state; active in-memory objects are released through normal server shutdown/room cleanup rather than being treated as a user-visible restore feature.

A real integration test exposed another subtle defect during implementation: standard providers forward received awareness updates. Rejecting every update mentioning another connection's client ID disconnected legitimate peers. The server now ignores older or already-known state before evaluating ownership of a genuinely new state. Presence appears in both clients and disappears after disconnection in the passing test.

On the client, one controlled textarea path replaces the old combination of a native input listener, React onChange, and a timer guard. The old guard could skip a real input event while a remote update flag was still set. The current handler applies a bounded text difference in one Yjs transaction, and the observer updates React state. This does not solve every cursor or IME interaction; those remain explicit exercises. Read the [tests](../server/test/documents.test.js) and [browser scenarios](../tests/collaboration.spec.ts) to see which outcomes are actually verified.
''')
doc('04-TESTING-AND-DEBUGGING.md',r'''
# Test the protocol boundary with real peers

Run `npm.cmd run test:server` before browser tests. The backend suite uses Node's test runner, real HTTP requests, real `ws` sockets, standard `WebsocketProvider` clients, Yjs documents, and temporary files. It does not substitute an in-memory fake transport for collaboration. The factory lets every fixture use an ephemeral port and clean up its own clients and servers.

Several tests protect conventional CRUD behavior: create returns a readable Location, repeated create-or-open preserves the existing title, invalid IDs and bodies are rejected, split UTF-8 request chunks preserve a title, and competing metadata writes produce one winner. Deletion tests verify the persisted tombstone, missing-resource responses, and refusal to reuse the deleted ID.

The collaborative tests observe both peers. One inserts text, another receives it and appends more, and the first receives the combined result. Another inserts A and B concurrently and waits for convergence while asserting that both characters remain. A third room stays empty, proving the room identifier actually isolates protocol state. These are stronger than checking that a WebSocket opened successfully.

Failure tests inspect the state on each side of the boundary. When persistence fails, the writer's connection closes, the other client's text stays unchanged, and server memory and file bytes retain the previous state. Oversized or invalid updates are rejected before live mutation. A separate-process startup test loads previously accepted content through the actual entrypoint, so persistence is not inferred from rereading the same object.

For a presence failure, inspect the client IDs, clocks, states, and connection ownership map together. A standard provider can relay a peer's update. An identical or stale relay should not become a new ownership claim. The first presence test failed during implementation because this distinction was missing. Avoid debugging by simply disabling all validation: preserve the real protocol behavior and the ownership boundary.

For a UI failure, check the connection status before typing. Editing is disabled while the new room synchronizes. Inspect the current room, session generation, Y.Text value, and React textarea value. Room cleanup must destroy the previous provider and document, and an asynchronous import must still belong to the same live session before it replaces content.

Run `npx.cmd playwright install chromium`, then `npm.cmd run test:e2e`. The configuration starts loopback services on separate test ports and refuses to reuse an unrelated existing server. Test data uses `.test-data` by default; `WHITEBOARD_E2E_DATA_DIR` can point to a disposable directory. Delivery verification supplies a temporary directory explicitly. Browser traces and screenshots are retained for failures, with desktop/narrow evidence captured by the scenarios.

Finally, run `npm.cmd run verify` to combine backend tests, lint, TypeScript/build, and browser checks. Passing a build does not prove synchronization, and passing a synchronization test does not prove authenticated access or power-loss durability. Use the [verification record](VERIFICATION.md) to keep the executed scope distinct from the [future exercises](05-PRACTICE.md).
''')
doc('05-PRACTICE.md',r'''
# Practice ladder toward a durable multi-user CRUD service

These exercises extend the delivered local lab. They are proposals, not existing guarantees. Start with a behavior contract, write a failing test, implement one coherent change, and describe its limit before adding the next feature. Keep the original document files out of failure-injection experiments.

## 1. Show a useful metadata conflict comparison

When a title rename conflicts, display the latest server title beside the user's proposed title. Offer an explicit retry or discard action. Two tabs should read version 1; tab A saves, tab B conflicts, and tab B can inspect both values before deciding. Do not automatically overwrite the winner just because a refreshed version is now available. Preserve the user's draft if refreshing metadata also fails.

## 2. Add an acknowledged persistence status

Define a server acknowledgment that identifies accepted collaborative state or an application-level revision after persistence succeeds. Distinguish connected, synchronized, pending local edits, and durably acknowledged state in the UI. A lost acknowledgment must not duplicate content on retry. Test a server write failure and a response lost after a successful write. Do not equate receiving a sync step 2 message with proof that a later local edit is on disk.

## 3. Improve editor selection and composition behavior

Use Yjs relative positions or an appropriate editor binding to preserve selection around remote inserts. Test two clients editing near the same cursor, selection replacement, emoji, multiline input, and composition events. The current prefix/suffix diff is a useful small example, but it does not establish robust IME or cursor semantics. Keep the text model authoritative and avoid adding another independent DOM input listener.

## 4. Move document storage behind a durable repository

Replace synchronous whole-state file writes with a designed persistence strategy. Consider snapshots plus an update log, compaction, bounded history, and recovery after interruption. Define which operation publishes accepted state and when compaction can remove old updates. Test restart after a partially completed compaction. Merely changing `writeFileSync` to an unawaited async write would weaken the existing acceptance order.

## 5. Add authenticated ownership and sharing

Introduce users and document membership. Apply authorization to list, create, read, rename, delete, WebSocket upgrade, and subsequent content/presence handling as required by your revocation policy. A room ID is not a secret or an access-control mechanism. Test an unauthorized user who knows another document's ID, and a connected collaborator whose access is revoked. Origin allowlists and display names do not supply authentication.

## 6. Support multiple server processes deliberately

Choose where document authority lives and how processes coordinate updates, metadata versions, tombstones, and presence. Two independent in-memory maps writing the same JSON directory are not a shared transactional repository. Add tests where different processes receive competing rename requests and collaborative updates. Explain whether a database, broker, leader assignment, or another mechanism owns each consistency boundary.

## 7. Add lifecycle and operational controls

Design tombstone retention, export before deletion, document-size policy, and recovery tooling. If IDs may eventually be reused, introduce a generation identifier so old clients cannot attach stale content to a new document. Add metrics for rejected writes and persistence latency without logging document contents or user text. Demonstrate a corrupt-record recovery flow that preserves the original and produces a reviewable recovered copy rather than silently discarding it.

A mid-level review should trace one accepted edit and one rejected edit through browser state, transport, validation, persistence, broadcast, and acknowledgment. Include evidence from real adapters and explain what remains uncertain.
''')
doc('06-SOLUTIONS-AND-REVIEW.md',r'''
# Solution guidance: separate the guarantees before combining them

Use these notes after attempting the [practice ladder](05-PRACTICE.md). They describe possible next implementations. The delivered lab has metadata version checks and collaborative persistence, but no authenticated membership, durable edit receipts, multi-process coordination, or database-backed update log.

For metadata conflicts, keep three values distinct: the original version the user edited, the latest server title/version, and the user's proposed title. A conflict response or follow-up read can populate the comparison. Retrying should be a deliberate action that sends the reviewed latest version. If the refresh fails, preserve the proposal and explain that the latest server state is unavailable; do not pretend a stale version became safe.

For persistence acknowledgment, choose an identifier the client can correlate with its pending work. A server revision or accepted state-vector protocol needs a precise definition, especially when one update depends on another. Persist before issuing the acknowledgment. Test both failure before commit and loss of the acknowledgment after commit. The client must not infer success from a connected socket or erase pending local content simply because a timeout occurred.

For selection handling, a raw DOM offset is unstable when another user inserts text before it. Relative positions can anchor selection to collaborative structures. Translate between the editor's selection and the document model at appropriate lifecycle points, and test composition rather than assuming all input arrives as a simple keypress. A proper editor binding may be a better teaching extension than expanding a hand-written textarea synchronizer indefinitely.

For storage, define a unit of accepted state. An append-only update log can reduce full-snapshot write cost, but introduces compaction and recovery work. A safe compaction sequence writes a complete replacement snapshot and records which log entries it covers before removing redundant entries. If asynchronous writes are introduced, serialize or coordinate them so an older write cannot finish after a newer one and overwrite it. A faster event loop is not an improvement if it loses the persistence ordering guarantee.

For authorization, derive identity from a trusted session and enforce membership at every adapter. A successful WebSocket upgrade is not necessarily permanent authorization: decide how revocation affects connected clients and queued updates. Presence names remain display values. A browser Origin header can help constrain expected browser callers but cannot establish who owns a document.

For multiple processes, decide whether a document is assigned to one authority or can be edited through several coordinated authorities. Metadata compare-and-update needs a shared atomic boundary. Tombstones must propagate before a stale process accepts another update. Presence needs expiration and ownership semantics across processes. A shared filesystem alone does not provide those guarantees.

During review, ask for an actual sequence diagram of one accepted edit and one failed edit. Label local application, network send, server validation, durable commit, live-state update, broadcast, and acknowledgment. Then ask which steps can be retried and which IDs make retries safe. A strong answer distinguishes CRDT replay, HTTP metadata conflicts, request idempotency, and lifecycle generation checks rather than calling them all deduplication.

The final artifact should include a failing test that motivated each change, a passing real-adapter check, and a concise statement of limits. Keep document contents out of operational logs and use disposable fixtures for corruption tests. These are practical habits for reviewing CRUD services, not merely additional folders to add to the repository.
''')
doc('07-TRACE-LAB.md',r'''
# Trace lab: two clients, one document, and explicit conflicts

Start the backend and frontend using the [course setup](README.md). Choose a separate learning data directory for the server. Open two browser tabs and join the same unused room ID, such as `trace-notes-01`. Wait for Live in both tabs before editing. Change the display names to Alice and Bob and confirm that each tab shows both presence entries.

In Alice's editor, enter a heading and a short list. Bob should see both source and preview. Append a sentence in Bob's editor and observe Alice. The transport is WebSocket sync, while the preview is React rendering of local Y.Text state. Use developer tools to distinguish the HTTP document-create request from the binary WebSocket frames. Do not expect every frame to be a complete JSON document.

Rename the document to `Review notes` in Alice's tab. Bob still holds the metadata version from its earlier read. Enter a different title in Bob's tab and save it. The server should return a conflict rather than overwriting Alice's title. The UI preserves Bob's proposed title, reports the conflict, and refreshes the expected version. Review the current document list before deliberately retrying or choosing another title.

The same flow can be observed with PowerShell and a disposable ID:

```powershell
$base = 'http://127.0.0.1:1234'
$doc = Invoke-RestMethod "$base/api/documents" -Method Post -ContentType 'application/json' -Body '{"id":"trace-api-01","title":"First"}'
$renamed = Invoke-RestMethod "$base/api/documents/trace-api-01" -Method Patch -ContentType 'application/json' -Body '{"title":"Updated","version":1}'
# A second PATCH with version 1 now conflicts; inspect the HTTP 409 response.
Invoke-RestMethod "$base/api/documents/trace-api-01"
```

Use a fresh ID if it already exists or was deleted. Create-or-open does not rename an existing record, and deleted IDs are reserved. For deletion, use the current returned metadata version and only a disposable document. In the browser, first cancel the confirmation and verify the room remains live. Then confirm deletion: the other tab should show Deleted and disable editing. Rejoining the old ID should fail rather than restoring old content.

Try search/replace with a replacement containing `$&`. The First action should insert those characters literally, not interpret them as a regular-expression replacement token. Import a small Markdown file only after confirmation, then use Bold on selected text and inspect the sanitized preview. Download the result and compare it with the editor's source.

For restart evidence, wait until another client has received an edit, stop your own server, restart it with the same learning directory, and reopen the document. The automated suite also verifies accepted state through a separate Node process. Do not kill unrelated processes or use real document files for corruption experiments.

Finish by explaining what Live proves and what it does not. The server persists accepted state before broadcasting, but the UI has no per-edit disk receipt. A sender can hold an unaccepted local edit during a failed write. Read the [failure tests](../server/test/documents.test.js) before designing a misleading Saved indicator.
''')
(P/'README.md').write_text(r'''# Collaborative Markdown Editor

A local React/TypeScript and Node/Yjs learning app with real-time Markdown editing, document metadata CRUD, file persistence, presence, import/export, formatting, and sanitized preview. Start the detailed [CRUD upskilling course](astraupskill/README.md) for source explanations, worked changes, tests, and exercises toward a mid-level web service.

## Install, run, verify

Delivery verification used Node 22.16.0 and npm 10.9.2. Use the checked-in lockfiles:

```powershell
npm.cmd ci
npm.cmd ci --prefix client
npm.cmd ci --prefix server
npm.cmd run dev:server
```

In another terminal, run `npm.cmd run dev:client`, then open `http://127.0.0.1:5173`. The server defaults to `127.0.0.1:1234`. It stores records in `server/data` unless `DATA_DIR` is set. For an isolated learning dataset, set that environment variable before starting the server. Relative paths resolve from the server process's working directory; npm's server script runs inside `server`.

```powershell
npm.cmd run test:server
npx.cmd playwright install chromium
npm.cmd run verify
```

Verification combines backend tests, lint, TypeScript/build, and browser scenarios. Browser tests use loopback ports 24123/25173 by default and `.test-data` instead of normal document storage. Override `WHITEBOARD_API_PORT`, `WHITEBOARD_CLIENT_PORT`, or `WHITEBOARD_E2E_DATA_DIR` as needed. They refuse to reuse an unrelated running server.

## Document workflow

Join a room ID containing 1–64 letters, numbers, underscores, or hyphens. Joining creates a new document or opens the existing one. Two clients in the same room exchange Yjs updates. A document title is separate metadata and can be renamed with an expected version. Conflicting metadata edits return 409 and preserve the proposed title for review.

Deletion requires confirmation and the expected metadata version. It persists a tombstone, closes connected room clients, hides the document, and reserves the ID against reuse. Use a new ID for a new document. There is no restore feature.

## HTTP API

| Method and route | Behavior |
|---|---|
| `GET /health` | Process health response |
| `GET /api/documents` | Active document metadata list |
| `POST /api/documents` | `{id,title?}` creates or opens; 201 or 200 |
| `GET /api/documents/:id` | Metadata for one active document |
| `PATCH /api/documents/:id` | `{title,version}` optimistic rename |
| `DELETE /api/documents/:id` | `{version}` persists deletion; 204 |

Create returns a readable Location. Invalid input returns 400, missing/deleted documents 404, metadata conflicts or reuse of deleted IDs 409, oversized JSON 413, unsupported content type 415, and unexpected storage failures 500. WebSocket rooms use `ws://127.0.0.1:1234/:id` and must already exist.

## Configuration and boundaries

`HOST`, `PORT`, `DATA_DIR`, and comma-separated `ALLOWED_ORIGINS` configure the server. `VITE_SYNC_URL` configures the client and its derived HTTP API URL. The root `.env.example` is a reference; the Node entrypoint does not load it automatically. A client environment example is provided in `client/.env.example` for Vite.

The server validates candidate collaborative state and persists it before live mutation and broadcast. Whole-record writes use temporary sibling files and rename replacement. Corrupt startup stops without replacing rejected records. Presence is temporary and display names are user-controlled. Live means protocol synchronization, not a per-edit durable receipt.

This is a shared local lab with no authenticated document ownership. Origin checks are not authentication. Storage is synchronous and single-process; there is no distributed lock, database transaction, power-loss guarantee, full cursor/IME binding, or tombstone cleanup policy. See [verification](astraupskill/VERIFICATION.md) and [practice](astraupskill/05-PRACTICE.md) before extending it.

Docker scaffolding remains available through `docker compose up --build`, with the client exposed on port 8080. Docker execution was not verified in this environment. Local Node and Chromium checks provide the recorded runtime evidence.
''',encoding='utf-8')
(P/'client/README.md').write_text(r'''# Collaborative editor client

The client is the React/TypeScript UI for the project's document service. Read the [root setup](../README.md) and [source-based course](../astraupskill/README.md) first.

`src/App.tsx` owns room selection, metadata commands, the current Yjs/provider session, a controlled textarea, presence, Markdown tools, and sanitized preview. One input path updates Y.Text; its observer updates React for local and remote changes. Cleanup destroys the previous provider/document and aborts an unfinished room request.

From the project root, use `npm.cmd run dev:client`, `npm.cmd run lint`, and `npm.cmd run build`. `VITE_SYNC_URL` defaults to `ws://127.0.0.1:1234`; the HTTP API base is derived by replacing `ws` with `http`. Copy this directory's `.env.example` to `.env.local` only if you need a different local endpoint, then restart Vite. The backend must allow the browser's origin.

Metadata rename/delete use an expected version. Conflicts preserve the proposed title for review. Editing is disabled while a room synchronizes or a metadata command runs. A deleted room disconnects and cannot be recreated with its old ID. The Live status is not a per-edit disk acknowledgment.

Browser verification is defined in `../tests/collaboration.spec.ts` and started from the root. It exercises two-client synchronization, preview sanitization, room switching, metadata conflicts, deletion, import/formatting, and a narrow viewport. The current textarea implementation does not claim complete IME or remote-cursor preservation; those are explicit course exercises.
''',encoding='utf-8')
(P/'.env.example').write_text('''# Reference values; Node does not automatically load this file.
# Relative DATA_DIR is resolved from the server process working directory.
HOST=127.0.0.1
PORT=1234
DATA_DIR=./data
ALLOWED_ORIGINS=http://127.0.0.1:5173,http://localhost:5173,http://127.0.0.1:8080,http://localhost:8080
VITE_SYNC_URL=ws://127.0.0.1:1234
''',encoding='utf-8')
(P/'client/.env.example').write_text('VITE_SYNC_URL=ws://127.0.0.1:1234\n',encoding='utf-8')
doc('VERIFICATION.md',r'''
# Verification record and practical limits

The project was repaired and tested in an isolated copy before delivery. The original startup command failed immediately because CommonJS `require` was used in an ES-module package. The implementation now uses the installed protocol APIs, and the production entrypoint is exercised by a separate-process test. Original document data and generated dependency/build directories are excluded from the delivery manifest.

The environment used Node 22.16.0, npm 10.9.2, the three checked-in dependency lockfiles, and Playwright's matching Chromium 148.0.7778.96. Locked installs succeeded for root, client, and server. Verification passed **17 backend tests** using real HTTP, WebSocket providers, Yjs documents, temporary filesystem storage, injected persistence failures, an actual failed rename, and separate-process startup.

Backend coverage includes metadata create/read/list, validation, UTF-8 chunk boundaries, competing rename versions, stale deletion, persisted tombstones, room isolation, bidirectional and concurrent content convergence, server recreation, presence cleanup, active deletion, failed-write preservation, update limits, corruption rejection, and temporary-file cleanup. The first presence integration attempt failed because ordinary relayed awareness updates were treated as new ownership claims; the corrected behavior passes with standard clients.

Verification also passed **eight Chromium browser scenarios**, for **25 distinct tests total**. They cover two-client editing and preview, presence/tools/sanitization, a narrow viewport, rename/reload and cancelled deletion, confirmed deletion across tabs, room isolation with literal replacement text, stale title conflicts, and confirmed import with toolbar formatting. Lint, TypeScript checking, and the production build passed.

Visual review found clipped text labels caused by old icon-width toolbar CSS. The layout was corrected, the production build rerun, and the two affected desktop/narrow browser scenarios rerun successfully. The narrow test now checks that toolbar labels fit their buttons and the page does not overflow horizontally. These two reruns are additional verification of existing cases, not two new distinct tests. The final screenshots were inspected:

- [Desktop workspace](images/desktop.png)
- [Narrow workspace](images/narrow.png)

Central logs and structured results are retained under `astra-remaining-improvements/checks/whiteboard/`, with project delivery ID `092c5e5b7052`. The central report records finite file hashes and backups.

This remains a local shared lab. It has no authenticated ownership, membership revocation, database, multi-process coordination, durable per-edit acknowledgment, complete IME/remote-cursor binding, tombstone retention policy, or document-history UI. Browser origin checks and user-controlled display names are not authentication. Live reports protocol synchronization and does not prove every local edit reached disk.

Persistence uses synchronous whole-record writes and filesystem rename replacement. Tests cover ordinary local failures and restart behavior, not power-loss durability or every network filesystem. The sender may retain unaccepted local edits after a write failure and retry through reconnection. Tombstones prevent ID reuse but retain lifecycle metadata. Docker scaffolding was not executed because the daemon was unavailable. Keep these boundaries explicit when presenting the project or implementing the next CRUD web-service exercises.
''')
