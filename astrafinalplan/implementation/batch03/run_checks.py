from pathlib import Path
import subprocess,json,os,time,concurrent.futures,sys
B=Path(__file__).resolve().parent;H=B.parent
(B/'logs').mkdir(exist_ok=True)
env=os.environ.copy();env['ASTRA_TEST_DATABASE_URL']='postgres://astra:local-test@127.0.0.1:55439/astra_test_ten';env['TZ']='America/Los_Angeles';env['NO_COLOR']='1'
tasks=[]
TS=['28', '30', '31', '33', '34', '35', '41', '43', '44', '47', '49', '50']
for n in range(21,51):
 cwd=B/'stage'/str(n)
 pattern='*.test.ts' if str(n) in TS else '*.test.cjs' if n in [21,22] else '*.test.js'
 files=list((cwd/'test').glob(pattern))
 if files:
  cmd=['node',str(H/'node_modules/tsx/dist/cli.mjs'),'--test',*map(str,files)] if str(n) in TS else ['node','--test',*map(str,files)]
  tasks.append((str(n),'tests',cwd,cmd))
 if n>=23:tasks.append((str(n),'build',cwd,['node',str(H/'node_modules/vite/bin/vite.js'),'build']))
 if str(n) in TS:tasks.append((str(n),'typecheck',cwd,['node',str(H/'node_modules/typescript/bin/tsc'),'--noEmit']))
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
