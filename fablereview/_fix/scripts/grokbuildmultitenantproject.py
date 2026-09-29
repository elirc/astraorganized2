import sys, json, os, shutil
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'grokbuildmultitenantproject'; P = fe.REG[S]['abs']; os.chdir(P); done = []
CK = r'C:\Users\Owner\Desktop\AstraOrganized2\astra-remaining-improvements\checks\tenant-workspace'
BK = r'C:\Users\Owner\Desktop\AstraOrganized2\astra-remaining-improvements\backups\01e135926859\backend\src'

# review#2: snapshots + evidence into the course
os.makedirs('astraupskill/snapshots', exist_ok=True); os.makedirs('astraupskill/evidence', exist_ok=True)
shutil.copy(os.path.join(BK, 'middleware', 'tenantContext.ts'), 'astraupskill/snapshots/tenantContext-before.ts.txt')
shutil.copy(os.path.join(BK, 'controllers', 'projectController.ts'), 'astraupskill/snapshots/projectController-before.ts.txt')
copied = []
for run in ['verified', 'final', 'browser-first']:
    d = os.path.join(CK, run)
    if not os.path.isdir(d): continue
    os.makedirs(f'astraupskill/evidence/{run}', exist_ok=True)
    for f in os.listdir(d):
        if f.endswith('.json') or f.endswith('-tests.log') or f in ('migrations.log', 'seed.log'):
            shutil.copy(os.path.join(d, f), f'astraupskill/evidence/{run}/{f}'); copied.append(f'{run}/{f}')
for f in ['results.json', 'frontend-fixed.json']:
    if os.path.exists(os.path.join(CK, f)):
        shutil.copy(os.path.join(CK, f), f'astraupskill/evidence/{f}'); copied.append(f)
done.append(f'review#2 snapshots (tenantContext-before, projectController-before) and {len(copied)} evidence files copied into astraupskill/')

# review#1: name the authoritative run and narrate the failed attempt
runs = sorted(d for d in os.listdir(CK) if os.path.isdir(os.path.join(CK, d)))
fe.append_section(S, 'VERIFICATION', '## Which run the numbers refer to', f"""The delivery left several evidence directories (`{', '.join(runs)}`; copies of the JSON summaries and test logs are in `astraupskill/evidence/`). They are attempts, in order: `first` and `second` are the initial backend/frontend runs; the frontend failed two tests in an early run (`frontend-fixed.json` is the rerun after the fix); `browser-first` is the first Playwright pass; `final` and **`verified`** are the complete reruns. **`verified/` is the run the 55-check figure refers to.** Read `evidence/verified/backend.json` and `frontend.json` for the per-test list, and `evidence/results.json` for the roll-up. If your own rerun differs, compare against `verified/`, not against the earlier attempts.""", before='## ')
done.append('review#1 VERIFICATION names verified/ as the authoritative run and narrates the earlier failed frontend attempt')

# review#3: direct middleware test, and open 04 with it
open('backend/src/__tests__/tenantContext.test.ts', 'w', encoding='utf-8', newline='\n').write('''import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  prisma: {
    organizationMember: { findUnique: vi.fn() },
    project: { findMany: vi.fn(), findFirst: vi.fn(), create: vi.fn(), update: vi.fn(), delete: vi.fn() }
  }
}));
vi.mock("../lib/prisma", () => ({ prisma: mocks.prisma }));

const { attachTenantContext } = await import("../middleware/tenantContext");

function run(headers: Record<string, string>, userId?: string) {
  const req = { headers, userId } as never;
  const next = vi.fn();
  return attachTenantContext(req, {} as never, next).then(() => ({ req: req as { tenant?: unknown }, error: next.mock.calls[0]?.[0] as { status?: number } | undefined }));
}

describe("tenant context is resolved from membership, never from the header alone", () => {
  beforeEach(() => vi.resetAllMocks());

  it("fails a request with no x-org-id before any project query", async () => {
    const { error } = await run({}, "user-1");
    expect(error?.status).toBe(400);
    expect(mocks.prisma.organizationMember.findUnique).not.toHaveBeenCalled();
    expect(mocks.prisma.project.findMany).not.toHaveBeenCalled();
  });

  it("fails an unknown organization (no membership row) with 403", async () => {
    mocks.prisma.organizationMember.findUnique.mockResolvedValue(null);
    const { error, req } = await run({ "x-org-id": "11111111-1111-4111-8111-111111111111" }, "user-1");
    expect(error?.status).toBe(403);
    expect(req.tenant).toBeUndefined();
    expect(mocks.prisma.project.findMany).not.toHaveBeenCalled();
  });

  it("fails a revoked membership the same way as an unknown one", async () => {
    // A revoked member has no row (membership is deleted on revoke); the header is worthless on its own.
    mocks.prisma.organizationMember.findUnique.mockResolvedValue(null);
    const { error } = await run({ "x-org-id": "11111111-1111-4111-8111-111111111111" }, "revoked-user");
    expect(error?.status).toBe(403);
    expect(mocks.prisma.organizationMember.findUnique).toHaveBeenCalledWith({
      where: { userId_organizationId: { userId: "revoked-user", organizationId: "11111111-1111-4111-8111-111111111111" } }
    });
  });

  it("attaches the membership role, not anything the caller sent", async () => {
    mocks.prisma.organizationMember.findUnique.mockResolvedValue({ role: "MEMBER" });
    const { error, req } = await run({ "x-org-id": "11111111-1111-4111-8111-111111111111", "x-role": "OWNER" }, "user-1");
    expect(error).toBeUndefined();
    expect(req.tenant).toEqual({ userId: "user-1", organizationId: "11111111-1111-4111-8111-111111111111", role: "MEMBER" });
  });
});
''')
fe.append_section(S, '04', '## Start here: the smallest test that holds the whole lesson', """`backend/src/__tests__/tenantContext.test.ts` (added in the fix pass) drives `attachTenantContext` directly with a fake Prisma client. Four cases: no `x-org-id` header is a 400 before any query; an organization the user is not a member of is a 403 and `prisma.project.*` is never called; a revoked membership (no row) behaves exactly like an unknown one; and the role attached to the request comes from the membership row, ignoring any `x-role` the caller sends. Run it with:

```powershell
cd backend
npx vitest run src/__tests__/tenantContext.test.ts
```

Everything else in this chapter is the same idea at a larger boundary.

## Break it: turn the premise into a measurement

Open `backend/src/middleware/tenantContext.ts` and replace the membership lookup with the delivered fallback from `astraupskill/snapshots/tenantContext-before.ts.txt`:

```ts
req.currentOrgId = (req.headers["x-org-id"] as string) || "demo-org";
```

(plus the matching `req.currentOrgId || 'demo-org'` reads in `projectController-before.ts.txt`). Rerun `npx vitest run`. Predict first which of the 24 integration tests turn red: every cross-tenant read test (a forged header now *selects* a tenant instead of being checked) and every "no header" test (the fallback silently picks `demo-org`). Write the actual count in your notes, then restore the file. The difference between your prediction and the count is the part of the lesson you had not yet internalized.""", before='## ')
done.append('review#3 tenantContext.test.ts (4 direct middleware cases) added and 04 opens with it; review#5 break-it step with the delivered fallback quoted')

# review#4: cross-reference + task 1 worked solution
fe.rw('astraupskill/05-PRACTICE.md', lambda t: t.replace('## 3. Add durable create idempotency\n', '## 3. Add durable create idempotency\n\nA working implementation of exactly this exercise exists in the sibling course: `grokbuildecommerceproject/backend/src/repositories/orderRepository.ts` (the `checkout` function, from the `pg_advisory_xact_lock` line): per-caller advisory lock, request fingerprint, durable receipt row, replay-or-409. Read it after you have attempted your own.\n', 1))
fe.append_section(S, '06', '## Task 1, worked: task due dates', """**Forward migration** (`backend/prisma/migrations/<timestamp>_task_due_date/migration.sql`):

```sql
ALTER TABLE "Task" ADD COLUMN "dueDate" DATE;
CREATE INDEX "Task_organizationId_dueDate_idx" ON "Task" ("organizationId", "dueDate");
```

Nullable on purpose: existing rows have no due date and the column must not invent one. A `NOT NULL` with a default of `now()` would silently make every old task due today.

**Schema** (`schema.prisma`): `dueDate DateTime? @db.Date` on `Task`, plus `@@index([organizationId, dueDate])`.

**Validation** (`backend/src/lib/validation.ts`): `dueDate: z.string().regex(/^\\d{4}-\\d{2}-\\d{2}$/).refine(isRealCalendarDay).nullable().optional()` on both the create and update schemas. The refine is the same round-trip check used elsewhere in this batch: parse, format, compare, so `2027-02-30` is rejected.

**Service**: the create and update paths pass `dueDate` through unchanged; the list path accepts `dueBefore`/`dueAfter` query params, each validated the same way, and adds `{ dueDate: { lte, gte } }` to the tenant-scoped `where`. The tenant predicate stays first in every query.

**Tests** (`backend/src/__tests__/projectService.test.ts` style, three cases): a create with `2027-02-30` is 400 and `prisma.task.create` is not called; an update setting `dueDate: null` clears it (assert the `data` object contains `dueDate: null`, not `undefined`); a list with `dueBefore` carries both `organizationId` and the date bound in one `where`.

**UI**: a `<input type="date">` bound to the draft; on submit send the string as-is (no `Date` object, no timezone shift); show overdue tasks with the same "derived, not stored" rule as progress in task 2.""", before='## ')
done.append('review#4 05 task 3 cross-references the ecommerce checkout implementation; 06 has a full worked solution for task 1 (migration, schema, validation, service, tests, UI)')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
