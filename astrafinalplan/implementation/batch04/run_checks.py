from pathlib import Path
import subprocess,json,os,time,concurrent.futures,sys
B=Path(__file__).resolve().parent;H=B.parent
(B/'logs').mkdir(exist_ok=True)
env=os.environ.copy();env['ASTRA_TEST_DATABASE_URL']='postgres://astra:local-test@127.0.0.1:55439/astra_test_ten';env['TZ']='America/Los_Angeles';env['NO_COLOR']='1'
tasks=[]
for n in range(51,76):
 root=B/'stage'/str(n)
 files=[* (root/'test').glob('*.test.ts'),*(root/'test').glob('*.test.js')]
 if n in (73,74):tasks.append((str(n),'tests',root,['node',str(root/'node_modules/vitest/vitest.mjs'),'run']))
 if files:tasks.append((str(n),'tests',root,['node',str(H/'node_modules/tsx/dist/cli.mjs'),'--test',*map(str,files)]))
 if 58<=n<=71:tasks.append((str(n),'server-build',root/'server',['node',str(H/'node_modules/typescript/bin/tsc'),'-p','tsconfig.json']))
 client=root/'client' if 58<=n<=71 or n==75 else root
 tasks.append((str(n),'build',client,['node',str((root if n in (73,74) else H)/'node_modules/vite/bin/vite.js'),'build']))
 for label,config in [('typecheck',root/'tsconfig.json'),('client-typecheck',root/'client/tsconfig.json'),('server-typecheck',root/'server/tsconfig.json')]:
  if config.exists():tasks.append((str(n),label,root,['node',str((root if n in (73,74) else H)/'node_modules/typescript/bin/tsc'),*(['-b','--noEmit'] if n in (73,74) and label=='typecheck' else ['--noEmit','-p',str(config)])]))
args=sys.argv[1:];output_name='checks.json'
if args and args[0].startswith('--output='):output_name=args.pop(0).split('=',1)[1]
select=set(args)
if select:tasks=[t for t in tasks if t[0] in select or t[0]+'-'+t[1] in select]
def run(task):
 n,kind,cwd,cmd=task;start=time.time();log=B/'logs'/f'{n}-{kind}.log'
 with log.open('w',encoding='utf-8') as output:
  try:code=subprocess.run(cmd,cwd=cwd,env=env,stdout=output,stderr=subprocess.STDOUT,timeout=600).returncode
  except subprocess.TimeoutExpired:code=124
 row=dict(project=n,check=kind,exit_code=code,seconds=round(time.time()-start,2),log=log.relative_to(B).as_posix(),command=cmd)
 print(json.dumps(row),flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,tasks))
p=B/output_name;old=json.loads(p.read_text()) if p.exists() else [];keys={(r['project'],r['check']) for r in results}
allrows=[r for r in old if (r['project'],r['check']) not in keys]+results;p.write_text(json.dumps(allrows,indent=2))
raise SystemExit(any(r['exit_code'] for r in results))
