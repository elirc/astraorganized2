# master7 — Enterprise LMS / Certification Platform — Fable review

- **Path:** `_Organized Desktop/03 Master Projects/master7`  ·  **Wave:** 2  ·  **Stack:** TypeScript / Express / npm workspaces / Vite+React / Vitest 2 · **in-memory store, Prisma schema present but unused**  ·  **Batch:** B14
- **Astra's change (one line):** Adds `visibleAuditLogs(actor)` to `apps/api/src/services.ts` so `GET /me/dashboard` filters audit records by `actor.organizationId` *before* `slice(0, 25)` (platform admins still cross-tenant, learners still `[]`), and seeds one Acme and one Nova audit record so the leak is observable.
- **Course size:** 3,814 words across 9 files  ·  **Tests claimed:** 19 (11 API + 4 policy + 4 domain)  ·  **Tests found on disk:** 19 across 3 files; `apps/api/src/api.test.ts` has 11 `it(...)` blocks including the new three-role audit-scope regression at line 35

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 4 | 4 | 4 | 4 | 5 | 5 | 5 | 5 | 4.5 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- Found a genuinely instructive class of bug: the *dedicated* audit endpoint was already tenant-scoped (`services.ts:131-141`), but a second projection on the dashboard was not. "A correct audit endpoint did not protect the separate dashboard projection" is exactly the lesson a junior needs about read-path authorization.
- The filter-before-slice point in `02-CONCEPTS.md` is the real insight and is explained with a concrete counterexample ("twenty-five Nova records and then one Acme record"). That is a distinct and transferable pagination-vs-authorization lesson, not filler.
- The regression test is a *real* HTTP test, not a helper call: `api.test.ts:4-13` boots `createApp()`, `server.listen(0)`, and `fetch`es the live port. The new case at `api.test.ts:35-58` logs in three distinct seeded actors and asserts all three arms (Acme-only for staff, both `version-security-v1` and `version-forklift-v1` for platform, `[]` for learner). Delete the helper call and that test fails — as `VERIFICATION.md` claims.
- `VERIFICATION.md` volunteers the most important caveat unprompted: "The Prisma schema elsewhere in the repository does not make these HTTP tests persistent-database integration tests." That is true — `grep -rn "PrismaClient" apps` returns nothing; the whole API runs off the module-level object in `apps/api/src/store.ts`. It also discloses a prior failed run that "invoked a missing Next executable".

## Problems found (evidence required)
- **[D1]** Astra added a broken link to the root `README.md`. Line 13 of the new Documentation Path reads ``13. `docs/code-walkthroughs/audit-log-scope/README.md` — tenant-scoped dashboard audit-log repair course``, but `ls docs/code-walkthroughs/` shows only `01-domain-rules.md` … `10-worker-boundary.md` and `README.md`. There is no `audit-log-scope` directory. The delivery JSON claims `courseLinksChecked: 23`, so whatever link check ran did not cover the README it edited.
- **[D2]** `visibleAuditLogs` (`services.ts:28-33`) re-implements the scope rule that already exists inside `services.auditLogs` (`services.ts:132-134`) rather than extracting one shared predicate. `02-CONCEPTS.md` even names the risk — "a future change cannot silently make the dashboard and audit-log endpoint disagree again" — but the delivered shape is two copies of `role === "PLATFORM_ADMIN" || log.organizationId === actor.organizationId`, which is precisely how they drifted the first time.
- **[D2]** The executable change is five lines plus two seed rows. It is correct and tested, but it is a small slice for a 3,800-word course; the store-seeding half of the diff is fixture work, not improvement.
- **[D3]** Four of five exercises in `05-PRACTICE.md` are prediction-only ("Which target IDs may appear?", "Why does their list contain both organizations?"). Only Exercise 4 asks the learner to change anything, and it requires hand-editing `store.ts` with no instruction on how to do so safely — the chapter just says "restore the fixture for the next actor or create a fresh store".
- **[D4]** There is no database, no transaction and no write path in this lesson at all. It teaches read-projection ownership and page-limit ordering well, but a junior will not learn Prisma, migrations or transactional writes here despite the batch's `prisma` tag.

## Spot-checks performed
- Course claim (`03-WORKED-CHANGE.md`): the original line was `auditLogs: actor.role === "LEARNER" ? [] : store.auditLogs.slice(0, 25)` -> diffed `backups/a1d53294d3b0/apps/api/src/services.ts:61` against the current file -> matches verbatim, and the `.txt` snapshot matches too.
- Course claim (`01-CODEBASE-MAP.md`): "The audit-log endpoint already calls the scoped service path" -> `services.ts:131-134` filters on `actor.role === "PLATFORM_ADMIN" || log.organizationId === actor.organizationId` and throws `Forbidden` for LEARNER -> matches; the premise of the whole lesson is true.
- Course claim (`VERIFICATION.md`): "passed **19 tests in three files**" -> `astraupskill/evidence/tests-root-01.log:97-98` "Test Files 3 passed (3) / Tests 19 passed (19)", process record `exitCode: 0` -> matches delivery `expectedTests: 19`.
- Course claim (`README.md` course file): "A Prisma schema is also present, but these dashboard tests do not use a persistent database" -> `ls prisma` fails; `package.json:11-12` points Prisma at `packages/database/prisma/schema.prisma`; no `PrismaClient` import exists under `apps/` -> matches, and the disclosure is accurate.
- Astra-added root README link to `docs/code-walkthroughs/audit-log-scope/README.md` -> `ls` of that path: "No such file or directory" -> **does not match**.

## Improvements needed (ordered, concrete, actionable)
1. Fix the root `README.md` line 13: point it at `astraupskill/README.md` (which does exist and is already linked lower in the same file), or delete the entry. (effort: S)
2. Extract one exported `auditLogScope(actor)` predicate in `apps/api/src/services.ts` and call it from both `visibleAuditLogs` and `services.auditLogs`, then add a test asserting the two endpoints return the same set for the same actor. This is the fix the course argues for but did not make. (effort: S)
3. Turn `05-PRACTICE.md` Exercise 4 into real work: add a `seedAuditLogs(count, organizationId)` test helper (or a `resetStore()` export) so the learner can actually build the 26-Nova/1-Acme fixture and watch filter-vs-slice ordering change the answer. Right now the decisive exercise cannot be run. (effort: M)
4. Add one write-path exercise — e.g. asserting that `createCourse` emits an audit row carrying the *actor's* `organizationId` — so the course covers at least one mutation and closes the loop between who writes audit records and who may read them. (effort: M)

## One-paragraph summary for the index
A compact lesson on a leak juniors write constantly: the team carefully scoped the dedicated `/audit-logs` endpoint by tenant, then assembled a *second* copy of the same data on the dashboard and forgot. The course makes you predict three role outcomes before running anything, and its central point — filter by owner *before* applying the page limit, or a noisy tenant eats your first page — is a genuinely good pagination-and-authorization idea. Its regression test is an honest end-to-end HTTP test against a real listening server, and the verification chapter is upfront that the "database" here is an in-memory object and that a Prisma schema sitting in the repo proves nothing. Take it for the read-path authorization habit; do not expect to learn Prisma or transactions from it, and note the root README link Astra added points at a directory that does not exist.
