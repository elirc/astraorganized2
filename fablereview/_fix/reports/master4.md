# _Organized Desktop/03 Master Projects/master4 — fix report (B14)

Fable, 2026-09-18.

## Done
- review#2 the write loop aggregates order lines by SKU and calls applyReservation as the guard at the write (no more dead guard, no double reservation rows)
- review#3 every Date.now()-based id in orders.service.ts is now randomUUID()-based
- review#1 tests/reservation-api.test.ts: two lines for one SKU over the seeded balance -> 200 ok:false with requested = available+1, reserved and reservation count unchanged, exactly one order.reservation_failed audit row; then one reservation row per SKU when the aggregate fits
- review#3 07 note on why time-based ids collide
- review#4 05 exercise 5 (missing balance row) with its answer in 06

## Skipped
- (none)

## Verification
- npx vitest run with DATABASE_URL=file:./dev.db via junctioned stage node_modules: 3 files, 14 tests passed (12 delivered + 2 reservation API tests); the seeded prisma/dev.db was byte-identical after the run (tests clean up); npm run typecheck exit 0; junction removed

## Course/code consistency check
- 07 explains the id collision the code no longer has; 05 exercise 5 and its 06 answer describe the missing-balance path as the code implements it (plan fails before the write loop).

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (on hand, reserved, available to promise, demand pool, reservation plan, failure reason, apply reservation, order status transition, stock reservation row, balance key, transaction boundary, outbox message). Verified every term against the source before citing it: the files `src/shared/inventoryRules.ts`, `prisma/schema.prisma`, `src/server/modules/orders/orders.service.ts`, and the symbols and identifiers `onHand`, `model InventoryItem`, `reserved`, `InventoryBalance`, `availableToPromise`, `requestedBySku`, `planReservation`, `planReservation(lines, balances)`, `failures`, `applyReservation(balance, quantity)`, `model StockReservation`, `@@unique([warehouseId, skuId])`, `db.$transaction`, `reserveSalesOrder`, `orders.service.ts`, `tx.outboxMessage.create`, `model OutboxMessage`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 04, 07. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **04** - tests/inventoryRules.test.ts (duplicate SKU aggregation case)
- **07** - src/shared/inventoryRules.ts (planReservation)

No source code was changed; only the chapter Markdown.
