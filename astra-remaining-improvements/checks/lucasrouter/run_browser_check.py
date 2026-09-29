"""Run the existing smoke test against an owned local production server."""
from pathlib import Path
from datetime import datetime, timezone
import json
import os
import re
import socket
import subprocess
import time
import urllib.request

C = Path(__file__).resolve().parent
B = C.parent.parent
S = B / 'stage/52d78d4a92a2'
label = __import__('sys').argv[1]
assert label and all(c.isalnum() or c in '-_' for c in label)
out = C / label
out.mkdir(exist_ok=False)
with socket.socket() as listener:
    listener.bind(('127.0.0.1', 0))
    port = listener.getsockname()[1]
base = f'http://127.0.0.1:{port}'
start = time.monotonic()
result = {'startedAt': datetime.now(timezone.utc).isoformat(), 'baseUrl': base, 'passed': False}
server = None
try:
    with (out / 'server.log').open('wb') as server_log:
        server = subprocess.Popen(['node', 'node_modules/next/dist/bin/next', 'start', '--hostname', '127.0.0.1', '--port', str(port)], cwd=S, stdout=server_log, stderr=subprocess.STDOUT)
        result['serverPid'] = server.pid
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            if server.poll() is not None:
                raise RuntimeError(f'Owned server exited {server.returncode} before readiness')
            try:
                with urllib.request.urlopen(base + '/api/health', timeout=3) as response:
                    health = json.loads(response.read())
                if health.get('ok') is True and health.get('algorithm') == 'nn-2opt-v1':
                    break
            except (OSError, ValueError):
                pass
            time.sleep(.5)
        else:
            raise RuntimeError('Owned production server did not become ready within 120 seconds')
        command = ['node', 'scripts/smoke-e2e.mjs', base]
        result['command'] = command
        with (out / 'smoke.log').open('wb') as log:
            smoke = subprocess.run(command, cwd=S, stdout=log, stderr=subprocess.STDOUT)
        text = (out / 'smoke.log').read_text(encoding='utf-8', errors='replace')
        result.update(exitCode=smoke.returncode, passed=smoke.returncode == 0,
                      passedChecks=len(re.findall(r'^PASS\s', text, re.M)), failedChecks=len(re.findall(r'^FAIL\s', text, re.M)))
except Exception as error:
    result['error'] = str(error)
finally:
    if server is not None and server.poll() is None:
        if os.name == 'nt':
            stopped = subprocess.run(['taskkill', '/PID', str(server.pid), '/T', '/F'], capture_output=True)
            result['stopExitCode'] = stopped.returncode
        else:
            server.terminate()
        server.wait(timeout=30)
    result['ownedServerStopped'] = server is None or server.poll() is not None
    result['elapsedSeconds'] = round(time.monotonic() - start, 2)
    (out / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result), flush=True)
raise SystemExit(0 if result['passed'] else 1)
