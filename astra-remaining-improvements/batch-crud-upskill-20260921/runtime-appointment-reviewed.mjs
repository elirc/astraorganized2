import test from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { loadTypeScript } from './helpers-load-typescript.mjs';

const fixedNow = new Date('2026-09-22T10:01:00Z');
class FixedDate extends Date {
  constructor(...args) { super(args.length ? args[0] : fixedNow.getTime()); }
  static now() { return fixedNow.getTime(); }
}
let appointment, failure, transactions, reads;
const updates = [], activities = [], audits = [];
const prisma = { $transaction: async callback => {
  transactions++;
  return callback({
    appointment: { update: async args => {
      updates.push(args);
      if (failure) throw failure;
      return { ...appointment, ...args.data };
    } },
    appointmentActivity: { create: async args => { activities.push(args); } },
    auditEvent: { create: async args => { audits.push(args); } }
  });
} };
const { appointmentsService } = await loadTypeScript('backend/src/modules/appointments/appointments.service.ts', {
  root: fileURLToPath(new URL('..', import.meta.url)),
  globals: { Date: FixedDate },
  stubs: {
    '@prisma/client': { AppointmentSource: {}, AppointmentStatus: { REQUESTED: 'REQUESTED', CONFIRMED: 'CONFIRMED', CANCELLED: 'CANCELLED', COMPLETED: 'COMPLETED', NO_SHOW: 'NO_SHOW', RESCHEDULED: 'RESCHEDULED' }, NotificationType: {}, Prisma: {} },
    '../../db/prisma.js': { prisma },
    '../../shared/utils/timezones.js': { assertValidTimezone: () => {}, convertLocalToUtc: () => { throw new Error('Unexpected timezone conversion'); } },
    '../../shared/utils/dates.js': { nowUtc: () => { throw new Error('Unexpected clock helper'); } },
    '../notifications/notifications.service.js': { notificationsService: {} },
    './recurrence.service.js': { recurrenceService: {} },
    './appointments.repository.js': { appointmentsRepository: { getById: async id => {
      reads++;
      assert.equal(id, 'appt-1');
      return appointment;
    } } }
  }
});
function reset(status = 'CONFIRMED') {
  appointment = { id: 'appt-1', status, startTimeUtc: new Date('2026-09-22T10:00:00Z') };
  failure = null;
  transactions = reads = 0;
  updates.length = activities.length = audits.length = 0;
}
function plain(value) { return JSON.parse(JSON.stringify(value)); }

test('real completion writes expected status, fixed timestamp, activity and audit', async () => {
  reset();
  const result = await appointmentsService.complete('appt-1', 'staff-1');
  assert.equal(result.status, 'COMPLETED');
  assert.equal(result.completedAt.getTime(), fixedNow.getTime());
  assert.equal(reads, 1);
  assert.equal(transactions, 1);
  assert.equal(updates.length, 1);
  assert.deepEqual(plain(updates[0].where), { id: 'appt-1', status: 'CONFIRMED' });
  assert.equal(updates[0].data.status, 'COMPLETED');
  assert.equal(updates[0].data.completedAt.getTime(), fixedNow.getTime());
  assert.deepEqual(plain(activities), [{ data: { appointmentId: 'appt-1', actorId: 'staff-1', action: 'APPOINTMENT_COMPLETED' } }]);
  assert.deepEqual(plain(audits), [{ data: { actorId: 'staff-1', entityType: 'Appointment', entityId: 'appt-1', action: 'APPOINTMENT_COMPLETED', ipAddress: null, userAgent: null } }]);
});
test('P2025 rejects before activity and actual audit helper', async () => {
  reset();
  failure = Object.assign(new Error('missing'), { code: 'P2025' });
  await assert.rejects(() => appointmentsService.complete('appt-1', 'staff-1'), error => error.code === 'APPOINTMENT_STATUS_CHANGED' && error.statusCode === 409);
  assert.equal(updates.length, 1);
  assert.equal(activities.length + audits.length, 0);
});
test('real domain rejects cancelled and already completed appointments before transaction', async () => {
  for (const status of ['CANCELLED', 'COMPLETED']) {
    reset(status);
    await assert.rejects(() => appointmentsService.complete('appt-1', 'staff-1'), error => error.code === 'INVALID_APPOINTMENT_STATUS_TRANSITION');
    assert.equal(transactions, 0);
    assert.equal(updates.length + activities.length + audits.length, 0);
  }
});
test('missing appointment returns real not-found error before transaction', async () => {
  reset(); appointment = null;
  await assert.rejects(() => appointmentsService.complete('appt-1', 'staff-1'), error => error.code === 'APPOINTMENT_NOT_FOUND' && error.statusCode === 404);
  assert.equal(transactions, 0);
  assert.equal(updates.length + activities.length + audits.length, 0);
});
test('unrelated update error retains identity without activity or audit', async () => {
  reset(); failure = new Error('database unavailable');
  await assert.rejects(() => appointmentsService.complete('appt-1', 'staff-1'), error => error === failure);
  assert.equal(updates.length, 1);
  assert.equal(activities.length + audits.length, 0);
});
