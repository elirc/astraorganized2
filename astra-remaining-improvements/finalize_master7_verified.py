"""Materialize Master7's observed checks and learner verification guide."""
from pathlib import Path
import json
import hashlib
import shutil

B = Path(__file__).resolve().parent
pid = 'a1d53294d3b0'
stage = B/'stage'/pid
checks = B/'checks'/pid
records = {}
for label in ['tests-root-01', 'typecheck-root-01', 'build-root-01']:
    record = json.loads((checks/(label+'.json')).read_text(encoding='utf-8'))
    assert record['status'] == 'complete' and record['passed'] is True and record['exitCode'] == 0
    records[label] = record
assert '19 passed (19)' in (checks/'tests-root-01.log').read_text(encoding='utf-8')
hashes = json.loads((checks/'root-final-source-hashes.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((stage/name).read_bytes()).hexdigest() == digest for name,digest in hashes.items())
evidence = stage/'astraupskill/evidence'
evidence.mkdir(parents=True, exist_ok=True)
copied = []
for source in [checks/'root-final-source-hashes.json', checks/'install-01.json', *[checks/(label+suffix) for label in records for suffix in ['.json','.log']]]:
    target = evidence/source.name
    shutil.copyfile(source,target)
    copied.append(target.relative_to(stage).as_posix())
result = {'passed': True, 'tests': 19, 'testFiles': 3, 'apiTests': 11, 'policyTests': 4, 'domainTests': 4,
          'typecheck': 'passed', 'build': 'passed', 'sourceHashesUnchanged': True, 'records': records}
(checks/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
(checks/'delivery-evidence-files.json').write_text(json.dumps(copied,indent=2)+'\n',encoding='utf-8')
(stage/'astraupskill/VERIFICATION.md').write_text('''# Verification: tenant-scoped dashboard audit logs

The reviewed change passed **19 tests in three files**, TypeScript checking, and the complete workspace build. The tests comprise eleven API tests, four policy tests and four domain tests. The newly added dashboard regression uses the actual local Express application and HTTP requests with synthetic seeded identities. This is stronger evidence than testing the new filter helper alone: removing the dashboard's call to the helper makes the organization isolation assertion fail against the two-organization fixture.

## Reproduce from the project root

Use Node 22.16 and npm 10.9.2, the versions used for this run, or verify compatibility separately when changing runtimes. The root lockfile and normal install were used; lifecycle scripts were enabled. The following commands use the package scripts already present in the project. They do not require a running PostgreSQL server.

```powershell
npm ci --no-audit --no-fund
if ($LASTEXITCODE -ne 0) { throw 'Installation failed' }
npm test -- --pool=threads --poolOptions.threads.singleThread=true --testTimeout=30000
if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }
npm run typecheck
if ($LASTEXITCODE -ne 0) { throw 'Type checking failed' }
npm run build
if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
```

The test options match this project's Vitest 2 runner. Do not copy version-specific runner flags into unrelated projects without checking their installed version. The application build runs the workspace scripts for the API, web application and shared packages. This project uses Vite for its web build; invoking a Next.js executable here is not a valid verification command.

## What was observed

The [test output](evidence/tests-root-01.log) records nineteen passing tests, and the [test process record](evidence/tests-root-01.json) records exit code zero and the command's working directory. [Typecheck output](evidence/typecheck-root-01.log) and its [process record](evidence/typecheck-root-01.json), plus [build output](evidence/build-root-01.log) and its [process record](evidence/build-root-01.json), retain the other successful checks. [Installation evidence](evidence/install-01.json) records the earlier successful normal dependency install. [Source hashes](evidence/root-final-source-hashes.json) were compared after the checks; the reviewed executable files stayed unchanged while these commands ran.

The dashboard regression signs in synthetic Acme staff, a platform administrator and a learner. The staff response must contain only Acme audit records, the platform response must include both seeded organizations, and the learner response must contain an empty audit list. The existing audit endpoint retains its own learner restriction and organization filtering. Filtering occurs before taking the first 25 records, so another organization's entries cannot consume the current organization's dashboard limit.

## Limits and the next useful test

The runtime uses the existing in-memory `store`. The Prisma schema elsewhere in the repository does not make these HTTP tests persistent-database integration tests. They establish response selection for the tested actors and fixtures, not row-level database security or behavior after a server restart. This patch does not redesign authentication, course-version submission validation, or the broader enrollment workflow. Synthetic demo credentials are teaching fixtures, not deployment credentials.

The focused source review confirmed that the policy is called by the dashboard service. A useful next exercise is to add more than 25 interleaved audit records for two organizations, then assert both the result limit and organization ownership. Another is to test every operational role explicitly using the same organization policy. These are proposed exercises; they are not included in the recorded nineteen-test count. Keep browser accessibility, a persistent adapter, concurrent writes and production deployment as separate verification scopes. A passing build is not evidence that those paths have been exercised.

An earlier ad hoc attempt invoked a missing Next executable and failed. Its raw output remains in the central history; the successful build recorded here uses the actual root `npm run build` script. Reading the exact command and exit status prevents a setup error from being mistaken for an application defect or silently counted as a pass.
''',encoding='utf-8')
spec_path = B/'specs'/(pid+'.json')
if spec_path.exists():
    spec=json.loads(spec_path.read_text(encoding='utf-8'))
    assert isinstance(spec['summary'],list)
    spec['changedFiles']=list(dict.fromkeys(spec['changedFiles']+copied))
    spec['checks']={'format':'json','resultsFile':'checks/'+pid+'/results.json','expectedTests':19,
                    'command':'npm test -- --pool=threads --poolOptions.threads.singleThread=true --testTimeout=30000; npm run typecheck; npm run build',
                    'environment':'Node 22.16; npm 10.9.2; Vitest 2; actual local HTTP API with synthetic in-memory fixtures; no PostgreSQL connection'}
    spec_path.write_text(json.dumps(spec,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'id':pid,'tests':19,'evidenceFiles':len(copied),'specUpdated':spec_path.exists()}))
