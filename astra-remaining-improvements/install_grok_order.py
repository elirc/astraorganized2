from pathlib import Path
import subprocess,concurrent.futures,json,os
B=Path(__file__).resolve().parent;P=B/'stage/e502bf8af566';C=B/'checks/grok-order';C.mkdir(parents=True,exist_ok=True)
def install(relative):
 result=subprocess.run(['npm.cmd','install','--no-audit','--no-fund','--cache',str(B/'npm-cache')],cwd=P/relative,capture_output=True,text=True,timeout=360)
 (C/f'install-{relative or "root"}.log').write_text(result.stdout+result.stderr,encoding='utf-8');return {'package':relative or 'root','exitCode':result.returncode,'tail':(result.stdout+result.stderr)[-1800:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor: results=list(executor.map(install,['','backend','frontend']))
print(json.dumps(results,indent=2));assert all(r['exitCode']==0 for r in results)
