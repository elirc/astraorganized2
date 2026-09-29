import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'master4'; P = fe.REG[S]['abs']; os.chdir(P); done = []
SVC = 'src/server/modules/orders/orders.service.ts'

def svc(t):
    if 'requestedBySku' in t and 'randomUUID' in t: return t
    t = t.replace("import { planReservation } from '../../../shared/inventoryRules'", "import { randomUUID } from 'node:crypto'\nimport { applyReservation, planReservation } from '../../../shared/inventoryRules'", 1)
    old = """    for (const line of order.lines) {
      const balance = balances.find((item) => item.skuId === line.skuId)

      if (!balance) {
        continue
      }

      await tx.inventoryItem.update({
        where: { id: balance.id },
        data: { reserved: { increment: line.quantity } },
      })
      await tx.stockReservation.create({
        data: {
          id: `res-${order.id}-${line.skuId}-${Date.now()}`,
          salesOrderId: order.id,
          skuId: line.skuId,
          warehouseId: order.warehouseId,
          quantity: line.quantity,
          status: 'active',
          expiresAt: new Date(Date.now() + 72 * 60 * 60 * 1000),
        },
      })
    }
"""
    new = """    // Write per SKU, not per line: two lines for one SKU are one demand on one balance,
    // exactly as planReservation counted them. One reservation row per SKU.
    const requestedBySku = new Map<string, number>()
    for (const line of order.lines) {
      requestedBySku.set(line.skuId, (requestedBySku.get(line.skuId) ?? 0) + line.quantity)
    }

    for (const [skuId, quantity] of requestedBySku) {
      const balance = balances.find((item) => item.skuId === skuId)

      if (!balance) {
        // planReservation already reported a missing balance as a failure, so this is unreachable
        // on the success path; keep the guard so a future change cannot write against nothing.
        continue
      }

      // The pure rule is the guard at the write, not only at the plan: it throws (and the
      // transaction rolls back) if the aggregate would exceed available-to-promise.
      applyReservation(balance, quantity)

      await tx.inventoryItem.update({
        where: { id: balance.id },
        data: { reserved: { increment: quantity } },
      })
      await tx.stockReservation.create({
        data: {
          id: `res-${randomUUID()}`,
          salesOrderId: order.id,
          skuId,
          warehouseId: order.warehouseId,
          quantity,
          status: 'active',
          expiresAt: new Date(Date.now() + 72 * 60 * 60 * 1000),
        },
      })
    }
"""
    assert old in t, 'write loop not found'
    t = t.replace(old, new, 1)
    for prefix in ['audit-reservation-failed', 'evt-order-reserved', 'outbox-order-reserved', 'audit-order-reserved']:
        t = t.replace('`' + prefix + '-${Date.now()}`', '`' + prefix + '-${randomUUID()}`')
    assert '${Date.now()}`' not in t, 'a Date.now() id remains'
    return t
fe.rw(SVC, svc)
done.append('review#2 the write loop aggregates order lines by SKU and calls applyReservation as the guard at the write (no more dead guard, no double reservation rows)')
done.append('review#3 every Date.now()-based id in orders.service.ts is now randomUUID()-based')

open('tests/reservation-api.test.ts', 'w', encoding='utf-8', newline='\n').write('''import request from 'supertest'
import { afterAll, beforeAll, describe, expect, it } from 'vitest'
import { createApp } from '../src/server/app'
import { defaultTenantId, prisma } from '../src/server/db'
import { availableToPromise } from '../src/shared/inventoryRules'

// Uses the seeded SQLite database like tests/api.test.ts; everything it creates is removed afterwards.
const app = createApp()
const orderId = 'so-test-aggregate'
const skuId = 'sku-pack-black'
const warehouseId = 'wh-west'

describe('POST /api/orders/:orderId/reserve', () => {
  let available = 0
  let reservedBefore = 0
  let reservationsBefore = 0

  beforeAll(async () => {
    const balance = await prisma.inventoryItem.findUniqueOrThrow({ where: { warehouseId_skuId: { warehouseId, skuId } } })
    available = availableToPromise(balance)
    reservedBefore = balance.reserved
    reservationsBefore = await prisma.stockReservation.count()
    await prisma.salesOrder.create({
      data: {
        id: orderId, tenantId: defaultTenantId, warehouseId, orderNumber: 'SO-TEST-AGG', customerName: 'Aggregate Test',
        channel: 'Wholesale', status: 'pending_reservation', paymentStatus: 'authorized', priority: 'high',
        placedAt: new Date(), promisedShipBy: new Date(Date.now() + 86_400_000),
        // Two lines for one SKU: each fits on its own, together they exceed what is available.
        lines: { create: [
          { id: orderId + '-1', skuId, quantity: available, unitPriceCents: 100 },
          { id: orderId + '-2', skuId, quantity: 1, unitPriceCents: 100 },
        ] },
      },
    })
  })

  afterAll(async () => {
    await prisma.auditLog.deleteMany({ where: { entityId: orderId } })
    await prisma.stockReservation.deleteMany({ where: { salesOrderId: orderId } })
    await prisma.salesOrderLine.deleteMany({ where: { salesOrderId: orderId } })
    await prisma.salesOrder.deleteMany({ where: { id: orderId } })
  })

  it('refuses the aggregate demand, changes no inventory, and records exactly one failure audit row', async () => {
    const response = await request(app).post(`/api/orders/${orderId}/reserve`)

    expect(response.status).toBe(200)
    expect(response.body.ok).toBe(false)
    expect(response.body.failures).toHaveLength(1)
    expect(response.body.failures[0]).toMatchObject({ skuId, requested: available + 1, available })

    const balance = await prisma.inventoryItem.findUniqueOrThrow({ where: { warehouseId_skuId: { warehouseId, skuId } } })
    expect(balance.reserved).toBe(reservedBefore)
    expect(await prisma.stockReservation.count()).toBe(reservationsBefore)
    expect(await prisma.auditLog.count({ where: { entityId: orderId, action: 'order.reservation_failed' } })).toBe(1)
    expect((await prisma.salesOrder.findUniqueOrThrow({ where: { id: orderId } })).status).toBe('pending_reservation')
  })

  it('reserves once per SKU when the aggregate fits', async () => {
    await prisma.salesOrderLine.update({ where: { id: orderId + '-1' }, data: { quantity: 1 } })
    const response = await request(app).post(`/api/orders/${orderId}/reserve`)

    expect(response.body).toMatchObject({ ok: true, status: 'allocated' })
    const rows = await prisma.stockReservation.findMany({ where: { salesOrderId: orderId } })
    expect(rows).toHaveLength(1)
    expect(rows[0].quantity).toBe(2)
    const balance = await prisma.inventoryItem.findUniqueOrThrow({ where: { warehouseId_skuId: { warehouseId, skuId } } })
    expect(balance.reserved).toBe(reservedBefore + 2)
    // Undo the reservation so the seeded database is unchanged for the next test file.
    await prisma.inventoryItem.update({ where: { id: balance.id }, data: { reserved: reservedBefore } })
  })
})
''')
done.append('review#1 tests/reservation-api.test.ts: two lines for one SKU over the seeded balance -> 200 ok:false with requested = available+1, reserved and reservation count unchanged, exactly one order.reservation_failed audit row; then one reservation row per SKU when the aggregate fits')

fe.append_section(S, '07', '## Why time-based ids collide', """The delivered service built ids like `` `res-${order.id}-${line.skuId}-${Date.now()}` ``. Two lines for the same SKU in one order run inside one transaction within the same millisecond, so the two ids were identical and the second insert failed on the primary key; and two orders reserved in the same millisecond produced the same `evt-order-reserved-<ms>`. `Date.now()` has millisecond resolution and no uniqueness guarantee; it is a timestamp, not an identifier. The fix pass uses `crypto.randomUUID()` (122 random bits) for every generated id. Keep a readable prefix if it helps debugging, but never let the uniqueness depend on the clock. Predict: which of the two collisions would the suite have caught before the fix? (Only the same-order one, and only with a two-line fixture; the cross-order one needs two requests in the same millisecond, which a test cannot force reliably. That is why the id scheme, not a test, is the guard.)""", before='## ')
done.append('review#3 07 note on why time-based ids collide')
fe.append_section(S, '05', '## Exercise 5: a valid quantity against a missing balance row', """Seed an order whose SKU has no `InventoryItem` row in the order's warehouse (a real case: the SKU exists, it has simply never been stocked there). Predict the response before running: `planReservation` treats a missing balance as `available = 0`, so the plan fails and the write loop is never reached. Write the test in `tests/reservation-api.test.ts` style: assert `ok: false`, one failure with `available: 0`, no `InventoryItem` created as a side effect, exactly one `order.reservation_failed` audit row, and the order still `pending_reservation`. Then remove the `if (!balance) continue` guard in the write loop and confirm the test still passes (the plan protects it); put the guard back and explain in one sentence why it stays.""", before='## ')
fe.append_section(S, '06', '## Exercise 5 answer', """The plan is the guard: `planReservation` reports the missing balance as a failure with `available: 0` and the service returns before writing. The test proves three absences (no reserved change, no reservation row, no new balance row) and one presence (the failure audit row). The `continue` in the loop stays because the loop must never write against a `balance` it does not have, even if a future change makes the plan more permissive; a guard that is unreachable today is still the right shape for the code path.""", before='## ')
done.append('review#4 05 exercise 5 (missing balance row) with its answer in 06')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
