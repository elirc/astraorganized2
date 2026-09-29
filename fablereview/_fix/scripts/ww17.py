import sys, json, os, re, glob
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'ww17'; P = fe.REG[S]['abs']; os.chdir(P); done = ['review#1 .int() on forecastAmount and review#5 duplicate createPlaybookRunSchema removal were completed by the earlier fix agent (verified on disk)']

# --- review #1: dedicated test for forecastAmount
sch = open('src/lib/validation/renewal-schemas.ts', encoding='utf-8-sig').read()
m = re.search(r'export const (\w+) = z\s*\.object\(\{[^}]*forecastAmount', sch, re.S)
schema_name = m.group(1) if m else None
if schema_name:
    def add_test(t):
        add = f'''
describe("renewal forecast validation", () => {{
  test("rejects a fractional forecastAmount on its own", () => {{
    const base = {schema_name}.parse({{ ...({schema_name}.parse ? {{}} : {{}}), }} as never) as unknown;
    void base;
  }});
}});
'''
        return t
    # simpler, robust test: build a valid sample from the schema's parse of a known-good object is not possible generically; assert the field schema directly
    def add_test2(t):
        add = f'''
describe("renewal forecast validation", () => {{
  test("rejects a fractional forecastAmount on its own", () => {{
    const shape = ({schema_name} as unknown as {{ shape: Record<string, {{ safeParse: (v: unknown) => {{ success: boolean }} }}> }}).shape;
    expect(shape.forecastAmount.safeParse(1000.5).success).toBe(false);
    expect(shape.forecastAmount.safeParse(1000).success).toBe(true);
    expect(shape.forecastAmount.safeParse(-1).success).toBe(false);
  }});
}});
'''
        return t.rstrip('\n') + '\n' + add
    fe.rw('src/tests/platform-behavior.test.ts', add_test2)
    done.append(f'review#1 test asserts {schema_name}.shape.forecastAmount rejects 1000.5 and -1 and accepts 1000')

# --- review #2: nine repeated "Applied exercise" paragraphs -> chapter-specific
specific = {
 '01': "Applied exercise for the map: list every repository method in `src/repositories/prisma/prisma-playbook-repository.ts` and `prisma-health-config-repository.ts` and write, next to each, the tenant predicate it carries (`where: { tenantId: context.tenantId, ... }`). Any method without one is a finding.",
 '02': "Applied exercise for the concepts: name the three meanings of `null` in this codebase (a nullable update result meaning \"the conditional write lost\", an explicit `outcome: null` meaning \"cleared\", and an absent field meaning \"leave it alone\") and point at the line that produces each.",
 '03': "Applied exercise for the worked change: with the before and after side by side below, write down which request in the before version could change another tenant's row (any PATCH naming a foreign id) and which line in the after version prevents it (`findFirst` scoped by tenant, then `updateMany` scoped again).",
 '04': "Applied exercise for testing: run `npm test -- --run --maxWorkers=1 --minWorkers=1`, then pick the test that covers the stale-status case and change its `expectedStatus` to the current status; predict whether it now passes for the wrong reason, run it, and restore it.",
 '05': "Applied exercise for practice: before starting exercise 1, write the tenant, actor, expected row state and postcondition for it in your notes; every exercise here starts from that four-line contract.",
 '06': "Applied exercise for the solutions: for each solution, find the assertion that would fail if the tenant predicate were dropped from `updateMany`; if you cannot find one, that is the test to add.",
 '07': "Applied exercise for the trace lab: follow one PATCH from `src/app/api/accounts/[accountId]/playbook-runs/[runId]/route.ts` (or the route that updates status) through the service to `updateStatusWithAudit` and the audit row; write the four SQL statements Prisma issues in order (`SELECT` scoped, `UPDATE ... WHERE id AND tenantId AND status`, `INSERT` audit, `SELECT` the row back).",
 'README': "Applied exercise for the index: write the tenant, actor, expected row state and postcondition for the first request you will make when you start the app, before you make it.",
 'VERIFICATION': "Applied exercise for verification: run the exact command in this file, then read `src/tests/platform-behavior.test.ts` and match each of the 12 test names to the claim in this chapter it supports.",
}
for f in glob.glob('astraupskill/*.md'):
    key = os.path.basename(f)[:2] if os.path.basename(f)[:2].isdigit() else os.path.basename(f)[:-3]
    body = specific.get(key)
    if not body:
        continue
    fe.rw(f, lambda t, body=body: re.sub(r'For (?:`[^`]+`|[A-Z0-9-]+|VERIFICATION|README), write down the tenant, actor, expected row state, and postcondition before running the command\..*?(?=\n\n|\Z)', body, t, count=1, flags=re.S))
done.append('review#2 the nine identical "write down the tenant, actor..." paragraphs replaced with one chapter-specific applied exercise each')

# --- review #4: before/after code in 03
bk = r'C:\Users\Owner\Desktop\AstraOrganized2\astra-remaining-improvements\backups\4b702f01579b\src\repositories\prisma\prisma-playbook-repository.ts'
before = open(bk, encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
b0 = next(i for i, l in enumerate(before) if 'async updateStatus(context, playbookRunId, input) {' in l)
cur = open('src/repositories/prisma/prisma-playbook-repository.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
a0 = next(i for i, l in enumerate(cur) if 'async function updateStatusWithAudit(' in l)
fe.append_section(S, '03', '## The diff that carries the lesson', """Before (`backups/.../prisma-playbook-repository.ts`, the delivered baseline): the update was **unscoped** and the tenant check ran *after* the write had already committed:

```typescript
""" + '\n'.join(before[b0:b0 + 14]) + """
```

After (`src/repositories/prisma/prisma-playbook-repository.ts:""" + str(a0 + 1) + """`): a tenant-scoped read, a conditional `updateMany` that carries the tenant and the expected status, the audit row in the same transaction, and a `null` result when the conditional write lost:

```typescript
""" + '\n'.join(cur[a0:a0 + 14]) + """
```

Read the two `where` clauses side by side. The first version could change another tenant's row and then throw; the second cannot touch a row it should not see, and a stale `expectedStatus` produces `count: 0`, which the service turns into a retryable error rather than a silent overwrite.""", before='## ')
done.append('review#4 03 shows the unscoped before and the scoped, conditional, audited after side by side')

# --- review #3 and #7: VERIFICATION for the learner, honest limits
def verif(t):
    return """# Verification

## Run it yourself

From this project directory, with Node 22.16.x:

```powershell
npm install
npx prisma generate
npm test -- --run --maxWorkers=1 --minWorkers=1
npx tsc --noEmit
```

Expected: one file, `src/tests/platform-behavior.test.ts`, 12 tests passing (13 with the forecast test added in the fix pass). The tests run against the **mock adapter**: `DATA_SOURCE` selects the repository factory (`src/repositories/repository-factory.ts:25`); it is unset by default, which means mock, and only `DATA_SOURCE=prisma` uses PostgreSQL. `tsconfig.json` sets `"incremental": false` so `tsc --noEmit` never writes a `.tsbuildinfo` into the project during checks.

## What is proven, and what is not

- The service and repository contracts are proven by the 12 mock tests: tenant scoping, conditional status updates, audit pairing, validation.
- `next build` proves compilation only.
- The Prisma adapter has **no executed evidence** in this course: no test ran `updateStatusWithAudit` against a database. `src/tests/prisma-integration.test.ts` (added in the fix pass) runs only when `WW17_TEST_DATABASE_URL` points at a disposable PostgreSQL database with the migrations applied; it fires two competing terminal updates and asserts one winner and one audit row. Run it once before trusting the adapter.
"""
fe.rw('astraupskill/VERIFICATION.md', verif)
open('src/tests/prisma-integration.test.ts', 'w', encoding='utf-8', newline='\n').write('''import { describe, it, expect } from "vitest";

// Runs only against a disposable PostgreSQL database:
//   docker run --rm -d -e POSTGRES_PASSWORD=local-test -p 5432:5432 postgres:18
//   $env:WW17_TEST_DATABASE_URL = "postgresql://postgres:local-test@127.0.0.1:5432/postgres"
//   npx prisma migrate deploy   (with DATABASE_URL set to the same URL)
//   npm test -- --run src/tests/prisma-integration.test.ts
const url = process.env.WW17_TEST_DATABASE_URL;

describe.skipIf(!url)("prisma adapter: competing terminal updates", () => {
  it("lets exactly one of two competing terminal updates win and writes one audit row", async () => {
    process.env.DATABASE_URL = url;
    const { PrismaClient } = await import("@prisma/client");
    const { createPrismaPlaybookRepository } = await import("@/repositories/prisma/prisma-playbook-repository");
    const prisma = new PrismaClient();
    const repo = createPrismaPlaybookRepository(prisma);
    const tenantId = "tenant-it";
    const run = await prisma.playbookRun.create({
      data: { tenantId, accountId: "acct-it", type: "RENEWAL", status: "IN_PROGRESS", ownerUserId: "user-it", dueDate: new Date(), notes: "" } as never,
    });
    const audit = (id: string) => ({ id, tenantId, actorUserId: "user-it", entityType: "PlaybookRun", entityId: run.id, action: "playbook.status", metadata: {}, createdAt: new Date().toISOString() });
    const [a, b] = await Promise.all([
      repo.updateStatusWithAudit({ tenantId, actorUserId: "user-it" }, run.id, { status: "COMPLETED", expectedStatus: "IN_PROGRESS", audit: audit("audit-a") } as never),
      repo.updateStatusWithAudit({ tenantId, actorUserId: "user-it" }, run.id, { status: "CANCELLED", expectedStatus: "IN_PROGRESS", audit: audit("audit-b") } as never),
    ]);
    expect([a, b].filter(Boolean)).toHaveLength(1);
    expect(await prisma.auditLog.count({ where: { entityId: run.id } })).toBe(1);
    await prisma.auditLog.deleteMany({ where: { entityId: run.id } });
    await prisma.playbookRun.delete({ where: { id: run.id } });
    await prisma.$disconnect();
  });
});
''')
done.append('review#3/#7 VERIFICATION rewritten for the learner (commands, DATA_SOURCE default, incremental:false) with honest limits; a skip-unless-configured Prisma integration test for two competing terminal updates was added but NOT executed here (no migrated database)')

# --- 3.1 code blocks in 04/06/07 and glossary
fe.append_section(S, '07', '## The four statements behind one PATCH', """```sql
-- 1. scoped read (findFirst)
SELECT * FROM "PlaybookRun" WHERE id = $1 AND "tenantId" = $2 LIMIT 1;
-- 2. conditional write (updateMany): the tenant and the expected status are both in the WHERE
UPDATE "PlaybookRun" SET status = $3, outcome = $4, "completedAt" = $5 WHERE id = $1 AND "tenantId" = $2 AND status = $6;
-- 3. the audit row, same transaction
INSERT INTO "AuditLog" (...) VALUES (...);
-- 4. the row as the client will see it
SELECT * FROM "PlaybookRun" WHERE id = $1;
```

If statement 2 reports 0 rows, statements 3 and 4 never run and the service receives `null`.""", before='## ')
fe.append_section(S, 'README', '## Prerequisites, glossary and pacing', """**Prerequisites:** one Prisma project (any of the `grokbuild*` courses) and the meaning of `where` in an `UPDATE`.

**Glossary.** *Tenant scope*: every query carries `tenantId` so a caller cannot reach another tenant's rows. *Conditional write*: an `UPDATE ... WHERE status = expected` whose row count tells you whether you won. *Audit row*: the record of the change, written in the same transaction. *Mock adapter*: the in-memory repository the tests use (`DATA_SOURCE` unset). *P2002*: Prisma's unique-violation code.

**Pacing:** map 45 min, concepts 60 min, worked change 90 min, testing 60 min, practice 3-4 h, solutions 45 min, trace lab 45 min.""", before='## ')
done.append('3.1 SQL block in 07; 3.5 README prerequisites, glossary and pacing')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
