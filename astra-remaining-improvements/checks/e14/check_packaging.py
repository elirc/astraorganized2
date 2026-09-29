from pathlib import Path
import json
import os
import subprocess
import sys
import time
import zipfile

C=Path(__file__).resolve().parent;S=C.parents[1]/'stage/ca549816cdd1'
name=sys.argv[1] if len(sys.argv)>1 else 'package-01'
assert name.replace('-','').isalnum()
output=C/name;output.mkdir(exist_ok=False)
checks=[];start=time.time()


def run(name,args,cwd=S,env=None):
    with (output/(name+'.log')).open('w',encoding='utf-8') as log:
        result=subprocess.run(args,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:raise RuntimeError(name+' failed; inspect its log')


try:
    run('build',[sys.executable,'-m','pip','wheel','--no-deps','--wheel-dir',str(output/'wheel'),'.'])
    wheels=list((output/'wheel').glob('*.whl'));assert len(wheels)==1
    checks.append('Build distributable wheel with pinned build dependencies')
    with zipfile.ZipFile(wheels[0]) as archive:
        for path in ['app/web/index.html','app/web/styles.css','app/web/app.js','app/crud.py','app/services/notification_outbox.py']:
            assert archive.read(path)==(S/path).read_bytes(),path
        assert not any(name.endswith(('.db','.sqlite','.env')) for name in archive.namelist())
    checks.append('Wheel contains current application and browser assets without database or environment files')
    installed=output/'installed'
    run('install',[sys.executable,'-m','pip','install','--no-index','--no-deps','--target',str(installed),str(wheels[0])])
    checks.append('Install wheel into a separate directory without an editable source checkout')
    probe=output/'probe.py'
    probe.write_text('''from pathlib import Path
import tempfile
import app
from app.api import create_app
from app.config import Settings
from fastapi.testclient import TestClient
assert Path(app.__file__).resolve().is_relative_to(Path(__file__).parent / 'installed')
with tempfile.TemporaryDirectory(prefix='e14-installed-') as temporary:
    directory=Path(temporary)
    cfg=Settings('sqlite:///'+str(directory/'installed.db'),directory,100,1000,1000,1048576,600,testing=True)
    with TestClient(create_app(cfg)) as client:
        assert client.get('/').status_code==200
        assert client.get('/assets/app.js').status_code==200
        setup=client.post('/api/v1/setup/bootstrap',json={'org_name':'Installed','org_slug':'installed','email':'installed@example.com','password':'installed-password','display_name':'Installed learner'})
        assert setup.status_code==200,setup.text
        token=setup.json()['token']
        result=client.post('/api/v1/dashboards',headers={'Authorization':'Bearer '+token},json={'name':'Installed dashboard'})
        assert result.status_code==200 and result.json()['version']==1
print('Installed application serves assets and persists authenticated CRUD on a fresh temporary database')
''',encoding='utf-8')
    env=os.environ.copy();env['PYTHONPATH']=str(installed);env['PYTHONIOENCODING']='utf-8'
    run('probe',[sys.executable,str(probe)],cwd=output,env=env)
    checks.append('Installed application imports from wheel, serves assets and persists authenticated CRUD')
    passed=True
finally:
    evidence={'passed':len(checks)==4,'checks':checks,'seconds':round(time.time()-start,2)}
    (output/'result.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    print(json.dumps(evidence),flush=True)
