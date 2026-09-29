from pathlib import Path
import os,json,hashlib,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path('C:/Users/Owner/Desktop');B=Path('astrafinalplan/implementation/batch02');B.mkdir(exist_ok=True)
names=['JS1/flashcards','JS1/habit-tracker','JS1/reading-list','JS1/note-vault','JS1/budget-tracker','JS1/pantry-inventory','JS1/snippet-vault','JS1/room-booking','newcodexJS/04-notes-app','newcodexJS/06-bookmark-manager']
(B/'projects.json').write_text(json.dumps(names,indent=2))
exclude={'node_modules','.git','dist','build','coverage','.next','.vite','data','.claude','.codex','.agents','fabledocs','fable-docs','docs','logs','.logs','astraupskill'}
base=[]
for i,name in enumerate(names,11):
 root=D/name;stage=B/'stage'/str(i)
 for parent,dirs,files in os.walk(root):
  dirs[:]=[d for d in dirs if d not in exclude and not d.startswith('.')]
  for filename in files:
   p=Path(parent)/filename
   if filename=='AGENTS.md':print('INSTRUCTIONS',p,p.read_text(encoding='utf-8'))
   if filename.startswith('.env') and filename!='.env.example':continue
   if p.suffix.lower() not in {'.js','.jsx','.ts','.tsx','.cjs','.mjs','.json','.html','.css','.md','.sql','.example'}:continue
   rel=p.relative_to(root);target=stage/rel;target.parent.mkdir(parents=True,exist_ok=True)
   if target.exists():raise RuntimeError('Stage already exists: '+str(target))
   shutil.copyfile(p,target);base.append({'project':name,'stage':str(i),'file':rel.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 print('STAGED',i,name,[(x.name,x.stat().st_size) for x in root.iterdir() if x.is_file()])
 if i>=18:print((root/'README.md').read_text(encoding='utf-8'))
 if (root/'.openai/hosting.json').exists():print('SITES',name)
(B/'baseline.json').write_text(json.dumps(base,indent=2))
plans=json.loads(Path('astrafinalplan/project-plans.json').read_text())['plans']
for p in plans:
 if p['path'] in names:print('PLAN',json.dumps(p))
print('Copied',len(base),'files')
