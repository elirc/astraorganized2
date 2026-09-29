import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-02-contact-book'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

RUN = """From the `server` folder, install dependencies once (`npm install`) and run `npm test`. The suite needs a PostgreSQL role that can `CREATE SCHEMA` in a database whose name starts with `astra_test_`; it creates a private schema per run and drops it afterwards. Point it at that database with `ASTRA_TEST_DATABASE_URL` (PowerShell: `$env:ASTRA_TEST_DATABASE_URL = "postgres://postgres:local-test@127.0.0.1:5432/astra_test_learning"`).

No local PostgreSQL? Use a throwaway container and create the database once:

```powershell
docker run --rm -d --name astra-pg -e POSTGRES_PASSWORD=local-test -p 5432:5432 postgres:18
docker exec astra-pg createdb -U postgres astra_test_learning
```

Stop it with `docker stop astra-pg` when you are done; nothing persists."""
fe.rw(fe.chapter(S, '04'), lambda t: fe.replace_section(t, r'Run the checks', RUN) or t)
done.append('review#3/#5 04 "Run the checks" rewritten: no circular pointer, Docker fallback, CREATE SCHEMA privilege named')

# review #1: HTTP-level import test
def patch_test(t):
    t = t.replace('const service = require("../src/services/contactService");', 'const service = require("../src/services/contactService");\nconst app = require("../src/app");', 1)
    t = t.replace("let clean;\nbefore(async () => {\n  clean = await harness.prepare(\n    db,\n    require(\"../db/migrations/202607030201_create_contacts_tags\").up,\n  );\n});\nafter(async () => {\n  if (clean) await clean();\n});",
                  "let clean, api;\nbefore(async () => {\n  clean = await harness.prepare(\n    db,\n    require(\"../db/migrations/202607030201_create_contacts_tags\").up,\n  );\n  api = await harness.listen(app);\n});\nafter(async () => {\n  if (api) await api.close();\n  if (clean) await clean();\n});", 1)
    add = '''
test("POST /api/contacts/import answers 200 for a good CSV and 400 for a malformed one, through the controller", async () => {
  const good = await api.request("POST", "/api/contacts/import", {
    csv: "first_name,last_name,email\\r\\nGrace,Hopper,grace@example.com",
  });
  assert.equal(good.status, 200, JSON.stringify(good.body));
  assert.equal(good.body.data.imported, 1);
  const before = Number((await db("contacts").count("* as n").first()).n);
  const bad = await api.request("POST", "/api/contacts/import", {
    csv: 'first_name,last_name,email\\r\\nAda,Lovelace,"unterminated',
  });
  assert.equal(bad.status, 400, JSON.stringify(bad.body));
  assert.equal(Number((await db("contacts").count("* as n").first()).n), before);
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('server/test/import.test.cjs', patch_test)
done.append('review#1 HTTP-level test for POST /api/contacts/import (200 with imported count; 400 for a malformed CSV with no rows saved)')

# review #2: performance note + exercise
fe.append_section(S, '03', '## Performance is a separate concern from correctness', """`importContactBatch` in `server/src/models/contactModel.js` (lines 160-176) is correct and slow: for every contact it runs one `INSERT ... RETURNING *`, then for every tag an `INSERT ... ON CONFLICT ... IGNORE`, a `SELECT`, and a junction `INSERT`. A 1,000-row file with three tags each is about 10,000 round trips inside one transaction. That is fine for a course and wrong for production, and the two are different lessons: the transaction gives all-or-nothing, the batching gives speed. Exercise 8 asks for the batched version with the *same* rollback test as its acceptance criterion, so you can prove you kept correctness while changing performance.""", before='## How to reason through the code')
fe.add_exercise(S, 'batch the import without losing the rollback',
"""Rewrite `importContactBatch` to use three statements instead of ~10 per contact, inside the same `db.transaction`:

1. `trx("contacts").insert(rows).returning("*")` for all contacts at once.
2. One `trx("tags").insert(distinctNames.map(name => ({ name }))).onConflict("name").ignore()`, then one `SELECT` of all those tags.
3. One `trx("contact_tags").insert(junctions)` built from the returned ids.

Acceptance: the existing test "a late database uniqueness failure rolls back contacts, new tags and junctions" must still pass unchanged, and a new test must import 200 generated rows and assert the count. Measure the wall time before and after with `console.time`.""",
"""Reference shape:

```js
async function importContactBatch(batch) {
  return db.transaction(async (trx) => {
    const created = await trx("contacts").insert(batch.map((b) => b.contact)).returning("*");
    const names = [...new Set(batch.flatMap((b) => b.tags))];
    if (names.length) await trx("tags").insert(names.map((name) => ({ name }))).onConflict("name").ignore();
    const tags = names.length ? await trx("tags").whereIn("name", names) : [];
    const byName = new Map(tags.map((t) => [t.name, t]));
    const junctions = batch.flatMap((b, i) => b.tags.map((name) => ({ contact_id: created[i].id, tag_id: byName.get(name).id })));
    if (junctions.length) await trx("contact_tags").insert(junctions);
    return created.map((c, i) => ({ ...c, tags: batch[i].tags.map((n) => byName.get(n)) }));
  });
}
```

Review: `created[i]` relies on PostgreSQL returning rows in insert order for a single multi-row `INSERT ... RETURNING`, which it does; say so explicitly. The rollback test is the acceptance criterion because it is the property most likely to be lost while optimizing."""
, number=8); done.append('review#2 03 performance note; exercise 8 batched import with the rollback test as acceptance (05, 06)')

fe.set_variations(S, """**Normal variation — a field that is only a quoted empty string.** Import `first_name,last_name,email,notes\\r\\nGrace,Hopper,grace@example.com,""`. Predict: one contact, `notes` is an empty string (or `null` if the normalizer converts it; read `csvToContacts` to decide before running).

**Invalid variation — a row ending in a bare `\\r`.** Import `first_name,last_name,email\\r\\nAda,Lovelace,ada@example.com\\r`. Predict whether the parser treats the trailing `\\r` as a line ending or as part of the email, and therefore whether the row is valid; then check with the email validation rule.

**Boundary variation — duplicate headers.** Import a file whose header row is `first_name,last_name,email,notes,notes`. Predict the exact error from the header check in `server/src/utils/csv.js` and that no transaction is opened (count `contacts` before and after)."""); done.append('review#4 three concrete CSV variations')

B = [
("the import screen decides what to send",
 "`client/src/features/contacts`: the import dialog reads the chosen file as text and posts `{ csv }` through `client/src/services`; the export button downloads the CSV built by `contactsToCsv`. The browser never parses the CSV: parsing is the server's job so the same rules apply to every client."),
("the request leaves the browser",
 "`POST /api/contacts/import` with a JSON body `{ csv: \"...\" }` (the controller also accepts a raw body). The client shows `error.message` from the envelope on failure, which is the CSV parser's message with the offending row."),
("the route and controller hand the text to the service",
 "`server/src/routes/contactRoutes.js:12` -> `contactController.importCsv` (line 49) -> `contactService.importContacts(req.body.csv || req.body)`. No validation happens here; the controller's only job is the envelope."),
("the service parses everything before touching the database",
 "`contactService.importContacts` (line 124): `csvToContacts` (`server/src/utils/csv.js`) turns the text into rows, handling quoted commas, doubled quotes, multiline notes and CRLF; every row is validated *before* a transaction is opened, so an invalid row 20 saves no rows (second test). Then it calls `importContactBatch`."),
("the model writes all rows in one transaction",
 "`contactModel.importContactBatch` (line 160): `db.transaction` -> per contact `INSERT ... RETURNING *`, per tag `INSERT ... ON CONFLICT (name) DO NOTHING`, `SELECT`, junction `INSERT`. A unique violation on a late row (third test) rolls back the contacts, new tags and junctions inserted earlier in the same call."),
("the envelope tells the client what happened",
 "`sendSuccess` answers `{ success: true, data: { imported, contacts } }`; a `ValidationError` from the parser becomes 400 with the row and column in the message. The new HTTP test reads both statuses and counts `contacts` directly to prove the 400 saved nothing."),
]
fe.set_boundaries(S, B); done.append('2.2 trace-lab call path section (07)')
R = [
"the HTTP test must post through `/api/contacts/import` (not call the service) and assert 200 with `data.imported` and 400 with an unchanged `contacts` count; explain which layer produced the 400 (the parser's `ValidationError`, mapped by the error middleware).",
"the batched import must keep the rollback test green unchanged; show the timing before and after for 200 rows and name the PostgreSQL guarantee (`RETURNING` order for one multi-row insert) that lets you map rows back to tags.",
"the late-failure test must inject the failure *after* at least one contact and one junction were inserted (the third test does this with a uniqueness violation) and assert all three tables are unchanged; explain why a per-row transaction would have left partial data.",
"the pagination test must create equal-name contacts, page twice and assert identical ids in identical order (a tie-breaker on `id`), and must show that `page=0` or `pageSize=1000` is a 400 rather than a silent clamp (or document the clamp if that is the contract).",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')
fe.add_exercise(S, 'ownership and authorization',
"""Contacts have no owner. Add one and scope the import.

1. Migration: `owner text NOT NULL DEFAULT 'anonymous'` on `contacts`.
2. Middleware: read `X-Actor`; blank on writes -> 401.
3. `importContacts(csv, actor)` stamps `owner` on every parsed row before `importContactBatch`; list, get, update and delete carry `WHERE owner = ?`.
3. Test: `ana` imports two contacts; `ben` lists (empty), gets one by id (404), deletes it (404, row still there); `ana` sees both.

Acceptance is the test plus one sentence on why the import stamps the owner in the service (before the transaction) rather than trusting a column in the CSV.""",
"""Reference: in `importContacts`, after parsing, `rows.forEach((r) => { r.contact.owner = actor; })`; in `contactModel.listContacts(filters, actor)` add `.where({ owner: actor })`; `getContact(id, actor)` -> `.where({ id, owner: actor }).first()` and 404 when missing.

Reference test skeleton: `api.request("POST", "/api/contacts/import", { csv }, { "X-Actor": "ana" })` -> 200; `api.request("GET", "/api/contacts", undefined, { "X-Actor": "ben" })` -> `data` empty; `GET /api/contacts/<id>` as `ben` -> 404; as `ana` -> 200.

Review: a CSV column named `owner` must be ignored (or rejected), otherwise an import file can assign contacts to someone else."""); done.append('2.5 ownership/authz exercise 7 (05, 06)')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **4**.", "Automated test cases: **4** delivered by Astra, plus **1** added in the fix pass (HTTP-level import), for 5 in `server/test/import.test.cjs`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
