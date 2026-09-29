import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-13-ecommerce-storefront'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

fe.append_section(S, '02', '## Why the products are locked in id order', """`checkout` in `server/src/services/storeService.ts` locks the cart row, then every product in the cart with `whereIn(...).orderBy("id").forUpdate()`. The `orderBy("id")` is not cosmetic. Two carts holding the same two products in opposite order would otherwise lock them in opposite order:

| step | transaction A (cart: 7, then 3) | transaction B (cart: 3, then 7) |
|---|---|---|
| 1 | `SELECT ... WHERE id = 7 FOR UPDATE` (holds 7) | |
| 2 | | `SELECT ... WHERE id = 3 FOR UPDATE` (holds 3) |
| 3 | `... WHERE id = 3 FOR UPDATE` -> waits for B | |
| 4 | | `... WHERE id = 7 FOR UPDATE` -> waits for A |
| 5 | PostgreSQL detects the cycle after `deadlock_timeout` and aborts one side with `40P01 deadlock_detected` | |

With `ORDER BY id`, both transactions ask for 3 first and 7 second, so the second one simply waits at step 2 and proceeds after the first commits. Note that a single `SELECT ... WHERE id IN (...) ORDER BY id FOR UPDATE` acquires the row locks in the order the rows are returned, which is what makes the one-statement form safe. Exercise 3 asks you to observe the difference; predict the two outcomes before you run it.""")
done.append('review#2 02-CONCEPTS lock-order box with the A/B deadlock sketch')

fe.append_section(S, '03', '## Why removal and merge do not take the product lock', """`changeCartQuantity` and `checkout` lock `products` because they *read* `stock_quantity` and then decide; the lock is what keeps that read true until the write. `removeCartItem` (`storeService.ts`) deletes a `cart_items` row and never reads stock, so there is nothing a concurrent checkout could invalidate: whichever order the delete and the checkout commit in, stock is right and the cart reflects the last writer. `mergeCart` runs in a transaction but also skips the product lock; it copies quantities from a guest cart, and the next `checkout` re-validates every line against locked stock anyway. If a future change made `mergeCart` clamp to stock, it would need the same `forUpdate()` as `changeCartQuantity`. The rule: lock what you read to decide, not what you merely write.""", before='## How to reason through the code')
done.append('review#3 03 explains why removeCartItem and mergeCart do not take the product lock')

B = [
("the store UI decides what to send",
 "`client/src/features/store/*` and `client/src/App.tsx`: add-to-cart posts `{ productId, quantity }`, the cart page edits quantities, and the checkout form submits `{ addressId, shippingMethod, paymentMethod }`. The client shows server totals; it never computes stock or price itself. Every mutation invalidates the cart query afterwards so what you see is a re-read."),
("the request leaves the browser",
 "`client/src/services/api.ts`: `checkout(payload)` (line 46) posts to `/checkout`; cart calls go to `/cart/items`. The axios instance sends the demo identity header; `unwrap()` reads the `{ success, data }` envelope and throws the server's message otherwise, which is how `Not enough stock` and `X is out of stock` reach the page."),
("the route validates the shape",
 "`server/src/routes/storeRoutes.ts` mounts `validateBody(...)` from `storeValidators.ts` in front of each write (positive whole quantities, required checkout fields). `changeCartQuantity` (`storeService.ts:42`) re-checks `Number.isSafeInteger(quantity) && quantity >= 1` because it is also called from the merge path, not only from HTTP."),
("the service locks, reads and decides inside one transaction",
 "`checkout` (`storeService.ts:134`): `db.transaction` -> address ownership check -> cart row `forUpdate()` -> product rows `whereIn(ids).orderBy(\"id\").forUpdate()` -> re-read cart items -> reject empty carts and any line whose `stock_quantity < quantity` or inactive product -> compute totals server-side. `changeCartQuantity` follows the same shape for a single product: lock cart, lock product, compare `next` (existing + added) with stock. The old code compared only the increment, which is the bug the first test pins."),
("the model writes four things or nothing",
 "Still inside the transaction: insert `orders`, insert `order_items`, `decrement(\"stock_quantity\")` per product, delete `cart_items`. Knex commits when the callback returns and rolls back on throw. The third test installs a trigger that rejects the `order_items` insert: the route answers 500, stock is still 5 and the cart still has its line, which is the rollback made visible."),
("the envelope tells the client what happened",
 "`utils/http.ts` `sendSuccess` returns 201 with the order; `ValidationError` becomes 400 (`Not enough stock`, `Cart is empty`), `NotFoundError` 404, anything else 500. The two-buyers test reads `[201, 400]` from two racing checkouts and then verifies `stock_quantity = 0` and exactly one `order_items` row directly in the database."),
]
fe.set_boundaries(S, B); done.append('review#1 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the failed checkout must answer 400 with a structured `details: [{ productId, requested, available }]` array (extend `ValidationError` or add a field) built from the same loop that throws `is out of stock`; the cart must be untouched (assert the `cart_items` row still exists, like the third test); the UI must highlight that line and keep the others editable.",
"the breakdown must display `subtotal`, `shipping_cost`, `tax_amount` and `total` exactly as returned by the server's `totals()`; a client estimate may be shown before checkout but must be replaced by the server values on success; assert in a server test that the persisted `orders.total` equals the response and that a client-supplied total is ignored.",
"create two carts holding the same two products in opposite insertion order and run `checkout(1)` and `checkout(2)` in a `Promise.all`; with the shipped `orderBy(\"id\")` you must observe `[201, 400]` or `[201, 201]` (depending on stock) and never a 500; then on a throwaway branch remove `orderBy(\"id\")` and lock in cart order, repeat until you observe a `40P01` in the server log, and write down the interleaving.",
"the design must separate `payment_status` from `status`, store an idempotency key per checkout attempt (unique index) so a retried `POST /checkout` returns the same order instead of a second one, and explain why the external payment call cannot sit inside the SQL transaction (a committed charge with a rolled-back order, or the reverse).",
]
fe.set_reviews(S, R); done.append('review#4 / 2.3 per-exercise review criteria (06)')

svc = open('server/src/services/storeService.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
i = next(i for i, l in enumerate(svc) if 'export async function checkout' in l)
k = next(k for k, l in enumerate(svc) if 'async function changeCartQuantity' in l)
excerpt = '// storeService.ts:' + str(k + 1) + '\n' + '\n'.join(svc[k:k + 25]) + '\n\n// storeService.ts:' + str(i + 1) + '\n' + '\n'.join(svc[i:i + 30])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/64/server/src/services/storeService.ts` with `diff --strip-trailing-cr -w`): `changeCartQuantity` compares the cumulative quantity against locked stock, and `checkout` locks the cart and then every product in id order before it reads, decides and writes. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows the changed cart and checkout transactions')

fe.set_variations(S, """**Normal variation — cumulative additions.** With a product at stock 3, add 2, then add 1, then try to add 1 more. Predict: 200, 200, 400 `Not enough stock`, and the `cart_items` row at quantity 3. Before the change the third call would have passed (it compared the increment, 1, against stock, 3).

**Invalid variation — an empty or stale cart.** Check out with no cart lines: predict 400 `Cart is empty` and no `orders` row. Then add a line, set the product `is_active = false` in `psql`, and check out: predict 400 `<name> is out of stock` and the cart line still present.

**Boundary variation — the last unit.** Reproduce the second test: two users each hold the last unit in their carts and check out concurrently. Predict `[201, 400]`, `stock_quantity = 0`, one `order_items` row. Then remove the products `forUpdate()` on a throwaway branch and repeat until you see `[201, 201]` and stock `-1`; restore it."""); done.append('2.4 three concrete variations')

fe.add_exercise(S, 'ownership of orders and addresses',
"""`checkout` already scopes the address to the buyer (`addresses.user_id = userId`). Extend the same discipline to reading orders.

1. Read `storeRoutes.ts` and list every route that returns an order or an address. For each, write down whether the query carries `user_id`.
2. Add `GET /orders/:id` (if missing) and make `GET /orders` and `GET /orders/:id` scope by the demo user; a foreign order id answers 404 (not 403: an order number should not confirm existence).
3. Add a test: user 1 checks out; user 2 requests that order by id -> 404; user 1 -> 200 with `order_items`; user 2's list does not contain it.

Acceptance is the test plus one sentence in `02-CONCEPTS.md` on why the scope lives in the `WHERE`, not in a post-query filter.""",
"""Reference (scope in the query, not after it):

```typescript
export function findOrderForUser(orderId: number, userId: number) {
  return db("orders").where({ id: orderId, user_id: userId }).first();
}
// service
const order = await store.findOrderForUser(id, userId);
if (!order) throw new NotFoundError("Order not found");
```

Reference test skeleton: after `checkout(1)` returns `201` with `data.id`, `api("/orders/" + id, "GET", undefined, 2)` -> 404; `api("/orders/" + id, "GET", undefined, 1)` -> 200; `api("/orders", "GET", undefined, 2)` -> body does not include `id`.

Review: explain why a post-query filter (`orders.filter(o => o.user_id === userId)`) is worse even when it returns the same rows (it reads everything, and a later pagination change would leak counts)."""); done.append('2.5 ownership/authz exercise 7 (05, 06)')

fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("| Chromium interaction | Passed |", "| Chromium interaction | Passed (smoke only: the recorded run issued 2 API requests and did not drive add-to-cart -> checkout; the concurrency lesson is proven by the HTTP tests, not by the browser check) |", 1))
done.append('review#5 VERIFICATION states honestly what the browser check covered')

rp = json.load(open('package.json', encoding='utf-8'))
rp['name'] = 'ecommerce-storefront-workspace'
rp.setdefault('devDependencies', {}).update({"pg": "^8.23.0", "tsx": "^4.23.13"})
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(rp, indent=2) + '\n')
done.append('root package renamed from astra-crud-workspace-64; pg and tsx declared at the root')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
