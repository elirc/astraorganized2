# JS1/recipe-studio — Fable review

- **Path:** `JS1/recipe-studio`  ·  **Wave:** 1  ·  **Stack:** Node/Express (in-memory array) + React 18 (Vite, JSX)  ·  **Batch:** B03
- **Astra's change (one line):** `validateRecipe` now validates the *nested array* before anything mutates — `ingredients` must be an array of 1-100 non-empty bounded strings, `cookTime`/`servings` must be whole numbers in range, optional `category`/`notes` are type-checked when present — and `normalizeRecipe` was changed from `String(item).trim()` + `filter(Boolean)` to a trim plus case-insensitive dedupe that keeps the **first** spelling; plus the JSON-object body guard, a testable `export const app`, and the missing React entry point `client/src/main.jsx`.
- **Course size:** 5,715 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 in `test/api.test.js` (+ `test/http.js`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 4 | 4 | 3 | 5 | 4 | 4 | 4 | 2 | 3.8 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- Validating the *elements* of a nested array is the right lesson and is rarely taught. `req.body.ingredients.every(x => isText(x,1,500))` (`server/server.js:69`) is what stops `ingredients: [{}]` from reaching the store — and the old code would have silently turned `{}` into the string `"[object Object]"` via `String(item)`.
- The dedupe preserves the first spelling rather than the last, which is the user-visible decision: `items.findIndex(other => other.toLowerCase() === item.toLowerCase()) === index` (`server/server.js:91`). `[" Salt ", "salt", "Water"]` -> `["Salt", "Water"]`, asserted directly in `test/api.test.js:7`.
- Validation genuinely precedes mutation. `validateRecipe` is wired as middleware on both `app.post` (line 37) and `app.put` (line 43), and `normalizeRecipe` is only reached from validated paths — which matters, because the new `normalizeRecipe` calls `item.trim()` with no `String()` coercion and *would throw* on a non-string element. The safety of the simplification depends entirely on the guard, which is a good thing to make a learner notice.
- Test 2 loops seven distinct malformed payloads including the two hard ones — `ingredients: [{}]` and `ingredients: []` — and asserts 400 with the payload in the failure message.
- Same real client repair as its siblings (`client/src/main.jsx` added, `client/index.html` repointed).

## Problems found (evidence required)
- **[D2] The coupling created by the change is never stated.** `normalizeRecipe` dropped its defensive `String(item)` (`backups/27/server/server.js:81` vs `server/server.js:91`). If any future caller invokes `normalizeRecipe` without `validateRecipe` in front of it, `item.trim()` throws a `TypeError` and the route 500s. This is exactly the kind of implicit contract a junior should be warned about, and `03-WORKED-CHANGE.md` does not mention it.
- **[D8]** Template. `05-PRACTICE.md` differs from the poll-studio version only in the fixture line and four exercise titles; `06-SOLUTIONS-AND-REVIEW.md` repeats one "Review:" paragraph under every exercise; `04-TESTING-AND-DEBUGGING.md` differs from `JS1/event-admin`'s on a handful of lines.
- **[D2]** Dead code: `realDate` is defined at `server/server.js:99` and never called in this file (no dates in this domain). Copy-pasted helper trio.
- **[D2]** Legacy guards now unreachable: `if (!recipe.name || recipe.name.length < 3)` (`server/server.js:72`) cannot fire after `isText(req.body.name,3)` at line 67. Two layers, two messages, one rule.
- **[D1, minor]** The report and `VERIFICATION.md` say "Ingredients must be 1-100 nonempty bounded strings". The lower bound is enforced only indirectly: `ingredients: []` fails because `every()` on an empty array returns `true`, so it passes line 69 — it is caught later by the pre-existing `recipe.ingredients.length` check. The test asserts the outcome, but the course's stated mechanism is not where the empty case is actually rejected.
- **[D8/D1]** `README.md` Prerequisites is the shared SQL-mentioning paragraph; `VERIFICATION.md` Limits cites "date representation and transaction scope" — none of which exists here.
- **[D2]** `htmlFor="lesson-field-N"` ids in `client/src/App.jsx`. **[D5]** all deps `"latest"`, no lockfile.
- **[D6]** `browser-checks.json` for project 27 is `{"passed": true}` with no assertion detail; `logs/27-browser.png` exists but the claim's content is not checkable read-only.

## Spot-checks performed
- "The excerpt below comes from server/server.js near line 66" -> `sed -n '66p'` = `function validateRecipe(req, res, next) {` and the pasted excerpt matches the file verbatim -> matches.
- "[' Salt ', 'salt', 'Water'] saves as ['Salt', 'Water']" -> `test/api.test.js:7` asserts exactly `['Salt','Water']`; I traced the dedupe at `server/server.js:91` and confirmed first-spelling-wins -> matches.
- "Servings '4' becomes numeric 4 without changing id" -> `whole("4",1,1000)` passes (`Number("4")` is a safe integer), `normalizeRecipe` does `Number(input.servings)`, and `test/api.test.js:8` asserts `edited.data.servings === 4` and `edited.data.id === made.data.id` -> matches.
- "Object ingredients, blanks, fractional servings and boolean cooking time fail" -> `test/api.test.js:12` loops `{ingredients:[{}]}`, `{ingredients:['']}`, `{ingredients:[]}`, `{servings:'bad'}`, `{servings:0.5}`, `{cookTime:true}`, `{notes:[]}` and asserts 400 for each. I verified `whole(true,...)` fails because `true` is neither a number nor a string -> matches.
- Test/build counts -> `logs/27-tests.log` `# tests 2 / # pass 2 / # fail 0`; `checks.json` project 27 build `exit_code: 0` -> matches.

## Improvements needed (ordered, concrete, actionable)
1. Add a paragraph to `03-WORKED-CHANGE.md` on the new implicit contract: `normalizeRecipe` no longer coerces, so it may only be called behind `validateRecipe`. Show the `TypeError` a learner gets if they call it directly. This is the most valuable teaching point the change created and it is currently invisible. (effort: S)
2. Delete the unused `realDate` at `server/server.js:99` and remove the unreachable legacy name/number guards so a single gate owns each rule. (effort: S)
3. Make the empty-array rule explicit: change line 69 to `req.body.ingredients.length >= 1 && req.body.ingredients.length <= 100 && ...`, so the stated "1-100" bound is actually enforced where the course says it is. (effort: S)
4. Rewrite `05-PRACTICE.md` Exercises 1-4 with recipe-specific acceptance criteria — e.g. "add quantities as `{name, amount, unit}` objects and prove the dedupe rule still keeps the first spelling but now sums amounts". (effort: M)
5. Strip the SQL/date/transaction boilerplate from `README.md` Prerequisites and `VERIFICATION.md` Limits. (effort: S)
6. Rename `lesson-field-N` ids; add a lockfile. (effort: S)

## One-paragraph summary for the index
The best "nested data" lesson in the batch: the payload has an array inside it, and the change shows how to validate the array's *elements* before anything mutates, then normalize by trimming and deduplicating case-insensitively while keeping the user's first spelling. The two API tests prove the interesting cases, including `ingredients: [{}]` and `ingredients: []`, and they check that a rejected payload never reaches the store. What the course misses is the consequence of its own simplification — `normalizeRecipe` stopped coercing with `String()`, so it is now only safe behind the validator, a contract nothing documents. As with the rest of this batch, the practice and solutions chapters are shared boilerplate and the server was left with an unused date helper and a dead legacy guard. Good core-path material with the fixes above.
