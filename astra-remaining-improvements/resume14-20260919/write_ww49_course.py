from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/e7862246212d'
chapters={
'README.md':('Atomic commerce demo workflows',"""
This marketplace demo creates orders from server-owned product prices, applies coupons, separates refund approval from execution, and tracks warehouse progress. The completed change strengthens the points where those workflows modify several related records. Creating an order now commits the order, coupon usage and audit together. Executing a refund commits the financial balance, refund lifecycle and audit together. Failure restores the complete previous in-memory graph.

The original fulfillment mapper replaced the order status with SHIPPED or DELIVERED even after a refund. The completed mapper gives financial refund history priority in the legacy status field while fulfillmentStatus continues to describe logistics. A partially refunded order may move through shipping without losing PARTIALLY_REFUNDED. A fully refunded unshipped order cannot advance toward shipment; an already shipped package can still be recorded as delivered. Cancellation preserves the financial summary too.

Direct service inputs now pass through runtime parsers, so an internal caller cannot bypass quantity, line-list, refund amount or reason rules simply by avoiding the route. Integer money helpers reject unsafe values and arithmetic overflow. Duplicate products are rejected explicitly instead of depending on the product repository's returned row count. Inputs and returned records are cloned at the transaction boundary.

This is a synchronous, process-local teaching store. It is not a SQL transaction, a durable payment ledger, a real payment capture, or a multi-worker coordination mechanism. Existing simulated paymentCaptured data remains simulated. Read the source excerpts, follow the rollback trace, and compare the accepted test evidence with those limits before adapting this design to a real commerce backend.
""",'src/lib/order-status.ts',None,80),
'01-CODEBASE-MAP.md':('Follow commands through validation, services and repositories',"""
Start in src/lib/validation/orderSchemas.ts. parseCreateOrderInput constructs a normalized command with a bounded nonempty item list, unique product IDs, valid quantities and a complete address. The order service invokes this parser itself before consulting users, products or coupons. The HTTP route remains a convenience boundary; the service owns the invariant for every caller.

orderService.ts builds item snapshots from productsRepository, calculates line totals through multiplyCents and combines amounts through sumCents. couponService.ts validates stored coupon configuration before applying its existing eligibility rules. Order creation stores a snapshot of the accepted discount, so later coupon changes do not rewrite historical prices.

refundService.ts owns request, approval and execution. Execution rereads the current refundable balance, validates the stored approved amount, and rejects a second execution. fulfillmentService.ts validates the logistics transition and calls orderStatusFor to preserve financial history. OrderActionPanel displays actions compatible with these rules, including hiding new refund requests when no refundable balance remains.

The repositories all resolve getStore at call time. withStoreTransaction temporarily exposes a cloned graph to those actual repositories; success keeps that graph, while failure restores its predecessor. That wiring is why the service tests exercise real repository mutations instead of merely testing a separate rollback helper.
""",'src/services/orderService.ts','  createOrder(',100),
'02-CONCEPTS.md':('Money, history and two independent state dimensions',"""
Amounts are integer cents. A number being finite is insufficient: a fractional cent is malformed, and a value beyond JavaScript's safe-integer range can lose precision before it reaches a ledger. assertCents validates the operands, multiplyCents validates quantity and the resulting product, and sumCents validates every intermediate total. A large positive input can therefore fail even when each individual field initially looks plausible.

Percentage coupons use exact integer multiplication through BigInt and integer division. The established coupon behavior floors the calculated discount. Coupon configuration is checked for known type, positive amount, valid percentage bound and safe counters before the discount is calculated. This prevents a corrupt stored coupon from creating a negative or imprecise order total.

Financial and logistics facts answer different questions. Refunded money does not become unrefunded when a warehouse ships a package. The legacy status field prioritizes REFUNDED or PARTIALLY_REFUNDED whenever refundedCents is positive, while fulfillmentStatus preserves PICKING, PACKED, SHIPPED, DELIVERED or CANCELED. Both are displayed in the order list.

This model deliberately retains the existing status fields instead of inventing a new database. A production design could introduce a separate payment-status enum, but it must migrate historical readers and reporting together. The current change establishes consistent behavior within the existing demo contract.
""",'src/lib/money.ts',None,100),
'03-WORKED-CHANGE.md':('Make refund execution one unit of work',"""
Consider an approved refund whose remaining order balance is still sufficient. The old service updated the order, updated the refund and finally appended an audit. If that final step threw, the earlier mutations remained visible. A caller could see an error while the demo ledger had already changed, and a retry could encounter a confusing terminal refund.

The completed executeRefund runs inside withStoreTransaction. Permission and status checks happen against the current graph. It validates the stored approved amount as positive safe integer cents and verifies paymentCaptured before comparing the amount with the freshly calculated balance. Approval does not reserve money: another approved refund may consume the balance first, so execution must check again.

Only after all preflight checks does the service construct the updated order and EXECUTED refund. Repository writes and the audit use the same cloned working graph. If any operation throws, the transaction helper restores the predecessor. If all operations succeed, the returned refund is cloned so a caller cannot mutate committed state by holding its result.

The test deliberately fails the final audit after both repository writes have occurred. It checks the full store snapshot, not just the refund status. That proves the actual orchestrated demo workflow restores financial totals, refund history and audits together.
""",'src/services/refundService.ts','  executeRefund(',100),
'04-TESTING-AND-DEBUGGING.md':('Test the real demo store and late failures',"""
The commerce-workflows suite resets the seeded store before each scenario and calls the actual order, refund and fulfillment services. It covers malformed direct commands, duplicate products, empty item lists, unsafe arithmetic, corrupt coupon configuration, valid server pricing, input cloning and result cloning. Those cases verify that validation happens at the service boundary as well as at the route.

Rollback cases inject a failure only when the expected earlier mutation has already happened. The order scenario checks that an order and coupon usage have changed before failing the audit. The refund scenario checks both financial and refund records before failing. Afterward, the complete graph must equal its original snapshot. A preflight-only failure would not exercise the same boundary.

Lifecycle cases follow partial refunds through shipment and delivery, apply the remaining refund, reject further shipment, and preserve the financial summary during cancellation. Another case records delivery after a fully refunded package was already shipped. Competing approved refunds are executed sequentially against the changing balance to show that the second cannot overspend it.

The package test command now includes every src/tests/*.test.ts file, keeping the original permission and schema tests in the same run. Passing these checks establishes behavior of this in-memory implementation. It does not prove database isolation, browser interaction, durability after restart or external payment idempotency.
""",'src/tests/commerce-workflows.test.ts',None,85),
'05-PRACTICE.md':('Review a refund and shipment sequence',"""
Exercise one: begin with seeded order_1001, record its total and fulfillment status, and request a refund for a positive amount below the total. Use the customer actor for the request and the permitted approval and execution roles for the later steps. Explain why request, approval and execution remain separate actions even though the store is in memory.

Exercise two: after executing that partial refund, advance the package from PACKED to SHIPPED and then DELIVERED. Predict both status fields before running the commands. Identify the single function that preserves the financial summary, and explain why updating only the legacy status would misrepresent the refund.

Exercise three: reset the store, refund the entire unshipped order and attempt to ship it. The service should reject the transition. Cancel it through the authorized cancellation path, then repeat cancellation. Compare timestamps and audit counts to confirm that the retry is stable while the refund summary remains intact.

Exercise four: create two approved refunds whose combined amounts exceed the remaining balance. Execute the first, then the second. The second must fail using the refreshed balance without changing either its own status or the order total. Approval is not a reservation of funds.

Exercise five: inject a failure at the final refund audit after both writes have occurred. Compare every store collection with the before snapshot. Finally describe what would change if the transaction callback awaited a network provider. Explain why a SQL rollback or a cloned JavaScript object cannot reverse an external payment that has already succeeded.
""",'src/lib/demo/store.ts','// A demo-only unit of work.',80),
'06-SOLUTIONS-AND-REVIEW.md':('Expected histories and failure outcomes',"""
After a partial refund, status remains PARTIALLY_REFUNDED as fulfillmentStatus advances from PACKED through SHIPPED to DELIVERED. The financial total is unchanged by warehouse actions. orderStatusFor validates total and refunded cents before choosing the financial summary, so a corrupt history with refundedCents greater than totalCents cannot be silently displayed as a normal shipment.

A fully refunded unshipped order cannot advance toward shipment. Cancellation remains permitted through the order cancellation service and changes fulfillmentStatus to CANCELED while retaining REFUNDED. A repeat cancellation returns the saved order without replacing its timestamp or adding another audit. Already shipped orders cannot be canceled, but delivery may still be recorded after a full refund because that shipment already exists.

For two approved refunds, the first execution reduces the current balance. The second must compare its stored amount with that new balance. A failed second execution remains approved; it does not become executed, reduce money again or append a success audit. A previously executed refund also rejects repetition through its terminal-state check.

The rollback exercise succeeds only if the injected failure occurs after the intended writes. Checking a flag that observed those mutations prevents an accidentally early failure from giving false confidence. The final complete-state equality assertion catches coupon, financial or audit leftovers that a narrow status assertion would miss.

Review the helper's synchronous restriction before reusing it. Production payment processing needs durable commands, provider idempotency and reconciliation. This delivery introduces none of those external guarantees and calls no payment provider.
""",'src/services/fulfillmentService.ts','const allowedTransitions',95),
'07-TRACE-LAB.md':('Trace an order creation that fails at audit',"""
Start with a valid operations actor, a customer, a keyboard and mouse, and the LAUNCH15 coupon. The service parses the command and verifies the customer account. Product records supply prices; the request supplies only product IDs and quantities. The calculated line amounts and subtotal pass safe-integer checks before coupon evaluation.

The coupon service verifies active status, usage limit, minimum subtotal and product eligibility using the existing policy. The completed validation additionally rejects malformed stored amounts and counters. The discount snapshot is copied into the new order and used to calculate its total. The shipping address is cloned so later caller edits cannot rewrite history.

Inside the working graph, the repository inserts the order and increments the coupon's usage. Now force the final audit operation to fail. withStoreTransaction catches the error, restores the original global graph and rethrows. The caller sees failure, but no new order, coupon increment or success audit remains.

Repeat without the injected failure. The working graph remains committed and the result is cloned before being returned. Modify the returned address and inspect the repository again: the stored address must remain unchanged. This trace demonstrates both atomicity and ownership of mutable data at the actual service boundary.

Inspect the test implementation for its late-failure condition. The important evidence is that the order and coupon changes happened before the throw, followed by equality of the entire restored graph. That is the scenario the original sequential writes could not satisfy.
""",'src/services/orderService.ts','    ordersRepository.create(order);',32),
'VERIFICATION.md':('Accepted checks and explicit demo limits',"""
The accepted records below identify commands, terminal exit codes and logs. The test total comes from Node's test-runner summary, including both the original tests and the new commerce workflow suite. A launched or still-running command is not counted as passing. Type checks and the production build verify the final source, including the action panel changes that follow the service rules.

The regressions exercise real services and real in-memory repositories. Fault injection demonstrates rollback after order and coupon writes, refund and financial writes, fulfillment transitions and cancellation. Additional cases cover safe money arithmetic, duplicate lines, direct runtime validation, role and ownership checks, stable cancellation retries and preservation of refund history during logistics changes.

The new unit of work is synchronous and process-local. Its state disappears on restart and is not shared between independent server workers. The helper rejects a returned promise; it is not an asynchronous transaction abstraction. All existing paymentCaptured values and refund execution remain a simulation. No provider was called, no money moved and no original database was reset.

The UI now hides invalid cancellation, fulfillment and refund actions according to the current order data. Server validation remains authoritative when a page is stale or a caller bypasses the browser. The verification does not claim a browser end-to-end run or visual comparison.

Exact original snapshots accompany changed baseline files. Keep those snapshots and the evidence with the course so a reviewer can compare the before behavior, the implementation and the actual accepted checks. Replace the evidence after any later code changes rather than treating these results as permanent certification.
""",'src/lib/order-status.ts',None,80),
}
nav='\n## Course navigation\n\n'+' / '.join(f'[{n.removesuffix(".md")}]({n})' for n in chapters)+'\n'
(P/'astraupskill').mkdir(exist_ok=True)
for name,(title,body,file,anchor,count) in chapters.items():
 source=(P/file).read_text(encoding='utf8');source=source[source.index(anchor):] if anchor else source;sample='\n'.join(source.splitlines()[:count])
 text='# '+title+'\n\n'+body.strip()+f'\n\n## Source excerpt\n\nFrom [{file}](../{file}).\n\n```ts\n{sample}\n```\n'+nav
 assert len(text.split())>=250,(name,len(text.split()));(P/'astraupskill'/name).write_text(text,encoding='utf8');print(name,len(text.split()))
f=P/'README.md';s=f.read_text(encoding='utf8')
if 'astraupskill/README.md' not in s:s+='\n## Commerce workflow course\n\n[Start the source-based course](astraupskill/README.md): safe integer prices, atomic demo order/refund writes, financial history during fulfillment, exercises, exact snapshots and accepted verification. This store remains process-local and payments remain simulated.\n'
f.write_text(s,encoding='utf8')
