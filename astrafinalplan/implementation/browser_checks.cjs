const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const ROOT = __dirname;
const LOGS = path.join(ROOT, 'logs');

async function serve(root) {
  const types = { '.html':'text/html', '.js':'text/javascript', '.css':'text/css', '.svg':'image/svg+xml', '.json':'application/json' };
  const server = http.createServer(async (req, res) => {
    try {
      let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url,'http://local').pathname));
      if (file !== root && !file.startsWith(root + path.sep)) { res.writeHead(403);res.end();return; }
      try { if ((await fs.stat(file)).isDirectory()) file=path.join(file,'index.html'); }
      catch { file=path.join(root,'index.html'); }
      res.setHeader('Content-Type',types[path.extname(file)] || 'application/octet-stream');
      res.end(await fs.readFile(file));
    } catch {res.writeHead(404);res.end();}
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  return { url:`http://127.0.0.1:${server.address().port}`,close:()=>new Promise(resolve=>{server.close(resolve);server.closeAllConnections();}) };
}

(async()=>{
 await fs.mkdir(LOGS,{recursive:true});
 const browser=await chromium.launch({headless:true,executablePath:'C:/Users/Owner/AppData/Local/ms-playwright/chromium-1243/chrome-win64/chrome.exe'});
 const results=[];
 async function check(n,action){
  const server=await serve(path.join(ROOT,'stage',n,...(['05','06'].includes(n)?['dist']:[])));
  const context=await browser.newContext({viewport:{width:1280,height:900}});
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/*',route=>route.request().url().startsWith(server.url)?route.continue():route.abort());
  try{await action(page,server.url,context);assert.deepEqual(errors,[]);results.push({project:n,check:'browser',passed:true});}
  catch(e){results.push({project:n,check:'browser',passed:false,error:e.stack});}
  finally{await context.close();await server.close();}
  console.log(JSON.stringify(results.at(-1)));
 }
 await check('01',async(page,url)=>{
  await page.goto(url);const first=await page.locator('.task-title').first().textContent();
  await page.locator('[data-action=delete]').first().click();await page.reload();
  await page.getByRole('button',{name:'Undo last deletion'}).click();
  assert.equal(await page.locator('.task-title').first().textContent(),first);
  assert.equal(await page.getByRole('button',{name:'Undo last deletion'}).isDisabled(),true);
 });
 await check('02',async(page,url)=>{
  await page.goto(url);const before=await page.locator('.contact-card').count();
  await page.locator('#name').fill('Duplicate');await page.locator('#email').fill('MAYA@example.com');await page.locator('#phone').fill('123');
  await page.getByRole('button',{name:'Add contact',exact:true}).click();
  assert.equal(await page.locator('.contact-card').count(),before);assert.match(await page.locator('#message').textContent(),/already exists/);
  assert.equal(await page.locator('#email').evaluate(el=>el===document.activeElement),true);
 });
 await check('03',async(page,url)=>{
  await page.addInitScript(()=>{window.astraNow=100000;Date.now=()=>window.astraNow;});
  await page.goto(url);await page.locator('#session-minutes').fill('1');await page.getByRole('button',{name:'Start',exact:true}).click();
  await page.evaluate(()=>{window.astraNow+=45000;tick();});assert.equal(await page.locator('#timer-display').textContent(),'00:15');
  await page.evaluate(()=>{window.astraNow+=30000;tick();tick();});assert.equal(await page.locator('#session-count').textContent(),'1');
 });
 await check('04',async(page,url)=>{
  await page.goto(url);await page.locator('#monthPicker').fill('2026-07');await page.locator('#monthPicker').dispatchEvent('change');
  await page.locator('[data-edit-expense]').first().click();await page.locator('#entryAmount').fill('123.45');await page.getByRole('button',{name:'Save entry'}).click();
  await page.reload();assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('eli-elyn-finance-dashboard-v1')).expenses.some(e=>e.amount===123.45)),true);
  await page.screenshot({path:path.join(LOGS,'04-browser.png'),fullPage:true});
 });
 await check('05',async(page,url,context)=>{
  await context.grantPermissions(['clipboard-read','clipboard-write']);
  await page.goto(url);await page.getByRole('button',{name:'+ Shopping list',exact:true}).first().click();
  await page.goto(url+'/#/shopping-list');const input=page.locator('.quantity-control input').first();
  await input.focus();await page.keyboard.press('ControlOrMeta+A');await page.keyboard.type('2 1/2 cups');
  await page.reload();assert.equal(await page.locator('.quantity-control input').first().inputValue(),'2 1/2 cups');
  await page.getByRole('button',{name:'Copy entire list',exact:true}).click();
  assert.match(await page.evaluate(()=>navigator.clipboard.readText()),/2 1\/2 cups/);
  await page.screenshot({path:path.join(LOGS,'05-browser.png'),fullPage:true});
  await page.getByRole('button',{name:/Remove .* from shopping list/}).first().click();
  assert.equal(await page.locator('.quantity-control').count(),0);
 });
 await check('06',async(page,url)=>{
  const record={id:'a',company:'Existing company',role:'Junior',location:'',url:'',status:'applied',stack:'JS',date:'2026-09-08',notes:''};
  await page.addInitScript(r=>localStorage.setItem('jobtracker:data',JSON.stringify([r])),record);
  await page.goto(url);await page.getByRole('button',{name:'Job Tracker',exact:true}).click();
  await page.getByRole('button',{name:'Export applications',exact:true}).waitFor();
  const input=page.locator('input[type=file]');
  await input.setInputFiles({name:'bad.json',mimeType:'application/json',buffer:Buffer.from('{bad')});
  await page.getByRole('status').filter({hasText:'Import failed'}).waitFor();
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('jobtracker:data'))[0].company),'Existing company');
  const text=JSON.stringify({format:'daybook.jobs',version:1,applications:[{...record,company:'Imported company'}]});
  await input.setInputFiles({name:'valid.json',mimeType:'application/json',buffer:Buffer.from(text)});
  await page.getByRole('status').filter({hasText:'Imported 1 applications'}).waitFor();
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('jobtracker:data'))[0].company),'Imported company');
  const downloadPromise=page.waitForEvent('download');await page.getByRole('button',{name:'Export applications',exact:true}).click();const download=await downloadPromise;
  const exported=JSON.parse(await fs.readFile(await download.path(),'utf8'));assert.equal(exported.applications[0].company,'Imported company');
  await page.screenshot({path:path.join(LOGS,'06-browser.png'),fullPage:true});
 });
 await browser.close();await fs.writeFile(path.join(ROOT,'browser-checks.json'),JSON.stringify(results,null,2));
 process.exitCode=results.some(r=>!r.passed)?1:0;
})().catch(e=>{console.error(e);process.exitCode=1;});
