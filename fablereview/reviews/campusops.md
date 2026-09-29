# CampusOps — Fable review

- **Path:** `campusops`  ·  **Wave:** 2  ·  **Stack:** .NET 10 modular monolith (minimal API, in-memory + SQLite/EF adapters) + React/Vite/TS console  ·  **Batch:** B10
- **Astra's change (one line):** Collapsed the two-call "reserve stock, then append history" flow into a single `IPartStore.ReserveForWorkOrderAsync` contract implemented by one lock-protected store that owns both dictionaries; made all part reads/writes detached copies (`Part.Snapshot()`), rejected duplicate IDs, `Receive` overflow, non-existent work orders and post-mutation cancellation; put the inventory routes behind the existing `Operations` policy; added `GET /api/v1/parts/{id}` and a history GET; fixed the Vite dev proxy port to 5110.
- **Course size:** 5,587 words across 9 files  ·  **Tests claimed:** 42 (18 Core / 16 Infrastructure / 8 API) + 1 web test + web build  ·  **Tests found on disk:** 42 exactly (Core 16 `[Fact]` + 1 `[Theory]`×2 = 18; Infra 14 + 2 = 16; API 6 + 2 = 8)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 4.9 |

## Verdict

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The change fixes a real class of bug, not a style nit. The backup shows `PartsService.ReserveAsync` calling `parts.TryReserveAsync(...)` and then `reservations.AddAsync(...)` as two independent stores — a crash or exception between them left stock reserved with no history row. The new `ReserveForWorkOrderAsync` (`src/CampusOps.Infrastructure/Inventory/InMemoryPartsStores.cs`) validates everything, builds the updated part and the receipt, and only then publishes both under one `lock (_gate)`.
- The DI subtlety is caught *and* taught. `Program.cs:48-50` now registers the concrete `InMemoryPartStore` once and forwards both interfaces to it (`provider.GetRequiredService<InMemoryPartStore>()`); `03-WORKED-CHANGE.md` explains why: "A class implementing two interfaces does not force the dependency-injection container to share instances." That is exactly the mistake a junior makes, and it is correct about Microsoft.Extensions.DependencyInjection.
- The tests are substantive xUnit, asserting reconciled state rather than call counts. `ConcurrentReservationTests.CompetingReservations_CommitMatchingStockAndHistory` races 64 tasks against 5 units and asserts `results.Count(x => x is not null) == 5`, `history.Count == 5`, distinct receipt IDs, `history.Sum(Quantity) == stored.Reserved`, and — the good one — `Assert.Equal(5, part.Available)` to prove the caller's object is not the stored aggregate.
- Verification is unusually scrupulous: it states the *baseline* was 28 tests, that 5 new tests were first run red against the original code, and it explicitly refuses to let SQLite-in-memory count as persistence ("That is real SQLite execution, but it is not evidence that inventory is persisted"). `manualBrowserVerified: false` in the delivery JSON matches VERIFICATION.md's "optional browser inspection were not executed".
- Exercises are genuinely escalating and domain-specific: overflow boundary → terminal work-order status rule → scoped idempotency key → durable SQLite adapter with a conditional-update predicate → inventory UI capstone. Each carries an explicit "Acceptance:" contract.

## Problems found (evidence required)
- **[D7]** Exercises 3–5 (`05-PRACTICE.md`) are mid-level-to-senior in scope — designing an idempotency-key commit boundary, writing a durable EF/SQLite adapter with `UPDATE ... WHERE available >= @qty` affected-row semantics, and a full accessible React CRUD UI — with no time estimate and no intermediate step. A junior could stall for days on #4 alone.
- **[D3/D7]** `06-SOLUTIONS-AND-REVIEW.md` deliberately contains *no code* ("The goal is not to copy a finished patch"). For exercises 1–2 that is right; for #4 (durable adapter) the learner is left with a paragraph of prose and no skeleton, and there is no way to self-check.
- **[D3]** The change was verified by writing 5 tests that failed against the old code, but the course never asks the learner to reproduce that red state — the old implementation is only quoted in prose (`03-WORKED-CHANGE.md` "The old two-call pattern was conceptually:"), and unlike borrowbox there is no `snapshots/` folder of the pre-change files to check out and run against.
- **[D4, minor]** The lesson's transactionality is taught on an in-memory `lock`, not a database. The course is explicit about this ("Inventory storage remains in one process's memory"), but a junior's actual job will be `SaveChangesAsync` + EF transactions, which stay an exercise.

## Spot-checks performed
- VERIFICATION claim: "the full backend suite passed 42 tests: 18 core, 16 infrastructure, and 8 API" -> counted attributes on disk (18/16/8) and read the three TRX files in `astra-remaining-improvements/checks/campusops-final/` (`total="18" ... passed="18"`, `total="16"`, `total="8"`) -> **matches exactly**.
- Course claim: "The local web proxy now targets port 5110, matching the checked-in API launch profile" -> diffed `web/CampusOps.Web/vite.config.ts` (5000 → 5110) and read `src/CampusOps.Api/Properties/launchSettings.json:8` (`"applicationUrl": "http://localhost:5110"`) -> **matches**.
- Course claim (Exercise 2): "Review `WorkOrderStatus` ... Open, assigned, in-progress, and blocked orders remain eligible" -> read `src/CampusOps.Core/WorkOrders/WorkOrder.cs:6`: `enum WorkOrderStatus { Open, Assigned, InProgress, Blocked, Completed, Cancelled }` -> **matches**, including which two are terminal.
- Course claim: "The inventory routes require the same Operations policy as the work-order workflow" -> read `PartEndpoints.cs` (`.RequireAuthorization(SecurityPolicies.Operations)` on both groups) and `Security/SecurityPolicies.cs:8` (`public const string Operations = "Operations"`) -> **matches**.
- Course claim (Exercise 4): "Use the existing SQLite model `src/CampusOps.Infrastructure/Data/CampusOpsDbContext.cs`" -> file exists alongside `SqliteStores.cs` and `Migrations/` -> **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Ship the pre-change files as `astraupskill/snapshots/*.before.cs` (as the borrowbox course does) and add a step-0 exercise: "copy the snapshot over `InMemoryPartsStores.cs`, run `dotnet test --filter FullyQualifiedName~PartStoreIsolationTests`, and record the four failures before reading chapter 03". This turns the claimed red-then-green story into something the learner performs. (effort: S)
2. Split `05-PRACTICE.md` exercise 4 into 4a (schema + `ReserveForWorkOrderAsync` on a `CampusOpsDbContext`-backed store, with the conditional-update SQL given) and 4b (competing-connection oversell test), and give each exercise an estimated session length in the README route table. (effort: M)
3. Add a compilable skeleton for the durable adapter to `06-SOLUTIONS-AND-REVIEW.md` — the class declaration, `using var tx = await db.Database.BeginTransactionAsync()`, the `ExecuteUpdateAsync` predicate and the rows-affected branch — leaving the assertions to the learner. (effort: M)
4. Add a short chapter section mapping the in-memory `lock (_gate)` onto its EF Core equivalents (transaction isolation, `RowVersion`/`[ConcurrencyCheck]`, `DbUpdateConcurrencyException`) so the transferable lesson is explicit rather than left as an exercise. (effort: S)

## One-paragraph summary for the index
The strongest course in this batch and a model for the rest. It takes one narrow feature — reserving parts against a work order — and walks a junior from "my endpoint works" to "I own this feature's consistency, failure behavior, access control, setup and evidence." The delivered change is real: two independent stores that could disagree became one commit boundary, reads and inserts became detached copies so callers cannot mutate persisted state through a returned object, and the routes picked up the authorization policy they were missing. Every claim spot-checked against the code held, and the 42-test count matches the TRX files exactly with the baseline (28) and the deliberately-red new tests both disclosed. Its one weakness is ambition: the last three exercises (idempotency keys, a durable SQLite adapter, a full inventory UI) are large and get reasoning rather than code, so budget several sessions and expect to need outside help on the database one.
