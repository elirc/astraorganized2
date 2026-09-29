from pathlib import Path
import json,subprocess,re
B=Path(__file__).resolve().parent;S=B/'stage'/'e2d8f836b7f9';out=B/'checks'/'kds'
r=subprocess.run(['npm.cmd','test','--','--test-reporter=tap'],cwd=S/'server',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace');(out/'api.log').write_text(r.stdout,encoding='utf-8');print(r.stdout[-5500:]);assert r.returncode==0
assert int(re.search(r'^# tests (\d+)',r.stdout,re.M)[1])==int(re.search(r'^# pass (\d+)',r.stdout,re.M)[1])==12
p=out/'results.json';j=json.loads(p.read_text());j['tests']=12;j['scope']='Real HTTP and in-memory SQLite; actual server startup and Socket.IO polling handshake; React production build; no live browser or persistent-file restart test';p.write_text(json.dumps(j,indent=2),encoding='utf-8')
