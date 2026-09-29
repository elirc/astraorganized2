from pathlib import Path
import json, os, subprocess, time
B=Path(__file__).resolve().parents[2]
S=B/'stage/077627a58eae'
C=Path(__file__).resolve().parent
marker=C/'build-02-execution.json'
deadline=time.time()+1800
while not marker.exists():
    if time.time()>deadline:raise SystemExit('Build remains incomplete; browser verification has not started.')
    time.sleep(2)
assert json.loads(marker.read_text(encoding='utf-8'))['exitCode']==0
assert not (C/'browser-02-execution.json').exists()
env={**os.environ,'LOCALOPS_BROWSER_OUTPUT':str(C/'browser-02'),'ASTRA_BROWSER_EXECUTABLE':str(B/'playwright-browsers/chromium-1223/chrome-win64/chrome.exe'),'PYTHONIOENCODING':'utf-8'}
command=['python','scripts/verify_browser.py'];start=time.time()
with (C/'browser-02-execution.log').open('w',encoding='utf-8') as log:result=subprocess.run(command,cwd=S,env=env,stdout=log,stderr=subprocess.STDOUT)
e={'command':command,'exitCode':result.returncode,'seconds':round(time.time()-start,2)}
(C/'browser-02-execution.json').write_text(json.dumps(e,indent=2),encoding='utf-8')
print(json.dumps(e));print((C/'browser-02-execution.log').read_text(encoding='utf-8')[-15000:])
raise SystemExit(result.returncode)
