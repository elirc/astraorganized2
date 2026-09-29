from pathlib import Path
import re,json
B=Path('astrafinalplan/implementation/batch04')
for n in (52,53,54):
 p=B/'stage'/str(n)/'client/src/App.tsx';s=p.read_text(encoding='utf-8').replace('type="number" min="0"','type="number" min="0" step="0.01"');p.write_text(s,encoding='utf-8')
for n in range(58,72):
 for p in (B/'stage'/str(n)/'server/src/controllers').glob('*.ts'):
  s=p.read_text(encoding='utf-8');s=re.sub(r'(?<!String\()req\.params\.(id|slug|emoji)(?!\w)',r'String(req.params.\1)',s);p.write_text(s,encoding='utf-8')
for n in range(58,62):
 for p in (B/'stage'/str(n)/'server/db/seeds').glob('*.ts'):
  s=p.read_text(encoding='utf-8');s=s.replace(']);','].map(record => ({...record,tags:JSON.stringify(record.tags)})));');p.write_text(s,encoding='utf-8')
for p in (B/'stage/66/server/db/seeds').glob('*.ts'):
 s=p.read_text(encoding='utf-8').replace('.insert(savedRequests);','.insert(savedRequests.map(request=>({...request,headers:JSON.stringify(request.headers),params:JSON.stringify(request.params)})));');p.write_text(s,encoding='utf-8')
p=B/'stage/66/server/src/models/requestModel.ts';s=p.read_text(encoding='utf-8').replace('...values, user_id:','...jsonFields(values), user_id:').replace('...values, updated_at:','...jsonFields(values), updated_at:').replace('...copy, name:','...jsonFields(copy), name:').replace('...request, user_id:','...jsonFields(request), user_id:');s+='\nfunction jsonFields(values: Record<string,unknown>) {return {...values,...(values.headers===undefined?{}:{headers:JSON.stringify(values.headers)}),...(values.params===undefined?{}:{params:JSON.stringify(values.params)})};}\n';p.write_text(s,encoding='utf-8')
for rel in ['components/ProtectedRoute.jsx','pages/LoginPage.jsx','pages/RegisterPage.jsx']:
 p=B/'stage/75/client/src'/rel;s=p.read_text(encoding='utf-8');s=re.sub(r'const \{ token, isReady \} = useAuthStore\(\(state\) => \(\{.*?\}\)\);', 'const token = useAuthStore((state) => state.token);\n  const isReady = useAuthStore((state) => state.isReady);',s,flags=re.S);p.write_text(s,encoding='utf-8')
p=B/'browser_checks.mts';s=p.read_text(encoding='utf-8');s=s.replace("n===75?'client/dist':'dist'","n===75?'client/dist':n===72?'dist/web':'dist'");s=s.replace("page.getByLabel('title',{exact:true})","page.getByLabel(s.fields[0],{exact:true})");s=s.replace("await page.locator('textarea').fill('Browser live message');","await page.getByPlaceholder(/^Message #/).fill('Browser live message');await eventually(async()=>assert.equal(await page.getByRole('button',{name:'Send',exact:true}).isEnabled(),true));");s=s.replace("await page.goto(web.url+'/settings');","await page.goto(web.url);await page.getByRole('link',{name:'Settings',exact:true}).click();");s=s.replace("error:String(error.stack||error)","error:String(error.stack||error),page_errors:errors,body:page?await page.locator('body').innerText().catch(()=>''):''");p.write_text(s,encoding='utf-8')
# Small-screen containment for the two compact JS1 panels.
for n in (55,56):
 p=B/'stage'/str(n)/'client/src/styles.css';s=p.read_text(encoding='utf-8');s+='\n/* Keep forms and ledger tables usable on narrow learning screens. */\n.panel, .grid > *, .field-row > * { min-width: 0; }\ninput, select, textarea { max-width: 100%; box-sizing: border-box; }\n@media(max-width:600px) { .field-row { grid-template-columns: minmax(0,1fr); } .panel { overflow-x:auto; } .account { flex-wrap:wrap; } }\n';p.write_text(s,encoding='utf-8')
# Correct examples to the actual domain fields.
p=B/'courses.json';cs=json.loads(p.read_text(encoding='utf-8'))
for c in cs:
 if c['stage'] in (60,61):
  primary='company' if c['stage']==60 else 'sku';secondary='role' if c['stage']==60 else 'name';c['example']=c['example'].replace('"title":',f'"{primary}":').replace('numeric title',f'numeric {primary}');c['concept']=c['concept'].replace('omitting body',f'omitting {secondary}').replace('empty body',f'empty {secondary}');c['exercises'][0]=f'Add a typed {"stage" if c["stage"]==60 else "category"} filter while preserving search.'
 if c['stage']==75:c['after']+=' Login, registration and protected-route selectors now read stable scalar values, avoiding a Zustand render loop.'
 if c['stage']==66:c['after']+=' Saved-request headers and parameters are serialized as JSONB arrays in seeds and CRUD writes.'
 if c['stage'] in (58,59,60,61):c['after']+=' Seed tags use the same explicit JSON serialization.'
 if c['stage'] in (52,53,54):c['after']+=' Currency inputs accept cent increments in the browser.'
(B/'courses.json').write_text(json.dumps(cs,indent=2),encoding='utf-8')
