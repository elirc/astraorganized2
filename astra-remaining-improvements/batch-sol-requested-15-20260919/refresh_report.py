"""Verify delivered batch files and refresh its report and the remaining queue."""
from pathlib import Path
from urllib.parse import quote
from datetime import datetime, timezone
from collections import defaultdict
import argparse
import hashlib
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from long_paths import extended_path

parser = argparse.ArgumentParser()
parser.add_argument('--final', action='store_true')
args = parser.parse_args()
batch = Path(__file__).resolve().parent
B = extended_path(batch.parent)
D = B.parent / 'astradocs'
state = json.loads((batch / 'state.json').read_text(encoding='utf-8'))
progress = json.loads((B / 'progress.json').read_text(encoding='utf-8'))
status = {p['id']: p['status'] for p in progress['projects']}
delivered = {}
hashes = 0
for item in state['projects']:
    path = B / 'deliveries' / (item['id'] + '.json')
    if not path.exists():
        continue
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if manifest['status'] != 'delivered':
        continue
    assert status[item['id']] == 'complete', item['path']
    results = manifest['testResults']
    assert results['passed'] and results['failed'] == 0
    assert results['checks']
    for check in results['checks']:
        assert check['status'] == 'complete' and check['exitCode'] == 0
    for entry in manifest['files']:
        target = B.parent.parent / manifest['project'] / entry['file']
        assert target.is_file(), str(target)
        assert hashlib.sha256(target.read_bytes()).hexdigest() == entry['after_sha256'], str(target)
        hashes += 1
    delivered[item['id']] = manifest
    item.update(status='delivered', files=len(manifest['files']), tests=results['total'], deliveredAt=manifest['deliveredAt'])
if args.final:
    assert len(delivered) == len(state['projects']) == 15
remaining = [p for p in progress['projects'] if p['status'] != 'complete']
completed = len(progress['projects']) - len(remaining)
tests = sum(m['testResults']['total'] for m in delivered.values())
checks = sum(len(m['testResults']['checks']) for m in delivered.values())
verification = dict(verifiedAt=datetime.now(timezone.utc).isoformat(), requestedProjects=15,
                   deliveredProjects=len(delivered), deliveredFileHashesVerified=hashes,
                   passingTestCases=tests, acceptedChecks=checks, remainingFamilies=len(remaining),
                   projectsEvidence=[dict(id=k, path=m['project'], files=len(m['files']), tests=m['testResults']['total']) for k,m in delivered.items()])
(batch / 'delivery-verification.json').write_text(json.dumps(verification, indent=2) + '\n', encoding='utf-8')
(batch / 'state.json').write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8')
lines = ['# Requested fifteen-project improvement report', '',
         f'**{len(delivered)} of 15 selected projects delivered.** ' + ('All selected work is complete.' if len(delivered)==15 else 'Implementation and verification continue for the remaining selected projects.'), '',
         f'Delivered work has **{tests} passing test cases**, **{checks} successful recorded checks**, and **{hashes} verified delivered file hashes**. Test counts describe the accepted per-project suites, not a claim that every upstream suite was run.', '',
         'Sol agents contributed initial staged changes. At the user\'s request, Astra took over the remaining implementation, review, checks and delivery without subagents. Existing Fable work and documentation are preserved. Each delivered project includes nine source-based `astraupskill` chapters, exercises and solutions, verification logs, and original snapshots for changed baseline files.', '',
         '| Project | Status | Passing tests | Evidence |', '|---|---|---:|---|']
for item in state['projects']:
    url = '../../' + quote(item['path'], safe='/')
    m = delivered.get(item['id'])
    evidence = f'[Course]({url}/astraupskill/README.md), [checks]({url}/astraupskill/VERIFICATION.md)' if m else 'Pending delivery review'
    lines.append(f"| [{item['path']}]({url}) | {'Delivered' if m else 'In progress'} | {m['testResults']['total'] if m else '—'} | {evidence} |")
lines += ['', '## Changes and additions delivered', '']
for item in state['projects']:
    m = delivered.get(item['id'])
    if not m:
        continue
    lines += ['### ' + item['path'], '']
    summary = m['summary']
    lines += [summary] if isinstance(summary, str) else ['- ' + s for s in summary]
    lines.append('')
    for label, was_present in [('Changed source/configuration files', True), ('Added source/test/setup files', False)]:
        names = [e['file'] for e in m['files'] if not e['file'].startswith('astraupskill/') and e['file'] != 'README.md' and bool(e['before_sha256']) == was_present]
        if names:
            lines += [f'**{label}:** ' + ', '.join('`'+n+'`' for n in names) + '.', '']
    limits = m.get('limits', [])
    if isinstance(limits, str):
        limits = [limits]
    if limits:
        lines += ['**Verification limits:** ' + ' '.join(limits), '']
    lines += [f"[Delivery manifest](../astra-remaining-improvements/deliveries/{item['id']}.json)", '']
lines += ['## Campaign status', '',
          f'The campaign ledger is **{completed} of {len(progress["projects"])} complete**; **{len(remaining)} project families remain queued**. See the [remaining list](REMAINING_PROJECTS_TO_DO_2026-09-19.md).', '',
          'The [earlier fourteen-project completion report](COMPLETED_14_PROJECTS_2026-09-19.md) is preserved as historical evidence. The 153 earlier Astra projects covered by Fable remain outside this campaign queue.', '',
          '[Verified delivery counts and hashes](../astra-remaining-improvements/batch-sol-requested-15-20260919/delivery-verification.json). Failed or interrupted setup/check attempts remain in the campaign logs; only accepted terminal-zero checks count as passing evidence.', '']
(D / 'REQUESTED_15_PROJECTS_2026-09-19.md').write_text('\n'.join(lines), encoding='utf-8')
groups = defaultdict(list)
for item in remaining:
    path = item['path'].replace('\\', '/')
    groups[path.split('/')[0] if '/' in path else 'Desktop'].append(path)
queue = ['# Remaining Desktop projects to do', '',
         f'**{len(remaining)} project families remain queued.** {len(delivered)} of the latest 15 selected projects are delivered; the previous 14-project batch is also complete.', '',
         '[Current fifteen-project report](REQUESTED_15_PROJECTS_2026-09-19.md) / [Earlier fourteen-project report](COMPLETED_14_PROJECTS_2026-09-19.md) / [Progress ledger](../astra-remaining-improvements/progress.json)', '',
         'An unchecked item has no completed delivery recorded. ' + ('Some selected projects are actively staged and being verified. ' if len(delivered) < 15 else 'All fifteen selected projects are delivered; the items below are outside that completed selection. ') + 'The 153 earlier Astra projects covered by Fable remain excluded; this is the existing campaign queue, not a fresh Desktop inventory.', '',
         f'## Remaining queued families ({len(remaining)})', '']
for group in sorted(groups, key=lambda g: (g != 'Desktop', g.casefold())):
    paths = sorted(groups[group], key=str.casefold)
    queue += [f"### {group} / {'top-level' if group == 'Desktop' else 'nested'} projects ({len(paths)})", '']
    queue += [f'- [ ] [{path}](../../{quote(path, safe="/")})' for path in paths]
    queue.append('')
(D / 'REMAINING_PROJECTS_TO_DO_2026-09-19.md').write_text('\n'.join(queue), encoding='utf-8')
print(json.dumps(verification, indent=2))
