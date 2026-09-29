"""Read-only metadata inventory. Writes audit reports only; never deletes project files."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import csv
import json
import os
import shutil
import threading
import time

WORK = Path(__file__).resolve().parents[2]
DESKTOP = WORK.parent
OUT = Path(__file__).resolve().parent
started = datetime.now(timezone.utc).isoformat()
lock = threading.Lock()
errors = []
links = []
rows = []

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def extended(path):
    value = str(path)
    return value if value.startswith('\\\\?\\') else '\\\\?\\' + value

def normal(path):
    return str(path).removeprefix('\\\\?\\')

def key(path):
    return normal(path).replace('\\', '/').rstrip('/').casefold()

registry = read(WORK / 'fablereview/registry.json')
progress = read(WORK / 'astra-remaining-improvements/progress.json')
projects = {key(p['abs']): Path(p['abs']) for p in registry}
for item in progress['projects']:
    if item.get('status') == 'complete':
        path = DESKTOP / item['path']
        projects[key(path)] = path
all_projects = sorted(projects.values(), key=lambda p: (len(p.parts), str(p).casefold()))
roots = []
covered = []
for path in all_projects:
    parent = next((r for r in roots if key(path).startswith(key(r) + '/')), None)
    if parent:
        covered.append({'project': str(path), 'coveredBy': str(parent)})
    else:
        roots.append(path)

delivered_ids = set()
for manifest in (WORK / 'astra-remaining-improvements/deliveries').glob('*.json'):
    try:
        if read(manifest).get('status') == 'delivered':
            delivered_ids.add(manifest.stem)
    except (OSError, ValueError):
        pass

DEPENDENCIES = {'node_modules', '.venv', 'venv', 'env'}
CACHES = {'.next', '.nuxt', '.svelte-kit', '.turbo', '.parcel-cache', '.vite', '.angular',
          '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.gradle', '.cache',
          'npm-cache', 'pip-cache', '.pnpm-store', '.eslintcache'}
GENERATED = {'dist', 'build', 'out', 'bin', 'obj', 'target', 'coverage', 'testresults',
             'test-results', 'playwright-report', 'browser-report', '.vs', '.idea', 'vendor',
             'pods', '.yarn', 'artifacts', 'logs'}
PROTECT = {'astraupskill', 'upskilling', 'dfableandopus', 'docs', 'astradocs', 'astrdocs'}
DATA = {'.db', '.sqlite', '.sqlite3', '.dump', '.bak', '.backup', '.mdf', '.ldf', '.vhdx',
        '.zip', '.7z', '.tar', '.gz', '.nupkg'}

def classify(path, parent, name, context, inside, protected):
    low = name.lower()
    if inside == 'A':
        return None
    if low == 'node_modules':
        return ('A', 'Installed dependencies', 'Reinstall with the retained package manifest and lockfile; running/building will require reinstalling.')
    if low in {'.venv', 'venv', 'env'} and (parent / name / 'pyvenv.cfg').is_file():
        return ('A', 'Python environment', 'Recreate the environment from retained dependency files; verify no personal source was placed inside it.')
    if low in CACHES and not protected:
        return ('A', 'Generated cache', 'Normally recreated by its tool; retained source and configuration must stay.')
    if context == 'Astra workspace' and not inside:
        if key(parent) == key(WORK / 'astra-remaining-improvements/stage'):
            if name in delivered_ids:
                return ('B', 'Delivered staging copy', 'Delivery manifest exists. Verify no later unique edits; retain canonical project, reports, original snapshots and accepted evidence before discarding this duplicate work area.')
            return ('C', 'Unconfirmed staging copy', 'No delivered manifest identified for this directory. May contain unfinished or unique work; inspect before considering deletion.')
        if low in {'dependency-quarantine', 'toolchains', 'tooldeps', 'playwright-browsers', 'dotnet-home'} or low.startswith('dependency-quarantine-'):
            return ('A', 'Campaign dependencies/tools', 'Disposable campaign dependency/cache or reinstallable tool installation; deleting may require reinstalling tools and packages to rerun checks.')
        if low in {'backups', 'independent-snapshot', 'snapshots'} or 'quarantine' in low:
            return ('C', 'Backups or quarantined originals', 'Contains recovery/comparison material. Keep unless originals and any unique work have been verified elsewhere.')
        if low in {'stage', 'pg-test'}:
            if key(path) == key(WORK / 'astra-remaining-improvements/stage'):
                return None
            return ('C', 'Other work area / database fixture', 'Potential duplicate or test workspace; delivery status/data ownership not established by this size scan.')
    if inside or protected:
        return None
    if low == '.git':
        return ('C', 'Git history — keep by default', 'Removing loses local commits, branches and recovery/history; source still readable, but do not treat as a cache.')
    if low in GENERATED:
        return ('B', 'Build/output or optional project folder', 'Name suggests generated output, reports or installed assets, but may contain tracked/custom files. Review contents/version control before approval; keep source, fixtures and learning evidence.')
    return None

def walk(path, project, context, inside=None, protected=False):
    size = count = 0
    try:
        with os.scandir(extended(path)) as iterator:
            entries = list(iterator)
    except OSError as error:
        with lock: errors.append({'path': str(path), 'error': str(error)})
        return 0, 0
    for entry in entries:
        child = path / entry.name
        if key(child) == key(OUT):
            continue
        try:
            stat = entry.stat(follow_symlinks=False)
            if entry.is_symlink() or getattr(stat, 'st_file_attributes', 0) & 0x400:
                with lock: links.append(str(child))
                continue
            if entry.is_dir(follow_symlinks=False):
                protect_child = protected or entry.name.lower() in PROTECT
                category = classify(child, path, entry.name, context, inside, protect_child)
                child_size, child_count = walk(child, project, context, category[0] if category else inside, protect_child)
                size += child_size
                count += child_count
                if category and child_size:
                    with lock: rows.append({'project': project, 'scope': context, 'path': str(child), 'tier': category[0], 'kind': category[1], 'bytes': child_size, 'files': child_count, 'impact': category[2]})
            else:
                size += stat.st_size
                count += 1
                if not inside and not protected:
                    suffix = Path(entry.name).suffix.lower()
                    if suffix in {'.tsbuildinfo', '.pyc'} or entry.name == '.eslintcache':
                        category = ('A', 'Generated incremental cache', 'Regenerated by the relevant compiler/tool.')
                    elif suffix in DATA or stat.st_size >= 100 * 1024**2:
                        category = ('C', 'Data/archive/large file — inspect', 'May be unique data, a fixture, backup, offline installer or source asset; size/extension alone does not establish redundancy.')
                    else:
                        category = None
                    if category and stat.st_size:
                        with lock: rows.append({'project': project, 'scope': context, 'path': str(child), 'tier': category[0], 'kind': category[1], 'bytes': stat.st_size, 'files': 1, 'impact': category[2]})
        except OSError as error:
            with lock: errors.append({'path': str(child), 'error': str(error)})
    return size, count

jobs = [(p, str(p.relative_to(DESKTOP)), 'Modified project', None) for p in roots]
jobs.append((WORK, WORK.name, 'Astra workspace', None))
# Shared parent dependencies can serve modified nested apps without lying inside an app root.
extra = set()
for project in all_projects:
    for parent in project.parents:
        if parent == DESKTOP:
            break
        if not parent.is_relative_to(DESKTOP):
            break
        for name in ['node_modules', '.venv', '.next', '.turbo']:
            path = parent / name
            if not any(key(path).startswith(key(root) + '/') for root in roots) and path.is_dir():
                extra.add(path)
for path in sorted(extra):
    jobs.append((path, str(path.relative_to(DESKTOP)), 'Shared parent dependency/cache', 'A'))

home = Path.home()
local = Path(os.environ.get('LOCALAPPDATA', str(home / 'AppData/Local')))
for path in [local/'npm-cache', local/'pnpm/store', home/'.nuget/packages', local/'pip/Cache', local/'ms-playwright']:
    if path.is_dir():
        jobs.append((path, path.name, 'Shared user cache', 'A'))

results = []
def run(job):
    path, label, context, tier = job
    if not path.exists():
        return {'project': label, 'path': str(path), 'scope': context, 'status': 'missing', 'bytes': 0, 'files': 0}
    root_stat = path.stat(follow_symlinks=False)
    if getattr(root_stat, 'st_file_attributes', 0) & 0x400:
        with lock: links.append(str(path))
        return {'project': label, 'path': str(path), 'scope': context, 'status': 'link-skipped', 'bytes': 0, 'files': 0}
    size, count = walk(path, label, context, tier)
    if tier and size:
        with lock: rows.append({'project': label, 'scope': context, 'path': str(path), 'tier': tier, 'kind': 'Shared reinstallable cache', 'bytes': size, 'files': count, 'impact': 'Shared beyond these projects. Tools/browsers/packages may need downloading again; not an application-data folder. Hard links may reduce reclaimed space.'})
    return {'project': label, 'path': str(path), 'scope': context, 'status': 'scanned', 'bytes': size, 'files': count}

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(run, job): job for job in jobs}
    for future in as_completed(futures):
        try: result = future.result()
        except Exception as error:
            result = {'project': futures[future][1], 'status': 'failed', 'error': str(error), 'bytes': 0, 'files': 0}
            errors.append(result)
        results.append(result)
        print(json.dumps({'done': len(results), 'total': len(jobs), 'project': result['project'], 'GiB': round(result['bytes']/1024**3,3)}, ensure_ascii=True), flush=True)
        (OUT/'scan-status.json').write_text(json.dumps({'completed':len(results),'total':len(jobs),'latest':result},indent=2),encoding='utf-8')

rows.sort(key=lambda row: (-row['bytes'],row['path']))
for number, row in enumerate(rows,1):
    row['id'] = f'D{number:04}'
    row['GiB'] = round(row['bytes']/1024**3,4)
    parents = [other for other in rows if other is not row and key(row['path']).startswith(key(other['path'])+'/')]
    row['containedIn'] = min(parents,key=lambda other:len(other['path']))['path'] if parents else ''

usage = shutil.disk_usage(DESKTOP)
output = {'startedAt':started,'finishedAt':datetime.now(timezone.utc).isoformat(),
          'method':'Read-only recursive file metadata; logical byte sizes; reparse points/symlinks skipped; no content hashes or tracked-file checks; no deletion.',
          'modifiedProjects':len(all_projects),'scanRoots':len(roots),'nestedProjectsCovered':covered,
          'disk':{'total':usage.total,'used':usage.used,'free':usage.free},
          'projects':results,'candidates':rows,'errors':errors,'skippedLinks':links}
(OUT/'inventory.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
with (OUT/'candidates.csv').open('w',encoding='utf-8-sig',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=['id','tier','scope','project','kind','path','bytes','GiB','files','containedIn','impact'])
    writer.writeheader();writer.writerows(rows)
print(json.dumps({'finished':True,'candidates':len(rows),'errors':len(errors),'skippedLinks':len(links)},indent=2),flush=True)
