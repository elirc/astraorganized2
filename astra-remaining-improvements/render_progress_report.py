from report_evidence import check_summary
from pathlib import Path
from urllib.parse import quote
import json,collections
B=Path(__file__).resolve().parent;R=B.parent
progress=json.loads((B/'progress.json').read_text(encoding='utf-8'));scope=json.loads((B/'scope.json').read_text(encoding='utf-8'))
completed=[p for p in progress['projects'] if p['status']=='complete'];total=progress['total'];manifests={p['id']:json.loads((B/'deliveries'/f'{p["id"]}.json').read_text(encoding='utf-8')) for p in completed}
lines=['# Remaining projects: implementation progress','','**In progress.** This is a completion ledger, not a claim that the entire collection is finished.','',f'- Scope: **{total} eligible project families** outside the audit’s top 50 and the previous 75 implementation targets.',f'- Completed and applied in original folders: **{len(completed)}**.',f'- Remaining: **{total-len(completed)}**.',f'- Delivered course files: **{sum(m["courseFiles"] for m in manifests.values())}**; learning words: **{sum(m["courseWords"] for m in manifests.values()):,}**.','','The broader scope includes the 124 unfinished audit projects and 115 other documented projects. Work begins with the unfinished projects. Duplicate locations are represented by their canonical project; prior delivered files were assigned to their deepest independent project so unrelated nested apps are not accidentally excluded.','','## Completed changes','','Each completion requires a code review, useful implemented behavior changes, detailed source-based lessons, recorded validation, and hash-verified delivery with backups. Tests run in isolated copies; a course exercise is not counted as implemented functionality.','']
for p in completed:
 m=manifests[p['id']];url=quote('../../'+p['path']+'/astraupskill/README.md',safe='/+')
 evidence_url=f'../astra-remaining-improvements/deliveries/{p["id"]}.json'
 count=check_summary(m)
 lines+=[f'### [{p["path"]}]({url})','']+['- '+s for s in m['summary']]+['',f'Validation: **{count}**. [Commands and evidence]({evidence_url}). Course: **{m["courseFiles"]} guides**, {m["courseWords"]:,} words.','', 'Remaining limits: '+' '.join(m['limits']),'']
lines+=['## Full work queue','','| Project | Status |','|---|---|']
for p in progress['projects']:lines.append(f'| [{p["path"]}]({quote("../../"+p["path"],safe="/+")}) | {p["status"]} |')
lines+=['','## Evidence','','[Scope and exclusions](../astra-remaining-improvements/scope.json) · [Machine-readable progress](../astra-remaining-improvements/progress.json) · [Delivery manifests](../astra-remaining-improvements/deliveries/)','','Backups and verification copies are retained under `astra-remaining-improvements/`. Existing project databases and Git histories are not replaced. The original audit remains a historical snapshot; this report tracks subsequent work.','']
(R/'astrdocs/REMAINING_PROJECTS_IMPLEMENTATION_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'complete':len(completed),'remaining':total-len(completed),'report':str(R/'astrdocs/REMAINING_PROJECTS_IMPLEMENTATION_REPORT.md')},indent=2))
