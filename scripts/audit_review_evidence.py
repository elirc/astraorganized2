from pathlib import Path
import json,re,hashlib,collections
from urllib.parse import unquote
R=Path(__file__).resolve().parents[1];D=R.parent;O=R/'documentation-audit'
units=json.loads((O/'location-inventory.json').read_text(encoding='utf-8'));evidence=[]
cachepath=O/'representative-evidence.json';cache={x['project']:x for x in json.loads(cachepath.read_text(encoding='utf-8'))} if cachepath.exists() else {}
for u in units:
 if u['status'].startswith('Excluded'):continue
 docs=[x for x in u['documents'] if x.get('words',0)>=120 and not x.get('skipped')]
 selected=[]
 # Cover an entry point, a concrete flow, hands-on work, and architecture independently.
 for pattern in [r'(?:LEARNER.GUIDE|(?:fable[^/]*/(?:upskill/)?|docs/upskill/)README\.md)$',r'(?:key.flows|walkthrough|request.lifecycle|codebase.map)',r'(?:good.first.tickets|tier.2|exercise|curriculum/sprint.0[567]|contribution.practice)',r'(?:side.effects|architecture.critique|system.map|adr.*outbox)']:
  matches=[d for d in docs if re.search(pattern,d['path'],re.I)]
  if matches:selected.append(max(matches,key=lambda x:x['words']))
 for d in u['selectedDocuments']:
  if d not in selected:selected.append(d)
 selected=list({d['path']:d for d in selected}.values())[:6]
 old=cache.get(u['path'])
 if old and [(d['path'],d['sha256']) for d in old['documents']]==[(d['path'],d['sha256']) for d in selected]:
  evidence.append(old);continue
 rows=[]
 for d in selected:
  p=D/d['path'];raw=p.read_bytes();t=raw.decode('utf-8-sig',errors='replace');prose=re.sub(r'```.*?```','',t,flags=re.S)
  links=[]
  for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',prose):
   link=link.strip('<>').split(' "')[0]
   if re.match(r'[a-z]+:|#',link,re.I):continue
   target=unquote(link.split('#')[0]);
   if not target:continue
   if len(links)>=20:break
   links.append({'target':link,'exists':(p.parent/target).exists()})
  parts=[t[:900]]
  m=re.search(r'(?im)^#{1,4} .*?(?:Flow 1|Ticket 1|Mission|Exercise|Drill|Lab|Decision)',t)
  if m:parts.append(t[m.start():m.start()+1300])
  rows.append({'path':d['path'],'sha256':hashlib.sha256(raw).hexdigest(),'words':len(t.split()),'sample':parts,'headings':d.get('headings',[])[:12],'localLinkChecks':links,'changedSinceScan':hashlib.sha256(raw).hexdigest()!=d.get('sha256')})
 evidence.append({'project':u['path'],'documents':rows,'sourceExamples':[f['path'] for f in u['files'] if f['source'] and f['bytes']>1000][:8]})
(O/'representative-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
print('Projects sampled:',len(evidence),'documents:',sum(len(x['documents']) for x in evidence),'changed:',sum(d['changedSinceScan'] for x in evidence for d in x['documents']))
