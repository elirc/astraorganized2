from pathlib import Path
s=Path('astra-remaining-improvements/stage/e502bf8af566')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
p=s/'README.md';t=p.read_text();t=t.replace('npm exec --prefix backend prisma generate\n# Run from backend so Prisma reads backend/.env and schema:\nSet-Location backend\n', '# Run from backend so Prisma reads backend/.env and schema:\nSet-Location backend\nnpx prisma generate\n');p.write_text(t,encoding='utf-8')
w('astraupskill/03-WORKED-CHANGE.md',r'''
# Worked change: prevent a stale editor from restoring sold stock

The original scaffold could create order rows but did not implement the promised stock transaction. Once reservation exists, another bug becomes possible: a product editor opened earlier can overwrite the new quantity. This walkthrough follows the delivered solution. Keep [the product repository](../backend/src/repositories/productRepository.ts), [order repository](../backend/src/repositories/orderRepository.ts) and [product screen](../frontend/src/features/products/pages/ProductsPage.tsx) open beside it.

## Reproduce the business problem

Imagine Product A has stock `5`, version `1`. Alice opens its edit form. Bob places an order for one unit, leaving stock `4`, version `2`. Alice changes only the name, but her form still contains stock `5`. An ordinary “update every submitted field by ID” operation would erase Bob's reservation. Both users performed reasonable actions; the server must arbitrate their overlap.

The request now includes the version Alice actually read:

```json
{"name":"Renamed notebook","price":"3.25","stock":5,"version":1}
```

Product input validation requires that version to be a positive integer. The repository performs `updateMany` with both `id` and `version` in its condition. Its data increments version while replacing allowed fields. If the count is zero, the repository distinguishes a missing product from a changed product and throws 404 or 409 respectively. A transaction keeps the winning write and returned row together.

## Make all inventory writers cooperate

A version column is ineffective if only the editor increments it. Order reservation also increments Product.version. Cancellation increments it while restoring stock. Therefore any form loaded before a stock movement is stale. This is a code-review question you can answer by searching for every product stock write, rather than trusting the first method you find.

The order transaction first reads the product and then conditionally reserves quantity using its fetched version and sufficient stock. Competing orders cannot both consume the same final unit. Sorting product IDs gives transactions a consistent reservation order, reducing lock-order contention. It is not a promise that all possible database deadlocks disappear.

## Give the user a safe recovery path

The API client turns 409 into ApiError. The screen retains the proposed form text, reports the error, refreshes fetched data and disables the stale save. “Reload current product” asks before discarding the proposal and creates a new draft from current fields and version. The learner must reapply intended changes against the latest stock. Merely replacing the version token while keeping old stock would allow the same lost update on the next click.

## Prove the change

The backend case creates a product, reserves stock, submits the original version and checks that stock remains reduced. The browser case performs the same race through an open editor and a separate HTTP request, then checks draft preservation and explicit reload. These tests support different claims: server rejection and usable recovery. Add a test for cancellation overlapping an edit as your first extension. The expected result is a conflict that preserves restored stock, not a clever automatic merge of unrelated fields.
''')
w('astraupskill/04-TESTING-AND-DEBUGGING.md',r'''
# Test the failure boundary, not only the happy path

Run `npm run test:api` from the project root for database cases, `npm run test:web` for frontend cases, and `npm run verify` for the complete build and browser gate. Read [the helper](../scripts/test-database.mjs) before changing these commands. It allocates a loopback port, creates a temporary PostgreSQL cluster, creates `astra_order_test`, generates Prisma, applies the migration and invokes Jest. Cleanup stops only the cluster directory it created. If shutdown cannot be confirmed, the directory is retained for investigation.

The backend suite additionally requires the helper marker, loopback hostname and exact database name before any table truncation. These guards are protections against accidental test configuration, not a sandbox against intentionally malicious code. Never remove them just to point the suite at your normal database. If initdb fails, inspect its log and binary path rather than bypassing isolation.

## Three complementary layers

[Backend tests](../backend/src/__tests__/orderService.test.ts) send real HTTP requests through Supertest and use real PostgreSQL transactions. They cover precision, unknown fields, CRUD versions, final-unit contention, historical snapshots, one-time cancellation and database constraints. SQL triggers deliberately fail an order insert or a later restock. Those cases check that earlier changes roll back as well. A mocked repository returning success could not establish those properties.

[Frontend tests](../frontend/src/__tests__/ProductsPage.test.tsx) run React in jsdom with a controlled fetch boundary. They inspect submitted payloads, failed loads, confirmation cancellation, empty 204 responses, retained order quantities and stale drafts. These cases make UI recovery easy to isolate. They do not prove PostgreSQL behavior because fetch is replaced.

[Browser tests](../e2e/orders.spec.ts) run Chromium, the actual API and the temporary database. They create and reload catalog records, reserve and restore stock, check fulfillment and exercise a stale edit caused by another HTTP client. Layout checks inspect document width at desktop and narrow sizes and capture screenshots. Passing width checks alone does not establish full accessibility or visual correctness.

## A debugging routine

For an unexpected 500, record the response requestId and reproduce with the smallest payload. Inspect the server-side error and database log; avoid returning raw SQL details to the browser. For a 409, inspect the current version and status before retrying. For a failing browser test, compare the API response with the visible state: was the mutation rejected, was the cache not refreshed, or was a form deliberately preserved?

One verification run found referenced-product deletion returning 500. PostgreSQL rejected the delete correctly, but the initial RESTRICT constraint did not produce the handled ORM error on the tested stack. The final migration uses non-deferrable NO ACTION references and the regression still requires 409 plus preserved records. This illustrates why asserting only “an error occurred” is too weak.

Do not increase timeouts to hide a deadlock without investigation. Keep failed logs, identify the layer, fix the cause and rerun affected checks. A passing suite describes exercised behavior under its environment; it does not prove power-loss recovery, production capacity or authenticated ownership.
''')
w('astraupskill/05-PRACTICE.md',r'''
# Progressive work toward mid-level CRUD ownership

Complete these exercises in order. Each asks for a behavior, an invariant and evidence. The features below are proposed learner work, not features already implemented. Keep changes small enough that another person can review the reasoning and the failing test together.

## 1. Filter the catalog without breaking paging

Add a name filter with a maximum length and explicit empty-string behavior. Extend the server query schema rather than accepting arbitrary Prisma filters. Include the filter in the QueryClient key and reset the page when it changes. Seed more than twenty products and prove the second page belongs to the same filter. Test rapid filter changes with delayed responses so an older request cannot overwrite the current result. Explain whether case sensitivity is defined by your query or database collation.

## 2. Add an inventory movement ledger

Create a StockMovement model recording product, signed quantity, reason, timestamp and an order reference where appropriate. Write reservation and cancellation movements in their existing transactions. A failed order insert must leave neither stock changes nor movement rows. A repeated cancellation must not create another restoration movement. Decide how direct catalog stock edits appear in the ledger; a journal that ignores adjustments cannot explain the balance. Build a read-only product history view and compare its sum with the stored quantity using a known opening balance.

## 3. Make order creation safe to retry

Add a caller-supplied idempotency key scoped to a future account or an explicitly documented local namespace. Store the key, canonical request fingerprint and winning order in the same transaction. Two concurrent equivalent requests should return one order; the same key with a different cart should conflict. Simulate the client losing the first successful response and retrying. Demonstrate that stock is reserved once. Do not merely disable the Place order button: that protects one mounted browser event path, not network retries or another tab.

## 4. Introduce authenticated ownership

Design an Account or Tenant boundary and derive it from verified server identity. Replace trust in the customer reference as a security mechanism. Scope every read, update, delete and transition, including nested product IDs in a cart. Test two users who know each other's resource IDs. An order belonging to one tenant must not reserve another tenant's product. Explain how unique constraints and idempotency scopes incorporate the owner. This exercise requires a complete authorization design, not just adding a login screen.

## 5. Implement supplier purchasing

Use the retained Supplier and PurchaseOrder models as a starting point. Specify draft, ordered and received states and whether partial receipt is supported. Receiving stock must update products and receipt history atomically. Repeat receipt commands need a defined conflict or replay rule. Add API validation, UI errors and transaction failure tests before expanding the dashboard. Do not claim procurement is complete because a model exists.

## 6. Plan a safe release

Write a migration plan for the previous schema's existing records, including historical names, decimal precision and invalid status values. Work on a disposable copy and preserve the original. Add separate process-liveness and database-readiness checks, bounded structured logs, graceful shutdown verification and an operational recovery note. State your expected workload before choosing indexes or caching. Finish with a short review document showing which invariants each test protects and what remains uncertain.
''')
print('Worked change, testing and practice written')
