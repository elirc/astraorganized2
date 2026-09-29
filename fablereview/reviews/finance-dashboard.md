# finance-dashboard — Fable review

- **Path:** `finance-dashboard`  ·  **Wave:** 1  ·  **Stack:** vanilla JS + localStorage, `<dialog>` modal (jsdom tests)  ·  **Batch:** B01
- **Astra's change (one line):** Added an expense *edit* mode to the existing entry modal — `editExpense(id)` prefills and locks the entry type, and `handleEntrySubmit` validates the amount/date/description, replaces the matching record by `id` via `map` into a new state object, writes to localStorage first and only publishes state on success, keeping the modal open with an error otherwise.
- **Course size:** 5,132 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 (`test/expense-edit.test.cjs`, plus harness `test/browser.cjs`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 4 | 4 | 5 | 4 | 4 | 3 | 4.1 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- This is the clearest "U in CRUD" lesson in the browser half of the batch. `handleEntrySubmit` (`app.js:205-218`) builds `updated = { ...existing, ...entry, id: existing.id, category: ... }` and a whole replacement state `next`, writes `next` to storage inside a `try`, and only then assigns `state = next`. The forced `id: existing.id` is the exact defence against "edit silently creates a duplicate", and the course names that risk directly: "A new id on edit would turn an update into an accidental duplicate".
- The second test is a good failure lab: it loops `['-1','0','1.001']` through the real submit event and asserts the *stored* amount is still `10` each time, then patches `Storage.prototype.setItem` to throw and asserts three things at once — `state.expenses[0].amount === 10`, `#entryModal.open === true`, and the error text matches `/Could not save/`. Keeping the editor open on failure is a genuinely good UX invariant to teach.
- Derived totals are asserted, not just the row: `assert.match(app.document.querySelector('#expenseKpi').textContent, /12.50/)` proves the KPI is computed from state rather than kept as a second mutable fact.
- `02-CONCEPTS.md` is honest about the money model: "Amounts remain JavaScript numbers in this educational app; validation limits decimal places, but robust financial systems commonly use integer minor units."

## Problems found (evidence required)
- **[D2]** The change is deliberately one-sided and the course only half-admits it. The edit path is validate → persist → publish; the *create* path immediately below it still mutates in place (`app.js:221-223`, `state.expenses.push({ ...entry, ... })`) and relies on the unguarded `saveState()` at `app.js:186-188`. A learner following the course's own rule will find two contradictory patterns 15 lines apart. `02-CONCEPTS.md` hand-waves this as "Existing add and other dashboard workflows have their own behavior" rather than stating it as a known defect with a suggested fix.
- **[D2]** `validateEntry` is applied to all entry types, but only expenses got the edit path. Bills, incomes, goals and investments remain uneditable and untested, so "validated editing with stable record identity" is a single-entity lesson sold with a dashboard-wide title.
- **[D8]** `02-CONCEPTS.md` shares 37 of 41 lines with the other nine B01 courses (only the "central idea" heading, the domain paragraph, the invariant quote and the data-model sentence are substituted). `05-PRACTICE.md` and `06-SOLUTIONS-AND-REVIEW.md` reuse the same per-exercise scaffolding sentences verbatim across the batch.
- **[D3]** `03-WORKED-CHANGE.md`'s "Three variations to work through" gives no actual variations for this project.
- **[D6]** `VERIFICATION.md:20` claims "Database suites ran against a fresh, separate PostgreSQL 18.1 instance" in a project with no database. Shared-harness boilerplate in a per-project honesty record.

## Spot-checks performed
- Course claim (`03-WORKED-CHANGE.md`): excerpt of `editExpense` "near line 791". -> `grep -n "function editExpense" app.js` returns `791`, and the 17-line body matches exactly, including `els.entryType.disabled = true;` and `document.querySelector("#entryModal h3").textContent = "Edit expense";`. -> **matches.**
- Course claim (`README.md` Scope): "Failed validation or storage keeps the original expense and the editor open." -> `app.js:209-212` returns early with `errorNode.textContent = "Could not save. The original expense is unchanged."` without touching `state`, and `els.entryModal.close()` is only reached after the successful assignment. Test 2 asserts `#entryModal.open === true`. -> **matches.**
- Course claim (`VERIFICATION.md`): "monthly spending must be $12.50, and reload must retain $12.50". -> Test 1 asserts `#expenseKpi` matches `/12.50/`, snapshots localStorage, reopens the app and asserts `state.expenses[0].amount === 12.5`. -> **matches.**
- Course claim (`01-CODEBASE-MAP.md` / test selector): rows expose `[data-edit-expense]`. -> `app.js:562` renders `data-edit-expense="${expense.id}"` with an `aria-label`, and `app.js:571` binds the handler. -> **matches.**
- Course claim (`VERIFICATION.md`): "Real Chromium browser interaction | Passed". -> `implementation/browser-checks.json` project "04" passed; `implementation/browser_checks.cjs:60+` drives `#monthPicker` and the edit flow in real headless Chromium. -> **matches.**
- Delivery claim: 2 test cases, 5,132 words. -> 2 `test(` blocks; `wc -w astraupskill/*` totals 5,132. -> **matches.**

## Improvements needed (ordered, concrete, actionable)
1. Either extend the persist-then-publish pattern to the create branch (`app.js:221-235`, replacing the direct `push` + `saveState()` with the same `next`/`try` shape) or add an explicit "Known inconsistency" box to `03-WORKED-CHANGE.md` naming `app.js:221` and making it Exercise 1. As written the project teaches one rule and demonstrates its violation on the next screenful. Effort: S (docs) / M (code).
2. Add one test that edits an expense whose `id` no longer exists (the `"This expense no longer exists."` branch at `app.js:207`) — it is currently untested dead-ish code in the function the course asks you to study. Effort: S.
3. Replace the generic "Three variations" block with the three concrete money fixtures the tests already imply (`0.1 + 0.2`, `1.001`, `1e3`) and state what each proves about `Number()` parsing. Effort: S.
4. Say in `README.md` Scope that only expenses are editable, and add an exercise to extend the pattern to incomes or bills. Effort: S.
5. Strip the PostgreSQL/Recipeweb sentences from `VERIFICATION.md:20` and replace with this project's true environment (Node 22.16.0, jsdom, Playwright Chromium). Effort: S.

## One-paragraph summary for the index
The clearest update-a-record lesson among the plain-browser projects: editing an expense reuses the entry modal in an explicit mode, forces the original `id` onto the replacement record, validates the amount to two decimals and a real date, and writes to storage before publishing to memory so a quota failure leaves the original intact and the editor open. All five spot-checks against `app.js` passed, and the failure test asserts the stored value rather than the error message. Its main flaw is an unflagged contradiction — the create path 15 lines below still mutates state first through an unguarded `saveState()` — and the course chooses to gloss that rather than turn it into the exercise it should be. Worth two to three hours as a core browser-side CRUD lesson, with the create-path inconsistency treated as the first thing you fix yourself.
