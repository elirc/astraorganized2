from pathlib import Path
import sys,subprocess,time,json,os
sys.stdout.reconfigure(encoding='utf-8')
C=Path(__file__).resolve().parent;S=C.parents[1]/'stage/ca549816cdd1'
name=sys.argv[1];assert name.replace('-','').isalnum() and not (C/(name+'.json')).exists()
args=sys.argv[2:] or ['tests'];cmd=[sys.executable,'-m','pytest','-q','--disable-warnings',*args]
env=os.environ.copy();env['PYTHONPATH']=str(S);env['PYTHONIOENCODING']='utf-8';start=time.time()
with (C/(name+'.log')).open('w',encoding='utf-8') as log:r=subprocess.run(cmd,cwd=S,env=env,stdout=log,stderr=subprocess.STDOUT)
evidence={'command':cmd,'exitCode':r.returncode,'seconds':round(time.time()-start,2)};(C/(name+'.json')).write_text(json.dumps(evidence,indent=2),encoding='utf-8');print(json.dumps(evidence));print((C/(name+'.log')).read_text(encoding='utf-8')[-14000:]);sys.exit(r.returncode)
