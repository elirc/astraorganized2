"""Sequential root-owned validation after dependency installation."""
from pathlib import Path
import json
import subprocess
import sys
import time

base = Path(__file__).resolve().parent.parent
out = Path(__file__).with_suffix('.json')
state = {'status': 'waiting', 'results': []}
pnpm = ['node', 'C:/Program Files/nodejs/node_modules/corepack/dist/pnpm.js']
jobs = [
    ('a81b176807e5', [
        ('astra-buildermentor-tests-r1', pnpm + ['--filter', '@shipshape/api', 'test', '--maxWorkers=1', '--minWorkers=1', '--testTimeout=60000', '--hookTimeout=60000']),
        ('astra-buildermentor-typecheck-r1', pnpm + ['-r', '--workspace-concurrency=1', 'typecheck']),
    ]),
    ('9d3b119f40a0', [
        ('astra-skillforge-generate-r1', pnpm + ['db:generate']),
        ('astra-skillforge-completion-r1', ['node', 'scripts/test-completion-local.mjs']),
        ('astra-skillforge-tests-r1', pnpm + ['test', '--maxWorkers=1', '--minWorkers=1', '--testTimeout=60000', '--hookTimeout=60000']),
        ('astra-skillforge-typecheck-r1', pnpm + ['typecheck']),
    ]),
]

def save():
    out.write_text(json.dumps(state, indent=2), encoding='utf-8')

for project, checks in jobs:
    prerequisite = base / 'checks' / project / 'astra-queued-pnpm-install-r1.json'
    state.update(status='waiting-for-install', current=project)
    save()
    while not prerequisite.exists() or json.loads(prerequisite.read_text())['status'] == 'running':
        time.sleep(5)
    if json.loads(prerequisite.read_text()).get('exitCode') != 0:
        state['results'].append({'id': project, 'status': 'install-failed'})
        save()
        continue
    for label, command in checks:
        state.update(status='running', label=label)
        save()
        code = subprocess.call([sys.executable, str(base / 'run_project_check.py'),
            '--env', 'HUSKY=0', '--env', 'NEXT_TELEMETRY_DISABLED=1', project, label, '--', *command])
        state['results'].append({'id': project, 'label': label, 'exitCode': code})
        save()
        if code != 0:
            break
state['status'] = 'complete'
save()
