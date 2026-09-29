"""Validate and materialize a finite, reviewable delivery manifest."""
from pathlib import Path
from urllib.parse import unquote
import json,hashlib,re,sys,xml.etree.ElementTree as ET
from long_paths import extended_path
B=extended_path(Path(__file__).resolve().parent);D=B.parent.parent
key=sys.argv[1];scope=json.loads((B/'scope.json').read_text(encoding='utf-8'));project=next(p for p in scope['eligible'] if p['path']==key)
spec=json.loads((B/'specs'/f'{project["id"]}.json').read_text(encoding='utf-8'));stage=B/'stage'/project['id'];baseline=json.loads((B/'baselines'/f'{project["id"]}.json').read_text(encoding='utf-8'))['files']
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
required=['README.md','01-CODEBASE-MAP.md','02-CONCEPTS.md','03-WORKED-CHANGE.md','04-TESTING-AND-DEBUGGING.md','05-PRACTICE.md','06-SOLUTIONS-AND-REVIEW.md','07-TRACE-LAB.md','VERIFICATION.md']
files=spec['changedFiles']+['astraupskill/'+f for f in required]
assert len(files)==len(set(files))
links=0;words=0
for f in required:
 p=stage/'astraupskill'/f;text=p.read_text(encoding='utf-8');words+=len(text.split())
 assert len(text.split())>=80,f'Too little substantive course content: {f}'
 for url in re.findall(r'\]\(([^)]+)\)',text):
  if re.match(r'[a-z]+:|#',url,re.I):continue
  assert (p.parent/unquote(url.split('#')[0])).resolve().exists(),(p,url)
  links+=1
checks=spec['checks']
if checks['format']=='trx':
 reports=list((B/checks['resultsDirectory']).glob('*.trx'));assert len(reports)==checks['expectedSuites']
 totals={'total':0,'passed':0,'failed':0,'notExecuted':0}
 for p in reports:
  counter=ET.parse(p).find('.//{*}Counters');assert counter is not None
  for k in totals:totals[k]+=int(counter.attrib.get(k,0))
 assert totals['total']==totals['passed']==checks['expectedTests'] and totals['failed']==totals['notExecuted']==0,totals
else:
 evidence=json.loads((B/checks['resultsFile']).read_text(encoding='utf-8'));assert evidence['passed'] is True
 totals=evidence
manifest=[]
for rel in files:
 source=(stage/rel).resolve();target=(D/key/rel).resolve();assert source.is_relative_to(stage.resolve()) and target.is_relative_to((D/key).resolve())
 assert source.is_file(),source
 before=baseline.get(rel);after=hashfile(source)
 assert (target.is_file() and hashfile(target)==before) if before else not target.exists(),f'Original changed: {target}'
 assert before!=after,f'Listed file was not changed: {rel}'
 manifest.append({'file':rel,'before_sha256':before,'after_sha256':after})
out={'project':key,'id':project['id'],'summary':spec['summary'],'checks':checks,'testResults':totals,'courseWords':words,'courseFiles':len(required),'courseLinksChecked':links,'files':manifest,'limits':spec['limits'],'status':'prepared'}
(B/'deliveries').mkdir(exist_ok=True);path=B/'deliveries'/f'{project["id"]}.json';path.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'manifest':str(path),'project':key,'changedFiles':len(files),'courseWords':words,'linksChecked':links,'tests':totals},indent=2))
