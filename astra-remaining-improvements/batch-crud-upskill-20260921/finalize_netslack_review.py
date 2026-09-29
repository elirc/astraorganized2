from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
pid='7f289bf2abfa';D=B/'stage'/pid/'astraupskill'
p=B/'specs'/f'{pid}.json';s=json.loads(p.read_text())
s['project']='_Organized Desktop/01 Net Workspaces/.netslack'
s['changedFiles']=list(dict.fromkeys(f for f in s['changedFiles'] if not f.startswith(('checks/','astra-remaining-improvements/'))))
s['summary'][1]='Re-query persisted state after a save failure: occupied slug maps to conflict; absent slug preserves the original save exception.'
s['limits'] += ['If the recovery query fails or is cancelled, its failure propagates instead of the original save error.', 'Classification is based on observed slug occupancy, not proof of which database constraint caused the save failure; no automatic retry is performed.']
p.write_text(json.dumps(s,indent=2),encoding='utf-8')
for p in D.glob('*.md'):
    t=p.read_text(encoding='utf-8')
    t=t.replace('ran four focused cases', 'runs focused cases')
    t=t.replace('This staged course is review material; it does not edit the canonical project or run migrations.', 'The course is delivered with the reviewed source change and its test evidence. It does not run migrations or upgrade the original application target.')
    t=t.replace('while allowing unrelated persistence failures to reach the caller.', 'while preserving the original save failure when a successful recovery query finds the slug absent.')
    p.write_text(t,encoding='utf-8')
p=D/'VERIFICATION.md';t=p.read_text(encoding='utf-8')
t=t.replace('dotnet run --project astra-remaining-improvements/stage/7f289bf2abfa/tests/NetSlack.ScopeHarness/NetSlack.ScopeHarness.csproj --no-restore --nologo -p:UseSharedCompilation=false -m:1', 'dotnet run --project tests/NetSlack.ScopeHarness --configuration Release -p:UseSharedCompilation=false')
t=t.replace('from the workspace root', 'with this reproducible command from the project root')
t=t.replace('The run passed four cases:', 'The final reviewed harness contains five cases:')
t=t.replace('and successful creation returns the normalized DTO while retaining workspace and general channel.', 'successful creation retains the normalized DTO, owner membership and general channel; and a different unique failure preserves the original exception object.')
t=t.replace('The output is recorded in `checks/7f289bf2abfa/results-crud-b02.json`.', 'The exact executed command and output are attached below after the final run. The captured run may use --no-restore because local harness assets already existed; omit that flag for a clean checkout.')
t+='\nClassification observes whether the requested slug is now occupied; it does not prove which database constraint caused the original error. If the recovery query itself fails, that query error propagates. No retry or live provider guarantee is claimed.\n'
p.write_text(t,encoding='utf-8')
print('Normalized manifest and portable evidence instructions; preserved native-run limits.')
