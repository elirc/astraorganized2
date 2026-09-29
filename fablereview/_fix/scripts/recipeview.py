import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'recipeview'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# --- review #1: document the fail() change
fe.append_section(S, '03', '## The error-handling change: what the browser sees and what the terminal sees', """`fail(res, e)` in `server/index.ts:94` now answers 400 with the message only for an `InputError`; every other exception becomes a generic 500 `Request failed`. The reason is to stop leaking internals (a SQLite constraint name, a file path) to the browser. The consequence for you as a debugger: when the client shows `Request failed`, the real message is in the **server terminal**, because `fail()` calls `console.error(e)` before answering. The UI cannot tell you what happened; the terminal can. Chapter 4's debugging workflow therefore starts with the terminal, not with the network panel.""", before='## How to reason through the code')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.rstrip('\n') + '\n\nNote on error messages: non-`InputError` failures are answered as a generic 500 `Request failed`; the underlying error is printed by `fail()` in `server/index.ts` on the server terminal. Read the terminal when a test or the UI reports `Request failed`.\n')
done.append('review#1 03 documents the fail() change and where the real error goes; VERIFICATION notes it')

# --- review #2, #3: 04 cleanup
def patch04(t):
    t = t.replace("```text\nnpm test\nnpm run build\n```\n", "", 1)
    t = t.replace("This project runs its real Express app through HTTP with fresh in-memory data. Browser checks exercise the built client separately. Read the project verification page for the exact observed checks and limits.",
                  "This project runs its real Express app through HTTP against a fresh SQLite database in a temporary directory (`RECIPE_LAB_DATA` is set before `server/db.ts` is imported, because the module opens the database at load time). The suite removes only that directory afterwards. Browser checks exercise the built client separately; read the project verification page for the exact observed checks and limits.", 1)
    return t
fe.rw(fe.chapter(S, '04'), patch04)
done.append('review#2/#3 04: duplicated command block removed; harness sentence now describes the temp-directory SQLite harness')

# --- review #4: two more tests
def patch_test(t):
    add = '''
test("id canonicalisation applies to write paths, and a rejected rename leaves the search index alone", async () => {
  for (const bad of ["1e2", "-1", "abc", "1.5"])
    assert.equal((await api(`/recipes/${bad}`, "PATCH", { title: "x" })).status, 400, bad);
  const before = db.prepare("SELECT title FROM search_index WHERE kind = 'dish' AND ref_id = ?").get(dish);
  assert.equal((await api(`/dishes/${dish}`, "PATCH", { name: 5 })).status, 400);
  assert.deepEqual(db.prepare("SELECT title FROM search_index WHERE kind = 'dish' AND ref_id = ?").get(dish), before);
  const padded = await api(`/dishes/0${dish}`, "PATCH", { notes: "padded id still resolves to the same row" });
  assert.equal(padded.status, 200);
  assert.equal(padded.data.id, dish);
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('test/recipes.test.ts', patch_test)
done.append('review#4 fourth test: malformed ids rejected on PATCH, a rejected dish rename leaves search_index unchanged, a zero-padded id resolves to the same row')

B = [
("the editor decides what to send",
 "`src/pages/RecipeEditor.tsx` and `DishEditor.tsx` build the payload from local form state (ingredient rows as strings, scaled quantities as numbers) and call `api.updateRecipe` / `api.updateDish` from `src/api.ts`. Quantities are parsed on the client (`shared/quantity.ts`, fractions allowed) before they are sent, but the server re-validates every row; the editor never assumes its parse is final."),
("the request leaves the browser",
 "`src/api.ts`: `updateDish(id, body)` is `PATCH /api/dishes/:id` (line 45), recipes likewise; the shared `req()` helper sets the JSON header and throws the server's `error` text. Because `fail()` hides non-input errors behind `Request failed`, the client can only ever show two kinds of message: a validation message or the generic one."),
("the `h()` wrapper validates ids and payloads before any handler",
 "`server/index.ts:69` `h(fn)` runs for every route: any `req.params` key ending in `id` must match `/^\\d+$/`, be a safe integer and be at least 1 (so `1e2`, `-1` and `1.5` are 400 before a query); for `POST` and `PATCH` (except photo uploads) it calls `validatePayload(req.body)` (line 600), which type-checks and bounds every field, tags and each ingredient row, throwing `InputError`. Then it calls the handler and routes any thrown or rejected error to `fail()`."),
("the handler and queries apply the change",
 "Each route handler in `server/index.ts` calls the functions in `server/queries.ts` (`updateRecipe`, `updateDish`, ...), which use prepared statements on the `node:sqlite` `DatabaseSync`. A nested recipe edit replaces the ingredient and step rows for that recipe and re-indexes; a dish rename updates `dishes` and its `search_index` row (`server/db.ts:39-51`)."),
("`tx()` commits the relational rows and the search index together",
 "`server/db.ts:18` `tx(fn)` runs `BEGIN`, the synchronous body, then `COMMIT`, and `ROLLBACK` on any throw. Because `node:sqlite` is synchronous, nothing can interleave inside the body; that is why a search-index failure (exercise 3) leaves the recipe untouched. Photo files on disk are outside the transaction and have their own lifecycle."),
("the response tells the client what happened",
 "Handlers answer `res.json(...)` with the updated detail; `fail()` answers 400 `{ error }` for `InputError` and 500 `{ error: \"Request failed\" }` otherwise, after `console.error(e)`. The editor then re-fetches the detail page, so the ingredient list you see is the committed one."),
]
fe.set_boundaries(S, B); done.append('2.2 six distinct trace-lab boundaries (07)')

R = [
"the message must be attached to the row whose `quantity` failed `shared/quantity.ts` parsing, the raw string must stay in the input, and the server rule must still be the authority: a client test shows the inline message, a server test shows the same row rejected with 400 by `validatePayload` and the recipe unchanged.",
"the scaled quantities must be derived state (`quantity * desiredYield / originalYield`) rendered next to the saved values, with no `PATCH` issued while previewing; assert with a client test that `api.updateRecipe` is not called until the user confirms, and that fractions round-trip through `shared/quantity.ts` formatting.",
"inject the failure inside `tx()` after the parent update (a temporary throw in the search-index insert, or a `db.exec` that drops `search_index` in the test) and assert the title, ingredients, steps and search rows all equal their pre-request values; explain which line of `server/db.ts` ran `ROLLBACK`.",
"the design must give ingredients a stable `id`, replace wholesale deletion with create/update/delete keyed by that id, keep `position` separate from identity, and describe what happens when two editors reorder concurrently (last write wins on `position`, or a version check on the recipe row).",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')

src = open('server/index.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
hstart = next(i for i, l in enumerate(src) if 'const h =' in l or 'function h(' in l) if any('const h =' in l or 'function h(' in l for l in src) else 68
vstart = next(i for i, l in enumerate(src) if 'function validatePayload' in l)
excerpt = '// server/index.ts:' + str(hstart + 1) + '\n' + '\n'.join(src[hstart:hstart + 26]) + '\n\n// server/index.ts:' + str(vstart + 1) + '\n' + '\n'.join(src[vstart:vstart + 20])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/72/server/index.ts` with `diff --strip-trailing-cr -w`): the `h()` wrapper that validates route ids and payloads for every handler, `validatePayload` as the single request-boundary validator, and `fail()` mapping `InputError` to 400 and everything else to a generic 500. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows the h() wrapper and validatePayload')

fe.set_variations(S, """**Normal variation — a partial recipe edit.** `PATCH /api/recipes/:id` with only `{ "title": "Weeknight v2" }`. Predict: 200, title changed, ingredient and step counts unchanged, and the `search_index` row for that recipe carries the new title. Read `search_index` in the SQLite file with `sqlite3` or a small script.

**Invalid variation — a bad ingredient row.** `PATCH` with `{ "ingredients": [{ "item": "Salt", "quantity": -1 }] }`. Predict 400 with the `InputError` text from `validatePayload`, and the recipe's ingredients unchanged. Then send `{ "tags": "x" }`: predict the exact message (`Tags must be at most 50 short strings`).

**Boundary variation — a failure the client cannot see.** Temporarily rename the `search_index` table in a scratch copy of the data directory and edit a dish. Predict: the browser shows `Request failed`, the terminal shows the SQLite error, and the dish name is unchanged because `tx()` rolled back. Restore the table."""); done.append('2.4 three concrete variations')

fe.add_exercise(S, 'ownership and authorization',
"""Dishes have no owner. Add one and enforce it at the `h()` boundary.

1. Migration in `server/schema.sql`: `owner TEXT NOT NULL DEFAULT 'anonymous'` on `dishes`.
2. In `server/index.ts`, read `X-Actor` in `h()` and expose it as `req.actor`; blank on `POST`, `PATCH`, `DELETE` -> 401 (a new `AuthError` mapped in `fail()`).
3. For dish and recipe writes, load the dish first and compare `owner` with `req.actor`; mismatch -> 403 through a `ForbiddenError`, before `tx()` runs. Recipes inherit their dish's owner.
4. `POST /api/dishes` sets `owner` from the header, ignoring any body value.

Acceptance, written first: cross-owner `PATCH /api/dishes/:id` is 403 and the row is unchanged; cross-owner recipe edit is 403; owner edit is 200; missing header is 401; `GET` needs no header. Extend the test `api()` helper with a headers argument.""",
"""Reference (the check runs inside `h()` after id validation, before the handler's transaction):

```typescript
class ForbiddenError extends Error {}
class AuthError extends Error {}
// in fail(): AuthError -> 401, ForbiddenError -> 403, InputError -> 400, else 500
function requireOwner(req: express.Request, dishId: number) {
  const row = db.prepare("SELECT owner FROM dishes WHERE id = ?").get(dishId) as { owner: string } | undefined;
  if (!row) throw new InputError("Dish not found");
  if (row.owner !== (req as any).actor) throw new ForbiddenError("Only the owner can change this dish.");
}
```

Reference test skeleton: create a dish with `{ "X-Actor": "ana" }`; `PATCH` it with `{ "X-Actor": "ben" }` -> 403 and `GET` deep-equals the original; `PATCH` with `ana` -> 200; `PATCH` with no header -> 401.

Review: explain why the ownership lookup is a separate read before `tx()` here (SQLite is synchronous and single-writer, so no interleaving can change `owner` between the check and the write) and what would change with PostgreSQL."""); done.append('2.5 ownership/authz exercise 7 (05, 06)')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **3**.", "Automated test cases: **3** delivered by Astra, plus **1** added in the fix pass (write-path id rules and search-index preservation), for 4 in `test/recipes.test.ts`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
