# BorrowBox — fix report (B10)

## Done
- [review #1 / backlog 3.4] Added a "Predict before you run" table (expected exception code, expected `equipment.Status`, expected store count, focused `dotnet test --filter` command per exercise) and a new **Exercise 0: make it red first** that restores `astraupskill/snapshots/Reservation-before.cs.txt` and `Loan-before.cs.txt`, records the failures and restores the fix — files: `astraupskill/05-PRACTICE.md`.
  - The exercise discloses the compile break the snapshot restore causes (the repair also changed two constructor signatures) and lists the four behaviours that must stay "old" to get a compiling red build. I performed this myself and pasted the **observed** result (5 failed / 14 passed of 19).
- [review #2] Replaced Solutions 1–2 with fixtures that are **not** the shipped tests: an `expiresAt == clock.UtcNow` equality case (asserting `error.Code == "reservation.expiry_invalid"`) and a 23:45-UTC same-day due-date checkout that must succeed. Both were compiled and run before being written into the chapter. Added a warning at the top of `05-PRACTICE.md` not to open `tests/BorrowBox.Infrastructure.Tests/` until exercises 1–4 are written, and a note in 06 explaining the fixtures differ from the repo's on purpose — files: `astraupskill/06-SOLUTIONS-AND-REVIEW.md`, `astraupskill/05-PRACTICE.md`.
- [review #3 / backlog 3.5] Added `##` sub-headings to `01-CODEBASE-MAP.md` (5) and `02-CONCEPTS.md` (7); added to `README.md` a prerequisites box, a toolchain/cross-platform note (backlog 3.15), a reading-route table with per-chapter time estimates, and a 7-term glossary (aggregate, candidate object, live reference, domain vs. workflow precondition, deterministic clock, split-brain state, validate-before-mutate).
- [review #4 / backlog 3.8] Added **Exercise 10** (port the reservation repair onto the existing `SqliteEquipmentStore`, with an acceptance contract) and **Solution 10** with a compilable arrangement skeleton; added a "Bridge: what each of these becomes against a database" section to `02-CONCEPTS.md` — a six-row table mapping live-reference reads → tracked entities/`AsNoTracking`, `SaveAsync` → `SaveChangesAsync`, two store calls → `BeginTransactionAsync`, `lock (_gate)` → the conditional `ExecuteUpdateAsync` already in `SqliteEquipmentStore.cs:38-46`, the racing fake → `RowVersion`/`DbUpdateConcurrencyException`, and no-rollback → `DbUpdateException` + unique index. It ends with the two things that do *not* translate (ordering still matters; a domain invariant is not a storage concern).
- [backlog 3.11] Solutions chapter now carries real code for exercises 0, 1, 2 and 10 rather than heuristics; no inline answers were moved *into* 05 (none existed there).

## Skipped
- [backlog 3.2] Nothing to do: `grep -nEi "manifest|baseline|frozen|root agent|stage" astraupskill/*.md` returns no hits.
- [backlog 3.3] Nothing to do: `astraupskill/evidence/` already holds the three TRX files, `results.json` and the cited run logs, and VERIFICATION.md links them relatively.
- [backlog 2.x] Wave-1 sweep items — not applicable (wave 2).
- No code change was required or made. The only source edits were the temporary red-first experiment described under Verification, which was reverted byte-for-byte.

## Verification
- `dotnet test BorrowBox.slnx --configuration Release` (before any edit) → `Passed! - Failed: 0, Passed: 6` (Core), `Passed: 19` (Infrastructure), `Passed: 4` (Api) = 29.
- Red-first experiment (reverted the four behaviours in `Reservation.cs`/`Loan.cs`, signatures kept): `dotnet test tests\BorrowBox.Infrastructure.Tests\BorrowBox.Infrastructure.Tests.csproj --configuration Release` → `Failed! - Failed: 5, Passed: 14, Skipped: 0, Total: 19`. The five: `CheckoutTests.InvalidDueDate_DoesNotCheckOutEquipment`, `CheckoutTests.ReturnBeforeCheckout_DoesNotChangeEitherEntity`, `ReservationTests.InvalidExpiry_DoesNotReserveEquipment`, `ReservationTests.Cancel_MismatchedEquipment_DoesNotChangeReservation`, `ReservationExpiryTests.ExpireDue_MismatchedEquipment_DoesNotChangeReservation`. This is the output quoted in Exercise 0 / Solution 0.
- Sources restored from a pre-experiment copy, then `dotnet test tests\BorrowBox.Infrastructure.Tests\...` → `Passed! - Failed: 0, Passed: 19`.
- The two new Solution 1–2 fixtures were put in a scratch `ZzScratchSolutionTests.cs`, run with `dotnet test ... --filter "FullyQualifiedName~ZzScratch"` → `Passed! - Failed: 0, Passed: 2`, and the scratch file was deleted.
- Final `dotnet test BorrowBox.slnx -c Release` → `Passed: 19`, `Passed: 6`, `Passed: 4` (29, unchanged).

## Course/code consistency check
- Re-read `02-CONCEPTS.md` against `src/BorrowBox.Core/Reservations/Reservation.cs:15` (`expiresAt <= reservedAt`) and `src/BorrowBox.Core/Loans/Loan.cs:13` — the new equality-boundary claims match.
- Re-read the new bridge table against `src/BorrowBox.Infrastructure/Equipment/SqliteEquipmentStore.cs` (verified `AsNoTracking()` in `GetAsync`, the `ExecuteUpdateAsync` conditional update at lines 38-46 and its `changed == 1` branch).
- Re-read `05-PRACTICE.md` Exercise 0 against `diff astraupskill/snapshots/{Reservation,Loan}-before.cs.txt` vs. the live files: the four listed "must stay old" behaviours are exactly the four hunks in that diff.
- Test names used in the `--filter` column were taken from the test sources, not invented.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 03. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **03** - src/BorrowBox.Core/Reservations/Reservation.cs (ReserveAsync)

No source code was changed; only the chapter Markdown.
