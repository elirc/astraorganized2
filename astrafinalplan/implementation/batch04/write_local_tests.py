from pathlib import Path
B=Path('astrafinalplan/implementation/batch04')
(B/'stage/74/src/importValidation.test.ts').write_text('''import 'fake-indexeddb/auto';
import {beforeEach,it,expect} from 'vitest';
import {db,seedAndLoad,buildExport,importData} from './db';
beforeEach(async()=>{await db.delete();await db.open();await seedAndLoad(Date.now());});
it('rejects malformed nested values and duplicate card IDs before changing any progress',async()=>{
 const original=await buildExport();
 for(const mutate of [(p:typeof original)=>{p.reviewStates[0].due=-1;},(p:typeof original)=>{p.reviewStates.push({...p.reviewStates[0]});},(p:typeof original)=>{p.settings.newCardsPerDay=-1;},(p:typeof original)=>{p.meta.lastReviewDay='2025-02-30';}]) {
  const bad=structuredClone(original);mutate(bad);await expect(importData(bad,Date.now())).rejects.toThrow(/Malformed backup/);
  const after=await buildExport();expect(after.reviewStates).toEqual(original.reviewStates);expect(after.settings).toEqual(original.settings);expect(after.meta).toEqual(original.meta);
 }
});
it('valid restore keeps progress, omits unknown-card logs, and recreates missing states',async()=>{
 const backup=await buildExport();const kept=backup.reviewStates[0];kept.reps=7;backup.reviewStates=[kept];backup.reviewLogs=[{cardId:kept.cardId,reviewedAt:Date.now(),grade:2,msTaken:100,statusBefore:'new'},{cardId:'removed-card',reviewedAt:Date.now(),grade:2,msTaken:100,statusBefore:'new'}];
 expect(await importData(backup,Date.now())).toBe(1);expect((await db.reviewStates.get(kept.cardId))?.reps).toBe(7);expect(await db.reviewStates.count()).toBeGreaterThan(1);expect(await db.reviewLogs.count()).toBe(1);
});
''')
root=B/'stage/72';(root/'test').mkdir(exist_ok=True)
(root/'test/recipes.test.ts').write_text('''import {test,before,after} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
let server:any,db:any,origin:string,directory:string,dish:number,recipe:number;
before(async()=>{directory=await mkdtemp(path.join(tmpdir(),'astra-recipe-test-'));process.env.RECIPE_LAB_DATA=directory;db=(await import('../server/db.ts')).db;const {app}=await import('../server/index.ts');server=app.listen(0,'127.0.0.1');await new Promise<void>(r=>server.once('listening',r));origin='http://127.0.0.1:'+server.address().port;});
after(async()=>{if(server)await new Promise<void>(r=>{server.close(()=>r());server.closeAllConnections();});db?.close();if(directory)await rm(directory,{recursive:true,force:true});});
async function api(path:string,method='GET',body?:unknown){const r=await fetch(origin+'/api'+path,{method,headers:{'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)});return {status:r.status,data:r.status===204?null:await r.json()};}
test('nested recipe create and partial edit preserve ingredients and steps',async()=>{let r=await api('/dishes','POST',{name:'Pasta'});assert.equal(r.status,201);dish=r.data.id;r=await api(`/dishes/${dish}/recipes`,'POST',{title:'Weeknight',yield_qty:2,ingredients:[{item:'Pasta',qty:100,unit:'g'}],steps:[{text:'Boil water'}]});assert.equal(r.status,201);recipe=r.data.id;r=await api(`/recipes/${recipe}`,'PATCH',{title:'Renamed'});assert.equal(r.status,200);assert.equal(r.data.ingredients[0].item,'Pasta');assert.equal(r.data.steps[0].text,'Boil water');});
test('invalid nested edits leave parent, children and search entries unchanged',async()=>{const before=(await api(`/recipes/${recipe}`)).data;for(const body of [{title:'',ingredients:[]},{title:'Changed',ingredients:[{item:'Pasta',qty:-2}]},{steps:[null]},{tags:[{}]},{yield_qty:0}])assert.equal((await api(`/recipes/${recipe}`,'PATCH',body)).status,400);assert.deepEqual((await api(`/recipes/${recipe}`)).data,before);assert.equal((await api('/recipes/1e2')).status,400);});
test('deleting a dish cascades recipes and removes search entries',async()=>{assert.equal((await api(`/dishes/${dish}`,'DELETE')).status,204);assert.equal((await api(`/recipes/${recipe}`)).status,404);assert.equal(db.prepare("SELECT count(*) AS n FROM search_index WHERE (kind='dish' AND ref_id=?) OR (kind='recipe' AND ref_id=?)").get(dish,recipe).n,0);});
''')
root=B/'stage/75';(root/'test').mkdir(exist_ok=True)
(root/'test/applications.test.js').write_text('''const {test,before,after}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');const os=require('node:os');const path=require('node:path');
let server,db,origin,directory,token,id;
before(async()=>{directory=await fs.mkdtemp(path.join(os.tmpdir(),'astra-job-test-'));process.env.JOB_TRACK_DATA_DIR=directory;process.env.JWT_SECRET='isolated-test-key-not-for-deployment';const {app}=require('../server/src/server');db=require('../server/src/db');server=app.listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));origin='http://127.0.0.1:'+server.address().port;const r=await api('/auth/register','POST',{name:'Learner',email:'learner@example.com',password:'learning123'});assert.equal(r.status,201);token=r.data.token;});
after(async()=>{if(server)await new Promise(r=>{server.close(r);server.closeAllConnections();});db?.close();if(directory)await fs.rm(directory,{recursive:true,force:true});});
async function api(path,method='GET',body){const r=await fetch(origin+'/api'+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:'Bearer '+token}:{})},body:body===undefined?undefined:JSON.stringify(body)});return{status:r.status,data:r.status===204?null:await r.json()};}
test('create and clear optional fields without turning blank salary into zero',async()=>{const r=await api('/applications','POST',{company:'Acme',role:'Engineer',applied_date:'2026-09-01',status:'applied',salary_min:'',salary_max:'',notes:'Old notes',next_step_date:'2026-09-10'});assert.equal(r.status,201,JSON.stringify(r.data));id=r.data.item.id;assert.equal(r.data.item.salary_min,null);const edit=await api('/applications/'+id,'PUT',{notes:'',next_step_date:''});assert.equal(edit.status,200);assert.equal(edit.data.item.notes,null);assert.equal(edit.data.item.next_step_date,null);assert.equal(edit.data.item.company,'Acme');});
test('impossible dates and partial salary inversions are rejected without changes',async()=>{assert.equal((await api('/applications/'+id,'PUT',{applied_date:'2026-02-30'})).status,400);assert.equal((await api('/applications/'+id,'PUT',{salary_min:100,salary_max:200})).status,200);assert.equal((await api('/applications/'+id,'PUT',{salary_max:50})).status,400);assert.equal((await api('/applications/'+id)).data.item.salary_max,200);assert.equal((await api('/applications/1e2')).status,400);});
test('repeating the same transition is a no-op; another user cannot edit the record',async()=>{const before=(await api('/applications/'+id)).data.item;const result=await api(`/applications/${id}/transition`,'PATCH',{status:before.status});assert.equal(result.status,200);assert.equal(result.data.item.updated_at,before.updated_at);const other=await api('/auth/register','POST',{name:'Other',email:'other@example.com',password:'learning123'});const original=token;token=other.data.token;assert.equal((await api('/applications/'+id,'PUT',{company:'Stolen'})).status,404);token=original;assert.equal((await api('/applications/'+id,'DELETE')).status,204);});
''')
