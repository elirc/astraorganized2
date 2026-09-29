from pathlib import Path
import json
import re
from scan_desktop import OUT, ROOT
from analyze_projects import readable

catalog = json.loads((OUT / 'project-catalog.json').read_text(encoding='utf-8'))
index = json.loads((OUT / 'scan-index.json').read_text(encoding='utf-8'))['directories']
bad = re.compile(r'(?i)(Open http|Open your browser|specific purpose is unclear|Welcome friends|official plugins|This curriculum|If multi.tenancy|This separation|production.style learning project built|production.style learning project for backend|Enterprise.style internal workflow|two separate production|backend.heavy structure|reviewed pull request|This is a Convex|51 lessons|passive.to.active|Almost every refactor|Course [35]|Double.click|Source plans this|Execution playbooks|10.week plan)')
focus = {'masterrnative', 'jstrain2', 'j3', 'ww6', 'z7', 'z8', 'z9', 'zz1', 'grokbuildppmproject', 'jobtrack'}
lines = []
for project in catalog['projects']:
    if not bad.search(project['purpose']) and project['name'] not in focus:
        continue
    # Equivalent copies will get the same purpose fix, so avoid redundant review output.
    if project['path'].startswith('geminiorganized/'):
        continue
    lines.append('\nPATH: ' + project['path'])
    for path in project['evidence']['documentation_inspected'][:1]:
        content = readable(path, 16000)
        headings = [line for line in content.splitlines() if line.startswith('#')][:5]
        lines.append('README headings: ' + ' | '.join(headings))
    sample = list(project['evidence']['source_files_inspected'][:3])
    for suffix in ['src/app/page.tsx', 'app/page.tsx', 'src/App.tsx', 'src/App.jsx', 'index.html']:
        candidate = project['path'] + '/' + suffix
        if (ROOT / candidate).is_file() and candidate not in sample:
            sample.insert(0, candidate)
    picked = []
    for path in sample[:4]:
        text = readable(path, 40000)
        snippets = [line.strip() for line in text.splitlines() if re.search(r'(?i)(<h1|<title|title:|description:|heading=|appname|applicationname|class \w+Application|system.out.println)', line)]
        if snippets:
            picked.append(Path(path).relative_to(project['path']).as_posix() + ': ' + ' | '.join(snippets[:4])[:500])
    lines.extend(picked)
    components = project['repository']['components'][:10]
    lines.append('Components: ' + ', '.join(Path(path).relative_to(project['path']).as_posix() for path in components))
    if not picked:
        direct = index.get(project['path'], {})
        lines.append('Top files/folders: ' + ', '.join(direct.get('files', [])[:12] + direct.get('directories', [])[:12]))
(OUT / 'ambiguous-review.txt').write_text('\n'.join(lines), encoding='utf-8')
print('\n'.join(lines))
