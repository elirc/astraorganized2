from pathlib import Path
import json
B=Path(__file__).resolve().parent;P=B/'stage/e502bf8af566'
def write(rel,text):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
write('package.json',json.dumps({'name':'order-inventory-learning-lab','version':'1.0.0','private':True,'scripts':{'install:all':'npm ci && npm ci --prefix backend && npm ci --prefix frontend','dev:api':'npm run dev --prefix backend','dev:web':'npm run dev --prefix frontend','build':'npm run build --prefix backend && npm run build --prefix frontend','test:web':'npm test --prefix frontend -- --run','test:api':'node scripts/test-database.mjs backend','verify':'node scripts/test-database.mjs verify'},'devDependencies':{'@playwright/test':'1.60.0'}},indent=2)+'\n')
p=P/'backend/package.json';data=json.loads(p.read_text());data['scripts'].update({'build':'tsc','start':'node dist/index.js','test':'jest --runInBand','prisma:deploy':'prisma migrate deploy'});data['devDependencies']['@types/jest']='^29.5.14';p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
write('backend/tsconfig.json',json.dumps({'compilerOptions':{'target':'ES2022','module':'CommonJS','moduleResolution':'Node','strict':True,'esModuleInterop':True,'skipLibCheck':True,'outDir':'dist','rootDir':'src','types':['node','jest']},'include':['src/**/*.ts'],'exclude':['src/**/__tests__/**']},indent=2)+'\n')
write('frontend/tsconfig.json',json.dumps({'compilerOptions':{'target':'ES2022','lib':['ES2022','DOM','DOM.Iterable'],'module':'ESNext','moduleResolution':'Bundler','jsx':'react-jsx','strict':True,'skipLibCheck':True,'noEmit':True,'esModuleInterop':True,'allowImportingTsExtensions':True,'types':['vite/client','vitest/globals','@testing-library/jest-dom']},'include':['src','vite.config.ts','vitest.config.ts']},indent=2)+'\n')
write('.gitignore','node_modules/\nbackend/dist/\nfrontend/dist/\n.env\n.env.local\n*.log\n.verification/\ntest-results/\nplaywright-report/\n')
