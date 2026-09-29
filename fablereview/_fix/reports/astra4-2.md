# astra4.2 — fix report (B18)

Fable, 2026-09-18.

## Done
- review#1 08-SERVER-PORT.md + service/ starter (node:http + node:sqlite server, schema with version and title CHECK, two node:test cases incl. competing PUTs -> one 200 one 409)
- review#2 01 "Reading the dense style" with a prettified renderPresets excerpt and the statement that the compression is deliberate
- review#3 04 documents the Chromium-channel prerequisite and the --grep-invert fallback with what 9/10 means; review#5 VERIFICATION maps the ten scenarios to the behavior each guards
- review#4 three explicit predict boxes (02: applyMessage returns/throws; 03: the stale form) with answers in 06

## Skipped
- (none)

## Verification
- service: npm test (node --test test/*.test.js, node:sqlite in-memory): 2/2 passed incl. the competing-PUT case (one 200, one 409); root npm test: 39/39 unchanged; the bare-directory script was corrected to a glob after Node 22 rejected it

## Course/code consistency check
- 08 mirrors the applyMessage error sentence the service returns; VERIFICATION scenario table generated from the spec titles; 06 answers were checked against applyMessage in extension/model.js (empty patch, revision check before action).

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md`, before the first existing second-level heading: a prerequisites line naming what a learner should already know (and, where one exists, the sibling course that comes first) plus an 11-term glossary table whose third column names a real file, function, table or header in this project. Every location was checked against the source before it was written: extension/model.js (normalize, applyMessage with expectedRevision, parsePreview), extension/state.js transition, extension/background.js (reconcile, synchronize warning) and service/schema.sql plus the If-Match handling in service/server.js.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `04-TESTING-AND-DEBUGGING.md` — quoted from `package.json` scripts + documented grep-invert browser run
- `06-SOLUTIONS-AND-REVIEW.md` — quoted from `extension/model.js:67-76` (`applyMessage` preset branch)
- `07-TRACE-LAB.md` — quoted from `src/app.js:128-135` (`saveSettings`)
