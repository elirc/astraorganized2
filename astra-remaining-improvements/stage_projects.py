"""Prepare isolated copies and immutable baselines. Never writes to Desktop projects."""
from pathlib import Path
import os,sys,json,shutil,hashlib
from long_paths import extended_path
BASE=extended_path(Path(__file__).resolve().parent);DESKTOP=BASE.parent.parent
scope=json.loads((BASE/'scope.json').read_text(encoding='utf-8'));eligible={x['path']:x for x in scope['eligible']}
SKIP={'.git','node_modules','bin','obj','dist','build','.next','.turbo','coverage','.cache','.venv','venv','__pycache__','.course-ops'}
for key in sys.argv[1:]:
 assert key in eligible,key
 record=eligible[key];dest=BASE/'stage'/record['id'];original=DESKTOP/key
 assert original.is_dir(),f'Original project is missing: {original}'
 assert not dest.exists(),f'Already staged: {dest}'
 baseline={};dest.mkdir(parents=True)
 for parent,dirs,files in os.walk(original):
  dirs[:]=[d for d in dirs if d not in SKIP and not (key=='aiheartbeat' and d=='tmp') and not (Path(parent)/d).is_symlink() and not (Path(parent)/d).is_junction()]
  for name in files:
   source=Path(parent)/name;rel=source.relative_to(original)
   if source.is_symlink() or (name.startswith('.env') and name not in {'.env.example','.env.sample','.env.template'}) or source.suffix.lower() in {'.db','.sqlite','.sqlite3','.log','.db-wal','.db-shm','.db-journal','.sqlite-wal','.sqlite-shm','.sqlite-journal','.sqlite3-wal','.sqlite3-shm','.sqlite3-journal'}:continue
   target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
   baseline[rel.as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest()
 (BASE/'baselines').mkdir(exist_ok=True)
 (BASE/'baselines'/f'{record["id"]}.json').write_text(json.dumps({'id':record['id'],'project':key,'files':baseline},indent=2),encoding='utf-8')
 print(json.dumps({'project':key,'stage':str(dest),'files':len(baseline)}),flush=True)
