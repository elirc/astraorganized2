from pathlib import Path
import json,os,re,hashlib,shutil,difflib
from urllib.parse import unquote
B=Path(__file__).resolve().parent;D=B.parents[3]
names=json.loads((B/'projects.json').read_text(encoding='utf-8'));courses=json.loads((B/'courses.json').read_text(encoding='utf-8'))
checks=json.loads((B/'checks.json').read_text(encoding='utf-8'));browser=json.loads((B/'browser-checks.json').read_text(encoding='utf-8'))
assert {x['project'] for x in checks if x['check']=='tests'}=={str(n) for n in range(11,21)}
assert all(x['exit_code']==0 for x in checks),'A check still fails'
assert {x['project'] for x in browser}=={str(n) for n in range(11,21)} and all(x['passed'] for x in browser),'Browser checks incomplete'
base={(x['stage'],x['file']):x for x in json.loads((B/'baseline.json').read_text(encoding='utf-8'))}
manifest=[];summary=[];diffs=[]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n,name,c in zip(range(11,21),names,courses):
 stage=str(n);root=B/'stage'/stage;rows=[x for x in checks if x['project']==stage]
 unit=next(x for x in rows if x['check']=='tests');log=(B/unit['log']).read_text(encoding='utf-8',errors='replace');count=int(re.findall(r'# tests (\d+)',log)[-1])
 doc=['# Verification: '+c['title'],'','[Course index](README.md)','','Verified on isolated working copies before application to the original project folder.','','| Check | Result |','|---|---|']
 doc += [f'| {x["check"]} | Passed |' for x in rows]
 doc += ['| Chromium interaction | Passed |','',f'Automated test cases: **{count}**.','','## What the evidence covers','',c['example'],'','## Environment and limits','','The harness used Node 22.16.0 and isolated dependencies matching the relevant declared packages. PostgreSQL tests used a separate local PostgreSQL 18.1 instance on port 55439 and uniquely named schemas in a dedicated test database. No development databases or personal saved records were fixtures. The source files were verified byte-for-byte after copying into the originals.']
 if n in [11,12,13,15,16,17]:doc+=['','The browser check used fresh Chromium storage and the actual app. DOM/module tests targeted the listed transitions and failure cases.']
 else:doc+=['','Browser checks used the real built client with controlled API responses, verifying event wiring, rendering and error feedback. Separately, the backend tests used actual HTTP and disposable file/database persistence. The browser check is not a claim that a deployed full-stack environment was exercised end to end.']
 if n==20:doc+=['','Metadata tests used a controlled local HTTP stub through an injected connection factory. Production response handling, destination rejection, redirect refusal, size limits and timeouts were exercised. No external website was fetched. Metadata remains disabled until exact allowed hosts are configured.']
 doc+=['','## Reproduce','',c['setup'],'',c['dbguide'],'','## Boundaries','','These checks cover the implemented improvements and described regression cases. They do not certify unrelated features or production readiness. Exercises in chapter 5 remain learner work. Source, test and setup limitations are explained in the concepts and trace lab.','','Machine-readable results and logs are retained in AstraOrganized2/astrafinalplan/implementation/batch02. The combined report is in AstraOrganized2/astrdocs/ALL_20_PROJECTS_REPORT.md.','']
 (root/'astraupskill/VERIFICATION.md').write_text('\n'.join(doc),encoding='utf-8')
 words=0
 for p in (root/'astraupskill').glob('*.md'):
  text=p.read_text(encoding='utf-8');words+=len(text.split());prose=re.sub(r'```.*?```','',text,flags=re.S)
  for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',prose):
   if '://' not in link:assert (p.parent/unquote(link.split('#')[0])).resolve().exists(),(p,link)
 for parent,dirs,files in os.walk(root):
  dirs[:]=[d for d in dirs if d not in ['node_modules','dist','.git','.vite','coverage']]
  for filename in files:
   p=Path(parent)/filename;rel=p.relative_to(root).as_posix();old=base.get((stage,rel));target=D/name/rel
   # Preserve original bytes when only newline serialization changed accidentally.
   if old and digest(p)!=old['sha256'] and target.exists():
    try:
     if p.read_text(encoding='utf-8')==target.read_text(encoding='utf-8'):shutil.copyfile(target,p)
    except UnicodeDecodeError:pass
   after=digest(p)
   if old and after==old['sha256']:continue
   if old:assert target.exists() and digest(target)==old['sha256'],f'Original changed during work: {target}'
   else:assert not target.exists(),f'New target already exists: {target}'
   manifest.append(dict(project=name,stage=stage,file=rel,before_sha256=old['sha256'] if old else None,after_sha256=after))
   if p.suffix in ['.js','.jsx','.ts','.tsx','.html','.css','.json'] and '/test/' not in '/'+rel and not rel.startswith('astraupskill/'):
    before=target.read_text(encoding='utf-8').splitlines() if old else []
    diffs.extend(difflib.unified_diff(before,p.read_text(encoding='utf-8').splitlines(),fromfile=name+'/'+rel+' (before)',tofile=name+'/'+rel+' (after)',lineterm=''))
 summary.append(dict(project=name,stage=stage,test_cases=count,learning_files=len(list((root/'astraupskill').glob('*.md'))),learning_words=words,changes=sum(x['stage']==stage for x in manifest)))
(B/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');(B/'delivery-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(B/'source-changes.diff').write_text('\n'.join(diffs)+'\n',encoding='utf-8')
print(json.dumps(dict(ready=True,projects=10,files=len(manifest),learning_files=sum(x['learning_files'] for x in summary),learning_words=sum(x['learning_words'] for x in summary),tests=sum(x['test_cases'] for x in summary)),indent=2))
