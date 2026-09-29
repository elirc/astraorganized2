from pathlib import Path
import json
BASE=Path(__file__).resolve().parent/'stage'
def write(n,f,s):
 p=BASE/n/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
helper='''const { Client } = require('pg');
const { randomBytes } = require('node:crypto');

function configure() {
  const input = process.env.ASTRA_TEST_DATABASE_URL;
  if (!input) throw new Error('Set ASTRA_TEST_DATABASE_URL to an isolated PostgreSQL database named astra_test_*');
  const url = new URL(input);
  if (!/^astra_test_[a-z0-9_]+$/.test(url.pathname.slice(1))) throw new Error('Tests require a dedicated astra_test_* database');
  process.env.DATABASE_URL = input;
  process.env.DB_HOST = url.hostname; process.env.DB_PORT = url.port || '5432';
  process.env.DB_NAME = url.pathname.slice(1); process.env.DB_USER = decodeURIComponent(url.username);
  process.env.DB_PASSWORD = decodeURIComponent(url.password) || 'local-test';
  process.env.DB_SSL = 'false'; process.env.NODE_ENV = 'test';
  process.env.JWT_ACCESS_SECRET = 'astra-local-test-access-secret';
  process.env.JWT_REFRESH_SECRET = 'astra-local-test-refresh-secret';
  process.env.COOKIE_SECRET = 'astra-local-test-cookie-secret';
  return input;
}

async function prepare(db, up) {
  const connectionString = configure();
  const schema = `astra_${Date.now()}_${randomBytes(5).toString('hex')}`;
  const admin = new Client({ connectionString }); await admin.connect();
  await admin.query(`CREATE SCHEMA "${schema}"`);
  db.client.config.searchPath = [schema];
  await up(db);
  return async () => {
    await db.destroy();
    // Only the unique schema created above is removed; never an existing schema.
    await admin.query(`DROP SCHEMA "${schema}" CASCADE`);
    await admin.end();
  };
}

async function listen(app) {
  const server = await new Promise((resolve, reject) => {
    const instance = app.listen(0, '127.0.0.1', () => resolve(instance));
    instance.on('error', reject);
  });
  return {
    async request(method, path, body, token) {
      const response = await fetch(`http://127.0.0.1:${server.address().port}${path}`, {
        method, headers: { 'Content-Type':'application/json', ...(token ? { Authorization:`Bearer ${token}` } : {}) },
        body: body === undefined ? undefined : JSON.stringify(body),
      });
      return { status:response.status, body:await response.json() };
    },
    close: () => new Promise((resolve) => { server.close(resolve); server.closeAllConnections(); }),
  };
}
module.exports = { configure, prepare, listen };
'''
for n in ['07','08','09','10']:
 write(n,'server/test/database.cjs',helper)
 p=BASE/n/'server/package.json';m=json.loads(p.read_text());m['scripts']['test']='tsx --test test/*.test.ts' if n=='10' else 'node --test test/*.test.cjs';p.write_text(json.dumps(m,indent=2)+'\n')

write('07','server/test/tasks.test.cjs','''const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const harness = require('./database.cjs'); harness.configure();
const { db } = require('../src/config/database');
const app = require('../src/app');
let clean, api;
before(async()=>{clean=await harness.prepare(db,require('../db/migrations/20260703000000_create_tasks_table').up);api=await harness.listen(app);});
after(async()=>{if(api)await api.close();if(clean)await clean();});
test('HTTP create/read/filter/edit/delete round trip persists actual SQL rows',async()=>{
 const created=await api.request('POST','/api/tasks',{title:'Learn the request path',priority:'high',due_date:'2099-01-01'});
 assert.equal(created.status,201);const id=created.body.data.id;
 assert.equal((await db('tasks').where({id}).first()).title,'Learn the request path');
 const list=await api.request('GET','/api/tasks?priority=high');assert.ok(list.body.data.some((task)=>task.id===id));
 const done=await api.request('PUT',`/api/tasks/${id}`,{status:'done'});assert.equal(done.status,200);assert.ok(done.body.data.completed_at);
 const reopened=await api.request('PUT',`/api/tasks/${id}`,{status:'todo'});assert.equal(reopened.body.data.completed_at,null);
 assert.equal((await api.request('DELETE',`/api/tasks/${id}`)).status,200);
 assert.equal((await api.request('GET',`/api/tasks/${id}`)).status,404);
});
test('invalid inputs are client errors and never create rows',async()=>{
 const before=Number((await db('tasks').count('* as count').first()).count);
 for(const body of [{title:' '},{title:'x'.repeat(256)},{title:'x',due_date:'2099-02-30'},{title:'x',priority:'urgent'}])
  assert.equal((await api.request('POST','/api/tasks',body)).status,400);
 assert.equal((await api.request('GET','/api/tasks/9007199254740992')).status,400);
 assert.equal(Number((await db('tasks').count('* as count').first()).count),before);
});
test('an overdue task can be edited when the existing date is submitted unchanged',async()=>{
 const [row]=await db('tasks').insert({title:'Overdue',due_date:'2020-01-01',priority:'low',status:'todo'}).returning('*');
 const result=await api.request('PUT',`/api/tasks/${row.id}`,{title:'Still relevant',due_date:'2020-01-01'});
 assert.equal(result.status,200);assert.equal((await db('tasks').where({id:row.id}).first()).title,'Still relevant');
 assert.equal((await api.request('PUT',`/api/tasks/${row.id}`,{due_date:'2020-01-02'})).status,400);
});
''')
write('08','server/test/import.test.cjs','''const { test, before, after }=require('node:test');const assert=require('node:assert/strict');
const harness=require('./database.cjs');harness.configure();
const db=require('../src/config/db');const service=require('../src/services/contactService');
const { csvToContacts, contactsToCsv }=require('../src/utils/csv');let clean;
before(async()=>{clean=await harness.prepare(db,require('../db/migrations/202607030201_create_contacts_tags').up);});
after(async()=>{if(clean)await clean();});
test('quoted commas, doubled quotes, multiline notes and CRLF round-trip with tags',async()=>{
 const csv='first_name,last_name,email,company,notes,tags\\r\\nAda,Lovelace,ada@example.com,"Labs, Inc.","Line one\\nShe said ""hello""",Friend|Colleague';
 const result=await service.importContacts(csv);assert.equal(result.imported,1);
 const contact=await service.getContact(result.contacts[0].id);assert.equal(contact.company,'Labs, Inc.');assert.equal(contact.notes,'Line one\\nShe said "hello"');
 assert.deepEqual(contact.tags.map((tag)=>tag.name),['Colleague','Friend']);
 assert.equal(csvToContacts(contactsToCsv([contact]))[0].notes,contact.notes);
});
test('malformed late record rejects the entire batch without saving the earlier valid contact',async()=>{
 const before=Number((await db('contacts').count('* as n').first()).n);
 for(const csv of ['first_name,last_name\\nGrace,Hopper\\nInvalid', 'first_name,last_name\\nGrace,Hopper\\n,Missing', 'first_name,last_name\\n"Unclosed,Hopper', 'first_name,first_name,last_name\\nA,B,C']) await assert.rejects(()=>service.importContacts(csv));
 assert.equal(Number((await db('contacts').count('* as n').first()).n),before);
});
test('a late database uniqueness failure rolls back contacts, new tags and junctions',async()=>{
 await assert.rejects(()=>service.importContacts('first_name,last_name,email,tags\\nFirst,Person,rollback@example.com,TemporaryTag\\nSecond,Person,rollback@example.com,OtherTag'),/no contacts were imported/);
 assert.equal((await db('contacts').where({email:'rollback@example.com'})).length,0);
 assert.equal((await db('tags').whereIn('name',['TemporaryTag','OtherTag'])).length,0);
});
test('equal-name contacts page deterministically and bad pagination is rejected',async()=>{
 await service.importContacts('first_name,last_name,company\\nA,Tie,PageFixture\\nB,Tie,PageFixture\\nC,Tie,PageFixture');
 const a=await service.listContacts({search:'PageFixture',page:1,limit:2});const b=await service.listContacts({search:'PageFixture',page:2,limit:2});
 assert.equal(a.pagination.total,3);assert.equal(new Set([...a.contacts,...b.contacts].map(x=>x.id)).size,3);
 await assert.rejects(()=>service.listContacts({page:'nope'}));await assert.rejects(()=>service.listContacts({limit:1.5}));
});
''')
write('09','server/test/reports.test.cjs','''const { test,before,after }=require('node:test');const assert=require('node:assert/strict');
const harness=require('./database.cjs');harness.configure();const db=require('../src/config/db');const service=require('../src/services/expenseService');let clean,food,travel;
before(async()=>{
 clean=await harness.prepare(db,require('../db/migrations/202607030301_create_expense_tracker').up);
 [food,travel]=await db('categories').insert([{name:'Food'},{name:'Travel'}]).returning('*');
 await db('expenses').insert([
  {amount:99,description:'Before',category_id:food.id,expense_date:'2024-01-31'},
  {amount:10.10,description:'First day',category_id:food.id,expense_date:'2024-02-01'},
  {amount:20.20,description:'Leap day',category_id:food.id,expense_date:'2024-02-29'},
  {amount:4.70,description:'Bus',category_id:travel.id,expense_date:'2024-02-15'},
  {amount:777,description:'After',category_id:food.id,expense_date:'2024-03-01'},
 ]);
});
after(async()=>{if(clean)await clean();});
test('monthly total and count include the leap day and exclude adjacent months',async()=>{
 const summary=await service.monthlySummary('2024-02');assert.equal(summary.total_spent,35);assert.equal(summary.expense_count,3);
 const empty=await service.monthlySummary('2025-01');assert.equal(empty.total_spent,0);assert.equal(empty.expense_count,0);
});
test('category SQL executes and reconciles with monthly and daily totals',async()=>{
 const rows=await service.byCategory({start_date:'2024-02-01',end_date:'2024-02-29'});
 assert.equal(rows.find(x=>x.name==='Food').total,30.3);assert.equal(rows.find(x=>x.name==='Travel').total,4.7);
 const daily=await service.dailyTrend('2024-02');assert.equal(daily.reduce((sum,x)=>sum+Math.round(x.total*100),0),3500);
 const filtered=await service.byCategory({start_date:'2024-02-01',end_date:'2024-02-29',category_id:travel.id});assert.equal(filtered.length,1);assert.equal(filtered[0].total,4.7);
});
test('date/filter/money validation fails before malformed data reaches SQL',async()=>{
 assert.throws(()=>service.monthlySummary('2024-13'));assert.throws(()=>service.byCategory({start_date:'2024-02-30'}));assert.throws(()=>service.byCategory({start_date:'2024-03-01',end_date:'2024-02-01'}));
 for(const amount of [Infinity,-1,0,1.001]) await assert.rejects(()=>service.createExpense({amount,description:'Invalid',category_id:food.id,expense_date:'2024-02-01'}));
});
''')
write('10','server/test/ownership.test.ts','''import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import jwt from 'jsonwebtoken';
import harness from './database.cjs';
harness.configure();
const { db } = await import('../src/config/db.js');
const service = await import('../src/services/recipeService.js');
const migration = await import('../db/migrations/001_initial_schema.js');
const appModule = await import('../src/app.js');
let cleanup: () => Promise<void>, api: any, alice: any, bob: any;
const input = { title:'Soup', ingredients:[{name:'Water',quantity:'1',unit:'cup'}],steps:[{instruction:'Boil'}],isPublic:false };
before(async()=>{
 cleanup = await harness.prepare(db,migration.up);
 [alice,bob]=await db('users').insert([{username:'alice',email:'alice@example.com',password_hash:'test-only'},{username:'bob',email:'bob@example.com',password_hash:'test-only'}]).returning('*');
 api=await harness.listen(appModule.app ?? appModule.default);
});
after(async()=>{if(api)await api.close();if(cleanup)await cleanup();});
const token=(user:any)=>jwt.sign({id:user.id,username:user.username,email:user.email},process.env.JWT_ACCESS_SECRET!);
test('authenticated nonowner cannot edit/delete or read a private recipe, even with forged ownership in the body',async()=>{
 const recipe=await service.createRecipeForUser(alice.id,input);
 const result=await api.request('PUT',`/api/recipes/${recipe.id}`,{...input,title:'Stolen',user_id:alice.id},token(bob));
 assert.equal(result.status,403);assert.equal((await db('recipes').where({id:recipe.id}).first()).title,'Soup');
 assert.equal((await api.request('DELETE',`/api/recipes/${recipe.id}`,undefined,token(bob))).status,403);
 assert.equal((await api.request('GET',`/api/recipes/${recipe.id}`,undefined,token(bob))).status,403);
 assert.equal((await api.request('PUT',`/api/recipes/${recipe.id}`,input)).status,401);
 assert.equal((await api.request('PUT',`/api/recipes/${recipe.id}`,{...input,title:'My soup'},token(alice))).status,200);
});
test('failed nested replacement rolls back the parent and all original children',async()=>{
 const recipe=await service.createRecipeForUser(alice.id,input);
 const before=await service.getRecipe(recipe.id,alice.id);
 await assert.rejects(()=>service.updateRecipeForUser(alice.id,recipe.id,{...input,title:'Should roll back',ingredients:[{name:'Salt'}],categoryIds:[2147483647]}));
 const after=await service.getRecipe(recipe.id,alice.id);
 assert.equal(after.title,before.title);assert.deepEqual(after.ingredients,before.ingredients);assert.deepEqual(after.steps,before.steps);
 const count=Number((await db('recipes').count('* as n').first())!.n);
 await assert.rejects(()=>service.createRecipeForUser(alice.id,{...input,categoryIds:[2147483647]}));
 assert.equal(Number((await db('recipes').count('* as n').first())!.n),count);
});
test('malformed nested payloads are validation errors, not silent empty recipes or TypeErrors',()=>{
 for(const change of [{title:' '},{ingredients:[null]},{ingredients:[{name:' '}]},{steps:[{}]},{servings:-1},{isPublic:'false'},{categoryIds:[0]}])
  assert.throws(()=>service.parseRecipeInput({...input,...change}),(error:any)=>error.name==='ValidationError');
});
''')
print('Wrote PostgreSQL-backed regression suites for all four servers')
