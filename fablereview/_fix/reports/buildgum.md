# _Organized Desktop/02 Build Projects/buildgum — fix report (B15)

Fable, 2026-09-18.

## Done
- review#1 03 Step 4 gains a three-outcome table (rejected / delivered / acknowledgement lost) with what replay() does
- review#2 02 "What this becomes on a server" (Idempotency-Key + table, If-Match/version, transaction, size limits + schema)
- review#3 README toolchain block incl. the Python/Playwright steps and the .verification note; review#4 generic framing replaced with buildgum-specific junior and mid-level milestones

## Skipped
- (none)

## Verification
- Documentation-only change (no code or tests touched), so no test run; edited files re-read for headings/links after the script

## Course/code consistency check
- README toolchain block reflects scripts/test.mjs (compiles into .verification/ when present) and the 04 Playwright steps; milestones name fields and behaviors the codebase has (requestKey, receipts, export/import).

## Phase 3 addendum (glossary)

Extended the README section that already carried the prerequisites and glossary (renamed so its heading starts with `## Prerequisites`), widening the existing 12-term glossary with a "Where in this project" column instead of adding a second glossary. Every location was checked against the source before it was written: src/model.ts (parsePrice, money, validateProduct, reduce, replay, fingerprint, quoteCart) and src/repository.ts (commit's base.raw compare, browserLock, STORAGE_KEY, restore revision).

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `06-SOLUTIONS-AND-REVIEW.md` — quoted from `src/repository.ts:41-65` (`restore`)
- `07-TRACE-LAB.md` — quoted from `src/repository.ts:26-39` (`commit` with replay)
