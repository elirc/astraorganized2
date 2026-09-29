from pathlib import Path
import hashlib, json, os, shutil, sys

B = Path(__file__).resolve().parent.parent
pid = sys.argv[1]
project = next(p for p in json.loads((B / "scope.json").read_text(encoding="utf-8"))["eligible"] if p["id"] == pid)
source = (B.parent.parent / project["path"]).resolve()
stage = (B / "stage" / pid).resolve()
baseline_path = B / "baselines" / f"{pid}.json"
assert stage.is_dir() and not baseline_path.exists()
skip = {".git", "node_modules", "bin", "obj", "dist", "build", ".next", ".turbo", "coverage", ".cache", ".venv", "venv", "__pycache__", ".course-ops"}
excluded = {".db", ".sqlite", ".sqlite3", ".log", ".db-wal", ".db-shm", ".db-journal", ".sqlite-wal", ".sqlite-shm", ".sqlite-journal", ".sqlite3-wal", ".sqlite3-shm", ".sqlite3-journal"}

def long_path(path):
    value = str(Path(path).resolve())
    return value if value.startswith("\\\\?\\") else "\\\\?\\" + value

def digest(path):
    with open(long_path(path), "rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

files = {}
for parent, dirs, names in os.walk(source):
    dirs[:] = [d for d in dirs if d not in skip and not (Path(parent) / d).is_symlink() and not (Path(parent) / d).is_junction()]
    for name in names:
        path = Path(parent) / name
        if path.is_symlink() or (name.startswith(".env") and name not in {".env.example", ".env.sample", ".env.template"}) or path.suffix.lower() in excluded:
            continue
        files[path.relative_to(source).as_posix()] = digest(path)

existing = 0
for parent, dirs, names in os.walk(stage):
    for name in names:
        path = Path(parent) / name
        rel = path.relative_to(stage).as_posix()
        assert rel in files and digest(path) == files[rel], f"staged mismatch: {rel}"
        existing += 1

for rel, expected in files.items():
    original, target = source / rel, stage / rel
    if not os.path.exists(long_path(target)):
        os.makedirs(long_path(target.parent), exist_ok=True)
        shutil.copyfile(long_path(original), long_path(target))

baseline_path.write_text(json.dumps({"id": pid, "project": project["path"], "files": files}, indent=2), encoding="utf-8")
print(json.dumps({"id": pid, "resumedUnchangedFiles": existing, "baselineFiles": len(files)}))
