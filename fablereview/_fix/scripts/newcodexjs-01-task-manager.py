import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-01-task-manager'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

RUN = """From the `server` folder, install dependencies once (`npm install`) and run `npm test`. The suite needs a PostgreSQL role that can `CREATE SCHEMA` in a database whose name starts with `astra_test_`; it creates a private schema per run and drops it afterwards. Point it at that database with `ASTRA_TEST_DATABASE_URL` (PowerShell: `$env:ASTRA_TEST_DATABASE_URL = "postgres://postgres:local-test@127.0.0.1:5432/astra_test_learning"`).

No local PostgreSQL? Use a throwaway container and create the database once:

```powershell
docker run --rm -d --name astra-pg -e POSTGRES_PASSWORD=local-test -p 5432:5432 postgres:18
docker exec astra-pg createdb -U postgres astra_test_learning
```

The `postgres` superuser has the `CREATE SCHEMA` privilege the harness requires. Stop it with `docker stop astra-pg` when you are done; nothing persists."""

def fix04(t):
    t = fe.replace_section(t, r'Run the checks', RUN) or t
    return t
fe.rw(fe.chapter(S, '04'), fix04)
done.append('review#1/#2 04 "Run the checks" rewritten: no circular pointer, Docker fallback, CREATE SCHEMA privilege named')

# review #3: description bound (already in code) — add the empty-body test if missing (review #5 too)
tst = 'server/test/tasks.test.cjs'
t = open(tst, encoding='utf-8-sig').read()
if 'At least one task field' not in t:
    def patch_test(t):
        add = '''
test("an update with no editable fields is a 400 and changes nothing", async () => {
  const created = await api.request("POST", "/api/tasks", { title: "Untouched", priority: "low" });
  assert.equal(created.status, 201);
  const id = created.body.data.id;
  const before = await db("tasks").where({ id }).first();
  const empty = await api.request("PUT", `/api/tasks/${id}`, {});
  assert.equal(empty.status, 400);
  assert.match(empty.body.error?.message ?? JSON.stringify(empty.body), /At least one task field/);
  assert.deepEqual(await db("tasks").where({ id }).first(), before);
});
'''
        return t.rstrip('\n') + '\n' + add
    assert fe.rw(tst, patch_test)
    done.append('review#5 new test: PUT {} is 400 "At least one task field must be provided." and the row is unchanged')
done.append('review#3 description bound (5000 characters) already present in normalizeDescription with a test case; verified, not re-added')

# review #4: honest title + what actually changed
fe.rw(fe.chapter(S, 'README'), lambda t: t.replace('# Task Manager API: a complete CRUD boundary', '# Task Manager API: a small validation change, tested as a complete CRUD boundary', 1))
fe.append_section(S, 'README', '## What actually changed', """Read the diff before the prose: compare `AstraOrganized2/astrafinalplan/implementation/backups/07/server/src/services/taskService.js` with the current file using `diff --strip-trailing-cr -w`. The production change is three hunks and a handful of lines in `normalizeTitle` / `normalizeDescription` (length bounds) and `buildUpdatePayload` (the "at least one field" guard and the unchanged-overdue-date rule). What is large is the *test suite* in `server/test/tasks.test.cjs`, which drives the real Express app over HTTP against a disposable PostgreSQL schema: that is the thing this course teaches you to read and extend.""", before='## Reading and practice order')
done.append('review#4 README title is honest and a "What actually changed" section points at the three hunks')

fe.set_variations(S, """**Normal variation — a bounded title.** `PUT /api/tasks/:id` with `{ "title": "x".repeat(255) }`: predict 200. Then `{ "title": "x".repeat(256) }`: predict 400 with the message from `normalizeTitle`, and the row unchanged (`SELECT title FROM tasks WHERE id = ...`).

**Invalid variation — an impossible date.** `PUT` with `{ "due_date": "2099-02-30" }`. Predict 400 from `normalizeDueDate` and no write. Then submit the task's *existing* overdue date unchanged with a new title: predict 200, because the rule only rejects a *new* past date (third test).

**Boundary variation — nothing to update.** `PUT` with `{}`. Predict 400 `At least one task field must be provided.` from `buildUpdatePayload` (line 281) and no `UPDATE` statement at all; the new fourth test pins it. Explain why this is a 400 and not a 200 no-op."""); done.append('review#5 three concrete variations')

B = [
("the form decides what to send",
 "`client/src/features/tasks` and `client/src/pages`: the task form posts the whole form on create and the edited fields on save; `client/src/services/tasksApi.js` maps those to `POST /api/tasks` and `PUT /api/tasks/:id`. Nothing is validated in the browser beyond input types."),
("the request leaves the browser",
 "`client/src/services/apiClient.js` wraps `fetch`, sets the JSON header and turns a non-2xx into an error carrying the server's `error.message`; that string is what the form shows."),
("the route and service validate",
 "`server/src/routes/taskRoutes.js` maps `PUT /:id` to `taskController.updateTask` via `asyncHandler`; the controller calls `taskService`, where `parseTaskId` (line 38), `normalizeTitle` (108), `normalizeDescription` (131, with the 5000-character bound), `normalizeDueDate` (162) and `buildUpdatePayload` (249, the \"at least one field\" guard at 281 and the unchanged-overdue-date rule) reject bad input with `ValidationError` before any query."),
("the model builds one statement",
 "`server/src/models/taskModel.js` `updateTask(id, updates)` (line 71) is one Knex `UPDATE ... WHERE id = ? RETURNING *`; `createTask` (58) one `INSERT ... RETURNING *`. There is no read-modify-write in the model; the service already loaded the existing task to decide what changed."),
("PostgreSQL commits or rejects",
 "The `tasks` table (`server/db/migrations/20260703000000_create_tasks_table.js`) has `date` and `text` columns; the length bounds are product rules enforced in the service, because `text` accepts anything. In tests the statement runs in a private schema created by `server/test/database.cjs`."),
("the envelope tells the client what happened",
 "`server/src/utils` `sendSuccess` answers `{ success: true, data }`; the error middleware maps `ValidationError` to 400 `{ success: false, error: { message } }`. The tests assert the status and then read the row with `db(\"tasks\")` to prove what was stored."),
]
fe.set_boundaries(S, B); done.append('2.2 trace-lab call path section (07)')

R = [
"the filter must be a bound parameter (`whereILike(\"title\", `%${q}%`)` or a parameterized `where`), never string-concatenated into SQL; your test sends a title containing `%` and `'` and asserts the query still matches exactly the intended rows.",
"the test must send `{ due_date: null }` (or `\"\"` if that is the contract) and assert the row's `due_date` is `NULL` while `title` is unchanged, and must also show that omitting `due_date` leaves the existing value alone; name the branch of `normalizeDueDate` that handles each.",
"add a `version` column, send it back on `PUT`, update with `WHERE id = ? AND version = ?` and answer 409 on zero rows; the test issues two sequential `PUT`s with the same stale version and asserts 200 then 409 with the row equal to the first result.",
"trace one message from `ValidationError` in the service, through the error middleware envelope, through `apiClient.js`, into the form; propose a wording change and show the same test string updated in `tasks.test.cjs` so the contract stays pinned.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')

fe.add_exercise(S, 'ownership and authorization',
"""Tasks have no owner. Add one end to end.

1. Migration: `owner text NOT NULL DEFAULT 'anonymous'` on `tasks`.
2. Middleware in `server/src/app.js`: read `X-Actor`, attach `req.actor`; blank on `POST`/`PUT`/`PATCH`/`DELETE` -> 401.
3. `taskService.createTask` sets `owner` from the actor; `updateTask`, `toggleTask` and `deleteTask` load the row and throw a `ForbiddenError` (403) when `row.owner !== actor`.
4. Send the header from `apiClient.js`.

Acceptance, written first: cross-owner `PUT` is 403 and the row deep-equals the original; cross-owner `DELETE` is 403 and the row still exists; owner `PUT` is 200; missing header is 401; `GET` needs no header. `api.request` in `server/test/database.cjs` needs a headers argument.""",
"""Reference (the check lives in the service, before the model writes):

```js
async function updateTask(id, payload, actor) {
  const existing = await taskModel.findTaskById(parseTaskId(id));
  if (!existing) throw new NotFoundError('Task not found.');
  if (existing.owner !== actor) throw new ForbiddenError('Only the owner can edit this task.');
  return taskModel.updateTask(existing.id, buildUpdatePayload(payload, existing));
}
```

Reference test skeleton: create as `ana`; `PUT` as `ben` -> 403 and `db("tasks").where({ id }).first()` unchanged; `DELETE` as `ben` -> 403; `PUT` as `ana` -> 200; `PUT` with no header -> 401.

Review: explain why the read-then-write is safe enough here (one `UPDATE`, owner never changes) and what you would add if owners could be reassigned concurrently (`WHERE id = ? AND owner = ?` in the update)."""); done.append('2.5 ownership/authz exercise 7 (05, 06)')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **3**.", "Automated test cases: **3** delivered by Astra, plus **1** added in the fix pass (empty update body), for 4 in `server/test/tasks.test.cjs`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
