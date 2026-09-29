"""Temporarily increase only Vitest worker startup limits on this constrained host."""
from pathlib import Path
import json
import subprocess
import sys
import time

base = Path(__file__).resolve().parent.parent
previous = base / 'checks/5be7edf43612/astra-gitjira-list-sprint-tests-r6.json'
while not previous.exists() or json.loads(previous.read_text())['status'] == 'running':
    time.sleep(5)
project = base / 'stage/5be7edf43612'
runner = project / 'node_modules/vitest/dist/chunks/cli-api.BK8pd4xc.js'
original = runner.read_bytes()
assert original.count(b'const START_TIMEOUT = 6e4;') == 1
assert original.count(b'const WORKER_START_TIMEOUT = 9e4;') == 1
modified = original.replace(b'const START_TIMEOUT = 6e4;', b'const START_TIMEOUT = 3e5;').replace(
    b'const WORKER_START_TIMEOUT = 9e4;', b'const WORKER_START_TIMEOUT = 33e4;')
print('Local-only Vitest worker startup allowance: 300s / 330s; assertions and test timeouts unchanged.', flush=True)
try:
    runner.write_bytes(modified)
    code = subprocess.call([sys.executable, str(base / 'run_project_check.py'),
        '5be7edf43612', 'astra-gitjira-web-shared-tests-r4', '--',
        'node', 'C:/Program Files/nodejs/node_modules/npm/bin/npm-cli.js', 'run', 'test',
        '-w', '@gitjira/web', '-w', '@gitjira/shared', '--', '--maxWorkers=1',
        '--testTimeout=60000', '--hookTimeout=60000'])
finally:
    assert runner.read_bytes() == modified, 'Runner changed concurrently; review before restoration'
    runner.write_bytes(original)
    assert runner.read_bytes() == original
    print('Original dependency bytes restored.', flush=True)
raise SystemExit(code)
