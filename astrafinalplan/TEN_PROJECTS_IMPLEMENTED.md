# Ten projects implemented

Completed 2026-09-08. The changes and learning courses are installed in the actual Desktop project folders below. Work through them in this order.

| Order | Project and learning course | Implemented improvement | Test cases |
|---|---|---|---:|
| 1 | [JS1/task-board](../../JS1/task-board/astraupskill/README.md) | Persistent one-level undo, including reload and failed-write handling. | 3 |
| 2 | [JS1/contact-book](../../JS1/contact-book/astraupskill/README.md) | Case-insensitive duplicate-email validation that supports editing your own record. | 2 |
| 3 | [JS1/focus-timer](../../JS1/focus-timer/astraupskill/README.md) | Deadline-based countdown, accurate pause/resume and single completion logging. | 3 |
| 4 | [finance-dashboard](../../finance-dashboard/astraupskill/README.md) | Validated expense editing with stable identity and persisted totals. | 2 |
| 5 | [recipeweb](../../recipeweb/astraupskill/README.md) | Saved shopping quantities, keyboard-editable controls and consistent clipboard output. | 3 |
| 6 | [jobtrack](../../jobtrack/astraupskill/README.md) | Validated application JSON export/import with atomic replacement and failure feedback. | 90 |
| 7 | [newcodexJS/01-task-manager](../../newcodexJS/01-task-manager/astraupskill/README.md) | CRUD regression coverage, bounded identifiers/titles and unchanged overdue-date editing. | 3 |
| 8 | [newcodexJS/02-contact-book](../../newcodexJS/02-contact-book/astraupskill/README.md) | Quoted/multiline CSV parsing, complete batch validation and transactional imports. | 4 |
| 9 | [newcodexJS/03-expense-tracker](../../newcodexJS/03-expense-tracker/astraupskill/README.md) | Correct category aggregates, month/date filtering and amount validation. | 3 |
| 10 | [newcodexJS/05-recipe-manager](../../newcodexJS/05-recipe-manager/astraupskill/README.md) | Owner-scoped updates, strict nested validation and transaction rollback coverage. | 3 |

## Learning material

Each project has an `astraupskill` folder linked from its root README. Together the courses contain 90 Markdown files and approximately 53,856 words, including source and test examples.

Each course includes prerequisites and setup, a linked codebase map, concepts explained from first principles, worked changes with actual code, test and debugging guidance, guided and independent exercises, solutions and a review rubric, and an honest verification record. Existing Fable/tutorial material is preserved. The exercises are follow-up learning tasks; they are clearly distinguished from implemented behavior.

## Verification

- 116 automated test cases passed across the ten project suites.
- All six relevant Vite client builds passed; Recipeweb lint and both Recipe Manager TypeScript checks passed.
- Six real Chromium interaction checks passed, covering persistence, validation, timing, keyboard quantity editing, clipboard output and backup import/export.
- The four backend suites exercised real HTTP/database behavior against an isolated PostgreSQL 18.1 test instance, including ownership denial and late transaction rollback.
- Every delivered file was checked against its staged SHA-256 after application; all learning-document links were checked in the actual project folders.

Verification ran on isolated working copies using Node 22.16.0 and a shared dependency harness; Recipeweb additionally used its own dependency tree. Daybook passed 89 tests in its full run; the remaining form test passed a focused retry with a 120-second limit. The isolated Vitest harness also needed a longer worker startup allowance. Assertions were unchanged. Byte-identical verified source was then applied to the originals. The original projects still require their documented local dependency/environment setup. These checks do not certify all unrelated functionality or production readiness.

## Change evidence

- [Per-project delivery summary](implementation/delivery-summary.json)
- [Exact delivered file manifest](implementation/delivery-manifest.json)
- [Automated check results](implementation/checks.json)
- [Browser interaction results](implementation/browser-checks.json)
- [Source changes](implementation/source-changes.diff)

Original versions of changed files are retained locally in `implementation/backups`. Project databases, personal records, existing dependency trees and unrelated source files were not replaced.
