"""Finalize evidence after a successful, reviewed MissionControl test run."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import xml.etree.ElementTree as ET

B = Path(__file__).resolve().parent
pid = 'ee8b0b1a6855'
stage = B/'stage'/pid
checks = B/'checks/missioncontrol'
label = sys.argv[1]
assert label.startswith('tests-') and label[6:].isdigit()
run = json.loads((checks/(label+'.json')).read_text(encoding='utf-8'))
assert run['status'] == 'complete' and run['exitCode'] == 0 and run['passed'] is True
reports = list((checks/label).glob('*.trx'))
assert len(reports) == 2
totals = dict(total=0, passed=0, failed=0, notExecuted=0)
for report in reports:
    counter = ET.parse(report).find('.//{*}Counters')
    assert counter is not None
    for key in totals:
        totals[key] += int(counter.attrib.get(key, 0))
assert totals['total'] == totals['passed'] and totals['total'] > 113
assert totals['failed'] == totals['notExecuted'] == 0
hash_record = json.loads((checks/(label+'-source-hashes.json')).read_text(encoding='utf-8'))
source_hashes = {item['file']: item['sha256'] for item in hash_record['files']} if 'files' in hash_record else hash_record
source_hashes = {name: digest for name, digest in source_hashes.items() if not name.startswith('astraupskill/')}
assert all(hashlib.sha256((stage/name).read_bytes()).hexdigest() == digest for name, digest in source_hashes.items())
for name in ['restore-01.json', 'restore-locked-01.json']:
    restore = json.loads((checks/name).read_text(encoding='utf-8'))
    assert restore['status'] == 'complete' and restore['exitCode'] == 0
spec_path = B/'specs'/(pid+'.json')
spec = json.loads(spec_path.read_text(encoding='utf-8'))
evidence = stage/'astraupskill/evidence'
evidence.mkdir(exist_ok=True)
copied = []
for file in [checks/(label+'.json'), checks/(label+'.log'), checks/(label+'-source-hashes.json'), checks/'restore-locked-01.json', *reports]:
    target = evidence/file.name
    shutil.copyfile(file, target)
    copied.append(target.relative_to(stage).as_posix())
readme = stage/'README.md'
original = readme.read_text(encoding='utf-8')
if 'astraupskill/README.md' not in original:
    readme.write_text(original.rstrip()+'\n\n## CRUD learning course\n\nStart with [the Astra upskilling course](astraupskill/README.md) for the code map, worked changes, regression tests, practice and solutions.\n', encoding='utf-8')
spec['changedFiles'] = list(dict.fromkeys(spec['changedFiles']+['README.md']+copied))
spec['summary'] = [
    'Task updates reject blank titles and validate project visibility within the current workspace before mutating tracked task state.',
    'Task creation and project reassignment allocate project ticket numbers inside an EF-owned serializable SQLite transaction; task/activity writes commit before event publication.',
    'Prevalidation and metadata serialization prevent rejected updates from contaminating later valid saves in the same scoped service; regression tests cover recovery and mixed concurrent create/move allocation.',
    'Add a forward EF migration for thirteen existing platform entities omitted from the original model snapshot, allowing the test API host to apply the complete schema without suppressing pending-model checks.',
    'Isolate the two lifecycle scenarios in disposable test hosts, disable parallel API tests that share process environment, correct the security-scan route, and provide an explicit scheduler opt-out.',
    'A nine-file learning course explains actual request paths, EF tracking versus database transactions, worked examples, debugging, progressive exercises and their solutions; original source snapshots and verification evidence are included.'
]
spec['checks'] = {'format':'trx','resultsDirectory':'checks/missioncontrol/'+label,'expectedSuites':2,'expectedTests':totals['total'],
                  'command':' '.join(run['command']), 'environment':'.NET SDK 10.0.302; Release; generated lockfiles and successful locked restore; ASP.NET test host with fake LLM and disposable SQLite'}
spec['limits'] = [
    'ProjectId remains nullable without presence tracking: omitted and explicit null both preserve the assignment; clearing a project is not implemented.',
    'Concurrency evidence covers request-scoped operations. A long-lived EF context can retain stale tracked entities after an external writer; this is not universal cross-context cache concurrency protection.',
    'A failed database save requires appropriate context disposal/recovery. Rolling back a SQL transaction does not restore EF tracked objects; the tested validation and serialization failures are prevented before mutation.',
    'Event publication follows commit but is not a durable outbox, and no cross-request optimistic concurrency token was added.',
    'The forward migration is exercised against disposable test databases; migration of an existing production dataset was not performed.',
    'No live LLM, webhook destination, production database, deployed service or visual browser workflow was used.'
]
spec_path.write_text(json.dumps(spec,indent=2),encoding='utf-8')
results = {'passed':True,**totals,'suites':2,'commandRecord':label+'.json','sourceHashesUnchanged':True,'lockedRestorePassed':True}
(checks/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
guide = f'''# Verification and repeatable checks

The reviewed implementation passed **{totals['passed']} tests across two suites**, with zero failures and zero skipped tests. The run built the solution in Release configuration under .NET SDK 10.0.302. It used the existing ASP.NET integration-test host, a fake LLM implementation and disposable SQLite databases. This verifies the exercised application behavior; it does not establish that a real agent fleet, webhook integration or deployed website works.

The exact command and process exit code are in [the run record](evidence/{label}.json), and [the full output](evidence/{label}.log) preserves the compiler and test-run results. [The locked-restore record](evidence/restore-locked-01.json) records dependency reproducibility. Six generated package lockfiles accompany the source. [Source hashes](evidence/{label}-source-hashes.json) were compared after testing to ensure the tested source and configuration did not change before finalization.

The raw hash record also includes draft teaching snapshots. Final review replaced two of those snapshots with byte-for-byte originals verified against the immutable baseline; this documentation correction did not change tested application or test code. The delivered snapshots, rather than the draft snapshot digests, are the originals to use for before/after study.

## Repeat the check

From the project root, use the installed .NET 10 SDK:

```powershell
dotnet restore FleetCommand.slnx --locked-mode
if ($LASTEXITCODE -ne 0) {{ throw 'Locked restore failed' }}
dotnet test FleetCommand.slnx --no-restore --configuration Release --logger trx
if ($LASTEXITCODE -ne 0) {{ throw 'Tests failed' }}
```

Restore validates the dependency graph against the delivered locks. Test compiles the projects and executes both suites. Read the command exit code as well as the summary: seeing the unit suite pass is insufficient if the API project later fails to compile. Earlier attempts during this improvement pass caught missing test namespace imports; those attempts remain recorded centrally and are not counted as successful verification.

The API startup also exposed thirteen platform entities registered in `FleetDbContext` but absent from the original migration snapshot. The forward `MissionControlPlatformEntities` migration creates those missing tables and updates the snapshot; it does not rewrite the initial migration or disable the pending-model check. The test host applies migrations to disposable SQLite databases. This proves the tested fresh-database startup path, not an upgrade rehearsal with a production dataset. Inspect the new migration and the preserved original snapshot before planning a separate existing-data migration exercise.

Most API cases use the existing shared collection fixture. The two lifecycle scenarios now use separate test hosts and databases so unrelated queued tasks cannot consume their scripted LLM verdicts. Those hosts remove hosted background services and invoke orchestration explicitly. API test parallelization is disabled because test hosts temporarily change process environment variables; disposal restores the previous values. The new `FC_DISABLE_SCHEDULER=1` option skips scheduler hosting in the application, while leaving its control service registered. It does not disable webhook services in an ordinary application run. The isolated test host separately removes all hosted services.

## What the regressions prove

The HTTP cases exercise blank-title rejection, workspace-filtered project assignment, same-project reassignment and concurrent ticket allocation. The mixed case creates tasks while other tasks move into the same project, then checks distinct consecutive ticket numbers and the persisted project counter. This tests a real SQLite path rather than a repository stub.

The scoped-service cases attempt an invalid update and then perform an unrelated valid save using the same context. They preserve an independent copy of the original title, so an assertion cannot accidentally compare a mutated entity with itself. One case uses a valid target project and an invalid feedback rating, ensuring the intended validation branch is reached. Another supplies cyclic metadata directly to the service and checks recovery after serialization fails.

## Interpret the boundary correctly

EF change tracking and a SQL transaction are separate mechanisms. The prevalidation and serialization steps protect tracked entities before mutation. SaveChanges writes within the transaction; CommitAsync establishes the durable success boundary; event publication follows. A rollback alone does not reset tracked properties, and an event bus is not a durable outbox.

The concurrency test covers fresh request-scoped reads. Do not infer that an arbitrarily long-lived context automatically refreshes entities after another writer changes them. The project-clear wire contract, optimistic concurrency, durable event delivery and browser usability remain separate work. Use [the practice guide](05-PRACTICE.md) and [solutions](06-SOLUTIONS-AND-REVIEW.md) to explain these limits before extending the implementation.
'''
(stage/'astraupskill/VERIFICATION.md').write_text(guide,encoding='utf-8')
print(json.dumps({'project':'missioncontrol','tests':totals,'evidenceFiles':len(copied),'sourceHashesUnchanged':True}))
