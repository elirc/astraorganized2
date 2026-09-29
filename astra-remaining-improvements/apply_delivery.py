"""Apply one fully checked manifest with backups and concurrent-change protection."""
from pathlib import Path
import json,hashlib,os,shutil,sys
from datetime import datetime,timezone
from long_paths import extended_path
B=extended_path(Path(__file__).resolve().parent);D=B.parent.parent;pid=sys.argv[1]
assert len(pid)==12 and all(c in '0123456789abcdef' for c in pid)
p=B/'deliveries'/f'{pid}.json';m=json.loads(p.read_text(encoding='utf-8'))
eligible={x['id']:x for x in json.loads((B/'scope.json').read_text(encoding='utf-8'))['eligible']}
assert pid in eligible and eligible[pid]['path']==m['project']
root=(D/m['project']).resolve();stage=(B/'stage'/pid).resolve()
assert root.is_relative_to(D.resolve()) and root!=D.resolve()
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f in m['files']:
 source=(stage/f['file']).resolve();target=(root/f['file']).resolve()
 assert source.is_relative_to(stage) and target.is_relative_to(root)
 assert hashfile(source)==f['after_sha256']
 assert not target.with_name(target.name+'.astra-write-tmp').exists()
 if target.exists() and hashfile(target)==f['after_sha256']:continue
 if f['before_sha256']:assert target.is_file() and hashfile(target)==f['before_sha256'],f'Concurrent edit: {target}'
 else:assert not target.exists(),f'Unexpected existing file: {target}'
for f in m['files']:
 source=stage/f['file'];target=root/f['file']
 if target.exists() and hashfile(target)==f['after_sha256']:continue
 if target.exists():
  backup=B/'backups'/pid/f['file'];backup.parent.mkdir(parents=True,exist_ok=True)
  if backup.exists():assert hashfile(backup)==f['before_sha256']
  else:shutil.copyfile(target,backup)
 target.parent.mkdir(parents=True,exist_ok=True);temporary=target.with_name(target.name+'.astra-write-tmp')
 shutil.copyfile(source,temporary);os.replace(temporary,target)
for f in m['files']:assert hashfile(root/f['file'])==f['after_sha256']
m['status']='delivered';m['deliveredAt']=datetime.now(timezone.utc).isoformat();p.write_text(json.dumps(m,indent=2),encoding='utf-8')
ledger=B/'progress.json';progress=json.loads(ledger.read_text(encoding='utf-8'));row=next(x for x in progress['projects'] if x['id']==pid)
row.update({'status':'complete','changes':m['summary'],'checks':m['checks'],'deliveryManifest':str(p),'courseFiles':m['courseFiles'],'courseWords':m['courseWords'],'completedAt':m['deliveredAt']})
ledger.write_text(json.dumps(progress,indent=2),encoding='utf-8')
print(json.dumps({'delivered':m['project'],'files':len(m['files']),'courseWords':m['courseWords'],'testResults':m['testResults'],'originalHashesVerified':True},indent=2))
