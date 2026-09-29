from pathlib import Path
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
checks=Path(__file__).resolve().parent
stage=checks.parents[1]/'stage/71e7b036865c'
name,relative,*command=sys.argv[1:]
assert name.replace('-','').isalnum() and not (checks/(name+'.json')).exists()
working=(stage/relative).resolve()
assert working.is_relative_to(stage.resolve())
env=os.environ.copy()
env.update({'DOTNET_CLI_TELEMETRY_OPTOUT':'1','DOTNET_NOLOGO':'1','PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8'})
start=time.monotonic()
with (checks/(name+'.log')).open('w',encoding='utf-8') as log:
    run=subprocess.run(command,cwd=working,env=env,stdout=log,stderr=subprocess.STDOUT)
result={'command':command,'workingDirectory':relative,'exitCode':run.returncode,'seconds':round(time.monotonic()-start,2)}
(checks/(name+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
print((checks/(name+'.log')).read_text(encoding='utf-8',errors='replace')[-10000:],flush=True)
sys.exit(run.returncode)
