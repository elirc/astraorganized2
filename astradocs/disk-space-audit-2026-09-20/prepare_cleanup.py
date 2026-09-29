"""Read-only checks and an explicit cleanup allowlist; does not delete files."""
import json, os, hashlib
from functools import lru_cache
from pathlib import Path
from datetime import datetime, timezone
BASE=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
DESKTOP=BASE.parent
data=json.loads((OUT/'inventory.json').read_text())
def key(p): return str(p).replace('\\','/').rstrip('/').casefold()
def within(p,q): return key(p)==key(q) or key(p).startswith(key(q)+'/')
protected=[DESKTOP/'lucasrouter',BASE/'astra-remaining-improvements/stage/52d78d4a92a2']
def excluded(p): return 'lucasrouter' in key(p) or '52d78d4a92a2' in key(p) or any(within(p,q) or within(q,p) for q in protected)
roots=[Path(r['path']) for r in data['projects'] if r.get('path') and r['status']=='scanned']
selected=[];skipped=[]
def skip(r,why): skipped.append(dict(r,reason=why))
@lru_cache(maxsize=None)
def no_links(p):
    if p.lstat().st_file_attributes & 0x400: return False
    return p.parent==p or no_links(p.parent)
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.digest()
def files(p):
    for current, dirs, names in os.walk(p,followlinks=False):
        for name in dirs[:]:
            if (Path(current)/name).lstat().st_file_attributes & 0x400:
                raise ValueError('Contains directory link; retained')
        for name in names:
            f=Path(current)/name
            if f.lstat().st_file_attributes & 0x400: raise ValueError('Contains file link; retained')
            yield f
for r in data['candidates']:
    print('checking',r['id'],flush=True)
    p=Path(r['path'])
    if excluded(p): skip(r,'Lucasrouter excluded');continue
    if r['tier']=='C': skip(r,'Keep-by-default history, backup, data or unconfirmed work');continue
    if not p.exists(): skip(r,'Already absent');continue
    if not any(within(p,root) for root in roots) or not no_links(p): skip(r,'Path containment or reparse check failed');continue
    if r['tier']=='A': selected.append(dict(r,verification='Known dependency/cache from approved inventory'));continue
    if r['kind']=='Delivered staging copy':
        skip(r,'Retained whole staging copy; duplicate verification not completed. Listed dependencies/caches inside remain eligible.')
        continue
        manifest=json.loads((BASE/'astra-remaining-improvements/deliveries'/f'{p.name}.json').read_text(encoding='utf-8-sig'))
        canonical=DESKTOP/manifest['project']
        nested=[Path(x['path']) for x in data['candidates'] if x['tier']=='A' and within(x['path'],p)]
        different=[];checked=0
        try:
            for current,dirs,names in os.walk(p,followlinks=False):
                dirs[:]=[n for n in dirs if not any(within(Path(current)/n,a) for a in nested)]
                for n in dirs:
                    if (Path(current)/n).lstat().st_file_attributes & 0x400: raise ValueError('Linked directory retained')
                for n in names:
                    f=Path(current)/n
                    if any(within(f,a) for a in nested): continue
                    target=canonical/f.relative_to(p)
                    if f.lstat().st_file_attributes & 0x400 or not target.is_file() or f.stat().st_size!=target.stat().st_size or digest(f)!=digest(target):
                        different.append(str(f.relative_to(p)))
                        if len(different)>=5: break
                    checked+=1
                if len(different)>=5: break
            if different: skip(r,'Staging has unique/different files; retained: '+', '.join(different))
            else: selected.append(dict(r,verification=f'{checked} non-cache files hash-match canonical {canonical}'))
        except (OSError,ValueError) as e: skip(r,str(e))
        continue
    try:
        if p.name.lower() in {'bin','obj'} and list(p.parent.glob('*.csproj')):
            fs=list(files(p))
            unsafe=[f for f in fs if f.suffix.lower() in {'.csproj','.sln','.md','.sql','.db','.sqlite','.sqlite3'} or (f.suffix.lower()=='.cs' and not (f.name.endswith(('.g.cs','.AssemblyInfo.cs','.GlobalUsings.g.cs')) or f.name.startswith('.NETCoreApp,')))]
            if unsafe: skip(r,'Potential unique source/data/documentation in output folder')
            elif fs: selected.append(dict(r,verification='Sibling .csproj and generated .NET output contents inspected'))
            else: skip(r,'Empty')
        elif p.name.lower()=='dist' and (p.parent/'package.json').is_file():
            fs=list(files(p));names={f.name for f in fs}
            if names.intersection({'package.json','README.md'}) or any(f.suffix.lower() in {'.md','.sql','.db','.sqlite','.cs','.tsx','.jsx','.vue','.svelte'} or (f.suffix=='.ts' and not f.name.endswith('.d.ts')) for f in fs): skip(r,'Distribution contains source/docs or package metadata; retained')
            elif (p.parent/'src').is_dir() and fs: selected.append(dict(r,verification='Package manifest and sibling source exist; distribution contents inspected'))
            else: skip(r,'Output provenance not established')
        else: skip(r,'Preserve source, evidence, reports or ambiguous folder')
    except (OSError,ValueError) as e: skip(r,str(e))
    print('checked',r['id'],flush=True)
selected.sort(key=lambda r:len(r['path']))
outer=[]
for r in selected:
    if not any(within(r['path'],s['path']) for s in outer): outer.append(r)
plan={'preparedAt':datetime.now(timezone.utc).isoformat(),'protectedPaths':[str(p) for p in protected], 'allowedRoots':[str(p) for p in roots], 'selected':outer,'skipped':skipped,'estimatedLogicalBytes':sum(r['bytes'] for r in outer)}
(OUT/'approved-cleanup-plan-2026-09-21.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
print(json.dumps({'selected':len(outer),'skipped':len(skipped),'logicalGiB':plan['estimatedLogicalBytes']/1024**3}))
