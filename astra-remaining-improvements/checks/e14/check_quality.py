from pathlib import Path
import json,subprocess,time
C=Path(__file__).resolve().parent;S=C.parents[1]/'stage/ca549816cdd1'
ruff='C:/Users/Owner/AppData/Roaming/Python/Python313/Scripts/ruff.exe'
commands=[[ruff,'check','app','tests','scripts'],[ruff,'format','--check','app','tests','scripts'],['node','--check','app/web/app.js']]
results=[]
for index,command in enumerate(commands):
    started=time.time()
    result=subprocess.run(command,cwd=S,capture_output=True,text=True,encoding='utf-8')
    (C/f'quality-final-{index}.log').write_text(result.stdout+result.stderr,encoding='utf-8')
    results.append({'command':command,'exitCode':result.returncode,'seconds':round(time.time()-started,2)})
evidence={'passed':all(item['exitCode']==0 for item in results),'commands':results}
(C/'quality-final.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print(json.dumps(evidence))
assert evidence['passed']
