# appmakertrack (kanban + time tracker) — fix report (B13)

## Done
- [review #1 / backlog 3.5] Added a 19-row glossary to `astraupskill/02-CONCEPTS.md`: running/completed entry, instant, compare-and-set, conditional update, zero-rows-as-conflict, lost update, read-then-write race, transaction, transaction client, injected client/seam, partial double, parking position, contiguous positions, no-op move, idempotency, 400 vs 404 vs 409 vs 500, `InputError`, application-wide running check.
- [review #2] Added a "Known strictness and cost" section to `VERIFICATION.md`: `parseInstant` rejecting >3 fractional digits, offsets outside ±23:59, zone-less strings and impossible calendar dates; `parseSeconds` bounded by Prisma `Int` (≈68 years) with `0` valid; unknown fields rejected rather than ignored; `moveTicket` costing ~2N writes inside one transaction; and the breaking status changes (stop 400 → 404/409, start 409 `TIMER_ALREADY_RUNNING`, PATCH 409 `RUNNING_TIMER`), plus the always-generic 500 body.
- [review #3] Exercise 8 is no longer "proposed": wrote `tests/board-service.integration.test.ts`, four cases against a **real** temporary SQLite database, skipped unless `APPMAKERTRACK_INTEGRATION=1`. Each case makes a unique `mkdtemp` directory, rewrites a copy of `prisma/schema.prisma` with an absolute `file:` URL (a literal URL is not overridden by `DATABASE_URL` — the trap the course already warned about), runs `db push` through `node node_modules/prisma/build/index.js` (spawning `npx.cmd` without a shell fails `EINVAL` on Windows — found and fixed while running it), constructs `new PrismaClient({ datasourceUrl })` against the same file, seeds only its own rows, and removes the directory in `finally`. It never opens `prisma/dev.db` and never runs `prisma/seed.ts`. Cases: within-column reorder stays contiguous; cross-column move leaves both sides contiguous; foreign target column writes nothing (before/after snapshot); a second `stopRunningEntry` loses the compare-and-set in a committed database.
- [review #4] Extended the injected-client seam to every route. `lib/time-entry-handlers.ts` now also exports `createStopTimerHandler`, `createPatchEntryHandler`, `createDeleteEntryHandler` and `createMoveTicketHandler`, each `(database = prisma)`; `app/api/time-entries/[entryId]/stop/route.ts`, `app/api/time-entries/[entryId]/route.ts` and `app/api/tickets/[ticketId]/move/route.ts` are now two-line re-exports. Behaviour is byte-identical (the handler bodies were moved, not rewritten). Added one response-level test per route (4 new cases, 13 → 17): stop 200/404/409/500 with the `TIMER_ALREADY_STOPPED` code, PATCH 200/400/404/409 asserting the exact `update` args for a notes-only edit, DELETE 200/404 asserting `delete` is never called for a missing row, move 200/400/404 asserting the project-scoped response body.
  - While writing the move test I found that a fake returning **live** references (rather than clones) lets a later `tx.ticket.update` mutate the `ticket` row the service read earlier, which corrupts `result.sourceColumnId`. Real Prisma returns detached rows, so the fake now clones; the reason is written into the test as a comment and into chapter 4.
- [review #5 / backlog 2.8] Stripped the UTF-8 BOM from `astraupskill/README.md` and `astraupskill/05-PRACTICE.md`. All nine chapter files: CRLF preserved, no BOM.
- [backlog 3.4] Added exercise 12, a red-first exercise with two reversible one-line edits (`lib/time-entry-service.ts:11` drop `endTime: null`; `lib/board-service.ts:15` drop the project check) plus a snapshot-restore variant, and wrote the exact expected failure output into `06-SOLUTIONS-AND-REVIEW.md` §12. Added exercise 13 (DELETE response test) with a solution explaining why asserting the 404 alone is weaker than asserting `deletes === 0`.
- [backlog 3.5] `astraupskill/README.md` gained a prerequisites section (and an explicit "you do not need React/Next/Docker") and a chapter table with per-chapter time estimates (~5 h total).
- [backlog 3.2] Removed the delivery-process wording from the course: "the staged route" → "the repaired route", "the staged source links" → "the changed source files", "Baseline source snapshots are preserved under snapshots" → a plain sentence about `snapshots/`. `grep -niE "manifest|baseline|frozen|root agent|staged "` over `astraupskill/*.md` → no match.
- Course chapters updated in the same pass as the code: chapter 3's "a second follow-up would be to extend the seam" paragraph now documents that it **was** done, with the new two-line route file shown; chapter 4 lists the new imports, shows a response-level test in full, and has a new "The temporary-database harness" section; chapter 5 exercise 8 now points at the runnable harness; chapter 6 §8–9 and the closing paragraph no longer call it proposed; `VERIFICATION.md` states the new counts.

## Skipped
- Nothing from the review's list.
- [backlog 2.5] Ownership/authorization exercise: deliberately not added as code. `TimeEntry` has no user relation and the course already argues, correctly, that adding an actor parameter without a schema change would create false confidence. The existing "application-wide running check" discussion and the cross-project rejection in `moveTicket` (which *is* an ownership check, at project granularity, and now has both a service test and a route test) cover the lesson. Recorded here rather than faked.
- [backlog 3.3] Evidence: already satisfied before I started — `astraupskill/evidence/` holds the logs and JSON the chapters cite.

## Verification
- Copied `astra-remaining-improvements/stage/b7429e8bf71d/node_modules` into the project (it had none).
- `npm test` (baseline, before edits) → `# tests 13 / # pass 13 / # fail 0`
- `npm test` (final) → `# tests 21 / # pass 17 / # fail 0 / # skipped 4` — the four skips are the integration file with the env flag unset, which is the intended default.
- `APPMAKERTRACK_INTEGRATION=1 npx tsx --test tests/board-service.integration.test.ts` → `# tests 4 / # pass 4 / # fail 0`, `duration_ms 153309` (real `prisma db push` per case).
- `npx tsx --test tests/board-service.integration.test.ts` with the flag unset → `# pass 0 / # skipped 4`.
- `npx tsc --noEmit` → exit 0, no output.
- `npm run lint` (`eslint .`, full project) → exit 0, no output.
- `prisma/dev.db` untouched; the harness only ever wrote into `%TEMP%\appmakertrack-*`, which it removed.
- Line endings: all source files still LF, all course files still CRLF. `node_modules` removed afterwards, since the project shipped without it.

## Course/code consistency check
- `03-WORKED-CHANGE.md` re-read against the new `lib/time-entry-handlers.ts` and the three rewritten route files; the quoted two-line `stop/route.ts` is the file on disk.
- `04-TESTING-AND-DEBUGGING.md` import block re-read against `tests/time-entry-validation.test.ts:8`; the quoted losing-stop test is a real excerpt of the shipped test; the six harness steps were checked line by line against `tests/board-service.integration.test.ts`.
- `05-PRACTICE.md` exercise 8 and 12 both name files and line numbers I opened (`lib/time-entry-service.ts:11`, `lib/board-service.ts:15`).
- `06-SOLUTIONS-AND-REVIEW.md` §12's quoted failure diff is the shape `node:test` prints for the existing `stop service distinguishes …` case; the surrounding claim (which assertions fail) was derived from the assertions in that case, which I re-read.
- `VERIFICATION.md`'s `# pass 17 / # skip 4` is the summary I observed, and the strictness list was checked against `lib/time-entry-validation.ts` and the status codes in `lib/time-entry-handlers.ts`.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `07-TRACE-LAB.md` — quoted from `lib/time-entry-service.ts:4-15` (`stopRunningEntry`)
