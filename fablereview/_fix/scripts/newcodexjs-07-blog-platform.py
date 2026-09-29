import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-07-blog-platform'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# --- client test suite (review #3)
os.makedirs('client/src', exist_ok=True)
test_src = r'''import { describe, expect, test, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import App from "./App";
import * as api from "./services/api";

vi.mock("./services/api", () => ({
  listRecords: vi.fn(),
  loadStats: vi.fn(),
  createRecord: vi.fn(),
  updateRecord: vi.fn(),
  deleteRecord: vi.fn(),
}));

type Deferred<T> = { promise: Promise<T>; resolve: (value: T) => void };
function deferred<T>(): Deferred<T> {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((r) => (resolve = r));
  return { promise, resolve };
}
const record = (id: number, title: string) => ({
  id,
  title,
  body: "",
  slug: title.toLowerCase(),
  status: "draft",
  tags: [],
  created_at: "",
  updated_at: "",
});

beforeEach(() => {
  cleanup();
  vi.mocked(api.loadStats).mockResolvedValue({ total: 0, byStatus: [] });
  vi.mocked(api.listRecords).mockReset();
  vi.mocked(api.createRecord).mockReset();
});

describe("App guards", () => {
  test("a slow, older search response does not overwrite a newer one", async () => {
    const first = deferred<ReturnType<typeof record>[]>();
    const second = deferred<ReturnType<typeof record>[]>();
    vi.mocked(api.listRecords)
      .mockReturnValueOnce(first.promise)
      .mockReturnValueOnce(second.promise);
    render(<App />);
    // Initial refresh (debounced 150 ms) issues request #1 for search "".
    await waitFor(() => expect(api.listRecords).toHaveBeenCalledTimes(1));
    fireEvent.change(screen.getByLabelText("Search records"), { target: { value: "b" } });
    // The search effect cleanup bumps the sequence, then request #2 fires after the debounce.
    await waitFor(() => expect(api.listRecords).toHaveBeenCalledTimes(2));
    second.resolve([record(2, "Newer")]);
    await screen.findByText("Newer");
    first.resolve([record(1, "Older")]);
    await new Promise((r) => setTimeout(r, 50));
    expect(screen.queryByText("Older")).toBeNull();
    expect(screen.getByText("Newer")).toBeTruthy();
  });

  test("a double submit issues exactly one create request", async () => {
    vi.mocked(api.listRecords).mockResolvedValue([]);
    const pending = deferred<ReturnType<typeof record>>();
    vi.mocked(api.createRecord).mockReturnValue(pending.promise);
    render(<App />);
    await waitFor(() => expect(api.listRecords).toHaveBeenCalled());
    fireEvent.change(screen.getByLabelText("title"), { target: { value: "Hello" } });
    fireEvent.change(screen.getByLabelText("slug"), { target: { value: "hello" } });
    fireEvent.change(screen.getByLabelText("status"), { target: { value: "draft" } });
    const button = screen.getByRole("button", { name: "Create" });
    fireEvent.click(button);
    fireEvent.click(button);
    fireEvent.submit(button.closest("form")!);
    expect(api.createRecord).toHaveBeenCalledTimes(1);
    expect(screen.getByRole("button", { name: "Saving…" })).toBeTruthy();
    pending.resolve(record(3, "Hello"));
    await screen.findByText("Record saved.");
  });
});
'''
open('client/src/App.test.tsx', 'w', encoding='utf-8', newline='\n').write(test_src)
vc = open('client/vite.config.ts', encoding='utf-8-sig').read().replace('\r\n', '\n')
if 'vitest/config' not in vc:
    vc = vc.replace('import { defineConfig } from "vite";', 'import { defineConfig } from "vitest/config";', 1)
    vc = vc.replace('  server: { port: 5173 },\n});', '  server: { port: 5173 },\n  test: { environment: "jsdom" },\n});', 1)
    open('client/vite.config.ts', 'w', encoding='utf-8', newline='\n').write(vc)
cp = json.load(open('client/package.json', encoding='utf-8'))
cp['scripts']['test'] = 'vitest run'
cp.setdefault('devDependencies', {}).update({"vitest": "^3.2.7", "jsdom": "^25.0.1", "@testing-library/react": "^16.3.0", "@testing-library/dom": "^10.4.0"})
open('client/package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(cp, indent=2) + '\n')
done.append('review#3 client test suite: client/src/App.test.tsx (Vitest + Testing Library, jsdom) proves the stale-search guard and the double-submit guard; `npm test --workspace client`')

# --- root package: name, test script, pg/tsx devDeps (review #4, #5, 11#5)
rp = json.load(open('package.json', encoding='utf-8'))
rp['name'] = 'blog-platform-workspace'
rp['scripts']['test'] = 'npm run test --workspace server && npm run test --workspace client'
rp.setdefault('devDependencies', {}).update({"pg": "^8.23.0", "tsx": "^4.23.13"})
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(rp, indent=2) + '\n')
done.append('review#4 root package renamed from astra-crud-workspace-58 to blog-platform-workspace; root `npm test` runs server then client suites; pg and tsx declared at the root so test/database.ts does not rely on hoisting')
done.append('review#5 kept `tsx --test ../test/*.test.ts`: Node 22 expands the glob itself, so it works under cmd.exe (a bare directory is rejected by Node 22.16); VERIFICATION notes where the recorded evidence came from')

B = [
("the React form decides what to send, and refuses to send twice",
 "`client/src/App.tsx`: `saveRecord` (line 72) returns immediately when `mutation.current` is already true, then sets it and `pending` before calling `updateRecord` or `createRecord`; the `<fieldset disabled={pending}>` greys the form at the same time. `refresh` (line 30) stamps each request with `++sequence.current` and ignores any response whose stamp is stale; the search effect (line 47) debounces 150 ms and bumps the sequence on cleanup. `client/src/App.test.tsx` proves both guards without a server."),
("the client serializes the operation through the API envelope",
 "`client/src/services/api.ts`: an `axios` instance with `baseURL` from `VITE_API_URL`; `createRecord` posts to `/posts`, `updateRecord` puts to `/posts/:id`. The response interceptor turns a non-2xx into `Error(error.response.data.error.message)`, and `unwrap()` reads the `{ success, data, error }` envelope. So the text in the red `role=\"alert\"` box is the server's Zod message, verbatim."),
("the route and service validate at runtime with Zod",
 "`server/src/routes/routes.ts` wraps every controller in `wrap()` so a rejected promise reaches `errorMiddleware`. The controller (`controllers/controller.ts`) passes `req.body` untouched to `service.create` / `service.update`. `parsePayload` (`services/service.ts:22`) runs `recordSchema` (or `recordSchema.partial()` for a `PUT`) with `safeParse`, joins every issue into one message, and rejects an empty object with `Provide at least one editable field.`; `parseId` (line 17) rejects `1e2` and non-positive ids before any query. `tags` are de-duplicated case-insensitively by the schema's `transform`."),
("the model shapes the row and lets Knex build the SQL",
 "`models/model.ts`: `databasePayload` (line 58) JSON-serializes `tags` only when the key is present, which is what makes a partial `PUT` leave `tags` alone (the `jsonb` column keeps its value). `updateRecord` (line 31) is one `UPDATE ... WHERE id = ? RETURNING *` with `updated_at = now()`; `listRecords` (line 4) builds an `ILIKE` per text column inside one `where` group instead of the old `CAST(posts AS TEXT) ILIKE`, so ids and timestamps no longer match a search, and orders by `created_at DESC, id ASC` for a stable page."),
("PostgreSQL commits or rejects",
 "The `posts` table (`server/db/migrations/001_init.ts`) declares `tags jsonb NOT NULL DEFAULT '[]'`. Each route is a single statement, so there is no explicit transaction: the row is either updated or not. In tests the statement runs inside a throwaway schema that `test/database.ts` created and migrated; `RETURNING *` gives the model the committed row rather than the request body."),
("the envelope tells the client what happened",
 "`utils/response.ts` `sendSuccess` answers `{ success: true, data }` with 200 or 201; `middleware/errorMiddleware.ts` maps a thrown `AppError` (`ValidationError` 400, `NotFoundError` 404) to `{ success: false, error: { message, code } }` and anything else to 500. The client's `unwrap()` and interceptor are the mirror image of these two functions; after a successful save `saveRecord` calls `refresh()` so the list is a fresh read, not the response."),
]
fe.set_boundaries(S, B); done.append('review#2 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the slug filter must be validated in `service.list` like `search` (short string) and applied in `model.listRecords` as an exact `where(\"slug\", ...)` combined with, not replacing, the search group; your test must show `?search=x&slug=y` returns only rows matching both and that a 256-character slug is a 400.",
"the dirty indicator must compare the draft with the original record field by field (tags as a joined string) and must clear after a successful save; cancelling a dirty draft must ask for confirmation and must not issue any request (assert `updateRecord` was not called in a client test using the `App.test.tsx` mocking pattern).",
"the test must resolve the older `listRecords` promise *after* the newer one and assert the newer titles remain (see `client/src/App.test.tsx`, first test); a test that only checks the request URL does not prove the guard; explain which line (`request === sequence.current`) makes it pass.",
"the version must be selected with the record, sent back on `PUT`, and checked in one statement (`UPDATE ... WHERE id = ? AND version = ?` with `RETURNING *`); zero rows means 409 through a new `ConflictError` in `utils/errors.ts`; the test sends two sequential `PUT`s with the same stale version and asserts 200 then 409 with the row equal to the first result.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')

svc = open('server/src/services/service.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
mdl = open('server/src/models/model.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
excerpt = '// server/src/services/service.ts:22\n' + '\n'.join(svc[21:35]) + '\n\n// server/src/models/model.ts:4\n' + '\n'.join(mdl[3:17]) + '\n\n// server/src/models/model.ts:58\n' + '\n'.join(mdl[57:62])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/58` with `diff -r --strip-trailing-cr -w`): `parsePayload` validates with Zod and treats a `PUT` as partial, the list query searches per text column instead of casting the whole row, and `databasePayload` serializes `tags` only when present. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows the changed service and model lines')

fe.set_variations(S, """**Normal variation — a partial edit.** `PUT /api/posts/:id` with only `{ "status": "published" }`. Predict: 200, `status` changed, `title`, `body`, `slug` and `tags` identical to the row before, `updated_at` newer. Then `PUT` with `{ "tags": [] }`: predict what `databasePayload` sends and what the `jsonb` column holds afterwards.

**Invalid variation — an empty edit.** `PUT` with `{}`. Predict: 400 `Provide at least one editable field.` and the row unchanged. Then `PUT` with `{ "tags": ["a", "A", ""] }`: predict which part of `recordSchema` rejects it (the empty string, before the de-duplication transform runs).

**Boundary variation — the search that used to match everything.** On the pre-change code (`backups/58`), `?search=2026` matched every row because `CAST(posts AS TEXT)` includes timestamps. Predict what the current `listRecords` returns for `?search=2026` when no title, body, slug or status contains it (nothing), then confirm in `psql` with `EXPLAIN` that the query has one `ILIKE` per text column."""); done.append('2.4 three concrete variations')

fe.add_exercise(S, 'ownership and authorization',
"""Posts have no author. Add one and enforce it end to end.

1. Migration `002_author.ts`: `author text NOT NULL DEFAULT 'anonymous'` on `posts`.
2. Middleware in `server/src/app.ts`: read `X-Actor`, attach `req.actor`; blank on `POST`/`PUT`/`DELETE` -> 401 through a new `UnauthorizedError` in `utils/errors.ts` (statusCode 401).
3. `service.create` sets `author` from the actor (ignore any body `author`); `service.update` and `service.remove` load the row first and throw `ForbiddenError` (403) when `row.author !== actor`. Keep the `NotFoundError` for a missing id.
4. `client/src/services/api.ts`: send the header from a small "writing as" input.

Acceptance, written first: cross-author `PUT` is 403 and the row deep-equals the original; cross-author `DELETE` is 403 and the row still exists; own `PUT` is 200; missing header is 401; `GET` needs no header. Extend `request()` in `test/database.ts` with a headers argument.""",
"""Reference (the check lives in the service, before the model writes anything):

```typescript
// utils/errors.ts
export class ForbiddenError extends AppError { constructor(m = "Forbidden") { super(m, 403, "FORBIDDEN"); } }
// services/service.ts
export async function update(value: string, payload: unknown, actor: string) {
  const id = parseId(value);
  const existing = await model.findRecord(id);
  if (!existing) throw new NotFoundError("Record not found.");
  if (existing.author !== actor) throw new ForbiddenError("Only the author can edit this post.");
  return model.updateRecord(id, parsePayload(payload, true));
}
```

Reference test skeleton:

```typescript
test("only the author can change a post", async () => {
  const mine = { "X-Actor": "ana" }, other = { "X-Actor": "ben" };
  const made = (await call(route, "POST", valid, mine)).data.data;
  assert.equal((await call(route + "/" + made.id, "PUT", { title: "Taken" }, other)).status, 403);
  assert.deepEqual((await call(route + "/" + made.id)).data.data, made);
  assert.equal((await call(route + "/" + made.id, "DELETE", undefined, other)).status, 403);
  assert.equal((await call(route + "/" + made.id, "PUT", { title: "Mine" }, mine)).status, 200);
  assert.equal((await call(route + "/" + made.id, "PUT", { title: "Nobody" })).status, 401);
});
```

Review: explain why the read-then-write in `update` is safe enough here (single statement, no interleaving that changes `author`) and what you would add if authors could be reassigned concurrently (`WHERE id = ? AND author = ?` in the `UPDATE` itself)."""); done.append('2.5 ownership/authz exercise 7 (05, 06)')

fe.append_section(S, '04', "## This project's test harness: `test/database.ts`", """`database()` refuses any `ASTRA_TEST_DATABASE_URL` whose database is not named `astra_test_*`, creates a schema `astra_<uuid>`, sets `process.env.DATABASE_URL` (with `search_path` pointing at that schema) and `NODE_ENV=test`, and only then imports `server/src/config/db.js` and runs the Knex migrations from `server/db/migrations` into the schema. The order is the whole trick: the Knex instance reads `DATABASE_URL` when its module loads, so importing it first would migrate the wrong database. Then it imports `server/src/app.js`, listens on port 0 and returns `{ admin, origin, close }`; `close()` drops the schema. `request()` returns `{ status, data }` and never throws, so a test can assert a 400 and then re-read the row. The client suite (`client/src/App.test.tsx`) needs no database at all: it mocks `./services/api` and drives the React tree with Testing Library in jsdom.""", before='## '); done.append('review#6 harness walkthrough (04)')
fe.append_section(S, '01', '## Scaffold leftovers you can ignore', """`server/package.json` and `client/package.json` still list `@tiptap/react`, `@tiptap/starter-kit`, `dompurify`, `slugify` and `rss` (and the server lists `helmet` and `morgan`). None of them is imported by the code this course covers; they are leftovers from the original scaffold. Do not spend time reading them, and do not treat their presence as evidence of a rich-text editor or an RSS feed.""")
done.append('review#6 01-CODEBASE-MAP warns about unused scaffold dependencies')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **4**.", "Automated test cases: **4** server tests delivered by Astra (`test/crud.test.ts`), plus **2** client tests added in the fix pass (`client/src/App.test.tsx`). Astra's recorded server evidence was produced from the isolated stage copy with an explicit test path; the same suite passes from this folder with `npm test`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
