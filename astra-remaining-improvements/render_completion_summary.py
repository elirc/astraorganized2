from report_evidence import check_summary
"""Concise per-delivery report requested by the user; never infer completion."""
from pathlib import Path
from urllib.parse import quote,unquote
from datetime import datetime,timezone
import json,re
B=Path(__file__).resolve().parent;R=B.parent
progress=json.loads((B/'progress.json').read_text(encoding='utf-8'))
complete=[item for item in progress['projects'] if item['status']=='complete']
manifests=[]
for item in complete:
    m=json.loads((B/'deliveries'/f'{item["id"]}.json').read_text(encoding='utf-8'));assert m['status']=='delivered';manifests.append(m)
manifests.sort(key=lambda item:item.get('deliveredAt',''))
audit_path=B/'delivered-files-audit.json'
audit=json.loads(audit_path.read_text(encoding='utf-8')) if audit_path.exists() else None
audit_by_id={item['id']:item for item in audit['results']} if audit else {}
target=R/'astradocs/PROJECT_CHANGES_AND_COMPLETION_REPORT.md'
lines=['# Project changes and completion report','',f'Updated {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}.','',f'**{len(manifests)} of {progress["total"]} eligible project families have been delivered. {progress["total"]-len(manifests)} remain.** The full collection is not finished. Original top-50 and previously modified family exclusions remain in force.','', 'Each entry below describes changes recorded as applied to the original project folder. Its learning link opens the detailed junior-to-mid-level course; the evidence link contains checks, file hashes and limitations. Exercise proposals are not counted as implemented features.','']
if audit:
    missing=sum(len(item['missing']) for item in audit['results']);changed=sum(len(item['differentFromDelivery']) for item in audit['results'])
    lines += [f'**File reconciliation:** checked {audit["files"]:,} delivered files across {audit["projects"]} projects; {missing} missing and {changed} different from their recorded delivery hashes. Later differences were preserved. This checks file content, not a fresh rerun of historical tests. [Read-only audit](../astra-remaining-improvements/delivered-files-audit.json).','']
for index,m in enumerate(manifests,1):
    course=quote('../../'+m['project']+'/astraupskill/README.md',safe='/+')
    lines += [f'## {index}. {m["project"]}','']
    lines += ['- '+item for item in m['summary']]
    lines += ['',f'**Delivered:** {len(m["files"])} files; {m["courseFiles"]} guides; {check_summary(m)}. [Learning course]({course}) · [Evidence and limits](../astra-remaining-improvements/deliveries/{m["id"]}.json).','']
    reconciled=audit_by_id.get(m['id'])
    if reconciled and not reconciled['matchesDelivery']:
        lines += ['**Current-file note:** '+str(len(reconciled['differentFromDelivery']))+' files differ from the recorded delivery; '+str(len(reconciled['missing']))+' are missing. Differences: '+', '.join('`'+name+'`' for name in reconciled['differentFromDelivery'])+'. These later edits were left untouched; recorded test results apply to the delivered version.','']
staged=[item for item in progress['projects'] if item['status']!='complete' and (B/'stage'/item['id']).is_dir()]
lines += ['## Still in progress','']
if staged:
    for item in staged:lines += [f'- `{item["path"]}` has a staged working copy and is not counted as delivered.']
else:lines += ['No additional staged working copy is currently recorded.']
lines += ['', 'The [full remaining queue](../astrdocs/REMAINING_PROJECTS_IMPLEMENTATION_REPORT.md) tracks every eligible family. The [long-form change report](NEW_PROJECTS_CHANGE_REPORT.md) and [machine-readable progress](../astra-remaining-improvements/progress.json) use the same delivery records. Historical check counts are evidence from the recorded runs, not a claim that every old test was rerun today.','']
text='\n'.join(lines)
for url in re.findall(r'\]\(([^)]+)\)',text):assert (target.parent/unquote(url)).exists(),url
target.write_text(text,encoding='utf-8');print(json.dumps({'report':str(target),'delivered':len(manifests),'remaining':progress['total']-len(manifests),'linksVerified':True}))
