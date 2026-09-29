from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
id='f1f996eeb9e7';P=B/'stage'/id
rel='zz4/astraupskill/evidence/results-crud-b07.json'
base=json.loads((B/'baselines'/f'{id}.json').read_text());assert rel not in base['files']
p=(P/rel).resolve();assert p.is_relative_to(P.resolve())
if p.exists():p.unlink()
P=B/'stage/1754dbb384b1'
for p in (P/'astraupskill').glob('*.md'):
 s=p.read_text().replace('../bagel-intel-platform/astraupskill/evidence/1754dbb384b1-runtime-review-moderation.tap.txt','evidence/crud-b07-astra-runtime.log')
 p.write_text(s,encoding='utf-8')
