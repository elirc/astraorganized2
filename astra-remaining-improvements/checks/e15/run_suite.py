from pathlib import Path
import json, os, subprocess, sys, time

root=Path(__file__).resolve().parent
stage=root.parents[1]/'stage/19110bf39fcf'
name,*tests=sys.argv[1:]
out=root/name
out.mkdir(exist_ok=False)
command=[sys.executable,'-m','pytest',*tests,'-q','--basetemp',str(out/'pytest-temp'),
         '--junitxml',str(out/'results.xml')]
start=time.time()
with (out/'execution.log').open('w',encoding='utf-8') as log:
    result=subprocess.run(command,cwd=stage,stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONIOENCODING':'utf-8'})
evidence={'command':command,'exitCode':result.returncode,'seconds':round(time.time()-start,2)}
(out/'execution.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print(json.dumps(evidence),flush=True)
print((out/'execution.log').read_text(encoding='utf-8')[-12000:],flush=True)
raise SystemExit(result.returncode)
