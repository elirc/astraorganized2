# newcodexJS/14-appointment-booking — Fable review

- **Path:** `newcodexJS/14-appointment-booking`  ·  **Wave:** 1  ·  **Stack:** Node/Express + Knex/Postgres + React/Vite, TypeScript  ·  **Batch:** B07
- **Astra's change (one line):** `createAppointment` and `updateAppointment` in `server/src/models/appointmentModel.ts` now run inside `db.transaction`, take `SELECT … FOR UPDATE` on the `provider_profiles` row before testing overlaps via a new `ensureNoConflict()` (half-open interval `start < end && end > start`, 409 `ConflictError`), and the booking-confirmed `notifications` row is inserted inside the same transaction as the appointment.
- **Course size:** 7,609 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/booking.test.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 3 | 5 | 4 | 5 | 4 | 4 | 4.5 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The double-booking hole was real and is closed at the right granularity. The backup `appointmentModel.ts` `createAppointment` was two lines — `const [appointment] = await db("appointments").insert(values).returning("*"); return appointment;` — with the overlap check (if any) done by an earlier, unlocked read. The new version locks `provider_profiles` for the booked provider first, so all writers for one provider serialize while different providers stay concurrent.
- `ensureNoConflict` uses the correct half-open overlap predicate: `.where("start_time", "<", end).where("end_time", ">", start)`, which is why the second test's 10:30 booking is allowed to sit immediately after a 10:00–10:30 slot instead of being rejected as a touch.
- The atomicity claim is proven by failure injection, not by inspection. Test 3 installs `CREATE TRIGGER reject_notification BEFORE INSERT ON notifications … RAISE EXCEPTION`, asserts the booking POST returns 500, then asserts the appointment count is unchanged — so the notification row and the appointment genuinely share one transaction.
- The reschedule test asserts the *negative* invariant, which is the part juniors usually skip: after a 409 on a conflicting reschedule it re-reads the row and asserts `start_time` is still `2099-01-01T10:30:00.000Z`.
- The limits are correctly scoped: "The booking notification is a database row, not an email sent by this task… the tested guarantee is overlap protection and atomic booking confirmation, not full scheduling policy enforcement" (`astrdocs/NEXT_25_IMPLEMENTATION_REPORT.md`, echoed in the course).
- All 45 substantive code lines in `03-WORKED-CHANGE.md` matched verbatim against the project's `.ts` sources (45/45).

## Problems found (evidence required)
- **[D2]** `ensureNoConflict` only searches `.where({ provider_id, status: "confirmed" })`. `createAppointment` calls it before inserting whatever `values.status` the service supplies, so an appointment created in any non-`confirmed` status is neither blocked by nor blocking of an overlapping booking. `server/src/services/appointmentService.ts:125` does set `status: "confirmed"` on the create path, so the delivered tests pass — but the invariant is one service-layer edit away from silently breaking, and nothing in `02-CONCEPTS.md` or `03-WORKED-CHANGE.md` names this coupling.
- **[D3]** `07-TRACE-LAB.md` "Trace the real call path" lists six differently-labelled boundaries followed by six byte-identical paragraphs, all saying "starting with [server/src/models/appointmentModel.ts](../server/src/models/appointmentModel.ts) and `createAppointment`". Boundaries 1, 2, 3 and 6 are therefore pointed at the wrong layer.
- **[D3/D8]** All exercise solutions in `06-SOLUTIONS-AND-REVIEW.md` share the identical "**Review:** Demonstrate an ordinary case and a case that would break a naive implementation…" paragraph.
- **[D8]** `04-TESTING-AND-DEBUGGING.md` is 94.4% character-identical to `newcodexJS/13-ecommerce-storefront`'s and `05-PRACTICE.md` 85.6%. The invariants/validation-vs-normalization/identity sections of `02-CONCEPTS.md` are shared batch-wide with only the quoted scope sentence swapped.
- **[D5]** Root `package.json` declares only `{"concurrently": "^9.1.2"}` while `test/database.ts` imports `pg`; the repeated claim that "The root workspace also makes pg and tsx available to the root test directory" is true only through npm workspace hoisting. The `README.md` setup block also pins no Node or Postgres version — those appear only in `VERIFICATION.md`.

## Spot-checks performed
- Claim: "Appointment creation and confirmed timing/status updates lock the provider before checking overlaps" -> read `appointmentModel.ts` `createAppointment` (`trx("provider_profiles").where({id: values.provider_id}).forUpdate().first()` then `ensureNoConflict`) and `updateAppointment` (`forUpdate()` on the provider, then `if (next.status === "confirmed") await ensureNoConflict(trx, next, id)`) -> matches.
- Claim: "Booking and its notification commit together" -> read the `trx("notifications").insert({ user_id: appointment.customer_id, appointment_id: appointment.id, type: "booking_confirmed", … })` inside the same `db.transaction` -> matches; test 3 asserts the rollback.
- Claim: "Conflicting reschedules leave the original appointment untouched" -> read test 2: PUT `/appointments/:id/reschedule` to 10:15 returns 409 and the re-read `start_time` is unchanged -> matches.
- Claim: "Automated test cases: 3" -> `batch04/logs/65-tests.log` shows `# tests 3 / # pass 3 / # fail 0`; `grep -c '^test('` returns 3 -> matches.
- Claim (VERIFICATION table): "Chromium interaction | Passed" -> `batch04/browser-checks.json` `{"project":"65","passed":true,"api":"actual isolated HTTP server","api_requests":3}` -> matches, but 3 requests is a shallow smoke.

## Improvements needed (ordered, concrete, actionable)
1. Make the `status: "confirmed"` coupling explicit. Either have `ensureNoConflict` take the statuses that hold a slot as a parameter, or add a paragraph to `03-WORKED-CHANGE.md` stating that only `confirmed` rows reserve time and that `appointmentService.ts:125` is what guarantees new bookings are confirmed. Add a test that a `pending` appointment does not block an overlapping confirmed one (or that it does, once the policy is decided). (effort: M)
2. Rewrite `07-TRACE-LAB.md` "Boundary 1..6" to name distinct code: 1 the booking form in `client/src/`, 2 the client fetch layer, 3 `validate.ts` + `appointmentValidators.ts`, 4 `appointmentService.createAppointment`, 5 `appointmentModel.createAppointment`'s transaction and `FOR UPDATE`, 6 `errorMiddleware.ts` mapping `ConflictError` to 409. (effort: S)
3. Add a half-open-interval box to `02-CONCEPTS.md`: show why `start < otherEnd && end > otherStart` is correct and why `<=`/`>=` would reject back-to-back appointments — the second test depends on this and it is never explained. (effort: S)
4. Replace the identical "**Review:**" paragraphs in `06-SOLUTIONS-AND-REVIEW.md` with per-exercise acceptance criteria, and give `04-TESTING-AND-DEBUGGING.md` booking-specific debugging (timezone vs instant, `cancellation_hours`, provider `timezone` column). (effort: M)
5. Pin Node/Postgres versions in `README.md` and add `pg` + `tsx` to the root `package.json` devDependencies. (effort: S)

## One-paragraph summary for the index
A provider-scheduling API where two customers could book the same slot. The lesson is pessimistic locking with the right granularity: lock the *provider* row, not the appointments table, then test the overlap with a half-open interval, return 409, and commit the appointment and its confirmation notification in the same transaction. All three tests are real HTTP tests against a disposable Postgres schema — one races two bookings for one slot, one proves a rejected reschedule leaves the original time intact, and one installs a Postgres trigger that makes the notification insert fail to prove the booking rolls back with it. This is the clearest transaction-boundary lesson in the batch and pairs well with the ecommerce checkout course. Skim the trace lab, whose six "boundaries" are the same paragraph repeated.
