# JS1/job-pipeline — Fable review

- **Path:** `JS1/job-pipeline`  ·  **Wave:** 1  ·  **Stack:** Node/Express (in-memory array) + React 18 (Vite, JSX)  ·  **Batch:** B03
- **Astra's change (one line):** `GET /api/applications` now applies a deterministic sort after filtering — by `nextStepDate` with undated records pushed last via a `"9999-99-99"` sentinel and ties broken by id — and `validateApplication` gained a type gate where `contact`/`notes`/`nextStepDate` are *optional* but, when present, must be the right type, with a blank date explicitly allowed; plus the JSON-object body guard, testable `export const app`, and the missing React entry point `client/src/main.jsx`.
- **Course size:** 5,680 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 in `test/api.test.js` (+ `test/http.js`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 4 | 4 | 3 | 5 | 4 | 4 | 4 | 2 | 3.8 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- The optional-field rule is written correctly and is the genuinely transferable lesson: `req.body.contact !== undefined && !isText(req.body.contact)` (`server/server.js:70`) distinguishes *absent* from *present-but-wrong-type*, and `req.body.nextStepDate !== "" && !realDate(...)` (line 72) distinguishes *deliberately blank* from *malformed*. Most juniors collapse these three states into one falsy check.
- The sort is stable and total: `(a.nextStepDate || "9999-99-99").localeCompare(...) || a.id.localeCompare(b.id)` (`server/server.js:34`). Using a sentinel that sorts after any real ISO date, and then an id tie-break, is the right pattern and is exactly what test 1 asserts.
- Test 1 composes filter *and* sort in one request (`/api/applications?search=AstraHiring&stage=Applied`) and asserts the exact ordered projection `['2028-03-01','2028-03-10','']`, then checks that a non-matching stage filter returns zero. That is a real behavioural assertion, not "the call happened".
- Test 2 proves non-destruction: after four rejected PUTs it re-fetches the record and `deepEqual`s it against the pre-edit snapshot (`test/api.test.js:14`). This is the assertion most rewrites forget.
- Same genuine client repair as its siblings — `client/src/main.jsx` is new, and `client/index.html` now loads it instead of a component module that never called `createRoot`.

## Problems found (evidence required)
- **[D8]** Template. `05-PRACTICE.md` here differs from `JS1/poll-studio/astraupskill/05-PRACTICE.md` on only the one fixture line and four exercise titles; everything else — Exercise 0, Exercises 5-6, the completion rubric — is byte-identical. `06-SOLUTIONS-AND-REVIEW.md` repeats one "Review:" paragraph under each exercise.
- **[D2]** Dead code: `whole` is defined at `server/server.js:98` and never called in this file (this project has no numeric fields); it is part of the copy-pasted helper trio. `realDate` *is* used here, so the trio was clearly pasted wholesale rather than per project.
- **[D2]** The sentinel `"9999-99-99"` is not a valid date and works only because `localeCompare` is a string comparison. That is a deliberate trick worth teaching, but `02-CONCEPTS.md` does not explain why an invalid-but-lexicographically-maximal string is safe here, nor what breaks if the date format ever stops being fixed-width ISO. A junior will copy this into a project with `MM/DD/YYYY` dates and be badly wrong.
- **[D2]** Sorting happens only on the list route, so the ordering invariant is not enforced anywhere else (e.g. `GET /api/applications/:id` neighbours, or the client's own state). Undiscussed.
- **[D8/D1]** `astraupskill/README.md` Prerequisites is the shared paragraph mentioning SQL; there is no SQL in this project. `VERIFICATION.md` Limits cites "transaction scope" and "status-command semantics" — neither exists here.
- **[D2]** `htmlFor="lesson-field-N"` ids in `client/src/App.jsx`.
- **[D5]** All dependencies `"latest"`, no lockfile.
- **[D6]** `browser-checks.json` for project 25 is a single `passed: true` with no assertion detail; the screenshot `logs/25-browser.png` exists but the claim's content is not independently checkable read-only.

## Spot-checks performed
- "The excerpt below comes from server/server.js near line 67" -> `sed -n '67p'` = `function validateApplication(req, res, next) {` and the pasted excerpt matches the file verbatim -> matches.
- "Dates March 10, March 1 and empty display as March 1, March 10, empty" -> `test/api.test.js:7-9` inserts in the order blank, 2028-03-10, 2028-03-01 and asserts `['2028-03-01','2028-03-10','']` -> matches, and I confirmed the sentinel logic at `server/server.js:34` produces that order.
- "An invalid follow-up edit returns 400 and leaves the original application identical" -> `test/api.test.js:12-14` loops `2028-02-30`, `[]`, `{}`, `42` against PUT and then `deepEqual`s the refetched record -> matches.
- Test/build counts -> `logs/25-tests.log` `# tests 2 / # pass 2 / # fail 0`; `checks.json` project 25 build `exit_code: 0` -> matches the report's "2 passing regression cases. Build and integrated browser checks passed."
- I checked whether `2028-02-30` really fails: `realDate` round-trips it to `2028-03-01`, which is not equal to the input -> rejected. Matches.

## Improvements needed (ordered, concrete, actionable)
1. Add a short subsection to `02-CONCEPTS.md` titled something like "Why a fake date sorts last": explain that `localeCompare` on fixed-width `YYYY-MM-DD` strings is equivalent to chronological order, that `"9999-99-99"` exploits that, and show the alternative (`nulls last` in SQL, or a comparator that returns `+1` for null) so the learner does not generalize the trick. (effort: S)
2. Delete the unused `whole` helper at `server/server.js:98`. (effort: S)
3. Rewrite `05-PRACTICE.md` Exercises 1-4 with pipeline-specific criteria — e.g. "add `?sort=stage` using the fixed stage vocabulary as an ordinal, and write the test that proves two applications in the same stage keep their id tie-break". (effort: M)
4. Strip the SQL/transaction boilerplate from `README.md` Prerequisites and `VERIFICATION.md` Limits. (effort: S)
5. Add a third test that pins the *stability* claim explicitly: create two applications with identical `nextStepDate`, fetch twice, assert the id order is the same both times. Today stability is implied by the tie-break but never asserted. (effort: S)
6. Rename `lesson-field-N` ids; add a lockfile. (effort: S)

## One-paragraph summary for the index
A good small lesson in two things that show up in every list endpoint: how to treat an optional field (absent, blank and malformed are three different states, not one falsy check) and how to make a sort total so results are stable across requests. The Express change is real and the two tests genuinely prove it — one asserts the exact ordered list from a combined search+filter query, the other proves four rejected edits leave the stored record byte-identical. The main gap is pedagogical: the course never explains why the `"9999-99-99"` sentinel is safe, which is precisely the kind of clever line a junior will copy into a codebase where it breaks. Chapters 5 and 6 are shared boilerplate. Keep it in the core path and pair it with the concepts fix above.
