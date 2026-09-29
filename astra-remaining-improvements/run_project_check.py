"""Capture one finite command in an eligible isolated project; never infer success."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import os
import subprocess
import time

B = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('id')
parser.add_argument('label')
parser.add_argument('--cwd', default='.')
parser.add_argument('--env', action='append', default=[])
parser.add_argument('command', nargs=argparse.REMAINDER)
args = parser.parse_args()
eligible = {p['id']: p for p in json.loads((B/'scope.json').read_text(encoding='utf-8'))['eligible']}
assert args.id in eligible
assert args.label and all(c.isalnum() or c in '-_' for c in args.label)
stage = (B/'stage'/args.id).resolve()
cwd = (stage/args.cwd).resolve()
assert cwd.is_relative_to(stage) and cwd.is_dir()
command = args.command[1:] if args.command[:1] == ['--'] else args.command
assert command
out = B/'checks'/args.id
out.mkdir(exist_ok=True)
record, log = out/(args.label+'.json'), out/(args.label+'.log')
assert not record.exists() and not log.exists(), 'Choose a fresh label to preserve evidence'
env = os.environ.copy()
overrides = dict(item.split('=', 1) for item in args.env)
env.update(overrides)
result = {'project': eligible[args.id]['path'], 'id': args.id, 'command': command,
          'cwd': str(cwd), 'environmentOverrides': overrides,
          'startedAt': datetime.now(timezone.utc).isoformat(), 'status': 'running', 'log': log.name}
def save():
    record.write_text(json.dumps(result, indent=2), encoding='utf-8')
save()
start = time.monotonic()
try:
    with log.open('wb') as stream:
        process = subprocess.Popen(command, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT)
        result['pid'] = process.pid
        save()
        code = process.wait()
    result.update(status='complete', exitCode=code, passed=code == 0)
except OSError as error:
    result.update(status='launch-failed', passed=False, error=str(error))
    code = 1
result.update(finishedAt=datetime.now(timezone.utc).isoformat(), elapsedSeconds=round(time.monotonic()-start, 2))
save()
print(json.dumps(result), flush=True)
raise SystemExit(code)
