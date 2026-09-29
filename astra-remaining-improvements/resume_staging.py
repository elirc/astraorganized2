"""Resume an interrupted copy only when every existing staged byte matches its source."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import sys

B = Path(__file__).resolve().parent
pid = sys.argv[1]
project = next(p for p in json.loads((B/'scope.json').read_text(encoding='utf-8'))['eligible'] if p['id'] == pid)
source = B.parent.parent/project['path']
stage = B/'stage'/pid
baseline_path = B/'baselines'/(pid+'.json')
assert stage.is_dir() and not baseline_path.exists(), 'Only incomplete staging is eligible'
skip = {'.git','node_modules','bin','obj','dist','build','.next','.turbo','coverage','.cache','.venv','venv','__pycache__','.course-ops'}
excluded = {'.db','.sqlite','.sqlite3','.log','.db-wal','.db-shm','.db-journal','.sqlite-wal','.sqlite-shm','.sqlite-journal','.sqlite3-wal','.sqlite3-shm','.sqlite3-journal'}
hashfile = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
files = {}
for parent, dirs, names in os.walk(source):
    dirs[:] = [d for d in dirs if d not in skip and not (project['path']=='aiheartbeat' and d=='tmp') and not (Path(parent)/d).is_symlink() and not (Path(parent)/d).is_junction()]
    for name in names:
        path = Path(parent)/name
        if path.is_symlink() or (name.startswith('.env') and name not in {'.env.example','.env.sample','.env.template'}) or path.suffix.lower() in excluded:
            continue
        files[path.relative_to(source).as_posix()] = hashfile(path)
existing = 0
for parent, dirs, names in os.walk(stage):
    assert all(not (Path(parent)/d).is_symlink() and not (Path(parent)/d).is_junction() for d in dirs)
    for name in names:
        path = Path(parent)/name
        rel = path.relative_to(stage).as_posix()
        assert not path.is_symlink() and rel in files and hashfile(path) == files[rel], f'Staged changes must be preserved: {path}'
        existing += 1
for rel, digest in files.items():
    original, target = source/rel, stage/rel
    assert hashfile(original) == digest, f'Source changed during recovery: {original}'
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original, target)
    assert hashfile(target) == digest
baseline_path.write_text(json.dumps({'id': pid, 'project': project['path'], 'files': files}, indent=2), encoding='utf-8')
print(json.dumps({'id': pid, 'resumedUnchangedFiles': existing, 'baselineFiles': len(files)}))
