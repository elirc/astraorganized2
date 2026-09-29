"""Capture reviewed Grok PPM evidence; refuse unfinished or failed checks."""
from pathlib import Path
import hashlib
import json
import re
import shutil

B = Path(__file__).resolve().parent
pid = '475084a31c00'
stage = B/'stage'/pid
checks = B/'checks'/pid
names = ['backend-prisma-validate-03', 'backend-prisma-generate-01',
         'backend-build-04', 'backend-test-04', 'frontend-test-03', 'frontend-build-03']
records = {}
for name in names:
    run = json.loads((checks/(name+'.json')).read_text(encoding='utf-8'))
    assert run['status'] == 'complete' and run['passed'] and run['exitCode'] == 0, name
    assert Path(run['cwd']).resolve() == (stage/name.split('-')[0]).resolve()
    records[name] = run
for name, expected in [('backend-test-04', 8), ('frontend-test-03', 6)]:
    log = (checks/(name+'.log')).read_text(encoding='utf-8')
    assert re.search(r'Tests\s+'+str(expected)+r' passed \('+str(expected)+r'\)', log), name
baseline = json.loads((B/'baselines'/(pid+'.json')).read_text(encoding='utf-8'))['files']
snapshot_map = {
    'taskService': 'backend/src/services/taskService.ts',
    'taskRoutes': 'backend/src/routes/taskRoutes.ts',
    'taskController': 'backend/src/controllers/taskController.ts',
    'index': 'backend/src/index.ts',
    'portfolioService': 'backend/src/services/portfolioService.ts',
    'authService': 'backend/src/services/authService.ts',
    'client': 'frontend/src/api/client.ts',
}
for name, original in snapshot_map.items():
    snapshot = stage/'astraupskill/snapshots'/(name+'-before.ts.txt')
    assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == baseline[original]
evidence = stage/'astraupskill/evidence'
evidence.mkdir(exist_ok=True)
copied = []
for name in names:
    for suffix in ['.json', '.log']:
        source = checks/(name+suffix)
        shutil.copyfile(source, evidence/source.name)
        copied.append('astraupskill/evidence/'+source.name)
spec_path = B/'specs'/(pid+'.json')
spec = json.loads(spec_path.read_text(encoding='utf-8'))
spec['changedFiles'] = list(dict.fromkeys(spec['changedFiles']+copied))
spec['checks'] = {'format': 'json', 'resultsFile': 'checks/'+pid+'/results.json', 'expectedTests': 14,
    'command': 'Backend: npm test -- --reporter=dot; frontend: npm test -- --run; both package builds and Prisma validate/generate',
    'environment': 'Node 22.16.0/npm 10.9.2; Express 4, Prisma 5.22, Vitest 1.6.1 and Vite 5.4.21; mocked database and fetch, loopback HTTP; no database writes'}
spec['limits'] += [
    'The frontend task and project pages remain list scaffolds; create/edit screens and browser-to-PostgreSQL end-to-end behavior are future work.',
    'Existing auth error classification and demo JWT secret fallback remain; organization membership and record ownership are not enforced.',
]
spec['limits'] = list(dict.fromkeys(spec['limits']))
spec_path.write_text(json.dumps(spec, indent=2)+'\n', encoding='utf-8')
(checks/'results.json').write_text(json.dumps({'passed': True, 'total': 14, 'passedTests': 14, 'failed': 0,
    'suites': {'backend': 8, 'frontend': 6}, 'records': [name+'.json' for name in names]}, indent=2)+'\n', encoding='utf-8')
guide = '''# Verification and repeatable checks

The final backend suite passed eight tests, and the frontend passed six tests across its task-list and API-client suites: fourteen tests in total. Both TypeScript builds completed successfully, including the frontend Vite production build. Prisma schema validation and client generation also completed successfully. These are actual completed process records, not proposed checks.

## Run from the delivered project

Open a PowerShell terminal in the project root. Backend and frontend are separate npm packages, each with its own lockfile. The following backend commands use a dummy local URL for generation and validation only; neither command connects to PostgreSQL or changes its schema.

```powershell
Set-Location backend
npm ci
if ($LASTEXITCODE -ne 0) { throw 'Backend install failed' }
$priorDatabaseUrl = $env:DATABASE_URL
try {
  $env:DATABASE_URL = 'postgresql://user:pass@127.0.0.1:5432/ppm'
  npx prisma validate
  if ($LASTEXITCODE -ne 0) { throw 'Schema validation failed' }
  npm run prisma:generate
  if ($LASTEXITCODE -ne 0) { throw 'Client generation failed' }
} finally {
  $env:DATABASE_URL = $priorDatabaseUrl
}
npm test -- --reporter=dot
if ($LASTEXITCODE -ne 0) { throw 'Backend tests failed' }
npm run build
if ($LASTEXITCODE -ne 0) { throw 'Backend build failed' }
Set-Location ../frontend
npm ci
if ($LASTEXITCODE -ne 0) { throw 'Frontend install failed' }
npm test -- --run
if ($LASTEXITCODE -ne 0) { throw 'Frontend tests failed' }
npm run build
if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed' }
Set-Location ..
```

The recorded environment used Node 22.16.0, npm 10.9.2, Prisma 5.22, Vitest 1.6.1 and Vite 5.4.21. The preserved JSON files contain exact commands, working directories, timestamps, exit codes and environment overrides. Their original paths point to the isolated review workspace; the commands above work from the delivered project. See [backend tests](evidence/backend-test-04.log), [backend build](evidence/backend-build-04.json), [frontend tests](evidence/frontend-test-03.log), [frontend build](evidence/frontend-build-03.json), [Prisma validation](evidence/backend-prisma-validate-03.json), and [client generation](evidence/backend-prisma-generate-01.json).

## What the checks establish

The backend uses the actual Express routes on an ephemeral loopback port, with Prisma mocked at its imported module. It checks strict validation, normalized persistence arguments, omission versus null, missing-record classification, safe outage responses and malformed JSON. Unknown PATCH fields stop before a write. The frontend tests task rendering and fetch response handling, including empty 204 deletes, direct auth payloads, CRUD envelopes and readable errors. Mocks reset between cases and the server closes after the suite.

The snapshots preserve seven exact original files so a learner can compare the original create allowlist with the unsafe original PATCH forwarding. The course does not claim that create originally permitted arbitrary Prisma writes. The review also repaired mismatched client organization inputs and response shapes; these defects required behavioral tests because compilation alone could not expose them.

## Practical limits

No PostgreSQL database, migration, production server, real account, external notification or browser end-to-end flow was used. A mock call cannot prove foreign-key enforcement or persistence durability. Organization identifiers must refer to records you create in a disposable development database before using registration or portfolio creation against it; no organization bootstrap endpoint is implemented. The task/project screens remain list scaffolds. Membership authorization, pagination and production identity remain future exercises. Existing auth failure classification and the demo JWT fallback also remain, so passing this course's checks does not establish production readiness.
'''
(stage/'astraupskill/VERIFICATION.md').write_text(guide, encoding='utf-8')
print(json.dumps({'id': pid, 'tests': 14, 'evidenceFiles': len(copied), 'snapshots': len(snapshot_map)}))
