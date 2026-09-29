from pathlib import Path
import hashlib,json,shutil
C=Path(__file__).resolve().parent;B=C.parents[1];S=B/'stage/af19f6e32dba'
baseline=json.loads((B/'baselines/af19f6e32dba.json').read_text(encoding='utf-8'))['files']
target=S/'docs/original';target.mkdir(exist_ok=False)
count=0
for name,digest in baseline.items():
    source=S/name
    assert hashlib.sha256(source.read_bytes()).hexdigest()==digest,name
    if source.suffix not in {'.md','.cs','.csproj','.sln','.json','.tsx','.ts','.css','.html'} and source.name not in {'.gitignore','.env.example'}:continue
    if source.name.startswith('appsettings'):
        billing=json.loads(source.read_text(encoding='utf-8')).get('Billing',{})
        for key,value in billing.items():
            if 'secret' in key.lower():assert value=='dev_secret_replace_me','Do not place a configured secret in learning documents'
    out=target/(name+'.txt');out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,out);count+=1
print(json.dumps({'preservedOriginalTextFiles':count}))
