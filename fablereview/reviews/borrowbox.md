# BorrowBox — Fable review

- **Path:** `borrowbox`  ·  **Wave:** 2  ·  **Stack:** .NET 10 / minimal-API + in-memory stores (SQLite adapter present but unused)  ·  **Batch:** B10
- **Astra's change (one line):** Reordered four lifecycle workflows so the fallible domain candidate (`Reservation`/`Loan`) is constructed from a single injected-`IClock` instant *before* any equipment mutation, added missing state preconditions (`Loan.Return` rejects a pre-checkout instant; `ReturnService`/`CancelAsync`/`ExpireDueAsync` require the cooperating `EquipmentItem` to be in the matching status), and moved the return endpoint off `DateTimeOffset.UtcNow`.
- **Course size:** 4,792 words across 9 files  ·  **Tests claimed:** 29 (6 Core / 19 Infrastructure / 4 API)  ·  **Tests found on disk:** 29 (16 `[Fact]` + one 3-case `[Theory]` in Infrastructure = 19; 6 Core; 4 API), 4 new cases in `CheckoutTests.cs`, `ReservationTests.cs`, `ReservationExpiryTests.cs`

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 4 | 4 | 5 | 5 | 4 | 5 | 4.6 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The change is a genuine correctness fix, not cosmetics. Backup vs. current shows `ReservationService.ReserveAsync` used to run `equipment.Reserve()` *then* `new Reservation(...)`, so an expiry in the past left the item stuck in `Reserved` with no reservation row; checkout had the same leak (`TryCheckOutAsync` before `new Loan`). Both are inverted now (`src/BorrowBox.Core/Reservations/Reservation.cs:76`, `src/BorrowBox.Core/Loans/Loan.cs:76-78`).
- The new tests are real xUnit facts that assert *state*, not call counts: `InvalidDueDate_DoesNotCheckOutEquipment` asserts `EquipmentStatus.Available` **and** an empty active-loan list; `ExpireDue_MismatchedEquipment_DoesNotChangeReservation` asserts count 0 plus both entity statuses. Each uses a `FixedClock` record so the boundary is deterministic.
- Backward compatibility was handled honestly: `IClock? clock = null` keeps existing 3/4-arg call sites compiling, and `Program.cs:36` already registers `AddSingleton<IClock, SystemClock>()` so the ASP.NET container supplies the real clock in production. `03-WORKED-CHANGE.md` explains exactly this trade-off instead of hiding it.
- VERIFICATION.md is unusually candid: it names what the concurrency test does *not* prove ("It does not establish database serialization or borrower-limit atomicity across different equipment") and labels Exercise 9's versioned command "a design proposal, not an implemented feature".

## Problems found (evidence required)
- **[D3]** The predict step is one sentence at the end of 05-PRACTICE ("write the failure code you expect before running") rather than a per-exercise "predict → run → verify" scaffold; no exercise asks the learner to run a command and compare observed output to a prediction.
- **[D3/D7]** `06-SOLUTIONS-AND-REVIEW.md` Solution 1 is byte-identical to `tests/.../ReservationTests.cs::InvalidExpiry_DoesNotReserveEquipment`, which Astra already committed to the repo. A learner who opens the test project has the answer before the exercise. The course never warns about this.
- **[D7]** Chapters 01–04 and 07 are unbroken paragraph walls with no sub-headings, no glossary, and no time estimates; e.g. 01-CODEBASE-MAP.md is six dense paragraphs. A junior gets no reading landmarks.
- **[D4]** The lesson is about in-memory aggregate ordering; it deliberately teaches *no* EF Core, SQL, pagination, or HTTP validation surface ("No durable database transaction ... or browser test", delivery `scope`). Valuable, but narrower than the target CRUD curriculum.

## Spot-checks performed
- Course claim: "`ReservationExpiryWorker` wakes once per minute ... The worker logs only positive counts" (07-TRACE-LAB) -> read `src/BorrowBox.Api/Reservations/ReservationExpiryWorker.cs:11,17` (`PeriodicTimer(TimeSpan.FromMinutes(1))`, `if (count > 0) logger.LogInformation(...)`) -> **matches**.
- Course claim: "`POST /api/v1/reservations` ... requires an authenticated demo identity" with header `X-Demo-Role: Student` -> read `ReservationEndpoints.cs:12` and `Security/DemoHeaderAuthenticationHandler.cs:21,26` -> **matches**.
- VERIFICATION claim: "29 passed tests: six Core, nineteen Infrastructure, four API" -> counted `[Fact]`/`[Theory]` on disk (Api 4, Core 6, Infrastructure 16 facts + 3 `InlineData` cases = 19) and cross-read the TRX counters (`total="19" executed="19" passed="19"` etc.) -> **matches exactly**; no inflation.
- Course claim: "Loan due dates are calendar dates, so the constructor compares against the UTC checkout date" -> read `Loan.cs:13` (`if (dueOn < DateOnly.FromDateTime(checkedOutAt.UtcDateTime))`) -> **matches**.
- Course claim: "The API no longer supplies an uncoordinated `UtcNow`" -> diffed `LoanEndpoints.cs` against the backup; `service.ReturnAsync(id, DateTimeOffset.UtcNow, ct)` → `service.ReturnAsync(id, ct)` -> **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Add an explicit predict/observe table to `05-PRACTICE.md`: for each of the 9 exercises give a "before you run, write down: (a) the expected `BorrowBoxException` code, (b) the expected `equipment.Status`, (c) the expected store count" block, and a `dotnet test --filter "FullyQualifiedName~<TestName>"` line to run just that case. (effort: S)
2. Replace Solutions 1–2 in `06-SOLUTIONS-AND-REVIEW.md` with a *different* fixture (e.g. `expiresAt == clock.UtcNow` equality case) so the shipped repo test is not the answer key, and add a one-line note at the top of `05-PRACTICE.md` telling the learner not to open `tests/BorrowBox.Infrastructure.Tests` until they have written their own. (effort: S)
3. Add `##` sub-headings and a 5-term glossary (aggregate, candidate object, live reference, domain vs. workflow precondition, deterministic clock) to `01-CODEBASE-MAP.md` and `02-CONCEPTS.md`, plus a per-chapter time estimate in `README.md`. (effort: S)
4. Add a stretch chapter or exercise that ports one of the four repairs onto the existing `SqliteEquipmentStore` so the learner sees what changes when persistence is real (transaction scope, rollback, `SaveChangesAsync`); the course currently only names this gap. (effort: M)

## One-paragraph summary for the index
A small, honest, high-signal .NET course about one thing: *validate and construct before you mutate*. It follows a real four-workflow repair in an equipment-lending API where a bad expiry date or due date used to leave equipment stuck in `Reserved`/`CheckedOut` with no matching record, and it shows how to prove the fix with deterministic `IClock`-driven xUnit tests that assert surviving state rather than exception type alone. Everything it claims checks out against the code and the TRX evidence, and it is refreshingly clear about what it does *not* prove (no database transaction, no authz, no browser test). The weak points are pedagogical rather than factual: dense unbroken prose, no real predict-run-verify loop, and two solutions that are copies of tests already in the repo. Do this one early in a .NET track for state-machine and ordering discipline, then go elsewhere for EF Core and SQL.
