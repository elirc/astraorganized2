# .netzen (SupportDesk) — fix report (B09)

## Done
- [review #1 / backlog P4 "netzen"] Closed the half-applied enum guard. `Ticket.Create` now runs `if (!Enum.IsDefined(priority)) throw new DomainException("Ticket priority is not supported.");` after the required-field guards and before the two SLA switches, with a comment explaining why a JSON body can deliver `(TicketPriority)99`. Added `TicketSafetyTests.Create_RejectsUndefinedPriority` asserting the exact message — files: `support-ticketing-app/backend/SupportDesk.Api/Domain/Ticket.cs`, `support-ticketing-app/backend/SupportDesk.Api.Tests/TicketSafetyTests.cs`.
- [review #2 / backlog 3.8] New "Pushing authorization into the query (what this code should become)" section in `02-CONCEPTS.md`: the in-memory loop set beside a real EF Core `IQueryable` — ownership predicate first, user filters second, `CountAsync()` and `Skip/Take` on the *same* query, projection inside the query — plus the three bug classes the loop hides, and a table mapping every in-memory mechanism here (`_writeLock`, `expectedVersion`, `Snapshot()`, seed load, tag replacement) to its relational equivalent (`RowVersion`/`IsConcurrencyToken`, `DbUpdateConcurrencyException` → 409/412, `ExecuteUpdateAsync` + affected rows, one `SaveChangesAsync` transaction, join table / `ON CONFLICT`).
- [review #3] Fixed the hub-connection churn. `App.tsx` now keeps `filtersRef`/`selectedIdRef` updated during render, the SignalR `useEffect` dependency list is `[]` (one connection per mount), the changed-callback reads `selectedIdRef.current`, and `refreshTickets` reads `filtersRef.current` so the copy captured by the long-lived callback still sends current filters. Added "Why the hub connection is created once (and reads state through refs)" to `07-TRACE-LAB.md` — the general rule, the two failure modes, and what refs do *not* fix — and corrected the earlier trace paragraph that described the old teardown-per-filter-change behaviour.
- [review #5 / backlog 3.11] `05-PRACTICE.md` rewritten: scenario + 7 acceptance criteria + four exercises (5a predict the request-number timeline; 5b instrument the hub effect with `[selectedId, filters]` vs `[]` and count connect/stop pairs; 5c revert `ReplaceTags` to the lazy `AddRange` form and predict which assertion fails first; 5d delete the new `Create` guard and read the due dates a priority-99 ticket gets). The step-by-step implementation narration was moved verbatim into `06-SOLUTIONS-AND-REVIEW.md` as "Exercise 5 walkthrough (moved from chapter 05)", with answers for 5a–5d.
- [backlog 3.4] Red-first lab added to `05-PRACTICE.md`: restore the pre-change one-source-page-then-filter `SearchTicketsHandler` shape, predict `Total`/`Items.Count` against the 121-ticket fixture, run, record the message, restore. Answer included in chapter 06.
- [backlog 3.5] `astraupskill/README.md` "Before you start": prerequisites, tool table naming what each unlocks (including the `DOTNET_ROLL_FORWARD=Major` requirement and the explicit "there is no frontend test runner"), per-chapter time estimates (4–6 h) and a 14-term glossary (aggregate, invariant, optimistic concurrency/`expectedVersion`, snapshot, materialise, deferred execution, page vs source page, authorization-before-pagination, projection/DTO, hub/group, data-free invalidation, stale response, ref, draft state).
- [P1 honesty] `README.md` and `VERIFICATION.md` now separate the delivered 3-test count from today's 4, quote the observed summary line, and record that the frontend change was type-checked only.
- [03-WORKED-CHANGE] Two "Follow-up" sections added documenting both code changes (the missing creation guard and the hub-connection lifetime), so the chapter matches the code.

## Skipped
- [review #4 — frontend test runner + three Vitest tests] Not done. `support-ticketing-app/frontend/package.json` has no test runner and no test script; vitest, @testing-library/react and jsdom are absent from the stage `node_modules` (`astra-remaining-improvements/stage/1bb35a95be79/.../frontend/node_modules`, 61 packages), so this could not be satisfied offline. It needs a network install plus a `vitest.config.ts`. The limits already state the frontend is untested and I strengthened that statement rather than weakening it.
- [backlog 3.7] Not applicable: the project already has a real xUnit project (`SupportDesk.Api.Tests`) run by `dotnet test`; there is no console harness.
- [backlog 3.2] Checked `grep -n "manifest|baseline|frozen|root agent|stage"` over `astraupskill/*.md` — nothing to rewrite (`root-dotnet-test-01` etc. are evidence file names, explained in `VERIFICATION.md`).
- [backlog 3.3] Evidence already under `astraupskill/evidence/`.

## Verification
- `DOTNET_ROLL_FORWARD=Major dotnet test support-ticketing-app/backend/SupportDesk.Api.Tests/SupportDesk.Api.Tests.csproj -c Release` → `Passed!  - Failed:     0, Passed:     4, Skipped:     0, Total:     4, Duration: 1 s - SupportDesk.Api.Tests.dll (net8.0)` (3 delivered + 1 added).
- Without the roll-forward the same command aborts: "Testhost process ... exited with error: You must install or update .NET to run this application ... version '8.0.0'". Documented in README/VERIFICATION.
- `npx tsc --noEmit -p tsconfig.json` in `support-ticketing-app/frontend` → exit code 0, after copying `node_modules` from the stage folder. The copied `node_modules` was deleted afterwards (the project had none before); verified absent.

## Course/code consistency check
- `07-TRACE-LAB.md` browser-trace paragraph re-read against the new `App.tsx` hub effect — the "cleanup stops the old connection when filters change" sentence was wrong after the fix and has been rewritten.
- `05-PRACTICE.md` third task paragraph (which described the `[selectedId, filters]` dependency list as correct) moved to chapter 06 with an explicit note that the effect has since changed and why.
- `03-WORKED-CHANGE.md` now covers both code changes; `README.md` and `VERIFICATION.md` test counts reconciled (3 delivered / 4 today).

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (aggregate, invariant guard, expected version, concurrency conflict, deferred execution, permission policy, source page, authorization before pagination, data-free invalidation, group membership, stale response guard, draft state), replacing the older prerequisites paragraph and untyped glossary in `## Before you start` so nothing is duplicated. Verified every term against the source before citing it: the files `support-ticketing-app/backend/SupportDesk.Api/Domain/Ticket.cs`, `Domain/Ticket.cs`, `Infrastructure/InMemoryTicketStore.cs`, `03-WORKED-CHANGE.md`, `Application/Permissions.cs`, `Application/Queries/SearchTickets.cs`, `SearchTickets.cs`, `Realtime/SignalRTicketNotifier.cs`, `Realtime/TicketHub.cs`, `frontend/src/App.tsx`, and the symbols and identifiers `Ticket`, `Ticket.Create`, `UpdatePriority`, `expectedVersion`, `UpdateAsync`, `ConcurrencyException`, `Ticket.ReplaceTags`, `Permissions.CanReadTicket`, `sourcePage`, `CanReadTicket`, `Skip`, `Take`, `SendAsync("tickets.changed", ...)`, `JoinInbox`, `listRequest`, `commentBody`, `tagDraft`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 06. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **06** - support-ticketing-app/backend/SupportDesk.Api/Domain/Ticket.cs (ReplaceTags)

No source code was changed; only the chapter Markdown.
