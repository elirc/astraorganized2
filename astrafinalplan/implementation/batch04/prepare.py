from pathlib import Path
import os,json,hashlib,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path('C:/Users/Owner/Desktop');B=Path('astrafinalplan/implementation/batch04');B.mkdir(exist_ok=True)
names=['JS1/legal-case-tracker', 'JS1/subscription-billing', 'JS1/field-service', 'JS1/research-studies', 'JS1/warehouse-ledger', 'JS1/secure-notes', 'JS1/live-chat', 'newcodexJS/07-blog-platform', 'newcodexJS/08-kanban-board', 'newcodexJS/09-job-application-tracker', 'newcodexJS/10-inventory-management', 'newcodexJS/11-survey-builder', 'newcodexJS/12-chat-polling', 'newcodexJS/13-ecommerce-storefront', 'newcodexJS/14-appointment-booking', 'newcodexJS/15-api-tester', 'newcodexJS/16-team-project-management', 'newcodexJS/17-support-ticket-system', 'newcodexJS/18-learning-management-system', 'newcodexJS/19-realtime-chat-platform', 'newcodexJS/20-marketplace-platform', 'recipeview', 'calendar+jobtrack', 'devdeck', '_Organized Desktop/08 App And Product Projects/job track']; (B/'projects.json').write_text(json.dumps(names,indent=2),encoding='utf-8')
exclude={'node_modules','.git','dist','build','coverage','.next','.vite','data','.claude','.codex','.agents','fabledocs','fable-docs','docs','logs','.logs','astraupskill','backups','backup','archive','archives','original','vendor','content'}
base=[];inventory=[]
for i,name in enumerate(names,51):
 root=D/name;stage=B/'stage'/str(i)
 if (root/'.openai/hosting.json').exists():raise RuntimeError('Sites skill required '+name)
 for parent,dirs,files in os.walk(root):
  dirs[:]=[d for d in dirs if d not in exclude and not d.startswith('.')]
  for filename in files:
   p=Path(parent)/filename
   if filename=='AGENTS.md':raise RuntimeError('Read project instructions before continuing: '+str(p))
   if filename.startswith('.env') and filename!='.env.example':continue
   if p.suffix.lower() not in {'.js','.jsx','.ts','.tsx','.cjs','.mjs','.json','.html','.css','.md','.sql','.example','.svg','.yaml','.yml'}:continue
   rel=p.relative_to(root);target=stage/rel;target.parent.mkdir(parents=True,exist_ok=True)
   if target.exists():raise RuntimeError('Stage already exists: '+str(target))
   shutil.copyfile(p,target);base.append({'project':name,'stage':str(i),'file':rel.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 inventory.append(dict(project=name,stage=str(i),files=[x['file'] for x in base if x['stage']==str(i)]))
 print('STAGED',i,name,flush=True)
(B/'baseline.json').write_text(json.dumps(base,indent=2),encoding='utf-8');(B/'inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
j=json.loads(Path('astrafinalplan/project-plans.json').read_text(encoding='utf-8'));print('PLAN KEYS',list(j));print('Copied',len(base),'files')
