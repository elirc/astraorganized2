# JS1/reading-list — Fable review

- **Path:** `JS1/reading-list`  ·  **Wave:** 1  ·  **Stack:** vanilla JS + localStorage (jsdom tests, no framework/server)  ·  **Batch:** B02
- **Astra's change (one line):** Adds a status `<select>` filter that composes with the existing search box, makes sorting total (rating ties break by title then id; title/status ties break by id), and renders a live `#reading-summary` that separates "showing N of M" from "K finished overall" — without mutating the saved order.
- **Course size:** 4,788 words across 9 files  ·  **Tests claimed:** 1  ·  **Tests found on disk:** 1 (`test/filters.test.cjs`, 4 assertions, plus `test/browser.cjs`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 3 | 3 | 3 | 4 | 4 | 4 | 3 | 3.6 |

**Verdict:** IMPROVE    **Path role:** elective

## What Astra did well
- The core lesson — that `Array.prototype.sort` is not stable across engines for your purposes unless the comparator is total — is taught with a correct fix: `app.js:141-146` chains `|| a.title.localeCompare(b.title) || a.id.localeCompare(b.id)`.
- Filter composition is done in one predicate rather than by chaining two `filter` passes over a mutated array, so the saved order is untouched; the test proves it by asserting `JSON.parse(localStorage.getItem('js1-reading-list'))[0].id === 'z'` after sorting put Alpha first.
- The summary deliberately distinguishes the *visible* count from the *overall* count (`app.js:149`), which is the exact bug class the exercise is about — the browser check asserts both `.book-card` count 0 and `#reading-summary` still reading "1 finished".
- The CSS additions (`styles.css:205-213`) are scoped to `.toolbar` and wrap the new control, so the change does not regress the existing layout.

## Problems found (evidence required)
- **[D2]** One test case for a change touching four behaviors. `test/filters.test.cjs` asserts the rating tie-break (Alpha before Zebra) but never asserts the *title/status* tie-break added on `app.js:145` (`a[sortMode].localeCompare(b[sortMode]) || a.id.localeCompare(b.id)`). That line is delivered untested.
- **[D2]** `a.id.localeCompare(b.id)` assumes every persisted record has a string `id`. Records written by an older build, or hand-edited `localStorage`, can carry a numeric id and this throws `a.id.localeCompare is not a function` — the failure is not guarded and not discussed anywhere in the course.
- **[D8]** Lowest specificity in the batch: only **33%** of substantive words are unique to this project. `06-SOLUTIONS-AND-REVIEW.md` repeats one identical "Review:" paragraph under every exercise ("Demonstrate an ordinary case and a case that would break a naive implementation. Explain which existing invariant remains unchanged."), so four exercises share one review rubric.
- **[D6]** `VERIFICATION.md` includes the shared "PostgreSQL tests used a separate local PostgreSQL 18.1 instance on port 55439" sentence; `checks.json` shows only a `node --test` run for project 13.
- **[D3]** `VERIFICATION.md` reports "Automated test cases: 1", which understates the evidence (the one test carries four assertions plus a separate Chromium check) while simultaneously being the thinnest suite in the batch. The course never tells the learner that one `test()` block here is doing the work of three.
- **[D4]** Browser-only; no HTTP, SQL, authz or transactions.
- **[D5]** No lockfile; `jsdom: ^25.0.1` unpinned.

## Spot-checks performed
- Claim: excerpt "comes from app.js near line 132" -> `getVisibleBooks` body starts at `app.js:132`, block is a verbatim substring -> **matches**.
- Claim (VERIFICATION): "Zebra and Alpha both have rating five and Finished status; Beta is Reading… Saved order remains Zebra, Alpha, Beta." -> exactly the `records` fixture and the `localStorage` assertion in `test/filters.test.cjs` -> **matches**.
- Claim (report): "Rating ties use title then id." -> `app.js:142` -> **matches**.
- Claim: `#status-filter` and `#reading-summary` exist -> `index.html:67-69` -> **matches**.
- Claim (VERIFICATION): "Chromium interaction Passed" -> `browser_checks.cjs:55-60` edits a book to Finished, filters, searches for an unmatched term, asserts 0 cards and "1 finished" -> **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Add a second test in `test/filters.test.cjs` that sorts by `title` with two identical titles and asserts the id tie-break, and one that sorts by `status` — the delivered comparator branch is currently unexercised (effort: S).
2. Harden `app.js:143-145`: coerce with `String(a.id).localeCompare(String(b.id))`, or validate ids on load, and explain the legacy-data hazard in `02-CONCEPTS.md` (effort: S).
3. Remove the PostgreSQL sentence from `astraupskill/VERIFICATION.md` (effort: S).
4. In `06-SOLUTIONS-AND-REVIEW.md`, write a distinct review criterion per exercise instead of repeating one paragraph four times (effort: M).
5. Add a worked "why is my list order changing between reloads?" failure lab to `04-TESTING-AND-DEBUGGING.md` using a non-total comparator, so the learner sees the bug before the fix (effort: M).

## One-paragraph summary for the index
The shortest and thinnest course in B02. The idea is worth knowing — a comparator that only compares one field leaves ties in engine-defined order, and a filtered view's count is not the same number as the domain's count — and the code change is correct. But the change ships with a single test that skips the tie-break branch it just added, the new `localeCompare` on ids will throw on legacy numeric ids, and two-thirds of the nine files are template shared with the other nine courses in this batch. Read it in twenty minutes for the total-ordering idea, then do the exercises somewhere with a real backend. Not a good first stop, and not worth doing in full.
