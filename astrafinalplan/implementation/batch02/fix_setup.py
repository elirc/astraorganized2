from pathlib import Path
import json,re
B=Path('astrafinalplan/implementation/batch02/stage')
R=B/'14';(R/'vite.config.js').write_text('import { defineConfig } from "vite";\nimport react from "@vitejs/plugin-react";\nexport default defineConfig({ root: "client", plugins: [react()], server: { host: "127.0.0.1" } });\n')
p=R/'package.json';d=json.loads(p.read_text());d['scripts']['build']='vite build';p.write_text(json.dumps(d,indent=2)+'\n')
# Make the metadata network adapter injectable without changing the production policy.
p=B/'20/server/src/services/metadata.ts';s=p.read_text();s=s.replace('export const requestHtml: Transfer = (url, address, { signal, maxBytes }) => new Promise((resolve, reject) => {','export function createHtmlTransfer(get: typeof https.get = https.get): Transfer {\nreturn (url, address, { signal, maxBytes }) => new Promise((resolve, reject) => {');s=s.replace('const request = https.get(url, {','const request = get(url, {');s=s.replace('  request.on("error", reject);\n});','  request.on("error", reject);\n});\n}\nexport const requestHtml = createHtmlTransfer();');s=s.replace('|| isIP(url.hostname) ||','|| isIP(url.hostname) || url.hostname.includes(":") ||');p.write_text(s,encoding='utf-8')
# Emitted ESM must use runtime-resolvable extensions and the correct output entrypoint.
for p in (B/'20/server').rglob('*.ts'):
 s=p.read_text(encoding='utf-8');s=re.sub(r'(from\s+["\'])(\.[^"\']+)(["\'])',lambda m:m[1]+m[2]+('' if Path(m[2]).suffix else '.js')+m[3],s);p.write_text(s,encoding='utf-8')
p=B/'20/server/package.json';d=json.loads(p.read_text());d['scripts']['start']='node dist/src/server.js';p.write_text(json.dumps(d,indent=2)+'\n')
(B/'20/client/src/vite-env.d.ts').write_text('/// <reference types="vite/client" />\n')
p=B/'18/client/src/App.tsx';s=p.read_text();s=s.replace('${pad(date.getHours())}:${pad(date.getMinutes())}`','${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}.${String(date.getMilliseconds()).padStart(3,"0")}`');s=s.replace('type="datetime-local" value=', 'type="datetime-local" step="0.001" value=');p.write_text(s,encoding='utf-8')
print('Prepared build entrypoints and testable metadata transport.')
