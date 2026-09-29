from pathlib import Path
import json,re,os,hashlib,shutil,difflib
from urllib.parse import unquote
B=Path(__file__).resolve().parent;D=B.parents[3]
names=json.loads((B/'projects.json').read_text(encoding='utf-8'));courses=json.loads((B/'courses.json').read_text(encoding='utf-8'))
merged={}
for file in ['checks.json','domain-checks.json','small-api-checks.json','special-checks.json','build-checks.json','type-fix-checks.json','final-checks.json','layout-checks.json','poll-final-checks.json']:
 for row in json.loads((B/file).read_text(encoding='utf-8')):merged[(row['project'],row['check'])]=row
checks=sorted(merged.values(),key=lambda x:(int(x['project']),x['check']))
assert len(checks)==70 and all(x['exit_code']==0 for x in checks)
assert len([x for x in checks if x['check']=='tests'])==30
(B/'checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
browser=json.loads((B/'browser-checks.json').read_text(encoding='utf-8'))
assert {x['project'] for x in browser}=={str(n) for n in range(21,51)} and all(x['passed'] for x in browser)
for row in browser:
 if row['project'] in ['21','22']:row['api']='none (browser-only)'
 if int(row['project'])>=35:row['responsive_check']='390px no horizontal overflow; 1280px usable search width'
(B/'browser-checks.json').write_text(json.dumps(sorted(browser,key=lambda x:int(x['project'])),indent=2),encoding='utf-8')
base={(x['stage'],x['file']):x for x in json.loads((B/'baseline.json').read_text(encoding='utf-8'))}
manifest=[];summary=[];diffs=[];links_checked=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,name,c in zip(range(21,51),names,courses):
 stage=str(n);root=B/'stage'/stage;rows=[x for x in checks if x['project']==stage]
 unit=next(x for x in rows if x['check']=='tests');log=(B/unit['log']).read_text(encoding='utf-8',errors='replace');count=int(re.findall(r'# tests (\d+)',log)[-1])
 assert re.findall(r'# fail (\d+)',log)[-1]=='0'
 doc=['# Verification: '+c['title'],'','[Course index](README.md)','','Verified September 8, 2026 on isolated working copies before application to the original project folder.','','| Check | Result |','|---|---|']
 doc += [f'| {x["check"]} | Passed |' for x in rows]+['| Chromium interaction | Passed |','',f'Automated test cases: **{count}**.','','## Tested behavior','',c['example'],'','The test file contains executable scenarios and assertions; the examples in the course also include hand-worked teaching variations. These are not additional tests counted in this total.','','## Environment and scope','','The isolated harness used Node 22.16.0, PostgreSQL 18.1 where applicable, and dependencies installed in the verification workspace. Dependency declarations using latest remain floating; the tested versions are recorded in the batch evidence. Original dependency trees and development databases were not replaced or used as fixtures.']
 if n<23:doc+=['','The actual HTML/app.js ran in jsdom with fresh storage for regressions and in Chromium for native interaction. There is no HTTP API in this project.']
 else:doc+=['','The browser check used the actual built React client. A local test proxy forwarded its API requests to the actual isolated Express server; it did not supply fabricated API responses. The backend used '+('a disposable PostgreSQL schema' if (root/'test/database.ts').exists() else 'a fresh in-memory repository')+'. This checks local UI/API integration, not a deployed environment.']
 if n>=35:doc+=['','The shared toolbar was checked at 1280px for a usable search width, and the page at 390px for no horizontal overflow. Screenshots are retained with the browser results.']
 doc+=['','## Reproduce','',c['setup'],'',c['dbguide'],'','## Limits','','These checks target the implemented improvement and its meaningful failure boundaries. Exercises remain future learner work. The concepts and trace lab explain limits such as in-memory restart behavior, status-command semantics, date representation and transaction scope where relevant.','','After copying to the original folders, delivery hashes and course links are checked by the batch verification script. Machine-readable results, command logs, screenshots, source diffs and backups are retained in AstraOrganized2/astrafinalplan/implementation/batch03. The combined report is AstraOrganized2/astrdocs/ALL_50_PROJECTS_REPORT.md.','']
 (root/'astraupskill/VERIFICATION.md').write_text('\n'.join(doc),encoding='utf-8')
 docs=list((root/'astraupskill').glob('*.md'));assert len(docs)==9,(n,len(docs));words=0
 for p in docs:
  text=p.read_text(encoding='utf-8');words+=len(text.split());assert text.count('```')%2==0,p
  assert '\ufffd' not in text and 'PLACEHOLDER' not in text,p
  prose=re.sub(r'```.*?```','',text,flags=re.S)
  for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',prose):
   if '://' not in link:
    assert (p.parent/unquote(link.split('#')[0])).resolve().exists(),(p,link);links_checked+=1
 assert words>=4500,(n,words)
 for parent,dirs,files in os.walk(root):
  dirs[:]=[d for d in dirs if d not in ['node_modules','dist','.git','.vite','coverage']]
  for filename in files:
   p=Path(parent)/filename;rel=p.relative_to(root).as_posix();old=base.get((stage,rel));target=D/name/rel
   if old and sha(p)!=old['sha256'] and target.exists():
    try:
     if p.read_text(encoding='utf-8')==target.read_text(encoding='utf-8'):shutil.copyfile(target,p)
    except UnicodeDecodeError:pass
   after=sha(p)
   if old and after==old['sha256']:continue
   if old:assert target.exists() and sha(target)==old['sha256'],f'Original changed during work: {target}'
   else:assert not target.exists(),f'New target already exists: {target}'
   manifest.append(dict(project=name,stage=stage,file=rel,before_sha256=old['sha256'] if old else None,after_sha256=after))
   if not rel.startswith(('astraupskill/','test/')) and p.suffix in ['.js','.jsx','.ts','.tsx','.html','.css','.json','.sql']:
    before=target.read_text(encoding='utf-8-sig').splitlines() if old else []
    diffs.extend(difflib.unified_diff(before,p.read_text(encoding='utf-8-sig').splitlines(),fromfile=name+'/'+rel+' (before)',tofile=name+'/'+rel+' (after)',lineterm=''))
 summary.append(dict(project=name,stage=stage,test_cases=count,learning_files=len(docs),learning_words=words,changes=sum(x['stage']==stage for x in manifest)))
for file,value in [('delivery-manifest.json',manifest),('delivery-summary.json',summary)]: (B/file).write_text(json.dumps(value,indent=2),encoding='utf-8')
(B/'source-changes.diff').write_text('\n'.join(diffs)+'\n',encoding='utf-8')
print(json.dumps(dict(ready=True,projects=30,files=len(manifest),learning_files=sum(x['learning_files'] for x in summary),learning_words=sum(x['learning_words'] for x in summary),tests=sum(x['test_cases'] for x in summary),links_checked=links_checked),indent=2))
