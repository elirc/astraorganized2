"""Render the exact selected batch from delivery evidence, keeping pending work visible."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote, unquote
import json
import os
import re
from report_evidence import check_summary

B = Path(__file__).resolve().parent
R = B.parent
folder = B/'checks/batch-luna-astra-50-20260912'
selection = json.loads((folder/'selection.json').read_text(encoding='utf-8'))
ledger = json.loads((B/'progress.json').read_text(encoding='utf-8'))
progress = {p['id']: p for p in ledger['projects']}
projects = selection['projects']
assert len(projects) == len({p['id'] for p in projects}) == 50
report = R/'astradocs/NEXT_50_PROJECT_IMPROVEMENTS_REPORT.md'
def link(label, path):
    return '['+label+']('+quote(os.path.relpath(path, report.parent).replace('\\','/'), safe='/.-')+')'
done = [p for p in projects if progress[p['id']]['status'] == 'complete']
total_done = sum(p['status'] == 'complete' for p in ledger['projects'])
lines = ['# Next 50 project improvements', '',
         f'Updated {datetime.now(timezone.utc).isoformat()}. **{len(done)} of these 50 projects delivered; {50-len(done)} still in progress or queued.**', '',
         f'This batch started after 42 eligible project families were delivered. Overall: **{total_done} of {ledger["total"]} eligible families delivered**, {ledger["total"]-total_done} remaining. The audited top 50 and previously modified families remain excluded.', '',
         'Luna implements project-specific code, regression tests and detailed learning courses. Astra plans and independently reviews correctness and teaching quality. Only verified changes applied to the canonical project folder count as delivered.', '',
         'The batch includes MissionControl and Pulse, which were already underway when the request expanded to 50. Selection and implementation use canonical project families, so duplicate Desktop copies are not counted twice.', '',
         link('Selection and ordered plan', folder/'PLAN.md')+' · '+link('Exact selection', folder/'selection.json'), '',
         '## Batch overview', '', '| # | Project | Status | Change or planned focus |', '|---|---|---|---|']
details = []
for p in projects:
    row = progress[p['id']]
    canonical = R.parent/p['path']
    delivered = row['status'] == 'complete'
    manifest_path = B/'deliveries'/(p['id']+'.json')
    spec_path = B/'specs'/(p['id']+'.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if delivered else None
    spec = json.loads(spec_path.read_text(encoding='utf-8-sig')) if spec_path.exists() else None
    planned_focus = p.get('reviewedFocus', p['initialFocus'])
    summary = manifest['summary'] if manifest else spec['summary'] if spec else [planned_focus]
    summary = [summary] if isinstance(summary, str) else summary
    focus = summary[0] if summary else planned_focus
    status = 'Delivered' if delivered else 'Staged; review/checks pending' if (B/'stage'/p['id']).exists() else 'Queued'
    lines.append(f'| {p["sequence"]} | {link(p["name"], canonical)} | {status} | {focus.replace(chr(10), " ").replace("|", "/")} |')
    details += ['', f'## {p["sequence"]}. {p["name"]}', '', f'**{status}.** Canonical folder: '+link(p['path'], canonical)+'.', '']
    review_path = folder/(p['id']+'-review.md')
    if review_path.exists():
        details += [link('Astra review findings and decision', review_path), '']
    if not delivered:
        plan_path = folder/(p['id']+'-plan.md')
        if plan_path.exists():
            details += [link('Astra plan based on source review', plan_path), '']
        details += ['Planned focus: '+planned_focus+'.', '', 'This entry does not yet claim completed changes or successful validation.']
        completed_checks = []
        for check_dir in {B/'checks'/p['id'], B/'checks'/p['name']}:
            for check_file in sorted(check_dir.glob('*.json')):
                try:
                    check = json.loads(check_file.read_text(encoding='utf-8'))
                except (ValueError, UnicodeError):
                    continue
                if (check.get('status') == 'complete' and check.get('passed') is True
                        and check.get('exitCode') == 0 and check.get('command')
                        and Path(check.get('cwd', '')).resolve().is_relative_to((B/'stage'/p['id']).resolve())):
                    completed_checks.append('- '+link(check_file.stem, check_file)+' completed with exit code 0. Command: `'+ ' '.join(check['command'])+'`.')
        if completed_checks:
            details += ['', 'Completed individual setup/check commands (these alone do not establish project completion):', '']+completed_checks
        continue
    details += ['Changes:', ''] + ['- '+v for v in manifest['summary']]
    details += ['', f'Learning material: {manifest["courseFiles"]} course files, {manifest["courseWords"]:,} words; '+link('start here', canonical/'astraupskill/README.md')+'.', '',
                'Validation: '+check_summary(manifest)+'. '+manifest['checks'].get('command','See evidence')+'.', '',
                link('Delivery manifest and results', manifest_path)+' · '+link('Verification guide', canonical/'astraupskill/VERIFICATION.md'), '', 'Changed files:', '']
    details += ['- '+link(f['file'], canonical/f['file']) for f in manifest['files']]
    details += ['', 'Limits:', ''] + ['- '+v for v in manifest['limits']]
lines += ['', '## Acceptance standard', '', 'Each delivered project has an actual code or setup improvement, regression evidence appropriate to the change, and a nine-file course covering the code map, concepts, worked change, debugging, exercises, solutions, trace lab and verification. Setup, browser, service and deployment limitations are stated explicitly. A staged draft is not completion.']
lines += details
text = '\n'.join(lines)+'\n'
assert '\ufffd' not in text
for target in re.findall(r'\]\(([^)]+)\)', text):
    assert (report.parent/unquote(target)).exists(), target
report.write_text(text, encoding='utf-8')
print(json.dumps({'report': str(report), 'selected': 50, 'deliveredInBatch': len(done), 'overallDelivered': total_done, 'localLinksChecked': len(re.findall(r'\]\(([^)]+)\)', text))}))
