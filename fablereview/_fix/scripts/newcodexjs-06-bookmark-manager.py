import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-06-bookmark-manager'
P = fe.REG[S]['abs']
os.chdir(P)
done = ['review#5 lockfiles for server/ and client/ were committed by the earlier fix agent (verified on disk)']

# review #1: bounded search over the text columns, no whole-row cast
def patch_model(t):
    old = 'if (query.search) builder.whereRaw("CAST(bookmarks AS TEXT) ILIKE ?", [`%${query.search}%`]); return builder; }'
    new = '''if (query.search) {
    // Search the fields a person typed, not ids, timestamps or serialized row metadata,
    // and escape LIKE metacharacters so "%" is a character, not a wildcard.
    const needle = "%" + query.search.replace(/[\\\\%_]/g, (c) => "\\\\" + c) + "%";
    builder.where(function () {
      for (const field of ["title", "url", "collection"]) this.orWhereRaw(`${field} ILIKE ? ESCAPE '\\\\'`, [needle]);
    });
  }
  return builder;
}'''
    assert old in t, 'listRecords search line not found'
    return t.replace(old, new, 1)
assert fe.rw('server/src/models/model.ts', patch_model)
def patch_test(t):
    add = '''
test("search is bounded to title, url and collection and treats % and _ as characters", async (t) => {
  const { db } = await import("../src/config/db.js");
  const { up } = await import("../db/migrations/001_init.js");
  const app = (await import("../src/app.js")).default;
  const cleanup = await helper.prepare(db, up);
  t.after(cleanup);
  const http = await helper.listen(app);
  t.after(http.close);
  const made = await http.request("POST", "/api/bookmarks", { title: "Percent 100% guide", url: "https://example.com/pct", collection: "Learning", status: "active", tags: [] });
  assert.equal(made.status, 201);
  const id = made.body.data.id;
  let r = await http.request("GET", "/api/bookmarks?search=%");
  assert.equal(r.status, 200);
  assert.equal(r.body.data.filter((x: any) => x.title !== "Percent 100% guide").length, 0, "a bare % must not match every row");
  r = await http.request("GET", "/api/bookmarks?search=100%25");
  assert.equal(r.body.data.some((x: any) => x.id === id), true);
  r = await http.request("GET", "/api/bookmarks?search=" + String(id));
  assert.equal(r.body.data.some((x: any) => x.id === id), false, "ids are not searchable");
  r = await http.request("GET", "/api/bookmarks?search=" + encodeURIComponent(made.body.data.created_at.slice(0, 4)));
  assert.equal(r.body.data.some((x: any) => x.id === id), false, "timestamps are not searchable");
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('server/test/bookmarks.test.ts', patch_test)
done.append('review#1 listRecords searches title/url/collection with escaped LIKE metacharacters instead of CAST(bookmarks AS TEXT); test proves % is literal and ids/timestamps do not match')

# review #3: CSS module declaration
ve = 'client/src/vite-env.d.ts'
vt = open(ve, encoding='utf-8-sig').read()
if 'module.css' not in vt:
    open(ve, 'w', encoding='utf-8', newline='\n').write(vt.rstrip('\n') + '\n\ndeclare module "*.module.css" {\n  const classes: { readonly [key: string]: string };\n  export default classes;\n}\n')
    done.append('review#3 `declare module "*.module.css"` restored in client/src/vite-env.d.ts')

# review #2 and #4: README structure and safe host
fe.append_section(S, 'README', '## Two lessons in one project: read the junior half first', """This course carries two different lessons. The **junior lesson** is Zod validation and partial-update semantics for a bookmark record: chapters 1, 3, 4 (validation sections), 5 exercises 1-2 and 7. The **advanced appendix** is the metadata fetcher and its SSRF defences (`server/src/services/metadata.ts`, `test/metadata.test.ts`, the DNS/redirect/port material in chapters 2, 5 exercises 3-4 and 6). Do the junior half completely before touching the appendix; the appendix assumes you already know what a private address range, a DNS rebinding and a redirect chain are.

**A safe host to practise metadata with.** Do not point `BOOKMARK_METADATA_HOSTS` at a real site. Start a local HTTPS stub (the metadata tests show how, with a self-signed certificate and a `Set-Cookie`-free response) and list only that host, e.g. `BOOKMARK_METADATA_HOSTS=localhost` with the stub on 443 or with the port the tests use; manual bookmark creation needs no metadata configuration at all.""", before='## Reading and practice order')
done.append('review#2/#4 README separates the junior lesson from the advanced appendix and gives a safe-host recipe')

B = [
("the bookmark form decides what to send",
 "`client/src/App.tsx` and `client/src/pages`: the form posts `{ title, url, collection, status, tags }` on create and only the edited keys on save; metadata fetch is a separate, optional action that the UI disables when the server reports no allowed hosts (exercise 1)."),
("the request leaves the browser",
 "`client/src/services`: `POST /api/bookmarks`, `PUT /api/bookmarks/:id`, `GET /api/bookmarks?search=...`; the envelope is unwrapped and the Zod message (`url: Invalid url`) is shown verbatim."),
("the service validates with Zod",
 "`server/src/services/service.ts`: `parseId` (line 18) bounds ids; the create/update schema is run with `safeParse` and every issue joined into one message (line 23); an empty edit is rejected (line 24); `list` (line 27) bounds `search` and `status` to 255 characters. The URL schema rejects `javascript:` and credentials in the authority."),
("the model builds one query",
 "`server/src/models/model.ts` `listRecords`: exact `status`, then a bounded `ILIKE` per text column with escaped metacharacters (the fix-pass change); `updateRecord` is one `UPDATE ... RETURNING *` with `tags` serialized only when present, so a partial `PUT` leaves them alone."),
("PostgreSQL commits the row",
 "`bookmarks` has `tags jsonb`; each write is one statement. The first test sends four malformed edits and reads the row back to prove none changed it; the new search test proves ids and timestamps are not searchable."),
("the envelope tells the client what happened",
 "`sendSuccess` / `errorMiddleware`: 201/200 with the row, 400 with the joined Zod message, 404 for a missing id. Metadata denial (host not allowed) is a 4xx that leaves the stored record intact."),
]
fe.set_boundaries(S, B); done.append('2.2 trace-lab call path section (07)')
R = [
"the capability flag must come from a server endpoint that reports whether any host is allowed (never the host list itself), the button must be disabled with an explanation when it is false, and manual entry must work in every state; assert both states in a client test.",
"the decoder must handle the named and numeric entities the tests list without executing anything (no `innerHTML`, no DOM parser that fetches), must cap input length before decoding, and must be tested against a title with nested entities and one that exceeds the cap.",
"the mixed-DNS test must return one public and one private address for the same name and assert no transfer starts; the port test must reject `https://host:8443` and `http://host:80` for the allow-listed host; explain which check runs first.",
"the redirect design must revalidate the target host against the allow-list on every hop, cap hops, keep one deadline and byte budget across hops, and never forward `Authorization` or cookies; the write-up must say why redirects stay rejected until all four hold.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')
fe.set_variations(S, """**Normal variation — a partial edit.** `PUT /api/bookmarks/:id` with `{ "status": "archived" }`. Predict 200, `status` changed, `tags` and `url` untouched. Then `{ "tags": ["a", "A"] }`: predict the stored value after de-duplication.

**Invalid variation — a dangerous URL.** `POST` with `url: "javascript:alert(1)"`, then with `https://user:password@example.com`. Predict two 400s with the Zod path in the message and no rows. Then `GET /api/bookmarks?search=%`: predict every row (before the fix pass) versus only titles containing a literal `%` (now).

**Boundary variation — a denied metadata host.** With `BOOKMARK_METADATA_HOSTS` empty, request metadata for a saved bookmark. Predict the 4xx and that the record is unchanged (first test). Then allow `localhost` and point it at the local stub from the metadata tests."""); done.append('2.4 three concrete variations')
fe.add_exercise(S, 'ownership and authorization',
"""Bookmarks have no owner. Add one end to end, keeping the metadata appendix untouched.

1. Migration: `owner text NOT NULL DEFAULT 'anonymous'` on `bookmarks`.
2. Middleware: read `X-Actor`; blank on writes -> 401.
3. `service.list` adds the owner to the filter; `get`, `update`, `remove` load with `{ id, owner }` and answer 404 for a foreign bookmark; `create` stamps the owner.
4. Test: `ana` creates two; `ben` lists (empty), gets one (404), edits (404, row unchanged); `ana` sees both; search as `ben` for `ana`'s title returns nothing.""",
"""Reference: `listRecords(query)` gains `.where("owner", query.owner)` *before* the search group so the `ILIKE` predicates are scoped; `findRecord(id, owner)` becomes `.where({ id, owner }).first()`.

Review: the owner filter and the search group must combine with AND (put the search predicates inside one `where(function () { ... })` as the model already does), otherwise `orWhereRaw` would escape the owner scope; write the failing test first to see that mistake."""); done.append('2.5 ownership/authz exercise 7 (05, 06)')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.rstrip('\n') + '\n\nToolchain recorded in the fix pass: server `zod ^3.24.1`, `knex ^3.1.0`, `typescript ^5.7.2` (see `server/package.json`; lockfiles committed for `server/` and `client/`). Automated test cases: the delivered suites plus one added test (bounded search in `server/test/bookmarks.test.ts`).\n')
done.append('review#5 VERIFICATION records the Zod/Knex/TS versions and the lockfiles')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
