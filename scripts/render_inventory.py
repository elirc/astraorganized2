from pathlib import Path
from collections import Counter
from urllib.parse import quote
import json
import hashlib
from scan_desktop import ROOT, OUT, SOURCE_EXT, save, now

catalog = json.loads((OUT / 'project-catalog.json').read_text(encoding='utf-8'))
projects = catalog['projects']
scan = json.loads((OUT / 'scan-index.json').read_text(encoding='utf-8'))
index = scan['directories']
coverage = json.loads((OUT / 'scan-exclusions.json').read_text(encoding='utf-8'))
boundaries = json.loads((OUT / 'project-boundaries.json').read_text(encoding='utf-8'))
duplicates = json.loads((OUT / 'likely-duplicates.json').read_text(encoding='utf-8'))['groups']

def cell(text):
    return str(text).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')

def link(path, label=None):
    return '[' + cell(label or path) + '](../' + quote(path, safe='/') + ')'

def location(path):
    if path.startswith('_Organized Desktop/'):
        return '/'.join(path.split('/')[:2])
    if path.startswith('geminiorganized/'):
        return 'geminiorganized'
    return 'Desktop directly'

ids = {p['project_id'] for p in projects}
assert len(ids) == len(projects), 'Duplicate project IDs'
assert len({p['path'].casefold() for p in projects}) == len(projects), 'Duplicate record paths'
assert not any(p['path'].casefold().startswith(('astraorganized/', 'astraorganized2/')) for p in projects)
file_paths = {path + '/' + name for path, item in index.items() for name in item['files']}
broken = []
for project in projects:
    assert project['path'] in index, project['path']
    assert project['purpose'].strip(), project['path']
    for key, paths in project['evidence'].items():
        if isinstance(paths, list):
            broken.extend(path for path in paths if path not in file_paths)
    broken.extend(path for path in project['learning_material']['key_paths'] if path not in file_paths)
    assert all(item['project_id'] in ids for item in project['repository']['related_projects'])
assert not broken, broken[:10]
assigned_git = {path for p in projects for path in p['repository']['git_roots']}
discovered_git = {path for path, item in index.items() if item['git']}
assert assigned_git == discovered_git, sorted(discovered_git - assigned_git)
roots = {p['path'] for p in projects}
unassigned = []
for path, item in index.items():
    if not item['source_files']:
        continue
    if not any('/'.join(path.split('/')[:i]) in roots for i in range(1, len(path.split('/')) + 1)):
        for name in item['files']:
            if Path(name).suffix.lower() in SOURCE_EXT:
                unassigned.append(path + '/' + name)
assert unassigned == ['gitvg/tools/publish-organized-projects.ps1'], unassigned
assert not coverage['errors'], 'Unresolved scan errors'
software = sum(p['record_kind'] == 'software-project-or-workspace' for p in projects)
resource = len(projects) - software
categories = Counter(p['category'] for p in projects)
regions = Counter(location(p['path']) for p in projects)
learning = sum(bool(p['learning_material']['key_paths']) for p in projects)
sample_count = sum(sum(len(v) for v in p['evidence'].values() if isinstance(v, list)) for p in projects)
validation = {'validated_at': now(), 'valid': True, 'records': len(projects), 'software_workspaces': software,
              'learning_or_reference_collections': resource, 'git_roots_covered': len(assigned_git),
              'directories_scanned': len(index), 'files_discovered': sum(len(x['files']) for x in index.values()),
              'sampled_file_references': sample_count, 'broken_evidence_paths': [], 'unresolved_scan_errors': [],
              'unassigned_source_files': [{'path': p, 'reason': 'Workspace publishing helper, not a separate project; not executed.'} for p in unassigned],
              'likely_duplicate_groups': len(duplicates), 'projects_with_learning_paths': learning,
              'checks': ['Unique IDs and paths', 'All referenced source/learning paths present in discovery',
                         'All Git roots covered', 'Relationship references resolve', 'All source directories accounted for',
                         'No AstraOrganized paths in independent inventory']}
save('inventory-validation.json', validation)
summary = [{k: p[k] for k in ['project_id', 'name', 'path', 'category', 'purpose', 'apparent_state', 'record_kind']} |
           {'primary_stack': p['stack']['languages'][:3] + p['stack']['frameworks'][:4],
            'has_learning_material': bool(p['learning_material']['key_paths']),
            'related_project_ids': [r['project_id'] for r in p['repository']['related_projects']]} for p in projects]
save('project-catalog-summary.json', {'schema_version': 1, 'projects': summary})

lines = ['# Desktop project inventory', '',
    f'**{len(projects)} records: {software} software projects/workspaces and {resource} learning/reference collections.**', '',
    f'This independent snapshot covers **{len(assigned_git)} Git roots** and **{len(duplicates)} likely copy/version groups**. It was built without opening `AstraOrganized`.', '',
    'Projects remain in their original locations. This folder contains the inventory and comparison reports only.', '',
    'Use the category links below or search this file for a project, language, or topic. For automation, start with [the compact JSON catalog](project-catalog-summary.json); [the full catalog](project-catalog.json) includes evidence, components, caveats, and stable IDs.', '',
    '## How to read this', '',
    '- Purpose summarizes local documentation and targeted source/UI inspection. It is not a promise that every documented feature is implemented.',
    '- **Working-looking** means recognizable application code and configuration were present. Nothing was installed, built, tested, or run for this inventory.',
    '- **Partial**, **tutorial**, and **unknown** are conservative static-inspection labels, not a quality ranking.',
    '- APIs, frontends, test projects, and CI helpers are normally components of one workspace. Independently versioned repositories inside a shared folder get separate records.',
    '- Learning links are selected by descriptive names and limited text sampling. PDF, DOCX, and ODT resources are listed by filename, not scored or exhaustively read.', '',
    '## Coverage by location', '', '| Location | Records |', '|---|---:|']
for name, count in sorted(regions.items()):
    lines.append(f'| {cell(name)} | {count} |')
lines.extend(['', '## Categories', ''])
for name, count in sorted(categories.items()):
    anchor = name.lower().replace('&', '').replace(',', '').replace('  ', ' ').replace(' ', '-')
    lines.append(f'- [{name}](#{anchor}) — {count}')
for category in sorted(categories):
    lines.extend(['', '## ' + category, '', '| Project / location | Purpose | Main stack | Apparent state | Learning |', '|---|---|---|---|---|'])
    for p in (p for p in projects if p['category'] == category):
        tech = list(dict.fromkeys(p['stack']['frameworks'] + p['stack']['data'] + p['stack']['languages']))[:7]
        learn = p['learning_material']['key_paths']
        learning_link = link(learn[0], 'Material') + f" ({p['learning_material']['matching_resource_count']} paths)" if learn else '—'
        related = ' · possible copy/version' if p['repository']['related_projects'] else ''
        label = p['path']
        lines.append('| ' + ' | '.join([link(p['path'], label), cell(p['purpose'] + related), cell(', '.join(tech) or 'Documents / no stack established'), cell(p['apparent_state']), learning_link]) + ' |')
lines.extend(['', '## Likely copies and versions', '',
    'Matching groups below share the contents of multiple selected manifests, README files, and source samples. **These are not complete byte-for-byte tree comparisons.** Modified copies may not appear here.', ''])
for n, group in enumerate(duplicates, 1):
    lines.append(f"{n}. " + ' ↔ '.join(link(path) for path in group['paths']))
lines.extend(['', '## Coverage notes and exclusions', '',
    f"- Discovery covered {len(index):,} directories and {validation['files_discovered']:,} files after dependency/cache/build exclusions.",
    '- `AstraOrganized`, `AstraOrganized2`, and `project-inventory` were excluded from discovery. Existing inventory READMEs found elsewhere were recognized as reference artifacts and not used to derive project records.',
    '- Directory links/junctions were not followed. Archives and binary contents were not unpacked or inspected.',
    f"- {len(coverage.get('original_long_path_errors', []))} initial long-path errors were retried successfully with extended Windows paths; there are no unresolved scan errors.",
    f"- {len(boundaries['omitted_workspaces'])} folders had no recognized project or document content after exclusions; they are listed below.",
    '- Loose category-level files are listed in [loose-resources.json](loose-resources.json). The one unassigned code file is the `gitvg/tools/publish-organized-projects.ps1` workspace helper; it was not run.',
    '- See [validation results](inventory-validation.json), [scan exclusions](scan-exclusions.json), and [resumable progress](analysis-progress.json).', '',
    '| Folder without project content | Files seen |', '|---|---:|'])
for item in boundaries['omitted_workspaces']:
    lines.append(f"| {link(item['path'])} | {item['counts']['files']} |")
(OUT / 'PROJECT_INDEX.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')

baseline_files = ['project-catalog.json', 'project-catalog-summary.json', 'PROJECT_INDEX.md', 'likely-duplicates.json', 'inventory-validation.json']
baseline = {'independent_inventory_completed_at': now(), 'astraorganized_read_before_completion': False,
            'record_count': len(projects), 'files': {name: hashlib.sha256((OUT / name).read_bytes()).hexdigest() for name in baseline_files}}
save('independent-baseline.json', baseline)
save('analysis-progress.json', {'phase': 'independent-inventory-complete', 'updated_at': now(), 'astraorganized_read': False,
                              'projects_reviewed': len(projects), 'completed_project_ids': sorted(ids),
                              'remaining_project_paths': [], 'unresolved_scan_errors': [],
                              'next_action': 'Only now inspect AstraOrganized and write a separate comparison without changing the independent baseline.'})
print(json.dumps(validation))
