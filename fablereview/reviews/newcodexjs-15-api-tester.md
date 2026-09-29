# newcodexJS/15-api-tester — Fable review

- **Path:** `newcodexJS/15-api-tester`  ·  **Wave:** 1  ·  **Stack:** Node/Express + Knex/Postgres + zod + React/Vite, TypeScript  ·  **Batch:** B07
- **Astra's change (one line):** `createEnvironment`, `updateEnvironment` and `activateEnvironment` in `server/src/models/environmentModel.ts` now all run in a transaction that first takes `SELECT … FOR UPDATE` on the owner's `users` row, verify the target belongs to the caller (404 otherwise) *before* clearing `is_active` on the user's other rows, so the "exactly one active environment per user" invariant survives concurrent activations; `replaceVariables` locks its environment, rejects duplicate trimmed keys before deleting anything, and saved-request `headers`/`params` are `JSON.stringify`-ed into JSONB in both seeds and CRUD writes.
- **Course size:** 8,041 words across 9 files  ·  **Tests claimed:** 4  ·  **Tests found on disk:** 4 (`test/environments.test.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 3 | 4 | 4 | 5 | 4 | 4 | 4.1 |

**Verdict:** KEEP    **Path role:** elective

## What Astra did well
- The verify-then-mutate ordering bug was real. The backup `activateEnvironment` ran `await trx("environments").where({user_id}).update({is_active: false})` **first** and only then tried to activate `{id, user_id}` — so activating someone else's (or a nonexistent) environment left the user with *zero* active environments. The new code reads the target, throws `NotFoundError` if it is missing, and only then clears the flags. Test 1 ("failed activation preserves the previous active environment") asserts exactly that, using both a foreign ID and `999999`.
- The atomicity of `replaceVariables` is genuinely improved: duplicate-key detection (`new Set(keys).size !== keys.length` on *trimmed* keys) runs before the `delete`, so a rejected replacement leaves the prior set intact. Test 3 proves it by sending `KEY` and `" KEY "`, asserting 400, then asserting the pre-existing `BASE_URL` row is still the only row.
- Clearing is treated as a distinct, legitimate operation rather than an error: `PUT …/variables` with `[]` returns 200 and leaves zero rows, which is exactly the "omission vs explicit empty" distinction `02-CONCEPTS.md` argues for.
- The JSON-array serialization fix is applied consistently in both the seed and the CRUD path; test 4 asserts `headers`/`params` survive create, *partial* edit and duplicate as real arrays (`assert.deepEqual(edit.data.data.params, [{key:"limit", value:"2"}])`).
- The security framing is honest: "Environment values may include secrets in normal use. The teaching examples use synthetic localhost URLs, not credentials. This task does not send proxy requests to external services."
- All 58 substantive code lines in `03-WORKED-CHANGE.md` matched verbatim against the project's `.ts` sources (58/58).

## Problems found (evidence required)
- **[D2]** The serialization strategy is a user-level lock: all three environment writers begin `await trx("users").where({ id: userId }).forUpdate().first()`. This serializes every environment write for a user, including writes to unrelated environments, and it locks a row in a table the operation does not modify. It works, and the report is honest that environments "serialize on the owner row", but neither `02-CONCEPTS.md` nor `03-WORKED-CHANGE.md` discusses the cost or the alternatives (a partial unique index `… WHERE is_active`, or locking the environments of that user with `FOR UPDATE` + `ORDER BY id`). A junior will copy this pattern into places where it is wrong.
- **[D4]** The domain is the weakest CRUD fit in the batch: "one active environment per user" and `{{variable}}` interpolation are niche developer-tooling concerns rather than the validation/ownership/pagination core the target learner needs. The transaction and verify-before-mutate lessons transfer; the domain does not.
- **[D3]** `07-TRACE-LAB.md` "Trace the real call path" lists six differently-labelled boundaries followed by six byte-identical paragraphs all pointing at "starting with [server/src/models/environmentModel.ts](../server/src/models/environmentModel.ts) and `activateEnvironment`".
- **[D3/D8]** Every exercise in `06-SOLUTIONS-AND-REVIEW.md` carries the identical "**Review:** Demonstrate an ordinary case and a case that would break a naive implementation…" paragraph.
- **[D8]** The shared chapters dominate: `04-TESTING-AND-DEBUGGING.md`, `05-PRACTICE.md` and most of `02-CONCEPTS.md` are the same batch-wide template with the scope sentence swapped; the only fully bespoke chapter is `03-WORKED-CHANGE.md`.
- **[D5]** Root `package.json` declares only `{"concurrently": "^9.1.2"}` though `test/database.ts` imports `pg`; the repeated claim "The root workspace also makes pg and tsx available to the root test directory" holds only through npm hoisting. No Node/Postgres version is pinned in `README.md`.

## Spot-checks performed
- Claim (`VERIFICATION.md`): "Concurrently activate Local and Staging: only one ends active for that user" -> read test 2: `Promise.all` of two activations, asserts both return 200, then asserts `where({user_id: 1, is_active: true})` has length 1, and separately that user 2's environment is untouched -> matches.
- Claim: "The target is verified before clearing active flags" -> read `environmentModel.activateEnvironment`: `const target = await trx("environments").where({id, user_id}).first(); if (!target) throw new NotFoundError(...)` precedes the `update({is_active:false})` -> matches, and is the inverse of the backup's order.
- Claim: "rejects duplicate normalized keys and preserves the prior set on failure" -> read `replaceVariables`: `const keys = variables.map(v => String(v.key).trim()); if (new Set(keys).size !== keys.length) throw new ValidationError("Variable keys must be unique")` placed before `.delete()` -> matches.
- Claim: "Saved-request headers and parameters are serialized as JSONB arrays in seeds and CRUD writes" -> diffed `server/db/seeds/001_api_tester_seed.ts` against the backup; `headers: JSON.stringify(request.headers)` / `params: JSON.stringify(request.params)` are new -> matches.
- Claim: "Automated test cases: 4" -> `batch04/logs/66-tests.log` shows `# tests 4 / # pass 4 / # fail 0`; `grep -c '^test('` returns 4 -> matches.
- Claim (VERIFICATION table): "Chromium interaction | Passed" -> `batch04/browser-checks.json` `{"project":"66","passed":true,"api":"actual isolated HTTP server","api_requests":3}` -> matches.

## Improvements needed (ordered, concrete, actionable)
1. Add a section to `02-CONCEPTS.md` justifying the owner-row lock: what it serializes, what it costs, and two alternatives — a Postgres partial unique index (`CREATE UNIQUE INDEX … ON environments (user_id) WHERE is_active`) that makes the invariant a database constraint, and locking the user's environment rows in ID order. Without this the course teaches a pattern with no stated boundary. (effort: M)
2. Rewrite `07-TRACE-LAB.md` "Boundary 1..6" to name distinct code: 1 the environment switcher in `client/src/`, 2 the client fetch layer, 3 `middleware/validate.ts` + `validators/schemas.ts`, 4 `services/environmentService.ts`, 5 `models/environmentModel.ts`'s transaction, 6 `errorMiddleware.ts`. (effort: S)
3. Demote this to an elective in the path and add one sentence to `README.md` "What you will be able to do" that names the transferable skill ("verify ownership before mutating siblings; make a uniqueness invariant explicit") rather than the tool domain. (effort: S)
4. Replace the four identical "**Review:**" paragraphs in `06-SOLUTIONS-AND-REVIEW.md` with per-exercise criteria, and give `04-TESTING-AND-DEBUGGING.md` project-specific debugging (JSONB round-tripping, `{{var}}` interpolation in `utils/interpolate.ts`, proxy timeouts). (effort: M)
5. Pin Node/Postgres in `README.md` and add `pg` + `tsx` to the root `package.json` devDependencies. (effort: S)

## One-paragraph summary for the index
A Postman-style API client whose backend had two classic bugs: activating an environment cleared every other `is_active` flag *before* checking that the target existed, so a bad ID left you with no active environment; and replacing an environment's variables deleted the old rows before validating the new ones. The fix is a transaction that verifies ownership first and validates before destroying, plus consistent JSONB serialization for saved-request header and parameter arrays. The four tests are real HTTP tests against a disposable Postgres schema, including a concurrent double-activation that asserts exactly one row stays active. Take this as an elective rather than a core stop — the verify-before-mutate lesson is excellent, but the domain is developer tooling and the chosen serialization mechanism (locking the owner's `users` row) is a pattern the course never critiques.
