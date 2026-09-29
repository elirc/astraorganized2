# newcodexJS/11-survey-builder — Fable review

- **Path:** `newcodexJS/11-survey-builder`  ·  **Wave:** 1  ·  **Stack:** Node/Express + Knex/Postgres + zod + React/Vite, TypeScript  ·  **Batch:** B07
- **Astra's change (one line):** `submitResponse` now opens a transaction, takes `SELECT … FOR UPDATE` on the survey row, then re-checks status / start_date / end_date / `max_responses` inside that lock; `buildAnswerRows` was rewritten from a lenient coercer into a per-question-type validator (unknown question IDs, unknown choice labels, non-integer or out-of-range ratings, matrix rows/columns, ISO dates, 20k text cap) that treats blank-but-optional as an explicit `null` instead of `0`/`""`.
- **Course size:** 7,900 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/responses.test.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 3 | 5 | 4 | 5 | 4 | 4 | 4.4 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The capacity race is fixed at the right layer and tested as a race. `server/src/services/surveyService.ts:176-182` opens `db.transaction`, does `trx("surveys").where({public_token: token}).forUpdate().first()`, and only then calls `assertAccepting(survey)`. The old code read the survey outside any transaction (`getPublicSurvey` in the backup) and opened a transaction only for the write.
- The test actually races: `Promise.all([1,2].map(() => api(...)))` against `max_responses: 1`, asserting `[201, 400]` **and** `response_count === 1` (`test/responses.test.ts`, "simultaneous respondents cannot exceed the last available slot"). That is an invariant assertion, not a "the call happened" assertion.
- The blank-vs-zero distinction is the most valuable idea here and it is both implemented and asserted: an empty string for an optional rating returns 201 and stores `rating_value: null`, while `9` on a 1–5 rating returns 400 (`test/responses.test.ts`, third test).
- The course is honest about what it did not fix: "The app still uses a demo owner header for administrative routes. Concurrent editing of question definitions and full administrative authorization deserve their own design" (`07-TRACE-LAB.md`, "Explain the design tradeoff").
- All 46 substantive code lines in `03-WORKED-CHANGE.md` matched verbatim against the project's `.ts` sources (46/46).

## Problems found (evidence required)
- **[D3]** `07-TRACE-LAB.md` "Trace the real call path" has six boundaries — "A React form, button or test sends…", "The client serializes…", "The server validates…", "The repository or model…", "The storage boundary commits…", "The response or broadcast…" — followed by six byte-identical paragraphs that all say "starting with [server/src/services/surveyService.ts](../server/src/services/surveyService.ts) and `submitResponse`". Five of the six pointers are wrong for the boundary they label.
- **[D3/D8]** `06-SOLUTIONS-AND-REVIEW.md` gives every exercise the same "**Review:**" paragraph ("Demonstrate an ordinary case and a case that would break a naive implementation…"), so the review criteria carry no per-exercise information.
- **[D8]** Chapters 04, 05 and 07 are mostly shared boilerplate: `04-TESTING-AND-DEBUGGING.md` is 92.8% character-identical to `newcodexJS/10-inventory-management`'s, `05-PRACTICE.md` 85.0%, `07-TRACE-LAB.md` 81.3%. Only `03-WORKED-CHANGE.md` (12.6% similarity to the neighbouring chat-polling course) is genuinely bespoke.
- **[D5]** The setup block pins nothing. `README.md` "Start the project" gives `npm install` and a `DATABASE_URL`; the toolchain versions (Node 22.16.0, PostgreSQL 18.1) appear only in `VERIFICATION.md` "Environment and scope". The root `package.json` declares only `{"concurrently": "^9.1.2"}` while `test/database.ts` imports `pg` directly, so `npm test` works only via workspace hoisting.
- **[D2, minor]** `assertAccepting` uses `new Date(survey.start_date).getTime() > now`, but `surveyValidators.ts:13-14` still types `start_date`/`end_date` as bare `z.string().optional().nullable()`. An admin can store `"not-a-date"`; `Date.parse` yields `NaN`, both comparisons are false, and the window silently stops applying. The course discusses instants-vs-dates but never mentions this gap.

## Spot-checks performed
- Claim (`VERIFICATION.md`): "Two submissions to max_responses=1 produce one 201 and one 400" -> read the second test; it asserts `results.map(r=>r.status).sort()` deep-equals `[201,400]` and re-reads `response_count` from the DB -> matches.
- Claim: "Submission locks the survey, validates answers against its questions, writes response/answers and increments the counter in one transaction" -> read `surveyService.ts:176-192` (`forUpdate`, `listQuestions(survey.id, trx)`, `surveys.createResponse(trx, …)`) and `surveyModel.ts:170-193` (insert response, insert answers, `.increment("response_count", 1)` all on `trx`) -> matches.
- Claim: "Optional blank ratings stay null" -> `buildAnswerRows` returns `{ ...base, answer_text: null }` for blank optional answers; the test reads `response_answers.rating_value === null` -> matches.
- Claim: "Automated test cases: 3" -> `batch04/logs/62-tests.log` shows `# tests 3 / # pass 3 / # fail 0`; `grep -c '^test('` on disk returns 3 -> matches.
- Claim (VERIFICATION table): "Chromium interaction | Passed" -> `batch04/browser-checks.json` `{"project":"62","passed":true,"api":"actual isolated HTTP server","api_requests":4}` -> matches.

## Improvements needed (ordered, concrete, actionable)
1. Rewrite the six boundary sections in `07-TRACE-LAB.md` so each names distinct code: 1 the public response form in `client/src/`, 2 the fetch in the client API module, 3 `validateBody(responseSchema)` in `server/src/middleware/validate.ts`, 4 `surveyService.submitResponse` + `buildAnswerRows`, 5 `surveyModel.createResponse` inside the transaction, 6 the `utils/http.ts` envelope. (effort: S)
2. Add a section to `02-CONCEPTS.md` on why `FOR UPDATE` on the survey row is the right lock granularity and what breaks if you lock the responses table instead — this is the course's best idea and is currently one sentence in the trace lab. (effort: S)
3. Tighten `surveyValidators.ts` `start_date`/`end_date` to `z.string().datetime()` (or add an `isFinite(Date.parse())` refinement) and add a test that an unparseable window is rejected at write time; if not fixed, list it as a known gap in `06-SOLUTIONS-AND-REVIEW.md`. (effort: S)
4. Replace the four identical "**Review:**" paragraphs in `06-SOLUTIONS-AND-REVIEW.md` with per-exercise acceptance criteria. (effort: S)
5. Pin the toolchain in `README.md` "Start the project" (Node 22.x, PostgreSQL 18.x) and add `pg` + `tsx` to the root `package.json` devDependencies so `npm test` does not depend on hoisting. (effort: S)

## One-paragraph summary for the index
This is the strongest concurrency lesson in the batch: a public survey endpoint that must accept the last response exactly once while validating free-form answers against per-question definitions. You will read a real `SELECT … FOR UPDATE` on the survey row, see why the capacity check has to live inside the same transaction as the counter increment, and learn the difference between "blank" and "zero" for an optional rating. The three tests run real HTTP against a disposable Postgres schema, and one is a genuine two-request race with an invariant assertion rather than a mock. Budget one long session; skim the trace-lab chapter, whose six "boundaries" are identical mislabelled paragraphs, and read `03-WORKED-CHANGE.md` and `test/responses.test.ts` closely instead.
