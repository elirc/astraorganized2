from pathlib import Path
import os,json,hashlib,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path('C:/Users/Owner/Desktop');B=Path('astrafinalplan/implementation/batch03');B.mkdir(exist_ok=True)
slugs=['poll-studio','kanban-flow','course-roster','event-admin','job-pipeline','stock-catalog','recipe-studio','org-explorer','mini-blog','pulse-analytics','support-tickets','issue-desk','forum-search','invoice-studio','asset-checkout','equipment-maintenance','library-lending','gym-membership','campaign-planner','volunteer-coordinator','learning-paths','project-risks','travel-requests','vendor-contracts','procurement-portal','property-rentals','quality-audits','patient-intake','grant-manager','incident-response']
names=['JS1/'+n for n in slugs];(B/'projects.json').write_text(json.dumps(names,indent=2),encoding='utf-8')
exclude={'node_modules','.git','dist','build','coverage','.next','.vite','data','.claude','.codex','.agents','fabledocs','fable-docs','docs','logs','.logs','astraupskill'}
base=[];inventory=[]
for i,name in enumerate(names,21):
 root=D/name;stage=B/'stage'/str(i)
 if (root/'.openai/hosting.json').exists():raise RuntimeError('Sites skill required '+name)
 for parent,dirs,files in os.walk(root):
  dirs[:]=[d for d in dirs if d not in exclude and not d.startswith('.')]
  for filename in files:
   p=Path(parent)/filename
   if filename=='AGENTS.md':raise RuntimeError('Read project instructions before continuing: '+str(p))
   if filename.startswith('.env') and filename!='.env.example':continue
   if p.suffix.lower() not in {'.js','.jsx','.ts','.tsx','.cjs','.mjs','.json','.html','.css','.md','.sql','.example','.svg'}:continue
   rel=p.relative_to(root);target=stage/rel;target.parent.mkdir(parents=True,exist_ok=True)
   if target.exists():raise RuntimeError('Stage already exists: '+str(target))
   shutil.copyfile(p,target);base.append({'project':name,'stage':str(i),'file':rel.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 inventory.append(dict(project=name,stage=str(i),files=[x['file'] for x in base if x['stage']==str(i)]))
 print('STAGED',i,name,flush=True)
(B/'baseline.json').write_text(json.dumps(base,indent=2),encoding='utf-8');(B/'inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
j=json.loads(Path('astrafinalplan/project-plans.json').read_text(encoding='utf-8'));print('PLAN KEYS',list(j));print('Copied',len(base),'files')
