# Final review: ww27 (`2c7ac2b52738`)

Decision: **REJECTED — do not deliver**.

The staged code and manifest hashes are complete for the declared intentional files, and the recorded test/typecheck/build/Prisma/lint checks pass. Two required behaviors remain unproven or incorrect:

1. `ApiVersionService.updateRollout` writes the new rollout through `versionCatalogRepository.updateRollout`, then records the audit event. If audit persistence fails, the rollout update remains committed. The plan explicitly calls for rollout atomicity, and the delivery limits acknowledge that audit/profile writes are not proven atomic across real database connections. There is no transaction/compensation path and no failure test asserting the runtime rollout is restored after an audit failure. This can leave live traffic controls changed without the required audit record.

2. The staged `next-env.d.ts` differs from canonical (adds `./.next/types/routes.d.ts` and changes the generated note) but is absent from the delivery manifest. It is a generated artifact/config delta from the build and must be restored to the baseline before delivery or explicitly included with its tested hash. The complete changed-file coverage requirement prohibits silently omitting it.

The focused tests do cover presence-aware v1/v2 patches including explicit `false`, unknown versions, client ownership, archived reactivation, empty/no-op input, rollout 0/100, and invalid rollout candidates, but they do not close the atomic rollout failure case.

Required repair evidence: add a real rollback/transaction boundary around rollout plus audit (and a test that injects audit failure and checks repository state/audit unchanged), then re-freeze and rerun checks. Resolve the `next-env.d.ts` generated delta in the new manifest. Canonical ww27 was not modified and no delivery was applied.
