import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-14-appointment-booking'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

model = open('server/src/models/appointmentModel.ts', encoding='utf-8-sig').read().replace('\r\n', '\n')
ml = model.split('\n')
e = next(i for i, l in enumerate(ml) if 'function ensureNoConflict' in l)
ensure = '\n'.join(ml[e:e + 22])
c = next(i for i, l in enumerate(ml) if 'export async function createAppointment' in l)
create = '\n'.join(ml[c:c + 24])

# --- review #1: make the confirmed-only coupling explicit + test
def patch_test(t):
    add = '''
test("only confirmed rows hold a slot: a cancelled row does not block, a confirmed one does", async () => {
  // Policy pinned here: ensureNoConflict only considers status = 'confirmed'.
  // (The status CHECK constraint allows confirmed, cancelled_by_customer, cancelled_by_provider, completed, no_show.)
  await h.db("appointments").insert({
    provider_id: 1, customer_id: 4, service_id: 1, status: "cancelled_by_customer",
    start_time: new Date("2099-02-01T09:00:00Z"), end_time: new Date("2099-02-01T09:30:00Z"), price: 10,
  });
  const overCancelled = await book("2099-02-01T09:00:00Z");
  assert.equal(overCancelled.status, 201, JSON.stringify(overCancelled.data));
  const overConfirmed = await book("2099-02-01T09:15:00Z");
  assert.equal(overConfirmed.status, 409);
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('test/booking.test.ts', patch_test)
fe.append_section(S, '03', '## Which rows hold a slot', """`ensureNoConflict` in `server/src/models/appointmentModel.ts` only looks at appointments whose `status` is `confirmed`. Two consequences follow, and both are now pinned by the fourth test. First, a cancelled, completed or no-show row never blocks a booking, so a slot is free the moment a customer cancels (the status `CHECK` constraint in the migration allows only `confirmed`, `cancelled_by_customer`, `cancelled_by_provider`, `completed` and `no_show`; there is no `pending`). Second, new bookings hold their slot only because `createAppointment` in `services/appointmentService.ts:125` inserts them with `status: "confirmed"`; if a future `pending` status were added and inserted there instead, two customers could book the same time and both succeed. The policy is a product decision (a provider who wants to approve bookings would add `pending` to the constraint and make it hold the slot). If you change it, change `ensureNoConflict`, the reschedule path in `updateAppointment` (which only re-checks when `next.status === "confirmed"`), and the test together.""", before='## How to reason through the code')
done.append('review#1 03 states the confirmed-only slot policy and the coupling to appointmentService.ts:125; new test pins it (a cancelled row does not block, a confirmed one does)')

# --- review #3: half-open interval box
fe.append_section(S, '02', '## Half-open intervals: why `start < otherEnd && end > otherStart`', """A 30-minute appointment at 10:00 occupies `[10:00, 10:30)`: it includes 10:00 and excludes 10:30. Two appointments overlap exactly when each starts before the other ends: `newStart < existingEnd && newEnd > existingStart`. Work the four cases before you read the SQL in `ensureNoConflict`:

| existing | new | `newStart < existingEnd` | `newEnd > existingStart` | overlap? |
|---|---|---|---|---|
| 10:00-10:30 | 11:00-11:30 (disjoint) | 11:00 < 10:30 false | | no |
| 10:00-10:30 | 10:30-11:00 (adjacent) | 10:30 < 10:30 **false** | | no |
| 10:00-10:30 | 10:15-10:45 (partial) | 10:15 < 10:30 true | 10:45 > 10:00 true | yes |
| 10:00-11:00 | 10:15-10:45 (contained) | true | true | yes |

With `<=` and `>=` the adjacent case would be flagged as a conflict and back-to-back bookings would be impossible; the second test (`10:30` right after a `10:00` half-hour) depends on the strict comparison. The same predicate, written in SQL, is `start_time < ? AND end_time > ?` with the new end and start as parameters.""")
done.append('review#3 02 half-open-interval box with the four worked cases')

B = [
("the booking form decides what to send",
 "`client/src/features/booking/*`: the slot picker shows times computed by `slotService.ts` on the server, and the form posts `{ providerId, serviceId, startTime, notes }` through `bookAppointment` (`client/src/services/api.ts:33`). The client never sends an end time: duration comes from the service on the server, so a tampered client cannot book a longer slot."),
("the request leaves the browser",
 "`client/src/services/api.ts`: the axios instance adds the demo `x-user-id`; `bookAppointment` posts to `/appointments`, reschedule puts to `/appointments/:id/reschedule`. `unwrap()` reads the envelope; a 409 surfaces as `That time slot is no longer available`, which the UI shows next to the picker so the customer can choose again."),
("the route validates the shape",
 "`server/src/routes/appointmentRoutes.ts` mounts `validateBody(...)` from `appointmentValidators.ts` (integer ids, ISO `startTime`, optional notes) in front of the controller; `middleware/validate.ts` replaces `req.body` with the parsed data. Business rules are not here: whether the provider accepts bookings, whether the service belongs to the provider, and whether the slot is free are decided lower down."),
("the service resolves the entities and computes the interval",
 "`createAppointment` in `services/appointmentService.ts` (line 40 onwards): load the provider (404 if not accepting), load the service and check `service.provider_id === input.providerId` and `is_active`, compute `endTime = start + duration_minutes`, run a first `findConflictingAppointments` for an early 409, then call the model with `status: \"confirmed\"` (line 125). The early check is advisory: the decisive one happens under the lock in the model."),
("the model locks the provider and decides under the lock",
 "`appointmentModel.createAppointment` (line 81): `db.transaction` -> `provider_profiles ... forUpdate()` -> `ensureNoConflict(trx, values)` (the half-open overlap query against `status = 'confirmed'`) -> insert `appointments` -> insert `notifications`. Two concurrent bookings serialize on the provider row; the second re-runs the overlap query after the first committed and throws `ConflictError`. The third test rejects the notification insert with a trigger and shows the appointment row was rolled back with it."),
("the envelope tells the client what happened",
 "`utils/errors.ts` `ConflictError` carries 409; `errorMiddleware.ts` maps it to `{ success: false, error: { message, code: \"CONFLICT\" } }`; success is 201 with the row. The first test asserts `[201, 409]` from two racing bookings, then counts one appointment and one notification directly in the database."),
]
fe.set_boundaries(S, B); done.append('review#2 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the four drawings must include the adjacent case and evaluate both inequalities for each; then run the second test with `<=` substituted on a throwaway branch and show that the adjacent booking becomes a 409, which is the observable consequence of getting the interval wrong.",
"stored instants (`start_time`, `end_time` as `timestamptz`) must not change; formatting must use the provider's `timezone` column with `Intl.DateTimeFormat` or `date-fns-tz`; your example must cross a daylight-saving transition and show the same instant rendered with two different wall-clock offsets.",
"start a confirmed appointment A at 10:00 and another B at 11:00; run `book(10:30)` and `reschedule(B -> 10:30)` in a `Promise.all`; assert that at most one row occupies 10:30-11:00 afterwards, whichever won, and that the loser's row is unchanged (B still at 11:00 if it lost); explain that both paths take the provider lock before `ensureNoConflict`.",
"the policy service must be called under the provider lock inside the model transaction (not only in the picker), must reject past times, closed days and buffer violations with 400 and slot conflicts with 409, and must state what happens when a cancelled appointment is reopened (it goes through `ensureNoConflict` again because `updateAppointment` re-checks when `next.status === \"confirmed\"`).",
]
fe.set_reviews(S, R); done.append('review#4 / 2.3 per-exercise review criteria (06)')

excerpt = '// models/appointmentModel.ts:' + str(c + 1) + '\n' + create + '\n\n// models/appointmentModel.ts:' + str(e + 1) + '\n' + ensure
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/65/server/src/models/appointmentModel.ts` with `diff --strip-trailing-cr -w`): `createAppointment` now locks the provider row, re-runs `ensureNoConflict` under that lock, and inserts the appointment and its notification in one transaction. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows the changed model transaction and the overlap check')

fe.set_variations(S, """**Normal variation — back to back.** Book 10:00 and then 10:30 for the 30-minute service. Predict 201 and 201, two `confirmed` rows, two notifications. Then book 10:15: predict 409 and no new row.

**Invalid variation — a service from another provider.** Insert a second provider with its own service in `psql` and post `{ providerId: 1, serviceId: <other> }`. Predict 404 `Service not found` (the service exists but belongs to someone else) and no row. Then post a malformed `startTime`: predict 400 from `validateBody`, before any query.

**Boundary variation — the race.** Reproduce the first test: two identical bookings in a `Promise.all`. Predict `[201, 409]` and one row. Then remove the provider `forUpdate()` on a throwaway branch and repeat until you see `[201, 201]` and two overlapping confirmed rows; restore it and explain which query read stale data."""); done.append('2.4 three concrete variations')

fe.add_exercise(S, 'ownership across the two roles',
"""Customers act through `x-user-id` and providers through their `provider_profiles.user_id`. Check every path that changes an appointment for the right owner.

1. List the write routes in `appointmentRoutes.ts` and, for each, which identity must match: `cancelCustomerAppointment` and `rescheduleAppointment` compare `appointment.customer_id`; `updateProviderAppointmentStatus` must compare the appointment's `provider_id` with the caller's provider profile.
2. Write three tests: customer 4 cannot cancel or reschedule an appointment booked by another customer (404, row unchanged); a provider user cannot mark another provider's appointment completed (404); the owning provider can.
3. Make the provider-side check happen under the same provider lock as the status write (inside `updateAppointment`'s transaction), so an appointment cannot be reassigned between the check and the write.

Acceptance is the three tests plus one sentence explaining why both roles get 404 rather than 403.""",
"""Reference for the provider-side check inside the transaction:

```typescript
// in updateAppointment(id, values, { providerId }) after the provider lock:
if (providerId !== undefined && found.provider_id !== providerId)
  throw new NotFoundError("Appointment not found");
```

Reference test skeleton: insert user 5 (customer) and book as 4; `api("/appointments/<id>/cancel", "POST", {}, { "x-user-id": "5" })` -> 404 and `status` still `confirmed`; insert a second provider profile for user 6 and call the provider status route as 6 -> 404; as 1 -> 200.

Review: explain why a customer-owned check can run before the transaction (a single-row update scoped by `customer_id` is enough) while the provider-side check belongs inside it (the same transaction re-checks overlaps)."""); done.append('2.5 ownership/authz exercise 7 across customer and provider roles (05, 06)')

fe.append_section(S, '04', "## Booking-specific debugging", """Three failure shapes are specific to this domain. **A slot that should be free is 409**: read `ensureNoConflict` and check the interval math (half-open, strict comparisons) and the status filter; then query the overlapping `confirmed` rows for that provider in `psql`. **A slot that should be taken is 201**: confirm the blocking row is `confirmed` (cancelled, completed and no-show rows do not hold slots by design) and that both requests took the provider lock. **Times look shifted by hours**: `start_time` is a `timestamptz` instant; the client sends ISO with `Z`, the provider has a `timezone` column for display, and `cancellation_hours` is compared against `new Date()` on the server, so a machine with a wrong clock produces wrong cancellation errors.

`test/database.ts` creates a private schema, migrates it, imports the app and returns `h.db` and `request(origin, path, method, body, headers)`; the `api()` helper adds `x-user-id: 4`. The first test proves the race with `Promise.all`; the third uses a `BEFORE INSERT` trigger on `notifications` to force a late failure. Run with `$env:ASTRA_TEST_DATABASE_URL = "postgres://user@127.0.0.1:5432/astra_test_yourname"` then `npm test`.""", before='## ')
done.append('review#4 booking-specific debugging section (04)')

rp = json.load(open('package.json', encoding='utf-8'))
rp['name'] = 'appointment-booking-workspace'
rp.setdefault('devDependencies', {}).update({"pg": "^8.23.0", "tsx": "^4.23.13"})
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(rp, indent=2) + '\n')
done.append('review#5 root package renamed from astra-crud-workspace-65; pg and tsx declared at the root; README carries the Toolchain block')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **3**.", "Automated test cases: **3** delivered by Astra, plus **1** added in the fix pass (cancelled rows do not hold a slot), for 4 in `test/booking.test.ts`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
