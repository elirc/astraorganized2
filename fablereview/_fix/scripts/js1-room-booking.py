import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'js1-room-booking'
P = fe.REG[S]['abs']
os.chdir(P)
done = ['review#1 00-PREREQS.md, review#3 wrap() on POST, review#4 pins + lockfile, review#5 sequence-diagram timeline and review#2 datetime-local note were completed by the earlier fix agent (verified on disk)']

B = [
("the form decides what instants to send",
 "`client/src/App.tsx`: `handleSubmit` (line 68) converts the two `datetime-local` strings to ISO instants, but if the input string is byte-identical to what the editor was opened with (`kept.startsAtInput`, line 79-80) it re-sends the *original* instant instead of re-parsing, so a browser that normalizes sub-second values cannot shift a booking by re-saving it unchanged. The room comes from the selected room id."),
("the request leaves the browser",
 "`client/src/api.ts`: `createBooking(input)` posts `{ roomId, title, bookedBy, startsAt, endsAt }` to `/api/bookings`; `updateBooking(id, input)` puts to `/api/bookings/:id`. A 409 arrives as `That room is already booked for an overlapping time.` and the form keeps its values."),
("`parseBooking` validates shape and order, not availability",
 "`server/src/validation.ts:16` `parseBooking`: object check, `uuid` for the room, bounded text for title and bookedBy, `timestamp` (line 12) requiring a real ISO timestamp *with an explicit offset* so `2026-03-29T02:30` cannot be misread on a DST day, and `endsAt > startsAt`. It deliberately does not look for conflicts: there is no `SELECT` to race on."),
("one statement inserts and returns the booking",
 "`server/src/index.ts:73` `POST /api/bookings` is a single `WITH inserted AS (INSERT ... RETURNING *) SELECT ... JOIN rooms`. The `wrap` helper forwards any rejection to the error middleware. `PUT` (line 88) is the same shape with an `UPDATE ... WHERE id = $1`."),
("PostgreSQL decides who wins",
 "`server/db/schema.sql:30` `CONSTRAINT no_overlap EXCLUDE USING gist (room_id WITH =, tstzrange(starts_at, ends_at) WITH &&)`; `btree_gist` makes the equality operand indexable. Two concurrent inserts for the same room and overlapping range serialize on the index: one commits, the other fails with SQLSTATE `23P01`. Adjacent slots (`[10:00, 11:00)` then `[11:00, 12:00)`) do not overlap because the range is half-open."),
("the error middleware translates the outcome",
 "`server/src/index.ts` error handler: `ValidationError` -> 400; `code === EXCLUSION_VIOLATION` (`23P01`) -> 409; `23503` (unknown room) -> 400; anything else 500. The test fires two overlapping `POST`s with `Promise.all`, asserts `[201, 409]` in some order, then reads the table directly."),
]
fe.set_boundaries(S, B); done.append('2.2 trace-lab call path section (07)')
R = [
"the version must be selected with the booking and checked in the `UPDATE ... WHERE id = $1 AND version = $2 RETURNING *`; zero rows means 409 with a distinct message from the overlap 409; the test issues two sequential `PUT`s with the same stale version and asserts 200 then 409 with the row equal to the first result; explain why the exclusion constraint cannot detect this case.",
"the display must format the stored UTC instants in the viewer's zone and show the date on both ends when the local calendar days differ; assert with a fixed `Intl.DateTimeFormat` zone in a client test that `2026-03-28T23:30Z`-`2026-03-29T00:30Z` renders two dates in Europe/Berlin and one in UTC.",
"construct local midnight and the next local midnight in a fixed DST-transition zone (Europe/Berlin, 2026-03-29 and 2026-10-25), assert the UTC instants sent differ by 23 and 25 hours, and assert the day filter (`dayStart`/`dayEnd`) still returns the bookings inside that window; the 26-hour limit in `GET /api/bookings` exists for exactly this reason.",
"the owner must be a verified caller identity stored in a new `owner_id` column (not the free-text `booked_by`), checked in the `PUT`/`DELETE` statement itself (`WHERE id = $1 AND owner_id = $2`) so a cross-owner edit updates zero rows and answers 404; the test proves a foreign edit is rejected and the row unchanged.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')
fe.set_variations(S, """**Normal variation — adjacent slots.** Book Birch `10:00-11:00Z`, then `11:00-12:00Z`. Predict 201 and 201: `[)` ranges that touch do not overlap. Then `10:30-11:30Z`: predict 409 from the exclusion constraint, and `SELECT count(*) FROM bookings` unchanged.

**Invalid variation — an offset-less timestamp.** Post `startsAt: "2026-03-29T02:30:00"`. Predict 400 `Times must be real ISO timestamps with an explicit timezone offset.` from `timestamp()` and no query. Then post `2026-02-30T10:00:00Z`: predict which check fires (`realDate`).

**Boundary variation — the race.** Reproduce the first test: two identical bookings in a `Promise.all`. Predict `[201, 409]` and one row. Then on a throwaway branch drop the `no_overlap` constraint in your dev database and repeat: predict `[201, 201]` and two overlapping rows; restore it with the statement from `schema.sql:30`."""); done.append('2.4 three concrete variations')
fe.append_section(S, '06', '### Exercise 4 — worked solution: a booking that belongs to someone', """```sql
ALTER TABLE bookings ADD COLUMN owner_id text NOT NULL DEFAULT 'anonymous';
```

```typescript
// server/src/index.ts: read the caller once
app.use((req, _res, next) => { (req as any).actor = String(req.get("X-Actor") ?? "").trim(); next(); });
const requireActor = (req: express.Request) => { const a = (req as any).actor; if (!a) throw new AuthError("Sign in to change bookings."); return a; };
// POST: owner comes from the caller, never from the body
[input.roomId, input.title, input.startsAt, input.endsAt, input.bookedBy, requireActor(req)]
// PUT / DELETE: the owner check is part of the statement
`UPDATE bookings SET ... WHERE id = $1 AND owner_id = $7 RETURNING *`
`DELETE FROM bookings WHERE id = $1 AND owner_id = $2`
// error middleware: AuthError -> 401
```

Test: create as `ana` with `X-Actor: ana`; `PUT` as `ben` -> 404 and the row unchanged (read it with `admin.query`); `DELETE` as `ben` -> 404 and `count(*)` unchanged; `PUT` as `ana` -> 200; `PUT` with no header -> 401.

Review criterion: because the owner predicate is inside the `UPDATE`, there is no window between an ownership read and the write; `booked_by` stays display text and must not be used for authorization.""", before='## Review questions')
done.append('2.5 exercise 4 (ownership) now has a worked solution with the owner predicate inside the statement (06)')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
