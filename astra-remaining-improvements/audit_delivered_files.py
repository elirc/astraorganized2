"""Read-only reconciliation of delivered files against recorded after-hashes."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import json,hashlib
B=Path(__file__).resolve().parent;D=B.parent.parent
progress=json.loads((B/'progress.json').read_text(encoding='utf-8'))
entries=[]
for item in progress['projects']:
    if item['status']!='complete':continue
    manifest=json.loads((B/'deliveries'/f'{item["id"]}.json').read_text(encoding='utf-8'));assert manifest['status']=='delivered'
    entries.append(manifest)
def audit(m):
    missing=[];different=[]
    for item in m['files']:
        file=(D/m['project']/item['file']).resolve();assert file.is_relative_to((D/m['project']).resolve())
        if not file.is_file():missing.append(item['file'])
        elif hashlib.sha256(file.read_bytes()).hexdigest()!=item['after_sha256']:different.append(item['file'])
    return {'id':m['id'],'project':m['project'],'files':len(m['files']),'missing':missing,'differentFromDelivery':different,'matchesDelivery':not missing and not different}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(audit,entries))
out={'date':datetime.now(timezone.utc).isoformat(),'projects':len(results),'files':sum(item['files'] for item in results),'matchingProjects':sum(item['matchesDelivery'] for item in results),'results':results,'note':'Read-only file-hash reconciliation. Differences may be later user edits; this audit never overwrites them and does not rerun historical tests.'}
(B/'delivered-files-audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({key:out[key] for key in ['projects','files','matchingProjects']}))
