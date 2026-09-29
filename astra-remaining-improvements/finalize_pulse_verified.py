"""Finalize Pulse from actual captured workspace checks, never summary claims."""
from pathlib import Path
import json
import re
import hashlib
import shutil

B=Path(__file__).resolve().parent
pid='9e1958f807df'
stage=B/'stage'/pid
checks=B/'checks'/pid
records={}
for label in ['tests-root-01','typecheck-root-01','build-root-01']:
    record=json.loads((checks/(label+'.json')).read_text(encoding='utf-8'))
    assert record['status']=='complete' and record['exitCode']==0 and record['passed'] is True,label
    records[label]=record
log=(checks/'tests-root-01.log').read_text(encoding='utf-8')
counts=list(map(int,re.findall(r'Tests\s+(\d+) passed',log)))
file_counts=list(map(int,re.findall(r'Test Files\s+(\d+) passed',log)))
assert counts==[313,69,123] and file_counts==[10,6,10],(counts,file_counts)
hashes=json.loads((checks/'root-final-source-hashes.json').read_text(encoding='utf-8'))
differences=[name for name,digest in hashes.items() if hashlib.sha256((stage/name).read_bytes()).hexdigest()!=digest]
assert not differences,differences
install=json.loads((B/'checks/aiheartbeat/install-03.json').read_text(encoding='utf-8'))
assert install['passed'] is True and install['exitCode']==0
debug=B/'npm-cache/_logs/2026-09-12T18_22_48_316Z-debug-0.log'
debug_text=debug.read_text(encoding='utf-8')
assert 'verbose exit 0' in debug_text and 'info ok' in debug_text and pid in debug_text
evidence=stage/'astraupskill/evidence'
evidence.mkdir(exist_ok=True)
files=[checks/'root-final-source-hashes.json',B/'checks/aiheartbeat/install-03.json',debug,
       *[checks/(label+suffix) for label in records for suffix in ['.json','.log']]]
copied=[]
for source in files:
    target=evidence/source.name
    shutil.copyfile(source,target)
    copied.append(target.relative_to(stage).as_posix())
results={'passed':True,'tests':sum(counts),'testFiles':sum(file_counts),
         'workspaces':{'core':313,'dashboard':69,'shared':123},'typecheck':'passed','build':'passed',
         'sourceHashesUnchanged':True,'records':records,'installRecord':'checks/aiheartbeat/install-03.json'}
(checks/'results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
readme=stage/'README.md'
text=readme.read_text(encoding='utf-8')
if 'astraupskill/README.md' not in text:
    readme.write_text(text.rstrip()+'\n\n## CRUD learning course\n\nStart with the [personal workspace upskilling course](astraupskill/README.md) for the actual HTTP-to-SQLite path, boundary checks, tests, exercises and worked solutions.\n',encoding='utf-8')
spec_path=B/'specs'/(pid+'.json')
spec=json.loads(spec_path.read_text(encoding='utf-8'))
spec['summary']=[
    'Guard direct workspace store callers with own-property collection allowlisting and positive safe-integer IDs before SQLite saves or deletes, preserving existing HTTP/Zod validation.',
    'Add seeded rejection regressions and verify all three workspaces:505 tests, type checking and the Next webpack dashboard build pass.',
    'Add nine source-grounded learning guides with complete practice examples, an import/export design exercise, exact original snapshots and captured verification evidence.'
]
spec['changedFiles']=list(dict.fromkeys(spec['changedFiles']+['README.md']+copied))
spec['checks']={'format':'json','resultsFile':'checks/'+pid+'/results.json','expectedTests':505,
                'command':'npm run test --workspaces --if-present -- --maxWorkers=1 --testTimeout=30000; npm run typecheck; npm run dashboard:build',
                'environment':'Node22.16; npm10.9.2; three Vitest4 workspaces; Next16.3.1 webpack; disposable absolute PULSE_WORKSPACE_DB'}
spec['limits']=[
    'This is a local personal workspace without account authentication or multi-user authorization; existing same-origin checks are a separate HTTP boundary.',
    'The new guards protect direct store callers. No exploitable SQL injection through the existing validated endpoint was demonstrated.',
    'The course proposes an import contract; no new import implementation, optimistic concurrency or distributed conflict resolution was added.',
    'Tests use synthetic data, temporary SQLite and mocks. No real daemon, Claude CLI, GitHub automation, external webhook, canonical database or browser workflow was exercised.',
    'Normal npm ci completed with lifecycle scripts enabled, but npm emitted invalid/damaged lockfile warnings. Actual npm exit0 and subsequent tests/typecheck/build are retained; no broad dependency upgrade was performed.'
]
spec_path.write_text(json.dumps(spec,indent=2)+'\n',encoding='utf-8')
(stage/'astraupskill/VERIFICATION.md').write_text('''# Verification and repeatable local checks

The final captured run passed **505 tests in 26 files** across all three workspaces: core had 313 tests in ten files, dashboard had 69 tests in six files, and shared had 123 tests in ten files. Type checking passed in all workspaces, and the Next.js 16.3.1 dashboard webpack build completed successfully. These are observed results from Node 22.16 and npm 10.9.2, with the executable source hashes checked again afterward.

## Reproduce with disposable data

From a fresh project copy without private environment/configuration files or existing database files, use the root workspace commands below. The tests use in-memory or temporary databases and mocked automation dependencies. The explicit absolute workspace path also keeps build-time personal-workspace initialization away from any existing workspace database.

```powershell
npm ci --no-audit --no-fund
if ($LASTEXITCODE -ne 0) { throw 'Installation failed' }
$learningFolder = Join-Path ([IO.Path]::GetTempPath()) ('pulse-learning-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $learningFolder | Out-Null
$env:PULSE_WORKSPACE_DB = Join-Path $learningFolder 'workspace.db'
npm run test --workspaces --if-present -- --maxWorkers=1 --testTimeout=30000
if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }
npm run typecheck
if ($LASTEXITCODE -ne 0) { throw 'Type checking failed' }
npm run dashboard:build
if ($LASTEXITCODE -ne 0) { throw 'Dashboard build failed' }
```

The test flags are forwarded directly to each workspace's Vitest command. Calling the root `npm test` with additional flags introduces another npm script layer, so inspect forwarding before assuming a concurrency or timeout option reached the test runner. The dashboard deliberately uses webpack through its existing script and shared TypeScript module-resolution configuration. There is no need to start the daemon or execute `pulse:once` to reproduce this CRUD check.

## Read the evidence

The [full test log](evidence/tests-root-01.log) contains separate summaries for all three workspaces. Its [process record](evidence/tests-root-01.json) contains the actual command, directory, absolute disposable database override, timestamps and exit status. [Typecheck output](evidence/typecheck-root-01.log) and [build output](evidence/build-root-01.log) accompany their [typecheck](evidence/typecheck-root-01.json) and [build](evidence/build-root-01.json) process records. [Source hashes](evidence/root-final-source-hashes.json) establish which source/configuration files were frozen during the final checks.

The [normal install record](evidence/install-03.json) is backed by the [npm debug log](evidence/2026-09-12T18_22_48_316Z-debug-0.log), which ends with npm exit zero and `info ok`. npm emitted repeated invalid/damaged lockfile warnings while reifying dependencies. An earlier PowerShell wrapper interpreted stderr warnings as its own error, which is why the actual npm exit evidence matters. This delivery preserves the existing lockfile; passing checks do not mean those installation warnings were never emitted.

## What the new regression establishes

The store tests seed projects, tasks and applications, submit hostile collection values or invalid numeric ids, and compare the entire decoded workspace with its pre-call snapshot. They also verify that a valid following save returns without throwing. Existing CRUD tests cover project deletion preserving tasks, completion timestamps, schema failures and missing records. The new boundary checks run before SQL construction or writes; the old route already validated its public request envelope with Zod. The results therefore establish defense in depth for direct store callers, not a demonstrated exploit against a previously unvalidated HTTP route.

The full workspace suite gives broader regression coverage than those new cases alone, but it still uses local test fixtures and mocks. It does not prove deployed authentication, real Claude/GitHub integration, multi-user authorization or browser accessibility. The original personal database and sidecars were never read, copied or modified. The versioned import/export example in the solutions is a proposed contract; the existing UI export remains available, and a new importer was not implemented by this change. Treat each of these boundaries explicitly when proposing the next mid-level extension.
''',encoding='utf-8')
print(json.dumps({'id':pid,'tests':505,'evidenceFiles':len(copied),'sourceHashesUnchanged':True}))
