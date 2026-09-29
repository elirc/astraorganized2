import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_blocks import apply

items = []

items.append(('buildgum', '06', '## Reviewing a backup is not replacing one',
"""The migration sketch has to fit the restore path that already exists. `restore` compares the caller's base against current bytes, then advances the revision past whatever the import claims, so a reviewed backup can never silently rewind the workspace. From `src/repository.ts:41-65`:

```ts
  async function restore(
    baseRaw: string | null,
    raw: string,
  ): Promise<Snapshot> {
    const imported = decode(raw);
    return lock(() => {
      const currentRaw = storage.getItem(STORAGE_KEY);
      if (currentRaw !== baseRaw)
        throw new Error(
          "Workspace changed while reviewing the import. Reload first.",
        );
      let revision = 0;
      try {
        revision = currentRaw === null ? 0 : decode(currentRaw).revision;
      } catch {
        /* Explicit recovery may replace invalid bytes after confirmation. */
      }
      const state = {
        ...structuredClone(imported),
        revision: Math.max(revision, imported.revision) + 1,
      };
      const encoded = encode(state);
      storage.setItem(STORAGE_KEY, encoded);
      return { state, raw: encoded };
    });
  }
```"""))

items.append(('buildgum', '07', '## The commit Lab D depends on',
"""Lab D is about an acknowledgement you did not see. Read `commit` first: the replay check runs before the base comparison, so a retried command with the same request key returns the stored receipt instead of a conflict. From `src/repository.ts:26-39`:

```ts
  async function commit(base: Snapshot, command: Command): Promise<Snapshot> {
    return lock(() => {
      const current = load();
      // A response may be lost after durable acceptance. Matching retries return the receipt.
      if (replay(current.state, command)) return current;
      if (current.raw !== base.raw)
        throw new Error(
          "Workspace changed in another tab. Export your draft, then reload.",
        );
      const state = reduce(current.state, command);
      const raw = encode(state);
      storage.setItem(STORAGE_KEY, raw); // Failure leaves the caller's accepted state untouched.
      return { state, raw };
    });
  }
```"""))

items.append(('master7', '03', '## The shipped predicate',
"""The replacement is two small functions: one exported predicate that both readers share, and the dashboard branch that still returns nothing for a learner. From `apps/api/src/services.ts:28-35`:

```ts
export function auditLogScope(actor: Actor) {
  return (log: { organizationId: string | null }) => actor.role === "PLATFORM_ADMIN" || log.organizationId === actor.organizationId;
}

function visibleAuditLogs(actor: Actor) {
  if (actor.role === "LEARNER") return [];
  return store.auditLogs.filter(auditLogScope(actor)).slice(0, 25);
}
```"""))

items.append(('master7', '04', '## Running the fixture',
"""The suite is Vitest at the repository root; `verify` is the ordered gate the repository uses, and it stops at the first failure rather than reporting a build over a red test. From the root `package.json`, `scripts`:

```bash
npm test     # vitest run
npm run verify   # db:validate && typecheck && test && build
```"""))

items.append(('master7', '06', '## Exercise 4, as the shipped test states it',
"""The assertion is not "the dashboard hides Nova rows"; it is that two endpoints return the same row IDs for the same actor, checked for a tenant admin and for the platform admin. From `apps/api/src/audit-scope.test.ts:31-42`:

```ts
  it("returns the same audit rows on the dashboard and on /audit-logs for the same actor", async () => {
    for (const email of ["admin@acme.test", "platform@lms.test"]) {
      const token = await login(email);
      const dashboard = await request("/me/dashboard", { headers: { Authorization: `Bearer ${token}` } });
      const dashboardBody = await dashboard.json() as { auditLogs: AuditRow[] };
      const endpoint = await request("/audit-logs?page=1&pageSize=25", { headers: { Authorization: `Bearer ${token}` } });
      const endpointBody = await endpoint.json() as { auditLogs: AuditRow[] };
      expect(dashboard.status).toBe(200);
      expect(endpoint.status).toBe(200);
      expect(dashboardBody.auditLogs.map((log) => log.id)).toEqual(endpointBody.auditLogs.map((log) => log.id));
    }
  });
```"""))

items.append(('master7', '07', '## The other end of the same trace',
"""Trace the paginated endpoint beside the dashboard: the learner is refused outright, the same `auditLogScope` predicate runs before the query filters, and paging happens last — which is why a noisy tenant cannot push an owner's row off page one. From `apps/api/src/services.ts:134-145`:

```ts
  auditLogs(actor: Actor, query: { action?: string; targetType?: string; page: number; pageSize: number }) {
    if (actor.role === "LEARNER") throw new Error("Forbidden");
    const scoped = store.auditLogs
      .filter(auditLogScope(actor))
      .filter((log) => !query.action || log.action.includes(query.action))
      .filter((log) => !query.targetType || log.targetType === query.targetType);
    const total = scoped.length;
    const totalPages = Math.max(1, Math.ceil(total / query.pageSize));
    const page = Math.min(query.page, totalPages);
    const start = (page - 1) * query.pageSize;
    return { auditLogs: scoped.slice(start, start + query.pageSize), pagination: { page, pageSize: query.pageSize, total, totalPages } };
  },
```"""))

items.append(('jsprojectlearn', '03', '## The pure half of the change',
"""`updateNote` never touches storage: it rejects an unknown identifier, stamps `updatedAt`, and returns a new progress object, leaving the original untouched for the debugger comparison described above. From `src/game/notes.ts:14-28`:

```ts
export function updateNote(
  progress: GameProgress,
  input: NoteInput,
  now = new Date(),
): GameProgress {
  const note = normalizeNote({ ...input, updatedAt: now.toISOString() });
  if (!progress.notes.some((item) => item.id === note.id))
    throw new Error(
      "This note no longer exists. Keep its text before loading current progress.",
    );
  return normalizeProgress({
    ...progress,
    notes: progress.notes.map((item) => (item.id === note.id ? note : item)),
  });
}
```"""))

items.append(('jsprojectlearn', '04', '## The four commands',
"""Each layer has its own command, and only the last one needs a browser runtime installed. From `package.json`, `scripts`:

```bash
npm test                        # vitest run src
npm run build                   # tsc -b && vite build
npx playwright install chromium # once, before the browser suite
npm run test:browser            # playwright test
```"""))

items.append(('jsprojectlearn', '06', '## What "demonstrates failure behavior" looks like',
"""A strong answer asserts on the refusal and on the stored bytes, not just on a thrown error. This shipped case resets identity, then proves an old tab's proposal is refused and the stored record is the reset one. From `src/game/storage.test.ts:136-157`:

```ts
it("reset checks exact raw data and changes identity so old tabs cannot resurrect drafts", async () => {
  const f = fixture();
  const lock = queue();
  const initial = await persistProgress(
    { ...createProgress(), callsign: "Old" },
    f.storage,
    lock,
  );
  const before = f.raw();
  f.storage.setItem(
    STORAGE_KEY,
    JSON.stringify({ ...initial, callsign: "Newer" }),
  );
  await expect(resetProgress(before, f.storage, lock)).rejects.toThrow(
    /changed/,
  );
  const reset = await resetProgress(f.raw(), f.storage, lock);
  expect(reset.epoch).not.toBe(initial.epoch);
  await expect(persistProgress(initial, f.storage, lock)).rejects.toThrow(
    /another tab/,
  );
  expect(loadProgress(f.storage).callsign).toBe("");
});
```"""))

items.append(('jsprojectlearn', '07', '## Inside the lock callback',
"""This is the code your Trace A breakpoint lands in and the code Trace B fails at: normalization happens outside the lock, and both revision and epoch are compared inside it before anything is written. From `src/game/storage.ts:20-36`:

```ts
export async function persistProgress(
  progress: GameProgress,
  storage: StoragePort = localStorage,
  lock: LockPort = browserLock,
): Promise<GameProgress> {
  const proposal = normalizeProgress(progress);
  return lock(() => {
    const current = loadProgress(storage);
    if (
      proposal.revision !== current.revision ||
      proposal.epoch !== current.epoch
    )
      throw new Error(
        "Progress changed in another tab. Export your pending draft or copy its text, then load current progress before retrying.",
      );
    if (current.revision === Number.MAX_SAFE_INTEGER)
      throw new Error("Save revision is exhausted. Export for recovery.");
```"""))

apply(items)
