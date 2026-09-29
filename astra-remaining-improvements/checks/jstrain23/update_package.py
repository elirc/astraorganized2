import json
from pathlib import Path
s = Path(__file__).resolve().parents[2] / 'stage/58c5c289a8ce'
p = s / 'package.json'
d = json.loads(p.read_text())
for name in ['@prisma/client','prisma','date-fns','lucide-react','uuid','y-websocket','yjs']:
    d['dependencies'].pop(name, None)
d['dependencies']['next'] = '16.3.3'
d['devDependencies']['eslint-config-next'] = '16.3.3'
d['type'] = 'module'
d['engines'] = {'node': '>=22.16.0'}
d['scripts'].update(dev='next dev --hostname 127.0.0.1', start='next start --hostname 127.0.0.1', setup='node scripts/setup.mjs', test='node scripts/test.mjs')
p.write_text(json.dumps(d, indent=2)+'\n')
