# JS1/pantry-inventory — Fable review

- **Path:** `JS1/pantry-inventory`  ·  **Wave:** 1  ·  **Stack:** vanilla JS + localStorage (jsdom tests, no framework/server)  ·  **Batch:** B02
- **Astra's change (one line):** Separates two predicates that the original code had conflated — low stock (`quantity <= minimum`) and expired (`expires < localToday()`) — so a row can show "Stock OK · Expired", adds an "Expired" filter, redefines the old "Fresh" filter as "In stock & not expired", tightens create/edit validation (blank quantity, non-finite numbers, impossible dates like `2026-02-30`), and re-renders on `visibilitychange` so a tab left open overnight recomputes date-based status.
- **Course size:** 4,939 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 (`test/expiration.test.cjs`, ~10 assertions, plus `test/browser.cjs`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 3 | 3 | 4 | 4 | 4 | 3 | 3.8 |

**Verdict:** IMPROVE    **Path role:** elective

## What Astra did well
- The underlying bug was real and is well chosen: in `backups/16/app.js` the status was `item.quantity <= item.minimum ? "Low" : "Fresh"`, so a fully-stocked expired jar of something read "Fresh". The fix makes the two facts independent rather than adding a third status value — a good modelling lesson.
- Local-date handling is correct where it matters. `localToday()` (`app.js:174-177`) builds the string from `getFullYear/getMonth/getDate` rather than `toISOString()`, which would shift the day for anyone west of UTC. `isRealDate` round-trips through `toISOString().slice(0,10)` so `2026-02-30` is rejected instead of silently becoming March 1.
- The test asserts the *combination*, not just each predicate: with `localToday` stubbed to `2026-09-08`, it checks the low-items counter is 1, that the Expired filter shows exactly one row whose status matches `/Stock OK.*Expired/`, that the Fresh filter shows only the future item, and that an item expiring *today* is not expired.
- The empty-string trap is covered explicitly. Validation now includes `quantityInput.value === ""` (`app.js:78`) because `Number('')` is `0`, which passes a `>= 0` check; the second test submits a blank quantity and asserts `items.length` is unchanged.

## Problems found (evidence required)
- **[D2]** `document.addEventListener("visibilitychange", ...)` is registered at module top level in the middle of the function declarations (`app.js:183`) with no corresponding teardown and no test. The Chromium check (`browser_checks.cjs:81-84`) stubs `localToday` and calls `renderItems()` directly instead, so the visibility handler — an advertised feature ("returning to the tab refreshes date-based status") — is delivered with **zero** automated coverage.
- **[D2]** The filter `<option>` markup was edited sloppily: `index.html:63-64` now reads `<option value="Fresh">In stock &amp; not expired</option>` followed by `<option value="Expired">Expired</option></select>` on one line with the `</select>` jammed onto the option. It parses, but it is the kind of edit a reviewer would reject.
- **[D8]** Only **35%** of substantive words are unique to this project. `06-SOLUTIONS-AND-REVIEW.md` repeats one identical "Review:" paragraph under all four exercises ("Demonstrate an ordinary case and a case that would break a naive implementation…"), so four different tasks share one rubric.
- **[D6]** `VERIFICATION.md` includes the batch-wide "PostgreSQL tests used a separate local PostgreSQL 18.1 instance on port 55439" sentence; `batch02/checks.json` records only a `node --test` run for project 16.
- **[D4]** Browser-only; no HTTP, SQL, ownership, transactions or React.
- **[D5]** No `package-lock.json`; `jsdom: ^25.0.1` unpinned.

## Spot-checks performed
- Claim: excerpt "comes from app.js near line 130" -> `getVisibleItems`' filter body is at `app.js:130` and the fenced block is a verbatim substring -> **matches**.
- Claim (VERIFICATION): "On September 8, an item expiring September 7 with quantity five and minimum one is Stock OK and Expired." -> `test/expiration.test.cjs` item `a` plus the `/Stock OK.*Expired/` assertion -> **matches**.
- Claim (report): "the in-stock/nonexpired view excludes expired items" -> `app.js:134` `(activeFilter === "Fresh" && !isLow && !isExpired(item))` -> **matches**.
- Claim (report): "returning to the tab refreshes date-based status" -> the listener exists at `app.js:183` -> **code matches, but no test exercises it**.
- Claim (VERIFICATION): "Automated test cases: 2" -> `batch02/logs/16-tests.log` `# tests 2 / # pass 2` -> **matches**.
- Claim (VERIFICATION): "Chromium interaction Passed" -> `browser_checks.cjs:81-84` selects the Expired filter and asserts one row -> **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Add a test for the `visibilitychange` path: dispatch the event through the jsdom harness with `localToday` advanced by a day and assert a formerly-fresh row becomes Expired (effort: S).
2. Tidy `index.html:63-64` — put `</select>` on its own line and keep the two `<option>` elements consistently formatted (effort: S).
3. Remove the PostgreSQL sentence from `astraupskill/VERIFICATION.md` (effort: S).
4. In `06-SOLUTIONS-AND-REVIEW.md`, give each of the four exercises its own review criterion rather than repeating one paragraph (effort: M).
5. Add a short section to `02-CONCEPTS.md` on why `toISOString()` is the wrong way to get "today" for a user west of UTC, with a worked example at 23:00 local — this is the single most reusable idea in the lesson and is currently only implicit in `localToday()` (effort: M).

## One-paragraph summary for the index
A clean lesson in not collapsing two independent facts into one status field, plus a solid drill on local-date correctness. The original code called a fully-stocked but expired item "Fresh"; the fix makes stock and expiry separate predicates and adds a filter for each. The validation work is the part worth copying: it rejects a blank quantity (because `Number('')` is `0`) and rejects `2026-02-30` (because `Date` silently rolls it to March 1), both of which the tests assert. Two gaps: the advertised "refresh when you return to the tab" behavior has no automated test at all, and about two-thirds of the nine course files are shared template — the exercise review rubric is literally the same paragraph four times. Worth an hour as an elective; it teaches nothing about HTTP, SQL or React.
