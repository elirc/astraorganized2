# newcodexJS/13-ecommerce-storefront — Fable review

- **Path:** `newcodexJS/13-ecommerce-storefront`  ·  **Wave:** 1  ·  **Stack:** Node/Express + Knex/Postgres + zod + React/Vite, TypeScript  ·  **Batch:** B07
- **Astra's change (one line):** Cart add and cart edit were merged into one `changeCartQuantity()` that runs in a transaction, locks the cart row and the product row, computes the *cumulative* quantity and rejects it against `stock_quantity`; `checkout()` now locks the cart, then locks every cart product `ORDER BY id … FOR UPDATE` before re-reading stock and `is_active`, so order + order_items + stock decrement + cart clear commit or roll back together.
- **Course size:** 7,975 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/checkout.test.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 3 | 5 | 4 | 5 | 4 | 4 | 4.5 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The oversell bug was real and the fix is at the right layer. The backup `storeService.ts` `addToCart` read the product with a plain `db("products").where(...).first()`, compared `product.stock_quantity < quantity` and then called `upsertCartItem` which did `merge({ quantity: db.raw("cart_items.quantity + excluded.quantity") })` — so the stock check compared the *incremental* quantity while the database added it to the existing one. The new `changeCartQuantity` computes `const next = quantity + (add ? (existing?.quantity ?? 0) : 0)` under `forUpdate()` and checks `next > product.stock_quantity`. The first test proves it: add 2 to stock 3 → 201, add 2 again → 400, PUT quantity 4 → 400, stored quantity still 2.
- Deterministic lock ordering is implemented, not just described: `checkout` does `trx("products").whereIn("id", cartRows.map(r => r.product_id)).orderBy("id").forUpdate()` before reading items. That is the standard deadlock-avoidance technique and `05-PRACTICE.md` Exercise 3 makes the learner test it ("Test two carts whose product order is reversed").
- The rollback test is the best test in the batch. `test/checkout.test.ts` installs a Postgres `BEFORE INSERT` trigger on `order_items` that raises, asserts the checkout returns 500, then asserts `stock_quantity` is still 5 **and** the cart item still exists — i.e. it observes the invariant, not the status code. It then drops the trigger and races two checkouts for `[201, 400]`.
- `06-SOLUTIONS-AND-REVIEW.md` Exercise 4 correctly refuses the tempting wrong answer: "A SQL transaction cannot atomically commit an external payment API" — with idempotency keys and reconciliation named as the real design.
- All 74 substantive code lines in `03-WORKED-CHANGE.md` matched verbatim against the project's `.ts` sources (74/74).

## Problems found (evidence required)
- **[D3]** `07-TRACE-LAB.md` "Trace the real call path" lists six differently-labelled boundaries and then repeats the same paragraph six times, each saying "starting with [server/src/services/storeService.ts](../server/src/services/storeService.ts) and `checkout`". The boundary labelled "A React form, button or test sends a concrete operation" sends the learner to the server checkout function.
- **[D3/D8]** In `06-SOLUTIONS-AND-REVIEW.md` all four exercise solutions carry the identical "**Review:** Demonstrate an ordinary case and a case that would break a naive implementation. Explain which existing invariant remains unchanged. Keep the code and the learner-facing explanation in agreement." paragraph.
- **[D2]** `removeCartItem` and `mergeCarts` were left outside the locking discipline the rest of the change establishes — `removeCartItem` still calls `store.getOrCreateCart` then `store.deleteCartItem` with no transaction (`server/src/services/storeService.ts`). The course never says why remove is safe to leave unlocked, which leaves an inconsistent-looking file for the learner to imitate.
- **[D8]** `04-TESTING-AND-DEBUGGING.md` is 94.4% character-identical to `newcodexJS/14-appointment-booking`'s and `05-PRACTICE.md` 85.6%; the generic sections ("The expectation should not be copied from the function being tested…", "An invariant is a rule that must remain true before and after an operation…") are shared verbatim across the whole batch.
- **[D2, cosmetic noise]** Of the 35 files the manifest lists as changed, the majority carry only Prettier reformatting — e.g. the entire `listProducts`/`getProductBySlug` diff in `server/src/models/storeModel.ts` is line-wrapping with no behavior change. The headline change count overstates the reviewable surface.
- **[D5]** Root `package.json` declares only `concurrently`; `test/database.ts` imports `pg` and the course claims three times that "The root workspace also makes pg and tsx available to the root test directory", which holds only via npm hoisting from `server/`.

## Spot-checks performed
- Claim (`03-WORKED-CHANGE.md`): "Checkout locks the cart and products in ID order, rechecks active stock" -> read `storeService.ts` `checkout`: `trx("carts").where({id}).forUpdate().first()`, then `trx("products").whereIn(...).orderBy("id").forUpdate()`, then `if (!item.product.is_active || item.product.stock_quantity < item.quantity) throw new ValidationError(...)` -> matches, including the newly added `is_active` check.
- Claim: "With stock 3, adding 2 succeeds but adding another 2 or editing to 4 fails and leaves quantity 2" -> read test 1; exactly these three calls and the stored-quantity assertion -> matches.
- Claim: "The failure-injection test rejects an order-item insert and observes stock and cart, not just the HTTP 500" (report limits) -> read test 3's `CREATE TRIGGER reject_order_item BEFORE INSERT ON order_items` and the two post-failure DB assertions -> matches.
- Claim: "Automated test cases: 3" -> `batch04/logs/64-tests.log` shows `# tests 3 / # pass 3 / # fail 0`; `grep -c '^test('` returns 3 -> matches.
- Claim (VERIFICATION table): "Chromium interaction | Passed" -> `batch04/browser-checks.json` `{"project":"64","passed":true,"api":"actual isolated HTTP server","api_requests":2}` -> matches, though 2 API requests is a thin browser smoke.

## Improvements needed (ordered, concrete, actionable)
1. Rewrite `07-TRACE-LAB.md` "Boundary 1..6" to name distinct code: 1 the cart/checkout component in `client/src/App.tsx`, 2 the client fetch layer, 3 `validateBody` + `storeValidators.ts`, 4 `storeService.checkout`, 5 the `db.transaction` / `FOR UPDATE` block in `storeModel.ts`, 6 the `utils/http.ts` envelope. (effort: S)
2. Add a short "why this order of locks" box to `02-CONCEPTS.md` with a two-column A/B transaction sketch showing the deadlock that `orderBy("id")` prevents. Exercise 3 asks the learner to test it but nothing explains it first. (effort: S)
3. Either bring `removeCartItem`/`mergeCarts` under the same transaction+lock pattern in `server/src/services/storeService.ts`, or add a paragraph to `03-WORKED-CHANGE.md` stating explicitly why removal does not need the product lock. (effort: S)
4. Replace the four identical "**Review:**" paragraphs in `06-SOLUTIONS-AND-REVIEW.md` with per-exercise acceptance criteria. (effort: S)
5. Deepen the browser check or drop the claim: 2 API requests (`browser-checks.json`) does not exercise add-to-cart → checkout, which is the whole lesson. (effort: M)

## One-paragraph summary for the index
This is the batch's transactions-and-locking course, and it is worth doing properly. The original code checked stock against the *incremental* quantity while the database added it to what was already in the cart, so two clicks oversold; the fix computes the cumulative quantity under a cart-and-product row lock, and checkout locks every cart product in ID order before writing the order, its line items, the stock decrement and the cart clear in one transaction. The three tests are real HTTP tests against a throwaway Postgres schema, including a genuine two-buyer race and a failure-injection test that installs a Postgres trigger to make the `order_items` insert explode and then asserts stock and cart are untouched. Read `03-WORKED-CHANGE.md` and `test/checkout.test.ts`; the trace lab and practice chapters are largely shared boilerplate. Budget one to two sessions.
