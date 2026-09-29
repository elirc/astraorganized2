# newcodexJS/10-inventory-management — Fable review

- **Path:** `newcodexJS/10-inventory-management`  ·  **Wave:** 1  ·  **Stack:** Node/Express + Knex/Postgres + React/Vite, TypeScript  ·  **Batch:** B07
- **Astra's change (one line):** Replaced hand-rolled field picking with a zod create/partial-update schema (trim, length bounds, case-insensitive tag dedupe), fixed a broken `whereRaw("CAST(products AS TEXT) ILIKE ?")` search with per-column `orWhereILike`, added an `id` tie-break to the list sort, made `tags` explicitly `JSON.stringify`-ed before insert/update, and made update/delete of a missing row return 404 instead of `undefined`.
- **Course size:** 8,086 words across 9 files  ·  **Tests claimed:** 4  ·  **Tests found on disk:** 4 (`test/crud.test.ts`, 4 `test(...)` blocks)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 4 | 4 | 3 | 5 | 4 | 4 | 4 | 2 | 3.8 |

**Verdict:** IMPROVE    **Path role:** elective

## What Astra did well
- The change is a genuine correctness fix, not cosmetics. The old search was `builder.whereRaw("CAST(products AS TEXT) ILIKE ?", ...)` (backup `server/src/models/model.ts:4`), which casts the whole row to text; it is now a grouped `orWhereILike` over `sku,name,category,status` (`server/src/models/model.ts:9-16`).
- 404-on-missing is now enforced at the service layer for update and delete (`server/src/services/service.ts`, `update`/`remove` both `throw new NotFoundError`), and the test asserts the whole sequence: delete → 200, GET → 404, DELETE again → 404, PUT → 404 (`test/crud.test.ts`, last test).
- Every code excerpt in `03-WORKED-CHANGE.md` is verbatim present in the source: I extracted all 42 substantive code lines from its fenced blocks and matched 42/42 against the project's `.ts`/`.tsx` files.
- Test harness is real, not mocked: `test/database.ts` creates a random Postgres schema, runs the actual migrations, boots the real Express app on a random loopback port, then drops the schema. It also refuses any database whose name does not start with `astra_test_`.

## Problems found (evidence required)
- **[D8]** This course is a noun-swapped clone of the 58–60 family. `03-WORKED-CHANGE.md` is 97.7% character-identical to `newcodexJS/09-job-application-tracker/astraupskill/03-WORKED-CHANGE.md`; `05-PRACTICE.md` 97.6%; `README.md` 99.1%. The scope paragraph ("Create and partial-update schemas validate editable fields. Tags are trimmed, bounded and deduplicated…") is reproduced word-for-word for stages 58, 59, 60 and 61 in `astrdocs/NEXT_25_IMPLEMENTATION_REPORT.md`.
- **[D3]** `07-TRACE-LAB.md` "Trace the real call path" lists six boundaries whose bodies are byte-identical and all point at the same place: "Find the relevant call in the source for this project, starting with [server/src/services/service.ts](../server/src/services/service.ts) and `parsePayload`." appears 6 times. A learner asked to trace "the React form" is sent to the server validator.
- **[D1/D6]** `VERIFICATION.md` "Tested behavior" says `PUT only {"sku":"Revised lesson"}` and "Reject a numeric sku"; the actual test uses `{ sku: "Revised fixture" }` and rejects `{ sku: {} }` / `{ sku: " " }` / `{ sku: "x".repeat(256) }` — no numeric case exists (`test/crud.test.ts`).
- **[D1/D5]** Repeated three times (04, 07, VERIFICATION): "The root workspace also makes pg and tsx available to the root test directory." The root `package.json` declares only `{"concurrently": "^9.1.2"}` as a devDependency; `pg` and `tsx` resolve only by npm workspace hoisting from `server/`, which is an implementation detail, not a declared guarantee.
- **[D2]** 20 of the 34 touched files are dominated by Prettier reformatting (e.g. `server/src/models/storeModel.ts`-style whitespace churn here in `errorMiddleware.ts`, `response.ts`, `tsconfig.json`), which inflates the "34 changes" headline relative to the ~4 files that carry behavior.

## Spot-checks performed
- Claim: "the model serializes JSON arrays explicitly" -> read `server/src/models/model.ts` `databasePayload()`: `payload.tags === undefined ? payload : { ...payload, tags: JSON.stringify(payload.tags) }` -> matches.
- Claim: tags are deduplicated case-insensitively -> read `recordSchema.tags.transform` using `new Map(values.map(v => [v.toLowerCase(), v]))` and test asserting `["one","ONE","two"] -> ["ONE","two"]` -> matches (last-wins, which the course does not mention).
- Claim (VERIFICATION table): "Chromium interaction | Passed" -> `astrafinalplan/implementation/batch04/browser-checks.json` has `{"project":"61","passed":true,"api":"actual isolated HTTP server","api_requests":8,"responsive":{"content":390,"viewport":390}}` -> matches.
- Claim: "Automated test cases: 4" -> `logs/61-tests.log` shows `# tests 4 / # pass 4 / # fail 0`, and `grep -c '^test('` on disk returns 4 -> matches.
- Claim: list ordering is stable -> `.orderBy("created_at","desc").orderBy("id","asc")` present -> matches, but no test asserts the tie-break (the "stable ordering" test only checks filter composition).

## Improvements needed (ordered, concrete, actionable)
1. De-clone the family. Keep exactly one of 07-blog-platform / 08-kanban-board / 09-job-application-tracker / 10-inventory-management in the path and delete or stub the other three `astraupskill/` folders; if all four stay, rewrite `02-CONCEPTS.md`, `05-PRACTICE.md` and `06-SOLUTIONS-AND-REVIEW.md` around domain-specific invariants (SKU uniqueness, stock quantity, reorder points) rather than generic "tags" prose. (effort: M)
2. Rewrite `07-TRACE-LAB.md` "Boundary 1..6" so each boundary names its own file: 1 → `client/src/App.tsx` submit handler, 2 → `client/src/services/api.ts`, 3 → `server/src/services/service.ts:parsePayload`, 4 → `server/src/models/model.ts:updateRecord`, 5 → Knex/Postgres, 6 → `server/src/utils/response.ts`. (effort: S)
3. Fix `VERIFICATION.md` "Tested behavior" to quote the actual fixture (`"Revised fixture"`) and the actual rejected payloads (`{}`, `{sku:{}}`, `{tags:[""]}`). (effort: S)
4. Add `pg` and `tsx` to the root `package.json` devDependencies, or change the three copies of the hoisting sentence to say the tests rely on workspace hoisting from `server/`. (effort: S)
5. Add one assertion for the `orderBy("id","asc")` tie-break (insert two rows with the same `created_at`, assert the returned order), and document the last-wins tag-dedupe rule in `02-CONCEPTS.md`. (effort: S)

## One-paragraph summary for the index
A small Express + Knex + Postgres product catalogue where the lesson is input validation at the service boundary: a zod create/partial-update schema, trimmed and deduplicated tag arrays, explicit JSON serialization before the insert, a stable list sort, and 404 instead of silence when you update or delete a row that is gone. The four tests are real end-to-end HTTP tests against a throwaway Postgres schema, and every code excerpt in the course matches the file on disk. The catch is that this course is a 97%+ character-for-character clone of the blog-platform, kanban-board and job-application-tracker courses, so doing all four teaches you the same lesson four times. Do one of them, and prefer this one only if inventory is the domain you care about. Budget one focused session, and expect the trace-lab chapter to be the weakest part.
