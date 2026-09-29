# recipeweb — Fable review

- **Path:** `recipeweb`  ·  **Wave:** 1  ·  **Stack:** React 19 + TypeScript + Vite (node:test via tsx)  ·  **Batch:** B01
- **Astra's change (one line):** Added `src/store/shoppingState.ts` — a `normalizeShoppingState(value: unknown, recipes)` function that treats persisted browser storage as untrusted input (drops unknown/duplicate slugs, non-boolean checks, orphaned or >100-char quantity overrides) plus `ingredientsWithQuantities()` so the rendered list and the clipboard text use the same effective quantities; wired through `ShoppingListContext` and a labelled per-ingredient quantity input in `IngredientChecklist.tsx`.
- **Course size:** 5,243 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/shopping-state.test.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 4 | 4 | 5 | 5 | 4 | 3 | 4.4 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The central idea is exactly right for the target profile and is stated in the code itself: `/** Treat browser storage as untrusted input, while retaining valid v1 data. */` (`src/store/shoppingState.ts:7`). The function is a hand-written runtime schema — the same job Zod does on a server — applied to a source juniors habitually trust.
- The validation is genuinely defensive and each branch is tested: non-object/array input → empty state; slugs filtered against the real recipe list and de-duplicated via `new Set`; a `validKeys` set built from `${slug}:${index}` so orphaned `checked`/`quantities` keys cannot survive; type checks on each value; a 100-character bound on overrides.
- Test 3 is a proper hostile-input lab: it loops `[null, [], 3, { recipeSlugs: [{}], checked: [] }]` and asserts the empty state each time, then asserts a 101-character override and a `soup:1` key that does not exist are both dropped. Test 2 proves the source recipe is *not* mutated (`recipes[0].ingredients[0].quantity === '1 cup'`) — the separation of override from source data is the actual lesson.
- Best-verified project in the batch. `checks.json` records four independent stage-05 checks — `tests` (tsx, exit 0), `build` (`npm run build` = `tsc -b && vite build`, exit 0), `lint` (`oxlint`, exit 0) and a real Chromium browser check — and `VERIFICATION.md` lists all four. Nothing is claimed that the evidence does not support.
- Reproducibility is solid: `tsx@^4.16.2` is declared in `devDependencies` and present in `package-lock.json`, so `npm install && npm test` genuinely works from a clean clone.

## Problems found (evidence required)
- **[D4]** The change is client-side state hygiene, not persistence: there is no server, no transaction, no ownership. It teaches the *validation* pillar well and the *persistence* pillar only as localStorage. A junior will still need the `newcodexJS` API courses for the rest.
- **[D8]** Same batch-wide template. `02-CONCEPTS.md` differs from the other nine courses in 4 lines out of 41; `05-PRACTICE.md`'s exercise scaffolding ("Close the worked-change chapter while implementing. Describe your design in three sentences…") is byte-identical across all ten projects. `06-SOLUTIONS-AND-REVIEW.md` repeats the same "Review: Demonstrate an ordinary case and a case that would break a naive implementation…" line under every exercise.
- **[D3]** `03-WORKED-CHANGE.md`'s "Three variations to work through" supplies no actual variations — only generic instructions to invent them. For a function with this many rejection branches that is a wasted opportunity.
- **[D6, minor]** `VERIFICATION.md:22` carries the shared environment paragraph, including "Database suites ran against a fresh, separate PostgreSQL 18.1 instance" — irrelevant to this project. The check table above it is accurate, so this is boilerplate rather than an overclaim.
- **[D2, minor]** `normalizeShoppingState` is dense — the `recipeSlugs` expression is a single ~200-character line combining `Array.isArray`, `filter`, a type predicate and `new Set`. For a course aimed at juniors the worked chapter should unpack that line rather than present it whole.

## Spot-checks performed
- Course claim (`03-WORKED-CHANGE.md`): excerpt from `src/store/shoppingState.ts` "near line 8". -> `sed -n '7,8p' src/store/shoppingState.ts` — the JSDoc is line 7 and `export function normalizeShoppingState(value: unknown, recipes: Recipe[])` is line 8. -> **matches.**
- Course claim (`README.md` Scope): "Shoppers can edit quantities using labeled keyboard-accessible controls." -> `src/components/IngredientChecklist.tsx:53-58` wraps the `<input type="text" maxLength={100}>` in a `<label className="quantity-control">` containing the text `Quantity for {ing.item}`. -> **matches** (a real `<label>`, not an `aria-label` on a div).
- Course claim (`VERIFICATION.md`): "The source ingredient says \"1 cup\" … The source recipe continues to say \"1 cup\"." -> `test/shopping-state.test.ts` test 2 asserts `ingredientsWithQuantities(...)[0].quantity === '2 1/2 cups'` and `recipes[0].ingredients[0].quantity === '1 cup'`. -> **matches.**
- Course claim (`README.md`): "Run `npm test` for its automated checks and `npm run build` for the production build." -> `package.json:8,11` define `"build": "tsc -b && vite build"` and `"test": "tsx --test test/*.test.ts"`; `tsx` is in `devDependencies` and in `package-lock.json`. -> **matches** (commands are runnable from a clean install).
- Course claim (`VERIFICATION.md` table): tests + build + lint + Chromium all passed. -> `implementation/checks.json` has stage-05 entries for `tests`, `build` and `lint` all at exit 0, and `browser-checks.json` has project "05" passed. -> **matches.**
- Delivery claim: 3 test cases, 5,243 words. -> 3 `test(` blocks; `wc -w astraupskill/*` totals 5,243. -> **matches.**

## Improvements needed (ordered, concrete, actionable)
1. Add a worked walkthrough of the `recipeSlugs` line in `03-WORKED-CHANGE.md`, decomposed into its four steps (is-array guard → type-predicate filter → membership check against `recipes` → `Set` dedupe), with the input/output for one bad value at each step. As written the densest line in the change is presented without explanation. Effort: S.
2. Replace "Three variations to work through" with three concrete fixtures and their expected normalized output: `{recipeSlugs: ['soup'], quantities: {'soup:0': 0}}` (wrong type), a slug that exists but whose ingredient count shrank, and a `checked` value of `'true'` as a string. Effort: S.
3. Add a chapter-2 paragraph bridging to the server: "the same job on an API is done by a schema library — see `newcodexJS/06-bookmark-manager` for Zod and `newcodexJS/05-recipe-manager` for hand-written nested validation." This is what makes the lesson transfer to CRUD work. Effort: S.
4. Add a fourth test covering the schema-migration case the course implies (a stored v1 document whose recipe has since lost an ingredient, so `soup:2` becomes orphaned) — currently only a synthetic orphan key is tested. Effort: S.
5. Strip the PostgreSQL/Recipeweb sentences from the shared paragraph at `VERIFICATION.md:22`. Effort: S.

## One-paragraph summary for the index
The best-verified course in this batch and the best React/TypeScript one: it adds a hand-written runtime schema over localStorage so a tampered or stale saved shopping list cannot poison the app, and a per-ingredient quantity override that the screen and the clipboard both read through one function. All six spot-checks passed, `tsx` is properly declared so `npm install && npm test` works from a clean clone, and the verification table is backed line-for-line by tests, build, lint and a real Chromium run in the evidence JSON. Its limits are that it is client-only — no server, transactions or authorization — and that the densest line in the change is presented without being unpacked. Budget three hours; do it as the TypeScript entry point before the `newcodexJS` Postgres API courses.
