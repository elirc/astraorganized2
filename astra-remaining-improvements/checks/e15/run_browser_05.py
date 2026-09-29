from pathlib import Path
import json, os, subprocess, sys, time

checks = Path(__file__).resolve().parent
bundle = checks.parents[1]
stage = bundle / 'stage/19110bf39fcf'
env = {**os.environ, 'PYTHONIOENCODING': 'utf-8',
       'ASTRA_BROWSER_EXECUTABLE': str(bundle / 'playwright-browsers/chromium-1223/chrome-win64/chrome.exe'),
       'HELPDESK_BROWSER_OUTPUT': str(checks / 'browser-05')}
assert not (checks / 'browser-05').exists()
command = [sys.executable, 'verification/verify_browser.py']
start = time.time()
with (checks / 'browser-05.log').open('w', encoding='utf-8') as log:
    result = subprocess.run(command, cwd=stage, env=env, stdout=log, stderr=subprocess.STDOUT)
evidence = {'command': command, 'exitCode': result.returncode, 'seconds': round(time.time()-start, 2)}
(checks / 'browser-05-execution.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
print(json.dumps(evidence), flush=True)
print((checks / 'browser-05.log').read_text(encoding='utf-8')[-12000:], flush=True)
raise SystemExit(result.returncode)
