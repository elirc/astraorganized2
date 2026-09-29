from pathlib import Path
import subprocess,os,json
B=Path(__file__).resolve().parent;S=B/'stage/6844a7b03c83';C=B/'checks/quiz-board/final';C.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env['PLAYWRIGHT_BROWSERS_PATH']=str(B/'playwright-browsers');env['QUIZ_RESULTS_DIR']=str(C)
r=subprocess.run(['node','--test','test/store.test.js'],cwd=S,env=env,capture_output=True,text=True,timeout=60);(C/'store.tap').write_text(r.stdout+r.stderr,encoding='utf-8');assert r.returncode==0 and '# pass 20' in r.stdout and '# fail 0' in r.stdout
for rel in ['main.js','board.js','edit.js','data.js','store.js','server.js']:
 r=subprocess.run(['node','--check',rel],cwd=S,env=env,capture_output=True,text=True,timeout=20);assert r.returncode==0,r.stderr
r=subprocess.run(['node','node_modules/playwright/cli.js','test','--reporter=json'],cwd=S,env=env,capture_output=True,text=True,timeout=180);(C/'browser.json').write_text(r.stdout,encoding='utf-8');(C/'browser.log').write_text(r.stderr,encoding='utf-8');assert r.returncode==0,(r.stdout[-5000:],r.stderr[-1000:]);stats=json.loads(r.stdout)['stats'];assert stats['expected']==11 and stats['unexpected']==stats['skipped']==stats['flaky']==0,stats
result={'passed':True,'tests':31,'storeTests':20,'chromiumScenarios':11,'syntaxChecks':6,'environment':'Node 22.16.0; Playwright 1.60.0; Chromium; isolated browser contexts and loopback static server','checks':['CRUD and persisted reload','Actual two-tab Web Locks and stale editor conflicts','Quota failure and corrupt-data recovery','Literal text rendering and import/export','Round progress and keyboard dialog behavior','Desktop/narrow screenshots and overflow checks','Static asset allowlist and response headers']}
(C/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
