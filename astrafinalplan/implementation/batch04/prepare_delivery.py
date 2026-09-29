from pathlib import Path
import json,re,os,hashlib,shutil,difflib
from urllib.parse import unquote
B=Path(__file__).resolve().parent;D=B.parents[3]
names=json.loads((B/'projects.json').read_text(encoding='utf-8'));courses=json.loads((B/'courses.json').read_text(encoding='utf-8'))
merged={}
for file in sorted(B.glob('*.json'),key=lambda p:p.stat().st_mtime):
 if file.name in ('checks.json','browser-checks.json'):continue
 rows=json.loads(file.read_text(encoding='utf-8'))
 if isinstance(rows,list):
  for row in rows:
   if isinstance(row,dict) and all(k in row for k in ['project','check','exit_code']):merged[(row['project'],row['check'])]=row
checks=sorted(merged.values(),key=lambda x:(int(x['project']),x['check']))
assert all(x['exit_code']==0 for x in checks),[x for x in checks if x['exit_code']]
for kind,count in [('tests',25),('build',25),('server-build',14),('setup-migrate',14),('setup-seed',14)]:assert sum(x['check']==kind for x in checks)==count,(kind,count)
(B/'checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
browser=json.loads((B/'browser-checks.json').read_text(encoding='utf-8'))
assert {x['project'] for x in browser}=={str(n) for n in range(51,76)} and all(x['passed'] for x in browser),[x['project'] for x in browser if not x['passed']]
base={(x['stage'],x['file']):x for x in json.loads((B/'baseline.json').read_text(encoding='utf-8'))}
manifest=[];summary=[];diffs=[];links_checked=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,name,c in zip(range(51,76),names,courses):
 stage=str(n);root=B/'stage'/stage;rows=[x for x in checks if x['project']==stage]
 unit=next(x for x in rows if x['check']=='tests');log=(B/unit['log']).read_text(encoding='utf-8',errors='replace');log=re.sub(r'\x1b\[[0-9;]*m','',log)
 if n in (73,74):count=int(re.findall(r'Tests\s+(\d+) passed',log)[-1])
 else:
  count=int(re.findall(r'# tests (\d+)',log)[-1]);assert re.findall(r'# fail (\d+)',log)[-1]=='0'
 br=next(x for x in browser if x['project']==stage)
 doc=['# Verification: '+c['title'],'','[Course index](README.md)','','Verified September 8, 2026 in isolated working copies before application to the original folder.','','| Check | Result |','|---|---|']
 doc += [f'| {x["check"]} | Passed |' for x in rows]+['| Chromium interaction | Passed |','',f'Automated test cases: **{count}**.','','## Tested behavior','',c['example'],'','The course contains additional hand-worked examples and optional exercises. These are not counted as implemented tests.','','## Environment and scope','','Node 22.16.0, PostgreSQL 18.1 where applicable, and dependencies installed in the isolated verification workspace were used. The exact dependency versions are recorded with the batch evidence. Floating dependency declarations remain floating; a clean dependency install was not repeated in every original folder.']
 if n in (73,74):doc+=['','The built React app was opened in a fresh Chromium browser context. A malformed backup was rejected through its real import screen. Automated tests also exercise nested validation and preservation of existing data.']
 else:doc+=['','Chromium used the actual built client and actual isolated Express server. A local verification proxy forwarded API requests and adjusted CORS for its temporary origin; it did not fabricate API responses. Data used '+('a disposable PostgreSQL schema' if (root/'test/database.ts').exists() else 'temporary SQLite storage' if n in (72,75) else 'a fresh in-memory repository')+'.']
 doc+=['',f'The browser screenshot was also captured at a 390px viewport. Measured document width: {br["responsive"]["content"]}px. This is a layout smoke check, not a complete accessibility or device audit.','','## Reproduce','',c['setup'],'',c['dbguide'],'','## Limits','',c['limitations'],'','These are focused learning improvements, not a production-readiness certification. Existing integrations and all optional exercises are outside the checked boundary unless named above.','','Delivery hashes and local course links are checked after applying the files. Logs, screenshots, diffs and backups are in AstraOrganized2/astrafinalplan/implementation/batch04. The combined report is AstraOrganized2/astrdocs/ALL_75_PROJECTS_REPORT.md.','']
 (root/'astraupskill/VERIFICATION.md').write_text('\n'.join(doc),encoding='utf-8')
 docs=list((root/'astraupskill').glob('*.md'));assert len(docs)==9;words=0
 for p in docs:
  text=p.read_text(encoding='utf-8');words+=len(text.split());assert text.count('```')%2==0,p
  assert '\ufffd' not in text and 'PLACEHOLDER' not in text,p
  for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',re.sub(r'```.*?```','',text,flags=re.S)):
   if '://' not in link:assert (p.parent/unquote(link.split('#')[0])).resolve().exists(),(p,link);links_checked+=1
 assert words>=4500,(n,words)
 for parent,dirs,files in os.walk(root):
  dirs[:]=[d for d in dirs if d not in ['node_modules','dist','.git','.vite','coverage','build']]
  for filename in files:
   if filename.endswith('.tsbuildinfo'):continue
   p=Path(parent)/filename;rel=p.relative_to(root).as_posix();old=base.get((stage,rel));target=D/name/rel
   if rel.endswith('package-lock.json') and not old:continue
   if old and sha(p)!=old['sha256'] and target.exists():
    try:
     if p.read_text(encoding='utf-8')==target.read_text(encoding='utf-8'):shutil.copyfile(target,p)
    except UnicodeDecodeError:pass
   after=sha(p)
   if old and after==old['sha256']:continue
   if old:assert target.exists() and sha(target)==old['sha256'],f'Original changed: {target}'
   else:assert not target.exists(),f'New target already exists: {target}'
   assert n!=75 or rel.startswith(('client/','server/','test/','astraupskill/')) or rel in ('README.md','package.json'),rel
   manifest.append(dict(project=name,stage=stage,file=rel,before_sha256=old['sha256'] if old else None,after_sha256=after))
   if not rel.startswith(('astraupskill/','test/')) and p.suffix in ['.js','.jsx','.ts','.tsx','.html','.css','.json','.sql']:
    before=target.read_text(encoding='utf-8-sig').splitlines() if old else []
    diffs.extend(difflib.unified_diff(before,p.read_text(encoding='utf-8-sig').splitlines(),fromfile=name+'/'+rel+' (before)',tofile=name+'/'+rel+' (after)',lineterm=''))
 summary.append(dict(project=name,stage=stage,test_cases=count,learning_files=len(docs),learning_words=words,changes=sum(x['stage']==stage for x in manifest)))
for file,value in [('delivery-manifest.json',manifest),('delivery-summary.json',summary)]: (B/file).write_text(json.dumps(value,indent=2),encoding='utf-8')
(B/'source-changes.diff').write_text('\n'.join(diffs)+'\n',encoding='utf-8')
print(json.dumps(dict(ready=True,projects=25,files=len(manifest),learning_files=sum(x['learning_files'] for x in summary),learning_words=sum(x['learning_words'] for x in summary),tests=sum(x['test_cases'] for x in summary),links_checked=links_checked),indent=2))
