from pathlib import Path
import json,subprocess,re
B=Path(__file__).resolve().parent;S=B/'stage'/'e2d8f836b7f9';out=B/'checks'/'kds';out.mkdir(parents=True,exist_ok=True)
results=[]
for name,cwd,command in [('api',S/'server',['npm.cmd','test','--','--test-reporter=tap']),('web-build',S/'client',['npm.cmd','run','build'])]:
 r=subprocess.run(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
 (out/(name+'.log')).write_text(r.stdout,encoding='utf-8');results.append({'name':name,'command':command,'exitCode':r.returncode,'log':'checks/kds/'+name+'.log'})
 print(r.stdout[-5500:],flush=True)
 if r.returncode:raise SystemExit(r.returncode)
 if name=='api':
  tests=int(re.search(r'^# tests (\d+)',r.stdout,re.M)[1]);passed=int(re.search(r'^# pass (\d+)',r.stdout,re.M)[1]);assert tests==passed==12
(out/'results.json').write_text(json.dumps({'passed':True,'tests':tests,'checks':results,'initialRegressionRun':{'tests':11,'passed':3,'failed':8,'note':'After adding isolated database and app factory, before business fixes'},'scope':'Real HTTP and in-memory SQLite; React production build; no live browser or persistent-file restart test'},indent=2),encoding='utf-8')
print('Kitchen checks passed',flush=True)
