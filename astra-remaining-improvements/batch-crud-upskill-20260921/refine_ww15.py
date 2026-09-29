from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/678b11ff9b03'
(P/'tests/transaction-offer-policy.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import {loadTypeScript} from './helpers/load-typescript.mjs';
const {TransactionService}=await loadTypeScript('src/services/transaction-service.ts',{root:path.resolve('.')});
const buyer={user:{id:'buyer-1',role:'BUYER'}};
const input={amount:100,financingType:'CASH',expirationDate:'2030-01-01T00:00:00.000Z'};
function fixture({missing=false,fail=null,error=new Error('repository unavailable')}={}){
 const calls=[];const offer={id:'offer-1'};
 const aggregate={transaction:{id:'t1',buyerId:'buyer-1',agentId:'agent-1',sellerId:'seller-1',status:'INTAKE'},documents:[],commissionSplits:[],checklistItems:[]};
 const repo={findVisibleAggregateById:async(id,user)=>{calls.push(['get',id,user]);return missing?null:aggregate;},createOffer:async(id,data)=>{calls.push(['create',id,data]);if(fail==='create')throw error;return offer;},updateTransactionStatus:async(id,status)=>{calls.push(['status',id,status]);if(fail==='status')throw error;},createAuditEvent:async(...args)=>{calls.push(['audit',...args]);if(fail==='audit')throw error;}};
 return {calls,offer,error,submit:(actor=buyer)=>new TransactionService(repo).submitOffer(actor,'t1',input)};
}
test('assigned buyer submits exact payload and status/audit follow creation',async()=>{
 const f=fixture();assert.equal(await f.submit(),f.offer);assert.deepEqual(f.calls.map(x=>x[0]),['get','create','status','audit']);assert.equal(f.calls[0][2],buyer.user);
 assert.deepEqual(JSON.parse(JSON.stringify(f.calls[1])),['create','t1',{...input,submittedById:'buyer-1'}]);assert.deepEqual(f.calls[2],['status','t1','OFFER_SUBMITTED']);assert.deepEqual(JSON.parse(JSON.stringify(f.calls[3])),['audit','t1','buyer-1','offer.submitted',{amount:100}]);
});
test('real viewer and offer guards reject unassigned buyer, broker and assigned agent before writes',async()=>{
 for(const user of [{id:'other',role:'BUYER'},{id:'broker',role:'BROKER'},{id:'agent-1',role:'AGENT'}]){const f=fixture();await assert.rejects(()=>f.submit({user}),e=>e.statusCode===403&&e.code==='FORBIDDEN');assert.deepEqual(f.calls.map(x=>x[0]),['get']);}
});
test('creation, status and audit failures preserve identity and stop subsequent calls',async()=>{
 for(const [fail,expected] of [['create',['get','create']],['status',['get','create','status']],['audit',['get','create','status','audit']]]){const f=fixture({fail});await assert.rejects(()=>f.submit(),e=>e===f.error);assert.deepEqual(f.calls.map(x=>x[0]),expected);}
});
test('missing visible aggregate produces real not-found error without writes',async()=>{
 const f=fixture({missing:true});await assert.rejects(()=>f.submit(),e=>e.statusCode===404&&e.code==='NOT_FOUND');assert.deepEqual(f.calls.map(x=>x[0]),['get']);
});
''',encoding='utf-8')
sp=B/'specs/678b11ff9b03.json';spec=json.loads(sp.read_text(encoding='utf-8-sig'));spec['changedFiles']=[x for x in spec['changedFiles'] if x!='src/services/transaction-service.ts' and '/evidence/' not in x];spec['limits']=['Four actual-service cases load real viewer/offer guards, policy and error classes with only repository port adapters. No Next, native persistence, external provider or rollback execution.', 'createOffer is a repository operation, not an external provider call in this lab. Status/audit failure can follow earlier attempted writes; there is no service transaction wrapper. submitOffer does not call the workflow-transition validator used by updateStatus.'];sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
