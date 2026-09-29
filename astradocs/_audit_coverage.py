"""Fresh read-only filesystem reconciliation against the delivered report."""
import os, json, sys, hashlib, time
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
HERE=Path(__file__).resolve().parent
DESKTOP=HERE.parent.parent
sys.path.insert(0,str(HERE.parent/'scripts'))
from scan_desktop import SKIP_DIRS, SOURCE_EXT, MARKERS
report=json.loads((HERE/'project-review.json').read_text(encoding='utf-8'))
roots={x['path']:x for x in report['projects']}
children={x['path']:x for x in report['nested_apps']}
known=set(roots)|set(children)
root_exclusions={'AstraOrganized','AstraOrganized2','project-inventory'}
counts=Counter(); groups=Counter(); perroot=defaultdict(Counter)
errors=[]; skipped=[]; unassigned=[]; git_roots=[]; markers=[]; boundary={}; missing=[]
started=datetime.now(timezone.utc).isoformat()
def owner(rel):
    bits=rel.split('/')
    while bits:
        p='/'.join(bits)
        if p in roots:return p
        bits.pop()
    return None
def longpath(p):
    s=str(p)
    return '\\\\?\\'+s if os.name=='nt' and not s.startswith('\\\\?\\') else s
stack=[('',str(DESKTOP))]; last=time.monotonic()
while stack:
    rel,absolute=stack.pop()
    own=owner(rel)
    try:
        entries=list(os.scandir(longpath(absolute)))
    except OSError as exc:
        errors.append({'path':rel,'error':str(exc)});continue
    counts['directories']+=1
    direct_sources=[]; direct_markers=[]; docs=[]; subdirs=[]; filecount=0
    for e in entries:
        child=(rel+'/' if rel else '')+e.name
        lower=e.name.lower()
        try:
            if e.is_symlink() or (hasattr(e,'is_junction') and e.is_junction()):
                skipped.append({'path':child,'reason':'link/junction not followed'});continue
            if lower=='.git':git_roots.append({'path':rel,'owner':own});continue
            if e.is_dir(follow_symlinks=False):
                if not rel and e.name in root_exclusions:
                    skipped.append({'path':child,'reason':'existing inventory/report container'});continue
                if lower in SKIP_DIRS:
                    counts['excluded_generated_directories']+=1;continue
                subdirs.append(e.name)
                stack.append((child,os.path.join(absolute,e.name)))
            elif e.is_file(follow_symlinks=False):
                filecount+=1; counts['files']+=1
                ext=Path(e.name).suffix.lower()
                if ext in SOURCE_EXT:direct_sources.append(child)
                if lower in MARKERS or ext in {'.sln','.slnx','.csproj','.fsproj'}:direct_markers.append(child)
                if ext in {'.md','.mdx','.txt','.rst','.docx','.pdf','.odt'}:docs.append(child)
        except OSError as exc:errors.append({'path':child,'error':str(exc)})
    if own:
        perroot[own].update({'files':filecount,'sources':len(direct_sources),'manifests':len(direct_markers),'documents':len(docs)})
    elif direct_sources or direct_markers:
        unassigned.append({'directory':rel,'source_files':direct_sources,'manifests':direct_markers})
    for marker in direct_markers:markers.append({'path':marker,'owner':own})
    depth=rel.count('/')+1 if rel else 0
    if depth==1 or (rel.startswith('_Organized Desktop/') and depth in {2,3}) or (rel.startswith('geminiorganized/') and depth==2):
        boundary[rel]={'direct_files':filecount,'subdirectories':subdirs,'owner':own,'sources':direct_sources,'manifests':direct_markers,'documents':docs}
    if time.monotonic()-last>20:
        print(json.dumps({'scanning':rel,'directories':counts['directories'],'files':counts['files']}),flush=True);last=time.monotonic()
for path in roots:
    if not os.path.isdir(longpath(DESKTOP/path)):missing.append(path)
for path in roots:
    if path.startswith('_Organized Desktop/'):
        groups[path.split('/')[1]]+=1
checks=0; broken=[]; hashes_changed=[]
for row in list(roots.values())+list(children.values()):
    for p in row.get('evidence_files',[]):
        checks+=1
        if not os.path.isfile(longpath(DESKTOP/p)):broken.append(p)
for row in json.loads((HERE/'review-gemini.json').read_text(encoding='utf-8'))['projects']:
    for item in row.get('fresh_checks',[]):
        try:
            with open(longpath(DESKTOP/item['path']),'rb') as f:h=hashlib.sha256(f.read()).hexdigest()
            if h!=item['sha256']:hashes_changed.append(item['path'])
        except OSError as exc:errors.append({'path':item['path'],'error':str(exc)})
result={'started_at':started,'completed_at':datetime.now(timezone.utc).isoformat(),'scope':str(DESKTOP),'counts':dict(counts),'report_records':len(roots),'nested_apps':len(children),'organized_records':sum(groups.values()),'organized_groups':dict(sorted(groups.items())),'per_project_fresh_counts':{k:dict(v) for k,v in perroot.items()},'boundaries':boundary,'missing_project_paths':missing,'source_or_manifest_outside_report':unassigned,'git_roots':git_roots,'uncovered_git_roots':[x for x in git_roots if not x['owner']],'manifest_count':len(markers),'evidence_paths_checked':checks,'missing_evidence':sorted(set(broken)),'gemini_sample_changes':hashes_changed,'scan_errors':errors,'explicit_exclusions':skipped,'method':'Fresh recursive metadata scan, current evidence-path verification and comparison of 476 previously hashed Gemini samples; dependencies/generated output and report containers excluded. No project code executed.'}
(HERE/'final-coverage-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in {'per_project_fresh_counts','boundaries','git_roots','explicit_exclusions'}},ensure_ascii=True))
