"""Normalize reviewed Master4 evidence without rerunning or inventing results."""
from pathlib import Path
import json
import shutil
import hashlib

B = Path(__file__).resolve().parent
pid = '3302b1d1ab07'
stage = B/'stage'/pid
checks = B/'checks'/pid
labels = ['npm-ci-3', 'prisma-generate', 'db-push', 'db-seed-absolute', 'inventory-rules', 'typecheck-2', 'build-2', 'full-test-absolute']
records = {}
evidence = stage/'astraupskill/evidence'
evidence.mkdir(exist_ok=True)
copied = []
for label in labels:
    record = json.loads((checks/(label+'.json')).read_text(encoding='utf-8'))
    assert record['status'] == 'complete' and record['exitCode'] == 0 and record['passed'] is True, label
    records[label] = record
    for suffix in ['.json', '.log']:
        source = checks/(label+suffix)
        assert source.is_file()
        target = evidence/source.name
        shutil.copyfile(source, target)
        copied.append(target.relative_to(stage).as_posix())
log = (checks/'full-test-absolute.log').read_text(encoding='utf-8')
assert '12 passed (12)' in log and '2 passed (2)' in log
assert '9 passed (9)' in (checks/'inventory-rules.log').read_text(encoding='utf-8')
hashes = {p: hashlib.sha256((stage/p).read_bytes()).hexdigest() for p in ['src/shared/inventoryRules.ts', 'tests/inventoryRules.test.ts']}
assert hashes['src/shared/inventoryRules.ts'] == 'bce8e7fd3d5ccf886241fb6347451c2580ebfdd4f2fa4ddebef3f57b611b2e7a'
assert hashes['tests/inventoryRules.test.ts'] == 'be8cad44448297e63dca3f114583d21d4faf151c0eb5790933ebf22867b19870'
results = {'passed': True, 'tests': 12, 'testFiles': 2, 'domainTests': 9, 'apiReadTests': 3, 'typecheck': 'passed', 'build': 'passed', 'sourceHashes': hashes, 'records': records}
(checks/'results.json').write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')
spec_path = B/'specs'/(pid+'.json')
spec = json.loads(spec_path.read_text(encoding='utf-8'))
if isinstance(spec['checks'], list):
    spec['recordedChecks'] = spec['checks']
spec['summary'] = [
    'Aggregate duplicate SKU lines before comparing requested inventory with available stock; reject invalid quantities and direct helper over-reservation.',
    'Add regression coverage for duplicate demand, invalid quantities and direct helper guards; the complete suite passes 12 tests, type checking and the client build.',
    'Add nine source-linked learning guides, an exact original rule snapshot, worked practice solutions and actual verification evidence.'
]
spec['checks'] = {'format': 'json', 'resultsFile': 'checks/'+pid+'/results.json', 'expectedTests': 12, 'command': 'npm ci; npm run db:generate; npm run db:push; npm run db:seed; npm test; npm run typecheck; npm run build', 'environment': 'Node 22.16; npm 10.9.2; disposable staged SQLite with absolute DATABASE_URL'}
spec['limits'] = [
    'Nine pure inventory rule tests and three API health/read/export tests pass. The API suite does not execute reservation writes or prove persistent reservation atomicity.',
    'Duplicate demand and direct helper boundaries are covered; concurrent reservations and invalid stored balance data require separate integration work.',
    'The existing db:push script resets prisma/dev.db and the seed deletes existing rows. Verification used only a disposable staged database.',
    'No browser workflow, deployed environment or external integration was exercised.'
]
spec.pop('limitations', None)
spec['changedFiles'] = list(dict.fromkeys(spec['changedFiles']+copied))
spec_path.write_text(json.dumps(spec, indent=2)+'\n', encoding='utf-8')
(stage/'astraupskill/VERIFICATION.md').write_text('''# Verification and honest coverage

The changed inventory rules were checked on Windows with Node 22.16 and npm 10.9.2. The final full run passed **12 tests in two files**: nine pure inventory rule tests and three API health, dashboard-read and CSV-export tests. Type checking and the TypeScript/Vite build also passed. The focused nine-test run is a subset of those twelve, so it is not an additional nine unique tests.

## What the evidence proves

The duplicate-line regression submits quantities 14 and 9 for one SKU with 22 available units. Each line fits independently; their combined demand of 23 does not. The planner now reports that combined shortage. Other new assertions reject invalid quantities and direct helper over-reservation. Source review confirmed that the real reservation service calls the planner before its inventory, reservation, order, event and outbox writes. Its rejected-decision branch still writes a failure audit. Rejection therefore does not imply that every table remains unchanged.

The API tests read seeded data; they do not exercise the reservation write endpoint. A passing build establishes compilation and bundle generation, not browser usability. Concurrent reservation correctness, persistent write rollback, invalid stored balances and external delivery remain separate exercises.

## Reproduce in a disposable project copy

Use a fresh copy of the project without existing database files, dependencies or private environment files. Run the following PowerShell commands from that copy's root. **The existing `db:push` script recreates `prisma/dev.db`, and `db:seed` deletes rows before inserting fixtures.** These commands belong in the disposable copy because changing `DATABASE_URL` does not redirect the custom schema creation script. Inspect [that script](../prisma/create-sqlite-schema.ts) and [the seed](../prisma/seed.ts) first.

```powershell
npm ci --no-audit --no-fund
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
$learningDbPath = Join-Path (Get-Location).Path 'prisma/dev.db'
$env:DATABASE_URL = 'file:' + $learningDbPath.Replace('\\', '/')
npm run db:generate
if ($LASTEXITCODE -ne 0) { throw 'Client generation failed' }
npm run db:push
if ($LASTEXITCODE -ne 0) { throw 'Schema creation failed' }
npm run db:seed
if ($LASTEXITCODE -ne 0) { throw 'Fixture seeding failed' }
npm test
if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }
npm run typecheck
if ($LASTEXITCODE -ne 0) { throw 'Type checking failed' }
npm run build
if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
```

An absolute SQLite URL avoids the relative-path ambiguity encountered during verification. Successful fixture creation alone is not enough: the seed and tests must open that same file. The actual recorded run used an absolute URL inside the isolated staging copy. No original project database was copied, reset or seeded. Database files and generated dependency/build folders are not part of this delivery.

## Recorded results and earlier failures

The final [full test log](evidence/full-test-absolute.log) and [machine-readable run record](evidence/full-test-absolute.json) show the twelve passing tests and the precise database override. The [focused test log](evidence/inventory-rules.log), [typecheck log](evidence/typecheck-2.log) and [build log](evidence/build-2.log) provide the other outcomes. Successful setup records are included for [installation](evidence/npm-ci-3.json), [client generation](evidence/prisma-generate.json), [schema creation](evidence/db-push.json) and [absolute-path seeding](evidence/db-seed-absolute.json).

Earlier command-launch attempts failed, initial generation-dependent type/build checks failed, and initial API runs returned errors before the database was correctly initialized and seeded. Those failures remain in the central audit history; they are not counted as passes. The final commands above explain the setup that resolved them. If your local result differs, compare the first failed command, database URL and generated Prisma client before changing application assertions. Keep the duplicate-SKU regression intact: relaxing it would remove the evidence for the behavior repaired here.
''', encoding='utf-8')
print(json.dumps({'id': pid, 'tests': 12, 'copiedEvidenceFiles': len(copied), 'spec': str(spec_path)}, indent=2))
