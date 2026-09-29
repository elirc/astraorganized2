from pathlib import Path
P=Path(__file__).resolve().parent/'stage/14690be423dc';D=P/'astraupskill';D.mkdir(exist_ok=True)
def doc(name,text): (D/name).write_text(text.strip()+'\n',encoding='utf-8')
doc('README.md',r'''
# Order management: protect the aggregate before adding an API

This Java CLI teaches CRUD through customers, products, orders, line items, discounts, and status transitions. The course focuses on an order as a related group of data whose rules must hold together. A line quantity is not merely an integer field: changing it changes the subtotal, can invalidate a discount, and may be forbidden by the order's current status.

The original application lost saved discounts during reload. It constructed an order with a discount but no items, recalculated against a zero subtotal, and clamped the discount to zero. Adding restored items afterward could not recover the original value. The delivered implementation restores the whole order at once, validates its saved discount against the complete item collection, and derives totals from owned item values.

Other changes support the same learning objective. Reads return detached orders and items. Paid orders reject edits. Quantity replacement is a first-class command and menu option. Sub-cent amounts are rejected rather than rounded silently. Customers, products, orders, and items now persist in one versioned atomic snapshot, and corrupt startup stops before an empty session can overwrite data.

## Run with learning data

Use JDK 17 or newer and set `JAVA_HOME` to your installed JDK if Java is not on PATH. From the project root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -Test
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -DataPath .\data\learning-orders
```

The override is a directory. With no override, the runner uses the project's `data` directory. It recompiles source before running, so old checked-in or leftover `out` classes are not the source of truth. The test command runs 35 regression cases with temporary data for filesystem scenarios.

Create a customer and an active product priced at 10.00. Create an order for that customer, add quantity 2, and apply a 5.00 discount. Save and restart: subtotal should be 20.00, discount 5.00, and total 15.00. Use menu 14 to change quantity to 3; the total becomes 25.00. Move through SUBMITTED to PAID, then try another quantity edit and observe the refusal.

## Course sequence

Follow the [code map](01-CODEBASE-MAP.md), [concepts](02-CONCEPTS.md), and [worked change](03-WORKED-CHANGE.md) before adding new features. Use [testing and debugging](04-TESTING-AND-DEBUGGING.md) with the [trace lab](07-TRACE-LAB.md). Attempt the [practice ladder](05-PRACTICE.md), then compare your reasoning with [solution guidance](06-SOLUTIONS-AND-REVIEW.md). The [verification record](VERIFICATION.md) describes executed checks and remaining limits.

This remains a single-threaded local application. It does not contain a browser, HTTP controller, authenticated owner model, database, payment processor, or stock reservation system. Those are possible extensions, and the exercises show where their boundaries would belong. A strong learning result is an explanation of why a rejected mutation leaves the order unchanged, why restoration differs from replaying interactive edits, and why an atomic file save is not a multi-user database transaction.
''')
doc('01-CODEBASE-MAP.md',r'''
# Read the code around the order's consistency boundary

[App.java](../src/oms/App.java) constructs `FileDataStore`, loads a complete `StoreSnapshot`, and initializes customer, product, and order services. Failed loading stops startup. The menu translates prompts into commands and prints results. Save is explicit through menu 12 or exit through 13. A failed normal exit keeps the session open so the user can retry; EOF attempts to save completed work and then closes input.

[CustomerService.java](../src/oms/service/CustomerService.java) and [ProductService.java](../src/oms/service/ProductService.java) own catalog maps. Their model objects are immutable, and the `all` methods return collection copies rather than live map views. Constructor duplicate checks prevent silently replacing one record with another during restoration. Product activity controls whether it can be added to an order; this project has no inventory quantity or reservation model.

[OrderService.java](../src/oms/service/OrderService.java) connects references: a new order needs an existing customer, and an added line needs an existing active product. It copies orders accepted during construction and returns detached copies from create, lookup, list, and `all`. `requireOrder` is private and obtains the owned aggregate for a command. The public quantity command delegates to `Order.setItemQuantity` rather than exposing a mutable item reference.

[Order.java](../src/oms/domain/Order.java) owns the item collection, discount, status, and timestamps. Its public edit methods enforce editable status and validate candidates before mutation. `getSubtotal` derives a sum from current item line totals; `getTotal` subtracts the validated discount. These values are no longer separate mutable caches that can disagree with an escaped item.

`Order.restore` receives all saved items at once. It copies them, rejects duplicate product lines, validates the discount against their subtotal, and checks whether the saved status requires items. It preserves saved timestamps instead of calling interactive edit methods that would touch `updatedAt`. `copy` uses the same complete construction path. This makes restoration a clear entry point rather than a partially initialized object plus a series of public repair calls.

[OrderItem.java](../src/oms/domain/OrderItem.java) stores the product ID, captured product name, quantity, and captured unit price. Quantity changes validate positivity; increments use checked integer addition. `Order.getItems` returns item copies. The catalog price and the order's price snapshot are different concepts, even if this small catalog currently has no price-update command.

[DomainValues.java](../src/oms/domain/DomainValues.java) centralizes required text and decimal precision. [OrderStatus.java](../src/oms/domain/OrderStatus.java) defines allowed transitions. `Order` adds the nonempty-item and editability rules around that transition graph.

[StoreSnapshot.java](../src/oms/persistence/StoreSnapshot.java) copies all collections, deep-copies orders, and validates duplicate identities and customer/product references through service constructors. [FileDataStore.java](../src/oms/persistence/FileDataStore.java) reads tagged records, groups items by order, restores complete aggregates, and writes a single atomic snapshot. [DelimitedFileUtil.java](../src/oms/persistence/DelimitedFileUtil.java) owns field escaping. The [regression harness](../test/oms/RegressionTests.java) exercises these actual boundaries with objects and real temporary files.
''')
doc('02-CONCEPTS.md',r'''
# Aggregates, state transitions, and historical snapshots

An aggregate is a group of related values with rules that must stay consistent through an operation. Here, an order's item quantities, price snapshots, discount, status, and total belong together. Allowing callers to mutate a line returned by `getItems` would bypass those rules. Even an unmodifiable list is insufficient if the contained items are still mutable shared objects.

```java
Order view = service.findById("O").orElseThrow();
view.getItems().get(0).setQuantity(99);
// The returned item is detached. Neither the view's aggregate nor
// the service's authoritative order changes through this item reference.
```

The intended update path is `service.updateItemQuantity(orderId, productId, quantity)`. The aggregate builds a candidate line using the existing name and unit price, computes the proposed subtotal, and checks the discount before replacing the line. If a quantity reduction would make subtotal smaller than the discount, it rejects the command. The user must reduce the discount explicitly first; the application no longer silently changes a discount as a side effect of recalculation.

Derived totals reduce the number of facts that must be kept synchronized. The subtotal is the sum of line totals, and total is subtotal minus discount. The application still stores a line total inside each `OrderItem`, but that item's own quantity method maintains it and owned items never escape. A future immutable line-item design could derive that value too; adding more caches without an ownership rule would move in the wrong direction.

Restoration is not the same as applying user commands. A paid order loaded from disk must regain its existing items and discount without reopening it for editing or changing its saved update time. `Order.restore` therefore accepts a complete collection and validates the resulting state directly. It does not call `addOrMergeItem` on a paid order, and it does not temporarily compare the discount to an empty subtotal.

Status transitions express workflow. DRAFT can become SUBMITTED or CANCELLED; SUBMITTED can become PAID or CANCELLED; PAID can become SHIPPED or CANCELLED; SHIPPED and CANCELLED are terminal. Only DRAFT and SUBMITTED permit content edits. SUBMITTED, PAID, and SHIPPED require items, and a submitted order cannot lose its final item. Cancellation from PAID is only a local state transition here: no payment or refund integration exists.

An order line captures product name and unit price when added. Merging another quantity of the same product keeps that existing snapshot. This preserves a stable order price even if a later catalog exercise adds price changes. Decide a different repricing policy explicitly rather than letting a getter fetch current catalog price during every total calculation.

Finally, validation and persistence protect different boundaries. The aggregate rejects invalid commands; the snapshot validates references across customers, products, and orders; atomic file replacement keeps related saved records together. None of these supplies authenticated ownership, concurrent request handling, cross-process stale-write detection, or payment idempotency. Those are the next lessons when this CLI becomes a CRUD web application.
''')
doc('03-WORKED-CHANGE.md',r'''
# Worked change: restore the complete order before validating totals

Begin with an order containing two units at 10.00 each and a 5.00 discount. The expected total is 15.00 before and after saving. The original reload produced a zero discount and a total of 20.00. This was not a formatting problem or an incorrect multiplication; it was an initialization-order defect.

The old constructor accepted the saved discount, initialized an empty item collection, and immediately recalculated totals. Its recalculation method clamped a discount larger than subtotal down to subtotal. Because subtotal was temporarily zero, the discount became zero. `FileDataStore` later added saved items one by one, but the original discount value had already been discarded.

The delivered design removes that temporary invalid state. The loader first parses order metadata and groups all item records by order ID. It then calls a complete restoration entry point:

```java
Order restored = Order.restore(
    "O", "C", OrderStatus.PAID, new BigDecimal("5.00"),
    savedCreatedAt, savedUpdatedAt,
    List.of(new OrderItem("P", "Notebook", 2, new BigDecimal("10.00")))
);
```

The factory copies all item values, rejects duplicate product lines, calculates the full subtotal, and validates the saved discount. It preserves status and timestamps directly. Paid status prevents interactive edits, but does not prevent reconstruction of a valid paid order from a complete saved snapshot. A saved discount greater than the final subtotal is rejected rather than silently repaired.

The mutation design follows the same principle. Updating quantity constructs a candidate item and computes the proposed subtotal before replacing the existing line. Removing a line checks the remaining subtotal and submitted-order nonempty rule before deleting anything. Changing a discount validates precision and range before assignment. Failed changes do not touch `updatedAt`, so a rejected request does not falsely look like a successful edit.

The ownership correction prevents bypasses. `OrderService` stores copies of incoming orders and returns detached copies. `Order` copies incoming and outgoing item values. Customers and products are immutable, while their services return copied collections. As a result, clearing a collection or changing a returned item cannot secretly remove catalog entries or desynchronize authoritative order totals.

Persistence now writes one `oms.snapshot.txt` file with C, P, O, and I record tags plus a count footer. Previously, customers, products, order metadata, and items were rewritten separately. An interruption could combine different generations of data. The new save validates and serializes a complete snapshot before writing a temporary sibling and atomically replacing the destination. Loading an existing corrupt snapshot stops startup and never falls back silently to older legacy files.

The [regression suite](../test/oms/RegressionTests.java) contains both the initial failing reproduction and broader protections. Read the saved-discount case, complete paid restoration, failed quantity reduction, missing-reference rejection, and legacy migration tests. Explain which assertion detects the original bug and which assertions protect newly defined behavior. That distinction keeps a review focused on actual guarantees rather than a generic statement that the code was refactored.
''')
doc('04-TESTING-AND-DEBUGGING.md',r'''
# Test invariants across commands, copies, and reloads

The project-local command `powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -Test` compiles Java 17 source and runs 35 named regression cases. The harness has no external test dependencies. Filesystem tests create checked temporary directories, observe real files, and remove only their own test data. A nonzero exit indicates failure; printed output alone is not a substitute for checking the process result.

Seven initial cases failed against the original source: saved discounts disappeared, returned orders could mutate service state, returned items could invalidate aggregate totals, paid orders remained editable, sub-cent prices were accepted, live service collections could delete records, and carriage returns were dropped by the field codec. The final suite preserves these fixes and adds tests for the related boundaries discovered during implementation.

For command tests, assert both rejection and preservation. A quantity reduction below the active discount must leave quantity, discount, total, and update time unchanged. An invalid status transition must leave the old status intact. An attempted mutation through a returned copy must leave the authoritative service unchanged. These are more meaningful than checking that a private helper was called.

```java
var before = service.findById("O").orElseThrow();
rejects(IllegalArgumentException.class,
    () -> service.updateItemQuantity("O", "P", 1));
var after = service.findById("O").orElseThrow();
equal(before.getUpdatedAt(), after.getUpdatedAt());
equal(before.getTotal(), after.getTotal());
```

This sketch assumes the starting discount makes quantity 1 invalid. Always arrange the state explicitly; an exception caused by a missing order would not prove discount protection.

For restoration debugging, put a breakpoint where `FileDataStore.parseRows` calls `Order.restore`. Inspect the entire item collection before stepping into the constructor. The discount should be compared with the final subtotal, and no interactive method should update the saved timestamp. Then test a paid order, because restoring only drafts can hide an accidental dependency on editable status.

For persistence, use a real save followed by a new load. The suite verifies four-file legacy migration, authority of the new snapshot, missing footer/count errors, orphan item rejection, strict booleans, and a failed atomic move. A footer mismatch detects ordinary truncation or missing records, but it is not a checksum and does not prove resistance to intentional edits that also change counts.

The delivery also ran seven CLI scenarios in separate Java processes: catalog reload, discount reload, quantity persistence, precision rejection, paid edit refusal, EOF handling, and corrupt-startup byte preservation. The [manual trace](07-TRACE-LAB.md) lets you inspect these behaviors interactively. The normal exit retry branch was source-reviewed; the automated failure test targets the storage replacement operation, not a live terminal retry interaction.

No concurrent service access, browser, HTTP route, database transaction, or payment provider was tested. The application is intentionally single-threaded. Before making it a web server, add tests that match the new concurrency and persistence boundaries instead of assuming this local suite proves them.
''')
doc('05-PRACTICE.md',r'''
# Practice ladder toward a CRUD order-management web app

These exercises extend the delivered foundation. They are not claims about existing features. Choose one, write its acceptance examples, add a failing test, implement it, and explain its remaining limits before moving to the next. Keep format experiments in a separate learning directory.

## 1. Add catalog updates with stable order snapshots

Add a product rename/price/activity update command that replaces the immutable catalog product. Create an order at 10.00, change the catalog price to 12.00, and verify that the existing line remains 10.00. A newly created order should capture 12.00. Define what adding another quantity to the existing line means; the current merge policy keeps its original price. Test invalid precision and duplicate SKU policy explicitly rather than allowing accidental behavior from map insertion.

## 2. Add draft-order deletion and reference-safe customer changes

Implement confirmed deletion only for DRAFT orders under a documented rule. Decide whether a draft with items may be deleted or must be emptied first. Preserve submitted, paid, shipped, and cancelled records as history. Add customer profile updates without changing customer identity. A physical customer delete must account for referenced orders; a user interface that hides a delete button does not enforce referential integrity.

## 3. Add deterministic time and optimistic versions

Inject a clock so failed-update timestamp tests and tie-ordering tests do not depend on wall-clock timing. Add a version to orders and require an expected version for edits. Two callers read version 1; one edit succeeds and the other conflicts. The comparison and replacement must happen together under the eventual repository's concurrency mechanism. Merely adding a version field without enforcing it does not prevent lost updates.

## 4. Build the CRUD HTTP contract

Expose customers, products, orders, line quantity replacement, line removal, discounts, and status transitions through explicit routes. Decide whether a status transition is a resource replacement or a named command endpoint. Define invalid input, missing resource, and state/version conflict responses. Keep decimal representation explicit in JSON. Test that creating an order returns an ID that can be read, and that a paid quantity edit returns the documented error without changing persisted totals.

## 5. Replace snapshot files with transactional persistence

Model customers, products, orders, and order items with foreign keys and appropriate uniqueness constraints. Persist an order edit and its version together in one transaction. Add a failure after changing an item but before committing order metadata and prove rollback. Loading should reconstruct a complete aggregate without using interactive edit methods. Preserve price snapshots on item rows rather than joining current catalog price to calculate historical totals.

## 6. Add inventory reservation and an outbox

Introduce stock only after defining when it is reserved, released, and consumed. A submitted order could reserve stock, cancellation could release it, and payment/shipping could follow explicit transitions. Two competing orders must not reserve the same final unit. If you also publish a notification, store dispatch intent in the same transaction as the accepted transition, then dispatch asynchronously. Test a broker outage and retry without duplicating the business transition.

## 7. Add authenticated ownership and review evidence

Choose a tenant or owner model and apply it to every lookup and mutation, including nested item routes. Test that changing an order ID cannot reach another owner's order. Demonstrate a stale edit, invalid amount, denied cross-owner lookup, failed transaction, and repeated notification dispatch. A mid-level review should explain the authoritative state and commit point for each case, supported by tests that exercise the real adapter and persistence layer.
''')
doc('06-SOLUTIONS-AND-REVIEW.md',r'''
# Solution guidance and review questions

Use this after attempting the [practice ladder](05-PRACTICE.md). The sketches describe future changes, not code already delivered. Your solution should name its invariants and show failure preservation, even if you choose a different implementation approach.

For catalog updates, replace an immutable product in the catalog map while preserving its ID. Existing `OrderItem` values retain their captured name and unit price. A good test reads both the changed catalog product and the unchanged historical line. If SKU uniqueness is required, define case/whitespace normalization and check it on creation, update, and import. Do not rely on uniqueness of product IDs to imply uniqueness of SKUs.

For draft deletion, place the status rule in the command path and enforce it again at the persistence boundary if concurrent state changes are possible. A proposed SQL delete might include both the order ID and expected version/status. A zero affected-row count should produce a defined missing-or-conflict result. Customer deletion requires a reference policy: rejecting referenced deletes, archiving, or another explicit design. Cascading deletion of historical orders would change the domain meaning and should not be an accidental ORM default.

For optimistic concurrency, the critical operation is compare-and-update, not the mere existence of a version property. In a database, an update conditioned on `id`, `owner_id`, and `version` can make the check atomic. In memory, a lock or another coordinated state mechanism is needed. The current services are single-threaded and do not provide this guarantee. Test two operations released together and observe both results.

The HTTP adapter should translate domain outcomes without duplicating all business rules in controllers. A possible contract uses 400 for malformed values, 404 for a visible missing resource, and 409 for a stale version or forbidden state transition. Keep the public response consistent and avoid returning raw stack traces. A route such as `PUT /orders/{id}/items/{productId}` can represent quantity replacement, but define whether the line must already exist. The delivered CLI command requires an existing line.

For database restoration, query the order metadata and all its line snapshots, then call the complete restoration path once. Do not construct an empty paid order and attempt to add items through editing methods. Use foreign keys for customer/product references and a unique order/product constraint if the one-line-per-product policy remains. Validate the discount against the full subtotal before accepting imported state.

For inventory and messaging, keep business acceptance and notification delivery separate. Reserve stock and record an outbox row in one database transaction. A dispatcher can retry publication using a stable event identity. Successful dispatch does not retroactively create the business transition, and failed dispatch must not erase an already accepted order. Define how cancellation releases reservations and how duplicate requests replay or conflict.

During review, ask the author to draw one order edit from HTTP parsing through validation, version check, item change, commit, and response. Then ask what happens if the response is lost after commit. The answer should distinguish request idempotency from optimistic concurrency and from message dispatch deduplication. These are related but separate guarantees, and each needs its own observable test rather than a general claim that the application is reliable.
''')
doc('07-TRACE-LAB.md',r'''
# Trace lab: discount restoration and state-aware item edits

Use a new directory for this exercise:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -DataPath .\data\trace-orders
```

Create a customer with menu 1 and record its ID. Use a learning address such as `learner@example.test`; no email is sent. Create an active Notebook product with menu 3, SKU NOTE, and price 10.00. Record that product ID. Create an order through menu 5 using the customer ID, then record the order ID. These IDs connect the records; names are display values rather than reliable lookup keys.

Use menu 6 to add the product with quantity 2. Use menu 10 to apply a discount of 5.00. Menu 8 should show subtotal 20.00, discount 5.00, and total 15.00. Save with 12 and exit with 13. Restart using the same directory and inspect the order again. The discount must remain 5.00. Open `oms.snapshot.txt` and identify the O metadata row and I item row that were restored together.

Use menu 14 to replace quantity with 3. The price remains 10.00 and total becomes 25.00. Change the discount to 25.00, then try to reduce quantity to 2. The proposed subtotal would be 20.00, so the command must fail and preserve quantity 3, discount 25.00, and total 5.00. Reduce the discount explicitly before retrying the quantity edit. This sequence demonstrates that rejection protects the whole aggregate rather than just one field.

Move the order to SUBMITTED with menu 11, then to PAID. Try menu 14, menu 7 item removal, and menu 10 discount changes. Each content edit should be rejected. A PAID-to-SHIPPED transition is allowed, while SHIPPED-to-CANCELLED is not. The program does not charge a payment method or issue a refund; these are local status values only.

For a corruption trace, exit and copy the learning directory to a fresh destination. Append a line after the count footer in the copied snapshot, then compare its hash before and after startup:

```powershell
Copy-Item -LiteralPath .\data\trace-orders -Destination .\data\trace-orders-corrupt -Recurse
Add-Content -LiteralPath .\data\trace-orders-corrupt\oms.snapshot.txt -Value 'broken'
$beforeHash = (Get-FileHash -LiteralPath .\data\trace-orders-corrupt\oms.snapshot.txt).Hash
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -DataPath .\data\trace-orders-corrupt
$afterHash = (Get-FileHash -LiteralPath .\data\trace-orders-corrupt\oms.snapshot.txt).Hash
$beforeHash -eq $afterHash
```

Use an unused copy destination to avoid nested-directory surprises. Startup should stop before the normal menu and leave the corrupt copy unchanged. Keep the valid source directory as the recovery copy; do not force fallback by deleting an authoritative snapshot from real learning work.

Finish by reading the [regression tests](../test/oms/RegressionTests.java). Map each observation to a test and explain which checks use direct domain calls, service calls, or real files. Record why restoration preserves timestamps, why item reads cannot mutate authoritative totals, and why this single-threaded trace does not establish correctness for concurrent HTTP requests.
''')
doc('VERIFICATION.md',r'''
# Verification and remaining limits

The project was reviewed and tested in an isolated copy before delivery. Original saved data and old compiled artifacts are excluded from the finite delivery manifest. The central implementation report and project manifest `14690be423dc` record changed source, course files, backups, hash checks, and evidence.

Verification used Microsoft OpenJDK 17.0.10 and the project runner's `--release 17 -Xlint:all` compilation. The reviewed full-access compiler run succeeded. Seven initial tests failed against the original implementation: discount reload, service order ownership, item ownership, paid edit protection, sub-cent pricing, live collection deletion, and carriage-return round trips. The final suite passed **35 Java regression tests**.

The expanded tests cover input/output copies, snapshot isolation, rejected-discount timestamps, quantity replacement, discount-preserving rejection, empty submission, terminal-state edits, inactive products, checked quantity growth, paid restoration, impossible discounts, duplicate identities, missing references, duplicate item lines, strict booleans, legacy migration, authoritative snapshot corruption, footer/count validation, orphan items, codec errors, failed atomic replacement cleanup, repeated saves, and non-mutating loads of a new directory.

A separate script passed **seven CLI scenarios in new Java processes**, for **42 checks total**. It verified customer/product reload, preserved discount, quantity persistence with price snapshot, sub-cent discount refusal, paid edit refusal, EOF during incomplete input, and unchanged file bytes on corrupt startup. The project runner executes the 35 Java cases; central CLI logs and results are retained under `astra-remaining-improvements/checks/j7/`.

The application is single-threaded. No concurrent service use, multi-process file coordination, HTTP server, browser UI, authentication, database, inventory reservation, payment, refund, or message broker was implemented or tested. Paid cancellation remains a local status transition, and should not be presented as a completed refund workflow.

Edits remain in memory until explicit save, exit, or EOF handling. A forced termination can lose unsaved work. Failed normal exit retains the session for retry; that branch was source-reviewed, while automated failure injection exercised storage replacement itself. Atomic replacement is required and fails visibly if unsupported. Power-loss durability and network-filesystem behavior are not established.

The snapshot footer detects missing records and ordinary truncation by comparing counts. It is not a cryptographic integrity mechanism. Loading validates identities, references, model values, and complete order invariants, but does not verify historical business events that the application never recorded. Customer email validation is intentionally basic, and SKU uniqueness is not enforced.

Legacy migration requires all four old files or a wholly new dataset. The first successful save creates `oms.snapshot.txt` and leaves legacy files unchanged. The snapshot then becomes authoritative; old binaries do not understand it and should not be alternated against the same directory. Strict validation can reject previously tolerated incomplete or invalid data, which should be repaired in a reviewed copy. CLI failures are text diagnostics rather than a structured automation exit-code contract. These boundaries are explicit subjects for the next CRUD web-development exercises.
''')
(P/'README.md').write_text(r'''# Order Management System

A Java 17 CLI learning project for customers, products, orders, items, discounts, and status transitions. The detailed [CRUD upskilling course](astraupskill/README.md) explains the actual source, worked fixes, examples, tests, debugging, and exercises toward a mid-level web application.

## Run and test

Install JDK 17 or newer and set `JAVA_HOME` if needed. From this project root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -Test
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -DataPath .\data\learning-orders
```

The override is a directory. Without it, the runner uses the project's `data` directory. The runner recompiles source and runs 35 dependency-free Java regression tests with `-Test`. Existing old `out` classes are not the current implementation until recompiled.

## Current behavior

Options 1–13 retain customer/product/order creation and listing, item addition/removal, details, discounts, status changes, save, and exit. Option 14 replaces an existing line's quantity while preserving its product name and unit-price snapshot.

Only DRAFT and SUBMITTED orders permit content edits. SUBMITTED, PAID, and SHIPPED require items; a submitted order cannot lose its final item. Paid and terminal orders reject quantity, item, and discount edits. Status transitions remain DRAFT to SUBMITTED/CANCELLED, SUBMITTED to PAID/CANCELLED, PAID to SHIPPED/CANCELLED, and no transitions from SHIPPED/CANCELLED. These statuses do not perform real payments or refunds.

Money must be non-negative or positive as appropriate and exactly representable with two decimal places. Sub-cent input is rejected without silent rounding. A quantity reduction or item removal that would make subtotal smaller than the discount is rejected; reduce the discount explicitly first.

Orders and items returned from reads are detached copies. Totals derive from owned item values. Restoration receives all items together before validating the saved discount, so discounts and timestamps survive reload without replaying interactive edits.

## Code responsibilities

- `App`: prompts, command translation, explicit save, exit, and EOF handling.
- `CustomerService` / `ProductService`: catalog identity and collection ownership.
- `OrderService`: customer/product lookup and commands on owned orders.
- `Order`: aggregate rules, complete restoration, copies, and derived totals.
- `OrderItem`: captured product values, guarded quantity, and line total.
- `DomainValues` / `OrderStatus`: field normalization and transition graph.
- `StoreSnapshot`: detached collections and cross-record reference validation.
- `FileDataStore` / `DelimitedFileUtil`: strict format parsing, migration, and atomic saving.

See the [code map](astraupskill/01-CODEBASE-MAP.md) for method-level traces.

## Saving and migration

The current authoritative file is `oms.snapshot.txt` inside the selected directory. It contains a version header, tagged customer/product/order/item records, and a count footer. Saving validates and serializes the whole snapshot before writing a temporary sibling and atomically replacing the target. There is no non-atomic fallback.

If no snapshot exists, loading accepts a complete legacy set of `customers.txt`, `products.txt`, `orders.txt`, and `order_items.txt`, or a new directory with none. Partial legacy sets fail explicitly. The first successful save creates the snapshot and preserves old files. Once created, the snapshot is authoritative; corruption does not silently fall back to older files. Do not alternate old binaries and the delivered runner against the same dataset.

Corrupt startup stops before the menu and does not overwrite the rejected file. A failed normal exit keeps the session open for retry. Save-on-exit and explicit save still mean a force-killed process can lose unsaved edits.

## Verification and next steps

Delivery verification passed 35 Java regression tests and seven separate-process CLI scenarios. Read the [verification record](astraupskill/VERIFICATION.md) for limits. The [practice ladder](astraupskill/05-PRACTICE.md) adds catalog updates, draft deletion, optimistic versions, HTTP contracts, database transactions, inventory/outbox behavior, and authenticated ownership.

This is a single-threaded local application. Atomic replacement does not supply cross-process locking, database transactions, power-loss guarantees, or request idempotency. No browser, HTTP API, real payment, stock reservation, or authentication is present.
''',encoding='utf-8')
