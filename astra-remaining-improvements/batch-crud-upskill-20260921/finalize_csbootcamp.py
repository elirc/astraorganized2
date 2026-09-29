from pathlib import Path
import json, shutil
B=Path(__file__).resolve().parent.parent
pid='c10fc180fa35';P=B/'stage'/pid
snapshot=P/'astraupskill/snapshots/README.md.original.txt'
snapshot.parent.mkdir(exist_ok=True)
if not snapshot.exists():shutil.copyfile(P/'README.md',snapshot)
readme=P/'README.md';original=snapshot.read_bytes()
readme.write_bytes(original+b'\n\n## CRUD web companion\n\nAfter the fundamentals, follow [the versioned CRUD web lab](astraupskill/README.md).\nIt runs a local .NET 10 API and HTTP checks for validation, CRUD operations and conflicting edits,\nwith trace exercises and separate answers. The original exercise scoreboard is unchanged.\n')
spec={'id':pid,'project':'_Organized Desktop/01 Net Workspaces/csbootcamp','summary':[
'Add a standalone .NET10 CRUD web companion with create/list/read/replace/delete, title validation and required version preconditions on writes.',
'Demonstrate atomic in-process version checks with actual loopback HTTP regressions and nine chapters covering traces, exercises, solutions and database follow-up design.'
], 'changedFiles':['README.md','guides/crud-web-lab/CrudWebLab.csproj','guides/crud-web-lab/Program.cs','guides/crud-web-lab/TaskStore.cs','guides/crud-web-lab/HttpChecks.cs','astraupskill/snapshots/README.md.original.txt'],
'checks':{'format':'json','resultsFile':f'checks/{pid}/results-crud-b02.json'},'limits':[
'This new teaching companion uses in-memory single-process storage; no authentication, durable database, browser UI or deployment is included.',
'The If-Match contract supports one strong numeric tag only, not full HTTP conditional request grammar.',
'The original bootcamp exercise suites and scoreboard were not rerun or modified.',
'One overlapping HTTP writer case checks observed behavior; exhaustive stress testing and multi-instance concurrency are outside this lab.'
]}
(B/'specs'/f'{pid}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
print(json.dumps({'id':pid,'specPrepared':True}))
