from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/2cdf30cead55'
for f in (P/'astraupskill').glob('*.md'):
    if f.name.startswith('08-'):continue
    t=f.read_text(encoding='utf-8-sig')
    t=t.replace('with one replacement','with every matching id replaced').replace('map one replacement','map all matching ids').replace('one replacement in a fresh array','replacement of all matching ids in a fresh array')
    t=t.replace('map` index branch','map` id comparison').replace('| array | one replacement |','| array | matching ids replaced |')
    t=t.replace('The helper replaces the first matching position and leaves the second unchanged; this exposes a data-quality issue rather than pretending uniqueness is enforced.','The helper replaces both matching positions, preserving the original map behavior. The new guard establishes existence, not uniqueness; duplicate cleanup is a separate data-quality policy.')
    t=t.replace('the two focused runtime cases','the three focused runtime cases')
    t=t.replace('The replacement array is immutable, so existing references are not mutated while a component renders.','The helper builds a fresh array without mutating its input. Unchanged records retain their original object references, and the replacement object is shared by matching positions; this is shallow structural preservation, not deep immutability.')
    t=t.replace('Authorization is local: this app has no server tenant boundary in the context.','The context provides no server authorization or tenant boundary; this helper is an identity check, not an access-control mechanism.')
    t=t.replace('A successful update should imply that one resource was selected and replaced.','A successful helper call implies at least one matching id existed in the supplied array. It does not establish that ids are unique.')
    t=t.replace('That means the missing identity error occurs before any promise is awaited. A screen can catch it at submit time.','The helper throws before the storage await. Because its context caller is async, the screen receives a rejected promise and must await or catch that promise.')
    if f.name=='03-WORKED-CHANGE.md':
        t+='\nCaller review found existing save-error handling in all six form paths. Feed usage delegates through saveUsage, whose normal submit awaits inside try/catch and whose warning-button path attaches catch. This was inspected in source, not exercised through React. The helper checks the collection captured by the callback; it does not reread AsyncStorage, so it cannot detect every stale-screen or concurrent deletion scenario.\n'
    if f.name=='04-TESTING-AND-DEBUGGING.md':
        t+='\nThe third runtime case preserves replacement of every duplicate id. The first now freezes both the input array and its records, checks a fresh output array, and verifies an unchanged neighbor retains its reference. The missing-id case also covers an empty array. These assertions establish helper behavior; the storage rows in the trace are source-inspected consequences, not recorded writer calls.\n'
    if f.name=='06-SOLUTIONS-AND-REVIEW.md':
        t+='\nFor the stale-screen prediction, distinguish the current array from a captured old array. If the callback receives a collection without A, the guard rejects. If its closure still contains A, the guard accepts; preventing resurrection requires a separate persistence/version policy. For duplicate ids, replace all matching positions to retain the baseline contract. An empty array rejects, and extra replacement fields remain intact because the helper returns the supplied object.\n'
    f.write_text(t,encoding='utf-8')
v=P/'astraupskill/VERIFICATION.md'
v.write_text('''# Verification record

Run from this project root:

```text
node --experimental-strip-types --test tests/collection-runtime.test.mjs
```

The captured Astra run executed three passing tests against the actual [collection helper](../src/utils/collection.ts), with zero failed or skipped cases. The first freezes the input array and records, verifies an order-preserving replacement, checks that the returned array is new, and confirms that an unchanged neighbor keeps its reference. The second checks the stable missing-id error for both an occupied collection and an empty one. The third verifies that duplicate ids retain the original behavior: all matching positions receive the replacement, while unrelated positions remain unchanged.

The executable evidence is [collection-runtime.test.mjs](../tests/collection-runtime.test.mjs). Node strips TypeScript syntax and imports the production helper directly. This is neither a copied algorithm nor a mounted React test. The separate TypeScript test file follows the repository's test shape, but the captured evidence belongs to the portable MJS command above. No full typecheck, Expo render, AsyncStorage integration, or native package-suite pass is claimed.

Source review of [AppDataContext.tsx](../src/context/AppDataContext.tsx) confirms all six update callbacks invoke the helper before their storage writer and state setter. Review also inspected each form's existing promise-error handling, including FeedUsageFormScreen's saveUsage wrapper and warning-button catch. These are source-level observations. The focused tests do not record persistence calls or prove that an alert appears on screen.

The exact original context is in [the snapshot](snapshots/src/context/AppDataContext.tsx). The helper validates the supplied collection, which may be captured by a React closure. It does not reread storage or solve races between whole-array writes. An old closure that still contains a deleted id can therefore pass this guard; a persistence version check would be a separate change. This distinction keeps a useful existence contract from being overstated as offline synchronization or conflict prevention.
''',encoding='utf-8')
s=B/'specs/2cdf30cead55.json';j=json.loads(s.read_text(encoding='utf-8-sig'))
j['changedFiles']=[n for n in j['changedFiles'] if n not in ['astraupskill/evidence/results-crud-b03.json','astraupskill/evidence/astra-crud-b03-masterrnative.log']]
j['limits']=['Three runtime cases execute only the actual identity helper; the six context call sites and form error handlers were reviewed in source, not mounted.','No Expo rendering, AsyncStorage integration, full typecheck or package-suite pass is claimed. The helper checks the supplied array and does not prevent stale-closure or concurrent whole-array writes.']
s.write_text(json.dumps(j,indent=2))
