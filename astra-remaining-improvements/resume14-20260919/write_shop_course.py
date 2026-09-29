from pathlib import Path
P = Path(__file__).resolve().parent.parent / 'stage/34d60d325094'
chapters = {
'README.md': ('Refund preflight and request-bound replay', '''
NetShopifyLite is a .NET 8 shop scaffold with EF Core, PostgreSQL and a React frontend. This course follows checkout and refunds across the domain, application handler, payment-provider port and database. The central improvement is rejection before an irreversible provider action: invalid refund batches and unavailable checkout inventory are validated as a whole before any payment request or aggregate mutation.

The completed implementation adds a pure refund plan, positive remaining-quantity checks, request fingerprints for idempotency records and complete inventory preflight. A matching request can replay its recorded order. A key reused with different customer, cart, email or refund details must fail. Legacy records without fingerprints require reconciliation rather than automatically returning an unrelated order. Discounted refunds are explicitly unsupported until the project has a net line-allocation ledger; rejecting them before the provider avoids refunding gross prices greater than the amount paid.

Prerequisites are basic C#, async handlers, entity tracking, relational transactions and decimal arithmetic. Money in this project uses decimal major units with two-decimal validation at the changed order boundaries. This differs from projects that represent cents as integers. A preflight computes a valid plan without mutation. Idempotency binds a retry key to an operation identity. Neither term means that a database transaction and an external provider become one atomic system.

Restore the solution with .NET 8, then run its tests using Docker or the supplied local PostgreSQL helper. The helper owns a temporary loopback cluster and the fixture owns a generated database. Tests use recording fake payments, not live charges. Read VERIFICATION and the additive fingerprint upgrade notes before applying schema changes to an existing development database.

Follow the map and worked change, attempt the exercises, and trace the provider-success/database-failure window. The course explains both the improved rejection guarantees and the operational work that remains outside this teaching scaffold.
''', None),
'01-CODEBASE-MAP.md': ('Trace the handler, aggregate and persistence model', '''
CheckoutCommand and RefundOrderCommand live in src/NetShopifyLite.Application/Orders. Their handlers invoke validators directly before reading replay records, so future internal callers do not depend on an HTTP validation pipeline having run. RequestIdentity serializes a normalized request description and hashes it. IdempotencyRecord stores that fingerprint alongside key, endpoint and resource ID.

RefundOrderHandler loads the order with lines, payments, refunds and timeline. It rejects duplicate line IDs before building a dictionary, then asks Order.PreflightRefund to validate the entire batch and calculate its total. If restocking is requested, it resolves every inventory target and validates each aggregate quantity before contacting the provider. Only after a successful provider result does it apply the domain refund, restock and save the replay record.

Order and OrderLine are in Domain/Sales/OrderModels.cs. OrderLine.PreflightRefund validates a positive quantity against the remaining quantity using subtraction, avoiding overflow from addition. Order.PreflightRefund checks financial state, supported pricing policy, every requested line and the remaining paid amount. Order.Refund repeats that pure validation before changing any line, creating history or touching timestamps.

CheckoutHandler loads the cart and customer, checks cart ownership and expiry, prices an order candidate and resolves all inventory reservations. A successful payment result is followed by reservation and order payment state changes. A declined result records a failed order without first mutating and undoing inventory. AppDbContext persists the complete graph and the idempotency record.

The EF mapping uses public collection navigations with backing-field access and declares domain-generated GUIDs. This avoids duplicate navigation discovery and mistaken updates of newly appended child records. Tests exercise the production model with PostgreSQL, while the provider remains a controlled fake that counts actual handler invocations.
''', ('src/NetShopifyLite.Application/Abstractions/RequestIdentity.cs', 'public static class RequestIdentity', None)),
'02-CONCEPTS.md': ('Preflight is not a distributed transaction', '''
The old refund order was dangerous: calculate a gross amount, call the provider, then let the domain discover a foreign line, excessive quantity or invalid financial state. Reversing that order makes predictable rejection safe. A pure plan also prevents a multi-line domain call from refunding its first line before failing on a later one. The plan is computed completely before the first quantity or timeline mutation.

Refund arithmetic must reflect what was paid. This delivery deliberately rejects discounted refunds because it does not yet implement a deterministic net allocation ledger. Multiplying each line's gross unit price is unsafe after an order-level discount. Supporting that feature later requires minor-unit allocation, a remainder policy and persisted line allocations that remain stable across partial refunds. A clear early rejection is the defined behavior today.

Idempotency requires identity as well as a key. A checkout key previously located a record by endpoint and key, then returned its order without comparing the new customer or cart. The fingerprint now binds those fields, normalized email and discount description, and the payment scenario. Refund fingerprints use the order, restock choice and lines sorted by line ID, so reordered equivalent requests can share identity while changed quantities cannot.

The database save still cannot atomically commit an external provider action. A successful provider response followed by a database failure can leave an unrecorded payment or refund. Concurrent first requests also need a stronger provider/database coordination design than a post-action unique replay record. The current code relies on provider idempotency behavior and does not claim exactly-once financial processing.

Likewise, a supplied customer ID is not a trusted authenticated principal. Cart-to-customer matching improves consistency but does not replace authorization. Keep identity binding, access control, database atomicity and provider recovery separate when discussing this scaffold's guarantees.
''', ('src/NetShopifyLite.Domain/Sales/OrderModels.cs', '    public Money PreflightRefund', 'public sealed class Payment')),
'03-WORKED-CHANGE.md': ('Build the whole refund plan before applying it', '''
Compare Order.Refund with its original snapshot. The old loop found each line and immediately called line.Refund. If a later line was invalid, earlier quantities and timestamps had already changed. The new PreflightRefund loop resolves and validates every line, accumulates the amount and returns a read-only plan. Refund calls that method first, validates the provider identifier, and only then applies each planned quantity and appends the refund and timeline.

The handler performs the same pure preflight before the provider request. Duplicate line IDs are rejected before ToDictionary. A missing or unsafe restock target also rejects before the provider. Grouping restock quantities by variant ensures that multiple order lines referencing one variant cannot separately pass an overflow check and overflow when combined. Inventory.ValidateRestock and ValidateReservation expose non-mutating checks used during orchestration.

Checkout constructs and validates an order candidate before provider invocation. It checks every required inventory row before reserving any of them. The candidate's line rules reject invalid quantity, incomplete variant metadata and unsupported money precision. Customer existence, an owned cart's customer ID and cart expiry are also checked first. A late missing stock row therefore cannot leave an earlier tracked reservation behind.

IdempotencyRecord now has a nullable RequestFingerprint column. New commands persist it after success or a recorded payment failure. A matching replay returns the existing resource; a mismatch becomes a domain conflict. The additive SQL script adds the nullable column without deleting rows. Null fingerprints are intentionally not guessed from incomplete historical information.

Review the provider call in the excerpt. Every predictable validation and restock lookup should be above that boundary, and every accepted mutation below it. Then identify the remaining database-commit failure window, which ordering alone cannot remove.
''', ('src/NetShopifyLite.Application/Orders/RefundOrder.cs', '        var order = await LoadOrder', '        var payment =')),
'04-TESTING-AND-DEBUGGING.md': ('Use real persistence with a recording provider', '''
RefundPreflightTests checks pure domain behavior. A late-invalid batch must preserve all line quantities, line timestamps, order timestamp, refund collection and timeline count. Other cases reject empty, foreign, zero, negative and extreme quantities. A positive control performs a partial refund followed by the remainder and verifies that the accumulated refund amount equals the paid order total.

CommerceHandlerTests runs actual handlers with the production AppDbContext and PostgreSQL. The fixture creates unique records for every scenario. RecordingPayments counts payment and refund invocations and records the requested amount; it never contacts an external provider. Invalid batches, unsupported discounted orders and missing restock targets must leave that count at zero. Successful refund and checkout replays must keep it at one.

Replay tests change quantities, restock choice, customer, email or cart while keeping the key. Each changed request must conflict before another provider call. A legacy record with no fingerprint rejects without loading or exposing its resource. Checkout stock tests make a later cart line unavailable and verify both the tracked and persisted earlier inventory remain unchanged.

The integration fixture uses the real EF mapping rather than a portable test-only substitute. This can expose navigation-discovery, owned-value and inserted-child behavior that a repository mock would miss. The API health test also starts the application with a test connection and a non-development environment, avoiding the ordinary demo seed startup path.

These tests prove selected persistence and handler outcomes with fake provider responses. They do not prove external provider idempotency, reconciliation after network ambiguity, authenticated ownership or a browser checkout flow. Read the failed run before changing an assertion: a provider call before rejection is a production defect, while a fixture that forgot a required customer is a setup defect. Preserve a valid success case alongside negative tests.
''', ('tests/NetShopifyLite.UnitTests/RefundPreflightTests.cs', '    public void Late_invalid', '    [Fact]\n    public void Empty')),
'05-PRACTICE.md': ('Practice replay identity and failure ordering', '''
Exercise one: create a refund request with two valid line IDs in one order, then replay it with those lines reversed. Both requests should produce the same fingerprint because the handler sorts line identities before hashing. Assert a single provider call and a single persisted refund. Then change only one quantity and prove that the same key conflicts before another provider call.

Exercise two: extend the restock test with two order lines sharing one variant. Put that inventory row near the maximum supported integer value. Choose quantities that would pass separately but overflow in combination. The handler must group and validate the total before the provider. Explain why testing only one line would miss this orchestration defect even if Inventory.ValidateRestock itself were correct.

Exercise three: add a declined checkout case. Begin with sufficient inventory and a valid customer/cart. Configure the recording provider to decline. Verify the returned order is payment-failed, no reservation was made, and a replay with the same identity returns that recorded outcome without a second provider invocation. Distinguish a declined response from an exception or unknown network outcome.

Exercise four is a future design: support discounted refunds with a net allocation ledger. Define a two-decimal minor-unit conversion, deterministic remainder allocation, persistence of each line's paid allocation and a rule for successive partial quantities. Show that cumulative refunds cannot exceed paid totals regardless of line order. Include migration handling for historical discounted orders before enabling the provider path.

For each implemented exercise, identify the earliest rejection boundary and the complete set of state that must remain unchanged. Use fixture-owned databases only. Record test outcomes with their exact command, and label the discounted-refund design as a proposal until both the domain ledger and provider orchestration are implemented and tested.
''', None),
'06-SOLUTIONS-AND-REVIEW.md': ('Compare outcomes rather than merely exceptions', '''
For the reordered refund exercise, sorting line IDs before serialization produces one canonical request description. Restock remains part of that description, so changing it is a different operation. A correct replay test checks the returned order identity, provider invocation count, refund collection and quantities. It must not simply assert that a second call did not throw; an implementation could accidentally perform the refund twice and still return success.

For the shared-variant exercise, group the plan lines by VariantId and sum their quantities before resolving the restock row. Validate the aggregate against both OnHand and Available using subtraction from the integer maximum. This makes overflow rejection happen before provider invocation. The domain Restock method repeats its guard because other callers may bypass the handler. Both layers protect a distinct entry point.

For a declined checkout, the candidate order exists only in memory until the save. The handler makes no reservation until the provider returns success. On decline it records payment failure and the matching replay fingerprint, then persists the order. Replaying the same key and request should return that resource even if the cart subsequently changes; a new operation requires deliberate new identity and cannot borrow the old result.

For discounted refunds, persist the allocation used when charging rather than recomputing from mutable product prices. Allocate residual cents deterministically and track previously refunded allocated amounts. Partial quantity allocation needs a stable per-unit or cumulative policy so repeated partial refunds converge exactly to the original net amount. Historical orders without that ledger require an explicit migration or reconciliation policy. The delivered implementation currently rejects them before the provider.

A final review should inspect the external side-effect boundary. Passing these tests does not eliminate a successful provider action followed by failed database commit. A durable operation state machine, provider reconciliation and trusted customer authorization remain distinct future work. State those limits without weakening the implemented preflight and replay guarantees.
''', None),
'07-TRACE-LAB.md': ('From a rejected batch to an ambiguous provider outcome', '''
Start with a paid order containing two lines: two units at ten dollars and one unit at twenty dollars. There is no discount. Request one unit from the first line and two from the second. The handler validates the request shape, rejects no duplicate IDs, and loads the order. Preflight validates the first line without mutating it, then rejects the excessive quantity on the second. The provider count remains zero, both line quantities remain zero-refunded, and no timeline event is appended.

Now request one unit from each line and choose no restock. Preflight produces a thirty-dollar plan, bounded by the remaining paid amount. The provider returns success. The domain repeats validation, applies both quantities, appends one refund and updates financial state. The handler stores the request fingerprint and saves. A replay with identical details finds that record, matches its fingerprint and returns the order without contacting the provider again.

Change only the replay's customer-independent refund quantity or restock flag. The fingerprint no longer matches, so the handler rejects before domain or provider work. For checkout, the equivalent identity check includes cart, customer and email, preventing a key alone from returning an order belonging to a different described request. This comparison is not an authentication check; the public caller's identity still needs a trusted principal in a production design.

Finally, return to the successful provider response and make SaveChanges fail. The provider may already have moved money while the database has no committed refund or replay record. Retrying blindly is unsafe unless the provider's idempotency contract and reconciliation process resolve the earlier action. Explain why a single SaveChanges call cannot roll back that external system. This trace defines the next reliability problem without pretending the current preflight change has solved distributed atomicity.
''', None),
'VERIFICATION.md': ('Reproduction, schema upgrade and operational limits', '''
The delivered evidence records solution restore, the complete .NET test suites against an isolated PostgreSQL server and the frontend TypeScript/Vite build. Command logs and machine-readable results are retained with the project. The provider used by handler tests is a local recording fake: no real payment, refund or email is sent. Passing test counts refer to executed tests, not the number of successful commands.

Run dotnet restore with .NET 8 first. The default integration fixture uses Testcontainers. With installed PostgreSQL binaries, use scripts/test-local.py and supply --postgres-bin and --dotnet as needed. The helper creates a unique temporary cluster, listens on loopback, passes NETSHOP_TEST_SERVER to the test process and stops the owned server afterwards. The fixture creates and drops its own randomly named database. Neither path resets the application's configured database.

Existing databases need the additive scripts/add-request-fingerprint.sql upgrade before handlers use the new column. Review and apply it to the intended database through your normal migration process. It adds a nullable column and preserves all rows. Historical null fingerprints deliberately fail automatic replay and require manual reconciliation. Fresh databases created from the EF model include the column directly. Verification does not apply this upgrade to a user's existing database.

The tests cover pure refund rejection, real persisted handler results, fake-provider call counts, matching and mismatched replay, stock preflight, restock targets and application health. They do not establish external provider exactly-once behavior, network recovery, authenticated customer ownership or complete browser end-to-end checkout. Discounted refunds are rejected until a stable net allocation ledger exists.

After a provider action succeeds, database failure can still require reconciliation. Dispose the request's context after failed persistence; tracked state is not promised to rewind automatically. Use the before snapshots and source-based exercises when reviewing future changes, and regenerate evidence after edits rather than relying on old passing results.
''', None),
}
title, body, excerpt = chapters['02-CONCEPTS.md']
body += "\n\nMoney is immutable in the domain, but EF owned values still have one owner. Order discounts, line prices and payment/refund amounts copy incoming records with a record clone. This prevents a cart snapshot or order total from being reparented when another aggregate stores the same monetary value. The real PostgreSQL tests caught that distinction; arithmetic-only unit tests could not."
chapters['02-CONCEPTS.md'] = (title, body, excerpt)
nav = '\n## Course navigation\n\n' + ' / '.join(f'[{n.removesuffix(".md")}]({n})' for n in chapters) + '\n'
(P / 'astraupskill').mkdir(exist_ok=True)
for name, (title, body, excerpt) in chapters.items():
    text = '# ' + title + '\n\n' + body.strip() + '\n'
    if excerpt:
        filename, start, end = excerpt; source = (P / filename).read_text(encoding='utf-8-sig'); index = source.index(start)
        sample = source[index:source.index(end, index) if end else len(source)].rstrip()
        text += f'\n## Source excerpt\n\nFrom [{filename}](../{filename}).\n\n```csharp\n{sample}\n```\n'
    text += nav
    assert len(text.split()) >= 250, (name, len(text.split()))
    (P / 'astraupskill' / name).write_text(text, encoding='utf-8')
    print(name, len(text.split()))
p = P / 'README.md'; text = p.read_text(encoding='utf-8')
if 'astraupskill/README.md' not in text: text += '\n## Refund and checkout learning course\n\n[Start the source-based course](astraupskill/README.md) for batch preflight, request-bound idempotency and provider recovery limits. Existing databases require the additive [fingerprint column upgrade](scripts/add-request-fingerprint.sql); historical records without fingerprints fail automatic replay and require reconciliation. Discounted refunds are safely rejected until a net allocation ledger is implemented.\n\nAfter `dotnet restore`, local PostgreSQL binaries can run the complete suite with `python scripts/test-local.py --postgres-bin "C:/Program Files/PostgreSQL/18/bin" --dotnet dotnet`; the helper owns a disposable database cluster.\n'
p.write_text(text, encoding='utf-8')
