# geminiorganized/LLM_Generated_Helper — fix report (B18)

Fable, 2026-09-18.

## Done
- review#1 the journal moved to practice-journal/ (own package.json: setup/start/test), root package.json describes the AI Call Assistant again with practice:*/test:practice scripts pointing at the new folder; README leads with the assistant and links the journal; astraupskill paths updated
- review#2 PARTIAL: domain.js is not split; 01 documents its four sections as the boundaries a split would follow (the physical split is left as practice)
- review#4 03 snippet is now the real test with the renameSync injection, the /replacement failure/ matcher and the restore
- review#5 "Which app am I in?" banners at the top of 02, 04 and 05
- review#3 08-PORT-TO-A-FRAMEWORK.md: three Fastify + SQLite routes reusing domain.js, with the removed/still-yours table

## Skipped
- review#2 domain.js was not physically split (its four sections are documented in 01 as the boundaries; left as practice)

## Verification
- after the move (src/practice -> practice-journal/src, tests + fixture -> practice-journal/test, requires rewritten): npm run test:practice (node --test practice-journal/test/*.test.js) 20/20 passed via junctioned stage node_modules; root npm test (verification/run-tests.js, the Electron suites): 100/100 passed; practice-journal/package.json test script fixed to a glob after Node 22 rejected the bare directory; junction removed

## Course/code consistency check
- README leads with the AI Call Assistant and links practice-journal/; astraupskill paths and the 03 snippet point at files that exist after the move; 08 imports domain.js from the new location.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (accepted state, revision, If-Match / ETag, conditional commit, writer lease, atomic replacement, required versus default, immutable field, reference rule, snapshot, state transition, owner token). Verified every term against the source before citing it: the files `src/main/settings-store.js`, `src/shared/json-file.js`, `practice-journal/src/server.js`, `practice-journal/src/domain.js`, and the symbols and identifiers `read()`, `accepted`, `digest(bytes)`, `JsonFile.read`, `revision(request)`, `ETag`, `commit(expectedRevision, mutate)`, `openSync(lock, "wx")`, `.tmp`, `renameSync`, `REQUIRED`, `DEFAULTS`, `payload()`, `IMMUTABLE`, `references(state, kind, next, previous)`, `questionSnapshot`, `profileSnapshot`, `references`, `createState`, `authenticate`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 06, 07. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **06** - practice-journal/src/domain.js (session transition and completion rule)
- **07** - src/shared/json-file.js (writer lease)

No source code was changed; only the chapter Markdown.
