from pathlib import Path
import json,os,subprocess,sys,time,zipfile

checks=Path(__file__).resolve().parent
bundle=checks.parents[1];stage=bundle/'stage/19110bf39fcf'
out=checks/'install-01';out.mkdir(exist_ok=False)
python=out/'.venv/Scripts/python.exe'
commands=[
    ('venv',[sys.executable,'-m','venv',str(out/'.venv')]),
    ('dependencies',[str(python),'-m','pip','install','--disable-pip-version-check','-r',str(stage/'requirements.lock')]),
    ('editable',[str(python),'-m','pip','install','--disable-pip-version-check','--no-deps','-e',str(stage)]),
    ('dependency-check',[str(python),'-m','pip','check']),
    ('wheel',[str(python),'-m','pip','wheel','--disable-pip-version-check','--no-deps','--wheel-dir',str(out/'wheels'),str(stage)]),
    ('smoke',[str(python),'-m','pytest','tests/test_contracts.py','tests/test_http_boundary.py','tests/test_reply_timers.py','-q',
              '--basetemp',str(out/'pytest-temp'),'--junitxml',str(out/'results.xml')]),
]
results=[]
for name,command in commands:
    start=time.time()
    with (out/f'{name}.log').open('w',encoding='utf-8') as log:
        result=subprocess.run(command,cwd=stage,env={**os.environ,'PYTHONIOENCODING':'utf-8','PIP_CACHE_DIR':str(bundle/'pip-cache')},stdout=log,stderr=subprocess.STDOUT)
    evidence={'name':name,'command':command,'exitCode':result.returncode,'seconds':round(time.time()-start,2)}
    results.append(evidence);(out/'execution.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(evidence),flush=True)
    if result.returncode:
        print((out/f'{name}.log').read_text(encoding='utf-8')[-12000:],flush=True);raise SystemExit(result.returncode)
wheel=next((out/'wheels').glob('*.whl'))
with zipfile.ZipFile(wheel) as archive:
    names=set(archive.namelist())
    for path in ['app/templates/index.html','app/templates/admin.html','app/templates/staff.html','app/templates/portal.html','app/templates/base.html','app/static/app.js','app/static/app.css']:
        assert path in names,path
(out/'package-check.json').write_text(json.dumps({'passed':True,'wheel':wheel.name,'templateAndStaticFiles':7},indent=2),encoding='utf-8')
print('Clean installation, dependency check, wheel assets and focused tests passed.',flush=True)
