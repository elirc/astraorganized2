# OpenSource_Upskilling_.Ramp — fix report (B10)

## Done
- [review #1 / P1 accuracy — the `BoundedChannelFullMode.Wait` claim] Rewrote the opening of `astraupskill/03-WORKED-CHANGE.md`. It no longer says the discarded `ValueTask` meant "no worker was admitted"; it now states that under `FullMode = BoundedChannelFullMode.Wait` (`BackgroundTaskQueue.cs:27-29`, capacity 100 from `Program.cs:20`) a `WriteAsync` on a full channel parks a pending writer that lands later, and names the three real defects: the lost exception, the lost back-pressure (with the unbounded pending-writer set that defeats the bound), and the wrong order.
  - Added a `## What a bounded channel actually does when it is full` section to `02-CONCEPTS.md` with a three-row `Wait` / `DropWrite` / `DropOldest`-`DropNewest` table covering both `WriteAsync` and `TryWrite`, the two consequences for reading the old code, and the "a `ValueTask` may be awaited only once" warning.
  - **Added a real test** proving it: `ExpenseWorkflowTests.Discarded_WriteAsync_on_a_full_queue_parks_and_lands_after_a_dequeue` — capacity-1 queue, `TryEnqueue` refused while full, the discarded writer's task observed incomplete, then after one `DequeueAsync` the parked item lands. Suite went 10 → 11, all green.
  - Updated every count the new test invalidated (`04-TESTING-AND-DEBUGGING.md` ×2, `README.md`, `VERIFICATION.md`, `06-SOLUTIONS-AND-REVIEW.md`, `05-PRACTICE.md`) rather than leaving the course claiming ten. VERIFICATION now says plainly that the shipped TRX records the original ten and that a local run reports eleven, and chapter 04 turns that mismatch into a lesson about checking which artifact is older.
- [review #2 / backlog 3.4] Added **Exercise 0** to `05-PRACTICE.md`: a red-first exercise that finally uses `astraupskill/snapshots/`. It first has the learner try the blunt approach (copy all five snapshots back) and read the resulting `CS1061`/`CS1501` errors as evidence that the repair changed a *contract*, then gives three behavioural reverts that keep the shape — `StartReimbursement` transition-then-fire-and-forget, `Reject` assigning the reason before the edge check, and `CanSystemTransition` losing `roles.Length == 0`. The observed result (4 failed / 7 passed of 11, each failure mapped to the edit that caused it) is quoted, plus three written questions including "re-apply edit 1 only and see which failures come back".
- [review #3] Added `## The five expense commands, end to end` to `01-CODEBASE-MAP.md`: a six-row request-path table (route → controller action with line numbers → service method → role gate → what is written → queued job) and a five-step table for the asynchronous half. It makes the point that `[Authorize(Roles = "Manager")]` answers "may a Manager call this" and never "is this *the* manager of *this* employee".
- [review #4 / backlog 3.8] Added `## Bridge: replacing the expense gate with a database` to `02-CONCEPTS.md` — six rows mapping the per-expense `lock` → `BeginTransactionAsync`, the leaking gate dictionary → nothing at all, the mutable live entity → a tracked entity invisible until commit, the absent lost-update protection → `[Timestamp] RowVersion` + `DbUpdateConcurrencyException`, `History.Add` in the lock → one `SaveChangesAsync`, and `TryEnqueue` → a transactional outbox. It ends by naming the honest limit of Astra's repair: `TryEnqueue` fixes a rejection race, not a crash between `Transition` and the job running.
  - Added **Exercise 6** to `05-PRACTICE.md` (schema with `RowVersion` and `OutboxMessage`, replacing the gate with a transaction, deciding retry-vs-409 on `DbUpdateConcurrencyException`, and an outbox poller) with an acceptance contract.
  - Added `## Known limitation: the lock dictionary grows forever` to `02-CONCEPTS.md`, documenting the leak Astra introduced *and* why the obvious fix is wrong (removing a gate on delete lets the next caller create a different gate for the same ID, so mutual exclusion silently stops working).
- [backlog 3.5] Added prerequisites, a toolchain/cross-platform note (`DOTNET_ROLL_FORWARD` in both shells), a ten-row reading route with time estimates, and a 12-term glossary to `astraupskill/README.md`.
- [backlog 3.15] macOS/Linux command forms given for every command in the new sections.

## Skipped
- [review #3, the "move ~600 words *out of* 06" half] I added the request-path table to chapter 01 (~600 words of new orientation material) but did not delete the fixture dump from `06-SOLUTIONS-AND-REVIEW.md`. The dump is accurate, is explicitly labelled as the complete executed fixture, and deleting it would remove working code a learner can run. The balance problem is addressed by making 01 bigger rather than 06 smaller. Flagging so Fable can overrule if the word ratio matters more than the content.
- [review, D2-minor: test project nested inside the API project directory] Not changed. Moving `backend/ExpenseManagement.Api.Tests/` to a sibling folder means editing two csproj files and the `<Compile Remove>` block, risking the one thing that currently works; VERIFICATION already discloses it.
- [backlog 3.2] No hits for agent-process language in `astraupskill/*.md`.
- [backlog 3.3] Already done by Astra: `astraupskill/evidence/` holds the TRX files, logs and `results.json`, and VERIFICATION links them relatively.

## Verification
- Baseline: `$env:DOTNET_ROLL_FORWARD='Major'; dotnet test backend\ExpenseManagement.Api.Tests\ExpenseManagement.Api.Tests.csproj` → `Passed! - Failed: 0, Passed: 10, Skipped: 0, Total: 10 - ExpenseManagement.Api.Tests.dll (net8.0)`.
- After adding the channel test: → `Passed! - Failed: 0, Passed: 11, Skipped: 0, Total: 11`.
- Blind restore of all five snapshots: → `error CS1061: 'BackgroundTaskQueue' does not contain a definition for 'TryEnqueue'` (×5) and `error CS1501: No overload for method 'ProcessReimbursement' takes 2 arguments`. Reverted. This is what Exercise 0 tells the learner to expect.
- Behavioural revert (the three edits now written into Exercise 0): → `Failed! - Failed: 4, Passed: 7, Skipped: 0, Total: 11`, failing `Reject_on_draft_does_not_change_reason_history_or_timestamp`, `Full_reimbursement_queue_leaves_approved_expense_unchanged`, `Throwing_reimbursement_queue_leaves_approved_expense_unchanged`, `System_transition_only_allows_marked_worker_edge`. That is the block quoted in the chapter.
- After restoring: → `Passed! - Failed: 0, Passed: 11`. Final run after all documentation edits: → `Passed! - Failed: 0, Passed: 11, Total: 11`.
- Frontend untouched, so `npm` was not run.

## Course/code consistency check
- `backend/Background/BackgroundTaskQueue.cs` — confirmed `BoundedChannelOptions` with `FullMode = BoundedChannelFullMode.Wait` at lines 27-30 and `TryEnqueue` → `_channel.Writer.TryWrite`; the corrected chapter 03 and the new chapter 02 table quote it exactly. `Program.cs:20` confirms `capacity: 100`.
- `backend/Domain/ExpenseStateMachine.cs:57-60` — `CanSystemTransition` still requires `roles.Length == 0`; Exercise 0's revert instruction restores the genuine original (`&& map.ContainsKey(to);`).
- `backend/Controllers/ExpensesController.cs` — every line number and `[Authorize(Roles = ...)]` in the new chapter-01 table was read off the file (`:47-48`, `:55-56`, `:71-72`, `:79-81`, `:88-90`, `:97-99`, class-level `[Route("api/expenses")]` and `[Authorize]`).
- `backend/Storage/DataStore.cs:23-26` — `_expenseLocks` is a `ConcurrentDictionary<Guid, object>` populated with `GetOrAdd` and never pruned, confirming the leak paragraph.
- `backend/Services/ExpenseService.cs` — `Reject` validates the reason before the lock and assigns it after the edge check; `StartReimbursement` admits before transitioning. Both match the corrected prose.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `07-TRACE-LAB.md` — quoted from `backend/Services/ExpenseService.cs:187-201` (`StartReimbursement`)
