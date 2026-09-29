"""Run remaining checks after the owned SQLite regression succeeds."""
from pathlib import Path
import json
import subprocess
import sys
import time

base = Path(__file__).resolve().parent.parent
previous = base / 'checks/9d3b119f40a0/astra-skillforge-completion-r4.json'
while not previous.exists() or json.loads(previous.read_text())['status'] == 'running':
    time.sleep(5)
if json.loads(previous.read_text()).get('exitCode') != 0:
    raise SystemExit('Owned SQLite check failed; review before continuing')
pnpm = ['node', 'C:/Program Files/nodejs/node_modules/corepack/dist/pnpm.js']
for label, args in [
    ('astra-skillforge-tests-r2', ['run', 'test', '--maxWorkers=1', '--minWorkers=1', '--testTimeout=60000', '--hookTimeout=60000']),
    ('astra-skillforge-typecheck-r1', ['run', 'typecheck']),
]:
    code = subprocess.call([sys.executable, str(base / 'run_project_check.py'),
        '9d3b119f40a0', label, '--', *pnpm, *args])
    if code:
        raise SystemExit(code)
