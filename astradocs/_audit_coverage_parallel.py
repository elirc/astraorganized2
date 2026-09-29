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

from concurrent.futures import ThreadPoolExecutor

def scan_one(item):
    rel,absolute=item
    r={'rel':rel,'owner':owner(rel),'counts':Counter(),'pending':[],'errors':[],'skipped':[], 'git':[], 'sources':[], 'markers':[], 'docs':[], 'subdirs':[], 'files':0}
    try: entries=list(os.scandir(longpath(absolute)))
    except OSError as exc:
        r['errors'].append({'path':rel,'error':str(exc)});return r
    r['counts']['directories']=1
    for e in entries:
        child=(rel+'/' if rel else '')+e.name
        lower=e.name.lower()
        try:
            if e.is_symlink() or (hasattr(e,'is_junction') and e.is_junction()):
                r['skipped'].append({'path':child,'reason':'link/junction not followed'});continue
            if lower=='.git':r['git'].append({'path':rel,'owner':r['owner']});continue
            if e.is_dir(follow_symlinks=False):
                if not rel and e.name in root_exclusions:
                    r['skipped'].append({'path':child,'reason':'existing inventory/report container'});continue
                if lower in SKIP_DIRS:
                    r['counts']['excluded_generated_directories']+=1;continue
                r['subdirs'].append(e.name)
                r['pending'].append((child,os.path.join(absolute,e.name)))
            elif e.is_file(follow_symlinks=False):
                r['files']+=1; r['counts']['files']+=1
                ext=Path(e.name).suffix.lower()
                if ext in SOURCE_EXT:r['sources'].append(child)
                if lower in MARKERS or ext in {'.sln','.slnx','.csproj','.fsproj'}:r['markers'].append(child)
                if ext in {'.md','.mdx','.txt','.rst','.docx','.pdf','.odt'}:r['docs'].append(child)
        except OSError as exc:r['errors'].append({'path':child,'error':str(exc)})
    return r

stack=[('',str(DESKTOP))]; last=time.monotonic()
with ThreadPoolExecutor(max_workers=16) as pool:
    while stack:
        batch=stack[-512:]; del stack[-512:]
        for r in pool.map(scan_one,batch):
            rel=r['rel']; own=r['owner']; depth=rel.count('/')+1 if rel else 0
            counts.update(r['counts']);errors.extend(r['errors']);skipped.extend(r['skipped']);git_roots.extend(r['git']);stack.extend(r['pending'])
            if own:perroot[own].update({'files':r['files'],'sources':len(r['sources']),'manifests':len(r['markers']),'documents':len(r['docs'])})
            elif r['sources'] or r['markers']:unassigned.append({'directory':rel,'source_files':r['sources'],'manifests':r['markers']})
            markers.extend({'path':p,'owner':own} for p in r['markers'])
            if depth==1 or (rel.startswith('_Organized Desktop/') and depth in {2,3}) or (rel.startswith('geminiorganized/') and depth==2):
                boundary[rel]={'direct_files':r['files'],'subdirectories':r['subdirs'],'owner':own,'sources':r['sources'],'manifests':r['markers'],'documents':r['docs']}
        if time.monotonic()-last>20:
            print(json.dumps({'directories':counts['directories'],'files':counts['files'],'pending_directories':len(stack)}),flush=True);last=time.monotonic()
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
