# JS1/budget-tracker — Fable review

- **Path:** `JS1/budget-tracker`  ·  **Wave:** 1  ·  **Stack:** vanilla JS + localStorage (jsdom tests, no framework/server)  ·  **Batch:** B02
- **Astra's change (one line):** Replaces `Number(amountInput.value)` with a strict `parseCents` regex parser (positive, at most two decimals, bounded, no `1e3` / `Infinity` / empty-string coercion), adds a real-date check, sums totals in integer cents instead of floats, preserves the record id on edit, and routes create/edit/delete through `commitTransactions(next)` so state is only published after `localStorage.setItem` succeeds (the form is retained on failure).
- **Course size:** 4,848 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 (`test/money.test.cjs`, ~17 assertions, plus `test/browser.cjs`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 3 | 3 | 4 | 4 | 4 | 3 | 3.8 |

**Verdict:** IMPROVE    **Path role:** elective

## What Astra did well
- The parser is the right fix and is tested against exactly the inputs that break `Number()`. `test/money.test.cjs` asserts `parseCents` returns NaN for `''`, `'0'`, `'-1'`, `'1.001'`, `'Infinity'`, `'1e3'` and `'1000000000'` — `Number('')` is 0 and `Number('1e3')` is 1000, so a naive implementation fails five of those seven.
- Totals now accumulate in cents (`app.js:135`, `summary[transaction.type] += Math.round(transaction.amount * 100)`) and the test pins the classic float bug: two income rows of `0.1` and `0.2` must display `$0.30`, which a float sum renders as `$0.30000000000000004`-rounding-dependent.
- Write-before-publish is genuinely enforced, not just claimed: `commitTransactions` (`app.js:187-192`) writes first and only assigns `transactions = next` on success. The second test stubs `Storage.prototype.setItem` to throw *after* loading the editor, submits, and asserts three things at once — `transactions[0].amount` is still `0.1`, `#amount` still holds the user's typed `'12.50'`, and the message says "Could not save".
- Record identity on edit is preserved explicitly (`app.js:84`, `{ ...transaction, id: editingId }`); the backup shows the previous code replaced the whole object.

## Problems found (evidence required)
- **[D2]** `renderTransactions` now does `Math.round(transaction.amount * 100)` on *every stored record at load time*, including records saved by the old build with more than two decimals. Those are silently rounded for display while the stored value keeps its extra digits, so the ledger total and the row amounts can disagree. Nothing in the course or the tests covers legacy data; `ALL_20_PROJECTS_REPORT.md` only notes that "Budget totals use cents for arithmetic while retaining the existing stored dollar-number schema."
- **[D2]** The parser rejects `'0'` as an amount, which is correct for this product, but `parseCents` is also used for *edits*, so an existing zero-amount record can never be re-saved. Not covered.
- **[D8]** Only **33%** of substantive words are unique to this project. `05-PRACTICE.md` is ~95% identical to `JS1/flashcards/astraupskill/05-PRACTICE.md`; Exercise 3's body ("Create a failing example in a disposable fixture. Capture the state before the operation and after the failure…") is verbatim in both, with one substituted prompt line.
- **[D6]** `VERIFICATION.md` carries the shared "PostgreSQL tests used a separate local PostgreSQL 18.1 instance on port 55439" line although `batch02/checks.json` records only a `node --test` run for project 15.
- **[D4]** Browser-only; no HTTP, SQL, ownership or transactions. The money-representation lesson transfers to any stack, but nothing else here does.
- **[D5]** No `package-lock.json`; `jsdom: ^25.0.1` is a caret range.

## Spot-checks performed
- Claim: excerpt "comes from app.js near line 175" -> `parseCents` is declared at `app.js:175` and the fenced block is a verbatim substring -> **matches**.
- Claim (VERIFICATION): "Income 0.10 plus 0.20 displays $0.30; 1.01 parses to 101 cents. Reject empty, zero, negative, 1.001, Infinity, scientific notation and values above 999999999.99." -> every one of those cases is an assertion in `test/money.test.cjs` -> **matches**.
- Claim (report): "Create, edit and delete publish only after storage succeeds, retaining the form on failure." -> `app.js:110` `if (!commitTransactions(...)) return;` in `deleteTransaction` and `app.js:87` in `saveTransaction`; the form is not reset before the guard -> **matches**.
- Claim: the error message bound "maximum 999999999.99" -> `parseCents` allows `cents <= 99999999999`, i.e. 999,999,999.99 -> **matches** (message and code agree).
- Claim (VERIFICATION): "Automated test cases: 2" -> `batch02/logs/15-tests.log` `# tests 2 / # pass 2` -> **matches**.
- Claim (VERIFICATION): "Chromium interaction Passed" -> `batch02/browser_checks.cjs:77-80` enters `0.10`, asserts `#income-total` is `$850.10`, reloads, asserts it again -> **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Add a migration-on-load step in `app.js` `loadTransactions()` that normalizes every stored `amount` to two decimals, and a test seeding a legacy record like `{amount: 0.105}` asserting the row and the total agree (effort: M).
2. Allow `0` when editing an existing record, or document in `02-CONCEPTS.md` why zero is rejected everywhere; add a test either way (effort: S).
3. Remove the PostgreSQL sentence from `astraupskill/VERIFICATION.md` (effort: S).
4. Rewrite `05-PRACTICE.md` exercises 1-4 so the whole body is about money: "store cents as the schema and migrate existing dollar-number records", "prove `Intl.NumberFormat` rounding does not hide a cent" (effort: M).
5. Add a failure lab in `04-TESTING-AND-DEBUGGING.md` that computes `0.1 + 0.2` in the console before showing the cents fix — the course currently states the conclusion without making the learner see it (effort: S).

## One-paragraph summary for the index
A tight, well-tested drill on the two things that make money handling go wrong: `Number()` accepting `''`, `'1e3'` and `'Infinity'` without complaint, and float addition losing cents. The change is real, the seventeen assertions in `test/money.test.cjs` are the kind a reviewer would ask for, and the failure test proves both that the stored record survived a rejected write and that the user's typed value stayed in the form. What holds it back: existing records with more than two decimals are silently rounded for display but not in storage, roughly two-thirds of the nine course files are shared template, and the verification page describes a PostgreSQL environment this project never touched. Do it as a one-to-two-hour elective before any project where you will store currency; skip the practice chapter and write your own exercises.
