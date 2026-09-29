import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_blocks import apply

items = []

items.append(('buildantigvg', '04', '## The commands these suites run under',
"""Every suite named above is reachable from the root `package.json` scripts; nothing here needs a hand-written jest invocation. These are the exact script lines (root `package.json`, `scripts`).

```bash
npm run test:api    # -> npm run test -w apps/api  -> jest --runInBand
npm run test:web    # -> playwright test
npm run test:e2e    # -> node scripts/test-database.mjs
npm run lint        # -> tsc --noEmit (api) && eslint (web)
```"""))

items.append(('buildantigvg', '07', '## The routes the cross-tenant probe hits',
"""The GET/PUT/status/delete calls in the ownership round all enter through one controller, and none of them accept a tenant from the body: the tenant travels on `req.actor`, which the guard loads from PostgreSQL. From `apps/api/src/workers.ts:233-246`:

```ts
  @Get("workers") list(@Req() req: ActorRequest, @Query() q: unknown) {
    return this.workers.list(req.actor, q);
  }
  @Get("workers/:id") get(@Req() req: ActorRequest, @Param("id") id: string) {
    return this.workers.get(req.actor, id);
  }
  @Post("workers") async create(
    @Req() req: ActorRequest,
    @Body() body: unknown,
    @Res({ passthrough: true }) res: Response,
  ) {
    const worker = await this.workers.create(req.actor, body);
    res.setHeader("Location", `/api/workers/${worker.id}`);
    return worker;
  }
```"""))

items.append(('jstrain2-3', '04', '## What `npm test` actually runs',
"""`npm test` is not a wildcard handed to a shell. `scripts/test.mjs` reads the `test/` directory itself and passes the explicit file list to Node's test runner, which is why the same command behaves identically on Windows and Unix. The whole script:

```js
import { readdirSync } from "node:fs";
import { spawnSync } from "node:child_process";
const files = readdirSync(new URL("../test/", import.meta.url))
  .filter((name) => name.endsWith(".test.mjs"))
  .sort()
  .map((name) => "test/" + name);
const result = spawnSync(process.execPath, ["--test", ...files], {
  stdio: "inherit",
  cwd: new URL("../", import.meta.url),
});
if (result.error) console.error(result.error.message);
process.exitCode = result.status ?? 1;
```"""))

items.append(('jstrain2-3', '07', '## The guard your `If-Match` header meets',
"""In Lab A and Lab B the quoted revision you read in DevTools is checked before any transaction starts. This is the whole check, from `src/lib/workspaceApi.mjs:70-75`; note that a missing or unquoted header is a 428, not a 409 conflict.

```js
function revision(request) {
  const raw = request.headers.get("if-match");
  if (!raw || !/^"[a-f0-9]{64}"$/.test(raw))
    throw fail("A quoted accepted revision is required in If-Match", 428);
  return raw.slice(1, -1);
}
```"""))

items.append(('d1', '04', '## The exact test command',
"""The regression suite is two explicit files handed to Node's runner through `tsx`; there is no watcher and no config file to discover. From `package.json`, `scripts.test`:

```bash
npm run test
# node --import tsx --test tests/socket-actions.test.ts tests/card-move-position.test.ts
```"""))

items.append(('d1', '07', '## The handler the trace starts in',
"""This is the registration the trace enters, from `src/lib/socket/actions.ts:249-272`. Read the three `hasOwnProperty` checks: they are the reason `{dueAt: null}` reaches the service as an explicit clear while an omitted key stays omitted.

```ts
  onAsync("card:update", async (payload: ClientToServerPayloads["card:update"]) => {
    try {
      if (!payload?.boardId || !payload.cardId || !Number.isSafeInteger(payload.expectedVersion) || payload.expectedVersion < 1) {
        emitError(payload?.boardId, "A valid board, card, and expected version are required");
        return;
      }
      const rawPatch = cardUpdatePatchSchema.parse(payload.patch);
      const patch: { title?: string; description?: string | null; dueAt?: Date | null } = {};
      if (Object.prototype.hasOwnProperty.call(rawPatch, "title")) patch.title = rawPatch.title;
      if (Object.prototype.hasOwnProperty.call(rawPatch, "description")) {
        patch.description = rawPatch.description ?? null;
      }
      if (Object.prototype.hasOwnProperty.call(rawPatch, "dueAt")) {
        patch.dueAt = rawPatch.dueAt === null || rawPatch.dueAt === undefined ? null : new Date(rawPatch.dueAt);
      }
      const result = await services.updateCardDetails({
        boardId: payload.boardId,
        cardId: payload.cardId,
        actorId: user.id,
        patch,
        expectedVersion: payload.expectedVersion
      });
```"""))

apply(items)
