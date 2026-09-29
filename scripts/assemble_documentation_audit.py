from pathlib import Path
import json,collections,re,math,hashlib,concurrent.futures
R=Path(__file__).resolve().parents[1];D=R.parent;O=R/'documentation-audit'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
prior=read(R/'astradocs/project-review.json');old={r['path']:r for r in prior['projects']}
tutorials={r['path']:r for r in read(R/'astradocs/project-tutorials.json')['projects']}
scans=[read(p) for p in O.glob('????????????.json')]
roots=dict(old)
for scan in scans:
 if not any(x==scan['top'] or x.startswith(scan['top']+'/') for x in roots):roots[scan['top']]={'path':scan['top'],'purpose':'Newly discovered location; inspect source and documentation.','record_kind':'new'}
for child,purpose in [('job-tracker-next','Separate job-tracker application variant.'),('live-chat-support-platform','Live customer-support chat application.'),('restaurant-kitchen-display-system','Restaurant kitchen order/display application.'),('task-queue-system','Background task queue application.')]:
 path='_Organized Desktop/08 App And Product Projects/job track/'+child
 roots[path]={'path':path,'purpose':purpose,'record_kind':'software-project-or-workspace'}
ordered=sorted(roots,key=len,reverse=True)
for original,mirror in [('gitvg','geminiorganized/General_Gitvg'),('jsharness','geminiorganized/General_Jsharness')]:
 for path,row in old.items():
  if path.startswith(original+'/') and (D/mirror/path[len(original)+1:]).is_dir():
   target=mirror+'/'+path[len(original)+1:]
   roots[target]={**row,'path':target}
 roots[mirror]['record_kind']='learning-or-reference-collection'
ordered=sorted(roots,key=len,reverse=True)
for path,purpose in [
 ('_Organized Desktop/05 Numbered Experiments/z3/customer-feedback-board','Independent feedback, voting, moderation and roadmap application.'),
 ('_Organized Desktop/05 Numbered Experiments/z3/founder-crm-lite','Independent founder CRM with leads, conversion, imports and pipeline workflows.'),
 ('_Organized Desktop/06 AI And Learning/codehelper/ww20','Copied multi-tenant service-platform sample embedded in Code Helper.')]:
 roots[path]={'path':path,'purpose':purpose,'record_kind':'software-project-or-workspace'}
ordered=sorted(roots,key=len,reverse=True)
def owner(path):
 return next((p for p in ordered if path==p or path.startswith(p+'/')),None)
units={p:{'path':p,'absolutePath':str(D/p),'name':p.split('/')[-1],'summary':r.get('purpose',''),'priorKind':r.get('record_kind'),'files':[],'documents':[],'components':[],'errors':[]} for p,r in roots.items()}
unassigned=[]
for scan in scans:
 for kind,dest in [('files','files'),('docs','documents'),('directories','components'),('errors','errors')]:
  for item in scan[kind]:
   key=owner(item['path'])
   if key:units[key][dest].append(item)
   elif kind in ('files','directories'):unassigned.append(item)
DIM=['onboarding','architecture','explanation','curriculum','workflow','advanced']
def docscore(x):
 h=x.get('dimensions',{});return sum(min(8,h.get(k,0)) for k in DIM)+min(8,math.log2(max(1,x.get('words',0))))+8*bool(re.search('fable|upskill|curriculum|mission-learning|_learning',x['path'],re.I))
for key,u in units.items():
 src=[f for f in u['files'] if f['source']];u['sourceFiles']=len(src);u['sourceBytes']=sum(f['bytes'] for f in src)
 docs=[x for x in u['documents'] if not x.get('skipped')];
 for x in docs:
  x['dimensions']['curriculum']+=sum(bool(re.search(r'exercises?|challenges?|checkpoints?|quizzes|drills?|missions?|tickets?|learning objectives|self.grade',h,re.I)) for h in x['headings'])
 u['documentCount']=len(docs);u['documentWords']=sum(x['words'] for x in docs)
 unique_docs=list({x['sha256']:x for x in reversed(docs) if not re.search(r'/embedded_assets_source/|/(?:docs|doc|documentation)/(?:docs/)?(?:cn|zh|zh-cn|zh-tw|de|fr|es|pt|ru|ja|ko|id|vi|tr|it|ar|nl|pl)/',x['path'],re.I)}.values())
 substantive=[x for x in unique_docs if x['words']>=120 and not x['placeholder'] and sum(v>=1 for v in x['dimensions'].values())>=2 and not re.search(r'(?:changelog|release-notes|translations|locales)/|CHANGELOG',x['path'],re.I)]
 learning=[x for x in substantive if x['learning_path'] or x['dimensions']['curriculum']>=3 or x['dimensions']['onboarding']>=3]
 u['learningDocumentCount']=len(learning);u['learningWords']=sum(x['words'] for x in learning);u['placeholderDocuments']=sum(x.get('placeholder',False) for x in docs)
 u['dimensionDocuments']={k:sum(x['dimensions'][k]>=1 for x in learning) for k in DIM}
 u['learningRoots']=list(collections.Counter('/'.join(x['path'].split('/')[:next((i+1 for i,b in enumerate(x['path'].split('/')) if re.search(r'fable|upskill|curriculum|learning|onboarding|tutorial|bootcamp',b,re.I)),len(x['path'].split('/'))-1)]) for x in learning).keys())[:20]
 u['selectedDocuments']=sorted(learning,key=docscore,reverse=True)[:8]
 ep=tutorials.get(key,{}).get('entrypoint')
 if ep:
  match=next((x for x in docs if x['path']==ep),None)
  if match and match not in u['selectedDocuments']:u['selectedDocuments'].insert(0,match)
 if not u['selectedDocuments']:u['selectedDocuments']=sorted(docs,key=docscore,reverse=True)[:4]
 if not src:u['status']='Excluded — no application source'
 elif u['priorKind']=='learning-or-reference-collection' or key in ['antigravupskill','hermes']:u['status']='Excluded — reference or operating collection'
 elif len(src)<3 and u['sourceBytes']<10000:u['status']='Unclear — needs manual review'
 elif len(learning)>=4 and u['learningWords']>=4500 and all(u['dimensionDocuments'][k]>=1 for k in ['onboarding','architecture']) and all(u['dimensionDocuments'][k]>=2 for k in ['explanation','curriculum']) and u['dimensionDocuments']['workflow']>=1:u['status']='Substantially enhanced'
 elif len(learning)>=2 and u['learningWords']>=1200:u['status']='Partially enhanced'
 elif u['documentWords']>=200:u['status']='Minimal documentation'
 else:u['status']='Not enhanced'
 u['rating']='High' if u['status']=='Substantially enhanced' else 'Medium' if u['status']=='Partially enhanced' else 'Low'
 complexity=len(src)
 if key in ['JS1','newcodex3','newcodexJS','newcodecjs2','grokjs','groktuts','JSProjectLearn']:
  groups=collections.Counter('/'.join(f['path'][len(key)+1:].split('/')[:2 if key=='newcodex3' else 1]) for f in src);complexity=max(groups.values(),default=1);u['countingNote']='Coherent learning workspace counted once; nested applications are inspected as components, not added to the total.'
 u['complexitySourceFiles']=complexity
 dims=u['dimensionDocuments'];u['score']=round(min(25,5*math.log10(max(1,u['learningWords']/10)))+min(15,3*dims['onboarding'])+min(15,4*math.log10(max(1,complexity)))+min(15,3*dims['architecture'])+min(10,sum(v>=1 for v in dims.values())*1.67)+min(10,2*dims['explanation'])+min(10,2*dims['curriculum']),2)
 if u['status']=='Substantially enhanced' and u['learningWords']>=25000 and len(learning)>=18 and complexity>=150 and min(dims.values())>=4:u['rating']='Exceptional'
(O/'location-inventory.json').write_text(json.dumps(list(units.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(O/'unassigned-boundaries.json').write_text(json.dumps(unassigned,indent=2),encoding='utf-8')
print('Locations',len(units),'status',collections.Counter(x['status'] for x in units.values()),'unassigned',len(unassigned))
for u in sorted(units.values(),key=lambda u:u['score'],reverse=True)[:100]:print(f'{u["score"]:5.1f} {u["rating"]:11} {u["sourceFiles"]:6} {u["learningDocumentCount"]:4} {u["learningWords"]:8} {u["path"]}')
