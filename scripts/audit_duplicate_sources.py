from pathlib import Path
import json,hashlib,concurrent.futures,collections,re
R=Path(__file__).resolve().parents[1];D=R.parent;O=R/'documentation-audit'
units=json.loads((O/'location-inventory.json').read_text(encoding='utf-8'))
cachepath=O/'source-fingerprints.json';cache=json.loads(cachepath.read_text(encoding='utf-8')) if cachepath.exists() else {}
def analyze(u):
 files=[x for x in u['files'] if x['source'] and x['bytes']>=128 and x['bytes']<=2000000 and not re.search(r'/(?:docs?|documentation|fabledocs\d*|astraupskill|embedded_assets_source)/',x['path'],re.I)]
 signature=hashlib.sha256(json.dumps([(x['path'],x['bytes']) for x in files]).encode()).hexdigest()
 if u['path'] in cache and cache[u['path']]['signature']==signature:return u['path'],cache[u['path']]
 # Compare a deterministic sample of up to 32 substantive files per location.
 available=len(files);files=sorted(files,key=lambda f:hashlib.sha256("/".join(f["path"].split("/")[-3:]).encode()).hexdigest())[:32]
 hashes=[];errors=[]
 for f in files:
  try:
   data=(D/f['path']).read_bytes().replace(b'\r\n',b'\n');hashes.append({'file':f['path'][len(u['path'])+1:],'sha256':hashlib.sha256(data).hexdigest()})
  except OSError as e:errors.append({'file':f['path'],'error':str(e)})
 return u['path'],{'signature':signature,'availableFiles':available,'sampled':available>len(files),'files':hashes,'errors':errors}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for key,value in pool.map(analyze,units):cache[key]=value
cachepath.write_text(json.dumps(cache,indent=2),encoding='utf-8')
prior=json.loads((R/'astradocs/project-review.json').read_text(encoding='utf-8'))
pairs={tuple(sorted((p['path'],q))) for p in prior['projects'] for q in p.get('related_paths',[]) if q!=p['path']}
pairs.update(tuple(sorted((r['path'],r['related_learning_path']))) for r in prior['gemini_learning_relationships'])
pairs.add(('_Organized Desktop/05 Numbered Experiments/ww20','_Organized Desktop/06 AI And Learning/codehelper/ww20'))
pairs.add(('_Organized Desktop/08 App And Product Projects/job track','_Organized Desktop/08 App And Product Projects/job track/job-tracker-next'))
for stem,suffix in [('agora','net'),('atlas','net'),('bazaar','app'),('folio','app'),('harbor','net'),('pulse','net'),('relay','app'),('tracer','net')]:pairs.add(tuple(sorted(('gitvg/'+stem,'gitvg/'+stem+'-'+suffix))))
for u in units:
 for original,mirror in [('gitvg','geminiorganized/General_Gitvg'),('jsharness','geminiorganized/General_Jsharness')]:
  if u['path'].startswith(mirror+'/'):
   pairs.add(tuple(sorted((u['path'],original+u['path'][len(mirror):]))))
sets={k:{f['sha256'] for f in v['files']} for k,v in cache.items()}
exact=collections.defaultdict(list)
for k,v in sets.items():
 if len(v)>=3:exact[tuple(sorted(v))].append(k)
for group in exact.values():
 for a in group:
  for b in group:
   if a<b:pairs.add((a,b))
rows=[]
for a,b in sorted(pairs):
 if a not in sets or b not in sets:continue
 x,y=sets[a],sets[b];common=x&y;small=min(len(x),len(y));large=max(len(x),len(y));overlap=len(common)/small if small else 0
 pathsx={f['file'].lower() for f in cache[a]['files']};pathsy={f['file'].lower() for f in cache[b]['files']};pathOverlap=len(pathsx&pathsy)/max(1,min(len(pathsx),len(pathsy)))
 gemini=a.startswith('geminiorganized/') or b.startswith('geminiorganized/')
 decision='group-copy-family' if (small>=3 and x==y) or (small>=5 and overlap>=.8 and small/large>=.7) or (gemini and small>=5 and pathOverlap>=.75 and overlap>=.1) else 'related-or-uncertain-do-not-merge'
 manual=(a,b) in {tuple(sorted(p)) for p in [('finance-dashboard','geminiorganized/General_Finance-Dashboard'),('newcodexJS','geminiorganized/General_Newcodexjs'),('perch','geminiorganized/General_Perch')]}
 if manual:decision='group-copy-family'
 if a=='_Organized Desktop/08 App And Product Projects/job track' and b==a+'/job-tracker-next':decision='group-copy-family';manual=True
 rows.append({'paths':[a,b],'sourceFilesCompared':[len(cache[a]['files']),len(cache[b]['files'])],'uniqueHashes':[len(x),len(y)],'matchingSourceHashes':len(common),'smallerSourceOverlap':round(overlap,4),'relativePathOverlap':round(pathOverlap,4),'decision':decision,'basis':'Current substantive source hashes (up to 32 deterministic samples for large locations), normalized only for CRLF; prior relationships were candidates, not proof. Documents may differ.'})
 if manual:rows[-1]['basis']='Manual version-family decision: matching application identity and source structure, with shared substantive source hashes; later modifications explain differences. This does not assert complete byte identity.'
 if a.startswith('gitvg/') and b.startswith('gitvg/') and decision!='group-copy-family':
  rows[-1]['decision']='related-implementation-variant-kept-separate'
  rows[-1]['basis']='Same product concept, separate application implementation/teaching track rather than a client/server package. Current source comparison does not establish a copy; retained separately and explicitly flagged as related.'
(O/'duplicate-source-review.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print('Hashed locations',len(cache),'source files',sum(len(x['files']) for x in cache.values()),'pair decisions',collections.Counter(x['decision'] for x in rows))
for x in rows:
 if x['decision']!='group-copy-family':print(x['paths'],x['matchingSourceHashes'],x['smallerSourceOverlap'],x['relativePathOverlap'])
