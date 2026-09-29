"""Sequential dependency setup for the root-only continuation (no agent delegation)."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import time

B = Path(__file__).resolve().parent.parent
prerequisite = B/'checks/1bf7dd59f47b/astra-mobile-install-r2.json'
state_file = Path(__file__).with_suffix('.json')
state = {'status': 'waiting', 'after': str(prerequisite), 'results': []}
def save():
    state_file.write_text(json.dumps(state, indent=2), encoding='utf-8')
save()
while json.loads(prerequisite.read_text(encoding='utf-8'))['status'] == 'running':
    time.sleep(3)
for project in ['37844e1ec56d', 'af5130b3aad2', '3b9c30ec3ce2', 'a8435f7ed53c']:
    if shutil.disk_usage(B).free < 4 * 1024**3:
        state.update(status='paused-low-disk', next=project)
        save()
        raise SystemExit('Dependency queue paused with less than 4 GiB free.')
    state.update(status='running', current=project)
    save()
    code = subprocess.call([
        sys.executable, str(B/'run_project_check.py'),
        '--env', 'HUSKY=0', '--env', 'npm_config_cache='+str(B/'npm-cache'),
        project, 'astra-queued-install-r1', '--',
        'node', 'C:/Program Files/nodejs/node_modules/npm/bin/npm-cli.js',
        'ci', '--prefer-offline', '--no-audit', '--no-fund', '--fetch-retries=1',
        '--fetch-timeout=20000', '--maxsockets=2', '--loglevel=verbose',
    ])
    state['results'].append({'id': project, 'exitCode': code})
    save()
state.update(status='complete')
save()
