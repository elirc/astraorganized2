from pathlib import Path
import hashlib
import json
import re
import shutil

C=Path(__file__).resolve().parent
B=C.parents[1]
S=B/'stage/71e7b036865c'
baseline=json.loads((B/'baselines/71e7b036865c.json').read_text(encoding='utf-8'))
config=json.loads((S/'server/Nethris.Api/appsettings.json').read_text(encoding='utf-8'))
assert re.search('development|change.this|dev.key',config['Jwt']['Key'],re.I), 'Review configuration before archiving it.'
destination=S/'docs/original'
assert not destination.exists(), 'Original snapshot already exists; do not regenerate it.'
for rel,digest in baseline['files'].items():
    source=S/rel
    assert hashlib.sha256(source.read_bytes()).hexdigest()==digest,rel
    source.read_text(encoding='utf-8')
    target=destination/(rel+'.txt')
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,target)
print(json.dumps({'preservedOriginalTextFiles':len(baseline['files'])}))
