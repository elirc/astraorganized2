"""Read-only preflight for an Astra-reviewed staged delivery. Never applies files."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote, urlsplit
from long_paths import extended_path

B = extended_path(Path(__file__).resolve().parent)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('id')
parser.add_argument('--labels', nargs='*', default=[])
parser.add_argument('--hashes', help='Optional source hash record, relative to improvement workspace')
parser.add_argument('--allow-unlisted', action='append', default=[])
args = parser.parse_args()
assert re.fullmatch(r'[0-9a-f]{12}', args.id), 'Invalid project ID'
P = B / 'stage' / args.id


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


baseline = read_json(B / 'baselines' / f'{args.id}.json')['files']
spec = read_json(B / 'specs' / f'{args.id}.json')
listed = set(spec['changedFiles'])
allowed = set(args.allow_unlisted)
issues = []
changed = []
ignored_dirs = {'node_modules', '.git', '.next', 'dist', 'bin', 'obj', '.venv',
                '__pycache__', 'coverage', 'TestResults', '.turbo', '.cache'}
source_suffixes = {'.cs', '.csproj', '.sln', '.props', '.targets', '.ts', '.tsx',
                   '.js', '.jsx', '.mjs', '.cjs', '.py', '.ps1', '.json', '.yaml',
                   '.yml', '.toml', '.sql', '.prisma', '.css', '.html', '.go', '.rs', '.vue'}

def baseline_changed(item):
    name, before_hash = item
    path = P / name
    return name, not path.is_file() or digest(path) != before_hash

with ThreadPoolExecutor(max_workers=16) as pool:
  for name, is_changed in pool.map(baseline_changed, baseline.items()):
    if is_changed:
        changed.append(name)
        if name not in listed and name not in allowed:
            issues.append({'kind': 'unlisted_baseline_change', 'file': name})

new_source = []
for directory, dirs, files in os.walk(P):
    dirs[:] = [name for name in dirs if name not in ignored_dirs]
    for filename in files:
        path = Path(directory) / filename
        name = path.relative_to(P).as_posix()
        if name.startswith(('astraupskill/', 'snapshots/')) or name in baseline:
            continue
        if path.suffix.lower() in source_suffixes:
            new_source.append(name)
            if name not in listed and name not in allowed:
                issues.append({'kind': 'unlisted_new_source', 'file': name})

for name in listed:
    path = (P / name).resolve()
    if not path.is_relative_to(P.resolve()) or not path.is_file():
        issues.append({'kind': 'missing_or_outside_manifest_file', 'file': name})

hash_checked = 0
if args.hashes:
    hash_path = (B / args.hashes).resolve()
    assert hash_path.is_relative_to(B), 'Hash record must be local'
    record = read_json(hash_path)
    for name, expected in record['files'].items():
        path = P / name
        if path.suffix.lower() not in source_suffixes or name.startswith(('astraupskill/', 'snapshots/')):
            continue
        hash_checked += 1
        if not path.is_file() or digest(path) != expected:
            issues.append({'kind': 'executable_hash_mismatch', 'file': name})

snapshots_checked = 0
original_hashes = set(baseline.values())
for name in listed:
    if '/snapshots/' not in name and not name.startswith('snapshots/'):
        continue
    path = P / name
    if path.is_file():
        snapshots_checked += 1
        if digest(path) not in original_hashes:
            issues.append({'kind': 'snapshot_not_exact_baseline_bytes', 'file': name})

required_chapters = ['README.md', '01-CODEBASE-MAP.md', '02-CONCEPTS.md',
                     '03-WORKED-CHANGE.md', '04-TESTING-AND-DEBUGGING.md',
                     '05-PRACTICE.md', '06-SOLUTIONS-AND-REVIEW.md',
                     '07-TRACE-LAB.md', 'VERIFICATION.md']
chapter_words = {}
long_paragraphs = {}
for chapter in required_chapters:
    path = P / 'astraupskill' / chapter
    if not path.is_file():
        issues.append({'kind': 'missing_required_chapter', 'file': chapter})
        continue
    try:
        chapter_text = path.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        issues.append({'kind': 'non_utf8_chapter', 'file': chapter})
        continue
    chapter_words[chapter] = len(chapter_text.split())
    if '\ufffd' in chapter_text:
        issues.append({'kind': 'replacement_character_in_chapter', 'file': chapter})
    prose = re.sub(r'```.*?```', '', chapter_text, flags=re.S)
    for paragraph in re.split(r'\n\s*\n', prose):
        normalized = ' '.join(paragraph.split())
        if len(normalized.split()) >= 60:
            long_paragraphs.setdefault(normalized, set()).add(chapter)
    if chapter_words[chapter] < 80:
        issues.append({'kind': 'short_required_chapter', 'file': chapter,
                       'words': chapter_words[chapter]})
    if any(line.startswith('\\n') and len(line) > 2 and line[2].isupper()
           for line in chapter_text.splitlines()):
        issues.append({'kind': 'literal_newline_in_prose', 'file': chapter})

for paragraph, chapters in long_paragraphs.items():
    if len(chapters) >= 3:
        issues.append({'kind': 'repeated_long_course_paragraph',
                       'files': sorted(chapters), 'preview': paragraph[:100]})

links_checked = 0
for path in (P / 'astraupskill').glob('*.md'):
    if path.name not in required_chapters and path.relative_to(P).as_posix() not in listed:
        continue  # Unlisted draft chapters are not delivered or linked from the course.
    try:
        text = path.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        if path.name not in required_chapters:
            issues.append({'kind': 'non_utf8_chapter', 'file': path.name})
        continue
    for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        target = raw.strip().strip('<>')
        scheme = urlsplit(target).scheme
        if target.startswith('#') or (scheme and scheme != 'file' and not re.match(r'^[A-Za-z]:[\\/]', target)):
            continue
        if scheme == 'file':
            issues.append({'kind': 'nonportable_file_uri', 'file': path.name, 'target': target})
            continue
        target = unquote(target.split('#', 1)[0])
        if not target:
            continue
        links_checked += 1
        resolved = (path.parent / target).resolve()
        if not resolved.is_relative_to(P.resolve()):
            issues.append({'kind': 'guide_link_outside_project', 'file': path.name, 'target': target})
        elif not resolved.exists():
            issues.append({'kind': 'missing_guide_link', 'file': path.name, 'target': target})
        elif resolved.is_file():
            destination_name = resolved.relative_to(P.resolve()).as_posix()
            delivery_names = listed | {'astraupskill/' + name for name in required_chapters}
            if destination_name not in baseline and destination_name not in delivery_names:
                issues.append({'kind': 'guide_link_not_delivered', 'file': path.name,
                               'target': target})

checks = []
for label in args.labels:
    assert re.fullmatch(r'[A-Za-z0-9_-]+', label), 'Invalid label'
    record_path = B / 'checks' / args.id / f'{label}.json'
    if not record_path.exists():
        issues.append({'kind': 'missing_check_record', 'label': label})
        continue
    record = read_json(record_path)
    checks.append({'label': label, 'status': record.get('status'), 'exitCode': record.get('exitCode')})
    if record.get('status') != 'complete' or record.get('exitCode') != 0:
        issues.append({'kind': 'check_not_terminal_pass', 'label': label})
    if not (record_path.parent / record.get('log', '')).is_file():
        issues.append({'kind': 'missing_check_log', 'label': label})

print(json.dumps({'id': args.id, 'passed': not issues, 'changedBaselineFiles': changed,
                  'newSourceFiles': new_source, 'executableHashesChecked': hash_checked,
                  'snapshotsChecked': snapshots_checked, 'projectLocalLinksChecked': links_checked,
                  'chapterWords': chapter_words, 'courseWords': sum(chapter_words.values()),
                  'checks': checks, 'issues': issues,
                  'limit': 'Mechanical preflight only; source correctness and test meaning require Astra review.'}, indent=2))
raise SystemExit(1 if issues else 0)
