"""Package Astra1 documentation only after all selected acceptance runs pass."""
from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', default='astra-astra1-owned-check-r2')
parser.add_argument('--api', default='astra-astra1-owned-api-r1')
parser.add_argument('--browser', default='astra-astra1-owned-browser-r1')
args = parser.parse_args()
batch = Path(__file__).resolve().parent
base = batch.parent
project_id = 'a8435f7ed53c'
project = base / 'stage' / project_id
labels = [args.check, args.api, args.browser]
records = []
logs = []
for label in labels:
    record = json.loads((base / 'checks' / project_id / (label + '.json')).read_text(encoding='utf-8'))
    assert record['status'] == 'complete' and record['exitCode'] == 0, label
    records.append(record)
    logs.append((base / 'checks' / project_id / record['log']).read_text(encoding='utf-8', errors='replace'))
assert re.findall(r'^# tests (\d+)\s*$', logs[0], re.M) == ['11', '37']
assert re.findall(r'^# pass (\d+)\s*$', logs[0], re.M) == ['11', '37']
assert re.findall(r'^# fail (\d+)\s*$', logs[0], re.M) == ['0', '0']
assert re.search(r'\b1 passed\b', logs[2]), 'Expected one repair browser case'

screenshots = ['operations-overview.png', 'intelligence-trace.png', 'cargo-delay.png', 'repair-complete.png']
browser_start = datetime.fromisoformat(records[2]['startedAt']).timestamp()
browser_archive = batch / 'astra1-browser-evidence' / args.browser
browser_archive.mkdir(parents=True, exist_ok=True)
for name in screenshots:
    source = project / 'artifacts/screenshots' / name
    cached = browser_archive / name
    if source.is_file() and source.stat().st_mtime >= browser_start:
        shutil.copy2(source, cached)
    assert cached.is_file() and cached.stat().st_mtime >= browser_start, name

baseline = json.loads((base / 'baselines' / (project_id + '.json')).read_text(encoding='utf-8-sig'))['files']
for name, expected in baseline.items():
    if name.endswith('.tsbuildinfo') or name.startswith('artifacts/'):
        original = Path('C:/Users/Owner/Desktop/astra1') / name
        assert hashlib.sha256(original.read_bytes()).hexdigest() == expected
        target = project / name
        if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            shutil.copyfile(original, target)

# Archive newly generated browser reports outside staging so they do not become
# source changes or replace the prior program's artifacts in the canonical copy.
artifact_root = (project / 'artifacts').resolve()
for source in artifact_root.rglob('*'):
    if not source.is_file():
        continue
    assert source.resolve().is_relative_to(artifact_root)
    relative = source.relative_to(project).as_posix()
    if relative in baseline:
        continue
    archived = browser_archive / 'generated' / source.relative_to(artifact_root)
    archived.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, archived)
    assert hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(archived.read_bytes()).digest()
    source.unlink()

plan = '''# Run 003: repair completion rollback regression

Mode: BUILD. Status: complete after isolated local verification.

The existing repair implementation already runs reservation consumption, work-order completion, crew release, incident resolution, audit creation, postmortem creation, and command receipt persistence in one PostgreSQL transaction. This pass preserves that implementation and adds a regression that rejects the late postmortem insert with a test-owned trigger.

The regression proves all earlier effects, including audit and receipt writes, roll back. Trigger/function cleanup runs in finally. Retrying the same command after cleanup succeeds once; replay returns the saved result without consuming inventory again.

The new launcher creates a temporary PostgreSQL 18 cluster on loopback with separate helios and helios_test databases. Its initial run correctly failed the existing isolation guard because both URLs were identical; the launcher was corrected without weakening that guard. API smoke and browser verification use only the helper-owned fixture. The original development database, packaged preview, prompts, and Run 002 record remain preserved.

Accepted verification: the combined check passed lint, TypeScript, 11 unit tests, 37 real PostgreSQL integration tests, and the production build. Both existing HTTP smoke programs passed. The coolant-repair Playwright case passed, including durable COMPLETED/RESOLVED state and no page errors. This is 49 distinct test cases, with the two smoke programs recorded separately.

Exact commands and results are in [verification](../../astraupskill/VERIFICATION.md). The four desktop screenshots from this browser run were visually inspected and are included with that evidence. They show the overview, pending adviser approval, delayed shipment, and completed repair with recovery records. [Learning material](../../upskilling/repair-rollback/README.md) contains exercises and separate solutions. Human learning remains unassessed.

These are local fixture checks, not verification of physical systems, public deployment, or live model providers. Historical Run 002 claims remain its own evidence and are not inferred from this focused follow-up.
'''
(project / 'docs/exec-plans/003-repair-rollback-regression.md').write_text(plan, encoding='utf-8')
current = project / 'docs/project/current-state.md'
text = current.read_text(encoding='utf-8')
marker = '\n## Follow-up: repair rollback verification (Run 003)\n'
text = text.split(marker)[0]
text += marker + '''
[Run 003](../exec-plans/003-repair-rollback-regression.md) adds a late-postmortem failure regression and an isolated PostgreSQL verification launcher. The existing repair transaction and the Run 002 implementation above are preserved. The new combined check passed lint/types, 11 unit tests, 37 PostgreSQL integration tests, and the production build; both HTTP smoke programs and the affected repair browser case passed. See the [new evidence](../../astraupskill/VERIFICATION.md) and [separate learning material](../../upskilling/repair-rollback/README.md). This follow-up used a temporary PostgreSQL 18 cluster and does not reverify the historical packaged preview or live-provider behavior. Human learning remains unassessed.
'''
current.write_text(text, encoding='utf-8')
subprocess.run([sys.executable, str(batch / 'write_astra1_course.py')], check=True)
subprocess.run([sys.executable, str(batch / 'package_review.py'), project_id,
                '--tests', '49', '--labels', *labels], check=True)
spec_path = base / 'specs' / (project_id + '.json')
spec = json.loads(spec_path.read_text(encoding='utf-8'))
verification = project / 'astraupskill/VERIFICATION.md'
with verification.open('a', encoding='utf-8') as output:
    output.write('\n## Browser screenshots from the accepted run\n\n')
    for name in screenshots:
        relative = 'astraupskill/evidence/' + name
        shutil.copyfile(browser_archive / name, project / relative)
        spec['changedFiles'].append(relative)
        output.write(f'- [{name}](evidence/{name})\n')
spec['changedFiles'] = sorted(set(spec['changedFiles']))
spec_path.write_text(json.dumps(spec, indent=2), encoding='utf-8')
for source in (project / 'astraupskill').glob('*.md'):
    mirrored = source.read_text(encoding='utf-8').replace('](../', '](../../')
    mirrored = mirrored.replace('](evidence/', '](../../astraupskill/evidence/')
    mirrored = mirrored.replace('](snapshots/', '](../../astraupskill/snapshots/')
    (project / 'upskilling/repair-rollback' / source.name).write_text(mirrored, encoding='utf-8')
print('Astra1 docs and evidence packaged; source review and delivery gates remain required.')
