from report_evidence import check_summary
"""Readable per-project summary of actual deliveries, with links to detailed evidence."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote, unquote
import json
import re

B = Path(__file__).resolve().parent
R = B.parent
progress = json.loads((B / 'progress.json').read_text(encoding='utf-8'))
manifests = []
for row in progress['projects']:
    if row['status'] == 'complete':
        manifest = json.loads((B / 'deliveries' / (row['id'] + '.json')).read_text(encoding='utf-8'))
        assert manifest['status'] == 'delivered'
        manifests.append(manifest)
manifests.sort(key=lambda m: m.get('deliveredAt', ''))
target = R / 'astradocs/FINISHED_PROJECTS_SUMMARY.md'
lines = ['# Finished projects: concise change summary', '',
         'Updated ' + datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC') + '.', '',
         f'**{len(manifests)} of {progress["total"]} eligible project families delivered; {progress["total"] - len(manifests)} remain.** The complete collection is still in progress. The original top-50 and previously modified family exclusions are preserved.', '',
         'Each project link opens its learning course. The table summarizes the main changes applied to its original folder; the evidence link contains the complete change list, verification and limits. Counts refer to recorded delivery runs, not fresh reruns of every older project.', '',
         '| Project / Desktop location | Main improvements | Learning and verification |',
         '| --- | --- | --- |']
def escape(text):
    return text.replace('|', '\\|').replace('\n', ' ')
for m in manifests:
    course = quote('../../' + m['project'] + '/astraupskill/README.md', safe='/+')
    evidence = '../astra-remaining-improvements/deliveries/' + m['id'] + '.json'
    summary = ' '.join(m['summary'][:2])
    lines.append(f'| [{escape(m["project"])}]({course}) | {escape(summary)} | {m["courseFiles"]} guides; [{check_summary(m)}]({evidence}) |')
lines += ['', '## Review notes', '',
          '- The [detailed per-project report](PROJECT_CHANGES_AND_COMPLETION_REPORT.md) covers additional changes, including reliability work, preserved originals and later file differences.',
          '- The [remaining queue](../astrdocs/REMAINING_PROJECTS_IMPLEMENTATION_REPORT.md) lists all unfinished eligible families.']
audit = json.loads((B / 'delivered-files-audit.json').read_text(encoding='utf-8'))
different = sum(len(row['differentFromDelivery']) for row in audit['results'])
missing = sum(len(row['missing']) for row in audit['results'])
lines += [f'- File reconciliation found {different} files differing from their recorded deliveries and {missing} missing files. Existing differences were preserved; historical checks apply to the delivered versions. [Read-only reconciliation](../astra-remaining-improvements/delivered-files-audit.json).']
cleanup = B / 'checks/nethris/cleanup-limitation.json'
if cleanup.exists():
    lines += ['- Automatic approval review blocked cleanup of one synthetic temporary test database and an older generated browser bundle. They were left untouched; Nethris verification used a fresh package folder. [Cleanup record](../astra-remaining-improvements/checks/nethris/cleanup-limitation.json).']
lines += ['']
text = '\n'.join(lines)
for url in re.findall(r'\]\(([^)]+)\)', text):
    assert (target.parent / unquote(url)).exists(), url
target.write_text(text, encoding='utf-8')
print(json.dumps({'report': str(target), 'projects': len(manifests), 'remaining': progress['total'] - len(manifests), 'linksVerified': True}))
