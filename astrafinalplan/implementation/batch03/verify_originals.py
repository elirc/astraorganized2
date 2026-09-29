from pathlib import Path
import json,re,hashlib
from urllib.parse import unquote
B=Path(__file__).resolve().parent;H=B.parent;D=B.parents[3]
results=[];links=0;files=0;mismatches=[]
for batch in [H,H/'batch02',B]:
 manifest=json.loads((batch/'delivery-manifest.json').read_text(encoding='utf-8'))
 for row in manifest:
  target=D/row['project']/row['file'];files+=1
  if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest()!=row['after_sha256']:mismatches.append(str(target))
 summary=json.loads((batch/'delivery-summary.json').read_text(encoding='utf-8'))
 for row in summary:
  docs=list((D/row['project']/'astraupskill').glob('*.md'));assert len(docs)==9,(row['project'],len(docs))
  for p in docs:
   text=re.sub(r'```.*?```','',p.read_text(encoding='utf-8'),flags=re.S)
   for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
    if '://' not in link:assert (p.parent/unquote(link.split('#')[0])).resolve().exists(),(p,link);links+=1
  assert '(astraupskill/README.md)' in (D/row['project']/'README.md').read_text(encoding='utf-8')
  results.append(row['project'])
record=dict(projects=len(results),files_checked=files,course_files=450,local_links_checked=links,hash_mismatches=mismatches)
(B/'original-verification.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record,indent=2));assert not mismatches
