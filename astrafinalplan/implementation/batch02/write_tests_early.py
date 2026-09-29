from pathlib import Path
import shutil
B=Path('astrafinalplan/implementation/batch02/stage')
helper=Path('astrafinalplan/implementation/stage/01/test/browser.cjs')
for n in [11,12,13,15,16]:
 p=B/str(n)/'test';p.mkdir(exist_ok=True);shutil.copyfile(helper,p/'browser.cjs')
def write(n,name,text):
 p=B/str(n)/'test'/name;p.parent.mkdir(exist_ok=True);p.write_text(text,encoding='utf-8')
head="const { test } = require('node:test');\nconst assert = require('node:assert/strict');\nconst { openApp } = require('./browser.cjs');\n"
write(11,'study.test.cjs',head+'''
const KEY = 'js1-flashcards';
const cards = [
  { id: 'a', deck: 'JS', front: 'Question A', back: 'Answer A', known: false },
  { id: 'b', deck: 'JS', front: 'Question B', back: 'Answer B', known: true },
  { id: 'c', deck: 'CSS', front: 'Question C', back: 'Answer C', known: false },
];
test('unlearned session snapshots matching ids, requires reveal, and completes once', async () => {
  const app = await openApp({ [KEY]: JSON.stringify(cards) });
  try {
    app.document.querySelector('#deck-filter').value = 'JS'; app.event('#deck-filter','change');
    app.document.querySelector('#unlearned-only').checked = true; app.event('#unlearned-only','change');
    app.event('#study-tab','click');
    assert.equal(app.evaluate('state.studyOrder.join()'), 'a');
    assert.equal(app.document.querySelector('#known-button').disabled, true);
    app.event('#flip-button','click'); app.event('#known-button','click');
    assert.match(app.document.querySelector('#flashcard-text').textContent, /Session complete/);
    assert.equal(app.document.querySelector('#known-button').disabled, true);
    app.evaluate('grade(false)');
    assert.equal(JSON.parse(app.w.localStorage.getItem(KEY))[0].known, true);
    app.evaluate('startStudy(false)'); assert.equal(app.evaluate('state.studyOrder.length'),0);
  } finally { app.close(); }
});
test('changing decks restarts the active session; failed grade preserves position and persisted state', async () => {
  const app = await openApp({ [KEY]: JSON.stringify(cards) });
  try {
    app.event('#study-tab','click');
    app.document.querySelector('#deck-filter').value='CSS'; app.event('#deck-filter','change');
    assert.equal(app.document.querySelector('#flashcard-text').textContent,'Question C');
    app.event('#flip-button','click');
    app.evaluate('Storage.prototype.setItem = () => { throw new Error("quota"); }');
    app.event('#known-button','click');
    assert.equal(app.evaluate('state.studyIndex'),0);
    assert.equal(JSON.parse(app.w.localStorage.getItem(KEY))[2].known,false);
    assert.match(app.document.querySelector('#study-summary').textContent,/Could not save/);
  } finally { app.close(); }
});
''')
write(12,'streaks.test.cjs',head+'''
test('best streak uses calendar days across leap day, gaps and invalid/future entries', async () => {
  const app = await openApp();
  try {
    const history = {'2024-02-28':true,'2024-02-29':true,'2024-03-01':true,'2024-03-03':true,'2024-03-04':false,'2024-02-30':true,'2025-01-01':true};
    assert.equal(app.evaluate(`bestStreak({ history: ${JSON.stringify(history)} }, '2024-03-03')`),3);
    assert.equal(app.evaluate("bestStreak({history:{}}, '2024-03-03')"),0);
    assert.equal(app.evaluate("bestStreak({history:{'2024-03-09':true,'2024-03-10':true,'2024-03-11':true}},'2024-03-11')"),3);
  } finally { app.close(); }
});
test('current streak can begin yesterday and becomes zero after a missed full day', async () => {
  const app = await openApp();
  try {
    app.evaluate('startOfToday = () => new Date(2024, 2, 11)');
    assert.equal(app.evaluate("currentStreak({history:{'2024-03-09':true,'2024-03-10':true}})"),2);
    assert.equal(app.evaluate("currentStreak({history:{'2024-03-09':true}})"),0);
    app.evaluate('render()');
    assert.equal(app.document.querySelectorAll('.best-streak').length,2);
    assert.match(app.document.querySelector('.day-cell').getAttribute('aria-label'),/2024-03-/);
  } finally { app.close(); }
});
''')
write(13,'filters.test.cjs',head+'''
const records=[
 {id:'z',title:'Zebra',author:'Maya',status:'Finished',rating:'5',notes:'JavaScript'},
 {id:'a',title:'Alpha',author:'Maya',status:'Finished',rating:'5',notes:'JavaScript'},
 {id:'b',title:'Beta',author:'Lin',status:'Reading',rating:'5',notes:'JavaScript'},
];
test('status, search and rating ordering compose without changing persisted order',async()=>{
 const app=await openApp({'js1-reading-list':JSON.stringify(records)});
 try {
  app.document.querySelector('#status-filter').value='Finished';app.event('#status-filter','change');
  app.document.querySelector('#search').value='maya';app.event('#search','input');
  app.document.querySelector('#sort').value='rating';app.event('#sort','change');
  assert.deepEqual([...app.document.querySelectorAll('.book-card h2')].map(x=>x.textContent),['Alpha','Zebra']);
  assert.equal(JSON.parse(app.w.localStorage.getItem('js1-reading-list'))[0].id,'z');
  assert.match(app.document.querySelector('#reading-summary').textContent,/Showing 2 of 3.*2 finished/);
  app.document.querySelector('#search').value='unmatched';app.event('#search','input');
  assert.equal(app.document.querySelector('#empty').hidden,false);
 } finally { app.close(); }
});
''')
write(15,'money.test.cjs',head+'''
test('decimal text is converted to bounded integer cents without permissive coercion',async()=>{
 const app=await openApp();
 try {
  for(const [input,expected] of [['0.10',10],['0.20',20],['1.01',101],['999999999.99',99999999999]]) assert.equal(app.evaluate(`parseCents(${JSON.stringify(input)})`),expected);
  for(const input of ['', '0','-1','1.001','Infinity','1e3','1000000000']) assert.ok(Number.isNaN(app.evaluate(`parseCents(${JSON.stringify(input)})`)),input);
  assert.equal(app.evaluate("isRealDate('2026-02-30')"),false);
 } finally { app.close(); }
});
test('whole-ledger totals are exact for tenths and storage failure keeps the old record and editor',async()=>{
 const rows=[{id:'a',description:'First',category:'Work',type:'income',amount:0.1,date:'2026-09-08'},{id:'b',description:'Second',category:'Work',type:'income',amount:0.2,date:'2026-09-08'}];
 const app=await openApp({'js1-budget-tracker':JSON.stringify(rows)});
 try {
  assert.equal(app.document.querySelector('#income-total').textContent,'$0.30');
  app.evaluate("editTransaction('a')");app.document.querySelector('#amount').value='12.50';
  app.evaluate('Storage.prototype.setItem = () => { throw new Error("quota"); }');
  app.event('#transaction-form','submit');
  assert.equal(app.evaluate('transactions[0].amount'),0.1);
  assert.equal(app.document.querySelector('#amount').value,'12.50');
  assert.match(app.document.querySelector('#message').textContent,/Could not save/);
 } finally { app.close(); }
});
''')
write(16,'expiration.test.cjs',head+'''
test('expiration is independent of low stock; today is not yet expired',async()=>{
 const app=await openApp();
 try {
  app.evaluate(`localToday=()=> '2026-09-08';items=[
   {id:'a',name:'Expired full',category:'Dry',quantity:5,minimum:1,expires:'2026-09-07'},
   {id:'b',name:'Today low',category:'Dry',quantity:1,minimum:1,expires:'2026-09-08'},
   {id:'c',name:'Future full',category:'Dry',quantity:5,minimum:1,expires:'2026-09-09'}];renderItems()`);
  assert.equal(app.document.querySelector('#low-items').textContent,'1');
  app.document.querySelector('#filter').value='Expired';app.event('#filter','change');
  assert.equal(app.document.querySelectorAll('#items tr').length,1);
  assert.match(app.document.querySelector('.status').textContent,/Stock OK.*Expired/);
  app.document.querySelector('#filter').value='Fresh';app.event('#filter','change');
  assert.equal(app.document.querySelector('.name').textContent,'Future full');
  assert.equal(app.evaluate("isExpired({expires:'2026-09-08'})"),false);
 } finally { app.close(); }
});
test('blank quantity and impossible dates cannot be stored',async()=>{
 const app=await openApp();
 try {
  const count=app.evaluate('items.length');
  app.document.querySelector('#item-name').value='Invalid';app.document.querySelector('#quantity').value='';
  app.document.querySelector('#minimum').value='1';app.document.querySelector('#expires').value='2026-09-09';app.event('#item-form','submit');
  assert.equal(app.evaluate('items.length'),count);
  assert.equal(app.evaluate("isRealDate('2026-02-30')"),false);
  assert.match(app.document.querySelector('#message').textContent,/valid/);
 } finally { app.close(); }
});
''')
write(17,'store.test.js','''import { test } from 'node:test';
import assert from 'node:assert/strict';
import { randomUUID } from 'node:crypto';
async function fixture() {
 const data=new Map();
 globalThis.localStorage={getItem:key=>data.get(key)??null,setItem:(key,value)=>data.set(key,value)};
 return {store:await import(`../src/store.js?case=${randomUUID()}`),data};
}
test('tags normalize once; failed writes do not publish a new snippet or consume an existing one',async()=>{
 const {store,data}=await fixture();
 store.saveSnippet({title:'Test',language:'JS',tags:' Utility,utility, EVENTS, ,events ',code:'const x = 1;'});
 const first=store.listSnippets()[0];assert.deepEqual(first.tags,['Utility','EVENTS']);
 const before=data.get('js1-snippet-vault');
 globalThis.localStorage.setItem=()=>{throw new Error('quota');};
 assert.throws(()=>store.saveSnippet({id:first.id,title:'Changed',language:'JS',tags:'x',code:'x'}),/quota/);
 assert.equal(store.getSnippet(first.id).title,'Test');
 assert.throws(()=>store.deleteSnippet(first.id),/quota/);
 assert.equal(data.get('js1-snippet-vault'),before);
});
test('missing ids and blank content fail without saving; clipboard rejection returns false',async()=>{
 const {store,data}=await fixture();
 assert.throws(()=>store.saveSnippet({id:'missing',title:'T',code:'x',language:'JS',tags:''}),/no longer/);
 assert.throws(()=>store.saveSnippet({title:' ',code:'x',language:'JS',tags:''}),/title/);
 assert.equal(data.size,0);
 const {copyToClipboard}=await import('../src/dom.js');
 Object.defineProperty(globalThis,'navigator',{configurable:true,value:{clipboard:{writeText:async()=>{throw new Error('denied');}}}});
 assert.equal(await copyToClipboard('x'),false);
 let copied='';globalThis.navigator.clipboard.writeText=async text=>{copied=text;};
 assert.equal(await copyToClipboard('const x = 1;'),true);assert.equal(copied,'const x = 1;');
});
''')
write(14,'persistence.test.js','''import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as fs from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createNoteRepository } from '../server/repository.js';
import { createApp } from '../server/server.js';
async function fixture(t) {
 const dir=await fs.mkdtemp(join(tmpdir(),'astra-notes-'));
 t.after(()=>fs.rm(dir,{recursive:true,force:true}));
 return join(dir,'notes.json');
}
test('concurrent mutations serialize the entire read-modify-write and survive a new repository instance',async(t)=>{
 const file=await fixture(t),repo=await createNoteRepository(file);
 const results=await Promise.all(Array.from({length:12},(_,i)=>repo.create({title:`Note ${i}`,body:'Persisted'})));
 assert.equal(new Set(results.map(x=>x.id)).size,12);
 const restarted=await createNoteRepository(file);
 assert.equal((await restarted.list({search:''})).length,13);
 await Promise.all(results.slice(0,4).map(note=>repo.togglePin(note.id)));
 assert.equal((await repo.list({search:'Note'})).filter(x=>x.pinned).length,4);
});
test('failed atomic rename preserves previous bytes; the queue recovers and corrupt data is not reseeded',async(t)=>{
 const file=await fixture(t);let fail=false;
 const repo=await createNoteRepository(file,{...fs,rename:async(...args)=>{if(fail){fail=false;throw new Error('simulated rename failure');}return fs.rename(...args);}});
 const before=await fs.readFile(file,'utf8');fail=true;
 await assert.rejects(repo.create({title:'Failed',body:'x'}),/rename failure/);
 assert.equal(await fs.readFile(file,'utf8'),before);
 await repo.create({title:'Retry',body:'works'});
 assert.equal((await repo.list({search:'Retry'})).length,1);
 await fs.writeFile(file,'{bad');
 await assert.rejects(createNoteRepository(file));
 assert.equal(await fs.readFile(file,'utf8'),'{bad');
});
test('HTTP rejects wrong types and serves a persisted create without touching development data',async(t)=>{
 const file=await fixture(t);const app=await createApp(file);
 const server=await new Promise(resolve=>{const s=app.listen(0,'127.0.0.1',()=>resolve(s));});
 t.after(()=>new Promise(resolve=>{server.close(resolve);server.closeAllConnections();}));
 const url=`http://127.0.0.1:${server.address().port}/api/notes`;
 const post=body=>fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
 assert.equal((await post({title:123,body:'x'})).status,400);
 const response=await post({title:'Saved note',body:'hello'});assert.equal(response.status,201);
 const note=await response.json();assert.ok(JSON.parse(await fs.readFile(file,'utf8')).some(x=>x.id===note.id));
 assert.equal((await fetch(url+'?search[]=bad')).status,400);
});
''')
print('Wrote focused regression tests for seven browser/file-backed projects.')
