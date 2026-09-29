from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]/'stage/af19f6e32dba/src/Billing.Web'
p=root/'package.json'; data=json.loads(p.read_text(encoding='utf-8')); lock=json.loads((root/'package-lock.json').read_text(encoding='utf-8'))
for section in ['dependencies','devDependencies']:
    for name in data[section]:data[section][name]=lock['packages']['node_modules/'+name]['version']
data['engines']={'node':'>=22.16.0 <23'}
p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('Pinned currently verified installed versions.')
