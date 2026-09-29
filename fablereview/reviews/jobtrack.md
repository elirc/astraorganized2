# jobtrack (Daybook) — Fable review

- **Path:** `jobtrack`  ·  **Wave:** 1  ·  **Stack:** React + Vite + Vitest, host `storage` adapter  ·  **Batch:** B01
- **Astra's change (one line):** Added `src/jobBackup.js` — a versioned `{format:'daybook.jobs', version:1, applications:[]}` envelope with a full-payload validator (2 MB / 10,000-record bounds, per-field text bounds, required non-blank `id`/`company`, in-set `status`, real `YYYY-MM-DD` dates, `http`/`https`-only URLs, duplicate-id rejection), an `exportJobBackup` that re-parses its own output, and a `commitJobBackup` that validates the entire batch before a single `storage.set` — wired into `JobTracker.jsx` behind the existing write queue.
- **Course size:** 5,476 words across 9 files  ·  **Tests claimed:** 90  ·  **Tests found on disk:** 4 `it` blocks in Astra's new `test/jobBackup.test.js` (two of them `it.each` over 4 and 6 cases); the "90" is the whole pre-existing suite of 8 test files

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 4 | 5 | 4 | 4 | 4 | 3 | 4.3 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The best *code* change in B01. `parseJobBackup` (`src/jobBackup.js:5-53`) is a complete, readable runtime schema written from scratch — size bound before `JSON.parse`, envelope check, record cap, per-field length bounds, a `Set` for duplicate ids, a real date round-trip check (`date.toISOString().slice(0,10) !== value.date` rejects `2026-02-30`), and a `new URL()` protocol allowlist that blocks `javascript:`. This is precisely the "validate untrusted input at the boundary" skill the target profile asks for.
- `exportJobBackup` calls `parseJobBackup(text)` on its own output with the comment `// Never generate a backup the importer cannot restore.` — a genuinely good engineering idea (round-trip invariant enforced in production code, not only in a test) that a junior will not have seen.
- The tests assert the *absence* of writes, which is the correct oracle for "all-or-nothing import": every rejection case asserts `expect(storage.set).not.toHaveBeenCalled()`, and the success case asserts `toHaveBeenCalledExactlyOnceWith('jobtracker:data', JSON.stringify([record]))` — exactly one complete write, not a per-record loop.
- The change is actually wired into the UI, not an orphan module: `src/JobTracker.jsx:1` imports it and `:503` chains `commitJobBackup(window.storage, text)` onto the existing `writeQueue` promise, so imports serialize against other writes.
- `VERIFICATION.md` includes a "Test-run detail" section that discloses the awkward result honestly: "Full suite: 89 of 90 passed; one form test exceeded 30 seconds. Focused retry of that test passed with 120-second allowance. Harness worker startup grace extended to 300 seconds; assertions unchanged." That matches the `note` field in `implementation/checks.json` exactly. Astra did not hide it.

## Problems found (evidence required)
- **[D6]** "**Automated test cases:** 90" in `VERIFICATION.md:12` silently conflates the entire pre-existing Vitest suite (8 files: `App.test.jsx`, `Calendar.test.jsx`, `dates.test.js`, `JobTracker.test.jsx`, `smoke.test.jsx`, `storage.test.js`, …) with Astra's contribution, which is 4 `it` blocks in `test/jobBackup.test.js`. The adjacent "What was exercised" paragraph describes only 2–3 backup scenarios, so the number and the narrative disagree by an order of magnitude. Every other project in B01 reports only its own new cases (2, 3, 4), which makes 90 read as inflation.
- **[D5]** The suite is slow and partly flaky on ordinary hardware: `checks.json` records 510.8 s for the full run plus a 242.6 s focused retry, with the worker-startup grace raised to 300 s. `README.md`/chapter 4 tell the learner to run `npm test` with no warning about runtime or the 30-second default timeout, so a junior on a normal laptop will hit the same failure and assume they broke something.
- **[D8]** Batch-wide template. `02-CONCEPTS.md` shares 37 of 41 lines with the other nine courses; `05-PRACTICE.md` shares 42 of 47; `06-SOLUTIONS-AND-REVIEW.md` repeats "Review: Demonstrate an ordinary case and a case that would break a naive implementation. Explain which existing invariant remains unchanged." verbatim under all four exercises, in all ten projects.
- **[D3]** `03-WORKED-CHANGE.md`'s "Three variations to work through" names no actual variations for this project.
- **[D6, minor]** `VERIFICATION.md:20` carries the shared "Database suites ran against a fresh, separate PostgreSQL 18.1 instance" sentence in a project with no database.

## Spot-checks performed
- Course claim (`VERIFICATION.md`): "A backup with a valid Acme application followed by another record with the same id is rejected as a whole. The storage set function must not be called." -> `src/jobBackup.js:32-34` (`if (!value.id.trim() || ids.has(value.id)) fail('id is missing or duplicated.')`) and `test/jobBackup.test.js` rejects `{ id: 'a' }` on the second record while asserting `storage.set` was not called. -> **matches.**
- Course claim (`README.md` Scope / manifest): the change adds `src/jobBackup.js` and wires it in. -> `grep -n "jobBackup\|commitJobBackup" src/JobTracker.jsx` returns lines 1, 484 and 503, with `commitJobBackup` chained onto `writeQueue.current`. -> **matches** (not dead code).
- Course claim: "validated application JSON export/import with atomic replacement" (`TEN_PROJECTS_IMPLEMENTED.md` row 6). -> `commitJobBackup` (`src/jobBackup.js:59-63`) parses first, then performs exactly one `storage.set('jobtracker:data', …)`; the test asserts `toHaveBeenCalledExactlyOnceWith`. -> **matches.**
- Course claim (`VERIFICATION.md` "Test-run detail"): 89/90 plus a focused retry. -> `implementation/checks.json` stage-06 `note`: "Full suite: 89 of 90 passed; one form test exceeded 30 seconds. Focused retry of that test passed with 120-second allowance." -> **matches exactly** — this is the honest part.
- Claim under test: is "90 automated test cases" Astra's work? -> `implementation/backups/06` contains only `README.md` and `src/JobTracker.jsx`; the manifest lists `src/jobBackup.js` and `test/jobBackup.test.js` as new. `test/` holds 8 files, 7 of them pre-existing. -> **does not match** the natural reading of "Automated test cases: 90".
- Delivery claim: 5,476 words. -> `wc -w astraupskill/*` totals 5,476. -> **matches.**

## Improvements needed (ordered, concrete, actionable)
1. Split the count in `astraupskill/VERIFICATION.md:12` into two lines — "New test cases for this change: 4 (`test/jobBackup.test.js`, 2 of them parameterized over 4 and 6 inputs)" and "Full project suite run: 90 cases, 89 passed on the first run" — so the honesty document stops reading as inflation. Effort: S.
2. Add a runtime warning to `astraupskill/04-TESTING-AND-DEBUGGING.md` and the course `README.md`: the full Vitest suite takes roughly 8–10 minutes here and one `JobTracker.test.jsx` form test exceeds the 30 s default; tell the learner to run `npx vitest run test/jobBackup.test.js` for the focused loop and give the `--testTimeout=120000` escape hatch. Effort: S.
3. Add a test for the two bounds that are currently asserted only by inspection — a payload over `MAX_BACKUP_BYTES` and an `applications` array over 10,000 entries — since both are cheap to construct and both guard against a real DoS-shaped mistake. Effort: S.
4. Replace the generic "Three variations" block with the three concrete payloads the validator makes interesting: a `notes` field of 100,001 characters, a `date` of `2026-02-30`, and a `url` of `javascript:alert(1)` — each with the expected error string from `fail()`. Effort: S.
5. Strip the PostgreSQL/Recipeweb sentences from the shared environment paragraph at `VERIFICATION.md:20`. Effort: S.

## One-paragraph summary for the index
The strongest code change in this batch: a hand-written, versioned backup format for job applications where the entire payload is validated — size, envelope, record cap, field bounds, duplicate ids, real calendar dates, `http`/`https`-only URLs — before a single write happens, and where the exporter re-validates its own output so it can never emit a file its importer would reject. The tests assert that a bad record leaves `storage.set` uncalled and that a good batch produces exactly one complete write, which is the right way to prove all-or-nothing behaviour, and the module is genuinely wired into the app's write queue rather than sitting unused. Two caveats: the verification file reports "90 automated test cases" when Astra actually added four, borrowing the whole pre-existing suite's count, and that suite takes eight to ten minutes with one known timeout-prone test the course never warns you about. Do it as a core lesson on input validation and atomic writes, but run only `test/jobBackup.test.js` while you work.
