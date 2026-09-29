"""Run API diagnostics after the active frontend check to limit load."""
from pathlib import Path
import json
import subprocess
import sys
import time

base = Path(__file__).resolve().parent.parent
previous = base / 'checks/5be7edf43612/astra-gitjira-web-shared-tests-r2.json'
while not previous.exists() or json.loads(previous.read_text())['status'] == 'running':
    time.sleep(5)
commands = [
    ('astra-gitjira-list-sprint-tests-r6', ['python', 'scripts/test-local.py', '--',
        'test/issue.test.js', 'test/sprint.test.js', '--maxWorkers=1',
        '--testTimeout=60000', '--hookTimeout=60000']),
    ('astra-gitjira-lint-r2', ['node', 'C:/Program Files/nodejs/node_modules/npm/bin/npm-cli.js', 'run', 'lint']),
]
for label, command in commands:
    code = subprocess.call([sys.executable, str(base / 'run_project_check.py'),
        '--env', 'PYTHONIOENCODING=utf-8', '5be7edf43612', label, '--', *command])
    if code != 0:
        raise SystemExit(code)
