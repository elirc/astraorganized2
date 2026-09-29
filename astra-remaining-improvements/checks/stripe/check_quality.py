from pathlib import Path
import ast
import json
import subprocess

C=Path(__file__).resolve().parent
S=C.parents[1]/'stage/af19f6e32dba'
ruff=Path('C:/Users/Owner/AppData/Roaming/Python/Python313/Scripts/ruff.exe')
commands=[
    [str(ruff),'check',str(S/'tests/browser_smoke.py')],
    [str(ruff),'format','--check',str(S/'tests/browser_smoke.py')]
]
results=[]
for command in commands:
    run=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
    results.append({'command':command,'exitCode':run.returncode,'output':run.stdout+run.stderr})
ast.parse((S/'tests/browser_smoke.py').read_text(encoding='utf-8'))
out={'passed':all(item['exitCode']==0 for item in results),'checks':results,'pythonSyntax':'passed'}
(C/'quality.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out))
assert out['passed']
