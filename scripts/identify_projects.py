"""Identify workspace/project boundaries from discovery metadata only."""
from pathlib import Path
from collections import Counter
import json
from scan_desktop import ROOT, OUT, save, now

STRONG = {'package.json', 'pyproject.toml', 'requirements.txt', 'cargo.toml',
          'go.mod', 'composer.json', 'gemfile', 'pom.xml', 'build.gradle',
          'pubspec.yaml', 'cmakelists.txt', 'manage.py'}

def within(path, parent):
    return path == parent or path.startswith(parent + '/')

def main():
    index = json.loads((OUT / 'scan-index.json').read_text(encoding='utf-8'))['directories']
    aggregates = {}
    for path in sorted(index, key=lambda x: x.count('/'), reverse=True):
        item = index[path]
        total = Counter({'source_files': item['source_files'], 'document_files': item['document_files'],
                         'files': len(item['files']), 'git_roots': int(item['git'])})
        for child in item['directories']:
            total.update(aggregates.get(path + '/' + child if path != '.' else child, {}))
        aggregates[path] = dict(total)
    workspaces = []
    for child in index['.']['directories']:
        if child == '_Organized Desktop':
            for category in index.get(child, {}).get('directories', []):
                category_path = child + '/' + category
                for workspace in index.get(category_path, {}).get('directories', []):
                    workspaces.append(category_path + '/' + workspace)
                if index.get(category_path, {}).get('files'):
                    workspaces.append(category_path)
        elif child == 'geminiorganized':
            workspaces.extend(child + '/' + name for name in index.get(child, {}).get('directories', []))
        else:
            workspaces.append(child)
    projects = []
    omitted = []
    for workspace in workspaces:
        dirs = [path for path in index if within(path, workspace)]
        git_roots = sorted((path for path in dirs if index[path]['git']), key=lambda x: (x.count('/'), x.lower()))
        outer_git_roots = []
        for path in git_roots:
            if not any(within(path, parent) for parent in outer_git_roots):
                outer_git_roots.append(path)
        total = aggregates[workspace]
        if not total.get('source_files') and not total.get('document_files') and not git_roots:
            omitted.append({'path': workspace, 'reason': 'No source code, project manifests, or readable/document resources found', 'counts': total})
            continue
        # A product's API, frontend, tests and CI actions are components, not extra projects.
        # Split a wrapper only when it contains multiple independent Git repositories.
        roots = outer_git_roots if len(outer_git_roots) > 1 else [workspace]
        for path in roots:
            projects.append({'path': path, 'workspace': workspace,
                             'boundary': 'independent-nested-git-root' if path != workspace else 'workspace-with-components',
                             'parent_path': None, 'counts': aggregates[path],
                             'git_roots': [git for git in git_roots if within(git, path)]})
    unique = {item['path']: item for item in projects}
    projects = sorted(unique.values(), key=lambda x: x['path'].lower())
    save('project-boundaries.json', {'created_at': now(), 'workspaces': workspaces,
                                   'projects': projects, 'omitted_workspaces': omitted})
    with (OUT / 'boundary-review.txt').open('w', encoding='utf-8') as stream:
        for n, project in enumerate(projects, 1):
            counts = project['counts']
            stream.write(f"{n:03d} | {project['path']} | {project['boundary']} | source={counts.get('source_files', 0)} docs={counts.get('document_files', 0)} | workspace={project['workspace']}\n")
    print(json.dumps({'workspaces': len(workspaces), 'projects': len(projects), 'omitted': len(omitted)}))

if __name__ == '__main__':
    main()
