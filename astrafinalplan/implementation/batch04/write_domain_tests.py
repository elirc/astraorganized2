from pathlib import Path
import json
B=Path('astrafinalplan/implementation/batch04');R=B/'stage'
memory=json.loads((B/'memory-domain-specs.json').read_text(encoding='utf-8'));sql=json.loads((B/'domain-specs.json').read_text(encoding='utf-8'))
helper='''import { app } from "../server/server.js";
export async function application() {
 const server=app.listen(0,"127.0.0.1");await new Promise(resolve=>server.once("listening",resolve));
 return {origin:"http://127.0.0.1:"+server.address().port,async close(){await new Promise(resolve=>{server.close(resolve);server.closeAllConnections();});}};
}
export async function request(origin,path,method="GET",body){
 const response=await fetch(origin+path,{method,headers:body===undefined?{}:{"Content-Type":"application/json"},body:body===undefined?undefined:JSON.stringify(body)});
 return {status:response.status,data:response.status===204?null:await response.json()};
}
'''
for x in json.loads((B/'kinds.json').read_text()):
 if not x['typescript']:
  p=R/x['stage']/'test';p.mkdir(exist_ok=True);(p/'http.js').write_text(helper,encoding='utf-8')
for x in memory+sql:
 is_sql=x in sql;p=R/x['stage']/'test';p.mkdir(exist_ok=True)
 code='''import {test,before,after} from 'node:test';
import assert from 'node:assert/strict';
IMPORT
let h;
before(async()=>{h=await FACTORY();});after(async()=>{if(h)await h.close();});
const route=ROUTE, statuses=STATUSES;
const valid={title:'A lesson record',owner:'Junior Learner',category:CATEGORY,status:statuses[0],amount:12.50,priority:'Medium',dueDate:'2028-02-29',notes:'A controlled regression fixture'};
const call=(path,method='GET',body=undefined)=>request(h.origin,path,method,body);

test('valid records round-trip and malformed edits leave the stored record intact',async()=>{
 const made=await call(route,'POST',valid);assert.equal(made.status,201);assert.equal(made.data.dueDate,'2028-02-29');
 for(const bad of [{title:44},{title:'x'.repeat(201)},{dueDate:'2027-02-29'},{priority:'Unknown'},{notes:{}},{amount:null}]){
  assert.equal((await call(route+'/'+made.data.id,'PUT',{...valid,...bad})).status,400,JSON.stringify(bad));
 }
 assert.deepEqual((await call(route+'/'+made.data.id)).data,made.data);
 assert.equal((await call(route+'/'+made.data.id+'/activity','POST',{body:{bad:true}})).status,400);
});
test('equal sort keys give stable pages and an out-of-range page retains real totals',async()=>{
 for(let i=0;i<3;i++)assert.equal((await call(route,'POST',{...valid,title:'Astrafixture shared'})).status,201);
 const filter='?search=Astrafixture&sort=title&dir=asc&pageSize=2';
 const first=(await call(route+filter+'&page=1')).data,again=(await call(route+filter+'&page=1')).data;
 assert.equal(first.total,3);assert.deepEqual(first.items.map(x=>x.id),again.items.map(x=>x.id));
 const last=(await call(route+filter+'&page=999')).data;assert.equal(last.total,3);assert.equal(last.page,2);assert.equal(last.items.length,1);
 const empty=(await call(route+'?search=absolutelyabsentfixture&page=999')).data;assert.equal(empty.total,0);assert.equal(empty.page,1);
 const fraction=(await call(route+'?page=1.5&pageSize=Infinity')).data;assert.equal(fraction.page,1);assert.equal(fraction.pageSize,6);
});
test('repeated status requests produce one history entry for the actual change',async()=>{
 const made=await call(route,'POST',valid),path=route+'/'+made.data.id;
 const responses=await Promise.all([call(path+'/status','PATCH',{status:statuses[1]}),call(path+'/status','PATCH',{status:statuses[1]})]);
 assert.deepEqual(responses.map(x=>x.status),[200,200]);
 const entries=(await call(path+'/activity')).data;assert.equal(entries.filter(x=>x.kind==='status').length,1);
 assert.equal((await call(path)).data.status,statuses[1]);assert.equal((await call(path+'/status','PATCH',{status:'Unknown'})).status,400);
});
'''.replace('IMPORT',"import {database,request} from './database.js';" if is_sql else "import {application,request} from './http.js';").replace('FACTORY','database' if is_sql else 'application').replace('ROUTE',json.dumps(x['route'])).replace('STATUSES',json.dumps(x['statuses'])).replace('CATEGORY',json.dumps(x['categories'][0]))
 if is_sql:code+='''
test('a failed activity insert rolls back the status update',async()=>{
 const made=await call(route,'POST',valid),id=made.data.id,path=route+'/'+id;
 await h.admin.query(`CREATE FUNCTION reject_lesson_audit() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN IF NEW.kind='status' THEN RAISE EXCEPTION 'injected audit failure'; END IF; RETURN NEW; END $$`);
 await h.admin.query('CREATE TRIGGER fail_lesson_audit BEFORE INSERT ON activity_entries FOR EACH ROW EXECUTE FUNCTION reject_lesson_audit()');
 try{
  assert.equal((await call(path+'/status','PATCH',{status:statuses[1]})).status,500);
  assert.deepEqual((await call(path)).data,made.data);
  assert.equal((await call(path+'/activity')).data.length,1);
 }finally{await h.admin.query('DROP TRIGGER fail_lesson_audit ON activity_entries');}
 assert.equal((await call(path+'/status','PATCH',{status:statuses[1]})).status,200);
});
'''
 (p/('workflow.test.ts' if is_sql else 'workflow.test.js')).write_text(code,encoding='utf-8')
print('Added regression suites for sixteen domain apps.')
