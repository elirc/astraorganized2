"""Read-only source inventory and campaign queue reconciliation."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,subprocess,re
BASE=Path(__file__).resolve().parent.parent
DESKTOP=BASE.parent
OUT=BASE/'astradocs'
ledger=json.loads((BASE/'astra-remaining-improvements/progress.json').read_text())
pending=[r for r in ledger['projects'] if r['status']!='complete']
catalog={r['path'].casefold():r for r in json.loads((OUT/'project-review.json').read_text())['projects']}
fable={r['rel'].replace('\\','/').casefold() for r in json.loads((BASE/'fablereview/registry.json').read_text())}
EXCLUDE=['node_modules','.git','.venv','venv','__pycache__','.next','.nuxt','.svelte-kit','.turbo','.cache','.pytest_cache','.mypy_cache','.ruff_cache','.gradle','.pnpm-store','npm-cache','pip-cache']
def inspect(r):
    p=DESKTOP/r['path']; old=catalog.get(r['path'].casefold(),{})
    result={'id':r['id'],'path':r['path'],'status':r['status'],'oldAuditStatus':r.get('auditStatus'),'priorReview':old,'exists':p.is_dir(),'fableCovered':r['path'].casefold() in fable}
    if not p.is_dir():return result
    command=['rg','--files','--hidden','--no-ignore']
    for name in EXCLUDE:command+=['-g',f'!**/{name}/**']
    proc=subprocess.run(command,cwd=p,capture_output=True,text=True,encoding='utf-8',errors='replace')
    names=sorted(n.replace('\\','/') for n in proc.stdout.splitlines())
    result.update(files=names,inventoryErrors=proc.stderr.strip(),fileCount=len(names))
    result['testFiles']=[n for n in names if re.search(r'(^|/)(tests?|__tests__)/|\.(test|spec)\.|(^|/)test_[^/]+\.py$|Tests?\.cs$',n,re.I)]
    result['learningFiles']=[n for n in names if any(part.casefold() in {'astraupskill','upskilling','dfableandopus'} for part in Path(n).parts)]
    result['manifests']=[n for n in names if Path(n).name in {'package.json','pyproject.toml','Cargo.toml','requirements.txt','go.mod'} or n.endswith('.csproj')]
    result['instructions']=[n for n in names if Path(n).name=='AGENTS.md']
    result['evidenceChecks']=[]
    for ef in old.get('evidence_files',[]):
        file=DESKTOP/ef
        result['evidenceChecks'].append({'path':ef,'exists':file.is_file()})
    scripts=[]
    for n in result['manifests']:
        if Path(n).name=='package.json':
            try:
                pkg=json.loads((p/n).read_text(encoding='utf-8-sig'))
                scripts.append({'file':n,'name':pkg.get('name'),'scripts':pkg.get('scripts',{})})
            except (OSError,ValueError) as e:scripts.append({'file':n,'error':str(e)})
    result['packageScripts']=scripts
    return result
rows=[]
with ThreadPoolExecutor(max_workers=4) as pool:
    for future in as_completed([pool.submit(inspect,r) for r in pending]):
        row=future.result();rows.append(row);print(len(rows),row['path'],row.get('fileCount',0),flush=True)
rows.sort(key=lambda r:r['path'].casefold())
output={'date':'2026-09-21','scope':'Pending campaign families; static inventory only; no project execution or installs','excludedDirectoryNames':EXCLUDE,'projects':rows}
(OUT/'REMAINING_PROJECT_REVIEW_INVENTORY_2026-09-21.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
(OUT/'REMAINING_PROJECT_NAMES_2026-09-21.txt').write_text('\n'.join(r['path'] for r in rows)+'\n',encoding='utf-8')
allfiles=sorted({r['path']+'/'+f for r in rows for f in r.get('files',[])},key=str.casefold)
(OUT/'REMAINING_PROJECT_FILE_NAMES_2026-09-21.txt').write_text('\n'.join(allfiles)+'\n',encoding='utf-8')
print(json.dumps({'projects':len(rows),'files':len(allfiles),'missing':[r['path'] for r in rows if not r['exists']],'errors':[r['path'] for r in rows if r.get('inventoryErrors')]}))
