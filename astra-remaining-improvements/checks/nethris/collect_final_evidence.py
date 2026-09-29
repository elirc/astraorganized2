from pathlib import Path
import json
import hashlib
import sys

C = Path(__file__).resolve().parent
S = C.parents[1] / 'stage/71e7b036865c'
frontend, browser = sys.argv[1:]
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path, value):
    path.write_text(json.dumps(value, indent=2), encoding='utf-8')
for source, target, test in [('http-04-evidence', 'http-final-evidence', True),
                              (browser + '-evidence', 'browser-final-evidence', True),
                              (frontend, 'frontend-final', False)]:
    value = read(C / (source + '.json'))
    assert value.get('passed') is True if test else value['exitCode'] == 0
    write(C / (target + '.json'), {**value, 'recordedRun': source})
for source, target in [('npm-audit-02', 'npm-audit-evidence'), ('nuget-audit-01', 'nuget-audit-evidence')]:
    assert read(C / (source + '.json'))['exitCode'] == 0
    write(C / (target + '.json'), read(C / (source + '.log')))
assert read(C / 'npm-tree-01.json')['exitCode'] == 0
lock = read(S / 'client/package-lock.json')['packages']
versions = {name: lock['node_modules/' + name]['version'] for name in ['baseline-browser-mapping', 'browserslist', 'nanoid', 'postcss']}
write(C / 'patched-versions.json', versions)
print(json.dumps({'recorded': True, 'patchedVersions': versions}))
