"""Continue the planned checks after the corrected API test setup passes."""
from pathlib import Path
import json
import subprocess
import sys
import time

base = Path(__file__).resolve().parent.parent
previous = base / 'checks/3b9c30ec3ce2/astra-buildreviewer-api-tests-r4.json'
while not previous.exists() or json.loads(previous.read_text())['status'] == 'running':
    time.sleep(5)
if json.loads(previous.read_text()).get('exitCode') != 0:
    raise SystemExit('API check failed; review before continuing')
npm = ['node', 'C:/Program Files/nodejs/node_modules/npm/bin/npm-cli.js']
for label, args in [
    ('astra-buildreviewer-web-tests-r1', ['run', 'test', '-w', '@reviewdeck/web', '--', '--maxWorkers=1', '--minWorkers=1', '--testTimeout=60000', '--hookTimeout=60000']),
    ('astra-buildreviewer-typecheck-r1', ['run', 'typecheck']),
    ('astra-buildreviewer-build-r1', ['run', 'build']),
]:
    code = subprocess.call([sys.executable, str(base / 'run_project_check.py'),
        '3b9c30ec3ce2', label, '--', *npm, *args])
    if code != 0:
        raise SystemExit(code)
