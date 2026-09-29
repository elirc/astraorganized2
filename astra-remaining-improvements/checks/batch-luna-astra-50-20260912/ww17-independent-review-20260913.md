# ww17 independent early review — 2026-09-13

Decision: HOLD pending concrete repairs. The current eight-test suite does not establish the full plan.

1. `src/repositories/prisma/prisma-health-config-repository.ts` computes `previous.version + 1` inside a normal transaction but has no tenant/version uniqueness or serialization guard. Two concurrent publishes can both select the same previous version and create duplicate versions; both can deactivate/read active state independently. Add a database-enforced per-tenant version invariant or explicit serializable/locking retry, and a regression showing one winner/unique versions. The mock `publishActiveByTenant` has the same unguarded read/increment and no concurrency test.
2. Config publish rollback is only structurally present. `platform-behavior.test.ts` exercises one success; it injects no failure after config deactivation, snapshot replacement, or audit insertion. Add a transactional fake that fails at each post-write boundary and proves config active row, snapshots, and audit are unchanged. Cover both mock and Prisma-shaped adapter path as the plan requires.
3. Playbook update path has a transaction in Prisma and clone/rollback in mock, but no regression for audit failure/rollback, competing terminal updates, foreign-tenant direct adapter update, or exact detached `from`/`to` audit snapshots. Add tests with a transaction-scoped fake (failure after mutation) and two competing updates, asserting one winner and no duplicate audit.
4. `src/repositories/prisma/prisma-playbook-repository.ts` direct `create` trusts `input.ownerUserId`; same-tenant owner existence is enforced only in `playbook-service.ts`. If repository boundary is part of the promised adapter parity, add a DB relation/transaction check or document service-only boundary and test route/service plus direct adapter behavior.
5. Renewal schema validates finite confidence/nonnegative amount, and service derives `updatedByUserId`, but there is no regression for foreign account, wrong-tenant attribution, incomplete playbook, or invalid numeric inputs in the route/service suite.
6. `updateActiveByTenant` remains a separate non-publish path and can leave config/snapshots/audit inconsistent if called; either remove/privatize it or make it obey the same atomic publish contract.

The current positive config test and seven other behavior tests are useful smoke coverage, but cannot close these race and rollback requirements.

## Repair update — 2026-09-13

The stage now adds a tenant/version uniqueness constraint, mock concurrent publish and playbook race tests, renewal attribution/numeric edge tests, typed Prisma audit JSON, and fresh 12-test, typecheck, lint, and preflight records. The original hold findings are addressed to the extent possible without a live PostgreSQL server; the delivery limits correctly state that mock tests do not prove cross-process database isolation. A fresh production build and bounded peer review remain required before application.
