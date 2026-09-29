"""Comparison phase only: the independent baseline must already exist."""
from pathlib import Path
from collections import Counter
from urllib.parse import quote
import json
import hashlib
import re
from datetime import datetime, timezone

ROOT = Path('C:/Users/Owner/Desktop')
OUT = ROOT / 'AstraOrganized2'
OLD = ROOT / 'AstraOrganized'

def now():
    return datetime.now(timezone.utc).isoformat()

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def normal(path):
    path = path.replace('\\', '/').rstrip('/')
    prefix = str(ROOT).replace('\\', '/') + '/'
    if path.lower().startswith(prefix.lower()):
        path = path[len(prefix):]
    return path.casefold()

def relative(path):
    path = path.replace('\\', '/')
    prefix = str(ROOT).replace('\\', '/') + '/'
    return path[len(prefix):] if path.lower().startswith(prefix.lower()) else path

def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')

def folder(path):
    path = relative(path)
    return '[' + cell(path) + '](../' + quote(path, safe='/') + ')'

baseline = read(OUT / 'independent-baseline.json')
assert baseline['astraorganized_read_before_completion'] is False
def verify_baseline():
    for name, digest in baseline['files'].items():
        path = OUT / name
        if name == 'PROJECT_INDEX.md' and (OUT / 'independent-snapshot' / name).exists():
            path = OUT / 'independent-snapshot' / name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, name

verify_baseline()
# Preserve the frozen original; repair only local table-of-contents anchor spelling.
index_path = OUT / 'PROJECT_INDEX.md'
original_index = (OUT / 'independent-snapshot' / 'PROJECT_INDEX.md')
original_bytes = original_index.read_bytes() if original_index.exists() else index_path.read_bytes()
index_text = original_bytes.decode('utf-8')
for category in {p['category'] for p in read(OUT / 'project-catalog.json')['projects']}:
    old_anchor = category.lower().replace('&', '').replace(',', '').replace('  ', ' ').replace(' ', '-')
    correct_anchor = re.sub(r'[^\w\s-]', '', category.lower()).replace(' ', '-')
    index_text = index_text.replace(f'](#{old_anchor})', f'](#{correct_anchor})')
if index_text.encode('utf-8') != original_bytes:
    original_index.parent.mkdir(exist_ok=True)
    if not original_index.exists():
        original_index.write_bytes(original_bytes)
    index_path.write_text(index_text, encoding='utf-8')
    save('presentation-fixes.json', {'change': 'Corrected only internal category navigation anchors in PROJECT_INDEX.md.',
                                   'original_snapshot': 'independent-snapshot/PROJECT_INDEX.md',
                                   'original_sha256': hashlib.sha256(original_bytes).hexdigest(),
                                   'current_sha256': hashlib.sha256(index_path.read_bytes()).hexdigest()})
comparison_started = now()
old_catalog = read(OLD / 'project-catalog.json')
new_catalog = read(OUT / 'project-catalog.json')
old = {normal(p['path']): p for p in old_catalog['projects']}
new = {normal(p['path']): p for p in new_catalog['projects']}
assert len(old) == len(old_catalog['projects'])
shared = sorted(old.keys() & new.keys())
only_old = sorted(old.keys() - new.keys())
only_new = sorted(new.keys() - old.keys())
boundaries = read(OUT / 'project-boundaries.json')
omitted = {normal(p['path']): p for p in boundaries['omitted_workspaces']}
old_only = []
new_only = []
for path in only_old:
    descendants = [new[k]['path'] for k in new if k.startswith(path + '/')]
    parents = [k for k in new if path.startswith(k + '/')]
    if path in omitted:
        reason, mapped = 'empty-folder-excluded', []
    elif descendants:
        reason, mapped = 'container-expanded', sorted(descendants)
    elif parents:
        reason, mapped = 'component-grouped-into-workspace', [new[max(parents, key=len)]['path']]
    else:
        reason, mapped = 'unmatched-needs-review', []
    old_only.append({'old_id': old[path]['id'], 'path': relative(old[path]['path']), 'reason': reason, 'new_paths': mapped})
for path in only_new:
    parents = [k for k in old if path.startswith(k + '/')]
    children = [old[k]['path'] for k in old if k.startswith(path + '/')]
    if parents:
        reason, mapped = 'expanded-from-old-container', [relative(old[max(parents, key=len)]['path'])]
    elif children:
        reason, mapped = 'grouped-old-components', [relative(k) for k in children]
    else:
        reason, mapped = 'new-coverage', []
    new_only.append({'new_id': new[path]['project_id'], 'path': new[path]['path'], 'reason': reason, 'old_paths': mapped})

changes = []
crosswalk = []
for key in shared:
    a, b = old[key], new[key]
    crosswalk.append({'old_id': a['id'], 'new_id': b['project_id'], 'path': b['path'], 'match': 'normalized-desktop-path'})
    changes.append({'path': b['path'], 'old_id': a['id'], 'new_id': b['project_id'],
        'old_purpose': a['purpose'], 'new_purpose': b['purpose'],
        'old_state': a['apparent_state'], 'new_state': b['apparent_state'],
        'old_category': a['category'], 'new_category': b['category'],
        'old_languages': a.get('languages', []), 'new_languages': b['stack']['languages'],
        'old_frameworks': a.get('frameworks', []), 'new_frameworks': b['stack']['frameworks'],
        'old_recorded_evidence_count': len(a.get('inspected_files', [])),
        'new_recorded_evidence_count': sum(len(v) for v in b['evidence'].values() if isinstance(v, list)),
        'new_evidence': b['evidence']})
old_evidence = sum(bool(p.get('inspected_files')) for p in old.values())
new_evidence = sum(any(v for v in p['evidence'].values() if isinstance(v, list)) for p in new.values())
state_changes = [item for item in changes if item['old_state'] != item['new_state']]
old_related = sum(bool(p.get('related_projects')) for p in old.values())
new_related = sum(bool(p['repository']['related_projects']) for p in new.values())
old_duplicate_ids = [identifier for identifier, n in Counter(p['id'] for p in old.values()).items() if n > 1]
stats = {'old_records': len(old), 'new_records': len(new), 'net_record_change': len(new) - len(old),
         'exact_path_matches': len(shared), 'old_only_paths': len(old_only), 'new_only_paths': len(new_only),
         'old_only_reasons': dict(Counter(p['reason'] for p in old_only)),
         'new_only_reasons': dict(Counter(p['reason'] for p in new_only)),
         'changed_apparent_states_on_shared_paths': len(state_changes),
         'old_records_with_file_evidence': old_evidence, 'new_records_with_file_evidence': new_evidence,
         'old_records_with_relationships': old_related, 'new_records_with_relationships': new_related,
         'old_duplicate_ids': old_duplicate_ids}
save('comparison-details.json', {'comparison_started_at': comparison_started,
    'independent_baseline_completed_at': baseline['independent_inventory_completed_at'],
    'old_catalog_sha256': hashlib.sha256((OLD / 'project-catalog.json').read_bytes()).hexdigest(),
    'statistics': stats, 'old_only': old_only, 'new_only': new_only, 'shared_record_differences': changes})
save('project-id-crosswalk.json', {'exact_matches': crosswalk, 'scope_changes': {'old_only': old_only, 'new_only': new_only}})

lines = ['# AstraOrganized vs. AstraOrganized2', '',
    f'**The independent inventory contains {len(new)} records versus {len(old)} in the earlier catalog: a net increase of {len(new)-len(old)}.** This is mainly a difference in grouping, not evidence that 47 new applications appeared.', '',
    'The new inventory was completed and hashed before `AstraOrganized` was opened. Its assessments have not been changed using the earlier catalog. See [the baseline checkpoint](independent-baseline.json). The original index is retained in `independent-snapshot`; only its navigation anchors were subsequently corrected.', '',
    '## Main differences', '', '| Area | AstraOrganized | AstraOrganized2 |', '|---|---|---|',
    '| `geminiorganized` | One container record | 78 project/resource records, with copied versions visible |',
    '| `gitvg` | One container record | 17 independently versioned projects plus the `astra` learning collection |',
    '| `jsharness` | One container record | Separate `ctvodejs` and `VTCode` repositories |',
    '| `newcodexJS` | 22 rows: 20 practice apps, `docs`, and `scripts` | One workspace record with component paths in JSON |',
    '| Empty folders counted by the earlier catalog | 27 project rows | Listed in coverage notes rather than counted as projects |',
    f'| Records with explicit inspected-file references | {old_evidence} of {len(old)} | {new_evidence} of {len(new)} |',
    '| Relationships | Primarily similar-name relationships | 56 likely copy/version groups based on matching multi-file samples |',
    '| Grouping for browsing | Mostly Desktop folder/category names | Project purpose/type, plus a location summary |',
    '| IDs and paths | Readable `proj-...` IDs and absolute paths | UUIDs, Desktop-relative paths, and absolute paths |', '',
    '**Count reconciliation:** 341 − 27 empty-folder rows − 3 container rows − 22 `newcodexJS` rows + 78 Gemini records + 18 `gitvg` records + 2 `jsharness` records + 1 `newcodexJS` workspace = **388**.', '',
    'The earlier index is more convenient if you want each `newcodexJS` exercise shown as its own row. The new index is more useful for seeing the separate repositories inside the larger containers and identifying copied versions. Neither row count is a count of unique, production-ready applications.', '',
    '## Matching and assessment changes', '',
    f'- **{len(shared)} records match by normalized Desktop path.** The 99 new-only paths and 52 old-only paths are fully explained by the scope changes above.',
    f'- **{len(state_changes)} shared records have different apparent-state labels.** The new labels use sampled code and configuration. These differences are not runtime test results and do not prove that a project became working or broken.',
    '- Stack detail is stored differently: the new catalog separates languages, frameworks, data stores, infrastructure, testing, and integrations. Comparing raw tag counts would be misleading.',
    '- Missing inspected-file references in the older JSON mean the evidence was not recorded there; they do not establish that no files were inspected.',
    '- The older catalog reuses three IDs across different paths: `proj-nethris`, `proj-aiapplybot`, and `proj-new-folder`. New IDs are unique. When joining catalogs, use the path-aware crosswalk rather than the old ID alone.',
    '- Neither inventory runs projects. The new inventory also records documentation caveats, including archived sources, scaffolds, mocked services, and unimplemented plans.', '',
    '## Examples of clarified descriptions', '', '| Project | Earlier description | New description |', '|---|---|---|']
examples = ['.netarchitectureproject', 'buildsmallplates', '_Organized Desktop/03 Master Projects/masterrnative',
            '_Organized Desktop/05 Numbered Experiments/ww49', '_Organized Desktop/02 Build Projects/buildjira']
for path in examples:
    key = normal(path)
    if key in old and key in new:
        lines.append('| ' + folder(path) + ' | ' + cell(old[key]['purpose']) + ' | ' + cell(new[key]['purpose']) + ' |')
lines.extend(['', '## Evidence and limitations', '',
    '- The independent scan covered 100,421 directories and 415,133 files after exclusions, and accounted for all 108 discovered Git roots.',
    '- All 24 initial long-path errors were recovered. Every catalog evidence/material path and relationship reference passed validation.',
    '- Matching sample fingerprints indicate likely copies or versions; the full source trees were not byte-compared. Changed copies may not be linked.',
    '- The comparison reads the two saved catalogs. It does not reinterpret differences as confirmed feature changes, and it does not merge the older assessments into the independent catalog.',
    '- UUIDs differ from the older IDs. Use [the ID crosswalk](project-id-crosswalk.json) to join the 289 exact path matches and inspect changed project boundaries.', '',
    '## Full difference data', '',
    '- [Independent project index](PROJECT_INDEX.md)',
    '- [Machine-readable field differences and coverage changes](comparison-details.json)',
    '- [ID crosswalk and scope mappings](project-id-crosswalk.json)',
    '- [Independent validation](inventory-validation.json)', '',
    '## Empty-folder rows removed from the project count', ''])
for item in old_only:
    if item['reason'] == 'empty-folder-excluded':
        lines.append('- ' + folder(item['path']))
lines.extend(['', '## New records within expanded containers', ''])
for item in new_only:
    lines.append('- ' + folder(item['path']))
(OUT / 'COMPARISON_REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
verify_baseline()
assert not any(p['reason'] == 'unmatched-needs-review' for p in old_only)
assert not any(p['reason'] == 'new-coverage' for p in new_only)
progress = read(OUT / 'analysis-progress.json')
progress.update({'phase': 'complete', 'updated_at': now(), 'astraorganized_read': True,
                 'comparison_started_at': comparison_started, 'independent_baseline_preserved': True,
                 'comparison_report': 'COMPARISON_REPORT.md', 'next_action': None})
save('analysis-progress.json', progress)
(OUT / 'README.md').write_text('''# Desktop inventory and comparison

Start here:

- [PROJECT_INDEX.md](PROJECT_INDEX.md) — the independent overview of 388 projects and resource collections.
- [COMPARISON_REPORT.md](COMPARISON_REPORT.md) — differences from AstraOrganized.
- [project-catalog-summary.json](project-catalog-summary.json) — compact data for filtering.
- [project-catalog.json](project-catalog.json) — full records, evidence, components, caveats, and IDs.

The independent inventory was completed before AstraOrganized was opened. Its original hashes are saved in independent-baseline.json and were verified after comparison. The original index is preserved in independent-snapshot; only navigation anchors were corrected in the displayed copy. Existing projects and the AstraOrganized folder were not modified.

Supporting JSON files preserve discovery, exclusions, validation, differences, and resumable state. Scripts document the analysis. No project was installed, built, tested, or run.
''', encoding='utf-8')
save('comparison-validation.json', {'validated_at': now(), 'valid': True, 'baseline_hashes_unchanged': True,
                                  'all_old_only_paths_explained': True, 'all_new_only_paths_explained': True,
                                  'exact_path_matches': len(shared), 'old_only': len(old_only), 'new_only': len(new_only)})
print(json.dumps(stats, ensure_ascii=False))
