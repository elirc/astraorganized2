from pathlib import Path
import subprocess,json,tempfile,os
B=Path(__file__).resolve().parent;P=B/'stage/092c5e5b7052';C=B/'checks/whiteboard';env=os.environ.copy();env['PLAYWRIGHT_BROWSERS_PATH']=str(B/'playwright-browsers');env['CI']='1'
r=subprocess.run(['npm.cmd','run','build'],cwd=P,env=env,capture_output=True,text=True,timeout=180);(C/'build.log').write_text(r.stdout+r.stderr,encoding='utf-8');print('build',r.returncode,flush=True);assert r.returncode==0
with tempfile.TemporaryDirectory(prefix='whiteboard-layout-') as temporary:
 env['WHITEBOARD_E2E_DATA_DIR']=temporary
 r=subprocess.run(['node',str(P/'node_modules/playwright/cli.js'),'test','--grep','syncs markdown|narrow viewport','--reporter=json'],cwd=P,env=env,capture_output=True,text=True,timeout=180)
 (C/'layout-playwright.json').write_text(r.stdout,encoding='utf-8');(C/'layout-server.log').write_text(r.stderr,encoding='utf-8');e=json.loads(r.stdout);print(json.dumps(e['stats']),flush=True)
 assert r.returncode==0 and e['stats']['expected']==2 and e['stats']['unexpected']==e['stats']['flaky']==e['stats']['skipped']==0
result=json.loads((C/'results.json').read_text(encoding='utf-8'));result['layoutRechecks']=2;result['buttonLabelsFit']=True;(C/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
