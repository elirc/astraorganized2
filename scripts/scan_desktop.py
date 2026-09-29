"""Read-only discovery. Never opens AstraOrganized during the inventory phase."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import json
import os
import time

ROOT = Path('C:/Users/Owner/Desktop')
OUT = ROOT / 'AstraOrganized2'
EXCLUDED_ROOTS = {'astraorganized', 'astraorganized2', 'project-inventory'}
SKIP_DIRS = {
    '.git', 'node_modules', '.venv', 'venv', 'env', '__pycache__',
    '.next', '.nuxt', '.output', '.svelte-kit', '.astro', '.angular',
    '.turbo', '.cache', 'coverage', 'dist', 'build', 'target', 'bin', 'obj',
    '.vs', '.idea', '.vscode', '.gradle', '.dart_tool', 'pods',
    'bower_components', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    'test-results', 'playwright-report', 'artifacts', '.parcel-cache',
    '.terraform', '.serverless', '.vercel', '.netlify', '.yarn', '.pnpm-store',
    '.codex', '.claude', '.gemini', '.agent', '.agents', '.cursor',
}
SOURCE_EXT = {'.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.py', '.cs', '.fs',
              '.go', '.rs', '.java', '.kt', '.swift', '.php', '.rb', '.vue',
              '.svelte', '.html', '.css', '.scss', '.sql', '.sh', '.ps1',
              '.ipynb', '.dart', '.c', '.cpp', '.h', '.razor', '.cshtml'}
DOC_EXT = {'.md', '.mdx', '.rst', '.txt', '.pdf', '.docx', '.html', '.ipynb'}
MARKERS = {'package.json', 'pyproject.toml', 'requirements.txt', 'cargo.toml',
           'go.mod', 'composer.json', 'gemfile', 'pom.xml', 'build.gradle',
           'pubspec.yaml', 'cmakelists.txt', 'dockerfile', 'manage.py',
           'pnpm-workspace.yaml', 'lerna.json', 'nx.json', 'angular.json'}

def now():
    return datetime.now(timezone.utc).isoformat()

def save(name, value):
    path = OUT / name
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(temporary, path)

def main():
    started = now()
    directories = {}
    skipped = []
    errors = []
    counts = Counter()
    stack = [ROOT]
    last_checkpoint = time.monotonic()
    while stack:
        path = stack.pop()
        relative = path.relative_to(ROOT).as_posix()
        try:
            entries = sorted(os.scandir(path), key=lambda item: item.name.lower())
        except OSError as error:
            errors.append({'path': relative, 'error': str(error)})
            continue
        files, children, markers = [], [], []
        extensions = Counter()
        git = False
        for entry in entries:
            child = Path(entry.path)
            child_rel = child.relative_to(ROOT).as_posix()
            lower = entry.name.lower()
            if path == ROOT and lower in EXCLUDED_ROOTS:
                skipped.append({'path': child_rel, 'reason': 'Excluded before entry: independent inventory or output folder'})
                continue
            try:
                if entry.is_symlink() or child.is_junction():
                    skipped.append({'path': child_rel, 'reason': 'Link or junction; not followed'})
                    continue
                if lower == '.git':
                    git = True
                    skipped.append({'path': child_rel, 'reason': 'Git metadata; root presence recorded'})
                    continue
                if entry.is_dir(follow_symlinks=False):
                    if lower in SKIP_DIRS:
                        skipped.append({'path': child_rel, 'reason': 'Dependency, generated output, cache, or editor/agent state'})
                    else:
                        children.append(entry.name)
                        stack.append(child)
                elif entry.is_file(follow_symlinks=False):
                    files.append(entry.name)
                    extension = child.suffix.lower()
                    extensions[extension] += 1
                    if lower in MARKERS or extension in {'.sln', '.slnx', '.csproj', '.fsproj'}:
                        markers.append(entry.name)
            except OSError as error:
                errors.append({'path': child_rel, 'error': str(error)})
        directories[relative] = {
            'files': files, 'directories': children, 'git': git, 'markers': markers,
            'source_files': sum(count for ext, count in extensions.items() if ext in SOURCE_EXT),
            'document_files': sum(count for ext, count in extensions.items() if ext in DOC_EXT),
        }
        counts['directories'] += 1
        counts['files'] += len(files)
        counts['git_roots'] += git
        if time.monotonic() - last_checkpoint > 15:
            save('analysis-progress.json', {
                'phase': 'independent-discovery', 'started_at': started,
                'updated_at': now(), 'counts': dict(counts),
                'last_scanned_directory': relative,
                'pending_directories': [p.relative_to(ROOT).as_posix() for p in stack],
                'astraorganized_read': False,
                'next_action': 'Finish metadata discovery, then inspect source samples in batches.'
            })
            print(json.dumps({'phase': 'discovery', **counts, 'current': relative}), flush=True)
            last_checkpoint = time.monotonic()
    save('scan-index.json', {'root': str(ROOT), 'started_at': started, 'completed_at': now(), 'directories': directories})
    save('scan-exclusions.json', {'skipped': skipped, 'errors': errors})
    save('analysis-progress.json', {
        'phase': 'discovery-complete', 'started_at': started, 'updated_at': now(),
        'counts': dict(counts), 'astraorganized_read': False,
        'errors': errors, 'next_action': 'Identify project boundaries and inspect representative files.'
    })
    print(json.dumps({'phase': 'discovery-complete', **counts, 'skipped': len(skipped), 'errors': len(errors)}), flush=True)

if __name__ == '__main__':
    main()
