from pathlib import Path
import subprocess,concurrent.futures,json
B=Path(__file__).resolve().parent;P=B/'stage/092c5e5b7052';C=B/'checks/whiteboard';C.mkdir(parents=True,exist_ok=True)
def install(relative):
 location=P/relative
 result=subprocess.run(['npm.cmd','ci','--no-audit','--no-fund','--cache',str(B/'npm-cache')],cwd=location,capture_output=True,text=True,timeout=300)
 (C/f'install-{relative or "root"}.log').write_text(result.stdout+result.stderr,encoding='utf-8')
 return {'package':relative or 'root','exitCode':result.returncode,'tail':(result.stdout+result.stderr)[-1800:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
 results=list(executor.map(install,['','client','server']))
print(json.dumps(results,indent=2));assert all(r['exitCode']==0 for r in results)
