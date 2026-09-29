from pathlib import Path
B=Path('astrafinalplan/implementation/batch03/stage')
head='''import {test,before,after} from 'node:test';import assert from 'node:assert/strict';import {randomUUID} from 'node:crypto';
import {database,request} from './database.js';let h;
before(async()=>{h=await database();});after(async()=>{if(h)await h.close();});
const call=(path,method='GET',body=undefined)=>request(h.origin,path,method,body);
'''
tests={28:'''test('self and descendant moves are rejected while moving back to a root is supported',async()=>{
 const a=await call('/api/nodes','POST',{name:'Astra root',title:'Root',parentId:null});assert.equal(a.status,201);
 const b=await call('/api/nodes','POST',{name:'Astra child',title:'Child',parentId:a.data.id});assert.equal(b.status,201);
 assert.equal((await call('/api/nodes/'+a.data.id+'/move','PATCH',{newParentId:b.data.id})).status,400);
 assert.equal((await call('/api/nodes/'+a.data.id+'/move','PATCH',{newParentId:a.data.id})).status,400);
 assert.equal((await call('/api/nodes/'+b.data.id+'/move','PATCH',{newParentId:null})).status,200);
 assert.equal((await call('/api/nodes/'+b.data.id)).data.depth,0);
});
test('opposing concurrent moves cannot introduce a cycle',async()=>{
 const a=await call('/api/nodes','POST',{name:'Concurrent A',title:'',parentId:null}),b=await call('/api/nodes','POST',{name:'Concurrent B',title:'',parentId:null});
 const results=await Promise.all([call('/api/nodes/'+a.data.id+'/move','PATCH',{newParentId:b.data.id}),call('/api/nodes/'+b.data.id+'/move','PATCH',{newParentId:a.data.id})]);
 assert.deepEqual(results.map(x=>x.status).sort(),[200,400]);
 const aa=(await call('/api/nodes/'+a.data.id)).data,bb=(await call('/api/nodes/'+b.data.id)).data;assert.equal(aa.depth+bb.depth,1);assert.equal((await call('/api/tree')).status,200);
});
test('invalid or nonexistent parent references leave the hierarchy unchanged',async()=>{
 const a=await call('/api/nodes','POST',{name:'Reference test',title:'',parentId:null});
 assert.equal((await call('/api/nodes/'+a.data.id+'/move','PATCH',{})).status,400);
 assert.equal((await call('/api/nodes/'+a.data.id+'/move','PATCH',{newParentId:randomUUID()})).status,400);
 assert.equal((await call('/api/nodes/'+a.data.id)).data.depth,0);
 assert.equal((await call('/api/nodes/invalid')).status,400);
});''',30:'''test('daily analytics fill missing calendar days and include exactly the requested window',async()=>{
 await h.admin.query('TRUNCATE events');
 await h.admin.query("INSERT INTO events(name,product,amount,occurred_at) VALUES ('purchase','Fixture',100,CURRENT_DATE-3),('purchase','Fixture',10,CURRENT_DATE-2),('purchase','Fixture',30,CURRENT_DATE)");
 assert.equal((await call('/api/metrics/refresh','POST',{})).status,200);
 const daily=(await call('/api/metrics/daily?days=3')).data;assert.equal(daily.length,3);assert.deepEqual(daily.map(x=>x.revenue),[10,0,30]);
 assert.deepEqual(daily.map(x=>x.revenueCumulative),[10,10,40]);assert.deepEqual(daily.map(x=>x.revenueMa7),[10,5,13.33]);assert.deepEqual(daily.map(x=>x.revenueDelta),[null,-10,30]);
 const summary=(await call('/api/metrics/summary?days=3')).data;assert.equal(summary.revenue,40);assert.equal(summary.orders,2);
});
test('invalid event values never reach the raw event table',async()=>{
 const before=Number((await h.admin.query('SELECT COUNT(*) AS n FROM events')).rows[0].n);
 for(const body of [{name:'purchase',product:'Fixture',amount:'Infinity'},{name:'purchase',product:'Fixture',amount:null},{name:'view',product:{}},{name:'unknown',product:'Fixture'}])assert.equal((await call('/api/events','POST',body)).status,400);
 assert.equal(Number((await h.admin.query('SELECT COUNT(*) AS n FROM events')).rows[0].n),before);
});
test('freshness reports the gap between raw events and the refreshed view',async()=>{
 const added=await call('/api/events','POST',{name:'view',product:'Fixture',amount:0});assert.equal(added.status,201);assert.equal(added.data.stale,true);
 const refreshed=await call('/api/metrics/refresh','POST',{});assert.equal(refreshed.data.stale,false);
});''',31:'''async function fixture(){const agents=(await call('/api/agents')).data,labels=(await call('/api/labels')).data;return {subject:'Astra support lesson',body:'Explain one transaction',priority:'normal',assigneeId:agents[0].id,labelIds:labels.slice(0,1).map(x=>x.id)};}
test('repeated status and assignment commands record only actual changes',async()=>{
 const made=await call('/api/tickets','POST',await fixture());assert.equal(made.status,201);const path='/api/tickets/'+made.data.id;
 const result=await Promise.all([call(path+'/status','PATCH',{status:'resolved'}),call(path+'/status','PATCH',{status:'resolved'})]);assert.deepEqual(result.map(x=>x.status),[200,200]);
 await call(path+'/assignee','PATCH',{assigneeId:null});await call(path+'/assignee','PATCH',{assigneeId:null});
 const events=(await call(path+'/events')).data;assert.equal(events.filter(x=>x.kind==='status').length,1);assert.equal(events.filter(x=>x.kind==='assignment').length,1);
});
test('a late invalid label reference rolls back edits and earlier label deletion',async()=>{
 const input=await fixture(),made=await call('/api/tickets','POST',input),path='/api/tickets/'+made.data.id;
 const changed=await call(path,'PUT',{...input,subject:'Must roll back',labelIds:[randomUUID()]});assert.equal(changed.status,400);
 assert.deepEqual((await call(path)).data,made.data);assert.equal((await call(path+'/events')).data.length,1);
 assert.equal((await call('/api/tickets','POST',{...input,subject:{}})).status,400);
});
test('an audit write failure cannot commit a ticket status change',async()=>{
 const made=await call('/api/tickets','POST',await fixture()),path='/api/tickets/'+made.data.id;
 await h.admin.query("CREATE FUNCTION reject_ticket_log() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN IF NEW.kind='status' THEN RAISE EXCEPTION 'injected log failure'; END IF; RETURN NEW; END $$");
 await h.admin.query('CREATE TRIGGER reject_ticket_log BEFORE INSERT ON ticket_events FOR EACH ROW EXECUTE FUNCTION reject_ticket_log()');
 try{assert.equal((await call(path+'/status','PATCH',{status:'closed'})).status,500);assert.deepEqual((await call(path)).data,made.data);}finally{await h.admin.query('DROP TRIGGER reject_ticket_log ON ticket_events');}
});''',33:'''test('search plus tag filtering retains totals when requesting a page beyond the end',async()=>{
 const user=(await call('/api/users')).data[0];
 for(let i=0;i<3;i++)assert.equal((await call('/api/threads','POST',{title:'Astraforum paging',body:'Astraforum explains stable SQL pagination.',authorId:user.id,tagNames:[' Lesson ','lesson']})).status,201);
 const query='/api/threads?q=Astraforum&tag=lesson&pageSize=2';const first=(await call(query)).data,again=(await call(query)).data;assert.equal(first.total,3);assert.deepEqual(first.items.map(x=>x.id),again.items.map(x=>x.id));
 const last=(await call(query+'&page=999')).data;assert.equal(last.total,3);assert.equal(last.page,2);assert.equal(last.items.length,1);
 const empty=(await call('/api/threads?q=absentfixture&page=999')).data;assert.equal(empty.total,0);assert.equal(empty.page,1);
});
test('malformed nested tags and author references do not create partial threads',async()=>{
 const user=(await call('/api/users')).data[0],input={title:'Validation lesson',body:'Some text',authorId:user.id,tagNames:['lesson']};
 const count=Number((await h.admin.query('SELECT COUNT(*) AS n FROM threads')).rows[0].n);
 for(const bad of [{tagNames:[{}]},{tagNames:['']},{authorId:'bad'},{authorId:randomUUID()},{title:4}])assert.equal((await call('/api/threads','POST',{...input,...bad})).status,400);
 assert.equal(Number((await h.admin.query('SELECT COUNT(*) AS n FROM threads')).rows[0].n),count);
});''',34:'''async function fixture(){const client=(await call('/api/clients')).data[0];return {clientId:client.id,status:'draft',issuedDate:'2028-02-29',taxRate:10,items:[{description:'Lesson',quantity:2,unitPrice:0.1}]};}
test('invoice totals use validated line inputs and preserve calendar dates',async()=>{
 const made=await call('/api/invoices','POST',await fixture());assert.equal(made.status,201);assert.equal(made.data.issuedDate,'2028-02-29');assert.equal(made.data.subtotal,0.2);assert.equal(made.data.tax,0.02);assert.equal(made.data.total,0.22);
});
test('invalid dates, whole quantities and nested values are rejected before replacing lines',async()=>{
 const input=await fixture(),made=await call('/api/invoices','POST',input),path='/api/invoices/'+made.data.id;
 for(const bad of [{issuedDate:'2027-02-29'},{taxRate:'Infinity'},{taxRate:101},{items:[null]},{items:[{description:'bad',quantity:1.5,unitPrice:2}]},{items:[{description:'bad',quantity:[1],unitPrice:2}]},{items:[{description:'bad',quantity:1,unitPrice:0.001}]}])assert.equal((await call(path,'PUT',{...input,...bad})).status,400,JSON.stringify(bad));
 assert.deepEqual((await call(path)).data,made.data);
});
test('a database failure after line deletion restores the original invoice and lines',async()=>{
 const input=await fixture(),made=await call('/api/invoices','POST',input),path='/api/invoices/'+made.data.id;
 await h.admin.query("CREATE FUNCTION reject_invoice_line() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN IF NEW.description='Fail after delete' THEN RAISE EXCEPTION 'injected line failure'; END IF; RETURN NEW; END $$");
 await h.admin.query('CREATE TRIGGER reject_invoice_line BEFORE INSERT ON invoice_items FOR EACH ROW EXECUTE FUNCTION reject_invoice_line()');
 try{assert.equal((await call(path,'PUT',{...input,items:[{description:'Fail after delete',quantity:1,unitPrice:2}]})).status,500);assert.deepEqual((await call(path)).data,made.data);}finally{await h.admin.query('DROP TRIGGER reject_invoice_line ON invoice_items');}
});'''}
for n,body in tests.items():(B/str(n)/'test/feature.test.ts').write_text(head+body+'\n',encoding='utf-8')
print('Added fourteen HTTP/database tests across the five distinct SQL apps.')
