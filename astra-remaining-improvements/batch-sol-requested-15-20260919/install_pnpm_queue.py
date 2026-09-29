"""Root-owned sequential dependency setup after the existing npm queue."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import time

B = Path(__file__).resolve().parent.parent
prior = Path(__file__).with_name('install_queue.json')
out = Path(__file__).with_suffix('.json')
state = {'status': 'waiting-for-npm', 'results': []}
def save():
    out.write_text(json.dumps(state, indent=2), encoding='utf-8')
save()
while json.loads(prior.read_text(encoding='utf-8'))['status'] not in ['complete', 'paused-low-disk']:
    time.sleep(3)
for project in ['a81b176807e5', '9d3b119f40a0']:
    if shutil.disk_usage(B).free < 4 * 1024**3:
        state.update(status='paused-low-disk', next=project)
        save()
        raise SystemExit('Dependency queue paused with less than 4 GiB free.')
    state.update(status='running', current=project)
    save()
    code = subprocess.call([
        sys.executable, str(B/'run_project_check.py'), '--env', 'HUSKY=0',
        project, 'astra-queued-pnpm-install-r1', '--', 'node',
        'C:/Program Files/nodejs/node_modules/corepack/dist/pnpm.js',
        'install', '--frozen-lockfile', '--reporter=append-only',
        '--network-concurrency=2', '--child-concurrency=1',
    ])
    state['results'].append({'id': project, 'exitCode': code})
    save()
state.update(status='complete')
save()
