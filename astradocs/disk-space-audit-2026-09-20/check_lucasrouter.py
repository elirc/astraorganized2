"""Record a metadata fingerprint without following links or changing either project."""
import os,json,hashlib,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
BASE=OUT.parents[1]
paths=[BASE.parent/'lucasrouter',BASE/'astra-remaining-improvements/stage/52d78d4a92a2']
result=[]
for root in paths:
    h=hashlib.sha256(); count=0; stack=[root]
    while stack:
        p=stack.pop()
        for e in sorted(os.scandir('\\\\?\\'+str(p)),key=lambda x:x.name):
            s=e.stat(follow_symlinks=False); f=p/e.name
            h.update(json.dumps([str(f.relative_to(root)),s.st_size,s.st_mtime_ns,s.st_file_attributes],ensure_ascii=True).encode())
            count+=1
            if e.is_dir(follow_symlinks=False) and not s.st_file_attributes&0x400: stack.append(f)
    result.append({'path':str(root),'entries':count,'metadataSHA256':h.hexdigest()})
mode=sys.argv[1]
if mode=='before': (OUT/'lucasrouter-before.json').write_text(json.dumps(result,indent=2))
else:
    before=json.loads((OUT/'lucasrouter-before.json').read_text())
    (OUT/'lucasrouter-after.json').write_text(json.dumps({'unchanged':before==result,'before':before,'after':result},indent=2))
    assert before==result,'Lucasrouter metadata changed; inspect external activity and cleanup log'
print(json.dumps(result))
