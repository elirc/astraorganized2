import json,re,hashlib,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE=Path(__file__).resolve().parent; DESKTOP=HERE.parent.parent
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
d=json.loads((HERE/'tutorial-discovery.json').read_text(encoding='utf-8'))
old=json.loads((HERE.parent/'project-catalog.json').read_text(encoding='utf-8'))['projects']
old={x['path']:x for x in old}
samples=d['samples']; extra=set()
for row in d['projects']:
    root=row['path']; options=row['candidates']
    for filename in ['README.md','LEARNER-GUIDE.md','CODEBASE_GUIDE.md','JOURNAL.md','PHASE_PLANS.md']:
        p=DESKTOP/root/filename
        if p.is_file():extra.add(root+'/'+filename)
    extra.update(p for p in old.get(root,{}).get('learning_material',{}).get('key_paths',[])[:3] if Path(p).suffix.lower() in {'.md','.mdx','.txt','.rst'})
    fable_families={}
    for x in options:
        if not x['fable_named'] or x['binary']:continue
        bits=x['relative'].split('/')
        for i,bit in enumerate(bits):
            if re.search(r'fable',bit,re.I):
                family='/'.join(bits[:i+1]);break
        fable_families.setdefault(family,[]).append(x)
    for fam,opts in fable_families.items():
        starters=sorted(opts,key=lambda x:(0 if Path(x['path']).name.lower()=='readme.md' else 1 if re.search(r'00|01.*(?:overview|map|architecture|readme)',Path(x['path']).name,re.I) else 2,len(x['relative']),x['path']))
        if starters:extra.add(starters[0]['path'])
for root in ['netsnapshot','netsnapshot1','geminiorganized/OpenSource_Upskilling_Snapshot','geminiorganized/OpenSource_Upskilling_Snapshot1']:
    for p in (DESKTOP/root/'snapshots').glob('00*/NOTES.md'):extra.add(p.relative_to(DESKTOP).as_posix())
extra-=set(samples)
def read_one(path):
    try:
        raw=(DESKTOP/path).read_bytes();t=raw.decode('utf-8-sig',errors='replace')
        h=[l.strip() for l in t.splitlines() if re.match(r'^#{1,5}\s',l)][:35]
        lines=[l.strip() for l in t.splitlines() if l.strip() and not l.startswith(('![','[![','<img','<a href'))]
        pats={'explanation':r'codebase|walkthrough|walk-through|request (?:flow|path|lifecycle)|how (?:it|the .{1,30}) works|file.by.file|code (?:map|tour)|architecture|data flow|call graph|execution flow|reading order|where (?:the|to)|trace','tutorial':r'exercise|lesson|sprint|curriculum|learn(?:er|ing)|checkpoint|practice|workbook|step.by.step|predict|teach|mission','plan':r'implementation plan|specification|build specification|not implemented|future work|planned|prompt','code_refs':r'[\w./-]+\.(?:tsx?|jsx?|cs|py|rs|sql|java)\b'}
        return path,{'path':path,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'headings':h,'opening':'\n'.join(lines[:32])[:2600],'signals':{k:len(re.findall(v,t,re.I)) for k,v in pats.items()},'sample_code_refs':list(dict.fromkeys(re.findall(pats['code_refs'],t,re.I)))[:8],'error':None}
    except OSError as e:return path,{'path':path,'error':str(e)}
with ThreadPoolExecutor(max_workers=16) as pool:samples.update(dict(pool.map(read_one,sorted(extra))))
for row in d['projects']:
    row['samples']=[v for p,v in samples.items() if p.startswith(row['path']+'/')]
d['samples']=samples
d['supplemental_samples']=len(extra)
(HERE/'tutorial-discovery.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'samples':len(samples),'additional':len(extra),'errors':[s for s in samples.values() if s.get('error')]}))
