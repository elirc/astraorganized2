from pathlib import Path
import json,os,subprocess,sys,time
C=Path(__file__).resolve().parent;S=C.parents[1]/'stage/af19f6e32dba'
name=sys.argv[1];relative=sys.argv[2];args=sys.argv[3:]
assert name.replace('-','').isalnum() and not (C/(name+'.json')).exists()
cwd=(S/relative).resolve();assert cwd.is_relative_to(S.resolve())
env=os.environ.copy();env['DOTNET_CLI_TELEMETRY_OPTOUT']='1';env['DOTNET_NOLOGO']='1';env['PYTHONIOENCODING']='utf-8'
started=time.time()
with (C/(name+'.log')).open('w',encoding='utf-8') as log:
    result=subprocess.run(args,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
evidence={'command':args,'workingDirectory':relative,'exitCode':result.returncode,'seconds':round(time.time()-started,2)}
(C/(name+'.json')).write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print(json.dumps(evidence));sys.stdout.reconfigure(encoding='utf-8');print((C/(name+'.log')).read_text(encoding='utf-8')[-10000:]);sys.exit(result.returncode)
