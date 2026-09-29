from pathlib import Path
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
