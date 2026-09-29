# .netvg (Pebl workforce quote) — fix report (B09)

## Done
- [review #1 / backlog 1.6] Corrected the `checked`/`decimal` claim. `03-WORKED-CHANGE.md` now states that `decimal` throws `OverflowException` regardless of the `checked`/`unchecked` context (which only affects integer types) and that the `try`/`catch` is what turns the throw into a `Result` failure; it also names the earlier claim as wrong. The `checked(...)` keyword was removed from `HiringQuoteCalculator.cs` and replaced by a comment stating the same thing — files: `astraupskill/03-WORKED-CHANGE.md`, `src/PeblClone.Application/Workforce/HiringQuoteCalculator.cs`.
- [review #1, sidebar] New "Sidebar: overflow and rounding are not the same lesson" in `02-CONCEPTS.md`: `int` silent wraparound vs `checked` vs `decimal` always-throws vs `double` → `Infinity`; banker's rounding vs `AwayFromZero`; and when an unreachable guard earns its place.
- [review #2] Added a genuine midpoint test: `[Theory] CalculateAsync_RoundsEmployerCostsAwayFromZeroAtAnExactMidpoint` with three exact half-cent products (`100.5*0.21=21.105`, `125.75*0.06=7.545`, `50.5*0.09=4.545`), asserting both the `AwayFromZero` value and `NotBe(<what ToEven would give>)`. Removing `MidpointRounding.AwayFromZero` now turns all three rows red. Also added `CalculateAsync_RejectsCompensationAboveTheDemoCap` — files: `tests/PeblClone.Application.Tests/HiringQuoteCalculatorTests.cs`.
  - Note: the existing `CalculateAsync_NormalizesCodesAndRoundsAwayFromZero` was kept as-is rather than converted, because it is the only test asserting trimming/upper-casing; the new theory covers the midpoint gap the review identified.
- [review #3] Dead code justified rather than deleted: both `_ =>` switch arms now throw `new ArgumentOutOfRangeException(nameof(request.EmploymentType), request.EmploymentType, "Unreachable: guarded by Enum.IsDefined above.")`, and the `catch (OverflowException)` carries a comment saying it is unreachable under the 1e12 ceiling and kept as defence in depth. `02-CONCEPTS.md` discusses the three conditions under which an unreachable guard earns its place.
- [review #4] `05-PRACTICE.md` rewritten as a task list: scenario, 8 numbered acceptance criteria, a required-checks list, plus two new **code** exercises — 5a (delete `.ToUpperInvariant()` from the currency line, run, record which assertion fails) and 5b (remove `MidpointRounding.AwayFromZero`, predict `21.10`, run the `~Midpoint` filter, restore). The step-by-step implementation prose was moved verbatim into `06-SOLUTIONS-AND-REVIEW.md` under "Exercise 5 walkthrough (moved from chapter 05)", with answer keys for 5a/5b and the lab.
- [backlog 3.4] Red-first lab added to `05-PRACTICE.md`: restore `snapshots/HiringQuoteCalculator-before.cs.txt` + `snapshots/QuoteBuilder-before.tsx.txt`, predict, run `dotnet test`, record the failures, find the mock-fallback line that fabricated a quote, restore, one sentence per failure.
- [backlog 3.5] `astraupskill/README.md`: "Before you start" with prerequisites (explicitly flagging that this project has no persistence, so it is an elective not a CRUD course), a tool/version table saying which checks each unlocks, per-chapter time estimates (3–5 h) and a 12-term glossary (EOR, contractor management, `Result<T>`, ProblemDetails, shape vs business rejection, normalization, `Enum.IsDefined`, midpoint rounding, request gate, stale response, mock fallback).
- [backlog 3.11] Inline implementation answers moved out of the practice chapter into chapter 06 (see review #4 above).
- [P1 honesty] `04-TESTING-AND-DEBUGGING.md` and `VERIFICATION.md` now separate the delivered count (14) from the current count (18) and quote the observed summary line, and the "the rounding sample is not a midpoint" sentence points at the new theory.

## Skipped
- [review #5 — mounted React test for `QuoteBuilder.tsx`] Not done. `src/PeblClone.Web` has no test runner at all (`package.json` devDependencies: vite, @vitejs/plugin-react, eslint, typescript only; the only test is a plain `node --test` harness for `RequestGate`). Adding this needs a network install of `vitest`, `@testing-library/react`, `@testing-library/jest-dom` and `jsdom`; the stage `node_modules` at `astra-remaining-improvements/stage/9e7b2d32e0fb/src/PeblClone.Web/node_modules` contains none of them, so it could not be satisfied offline. The existing limits statement ("no component was mounted") remains accurate and is not overclaimed.
- [backlog 3.8 — DB bridge] Not applicable: this project has no database, no EF Core and no persistence of any kind (the read model is in-memory static data). Stated in the README prerequisites instead.
- [backlog 3.2] Checked: no "manifest"/"baseline"/"frozen"/"root agent" language in `astraupskill/*.md`. "root-dotnet-test-02" etc. are evidence file names, explained in `VERIFICATION.md`.
- [backlog 3.3] Evidence (TRX, logs, results.json) already present under `astraupskill/evidence/` and linked.

## Verification
- `dotnet test tests/PeblClone.Application.Tests/PeblClone.Application.Tests.csproj -c Release` → `Passed!  - Failed:     0, Passed:    18, Skipped:     0, Total:    18, Duration: 1 s - PeblClone.Application.Tests.dll (net10.0)` (14 delivered + 4 added).
- Removal of `checked` and the new `ArgumentOutOfRangeException` messages compile clean under `TreatWarningsAsErrors` (the Release build above includes `PeblClone.Application`).

## Course/code consistency check
- `03-WORKED-CHANGE.md` arithmetic paragraph re-read against `HiringQuoteCalculator.cs:78-96` after removing `checked` — matches.
- `04-TESTING-AND-DEBUGGING.md` fixture inventory and `VERIFICATION.md` counts re-read against `HiringQuoteCalculatorTests.cs` — the "rounding sample is not a midpoint" caveat now points at the test that closes it, and both files distinguish 14 (delivered) from 18 (today).
- `README.md` chapter-05 description updated to match the rewritten practice chapter.

## Phase 3 addendum (glossary)

Extended the README section that already carried the prerequisites and glossary (renamed so its heading starts with `## Prerequisites`), widening the existing 12-term glossary with a "Where in this project" column instead of adding a second glossary. Every location was checked against the source before it was written: EmploymentType.cs (Contractor, PayrollOnly), Common/Result.cs, WorkforceController.cs ProblemDetails, HiringQuoteCalculator.cs (Enum.IsDefined, ToUpperInvariant, MidpointRounding.AwayFromZero, ContractorManagementAvailable), services/requestGate.ts RequestGate and services/workforceApi.ts source: mock.

## Phase 3 addendum (code blocks)

Each chapter below had no fenced code block and now carries one short section with a real excerpt from this project:

- `07-TRACE-LAB.md` — quoted from `src/PeblClone.Application/Workforce/HiringQuoteCalculator.cs:17-38` (shape gates)
