import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'job-track'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# --- review #4: undefined vs null vs absent section
fe.append_section(S, '02', '## `undefined`, `null` and absent: three states of a partial update', """A `PATCH` body can say three different things about `location`: the key is **absent** (keep what is stored), the key is **`\"\"`** (the user cleared the field), or the key has a **value**. JSON has no `undefined`, so the wire only carries the last two, and Zod has to turn `\"\"` into an explicit \"clear\" that the route can tell apart from \"not sent\". That is what the transform in `server/src/validation.js` does:

```js
// before: an empty string failed the URL/date rule, or was stored as ""
job_url: z.string().url().max(500).optional(),
// after: absent stays undefined; "" becomes null; a value is validated
job_url: z.string().url().max(500).optional().or(z.literal("").transform(() => null)),
```

The route then merges with the three states in mind (`server/src/routes/applications.js`, the `merged` block): `data.location !== undefined ? data.location || null : existing.location`. Absent -> keep; `null` -> clear; value -> replace. SQLite stores `null` as `NULL`, so a cleared field reads back as `null`, never as `\"\"` or `0`. The salary fields use `z.coerce.number().nullable()` for the same reason: blank must not become zero, which is the first test's whole point.""")
done.append('review#4 02 section on undefined vs null vs absent with the before/after Zod lines')

# --- review #3: fourth test covering location and job_url
def patch_test(t):
    add = '''
test("location and job_url follow the same three-state rule as notes", async () => {
  const made = await api("/applications", "POST", {
    company: "Three States", position: "Engineer", status: "applied",
    location: "Remote", job_url: "https://example.com/job",
  }, token);
  assert.equal(made.status, 201, JSON.stringify(made.data));
  const path = "/applications/" + made.data.id;
  const untouched = await api(path, "PATCH", { position: "Senior Engineer" }, token);
  assert.equal(untouched.status, 200);
  assert.equal(untouched.data.location, "Remote");
  assert.equal(untouched.data.job_url, "https://example.com/job");
  const cleared = await api(path, "PATCH", { location: "", job_url: "" }, token);
  assert.equal(cleared.status, 200);
  assert.equal(cleared.data.location, null);
  assert.equal(cleared.data.job_url, null);
  const bad = await api(path, "PATCH", { job_url: "not a url" }, token);
  assert.equal(bad.status, 400);
  assert.equal((await api(path, "GET", undefined, token)).data.job_url, null);
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('test/applications.test.js', patch_test)
done.append('review#3 fourth test: absent keeps, "" clears to null, invalid value is 400 with the row unchanged, for location and job_url')

# --- review #1, #5: toolchain and test script
sp = json.load(open('server/package.json', encoding='utf-8'))
sp['scripts']['test'] = 'node --test ../test/*.test.js'
sp.setdefault('engines', {})['node'] = '>=22.16'
open('server/package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(sp, indent=2) + '\n')
fe.rw(fe.chapter(S, 'README'), lambda t: t.replace('### Toolchain\n\n', '### Toolchain\n\n`better-sqlite3` is a native module. If `npm install --prefix server` prints a build or ABI error, run `npm rebuild better-sqlite3 --prefix server` with the same Node major the project was verified with (22.16.x); switching Node versions afterwards requires the rebuild again. This is the most likely fresh-machine failure in this project.\n\n', 1))
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.rstrip('\n') + '\n\nToolchain: Node 22.16.0; `better-sqlite3` ^11 (native module, rebuild with `npm rebuild better-sqlite3 --prefix server` if the ABI does not match). `npm test` at the root runs `npm run test --prefix server`, which runs `node --test ../test/*.test.js`; Node 22 expands the pattern itself, so it works under cmd.exe and PowerShell.\n')
done.append('review#1 README and VERIFICATION pin Node 22.16 and give the better-sqlite3 rebuild fallback; engines.node added to server/package.json')
done.append('review#5 server test script is `node --test ../test/*.test.js` (Node 22 expands the glob; a bare directory is rejected by Node 22.16)')

B = [
("the applications page decides what to send",
 "`client/src/pages/ApplicationsPage.jsx`: the edit form sends every field it renders, so a cleared input arrives as `\"\"`, never as a missing key; the status buttons send only `{ status }`. That difference is what the three-state rule in chapter 2 is built for."),
("the request leaves the browser",
 "`client/src/api` wraps `fetch` with the stored JWT as `Authorization: Bearer <token>`; edits are `PATCH /api/applications/:id`. A 401 clears the token and sends the user to the login page; a 400 or 404 is shown as the server's `message`."),
("authentication and validation run before the handler body",
 "`server/src/middleware/auth.js` `requireAuth` verifies the JWT and sets `req.user`; the route (`server/src/routes/applications.js`) first loads the row with `WHERE id = ? AND user_id = ?` (a foreign or missing id is 404 either way), then `parseOrRespond(updateApplicationSchema, req.body, res)` (`server/src/utils.js`) runs the Zod schema and answers 400 itself when parsing fails. An empty object after parsing is 400 `No fields provided`."),
("the handler merges three-state fields and enforces transitions",
 "Still in `applications.js`: a status change is checked against `ALLOWED_TRANSITIONS[existing.status]` (a repeated identical status is a no-op, the third test); then the `merged` block combines `existing` with `data`, turning `\"\"` into `null` for `location`, `job_url`, `notes` and `next_step_date`, and re-validates the salary pair after the merge because a partial update can change only one side."),
("SQLite writes the row",
 "The `UPDATE applications SET ... WHERE id = ? AND user_id = ?` runs through `better-sqlite3`, synchronously; `null` is stored as `NULL`, and `user_id` in the `WHERE` means an id that belongs to someone else updates zero rows even if the earlier check were skipped. Exercise 4 adds a stage-history row in the same transaction."),
("the response tells the client what happened",
 "The route answers 200 with the re-read row (`SELECT * ... WHERE id = ?`), so `null` fields come back as `null`; the tests read `data.notes`, `data.next_step_date`, `data.location` and `data.job_url` straight from that response and then `GET` again to confirm the stored state."),
]
fe.set_boundaries(S, B); done.append('review#2 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the UI must render `null` salary as `Not provided` and `0` as `0` (a real number), with a test that creates one of each and asserts the two labels; the check must be `=== null`, never a truthiness test, and the server must keep storing blank as `null` (the first test).",
"the button must send `{ next_step_date: \"\" }` (the API's explicit-clear contract) rather than omitting the field, and the following `GET` must return `null`; assert both in a test, and show that a `PATCH` without the key leaves the date alone.",
"seed three applications with the same `updated_at`, page through with `pageSize=2` twice, and assert the ids are stable across reads (the list query must order by the sort column *and* `id`); document what a client should do when a row is inserted between pages.",
"the status change and the history insert must run in one `better-sqlite3` transaction (`db.transaction(fn)`), a repeated identical status must write no history row, and a test must force the history insert to fail (drop the table in the test database) and show the status unchanged.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')

route = open('server/src/routes/applications.js', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
m0 = next(i for i, l in enumerate(route) if 'const merged = {' in l)
val = open('server/src/validation.js', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
v0 = next(i for i, l in enumerate(val) if 'const optionalDateSchema' in l)
excerpt = '// server/src/validation.js:' + str(v0 + 1) + '\n' + '\n'.join(val[v0:v0 + 16]) + '\n\n// server/src/routes/applications.js:' + str(m0 + 1) + '\n' + '\n'.join(route[m0:m0 + 14])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/75/server/src` with `diff -r --strip-trailing-cr -w`): the `z.literal(\"\").transform(() => null)` branches that turn a cleared field into an explicit `null`, and the `merged` block that keeps absent fields, clears `null` ones and re-validates the salary pair after the merge. The linked source is authoritative if you later edit the project.", excerpt, 'javascript'); done.append('2.4 excerpt shows the transforms and the merge block')

fe.set_variations(S, """**Normal variation — keep and clear.** Create an application with `notes` and `location`; `PATCH` only `{ position: \"x\" }`, then `PATCH` `{ notes: \"\" }`. Predict the two responses (notes kept, then `null`) and confirm with a `GET`.

**Invalid variation — blank salary.** `PATCH` `{ salary_min: \"\" }`. Predict what `z.coerce.number()` would do with `\"\"` without the nullable branch (it would become `0`) and what the schema does now (`null`); then send `{ salary_min: 500, salary_max: 100 }` and predict the post-merge 400.

**Boundary variation — someone else's record.** Register a second user and `PATCH` the first user's application with the second token. Predict 404 (not 403) and an unchanged row; explain which `WHERE` clause made it so even before the transition check ran."""); done.append('2.4 three concrete variations')

fe.append_section(S, '04', "## This project's test harness", """`test/applications.test.js` sets `JOB_TRACK_DATA_DIR` to a fresh temporary directory and `JWT_SECRET` to a throwaway value before requiring `server/src/server`, because the database module opens its file at load time. `before()` registers one user and keeps the JWT in `token`; the `api()` helper adds `Authorization: Bearer <token>` when a token is passed, which is how the third test can act as a second user. Each test reads the row back with a `GET` after the `PATCH`, so what is asserted is stored state, not the response alone. Run `npm test` from the project root (`node --test ../test/*.test.js` inside `server/`).""", before='## ')
done.append('harness section (04)')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **3**.", "Automated test cases: **3** delivered by Astra, plus **1** added in the fix pass (three-state rule for location and job_url), for 4 in `test/applications.test.js`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
