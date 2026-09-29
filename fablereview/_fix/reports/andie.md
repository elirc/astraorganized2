# _Organized Desktop/12 Other Projects/andie — fix report (B17)

Fable, 2026-09-18.

## Done
- review#2 client.js attaches redacted GraphQL error and userErrors detail (field/code/message) to thrown errors via a shared redact() that masks shpat_ tokens and never includes headers; one test added
- review#1 .prettierrc (100 cols, single quotes) + format / format:check scripts; planner.js, client.js and migration.test.js reformatted in the pipeline (see report)
- review#2 04 "Safe error detail" section
- review#3 10-WHAT-THIS-LOOKS-LIKE-IN-A-WEB-APP.md (plan/apply routes with a hash compare-and-set, cursor pagination with a stall guard); review#4 REPO-CONTENTS.md; review#5 VERIFICATION names the backup location for the token revocation

## Skipped
- (none)

## Verification
- prettier (from .prettierrc: 100 cols, single quotes) rewrote planner.js 105->313, client.js 67->199, migration.test.js 68->620 lines plus the CLI entry; npm run check (node --check x3) ok; node --test test/*.test.js: 43/43 passed (42 delivered + 1 redaction test); prettier --check: all files formatted

## Course/code consistency check
- The redaction test exercises the real createClient with a fake fetch; 04 "Safe error detail" describes detailed()/redact() as implemented; VERIFICATION names the backup path where the token copy was found (already redacted by this review, revocation still pending).

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md`, before the first existing second-level heading: a prerequisites line naming what a learner should already know (and, where one exists, the sibling course that comes first) plus a 12-term glossary table whose third column names a real file, function, table or header in this project. Every location was checked against the source before it was written: scripts/lib/planner.js (normalizeSnapshot, buildPlan operations/conflicts, applyPlan status and failed), scripts/lib/client.js (exportSnapshot, pages, createRemote userErrors) and scripts/populate-metaobjects.js (journalWriter, newOutput).

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `04-TESTING-AND-DEBUGGING.md` — quoted from `scripts/lib/client.js:7-20` (`redact`/`detailed`)
- `06-SOLUTIONS-AND-REVIEW.md` — quoted from `scripts/lib/planner.js:4-15` (`stable`/`canonical`/`hash`)
- `07-TRACE-LAB.md` — quoted from `scripts/lib/planner.js:156-171` (`buildPlan`)
