from pathlib import Path
import subprocess,json,os,time,concurrent.futures,sys
B=Path(__file__).resolve().parent;H=B.parent
(B/'logs').mkdir(exist_ok=True)
env=os.environ.copy();env['ASTRA_TEST_DATABASE_URL']='postgres://astra:local-test@127.0.0.1:55439/astra_test_ten';env['TZ']='America/Los_Angeles';env['NO_COLOR']='1'
tasks=[]
for n in range(11,21):
 cwd=B/'stage'/str(n)
 if n in [11,12,13,15,16]:cmd=['node','--test',*map(str,(cwd/'test').glob('*.test.cjs'))]
 elif n in [14,17]:cmd=['node','--test',*map(str,(cwd/'test').glob('*.test.js'))]
 elif n==18:cmd=['node',str(H/'node_modules/tsx/dist/cli.mjs'),'--test',str(cwd/'test/booking.test.ts')]
 elif n==19:
  cwd=cwd/'server';cmd=['node','--test',str(cwd/'test/search.test.cjs')]
 else:
  cwd=cwd/'server';cmd=['node',str(H/'node_modules/tsx/dist/cli.mjs'),'--test',*map(str,(cwd/'test').glob('*.test.ts'))]
 tasks.append((str(n),'tests',cwd,cmd))
for n in [14,18,19,20]:
 cwd=B/'stage'/str(n)
 if n in [19,20]:cwd=cwd/'client'
 tasks.append((str(n),'build',cwd,['node',str(H/'node_modules/vite/bin/vite.js'),'build']))
for n,sub in [(18,''),(20,'server'),(20,'client')]:
 cwd=B/'stage'/str(n)/sub
 tasks.append((str(n),'typecheck'+('-'+sub if sub else ''),cwd,['node',str(H/'node_modules/typescript/bin/tsc'),'--noEmit']))
select=set(sys.argv[1:])
if select:tasks=[t for t in tasks if t[0] in select or t[0]+'-'+t[1] in select]
def run(task):
 n,kind,cwd,cmd=task;start=time.time();log=B/'logs'/f'{n}-{kind}.log'
 with log.open('w',encoding='utf-8') as output:
  try:code=subprocess.run(cmd,cwd=cwd,env=env,stdout=output,stderr=subprocess.STDOUT,timeout=600).returncode
  except subprocess.TimeoutExpired:code=124
 row=dict(project=n,check=kind,exit_code=code,seconds=round(time.time()-start,2),log=log.relative_to(B).as_posix(),command=cmd)
 print(json.dumps(row),flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,tasks))
p=B/'checks.json';old=json.loads(p.read_text()) if p.exists() else [];keys={(r['project'],r['check']) for r in results}
allrows=[r for r in old if (r['project'],r['check']) not in keys]+results;p.write_text(json.dumps(allrows,indent=2))
raise SystemExit(any(r['exit_code'] for r in results))
