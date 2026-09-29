from pathlib import Path
import os,subprocess,json,time,concurrent.futures,sys
BASE=Path(__file__).resolve().parent
LOGS=BASE/'logs';LOGS.mkdir(exist_ok=True)
env=os.environ.copy()
env['ASTRA_TEST_DATABASE_URL']='postgres://astra:local-test@127.0.0.1:55439/astra_test_ten'
env['CI']='1';env['NO_COLOR']='1';env['FORCE_COLOR']='0'
binary=Path('C:/Program Files/PostgreSQL/18/bin')
result=subprocess.run([str(binary/'psql.exe'),'-h','127.0.0.1','-p','55439','-U','astra','-d','postgres','-Atc',"SELECT 1 FROM pg_database WHERE datname='astra_test_ten'"],capture_output=True,text=True)
if result.returncode: print(result.stderr);raise SystemExit(result.returncode)
if not result.stdout.strip():subprocess.run([str(binary/'createdb.exe'),'-h','127.0.0.1','-p','55439','-U','astra','astra_test_ten'],check=True)
tasks=[]
for i in range(1,11):
 n=f'{i:02}';cwd=BASE/'stage'/n
 if i<=4:cmd=['node','--test',*map(str,(cwd/'test').glob('*.test.cjs'))]
 elif i==5:cmd=['node',str(BASE/'node_modules/tsx/dist/cli.mjs'),'--test',str(cwd/'test/shopping-state.test.ts')]
 elif i==6:cmd=['node',str(BASE/'node_modules/vitest/vitest.mjs'),'run','--maxWorkers=2']
 elif i<10:
  cwd=cwd/'server';cmd=['node','--test',*map(str,(cwd/'test').glob('*.test.cjs'))]
 else:
  cwd=cwd/'server';cmd=['node',str(BASE/'node_modules/tsx/dist/cli.mjs'),'--test',str(cwd/'test/ownership.test.ts')]
 tasks.append((n,'tests',cwd,cmd))
for n in ['05','06','07','08','09','10']:
 cwd=BASE/'stage'/n
 if int(n)>=7:cwd=cwd/'client'
 if n=='05':cmd=['npm.cmd','run','build']
 else:cmd=['node',str(BASE/'node_modules/vite/bin/vite.js'),'build']
 tasks.append((n,'build',cwd,cmd))
tasks.append(('10','server-typecheck',BASE/'stage/10/server',['node',str(BASE/'node_modules/typescript/bin/tsc'),'--noEmit']))
tasks.append(('10','client-typecheck',BASE/'stage/10/client',['node',str(BASE/'node_modules/typescript/bin/tsc'),'--noEmit']))
tasks.append(('05','lint',BASE/'stage/05',['npm.cmd','run','lint']))
selected=set(sys.argv[1:])
if selected:tasks=[t for t in tasks if t[0] in selected or t[0]+'-'+t[1] in selected]
def run(task):
 n,kind,cwd,cmd=task;start=time.time()
 path=LOGS/f'{n}-{kind}.log'
 with path.open('w',encoding='utf-8') as log:
  try:result=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=900 if n=='06' and kind=='tests' else 300);code=result.returncode
  except subprocess.TimeoutExpired:code=124
 item={'project':n,'check':kind,'exit_code':code,'seconds':round(time.time()-start,2),'log':path.relative_to(BASE).as_posix(),'command':cmd}
 print(json.dumps(item),flush=True);return item
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,tasks))
previous=json.loads((BASE/'checks.json').read_text()) if (BASE/'checks.json').exists() else []
keys={(r['project'],r['check']) for r in results}
results=[r for r in previous if (r['project'],r['check']) not in keys]+results
(BASE/'checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
raise SystemExit(any(r['exit_code'] for r in results))
