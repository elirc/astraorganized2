import json,re,sys
from pathlib import Path
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote,unquote
HERE=Path(__file__).resolve().parent;DESKTOP=HERE.parent.parent
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
d=json.loads((HERE/'tutorial-discovery.json').read_text(encoding='utf-8'))
master=json.loads((HERE/'project-review.json').read_text(encoding='utf-8'))
samples=d['samples']
fable=re.compile(r'fable[ _-]*doc|(?:^|/)fable(?:/|\.md$)|fable learning',re.I)
workflow={'hermes','geminiorganized/FableDocs_Projects_Hermes','master plan','geminiorganized/General_MasterPlan','readme','geminiorganized/General_Readme','gitjira','geminiorganized/General_Gitjira'}
labels={4:'Codebase walkthrough / study pack',3:'Structured tutorial / exercises',2:'Developer explanation / brief orientation',1:'Plans, workflow, setup or reference only',0:'No substantive guide verified'}
def clean(s):
    s=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',str(s))
    return re.sub(r'\s+',' ',s.replace('|',' / ').replace('`','')).strip()
def link(p,label=None):return '['+clean(label or p).replace('[','').replace(']','')+'](../../'+quote(p,safe='/')+')'
def stub(s):
    if s.get('error'):return True
    t=s.get('opening','').lower()
    return s.get('bytes',0)<150 or (s.get('bytes',0)<600 and bool(re.search(r'todo|not yet filled|placeholder|not populated|coming soon',t)))
def classify(s,root):
    if stub(s):return 0
    rel=s['path'][len(root)+1:].lower();base=Path(rel).name
    h=' '.join(s.get('headings',[])).lower();t=s.get('opening','').lower();sig=s.get('signals',{})
    e=sig.get('explanation',0);c=sig.get('code_refs',0);learn=sig.get('tutorial',0);size=s.get('bytes',0)
    if root in workflow:return 1
    if re.search(r'proposed|rebuild specification', (s.get('headings') or [''])[0],re.I):return 1
    if re.search(r'(^|/)(?:handoff|prompts?)(/|$)',rel) or re.search(r'(?:^|[-_])(?:spec|specification|plan|roadmap|prompt|backlog|user.stories)(?:[-_.]|$)',base):return 1
    if fable.search(rel) and 'code review' in (s.get('headings') or [''])[0].lower():return 2
    if fable.search(rel) and not re.search(r'pm.onboarding|product.reference|build.order',rel) and (e>=1 or c>=2) and size>=250:return 4
    if re.search(r'codebase|cartography|walkthrough|walk-through|code.reading.guide|code.tour|how.this.app.works|app.overview',rel+' '+h) and (e>=1 or c>=2) and size>=250:return 4
    if re.search(r'learner.guide|workbook|worked.examples|upskill|tutorial|curriculum|learning.path|training.docs|training.lab|teaching|snapshot|learning.lab|course',rel+' '+h) and (learn>=2 or e>=3) and size>=250:return 3
    if base in {'learning-journal.md','journal.md'} and learn>=2:return 3
    if re.search(r'architecture|onboarding|developer.guide|code.map|project.map|folder.map|how.it.works',rel+' '+h) and size>=500 and (e>=1 or c>=2):return 2
    if base=='readme.md' and c>=5 and re.search(r'map|architecture|flow|layout',h):return 2
    return 1

def pick(root,ss):
    scored=[]
    for s in ss:
        rank=classify(s,root)
        rel=s['path'][len(root)+1:]
        order=(rank, int(bool(fable.search(rel))), int(Path(rel).name.lower() in {'readme.md','fable.md','learner-guide.md','codebase_guide.md'}),-len(rel))
        scored.append((order,s))
    return sorted(scored,key=lambda x:x[0],reverse=True)

def topics(s):
    h=' '.join(s.get('headings',[])).lower();t=s.get('opening','').lower();alltext=h+' '+t
    result=[]
    for pattern,label in [(r'cartography|codebase.map|system.map|project.map|folder.map|file.reading|reading.order|code.tour','code map and reading order'),(r'flow|request|lifecycle','request/data-flow explanations'),(r'architecture|layer|boundar','architecture and boundaries'),(r'exercise|lab|mission|challenge|checkpoint','exercises or checkpoints'),(r'sprint|curriculum|course|lesson','ordered learning material'),(r'bug|gotcha|trap|defect|review','review notes and pitfalls'),(r'interview','interview practice'),(r'test|debug','testing/debugging guidance')]:
        if re.search(pattern,alltext):result.append(label)
    return ', '.join(result[:4]) or 'Orientation and usage information; see the linked entrypoint.'

def make_row(root,purpose,phase,ss,candidates):
    ranked=pick(root,ss)
    best=ranked[0][1] if ranked else None
    level=ranked[0][0][0] if ranked else 0
    selected=[x[1]['path'] for x in ranked if x[0][0]>=2][:3]
    if not selected and best:selected=[best['path']]
    fb=[x for x in candidates if x['fable_named']]
    families=set()
    for x in fb:
        bits=x['relative'].split('/')
        for i,bit in enumerate(bits):
            if 'fable' in bit.lower():families.add(root+'/'+'/'.join(bits[:i+1]));break
    placeholders=[s['path'] for s in ss if not s.get('error') and stub(s)]
    notes=[]
    if placeholders:notes.append('Some sampled documentation is empty/placeholder material; use the populated starting file.')
    if root in workflow:notes.append('Useful workflow/planning/reference material, not an explanation of an application codebase.')
    if root.endswith('/.netvg'):notes.append('The Fable folder is a code-review pack; docs/upskill supplies the actual learning curriculum.')
    if root=='spacegamev2':notes.append('fabledocs describes the existing build; fabledocs2 is a rebuild specification; fabledocs3 is product onboarding. These are different purposes, not interchangeable editions.')
    if root.endswith('buildagentteachGEM'):notes.append('The gotchas document describes an earlier baseline; check 04-what-changed.md before treating a listed issue as current.')
    if root in {'netnotion','geminiorganized/OpenSource_Upskilling_Notion'}:notes.append('docs/fable is substantive; the sampled docs/upskill README is explicitly unfilled.')
    if len(families)>1 and any(re.search(r'fable[ _-]*docs?[0-9]+$',Path(p).name,re.I) for p in families):notes.append('Multiple Fable sets are listed; a higher suffix is not proof of a better starting point.')
    return {'path':root,'purpose':purpose,'phase':phase,'level':level,'classification':labels[level],'fable_named_files':len(fb),'fable_locations':sorted(families),'candidate_file_count':len(candidates),'entrypoint':best['path'] if best else None,'selected_docs':selected,'topics':topics(best) if best else '', 'notes':notes,'placeholder_samples':placeholders,'sampled_files':[s['path'] for s in ss],'binary_candidates':[x['path'] for x in candidates if x['binary']]}
rows=[make_row(x['path'],x['purpose'],x['phase'],x['samples'],x['candidates']) for x in d['projects']]
# The newer direct course and older copied course are deliberately kept separate.
for r in rows:
    if r['path'] in {'grokjs','geminiorganized/LLM_Generated_Grokjs'}:
        r.update(level=3,classification=labels[3],topics='Fable Learning Lab: worked JavaScript, TypeScript, React and C# problems, plus broader language labs.')
    if r['path'] in {'GPTDocs','claude docs','geminiorganized/LLM_Generated_Gptdocs','geminiorganized/LLM_Generated_ClaudeDocs'}:
        r.update(level=3,classification=labels[3],topics='General engineering worked examples and best-practice explanations; this is a learning/reference collection, not a walkthrough of one application.')
        r['notes'].append('The worked-example material is separate from any planning documents in this folder.')
    if r['path']=='recipeweb':
        r['entrypoint']='recipeweb/docs/01-ONBOARDING.md'
    if r['path']=='JS1':
        r['entrypoint']='JS1/README.md'
        r['notes'].append('Start with the root tier map; CODEBASE_GUIDE.md files explain individual exercises at different levels.')
    if r['path'] in {'newcodexJS','geminiorganized/General_Newcodexjs'}:
        r['entrypoint']=r['path']+'/01-task-manager/docs/FABLE.md'
    if r['path']=='JSProjectLearn':
        r.update(level=3,classification=labels[3],entrypoint='JSProjectLearn/README.md',topics='SkillForge Quest: a guided mission curriculum; distinguish the current course from the expansion proposal in handoff/.')
    if r['path']=='geminiorganized/LLM_Generated_Jsprojectlearn':
        r.update(level=3,classification=labels[3],topics='Older JavaScript, React and TypeScript refactoring curriculum; differs from the direct Desktop SkillForge Quest version.')
child_rows=[]
for child in master['nested_apps']:
    path=child['path'];ss=[s for p,s in samples.items() if p.startswith(path+'/')]
    candidates=[]
    for x in d['child_candidates'].get(path,[]):
        x=dict(x);x['relative']=x['path'][len(path)+1:];candidates.append(x)
    child_rows.append(make_row(path,child['purpose'],child['phase'],ss,candidates))
counts=Counter(r['classification'] for r in rows)
fables=[r for r in rows if r['fable_named_files']]
confirmed=[r for r in rows if r['level']>=2]
lines=['# Projects with codebase explanations and tutorials','', 'Reviewed September 7, 2026. Scope: the 389 Desktop/workspace/resource records, including all 202 records in `_Organized Desktop`, plus the 75 separately listed teaching apps within three parent workspaces.','',
    f'**{len(fables)} project/workspace locations contain Fable-named documentation.** Across Fable and other names, **{sum(r["level"]>=3 for r in rows)} locations have a walkthrough, study pack, or structured tutorial**, and **{sum(r["level"]==2 for r in rows)} have lighter developer explanations/orientation** in the sampled material. The categories below distinguish their depth and purpose. Copies remain separate locations, not separate course recommendations.','',
    '| Material found | Workspace/resource records |','|---|---:|']
for level in [4,3,2,1,0]:lines.append('| '+labels[level]+' | '+str(sum(r['level']==level for r in rows))+' |')
lines+=['','A Fable label is a discovery clue. Some Fable files are reviews, specifications, or coaching workflows. Likewise, a folder called docs/upskill can contain placeholders. The linked starting files below were freshly read; this is not a claim that every page or its code references are current.','',
'## Navigation','', '- [Fable documentation by project](#projects-with-fable-named-material)', '- [Similar guides and tutorials](#similar-material-without-a-fable-name)', '- [Guides for the 75 nested apps](#guides-inside-the-75-nested-teaching-apps)', '- [Placeholder documents](#sampled-empty-or-placeholder-guides)', '- [Other projects and review limits](#other-projects-no-dedicated-explanationtutorial-confirmed)', '', '## Useful starting points','', '| Goal | Open first | What it gives you |','|---|---|',
'| Small app plus guided changes | '+link('newcodexJS/01-task-manager/docs/FABLE.md')+' | A FABLE guide for the first numbered app; use the child-app table below for all 20. |',
'| Understand a small React codebase | '+link('jobtrack/fabledocs/01-codebase-cartography/README.md')+' | Code map, file reading order and flow traces for the local-first Daybook app. This is the Desktop jobtrack, not the separate organized-folder job track. |',
'| React onboarding | '+link('recipeweb/docs/01-ONBOARDING.md')+' | Running the app and touring the source; distinguish this from its proposed .NET rewrite docs. |',
'| Full-stack concept-and-flow course | '+link('_Organized Desktop/04 JavaScript Training/jstrain5/fable-docs/README.md')+' | OpsForge chapters tied to source, exercises, glossary, and an older per-file guide collection. |',
'| React architecture | '+link('_Organized Desktop/04 JavaScript Training/reactbullet/bulletproof-react/fable-docs/README.md')+' | Junior-oriented explanations around Bulletproof React. |',
'| Larger application walkthrough | '+link('_Organized Desktop/02 Build Projects/buildagentteaching/docs/02-codebase-reading-guide.md')+' | File reading order and specific feature/request traces. |',
'| Guided .NET practice | '+link('borrowbox/LEARNER-GUIDE.md')+' | Learner instructions around the lending application and its teaching progression. |',
'| .NET codebase reading | '+link('netnotion/docs/fable/01-codebase-map.md')+' | A populated code map and exercises; its separate upskill index is a placeholder. |',
'| Architecture reference study | '+link('netcleanarch/CleanArchitecture/fabledocs/01-codebase-cartography/README.md')+' | A code map and reading path before the other Fable architecture/decision packs. |','',
'## Projects with Fable-named material','',
'Counts in this section are discovered Fable-named document files, not a count of fully read or completed lessons. Each location is retained so you can find your actual working copy.','']

def table(group,show_fable=False):
    out=['| Project / folder | Material and starting file | What to expect |','|---|---|---|']
    for r in sorted(group,key=lambda x:(x['phase'],x['path'].lower())):
        start=link(r['entrypoint'],'Start here') if r['entrypoint'] else 'No readable text entrypoint verified'
        material=r['classification']+'. '+start
        if show_fable:material+='; '+str(r['fable_named_files'])+' Fable-named files. '+', '.join(link(p,Path(p).name) for p in r['fable_locations'])
        note=r['topics']+(' '+ ' '.join(r['notes']) if r['notes'] else '')
        out.append('| '+link(r['path'])+' (stage '+str(r['phase'])+') | '+material+' | '+clean(note)+' |')
    return out+['']
for title,pred in [('Desktop projects',lambda r:not r['path'].startswith(('_Organized Desktop/','geminiorganized/'))),('Inside _Organized Desktop',lambda r:r['path'].startswith('_Organized Desktop/')),('Gemini copies and related locations',lambda r:r['path'].startswith('geminiorganized/'))]:
    lines+=['### '+title,'']+table([r for r in fables if pred(r)],True)
lines+=['## Similar material without a Fable name','',
'These are also useful matches: codebase guides, docs/upskill, learner guides, walkthroughs, architecture explanations, workbooks, and teaching histories. A brief developer orientation is labeled separately from an actual curriculum.','']
for title,pred in [('Desktop projects',lambda r:not r['path'].startswith(('_Organized Desktop/','geminiorganized/'))),('Inside _Organized Desktop',lambda r:r['path'].startswith('_Organized Desktop/')),('Gemini copies and related locations',lambda r:r['path'].startswith('geminiorganized/'))]:
    lines+=['### '+title,'']+table([r for r in rows if not r['fable_named_files'] and r['level']>=2 and pred(r)])
lines+=['## Guides inside the 75 nested teaching apps','',
'These apps are already included in the parent-workspace totals. They are listed individually here so you can open the precise guide. All 20 newcodexJS apps have a docs/FABLE.md file; the other workspaces use their own README/upskill documents.','']
for parent in ['newcodexJS','newcodecjs2','newcodex3']:
    lines+=['### '+parent,'']+table([r for r in child_rows if r['path'].startswith(parent+'/')])
lines+=['## Documentation that needs care','',
'- **Hermes/FABLEDOCS.md:** a coaching/operating pack, not a walkthrough of an application implementation.',
'- **Fable review packs:** issues and improvements can teach code reading, but they are not automatically a sequential tutorial. Check their review date and the current source.',
'- **Multiple editions:** fabledocs2/3/4 can be architecture commentary, inferred decisions, product onboarding, or a future rebuild specification. Read the stated scope before choosing one.',
'- **Placeholder modules:** a populated curriculum index does not mean the rest of its chapters are filled. The table flags placeholders seen in the samples.',
'- **Plans and source comments:** an implementation spec or proposed rewrite is different from an explanation of the current code. Inline source comments were not exhaustively evaluated for this report.','',
'### Sampled empty or placeholder guides','', '| Project | Placeholder example | Populated starting point, if found |','|---|---|---|']
for r in rows:
    if r['placeholder_samples']:
        lines.append('| '+link(r['path'])+' | '+link(r['placeholder_samples'][0])+' | '+(link(r['entrypoint']) if r['level']>=2 else 'No substantive guide confirmed in the sample')+' |')
lines+=['','## Other projects: no dedicated explanation/tutorial confirmed','',
'These entries are included for coverage. They may have setup notes, specs, ordinary reference documents, or material not captured by the sampled entrypoints. This is not proof that no useful explanation exists anywhere in the source.','']
for r in sorted((r for r in rows if r['level']<2),key=lambda r:r['path'].lower()):
    lines.append('- '+link(r['path'])+' - '+r['classification']+'.'+(' Sample: '+link(r['entrypoint']) if r['entrypoint'] else ''))
lines+=['','## Method and validation','',
    f'Searched the full indexed file tree for Fable variants and equivalent documentation patterns, then freshly read {len(samples):,} text files across project entrypoints and nested app guides. Titles, structure, content, and source-path references informed the categories. The same Desktop coverage was reconciled in the [final coverage review](FINAL_REVIEW.md).',
    'The documentation itself was reviewed for what it offers. Its historical bug claims, inferred architecture decisions, line numbers, and advertised test results were not revalidated by running projects. Large chapter sets were sampled rather than read end to end. Binary documents were not used as positive evidence without text inspection.',
    'Stages are inherited from the [master learning report](MASTER_REPORT.md); a well-documented large system can still be an advanced reading project.',
    'The [structured tutorial inventory](project-tutorials.json) preserves every classification, starting file, sampled file, placeholder flag, and candidate count.','']
text='\n'.join(lines)
(HERE/'PROJECT_TUTORIALS_REPORT.md').write_text(text,encoding='utf-8')
payload={'review_date':'2026-09-07','workspace_records':len(rows),'nested_apps':len(child_rows),'fable_named_locations':len(fables),'confirmed_explanation_or_tutorial_locations':len(confirmed),'classification_counts':dict(counts),'fresh_text_files_read':len(samples),'projects':rows,'nested_app_guides':child_rows}
(HERE/'project-tutorials.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
links=[]
for target in re.findall(r'\]\(([^)]+)\)',text):
    if not target.startswith(('http://','https://','#')):links.append(target)
with ThreadPoolExecutor(max_workers=16) as pool:
    exists=list(pool.map(lambda t:(HERE/unquote(t.split('#')[0])).exists(),links))
broken=[p for p,ok in zip(links,exists) if not ok]
validation={'workspace_records':len(rows),'organized_records':sum(x['path'].startswith('_Organized Desktop/') for x in rows),'nested_app_records':len(child_rows),'fresh_text_files_read':len(samples),'read_errors':[s for s in samples.values() if s.get('error')],'links_checked':len(links),'broken_links':broken,'valid':not broken and not any(s.get('error') for s in samples.values())}
(HERE/'tutorial-report-validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
print(json.dumps({'counts':dict(counts),'fable':len(fables),'positive':len(confirmed),'validation':validation},ensure_ascii=True))
print('REVIEW_CLASSIFICATIONS')
for r in rows:
    print(json.dumps({'p':r['path'],'level':r['level'],'start':r['entrypoint'],'placeholder_count':len(r['placeholder_samples'])},ensure_ascii=True))
if broken:raise SystemExit(1)
