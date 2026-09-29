# Next ten: implementation details

Applied September 8, 2026. [Combined report](ALL_20_PROJECTS_REPORT.md).

This batch follows the first ten with six small browser apps, one file-backed app and three PostgreSQL apps. All listed improvements are installed in the original project folders.

## 11. Flashcards: finite study sessions

[Start the course](../../JS1/flashcards/astraupskill/README.md) | [JS1/flashcards verification](../../JS1/flashcards/astraupskill/VERIFICATION.md)

**Learning focus:** session snapshots, state transitions and persistence failure.

**Before:** Grading the last card never advanced beyond it. Changing decks during study retained the old order, and there was no unlearned-only study option.

**Implemented:** Study can select unlearned cards only, changing decks restarts the session, and the final grade produces an explicit completion state. Grading requires revealing the answer. Failed storage leaves the card and cursor unchanged.

**Concrete example:** JS contains a unknown and b known; CSS contains c unknown. Select JS and unlearned-only: the session contains just a. Reveal and mark it known: progress becomes Completed 1 of 1 and grading is disabled. Restarting now finds no eligible cards. A rejected write instead keeps a at index zero.

**Evidence:** 2 automated test cases; Chromium interaction passed. See the project verification file for its build/typecheck coverage and the distinction between backend persistence tests and client API fixtures.

**Learning material:** 9 files, approximately 5,144 words.

**Changed or added project files outside the course:**

- [app.js](../../JS1/flashcards/app.js)
- [index.html](../../JS1/flashcards/index.html)
- [package.json](../../JS1/flashcards/package.json)
- [README.md](../../JS1/flashcards/README.md)
- [styles.css](../../JS1/flashcards/styles.css)
- [test/browser.cjs](../../JS1/flashcards/test/browser.cjs)
- [test/study.test.cjs](../../JS1/flashcards/test/study.test.cjs)

## 12. Habit Tracker: calendar streaks

[Start the course](../../JS1/habit-tracker/astraupskill/README.md) | [JS1/habit-tracker verification](../../JS1/habit-tracker/astraupskill/VERIFICATION.md)

**Learning focus:** local dates, derived statistics and edge cases.

**Before:** The current streak required today to be checked already, and there was no longest historical streak.

**Implemented:** A current streak may continue through yesterday while today is still in progress. The best badge counts consecutive real dates, ignoring invalid, false and future entries. Day buttons have full accessible names.

**Concrete example:** Checks on February 28, February 29 and March 1, 2024 give best three. Add March 3 and invalid February 30: best remains three. With today March 11, checks on March 9 and 10 give current two; a check only on March 9 gives zero.

**Evidence:** 2 automated test cases; Chromium interaction passed. See the project verification file for its build/typecheck coverage and the distinction between backend persistence tests and client API fixtures.

**Learning material:** 9 files, approximately 4,952 words.

**Changed or added project files outside the course:**

- [app.js](../../JS1/habit-tracker/app.js)
- [package.json](../../JS1/habit-tracker/package.json)
- [README.md](../../JS1/habit-tracker/README.md)
- [test/browser.cjs](../../JS1/habit-tracker/test/browser.cjs)
- [test/streaks.test.cjs](../../JS1/habit-tracker/test/streaks.test.cjs)

## 13. Reading List: composed views

[Start the course](../../JS1/reading-list/astraupskill/README.md) | [JS1/reading-list verification](../../JS1/reading-list/astraupskill/VERIFICATION.md)

**Learning focus:** filter composition, deterministic ordering and summaries.

**Before:** Search and sorting existed without an explicit status filter or matching-versus-overall summary. Equal ratings relied on source order.

**Implemented:** Status filtering composes with search and sorting. Rating ties use title then id. The live summary distinguishes visible books from overall finished count, and sorting preserves saved order.

**Concrete example:** Zebra and Alpha both have rating five and Finished status; Beta is Reading. Filter Finished, search Maya and sort by rating: Alpha then Zebra appear. Saved order remains Zebra, Alpha, Beta. An unmatched query shows zero results while overall finished stays two.

**Evidence:** 1 automated test cases; Chromium interaction passed. See the project verification file for its build/typecheck coverage and the distinction between backend persistence tests and client API fixtures.

**Learning material:** 9 files, approximately 4,788 words.

**Changed or added project files outside the course:**

- [app.js](../../JS1/reading-list/app.js)
- [index.html](../../JS1/reading-list/index.html)
- [package.json](../../JS1/reading-list/package.json)
- [README.md](../../JS1/reading-list/README.md)
- [styles.css](../../JS1/reading-list/styles.css)
- [test/browser.cjs](../../JS1/reading-list/test/browser.cjs)
- [test/filters.test.cjs](../../JS1/reading-list/test/filters.test.cjs)

## 14. Note Vault: durable serialized writes

[Start the course](../../JS1/note-vault/astraupskill/README.md) | [JS1/note-vault verification](../../JS1/note-vault/astraupskill/VERIFICATION.md)

**Learning focus:** async queues, atomic file replacement and repositories.

**Before:** Concurrent operations could read the same file version and overwrite each other. Direct target writes risked truncation. The client imported a component without mounting React.

**Implemented:** Operations serialize through one queue. Writes use a unique sibling file and rename after writing succeeds. Failure preserves old bytes and does not poison later operations. HTTP errors are handled and Vite mounts the client correctly.

**Concrete example:** With one welcome note, twelve concurrent creates leave thirteen records. Pin four created ids: those four are pinned independently of the welcome note. Reject a rename, compare original bytes, retry successfully and reopen the repository to read the result.

**Evidence:** 3 automated test cases; Chromium interaction passed. See the project verification file for its build/typecheck coverage and the distinction between backend persistence tests and client API fixtures.

**Learning material:** 9 files, approximately 5,385 words.

**Changed or added project files outside the course:**

- [package.json](../../JS1/note-vault/package.json)
- [README.md](../../JS1/note-vault/README.md)
- [vite.config.js](../../JS1/note-vault/vite.config.js)
- [client/index.html](../../JS1/note-vault/client/index.html)
- [client/src/App.jsx](../../JS1/note-vault/client/src/App.jsx)
- [client/src/main.jsx](../../JS1/note-vault/client/src/main.jsx)
- [server/repository.js](../../JS1/note-vault/server/repository.js)
- [server/server.js](../../JS1/note-vault/server/server.js)
- [test/persistence.test.js](../../JS1/note-vault/test/persistence.test.js)

## 15. Budget Tracker: cents and safe commits

[Start the course](../../JS1/budget-tracker/astraupskill/README.md) | [JS1/budget-tracker verification](../../JS1/budget-tracker/astraupskill/VERIFICATION.md)

**Learning focus:** numeric parsing, representations and persisted state.

**Before:** Number conversion and <= 0 did not reject all malformed values. Direct decimal accumulation complicated totals, and failed writes could put memory ahead of storage.

**Implemented:** New amounts require positive bounded decimal text with at most two fractional digits and real dates. Totals accumulate cents. Create, edit and delete publish only after storage succeeds, retaining the form on failure.

**Concrete example:** Income 0.10 plus 0.20 displays $0.30; 1.01 parses to 101 cents. Reject empty, zero, negative, 1.001, Infinity, scientific notation and values above 999999999.99. A failed edit to 12.50 keeps the prior amount and the entered form value.

**Evidence:** 2 automated test cases; Chromium interaction passed. See the project verification file for its build/typecheck coverage and the distinction between backend persistence tests and client API fixtures.

**Learning material:** 9 files, approximately 4,848 words.

**Changed or added project files outside the course:**

- [app.js](../../JS1/budget-tracker/app.js)
- [package.json](../../JS1/budget-tracker/package.json)
- [README.md](../../JS1/budget-tracker/README.md)
- [test/browser.cjs](../../JS1/budget-tracker/test/browser.cjs)
- [test/money.test.cjs](../../JS1/budget-tracker/test/money.test.cjs)

## 16. Pantry Inventory: expiration versus stock

[Start the course](../../JS1/pantry-inventory/astraupskill/README.md) | [JS1/pantry-inventory verification](../../JS1/pantry-inventory/astraupskill/VERIFICATION.md)

**Learning focus:** independent predicates, calendar rules and validation.

**Before:** Fresh really meant above the stock threshold, so an expired item could appear fresh. Some invalid numeric values passed validation.

**Implemented:** Rows show stock and expiration independently. Expired filtering is available, and the in-stock/nonexpired view excludes expired items. New quantities must be finite and nonnegative, dates must be real, and returning to the tab refreshes date-based status.

**Concrete example:** On September 8, an item expiring September 7 with quantity five and minimum one is Stock OK and Expired. An item expiring today with quantity one and minimum one is Low stock and not expired. Only a future sufficiently stocked item matches the combined view.

**Evidence:** 2 automated test cases; Chromium interaction passed. See the project verification file for its build/typecheck coverage and the distinction between backend persistence tests and client API fixtures.

**Learning material:** 9 files, approximately 4,939 words.

**Changed or added project files outside the course:**

- [app.js](../../JS1/pantry-inventory/app.js)
- [index.html](../../JS1/pantry-inventory/index.html)
- [package.json](../../JS1/pantry-inventory/package.json)
- [README.md](../../JS1/pantry-inventory/README.md)
- [test/browser.cjs](../../JS1/pantry-inventory/test/browser.cjs)
- [test/expiration.test.cjs](../../JS1/pantry-inventory/test/expiration.test.cjs)

## 17. Snippet Vault: storage and clipboard failure

[Start the course](../../JS1/snippet-vault/astraupskill/README.md) | [JS1/snippet-vault verification](../../JS1/snippet-vault/astraupskill/VERIFICATION.md)

**Learning focus:** ES modules, normalization and rejected promises.

**Before:** The store mutated before writing, duplicate tag variants accumulated, and rejected clipboard promises could escape without feedback.

**Implemented:** Create, edit and delete publish only after persistence succeeds. Tags deduplicate case-insensitively, missing edit ids and blank content are rejected, and clipboard denial returns false so the UI can explain failure.

**Concrete example:** Tags Utility,utility, EVENTS,events become Utility and EVENTS. A failed title-edit write leaves saved and in-memory titles unchanged. Clipboard rejection resolves false instead of producing an unhandled rejection.

**Evidence:** 2 automated test cases; Chromium interaction passed. See the project verification file for its build/typecheck coverage and the distinction between backend persistence tests and client API fixtures.

**Learning material:** 9 files, approximately 4,843 words.

**Changed or added project files outside the course:**

- [package.json](../../JS1/snippet-vault/package.json)
- [README.md](../../JS1/snippet-vault/README.md)
- [src/dom.js](../../JS1/snippet-vault/src/dom.js)
- [src/main.js](../../JS1/snippet-vault/src/main.js)
- [src/store.js](../../JS1/snippet-vault/src/store.js)
- [test/store.test.js](../../JS1/snippet-vault/test/store.test.js)

## 18. Room Booking: editable reservations and time boundaries

[Start the course](../../JS1/room-booking/astraupskill/README.md) | [JS1/room-booking verification](../../JS1/room-booking/astraupskill/VERIFICATION.md)

**Learning focus:** half-open intervals, database constraints and timezones.

**Before:** The UI could not edit although PUT existed. Runtime checks accepted malformed types or ambiguous timestamps, and local slot defaults mishandled midnight rollover.

**Implemented:** The UI edits existing ids and converts local input to explicit instants. The API validates ids, bounded text, real timestamps and forward windows. Day views send browser-local boundaries; a legacy date query explicitly means a UTC day. Database overlap enforcement is verified under concurrency and failed edits.

**Concrete example:** Two requests for one room from 10:00 to 11:00 UTC yield one 201 and one 409. An adjacent 11:00-to-12:00 slot succeeds. Extending the first to 11:30 fails and preserves its old end. Renaming preserves its id. A query window ending at 11:00 excludes the adjacent slot.

**Evidence:** 2 automated test cases; Chromium interaction passed. See the project verification file for its build/typecheck coverage and the distinction between backend persistence tests and client API fixtures.

**Learning material:** 9 files, approximately 5,563 words.

**Changed or added project files outside the course:**

- [package.json](../../JS1/room-booking/package.json)
- [README.md](../../JS1/room-booking/README.md)
- [client/src/api.ts](../../JS1/room-booking/client/src/api.ts)
- [client/src/App.tsx](../../JS1/room-booking/client/src/App.tsx)
- [client/src/styles.css](../../JS1/room-booking/client/src/styles.css)
- [client/src/vite-env.d.ts](../../JS1/room-booking/client/src/vite-env.d.ts)
- [server/src/index.ts](../../JS1/room-booking/server/src/index.ts)
- [server/src/validation.ts](../../JS1/room-booking/server/src/validation.ts)
- [test/booking.test.ts](../../JS1/room-booking/test/booking.test.ts)

## 19. Notes API: actual content search

[Start the course](../../newcodexJS/04-notes-app/astraupskill/README.md) | [newcodexJS/04-notes-app verification](../../newcodexJS/04-notes-app/astraupskill/VERIFICATION.md)

**Learning focus:** PostgreSQL text search, runtime validation and stale responses.

**Before:** The API cast a whole row to text, and the UI searched serialized JSON locally. Internal metadata could match a document query. Payload field types were not enforced.

**Implemented:** English to_tsvector/plainto_tsquery search uses bound parameters over title/body. The UI debounces requests and ignores older responses. Payloads and filters are bounded, tags serialize correctly to JSON, and partial edits retain omitted fields.

**Concrete example:** Running notes matches search run through stemming. A note whose folder is HiddenKeyword does not match that content query. Invalid tags are rejected before writing. Updating only body retains title/id and makes its new words searchable.

**Evidence:** 1 automated test cases; Chromium interaction passed. See the project verification file for its build/typecheck coverage and the distinction between backend persistence tests and client API fixtures.

**Learning material:** 9 files, approximately 5,220 words.

**Changed or added project files outside the course:**

- [README.md](../../newcodexJS/04-notes-app/README.md)
- [client/src/App.jsx](../../newcodexJS/04-notes-app/client/src/App.jsx)
- [server/package.json](../../newcodexJS/04-notes-app/server/package.json)
- [server/src/models/model.js](../../newcodexJS/04-notes-app/server/src/models/model.js)
- [server/src/services/service.js](../../newcodexJS/04-notes-app/server/src/services/service.js)
- [server/test/database.cjs](../../newcodexJS/04-notes-app/server/test/database.cjs)
- [server/test/search.test.cjs](../../newcodexJS/04-notes-app/server/test/search.test.cjs)

## 20. Bookmark Manager: validated links and metadata

[Start the course](../../newcodexJS/06-bookmark-manager/astraupskill/README.md) | [newcodexJS/06-bookmark-manager verification](../../newcodexJS/06-bookmark-manager/astraupskill/VERIFICATION.md)

**Learning focus:** runtime schemas, outbound policy and controlled network tests.

**Before:** The scaffold copied fields without substantive runtime validation and lacked a metadata boundary. Emitted ESM paths also needed correction for a normal Node start.

**Implemented:** Zod validates create and partial updates. Metadata accepts configured exact HTTPS hosts on port 443, validates public IPv4 DNS answers, pins the connection, rejects redirects, and bounds headers/body/time. The UI applies a proposed title only if its URL still matches the request.

**Concrete example:** A controlled host returns title A &amp; B, yielding A & B. A redirect to loopback is rejected without contacting its target. Private DNS, unlisted hosts, oversized bodies and timeouts fail. DNS finishing after timeout cannot start a transfer. A javascript: URL is rejected before insertion.

**Evidence:** 4 automated test cases; Chromium interaction passed. See the project verification file for its build/typecheck coverage and the distinction between backend persistence tests and client API fixtures.

**Learning material:** 9 files, approximately 5,898 words.

**Changed or added project files outside the course:**

- [.env.example](../../newcodexJS/06-bookmark-manager/.env.example)
- [README.md](../../newcodexJS/06-bookmark-manager/README.md)
- [client/src/App.tsx](../../newcodexJS/06-bookmark-manager/client/src/App.tsx)
- [client/src/vite-env.d.ts](../../newcodexJS/06-bookmark-manager/client/src/vite-env.d.ts)
- [client/src/services/api.ts](../../newcodexJS/06-bookmark-manager/client/src/services/api.ts)
- [server/knexfile.ts](../../newcodexJS/06-bookmark-manager/server/knexfile.ts)
- [server/package.json](../../newcodexJS/06-bookmark-manager/server/package.json)
- [server/db/seeds/001_seed.ts](../../newcodexJS/06-bookmark-manager/server/db/seeds/001_seed.ts)
- [server/src/app.ts](../../newcodexJS/06-bookmark-manager/server/src/app.ts)
- [server/src/server.ts](../../newcodexJS/06-bookmark-manager/server/src/server.ts)
- [server/src/config/db.ts](../../newcodexJS/06-bookmark-manager/server/src/config/db.ts)
- [server/src/controllers/controller.ts](../../newcodexJS/06-bookmark-manager/server/src/controllers/controller.ts)
- [server/src/middleware/errorMiddleware.ts](../../newcodexJS/06-bookmark-manager/server/src/middleware/errorMiddleware.ts)
- [server/src/models/model.ts](../../newcodexJS/06-bookmark-manager/server/src/models/model.ts)
- [server/src/routes/routes.ts](../../newcodexJS/06-bookmark-manager/server/src/routes/routes.ts)
- [server/src/services/metadata.ts](../../newcodexJS/06-bookmark-manager/server/src/services/metadata.ts)
- [server/src/services/service.ts](../../newcodexJS/06-bookmark-manager/server/src/services/service.ts)
- [server/test/bookmarks.test.ts](../../newcodexJS/06-bookmark-manager/server/test/bookmarks.test.ts)
- [server/test/database.cjs](../../newcodexJS/06-bookmark-manager/server/test/database.cjs)
- [server/test/metadata.test.ts](../../newcodexJS/06-bookmark-manager/server/test/metadata.test.ts)

## Final review fixes

The visual review also corrected the Flashcards checkbox grouping, the Reading List search/filter layout, and Room Booking's full-precision date-field layout and display text. Affected browser checks were rerun after those changes. Bookmark Manager also received an explicit TypeScript loader and extension selection for migration/seed commands, plus JSON serialization in the seed. Those commands were checked in a disposable schema.
