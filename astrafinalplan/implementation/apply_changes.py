"""Apply only reviewed files to the ten explicitly requested Desktop projects."""
from pathlib import Path
import json,hashlib,os,shutil
BASE=Path(__file__).resolve().parent
DESKTOP=BASE.parents[2]
manifest=json.loads((BASE/'delivery-manifest.json').read_text())
allowed=set(json.loads((BASE/'projects.json').read_text()))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Complete all path/content checks before writing any original project file.
for item in manifest:
 assert item['project'] in allowed
 root=(DESKTOP/item['project']).resolve();target=(root/item['file']).resolve()
 assert target.is_relative_to(root),f'Path escaped project: {target}'
 source=BASE/'stage'/item['stage']/item['file']
 assert digest(source)==item['after_sha256'],f'Prepared file changed: {source}'
 assert not target.with_name(target.name+'.astra-write-tmp').exists(),f'Temporary target already exists: {target}'
 if target.exists() and digest(target)==item['after_sha256']:continue
 if item['before_sha256']:
  assert target.exists() and digest(target)==item['before_sha256'],f'Concurrent change: {target}'
 else:assert not target.exists(),f'New target already exists: {target}'
for item in manifest:
 target=DESKTOP/item['project']/item['file'];source=BASE/'stage'/item['stage']/item['file']
 if target.exists() and digest(target)==item['after_sha256']:continue
 if target.exists():
  backup=BASE/'backups'/item['stage']/item['file'];backup.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(target,backup)
 target.parent.mkdir(parents=True,exist_ok=True)
 temporary=target.with_name(target.name+'.astra-write-tmp')
 assert not temporary.exists(),f'Temporary target already exists: {temporary}'
 shutil.copyfile(source,temporary)
 os.replace(temporary,target)
 assert digest(target)==item['after_sha256']
print(json.dumps({'applied':True,'projects':len(allowed),'files':len(manifest),'backups':str(BASE/'backups')},indent=2))
