# .nettrello — fix report (B09)

## Done
- [review #1 / backlog 3.7] Converted the console harness to xUnit. New project `tests/NetTrello.Tests` (xUnit 2.9.2, Microsoft.NET.Test.Sdk 17.12.0, `net10.0`, project reference to the API) with:
  - `BoardFixture.cs` — the shared arrangement (fixed clock 2026-09-12 12:00Z, unlimited "Source" column with two cards, capacity-2 "Target" column already full, one member, in-memory repository) plus the `Describe`/`DescribeCard`/`Request`/`Element` helpers. **Each test builds its own fixture**, which removes the old harness's sequential shared state.
  - `BoardAggregateTests.cs` — 8 `[Fact]`s: three rejected `MoveCard` cases, same-column reorder at capacity, late label validation, stale `expectedVersion`, competing writes, clone isolation.
  - `CardPatchTests.cs` — title-only PATCH, explicit-null clears, full UI-shaped update, a five-row `[Theory]` of malformed bodies, and the serializer's unknown-property rejection.
  The old `tests/NetTrello.Checks/Program.cs` was **kept**, as the brief requires.
- [review #2] Replaced `tests/http-regression.ps1` with `BoardApiTests.cs`: `IClassFixture<WebApplicationFactory<Program>>`, four HTTP cases (title-only PATCH → 200 with the omitted description preserved; a two-row `[Theory]` asserting 400 + the serialized problem `code` for `{"priority":"Imaginary"}` and `{}`; `/health` → 200). No port, no `Start-Process`, no readiness loop, no PowerShell and **no `DOTNET_ROLL_FORWARD`**. The script itself was kept.
- [review #3] Added the missing assertion: `BoardFixture.Describe` now serialises `board.Version` and `board.UpdatedAt` alongside the columns and cards, so every rejected-move test proves the version and timestamp are untouched. Recorded in `VERIFICATION.md` as closing the gap the delivery admitted.
- [review #5] New "The `JsonValueKind` decision table" section in `02-CONCEPTS.md`: a six-row table (`Undefined`/`Null`/`String`/`Number`/`Array`/other) mapping each kind to the PATCH decision with a concrete example and the resulting contract code, plus the unknown-property case. Followed by "The two alternatives you will meet in the wild" — an `Optional<T>` wrapper DTO (with the converter caveat and when it is the right choice) and `JsonPatchDocument`/RFC 6902 (with when it is and is not appropriate, and a note that RFC 7396 JSON Merge Patch standardises the `null`-means-delete convention this project hand-rolls).
- [backlog 3.8] "From an in-memory board to a database" table in `02-CONCEPTS.md`: `SemaphoreSlim` → transaction + `RowVersion`/`IsRowVersion` and `DbUpdateConcurrencyException`; `expectedVersion` → 412 with `If-Match` or 409, or `ExecuteUpdateAsync` + affected rows; clone-on-read → `AsNoTracking()` and why the change tracker punishes the habit this repository protects you from; aggregate → one `SaveChangesAsync`; `Position` → column + unique index; `CardLimit` → why check-then-act still races without a transaction.
- [backlog 3.4] Red-first lab in `05-PRACTICE.md`: restore `../snapshots/Board-before.cs.txt` and `BoardDtos-before.cs.txt`, predict which of the 21 tests go red (specifically what a title-only body does to the description), run, record, compare — with an explicit note that a test you expected to fail but which passed is a gap worth finding. Plus exercises 8 (write the positive move `[Fact]` yourself, asserting `Version` increased by exactly one) and 9 (add `{"assigneeId":"not-a-guid"}` as a theory row and decide whether an unexpected code is your error or a reporting gap).
- [backlog 3.5] `astraupskill/README.md` "Before you start": prerequisites, a tool table (SDK 10.0.302; the client is optional and untested), per-chapter time estimates (4–6 h) and a 12-term glossary (PATCH vs PUT, aggregate, `JsonElement`/`JsonValueKind`, `[JsonUnmappedMemberHandling]`, `TryParse` + `IsDefined`, optimistic concurrency, clone-on-write, problem `code`, snapshot assertion, `[Fact]`/`[Theory]`/`[InlineData]`, `WebApplicationFactory<Program>`, reindexing positions).
- [backlog 3.2] Rewrote the agent-facing paragraph in `VERIFICATION.md` ("keep `bin`/`obj` out of the **manifest** … a reviewer can compare the **staged tree** … this **handoff**") into learner guidance about `.gitignore` and reading diffs with `git diff -w` / `diff --strip-trailing-cr` (which also covers backlog 2.9's advice). Changed "intended for a reviewer" to "intended for a junior engineer" in `README.md`.
- `04-TESTING-AND-DEBUGGING.md` rewritten to lead with `dotnet test`: the three test classes and what each covers, the fixture, a worked `[Fact]`, why `Describe` compares independent serialisations, the `[Theory]` rows, a four-point explanation of what the conversion bought (fail-fast masking, a real count, shared state, environment coupling), the `WebApplicationFactory` example with the two setup requirements, and the layer-first debugging guide.
- Cross-references updated in `01-CODEBASE-MAP.md`, `03-WORKED-CHANGE.md`, `06-SOLUTIONS-AND-REVIEW.md`, `README.md` and `VERIFICATION.md` so no chapter points a learner at the console harness as the primary evidence. `VERIFICATION.md` also fixes the `snapshots/` path (project root, `../snapshots/` from the chapter).

## Skipped
- [review #4 — Vitest + Testing Library test for `CardEditor` + `boardClient.updateCard`] Not done. `client/package.json` has no test script and empty `devDependencies`; there is no `node_modules` for the client in the project or in `stage/a92b3a3a2282`, so vitest/@testing-library/jsdom could not be installed offline. `VERIFICATION.md` now states explicitly that the client is source-reviewed only, and that `CompleteUpdateFromTheUi_RemainsCompatible` (which sends the shape the client builds) is indirect evidence, not execution of the client.
- [backlog 3.3] Evidence already under `astraupskill/evidence/` (`verify-03.json`, `verify-03.log`, `results.json`) and linked.
- [backlog 3.11] Checked: `05-PRACTICE.md` contains no inline answers; `06-SOLUTIONS-AND-REVIEW.md` has per-exercise solutions with code. Nothing to move.

## Verification
- `dotnet test tests/NetTrello.Tests/NetTrello.Tests.csproj -c Release` (first run) → `Failed!  - Failed:     1, Passed:    20, Skipped:     0, Total:    21` — `{"labels":["ok",4]}` returns `card.labels_invalid`, not the `card.field_invalid` the review's suggested `[InlineData]` list implied. The expectation was corrected to the code the service actually returns (verified against `BoardService`), not the other way round.
- `dotnet test tests/NetTrello.Tests/NetTrello.Tests.csproj -c Release` (after) → `Passed!  - Failed:     0, Passed:    21, Skipped:     0, Total:    21, Duration: 5 s - NetTrello.Tests.dll (net10.0)`.
- No roll-forward override was needed; the API builds as `net8.0` and is hosted in-process by the `net10.0` test assembly.

## Course/code consistency check
- `04-TESTING-AND-DEBUGGING.md` rewritten against the new suite; every quoted block is copied from a file that exists (`BoardAggregateTests.cs`, `CardPatchTests.cs`, `BoardApiTests.cs`).
- `01-CODEBASE-MAP.md`, `03-WORKED-CHANGE.md`, `06-SOLUTIONS-AND-REVIEW.md` and `README.md` re-read for links to the console harness; each now names the xUnit test that covers the same behaviour, while still acknowledging the harness exists.
- `VERIFICATION.md` reconciled: delivered evidence (`verify-03.json`, harness + script, exit code 0) is kept and labelled as the earlier run; today's `21/21` line is quoted separately.
- The `[Theory]` codes in chapter 04 and chapter 02's table were checked against the observed run (including the corrected `card.labels_invalid`).

## Phase 3 addendum (glossary)

Extended the README section that already carried the prerequisites and glossary (renamed so its heading starts with `## Prerequisites`), widening the existing 12-term glossary with a "Where in this project" column instead of adding a second glossary. Every location was checked against the source before it was written: Contracts/BoardDtos.cs (UpdateCardRequest JsonElement properties, JsonUnmappedMemberHandling, ResolveAgainst), Application/BoardService.cs MutateAsync board.version_conflict, Infrastructure/InMemoryBoardRepository.cs Clone, Middleware/ExceptionHandlingMiddleware.cs WriteProblemAsync, Domain/BoardColumn.cs RepositionCard and the three test files.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `07-TRACE-LAB.md` — quoted from `src/NetTrello.Api/Contracts/BoardDtos.cs:63-78` (`ResolveAgainst`)
