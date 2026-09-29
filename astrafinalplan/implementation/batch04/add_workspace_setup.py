from pathlib import Path
import json
B=Path('astrafinalplan/implementation/batch04')
for n in range(58,72):
 root=B/'stage'/str(n)
 (root/'package.json').write_text(json.dumps({'name':'astra-crud-workspace-'+str(n),'private':True,'version':'1.0.0','workspaces':['client','server'],'scripts':{'dev':'concurrently -n api,web "npm run dev --workspace server" "npm run dev --workspace client"','test':'npm run test --workspace server','build':'npm run build --workspaces --if-present','db:migrate':'npm run migrate --workspace server','db:seed':'npm run seed --workspace server'},'devDependencies':{'concurrently':'^9.1.2'}},indent=2)+'\n')
 p=root/'server/tsconfig.json';d=json.loads(p.read_text());d['include']=list(dict.fromkeys(d.get('include',[])+['scripts/**/*.ts']));p.write_text(json.dumps(d,indent=2)+'\n')
p=B/'stage/75/package.json';d=json.loads(p.read_text());d['scripts']['test']='npm run test --prefix server';p.write_text(json.dumps(d,indent=2)+'\n')
