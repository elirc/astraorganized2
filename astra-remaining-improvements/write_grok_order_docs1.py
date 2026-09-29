from pathlib import Path
s=Path('astra-remaining-improvements/stage/e502bf8af566')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('README.md',r'''
# Order and inventory learning lab

A React + Express + Prisma/PostgreSQL CRUD application for learning reliable product editing, inventory reservations and order transitions. Start with [the learning course](astraupskill/README.md).

Implemented: product create/list/read/update/delete; version-checked edits; paged product/order lists; server-priced order creation; transactional stock reservations; cancellation with one-time stock restoration; final fulfillment; historical item names/prices; structured validation and errors; a responsive UI with conflicts and confirmation dialogs.

This is a shared local demo. `userId` is a caller-provided customer reference, not authenticated identity. Supplier and PurchaseOrder models are future exercises with no implemented routes. There is no payment processing, request idempotency or deployment hardening.

## Install and verify

Prerequisites: Node 22, npm, and PostgreSQL binaries (`initdb`, `pg_ctl`, `createdb`). Verification was performed with PostgreSQL 18.1. From this project root:

```powershell
npm run install:all
npx playwright install chromium
# Override if PostgreSQL binaries are elsewhere:
$env:POSTGRES_BIN = 'C:\Program Files\PostgreSQL\18\bin'
npm run verify
```

`verify` owns a temporary loopback-only test cluster, applies the migration, runs database/frontend/browser tests and builds both apps, then stops that cluster. It never connects to your normal DATABASE_URL. Results go to `.verification`. Tests intentionally truncate tables only in the helper-created database. PostgreSQL must permit running these binaries under your account; Unix root cannot run initdb.

## Run for learning

Create a **new empty** PostgreSQL database named `order_learning` using your local database administration tools. Copy `backend/.env.example` to `backend/.env` and replace its connection placeholders. Copy `frontend/.env.example` to `frontend/.env`. Then:

```powershell
npm exec --prefix backend prisma generate
# Run from backend so Prisma reads backend/.env and schema:
Set-Location backend
npx prisma migrate deploy
Set-Location ..
npm run dev:api
# In another terminal at the project root:
npm run dev:web
```

Open Vite's local URL. Create a product, select an order quantity, enter a customer reference, and place an order. Refresh to observe database persistence. Cancellation restores stock; fulfillment leaves stock consumed. A product referenced by order history cannot be deleted.

The initial migration targets a fresh database. If you already have data from the previous schema, review a separate data-preserving migration/baseline plan; do not reset it or apply this initial migration blindly. The old Docker Compose file is optional historical scaffolding and was not executed during verification.

Commands: `npm run test:api` for isolated database cases; `npm run test:web` for frontend cases; `npm run build` for both builds. Full evidence and remaining work are explained in [VERIFICATION](astraupskill/VERIFICATION.md).
''')
w('JOURNAL.md',r'''
# Implementation journal

The earlier scaffold described an order transaction while leaving stock updates as a TODO. The current implementation puts reservation, historical item snapshots and order creation in one PostgreSQL transaction. Product version checks also prevent a stale catalog form from restoring stock consumed by an order.

The original Jest configuration and Vitest imports disagreed. Backend tests now use Jest against a temporary real PostgreSQL cluster. Frontend tests use Vitest/jsdom; Playwright covers browser-to-database workflows. See [verification](astraupskill/VERIFICATION.md) for executed evidence and limitations.

The React catalog now supports CRUD and order workflows. Business transitions are PENDING to CANCELLED or FULFILLED. Cancellation restores stock once. Fulfillment is final, with no payment integration. Reference constraints protect historical products.

Follow-up learning work is in [practice](astraupskill/05-PRACTICE.md). Authentication, tenant ownership, idempotency, stock movement ledgers and existing-database migration are proposals, not delivered features.
''')
w('PHASE_PLANS.md',r'''
# Learning phases

1. **Delivered foundation:** typed API client, explicit product inputs, list pagination, CRUD UI, version checks and readable errors.
2. **Delivered domain consistency:** database transactions, server decimal prices, historical item snapshots, stock reservation, cancellation and fulfillment.
3. **Delivered verification:** guarded temporary PostgreSQL cluster, real database tests, frontend boundary tests and Chromium workflows. Read [the evidence](astraupskill/VERIFICATION.md).
4. **Learner extension:** add stock-movement records and order request idempotency with concurrent retry tests.
5. **Learner extension:** add authenticated ownership, tenant-scoped queries, authorization tests and operational readiness. Supplier/purchase-order workflows also remain exercises.

Use [the detailed practice sequence](astraupskill/05-PRACTICE.md) and [review guidance](astraupskill/06-SOLUTIONS-AND-REVIEW.md). A deployment should not be inferred from local verification.
''')
w('astraupskill/README.md',r'''
# From CRUD screens to reliable inventory workflows

This course uses an actual React, Express, Prisma and PostgreSQL application. Your objective is to explain a change across the browser, HTTP boundary, business rules and database, then prove that it behaves correctly when two people act at once. That is a useful step from junior feature implementation toward mid-level ownership.

Start by reading the [project setup](../README.md). Install the locked dependencies and run `npm run verify`. The helper creates its own disposable PostgreSQL database; it does not require you to sacrifice an existing learning database. For interactive work, configure a new persistent local database separately. Keep those two purposes distinct: repeatable automated fixtures and a sandbox whose records you want to keep.

## A concrete first session

Create a product called Notebook with price `3.25` and stock `5`. Set its order quantity to `2`, use `customer-a` as the customer reference and place the order. The order total must be `6.50`, and stock becomes `3`. Reload the browser. Both the order and remaining stock should still be visible because PostgreSQL holds the data. Cancel the order and observe stock return to `5`. There is no second cancellation button because the order is now terminal; the server also rejects a repeated cancellation.

Next, try deleting Notebook. Its order history still refers to it, so deletion returns a conflict. Explain why cancelling a sale does not mean deleting its audit evidence. Create an unused Pen instead and delete that product. Those two outcomes demonstrate domain rules more clearly than a generic delete-everything endpoint.

## Reading and practice sequence

Read [the code map](01-CODEBASE-MAP.md), then [concepts](02-CONCEPTS.md). Work through [the change walkthrough](03-WORKED-CHANGE.md) with the source open. Use [testing and debugging](04-TESTING-AND-DEBUGGING.md) to investigate failures. Complete [practice](05-PRACTICE.md) before consulting [solutions and review](06-SOLUTIONS-AND-REVIEW.md). Finish with [the trace lab](07-TRACE-LAB.md) and compare your claims with [verification](VERIFICATION.md).

For each session, keep a small engineering note: the user-visible problem, the invariant you want to preserve, the files involved, the test that would fail without your change, and the remaining limitation. For example: “Stock may never go below zero; two customers compete for one unit; one order succeeds and one conflicts.” This statement drives both implementation and testing.

The customer reference is not login. There is no ownership boundary, real payment, request retry deduplication or production deployment. Learn to state these limits as precisely as the implemented features. A mid-level engineer can distinguish a passing demonstration from the evidence needed for a wider release.
''')
w('astraupskill/01-CODEBASE-MAP.md',r'''
# Follow one request through the codebase

Begin at [main.tsx](../frontend/src/main.tsx), which mounts React. [App.tsx](../frontend/src/App.tsx) creates a QueryClient for that mounted application. The client caches server responses, but it is not the database and does not own stock. [ProductsPage.tsx](../frontend/src/features/products/pages/ProductsPage.tsx) contains the catalog, product editor, cart and order history. Local component state holds unsaved input. Query state holds fetched products and orders. Keeping those categories separate prevents a background refresh from silently replacing a draft.

The [API client](../frontend/src/api/client.ts) defines Product, Order and ProductInput types. It checks the HTTP status before returning the response's `data`. A non-success response becomes an ApiError; a successful 204 returns without parsing JSON. This small boundary prevents an error object from masquerading as a product array. Types help callers during compilation; server validation remains necessary because any client can send HTTP requests.

On the server, [index.ts](../backend/src/index.ts) loads environment configuration, starts the listener and disconnects Prisma on shutdown. [app.ts](../backend/src/app.ts) constructs an injectable Express application, assigns request IDs and translates failures into consistent JSON. Tests pass a Prisma client connected to their own database. The listener and app factory are separate so tests do not need to find or reuse an ordinary development port.

Read [product routes](../backend/src/routes/productRoutes.ts) and [order routes](../backend/src/routes/orderRoutes.ts) next. A route maps HTTP to a service call and selects status codes or a Location header. [validation.ts](../backend/src/validation.ts) defines accepted payloads and pagination bounds. Services parse unknown input and call repositories. Repositories own the database operations and transaction boundaries. See [productRepository.ts](../backend/src/repositories/productRepository.ts) for version checks and [orderRepository.ts](../backend/src/repositories/orderRepository.ts) for reservation and restoration.

## Data ownership map

| Data | Owner | Example |
| --- | --- | --- |
| Unsaved product text | React draft state | A proposed name after a conflict |
| Fetched catalog | Query cache, refreshed from API | Stock displayed on a card |
| Authoritative quantity | PostgreSQL Product | Stock checked during reservation |
| Purchase-time description and price | PostgreSQL OrderItem | Notebook at 3.25 even after catalog changes |
| Order lifecycle | PostgreSQL Order | PENDING changes once to a terminal state |

Read [schema.prisma](../backend/prisma/schema.prisma) beside the SQL migration. Prisma describes models; the migration also creates database check constraints. Supplier and PurchaseOrder are retained models for future exercises. Their presence is not evidence of implemented screens or routes.

Finally inspect [the database helper](../scripts/test-database.mjs), [backend cases](../backend/src/__tests__/orderService.test.ts), [frontend cases](../frontend/src/__tests__/ProductsPage.test.tsx) and [browser cases](../e2e/orders.spec.ts). For every behavior you explain, identify which layer of evidence supports it and which layer remains untested.
''')
w('astraupskill/02-CONCEPTS.md',r'''
# Invariants, transactions and conflicts

An invariant is a condition that must remain true after a successful operation. Here, stock cannot be negative; one pending order can restore its stock at most once; an order's price comes from the server's catalog; historical item prices do not change when the catalog changes. Writing these conditions first is more useful than starting with controller names.

## Atomicity is about all related writes

Suppose a cart contains two products. Reserving the first succeeds, but the second has insufficient stock. If each update commits independently, the customer receives no order while the first product loses stock. In [orderRepository.ts](../backend/src/repositories/orderRepository.ts), reservation and order creation run inside one interactive transaction. An exception aborts the transaction, restoring earlier writes. The test suite also injects a failure at the final order insert: this proves that successful reservations alone are not enough to commit the workflow.

A transaction does not automatically settle every race. Consider two requests that both read stock `1`. Each initially believes it can buy the item. The implementation uses a conditional update matching the product's version and sufficient stock. One request changes stock and increments the version; the other finds that its condition no longer matches and returns a conflict. The database evaluates the condition at the write boundary. A prior JavaScript `if` alone would not provide that guarantee.

## Optimistic product editing

A product editor remembers version `4`. An order reserves stock and increments it to `5`. The editor still contains the older stock value. Sending an unconditional full update would restore consumed inventory. PATCH therefore includes the expected version. On conflict, the UI preserves the draft but disables that stale write until the learner explicitly reloads current data. It does not quietly attach version `5` to old stock; that would defeat the purpose of the check.

## Money and history

Prices cross HTTP as decimal strings, for example `"3.25"`. Validation allows at most two fractional digits. Prisma Decimal calculates totals without binary floating-point accumulation. The server ignores no forged price field: strict schemas reject it. OrderItem stores the catalog name and price at creation, so later renaming Notebook to Journal does not rewrite an earlier purchase description.

## State transitions and deletion

PENDING may become CANCELLED or FULFILLED. Cancellation changes the status and restores quantities in the same transaction. Its conditional status update ensures concurrent cancellation requests have one winner. Fulfillment leaves stock consumed. There is no payment provider behind that word. Product deletion is version-checked and constrained by foreign keys; referenced order history remains valid. The migration uses non-deferrable NO ACTION references, which reject an invalid delete at the statement boundary.

These guarantees have limits. A retried successful POST can create a second order because request idempotency is not implemented. Customer references are caller-controlled, so transactions do not establish authorization. Learn the difference between data consistency, identity and delivery uncertainty before combining them in later exercises.
''')
print('Setup and first three course files written')
