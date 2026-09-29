"""Lightweight static inspection; does not execute or change any project."""
from pathlib import Path
from collections import Counter, defaultdict
import hashlib
import json
import re
import uuid
from scan_desktop import ROOT, OUT, SOURCE_EXT, save, now
from identify_projects import within

NAMESPACE = uuid.UUID('d4f4aec4-1a73-4b15-9945-dcc7a4f87835')
REPORT_NAMES = {'project_index.md', 'project-catalog.json', 'project-catalog-summary.json',
                'analysis-progress.json', 'core_project_collection.md',
                'personal_swe_curriculum.md', 'codebase_learning_map.md'}
LANGUAGES = {'.ts': 'TypeScript', '.tsx': 'TypeScript', '.js': 'JavaScript', '.jsx': 'JavaScript',
             '.mjs': 'JavaScript', '.cjs': 'JavaScript', '.py': 'Python', '.cs': 'C#', '.fs': 'F#',
             '.go': 'Go', '.rs': 'Rust', '.java': 'Java', '.kt': 'Kotlin', '.swift': 'Swift',
             '.php': 'PHP', '.rb': 'Ruby', '.vue': 'Vue', '.svelte': 'Svelte', '.html': 'HTML',
             '.css': 'CSS', '.scss': 'SCSS', '.sql': 'SQL', '.dart': 'Dart', '.c': 'C', '.cpp': 'C++',
             '.razor': 'Razor', '.cshtml': 'Razor', '.ipynb': 'Jupyter'}
DEPENDENCIES = {
    'react': ('frameworks', 'React'), 'next': ('frameworks', 'Next.js'), 'vite': ('frameworks', 'Vite'),
    'express': ('frameworks', 'Express'), 'fastify': ('frameworks', 'Fastify'), '@nestjs/core': ('frameworks', 'NestJS'),
    'hono': ('frameworks', 'Hono'), 'vue': ('frameworks', 'Vue'), 'nuxt': ('frameworks', 'Nuxt'),
    'svelte': ('frameworks', 'Svelte'), '@sveltejs/kit': ('frameworks', 'SvelteKit'),
    '@angular/core': ('frameworks', 'Angular'), 'astro': ('frameworks', 'Astro'),
    'react-native': ('frameworks', 'React Native'), 'expo': ('frameworks', 'Expo'),
    'electron': ('frameworks', 'Electron'), 'tailwindcss': ('frameworks', 'Tailwind CSS'),
    'typescript': ('languages', 'TypeScript'), 'django': ('frameworks', 'Django'),
    'flask': ('frameworks', 'Flask'), 'fastapi': ('frameworks', 'FastAPI'),
    'streamlit': ('frameworks', 'Streamlit'), 'axum': ('frameworks', 'Axum'),
    'laravel/framework': ('frameworks', 'Laravel'), 'actix-web': ('frameworks', 'Actix Web'),
    '@supabase/supabase-js': ('data', 'Supabase'), 'supabase': ('data', 'Supabase'),
    'pg': ('data', 'PostgreSQL'), 'psycopg': ('data', 'PostgreSQL'), 'psycopg2': ('data', 'PostgreSQL'),
    'psycopg2-binary': ('data', 'PostgreSQL'), 'npgsql': ('data', 'PostgreSQL'),
    'mysql2': ('data', 'MySQL'), 'mysql': ('data', 'MySQL'), 'pymysql': ('data', 'MySQL'),
    'sqlite3': ('data', 'SQLite'), 'better-sqlite3': ('data', 'SQLite'),
    'mongoose': ('data', 'MongoDB'), 'mongodb': ('data', 'MongoDB'), 'pymongo': ('data', 'MongoDB'),
    '@prisma/client': ('data', 'Prisma'), 'prisma': ('data', 'Prisma'),
    'drizzle-orm': ('data', 'Drizzle'), 'sqlalchemy': ('data', 'SQLAlchemy'),
    'redis': ('data', 'Redis'), 'ioredis': ('data', 'Redis'), 'dexie': ('data', 'IndexedDB / Dexie'),
    'firebase': ('data', 'Firebase'), 'firebase-admin': ('data', 'Firebase'),
    'vitest': ('testing', 'Vitest'), 'jest': ('testing', 'Jest'),
    '@playwright/test': ('testing', 'Playwright'), 'playwright': ('testing', 'Playwright'),
    'cypress': ('testing', 'Cypress'), 'pytest': ('testing', 'pytest'),
    'xunit': ('testing', 'xUnit'), 'nunit': ('testing', 'NUnit'), 'moq': ('testing', 'Moq'),
    'openai': ('integrations', 'OpenAI API'), '@anthropic-ai/sdk': ('integrations', 'Anthropic API'),
    'anthropic': ('integrations', 'Anthropic API'), '@google/generative-ai': ('integrations', 'Gemini API'),
    '@google/genai': ('integrations', 'Gemini API'), 'langchain': ('integrations', 'LangChain'),
    'llama-index': ('integrations', 'LlamaIndex'), '@modelcontextprotocol/sdk': ('integrations', 'MCP'),
    'stripe': ('integrations', 'Stripe'), 'twilio': ('integrations', 'Twilio'),
    'socket.io': ('integrations', 'Socket.IO'), 'bullmq': ('integrations', 'BullMQ'),
    'celery': ('integrations', 'Celery'), 'boto3': ('infrastructure', 'AWS SDK'),
}
LEARNING = re.compile(r'(?i)(curricul|upskill|learn|lesson|exercise|tutorial|walkthrough|training|study.guide|interview|onboarding|architecture|roadmap|workbook|syllabus)')

def readable(path, limit=16000):
    relative = Path(path)
    if relative.parts[0].lower() in {'astraorganized', 'astraorganized2', 'project-inventory'}:
        raise ValueError('Independent analysis cannot read an excluded folder: ' + path)
    if relative.name.lower() in REPORT_NAMES or relative.name.lower().startswith('.env'):
        return ''
    try:
        with (ROOT / relative).open('rb') as stream:
            raw = stream.read(limit)
        if b'\x00' in raw[:500]:
            return ''
        text = raw.decode('utf-8-sig', errors='replace')
        text = re.sub(r'(?i)(?:sk-[A-Za-z0-9_-]{16,}|AKIA[A-Z0-9]{16}|gh[pousr]_[A-Za-z0-9_]{20,})', '[REDACTED]', text)
        return text
    except OSError:
        return ''

def purpose_from_readme(text):
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    paragraphs = re.split(r'\n\s*\n', text)
    for paragraph in paragraphs:
        paragraph = ' '.join(paragraph.split())
        if not 35 <= len(paragraph) <= 950:
            continue
        if re.match(r'[#|>!*\[\]-]|\d+\.', paragraph):
            continue
        if re.search(r'(?i)(npm (install|run)|git clone|copyright|all rights reserved|license|badge|getting started|table of contents|^https?://|^this is a \[?next|^this template provides)', paragraph):
            continue
        paragraph = re.sub(r'[*_`]', '', paragraph)
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', paragraph)
        return (sentences[0][:280].rstrip() + ('…' if len(sentences[0]) > 280 else ''))
    return ''

def source_score(path, root):
    lower = path.lower()
    base = Path(path).name.lower()
    score = 0
    if re.search(r'(test|spec|fixture|mock|sample|example|generated|migration|\.d\.ts)', lower):
        score -= 35
    if base in {'program.cs', 'app.tsx', 'app.jsx', 'app.vue', 'main.py', 'app.py', 'server.ts', 'server.js', 'main.rs', 'main.go', 'main.dart'}:
        score += 55
    if re.search(r'(controller|endpoint|routes|service|handler)', lower):
        score += 25
    if re.search(r'(auth|order|payment|project|task|chat|study|note|user|customer|job|document)', base):
        score += 10
    if re.search(r'/(src|app|api|server|pages|controllers|services)/', lower):
        score += 10
    if Path(path).suffix.lower() in {'.css', '.scss', '.sql', '.html'}:
        score -= 20
    score -= (len(Path(path).parts) - len(Path(root).parts)) * 2
    return (-score, len(path), path)

def identify_category(stack, purpose, sources, documents, workspace):
    technologies = set(sum(stack.values(), []))
    lower = (purpose + ' ' + workspace).lower()
    if not sources:
        return 'Learning & reference'
    if any(x in technologies for x in {'React Native', 'Expo'}) or any(x in technologies for x in {'Swift', 'Kotlin', 'Dart'}):
        return 'Mobile & desktop'
    if any(x in technologies for x in {'Electron'}):
        return 'Mobile & desktop'
    if re.search(r'\b(game|soccer|spacegame|tagalog)\b', lower):
        return 'Games & language learning'
    if re.search(r'(?i)(ai |llm|agent|rag\b|copilot|assistant|chatbot|harness)', purpose) or any(x in technologies for x in {'OpenAI API', 'Anthropic API', 'Gemini API', 'LangChain', 'LlamaIndex', 'MCP'}):
        return 'AI & developer tools'
    if LEARNING.search(Path(workspace).name) and documents:
        return 'Learning & reference'
    if 'C#' in technologies or 'ASP.NET Core' in technologies:
        return 'C# & .NET'
    frontend = any(x in technologies for x in {'React', 'Next.js', 'Vue', 'Nuxt', 'Angular', 'Svelte', 'SvelteKit'})
    backend = any(x in technologies for x in {'Express', 'Fastify', 'NestJS', 'Django', 'FastAPI', 'Flask', 'Go', 'Rust', 'PHP', 'Laravel'}) or bool(stack['data'])
    if frontend and (backend or 'Next.js' in technologies):
        return 'Full-stack web apps'
    if frontend or {'HTML', 'CSS'} <= technologies:
        return 'Frontend & websites'
    if backend:
        return 'Backend & infrastructure'
    return 'Experiments & utilities'

def analyze(boundary, files, index, all_boundaries):
    root = boundary['path']
    workspace = boundary['workspace']
    nested = [other['path'] for other in all_boundaries if other['path'] != root and within(other['path'], root)]
    owned = [path for path in files if within(path, root) and not any(within(path, child) for child in nested)]
    source = [path for path in owned if Path(path).suffix.lower() in SOURCE_EXT and not path.endswith('.d.ts')]
    docs = [path for path in owned if Path(path).suffix.lower() in {'.md', '.mdx', '.rst', '.txt', '.pdf', '.docx', '.ipynb'} and Path(path).name.lower() not in REPORT_NAMES and Path(path).name.lower() not in {'agents.md', 'claude.md', 'gemini.md', 'license.txt', 'license.md', 'changelog.md'}]
    wrapper_docs = [path for path in files if workspace != root and within(path, workspace) and not within(path, root) and LEARNING.search(path) and Path(path).suffix.lower() in {'.md', '.mdx', '.rst', '.txt', '.pdf', '.docx'} and not any(within(path, other['path']) for other in all_boundaries if other['path'] != root and within(other['path'], workspace))]
    docs = sorted(set(docs + wrapper_docs))
    manifests = [path for path in owned if Path(path).name.lower() in {'package.json', 'pyproject.toml', 'requirements.txt', 'cargo.toml', 'go.mod', 'composer.json', 'gemfile', 'pom.xml', 'build.gradle', 'pubspec.yaml', 'docker-compose.yml', 'docker-compose.yaml', 'compose.yaml', 'dockerfile'} or Path(path).suffix.lower() in {'.csproj', '.fsproj'}]
    manifests.sort(key=lambda path: (path.count('/'), 0 if Path(path).name == 'package.json' else 1, path))
    manifests = manifests[:12]
    readmes = [path for path in owned if Path(path).name.lower() in {'readme.md', 'readme.mdx', 'readme.rst', 'readme.txt'}]
    readmes.sort(key=lambda path: (path.count('/'), len(path)))
    if workspace != root:
        for name in index.get(workspace, {}).get('files', []):
            if name.lower() == 'readme.md':
                readmes.append(workspace + '/' + name)
    readmes = list(dict.fromkeys(readmes))[:3]
    doc_texts = {path: readable(path) for path in readmes}
    purpose = ''
    purpose_evidence = None
    for path, content in doc_texts.items():
        purpose = purpose_from_readme(content)
        if purpose:
            purpose_evidence = path
            break
    stack = {key: [] for key in ['languages', 'frameworks', 'data', 'infrastructure', 'testing', 'integrations']}
    language_counts = Counter(LANGUAGES[Path(path).suffix.lower()] for path in source if Path(path).suffix.lower() in LANGUAGES)
    stack['languages'] = [name for name, count in language_counts.most_common(8)]
    manifest_texts = {}
    scripts = {}
    package_descriptions = []
    for path in manifests:
        content = readable(path, 80000)
        manifest_texts[path] = content
        deps = set()
        if Path(path).name == 'package.json':
            try:
                package = json.loads(content)
                for key in ['dependencies', 'devDependencies', 'peerDependencies']:
                    deps.update(package.get(key, {}))
                scripts.update({key: path for key in package.get('scripts', {})})
                if isinstance(package.get('description'), str):
                    package_descriptions.append((package['description'], path))
                if any(dep in deps for dep in ['express', 'fastify', 'next', '@nestjs/core', 'hono']):
                    stack['frameworks'].append('Node.js')
            except (ValueError, TypeError):
                pass
        else:
            for dep in DEPENDENCIES:
                if re.search(r'(?im)(?:^|[\s"\[\x27>])' + re.escape(dep) + r'(?:[\s"\x27<>=\[\]:,]|$)', content):
                    deps.add(dep)
        for dep in deps:
            if dep.lower() in DEPENDENCIES:
                group, technology = DEPENDENCIES[dep.lower()]
                stack[group].append(technology)
            if dep.startswith('@aws-sdk/'):
                stack['infrastructure'].append('AWS SDK')
            if dep.startswith('@azure/'):
                stack['infrastructure'].append('Azure SDK')
        if Path(path).suffix.lower() in {'.csproj', '.fsproj'}:
            if 'Microsoft.NET.Sdk.Web' in content:
                stack['frameworks'].append('ASP.NET Core')
            if 'Microsoft.EntityFrameworkCore' in content:
                stack['data'].append('Entity Framework Core')
            if 'Microsoft.AspNetCore.Components' in content or 'Blazor' in content:
                stack['frameworks'].append('Blazor')
            for word, tech in [('Npgsql', 'PostgreSQL'), ('SqlServer', 'SQL Server'), ('Sqlite', 'SQLite'), ('Dapper', 'Dapper')]:
                if word in content:
                    stack['data'].append(tech)
            for word, tech in [('xunit', 'xUnit'), ('NUnit', 'NUnit'), ('MSTest', 'MSTest')]:
                if word.lower() in content.lower():
                    stack['testing'].append(tech)
        if Path(path).name.lower() in {'dockerfile', 'docker-compose.yml', 'docker-compose.yaml', 'compose.yaml'}:
            stack['infrastructure'].append('Docker')
    if any('/.github/workflows/' in path for path in owned):
        stack['infrastructure'].append('GitHub Actions')
    if any(Path(path).suffix == '.tf' for path in owned):
        stack['infrastructure'].append('Terraform')
    for key in stack:
        stack[key] = sorted(set(stack[key]))
    if not purpose and package_descriptions:
        purpose, purpose_evidence = package_descriptions[0]
    sample = sorted([path for path in source if Path(path).suffix.lower() not in {'.ipynb', '.sh', '.ps1'}], key=lambda path: source_score(path, root))[:6]
    source_texts = {path: readable(path, 12000) for path in sample}
    features = []
    checks = {
        'HTTP API routing / request handling': r'(?:\[Http(?:Get|Post|Put|Delete)|\.Map(?:Get|Post|Put|Delete|Group)\s*\(|(?:app|router)\.(?:get|post|put|delete)\s*\(|@(?:app|router)\.(?:get|post)|export\s+(?:async\s+)?function\s+(?:GET|POST)|@(?:Get|Post)\()',
        'Rendered application UI': r'(?:return\s*\([\s\S]{0,250}<[A-Za-z]|<template>|@page\s+"|ReactDOM\.createRoot|createApp\(|<RouterView|<Routes|<script setup)',
        'Database access / persistence': r'(?:DbContext|\.SaveChangesAsync\s*\(|prisma\.[a-z]|db\.query\s*\(|pool\.query\s*\(|from\s+[\x27"]dexie|\.ToListAsync\s*\(|session\.query\s*\(|sqlite3\.connect)',
        'Authentication / authorization handling': r'(?:\.RequireAuthorization\s*\(|\[Authorize|signInWith|jwt\.verify\s*\(|\.AddAuthentication\s*\(|\.UseAuthentication\s*\(|getServerSession\s*\(|verifyToken\s*\(|useAuth\s*\()',
        'AI provider / model integration': r'(?:chat\.completions\.create|responses\.create\s*\(|messages\.create\s*\(|generateContent\s*\(|ChatOpenAI\s*\(|new OpenAI\s*\(|streamText\s*\()',
        'Automated background / scheduled work': r'(?:BackgroundService|\.AddHostedService|new Worker\s*\(|@shared_task|@celery\.task|cron\.schedule\s*\()',
        'Command-line entry point': r'(?:fn main\s*\(|func main\s*\(|if __name__\s*==\s*[\x27"]__main__|ArgumentParser\s*\(|CommandLineApplication)',
    }
    for label, pattern in checks.items():
        evidence = [path for path, content in source_texts.items() if re.search(pattern, content)]
        if evidence:
            features.append({'feature': label, 'evidence': evidence, 'basis': 'Construct observed in sampled source; not executed'})
    test_paths = [path for path in owned if re.search(r'(?i)(?:\.(?:test|spec)\.|/tests?/|tests?\.cs$)', path) and Path(path).suffix.lower() in SOURCE_EXT]
    test_sample = sorted(test_paths, key=lambda path: (path.count('/'), len(path)))[:2]
    for path in test_sample:
        readable(path, 4000)
    learning = [path for path in docs if LEARNING.search(path)]
    learning.sort(key=lambda path: (0 if re.search(r'(?i)(readme|index|curriculum|roadmap|syllabus)', Path(path).name) else 1, path.count('/'), path))
    learning = list(dict.fromkeys(learning))
    selected_learning = learning[:12]
    for path in selected_learning[:2]:
        if Path(path).suffix.lower() in {'.md', '.mdx', '.rst', '.txt'}:
            readable(path, 6000)
    if not purpose:
        purpose = ('Learning/reference collection; see the linked materials for its topics.' if not source else
                   'Source project with ' + ', '.join(stack['languages'][:3]) + '; its specific purpose is unclear from the inspected files.')
    category = identify_category(stack, purpose, source, docs, workspace)
    state = 'unknown'
    if not source or (LEARNING.search(Path(workspace).name) and learning):
        state = 'tutorial'
    elif features and (scripts or any(Path(path).suffix in {'.csproj', '.fsproj'} or Path(path).name in {'Cargo.toml', 'go.mod', 'pyproject.toml'} for path in manifests)):
        state = 'working-looking'
    if len(source) < 30 and any('Vite + React' in text or 'Get started by editing' in text for text in doc_texts.values()):
        state = 'partial'
    uncertainties = ['Static inspection only; dependencies, builds, tests, and runtime behavior were not executed.']
    if not features and source:
        uncertainties.append('Sampled files did not establish concrete application behavior; inspect more source before judging completeness.')
    if not source and docs:
        uncertainties.append('Documentation/resource collection; no implementation was found in the scanned scope.')
    if purpose_evidence:
        uncertainties.append('Purpose is described by project documentation or its manifest; it is not a claim that every documented feature is implemented.')
    components = []
    for path in owned:
        if Path(path).name == 'package.json' or Path(path).suffix.lower() in {'.csproj', '.fsproj'}:
            directory = Path(path).parent.as_posix()
            if directory != root:
                components.append(directory)
    signature_parts = [(Path(path).name.lower(), hashlib.sha256(text.encode()).hexdigest()) for path, text in {**doc_texts, **manifest_texts, **source_texts}.items() if text and within(path, root)]
    signature = hashlib.sha256(json.dumps(sorted(signature_parts)).encode()).hexdigest() if signature_parts else None
    return {
        'project_id': str(uuid.uuid5(NAMESPACE, root.casefold())),
        'name': Path(root).name, 'path': root, 'absolute_path': str(ROOT / root),
        'workspace_path': workspace, 'category': category, 'purpose': purpose,
        'purpose_evidence': purpose_evidence, 'stack': stack,
        'apparent_state': state, 'runtime_verification': 'not_run',
        'implemented_features': features,
        'learning_material': {'matching_resource_count': len(learning), 'key_paths': selected_learning,
                              'selection': 'Up to 12 resources selected by descriptive paths; up to two text samples inspected. Binary documents are listed by filename only.'},
        'repository': {'git_repository': bool(boundary.get('git_roots')), 'git_roots': boundary.get('git_roots', []), 'parent_project_id': str(uuid.uuid5(NAMESPACE, boundary['parent_path'].casefold())) if boundary['parent_path'] else None,
                       'components': sorted(set(components)), 'related_projects': []},
        'scope': {'source_files': len(source), 'document_files': len(docs), 'test_files': len(test_paths),
                  'boundary_reason': boundary['boundary']},
        'evidence': {'manifests_inspected': manifests, 'source_files_inspected': sample,
                     'documentation_inspected': readmes, 'tests_inspected': test_sample,
                     'tree_source': 'scan-index.json'},
        'uncertainties': uncertainties, 'inspection_level': 'lightweight-static-sample',
        'sample_fingerprint': signature, 'fingerprint_file_count': len(signature_parts),
        'last_reviewed': now(),
    }

def main():
    discovery = json.loads((OUT / 'scan-index.json').read_text(encoding='utf-8'))
    index = discovery['directories']
    boundaries = json.loads((OUT / 'project-boundaries.json').read_text(encoding='utf-8'))['projects']
    workspace_names = {boundary['workspace'] for boundary in boundaries}
    workspace_files = defaultdict(list)
    workspace_boundaries = defaultdict(list)
    for boundary in boundaries:
        workspace_boundaries[boundary['workspace']].append(boundary)
    for path, item in index.items():
        parent = path
        while parent not in workspace_names and '/' in parent:
            parent = parent.rsplit('/', 1)[0]
        if parent in workspace_names:
            workspace_files[parent].extend(path + '/' + name for name in item['files'])
    projects = []
    for number, boundary in enumerate(boundaries, 1):
        projects.append(analyze(boundary, workspace_files[boundary['workspace']], index, workspace_boundaries[boundary['workspace']]))
        if number % 15 == 0 or number == len(boundaries):
            catalog = {'schema_version': 1, 'root': str(ROOT), 'created_at': discovery['started_at'], 'updated_at': now(),
                       'independence': {'astraorganized_read': False, 'excluded_prior_inventory_roots': ['AstraOrganized', 'project-inventory'], 'phase': 'independent-analysis'},
                       'method': 'Read-only metadata discovery plus sampled manifests, README files, source and tests. No projects executed.',
                       'projects': projects}
            save('project-catalog.json', catalog)
            save('analysis-progress.json', {'phase': 'independent-analysis', 'updated_at': now(), 'astraorganized_read': False,
                                          'projects_discovered': len(boundaries), 'projects_reviewed': len(projects),
                                          'completed_project_ids': [p['project_id'] for p in projects],
                                          'next_batch': [b['path'] for b in boundaries[number:number + 15]],
                                          'remaining_paths': [b['path'] for b in boundaries[number:]]})
            print(json.dumps({'reviewed': number, 'total': len(boundaries), 'last': boundary['path']}), flush=True)
    groups = defaultdict(list)
    for project in projects:
        if project['sample_fingerprint'] and project['fingerprint_file_count'] >= 3:
            groups[project['sample_fingerprint']].append(project)
    duplicate_groups = []
    for fingerprint, group in groups.items():
        if len(group) < 2:
            continue
        duplicate_groups.append({'sample_fingerprint': fingerprint, 'project_ids': [p['project_id'] for p in group],
                                 'paths': [p['path'] for p in group],
                                 'evidence': 'Selected manifests, README and source sample contents match; full trees have not been byte-compared.',
                                 'relationship': 'likely-duplicate-or-version'})
        for project in group:
            project['repository']['related_projects'] = [
                {'project_id': other['project_id'], 'relationship': 'likely-duplicate-or-version',
                 'evidence': 'Matching multi-file sample fingerprint; not a complete tree comparison.'}
                for other in group if other != project]
    catalog['projects'] = projects
    catalog['updated_at'] = now()
    save('project-catalog.json', catalog)
    save('likely-duplicates.json', {'groups': duplicate_groups})
    with (OUT / 'review-digest.txt').open('w', encoding='utf-8') as stream:
        for n, project in enumerate(projects, 1):
            stream.write(f"{n:03d} | {project['path']} | {project['category']} | {project['apparent_state']}\n")
            stream.write(project['purpose'] + '\n')
            stream.write('Stack: ' + ', '.join(sum(project['stack'].values(), [])) + '\n')
            stream.write('Source samples: ' + '; '.join(project['evidence']['source_files_inspected'][:4]) + '\n\n')
    print(json.dumps({'analyzed': len(projects), 'likely_duplicate_groups': len(duplicate_groups)}))

if __name__ == '__main__':
    main()
