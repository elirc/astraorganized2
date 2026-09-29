# aiapplybot — fix report (B15)

Fable, 2026-09-18.

## Done
- review#1 README opens with the environment block (venv, requirements, requirements-dev, Playwright Chromium, init, pytest)
- review#2 08-TRANSLATION.md mapping the wrapper, the conditional UPDATE + rowcount, and the baseline/adopt rule to Express/Prisma, ASP.NET/EF Core and React
- review#3 02 two-tab table with versions and a paragraph on why validation runs outside the SQLite write transaction
- review#4 01 marks browser/llm/ats/tracker out of scope and names the four modules to read

## Skipped
- (none)

## Verification
- Documentation-only change (no code or tests touched), so no test run; edited files re-read for headings/links after the script

## Course/code consistency check
- README environment block mirrors the root README commands; 02 paragraph describes the validation-before-transaction order visible in application_store.py; 01 out-of-scope list names modules present in applybot/.

## Phase 3 addendum (glossary)

Extended the README section that already carried the prerequisites and glossary (renamed so its heading starts with `## Prerequisites`), widening the existing 12-term glossary with a "Where in this project" column instead of adding a second glossary. Every location was checked against the source before it was written: applybot/application_store.py (version/rowcount checks in update and delete, transaction(), _audit, _check_identity, application_input, version_input, import_history), applybot/dashboard.py (Location header, _authorize token) and applybot/web/app.js (editor, adopt, retry guidance).

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `04-TESTING-AND-DEBUGGING.md` — quoted from `tests/test_store.py:57-71` (concurrent writers)
- `06-SOLUTIONS-AND-REVIEW.md` — quoted from `applybot/application_store.py:217-241` (`update`)
- `07-TRACE-LAB.md` — quoted from `applybot/application_store.py:217-225` (version comparison)
