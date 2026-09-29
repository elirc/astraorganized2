# Invoice Studio — Fable review

- **Path:** `JS1/invoice-studio`  ·  **Wave:** 1  ·  **Stack:** TypeScript + Express + PostgreSQL (`pg`) + React/Vite  ·  **Batch:** B04
- **Astra's change (one line):** Invoice writes now enforce an explicit input contract — UUID client id, real calendar `issuedDate` (round-tripped through `toISOString().slice(0,10)`), at most 100 line items, whole safe-integer quantities, `^\d+(?:\.\d{1,2})?$` unit prices and tax 0-100 — the computed `total` is rounded to cents (`Math.round((subtotal + tax) * 100) / 100`), parent and line writes stay in one transaction, and PostgreSQL SQLSTATEs map to 400 rather than 500.
- **Course size:** 6,606 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/feature.test.ts`, helper `test/database.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 3 | 5 | 4 | 5 | 3 | 2 | 4.0 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- The money handling is taught with a concrete, checkable arithmetic case. `test/feature.test.ts` builds two lines at `unitPrice: 0.1`, `quantity: 2`, `taxRate: 10`, then asserts `subtotal === 0.2`, `tax === 0.02` and `total === 0.22` — numbers that only come out right because of the new `Math.round((subtotal + tax) * 100) / 100`. That is a real float-representation lesson, not an abstraction.
- The validation table is genuinely adversarial. The second test walks seven bad payloads — `{issuedDate:'2027-02-29'}` (a date that parses but is not real), `{taxRate:'Infinity'}`, `{taxRate:101}`, `{items:[null]}`, fractional quantity `1.5`, array-wrapped quantity `[1]`, and a three-decimal price `0.001` — and after all seven asserts `deepEqual` against the pre-edit invoice. Error codes alone are not accepted as proof.
- The transactional lesson is demonstrated by fault injection, not by assertion. The third test creates a real `BEFORE INSERT` trigger on `invoice_items` that raises on a specific description, then PUTs an invoice whose lines are deleted-then-reinserted, asserts 500, and asserts the original invoice **and its lines** are still intact. That is the clearest demonstration of "DELETE + INSERT must share a transaction" in the batch.
- Calendar-date correctness is handled at the boundary rather than trusted: `parseInvoice` rejects `2027-02-29` because `new Date(value+"T00:00:00Z").toISOString().slice(0,10) !== value`, and the test covers it.

## Problems found (evidence required)
- **[D8]** Template scaffolding. `02-CONCEPTS.md`'s "Invariants", "Validation versus normalization", "State transitions and failure boundaries", "Identity, representation and derived values" and "Small design decisions deserve explanations" sections are byte-identical across **all 48** `JS1/*/astraupskill/02-CONCEPTS.md` files (`grep -l "Validation rejects values the operation cannot accept" JS1/*/astraupskill/02-CONCEPTS.md` returns 48). `astraupskill/README.md` differs from `JS1/forum-search/astraupskill/README.md` by 6 lines out of 72 — and this is the project where decimal semantics *should* have produced project-specific concept prose.
- **[D8/D1]** `04-TESTING-AND-DEBUGGING.md` includes the off-topic paragraph "For Poll Studio and Kanban Flow, jsdom runs the actual app.js against its HTML and fresh browser storage…", which refers to stages 21-22, not this project.
- **[D7]** `test/feature.test.ts` is minified onto 15 physical lines; the seven-case bad-payload loop is a single line of ~450 characters. `03-WORKED-CHANGE.md` asks the learner to "Read each test as arrange → act → assert" over it.
- **[D3]** `05-PRACTICE.md` exercises are one-sentence stubs; `06-SOLUTIONS-AND-REVIEW.md` repeats one identical **Review** paragraph under every exercise.
- **[D2, minor]** The quantity guard is written awkwardly: `!Number.isSafeInteger(Number(item.quantity)) || !(typeof item.quantity === "number" || typeof item.quantity === "string") || ...`. The type check runs *after* the coercion check, so the reasoning order a learner is being taught (validate shape, then value) is inverted in the code they are told to read.
- **[D5]** All dependencies are `"latest"` in `package.json` with no lockfile; VERIFICATION.md discloses this but nothing is pinned.

## Spot-checks performed
- Claim "The excerpt below comes from server/src/index.ts near line 108" (`03-WORKED-CHANGE.md:19`) -> read `server/src/index.ts:108` -> quoted block **matches** exactly.
- Claim (report and VERIFICATION) "Create two units at 12.34, zero tax, issued 2028-02-29: total 24.68" -> read `test/feature.test.ts` -> the test actually uses `unitPrice: 0.1`, `taxRate: 10` and asserts `total === 0.22`. The arithmetic principle matches but the literal fixture **does not match** the test; this is a narrative rewording, not a false capability claim.
- Claim "Reject quantity [2], a three-decimal price and 2027-02-29" -> `test/feature.test.ts` bad-payload loop contains `{items:[{description:'bad',quantity:[1],unitPrice:2}]}`, `{items:[{description:'bad',quantity:1,unitPrice:0.001}]}` and `{issuedDate:'2027-02-29'}`; **matches** (quantity `[1]` rather than `[2]`).
- Claim VERIFICATION.md "Automated test cases: **3**" -> 3 `test(` blocks on disk; **matches**.
- Claim VERIFICATION.md "typecheck | Passed" -> `batch03/type-fix-checks.json` has project 34 `typecheck exit_code: 0`; `batch03/logs/34-typecheck.log` exists; **matches**.
- Independent check: `diff -rq batch03/stage/34 JS1/invoice-studio` differs only by `client/dist`; **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Rewrite `astraupskill/02-CONCEPTS.md` so at least two sections are about money and dates in this codebase: why `numeric` in PostgreSQL and `number` in JavaScript disagree, why `subtotal + tax` needs `Math.round(x*100)/100` before it is stored or shown, and what `/^\d+(?:\.\d{1,2})?$/` accepts and rejects (including `'2.50'` vs `2.5` vs `.5`). Replace the generic "Identity, representation and derived values" and "Small design decisions" sections. (effort: M)
2. Align the fixture narrative: either change the VERIFICATION.md / chapter sentence to the `0.1 × 2 @ 10%` case the test really runs, or add a `12.34 × 2, tax 0` case to `test/feature.test.ts`. (effort: S)
3. Reorder the quantity guard in `server/src/index.ts` so the `typeof` check precedes `Number.isSafeInteger(Number(...))`, matching the shape-then-value order the course teaches. (effort: S)
4. Reformat `test/feature.test.ts` (especially the seven-case loop) to one payload per line and re-paste it into `03-WORKED-CHANGE.md`. (effort: S)
5. Delete the "For Poll Studio and Kanban Flow…" paragraph from `04-TESTING-AND-DEBUGGING.md`, and expand `05-PRACTICE.md` exercises into prompts with a starting state and acceptance example. (effort: M)

## One-paragraph summary for the index
If you do one course from this batch on input contracts and parent/child writes, do this one. Astra added a full validation contract for invoices — UUID client, a real calendar date, bounded line arrays, whole quantities, two-decimal prices, tax 0-100 — fixed the total to round to cents, and proved the transaction boundary by installing a PostgreSQL trigger that fails a line insert *after* the old lines were deleted, then asserting the original invoice and its lines survive. Every path, line reference and excerpt in the course matches the code on disk, the test count is real, and VERIFICATION.md matches the batch evidence. The failings are in the writing, not the engineering: five of six chapter-2 sections are boilerplate shared with 47 other courses, the exercises are one-liners, and the tests are minified so densely that the "read them as arrange/act/assert" instruction is impractical.
