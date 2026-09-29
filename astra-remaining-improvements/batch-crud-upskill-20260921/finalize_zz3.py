from pathlib import Path
import json, shutil
B=Path(__file__).resolve().parent.parent
pid='c94cd4bde644'; P=B/'stage'/pid; D=P/'astraupskill'; C=B/'checks'/pid
record=json.loads((C/'astra-crud-b01-schema.json').read_text())
assert record['status']=='complete' and record['passed']
log=(C/'astra-crud-b01-schema.log').read_text()
assert '# tests 7' in log and '# pass 7' in log and '# fail 0' in log
for file in D.glob('*.md'):
    t=file.read_text()
    for filler in ['\nThat distinction is part of the skill.\n','\nAlways.\n','\nKeep unresolved questions visible for the next reviewer.\n']:
        t=t.replace(filler,'\n')
    t=t.replace('No canonical project file is changed here.', 'The original schema is retained in the linked snapshot so you can compare the accepted change with its baseline.')
    t=t.replace('omitted optional update tags pass', 'omitted optional update tags pass when another valid update field is present; an entirely empty PATCH still fails')
    t=t.replace('update with no `tagIds`', 'update with a valid subject and no `tagIds`')
    t=t.replace('Trace C: metadata update omits `tagIds`;', 'Trace C: metadata update supplies a valid subject and omits `tagIds`;')
    if file.name != 'VERIFICATION.md':
        t += '\nStudy links: [production schemas](../src/lib/validation/ticket-schemas.ts), [executed runtime tests](../tests/runtime-schema.test.mjs), and [original schema](snapshots/src/lib/validation/ticket-schemas.ts).\n'
    file.write_text(t,encoding='utf-8')
f=D/'03-WORKED-CHANGE.md'; t=f.read_text(); t+='''
For a concrete PATCH, compare `{"subject":"Updated subject"}` with
`{"tagIds":[]}`. The former preserves existing tags; the latter clears them.
`{"tagIds":["a","a"]}` now returns a schema issue at `tagIds` before the
route calls the service. The executed test checks that issue path as well as
rejection, so a failure in an unrelated required field cannot stand in for
the intended duplicate check.
'''; f.write_text(t,encoding='utf-8')
f=D/'07-TRACE-LAB.md';t=f.read_text();t+='''
| Input after authorization | Schema result | Expected next boundary |
|---|---|---|
| Create with distinct `a,b` | Accept | Service creates joins |
| Create with duplicate `a,a` | Reject | No service invocation |
| PATCH subject only | Accept; tags absent | Preserve existing joins |
| PATCH empty tag array | Accept | Clear existing joins |
| PATCH duplicate `a,b,a` | Reject at tagIds | Preserve existing state |
| Empty PATCH object | Reject | No service invocation |

Only the schema column was executed in this verification. Service effects
are predictions grounded in the route and service source, not observed SQL.
''';f.write_text(t,encoding='utf-8')
f=D/'06-SOLUTIONS-AND-REVIEW.md';t=f.read_text();t+='''
For the three-distinct-ids exercise, expect the parsed array to retain all
three ids in the supplied order. For the whitespace exercise, `min(1)`
accepts a space: it counts characters and does not trim. That is a separate
reference-validation question, not evidence that duplicate detection failed.
For the bypass exercise, a caller invoking the service directly does not run
Zod automatically. Identify that trust boundary before claiming validation
protects every possible caller. The composite Prisma primary key is the
durable safeguard; this patch adds a clearer earlier rejection for API input.
''';f.write_text(t,encoding='utf-8')
f=D/'04-TESTING-AND-DEBUGGING.md';t=f.read_text();t+='''
The executed alternative is `node --experimental-vm-modules --test
tests/runtime-schema.test.mjs` with Node 22.16.0. It loads the actual TypeScript
schema and actual Zod 4.3.6. Seven tests passed: duplicate create, duplicate
update, clear/empty PATCH rules, create defaults, omitted PATCH tags,
distinct ordered ids, and the duplicate issue path. The helper only replaces
module loading; it does not copy the schema predicate or simulate Zod.
''';f.write_text(t,encoding='utf-8')
(D/'VERIFICATION.md').write_text('''# Verification

Seven runtime tests passed against the actual ticket schemas and real Zod
4.3.6. Read the [captured output](evidence/astra-crud-b01-schema.log) and
[command record](evidence/results.json). The tested cases cover duplicate
create and update input, clear and empty-PATCH behavior, omitted create tags
defaulting to an empty array, omitted tags in a subject-only PATCH, distinct
ordered identities, and a validation issue whose path is `tagIds`.

Run `node --experimental-vm-modules --test tests/runtime-schema.test.mjs`
from the project root using Node 22.16.0. The test normally resolves this
project's declared `zod` dependency. During this verification the explicit
`CRUD_ZOD_PATH` environment override pointed to an existing Zod 4.3.6 install
in another isolated staging project, avoiding a second dependency download.
The captured record shows that exact path. It is an optional test-runner
override, not a dependency hardcoded into delivered source. Install this
project's lockfile dependencies before running the command without it.

The [runtime loader](../tests/helpers/load-typescript.mjs) reads production
TypeScript and executes it in a VM after Node's type transformation. The
[runtime suite](../tests/runtime-schema.test.mjs) supplies the real Zod module;
it does not reproduce the validator or return canned parse results. This
checks runtime behavior, not TypeScript static types. The original Vitest
suite was extended but was not executed because its dependencies were not
restored. Full typecheck, application build, and browser tests were not run.

No Prisma transaction, database uniqueness constraint, foreign key,
authorization middleware, or HTTP request was executed by these tests.
Route and service inspection confirms where the schema is called and how
tag arrays become join writes; those observations explain the fix but do
not substitute for integration tests. The [original schema snapshot](snapshots/src/lib/validation/ticket-schemas.ts)
allows a reviewer to reproduce the earlier acceptance of duplicate ids.

For a later integration exercise, submit an authenticated duplicate PATCH
to a disposable database, assert the validation response, and inspect that
existing joins remain unchanged. Then test a distinct but nonexistent tag id
separately. Those cases explore different boundaries and should not be
combined into one broad claim that every malformed relation is now safe.
''',encoding='utf-8')
result={'passed':True,'executedTests':7,'checks':[record], 'limits':[
    'Runtime schema tests used real Zod 4.3.6 through an explicit shared-install override; normal runner resolves project-local zod.',
    'Vitest, full typecheck/build, HTTP, authorization and Prisma/database integration were not executed.'
]}
(C/'results-crud-b01.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
E=D/'evidence';E.mkdir(exist_ok=True)
shutil.copyfile(C/'astra-crud-b01-schema.log',E/'astra-crud-b01-schema.log')
shutil.copyfile(C/'results-crud-b01.json',E/'results.json')
specpath=B/'specs'/f'{pid}.json';spec=json.loads(specpath.read_text())
spec['limits']=result['limits']
for name in ['astraupskill/evidence/astra-crud-b01-schema.log','astraupskill/evidence/results.json']:
    if name not in spec['changedFiles']:spec['changedFiles'].append(name)
specpath.write_text(json.dumps(spec,indent=2),encoding='utf-8')
print('zz3 evidence and teaching finalized')
