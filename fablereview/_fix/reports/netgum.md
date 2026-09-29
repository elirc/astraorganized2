# .netgum — fix report (B09)

## Done
- [review #1 / backlog 1.13] Disclosed the silently repaired compile error. New "Prerequisite repair: the baseline did not compile" section at the top of `astraupskill/03-WORKED-CHANGE.md` quotes `snapshots/EmailAddress-before.cs.txt:27-30` (`throw new DomainException(...) from ex;`), states that this is Python syntax C# rejects, and that the baseline therefore did not build — files: `astraupskill/03-WORKED-CHANGE.md`.
- [review #2] Fixed the inner-exception loss. Added `DomainException(string, Exception)` ctor and changed `EmailAddress.Create` to `throw new DomainException("Email address is not valid.", ex);`. Added a "Exceptions carry a cause" section to `02-CONCEPTS.md` — files: `src/Netgum.Domain/Abstractions/DomainException.cs`, `src/Netgum.Domain/ValueObjects/EmailAddress.cs`, `astraupskill/02-CONCEPTS.md`.
- [review #2, regression test] New `tests/Netgum.Tests/Domain/EmailAddressTests.cs` (3 cases: normalisation, blank address has no inner exception, invalid address preserves `FormatException` as `InnerException`).
- [review #3] Added `global.json` pinning SDK `10.0.302` (`rollForward: latestFeature`); `VERIFICATION.md` now separates the SDK pin from the net8.0 *runtime* requirement, names `DOTNET_ROLL_FORWARD=Major` as the fallback rather than the happy path, and explains that the `cwd` in the evidence JSON is Astra's staging directory, not a path the learner needs.
- [review #4] `05-PRACTICE.md`: exercises 1 and 4 are now predict-then-run with a five-row prediction table (`payments.CreateCalls`, `coupon.RedeemedCount`, `StockQuantity`, `Orders.Count()`, `emails.SentCount`); added **Lab A** (move `ReserveInventory` back above `Order.CreatePending`, predict which tests go red, run, restore).
- [review #5] `CompleteOrderAsync` no longer queries the product on the Failed early-return path: the `PaymentStatus.Failed` check now precedes `_products.GetByIdAsync`. Chapter 03's completion paragraph was rewritten to describe the new read ordering — files: `src/Netgum.Application/Checkout/CheckoutService.cs`, `astraupskill/03-WORKED-CHANGE.md`.
- [backlog 3.4] Red-first exercise added as **Lab B** in `05-PRACTICE.md`: restore `snapshots/CheckoutService-before.cs.txt` + `snapshots/EmailAddress-before.cs.txt`, observe the compile error first, repair only that line, run the focused filter, record the failures, restore.
- [backlog 3.5] `astraupskill/README.md` gained a "Before you start" block: prerequisites, a tool/version table, per-chapter time estimates (6–8 h total) and a 11-term glossary (aggregate, layering, preflight, payment intent, change tracking, unit of work, counting double, idempotent, terminal state, EF InMemory, optimistic concurrency). `04-TESTING-AND-DEBUGGING.md` gained a "What you need installed" block.
- [backlog 3.8] "From EF InMemory to a real database" section in `02-CONCEPTS.md`: `SaveChangesAsync`-as-transaction vs. `BeginTransactionAsync`, conditional `ExecuteUpdateAsync` + affected-row count for stock, `[Timestamp]`/`IsRowVersion` + `DbUpdateConcurrencyException` → 409/412, unique index + `DbUpdateException` for idempotency.

## Skipped
- [backlog 3.7 xUnit conversion] Not applicable: this project already ships a real xUnit + FluentAssertions project (`tests/Netgum.Tests`) run by `dotnet test`. No console harness exists.
- [backlog 3.2] Checked: `grep -n "manifest|baseline|frozen|root agent|stage" astraupskill/*.md` returns only one benign use of "frozen" ("product names are not frozen on the order") — no agent-process language to remove.
- [backlog 3.3] Evidence already lives in `astraupskill/evidence/` (TRX, logs, results.json) and is linked from `VERIFICATION.md`.
- [backlog 3.11] Checked: `05-PRACTICE.md` has no inline answers and `06-SOLUTIONS-AND-REVIEW.md` is 362 lines of per-exercise worked solutions with fixtures and call-count assertions. Nothing to move.

## Verification
- `dotnet test Netgum.sln --configuration Release` (no roll-forward) → **Test Run Aborted**: "Testhost process ... exited with error: You must install or update .NET to run this application. Framework: 'Microsoft.NETCore.App', version '8.0.0'". Only 10.0.10 is installed. This confirms the runtime caveat now documented in `VERIFICATION.md`.
- `DOTNET_ROLL_FORWARD=Major dotnet test Netgum.sln --configuration Release --no-build` → `Passed!  - Failed:     0, Passed:    14, Skipped:     0, Total:    14, Duration: 13 s - Netgum.Tests.dll (net8.0)` (11 delivered + 3 added).

## Course/code consistency check
- `03-WORKED-CHANGE.md` completion paragraph re-read against `CheckoutService.cs:95-115` after the read reorder — now matches.
- `02-CONCEPTS.md` terminal-completion paragraph ("the service loads the product name for a paid receipt") still true: the load stays above the Paid check, only below the Failed check.
- `VERIFICATION.md` test count reconciled: 11 delivered (evidence) vs 14 observed today, both stated with which is which.
- `README.md` chapter-05 description updated to mention the two new labs.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (aggregate, preflight validation, reservation check, payment intent, captured clock value, tracked entity, unit of work, terminal state, idempotent completion, receipt, coupon redemption, counting double), moving the older prerequisites paragraph and untyped glossary out of `## Before you start` so nothing is duplicated. Verified every term against the source before citing it: the files `src/Netgum.Domain/Products/Product.cs`, `src/Netgum.Domain/Orders/Order.cs`, `src/Netgum.Domain`, `src/Netgum.Domain/Products/ProductVariant.cs`, `src/Netgum.Application/Checkout/CheckoutService.cs`, `src/Netgum.Infrastructure/Persistence/NetgumDbContext.cs`, `src/Netgum.Application/Abstractions/IUnitOfWork.cs`, `src/Netgum.Domain/Orders/PaymentStatus.cs`, `CheckoutService.cs`, `src/Netgum.Application/Checkout/CheckoutContracts.cs`, `src/Netgum.Domain/Products/Coupon.cs`, `tests/Netgum.Tests/Application/CheckoutServiceTests.cs`, and the symbols and identifiers `Product`, `Order`, `Product.ValidatePurchase`, `Order.ValidateCustomer`, `ProductVariant.ValidateReservation`, `CreatePaymentIntentAsync`, `var now = _clock.UtcNow;`, `CheckoutService.CreateSessionAsync`, `NetgumDbContext`, `IUnitOfWork`, `Paid`, `Failed`, `CompleteOrderAsync`, `OrderReceiptResponse`, `Coupon.MarkRedeemed`, `CountingPaymentGateway`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 04. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **04** - tests/Netgum.Tests/Application/CheckoutServiceTests.cs (InvalidCustomerInput_DoesNotCallGatewayOrReserve)

No source code was changed; only the chapter Markdown.
