import sys, json, os, shutil
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'grokbuildhrproject'; P = fe.REG[S]['abs']; os.chdir(P); done = []
CK = r'C:\Users\Owner\Desktop\AstraOrganized2\astra-remaining-improvements\checks\hr-workspace'
BK = r'C:\Users\Owner\Desktop\AstraOrganized2\astra-remaining-improvements\backups\baf8258948be\backend\src'

os.makedirs('astraupskill/snapshots', exist_ok=True); os.makedirs('astraupskill/evidence', exist_ok=True)
shutil.copy(os.path.join(BK, 'routes', 'leaveRoutes.ts'), 'astraupskill/snapshots/leaveRoutes-before.ts.txt')
shutil.copy(os.path.join(BK, 'services', 'leaveService.ts'), 'astraupskill/snapshots/leaveService-before.ts.txt')
shutil.copy(os.path.join(BK, 'repositories', 'leaveRepository.ts'), 'astraupskill/snapshots/leaveRepository-before.ts.txt')
copied = []
for sub in ['browser-final', 'full-first']:
    d = os.path.join(CK, sub)
    if not os.path.isdir(d): continue
    os.makedirs(f'astraupskill/evidence/{sub}', exist_ok=True)
    for f in os.listdir(d):
        if f.endswith('.json') or f.endswith('-tests.log') or f in ('migrations.log', 'seed.log'):
            shutil.copy(os.path.join(d, f), f'astraupskill/evidence/{sub}/{f}'); copied.append(f'{sub}/{f}')
shutil.copy(os.path.join(CK, 'results.json'), 'astraupskill/evidence/results.json')
fe.append_section(S, 'VERIFICATION', '## Evidence and snapshots inside the repo', f"""`astraupskill/snapshots/` now holds the delivered `leaveRoutes`, `leaveService` and `leaveRepository` as `-before.ts.txt`, so chapter 03's before/after claims can be diffed locally. `astraupskill/evidence/` holds `results.json`, `full-first/backend.json` and `frontend.json` with their test logs, and `browser-final/browser.json`, `results.json` and `browser-tests.log`. The counts in this file refer to `full-first` (backend and frontend) plus `browser-final` (browser).""", before='## ')
fe.rw('astraupskill/03-WORKED-CHANGE.md', lambda t: t.rstrip('\n') + '\n\nThe delivered versions of the three files this chapter changes are in `astraupskill/snapshots/` (`leaveRoutes-before.ts.txt`, `leaveService-before.ts.txt`, `leaveRepository-before.ts.txt`); diff them against `backend/src/` to see the whole change.\n')
done.append(f'review#1 three before-snapshots and {len(copied)} evidence files copied; linked from 03 and VERIFICATION')

fe.append_section(S, '02', '## What the single chart lock costs', """`chartLock` in `backend/src/repositories/employeeRepository.ts` takes `pg_advisory_xact_lock(74219801)`: one constant, so *every* employee create, update and reporting change in the whole system waits for every other. That is what guarantees the reporting graph never gains a cycle: two transactions cannot each see a cycle-free chart and commit changes that together form one. The cost is that all employee writes are serialized, across all departments, even ones that cannot possibly interact.

The finer alternative is a key derived from the affected chain, for example `hashtextextended(rootManagerId, 0)` where `rootManagerId` is the top of the reporting chain the change touches. Two edits in unrelated chains then proceed in parallel. The catch is that a change can *join* two chains (moving a manager under another tree), and then you must lock both roots in a fixed order or you trade the cycle bug for a deadlock. The delivered code picks the simple, provably correct option and pays in throughput; that is the right choice until a measurement says employee writes are the bottleneck. Predict: with the constant lock, what happens to leave-request writes, which do not call `chartLock`? (Nothing: they are unaffected, which is why the lock is scoped to the chart.)""", before='## ')
fe.rw('backend/src/repositories/employeeRepository.ts', lambda t: t.replace('async function chartLock(tx: Tx) {', '// One constant key: every chart write waits for every other. Correct and simple; the finer\n// per-chain key (hashtextextended(rootManagerId, 0)) is discussed in astraupskill/02-CONCEPTS.md.\nasync function chartLock(tx: Tx) {', 1))
done.append('review#2 02 names the trade-off of the constant advisory lock; a two-line comment at chartLock points at it')

fe.append_section(S, '04', '## Break it: two guards, two existing tests', """**The exclusion constraint.** In a scratch database (never the one you keep), run `ALTER TABLE "LeaveRequest" DROP CONSTRAINT "LeaveRequest_no_overlap";` and rerun `npm test` in `backend/`. Prediction: `database exclusion rejects overlap even when repository validation is bypassed` fails, because it inserts an overlapping row directly with Prisma and expects PostgreSQL to refuse; `accepts only one of two overlapping concurrent requests` still passes, because the application-level lock and the `overlap()` check in the repository catch the concurrent case first. Restore with `npx prisma migrate reset` (scratch database only).

**The pending guard.** In `backend/src/repositories/leaveRepository.ts`, remove `status: "PENDING"` from the `updateMany` `where` in `decide` (keep the pre-check above it). Prediction: `only the direct manager or HR can decide a visible non-self request` still passes, but the competing-decision test now lets a second decision overwrite the first when both read `PENDING` before either writes: the pre-check is a read, the `where` is the guard. Restore the line.

Write down, for each, whether your prediction matched. Then ask what test would catch the case where the pre-check passes but the conditional write loses (a count of 0 must become a 409, never a silent success).""", before='## ')
done.append('review#3 04 break-it section for the exclusion constraint and the PENDING guard, naming the existing tests')

fe.append_section(S, '06', '## Task 1, worked: bounded manager filter', """**Validator** (`backend/src/lib/validation.ts`), on the directory query schema: `managerId: identity.optional()` (the same UUID validator the rest of the file uses; a malformed id is a 400 before any query).

**Service / scope composition** (`employeeRepository.list`): never replace the scope; intersect with it:

```ts
where: { AND: [employeeScope(actor), managerId ? { managerId } : {}, search ? { OR: [...] } : {}] }
```

`employeeScope(actor)` for a manager already restricts rows to their reports, so a forged `managerId` for another manager intersects to an empty set: the API *safely intersects* rather than rejects. Document that choice in the endpoint comment; the alternative (403 for a non-HR caller sending `managerId`) leaks that the id exists. HR's scope is the whole company, so the filter works as a real filter for HR.

**React Query key**: `["directory", { page, search, active, department, managerId }]`; changing `managerId` resets `page` to 1 in the same state update so the key never combines a new filter with an old page.

**Tests** (four, in `backend/src/__tests__/workflow.integration.test.ts` style): an HR filter on a manager with no reports returns `{ total: 0, items: [] }`; an unknown but well-formed UUID returns the same empty shape (not 404); a malformed id is 400 with no query; a manager account filtering by *another* manager's id gets an empty result and, crucially, the same `total` the list shows, so count and rows agree.

Completion: both the displayed count and the listed rows obey the one `AND` predicate above.""", before='## ')
done.append('review#4 06 worked solution for task 1 (validator, scope intersection, query key, four tests, documented intersect-vs-reject choice)')

fe.append_section(S, 'README', '## Session boundaries', """`02-CONCEPTS.md` covers five mid-level topics; do not read it in one sitting.

- **Session 1 (about 2 h):** `01` and `02` up to the state machine (roles vs scope, owner edits, calendar days).
- **Session 2 (about 2 h):** the rest of `02` (overlap intervals, versions, transactions, the reporting-graph lock and its cost) and `03` with the snapshots open.
- **Session 3 (about 2 h):** `04` including the break-it section, then `07`.
- **Session 4+:** `05` tasks in order, checking task 1 against `06` before attempting the harder two.""", before='## ')
done.append('review#5 README session boundaries')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
