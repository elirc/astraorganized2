from pathlib import Path
import json,subprocess,sys,time
C=Path(__file__).resolve().parent;S=C.parents[1]/'stage/58c5c289a8ce'
name=sys.argv[1];assert name in {'foundation-01','backend-01','backend-02','backend-03','final-01'}
assert not (C/(name+'.json')).exists()
files=['test/schema.test.mjs','test/merge.test.mjs'] if name=='foundation-01' else sorted(str(p.relative_to(S)) for p in (S/'test').glob('*.test.mjs'))
command=['node','--test',*files];start=time.time()
with (C/(name+'.log')).open('w',encoding='utf-8') as log:result=subprocess.run(command,cwd=S,stdout=log,stderr=subprocess.STDOUT)
evidence={'command':command,'exitCode':result.returncode,'seconds':round(time.time()-start,2)}
(C/(name+'.json')).write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print(json.dumps(evidence),flush=True);print((C/(name+'.log')).read_text(encoding='utf-8')[-11000:],flush=True)
sys.exit(result.returncode)
