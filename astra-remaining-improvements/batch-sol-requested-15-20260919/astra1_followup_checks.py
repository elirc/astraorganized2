"""Run the corrected owned database check and its dependent smoke checks."""
from pathlib import Path
import json
import subprocess
import sys
import time

base = Path(__file__).resolve().parent.parent
previous = base / 'checks/a8435f7ed53c/astra-astra1-owned-check-r1.json'
while json.loads(previous.read_text())['status'] == 'running':
    time.sleep(5)
for label, mode in [('astra-astra1-owned-check-r2', 'check'),
                    ('astra-astra1-owned-api-r1', 'api'),
                    ('astra-astra1-owned-browser-r1', 'browser')]:
    code = subprocess.call([sys.executable, str(base / 'run_project_check.py'),
        '--env', 'PYTHONIOENCODING=utf-8', '--env', 'NEXT_TELEMETRY_DISABLED=1',
        'a8435f7ed53c', label, '--', sys.executable,
        'scripts/test-owned-postgres.py', '--mode', mode])
    if code:
        raise SystemExit(code)
