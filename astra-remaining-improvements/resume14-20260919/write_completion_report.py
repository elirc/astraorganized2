from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote
import hashlib, json
B=Path(__file__).resolve().parent.parent
D=B.parent/'astradocs'
state=json.loads((B/'resume14-20260919/state.json').read_text(encoding='utf-8'))
assert len(state['projects'])==14
manifests=[];hashes=0
for item in state['projects']:
 m=json.loads((B/'deliveries'/f"{item['id']}.json").read_text(encoding='utf-8'))
 assert m['status']=='delivered',item['id']
 assert m['testResults']['passed'] and m['testResults']['failed']==0,item['id']
 if 'checks' not in m['testResults']:
  labels=m['testResults']['evidence']
  assert labels
  m['testResults']['checks']=[json.loads((B/'checks'/item['id']/(label+'.json')).read_text(encoding='utf-8')) for label in labels]

 for check in m['testResults']['checks']:
  assert check['status']=='complete' and check['exitCode']==0,(item['id'],check)
 for entry in m['files']:
  path=B.parent.parent/m['project']/entry['file']
  assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==entry['after_sha256'],str(path)
  hashes+=1
 item.update(status='delivered',files=len(m['files']),tests=m['testResults']['total'],deliveredAt=m['deliveredAt'])
 manifests.append(m)
progress=json.loads((B/'progress.json').read_text(encoding='utf-8'))
remaining=[row for row in progress['projects'] if row['status']!='complete']
assert len(remaining)==147,len(remaining)
selection=json.loads((B/'checks/batch-luna-astra-50-20260912/selection.json').read_text(encoding='utf-8'))
selected=selection['projects']
status_by_id={row['id']:row['status'] for row in progress['projects']}
assert len(selected)==50
assert all(status_by_id[row['id']]=='complete' for row in selected)
assert sum(row['status']=='complete' for row in progress['projects'])==92

assert not ({row['id'] for row in remaining}&{row['id'] for row in state['projects']})
checks=sum(len(m['testResults']['checks']) for m in manifests)
tests=sum(m['testResults']['total'] for m in manifests)
now=datetime.now(timezone.utc).isoformat()
verification={'verifiedAt':now,'projects':14,'deliveredFileHashesVerified':hashes,'passingTestCases':tests,'acceptedChecks':checks,'remainingFamilies':147,'projectsEvidence':[{'id':m['id'],'path':m['project'],'files':len(m['files']),'tests':m['testResults']['total'],'deliveredAt':m['deliveredAt']} for m in manifests]}
(B/'resume14-20260919/completion-verification.json').write_text(json.dumps(verification,indent=2)+'\n')
(B/'resume14-20260919/state.json').write_text(json.dumps(state,indent=2)+'\n')
lines=['# Completion report: the 14 resumed Desktop projects','',f'Completed September 19, 2026. All 14 selected projects are delivered to their canonical Desktop folders. Final verification matched **{hashes} delivered file hashes**, with **{tests} passing test cases** across the accepted project suites and **{checks} successful recorded checks**.','',
'Each project includes nine source-based `astraupskill` guides, worked examples, exercises and solutions, exact original snapshots for changed baseline files, and saved verification logs. That is **126 course chapters** across these 14 projects. File counts below include implementation, tests, courses, snapshots and evidence; they are not all new application source files.','',
'The 153 earlier Astra projects covered by Fable remain excluded. This work completes the 14 staged families from the existing campaign. **147 other project families remain queued**; see the [updated remaining list](REMAINING_PROJECTS_TO_DO_2026-09-19.md). The second-wave ledger is now **92 of 239 complete**, and the selected 50-project batch is complete.','',
'| Project | Delivered files | Passing tests | Course and evidence |','| --- | ---: | ---: | --- |']
for m in manifests:
 url='../../'+quote(m['project'],safe='/')
 lines.append(f"| [{m['project']}]({url}) | {len(m['files'])} | {m['testResults']['total']} | [Course]({url}/astraupskill/README.md), [verification]({url}/astraupskill/VERIFICATION.md), [manifest](../astra-remaining-improvements/deliveries/{m['id']}.json) |")
lines+=['','## Changes and additions by project','']
for m in manifests:
 summary=m['summary'] if isinstance(m['summary'],str) else '\n'.join('- '+entry for entry in m['summary'])
 lines += ['### '+m['project'],'',summary,'']
 changed=[entry['file'] for entry in m['files'] if not entry['file'].startswith('astraupskill/') and entry['file']!='README.md' and entry['before_sha256']]
 added=[entry['file'] for entry in m['files'] if not entry['file'].startswith('astraupskill/') and entry['file']!='README.md' and not entry['before_sha256']]
 if changed:lines+=['**Updated application/configuration files:** '+', '.join('`'+name+'`' for name in changed)+'.','']
 if added:lines+=['**Added source, test and setup files:** '+', '.join('`'+name+'`' for name in added)+'.','']
 labels=[Path(check['log']).stem for check in m['testResults']['checks']]
 lines+=['**Accepted checks:** '+', '.join('`'+label+'`' for label in labels)+'.','']
 limits=m.get('limits') or []
 if isinstance(limits,str):limits=[limits]
 if limits:lines+=['**Practical limits:** '+' '.join(limits),'']
lines+=['## Verification scope','',
'Linear and Shop include real disposable PostgreSQL integration tests. buildagentteachGEM includes real disposable SQLite server-action tests and audit-failure triggers. Other projects use their documented unit, service, repository-mock or process-local store tests; ww34 also compares actual child processes in three timezones. Per-project verification files distinguish those forms of evidence and identify builds that use inert database configuration.','',
'No original application database was reset or seeded, and no real payment, email or external model operation was performed. Schema changes that need deployment are documented in the relevant course. Demo storage and identity limitations are retained explicitly rather than presented as production guarantees.','',
'Failed setup and earlier check attempts remain in the campaign logs. Only final accepted, terminal-zero checks are linked as passing evidence. The final [hash and count verification](../astra-remaining-improvements/resume14-20260919/completion-verification.json) was generated after all fourteen deliveries.','']
report=D/'COMPLETED_14_PROJECTS_2026-09-19.md';report.write_text('\n'.join(lines),encoding='utf8')
f=D/'REMAINING_PROJECTS_TO_DO_2026-09-19.md';old=f.read_text(encoding='utf8');marker='## Other queued families (147)' if '## Other queued families (147)' in old else '## Remaining queued families (147)';queued=old[old.index(marker):].replace(marker,'## Remaining queued families (147)',1)
header="""# Remaining Desktop projects to do

Updated September 19, 2026: **147 project families remain queued. The 14 previously staged projects are now finished and delivered.**

The 153 earlier Astra projects covered by Fable remain excluded and were not reopened. This is the existing campaign queue, not a fresh inventory of every Desktop folder.

[Completion report for all 14 projects](COMPLETED_14_PROJECTS_2026-09-19.md) / [Progress ledger](../astra-remaining-improvements/progress.json) / [Original status snapshot](ASTRA_PROJECT_STATUS_2026-09-19.md)

An unchecked box below means no delivery is recorded for that queued family. None of the 14 completed projects remains on this list.

"""
f.write_text(header+queued,encoding='utf8')
f=D/'ASTRA_PROJECT_STATUS_2026-09-19.md';old=f.read_text(encoding='utf8');note='\n## Follow-up: staged work completed\n\nThe 14 staged projects in this historical snapshot were subsequently completed and delivered on September 19, 2026. See the [completion report](COMPLETED_14_PROJECTS_2026-09-19.md) and [current 147-project queue](REMAINING_PROJECTS_TO_DO_2026-09-19.md). The original snapshot above is preserved as history; its staged/pending counts are superseded by that completion report.\n'
if '## Follow-up: staged work completed' not in old:f.write_text(old+note,encoding='utf8')
print(json.dumps({'report':str(report),'tests':tests,'checks':checks,'hashes':hashes,'remaining':147},indent=2))
