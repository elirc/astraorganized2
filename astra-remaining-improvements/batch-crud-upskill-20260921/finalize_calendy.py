from pathlib import Path
import json,re,shutil
B=Path(__file__).resolve().parent.parent;pid='ef1449fa0c77';P=B/'stage'/pid;C=B/'checks'/pid
label='crud-b02-scope-harness';record=json.loads((C/f'{label}.json').read_text())
assert record['passed'] and record['status']=='complete' and record['exitCode']==0
log=(C/f'{label}.log').read_text()
for field,value in [('tests',11),('pass',11),('fail',0),('skipped',0)]:
    assert re.search(rf'^# {field} {value}$',log,re.M)
limits=[
    'Eleven handler cases compiled and executed actual linked production source on .NET10 with explicit repository and minimal MediatR contract doubles.',
    'Original .NET9 solution/xUnit suites, ASP.NET/MediatR pipelines, EF Core, PostgreSQL and browser integration were not executed.',
    'This relationship/state guard does not establish booking availability membership, timezone correctness, atomic double-booking prevention or tenant middleware behavior.'
]
result={'passed':True,'executedTests':11,'checks':[record],'limits':limits}
resultfile=C/'results-crud-b02.json';resultfile.write_text(json.dumps(result,indent=2),encoding='utf-8')
E=P/'astraupskill/evidence';E.mkdir(exist_ok=True)
shutil.copyfile(resultfile,E/'results.json');shutil.copyfile(C/f'{label}.log',E/f'{label}.log')
v=P/'astraupskill/VERIFICATION.md';t=v.read_text()
t=t.replace('Accepted execution evidence is attached below after the command completes;\nthis explanation alone is not a claim that an unfinished command passed.', 'The captured run completed successfully: eleven tests passed, zero failed\nand zero skipped. The linked record contains the exact command and timestamps.')
if '## Accepted execution' not in t:
    t+='\n## Accepted execution\n\nRead the [eleven-case output](evidence/crud-b02-scope-harness.log) and [command record with limits](evidence/results.json). The command compiled the selected source and exited zero. No dependency-install step is counted as a test.\n'
v.write_text(t,encoding='utf-8')
changed=[
    'src/NetCalendy.Application/Bookings/Commands/CreateBooking/CreateBookingHandler.cs',
    'src/NetCalendy.Application/Schedules/Queries/GetAvailableSlots/GetAvailableSlotsHandler.cs',
    'tests/NetCalendy.ScopeHarness/NetCalendy.ScopeHarness.csproj',
    'tests/NetCalendy.ScopeHarness/MediatorContracts.cs','tests/NetCalendy.ScopeHarness/Program.cs'
]
changed += [p.relative_to(P).as_posix() for folder in ['astraupskill/snapshots','astraupskill/evidence'] for p in sorted((P/folder).iterdir())]
spec={'summary':[
    'Require selected event types to match the resolved tenant and requested host before booking or availability work.',
    'Reject inactive event types consistently in availability while preserving valid booking, existing conflict and empty-schedule behavior.',
    'Add eleven executable production-source C# cases and nine linked teaching chapters on resource relationships, early rejection and evidence boundaries.'
], 'changedFiles':changed,'checks':{'format':'json','resultsFile':f'checks/{pid}/results-crud-b02.json'},'limits':limits}
(B/'specs'/f'{pid}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
print(json.dumps({'id':pid,'tests':11,'changedFiles':len(changed)}))
