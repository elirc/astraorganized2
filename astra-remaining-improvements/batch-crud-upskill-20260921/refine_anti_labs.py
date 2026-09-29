from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parent.parent;C=Path(__file__).resolve().parent
for id in ['40905c751e8c','859e461c9fd8','bcde1b4da8c5']:
 p=B/'stage'/id/'tests/helpers/load-typescript.mjs';shutil.copyfile(C/'test-tools/load-typescript.mjs',p)
P=B/'stage/40905c751e8c'
(P/'tests/onboarding-progress-runtime.test.mjs').write_text('''import test from 'node:test';import assert from 'node:assert/strict';import {fileURLToPath} from 'node:url';import {loadTypeScript} from './helpers/load-typescript.mjs';
const root=fileURLToPath(new URL('..',import.meta.url));
async function setup(statuses, current={status:'IN_PROGRESS',completedAt:null}){
 const calls=[];const db={onboardingTask:{findMany:async input=>{calls.push(['tasks',JSON.parse(JSON.stringify(input))]);return statuses.map(status=>({status}));}},onboardingCase:{findUnique:async input=>{calls.push(['case',JSON.parse(JSON.stringify(input))]);return current;},update:async input=>{calls.push(['update',input]);return input;}}};
 const mod=await loadTypeScript('backend/src/modules/onboardingCases/onboardingProgress.service.ts',{root,stubs:{'../../db/prisma':{prisma:db}}});return{mod,calls,db};
}
test('completed and skipped tasks contribute to rounded percentage with scoped queries',async()=>{
 const {mod,calls}=await setup(['COMPLETED','SKIPPED','IN_PROGRESS']);assert.equal(await mod.OnboardingProgressService.recalculateOnboardingProgress('case1'),67);
 assert.deepEqual(calls[0],['tasks',{where:{onboardingCaseId:'case1'}}]);assert.deepEqual(calls[1],['case',{where:{id:'case1'},select:{status:true,completedAt:true}}]);assert.deepEqual(JSON.parse(JSON.stringify(calls[2][1])),{where:{id:'case1'},data:{progressPercent:67}});
});
test('empty task set returns zero without reading or updating case',async()=>{
 const {mod,calls}=await setup([]);assert.equal(await mod.OnboardingProgressService.recalculateOnboardingProgress('empty'),0);assert.equal(calls.length,1);
});
test('all complete sets completion once and preserves existing timestamp',async()=>{
 let h=await setup(['COMPLETED','SKIPPED']);await h.mod.OnboardingProgressService.recalculateOnboardingProgress('case1');let data=h.calls[2][1].data;assert.equal(data.status,'COMPLETED');assert.ok(Number.isFinite(data.completedAt.getTime()));
 h=await setup(['SKIPPED'],{status:'COMPLETED',completedAt:new Date('2025-01-01')});await h.mod.OnboardingProgressService.recalculateOnboardingProgress('case1');data=h.calls[2][1].data;assert.equal(data.status,'COMPLETED');assert.equal(Object.hasOwn(data,'completedAt'),false);
});
test('reopening completed case changes status while leaving original timestamp omitted',async()=>{
 const {mod,calls}=await setup(['COMPLETED','IN_PROGRESS'],{status:'COMPLETED',completedAt:new Date('2025-01-01')});assert.equal(await mod.OnboardingProgressService.recalculateOnboardingProgress('case1'),50);assert.deepEqual(JSON.parse(JSON.stringify(calls[2][1].data)),{progressPercent:50,status:'IN_PROGRESS'});
});
test('explicit transaction client is used and late persistence failure propagates',async()=>{
 const {mod,calls}=await setup([]);const tx={onboardingTask:{findMany:async()=>[{status:'COMPLETED'}]},onboardingCase:{findUnique:async()=>({status:'IN_PROGRESS',completedAt:null}),update:async()=>{throw Error('write unavailable');}}};await assert.rejects(mod.OnboardingProgressService.recalculateOnboardingProgress('case1',tx),/write unavailable/);assert.equal(calls.length,0);
});
''',encoding='utf-8')
P=B/'stage/bcde1b4da8c5';t=P/'tests/products-service.test.mjs';s=t.read_text().replace('globals:{__prisma:prisma}',"stubs:{'../../db/prisma':{prisma}}")
s=s.replace("test('create checks SKU then writes the real product service',async()=>{existing=null;","test('create checks SKU then writes the real product service',async()=>{calls.length=0;existing=null;")
s=s.replace("assert.equal(calls.at(-1)[0],'create');","assert.deepEqual(JSON.parse(JSON.stringify(calls)),[['findUnique',{where:{sku:'SKU-1'}}],['create',{data:{sku:'SKU-1',name:'Scanner'}}]]);")
s+='''
test('read and update use exact record id and forward supplied fields',async()=>{
 existing={id:'p3',sku:'SKU-3'};calls.length=0;prisma.product.update=async args=>{calls.push(['update',args]);return{id:args.where.id,...args.data};};
 assert.equal((await m.ProductsService.getById('p3')).sku,'SKU-3');const out=await m.ProductsService.update('p3',{name:'Renamed'});assert.equal(out.name,'Renamed');assert.deepEqual(JSON.parse(JSON.stringify(calls.at(-1))),['update',{where:{id:'p3'},data:{name:'Renamed'}}]);
});
test('deactivate writes isActive false without a preliminary lookup',async()=>{
 calls.length=0;await m.ProductsService.deactivate('p3');assert.deepEqual(JSON.parse(JSON.stringify(calls)),[['update',{where:{id:'p3'},data:{isActive:false}}]]);
});
''';t.write_text(s,encoding='utf-8')
P=B/'stage/859e461c9fd8';t=P/'tests/permissions-errors.test.mjs';s=t.read_text();s+='''
test('requester own-read is distinct from broad read and agent cannot delete',()=>{
 assert.equal(m.hasPermission('REQUESTER','ticket:read:own'),true);assert.equal(m.hasPermission('REQUESTER','ticket:read'),false);assert.equal(m.hasPermission('AGENT','ticket:update'),true);assert.equal(m.hasPermission('AGENT','ticket:delete'),false);
});
test('permission strings are exact, while owner wildcard also allows unknown names',()=>{
 assert.equal(m.hasPermission('ADMIN','Ticket:read'),false);assert.equal(m.hasPermission('ADMIN','typo'),false);assert.equal(m.hasPermission('OWNER','typo'),true);
});
''';t.write_text(s,encoding='utf-8')
for id,source,testfile,summary in [
 ('40905c751e8c','backend/src/modules/onboardingCases/onboardingProgress.service.ts','tests/onboarding-progress-runtime.test.mjs','Five actual progress-service cases cover percentage rounding, empty tasks, completion, reopen, transaction selection and late write failure.'),
 ('859e461c9fd8','backend/src/shared/utils/permissions.ts','tests/permissions-errors.test.mjs','Five actual permission-policy cases cover wildcard, refusal, unknown roles, own-read versus broad-read and exact permission strings.'),
 ('bcde1b4da8c5','backend/src/modules/products/products.service.ts','tests/products-service.test.mjs','Five actual product-service cases cover create payload, duplicate and missing refusal, late failure, read/update and soft deactivation.')]:
 P=B/'stage'/id;rel='astraupskill/snapshots/'+Path(source).name+'.original.txt';target=P/rel;target.parent.mkdir(parents=True,exist_ok=True)
 base=json.loads((B/'baselines'/f'{id}.json').read_text());raw=(P/source).read_bytes();assert hashlib.sha256(raw).hexdigest()==base['files'][source];target.write_bytes(raw)
 p=B/'specs'/f'{id}.json';s=json.loads(p.read_text(encoding='utf-8-sig'));s['changedFiles']=[testfile,'tests/helpers/load-typescript.mjs',rel]
 # Preserve existing auxiliary tests in the manifest if agents already added them.
 if id!='859e461c9fd8':s['changedFiles'].append('tests/app-error.test.mjs')
 s['summary']=[summary,'Add nine source-grounded teaching chapters with predictions, worked fixtures, separate practice/solutions and evidence limits; no production behavior changed.']
 s['limits']=['Actual source runtime with explicitly injected persistence or enum adapters. No HTTP authentication, live database or concurrency proof.']
 p.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
