from pathlib import Path
import subprocess,json,tempfile,os,re
B=Path(__file__).resolve().parent;P=B/'stage/092c5e5b7052';C=B/'checks/whiteboard';C.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env['PLAYWRIGHT_BROWSERS_PATH']=str(B/'playwright-browsers');env['CI']='1'
commands=[('backend',['npm.cmd','run','test:server']),('lint',['npm.cmd','run','lint']),('build',['npm.cmd','run','build'])]
for name,command in commands:
 result=subprocess.run(command,cwd=P,env=env,capture_output=True,text=True,timeout=180)
 (C/f'{name}.log').write_text(result.stdout+result.stderr,encoding='utf-8');print(name,result.returncode,(result.stdout+result.stderr)[-1800:],flush=True);assert result.returncode==0,name
 if name=='backend':assert '# tests 17' in result.stdout and '# pass 17' in result.stdout and '# fail 0' in result.stdout
with tempfile.TemporaryDirectory(prefix='whiteboard-e2e-') as temporary:
 env['WHITEBOARD_E2E_DATA_DIR']=temporary
 result=subprocess.run(['node',str(P/'node_modules/playwright/cli.js'),'test','--reporter=json'],cwd=P,env=env,capture_output=True,text=True,timeout=300)
 (C/'playwright.json').write_text(result.stdout,encoding='utf-8');(C/'playwright-server.log').write_text(result.stderr,encoding='utf-8')
 try: evidence=json.loads(result.stdout);stats=evidence['stats'];print(json.dumps(stats),flush=True)
 except Exception: print(result.stdout[-5000:],result.stderr[-3000:],flush=True);raise
 if result.returncode!=0:
  print(json.dumps(evidence.get('errors',[])),flush=True)
  def failures(suites):
   for suite in suites:
    for spec in suite.get('specs',[]):
     if not spec.get('ok'): print(json.dumps(spec,indent=2),flush=True)
    failures(suite.get('suites',[]))
  failures(evidence.get('suites',[]))
 assert result.returncode==0 and stats['expected']==8 and stats['unexpected']==stats['flaky']==stats['skipped']==0
result={'passed':True,'tests':25,'backendTests':17,'browserTests':8,'lint':True,'typecheckAndBuild':True,'environment':'Node 22.16.0; npm 10.9.2; locked dependencies; Chromium 148.0.7778.96; real HTTP/WebSocket/Yjs, temporary files and separate-process startup','limits':['No Docker daemon verification, authenticated access, multi-process storage locking, or per-edit disk receipt.']}
(C/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
