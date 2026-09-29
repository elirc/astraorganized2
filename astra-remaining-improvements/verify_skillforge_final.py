from pathlib import Path
import subprocess,json,time
b=Path(__file__).resolve().parent;s=b/'stage/a9672affc47e';out=b/'checks/skillforge/final';out.mkdir(parents=True,exist_ok=True)
steps=[('model',['node','node_modules/vitest/vitest.mjs','run','src','--reporter=json','--outputFile='+str(out/'model.json')]),('build',['cmd','/c','npm','run','build']),('archive',['node','scripts/verify-content.mjs'])]
results=[]
for name,args in steps:
 start=time.time();r=subprocess.run(args,cwd=s,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace');(out/(name+'.log')).write_text(r.stdout,encoding='utf-8');results.append({'name':name,'exitCode':r.returncode,'seconds':round(time.time()-start,2)});print(name,r.returncode,flush=True)
 if r.returncode:print(r.stdout[-3500:],flush=True);break
(out/'commands.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
raise SystemExit(any(r['exitCode'] for r in results))
