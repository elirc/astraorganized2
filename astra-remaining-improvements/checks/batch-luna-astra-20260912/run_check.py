"""Capture a long-running check; tool yields are not command completion."""
from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess
import sys
import time

project, label, *command = sys.argv[1:]
assert project in {'buildsmallplates', 'lucasrouter', 'missioncontrol', 'aiheartbeat'}
assert label and all(c.isalnum() or c in '-_' for c in label)
assert command
B = Path(__file__).resolve().parents[2]
pid = {'buildsmallplates': '676bcb38df2b', 'lucasrouter': '52d78d4a92a2', 'missioncontrol': 'ee8b0b1a6855', 'aiheartbeat': '9e1958f807df'}[project]
cwd = B / 'stage' / pid
out = B / 'checks' / project
out.mkdir(exist_ok=True)
log = out / (label + '.log')
record = out / (label + '.json')
assert not log.exists() and not record.exists(), 'Use a fresh run label to preserve evidence'
result = {'command': command, 'cwd': str(cwd), 'startedAt': datetime.now(timezone.utc).isoformat(), 'status': 'running', 'log': log.name}
record.write_text(json.dumps(result, indent=2), encoding='utf-8')
start = time.monotonic()
try:
    with log.open('wb') as stream:
        process = subprocess.Popen(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT)
        result['pid'] = process.pid
        record.write_text(json.dumps(result, indent=2), encoding='utf-8')
        code = process.wait()
    result.update(status='complete', exitCode=code, passed=code == 0)
except OSError as error:
    result.update(status='launch-failed', passed=False, error=str(error))
    code = 1
result.update(finishedAt=datetime.now(timezone.utc).isoformat(), elapsedSeconds=round(time.monotonic()-start, 2))
record.write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result), flush=True)
sys.exit(code)
