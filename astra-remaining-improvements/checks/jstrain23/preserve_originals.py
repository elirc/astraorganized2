from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[2];S=B/'stage/58c5c289a8ce'
baseline=json.loads((B/'baselines/58c5c289a8ce.json').read_text(encoding='utf-8'))['files']
count=0
for rel,sha in baseline.items():
    p=S/rel
    if p.suffix not in {'.js','.mjs','.css','.json','.md'} and p.name!='.gitignore':continue
    assert hashlib.sha256(p.read_bytes()).hexdigest()==sha,rel
    target=S/'docs/original'/(rel+'.txt');assert not target.exists();target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());count+=1
print('Preserved',count,'original text files without executing archived source.')
