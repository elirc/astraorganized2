# JS1/habit-tracker — Fable review

- **Path:** `JS1/habit-tracker`  ·  **Wave:** 1  ·  **Stack:** vanilla JS + localStorage (jsdom tests, no framework/server)  ·  **Batch:** B02
- **Astra's change (one line):** `currentStreak` now lets a streak anchor on yesterday while today is still unchecked; a new `bestStreak(habit, today)` counts the longest run of consecutive *real, non-future, strictly-`true`* dates and is rendered as a "Best: N days" badge; day buttons gain `aria-label`.
- **Course size:** 4,952 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 (`test/streaks.test.cjs`, ~8 assertions, plus `test/browser.cjs`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 3 | 3 | 4 | 4 | 4 | 3 | 3.8 |

**Verdict:** IMPROVE    **Path role:** elective

## What Astra did well
- The date-validation logic is the genuinely instructive part and it is correct: `app.js:209-221` rejects `checked !== true`, rejects a bad shape, rejects future dates, and — the subtle one — round-trips through `new Date(\`${date}T00:00:00Z\`).toISOString().slice(0,10) === date` so that `2024-02-30` (which `Date` silently rolls to March 1) is thrown out.
- The test is a real calendar test, not a tautology: `test/streaks.test.cjs` feeds `{'2024-02-28':true,'2024-02-29':true,'2024-03-01':true,'2024-03-03':true,'2024-03-04':false,'2024-02-30':true,'2025-01-01':true}` and asserts `bestStreak === 3`, which simultaneously exercises leap day, a gap, an explicit `false`, an impossible date and a future date.
- The one-day-behind fix is pinned by an independent assertion: with `startOfToday` stubbed to 2024-03-11, two consecutive days ending yesterday give 2, while a single day two days ago gives 0 (`test/streaks.test.cjs`, second test).
- The Chromium check (`batch02/browser_checks.cjs:49-54`) is a real end-to-end round trip: read "Best: 3", click today's cell, assert the *current* badge becomes "2 day", reload, assert "Best: 2" persisted.

## Problems found (evidence required)
- **[D8]** Only **35%** of the course's substantive words are unique to this project (measured across the 10 B02 courses). `02-CONCEPTS.md` sections 2-6, `04-TESTING-AND-DEBUGGING.md` and `05-PRACTICE.md` are near-verbatim shared text; e.g. "Validation rejects values the operation cannot accept. Normalization converts acceptable values to the representation the rest of the program expects." appears identically in all ten.
- **[D6]** `VERIFICATION.md` carries the shared line "PostgreSQL tests used a separate local PostgreSQL 18.1 instance on port 55439…" although `checks.json` shows only `node --test .../12/test/streaks.test.cjs` for this project. Misleading boilerplate.
- **[D2]** `bestStreak` is tested only by direct invocation via `app.evaluate(...)`, i.e. as a private function, not through the UI path that computes it per habit. The single DOM assertion is `querySelectorAll('.best-streak').length === 2`, which proves the badge is rendered but never that the *displayed number* is correct for a seeded habit. The Chromium check covers that gap, but the in-repo suite a learner runs with `npm test` does not.
- **[D2]** The new `aria-label` (`app.js:156`, `\`${habit.name}: ${iso}\``) *overrides* the visible "Mon 8" text for screen-reader users and does not include the done/not-done state in words (it relies on `aria-pressed`). Defensible, but the course presents it as "full accessible names" without discussing the override.
- **[D4]** No HTTP, SQL, ownership, transactions or React. The transferable content is date correctness and derived-vs-stored values.
- **[D5]** No `package-lock.json`; `jsdom: ^25.0.1` is unpinned.

## Spot-checks performed
- Claim: excerpt "comes from app.js near line 209" -> `bestStreak` is declared at `app.js:209` and the fenced block is a verbatim substring of `app.js` -> **matches**.
- Claim (VERIFICATION): "Checks on February 28, February 29 and March 1, 2024 give best three. Add March 3 and invalid February 30: best remains three." -> exactly the fixture in `test/streaks.test.cjs` line 8-9 -> **matches**.
- Claim (report): "A current streak may continue through yesterday while today is still in progress." -> `app.js:200-201` `if (!habit.history[isoDate(cursor)]) cursor.setDate(cursor.getDate() - 1);` before the while loop -> **matches**.
- Claim (VERIFICATION): "Automated test cases: 2" -> `logs/12-tests.log` `# tests 2 / # pass 2` -> **matches**.
- Claim (VERIFICATION): PostgreSQL 18.1 environment -> no PG entry for project 12 in `checks.json` -> **does not match**.

## Improvements needed (ordered, concrete, actionable)
1. Strip the PostgreSQL sentence from `astraupskill/VERIFICATION.md`; state the actual environment (Node 22.16.0 + jsdom) (effort: S).
2. Add a test that seeds two habits in `localStorage`, calls `render()`, and asserts the *text* of each `.best-streak` badge, so `npm test` alone proves the wiring (effort: S).
3. In `02-CONCEPTS.md`, replace the generic validation/normalization section with a project-specific one on why `'2024-02-30'` must be rejected by round-trip rather than by `isNaN(Date.parse(...))` — that is the single most valuable idea here and it is currently buried in a code comment (effort: M).
4. Make `05-PRACTICE.md` Exercise 4 concrete: "schedule a refresh at local midnight without assuming 24h, and prove it survives a DST transition" — the current stretch body is the shared template (effort: M).
5. Document the `aria-label` override tradeoff in `04-TESTING-AND-DEBUGGING.md` (effort: S).

## One-paragraph summary for the index
The best small date-logic exercise in this batch. The change forces you to confront three things juniors routinely get wrong: that `new Date('2024-02-30')` does not fail, that "current streak" and "longest streak" are different computations with different edge cases, and that today being incomplete is not the same as today being missed. The test is honest — it mixes a leap day, a gap, a literal `false`, an impossible date and a future date into one fixture — and the Chromium check verifies the badge survives a reload. The drawback is that roughly two-thirds of the nine files are template shared with nine sibling courses, so the concepts, testing and practice chapters read generically, and the verification page claims a PostgreSQL environment that was never used here. Worth an hour as an elective; it is not on the target CRUD stack.
