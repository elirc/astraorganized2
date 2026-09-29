from pathlib import Path
import json,os,subprocess,sys,time

checks=Path(__file__).resolve().parent;bundle=checks.parents[1];stage=bundle/'stage/19110bf39fcf'
env={**os.environ,'PYTHONIOENCODING':'utf-8',
     'ASTRA_BROWSER_EXECUTABLE':str(bundle/'playwright-browsers/chromium-1223/chrome-win64/chrome.exe'),
     'HELPDESK_RENDER_OUTPUT':str(checks/'rendering-02'),
     'HELPDESK_BROWSER_OUTPUT':str(checks/'browser-04')}
for name,script in [('rendering-02','verification/verify_rendering.py'),('browser-04','verification/verify_browser.py')]:
    assert not (checks/name).exists(),name
    command=[sys.executable,script];start=time.time()
    with (checks/f'{name}.log').open('w',encoding='utf-8') as log:
        result=subprocess.run(command,cwd=stage,env=env,stdout=log,stderr=subprocess.STDOUT)
    evidence={'command':command,'exitCode':result.returncode,'seconds':round(time.time()-start,2)}
    (checks/f'{name}-execution.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    print(json.dumps(evidence),flush=True)
    print((checks/f'{name}.log').read_text(encoding='utf-8')[-12000:],flush=True)
    if result.returncode:raise SystemExit(result.returncode)
