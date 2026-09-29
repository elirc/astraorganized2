from pathlib import Path
import subprocess,json,time,sys
sys.stdout.reconfigure(encoding='utf-8')
c=Path(__file__).resolve().parent;s=c.parents[1]/'stage/58c5c289a8ce'
name=sys.argv[1];kind=sys.argv[2];assert name.replace('-','').isalnum()
commands={'lint':['node','node_modules/eslint/bin/eslint.js','src','scripts','test'],'build':['node','node_modules/next/dist/bin/next','build']}
assert kind in commands and not (c/(name+'.json')).exists()
started=time.time()
with (c/(name+'.log')).open('w',encoding='utf-8') as log:r=subprocess.run(commands[kind],cwd=s,stdout=log,stderr=subprocess.STDOUT)
result={'command':commands[kind],'exitCode':r.returncode,'seconds':round(time.time()-started,2)}
(c/(name+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True);print((c/(name+'.log')).read_text(encoding='utf-8')[-16000:],flush=True);sys.exit(r.returncode)
