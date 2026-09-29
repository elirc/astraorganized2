from pathlib import Path
import re,json,shutil
B=Path('astrafinalplan/implementation/batch04');R=B/'stage';kinds=[]
for n in range(51,57):
 root=R/str(n);ts=(root/'server/src/index.ts').exists();p=root/('server/src/index.ts' if ts else 'server/server.js');s=p.read_text(encoding='utf-8')
 s = s if 'import { pathToFileURL }' in s else 'import { pathToFileURL } from "node:url";\n'+s
 s = s if 'export const app = express();' in s else s.replace('const app = express();','export const app = express();',1)
 s=re.sub(r'^app.listen\(port, (.*?^\}\);|[^\n]+\);)',lambda m:'if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) '+m[0],s,flags=re.M|re.S)
 # Express 4 and 5 both receive async failures through next().
 if ts:
  s=re.sub(r'app\.(get|post|put|patch|delete)\(("[^\"]+"), async (\([^\n]*?\) => \{.*?^\})\);',r'app.\1(\2, asyncRoute(async \3));',s,flags=re.M|re.S)
  if 'function asyncRoute(' not in s: s+='\nfunction asyncRoute(handler: (req: express.Request, res: express.Response, next: express.NextFunction) => Promise<unknown>): express.RequestHandler {\n  return (req,res,next) => { Promise.resolve(handler(req,res,next)).catch(next); };\n}\n'
 elif 'Send a JSON object.' not in s:
  s=s.replace('app.use(express.json());','''app.use(express.json());
app.use((req,res,next) => {
  if (["POST","PUT","PATCH"].includes(req.method) && (!req.body || typeof req.body !== "object" || Array.isArray(req.body)))
    return res.status(400).json({ error: "Send a JSON object." });
  next();
});''')
 p.write_text(s,encoding='utf-8')
 package=root/'package.json';j=json.loads(package.read_text(encoding='utf-8-sig'));j['scripts']['test']='tsx --test test/*.test.ts' if ts else 'node --test test/*.test.js';j['scripts']['build']='vite build';package.write_text(json.dumps(j,indent=2)+'\n',encoding='utf-8')
 if not ts:
  p=root/'client/src/main.jsx';p.write_text('import React from "react";\nimport { createRoot } from "react-dom/client";\nimport App from "./App.jsx";\ncreateRoot(document.getElementById("root")).render(<App />);\n',encoding='utf-8')
  p=root/'client/index.html';s=p.read_text(encoding='utf-8').replace('/src/App.jsx','/src/main.jsx');p.write_text(s,encoding='utf-8')
  p=root/'vite.config.js';p.write_text('import { defineConfig } from "vite";\nimport react from "@vitejs/plugin-react";\nexport default defineConfig({ root: "client", plugins: [react()] });\n',encoding='utf-8')
 else:
  p=root/'client/src/vite-env.d.ts'
  if not p.exists():p.write_text('/// <reference types="vite/client" />\n',encoding='utf-8')
 p=root/('client/src/App.tsx' if ts else 'client/src/App.jsx');s=p.read_text(encoding='utf-8');counter=[0]
 def label(m):
  if ' id=' in m[3]:return m[0]
  counter[0]+=1;ident='lesson-field-'+str(counter[0]);return f'<label htmlFor="{ident}">{m[1]}</label>'+m[2]+m[3].replace('<'+m[4],'<'+m[4]+' id="'+ident+'"',1)
 # Static labels only: leave mapped/dynamic labels for project-specific treatment.
 s=re.sub(r'<label>([A-Za-z][A-Za-z /()-]*)</label>(\s*)(<(input|select|textarea)\b[^>]*>)',label,s)
 s=s.replace('<p className="message"','<p role="status" className="message"')
 p.write_text(s,encoding='utf-8');kinds.append({'stage':str(n),'typescript':ts})
(B/'kinds.json').write_text(json.dumps(kinds,indent=2),encoding='utf-8')
source=B.parent/'batch02/node_modules/@types/pg';target=B/'node_modules/@types/pg';target.parent.mkdir(parents=True,exist_ok=True)
if not target.exists():shutil.copytree(source,target)
print('Added importable server entrypoints, async error handling and runnable client entrypoints for 28 API apps.')
