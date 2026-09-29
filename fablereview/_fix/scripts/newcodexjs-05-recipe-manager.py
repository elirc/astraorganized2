import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-05-recipe-manager'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# review #2 / P4: omitted isPublic means private
def patch_service(t):
    old = "isPublic: body.isPublic !== false,"
    new = "isPublic: body.isPublic === true, // omitted means private: the safe default in an ownership course"
    assert old in t
    return t.replace(old, new, 1)
assert fe.rw('server/src/services/recipeService.ts', patch_service)
def patch_test(t):
    add = '''
test("a recipe created without isPublic is private: a non-owner cannot read it", async () => {
  const { isPublic: _omitted, ...withoutFlag } = input;
  const recipe = await service.createRecipeForUser(alice.id, withoutFlag as any);
  assert.equal((await db("recipes").where({ id: recipe.id }).first()).is_public, false);
  assert.equal(
    (await api.request("GET", `/api/recipes/${recipe.id}`, undefined, token(bob))).status,
    403,
  );
  const shared = await service.createRecipeForUser(alice.id, { ...withoutFlag, isPublic: true } as any);
  assert.equal(
    (await api.request("GET", `/api/recipes/${shared.id}`, undefined, token(bob))).status,
    200,
  );
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('server/test/ownership.test.ts', patch_test)
done.append('review#2 / P4 isPublic defaults to private when omitted (recipeService.ts:55); test proves a non-owner gets 403 unless isPublic: true was sent')

# review #1: parseRecipeInput walkthrough
svc = open('server/src/services/recipeService.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
p0 = next(i for i, l in enumerate(svc) if 'export function parseRecipeInput' in l)
fe.append_section(S, '03', '## Second excerpt: `parseRecipeInput`, three helpers and one worked input each', """`parseRecipeInput` (`server/src/services/recipeService.ts:""" + str(p0 + 1) + """`) is the densest new code in the project. It is three tiny helpers applied to a nested body:

```typescript
""" + '\n'.join(svc[p0 + 2:p0 + 16]) + """
```

- `text(value, field, limit, required)`: `undefined`/`null` is allowed unless required; anything else must be a string within `limit` after trimming. Worked input: `text("  Soup ", "Title", 255, true)` -> `"Soup"`; `text("", "Title", 255, true)` -> throws `Title must be non-empty text, at most 255 characters`; `text(undefined, "Description", 100000)` -> `undefined`.
- `positive(value, field)`: blank means absent; otherwise a safe positive integer, also accepted as a numeric string. Worked input: `positive("4", "Servings")` -> `4`; `positive(0, "Servings")` -> throws; `positive(2.5, "Prep time")` -> throws (not an integer).
- `object(value)`: an ingredient or step must be a plain object. Worked input: `object("Water")` -> throws `Ingredients and steps must be objects`; that is the third test's `TypeError`-prevention case.

Then the function applies bounds to the arrays (1-100 ingredients, 1-200 steps), validates `difficulty` and `isPublic`, de-duplicates `categoryIds` through `positive`, and only then builds the typed `RecipeInput`. Nothing has touched the database yet; a rejected body costs zero writes.""", before='## How to reason through the code')
done.append('review#1 03 second excerpt and walkthrough of parseRecipeInput with one worked input per helper')

RUN = """From the `server` folder, install dependencies once (`npm install`) and run `npm test`. The suite needs a PostgreSQL role that can `CREATE SCHEMA` in a database whose name starts with `astra_test_`; it creates a private schema per run and drops it afterwards. Point it at that database with `ASTRA_TEST_DATABASE_URL` (PowerShell: `$env:ASTRA_TEST_DATABASE_URL = "postgres://postgres:local-test@127.0.0.1:5432/astra_test_learning"`). The harness sets `JWT_ACCESS_SECRET` itself, so you do not need to configure auth secrets to run the tests.

No local PostgreSQL? Use a throwaway container and create the database once:

```powershell
docker run --rm -d --name astra-pg -e POSTGRES_PASSWORD=local-test -p 5432:5432 postgres:18
docker exec astra-pg createdb -U postgres astra_test_learning
```

Stop it with `docker stop astra-pg` when you are done; nothing persists."""
fe.rw(fe.chapter(S, '04'), lambda t: fe.replace_section(t, r'Run the checks', RUN) or t)
done.append('review#5/#6 04 "Run the checks" rewritten with the Docker fallback, privilege note and the JWT_ACCESS_SECRET note')

fe.set_variations(S, """**Normal variation — two owner updates at once.** As Alice, send two `PUT /api/recipes/:id` with different titles in a `Promise.all`. Predict: both 200, and the stored title is whichever transaction committed last. The `SELECT ... FOR UPDATE` in `updateRecipeForUser` serializes the two writes (no torn nested replacement) but it does *not* tell the loser that it overwrote a newer edit; that is what the version column in the worked example below adds.

**Invalid variation — a valid token for a deleted account.** Delete Bob's user row directly in the test schema, then call `GET /api/recipes/:id` with Bob's still-valid JWT. Predict which layer notices (the auth middleware's user lookup, or the ownership check) and the status code; then read `authService.ts` to confirm.

**Boundary variation — a duplicated category id.** Create a recipe with `categoryIds: [1, 1]`. Predict that `parseRecipeInput` de-duplicates to `[1]` before the junction insert, so no unique violation occurs; then send `[1, 0]` and predict the message from `positive`."""); done.append('review#3 three concrete concurrency/authz variations')

fe.append_section(S, '06', '### Exercise 1 — worked example: a version column for stale edits', """The row lock in `updateRecipeForUser` prevents torn writes; a `version` column prevents *silent overwrites*. Worked example:

```typescript
// migration: recipes.version integer not null default 1
// service, inside the transaction after SELECT ... FOR UPDATE:
if (input.expectedVersion !== undefined && existing.version !== input.expectedVersion)
  throw new ConflictError("This recipe changed since you loaded it. Reload and try again.");
// the update statement:
.update({ ...columns, version: existing.version + 1, updated_at: trx.fn.now() })
// errorMiddleware: ConflictError -> 409
```

Test (add to `ownership.test.ts`): create as Alice, read `version` (1); `PUT` with `expectedVersion: 1` -> 200 and the response carries `version: 2`; `PUT` again with `expectedVersion: 1` -> 409 and the stored title equals the first update's. Clients that do not send `expectedVersion` keep the old behavior, which lets you roll this out without breaking the form.

Review criterion: the comparison must happen on the locked row inside the transaction; a check before `FOR UPDATE` reintroduces the race the lock closed.""", before='## Review questions')
done.append('review#4 06 worked example for the version column (exercise 1)')

B = [
("the recipe form decides what to send",
 "`client/src/features/recipes` builds the nested body (`ingredients[]`, `steps[]`, `categoryIds[]`, `isPublic`) and sends it with the stored access token; a forged `user_id` in the body is possible from the client and is exactly what the first test sends."),
("the request leaves the browser",
 "`PUT /api/recipes/:id` with `Authorization: Bearer <access token>`; `client/src/services` unwraps the envelope. A 403 arrives as `error.message` and the form keeps its draft."),
("authentication, then validation",
 "`server/src/middleware/auth` verifies the JWT and attaches the user; the controller calls `recipeService.updateRecipeForUser(userId, id, body)`, which runs `parseRecipeInput` (line 17) on the raw body. Anything in the body that is not part of `RecipeInput`, including `user_id`, is dropped here."),
("ownership is read inside the transaction",
 "`updateRecipeForUser` (`recipeService.ts:88`) opens `db.transaction`, `SELECT ... FOR UPDATE` on the recipe, compares `user_id` with the caller and throws `ForbiddenError` (403) on mismatch, all before any write. Reads of a private recipe go through the same owner check (`is_public` false and not yours -> 403); the new fourth test proves an omitted `isPublic` means private."),
("the nested replacement commits or rolls back",
 "Still inside the transaction: update the recipe row, delete and re-insert `recipe_ingredients` and `recipe_steps`, replace the category junctions. The second test forces a late failure and shows the parent and all original children survive."),
("the envelope tells the client what happened",
 "`sendSuccess` returns the recipe with its nested children re-read from the database; `ForbiddenError` -> 403, `ValidationError` -> 400 (`parseRecipeInput` messages), `NotFoundError` -> 404."),
]
fe.set_boundaries(S, B); done.append('2.2 trace-lab call path section (07)')
R = [
"the version check must run on the row returned by `SELECT ... FOR UPDATE` inside the transaction; the test issues two sequential `PUT`s with the same `expectedVersion` and asserts 200 then 409 with the stored row equal to the first result; a client that omits `expectedVersion` must still succeed.",
"field paths must come from the helper calls (`text(item.name, \\`ingredients[${i}].name\\`, ...)`), be asserted exactly in a test (`ingredients[2].name must be non-empty text ...`), and must not change any success path.",
"the favorites regression must show that favoriting a private recipe you cannot read is 403 (not 201), that the junction row is not created, and that the owner can still favorite their own private recipe.",
"the late-failure test must break the *second* replacement (categories, after steps succeeded) with a trigger or an invalid id inserted after validation, and assert the recipe, steps and categories all equal their pre-request values.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **3**.", "Automated test cases: **3** delivered by Astra, plus **1** added in the fix pass (omitted isPublic is private), for 4 in `server/test/ownership.test.ts`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
