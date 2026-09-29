"""Finish the interrupted Windows copy without overwriting staged edits."""
from pathlib import Path
import hashlib, json, os, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from long_paths import extended_path
B=extended_path(Path(__file__).resolve().parent.parent)
pid='195e77d61335';key='_Organized Desktop/05 Numbered Experiments/rn1'
source=B.parent.parent/key;stage=B/'stage'/pid
manifest=B/'baselines'/f'{pid}.json'
assert stage.is_dir() and not manifest.exists(),'Only an incomplete stage can be recovered'
allowed=set()
skip={'.git','node_modules','bin','obj','dist','build','.next','.turbo','coverage','.cache','.venv','venv','__pycache__','.course-ops'}
excluded={'.db','.sqlite','.sqlite3','.log','.db-wal','.db-shm','.db-journal','.sqlite-wal','.sqlite-shm','.sqlite-journal','.sqlite3-wal','.sqlite3-shm','.sqlite3-journal'}
files={};copied=0;preserved=[]
def recover(original):
    rel=original.relative_to(source).as_posix();target=stage/rel
    content=original.read_bytes();digest=hashlib.sha256(content).hexdigest()
    changed=False;written=False
    if target.exists():
        changed=hashlib.sha256(target.read_bytes()).hexdigest()!=digest
        assert not changed or rel in allowed,('Unlisted staged change',rel)
    else:
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(content);written=True
    return rel,digest,changed,written
with ThreadPoolExecutor(max_workers=16) as pool:
    jobs=[]
    for parent,dirs,names in os.walk(source):
        dirs[:]=[d for d in dirs if d not in skip and not (Path(parent)/d).is_symlink() and not (Path(parent)/d).is_junction()]
        for name in names:
            original=Path(parent)/name
            if original.is_symlink() or (name.startswith('.env') and name not in {'.env.example','.env.sample','.env.template'}) or original.suffix.lower() in excluded:continue
            jobs.append(pool.submit(recover,original))
    for job in as_completed(jobs):
        rel,digest,changed,written=job.result();files[rel]=digest;copied+=int(written)
        if changed:preserved.append(rel)
        if len(files)%1000==0:print(json.dumps({'scanned':len(files),'copied':copied}),flush=True)
manifest.write_text(json.dumps({'id':pid,'project':key,'files':files},indent=2),encoding='utf-8')
print(json.dumps({'id':pid,'baselineFiles':len(files),'copiedMissing':copied,'preservedEdits':preserved}),flush=True)
