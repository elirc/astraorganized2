from pathlib import Path
import json,subprocess,re
B=Path(__file__).resolve().parent;S=B/'stage'/'19856a4178bf';out=B/'checks'/'task-queue';out.mkdir(parents=True,exist_ok=True)
checks=[]
for p in (S/'server'/'src').rglob('*.js'):
 r=subprocess.run(['node','--check',str(p)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace');assert r.returncode==0,(p,r.stdout)
checks.append({'name':'server-syntax','passed':True})
for name,cwd,command in [('api-outbox',S/'server',['npm.cmd','test','--','--test-reporter=tap']),('web-build',S/'client',['npm.cmd','run','build'])]:
 r=subprocess.run(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace');(out/(name+'.log')).write_text(r.stdout,encoding='utf-8');print(r.stdout[-10000:],flush=True);assert r.returncode==0
 checks.append({'name':name,'command':command,'exitCode':r.returncode,'log':'checks/task-queue/'+name+'.log'})
 if name=='api-outbox':
  count=int(re.search(r'^# tests (\d+)',r.stdout,re.M)[1]);passed=int(re.search(r'^# pass (\d+)',r.stdout,re.M)[1]);assert count==passed==19
(out/'results.json').write_text(json.dumps({'passed':True,'tests':count,'checks':checks,'initialRegressionRun':{'tests':2,'failed':2,'note':'After database isolation/schema and router factory, before business fixes'},'scope':'Real HTTP and SQLite, controlled queue responses, separate-process file persistence, server syntax, React build. Redis/BullMQ worker execution and live browser not verified; Docker daemon unavailable.'},indent=2),encoding='utf-8')
