"""Record sequential checks after each project's dependencies are installed."""
from pathlib import Path
import json
import subprocess
import sys
import time

B=Path(__file__).resolve().parent.parent
state={'status':'waiting','results':[]}
out=Path(__file__).with_suffix('.json')
npm=['node','C:/Program Files/nodejs/node_modules/npm/bin/npm-cli.js']
single=['--maxWorkers=1','--minWorkers=1','--testTimeout=30000']
jobs=[
 ('37844e1ec56d','astra-queued-install-r1',[
  ('astra-astra5-ui-tests-r1',npm+['run','test','--',*single]),
  ('astra-astra5-typecheck-r1',npm+['run','typecheck']),
 ]),
 ('af5130b3aad2','astra-queued-install-r1',[
  ('astra-buildevent-generate-r1',npm+['run','db:generate','-w','@ticketing/api']),
  ('astra-buildevent-api-tests-r1',npm+['run','test','-w','@ticketing/api','--',*single]),
  ('astra-buildevent-typecheck-r1',npm+['run','typecheck']),
 ]),
 ('3b9c30ec3ce2','astra-queued-install-r1',[
  ('astra-buildreviewer-shared-build-r1',npm+['run','build','-w','@reviewdeck/shared']),
  ('astra-buildreviewer-shared-tests-r1',npm+['run','test','-w','@reviewdeck/shared','--',*single]),
  ('astra-buildreviewer-api-tests-r1',npm+['run','test','-w','@reviewdeck/api','--','--testTimeout=60000']),
  ('astra-buildreviewer-web-tests-r1',npm+['run','test','-w','@reviewdeck/web','--',*single]),
  ('astra-buildreviewer-typecheck-r1',npm+['run','typecheck']),
 ]),
 ('a8435f7ed53c','astra-queued-install-r1',[
  ('astra-astra1-owned-check-r1',['python','scripts/test-owned-postgres.py','--mode','check']),
  ('astra-astra1-owned-api-r1',['python','scripts/test-owned-postgres.py','--mode','api']),
  ('astra-astra1-owned-browser-r1',['python','scripts/test-owned-postgres.py','--mode','browser']),
 ]),
]
def save():out.write_text(json.dumps(state,indent=2),encoding='utf-8')
save()
for project,install,checks in jobs:
    prerequisite=B/'checks'/project/(install+'.json')
    state.update(status='waiting-for-install',current=project)
    save()
    while not prerequisite.exists() or json.loads(prerequisite.read_text())['status']=='running':
        time.sleep(3)
    if json.loads(prerequisite.read_text()).get('exitCode')!=0:
        state['results'].append({'id':project,'status':'install-failed'})
        save()
        continue
    for label,command in checks:
        state.update(status='running',current=project,label=label)
        save()
        code=subprocess.call([sys.executable,str(B/'run_project_check.py'),
            '--env','PYTHONIOENCODING=utf-8','--env','NEXT_TELEMETRY_DISABLED=1',
            project,label,'--',*command])
        state['results'].append({'id':project,'label':label,'exitCode':code})
        save()
        if code!=0:break
state.update(status='complete')
save()
