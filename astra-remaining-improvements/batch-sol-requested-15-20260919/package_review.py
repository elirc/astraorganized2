"""Collect exact snapshots and already-passing evidence for a resumed project; never apply."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from long_paths import extended_path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('id')
parser.add_argument('--tests', type=int, required=True)
parser.add_argument('--labels', nargs='+', required=True)
parser.add_argument('--trx', nargs='+')
parser.add_argument('--non-trx-tests', type=int, default=0)
args = parser.parse_args()
B = extended_path(Path(__file__).resolve().parent.parent)
P = B / 'stage' / args.id
scope = json.loads((B / 'scope.json').read_text(encoding='utf-8'))
project = next(p for p in scope['eligible'] if p['id'] == args.id)
canonical = B.parent.parent / project['path']
baseline = json.loads((B / 'baselines' / (args.id + '.json')).read_text(encoding='utf-8-sig'))['files']
spec_path = B / 'specs' / (args.id + '.json')
spec = json.loads(spec_path.read_text(encoding='utf-8-sig'))
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
required = ['README.md', '01-CODEBASE-MAP.md', '02-CONCEPTS.md', '03-WORKED-CHANGE.md', '04-TESTING-AND-DEBUGGING.md', '05-PRACTICE.md', '06-SOLUTIONS-AND-REVIEW.md', '07-TRACE-LAB.md', 'VERIFICATION.md']
ignored = {'node_modules', '.git', '.next', 'dist', 'bin', 'obj', '.venv', '__pycache__', 'coverage', 'TestResults', '.turbo', '.cache'}
suffixes = {'.cs', '.csproj', '.sln', '.props', '.targets', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.py', '.ps1', '.json', '.yaml', '.yml', '.toml', '.sql', '.prisma', '.css', '.html', '.md'}
files = set()
for name, original in baseline.items():
    if not (P / name).is_file(): raise AssertionError('Missing baseline file: ' + name)
    if digest(P / name) != original:
        files.add(name)
        assert digest(canonical / name) == original, 'Canonical changed: ' + name
        snapshot = 'astraupskill/snapshots/' + name.replace('/', '__') + '.original.txt'
        (P / snapshot).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(canonical / name, P / snapshot)
        files.add(snapshot)
for directory, dirs, names in os.walk(P):
    dirs[:] = [n for n in dirs if n not in ignored]
    for name in names:
        path = Path(directory) / name
        rel = path.relative_to(P).as_posix()
        if rel.startswith(('astraupskill/', 'snapshots/')) or rel in baseline: continue
        if path.suffix.lower() in suffixes or rel in {'README.md', '.env.example'}: files.add(rel)
records = []
rows = []
for label in args.labels:
    record_path = B / 'checks' / args.id / (label + '.json')
    record = json.loads(record_path.read_text(encoding='utf-8'))
    assert record['status'] == 'complete' and record['exitCode'] == 0, label
    records.append(record)
    for source in [record_path, record_path.parent / record['log']]:
        rel = 'astraupskill/evidence/' + source.name
        (P / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, P / rel)
        files.add(rel)
    rows.append(f'| `{label}` | `{json.dumps(record["command"])}` | 0 | [record](evidence/{label}.json), [log](evidence/{record["log"]}) |')
trx_links = []
if args.trx:
    total = 0
    for index, name in enumerate(args.trx, 1):
        trx = B / name
        counts = ET.parse(trx).find('.//{*}Counters').attrib
        assert int(counts['total']) == int(counts['passed'])
        assert int(counts['failed']) == int(counts['notExecuted']) == 0
        total += int(counts['total'])
        filename = 'regression.trx' if len(args.trx) == 1 else f'regression-{index}.trx'
        rel = 'astraupskill/evidence/' + filename
        shutil.copyfile(trx, P / rel); files.add(rel)
        trx_links.append(f'[Machine-readable results {index}](evidence/{filename})')
    assert total + args.non_trx_tests == args.tests
result = {'passed': True, 'total': args.tests, 'passedTests': args.tests, 'failed': 0, 'checks': records}
result_path = B / 'checks' / args.id / 'sol15-results.json'
result_path.write_text(json.dumps(result, indent=2), encoding='utf-8')
verification = P / 'astraupskill/VERIFICATION.md'
text = verification.read_text(encoding='utf-8').split('\n## Recorded command evidence')[0]
text += '\n## Recorded command evidence\n\n' + f'The accepted test evidence covers **{args.tests} distinct passing tests**. The commands below define the verified scope; repeated targeted runs do not increase the count.\n\n'
text += '| Check | Recorded command | Exit | Evidence |\n|---|---|---:|---|\n' + '\n'.join(rows) + '\n'
if args.trx: text += '\n' + ', '.join(trx_links) + '.\n'
verification.write_text(text, encoding='utf-8')
spec['changedFiles'] = sorted(files - {'astraupskill/' + n for n in required})
spec['checks'] = {'format': 'json', 'resultsFile': result_path.relative_to(B).as_posix(), 'expectedTests': args.tests, 'command': 'Recorded test runs and build/type checks'}
spec_path.write_text(json.dumps(spec, indent=2), encoding='utf-8')
print(json.dumps({'id': args.id, 'listedFiles': len(files), 'tests': args.tests, 'checks': args.labels}, indent=2))
