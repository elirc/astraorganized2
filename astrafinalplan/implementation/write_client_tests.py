from pathlib import Path
import json
BASE=Path(__file__).resolve().parent/'stage'
def write(n,f,s):
 p=BASE/n/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')

helper='''const { JSDOM } = require('jsdom');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const vm = require('node:vm');
const { randomUUID } = require('node:crypto');

exports.openApp = async function openApp(saved = {}) {
  const root = resolve(__dirname, '..');
  const dom = new JSDOM(readFileSync(resolve(root, 'index.html'), 'utf8'), {
    url: 'http://localhost/', runScripts: 'outside-only',
  });
  const w = dom.window;
  await new Promise((done) => w.addEventListener('load', done));
  w.crypto.randomUUID = randomUUID;
  w.structuredClone = structuredClone;
  if (w.HTMLDialogElement) {
    w.HTMLDialogElement.prototype.showModal = function () { this.open = true; };
    w.HTMLDialogElement.prototype.close = function () { this.open = false; };
  }
  let now = 1000000; let nextId = 0; const intervals = new Map();
  w.Date.now = () => now;
  w.setInterval = (fn) => { intervals.set(++nextId, fn); return nextId; };
  w.clearInterval = (id) => intervals.delete(id);
  for (const [key, value] of Object.entries(saved)) w.localStorage.setItem(key, value);
  const evaluate = (code) => vm.runInContext(code, dom.getInternalVMContext());
  evaluate(readFileSync(resolve(root, 'app.js'), 'utf8'));
  w.document.dispatchEvent(new w.Event('DOMContentLoaded'));
  return { w, document: w.document, evaluate, intervals,
    advance(ms) { now += ms; },
    event(selector, type) { w.document.querySelector(selector).dispatchEvent(new w.Event(type, { bubbles: true, cancelable: true })); },
    snapshot() { return Object.fromEntries(Object.keys(w.localStorage).map((key) => [key, w.localStorage.getItem(key)])); },
    close() { w.close(); },
  };
};
'''
for n in ['01','02','03','04']:
 write(n,'test/browser.cjs',helper)
 write(n,'package.json',json.dumps({'name':f'astra-browser-exercise-{n}','private':True,'scripts':{'test':'node --test test/*.test.cjs'},'devDependencies':{'jsdom':'^25.0.1'}},indent=2)+'\n')

write('01','test/undo.test.cjs','''const { test } = require('node:test');
const assert = require('node:assert/strict');
const { openApp } = require('./browser.cjs');
const KEY = 'js1-task-board';
const tasks = ['a','b','c'].map((id) => ({ id, title:id, due:'2026-10-01', priority:'Low', status:'Backlog', notes:'' }));

test('legacy data upgrades; undo after reload restores identity and position once', async () => {
  let app = await openApp({ [KEY]: JSON.stringify(tasks) });
  app.evaluate("deleteTask('b')");
  const saved = app.snapshot(); app.close();
  app = await openApp(saved);
  assert.equal(app.document.querySelector('#undo-delete').disabled, false);
  app.event('#undo-delete', 'click');
  let result = JSON.parse(app.w.localStorage.getItem(KEY));
  assert.deepEqual(result.tasks.map((task) => task.id), ['a','b','c']);
  assert.equal(result.deleted, null);
  app.evaluate('undoDelete()');
  assert.equal(JSON.parse(app.w.localStorage.getItem(KEY)).tasks.length, 3);
  app.close();
});
test('undo preserves intervening edits and uses only the latest deletion', async () => {
  const app = await openApp({ [KEY]: JSON.stringify(tasks) });
  app.evaluate("deleteTask('a'); state.tasks[0].title = 'Edited B'; saveTasks(); deleteTask('c'); undoDelete()");
  const result = JSON.parse(app.w.localStorage.getItem(KEY));
  assert.deepEqual(result.tasks.map((task) => task.id), ['b','c']);
  assert.equal(result.tasks[0].title, 'Edited B'); app.close();
});
test('failed storage does not delete a task or consume recovery data', async () => {
  const app = await openApp({ [KEY]: JSON.stringify(tasks) });
  app.evaluate("Storage.prototype.setItem = () => { throw new Error('quota'); }; deleteTask('b')");
  assert.equal(app.evaluate('state.tasks.length'), 3);
  assert.match(app.document.querySelector('#form-message').textContent, /Could not save/); app.close();
});
''')
write('02','test/duplicates.test.cjs','''const { test } = require('node:test');
const assert = require('node:assert/strict');
const { openApp } = require('./browser.cjs');
const KEY = 'js1-contact-book';
const contacts = [{id:'a',name:'Ada',email:'Ada@Example.com',phone:'123',company:'',relationship:'Friend'}, {id:'b',name:'Bob',email:'bob@example.com',phone:'456',company:'',relationship:'Client'}];
test('case/whitespace duplicate create and conflicting edit leave storage untouched', async () => {
 const app = await openApp({[KEY]:JSON.stringify(contacts)});
 for (const [selector,value] of [['#name','Other'],['#email',' ada@example.COM '],['#phone','789']]) app.document.querySelector(selector).value=value;
 app.event('#contact-form','submit');
 assert.equal(app.w.localStorage.getItem(KEY),JSON.stringify(contacts));
 assert.equal(app.document.querySelector('#email').getAttribute('aria-invalid'),'true');
 app.evaluate("editContact('b')");app.document.querySelector('#email').value='ADA@example.com';app.event('#contact-form','submit');
 assert.equal(app.w.localStorage.getItem(KEY),JSON.stringify(contacts));app.close();
});
test('editing your own email and adding a distinct email both succeed after reload', async () => {
 let app=await openApp({[KEY]:JSON.stringify(contacts)});
 app.evaluate("editContact('a')");app.document.querySelector('#name').value='Ada Updated';app.event('#contact-form','submit');
 assert.equal(JSON.parse(app.w.localStorage.getItem(KEY))[0].name,'Ada Updated');
 const saved=app.snapshot();app.close();app=await openApp(saved);
 for (const [selector,value] of [['#name','Cara'],['#email','cara@example.com'],['#phone','789']]) app.document.querySelector(selector).value=value;
 app.event('#contact-form','submit');assert.equal(JSON.parse(app.w.localStorage.getItem(KEY)).length,3);app.close();
});
''')
write('03','test/timer.test.cjs','''const { test } = require('node:test');
const assert = require('node:assert/strict');
const { openApp } = require('./browser.cjs');
test('one delayed callback accounts for all elapsed time and completes only once', async () => {
 const app=await openApp();app.document.querySelector('#session-minutes').value='1';
 app.evaluate('startTimer(); startTimer()');assert.equal(app.intervals.size,1);
 app.advance(45000);app.evaluate('tick()');assert.equal(app.document.querySelector('#timer-display').textContent,'00:15');
 app.advance(30000);app.evaluate('tick(); tick(); completeSession()');
 assert.equal(JSON.parse(app.w.localStorage.getItem('js1-focus-timer')).length,1);
 assert.equal(app.intervals.size,0);app.close();
});
test('pause preserves subsecond remainder and excludes paused time', async () => {
 const app=await openApp();app.document.querySelector('#session-minutes').value='1';app.evaluate('startTimer()');
 app.advance(1250);app.evaluate('pauseTimer()');assert.equal(app.evaluate('timer.remaining'),58.75);
 app.advance(120000);app.evaluate('startTimer()');app.advance(58749);app.evaluate('tick()');
 assert.equal(app.evaluate('timer.mode'),'running');app.advance(1);app.evaluate('tick()');
 assert.equal(app.evaluate('timer.mode'),'idle');app.close();
});
test('reset cancels a run; pausing after its deadline logs a completed session', async () => {
 const app=await openApp();app.document.querySelector('#session-minutes').value='1';app.evaluate('startTimer(); resetTimer()');
 app.advance(90000);app.evaluate('tick()');assert.equal(app.evaluate('state.sessions.length'),0);
 app.evaluate('startTimer()');app.advance(60000);app.evaluate('pauseTimer()');assert.equal(app.evaluate('state.sessions.length'),1);app.close();
});
''')
write('04','test/expense-edit.test.cjs','''const { test } = require('node:test');
const assert = require('node:assert/strict');
const { openApp } = require('./browser.cjs');
const KEY='eli-elyn-finance-dashboard-v1';
const fixture={expenses:[{id:'e1',owner:'Household',date:'2026-07-10',category:'Food',description:'Lunch',amount:10}],bills:[],incomes:[],goals:[],investments:[]};
test('edit updates one row and derived totals, preserving identity through reload',async()=>{
 let app=await openApp({[KEY]:JSON.stringify(fixture)});
 app.document.querySelector('#monthPicker').value='2026-07';app.event('#monthPicker','change');
 app.event('[data-edit-expense="e1"]','click');app.document.querySelector('#entryAmount').value='12.50';app.event('#entryForm','submit');
 const stored=JSON.parse(app.w.localStorage.getItem(KEY));assert.equal(stored.expenses.length,1);assert.equal(stored.expenses[0].id,'e1');assert.equal(stored.expenses[0].amount,12.5);
 assert.match(app.document.querySelector('#expenseKpi').textContent,/12.50/);
 const saved=app.snapshot();app.close();app=await openApp(saved);assert.equal(app.evaluate('state.expenses[0].amount'),12.5);app.close();
});
test('invalid input and storage failure preserve the original expense and open editor',async()=>{
 const app=await openApp({[KEY]:JSON.stringify(fixture)});app.evaluate("editExpense('e1')");
 for(const value of ['-1','0','1.001']){app.document.querySelector('#entryAmount').value=value;app.event('#entryForm','submit');assert.equal(JSON.parse(app.w.localStorage.getItem(KEY)).expenses[0].amount,10);}
 app.document.querySelector('#entryAmount').value='20';app.evaluate("Storage.prototype.setItem=()=>{throw new Error('quota')}");app.event('#entryForm','submit');
 assert.equal(app.evaluate('state.expenses[0].amount'),10);assert.equal(app.document.querySelector('#entryModal').open,true);assert.match(app.document.querySelector('#entryError').textContent,/Could not save/);app.close();
});
''')
write('05','test/shopping-state.test.ts','''import { test } from 'node:test';
import assert from 'node:assert/strict';
import { normalizeShoppingState, ingredientsWithQuantities } from '../src/store/shoppingState.ts';
const recipes: any[] = [{slug:'soup',ingredients:[{quantity:'1 cup',item:'Water',group:null}]}];
test('old storage upgrades without losing checked items; duplicates and unknown keys are removed',()=>{
 const state=normalizeShoppingState({recipeSlugs:['soup','soup','missing'],checked:{'soup:0':true,'missing:0':true,'soup:1':'yes'}},recipes);
 assert.deepEqual(state,{recipeSlugs:['soup'],checked:{'soup:0':true},quantities:{}});
});
test('quantity overrides survive a serialization round trip and feed the displayed/copied ingredients',()=>{
 const state=normalizeShoppingState(JSON.parse(JSON.stringify({recipeSlugs:['soup'],checked:{},quantities:{'soup:0':'2 1/2 cups'}})),recipes);
 assert.equal(ingredientsWithQuantities(recipes[0],state.quantities)[0].quantity,'2 1/2 cups');
 assert.equal(recipes[0].ingredients[0].quantity,'1 cup');
 assert.equal(ingredientsWithQuantities(recipes[0],{'soup:0':''})[0].quantity,'');
});
test('malformed storage and oversized or orphaned quantities cannot pollute state',()=>{
 for(const input of [null,[],3,{recipeSlugs:[{}],checked:[]}]) assert.deepEqual(normalizeShoppingState(input,recipes),{recipeSlugs:[],checked:{},quantities:{}});
 assert.deepEqual(normalizeShoppingState({recipeSlugs:['soup'],quantities:{'soup:0':'x'.repeat(101),'soup:1':'2'}},recipes).quantities,{});
});
''')
p=BASE/'05/package.json';m=json.loads(p.read_text());m['scripts']['test']='tsx --test test/*.test.ts';m['devDependencies']['tsx']='^4.16.2';p.write_text(json.dumps(m,indent=2)+'\n')
write('06','test/jobBackup.test.js','''import { describe, it, expect, vi } from 'vitest';
import { parseJobBackup, exportJobBackup, commitJobBackup } from '../src/jobBackup.js';
const record={id:'a',company:'Acme',role:'Junior SWE',location:'',url:'https://example.com/job',status:'applied',stack:'JS',date:'2026-09-08',notes:'Ask about mentoring'};
describe('application backups',()=>{
 it('exports and restores records without inventing new identities',()=>{expect(parseJobBackup(exportJobBackup([record]))).toEqual([record]);});
 it.each([null,{},[],{format:'daybook.jobs',version:2,applications:[]}])('rejects an invalid envelope without writing: %j',async(payload)=>{const storage={set:vi.fn()};await expect(commitJobBackup(storage,JSON.stringify(payload))).rejects.toThrow();expect(storage.set).not.toHaveBeenCalled();});
 it.each([{id:'a'}, {company:''},{status:'unknown'},{date:'2026-02-30'},{url:'javascript:alert(1)'},{notes:123}])('rejects an entire batch with a bad record: %j',async(change)=>{
  const storage={set:vi.fn()};const text=JSON.stringify({format:'daybook.jobs',version:1,applications:[record,{...record,id:'b',...change}]});
  await expect(commitJobBackup(storage,text)).rejects.toThrow();expect(storage.set).not.toHaveBeenCalled();
 });
 it('writes exactly one complete value; a failing host write never returns replacement state',async()=>{
  const storage={set:vi.fn().mockResolvedValue({})};expect(await commitJobBackup(storage,exportJobBackup([record]))).toEqual([record]);
  expect(storage.set).toHaveBeenCalledExactlyOnceWith('jobtracker:data',JSON.stringify([record]));
  storage.set.mockRejectedValue(new Error('quota'));await expect(commitJobBackup(storage,exportJobBackup([]))).rejects.toThrow('quota');
 });
});
''')
print('Wrote focused browser, quantity and import tests')
