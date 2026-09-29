from pathlib import Path
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
C = Path(__file__).resolve().parent
S = C.parents[1] / 'stage/4de416cd300b'
name = sys.argv[1]
assert name.replace('-', '').isalnum()
output = C / name
assert not output.exists()
output.mkdir()
with socket.socket() as reserve:
    reserve.bind(('127.0.0.1', 0))
    port = reserve.getsockname()[1]
url = f'http://127.0.0.1:{port}/'
environment = os.environ.copy()
environment['TIDEBOUND_URL'] = url
environment['TIDEBOUND_BROWSER_PATH'] = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
environment['PYTHONUTF8'] = '1'
results = []
with (output / 'preview.log').open('w', encoding='utf-8') as log:
    server = subprocess.Popen(['node', str(S / 'node_modules/vite/bin/vite.js'), 'preview', '--host', '127.0.0.1', '--port', str(port), '--strictPort'],
                              cwd=S, env=environment, stdout=log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        deadline = time.monotonic() + 60
        while True:
            if server.poll() is not None:
                raise RuntimeError('Owned preview exited before readiness.')
            try:
                with urllib.request.urlopen(url, timeout=2) as response:
                    if response.status == 200:
                        break
            except OSError:
                pass
            if time.monotonic() > deadline:
                raise TimeoutError('Owned preview did not become ready.')
            time.sleep(.2)
        for script, report in [('browser-check.mjs', 'browser-report.json'), ('release-check.mjs', 'release-report.json'), ('performance-check.mjs', 'performance-report.json')]:
            started = time.monotonic()
            with (output / (script + '.log')).open('w', encoding='utf-8') as runlog:
                run = subprocess.run(['node', 'scripts/' + script], cwd=S, env=environment, stdout=runlog, stderr=subprocess.STDOUT)
            result = {'script': script, 'exitCode': run.returncode, 'seconds': round(time.monotonic() - started, 2)}
            results.append(result)
            print(json.dumps(result), flush=True)
            if run.returncode:
                print((output / (script + '.log')).read_text(encoding='utf-8', errors='replace')[-6000:], flush=True)
                raise RuntimeError(script + ' failed')
            shutil.copyfile(S / 'artifacts' / report, output / report)
            if script == 'browser-check.mjs':
                for picture in ['desktop-game.png', 'mobile-game.png', 'mobile-settings.png']:
                    shutil.copyfile(S / 'artifacts' / picture, output / picture)
        (output / 'results.json').write_text(json.dumps({'passed': True, 'results': results, 'url': url}, indent=2), encoding='utf-8')
    except Exception as error:
        (output / 'results.json').write_text(json.dumps({'passed': False, 'results': results, 'error': str(error), 'url': url}, indent=2), encoding='utf-8')
        raise
    finally:
        if server.poll() is None:
            server.terminate()
        server.wait(timeout=30)
        print('Owned preview stopped.', flush=True)
