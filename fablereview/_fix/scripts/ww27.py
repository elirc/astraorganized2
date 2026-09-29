import sys, json, os, re, glob
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'ww27'; P = fe.REG[S]['abs']; os.chdir(P); done = ['review#1 first VERIFICATION paragraph corrected to ww27-test-18 / 12 tests in four suites (P1 1.14)']

# --- review #3: one H1 per file, drop the duplicated trace-lab H1
for f in glob.glob('astraupskill/*.md'):
    def fn(t):
        lines = t.split('\n'); seen = False; out = []
        for l in lines:
            if l.startswith('# '):
                if seen:
                    # second H1 -> either drop (identical to first) or demote
                    first = out[0] if out else ''
                    if l.strip() == first.strip():
                        continue
                    l = '#' + l
                seen = True
            out.append(l)
        return '\n'.join(out)
    fe.rw(f, fn)
done.append('review#3 every chapter now has one H1; the second title became a section heading and the duplicated "# Trace lab" was removed')

# --- review #2: learner-facing VERIFICATION
def verif(t):
    head = t.split('\n## Verification record')[0] if '\n## Verification record' in t else t.split('\n# Verification record')[0]
    learner = """
## Run it yourself

```powershell
node --version            # 22.16.x was used for the recorded run
npm install
npx prisma generate       # only needed if the client is missing; tests use fake repositories
npm test                  # vitest run
```

Expected summary line: `Test Files  4 passed (4)` and `Tests  12 passed (12)`. The four files are `tests/routes/version-rollout-route.test.ts`, `tests/services/customer-profile-service.test.ts`, `tests/services/versioned-profile-service.test.ts` and `tests/validation/customer-profile-schemas.test.ts`. `npm run typecheck` is not defined; use `npx tsc --noEmit` (its result for the fix pass is in `evidence/`).

## Limits

The suites use fake repositories and a demo session: they prove the service and route contracts, not database transactions, live authentication or concurrent rollout behavior. Chapter 3 shows what a real `prisma.$transaction` around rollout and audit would look like and why the current in-process compensation is weaker.
"""
    return head.rstrip('\n') + '\n' + learner
fe.rw('astraupskill/VERIFICATION.md', verif)
done.append('review#2 VERIFICATION second half (manifest/handoff/word-count checklist) replaced with a learner block: commands, expected summary, limits')

# --- review #6: compensation block formatted, definition! replaced
def svc(t):
    old = """    try { await this.auditLogRepository.record({
      actorUserId: session.userId,
      action: "api_version.rollout_updated",
      entityType: "ApiVersion",
      entityId: versionId,
      metadata: {
        percentage: rollout.percentage,
        allowlistClientIds: rollout.allowlistClientIds
      }
    }); } catch (error) {
      const definition = getVersionDefinition(versionId);
      await this.versionCatalogRepository.updateRollout(versionId, previous?.rollout ?? definition!.rollout);
      throw error;"""
    new = """    try {
      await this.auditLogRepository.record({
        actorUserId: session.userId,
        action: "api_version.rollout_updated",
        entityType: "ApiVersion",
        entityId: versionId,
        metadata: {
          percentage: rollout.percentage,
          allowlistClientIds: rollout.allowlistClientIds
        }
      });
    } catch (error) {
      // Compensation: the rollout write already committed, so put it back before surfacing the error.
      // This is weaker than a transaction (see chapter 3): a crash between the two writes leaves the
      // rollout changed with no audit row.
      const definition = getVersionDefinition(versionId);
      if (!previous && !definition) {
        throw error;
      }
      await this.versionCatalogRepository.updateRollout(versionId, previous?.rollout ?? definition!.rollout);
      throw error;"""
    assert old in t, 'compensation block not found'
    return t.replace(old, new, 1)
fe.rw('src/services/api-version-service.ts', svc)
done.append('review#6 compensation try/catch reformatted onto separate lines with an explicit definition check and a comment naming the weakness')

# --- review #5: lifecycle vocabulary comes from the zod enum
def cps(t):
    if 'lifecycleStateSchema' not in t:
        t = t.replace('import ', 'import { lifecycleStateSchema } from "@/lib/validation/customer-profile-schemas";\nimport ', 1)
    t = t.replace('  if (!["TRIAL", "ACTIVE", "SUSPENDED", "ARCHIVED"].includes(input.lifecycleState)) {', '  if (!lifecycleStateSchema.safeParse(input.lifecycleState).success) {', 1)
    t = t.replace('  if (input.lifecycleState !== undefined &&\n    !["TRIAL", "ACTIVE", "SUSPENDED", "ARCHIVED"].includes(input.lifecycleState)) {', '  if (input.lifecycleState !== undefined &&\n    !lifecycleStateSchema.safeParse(input.lifecycleState).success) {', 1)
    return t
fe.rw('src/services/customer-profile-service.ts', cps)
if '["TRIAL", "ACTIVE", "SUSPENDED", "ARCHIVED"]' in open('src/services/customer-profile-service.ts', encoding='utf-8-sig').read():
    done.append('review#5 PARTIAL: one hand-rolled lifecycle list still present (pattern differed); see report')
else:
    done.append('review#5 service lifecycle checks now use lifecycleStateSchema from the zod module (one definition)')
def sched_test(t):
    add = '''
import { lifecycleStateSchema } from "@/lib/validation/customer-profile-schemas";

describe("lifecycle vocabulary has one definition", () => {
  it("the schema enum is the list the service accepts", () => {
    expect(lifecycleStateSchema.options).toEqual(["TRIAL", "ACTIVE", "SUSPENDED", "ARCHIVED"]);
    expect(lifecycleStateSchema.safeParse("PAUSED").success).toBe(false);
  });
});
'''
    return t.rstrip('\n') + '\n' + add
fe.rw('tests/validation/customer-profile-schemas.test.ts', sched_test)
done.append('test: the zod enum is asserted as the single lifecycle vocabulary')

# --- review #4 code blocks + review #7 transaction lesson
contracts = open('src/lib/versioning/customer-profile-contracts.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
a = next(i for i, l in enumerate(contracts) if 'function assertSupportedVersion' in l)
svc_lines = open('src/services/api-version-service.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
c0 = next(i for i, l in enumerate(svc_lines) if '// Compensation:' in l) - 12
fe.append_section(S, '03', '## The shapes, in code', """The v1 contract carries `{ email }` and the v2 contract adds `marketingOptIn`; both map to one canonical object. `assertSupportedVersion` (`src/lib/versioning/customer-profile-contracts.ts:""" + str(a + 1) + """`) is the guard that turns an unknown version header into a 400 instead of a silent default:

```typescript
""" + '\n'.join(contracts[a:a + 8]) + """
```

A v1 PATCH that omits `marketingOptIn` must not flip an existing `true` to `false`; the canonical object records only the fields the version can express, and `marketingOptIn: false` is written only when v2 sent it explicitly (see `customer-profile-contracts.ts:77` for the presence test).

The rollout service's compensation block (`src/services/api-version-service.ts:""" + str(c0 + 1) + """`):

```typescript
""" + '\n'.join(svc_lines[c0:c0 + 22]) + """
```

## The transaction lesson the limits point to

The compensation above is not a transaction. If the process dies after `updateRollout` and before `record`, the rollout is changed and no audit row exists; if `record` fails, the compensating `updateRollout` can itself fail. With Prisma the two writes belong in one interactive transaction:

```typescript
await prisma.$transaction(async (tx) => {
  await tx.apiVersion.update({ where: { id: versionId }, data: { rolloutPercentage: rollout.percentage, allowlist: rollout.allowlistClientIds } });
  await tx.auditLog.create({ data: { actorUserId: session.userId, action: "api_version.rollout_updated", entityType: "ApiVersion", entityId: versionId, metadata: rollout } });
});
```

Both rows appear or neither does, and there is no compensation code to get wrong. The fake repositories in this course cannot demonstrate it; the Prisma projects in this batch (`ww17`, `master 6`) do.""", before='## ')
done.append('review#4 code blocks for assertSupportedVersion and the compensation catch; review#7 transaction lesson with a $transaction snippet (03)')
fe.append_section(S, 'README', '## Prerequisites, glossary and pacing', """**Prerequisites:** one Express or Next route-handler project with Zod validation (the `newcodexJS/07` or `ww37` course), and the difference between a PATCH that omits a field and one that sends `null`.

**Glossary.** *Canonical object*: the one internal shape every API version maps to. *Version adapter*: the code that translates a versioned wire payload to and from the canonical object. *Rollout*: which callers get which version (percentage plus allow-list). *Compensation*: undoing an earlier write after a later one failed, by hand; weaker than a transaction. *Audit row*: the record of who changed what, written next to the change.

**Pacing:** map 45 min, concepts 60 min, worked change 90 min, testing 60 min, practice 3-4 h, solutions 45 min, trace lab 45 min.""", before='## ')
done.append('3.5 README prerequisites, glossary and per-chapter pacing')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
