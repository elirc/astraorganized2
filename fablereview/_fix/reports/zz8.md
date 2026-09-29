# zz8 (self-review / integration queue) — fix report (B13)

## Done
- [review #1 / backlog 1.7] Re-filed every chapter so filename, `# N.` heading and README navigation agree. The course was offset: `04-TESTING-AND-DEBUGGING.md` held "4. Worked review submission", `05-PRACTICE.md` held "5. Worked queue claim", `06-SOLUTIONS-AND-REVIEW.md` held "6. Testing and debugging", `07-TRACE-LAB.md` held "7. Practice exercises", and VERIFICATION claimed to be chapter 9 with no chapter 8. New layout (canonical filenames kept, content moved to match):
  - `01-CODEBASE-MAP.md` — "1. Codebase map" (+ new "Two naming conventions, one service" and "What to ignore" sections)
  - `02-CONCEPTS.md` — "2. Concepts: the review workflow and the integration queue" (old 02 + old 03 queue concepts + glossary)
  - `03-WORKED-CHANGE.md` — "3. Worked change" (old 04 worked review + old 05 worked claim + new material)
  - `04-TESTING-AND-DEBUGGING.md` — "4. Testing and debugging" (old 06)
  - `05-PRACTICE.md` — "5. Practice exercises" (old 07 exercises A–C + new D/E)
  - `06-SOLUTIONS-AND-REVIEW.md` — "6. Solutions and review" (**new**, was missing entirely)
  - `07-TRACE-LAB.md` — "7. Trace lab" (**rewritten**)
  - `VERIFICATION.md` — "8. Verification" (renumbered from 9, the review's own stated alternative)
- [review #2 / backlog 2.3, 3.11] Wrote the missing solutions chapter: a shared runnable Vitest harness, full worked answers to exercises A, B and C (each a paste-and-run block), expected-failure answers for D, and a design sketch for E. One distinct review paragraph per exercise, each naming what the assertion actually discriminates.
- [review #3 / backlog 3.13] Rewrote `src/tests/workflow-atomicity.test.ts`. The old test 1 was tautological: its fake `submitSelfReview` snapshotted state, threw, and restored it in its own `catch`. The new file mocks `@/lib/db` with a dumb in-memory Prisma double whose **`$transaction` helper** performs the snapshot/restore, and exercises the **real** `ReviewRepository` + `ReviewService`. Discriminator: if the repository moved any of its three writes outside `db.$transaction`, the snapshot taken when the transaction opens would already contain the committed change and the assertion would fail. Added two further real tests (one-winner concurrency against the real predicate; mismatched `subjectEmployeeId` writes nothing). Suite went 6 → 8 tests.
- [review #4 / backlog 3.15] `VERIFICATION.md` rewritten: `node_modules/.bin/vitest.mjs` (does not exist) and `node_modules/.bin/tsc.cmd` (Windows-only) replaced with `npm test -- run ...` and `npx tsc --noEmit`, plus an explicit clean-checkout setup block (Node version, `npm ci`, `npm run db:generate`, optional `docker compose up -d`, `cp .env.example .env`, `npm run db:push`, `npm run db:seed`, `npm run dev`) and the expected summary I observed.
- [review #5] Added a "The schema change: `claimToken`" section to chapter 3: the exact schema lines (`prisma/schema.prisma:368`), what `db push` does to an existing database (nullable column + index; mid-flight `RUNNING` rows keep a NULL token and can no longer be completed, so they must be retried), why that is a one-way door, and the real `prisma migrate dev` equivalent. Also documented the changed meaning of `attemptCount` (incremented on claim, not on retry — mixed history on an existing database) and that the claim re-read at `integration-repository.ts:205` is **outside** any transaction, with the token equality check as what makes it safe.
- [review #6 / backlog 3.5] Added a 15-row glossary to `02-CONCEPTS.md` (tenant, tenant context, session, repository, service, service factory/DI, `$transaction`, conditional update, zero-rows-as-conflict, claim token/lease, audit row, assignment, cycle, race window, detached result) and a predict → run → verify block at the end of chapters 2 and 3.
- [review #7 / backlog 2.8] Re-encoded the course as clean UTF-8; the `â€™` mojibake in the old `05-PRACTICE.md:3` and `02-CONCEPTS.md` is gone (`grep -n "â€" *.md` → no match; no BOM).
- [backlog 2.2] Rewrote `07-TRACE-LAB.md` as six *distinct* boundary sections, each naming the real file and lines I checked: form component (`src/components/reviews/review-cycle-panel.tsx:129-150`) → mutation hook + fetch wrapper (`src/hooks/useReviewCycles.ts:47-70`, `src/lib/http/client.ts:38-66`) → route handler (`src/app/api/review-cycles/[cycleId]/submit-self-review/route.ts:12-28`) → validator (`src/lib/validation/reviewSchemas.ts:9-15`) → service (`src/services/review-service.ts:36-86`) → repository transaction (`src/repositories/review-repository.ts:91-156`), each with an "if this boundary were missing" note, plus a fill-in failure-mode table and a second trace for the queue path.
- [backlog 2.4] Chapter 3 now supplies three concrete variations with expected results (delete `subjectEmployeeId` from the where clause; move `auditLog.create` outside the transaction; drop `claimToken` from `completeJob`) and a predict-then-verify table of expected row counts.
- [backlog 3.1] Code blocks now appear in chapters 3 (claim loop, `completeJob`, schema, commands), 4 (the whole mock harness), 6 (four full runnable test blocks), 7 (route handler, Zod schema) and VERIFICATION (setup and repeat commands).
- [backlog 3.2] Removed the agent-process language from `VERIFICATION.md` ("immutable baseline", "frozen manifest", "stage working directory", "post-freeze hash", "before delivery … hash exact teaching snapshots"). `grep -nE "manifest|baseline|frozen|root agent|stage " astraupskill/*.md` → no match.
- [backlog 3.4] Added exercise D, a red-first exercise that restores `astraupskill/snapshots/review-repository.ts.original.txt`, runs the focused test, records the two expected failures, and restores the fix. Chapter 6 lists the expected failing test names.
- [backlog 3.5] README rewritten with a prerequisites box (what you need and, explicitly, what you do not), a chapter table with per-chapter time estimates (~4 h total), a one-line setup, and an honest-limits section.

## Skipped
- Nothing from the review list was skipped. Backlog 2.5 (ownership/authz exercise) is already satisfied here: the change *is* an ownership fix, the new "writes nothing when the subject employee predicate does not match" test is the cross-owner rejection test, and chapter 3 variation 1 makes the learner break and restore it.
- [3.3] Copying cited evidence into `astraupskill/evidence/`: not done. This project ships no logs or screenshots of its own, and the only records live in Astra's evidence folders, which I must not touch or duplicate. VERIFICATION now prints the commands plus the summaries I observed myself instead.
- I did not wrap the claim `updateMany` + `findFirst` pair in a transaction. The review calls it "defensible", and changing it would alter behaviour the course describes throughout; it is documented as an explicit caveat in chapter 3 instead.

## Verification
- Copied `astra-remaining-improvements/stage/332058fd8671/node_modules` into the project with robocopy (the project had none), then:
- `node .\node_modules\vitest\vitest.mjs run --maxWorkers=1` (baseline, before my edits) → `Test Files  5 passed (5)` / `Tests  6 passed (6)`
- `node .\node_modules\vitest\vitest.mjs run src/tests/workflow-atomicity.test.ts --maxWorkers=1` → `Test Files  1 passed (1)` / `Tests  4 passed (4)`
- `node .\node_modules\typescript\bin\tsc --noEmit` → no output, `exit=0`
- `node .\node_modules\vitest\vitest.mjs run --maxWorkers=1` (final) → `Test Files  5 passed (5)` / `Tests  8 passed (8)`
- Markdown link check over `astraupskill/*.md` → all 8 relative links resolve.
- Line endings: all nine chapter files still CRLF, as delivered. No BOM. Course grew 3,843 → 9,538 words.
- `node_modules` removed afterwards, since the project shipped without it.

## Course/code consistency check
- Chapter 3 excerpt of the claim loop re-read against `src/repositories/integration-repository.ts:181-208`, and `completeJob` against `:213-236` — line numbers and code match.
- Chapter 3 self-review excerpt matches `src/repositories/review-repository.ts:105-147`; the eight predicates listed in chapter 7 were counted in the actual `where` clause.
- Chapter 7 six boundaries were each opened and the quoted lines checked (`review-cycle-panel.tsx:129-150`, `useReviewCycles.ts:47-70`, `client.ts:38-66`, `route.ts:12-28`, `reviewSchemas.ts:9-15`, `review-service.ts:36-86`, `review-repository.ts:91-156`).
- Chapter 4 harness walk-through was written from the shipped `src/tests/workflow-atomicity.test.ts` after it passed, so the quoted `$transaction` helper is the code on disk.
- VERIFICATION expected summary (`5 passed` / `8 passed`) is what I observed, not a claim.
- Chapter 1 "what to ignore" list checked against `ls src/app`, `src/app/api` and `src/components`.
