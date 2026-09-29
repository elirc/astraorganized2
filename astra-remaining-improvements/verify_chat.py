from pathlib import Path
import json,subprocess,re
B=Path(__file__).resolve().parent;S=B/'stage'/'22be3051241f';out=B/'checks'/'chat';out.mkdir(parents=True,exist_ok=True)
checks=[]
for name,cwd,command in [('socket',S,['npm.cmd','test','--','--test-reporter=tap']),('web-build',S/'client',['npm.cmd','run','build'])]:
 r=subprocess.run(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace');(out/(name+'.log')).write_text(r.stdout,encoding='utf-8');print(r.stdout[-6500:],flush=True);assert r.returncode==0
 checks.append({'name':name,'command':command,'exitCode':r.returncode,'log':'checks/chat/'+name+'.log'})
 if name=='socket':
  count=int(re.search(r'^# tests (\d+)',r.stdout,re.M)[1]);passed=int(re.search(r'^# pass (\d+)',r.stdout,re.M)[1]);assert count==passed==13
(out/'results.json').write_text(json.dumps({'passed':True,'tests':count,'checks':checks,'initialRegressionRun':{'tests':6,'failed':6,'note':'After adding isolated database option, before business fixes'},'scope':'Real Socket.IO server/client connections and SQLite memory database; React production build; no live browser, upload or REST endpoint verification'},indent=2),encoding='utf-8')
