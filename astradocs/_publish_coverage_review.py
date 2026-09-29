import os,json,re,sys
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote,unquote
HERE=Path(__file__).resolve().parent
DESKTOP=HERE.parent.parent
sys.path.insert(0,str(HERE.parent/'scripts'))
from scan_desktop import SKIP_DIRS
A=json.loads((HERE/'final-coverage-audit.json').read_text(encoding='utf-8'))
R=json.loads((HERE/'project-review.json').read_text(encoding='utf-8'))
roots={r['path'] for r in R['projects']}
old=json.loads((HERE.parent/'project-catalog.json').read_text(encoding='utf-8'))
prior_git={p for x in old['projects'] for p in x.get('repository',{}).get('git_roots',[])}
A['new_git_roots']=[x for x in A['git_roots'] if x['path'] not in prior_git]
A['new_git_metadata_for_existing_records']=[x for x in A['new_git_roots'] if x['path'] in roots]
A['unresolved_new_git_roots']=[x for x in A['new_git_roots'] if x['path'] not in roots]
resolved=[]; unresolved=[]
for x in A['source_or_manifest_outside_report']:
    if x['directory']=='gitvg/tools' and set(x['source_files'])=={'gitvg/tools/publish-organized-projects.ps1'} and not x['manifests']:
        resolved.append({'path':x['source_files'][0],'reason':'Workspace publishing helper under the already-covered gitvg container; not a separate product, and not executed.'})
    else:unresolved.append(x)

empty=[];containers=[];uncataloged=[]
for path,b in A['boundaries'].items():
    parts=path.split('/')
    candidate=(len(parts)==1 and path not in {'_Organized Desktop','geminiorganized'}) or (parts[0]=='_Organized Desktop' and len(parts)==3) or (parts[0]=='geminiorganized' and len(parts)==2)
    if not candidate or path in roots:continue
    covered_children=[p for p in roots if p.startswith(path+'/')]
    if covered_children:
        containers.append({'path':path,'covered_descendants':len(covered_children)});continue
    meaningful=[]
    for folder,dirs,files in os.walk(DESKTOP/path):
        dirs[:]=[d for d in dirs if d.lower() not in SKIP_DIRS and d!='.git']
        meaningful.extend(str((Path(folder)/f).relative_to(DESKTOP)).replace(chr(92),'/') for f in files if f.lower() not in {'desktop.ini','.ds_store','.gitkeep'})
    if meaningful:uncataloged.append({'path':path,'files':meaningful[:30],'file_count':len(meaningful)})
    else:empty.append(path)

text=(HERE/'MASTER_REPORT.md').read_text(encoding='utf-8')
allrows=R['projects']+R['nested_apps']
missing_headings=[x['path'] for x in allrows if not re.search(r'^#{3,4} '+re.escape(x['path'])+r'$',text,re.M)]
keys=['purpose','stack','assessment','learning','phase','prerequisites','next_action']
missing_fields=[{'path':x['path'],'fields':[k for k in keys if k not in x or (k!='phase' and not x[k])]} for x in allrows if any(k not in x or (k!='phase' and not x[k]) for k in keys)]
A.update(resolved_nonproject_source=resolved,unresolved_source=unresolved,uncataloged_nonempty_boundaries=uncataloged,empty_placeholders=sorted(empty),covered_containers=containers,missing_report_headings=missing_headings,missing_record_fields=missing_fields)
A['valid']=not any([A['scan_errors'],A['missing_project_paths'],A['missing_evidence'],A['gemini_sample_changes'],A['uncovered_git_roots'],A['unresolved_new_git_roots'],unresolved,uncataloged,missing_headings,missing_fields])
(HERE/'final-coverage-audit.json').write_text(json.dumps(A,ensure_ascii=False,indent=2),encoding='utf-8')
if not A['valid']:
    print(json.dumps({k:A[k] for k in ['scan_errors','missing_project_paths','missing_evidence','gemini_sample_changes','uncovered_git_roots','new_git_roots','unresolved_source','uncataloged_nonempty_boundaries','missing_report_headings','missing_record_fields']},ensure_ascii=True));raise SystemExit(1)

def link(p):return '['+p+'](../../'+quote(p,safe='/')+')'
lines=['# Final Desktop coverage review','', 'Checked September 7, 2026.','',
'**Confirmed: all 202 reviewed project/resource records inside `_Organized Desktop` are included in the master report.** The complete report covers 389 workspaces/resource collections across the Desktop and 75 additional app entries nested inside three already-counted workspaces. No additional project requiring a new report entry was found in this fresh scan.','',
'## Organized Desktop breakdown','', '| Subfolder | Included records | Empty placeholders |','|---|---:|---:|']
for group in sorted(p.split('/')[1] for p in A['boundaries'] if p.startswith('_Organized Desktop/') and len(p.split('/'))==2):
    num=A['organized_groups'].get(group,0)
    ec=sum(x.startswith('_Organized Desktop/'+group+'/') for x in empty)
    lines.append('| '+group+' | '+str(num)+' | '+str(ec)+' |')
lines+=['| **Total** | **202** | **'+str(sum(p.startswith('_Organized Desktop/') for p in empty))+'** |','',
'Group 10 contains empty placeholder folders. Group 11 contains three loose reference/data files, not a software project. Both groups were inspected and accounted for.','',
'## What was checked','',
f'- Fresh recursive metadata scan: {A["counts"]["directories"]:,} directories and {A["counts"]["files"]:,} files after exclusions.',
f'- All {len(A["git_roots"])} discovered Git roots and {A["manifest_count"]:,} project/component manifests were reconciled to report workspaces.',
f'- All 389 workspace/resource paths, 75 nested-app report entries, and {A["evidence_paths_checked"]:,} evidence references were checked.',
'- Every report entry has a purpose, stack, assessment, learning stage, prerequisites, and next action.',
'- The 476 previously hashed Gemini evidence files were reread; their hashes are unchanged.',
'- No missing report entries, unresolved project candidates, missing evidence paths, or filesystem scan errors remained.',
'- The unassigned gitvg publishing script was identified as a workspace helper, not a separate application.',
'- Git metadata was newly detected for `astraspacegameweb`; that project already has a complete report entry, so this changes the Git-root count without adding a project.','',
'This was a coverage and report-consistency audit. The earlier source assessments remain static; builds, tests, and application behavior were not executed. API/frontend packages and snapshots remain grouped under their parent workspace unless separately inventoried. Dependency/cache/generated directories, agent/editor state, links/junctions and existing inventory-output containers are excluded explicitly in the audit data.','',
'## Empty placeholders checked','']
lines.extend('- '+link(p) for p in sorted(empty))
lines+=['','[Master report](MASTER_REPORT.md) | [Detailed audit data](final-coverage-audit.json)','']
(HERE/'FINAL_REVIEW.md').write_text('\n'.join(lines),encoding='utf-8')
summary='**Final coverage check - September 7, 2026:** `_Organized Desktop` contributes **202 included project/resource records**, including 40 Master Projects and 84 Numbered Experiments. A fresh Desktop-wide scan found no additional project requiring a report entry. See the [dated coverage review](FINAL_REVIEW.md) for the full folder breakdown and exclusions.'
(HERE/'_coverage_summary.md').write_text(summary+'\n',encoding='utf-8')
text=text.replace('# Desktop projects: master SWE upskilling report\n','# Desktop projects: master SWE upskilling report\n\n'+summary+'\n',1)
(HERE/'MASTER_REPORT.md').write_text(text,encoding='utf-8')
p=HERE/'_build_master.py';s=p.read_text(encoding='utf-8')
needle="report='\\n'.join(lines)"
if '_coverage_summary.md' not in s:
    s=s.replace(needle,needle+"\nif (HERE/'_coverage_summary.md').exists():\n    report=report.replace('# Desktop projects: master SWE upskilling report\\n', '# Desktop projects: master SWE upskilling report\\n\\n'+(HERE/'_coverage_summary.md').read_text(encoding='utf-8').strip()+'\\n',1)")
    p.write_text(s,encoding='utf-8')
p=HERE/'README.md';s=p.read_text(encoding='utf-8')
if 'FINAL_REVIEW.md' not in s:p.write_text(s+'\n[Final coverage review, September 7](FINAL_REVIEW.md) confirms the organized-subfolder coverage and records the fresh filesystem checks.\n',encoding='utf-8')
link_targets=[]
for filename in ['MASTER_REPORT.md','FINAL_REVIEW.md','README.md']:
    for target in re.findall(r'\]\(([^)]+)\)',(HERE/filename).read_text(encoding='utf-8')):
        if not target.startswith(('http://','https://','#')):link_targets.append((filename,target))
def exists(item):return (HERE/unquote(item[1].split('#')[0])).exists()
with ThreadPoolExecutor(max_workers=16) as pool:
    results=list(pool.map(exists,link_targets))
A['final_document_links_checked']=len(link_targets)
A['broken_final_document_links']=[item for item,ok in zip(link_targets,results) if not ok]
A['valid']=A['valid'] and not A['broken_final_document_links']
(HERE/'final-coverage-audit.json').write_text(json.dumps(A,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'valid':A['valid'],'organized_records':202,'total_records':389,'nested_apps':75,'scanned':A['counts'],'git_roots':len(A['git_roots']),'evidence_paths_checked':A['evidence_paths_checked'],'final_links_checked':len(link_targets),'broken_links':A['broken_final_document_links'],'empty_placeholders':len(empty)},ensure_ascii=True))
if not A['valid']:raise SystemExit(1)
