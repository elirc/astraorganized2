from pathlib import Path
B=Path('astrafinalplan/implementation/batch03/stage')
head='''import {test,before,after} from 'node:test';import assert from 'node:assert/strict';
import {application,request} from './http.js';let h;
before(async()=>{h=await application();});after(async()=>{if(h)await h.close();});
const call=(path,method='GET',body=undefined)=>request(h.origin,path,method,body);
'''
tests={
23:'''const valid={code:'astra-101',title:'Astra lesson',instructor:'Junior Mentor',capacity:4,enrolled:2,level:'Beginner'};
test('normalized course codes are unique while an unchanged code can be edited',async()=>{
 const made=await call('/api/courses','POST',valid);assert.equal(made.status,201);assert.equal(made.data.code,'ASTRA-101');
 assert.equal((await call('/api/courses','POST',{...valid,code:' ASTRA-101 '})).status,409);
 const edited=await call('/api/courses/'+made.data.id,'PUT',{...valid,title:'Updated lesson'});assert.equal(edited.status,200);assert.equal(edited.data.id,made.data.id);
});
test('counts must be finite whole numbers and enrollment cannot exceed capacity',async()=>{
 for(const bad of [{capacity:'bad'},{capacity:1.5},{enrolled:-1},{enrolled:5},{enrolled:null},{title:{}},{level:'Unknown'}]) assert.equal((await call('/api/courses','POST',{...valid,code:'astra-invalid',...bad})).status,400,JSON.stringify(bad));
});''',
24:'''const valid={name:'Astra event',location:'Learning room',date:'2028-02-29',capacity:3,registered:2,status:'Open'};
test('real leap-day events round-trip and invalid edits preserve the event',async()=>{
 const made=await call('/api/events','POST',valid);assert.equal(made.status,201);
 for(const bad of [{date:'2027-02-29'},{date:'2028-04-31'},{capacity:'bad'},{registered:4},{registered:1.5},{name:12}])assert.equal((await call('/api/events/'+made.data.id,'PUT',{...valid,...bad})).status,400,JSON.stringify(bad));
 const all=(await call('/api/events')).data;assert.deepEqual(all.find(x=>x.id===made.data.id),made.data);
});
test('full capacity is allowed but one registration beyond it is rejected',async()=>{
 assert.equal((await call('/api/events','POST',{...valid,registered:3})).status,201);
 assert.equal((await call('/api/events','POST',{...valid,registered:4})).status,400);
});''',
25:'''const valid={company:'AstraHiring',role:'Junior developer',stage:'Applied',contact:'Mentor',nextStepDate:'2028-03-10',notes:''};
test('follow-ups are sorted by date with undated records last and filters composed',async()=>{
 await call('/api/applications','POST',{...valid,nextStepDate:''});await call('/api/applications','POST',valid);await call('/api/applications','POST',{...valid,nextStepDate:'2028-03-01'});
 const result=(await call('/api/applications?search=AstraHiring&stage=Applied')).data;assert.deepEqual(result.map(x=>x.nextStepDate),['2028-03-01','2028-03-10','']);
 assert.equal((await call('/api/applications?search=AstraHiring&stage=Offer')).data.length,0);
});
test('invalid follow-up dates or field types do not overwrite an existing application',async()=>{
 const made=await call('/api/applications','POST',valid);
 for(const bad of [{nextStepDate:'2028-02-30'},{nextStepDate:[]},{company:{}},{notes:42}])assert.equal((await call('/api/applications/'+made.data.id,'PUT',{...valid,...bad})).status,400);
 assert.deepEqual((await call('/api/applications')).data.find(x=>x.id===made.data.id),made.data);
});''',
26:'''const valid={name:'Astraproduct tie',category:'Learning',price:12.5,stock:2};
test('equal sort values have stable page boundaries and invalid page numbers normalize',async()=>{
 for(let i=0;i<3;i++)assert.equal((await call('/api/products','POST',valid)).status,201);
 const query='/api/products?search=Astraproduct&sort=price&pageSize=2';const first=(await call(query)).data,again=(await call(query)).data;
 assert.deepEqual(first.items.map(x=>x.id),again.items.map(x=>x.id));assert.equal(first.total,3);
 const last=(await call(query+'&page=999')).data;assert.equal(last.page,2);assert.equal(last.items.length,1);
 const malformed=(await call('/api/products?page=Infinity&pageSize=2.5')).data;assert.equal(malformed.page,1);assert.equal(malformed.pageSize,5);
});
test('bad numeric/text values cannot replace a valid product',async()=>{
 const made=await call('/api/products','POST',valid);
 for(const bad of [{price:'Infinity'},{price:''},{price:true},{stock:1.5},{name:{}},{stock:null}])assert.equal((await call('/api/products/'+made.data.id,'PUT',{...valid,...bad})).status,400);
});''',
27:'''const valid={name:'Astra soup',category:'Dinner',cookTime:20,servings:2,ingredients:[' Salt ','salt','Water'],notes:''};
test('ingredient normalization deduplicates case variants while preserving first spelling',async()=>{
 const made=await call('/api/recipes','POST',valid);assert.equal(made.status,201);assert.deepEqual(made.data.ingredients,['Salt','Water']);
 const edited=await call('/api/recipes/'+made.data.id,'PUT',{...valid,servings:'4'});assert.equal(edited.status,200);assert.equal(edited.data.servings,4);assert.equal(edited.data.id,made.data.id);
});
test('nested ingredient and number failures are rejected before mutation',async()=>{
 for(const bad of [{ingredients:[{}]},{ingredients:['']},{ingredients:[]},{servings:'bad'},{servings:0.5},{cookTime:true},{notes:[]}])assert.equal((await call('/api/recipes','POST',{...valid,...bad})).status,400,JSON.stringify(bad));
});''',
29:'''const valid={title:'Astra relationship lesson',author:'Mentor',body:'One post owns many comments.'};
test('nested comments belong to one parent and deleting it removes its children',async()=>{
 const one=await call('/api/posts','POST',valid),two=await call('/api/posts','POST',valid);
 const comment=await call('/api/posts/'+one.data.id+'/comments','POST',{author:'Junior',text:'A useful example'});assert.equal(comment.status,201);
 assert.equal((await call('/api/posts/'+two.data.id+'/comments/'+comment.data.id,'DELETE')).status,404);
 assert.equal((await call('/api/posts/'+one.data.id+'/comments')).data.length,1);
 assert.equal((await call('/api/posts/'+one.data.id,'DELETE')).status,204);
 assert.equal((await call('/api/posts/'+one.data.id+'/comments')).status,404);
});
test('object-valued text produces a clear validation response without saving a comment',async()=>{
 assert.equal((await call('/api/posts','POST',{...valid,title:{}})).status,400);
 const made=await call('/api/posts','POST',valid);
 for(const bad of [{author:4,text:'hello'},{author:'Junior',text:{}},{author:'Junior',text:'x'.repeat(2001)}])assert.equal((await call('/api/posts/'+made.data.id+'/comments','POST',bad)).status,400);
 assert.equal((await call('/api/posts/'+made.data.id+'/comments')).data.length,0);
});''',
32:'''const valid={title:'Astra priority lesson',status:'Backlog',priority:'High',assignee:'Junior',description:'Priority and status are independent.'};
test('priority, status and search filters compose without changing records',async()=>{
 await call('/api/issues','POST',valid);await call('/api/issues','POST',{...valid,priority:'Low'});await call('/api/issues','POST',{...valid,status:'Done'});
 const rows=(await call('/api/issues?search=Astra&status=Backlog&priority=High')).data;assert.equal(rows.length,1);assert.equal(rows[0].priority,'High');assert.equal(rows[0].status,'Backlog');
 assert.equal((await call('/api/issues?priority=Unknown')).status,400);
});
test('malformed issue text cannot overwrite existing details',async()=>{
 const made=await call('/api/issues','POST',valid);
 for(const bad of [{title:{}},{assignee:[]},{description:42}])assert.equal((await call('/api/issues/'+made.data.id,'PUT',{...valid,...bad})).status,400);
 assert.deepEqual((await call('/api/issues/'+made.data.id)).data,made.data);
});'''}
for n,body in tests.items():(B/str(n)/'test/api.test.js').write_text(head+body+'\n',encoding='utf-8')
print('Added fourteen tests across the seven smaller API projects.')
