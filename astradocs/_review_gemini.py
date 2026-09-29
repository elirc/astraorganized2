import json, re, hashlib, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESKTOP = ROOT.parent
catalog = json.loads((ROOT / 'project-catalog.json').read_text(encoding='utf-8'))['projects']
records = []
for item in catalog:
    if not item['path'].startswith('geminiorganized/'):
        continue
    paths = []
    if item.get('purpose_evidence'):
        paths.append(item['purpose_evidence'])
    for kind in ('documentation_inspected', 'manifests_inspected', 'source_files_inspected', 'tests_inspected'):
        paths.extend(item.get('evidence', {}).get(kind, [])[:2])
    paths = list(dict.fromkeys(paths))
    checked, errors, excerpts = [], [], []
    for rel in paths:
        p = DESKTOP / rel
        if '.env' in p.name.lower() or p.suffix.lower() in {'.pdf','.docx','.odt'}:
            continue
        try:
            raw = p.read_bytes()
            txt = raw.decode('utf-8', errors='replace')
            checked.append({'path': rel, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
            if rel == item.get('purpose_evidence') or (p.suffix in {'.md','.txt'} and len(excerpts) < 1):
                lines = [l.strip() for l in txt.splitlines() if l.strip() and not l.startswith(('[!', '[![', '<img', '![', 'http'))]
                excerpts.append({'path': rel, 'excerpt': '\n'.join(lines[:18])[:1800]})
        except OSError as exc:
            errors.append({'path': rel, 'error': str(exc)})
    rec = {'path': item['path'], 'purpose': item['purpose'], 'assessment': item['apparent_state'],
           'evidence_files': [x['path'] for x in checked], 'fresh_checks': checked,
           'errors': errors, 'excerpts': excerpts, 'documentation_caveats': item.get('documentation_caveats', [])}
    records.append(rec)
(ROOT / 'astradocs' / 'review-gemini.json').write_text(json.dumps({'method':'Fresh read of saved evidence paths; no project runtime executed.', 'projects':records}, ensure_ascii=False, indent=2), encoding='utf-8')
for item in records:
    print('\n' + item['path'] + ' | ' + item['assessment'] + ' | files=' + str(len(item['fresh_checks'])))
    for excerpt in item['excerpts'][:1]:
        print(excerpt['excerpt'][:950])
    if item['documentation_caveats']:
        print('CAVEATS:', str(item['documentation_caveats'])[:800])
    if item['errors']:
        print('ERRORS:', item['errors'])
print('TOTAL', len(records), 'READS', sum(len(x['fresh_checks']) for x in records))
