from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/4e19ba5b5028'
p=P/'tests/runtime-notification-open-lab.test.mjs';t=p.read_text()
t='\n'.join(l for l in t.split('\n') if not l.startswith('class ApiError'))
t=t.replace("  UserRole:", "  Prisma: {},\n  BatchStatus: Object.fromEntries(['QUEUED','COMPLETED','FAILED','PARTIAL_FAILURE','PROCESSING'].map(x=>[x,x])),\n  NotificationStatus: Object.fromEntries(['QUEUED','COMPLETED','FAILED','PARTIAL_FAILURE','PROCESSING'].map(x=>[x,x])),\n  UserRole:")
t=t.replace("  '@/lib/http/api-errors': { ApiError },", "  'zod': { ZodError: class extends Error {} },")
a=t.index('const permissionModule');b=t.index('\nfunction fixture',a)
t=t[:a]+"const actualRepository = await loadTypeScript('src/repositories/notificationRepository.ts', { root, stubs: { '@prisma/client': prismaEnums, '@/lib/db': { prisma: {} } } });\n"+t[b:]
t=t.replace("    '@/lib/auth/permissions': permissionModule,\n",'')
t=t.replace("deriveNotificationStatus: statuses => statuses.every(s => s === 'OPENED') ? 'COMPLETED' : 'PARTIAL_FAILURE', deriveBatchStatus: statuses => statuses.every(s => s === 'COMPLETED') ? 'COMPLETED' : 'PARTIAL_FAILURE'", "deriveNotificationStatus: actualRepository.deriveNotificationStatus, deriveBatchStatus: actualRepository.deriveBatchStatus")
t+='''
test('mixed failed and opened deliveries use actual aggregate policy', async () => {
  const f = fixture();
  f.repos.getDeliveryStatusesForNotification = async () => [{ status: 'OPENED' }, { status: 'FAILED' }];
  f.repos.getNotificationStatusesForBatch = async () => [{ status: 'COMPLETED' }, { status: 'PARTIAL_FAILURE' }];
  await (await serviceFor(f)).markNotificationOpenedForSession(viewer, 'notification-1');
  assert.deepEqual(f.calls.slice(2,4), [['notification-status', 'notification-1', 'PARTIAL_FAILURE'], ['batch-status', 'batch-1', 'PARTIAL_FAILURE']]);
});

test('aggregate write failure propagates after open writes and prevents audit', async () => {
  const f = fixture(); const failure = new Error('aggregate unavailable');
  f.repos.updateNotificationStatus = async () => { throw failure; };
  await assert.rejects((await serviceFor(f)).markNotificationOpenedForSession(viewer, 'notification-1'), e=>e===failure);
  assert.deepEqual(f.calls, [['open-deliveries', ['delivery-1']], ['opened-at', 'notification-1']]);
});
'''
p.write_text(t)
s=B/'specs/4e19ba5b5028.json';d=json.loads(s.read_text(encoding='utf-8-sig'))
d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')]
d['summary']=[n.replace('four executed','six executed') for n in d['summary']]
d['limits'].append('Real service, permissions, ApiError and repository aggregate functions execute. Prisma enum exports and unused rendering/Zod imports are adapted. Open tracking has no encompassing transaction; aggregate failure can follow earlier open writes.')
s.write_text(json.dumps(d,indent=2))
