# All 20 projects: implementation and learning report

Completed September 8, 2026. The second batch is applied to the ten original Desktop project folders, with detailed junior SWE courses in each project's `astraupskill` folder. This report also consolidates the first batch and the earlier inventory/planning work.

## Delivered totals

- **20 projects** improved across two batches; **322 project files** added or changed.
- **180 learning files**, approximately **105,436 words** including executable source and test excerpts.
- **137 automated test cases passed** across the two batches, subject to the first-batch retry detail below.
- Second batch: **171 files**, **90 learning files**, **51,580 words**, **21 test cases**, **4 client builds**, **3 TypeScript checks**, **10 Chromium interaction checks**, and a **Knex migration/seed setup check**.

Word counts describe the delivered material, not a required reading quota. Each course focuses on explaining and independently reproducing one useful engineering improvement.

## Project-by-project delivery and study order

| Order | Project / course | Implemented improvement | Test cases |
|---|---|---|---:|
| 1 | [JS1/task-board](../../JS1/task-board/astraupskill/README.md) | Persistent one-level task undo, including reload and failed-write handling. | 3 |
| 2 | [JS1/contact-book](../../JS1/contact-book/astraupskill/README.md) | Case-insensitive duplicate-email validation that permits editing the same contact. | 2 |
| 3 | [JS1/focus-timer](../../JS1/focus-timer/astraupskill/README.md) | Deadline-based countdown, accurate pause/resume and a single completion log. | 3 |
| 4 | [finance-dashboard](../../finance-dashboard/astraupskill/README.md) | Validated expense editing with stable record identity and persisted totals. | 2 |
| 5 | [recipeweb](../../recipeweb/astraupskill/README.md) | Saved shopping quantities, keyboard-editable controls and consistent clipboard output. | 3 |
| 6 | [jobtrack](../../jobtrack/astraupskill/README.md) | Validated application JSON export/import with atomic replacement and failure feedback. | 90 |
| 7 | [newcodexJS/01-task-manager](../../newcodexJS/01-task-manager/astraupskill/README.md) | CRUD regressions, bounded identifiers/titles and unchanged overdue-date editing. | 3 |
| 8 | [newcodexJS/02-contact-book](../../newcodexJS/02-contact-book/astraupskill/README.md) | Quoted and multiline CSV parsing, complete batch validation and transactional import. | 4 |
| 9 | [newcodexJS/03-expense-tracker](../../newcodexJS/03-expense-tracker/astraupskill/README.md) | Correct category aggregates, month/date filters and amount validation. | 3 |
| 10 | [newcodexJS/05-recipe-manager](../../newcodexJS/05-recipe-manager/astraupskill/README.md) | Owner-scoped updates, strict nested validation and transaction rollback coverage. | 3 |
| 11 | [JS1/flashcards](../../JS1/flashcards/astraupskill/README.md) | Study can select unlearned cards only, changing decks restarts the session, and the final grade produces an explicit completion state. Grading requires revealing the answer. Failed storage leaves the card and cursor unchanged. | 2 |
| 12 | [JS1/habit-tracker](../../JS1/habit-tracker/astraupskill/README.md) | A current streak may continue through yesterday while today is still in progress. The best badge counts consecutive real dates, ignoring invalid, false and future entries. Day buttons have full accessible names. | 2 |
| 13 | [JS1/reading-list](../../JS1/reading-list/astraupskill/README.md) | Status filtering composes with search and sorting. Rating ties use title then id. The live summary distinguishes visible books from overall finished count, and sorting preserves saved order. | 1 |
| 14 | [JS1/note-vault](../../JS1/note-vault/astraupskill/README.md) | Operations serialize through one queue. Writes use a unique sibling file and rename after writing succeeds. Failure preserves old bytes and does not poison later operations. HTTP errors are handled and Vite mounts the client correctly. | 3 |
| 15 | [JS1/budget-tracker](../../JS1/budget-tracker/astraupskill/README.md) | New amounts require positive bounded decimal text with at most two fractional digits and real dates. Totals accumulate cents. Create, edit and delete publish only after storage succeeds, retaining the form on failure. | 2 |
| 16 | [JS1/pantry-inventory](../../JS1/pantry-inventory/astraupskill/README.md) | Rows show stock and expiration independently. Expired filtering is available, and the in-stock/nonexpired view excludes expired items. New quantities must be finite and nonnegative, dates must be real, and returning to the tab refreshes date-based status. | 2 |
| 17 | [JS1/snippet-vault](../../JS1/snippet-vault/astraupskill/README.md) | Create, edit and delete publish only after persistence succeeds. Tags deduplicate case-insensitively, missing edit ids and blank content are rejected, and clipboard denial returns false so the UI can explain failure. | 2 |
| 18 | [JS1/room-booking](../../JS1/room-booking/astraupskill/README.md) | The UI edits existing ids and converts local input to explicit instants. The API validates ids, bounded text, real timestamps and forward windows. Day views send browser-local boundaries; a legacy date query explicitly means a UTC day. Database overlap enforcement is verified under concurrency and failed edits. | 2 |
| 19 | [newcodexJS/04-notes-app](../../newcodexJS/04-notes-app/astraupskill/README.md) | English to_tsvector/plainto_tsquery search uses bound parameters over title/body. The UI debounces requests and ignores older responses. Payloads and filters are bounded, tags serialize correctly to JSON, and partial edits retain omitted fields. | 1 |
| 20 | [newcodexJS/06-bookmark-manager](../../newcodexJS/06-bookmark-manager/astraupskill/README.md) | Zod validates create and partial updates. Metadata accepts configured exact HTTPS hosts on port 443, validates public IPv4 DNS answers, pins the connection, rejects redirects, and bounds headers/body/time. The UI applies a proposed title only if its URL still matches the request. | 4 |

The numbering is the agreed first batch followed by the next selected batch. Within the second batch, begin with browser state, filters and date rules, then proceed through file persistence to API/database work. Room Booking is the most demanding second-batch domain exercise; revisit its SQL and timestamp lessons after the simpler browser projects if needed.

## What each learning folder contains

Each project has nine Markdown files: a start page; source-linked codebase map; concepts from first principles; worked implementation with concrete input/output examples; testing and debugging; guided and independent practice; separate solutions and review rubric; a trace lab; and verification results. The project root README links the course. Existing Fable and other guides are preserved and linked where applicable.

The worked changes are implemented. Practice variations are deliberately learner exercises and are not represented as completed features. A useful session is: predict a result, trace the real source, run the focused test, explain the result, then attempt a variation before opening the solution.

## Earlier review and planning work

- [Master Desktop review](../astradocs/MASTER_REPORT.md) inventories projects and their SWE learning placement.
- [Final coverage review](../astradocs/FINAL_REVIEW.md) includes the nested `_Organized Desktop` coverage and discovery exclusions.
- [Tutorial/codebase explanation report](../astradocs/PROJECT_TUTORIALS_REPORT.md) identifies Fable material and similar guides, including placeholders.
- [Five-section improvement plan](../astrafinalplan/README.md) covers 389 root records (including 202 organized-subfolder records) plus 75 nested teaching apps: 464 planned entries.
- [First-ten implementation report](../astrafinalplan/TEN_PROJECTS_IMPLEMENTED.md) retains the first delivery details.

These inventory counts describe the prior completed review. This turn implemented the next ten; it did not perform another full Desktop scan or claim that every inventoried project was modified. The initial tutorial inventory predates the newly added courses.

## Verification and limits

The second batch was tested on isolated working copies, then applied with whole-batch original-file hash checks and per-file post-copy SHA-256 verification. All second-batch delivered hashes and all 20 courses' local file links were checked in the original folders. The first batch still matches its recorded delivery hashes.

Second-batch browser checks used actual static apps for the six browser projects. The four React clients were built and exercised with controlled API responses. Their backend suites separately used real HTTP and disposable JSON-file or PostgreSQL persistence. This is not a claim of a deployed end-to-end environment. Metadata fetch tests used a controlled local stub; no external website was fetched.

First-batch results are historical evidence from the preceding delivery, not freshly rerun in this turn: 116 test cases, six client builds, Recipeweb lint, two Recipe Manager typechecks and six Chromium checks. Daybook passed 89 tests in its full run; the remaining form test passed a focused retry with a 120-second limit. The isolated Vitest worker startup allowance was also extended. Assertions were unchanged.

The isolated harness used Node 22.16.0 and PostgreSQL 18.1. Development databases, personal saved records and original dependency trees were not used as test fixtures or replaced. The projects still require their documented local dependency/environment setup.

## Important implemented boundaries

- Note Vault serializes writes within one repository instance in one process, using temporary-file replacement. It does not provide multi-process locking or guaranteed power-loss durability.
- Room Booking retains the database exclusion constraint and adds validated edits/time handling. A booked-by label is not authentication or authorization.
- Notes App now performs English full-text search on the server. Ranking and a GIN index remain future scaling work.
- Bookmark Manager validates saves separately from optional metadata retrieval. Metadata requires an exact configured host allowlist, defaults disabled, checks DNS and pins the approved address, refuses redirects, and enforces response/time limits. Manual bookmark creation remains available.
- Browser date/streak improvements do not introduce a continuously scheduled midnight refresh. Budget totals use cents for arithmetic while retaining the existing stored dollar-number schema.

## Evidence and recovery

- [Second-batch detailed report](NEXT_10_IMPLEMENTATION_REPORT.md)
- [Second-batch delivery manifest](../astrafinalplan/implementation/batch02/delivery-manifest.json)
- [Second-batch automated checks](../astrafinalplan/implementation/batch02/checks.json)
- [Second-batch browser checks](../astrafinalplan/implementation/batch02/browser-checks.json)
- [Second-batch source diff](../astrafinalplan/implementation/batch02/source-changes.diff)
- [Combined machine-readable delivery](all-20-delivery.json)

Original versions of changed files are retained locally under `astrafinalplan/implementation/backups` for batch one and `astrafinalplan/implementation/batch02/backups` for batch two. New files are identified by a null `before_sha256` in the manifests. Restoring an original file is a deliberate per-file recovery action; the new learning folders can remain.
