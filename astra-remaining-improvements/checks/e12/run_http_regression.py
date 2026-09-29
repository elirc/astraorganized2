from pathlib import Path
import json, subprocess, time, sys

C = Path(__file__).resolve().parent
S = C.parents[1] / 'stage/767d610cb528'
name = sys.argv[1] if len(sys.argv) > 1 else 'http-01'
assert name in {'http-01', 'http-02'}
assert not (C / f'{name}.json').exists()
command = ['node', 'verification/run-tests.js'] if name == 'http-01' else ['node', '--test', 'test/http.test.js']
started = time.time()
with (C / f'{name}.log').open('w', encoding='utf-8') as log:
    result = subprocess.run(command, cwd=S, stdout=log, stderr=subprocess.STDOUT)
evidence = {'command': command, 'exitCode': result.returncode, 'seconds': round(time.time()-started, 2)}
(C / f'{name}.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
print(json.dumps(evidence), flush=True)
print((C / f'{name}.log').read_text(encoding='utf-8')[-30000:], flush=True)
raise SystemExit(result.returncode)
