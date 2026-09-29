"""Discover and sample learning documentation; no source project execution."""
import json,re,hashlib,sys
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
HERE=Path(__file__).resolve().parent; DESKTOP=HERE.parent.parent
catalog=json.loads((HERE/'project-review.json').read_text(encoding='utf-8'))
roots={r['path']:r for r in catalog['projects']}
children={r['path']:r for r in catalog['nested_apps']}
index=json.loads((HERE.parent/'scan-index.json').read_text(encoding='utf-8'))['directories']
docs=defaultdict(list)
TEXT={'.md','.mdx','.txt','.rst'}
BINARY={'.pdf','.docx','.odt'}
fable=re.compile(r'fable[ _-]*doc|(?:^|/)fable(?:/|\.md$)|fable learning',re.I)
strong=re.compile(r'codebase|walkthrough|walk-through|learner.guide|learning.path|upskill|tutorial|curriculum|explain|deep.dive|learning.outcome|learners?|teaching|handbook|workbook|getting.started|onboarding|architecture|guide|training|lesson|curriculum',re.I)
def owner(path):
    bits=path.split('/')
    while bits:
        p='/'.join(bits)
        if p in roots:return p
        bits.pop()
    return None
def rate(relative):
    name=Path(relative).name.lower(); low=relative.lower()
    if any(x in low.split('/') for x in ['fixtures','translations','locales','changelog','changes','__snapshots__']):return 0
    fb=bool(fable.search(relative))
    score=120 if fb else 0
    if re.search(r'codebase|walkthrough|walk-through|learner.guide|learning.path|upskill|curriculum|tutorial|explain',low):score+=55
    elif strong.search(low):score+=30
    if name in ['readme.md','index.md','00-readme.md','00-index.md','start-here.md','00-start-here.md']:score+=25
    if re.search(r'(^|[-_])0[01][-_]|overview|codebase.map|reading.order|learning.path',name):score+=15
    if re.search(r'codebase.guide|learner.guide|fable\.md',name):score+=40
    score-=max(0,len(relative.split('/'))-3)*2
    if name in ['agents.md','claude.md','gemini.md','license.md','changelog.md']:return 0
    if name.startswith(('package-lock','yarn.lock','pnpm-lock')):return 0
    return score
for directory,info in index.items():
    root=owner(directory)
    if not root:continue
    for name in info['files']:
        ext=Path(name).suffix.lower()
        if ext not in TEXT|BINARY:continue
        full=directory+'/'+name
        relative=full[len(root)+1:]
        score=rate(relative)
        if score>0:
            entry={'path':full,'relative':relative,'score':score,'fable_named':bool(fable.search(relative)),'binary':ext in BINARY}
            docs[root].append(entry)
# Read the root README for the one root absent from the old discovery index if present.
for root in set(roots)-{owner(k) for k in index}:
    for p in (DESKTOP/root).glob('README*'):
        if p.suffix.lower() in TEXT:docs[root].append({'path':p.relative_to(DESKTOP).as_posix(),'relative':p.name,'score':25,'fable_named':False,'binary':False})

def family(entry):
    bits=entry['relative'].split('/')
    for i,b in enumerate(bits):
        if fable.search(b):return '/'.join(bits[:i+1])
    return '/'.join(bits[:-1]) or '.'
selected={}
for root,options in docs.items():
    ordered=sorted((x for x in options if not x['binary']),key=lambda x:(-x['score'],len(x['relative']),x['path']))
    picks=[];families=set()
    for option in ordered:
        fam=family(option)
        if fam not in families and len(picks)<3:
            picks.append(option);families.add(fam)
    if len(picks)<3:
        picks.extend(x for x in ordered if x not in picks and len(picks)<3)
    for p in picks:selected[p['path']]=p
# Individually evaluate the 75 nested apps, not only their parent's best doc.
child_candidates={}
for child in children:
    parent=children[child]['parent_path']
    options=[x for x in docs.get(parent,[]) if x['path'].startswith(child+'/')]
    ordered=sorted((x for x in options if not x['binary']),key=lambda x:(-x['score'],len(x['path'])))
    child_candidates[child]=options
    for p in ordered[:2]:selected[p['path']]=p

def read_one(item):
    path,entry=item
    try:
        raw=(DESKTOP/path).read_bytes();text=raw.decode('utf-8-sig',errors='replace')
        headings=[s.strip() for s in text.splitlines() if re.match(r'^#{1,5}\s',s)][:35]
        lines=[s.strip() for s in text.splitlines() if s.strip() and not s.startswith(('![','[![','<img','<a href'))]
        terms={
          'explanation':re.findall(r'codebase|walkthrough|walk-through|request (?:flow|path|lifecycle)|how (?:it|the .{1,30}) works|file.by.file|code (?:map|tour)|architecture|data flow|call graph|execution flow|reading order|where (?:the|to)|trace',text,re.I),
          'tutorial':re.findall(r'exercise|lesson|sprint|curriculum|learn(?:er|ing)|checkpoint|practice|workbook|step.by.step|predict|teach|mission',text,re.I),
          'plan':re.findall(r'implementation plan|specification|build specification|not implemented|future work|planned|prompt',text,re.I),
          'code_refs':re.findall(r'[\w./-]+\.(?:tsx?|jsx?|cs|py|rs|sql|java)\b',text),
        }
        return path,{'path':path,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'headings':headings,'opening': '\n'.join(lines[:28])[:2300], 'signals':{k:len(v) for k,v in terms.items()},'sample_code_refs':list(dict.fromkeys(terms['code_refs']))[:8], 'error':None}
    except OSError as exc:return path,{'path':path,'error':str(exc)}
with ThreadPoolExecutor(max_workers=16) as pool:samples=dict(pool.map(read_one,selected.items()))
profiles=[]
for root,row in roots.items():
    options=docs.get(root,[]);picks=[samples[x['path']] for x in selected.values() if x['path'].startswith(root+'/') and owner(x['path'])==root]
    # Child samples remain attached for complete evidence, but classification is at workspace level.
    profiles.append({'path':root,'purpose':row['purpose'],'phase':row['phase'],'role':row['curriculum_role'],'candidates':options,'fable_named_files':sum(x['fable_named'] for x in options),'samples':picks})
result={'date':'2026-09-07','scope_records':len(roots),'nested_apps':len(children),'method':'Discover documentation from the complete file inventory; freshly read representative text entrypoints. A path name is a discovery hint, not confirmation of tutorial quality.','projects':profiles,'child_candidates':child_candidates,'samples':samples}
(HERE/'tutorial-discovery.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'projects':len(profiles),'with_candidates':sum(bool(x['candidates']) for x in profiles),'with_fable_named_docs':sum(x['fable_named_files']>0 for x in profiles),'fresh_samples':len(samples),'read_errors':[x for x in samples.values() if x.get('error')]},ensure_ascii=True))
for x in profiles:
    if x['fable_named_files']:
        chosen=[s for s in x['samples'] if not s.get('error')][:2]
        print(json.dumps({'path':x['path'],'fable_files':x['fable_named_files'],'samples':[{'file':s['path'],'headings':s['headings'][:8],'opening':s['opening'][:650],'signals':s['signals']} for s in chosen]},ensure_ascii=True))
