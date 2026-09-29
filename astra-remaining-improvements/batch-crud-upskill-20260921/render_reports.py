from pathlib import Path
from urllib.parse import quote
from datetime import datetime,timezone
import json,hashlib
HERE=Path(__file__).resolve().parent;B=HERE.parent;DOCS=B.parent/'astradocs';DESKTOP=B.parent.parent
policy=json.loads((HERE/'campaign.json').read_text())
completed=0
for batch in policy['batches']:
    if not any(r['status']=='complete' for r in batch['projects']) and batch['status']!='in_progress' and batch['batch']!=1:continue
    lines=[f"# CRUD upskilling batch {batch['batch']:02} — 2026-09-21",'',
           f"**{sum(r['status']=='complete' for r in batch['projects'])} of {len(batch['projects'])} projects delivered.** Remaining entries are pending, not accepted changes.",'',
           'Luna implements most projects in isolated stages; Astra reviews correctness, meaningful test evidence and teaching quality before applying finite manifests. Protected project families and every applybot/applyboy variant are excluded.','',
           '| Project | Status | Accepted test cases | Learning guide |','|---|---|---:|---|']
    details=[]
    changed_names=[]
    batch_tests=0
    for r in batch['projects']:
        if r['status']!='complete':
            lines.append(f"| {r['path']} | Pending | — | — |");continue
        m=json.loads((B/'deliveries'/f"{r['id']}.json").read_text())
        assert m['status']=='delivered'
        for f in m['files']:
            assert hashlib.sha256((DESKTOP/r['path']/f['file']).read_bytes()).hexdigest()==f['after_sha256'],f"Delivered file changed: {r['path']}/{f['file']}"
        completed+=1
        tests=m['testResults'].get('executedTests',m['testResults'].get('total','See evidence'))
        if isinstance(tests,int):batch_tests+=tests
        changed_names += [r['path']+'/'+f['file'] for f in m['files']]
        course='../../'+quote(r['path']+'/astraupskill/README.md',safe='/.')
        lines.append(f"| {r['path']} | Delivered | {tests} | [Course]({course}) |")
        details += ['',f"## {Path(r['path']).name}",'']+['- '+s for s in m['summary']]
        details += ['',f"**Teaching:** {m['courseFiles']} source-based chapters; {m['courseWords']:,} words. Includes code-reading paths, worked changes, tests/debugging, graduated exercises, separate solutions, trace labs and verification limits.",'','**Changed or added files:**','']+['- `'+f['file']+'`' for f in m['files']]
        details += ['','**Verification limits:**','']+['- '+x for x in m['limits']]
        details += ['',f"[Delivery manifest](../astra-remaining-improvements/deliveries/{r['id']}.json) / [Astra review](../astra-remaining-improvements/batch-crud-upskill-20260921/{r['id']}-astra-review.json)",'']
    names_file=f"CRUD_UPSKILL_BATCH_{batch['batch']:02}_CHANGED_FILES_2026-09-21.txt"
    (DOCS/names_file).write_text('\n'.join(sorted(changed_names,key=str.casefold))+'\n',encoding='utf-8')
    lines += ['',f"**Accepted runtime tests:** {batch_tests}. **Changed/added files:** {len(changed_names)}. [Complete file-name list]({names_file}).",'']
    lines+=details+['','Canonical file hashes were checked when this report was generated. Passing counts refer only to the accepted suites; they are not a claim that every upstream or external-service check ran.','']
    (DOCS/f"CRUD_UPSKILL_BATCH_{batch['batch']:02}_REPORT_2026-09-21.md").write_text('\n'.join(lines),encoding='utf-8')
pending=[r for batch in policy['batches'] for r in batch['projects'] if r['status']!='complete']
lines=['# Eligible CRUD upskilling queue — current campaign','',
       f"Updated {datetime.now(timezone.utc).isoformat()}. **{completed} delivered; {len(pending)} remain eligible.** Fourteen original pending families are excluded by the user; all applybot/applyboy variants are protected.",'',
       '[Batch plan](CRUD_UPSKILL_BATCH_PLAN_2026-09-21.md) / [Machine-readable campaign](../astra-remaining-improvements/batch-crud-upskill-20260921/campaign.json)','']
for batch in policy['batches']:
    lines += [f"## Batch {batch['batch']:02}",'']
    for r in batch['projects']:
        mark='x' if r['status']=='complete' else ' '
        lines.append(f"- [{mark}] {r['path']}")
    lines.append('')
(DOCS/'CRUD_UPSKILL_REMAINING_2026-09-21.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'delivered':completed,'remainingEligible':len(pending)}))
