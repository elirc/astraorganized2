from pathlib import Path
import subprocess,os,json
B=Path(__file__).resolve().parent;S=B/'stage/b415b13a50ee';C=B/'checks/interlude/first';C.mkdir(parents=True,exist_ok=True);env=os.environ.copy();env['PLAYWRIGHT_BROWSERS_PATH']=str(B/'playwright-browsers');env['INTERLUDE_RESULTS_DIR']=str(C)
commands=[('build',['npm.cmd','run','build']),('tests',['node','--test','tests/background.test.js','tests/timer.test.js','tests/model.test.js','tests/worker-reliability.test.js']),('browser',['node','node_modules/playwright/cli.js','test','--reporter=json'])]
for label,command in commands:
 r=subprocess.run(command,cwd=S,env=env,capture_output=True,text=True,timeout=240);(C/f'{label}.log').write_text(r.stdout+r.stderr,encoding='utf-8');print(label,r.returncode,flush=True)
 if label=='browser':(C/'browser.json').write_text(r.stdout,encoding='utf-8')
 if r.returncode:print((r.stdout+r.stderr)[-4500:]);raise SystemExit(r.returncode)
