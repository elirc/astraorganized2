from pathlib import Path
s=Path('astra-remaining-improvements/stage/e502bf8af566')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('astraupskill/06-SOLUTIONS-AND-REVIEW.md',r'''
# Solution sketches and review questions

Use these notes after attempting [the exercises](05-PRACTICE.md). They are design guidance, not drop-in implementations. A useful review checks observable behavior and failure handling rather than whether the code resembles one preferred pattern.

For filtering, a sound solution parses a bounded `search` value, applies it consistently to count or page queries if both exist, and gives the browser a cache key such as `['products', { search, offset }]`. Resetting offset prevents an old page number from producing a misleading empty result under a narrower search. Test the outgoing query and the final rendered list after two responses arrive out of order. Avoid deriving correctness from a debounce timer alone; cancellation or query identity must still protect the result.

For the movement ledger, begin with a transaction-level invariant: the stock delta and its explanation commit together. A reservation movement should have a negative quantity and a cancellation movement a positive quantity. Record a stable relationship to the order and product. Decide whether uniqueness can enforce one movement of each relevant type per order item. Then inject a late failure and assert both stock and movement counts remain unchanged. A ledger that writes after commit can fail independently and leave an unexplained balance.

For idempotency, separate the key from the payload fingerprint. Canonicalize cart ordering before comparison because two arrays may describe the same order. Persist a winning result under a unique scoped key. Handle the concurrent loser by reading the winner after its transaction conflict, then compare fingerprints. Return the same resource identity for an equivalent retry and conflict for changed input. Do not catch every database exception and label it a duplicate: connection failure and uniqueness contention require different recovery. Verify the actual transaction behavior with two clients, not just a mocked lookup returning an existing key.

For authorization, write an access matrix before adding middleware. Every product and order operation needs an owner scope. A customer reference typed into the UI is not proof of identity. The service should receive an authenticated principal or owner identifier from trusted middleware, while request bodies remain untrusted business input. Test resource IDs copied from another account, including IDs nested inside cart items. Decide whether unauthorized resources appear as 403 or 404 and apply that policy consistently.

For purchasing, a receipt is a business command with durable consequences, not a generic status edit. A correct design links receipt quantities to purchase lines, validates remaining quantities and increments inventory in the same transaction. Replaying a receipt must not add stock twice. Partial receipt introduces a new invariant: cumulative accepted quantity cannot exceed the permitted amount. Explain over-receipt policy before coding it.

During review, ask the author to show one concrete failure: a stale editor, a duplicate request, an unauthorized ID or a failed final insert. Ask which test fails if the crucial condition is removed. Check schema constraints, HTTP errors, UI recovery and migration implications together. Conclude with the remaining limitation and a proportionate next step, rather than calling local success production readiness.
''')
w('astraupskill/07-TRACE-LAB.md',r'''
# Trace lab: one order, two clients, one inventory balance

Use a new persistent local learning database configured according to [setup](../README.md). Keep the browser Network panel open. The automated equivalent runs safely inside the temporary cluster through `npm run verify`. Do not run the destructive backend fixtures against your interactive database.

Create Notebook with price `3.25` and stock `5`. Inspect the POST `/api/products` request: price is a string, stock is an integer, and no caller-selected ID is sent. The response is 201 with a Location header. Follow that path with GET and compare the ID, price and version. The list endpoint returns an envelope containing a `data` array; the API client unwraps it before React sees the value.

Set quantity to `2` and enter `trace-customer`. Place the order. Its request should resemble:

```json
{"userId":"trace-customer","items":[{"productId":"COPY_THE_REAL_ID","quantity":2}]}
```

There is no total, price, status or product name in the request. Find the corresponding strict schema and explain what happens if you add a forged total. Follow service parsing into the repository transaction: fetch products, conditionally decrement stock and increment version, calculate Decimal totals, snapshot item name and price, insert the order and return it. The final total is `6.50`; remaining stock is `3`.

Now open an edit form before another client changes inventory. You can use a second browser tab to place another one-unit order. Return to the older form, change its name and save. Inspect the submitted version and the 409 response. The draft remains visible. Compare the refreshed catalog stock with the disabled draft stock. Confirm “Reload current product,” reapply your intended name change and save. Explain why automatically replacing only the version would be unsafe.

Cancel the first order. Observe the status transition and stock restoration. Repeat the transition directly from a local API client using the same order ID: the expected result is 409 and unchanged stock. The absence of a second cancel button is useful UX; the server condition is the actual consistency guard.

Finally change the catalog price and compare an older order. Its item price and name remain the purchase-time snapshot. Attempt to delete the referenced product. Expect conflict and preserved order history. Delete a separate unused product to demonstrate successful 204 handling without JSON parsing.

Write a trace table with columns for action, HTTP request, database invariant, response and UI recovery. Include at least one failed action. Finish by explaining two limitations: a lost successful order response can still lead to a duplicate on retry, and any local client can use another customer reference because authentication is absent. Accurate boundaries are part of the lab, not optional footnotes.
''')
w('astraupskill/VERIFICATION.md',r'''
# Verification evidence and practical limits

This project includes three complementary test layers and a repeatable full gate. The delivered evidence is recorded in the central implementation report and its per-project manifest. Run `npm run verify` from the root to reproduce the database, frontend, browser and build checks. Prerequisites are Node/npm, PostgreSQL command-line binaries and the Playwright Chromium installation matching the locked dependency version.

The verification environment used Node 22.16.0, npm 10.9.2, PostgreSQL 18.1, Prisma 5.22.0 and Playwright 1.60.0. Dependency lockfiles cover root, backend and frontend. The initial install wrapper timed out, but npm's completion logs and subsequent dependency-tree checks showed successful installs in all three locations. The actual compile and runtime checks are stronger evidence than installation alone.

The backend suite contains 24 real PostgreSQL cases. It covers valid and invalid CRUD, version contention, last-unit reservation races, decimal totals, rollback after an invalid later cart item, injected final-insert failure, cancellation rollback, competing cancellation, fulfillment, reference protection, historical snapshots, pagination and malformed JSON. The frontend suite contains eight cases with controlled fetch responses. Five Chromium scenarios cover persisted catalog CRUD, order reservation/cancellation, stale form recovery, fulfillment and desktop/narrow layouts. Build checks compile both TypeScript projects and create the Vite production bundle.

The helper creates a new temporary cluster and applies the checked-in SQL migration. It replaces DATABASE_URL for its own child processes, uses allocated loopback ports, and requires a dedicated test marker before fixture cleanup. It stops its own cluster before removing its verified temporary path. A shutdown failure retains the data directory rather than deleting a potentially running cluster. Browser servers refuse to reuse an existing listener. Existing personal databases and original project data are not test fixtures.

Earlier failed runs remain useful diagnostic evidence. The initial backend run passed 23 cases and exposed referenced-product deletion returning 500; the final constraint declaration and regression check address that response mapping. An initial sandboxed Vitest launch failed because esbuild could not read an ancestor directory; full verification uses the reviewed execution path. Neither failure was counted as a pass.

The evidence does not establish production readiness. There is no authenticated ownership, request idempotency, payment service, supplier workflow, stock ledger, capacity benchmark, power-loss test or migration of an existing database. The `/health` endpoint reports process liveness, not database readiness. CORS is not access control. Browser reload proves committed records can be fetched again; it is not a server crash-recovery or failover experiment. The historical Docker Compose scaffolding was not executed. Treat the fresh initial migration separately from any future data-preserving upgrade of an older installation.
''')
print('Course complete; verification counts pending final gate')
