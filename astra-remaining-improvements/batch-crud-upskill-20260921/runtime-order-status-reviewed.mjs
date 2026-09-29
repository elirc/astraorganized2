import test from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { loadTypeScript } from './helpers-load-typescript.mjs';

const actor = { id: 'admin-1', email: 'admin@example.test', role: 'ADMIN' };
let order, failure, transactionCalls;
const updates = [], audits = [], notifications = [];
const prisma = {
  order: { findUniqueOrThrow: async (args) => {
    assert.equal(args.where.id, 'order-1');
    assert.equal(args.include.splits, true);
    return order;
  } },
  $transaction: async (callback) => {
    transactionCalls++;
    return callback({
      order: { update: async (args) => {
        updates.push(args);
        if (failure) throw failure;
        return { ...order, status: args.data.status };
      } },
      auditLog: { create: async (args) => { audits.push(args); } }
    });
  }
};
const { updateOrderStatus } = await loadTypeScript('src/server/orders/service.ts', {
  root: fileURLToPath(new URL('..', import.meta.url)),
  stubs: {
    // Load actual order-state and ApiError modules; substitute only unused Zod error handling.
    zod: { ZodError: class extends Error {} },
    '@/server/db/prisma': { prisma },
    '@/server/notifications/service': { notifyOrderStatus: async (args) => { notifications.push(args); } },
    '@/server/payments/stripe-connect': { issueOrderRefund: async () => { throw new Error('Unexpected refund'); } },
    'server-only': {}
  }
});
function reset(status = 'PLACED') {
  order = { id: 'order-1', orderNumber: 'ORD-1', buyerId: 'buyer-1', status, splits: [{ sellerId: 'seller-1' }] };
  failure = null;
  transactionCalls = 0;
  updates.length = audits.length = notifications.length = 0;
}
function plain(value) { return JSON.parse(JSON.stringify(value)); }

test('legal payment transition scopes status and records event, audit and notification', async () => {
  reset();
  const result = await updateOrderStatus({ actor, orderId: 'order-1', status: 'PAID', requestId: 'req-1' });
  assert.equal(result.status, 'PAID');
  assert.equal(transactionCalls, 1);
  assert.equal(updates.length, 1);
  assert.deepEqual(plain(updates[0].where), { id: 'order-1', status: 'PLACED' });
  assert.equal(updates[0].data.status, 'PAID');
  assert.equal(updates[0].data.events.create.status, 'PAID');
  assert.equal(updates[0].data.events.create.metadata.actorId, actor.id);
  assert.equal(audits.length, 1);
  assert.deepEqual(plain(audits[0].data.metadata), { from: 'PLACED', to: 'PAID' });
  assert.equal(audits[0].data.requestId, 'req-1');
  assert.deepEqual(plain(notifications), [{ buyerId: 'buyer-1', orderNumber: 'ORD-1', status: 'PAID' }]);
});
test('P2025 status conflict maps to 409 before audit or notification', async () => {
  reset();
  failure = Object.assign(new Error('missing'), { code: 'P2025' });
  await assert.rejects(() => updateOrderStatus({ actor, orderId: 'order-1', status: 'PAID' }),
    error => error.code === 'ORDER_STATUS_CHANGED' && error.status === 409);
  assert.equal(updates.length, 1);
  assert.equal(audits.length, 0);
  assert.equal(notifications.length, 0);
});
test('seller outside order scope is rejected before transaction', async () => {
  reset('PAID');
  const seller = { id: 'seller-user', email: 'seller@example.test', role: 'SELLER', sellerId: 'seller-2' };
  await assert.rejects(() => updateOrderStatus({ actor: seller, orderId: 'order-1', status: 'SHIPPED' }),
    error => error.code === 'ORDER_SELLER_SCOPE_FORBIDDEN');
  assert.equal(transactionCalls, 0);
  assert.equal(updates.length + audits.length + notifications.length, 0);
});
test('unrelated update failure passes through the catch unchanged', async () => {
  reset();
  failure = new Error('database unavailable');
  await assert.rejects(() => updateOrderStatus({ actor, orderId: 'order-1', status: 'PAID' }), error => error === failure);
  assert.equal(updates.length, 1);
  assert.equal(audits.length + notifications.length, 0);
});
test('real domain rule rejects an illegal transition before persistence', async () => {
  reset('REFUNDED');
  await assert.rejects(() => updateOrderStatus({ actor, orderId: 'order-1', status: 'PAID' }), /ORDER_INVALID_TRANSITION:REFUNDED->PAID/);
  assert.equal(transactionCalls, 0);
  assert.equal(updates.length + audits.length + notifications.length, 0);
});
test('in-scope seller preserves legal fulfillment path', async () => {
  reset('PAID');
  const seller = { id: 'seller-user', email: 'seller@example.test', role: 'SELLER', sellerId: 'seller-1' };
  const result = await updateOrderStatus({ actor: seller, orderId: 'order-1', status: 'SHIPPED' });
  assert.equal(result.status, 'SHIPPED');
  assert.deepEqual(plain(updates[0].where), { id: 'order-1', status: 'PAID' });
  assert.equal(audits.length, 1);
  assert.equal(notifications.length, 1);
});
