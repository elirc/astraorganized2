import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-11-survey-builder'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# --- review #3: date window validation
def patch_validators(t):
    old = """  start_date: z.string().optional().nullable(),
  end_date: z.string().optional().nullable(),"""
    new = """  start_date: z.string().datetime({ offset: true }).optional().nullable(),
  end_date: z.string().datetime({ offset: true }).optional().nullable(),"""
    assert old in t
    return t.replace(old, new, 1)
assert fe.rw('server/src/validators/surveyValidators.ts', patch_validators)
done.append('review#3 surveySchema now requires ISO-8601 date-times for start_date/end_date (z.string().datetime({ offset: true }))')

def patch_test(t):
    add = '''
test("an unparseable survey window is rejected at write time", async () => {
  await h.db("users").insert({ id: 2, email: "owner@example.com", display_name: "Owner" }).onConflict("id").ignore();
  const bad = await request(h.origin, "/api/surveys", "POST", {
    title: "Window",
    start_date: "next tuesday",
  }, { "x-user-id": "2" });
  assert.equal(bad.status, 400);
  const good = await request(h.origin, "/api/surveys", "POST", {
    title: "Window",
    start_date: "2099-01-01T00:00:00Z",
  }, { "x-user-id": "2" });
  assert.equal(good.status, 201, JSON.stringify(good.data));
});
'''
    return t.rstrip('\n') + '\n' + add
# only add if request() supports headers; check database.ts
dbts = open('test/database.ts', encoding='utf-8-sig').read()
if 'headers' not in dbts.split('export async function request')[1][:400]:
    def patch_db(t):
        t = t.replace("export async function request(\n  origin: string,\n  path: string,\n  method = \"GET\",\n  body?: unknown,\n) {", "export async function request(\n  origin: string,\n  path: string,\n  method = \"GET\",\n  body?: unknown,\n  headers: Record<string, string> = {},\n) {", 1)
        t = t.replace('headers: body === undefined ? {} : { "Content-Type": "application/json" },', 'headers: { ...headers, ...(body === undefined ? {} : { "Content-Type": "application/json" }) },', 1)
        return t
    fe.rw('test/database.ts', patch_db)
assert fe.rw('test/responses.test.ts', patch_test)
done.append('review#3 regression test: "next tuesday" as start_date is 400, an ISO date-time is 201 (test/responses.test.ts; request() gained a headers argument)')

# --- review #2: lock granularity section
fe.append_section(S, '02', '## Why the lock is on the survey row', """`submitResponse` (`server/src/services/surveyService.ts:176`) starts a transaction and immediately runs `SELECT ... FROM surveys WHERE public_token = ? FOR UPDATE`. Everything that decides whether this response may exist, the status, the date window, the access code and `response_count >= max_responses`, is read from that locked row, and the counter increment at the end of `createResponse` writes to the same row. A second respondent blocks on the lock until the first transaction commits, then re-reads the row and sees the incremented counter. That is why the capacity test observes exactly `[201, 400]` and `response_count = 1`.

Predict what breaks with the two obvious alternatives before you read on:

- **Lock the `responses` table instead.** Every survey now waits on every other survey's respondents, and the counter check still reads an unlocked `surveys` row, so two respondents can both see `0 < 1` and both insert. Coarser lock, and still wrong.
- **No lock, check then insert.** Both respondents read `0`, both insert, both increment: `response_count = 2` with `max_responses = 1`. The classic time-of-check-to-time-of-use race.

A third design, `UPDATE surveys SET response_count = response_count + 1 WHERE id = ? AND response_count < max_responses RETURNING *` as the *first* statement, avoids `FOR UPDATE` by making the increment itself the check. It is a good exercise 3 follow-up: which of the other checks (dates, access code) can move into that `WHERE`, and which cannot?""")
done.append('review#2 02-CONCEPTS section on lock granularity with the two failing alternatives')

B = [
("the public form decides what to send",
 "`client/src/features/surveys/PublicSurveyPage.tsx`: `answers` is a `Record<number, unknown>` filled by `QuestionInput` callbacks; the form's `onSubmit` calls `submit.mutate()`, a `useMutation` whose `mutationFn` is `surveyApi.submitResponse(token, { answers })`. The page renders \"Thank you\" only when `submit.isSuccess`, so a 400 leaves the draft on screen. Note that the client sends every answer it has, including blanks; deciding what blank means is the server's job."),
("the request leaves the browser",
 "`client/src/services/api.ts:42` posts to `/public/surveys/:token/responses` through the shared axios instance and `unwrap()`s the `{ success, data }` envelope. The token in the URL is the only identity a respondent has; there is no session and no user id on this path."),
("the route validates the shape, the service validates the meaning",
 "`server/src/routes/surveyRoutes.ts:51` mounts `validateBody(responseSchema)` (`middleware/validate.ts`): `answers` must be an object keyed by strings, nothing more. `buildAnswerRows` (`services/surveyService.ts:60`) then does the real work against the survey's questions: unknown question ids, missing required answers, choices that are not in `question.options`, ratings outside `config`, all throw `ValidationError` before any row is written. The first test sends each of those and asserts the `responses` table is unchanged."),
("the service locks the survey and decides under the lock",
 "`submitResponse` (line 176): `db.transaction` -> `trx(\"surveys\").where({ public_token }).forUpdate().first()` -> `assertAccepting(survey)` (status, `start_date`, `end_date`, `max_responses` vs `response_count`) -> access code -> `listQuestions` with the same `trx` -> `buildAnswerRows`. All reads that feed a decision happen after the lock, which is what makes the capacity test deterministic."),
("the model writes three things or nothing",
 "`surveyModel.createResponse` (line 170) inserts the `responses` row, then the `response_answers` rows, then increments `response_count` and touches `updated_at` on the locked survey, all on `trx`. Knex commits when the callback resolves and rolls back when it throws; exercise 3 injects a trigger on the second insert and expects zero rows in all three tables."),
("the envelope tells the respondent what happened",
 "`utils/http.ts` `sendSuccess` answers 201 with the response row; `middleware/errors.ts` maps `ValidationError` to 400, `NotFoundError` to 404 and everything else to 500. In the browser, `useMutation` flips to `isSuccess` on 201 and exposes `error.message` otherwise; the page never re-reads the survey, because a respondent has nothing to re-read."),
]
fe.set_boundaries(S, B); done.append('review#1 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"errors must be keyed by question id from the server message or a structured `issues` array you add to `ValidationError`, rendered next to the matching `QuestionInput`, and the draft must survive the 400; a client test should assert that a required-answer error appears under the right question and disappears after the answer is filled.",
"the preview must be a pure projection of `answers` (no request, no counter change: assert `response_count` unchanged after opening the preview in a server test, or `submitResponse` not called in a client test), and it must show the option label the server will validate against, not an index.",
"install a `BEFORE INSERT` trigger on `response_answers` that raises on the second row (use `h.db.raw` in the test), send a valid two-question response, assert 500, then assert `responses`, `response_answers` and `surveys.response_count` all equal their pre-request values; explain which line of `createResponse` had already run when the error was raised.",
"the policy must say what happens to existing `response_answers` when an option is renamed or removed (`selected_option_id` becomes dangling or the row cascades), must propose immutable question revisions or a `retired_at` flag, and must show one SQL query that reports results correctly across a revision.",
]
fe.set_reviews(S, R); done.append('review#4 / 2.3 per-exercise review criteria (06)')

svc = open('server/src/services/surveyService.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
i = next(i for i, l in enumerate(svc) if 'export async function submitResponse' in l)
j = next(j for j, l in enumerate(svc) if 'function assertAccepting' in l)
excerpt = '// services/surveyService.ts:' + str(j + 1) + '\n' + '\n'.join(svc[j:j + 12]) + '\n\n// services/surveyService.ts:' + str(i + 1) + '\n' + '\n'.join(svc[i - 1:i + 22])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/62/server/src/services/surveyService.ts` with `diff --strip-trailing-cr -w`): `submitResponse` now runs inside one transaction, locks the survey row with `FOR UPDATE` before `assertAccepting` reads the counter, and `buildAnswerRows` validates every answer against the question definitions before any insert. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows the changed submitResponse and assertAccepting')

fe.set_variations(S, """**Normal variation — the last slot.** Create a survey with `max_responses: 2`, submit twice, then a third time. Predict: 201, 201, 400 `Survey response limit reached`, and `response_count = 2`. Read the row in `psql` between calls to see the counter move inside the same commit as the response.

**Invalid variation — an answer to a question that does not exist.** Submit `{ answers: { "999": "Yes" } }`. Predict: 400 `Unknown question`, and `SELECT count(*) FROM responses` unchanged. Then submit a `single_choice` answer whose label differs only in case from an option: predict whether `buildAnswerRows` accepts it (it compares labels exactly).

**Boundary variation — two respondents at once.** Reproduce the second test with `max_responses: 1` and two concurrent submits. Predict `[201, 400]` and `response_count = 1`. Then comment out `.forUpdate()` on a throwaway branch and repeat several times until you observe `[201, 201]` with `response_count = 2`; restore it and explain which read raced."""); done.append('2.4 three concrete variations')

fe.add_exercise(S, 'ownership and authorization on the owner side',
"""Respondents are anonymous by design, but survey owners are not: every `/api/surveys/:id` route trusts the demo `x-user-id` header and `getSurvey(surveyId, userId)` is the only thing standing between two owners.

1. Read `getSurvey` in `services/surveyService.ts` and write down which routes call it and which write routes reach `surveyModel` without it (questions, reorder, delete).
2. Make every question route (`POST /surveys/:id/questions`, `PUT`/`DELETE /questions/:questionId`, `PUT /surveys/:id/questions/reorder`) verify that the survey belongs to `userId` before writing, using one helper `assertOwner(surveyId, userId)` that throws `NotFoundError` (deliberately not 403: an owner should not learn that another owner's survey id exists).
3. Test: user 1 creates a survey with a question; user 2 attempts to update, reorder and delete that question and to add a new one; every call is 404 and the rows are unchanged; user 1's same calls succeed.

Acceptance is the test in step 3 plus one sentence in `02-CONCEPTS.md` on why the public respondent path must never use `x-user-id`.""",
"""Reference helper (one query, reused by every owner-side write):

```typescript
async function assertOwner(surveyId: number, userId: number, trx = db) {
  const row = await trx("surveys").select("id").where({ id: surveyId, user_id: userId }).first();
  if (!row) throw new NotFoundError("Survey not found");
}
// e.g. in updateQuestion(questionId, userId, data):
const question = await db("questions").where({ id: questionId }).first();
if (!question) throw new NotFoundError("Question not found");
await assertOwner(question.survey_id, userId);
```

Reference test skeleton: insert user 2, create a survey and a question as user 1 (`{ "x-user-id": "1" }`), then `PUT /api/questions/<id>` as user 2 -> 404 and `SELECT title FROM questions WHERE id = <id>` unchanged; `POST /api/surveys/<sid>/questions` as user 2 -> 404 and question count unchanged; the same as user 1 -> 200/201.

Review: explain why the check is done by survey id even for question routes, why 404 rather than 403 here, and what would change if the demo header were replaced by a signed session (nothing in `assertOwner`; only where `userId` comes from)."""); done.append('2.5 ownership/authz exercise 7 on the owner-side routes (05, 06)')

fe.append_section(S, '04', "## This project's test harness: `test/database.ts`", """`database()` creates a private schema in the `astra_test_*` database named by `ASTRA_TEST_DATABASE_URL`, points `DATABASE_URL` at it, then imports the Knex config and runs the migrations into that schema before importing the app; `h.db` is the same Knex instance the app uses, which is why the tests can insert users and surveys directly and read `response_count` back. `request(origin, path, method, body, headers)` returns `{ status, data }` and never throws. The capacity test proves a real race: two `POST`s in a `Promise.all` against a survey with `max_responses: 1`, then a direct read of the counter. Run with `$env:ASTRA_TEST_DATABASE_URL = "postgres://user@127.0.0.1:5432/astra_test_yourname"` then `npm test`.""", before='## '); done.append('harness walkthrough (04)')

rp = json.load(open('package.json', encoding='utf-8'))
rp['name'] = 'survey-builder-workspace'
rp.setdefault('devDependencies', {}).update({"pg": "^8.23.0", "tsx": "^4.23.13"})
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(rp, indent=2) + '\n')
done.append('review#5 root package renamed from astra-crud-workspace-62; pg and tsx declared at the root; README already carries the Toolchain block')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **3**.", "Automated test cases: **3** delivered by Astra, plus **1** added in the fix pass (date-window validation), for 4 in `test/responses.test.ts`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
