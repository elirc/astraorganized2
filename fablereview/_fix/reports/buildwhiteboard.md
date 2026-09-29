# buildwhiteboard — fix report (B18)

Fable, 2026-09-18.

## Done
- review#1 App.tsx and server/index.js reformatted with prettier at 100 columns in the pipeline; 01 notes the width
- review#2 02 message-flow diagram (HTTP versioned metadata vs WebSocket sync/update/awareness/persist) with the live-vs-durable gap and a glossary box
- review#3 README uses install:all and moves the .env.example warning to the top of the section; review#4 both READMEs mark the Docker files as unverified scaffolding
- review#5 05 ticket 3 explains the callback form of replace with the $& example and names the browser scenario; review#6 ticket 5 has five concrete acceptance criteria (session-derived owner, 404 not 403, socket authorization, isolation tests)

## Skipped
- the Playwright suite was not run; the $& replace scenario is specified in 05 ticket 3 rather than added to collaboration.spec.ts

## Verification
- prettier (100 cols, single quotes) on client/src/App.tsx (198 -> 488 lines, no line over 200 chars) and server/index.js (199 -> 354); node --check server ok; temporary npm ci in server + npm test: 17/17; temporary npm ci in client + tsc --noEmit exit 0 + vite build ok; both node_modules removed

## Course/code consistency check
- The callback-form note describes the code as it is (App.tsx already uses text.replace(search, () => replacement) and split/join); ticket 5 criteria reference documents.test.js which exists; README install:all matches package.json.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (metadata version, conditional rename, tombstone, room, Yjs update, sync step 1 / state vector, sync step 2, durable acceptance, awareness / presence, envelope, DocumentError, shared text). Verified every term against the source before citing it: the files `server/store.js`, `server/index.js`, and the symbols and identifiers `checkVersion`, `rename(id, title, version)`, `deleted: true`, `delete(id, version)`, `roomFor(id)`, `applyUpdate(id, update)`, `sync.writeSyncStep1`, `sync.writeSyncStep2`, `if (store.applyUpdate(id, payload))`, `awarenessProtocol.Awareness`, `removeAwarenessStates`, `envelope(type, write)`, `DocumentError`, `doc.getText('markdown-content')`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 04, 06. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **04** - server/test/documents.test.js (two collaborative WebSocket tests)
- **06** - server/store.js (applyUpdate)

No source code was changed; only the chapter Markdown.
