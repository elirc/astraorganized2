# _Organized Desktop/02 Build Projects/buildantigVG — fix report (B14)

Fable, 2026-09-18.

## Done
- review#1 15 evidence files copied into astraupskill/evidence/ and linked from VERIFICATION; review#5 the two-run composition is stated instead of hidden (no rerun possible here)
- review#2 03b-BREAK-IT.md (version predicate, tenant predicate, terminated guard) with predictions and a README link
- review#3 06 worked solution for exercise 1 (validation, shared where, UI, three tests)
- review#4 01 explains the draft vs editing state split in App.tsx

## Skipped
- review#5 no end-to-end rerun (needs the PostgreSQL bootstrap and Playwright); VERIFICATION states the two-run composition instead
- review#3 the exercise 1 solution is written in 06, not applied to the code (no dependencies staged for the NestJS workspace)

## Verification
- Documentation and evidence copies only; no code or tests changed, so no test run. Evidence files verified present under astraupskill/evidence/

## Course/code consistency check
- 03b quotes the real updateMany where clause from workers.ts; 01 describes the editing/draft state as declared in App.tsx; README links 03b.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (actor, tenant scope, version, conditional update, affected-row check, conflict, state transition table, read-only terminal state, referential precondition, audit entry, atomic acceptance, draft versus editing state). Verified every term against the source before citing it: the files `apps/api/src/auth.ts`, `apps/api/src/workers.ts`, `apps/api/prisma/schema.prisma`, `apps/api/src/validation.ts`, `apps/web/src/App.tsx`, and the symbols and identifiers `Actor`, `AuthGuard`, `request.actor`, `where: { id, tenantId: actor.tenantId }`, `version Int @default(1)`, `model Worker`, `tx.worker.updateMany({ where: { ..., version } })`, `if (result.count !== 1)`, `ConflictException`, `transitions`, `Workers.transition`, `TERMINATED`, `not: "TERMINATED"`, `Workers.company(tx, tenantId, companyId)`, `Workers.audit`, `tx.auditLog.create`, `db.$transaction`, `draft`, `editing`, `{ ...draft, version: editing.version }`.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `04-TESTING-AND-DEBUGGING.md` — quoted from root `package.json` test scripts (`test:api`/`test:web`/`test:e2e`)
- `07-TRACE-LAB.md` — quoted from `apps/api/src/workers.ts:233-246` (WorkersController routes)
