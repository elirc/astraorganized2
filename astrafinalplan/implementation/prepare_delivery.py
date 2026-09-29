from pathlib import Path
import json,os,hashlib,re,subprocess,difflib
from urllib.parse import unquote
BASE=Path(__file__).resolve().parent
STAGE=BASE/'stage'
DESKTOP=BASE.parents[2]
names=json.loads((BASE/'projects.json').read_text())
courses=json.loads((BASE/'courses.json').read_text())
checks=json.loads((BASE/'checks.json').read_text())
browser=json.loads((BASE/'browser-checks.json').read_text())
assert all(c['exit_code']==0 for c in checks), 'A verification check still fails'
assert {c['project'] for c in checks if c['check']=='tests'} == {f'{i:02}' for i in range(1,11)}
assert len(browser)==6 and all(c['passed'] for c in browser), 'Browser verification incomplete'
baseline={(x['stage'],x['file']):x for x in json.loads((BASE/'baseline.json').read_text())}
changes=[];summaries=[];diffs=[]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for i,name in enumerate(names,1):
 n=f'{i:02}';root=STAGE/n;rows=[c for c in checks if c['project']==n]
 unit=next(c for c in rows if c['check']=='tests')
 log=(BASE/unit['log']).read_text(encoding='utf-8',errors='replace')
 log=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',log)
 count=re.findall(r'# tests (\d+)',log) or re.findall(r'Tests\s+(\d+) passed',log)
 count=unit.get('test_cases',int(count[-1]) if count else None)
 verification=[f'# Verification: {courses[i-1]["title"]}', '', '[Course index](README.md)', '', '**Implementation date:** 2026-09-08. Checks below ran on isolated working copies before the reviewed files were applied to this project.', '', '| Check | Result |', '|---|---|']
 for row in rows:verification.append(f'| {row["check"]} | Passed (exit code 0) |')
 if i<=6:verification.append('| Real Chromium browser interaction | Passed |')
 verification += ['',f'**Automated test cases:** {count if count is not None else "See the test-run log"}.', '', '## What was exercised', '', courses[i-1]['example'], '', '## Environment and scope', '', 'The verification environment used Node 22.16.0. Browser checks used the installed Chromium build. Database suites ran against a fresh, separate PostgreSQL 18.1 instance; development and personal data were not test fixtures.', '', 'Tests and builds ran in working copies with an isolated shared dependency harness; Recipeweb also used its own installed dependency tree for its production build. Source files were checked against the original content before application. Install this project’s declared dependencies locally to run its scripts; no running service or installed dependency tree is assumed merely because the source changes are present.', '', 'The tests target the implemented change and relevant existing behavior. They do not establish production readiness, every browser/version, multi-tab safety or every unrelated workflow. Practice extensions in chapter 5 are not completed features.', '', '## Reproduce the checks', '', ('From this project folder: `npm install`, then `npm test`.' if i<=6 else 'From `server`: install dependencies, set `ASTRA_TEST_DATABASE_URL` to your dedicated `astra_test_*` database, then run `npm test`. See chapter 4 for setup and isolation details.'), '', 'The central implementation report in AstraOrganized2/astrafinalplan/TEN_PROJECTS_IMPLEMENTED.md links all ten courses. Machine-readable check results and logs are retained with the implementation tooling in that repository.', '']
 if unit.get('note'):verification += ['## Test-run detail', '', unit['note'], '']
 (root/'astraupskill/VERIFICATION.md').write_text('\n'.join(verification),encoding='utf-8')
 docwords=0
 for file in (root/'astraupskill').glob('*.md'):
  text=file.read_text(encoding='utf-8');docwords+=len(text.split())
  prose=re.sub(r'```.*?```','',text,flags=re.S)
  for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',prose):
   if '://' in target:continue
   dest=(file.parent/unquote(target.split('#')[0])).resolve()
   assert dest.exists(),f'Broken learning link: {file} -> {target}'
 for parent,dirs,files in os.walk(root):
  dirs[:]=[d for d in dirs if d not in ['node_modules','dist','.git','.vite','coverage']]
  for filename in files:
   file=Path(parent)/filename;rel=file.relative_to(root).as_posix()
   old=baseline.get((n,rel));new_hash=digest(file)
   if old and old['sha256']==new_hash:continue
   target=DESKTOP/name/rel
   if old:assert target.exists() and digest(target)==old['sha256'],f'Original changed since review: {target}'
   else:assert not target.exists(),f'New file would overwrite existing content: {target}'
   entry={'project':name,'stage':n,'file':rel,'before_sha256':old['sha256'] if old else None,'after_sha256':new_hash}
   changes.append(entry)
   if file.suffix in ['.js','.jsx','.ts','.tsx','.html','.css'] and 'test/' not in rel and 'astraupskill/' not in rel:
    before=target.read_text(encoding='utf-8').splitlines() if old else []
    diffs.extend(difflib.unified_diff(before,file.read_text(encoding='utf-8').splitlines(),fromfile=name+'/'+rel+' (before)',tofile=name+'/'+rel+' (after)',lineterm=''))
 summaries.append({'project':name,'stage':n,'test_cases':count,'learning_files':len(list((root/'astraupskill').glob('*.md'))),'learning_words':docwords,'changes':sum(x['stage']==n for x in changes)})
(BASE/'delivery-manifest.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
(BASE/'delivery-summary.json').write_text(json.dumps(summaries,indent=2),encoding='utf-8')
(BASE/'source-changes.diff').write_text('\n'.join(diffs)+'\n',encoding='utf-8')
print(json.dumps({'ready':True,'projects':len(summaries),'changed_or_new_files':len(changes),'learning_files':sum(x['learning_files'] for x in summaries),'learning_words':sum(x['learning_words'] for x in summaries),'tests':sum(x['test_cases'] or 0 for x in summaries)},indent=2))
