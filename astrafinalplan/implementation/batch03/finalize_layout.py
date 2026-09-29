from pathlib import Path
import json
B=Path(__file__).resolve().parent
ids=[int(d['stage']) for f in ['domain-specs.json','memory-domain-specs.json'] for d in json.loads((B/f).read_text(encoding='utf-8'))]
for n in ids:
 p=B/'stage'/str(n)/'client/src/styles.css';s=p.read_text(encoding='utf-8')
 s=s.replace('grid-template-columns: 1fr 160px 160px 160px;', 'grid-template-columns: repeat(2, minmax(0, 1fr));')
 p.write_text(s,encoding='utf-8')
print('Made domain toolbar controls readable in narrow middle panels:',ids)
