const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const http=require('node:http');
const B=__dirname;
async function serve(root){
 const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml'};
 const server=http.createServer(async(req,res)=>{
  try{
   let file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname));
   if(file!==root&&!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
   try{if((await fs.stat(file)).isDirectory())file=path.join(file,'index.html');}catch{file=path.join(root,'index.html');}
   res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');res.end(await fs.readFile(file));
  }catch{res.writeHead(404);res.end();}
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 return{url:`http://127.0.0.1:${server.address().port}`,close:()=>new Promise(resolve=>{server.close(resolve);server.closeAllConnections();})};
}
async function json(route,value,status=200){await route.fulfill({status,headers:{'Content-Type':'application/json','Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'content-type','Access-Control-Allow-Methods':'GET,POST,PUT,PATCH,DELETE,OPTIONS'},body:status===204?'':JSON.stringify(value)});}
(async()=>{
 await fs.mkdir(path.join(B,'logs'),{recursive:true});
 const browser=await chromium.launch({headless:true,executablePath:'C:/Users/Owner/AppData/Local/ms-playwright/chromium-1243/chrome-win64/chrome.exe'});
 const results=[];const selected=new Set(process.argv.slice(2));
 async function check(n,action,mock){
  if(selected.size&&!selected.has(n))return;
  const root=path.join(B,'stage',n,...(['14','18','19','20'].includes(n)?['client','dist']:[]));
  const server=await serve(root);const context=await browser.newContext({viewport:{width:1280,height:900},timezoneId:'America/Los_Angeles'});
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/*',async route=>{
   if(route.request().url().startsWith(server.url))return route.continue();
   if(mock&&/http:\/\/localhost:(4104|4106|4112)\/api\//.test(route.request().url())){
    if(route.request().method()==='OPTIONS')return json(route,{},204);
    return mock(route);
   }
   return route.abort();
  });
  try{await action(page,server.url,context);assert.deepEqual(errors,[]);await page.screenshot({path:path.join(B,'logs',`${n}-browser.png`),fullPage:true});results.push({project:n,check:'browser',passed:true});}
  catch(error){await page.screenshot({path:path.join(B,'logs',`${n}-browser-failure.png`),fullPage:true}).catch(()=>{});results.push({project:n,check:'browser',passed:false,error:error.stack});}
  finally{await context.close();await server.close();}
  console.log(JSON.stringify(results.at(-1)));
 }
 await check('11',async(page,url)=>{
  await page.goto(url);await page.locator('#deck-filter').selectOption('JS');await page.locator('#unlearned-only').check();await page.locator('#study-tab').click();
  assert.equal(await page.locator('#known-button').isDisabled(),true);await page.locator('#flip-button').click();await page.locator('#known-button').click();
  assert.match(await page.locator('#flashcard-text').textContent(),/Session complete/);await page.reload();
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('js1-flashcards')).find(c=>c.deck==='JS').known),true);
 });
 await check('12',async(page,url)=>{
  await page.goto(url);assert.match(await page.locator('.best-streak').first().textContent(),/Best: 3/);
  await page.locator('.habit-row').first().locator('.day-cell').last().click();
  assert.match(await page.locator('.habit-row').first().locator('.streak-badge').first().textContent(),/2 day/);
  await page.reload();assert.match(await page.locator('.best-streak').first().textContent(),/Best: 2/);
 });
 await check('13',async(page,url)=>{
  await page.goto(url);await page.locator('[data-action=edit]').first().click();await page.locator('#status').selectOption('Finished');await page.locator('#save-button').click();
  await page.locator('#status-filter').selectOption('Finished');assert.equal(await page.locator('.book-card').count(),1);
  await page.locator('#search').fill('unmatched');assert.equal(await page.locator('.book-card').count(),0);assert.match(await page.locator('#reading-summary').textContent(),/1 finished/);
 });
 let notes=[{id:'welcome',title:'Welcome',body:'Initial note',pinned:true,updatedAt:'2026-09-08T10:00:00Z'}];let failNote=false;
 const noteMock=async route=>{
  const request=route.request(),url=new URL(request.url());
  if(request.method()==='GET')return json(route,notes.filter(n=>(n.title+' '+n.body).toLowerCase().includes((url.searchParams.get('search')||'').toLowerCase())));
  if(request.method()==='POST'){
   if(failNote)return json(route,{error:'Simulated storage failure'},500);
   const note={...request.postDataJSON(),id:'created',pinned:false,updatedAt:'2026-09-08T11:00:00Z'};notes.push(note);return json(route,note,201);
  }
  if(request.method()==='PATCH'){const note=notes.find(n=>url.pathname.includes(n.id));note.pinned=!note.pinned;return json(route,note);}
  return json(route,{error:'Unexpected test request'},400);
 };
 await check('14',async(page,url)=>{
  await page.goto(url);await page.getByRole('heading',{name:'Welcome',exact:true}).waitFor();
  await page.getByLabel('Title',{exact:true}).fill('Saved learning note');await page.getByLabel('Body',{exact:true}).fill('Explain a serialized write');await page.getByRole('button',{name:'Add note',exact:true}).click();
  await page.getByRole('heading',{name:'Saved learning note',exact:true}).waitFor();assert.equal(notes.length,2);
  failNote=true;await page.getByLabel('Title',{exact:true}).fill('Retain this draft');await page.getByLabel('Body',{exact:true}).fill('Retry later');await page.getByRole('button',{name:'Add note',exact:true}).click();
  await page.getByRole('status').filter({hasText:'Simulated storage failure'}).waitFor();assert.equal(await page.getByLabel('Title',{exact:true}).inputValue(),'Retain this draft');assert.equal(notes.length,2);
 },noteMock);
 await check('15',async(page,url)=>{
  await page.goto(url);await page.locator('#description').fill('Ten cents');await page.locator('#category').fill('Learning');await page.locator('#type').selectOption('income');await page.locator('#amount').fill('0.10');await page.locator('#date').fill('2026-09-08');await page.locator('#save-button').click();
  assert.equal(await page.locator('#income-total').textContent(),'$850.10');await page.reload();assert.equal(await page.locator('#income-total').textContent(),'$850.10');
 });
 await check('16',async(page,url)=>{
  await page.goto(url);await page.evaluate(()=>{localToday=()=> '2026-09-08';renderItems();});await page.locator('#filter').selectOption('Expired');
  assert.equal(await page.locator('#items tr').count(),1);assert.match(await page.locator('.status').textContent(),/Stock OK.*Expired/);
 });
 await check('17',async(page,url)=>{
  await page.addInitScript(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('denied');}}}));
  await page.goto(url);await page.locator('#snippet-title').fill('Learning snippet');await page.locator('#snippet-tags').fill('Utility, utility, Events');await page.locator('#snippet-code').fill('const answer = 42;');await page.locator('#submit-button').click();
  const card=page.locator('.snippet-card').filter({has:page.getByRole('heading',{name:'Learning snippet'})});assert.equal(await card.locator('.tag').count(),2);
  await card.getByRole('button',{name:'Copy',exact:true}).click();await page.locator('#form-message').filter({hasText:'Clipboard not available'}).waitFor();
  await page.reload();await page.getByRole('heading',{name:'Learning snippet'}).waitFor();
 });
 const roomId='00000000-0000-0000-0000-000000000001';let booking={id:'00000000-0000-0000-0000-000000000002',roomId,roomName:'Learning Room',title:'Original meeting',bookedBy:'Junior',startsAt:'2030-03-10T10:00:12.345Z',endsAt:'2030-03-10T11:00:12.345Z'};let updateBody;
 const roomMock=async route=>{
  const req=route.request(),url=new URL(req.url());
  if(url.pathname==='/api/rooms')return json(route,[{id:roomId,name:'Learning Room',capacity:4}]);
  if(req.method()==='GET'){assert.ok(url.searchParams.get('dayStart')?.endsWith('Z'));return json(route,[booking]);}
  if(req.method()==='PUT'){updateBody=req.postDataJSON();booking={...booking,...updateBody};return json(route,booking);}
  return json(route,{error:'Unexpected test request'},400);
 };
 await check('18',async(page,url)=>{
  await page.goto(url);await page.getByText('Original meeting',{exact:true}).waitFor();await page.getByRole('button',{name:'Edit',exact:true}).click();
  await page.getByLabel('Title',{exact:true}).fill('Edited meeting');await page.getByRole('button',{name:'Save changes',exact:true}).click();await page.getByText('Edited meeting',{exact:true}).waitFor();
  assert.equal(updateBody.startsAt,'2030-03-10T10:00:12.345Z');assert.equal(updateBody.endsAt,'2030-03-10T11:00:12.345Z');
 },roomMock);
 const searched=[];let resolveOld;const oldSent=new Promise(resolve=>{resolveOld=resolve;});
 const notesApiMock=async route=>{
  const url=new URL(route.request().url());if(url.pathname.endsWith('/stats'))return json(route,{total:2});
  const term=url.searchParams.get('search')||'';searched.push(term);
  if(term==='old'){resolveOld();await new Promise(resolve=>setTimeout(resolve,1200));}
  return json(route,{success:true,data:[{id:1,title:term==='old'?'Old response':term==='new'?'New response':'Initial note',body:'Content',folder:'General',status:'active',tags:[]}]});
 };
 await check('19',async(page,url)=>{
  await page.goto(url);await page.getByRole('heading',{name:'Initial note',exact:true}).waitFor();await page.getByLabel('Search note content').fill('old');await oldSent;
  await page.getByLabel('Search note content').fill('new');await page.getByRole('heading',{name:'New response',exact:true}).waitFor();await page.waitForTimeout(1500);
  assert.equal(await page.getByRole('heading',{name:'Old response',exact:true}).count(),0);assert.ok(searched.includes('old')&&searched.includes('new'));
 },async route=>{
  if(new URL(route.request().url()).pathname.endsWith('/stats'))return json(route,{success:true,data:{total:2}});
  return notesApiMock(route);
 });
 let savedBookmark=null;
 const bookmarksMock=async route=>{
  const req=route.request(),url=new URL(req.url());
  if(url.pathname.endsWith('/stats'))return json(route,{success:true,data:{total:savedBookmark?1:0}});
  if(url.pathname.endsWith('/metadata'))return json(route,{success:true,data:{title:'A retrieved title',url:req.postDataJSON().url}});
  if(req.method()==='GET')return json(route,{success:true,data:savedBookmark?[savedBookmark]:[]});
  if(req.method()==='POST'){savedBookmark={...req.postDataJSON(),id:1};return json(route,{success:true,data:savedBookmark},201);}
  return json(route,{success:false,error:{message:'Unexpected test request'}},400);
 };
 await check('20',async(page,url)=>{
  await page.goto(url);await page.getByRole('button',{name:'Use page title',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('input')&&[...document.querySelectorAll('input')].some(x=>x.value==='A retrieved title'));
  await page.getByRole('button',{name:'Create',exact:true}).click();await page.getByRole('heading',{name:'A retrieved title',exact:true}).waitFor();assert.equal(savedBookmark.title,'A retrieved title');
 },bookmarksMock);
 await browser.close();
 const file=path.join(B,'browser-checks.json');let prior=[];try{prior=JSON.parse(await fs.readFile(file,'utf8'));}catch{}
 const ids=new Set(results.map(x=>x.project));await fs.writeFile(file,JSON.stringify([...prior.filter(x=>!ids.has(x.project)),...results],null,2));
 process.exitCode=results.some(x=>!x.passed)?1:0;
})().catch(error=>{console.error(error);process.exitCode=1;});
