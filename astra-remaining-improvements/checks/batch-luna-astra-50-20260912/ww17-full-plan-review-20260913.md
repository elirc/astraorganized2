# ww17 full-plan review — 2026-09-13

Read-only comparison of `4b702f01579b-plan.md` with the current stage implementation.

## Missing or incomplete planned behavior

1. **Health-config publish is still non-atomic at the service boundary.** `health-score-config-service.ts` calls `upsertActiveByTenant`, then `recordAuditLog`, then `recalculateTenantHealthScores`. A recalculation or audit failure leaves the new active config and deactivated prior config in place with stale/old snapshots. The Prisma repository transaction only covers deactivate/create, and reads `previous` before that transaction, so concurrent publishes can choose the same next version. The mock repository has the same split and no rollback. Required repair: one publish unit of work that pins/chooses the version inside the transaction, writes config/components, snapshots, and audit together (or an explicit pending/versioned state if recalculation is async), with mock clone/commit rollback coverage and a concurrent-version test.
2. **Prisma playbook creation does not validate owner/account tenant membership.** `createPlaybookRun` checks the account tenant but passes arbitrary `input.ownerUserId` into `prisma.playbookRun.create`. The plan requires owner existence in the same tenant. Add a tenant-scoped owner lookup/constraint before the write and a negative cross-tenant test.
3. **Playbook transition plus audit remains split.** `prisma-playbook-repository.updateStatus` conditionally updates, but `transitionPlaybookRunStatus` calls `recordAuditLog` afterward. Audit failure leaves the terminal status committed. The mock path mutates before audit as well. Add a transaction-scoped transition-and-audit repository method (or shared unit of work) and test rollback/no duplicate audit. Keep the expected-status compare-and-set.
4. **Renewal numeric validation is not visibly complete.** Confirm the runtime schema rejects non-finite confidence and negative forecast amounts; the service must retain trusted `context.actorUserId` and same-account completed-playbook attribution. Existing actor threading is good, but evidence should include the malformed numeric cases.
5. **Own-key transition guard needs an own-property test.** The current `isPlaybookStatus` uses `hasOwnProperty`, which is correct; add a regression for `__proto__`/inherited keys if the status input is widened or parsed outside the schema.

## Existing strengths

Tenant predicates and detached mock transition results are present; playbook expected-status compare-and-set, same-account completed attribution, health-config weight/unique-signal/floor validation, and trusted renewal actor assignment are directionally correct. The current seven tests do not establish the missing publish/transition rollback or Prisma owner checks.

Do not accept/apply until the three atomicity/ownership gaps have source coverage and fresh terminal evidence. Mock rollback is useful contract coverage but must remain labeled as distinct from PostgreSQL durability/concurrency proof.
