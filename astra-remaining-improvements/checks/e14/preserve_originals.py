from pathlib import Path
import json,shutil,hashlib
C=Path(__file__).resolve().parent;B=C.parents[1];S=B/'stage/ca549816cdd1'
baseline=json.loads((B/'baselines/ca549816cdd1.json').read_text(encoding='utf-8'))['files'];out=S/'docs/original';assert not out.exists();count=0
for name,digest in baseline.items():
    if '.egg-info/' in name:continue
    p=S/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
    if p.suffix in {'.py','.md','.toml','.json','.txt'}:
        target=out/(name+'.txt');target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target);count+=1
print(json.dumps({'preservedTextFiles':count}))
