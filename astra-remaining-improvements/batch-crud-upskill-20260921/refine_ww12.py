from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/5fd517cae993'
(P/'tests/runtime-conversation-update-count.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {loadTypeScript} from './helpers/load-typescript.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const session={userId:'agent-1',organizationId:'org-1',organizationRole:'AGENT'};
async function fixture({count=1,status='OPEN',missing=false,error=null}={}){
 const calls=[];const tx={id:'transaction'};const first=new Date('2026-01-01'),next=new Date('2026-01-02');
 const conversation={id:'conv-1',status,firstResponseDueAt:first,nextResponseDueAt:next};
 const {conversationService}=await loadTypeScript('src/services/conversationService.ts',{root,stubs:{
  'date-fns':{differenceInMinutes:()=>60},
  '@/lib/db':{prisma:{$transaction:async fn=>{calls.push(['tx']);return fn(tx);}}},
  '@/repositories/conversationRepository':{conversationRepository:{
   findById:async(org,id,client)=>{assert.equal(org,'org-1');assert.equal(id,'conv-1');assert.equal(client,tx);calls.push(['find']);return missing?null:conversation;},
   updateConversation:async(org,id,data,client)=>{assert.equal(org,'org-1');assert.equal(id,'conv-1');assert.equal(client,tx);calls.push(['update',data]);if(error)throw error;return {count};}
  }},
  '@/repositories/userRepository':{userRepository:{}},
  '@/repositories/auditRepository':{auditRepository:{create:async(data,client)=>{assert.equal(client,tx);calls.push(['audit',data]);}}}
 }});
 return {calls,first,next,transition:(target='PENDING',actor=session)=>conversationService.transitionConversationStatus(actor,{conversationId:'conv-1',status:target})};
}
test('zero-row status update returns real 404 before audit',async()=>{
 const f=await fixture({count:0});await assert.rejects(()=>f.transition(),e=>e.status===404&&e.code==='NOT_FOUND');assert.deepEqual(f.calls.map(x=>x[0]),['tx','find','update']);
});
test('successful pending transition preserves due dates and records scoped audit',async()=>{
 const f=await fixture();assert.equal((await f.transition()).success,true);assert.deepEqual(f.calls.map(x=>x[0]),['tx','find','update','audit']);
 assert.equal(f.calls[2][1].firstResponseDueAt,f.first);assert.equal(f.calls[2][1].nextResponseDueAt,f.next);
 assert.deepEqual(JSON.parse(JSON.stringify(f.calls[3][1])),{organizationId:'org-1',actorUserId:'agent-1',entityType:'conversation',entityId:'conv-1',action:'conversation.status_changed',details:{from:'OPEN',to:'PENDING'}});
});
test('resolved and closed transitions clear both SLA due dates',async()=>{
 for(const target of ['RESOLVED','CLOSED']){const f=await fixture();await f.transition(target);assert.equal(f.calls[2][1].status,target);assert.equal(f.calls[2][1].firstResponseDueAt,null);assert.equal(f.calls[2][1].nextResponseDueAt,null);}
});
test('real permission, missing row and illegal transition stop at their boundaries',async()=>{
 const denied=await fixture();await assert.rejects(()=>denied.transition('PENDING',{...session,organizationRole:'VIEWER'}),e=>e.status===403);assert.deepEqual(denied.calls,[]);
 const missing=await fixture({missing:true});await assert.rejects(()=>missing.transition(),e=>e.status===404);assert.deepEqual(missing.calls.map(x=>x[0]),['tx','find']);
 const closed=await fixture({status:'CLOSED'});await assert.rejects(()=>closed.transition('OPEN'),e=>e.status===400);assert.deepEqual(closed.calls.map(x=>x[0]),['tx','find']);
});
test('update failure preserves original error and skips audit',async()=>{
 const error=new Error('database unavailable');const f=await fixture({error});await assert.rejects(()=>f.transition(),e=>e===error);assert.deepEqual(f.calls.map(x=>x[0]),['tx','find','update']);
});
''',encoding='utf-8')
sp=B/'specs/5fd517cae993.json';spec=json.loads(sp.read_text(encoding='utf-8-sig'));spec['changedFiles']=[x for x in spec['changedFiles'] if '/evidence/' not in x]
spec['limits']=['Five runtime cases execute actual conversation service, permission policy and error helpers with transaction/repository/audit adapters. No native Prisma, HTTP, SQL or rollback execution.', 'The new count check detects a non-single-row update; repository write predicates do not compare the old status. It does not prevent stale-state transition races or prove concurrent safety.']
sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
