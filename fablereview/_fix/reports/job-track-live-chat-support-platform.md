# _Organized Desktop/08 App And Product Projects/job track/live-chat-support-platform — fix report (B17)

Fable, 2026-09-18.

## Done
- review#1 mark_read range read + receipt writes are one db.transaction; 14th test pins the read-through boundary; 03 documents it as the seventh defect
- review#2 UTF-8 BOM stripped from 9 files; review#3 .nvmrc, engines, POSIX block; review#4 02 glossary (20 terms) and README prerequisite gate; review#5 npm run reset:db and the README note

## Skipped
- (none)

## Verification
- temporary npm ci in server (171) and client (97), then npm test at the root: 14/14 passed (13 delivered + the new read-through boundary test) with the mark_read transaction change; node_modules removed

## Course/code consistency check
- 03 seventh-defect section describes the exact block now in socket.js; the README reset:db note matches the script; glossary terms are the ones the chapters use.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 03, 06. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **03** - server/src/socket.js (mark_read transaction)
- **06** - server/src/socket.js (addPresence/removePresence)

No source code was changed; only the chapter Markdown.
