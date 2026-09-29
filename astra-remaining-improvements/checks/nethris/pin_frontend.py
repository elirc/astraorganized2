from pathlib import Path
import json

S=Path(__file__).resolve().parents[2]/'stage/71e7b036865c/client'
path=S/'package.json'
data=json.loads(path.read_text(encoding='utf-8'))
lock=json.loads((S/'package-lock.json').read_text(encoding='utf-8'))
versions={name:lock['packages']['node_modules/'+name]['version'] for name in ['react','react-dom','lucide-react','typescript','@vitejs/plugin-react','@types/react','@types/react-dom']}
data['dependencies']={name:versions[name] for name in ['react','react-dom','lucide-react']}
data['devDependencies']={name:versions[name] for name in ['typescript','@vitejs/plugin-react','@types/react','@types/react-dom']}
data['devDependencies']['vite']='6.4.3'
data['engines']={'node':'>=22.16.0 <23'}
path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('Pinned the existing React/icon/type versions and selected Vite 6.4.3.')
