from pathlib import Path
import json,os,subprocess,sys,time

checks=Path(__file__).resolve().parent
bundle=checks.parents[1]
stage=bundle/'stage/19110bf39fcf'
name=sys.argv[1]
output=checks/name
assert not output.exists(),output
command=[sys.executable,'verification/verify_browser.py']
env={**os.environ,'PYTHONIOENCODING':'utf-8','HELPDESK_BROWSER_OUTPUT':str(output),
     'ASTRA_BROWSER_EXECUTABLE':str(bundle/'playwright-browsers/chromium-1223/chrome-win64/chrome.exe')}
started=time.time()
with (checks/f'{name}.log').open('w',encoding='utf-8') as log:
    result=subprocess.run(command,cwd=stage,env=env,stdout=log,stderr=subprocess.STDOUT)
evidence={'command':command,'exitCode':result.returncode,'seconds':round(time.time()-started,2)}
(checks/f'{name}-execution.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print(json.dumps(evidence),flush=True)
print((checks/f'{name}.log').read_text(encoding='utf-8')[-14000:],flush=True)
raise SystemExit(result.returncode)
