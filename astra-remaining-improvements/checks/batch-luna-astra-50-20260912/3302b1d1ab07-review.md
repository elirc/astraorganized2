# Master4 independent Astra review

Decision: APPROVED — implementation, bounded test evidence and repaired learning guides accepted for the stated scope.

## Implementation and wiring

Reviewed `src/shared/inventoryRules.ts`, its original snapshot, `tests/inventoryRules.test.ts`, the actual `reserveSalesOrder` service and Express reservation route. The service reads balances for the order warehouse and calls `planReservation(order.lines, balances)` before inventory/reservation/order/event/outbox writes. Grouping duplicate SKU demand therefore repairs the actual reservation decision path. The existing failed-decision branch writes a failure audit, so rejection does not mean every database table is unchanged.

The 14 + 9 regression correctly fails the old per-line algorithm by inspection: both lines independently fit within 22, so the original returns success, while the new rule reports one failure for 23. Invalid-quantity tests check the validation reason, distinguishing it from the old missing-balance failure. The direct `applyReservation` zero/over-availability tests also fail the original unguarded helper. `applyReservation` is a pure helper, not the mutation function used by `reserveSalesOrder`; the planner is the real service integration point.

No source repair requested. This patch does not establish concurrent reservation correctness or exhaustively validate all inventory balance state. Those are outside the chosen duplicate-line and direct quantity boundary.

## Evidence inspected

- Exact original snapshot SHA-256 matches the baseline hash for `src/shared/inventoryRules.ts`.
- `inventory-rules.json` and raw log: exit 0, 1 test file, 9 tests.
- `full-test-absolute.json` and raw log: exit 0, 2 files, 12 tests, with absolute staged SQLite `DATABASE_URL`.
- `typecheck-2.json` and raw log: exit 0, `tsc --noEmit`.
- `build-2.json` and raw log: exit 0, TypeScript check and Vite client build.
- Actual API tests are health, seeded dashboard read and CSV export. They do not execute reservation writes, duplicate-line persistence, rollback or concurrent reservations.

Reviewed source SHA-256: `bce8e7fd3d5ccf886241fb6347451c2580ebfdd4f2fa4ddebef3f57b611b2e7a`.
Reviewed test SHA-256: `be8cad44448297e63dca3f114583d21d4faf151c0eb5790933ebf22867b19870`.

## Documentation repairs completed

1. Chapter 06 promises complete solutions but paraphrases exercises 1–3. Supply complete pasteable test/implementation solutions with fixture/imports or precise insertion context. Answer exercise 4 with the explicit list of actual written records and the failure-audit distinction.
2. Chapter 04 claims an existing missing-balance test; none exists in the reviewed test file. Remove or clearly label it a proposed exercise.
3. `VERIFICATION.md` repeats the failed relative-database commands and lacks observed final results. Record the successful absolute SQLite URL setup/check sequence and evidence labels, 9 pure domain tests plus 3 API read/health tests, and actual typecheck/build outcomes. Do not imply reservation persistence coverage.

The reviewer repaired chapters 04, 06 and 07. Chapter 06 now supplies complete exercise-matched pasteable tests with exact fixture/insertion context, the full guarded helper implementation, explicit success records and a worked failure-audit review. Chapter 04 identifies actual tests and accurately separates pure domain tests from read-only API coverage. Chapter 07 distinguishes predicted arithmetic from experimental proof and documents HTTP 200 with `ok: false` plus a failure audit.

Root's revised `VERIFICATION.md` was independently read and accepted. It records 12 unique tests, the actual successful evidence labels, generation/build results, and absolute-path seed/test instructions. The warning that custom `db:push` recreates `prisma/dev.db` regardless of `DATABASE_URL` was checked against `prisma/create-sqlite-schema.ts`; reproduction is correctly confined to a disposable copy.

The remaining guides were checked against the actual Express role gate, client reservation path, Prisma warehouse/SKU unique constraint, order-line integer quantity and transaction service. No further factual map repair was required. All nine guides have balanced code fences. Source and test SHA-256 values remain exactly those recorded above; no source/test/spec edits or executable reruns were made during these docs-only repairs.
