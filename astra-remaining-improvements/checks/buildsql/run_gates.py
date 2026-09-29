from pathlib import Path
import json, os, subprocess, time
B=Path(__file__).resolve().parents[2]
S=B/'stage/0f3292fc93dc'
C=Path(__file__).resolve().parent
marker=C/'install-01-execution.json'
deadline=time.time()+1800
while not marker.exists():
    if time.time()>deadline:raise SystemExit('Installation remains incomplete; no checks were claimed.')
    time.sleep(2)
assert json.loads(marker.read_text(encoding='utf-8'))['exitCode']==0
commands=[
 ('format-01',['node',str(B/'npm-cache/_npx/83e71da30ae7cab2/node_modules/prettier/bin/prettier.cjs'),'--write','src','scripts/merge-content.mjs','scripts/validate-content.mjs','content-src/vol3/assemble.mjs','astraupskill','README.md']),
 ('typecheck-01',['node','--max-old-space-size=512','node_modules/typescript/bin/tsc','-b']),
 ('tests-01',['node','--max-old-space-size=768','node_modules/vitest/vitest.mjs','run','--maxWorkers=1','--no-file-parallelism','--reporter=json','--outputFile='+str(C/'tests-01.json')]),
 ('content-01',['node','--max-old-space-size=512','scripts/validate-content.mjs']),
 ('build-01',['node','--max-old-space-size=512','node_modules/vite/bin/vite.js','build'])]
for name,command in commands:
    assert not (C/f'{name}-execution.json').exists(),name
    start=time.time()
    with (C/f'{name}.log').open('w',encoding='utf-8') as out:result=subprocess.run(command,cwd=S,stdout=out,stderr=subprocess.STDOUT,env=os.environ.copy())
    evidence={'command':command,'exitCode':result.returncode,'seconds':round(time.time()-start,2)}
    (C/f'{name}-execution.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    print(json.dumps(evidence),flush=True)
    if result.returncode:
        print((C/f'{name}.log').read_text(encoding='utf-8')[-15000:],flush=True)
        raise SystemExit(result.returncode)
