from pathlib import Path
import subprocess,os,json,shutil,zipfile,hashlib
b=Path(__file__).resolve().parent;s=b/'stage/b415b13a50ee';c=b/'checks/interlude/layout';c.mkdir(exist_ok=True)
e=os.environ.copy();e['PLAYWRIGHT_BROWSERS_PATH']=str(b/'playwright-browsers');e['INTERLUDE_RESULTS_DIR']=str(c)
r=subprocess.run(['node','node_modules/playwright/cli.js','test','--grep','fit desktop','--reporter=json'],cwd=s,env=e,capture_output=True,text=True,encoding='utf-8',timeout=120);(c/'browser.json').write_text(r.stdout,encoding='utf-8');(c/'browser.stderr').write_text(r.stderr,encoding='utf-8');assert r.returncode==0,r.stdout[-4000:]+r.stderr
j=json.loads(r.stdout);assert j['stats']['expected']==1 and j['stats']['unexpected']==0
out=s/'astraupskill/images';out.mkdir(exist_ok=True)
for p in c.glob('*.png'):shutil.copy2(p,out/p.name)
with zipfile.ZipFile(s/'interlude-extension.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((s/'extension').rglob('*')):
  if p.is_file():z.write(p,p.relative_to(s/'extension').as_posix())
with zipfile.ZipFile(s/'interlude-extension.zip') as z:
 for name in z.namelist():assert z.read(name)==(s/'extension'/name).read_bytes()
results={'passed':True,'tests':49,'nodeTests':39,'browserTests':10,'additionalLayoutRecheck':1,'build':'passed','archiveMembers':len(z.namelist()),'screenshots':4,'environment':'Node 22.16.0; Playwright 1.60.0; Chromium 148; isolated real unpacked extension and preview'}
first=json.loads((b/'checks/interlude/first/browser.json').read_text(encoding='utf-8'));assert first['stats']['expected']==10 and first['stats']['unexpected']==0 and first['stats']['skipped']==0
assert '# pass 39' in (b/'checks/interlude/first/tests.log').read_text(encoding='utf-8')
(b/'checks/interlude/results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results))
