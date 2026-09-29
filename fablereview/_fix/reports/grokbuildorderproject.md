# grokbuildorderproject — fix report (B15)

## Done
- [review #1] Deleted the three empty leftover directories `backend/src/controllers`, `backend/src/middleware`, `backend/src/types` (verified empty and unreferenced by any `.ts/.tsx/.json/.mjs` file first). Added a paragraph to `astraupskill/01-CODEBASE-MAP.md` stating that routing lives in `backend/src/routes/` + `http.ts` and cross-cutting failure translation in `errors.ts`/`app.ts`, so a learner is told the folders do not exist rather than meeting three dead ones.
- [review #2] Added a six-row "What the database sees during the last-unit race" two-transaction timeline table to `astraupskill/02-CONCEPTS.md`, with the real `updateMany` predicate, the real 409 message from `orderRepository.ts:23`, and the named backend case that drives the sequence. Step 3 is called out explicitly as the courtesy check that both requests pass.
- [review #3 / backlog 3.4] `astraupskill/05-PRACTICE.md`: labelled exercises 5–7 (formerly 4–6) *stretch — pair with a senior*; inserted a new exercise 2 "Add order notes behind a version check (write the test first)" at the difficulty of the delivered change (schema `notes` + `version`, strict Zod, conditional `updateMany`, 404-vs-409 disambiguation, three explicit design decisions); and added a red-first exercise 0 that deletes `version: product.version`, then `stock: { gte: ... }`, from the reservation predicate, records which named cases go red for each, and restores.
- [review #4 / backlog 3.5] `astraupskill/README.md`: added "Before you start" (prerequisites, tool versions, cross-platform note) with a per-chapter pacing table (~10h total), and a 12-term glossary (invariant, interactive transaction, optimistic locking, conditional update, stale draft, 409 vs 404, Decimal, snapshot, idempotency, terminal state, envelope).
- [backlog 3.11] `astraupskill/06-SOLUTIONS-AND-REVIEW.md`: converted to per-exercise headings and gave **real code** for exercises 0–4 — the `productQuerySchema`/`ILIKE` filter and React Query cache key, the full `updateNotes` repository method plus the failing test to write first, the `StockMovement` model with `@@unique([orderId, productId, reason])` and the `tx`-not-`db` trap, and the `IdempotencyKey` model with the sorted-cart fingerprint and the P2002-only catch. Exercises 5–7 remain design guidance, stated as deliberate.
- [backlog 3.3] Copied the delivery run's unedited logs into `astraupskill/evidence/` (from `checks/grok-order/verified/` plus the failed `backend-first/backend-tests.log`, renamed `backend-tests-first-run.log`). Screenshots were not duplicated — they already ship in `astraupskill/images/`. Added an evidence table to `VERIFICATION.md` linking each file to the number it proves. Three zero-byte logs (`backend-build.log`, `createdb.log`, `frontend-typecheck.log`) were dropped rather than shipped empty, and that is stated in the chapter.
- [backlog 3.2] Removed the agent-process sentence "The delivered evidence is recorded in the central implementation report and its per-project manifest" from `VERIFICATION.md`, replaced by the learner-facing evidence table. A re-grep for `manifest|baseline|frozen|root agent` over `astraupskill/*.md` now returns nothing.
- [backlog 1.15 / D6] Date-stamped the headline count in `VERIFICATION.md` and stated the per-file breakdown (24 + 8 + 5 literal `it(` blocks, no parametrized expansion) so it is countable by hand.

## Skipped
- backlog 3.6 (`08-TRANSLATION.md`): not applicable — this project *is* the Express/Prisma target stack.
- backlog 3.1 (code blocks): 03 and 07 already had fenced blocks; 06 now has 22 fences. 04 remains prose because it is a command/procedure chapter whose commands are already inline-coded.
- backlog 2.x: wave-1 sweep items, already applied by the script.

## Verification
- `python links.py astraupskill` → `checked 68 relative links, 0 missing` (run after every edit, including the new links to `evidence/` and `../backend/src/http.ts`).
- BOM/empty scan over `astraupskill/*.md` → `no BOM, no empty files`.
- `grep -rniE "controllers|middleware/|src/types" --include=*.ts --include=*.tsx --include=*.json --include=*.mjs .` → the only hit is the new sentence in 01-CODEBASE-MAP.md; no source file referenced the deleted directories.
- `grep -niE "manifest|baseline|frozen|root agent" astraupskill/*.md` → no output.
- **Tests not run.** No application code was changed (the only filesystem change outside `astraupskill/` is the removal of three empty directories). `stage/e502bf8af566` has no `node_modules` to junction, so proving 37 passes would have required three fresh npm installs plus an `initdb` cluster for a docs-only change; the delivery's own run is now shipped in `astraupskill/evidence/` instead. Nothing in this report claims an observed pass.

## Course/code consistency check
- `backend/src/repositories/orderRepository.ts` (whole file) re-read against the new 02-CONCEPTS timeline: predicate, `reserved.count` guard, 409 message string and the sort-before-reserve comment all match the table verbatim.
- `backend/src/repositories/productRepository.ts` re-read against the new exercise-2 solution: the 404/409 disambiguation in `updateNotes` is the same shape as the delivered `update`, as the text claims.
- `backend/src/validation.ts`, `services/orderService.ts`, `routes/orderRoutes.ts` and `prisma/schema.prisma` re-read to confirm `Order` currently has **no** `version` or `notes` column, so exercise 2 is genuinely unimplemented work and not a task the delivered tree pre-answers.
- `astraupskill/01-CODEBASE-MAP.md` re-read against `backend/src/` after the directory deletion: every file it names still exists.
- 05/06 cross-numbering re-checked after renumbering: 05 has exercises 0–7; 06 has matching sections 0–6 plus a review section covering 7.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `04-TESTING-AND-DEBUGGING.md` — quoted from root `package.json` test scripts
