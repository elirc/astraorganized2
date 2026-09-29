import sys, json, os, shutil
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'buildantigvg'; P = fe.REG[S]['abs']; os.chdir(P); done = []
CK = r'C:\Users\Owner\Desktop\AstraOrganized2\astra-remaining-improvements\checks\workforce'

# review#1 evidence
os.makedirs('astraupskill/evidence', exist_ok=True); copied = []
for sub in ['fourth', 'browser']:
    d = os.path.join(CK, sub)
    if not os.path.isdir(d): continue
    os.makedirs(f'astraupskill/evidence/{sub}', exist_ok=True)
    for f in os.listdir(d):
        if f.endswith('.json') or f.endswith('-tests.log') or f in ('migrations.log', 'seed.log', 'frontend-lint.log', 'frontend-typecheck.log'):
            shutil.copy(os.path.join(d, f), f'astraupskill/evidence/{sub}/{f}'); copied.append(f'{sub}/{f}')
if os.path.exists(os.path.join(CK, 'results.json')):
    shutil.copy(os.path.join(CK, 'results.json'), 'astraupskill/evidence/results.json'); copied.append('results.json')
fe.append_section(S, 'VERIFICATION', '## Evidence inside the repo', f"""Copies of the recorded runs live in `astraupskill/evidence/`: `fourth/backend.json` and `fourth/backend-tests.log` (the API suite), `browser/browser.json` and `browser/browser-tests.log` (the Playwright pass), and `results.json` (the roll-up). The 37-check total is the sum of the backend run in `fourth/` and the browser run in `browser/`; they were not produced by one invocation, so treat `results.json` as a composition of two runs, not as a single transcript. A single end-to-end rerun was not performed in the fix pass (it needs the `scripts/test-database.mjs` PostgreSQL bootstrap and a Playwright Chromium).""", before='## ')
done.append(f'review#1 {len(copied)} evidence files copied into astraupskill/evidence/ and linked from VERIFICATION; review#5 the two-run composition is stated instead of hidden (no rerun possible here)')

# review#2 break-it chapter
open('astraupskill/03b-BREAK-IT.md', 'w', encoding='utf-8', newline='\n').write("""# 03b. Break it first

[Course index](README.md) · [Previous: worked change](03-WORKED-CHANGE.md) · [Next: testing](04-TESTING-AND-DEBUGGING.md)

Each step removes one guard, predicts the failure, runs the suite, then restores the guard. Do not skip the prediction: it is the measurement.

## 1. Lose the version predicate

In `apps/api/src/workers.ts`, inside `update`, delete the line `version,` from the `updateMany` `where` clause (keep `tenantId` and the status predicate). Prediction: the concurrency spec in `apps/api/test/workers.spec.ts` that updates the same worker from two stale clients no longer sees a `ConflictException` on the second write; the second client's data silently overwrites the first (a lost update), and `version` still increments twice, so the row *looks* healthy. Run `npm test --workspace @workforce/api` (or the api workspace's `npm test`). Note which assertion fails and what the persisted row contains. Restore the line.

## 2. Lose the tenant predicate on read

In `get`, change `where: { id: input.id.parse(id), tenantId: actor.tenantId }` to `where: { id: input.id.parse(id) }`. Prediction: the cross-tenant spec that fetches another tenant's worker id now returns 200 with the foreign row instead of 404; every list test still passes because `list` keeps its own predicate. This is why the tests exist per operation. Restore the line.

## 3. Lose the terminated guard

Remove `employmentStatus: { not: "TERMINATED" }` from the `updateMany` `where`. Prediction: the pre-check (`if (current.employmentStatus === "TERMINATED") throw`) still catches the serial case, so the spec that edits a terminated worker still passes. Only a concurrent terminate-then-update loses its protection, which no unit test covers. Write the test that would (two transactions, one terminating between the read and the write), or accept that this guard is proven only by reasoning. Restore the line.

What you should have noticed: step 1 is caught by an existing test, step 2 by an existing test, step 3 by nothing. Pick your next exercise from `05-PRACTICE.md` accordingly.
""")
fe.rw('astraupskill/README.md', lambda t: t.replace('03-WORKED-CHANGE.md)', '03-WORKED-CHANGE.md), then [03b: break it first](03b-BREAK-IT.md)', 1) if '03-WORKED-CHANGE.md)' in t else t.rstrip('\n') + '\n\nAfter chapter 03 read [03b: break it first](03b-BREAK-IT.md).\n')
done.append('review#2 03b-BREAK-IT.md (version predicate, tenant predicate, terminated guard) with predictions and a README link')

# review#3 worked solution for exercise 1
fe.append_section(S, '06', '## Exercise 1, worked: department filter', """**`apps/api/src/validation.ts`**, in the `query` schema:

```ts
department: z.string().trim().min(1).max(100).optional(),
```

Bounded like the profile field (100), optional, trimmed. An empty string after trim is *absent*, not "match the empty department"; if you want the latter, add an explicit `department=none` token and a test for it.

**`apps/api/src/workers.ts`**, in `list`, extend the `where` that both queries share:

```ts
const where = {
  tenantId: actor.tenantId,
  ...(q.status ? { employmentStatus: q.status } : {}),
  ...(q.department ? { department: q.department } : {}),
  ...(q.search ? { OR: [ /* unchanged */ ] } : {}),
};
```

Both `count` and `findMany` in the `RepeatableRead` transaction use the same `where`, so `total` and `items` describe one filtered view. The tenant predicate stays first.

**`apps/web/src/App.tsx`**: one more piece of query state, a labelled `<select aria-label="Department">` (or a text input) that calls `setDepartment(value); setPage(1);`, and `department` added to the effect's dependency list next to `page, query, status`. Keep the existing "ignore a late response" guard (`reload` token) so a slow response for the previous department cannot overwrite the current page.

**`apps/api/test/workers.spec.ts`**, three cases: two tenants with a `Finance` department each, a `Finance` filter in tenant A returns only A's rows and `total` equals `items.length`; `department=` (empty) behaves like no filter; a filter change resets to page 1 (assert the request's `page` param in the frontend test, or the API's `page: 1` in the response).

Acceptance is met when the count and the list obey the same predicate, and when the two-tenant test fails if you remove `tenantId` from `where`.""", before='## ')
done.append('review#3 06 worked solution for exercise 1 (validation, shared where, UI, three tests)')

# review#4 01 section on App.tsx
fe.append_section(S, '01', '## `apps/web/src/App.tsx`: one file, two kinds of state', """The web app is a single 605-line component. Two pieces of state matter for the conflict exercise in chapter 03: `editing` (`useState<Worker | null>`, the *saved* worker being edited, including its `version`) and `draft` (`useState<Profile>`, the form's unsaved text). They are deliberately separate: a PUT sends `{ ...draft, version: editing.version }`, so the version the server checks is the one the user *loaded*, not something typed. On a 409 the app keeps `draft` and offers to reload `editing` ("Replace the form with the current saved worker? Copy any draft text you want to keep first."), which is the whole point of the split: the server refuses, the user loses nothing. Read the effect that fetches the list (it depends on `page`, `query`, `status` and a `reload` token) and the submit handler before attempting the two-tab exercise.""", before='## ')
done.append('review#4 01 explains the draft vs editing state split in App.tsx')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
