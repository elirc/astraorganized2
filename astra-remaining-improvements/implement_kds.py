from pathlib import Path
S=Path(__file__).resolve().parent/'stage'/'e2d8f836b7f9'
p=S/'server/src/routes/api.js';t=p.read_text(encoding='utf-8')
a=t.index("  router.patch('/menu-items/:menuItemId/availability'");b=t.index("  router.post('/orders'",a)
t=t[:a]+'''  router.patch('/menu-items/:menuItemId/availability', (req, res) => {
    const payload = validateOrRespond(availabilitySchema, req.body, res);
    if (!payload) return;
    const item = db.prepare('SELECT id FROM menu_items WHERE id = ?').get(req.params.menuItemId);
    if (!item) return res.status(404).json({ message: 'Menu item not found' });

    // One transaction owns availability, affected items, parent summaries and audit records.
    const result = db.transaction(() => {
      const now = new Date().toISOString();
      db.prepare('UPDATE menu_items SET is_available = ?, updated_at = ? WHERE id = ?')
        .run(payload.isAvailable ? 1 : 0, now, item.id);
      recordEvent('menu_item.availability_changed', null, null, {
        menuItemId: item.id, isAvailable: payload.isAvailable, reason: payload.reason || null
      });
      const affectedOrderIds = new Set();
      if (!payload.isAvailable) {
        const affected = db.prepare(`SELECT id, order_id FROM order_items
          WHERE menu_item_id = ? AND status IN ('queued', 'started', 'cooking')`).all(item.id);
        for (const orderItem of affected) {
          db.prepare('UPDATE order_items SET status = ?, is_eighty_sixed = 1, notes = ?, updated_at = ? WHERE id = ?')
            .run('eighty_sixed', payload.reason || '86d mid-service', now, orderItem.id);
          affectedOrderIds.add(orderItem.order_id);
          recordEvent('order_item.eighty_sixed', orderItem.order_id, orderItem.id, {
            reason: payload.reason || '86d mid-service', source: 'menu_item_availability'
          });
        }
      }
      const orders = Array.from(affectedOrderIds, recomputeOrder).filter(Boolean);
      const updatedItem = db.prepare('SELECT id, name, station, is_available, updated_at FROM menu_items WHERE id = ?').get(item.id);
      return { item: updatedItem, orders, affectedOrders: Array.from(affectedOrderIds) };
    })();

    // Network notifications describe committed state; they cannot roll back a database write.
    for (const order of result.orders) emit('order_updated', order);
    emit('menu_item_updated', result.item);
    return res.json({ item: result.item, affectedOrders: result.affectedOrders });
  });

'''+t[b:]
# Keep HTTP validation outside; group each complete successful write and audit in a transaction.
a=t.index("  router.patch('/orders/:orderId/priority'");b=t.index("  router.patch('/order-items/:itemId/status'",a)
segment=t[a:b];start=segment.index("    db.prepare('UPDATE orders SET priority");end=segment.index("    emit('order_updated', updated);")
body=segment[start:end].replace('    const updated = getOrderById(req.params.orderId);','    return getOrderById(req.params.orderId);')
segment=segment[:start]+'    const updated = db.transaction(() => {\n'+''.join('  '+line+'\n' for line in body.rstrip().splitlines())+'    })();\n'+segment[end:];t=t[:a]+segment+t[b:]
for route,next_route in [("  router.patch('/order-items/:itemId/status'","  router.patch('/order-items/:itemId/eighty-six'"),("  router.patch('/order-items/:itemId/eighty-six'","  router.get('/stations/:station/board'")]:
 a=t.index(route);b=t.index(next_route,a);segment=t[a:b];start=segment.index('    const now = new Date().toISOString();');end=segment.index("    emit('item_updated', item);");body=segment[start:end]
 segment=segment[:start]+'    const { item, order } = db.transaction(() => {\n'+''.join('  '+line+'\n' for line in body.rstrip().splitlines())+'      return { item, order };\n    })();\n\n'+segment[end:];t=t[:a]+segment+t[b:]
p.write_text(t,encoding='utf-8')
p=S/'server/src/lib/validation.js';t=p.read_text();old='includeLateOnly: z.coerce.boolean().optional()';assert old in t;t=t.replace(old,"includeLateOnly: z.enum(['true', 'false']).transform(value => value === 'true').optional()");p.write_text(t)
p=S/'server/src/lib/kdsService.js';t=p.read_text();old='} else if ((counts.active_count || 0) > 0) {';assert old in t;t=t.replace(old,'} else if ((counts.active_count || 0) + terminalCount > 0) {');p.write_text(t)
p=S/'client/src/App.jsx';t=p.read_text();t=t.replace("    const reason = window.prompt('Reason for 86 item (optional):') || undefined;","    const answer = window.prompt('Reason for 86 item (optional):');\n    if (answer === null) return;\n    const reason = answer.trim() || undefined;");t=t.replace("      reason = window.prompt(`Reason for 86'ing ${menuItem.name}:`) || undefined;","      const answer = window.prompt(`Reason for 86'ing ${menuItem.name}:`);\n      if (answer === null) return;\n      reason = answer.trim() || undefined;");t=t.replace("      socket.off('kds_event', onKitchenEvent);","      socket.off('kds_event', onKitchenEvent);\n      clearTimeout(refreshTimerRef.current);\n      refreshTimerRef.current = null;");p.write_text(t)
print('Kitchen transaction, query, aggregate and cancellation fixes staged')
