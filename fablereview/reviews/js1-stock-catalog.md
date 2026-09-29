# JS1/stock-catalog — Fable review

- **Path:** `JS1/stock-catalog`  ·  **Wave:** 1  ·  **Stack:** Node/Express (in-memory repository with filter/sort/paginate) + React 18 (Vite, JSX)  ·  **Batch:** B03
- **Astra's change (one line):** Pagination inputs are now validated rather than coerced (`whole(req.query.page,...)` / `whole(req.query.pageSize,...)` replace `Number(x) || default`, so `page=Infinity` and `pageSize=2.5` fall back to defaults instead of producing nonsense), the sort comparator gained an id tie-break so equal keys page deterministically, and `validateProduct` now rejects non-finite prices and fractional/negative stock before the legacy checks run; plus the JSON-object body guard and a testable `export const app`.
- **Course size:** 5,775 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 in `test/api.test.js` (+ `test/http.js`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 3 | 4 | 3 | 5 | 4 | 4 | 4 | 2 | 3.6 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- This is the most CRUD-relevant change in the batch. Pagination + sorting + filtering is *the* list-endpoint problem, and the two fixes are the two real bugs: `Math.max(1, Number(req.query.page) || 1)` accepted `Infinity` (since `Number("Infinity")` is truthy) and `clamp(Number(pageSize) || 5, 1, 50)` accepted `2.5`. The replacements at `server/server.js:27-28` require a safe integer in range or fall back to the default.
- The tie-break `compare(a, b, sort, dir) || a.id.localeCompare(b.id)` (`server/server.js:111`) is the correct fix for the classic "items jump between pages" bug, and test 1 proves it the right way: it issues the *same* query twice and asserts the id lists are identical, then pages past the end and asserts the clamp lands on page 2 with one item.
- Price validation is precise: it requires a number or a non-blank numeric string, requires `Number.isFinite`, and caps the magnitude (`server/server.js:64-66`). Test 2 covers `'Infinity'`, `''`, `true`, `1.5` stock, `{}` name and `null` stock — six payloads, all asserted as 400.
- Existing last-page clamping got regression coverage it did not have before, which the report states honestly rather than claiming it as new behaviour.

## Problems found (evidence required)
- **[D1] The chapter's one "Actual implementation excerpt" contains none of the change.** `03-WORKED-CHANGE.md` says "The excerpt below comes from `server/server.js` near line 16" and then shows five lines of *unmodified pre-existing* code:
  > `const repository = createProductRepository();` / `const SORTABLE = ["name", "price", "stock", "category"];` / `// The list route does the heavy lifting on the server: filter, then sort, / // then slice a single page. The client only ever receives one page.`
  None of the actual change — the `whole()` page normalization at lines 27-28, the `|| a.id.localeCompare(b.id)` tie-break at line 111, or the price/stock gate at lines 64-66 — appears anywhere in the worked-change chapter. A learner who reads chapter 3 as instructed never sees the worked change. This is the single biggest defect in this course.
- **[D8]** Template. `05-PRACTICE.md`, `06-SOLUTIONS-AND-REVIEW.md` and `04-TESTING-AND-DEBUGGING.md` are the shared batch scaffolding; against `JS1/event-admin` the testing chapter differs on about 3 of 64 lines.
- **[D2]** Dead code: `realDate` is defined at `server/server.js:173` and never called in this file (no dates in this domain). Copy-pasted helper trio.
- **[D2]** The legacy guards at `server/server.js:67-79` (`if (!name || name.trim().length < 2)`, the price and stock checks) are now unreachable behind the new gate, leaving two validation layers with different messages for the same rule. Undiscussed in the course.
- **[D2]** `pageSize` semantics changed subtly and silently: the old `clamp(...,1,50)` coerced `pageSize=500` down to 50; the new code accepts any safe integer up to 1,000,000 and *then* does `Math.min(..., 50)` — same result, but the validation bound (1,000,000) and the business bound (50) are now two different numbers in one expression. Neither the course nor a test pins `pageSize=500 -> 50`.
- **[D8/D1]** `astraupskill/README.md` Prerequisites carries the shared SQL sentence; there is no SQL here. `VERIFICATION.md` Limits mentions "date representation and transaction scope".
- **[D6]** `logs/26-browser-failure.png` exists alongside `logs/26-browser.png`, but `browser-checks.json` records only `{"project":"26","passed":true}` with no note of an intermediate failure and no assertion detail. The course claims "integrated browser checks passed"; the evidence shows a pass and an unexplained failure artifact.
- **[D2]** `htmlFor="lesson-field-1..4"` ids in `client/src/App.jsx`. **[D5]** all deps `"latest"`, no lockfile.

## Spot-checks performed
- "The excerpt below comes from server/server.js near line 16" -> `sed -n '16p'` = `const repository = createProductRepository();`. The line reference is *correct*, but the excerpt is unchanged pre-existing code -> claim technically matches, content does not serve the chapter's stated purpose.
- "Page 999 becomes page 2 with one item" -> `test/api.test.js:10` asserts `last.page === 2` and `last.items.length === 1` against 3 seeded products at `pageSize=2`; the repository clamps with `Math.max(1, Math.ceil(total/pageSize))` -> matches.
- "Infinite/fractional page inputs use defaults" -> `test/api.test.js:11` requests `?page=Infinity&pageSize=2.5` and asserts `page === 1`, `pageSize === 5`; `whole()` rejects both because `Number.isSafeInteger(Infinity)` and `Number.isSafeInteger(2.5)` are false -> matches.
- "Three same-price products at two per page give stable ids on page 1" -> `test/api.test.js:8-9` runs the identical query twice and `deepEqual`s the id lists -> matches the tie-break at line 111.
- Test/build counts -> `logs/26-tests.log` `# tests 2 / # pass 2 / # fail 0`; `checks.json` project 26 build `exit_code: 0` -> matches.

## Improvements needed (ordered, concrete, actionable)
1. **Replace the excerpt in `03-WORKED-CHANGE.md`.** Show `server/server.js:27-28` (the `whole()` page/pageSize normalization) and `server/server.js:111` (the id tie-break) side by side with the backup versions, and update the "near line N" pointer. As delivered, the worked-change chapter does not contain the worked change. (effort: S)
2. Delete the unused `realDate` at `server/server.js:173` and remove the now-unreachable legacy guards at lines 67-79, so one gate owns each rule. (effort: S)
3. Add a test pinning `pageSize=500 -> 50` and `pageSize=0 -> 5`, and explain in `02-CONCEPTS.md` the difference between *rejecting* an out-of-range page size and *clamping* it — the code currently does both, with two different bounds in one line. (effort: S)
4. Note the `logs/26-browser-failure.png` artifact in `VERIFICATION.md` (what failed, what was changed, what re-passed) or remove the stale screenshot. Right now the evidence folder contradicts the clean "passed" claim. (effort: S)
5. Rewrite `05-PRACTICE.md` Exercises 1-4 with catalog-specific criteria — e.g. "add `?minStock=` and prove it composes with search, sort and paging by asserting `total` changes but `pageSize` does not". (effort: M)
6. Rename `lesson-field-N` ids; add a lockfile; strip the SQL/date boilerplate from README and VERIFICATION. (effort: S)

## One-paragraph summary for the index
The most directly useful domain in the batch — filter, then sort, then slice one page — and the change fixes the two bugs that bite every real list endpoint: query parameters coerced instead of validated (so `page=Infinity` and `pageSize=2.5` used to get through), and a non-total sort comparator that let equal-priced items shuffle between pages. The two tests prove both properly, including issuing the same query twice to check id stability. The serious flaw is in the teaching, not the code: the "Actual implementation excerpt" in chapter 3 shows five lines of *unchanged* pre-existing setup code and none of the actual change, so the worked-change chapter has no worked change in it. Fix that one excerpt and this becomes a strong core lesson; until then, read the diff against `implementation/batch03/backups/26` instead of chapter 3.
