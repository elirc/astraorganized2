from pathlib import Path
from datetime import datetime,timezone
import json
BASE=Path(__file__).resolve().parent.parent
OUT=BASE/'astra-remaining-improvements/batch-crud-upskill-20260921'
OUT.mkdir(exist_ok=True)
ledger=json.loads((BASE/'astra-remaining-improvements/progress.json').read_text())
blocked={'spacegame','tagalog','aicallhelper','aicallhelper2','alanandelisoccer','ankijs','astraspacegameweb','fableaihelperv2','fableaihelperv3','finalcallhelp'}
def excluded(path):
    return 'applybot' in path.casefold() or 'applyboy' in path.casefold() or any(s.casefold() in blocked for s in Path(path).parts)
pending=[r for r in ledger['projects'] if r['status']!='complete']
protected=[r for r in pending if excluded(r['path'])]
eligible=[r for r in pending if not excluded(r['path'])]
priority=['recipegen-app','HNJOBTRACK','grouphelpdesk','ww36','ww43','ww48','zz2','zz3','buildaffiliate','buildanalytics']
eligible.sort(key=lambda r:(priority.index(Path(r['path']).name) if Path(r['path']).name in priority else len(priority),r['path'].casefold()))
batches=[{'batch':i//10+1,'status':'pending','projects':[{'id':r['id'],'path':r['path'],'status':'pending'} for r in eligible[i:i+10]]} for i in range(0,len(eligible),10)]
policy={'createdAt':datetime.now(timezone.utc).isoformat(),'instruction':'Exclude every applybot/applyboy variant and all explicitly protected project families. Luna implementation; Astra review/delivery. Batches of ten; final batch may be shorter. Preserve existing learning material and completed Fable/Astra work.','protectedNameParts':sorted(blocked),'protectedSubstrings':['applybot','applyboy'],'excludedPendingProjects':[r['path'] for r in protected],'eligibleCount':len(eligible),'batches':batches}
p=OUT/'campaign.json'
assert not p.exists(),'Do not overwrite campaign progress'
p.write_text(json.dumps(policy,indent=2),encoding='utf-8')
lines=['# CRUD upskilling campaign — 2026-09-21','',f'**{len(eligible)} eligible families in {len(batches)} batches**: eleven batches of ten and a final batch of eight. Fourteen previously queued families are excluded. Every applybot/applyboy variant is protected even if absent from the old queue.','',
'Luna implements staged changes; Astra reviews, validates and applies finite manifests. No completed campaign/Fable project is added to this queue. Existing courses and tests stay intact; improvements must address a specific gap.','',
'## Protected projects','']+['- '+r['path'] for r in protected]+['','The matching rule also excludes any other path containing `applybot` or `applyboy`.','',
'## Teaching and delivery standard','',
'Each delivery pairs a bounded code/test improvement with source-grounded teaching: code-reading maps, worked before/after examples, trace tables, debugging exercises, prediction questions, graduated practice, separately placed solutions, review rubrics and honest verification limits. Explain how the selected behavior connects UI/API contracts, validation, authorization, persistence, failures and observability. Do not fabricate a full-stack example in a project that lacks those layers.','',
'Retain exact originals of changed files. Run appropriate regression checks and review actual changes before delivery. Do not infer passing tests from file presence. Shared ledger updates and canonical writes are Astra-only. Install only the tools needed for the active batch; no broad dependency restoration.','']
for b in batches:
    lines += [f"## Batch {b['batch']:02} — pending",'']+[f"- [ ] {r['path']} (`{r['id']}`)" for r in b['projects']]+['']
(BASE/'astradocs/CRUD_UPSKILL_BATCH_PLAN_2026-09-21.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'eligible':len(eligible),'excluded':len(protected),'batches':len(batches),'firstBatch':batches[0]},indent=2))
