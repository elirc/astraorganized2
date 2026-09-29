"""Finalize B1 only after root's review accepts the named terminal regression."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

B = Path(__file__).resolve().parent
pid = 'd84730649bc6'
stage = B/'stage'/pid
checks = B/'checks'/pid
label = sys.argv[1]
assert label.startswith('service-regression-')
names = [label, 'lint-04', 'typecheck-01', 'build-01']
records = {}
copied = []
evidence = stage/'astraupskill/evidence'
evidence.mkdir(exist_ok=True)
for name in names:
    run = json.loads((checks/(name+'.json')).read_text(encoding='utf-8'))
    assert run['status'] == 'complete' and run['exitCode'] == 0 and run['passed']
    assert Path(run['cwd']).resolve() == stage.resolve()
    records[name] = run
    for suffix in ['.json', '.log']:
        source = checks/(name+suffix)
        shutil.copyfile(source, evidence/source.name)
        copied.append('astraupskill/evidence/'+source.name)
baseline = json.loads((B/'baselines'/(pid+'.json')).read_text(encoding='utf-8'))
assert hashlib.sha256((stage/'astraupskill/snapshots/platform-before.ts.txt').read_bytes()).hexdigest() == baseline['files']['src/lib/platform.ts']
spec_path = B/'specs'/(pid+'.json')
spec = json.loads(spec_path.read_text(encoding='utf-8'))
readme = stage/'README.md'
text = readme.read_text(encoding='utf-8')
if 'astraupskill/README.md' not in text:
    readme.write_text(text.rstrip()+'\n\n## Incident confidentiality learning course\n\nFollow [the Astra upskilling course](astraupskill/README.md) for the code map, relationship authorization repair, regression checks, practice and solutions.\n', encoding='utf-8')
spec['summary'] = [
    'Incident detail responses authorize embedded parent and child records with the same existing policy used for direct incident access.',
    'The service regression tests hidden relationships and retained admin, matched responder and assignee access, with intercepted store reads and fail-on-write mocks in a unique temporary workspace.',
    'Nine learning guides explain the request flow, projection authorization, exact before/after code, debugging, runnable practice and solutions; original source and actual check logs accompany the course.'
]
spec['changedFiles'] = list(dict.fromkeys(spec['changedFiles']+['README.md']+copied))
# The runner now writes its compiler configuration into its unique temporary workspace.
spec['changedFiles'] = [name for name in spec['changedFiles'] if name != 'checks/incident-detail-regression.tsconfig.json']
spec['checks'] = {'format':'json', 'resultsFile':'checks/'+pid+'/results.json',
                  'command':'node checks/incident-detail-regression.mjs',
                  'environment':'Node 22.16.0, npm 10.9.2, Next 16.1.6; mocked store and unique OS temporary compilation'}
spec_path.write_text(json.dumps(spec,indent=2)+'\n',encoding='utf-8')
(checks/'results.json').write_text(json.dumps({'passed':True,'harnesses':1,'records':[name+'.json' for name in names],
    'notes':'One executable service regression harness, plus complete lint, typecheck and Next production build. Harness calls are scenarios, not a unit-test count.'},indent=2)+'\n',encoding='utf-8')
guide = f'''# Verification and repeatable checks

The revised service regression, full-project lint, TypeScript check and Next.js production build all completed with exit code zero. The application was built with Next 16.1.6 under Node 22.16.0 and npm 10.9.2. This is one executable assertion harness; its actor requests are scenarios, not separately reported unit tests.

## Repeat from the project root

```powershell
npm ci
if ($LASTEXITCODE -ne 0) {{ throw 'Dependency installation failed' }}
node checks/incident-detail-regression.mjs
if ($LASTEXITCODE -ne 0) {{ throw 'Incident detail regression failed' }}
npm run lint
if ($LASTEXITCODE -ne 0) {{ throw 'Lint failed' }}
node node_modules/typescript/bin/tsc --noEmit
if ($LASTEXITCODE -ne 0) {{ throw 'Typecheck failed' }}
npm run build
if ($LASTEXITCODE -ne 0) {{ throw 'Build failed' }}
```

Read [the regression process record](evidence/{label}.json) and [output](evidence/{label}.log), [full lint record](evidence/lint-04.json), [typecheck record](evidence/typecheck-01.json), and [build output](evidence/build-01.log). Each JSON preserves the actual command, working directory, timestamps and process exit code. Historical records contain the isolated review workspace path; the commands above run from the delivered project folder.

## What the harness exercises

The runner compiles the actual library source into a uniquely created OS temporary directory. It installs mocks on the CommonJS store module that the service's alias import actually resolves to. A read-call assertion verifies interception. Each read returns a fresh complete synthetic StoreData snapshot. Both persistence functions throw on any unexpected call, and the returned snapshots are compared after the actor requests.

The fixture has no due escalation deadlines. Under that condition, the service must hide confidential nested incidents from unauthorized actors, retain the existing authorized exceptions, omit missing relations, and leave its snapshots unchanged. Earlier review found that the first mock targeted a different copy of the module. Those earlier passing process exits are not used as proof of the repaired no-write assertions.

## Limits and review practice

This is service-level evidence with mocked storage. It does not start an HTTP server, test browser identity, or establish production authentication. The existing `as` query parameter is still a demo actor selector. The original detail service may perform escalation writes when deadlines are due; this fixture intentionally excludes that behavior. Raw parent/child identifiers and other response projections retain their existing contracts.

The production build verifies compilation and Next route generation. It does not contact live integrations, migrate a database, or prove concurrent file persistence. The runner leaves its unique temporary compilation artifacts for inspection and does not reset fixed project directories. Read [the practice exercises](05-PRACTICE.md) and [matching solutions](06-SOLUTIONS-AND-REVIEW.md), then explain why primary-record authorization alone missed the original related-record disclosure.
'''
(stage/'astraupskill/VERIFICATION.md').write_text(guide,encoding='utf-8')
print(json.dumps({'id':pid,'checkRecords':names,'evidenceFiles':len(copied),'snapshotMatchesBaseline':True}))
