from pathlib import Path
import subprocess,json
B=Path(__file__).resolve().parent;stage=B/'stage/30217cacf1b9';out=B/'checks/formforge';out.mkdir(exist_ok=True,parents=True)
commands=[['pnpm.cmd','-r','--workspace-concurrency=1','exec','vitest','run','--maxWorkers=2','--reporter=json','--outputFile=astra-verification.json'],['pnpm.cmd','exec','turbo','run','lint','typecheck','build','--concurrency=2'],['pnpm.cmd','sizecheck'],['pnpm.cmd','seed']]
checks=[]
for i,command in enumerate(commands,1):
 result=subprocess.run(command,cwd=stage,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
 (out/f'check-{i}.log').write_text(result.stdout,encoding='utf-8');checks.append({'command':command,'exitCode':result.returncode,'log':f'checks/formforge/check-{i}.log'})
 print(json.dumps(checks[-1]),flush=True)
 if result.returncode:
  print(result.stdout[-7000:],flush=True);(out/'results.json').write_text(json.dumps({'passed':False,'checks':checks},indent=2),encoding='utf-8');raise SystemExit(result.returncode)
reports={name:json.loads((stage/path/'astra-verification.json').read_text(encoding='utf-8')) for name,path in [('core',Path('packages/core')),('data',Path('packages/data')),('api',Path('apps/api')),('web',Path('apps/web'))]}
assert all(r['success'] and r['numFailedTests']==0 for r in reports.values())
result={'passed':True,'tests':sum(r['numPassedTests'] for r in reports.values()),'suites':{n:r['numPassedTests'] for n,r in reports.items()},'checks':checks,'scope':'Isolated dependency install, real code tests, jsdom UI tests, lint, typecheck, builds, bundle budget and seed. No live browser or deployed service claimed.'}
(out/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2),flush=True)
