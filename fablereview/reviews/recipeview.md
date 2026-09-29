# recipeview (Recipe Lab) — Fable review

- **Path:** `recipeview`  ·  **Wave:** 1  ·  **Stack:** Node/TS, Express 4, node:sqlite (DatabaseSync) + FTS5, React/Vite  ·  **Batch:** B08
- **Astra's change (one line):** Adds a single request boundary inside the existing `h()` handler wrapper that (a) rejects any `:...id` route param that is not a canonical positive integer and (b) runs a new `validatePayload` over every POST/PATCH body (except photo uploads) so malformed nested ingredient/step/tag values are rejected before any row is touched; also tightens `isDate` to reject impossible calendar dates, maps `InputError` to 400 (everything else to a generic 500), and exports `app` so the server can be imported without binding a port.
- **Course size:** 7,690 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/recipes.test.ts`, new file; `"test": "tsx --test test/*.test.ts"` added to `package.json`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 4 | 4 | 3 | 5 | 4 | 4 | 4 | 3 | 3.9 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- The change is placed at exactly the right layer for a junior to learn from. Rather than sprinkling `if` statements into twenty handlers, it hooks the existing `h()` wrapper in `server/index.ts` so every route inherits ID canonicalisation and payload validation. That is a genuinely good architectural lesson about request boundaries.
- `validatePayload` (`server/index.ts:600`) is the kind of validator worth reading: it distinguishes "omitted" from "explicitly blank" for `qty` (`row.qty !== undefined && row.qty !== null && row.qty !== ""`), bounds arrays (300 ingredients, 50 tags), and requires `yield_qty > 0` — all domain-real constraints, not generic type checks.
- The test is a real integration test: `test/recipes.test.ts` points `RECIPE_LAB_DATA` at a fresh `mkdtemp` directory, imports the real Express app, listens on port 0 and drives it over HTTP, then asserts `deepEqual` of the whole recipe before/after five rejected PATCH bodies. That is much stronger than "the handler threw".
- `export const app` plus `if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) app.listen(...)` (`server/index.ts:594`) is the correct, teachable fix for "importing the server starts a server".
- Evidence matches: `batch04/checks.json` shows build/tests/typecheck all exit 0 for project 72, and `logs/72-tests.log` ends `# pass 3 / # fail 0`.

## Problems found (evidence required)
- **[D1/D2]** The change also rewrote error reporting and the course never mentions it. Before: `res.status(500).json({ error: String((e as Error)?.message ?? e) })`. After: `res.status(e instanceof InputError ? 400 : 500).json({ error: e instanceof InputError ? e.message : "Request failed" })`. Every non-validation failure now returns the opaque string `"Request failed"`. Meanwhile `04-TESTING-AND-DEBUGGING.md` tells the learner to debug by reading the response, and `grep -rn "Request failed" astraupskill/` returns nothing. A junior hitting a genuine 500 will get no information and no warning that the course removed it.
- **[D3]** `astraupskill/04-TESTING-AND-DEBUGGING.md:23-26` contains a stray duplicated code block — a ```` ```text ```` fence repeating `npm test` / `npm run build` four lines after the real PowerShell block that already said it. It is a template assembly bug, and it sits immediately before the chapter's substantive paragraph.
- **[D8]** `04-TESTING-AND-DEBUGGING.md:35` drops other projects into this course: *"Questboard uses Vitest and simulated browser storage; DevDeck uses Vitest with fake-indexeddb for its actual Dexie methods… Live Chat also tests a real WebSocket…"* — irrelevant to a learner working on Recipe Lab and clear evidence of a shared template. `diff recipeview/astraupskill/05-PRACTICE.md devdeck/astraupskill/05-PRACTICE.md` changes only 12 of 47 lines between two completely unrelated apps.
- **[D3]** Same structural filler as the rest of the batch: `07-TRACE-LAB.md` repeats *"Find the relevant call in the source for this project…"* 6 times and `06-SOLUTIONS-AND-REVIEW.md` repeats *"Demonstrate an ordinary case and a case that would break a naive implementation…"* 4 times.
- **[D6]** `VERIFICATION.md` says *"Node 22.16.0, PostgreSQL 18.1 where applicable"* for an app that has no PostgreSQL anywhere (it uses `node:sqlite`). Harmless but it is boilerplate pasted into a verification page, which is the one document that should be literal.
- **[D5]** The documented `npm test` (`tsx --test test/*.test.ts`) was not what ran: `batch04/checks.json` shows the check invoked `tsx --test <absolute path>/test/recipes.test.ts`. Shell glob expansion through an npm script on Windows is unverified.
- **[D2]** Roughly 90% of the `server/index.ts` diff is a single-to-double-quote Prettier reformat of a 700-line file, which buries the ~120 real lines.

## Spot-checks performed
- Course: *"The excerpt below comes from server/index.ts near line 600"* -> `grep -n "function validatePayload" server/index.ts` returns `600:function validatePayload(body: unknown) {` and the quoted body matches -> **matches**.
- Course: *"Canonical positive integer IDs reject strings such as 1e2 rather than interpreting them as another record"* -> `server/index.ts` `h()` wrapper loops `Object.entries(req.params)` and tests `/^\d+$/` on any key ending in `id`; `test/recipes.test.ts` asserts `(await api("/recipes/1e2")).status === 400` -> **matches**.
- Course: *"The browser parses kitchen fractions before sending JSON"* -> `src/pages/RecipeEditor.tsx:74,80` call `parseQty(...)` before building the payload, and `formatQty` renders it back -> **matches** (this is pre-existing behavior the course correctly describes rather than claims to have added).
- Course: *"The app can be imported without binding a development port"* -> `server/index.ts:594` guards `app.listen` behind the `import.meta.url === pathToFileURL(process.argv[1]).href` main-module check, and the test imports `{ app }` and calls `app.listen(0)` itself -> **matches**.
- Course: *"The regression suite assigns RECIPE_LAB_DATA to a fresh temporary directory before importing the database"* -> `server/db.ts:7` reads `process.env.RECIPE_LAB_DATA`, and the test sets it before the dynamic `await import("../server/db.ts")` -> **matches**, and the ordering is correct (env set before import, which is the subtle part worth teaching).

## Improvements needed (ordered, concrete, actionable)
1. Document the error-handling change. Add a short section to `03-WORKED-CHANGE.md` and a line to `VERIFICATION.md` explaining that `fail()` now returns `"Request failed"` for non-`InputError` failures, why (not leaking internals), and how to get the real message while debugging (the `console.error(e)` in `fail()` — tell the learner to read the server terminal, not the browser). (effort: S)
2. Delete the duplicated ```` ```text ```` block at `astraupskill/04-TESTING-AND-DEBUGGING.md:23-26`. (effort: S)
3. Remove the Questboard/DevDeck/Live Chat paragraph from `04-TESTING-AND-DEBUGGING.md:35` and replace it with one sentence about this project's own harness (real Express over HTTP + temp SQLite dir). (effort: S)
4. Add a fourth test covering the ID-canonicalisation rule on a *write* path (e.g. `PATCH /api/recipes/1e2` and `PATCH /api/dishes/01`), since today only a GET is asserted; and add one asserting that a rejected body leaves `search_index` untouched for a dish rename. (effort: S)
5. Fix `VERIFICATION.md` to drop "PostgreSQL 18.1 where applicable" and state the real toolchain: Node >= 22.16 for `node:sqlite`, no database server. (effort: S)

## One-paragraph summary for the index
Recipe Lab is one of the better courses to actually do: it is a small, readable Express + SQLite app, and the change teaches a lesson that transfers directly to any Node CRUD job — put validation at one request boundary instead of scattering it, and distinguish "field omitted" from "field deliberately blank" when replacing child rows. The three tests are real integration tests against the live app with a throwaway database, and the evidence backs the claims. Two things to fix before handing it to a junior: the course silently changed all 500-level error bodies to the opaque string "Request failed" without telling the reader, and the testing chapter has a duplicated code block plus a paragraph about three unrelated projects. Budget a few hours; you need Node 22.16+ and nothing else.
