from pathlib import Path
import json, subprocess, sys, time

C = Path(__file__).resolve().parent
B = C.parents[1]
stage = B / 'stage/767d610cb528'
name = sys.argv[1]
assert name in {'context-before', 'context-after', 'sdk-after', 'evaluation-safety'}
assert not (C / f'{name}.json').exists()
command = ['node', '--test', 'test/context-cache.test.js']
if name == 'sdk-after':
    command = ['node', '--test', 'test/context-cache.test.js', 'test/sdk.test.js']
if name == 'evaluation-safety':
    command = ['node', '--test', 'test/evaluation.test.js', 'test/evaluation-safety.test.js', 'test/context-cache.test.js']
started = time.time()
with (C / f'{name}.log').open('w', encoding='utf-8') as log:
    result = subprocess.run(command, cwd=stage, stdout=log, stderr=subprocess.STDOUT)
evidence = {'command': command, 'exitCode': result.returncode,
            'seconds': round(time.time()-started, 2),
            'expectedFailureBeforeFix': name == 'context-before'}
(C / f'{name}.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
print(json.dumps(evidence), flush=True)
print((C / f'{name}.log').read_text(encoding='utf-8'), flush=True)
raise SystemExit(0 if name == 'context-before' and result.returncode else result.returncode)
