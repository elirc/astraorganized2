# master4 — Atlas Fulfillment (inventory reservation) — Fable review

- **Path:** `_Organized Desktop/03 Master Projects/master4`  ·  **Wave:** 2  ·  **Stack:** TypeScript / Express 5 / Prisma+SQLite / React 19 / Vitest / Vite  ·  **Batch:** B14
- **Astra's change (one line):** `planReservation` now groups order lines by `skuId` into a `Map` before comparing demand against available-to-promise (fixing an oversell where two lines of the same SKU each fit but their sum did not), rejects non-positive/fractional/non-finite quantities as normal decision failures, and `applyReservation` now throws on invalid or over-available quantities.
- **Course size:** 3,801 words across 9 files  ·  **Tests claimed:** 12 (9 domain + 3 API)  ·  **Tests found on disk:** 12 — `tests/inventoryRules.test.ts` (9), `tests/api.test.ts` (3)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 5 | 4 | 5 | 5 | 5 | 5 | 4.8 |

## Verdict

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- Picked a real, subtle invariant bug rather than a cosmetic one. The pre-change `lines.flatMap` (preserved verbatim at `astraupskill/snapshots/inventoryRules-before.ts.txt`, and matching the backup byte-for-byte) compared each line against the same `available` number independently, so `[14, 9]` against 22 available passed. The new `requestedBySku` map at `src/shared/inventoryRules.ts:33-40` is the minimal correct fix.
- The regression test describes the production failure, not the implementation: `tests/inventoryRules.test.ts:38-55` asserts `requested: 23, available: 22`, which cannot pass against the snapshot version. `04-TESTING-AND-DEBUGGING.md` explicitly says why that beats "asserting an internal `Map` or loop".
- `05-PRACTICE.md` Exercise 1 is a true predict-run-change-verify loop: "Before changing source, run the test and observe it fail against the original `flatMap` implementation." Solutions live in a separate file (`06-SOLUTIONS-AND-REVIEW.md`), which opens by saying they are worked answers, not the delivered suite.
- `VERIFICATION.md` is the most honest one I read in this batch. It volunteers that the focused 9-test run is a subset ("not an additional nine unique tests"), that "The API tests read seeded data; they do not exercise the reservation write endpoint", that a rejected decision *still writes an audit row* so "Rejection therefore does not imply that every table remains unchanged", and that earlier runs failed before the DB was seeded correctly. It also warns that `db:push`/`db:seed` destroy `prisma/dev.db` and tells the learner to work in a disposable copy.

## Problems found (evidence required)
- **[D2]** Nothing exercises `POST /api/orders/:orderId/reserve`. The only DB-backed tests are `tests/api.test.ts:8,15,23` — health, dashboard metrics, CSV export. So the one code path the whole course is about is proven only through a pure function with hand-built objects. Astra discloses this, which is why D6 stays at 5, but it still caps D2.
- **[D2]** The new `applyReservation` guards are unreachable from the server. `grep -rn "applyReservation" src` returns only its own definition in `src/shared/inventoryRules.ts:83`; `orders.service.ts:82-84` increments with raw Prisma (`reserved: { increment: line.quantity } }`) and never calls the helper. `02-CONCEPTS.md` justifies the guard as protecting "callers that skip planning" — there are currently none, so half the delivered change is defensive dead code.
- **[D2]** An adjacent bug the fix makes more visible goes unmentioned: on the success path, `orders.service.ts:86-95` creates one `StockReservation` per *line* with `id: \`res-${order.id}-${line.skuId}-${Date.now()}\``. Two lines for the same SKU in the same millisecond produce an identical primary key and abort the transaction. `07-TRACE-LAB.md` walks the duplicate-line success case ("one line of 18 … reserved at 38") without ever reaching a duplicate-line *success*, so the collision never surfaces.
- **[D4]** The change is narrow: one pure function plus its tests. There is no ownership, pagination, idempotency, or HTTP error-mapping content, so as CRUD upskilling this is a domain-invariant lesson rather than a full CRUD lesson.

## Spot-checks performed
- Course claim (`01-CODEBASE-MAP.md`): "`InventoryItem` has one row per `(warehouseId, skuId)` because of its compound unique constraint" -> `prisma/schema.prisma:111` `@@unique([warehouseId, skuId])` -> matches, and this is the actual evidence for the bug.
- Course claim (`07-TRACE-LAB.md`): "A warehouse manager or admin sends `POST /api/orders/:orderId/reserve` … `requireRole` checks the role" -> `src/server/app.ts:52` `app.post('/api/orders/:orderId/reserve', requireRole(['warehouse_manager','admin']), …)` -> matches exactly, including the role list.
- Course claim (`VERIFICATION.md`): "passed **12 tests in two files**" -> `astraupskill/evidence/full-test-absolute.log:9-10` "Test Files 2 passed (2) / Tests 12 passed (12)"; delivery JSON `expectedTests: 12`, `domainTests: 9`, `apiReadTests: 3` -> matches, no inflation.
- Course claim (`03-WORKED-CHANGE.md`): the exact failure reason string `Reservation quantity must be a positive whole number.` -> `src/shared/inventoryRules.ts:37` and `:85` -> matches character-for-character.
- Course claim (`02-CONCEPTS.md`): "`availableToPromise` is `Math.max(0, onHand - reserved)`" -> read the helper in `src/shared/inventoryRules.ts` -> matches.

## Improvements needed (ordered, concrete, actionable)
1. Add `tests/reservation-api.test.ts` using the existing supertest + seeded-SQLite setup from `tests/api.test.ts`: seed an order with two lines for one SKU, POST the reserve endpoint, assert HTTP 200 with `ok: false` / `requested: 23`, and assert `inventoryItem.reserved` and `stockReservation.count()` are unchanged while exactly one `order.reservation_failed` audit row exists. This closes the single biggest gap the course itself names. (effort: M)
2. Make `orders.service.ts` actually use `applyReservation`, or aggregate `order.lines` by `skuId` in the write loop too. Today the guard is dead code and the loop double-creates reservation rows. (effort: M)
3. Replace the `Date.now()`-based ids in `orders.service.ts:87,104,114,123` with `crypto.randomUUID()` (or a `@default(uuid())` in the schema), and add a short "why time-based ids collide" note to `07-TRACE-LAB.md`. (effort: S)
4. Add one exercise to `05-PRACTICE.md` covering a valid quantity against a *missing* balance row — `04-TESTING-AND-DEBUGGING.md` already flags that this regression is absent from the delivered suite. (effort: S)

## One-paragraph summary for the index
A short, very well-made lesson on one class of CRUD bug: an inventory planner that validated each order line against the same stock pool independently, so two lines of 14 and 9 could both "fit" in 22 available units. The course makes you reproduce the oversell as a failing test before you touch the source, keeps solutions in a separate file, and traces the fix out through the Express route and the Prisma transaction that surrounds it. Its verification chapter is unusually candid — it tells you outright that the three DB-backed tests never hit the reservation endpoint and that a rejected reservation still writes an audit row. Worth doing in about two hours; the natural follow-on is writing the API-level test it admits is missing.
