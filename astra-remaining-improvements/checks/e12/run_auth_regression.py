from pathlib import Path
import json, subprocess, time

C = Path(__file__).resolve().parent
S = C.parents[1] / 'stage/767d610cb528'
assert not (C / 'auth-01.json').exists()
command = ['node', '--test']
started = time.time()
with (C / 'auth-01.log').open('w', encoding='utf-8') as log:
    result = subprocess.run(command, cwd=S, stdout=log, stderr=subprocess.STDOUT)
evidence = {'command': command, 'exitCode': result.returncode, 'seconds': round(time.time()-started, 2)}
(C / 'auth-01.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
print(json.dumps(evidence), flush=True)
print((C / 'auth-01.log').read_text(encoding='utf-8')[-25000:], flush=True)
raise SystemExit(result.returncode)
