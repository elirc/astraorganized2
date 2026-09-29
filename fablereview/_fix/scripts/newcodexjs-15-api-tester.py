import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-15-api-tester'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

fe.append_section(S, '02', '## The owner-row lock: what it serializes, what it costs, and two alternatives', """`activateEnvironment`, `createEnvironment` and `updateEnvironment` in `server/src/models/environmentModel.ts` all begin with `trx("users").where({ id: userId }).forUpdate().first()`. The invariant they protect is *one active environment per user*. Locking the user's row means every write that can change `is_active` for that user runs one at a time, so the sequence "clear all, then set one" (lines 80-85) can never interleave with another request's clear-then-set. The second test proves it: two activations in a `Promise.all` end with exactly one active row.

What it costs: the lock is on the *user*, so two unrelated writes by the same user (rename Staging, activate Local) also serialize, and the lock is held for the whole transaction including the `RETURNING *` round trip. For an API tester with one human per user that is invisible; for a shared account it would be a hot row. Two alternatives, both worth trying in a throwaway branch:

1. **Make the invariant a constraint.** `CREATE UNIQUE INDEX one_active_env_per_user ON environments (user_id) WHERE is_active;` Then the clear-then-set sequence still works, but a buggy code path that forgets the clear gets a unique-violation error instead of silently leaving two active rows. The lock becomes optional: without it, two racing activations both clear, both set, and the second `UPDATE ... SET is_active = true` fails with `23505`, which the service can map to 409 or retry.
2. **Lock the environment rows instead of the user row.** `SELECT ... FROM environments WHERE user_id = ? ORDER BY id FOR UPDATE` before the clear. Finer than the user row (a rename that does not touch `is_active` no longer waits), coarser than nothing, and the `ORDER BY id` matters for the same deadlock reason as in the checkout lesson.

Predict, before the exercise: with alternative 1 and no lock, what do two concurrent activations return? (One 200 and one 409/500, never two active rows.)""")
done.append('review#1 02-CONCEPTS section on the owner-row lock, its cost and two alternatives (partial unique index, ordered environment locks)')

B = [
("the environment switcher decides what to send",
 "`client/src/features/environments/components/*`: the switcher renders the user's environments and calls `activateEnvironment(id)` from `client/src/services/api.ts:58` on click; the variables editor sends the whole variable list to the replace endpoint. The UI shows the active badge from the server's `is_active` flag after the query refetches, which is exactly what exercise 1 asks you to make explicit."),
("the request leaves the browser",
 "`client/src/services/api.ts`: `POST /environments/:id/activate` with no body; `PUT /environments/:id/variables` with `{ variables: [...] }`; the axios instance adds the demo `x-user-id`. `unwrap()` reads the envelope, so the 404 for a foreign environment arrives as `Environment not found` and is indistinguishable from a missing id."),
("the route validates the shape",
 "`server/src/routes/index.ts` mounts `validateBody(schema)` from `middleware/validate.ts` with the Zod schemas in `validators/schemas.ts` (environment names, variable `{ key, value, enabled }` arrays, saved-request header/parameter arrays); `middleware/requestContext.ts` resolves the demo user. Activation has no body to validate; ownership is decided below."),
("the service delegates; the model owns the invariant",
 "`services/environmentService.ts:38` `activateEnvironment(userId, id)` calls the model and returns the row. `models/environmentModel.ts:73`: `db.transaction` -> lock the user row -> load the target scoped by `{ id, user_id }` (404 if foreign or missing, and the transaction ends with nothing written, which the first test checks by re-reading the previously active row) -> `UPDATE environments SET is_active = false WHERE user_id = ?` -> `UPDATE ... SET is_active = true WHERE id = ? AND user_id = ? RETURNING *`. Before Astra's change the clear ran before the existence check, so a bad id deactivated everything."),
("PostgreSQL commits both updates or neither",
 "The clear and the set are two statements in one transaction; a failure between them rolls both back, which is why `replaceVariables` (line 92) can safely `DELETE` all variables and re-insert: the third test rejects duplicate keys and shows the original variables intact. Saved-request header and parameter arrays are `jsonb` columns; the fourth test proves they round-trip through create, partial edit and duplication."),
("the envelope tells the client what happened",
 "`utils/response.ts` `sendSuccess` returns `{ success: true, data }`; `errorMiddleware.ts` maps `NotFoundError` to 404 and `ValidationError` to 400. After activation the client invalidates the environments query and re-renders badges from the committed rows."),
]
fe.set_boundaries(S, B); done.append('review#2 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the badge must move only after the activation mutation resolves and the environments query refetches; on a failed activation (mock a 404) the previous badge must remain; assert both in a client test using the mocking pattern from the blog-platform course, and assert in a server test that a failed activation leaves `is_active` unchanged (the first test already does this).",
"the hint must use the same normalization as `replaceVariables` (`String(v.key).trim()`), highlight both conflicting rows, and must not disable the server check; prove the server still returns 400 for a duplicate that the client failed to flag (send it through the API directly).",
"install a `BEFORE INSERT` trigger on `env_variables` that raises on the second row, submit three variables, assert 400/500 as appropriate, then assert the original ordered key/value pairs are unchanged; explain which statement in `replaceVariables` had already run (the `DELETE`) and why the transaction made it disappear.",
"every move must load both the source and the destination with `user_id = ?` in the same query or transaction, reject a cross-owner reference with 404 before writing, and verify that the folder belongs to the target collection; your test must attempt a move into another user's collection and assert nothing changed.",
]
fe.set_reviews(S, R); done.append('review#4 / 2.3 per-exercise review criteria (06)')

mdl = open('server/src/models/environmentModel.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
a = next(i for i, l in enumerate(mdl) if 'export async function activateEnvironment' in l)
r = next(i for i, l in enumerate(mdl) if 'export async function replaceVariables' in l)
excerpt = '// models/environmentModel.ts:' + str(a + 1) + '\n' + '\n'.join(mdl[a:a + 17]) + '\n\n// models/environmentModel.ts:' + str(r + 1) + '\n' + '\n'.join(mdl[r:r + 22])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/66/server/src/models/environmentModel.ts` with `diff --strip-trailing-cr -w`): `activateEnvironment` now checks the target exists before clearing the other rows and does both under the user lock, and `replaceVariables` validates duplicate keys and replaces the set inside one transaction. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows the changed activation and variable replacement')

fe.set_variations(S, """**Normal variation — switch twice.** Activate Staging, then Local. Predict: after each call exactly one row has `is_active = true` for user 1, and user 2's row is untouched. Read the rows in `psql` between calls.

**Invalid variation — a foreign environment.** Activate user 2's environment as user 1. Predict 404 `Environment not found` and user 1's active row unchanged (before the change, the clear ran first and left user 1 with no active environment). Then send variables `[{ key: " token " }, { key: "token" }]`: predict 400 `Variable keys must be unique` and the old variables intact.

**Boundary variation — the race.** Activate Local and Staging in a `Promise.all`. Predict `[200, 200]` and one active row. Then on a throwaway branch remove the user-row lock and add the partial unique index from chapter 2; repeat and record the statuses you observe (one 200 and one 23505-derived error) and the row count (still one)."""); done.append('2.4 three concrete variations')

fe.add_exercise(S, 'ownership on collections, folders and requests',
"""Environments are scoped by `user_id` in every query. Collections, folders and saved requests are where a cross-owner reference can slip in: a request moved into someone else's folder, a folder attached to someone else's collection.

1. Read `collectionService.ts` and `collectionModel.ts` and list every write that takes a foreign key from the body (`collection_id`, `folder_id`). For each, write down whether the referenced row is loaded with `user_id = ?`.
2. Add one helper, `assertOwned(trx, table, id, userId)`, that throws `NotFoundError` when the row is missing or foreign, and call it for every foreign key before the write, inside the same transaction as the write.
3. Test: user 1 creates a collection and folder; user 2 tries to create a request in that folder, move their own request into it, and rename the collection; all three are 404 and the rows are unchanged; user 1's same calls succeed.

Acceptance is the test plus one sentence on why the helper runs inside the transaction (a row could be re-parented between the check and the write).""",
"""Reference helper:

```typescript
async function assertOwned(trx: Knex.Transaction, table: string, id: number, userId: number) {
  const row = await trx(table).where({ id, user_id: userId }).forUpdate().first();
  if (!row) throw new NotFoundError(`${table.slice(0, -1)} not found`);
  return row;
}
```

Reference test skeleton: `api("/collections", "POST", { name: "Mine" })` as user 1 -> id; as user 2 (`x-user-id: 2`) `api("/collections/" + id + "/folders", "POST", { name: "Sneaky" })` -> 404 and folder count unchanged; `api("/collections/" + id, "PUT", { name: "Taken" })` -> 404 and name unchanged.

Review: explain why 404 rather than 403, and why the ownership lookup uses `forUpdate()` (it doubles as the lock that keeps the parent from being deleted or re-owned during the write)."""); done.append('2.5 ownership/authz exercise 7 on collections/folders/requests (05, 06)')

fe.append_section(S, '04', "## Project-specific debugging: JSONB round trips, interpolation and the proxy", """Three things are specific to this project. **Header and parameter arrays come back changed**: they are `jsonb` columns; check that the model serializes arrays with `JSON.stringify` only when the key is present (a partial edit must not reset them), and read the fourth test, which proves create, partial edit and duplication preserve them. **A `{{var}}` is not replaced**: `utils/interpolate.ts` substitutes from the *active* environment's enabled variables (`getVariableMap`, `environmentModel.ts:135`); if the wrong environment is active or the variable is disabled, the placeholder survives. Reproduce by activating the other environment and re-sending. **The proxy hangs or returns 502**: `proxyService.ts` forwards the request with a timeout; a target that never answers surfaces as a timeout error, not as a saved-request problem. Test the proxy against a local echo server, never against a real API.

`test/database.ts` creates a private schema, migrates it and returns `h.db` plus `request(origin, path, method, body, headers)`; the `api()` helper adds `x-user-id: 1`. Run with `$env:ASTRA_TEST_DATABASE_URL = "postgres://user@127.0.0.1:5432/astra_test_yourname"` then `npm test`.""", before='## ')
done.append('review#4 project-specific debugging section (04)')

fe.rw(fe.chapter(S, 'README'), lambda t: t.replace("## What you will be able to do\n\n", "## What you will be able to do\n\nThe transferable skill in this course is not the API-tester domain: it is *verify ownership before mutating siblings, and make a uniqueness invariant explicit* (one active environment per user). Treat the project as an elective that practises that skill; the same shape appears in any app with a \"default\" or \"current\" row per user.\n\n", 1))
done.append('review#3 README names the transferable skill and positions the course as an elective')

rp = json.load(open('package.json', encoding='utf-8'))
rp['name'] = 'api-tester-workspace'
rp.setdefault('devDependencies', {}).update({"pg": "^8.23.0", "tsx": "^4.23.13"})
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(rp, indent=2) + '\n')
done.append('review#5 root package renamed from astra-crud-workspace-66; pg and tsx declared at the root; README carries the Toolchain block')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
