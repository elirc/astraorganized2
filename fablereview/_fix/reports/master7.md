# master7 — Enterprise LMS audit-scope course — fix report (B14)

## Done
- [backlog 1.12 / review #1] Root `README.md` line 45 pointed at `docs/code-walkthroughs/audit-log-scope/README.md`, which has never existed. Now points at `astraupskill/README.md`. — files: `README.md`
- [review #2] Extracted one exported scope predicate `auditLogScope(actor)` in `apps/api/src/services.ts`; both `visibleAuditLogs` (dashboard projection) and `services.auditLogs` (dedicated endpoint) now call it instead of holding two copies of `role === "PLATFORM_ADMIN" || log.organizationId === actor.organizationId`. Added a test asserting both endpoints return the same row ids for the same actor. — files: `apps/api/src/services.ts`, `apps/api/src/audit-scope.test.ts`
- [review #3] Added `resetStore()` and `seedAuditLogs(count, organizationId, options?)` to `apps/api/src/store.ts` (the store's seeded fixture is deep-cloned at module load), so practice exercise 4 (26 Nova rows / 1 Acme row) is buildable without hand-editing the store. The exercise is now a shipped, passing test. — files: `apps/api/src/store.ts`, `apps/api/src/audit-scope.test.ts`, `astraupskill/05-PRACTICE.md`, `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- [review #4] Added a write-path test: an Acme instructor `POST /courses` must emit a `course.created` audit row carrying the *actor's* organization, visible to the Acme admin and excluded by `auditLogScope` for a Nova admin; plus a negative test that naming another organization in the body returns 403 and writes no audit row. New practice exercise 7 and a full worked answer (naming `assertCanAuthorCourse`/`canAuthorCourse`). — files: `apps/api/src/audit-scope.test.ts`, `astraupskill/05-PRACTICE.md`, `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- [backlog 3.4] Red-first exercise added: "Break it first" section in `04-TESTING-AND-DEBUGGING.md` restores the unscoped `slice(0, 25)` from `snapshots/services-before.ts.txt`, runs the two focused files, names the exact tests and assertion messages that turn red, then restores the fix. Repeated for the shared predicate. New practice exercise 6 + worked answer in `06`. — files: `astraupskill/04-TESTING-AND-DEBUGGING.md`, `05-PRACTICE.md`, `06-SOLUTIONS-AND-REVIEW.md`
- [backlog 3.5] Glossary (8 terms), prerequisites box and a per-chapter time-estimate table added to `astraupskill/README.md`. — files: `astraupskill/README.md`
- [backlog 3.8] "If this store were a database" table in `02-CONCEPTS.md` mapping the in-memory filter/slice to Prisma `where`/`take` and EF Core `Where`/`Take`, and naming fetch-then-filter as the same bug in a new costume. — files: `astraupskill/02-CONCEPTS.md`
- [backlog 3.11] Exercises 4–7 now have real code answers in `06-SOLUTIONS-AND-REVIEW.md` (previously exercise 4 was labelled "proposed, not part of the recorded count"; it is now a shipped test). — files: `astraupskill/06-SOLUTIONS-AND-REVIEW.md`
- [backlog 3.15] macOS/Linux reproduce block added to `VERIFICATION.md` alongside the PowerShell one, with a note that the `--testTimeout=30000` flag is what keeps a cold-start transform from failing the first test. — files: `astraupskill/VERIFICATION.md`
- [backlog 3.1] New fenced code blocks in `02`, `03`, `04`, `05`, `06` (previously `02`/`03` had none). — files: as above
- [D1 honesty] `VERIFICATION.md` now carries an update banner: 19 tests as delivered (log `evidence/tests-root-01.log`), 23 after this pass (log `evidence/tests-root-02.log`), with both logs kept.
- [backlog 3.3] Evidence already shipped in `astraupskill/evidence/`; added the new run log `tests-root-02.log`.

## Skipped
- [backlog 3.2] Nothing to do: grep for `manifest|baseline|frozen|root agent|stage` over `astraupskill/*.md` returns only "No package manifest, lockfile, JWT…" in `03-WORKED-CHANGE.md`, which is ordinary developer vocabulary, not agent-process language.
- [backlog 2.x] Wave-1 sweep items — out of scope for a wave-2 project.
- Review problem "[D4] no database/transaction content": genuinely true and not fixable without changing what the project is. Mitigated with the Prisma/EF Core translation table rather than by inventing a database layer.

## Verification
- `npm test -- --pool=threads --poolOptions.threads.singleThread=true --testTimeout=30000` → `Test Files  4 passed (4)` / `Tests  23 passed (23)` (log saved to `astraupskill/evidence/tests-root-02.log`)
- `npm run typecheck` (`tsc -b tsconfig.json`) → exit 0, no output
- Baseline before any edit: `npm test` → `Test Files 3 passed (3)` / `Tests 19 passed (19)`
- One earlier run with vitest's default 5 s timeout failed `api.test.ts > logs in seeded learner and returns dashboard` with `Test timed out in 5000ms` on a cold transform; rerunning with the project's documented `--testTimeout=30000` was green. Recorded in `VERIFICATION.md` rather than hidden.
- Dependencies: junction from `astra-remaining-improvements/stage/a1d53294d3b0/node_modules` (no copy), removed afterwards. Project has no `node_modules` now, as found.

## Course/code consistency check
- `02-CONCEPTS.md`, `03-WORKED-CHANGE.md`, `04-TESTING-AND-DEBUGGING.md`, `06-SOLUTIONS-AND-REVIEW.md` and `VERIFICATION.md` were re-read against the edited `services.ts`, `store.ts` and `audit-scope.test.ts`. The new prose quotes the shipped source verbatim.
- The old text in `05`/`06` describing exercise 4 as "a proposed ordering test, not part of the recorded nineteen tests" is left in place and is still accurate for the delivered run; the new sections state plainly that it is now shipped and counted in the 23.
- Verified the hint in practice exercise 7 against `apps/api/src/policies.ts:10` and `packages/domain/src/index.ts:19-21` before printing it.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `03-WORKED-CHANGE.md` — quoted from `apps/api/src/services.ts:28-35` (`auditLogScope`/`visibleAuditLogs`)
- `04-TESTING-AND-DEBUGGING.md` — quoted from root `package.json` (`test`, `verify`)
- `06-SOLUTIONS-AND-REVIEW.md` — quoted from `apps/api/src/audit-scope.test.ts:31-42`
- `07-TRACE-LAB.md` — quoted from `apps/api/src/services.ts:134-145` (`auditLogs` endpoint)
