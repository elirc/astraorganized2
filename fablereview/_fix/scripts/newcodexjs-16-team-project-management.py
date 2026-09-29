import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-16-team-project-management'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# --- review #2: dead argument in restoreRecord
def patch_model(t):
    old = """  return lifecycleUpdate(
    id,
    { archived_at: null, status: "active" },
    context,
    "restored",
  );"""
    new = """  // The real restore values are computed inside lifecycleUpdate from
  // status_before_archive; only the action name matters here.
  return lifecycleUpdate(id, {}, context, "restored");"""
    assert old in t
    return t.replace(old, new, 1)
assert fe.rw('server/src/models/model.ts', patch_model)
done.append('review#2 dead `status: "active"` argument removed from restoreRecord (server/src/models/model.ts); "active" was never a status of this app')

# --- review #5: cap after de-duplication
def patch_service(t):
    old = """  if (
    !Array.isArray(payload.ids) ||
    payload.ids.length === 0 ||
    payload.ids.length > 100
  )
    throw new ValidationError("ids must be a non-empty array.");
  const ids = [...new Set(payload.ids.map((id) => parseId(String(id))))];"""
    new = """  if (!Array.isArray(payload.ids) || payload.ids.length === 0)
    throw new ValidationError("ids must be a non-empty array.");
  const ids = [...new Set(payload.ids.map((id) => parseId(String(id))))];
  if (ids.length > 100)
    throw new ValidationError("At most 100 distinct ids per bulk action.");"""
    assert old in t
    return t.replace(old, new, 1)
assert fe.rw('server/src/services/service.ts', patch_service)
def patch_test(t):
    add = '''
test("the bulk cap counts distinct ids, and restore reads status_before_archive", async () => {
  const a = await create("Cap", "blocked");
  const repeated = Array.from({ length: 150 }, () => a.id);
  assert.equal((await api("/bulk/status", "POST", { ids: repeated, status: "done" })).status, 200);
  assert.equal((await api(`/${a.id}`)).data.data.status, "done");
  assert.equal((await api(`/${a.id}/archive`, "PATCH", {})).status, 200);
  const restored = await api(`/${a.id}/restore`, "PATCH", {});
  assert.equal(restored.data.data.status, "done");
  assert.equal(restored.data.data.status_before_archive, null);
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('test/crud.test.ts', patch_test)
done.append('review#5 bulk cap now applies after de-duplication (150 repeats of one id are accepted); regression test added')

# --- review #4: desired-state vs event commands
fe.append_section(S, '02', '## Desired state versus events: why a repeated archive writes nothing', """`PATCH /tasks/:id/archive` does not mean "append an archive event"; it means "make this record archived". That is a *desired-state* command: sending it twice must leave the record and the audit log exactly as one send did. `lifecycleUpdate` in `server/src/models/model.ts` implements that with the early returns `if (action === "archived" && before.archived_at) return before;` and the mirror for restore, and the second test counts audit rows to prove nothing was written. Contrast `addComment`, which is an *event* command: two identical posts are two comments, by design.

The `version` column is not optimistic concurrency. It is incremented on every write (`version: trx.raw("version + 1")`) so a reader can tell that something changed, but nothing checks the version a client last saw. The row lock (`forUpdate()` at the start of every lifecycle and bulk transaction) is what prevents lost updates *between concurrent requests*; it does nothing about a stale form submitted after someone else's edit. Exercise 4 adds the missing half: `UPDATE ... WHERE id = ? AND version = ?` and a 409 when zero rows match.""")
done.append('review#4 02-CONCEPTS section on desired-state vs event commands and why version is not optimistic concurrency')

B = [
("the React screen decides what to send",
 "`client/src/App.tsx`: `saveRecord` (line 100) sends the form; archive and restore buttons call `archiveRecord(id)` / `restoreRecord(id)` from `client/src/services/api.ts:63-68` with no body; `runBulkStatus(status)` (line 125) sends the current `selectedIds` and one status. The client never sends `archived_at` or `status_before_archive`: lifecycle fields are computed on the server."),
("the request leaves the browser",
 "`client/src/services/api.ts`: `PATCH /tasks/:id/archive`, `PATCH /tasks/:id/restore`, `POST /tasks/bulk/status` with `{ ids, status }`. The axios instance adds the demo actor and role headers; `unwrap()` reads the envelope, so the 404 for a missing id in a bulk request arrives as `One or more records were not found; no statuses changed.`"),
("the service sanitizes and authorizes",
 "`services/service.ts`: `sanitizePayload` (line 54) whitelists editable fields and treats a `PUT` as partial; `bulkStatus` (line 188) requires the operator role, de-duplicates the ids, applies the 100-id cap to the distinct set, and validates the status against `allowedStatuses`. `parseId` rejects anything that is not a positive integer before any query."),
("the model locks and applies lifecycle rules",
 "`models/model.ts` `lifecycleUpdate` (line 173): `db.transaction` -> `forUpdate()` on the row -> early return if already archived / not archived -> for restore, compute `status = status_before_archive || \"todo\"` and clear both flags; for archive, `statusFields(before, \"archived\")` stores the previous status. `bulkStatus` (line 99) locks all rows in id order, rejects if any id is missing (nothing written), skips rows already in the target status, and writes activity plus audit per changed row."),
("PostgreSQL commits the row, its activity and its audit together",
 "Every lifecycle write is one transaction containing the `UPDATE ... RETURNING *`, an `activity` insert and an `audit_log` insert with real before/after JSON; the third test reads `audit.before.status` and `audit.after.status` back from the database. Exercise 3 injects an audit failure to show that all bulk changes disappear together."),
("the envelope tells the client what happened",
 "`utils/response.ts` `sendSuccess` returns the row (or the array of rows for bulk); `middleware/errorMiddleware.ts` maps `NotFoundError` to 404 and `ValidationError` to 400. After any lifecycle call the client refreshes the list and the dashboard counts, which are computed on the server from `archived_at` and `deleted_at`."),
]
fe.set_boundaries(S, B); done.append('review#3 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the badge must read `status_before_archive` from the record and render an explicit \"unknown\" for a legacy row where it is `null`; a server test should archive a record with status `blocked` and assert the field, and a client test should render both a known and a null value.",
"the preview must show the count of *distinct* ids (`new Set(selectedIds).size`) and must not disable the server-side 404 for stale ids; a server test should send `[a, a, missing]` and assert 404 with nothing changed, and `[a, a]` and assert one row in the response.",
"install a `BEFORE INSERT` trigger on `audit_log` in the test schema, submit a bulk status change for two records, assert 500, then assert both records' `status` and `version` and the audit count equal their pre-request values; name the statement that had already run for the first record when the second failed.",
"the design must (a) add `expectedVersion` to the edit payload and update with `WHERE id = ? AND version = ?`, returning 409 when zero rows match; (b) replace the demo role header with a verified session and scope every query by team membership in SQL; and (c) show one test where a stale edit is rejected and the stored row is the newer one.",
]
fe.set_reviews(S, R); done.append('review#5 / 2.3 per-exercise review criteria (06)')

mdl = open('server/src/models/model.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
l = next(i for i, l in enumerate(mdl) if 'async function lifecycleUpdate' in l)
s = next(i for i, l in enumerate(mdl) if 'function statusFields' in l)
excerpt = '// models/model.ts:' + str(l + 1) + '\n' + '\n'.join(mdl[l:l + 30]) + '\n\n// models/model.ts:' + str(s + 1) + '\n' + '\n'.join(mdl[s:s + 12])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/67/server/src/models/model.ts` with `diff --strip-trailing-cr -w`): `lifecycleUpdate` locks the row, makes a repeated archive or restore a no-op, restores the previous status, and writes activity and audit in the same transaction; `statusFields` keeps the flags consistent when a form or bulk action sets `status` directly. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows lifecycleUpdate and statusFields')

fe.set_variations(S, """**Normal variation — archive from `blocked`.** Create a record with status `blocked`, archive it, restore it. Predict: after archive `status = archived`, `status_before_archive = blocked`, `archived_at` set; after restore `status = blocked`, both flags null, and exactly two new audit rows for the pair. Read the rows in `psql`.

**Invalid variation — a bulk with one bad id.** `POST /tasks/bulk/status` with `{ ids: [a, 999999], status: "done" }`. Predict 404 and record `a` unchanged, including its `version`. Then send `{ ids: [a, a, a], status: "done" }`: predict 200 with one row in the response and one audit row.

**Boundary variation — the same archive twice, at once.** Send two `PATCH /archive` for one record in a `Promise.all`. Predict `[200, 200]`, one `archived` activity row, one audit row. Explain which line makes the second call a no-op (the early return runs after `forUpdate()`, so it sees the first call's commit)."""); done.append('2.4 three concrete variations')

fe.add_exercise(S, 'ownership and authorization beyond the role header',
"""The operator role for bulk actions comes from a demo header, and records have no owner or team. Make authorization real for one path.

1. Migration: add `team_id` to the records table and a `team_members(team_id, actor, role)` table with two seeded teams.
2. In `services/service.ts`, replace `requireOperator(context)` for `bulkStatus` with a query: the actor must be an `operator` member of the team of *every* record in `ids` (one query with `WHERE id IN (...) AND team_id IN (SELECT team_id FROM team_members WHERE actor = ? AND role = 'operator')`; if the count differs from `ids.length`, throw `NotFoundError`). Run it inside the same transaction as the update so membership cannot change in between.
3. Test: seed two teams; an operator of team A bulk-updates a mix of team A and team B ids -> 404 and nothing changed; team A ids only -> 200.

Acceptance is the test plus a sentence explaining why the check is by *every* id, not by the actor's default team.""",
"""Reference query (inside the bulk transaction, after locking the rows):

```typescript
const allowed = await trx(table)
  .whereIn("id", ids)
  .whereIn("team_id", trx("team_members").select("team_id").where({ actor: context.actor, role: "operator" }))
  .count("* as n").first();
if (Number(allowed.n) !== ids.length) throw new NotFoundError("One or more records were not found; no statuses changed.");
```

Reference test skeleton: insert `team_members` rows for actor `ana` (team 1 operator) and `ben` (team 2 operator); create record `x` in team 1 and `y` in team 2; `POST /bulk/status` as `ana` with `[x, y]` -> 404 and both statuses unchanged; with `[x]` -> 200.

Review: the membership check reuses the \"all or nothing\" shape of the existing missing-id check, which is why the same error message is appropriate; explain what would go wrong if the check ran before the row lock."""); done.append('2.5 ownership/authz exercise 7 (05, 06)')

fe.append_section(S, '04', "## This project's test harness and what each test proves", """`test/database.ts` creates a private schema, migrates it and returns `h.db` plus `request(origin, path, method, body, headers)`; the `api()` helper adds the demo actor and role headers. The second test proves idempotence by counting `audit_log` rows before and after a repeated archive and restore. The third proves atomicity of bulk actions (a missing id changes nothing) and reads the audit `before`/`after` JSON back. The fifth (added in the fix pass) proves the cap counts distinct ids and that restore reads `status_before_archive`. When a lifecycle test fails, read the row and the last two `audit_log` entries in `psql` before touching code: the audit JSON tells you what the server believed the before state was. Run with `$env:ASTRA_TEST_DATABASE_URL = "postgres://user@127.0.0.1:5432/astra_test_yourname"` then `npm test`.""", before='## ')
done.append('harness and test-purpose section (04)')

rp = json.load(open('package.json', encoding='utf-8'))
rp['name'] = 'team-project-management-workspace'
rp.setdefault('devDependencies', {}).update({"pg": "^8.23.0", "tsx": "^4.23.13"})
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(rp, indent=2) + '\n')
done.append('root package renamed from astra-crud-workspace-67; pg and tsx declared at the root; README carries the Toolchain block')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **4**.", "Automated test cases: **4** delivered by Astra, plus **1** added in the fix pass (distinct-id cap and restore status), for 5 in `test/crud.test.ts`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
