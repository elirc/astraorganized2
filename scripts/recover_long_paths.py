"""Retry only failed directory reads using Windows extended-length paths."""
from pathlib import Path
import os
import json
from collections import Counter
from scan_desktop import ROOT, OUT, SKIP_DIRS, SOURCE_EXT, DOC_EXT, MARKERS, save, now

index = json.loads((OUT / 'scan-index.json').read_text(encoding='utf-8'))
coverage = json.loads((OUT / 'scan-exclusions.json').read_text(encoding='utf-8'))
stack = [entry['path'] for entry in coverage['errors']]
original_errors = coverage['errors']
errors = []
recovered = []
while stack:
    relative = stack.pop()
    if relative in index['directories']:
        continue
    extended = '\\\\?\\' + str(ROOT / relative).replace('/', '\\')
    try:
        entries = sorted(os.scandir(extended), key=lambda item: item.name.lower())
    except OSError as error:
        errors.append({'path': relative, 'error': str(error)})
        continue
    files, children, markers = [], [], []
    extensions = Counter()
    git = False
    for entry in entries:
        child_rel = relative + '/' + entry.name
        lower = entry.name.lower()
        try:
            if entry.is_symlink():
                coverage['skipped'].append({'path': child_rel, 'reason': 'Link; not followed'})
            elif lower == '.git':
                git = True
            elif entry.is_dir(follow_symlinks=False):
                if lower in SKIP_DIRS:
                    coverage['skipped'].append({'path': child_rel, 'reason': 'Dependency/generated directory'})
                elif entry.stat(follow_symlinks=False).st_file_attributes & 0x400:
                    coverage['skipped'].append({'path': child_rel, 'reason': 'Reparse point; not followed'})
                else:
                    children.append(entry.name)
                    stack.append(child_rel)
            elif entry.is_file(follow_symlinks=False):
                files.append(entry.name)
                ext = Path(entry.name).suffix.lower()
                extensions[ext] += 1
                if lower in MARKERS or ext in {'.sln', '.slnx', '.csproj', '.fsproj'}:
                    markers.append(entry.name)
        except OSError as error:
            errors.append({'path': child_rel, 'error': str(error)})
    index['directories'][relative] = {'files': files, 'directories': children, 'markers': markers, 'git': git,
        'source_files': sum(n for ext, n in extensions.items() if ext in SOURCE_EXT),
        'document_files': sum(n for ext, n in extensions.items() if ext in DOC_EXT)}
    recovered.append(relative)
index['completed_at'] = now()
coverage['errors'] = errors
coverage['recovered_long_paths'] = recovered
coverage['original_long_path_errors'] = original_errors
save('scan-index.json', index)
save('scan-exclusions.json', coverage)
print(json.dumps({'recovered_directories': len(recovered), 'remaining_errors': len(errors),
                  'directories': len(index['directories']), 'files': sum(len(x['files']) for x in index['directories'].values())}))
