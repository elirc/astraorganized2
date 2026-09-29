from course_writer import write_course
chapters={
'README.md':('Date-only stays, safe prices and locked reviews',"""
Staybound is a booking demonstration with guest requests, host approvals, simulated payments, cancellation quotes and post-stay reviews. The completed work defines the calendar and money contracts shared by those paths and moves review eligibility into the same locked transaction as review creation and its audit.

A stay now consists of UTC calendar dates. HTTP callers send YYYY-MM-DD; internal callers may supply valid Date objects at UTC midnight. Timestamps with a time-of-day or offset are rejected instead of being silently converted using the server's local timezone. Check-out is exclusive, stays contain one through 366 nights, and seasonal rule endpoints are inclusive. These are explicit demo product choices.

The pricing engine checks integer cents, signed seasonal adjustments, effective nightly prices and cumulative totals. Percentage adjustments use exact integer arithmetic with Math.round-compatible half rounding. A malformed rule or unsafe amount fails before a booking is written. Cancellation quotes use the same UTC day model; service fees remain nonrefundable, and no policy refunds on or after the check-in date.

The existing listing advisory lock, serializable booking transactions, overlap rechecks and audit writes were useful foundations. They are preserved. Review creation now acquires that listing lock and rereads booking ownership, status and check-out before checking for an existing review. The unique booking-review index remains the last persistence guard.

Payments are still deterministic mock operations. The adapter validates positive integer amounts and required references without persisting token material. No external provider was invoked. The course distinguishes mocked transaction evidence from actual timezone child-process tests and records accepted command results in VERIFICATION.
""", [('src/lib/pricing/calendar.ts',None,80)]),
'01-CODEBASE-MAP.md':('Trace a request through the actual boundaries',"""
The common validation module exposes unrefined dateRangeFields for schemas that need to extend or partially select fields, then applies validStay at the completed boundary. This fixes the original attempt to call extend and partial on a refined ZodEffects value. createBookingSchema requires both dates and a valid guest count. Search permits either no date filter or a complete valid pair.

bookingService parses direct creation, payment and cancellation commands itself. A TypeScript annotation does not validate runtime data, and an internal caller must meet the same invariants as an HTTP route. The creation path compares check-in with utcToday, then retains the existing listing lock, published-listing lookup, capacity check and blocking-booking query before pricing and persistence.

listingService uses the search schema before querying candidate listings and calls the same pricing engine for previews. APPROVED and PAID bookings remain the blocking statuses. A REQUESTED booking is not described as a reserved date merely because it has been saved.

reviewService coordinates a separate post-stay command. Its initial transaction-scoped lookup identifies and authorizes the booking, its lock serializes listing lifecycle changes, and its second lookup supplies the facts actually used for eligibility and review creation. reviewRepository accepts the transaction client for duplicate reads and writes; auditRepository records the success in that same transaction.
""", [('src/services/reviewService.ts',None,100)]),
'02-CONCEPTS.md':('Separate calendar dates from instants and cents from floats',"""
A rental date is not a host-local midnight. If one server interprets a date in Los Angeles and another in Tokyo, host-local iteration can produce different boundaries. The completed contract stores accepted dates at UTC midnight and advances an integer number of UTC days. DST in the server timezone therefore does not change the number of nights.

Seasonal rules apply to each included night, with inclusive start and end dates. The stay itself excludes check-out. Overlapping rules add their adjustments to the original base nightly rate, rather than compounding percentages against an already adjusted rate. Each rule is validated before iteration, including rules outside the requested stay, so corrupt stored configuration is not silently ignored.

Cents must remain safe integers throughout the calculation. Percentage multiplication can overflow ordinary floating-point precision even when the final divided result would be small enough. percentageCents uses BigInt for the multiplication and rounding, then validates the converted result. Negative adjustments follow Math.round's ties-toward-positive-infinity convention; a final negative effective nightly rate is rejected.

Cancellation uses the UTC date containing the injected cancelledAt instant. FLEXIBLE refunds the refundable base at least one date before check-in; MODERATE refunds all at five days and half at one through four; STRICT refunds half at seven or more. Service fees are excluded in every case. These are the demo's written rules, not claims about an external rental platform.
""", [('src/services/cancellationService.ts',None,90)]),
'03-WORKED-CHANGE.md':('Revalidate reviews after the listing lock',"""
The original review service checked ownership, booking status, check-out and duplicate review before opening its write transaction. Those reads could become stale while another request canceled or otherwise changed the booking. Wrapping only create and audit did not make the earlier eligibility decision atomic with the write.

The completed service validates the direct command, begins a serializable transaction and looks up the booking through that transaction. It checks the actor before taking the listing lock, then rereads the booking after acquiring the lock. Ownership, listing identity, eligible PAID or COMPLETED status and elapsed check-out are checked against that second result. The duplicate read also uses the transaction client.

Review creation and audit follow only after those checks. If the audit fails, the transaction rolls back the review. A duplicate conflict is translated only for an actual Prisma P2002 error naming the bookingId target or its expected index. A different unique constraint or an ordinary error containing the word duplicate propagates unchanged.

The fixture tests record the exact order of reads, lock, duplicate check, creation and audit. They then replace booking facts at lock acquisition to demonstrate why the second read matters. This verifies real service orchestration against a transaction-aware mock; it does not establish how a live PostgreSQL scheduler interleaves two requests.
""", [('src/tests/review-workflows.test.ts','describe(',110)]),
'04-TESTING-AND-DEBUGGING.md':('Use separate evidence for time, money and transactions',"""
The pricing-boundaries suite invokes the actual pricing, cancellation, validation and mock-payment modules. Cases include impossible dates, timestamp inputs, same-day and reversed stays, excessive duration, unsafe money, malformed seasonal rules and negative effective nightly rates. The successful calculation combines percentage and fixed adjustments to verify that endpoints and rounding agree with the stated contract.

A child-process fixture runs identical calculations with TZ set to UTC, America/Los_Angeles and Asia/Tokyo. The stay crosses the March daylight-saving transition. Comparing the full serialized outputs proves the selected calculations do not depend on those host timezones, rather than merely changing a variable inside a process whose date behavior may already be initialized.

Review tests use actual service code and mocked repositories bound to a fake transaction. They simulate changed ownership, canceled state, future check-out, a different listing, existing reviews and a final audit failure. The fixture commits or restores its cloned state to make the rollback expectation explicit.

The original permission, state-transition, validation and guest-scope tests remain in the full run. The guest-query mock uses vi.hoisted so module import order cannot reference an uninitialized mock. When a check fails, distinguish a setup/import failure from a failed business assertion, retain its log, and rerun the complete affected suite after correcting the cause.
""", [('src/tests/pricing-boundaries.test.ts','describe(',90)]),
'05-PRACTICE.md':('Calendar and review exercises',"""
Exercise one: price a March 7 through March 10 stay with a 10001-cent base, a 15 percent rule covering March 8 and 9, and a negative 100-cent fixed adjustment applying only on March 8. Calculate each night before calculating the total. Include cleaning and service fees separately and explain why check-out itself receives no nightly charge.

Exercise two: submit February 30, a local timestamp with an offset, a same-day stay and a guest count of 1.5 through the real schemas. Each should fail before persistence. Then submit a complete search date pair and compare it with a search containing only check-in. Explain why a partial pair should not silently disable availability filtering.

Exercise three: cancel a booking at 23:30 UTC on the day before check-in. Compare FLEXIBLE, MODERATE and STRICT quotes, including the nonrefundable service fee. Repeat exactly on the check-in date and after it. State the UTC-date policy rather than assuming a rolling twenty-four-hour window.

Exercise four: arrange for the transaction fixture to return PAID before the listing lock and CANCELLED after it. Assert that no review or audit is created. Repeat with a different guest owner and with a future check-out date. Inspect the recorded call sequence.

Exercise five: force a bookingId unique violation at review creation, then force a unique violation for a different column. Only the known review-duplication error should become a 409. Finally explain why replacing the mock payment adapter with a real capture API requires idempotency and reconciliation beyond the existing database transaction.
""", [('src/lib/pricing/pricingEngine.ts',None,80)]),
'06-SOLUTIONS-AND-REVIEW.md':('Expected calendar, price and review outcomes',"""
The example stay has three nights. The two applicable 15 percent adjustments each round to 1500 cents, while the fixed discount removes 100 cents from only the first seasonal night. The base subtotal is 30003 cents and the seasonal total is 2900. With 50 cents cleaning and 99 cents service, the final total is 33052 cents. Rules add against the base rate and do not compound.

February 30 fails the date round-trip check. Arbitrary timestamps fail the date-only contract even if Date can parse them. Same-day and reversed stays fail validStay, and a fractional guest count fails the integer schema. A search without dates is valid, while supplying only one endpoint is rejected because the service cannot make a coherent availability decision from it.

At 23:30 UTC before check-in, the calendar difference is one. FLEXIBLE refunds the refundable base, MODERATE refunds half and STRICT refunds none. On the check-in date all three return zero. Service fees remain part of the nonrefundable amount, and exact integer rounding keeps the two amounts consistent with the accepted booking total.

A changed booking fails after the second transaction-scoped read and before duplicate lookup or creation. An audit failure after creation restores the review fixture. A typed bookingId unique violation maps to conflict, but unrelated failures retain their original meaning. Reviewers should verify those boundaries in production calls rather than accepting a test of a separate helper as proof of service wiring.
""", [('src/services/reviewService.ts','export function isDuplicateBookingReview',70)]),
'07-TRACE-LAB.md':('Trace a malformed direct booking request',"""
Begin with a guest actor and a direct call to createBookingRequest. Supply a future check-in, a later check-out and an invalid guest count such as NaN. The role guard accepts the guest role, but createBookingSchema rejects the malformed command before a transaction is opened. The test asserts that neither transaction nor repository create was called.

Now replace the guest count with a valid integer and trace the normal path in bookingService. The accepted dates are UTC-midnight Date objects. utcToday establishes whether check-in is in the past using the same calendar convention. The existing transaction and listing advisory lock precede listing, overlap and host-block checks.

Pricing uses server-owned listing amounts and rules. A corrupt stored seasonal adjustment can still fail here even though the request itself is valid. That distinction matters: request validation protects the command shape, while pricing validation protects arithmetic and stored configuration. Either failure occurs before createRequest and its success audit.

After a booking is approved, payBooking parses the token command and rechecks state and overlaps under the existing lock before invoking the mock adapter. The adapter returns a deterministic reference and timestamp metadata without raw token or token suffix. No external capture happens in this demonstration.

Finally inspect cancellation and review separately. Cancellation uses stored booking totals and an explicit instant for its quote. Review requires the stay to have ended and repeats ownership after its lock. Sharing a calendar contract does not make these different lifecycle decisions interchangeable.
""", [('src/services/bookingService.ts','  async createBookingRequest(',85)]),
'VERIFICATION.md':('Accepted checks and what they establish',"""
The accepted records below identify the complete test command, TypeScript check, Prisma generation and production build, with terminal exit codes and retained logs. The total counts actual test cases. Setup failures and failed attempts remain available separately and are not presented as successful checks.

The timezone test launches real child processes in three named timezones and compares the actual price and cancellation outputs. This demonstrates the selected UTC date calculations across a DST transition. It is not an exhaustive survey of every historical timezone rule, nor does it turn a date-only rental model into a timezone-aware check-in-time product.

Transaction tests invoke the real review service with transaction-bound repository mocks. They prove read ordering, ownership and lifecycle revalidation, narrow error translation and rollback behavior of the fixture. They do not claim that a live PostgreSQL review race or migration deployment was performed. Existing advisory locking and serializable booking transactions are preserved, not newly introduced features.

The payment adapter remains a deterministic simulation. Positive integer amounts and nonempty identifiers are validated; token material is omitted from returned persistence payloads. No external capture or refund was made. A future real provider needs an idempotent command and reconciliation design because database rollback cannot undo a completed external operation.

The new stay contract accepts YYYY-MM-DD strings or UTC-midnight Date objects, permits one through 366 nights and rejects arbitrary timestamp inputs. Cancellation thresholds are measured in UTC dates and refund nothing on or after check-in. Keep these explicit product choices with the course, original snapshots and accepted evidence when extending the application.
""", [('src/services/paymentService.ts','export const paymentService',65)]),
}
write_course('e5fa6d1a40be',chapters,'UTC date-only stays, safe integer pricing, locked review eligibility and mock-payment boundaries. See VERIFICATION for the exact commands and limits; no original database was reset.')
