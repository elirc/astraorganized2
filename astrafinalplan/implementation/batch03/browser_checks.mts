import {chromium} from 'playwright';
import {readFile,mkdir,stat,writeFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const B=path.dirname(fileURLToPath(import.meta.url));
const kinds=JSON.parse(await readFile(path.join(B,'kinds.json'),'utf8'));
const domains=[...JSON.parse(await readFile(path.join(B,'domain-specs.json'),'utf8')),...JSON.parse(await readFile(path.join(B,'memory-domain-specs.json'),'utf8'))];
const selected=new Set(process.argv.slice(2));const results=[];
async function serve(root){
 const server=createServer(async(req,res)=>{
  try{let file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url!,'http://local').pathname));if(file!==root&&!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
   try{if((await stat(file)).isDirectory())file=path.join(file,'index.html');}catch{file=path.join(root,'index.html');}
   const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml'};res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');res.end(await readFile(file));
  }catch{res.writeHead(404).end();}
 });await new Promise<void>(resolve=>server.listen(0,'127.0.0.1',resolve));
 return {url:'http://127.0.0.1:'+(server.address() as any).port,close:()=>new Promise<void>(resolve=>{server.close(()=>resolve());server.closeAllConnections();})};
}
async function eventually(work){let last;for(let i=0;i<50;i++){try{await work();return;}catch(e){last=e;await new Promise(r=>setTimeout(r,200));}}throw last;}
const browser=await chromium.launch({headless:true,executablePath:'C:/Users/Owner/AppData/Local/ms-playwright/chromium-1243/chrome-win64/chrome.exe'});
try{
for(let n=21;n<=50;n++){
 if(selected.size&&!selected.has(String(n)))continue;
 const root=path.join(B,'stage',String(n));let host,server,context,page;let closing=false;const errors=[];const calls=[];
 try{
  if(n>=23){const kind=kinds.find(x=>x.stage===String(n));const mod=await import(pathToFileURL(path.join(root,'test',kind.typescript?'database.ts':'http.js')).href);host=await(kind.typescript?mod.database():mod.application());}
  const api=async(url,method='GET',body=undefined)=>{const response=await fetch(host.origin+url,{method,headers:body===undefined?{}:{'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)});return{status:response.status,data:response.status===204?null:await response.json()};};
  server=await serve(n<23?root:path.join(root,'client','dist'));context=await browser.newContext({viewport:{width:1280,height:1000},timezoneId:'America/Los_Angeles'});page=await context.newPage();page.on('pageerror',error=>errors.push(error.message));
  await page.route('**/*',async route=>{
   const url=new URL(route.request().url());if(route.request().url().startsWith(server.url))return route.continue();
   if(host&&url.hostname==='localhost'&&url.pathname.startsWith('/api/')){
    try { const response=await route.fetch({url:host.origin+url.pathname+url.search,maxRedirects:0});calls.push({method:route.request().method(),path:url.pathname,status:response.status()});return await route.fulfill({response}); } catch(error) { if(!closing)errors.push(String(error)); return route.abort().catch(()=>{}); }
   }
   return route.abort();
  });
  const domain=domains.find(x=>x.stage===String(n));
  if(domain){
   const made=await api(domain.route,'POST',{title:'Browser lesson',owner:'Junior Mentor',category:domain.categories[0],status:domain.statuses[0],amount:12,priority:'Medium',dueDate:'2028-02-29',notes:'Disposable UI fixture'});assert.equal(made.status,201);
   await page.goto(server.url);let card=page.locator('article').filter({has:page.getByRole('heading',{name:'Browser lesson',exact:true})});await card.getByRole('button',{name:'Edit',exact:true}).click();
   assert.equal(await page.locator('form').first().locator('input[type=date]').inputValue(),'2028-02-29');await page.locator('#lesson-field-1').fill('Browser revised');
   await page.locator('form').first().getByRole('button',{name:'Update',exact:true}).click();await page.getByRole('heading',{name:'Browser revised',exact:true}).waitFor();
   card=page.locator('article').filter({has:page.getByRole('heading',{name:'Browser revised',exact:true})});await card.locator('.actions select').selectOption(domain.statuses[1]);
   await eventually(async()=>assert.equal((await api(domain.route+'/'+made.data.id)).data.status,domain.statuses[1]));
   assert.equal((await api(domain.route+'/'+made.data.id+'/activity')).data.filter(x=>x.kind==='status').length,1);
   await card.click();await page.getByPlaceholder('Add note').fill('Explain the status history');await page.locator('form.note-form').getByRole('button',{name:'Add',exact:true}).click();
   await page.locator('.timeline').getByText(/Explain the status history/).waitFor();
   const searchBox=await page.getByPlaceholder('Search',{exact:true}).boundingBox();assert.ok(searchBox&&searchBox.width>=150,'Search control remains usable in the middle column');
   await page.setViewportSize({width:390,height:844});
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'Mobile layout has no horizontal overflow');
   await page.screenshot({path:path.join(B,'logs',`${n}-mobile.png`),fullPage:true});
   await page.setViewportSize({width:1280,height:1000});
  }else if([23,24,25,26,27,29,32].includes(n)){
   const settings={
    23:{route:'/api/courses',field:'title',input:2,body:{code:'BROWSER101',title:'Browser lesson',instructor:'Junior Mentor',capacity:4,enrolled:1,level:'Beginner'}},
    24:{route:'/api/events',field:'name',input:1,body:{name:'Browser lesson',location:'Learning room',date:'2028-02-29',capacity:4,registered:1,status:'Open'}},
    25:{route:'/api/applications',field:'company',input:1,body:{company:'Browser lesson',role:'Junior SWE',stage:'Applied',contact:'Mentor',nextStepDate:'2028-02-29',notes:''}},
    26:{route:'/api/products',field:'name',input:1,body:{name:'Browser lesson',category:'Learning',price:12,stock:3}},
    27:{route:'/api/recipes',field:'name',input:1,body:{name:'Browser lesson',category:'Dinner',cookTime:20,servings:2,ingredients:['Salt','Water'],notes:''}},
    29:{route:'/api/posts',field:'title',input:1,body:{title:'Browser lesson',author:'Junior Mentor',body:'One post and its comments.'}},
    32:{route:'/api/issues',field:'title',input:1,body:{title:'Browser lesson',assignee:'Junior Mentor',status:'Backlog',priority:'High',description:'A priority filter lesson'}}
   }[n];const made=await api(settings.route,'POST',settings.body);assert.equal(made.status,201);
   await page.goto(server.url);if(n===26)await page.locator('.toolbar input').fill('Browser');
   const item=page.locator(n===26?'tbody tr':'article').filter({hasText:'Browser lesson'}).first();await item.getByRole('button',{name:'Edit',exact:true}).click();
   await page.locator('#lesson-field-'+settings.input).fill('Browser revised');await page.locator('form').first().getByRole('button',{name:/Update|Save/}).first().click();
   await eventually(async()=>{const value=(await api(settings.route+(n===26?'?search=Browser':''))).data;assert.equal((Array.isArray(value)?value:value.items).find(x=>x.id===made.data.id)?.[settings.field],'Browser revised');});
   if(n===32){await page.getByLabel('Filter priority').selectOption('Low');await eventually(async()=>assert.equal(await page.getByRole('heading',{name:'Browser revised',exact:true}).count(),0));await page.getByLabel('Filter priority').selectOption('High');await page.getByRole('heading',{name:'Browser revised',exact:true}).waitFor();}
  }else if(n===21){
   await page.goto(server.url);await page.getByRole('button',{name:'Edit',exact:true}).first().click();await page.getByLabel('Remove option 1',{exact:true}).click();await page.getByRole('button',{name:'Update poll',exact:true}).click();
   assert.equal(await page.locator('.result').count(),2);assert.match(await page.locator('.poll-card').innerText(),/9 votes/);await page.reload();assert.equal(await page.locator('.result').count(),2);
  }else if(n===22){
   await page.goto(server.url);const card=page.locator('article.card').first(),id=await card.getAttribute('data-id');await card.locator('select').selectOption('done');await page.reload();assert.equal(await page.locator('[data-column="done"] article[data-id="'+id+'"]').count(),1);
  }else if(n===28){
   const rootNode=await api('/api/nodes','POST',{name:'Browser root',title:'Root',parentId:null}),child=await api('/api/nodes','POST',{name:'Browser child',title:'Child',parentId:rootNode.data.id});
   await page.goto(server.url);await page.getByRole('button',{name:/Browser root/}).click();await page.locator('.move-row select').selectOption(child.data.id);await page.getByRole('button',{name:'Move',exact:true}).click();await page.getByRole('status').filter({hasText:/Cannot move/}).waitFor();assert.equal((await api('/api/nodes/'+rootNode.data.id)).data.depth,0);
  }else if(n===30){
   await page.goto(server.url);await page.getByRole('button',{name:'7d',exact:true}).click();await eventually(async()=>assert.equal(await page.locator('.bar-col').count(),7));
   await page.getByRole('button',{name:'+ Sample events',exact:true}).click();await page.locator('.banner').waitFor();await page.getByRole('button',{name:'Refresh view',exact:true}).click();await page.locator('.banner').waitFor({state:'hidden'});
  }else if(n===31){
   const made=await api('/api/tickets','POST',{subject:'Browser lesson',body:'Check history',priority:'normal',assigneeId:null,labelIds:[]});assert.equal(made.status,201);
   await page.goto(server.url);const card=page.locator('article').filter({has:page.getByRole('heading',{name:'Browser lesson',exact:true})});await card.locator('.controls select').first().selectOption('resolved');
   await eventually(async()=>assert.equal((await api('/api/tickets/'+made.data.id)).data.status,'resolved'));await card.getByRole('button',{name:'History',exact:true}).click();await card.getByText('Status changed to resolved',{exact:true}).waitFor();
  }else if(n===33){
   const user=(await api('/api/users')).data[0];for(let i=0;i<6;i++)await api('/api/threads','POST',{title:'Browserforum lesson',body:'Browserforum pagination with six records.',authorId:user.id,tagNames:['lesson']});
   await page.goto(server.url);await page.getByLabel('Search',{exact:true}).fill('Browserforum');await eventually(async()=>{assert.equal(await page.locator('article.thread').count(),5);assert.equal(await page.locator('article.thread h3').filter({hasText:'Browserforum lesson'}).count(),5);});await page.getByRole('button',{name:'Next',exact:true}).click();await eventually(async()=>assert.equal(await page.locator('article.thread').count(),1));
   await page.locator('article.thread').getByRole('button',{name:'Delete',exact:true}).click();await page.getByText('Page 1 / 1',{exact:true}).waitFor();assert.equal((await api('/api/threads?q=Browserforum')).data.total,5);
  }else if(n===34){
   const before=(await api('/api/invoices')).data.map(x=>x.id);await page.goto(server.url);await page.getByLabel('Client',{exact:true}).selectOption({index:1});await page.getByLabel('Issued',{exact:true}).fill('2028-02-29');await page.getByPlaceholder('Description',{exact:true}).fill('Browser lesson');await page.getByLabel('Quantity',{exact:true}).fill('2');await page.getByLabel('Unit price',{exact:true}).fill('12.34');await page.getByRole('button',{name:'Create invoice',exact:true}).click();
   await eventually(async()=>{const created=(await api('/api/invoices')).data.find(x=>!before.includes(x.id));assert.equal(created?.total,24.68);assert.equal(created?.issuedDate,'2028-02-29');});
  }
  assert.deepEqual(errors,[]);if(n>=23)assert.ok(calls.length>0);await page.screenshot({path:path.join(B,'logs',n+'-browser.png'),fullPage:true});results.push({project:String(n),check:'browser',passed:true,api:n<23?'none (browser-only)':'actual isolated HTTP server',persistence:n<23?'fresh browser storage':kinds.find(x=>x.stage===String(n)).typescript?'disposable PostgreSQL schema':'fresh in-memory repository'});
 }catch(error){if(page)await page.screenshot({path:path.join(B,'logs',n+'-browser-failure.png'),fullPage:true}).catch(()=>{});results.push({project:String(n),check:'browser',passed:false,error:String(error.stack||error)});}
 finally{closing=true;if(page)await page.unrouteAll({behavior:'ignoreErrors'});if(context)await context.close();if(server)await server.close();if(host)await host.close();}
 console.log(JSON.stringify(results.at(-1)));
 const file=path.join(B,'browser-checks.json');let prior=[];try{prior=JSON.parse(await readFile(file,'utf8'));}catch{}const ids=new Set(results.map(x=>x.project));await writeFile(file,JSON.stringify([...prior.filter(x=>!ids.has(x.project)),...results],null,2));
}
}finally{await browser.close();}
process.exitCode=results.some(x=>!x.passed)?1:0;
