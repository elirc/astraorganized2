from pathlib import Path
import json
b=Path(__file__).resolve().parent.parent;p=b/'stage/5df5911fc343'
(p/'tests/runtime-ticket-boundary-lab.test.mjs').write_text('''import assert from 'node:assert/strict';
import test from 'node:test';
import {fileURLToPath} from 'node:url';
import {loadTypeScript} from './helpers/load-typescript.mjs';
const root=fileURLToPath(new URL('..',import.meta.url));
const context={session:{tenantId:'tenant-a',userId:'user-1'}};
async function fixture(options={}) {
  const calls=[],tx=Object.freeze({tx:true});
  const existing={id:'t1',tenantId:options.foreign?'tenant-b':'tenant-a',status:options.status||'OPEN'};
  const updated={id:'t1',tenantId:'tenant-a',status:'IN_PROGRESS'};
  const repo={findTicketById:async(id,tenant,client)=>{
    calls.push('find');assert.equal(id,'t1');assert.equal(tenant,'tenant-a');assert.equal(client,tx);
    return existing.tenantId===tenant?existing:null;
  },updateTicketStatusRecord:async(id,tenant,status,client)=>{
    calls.push('update');assert.equal(id,'t1');assert.equal(tenant,'tenant-a');assert.equal(status,'IN_PROGRESS');assert.equal(client,tx);
    return options.noUpdate?null:updated;
  },createTicketRecord:async()=>{},listTicketsByTenant:async()=>({}),listTicketSnapshotForTenant:async()=>[]};
  const effect=(name,client)=>{assert.equal(client,tx);calls.push(name);if(options.failAt===name)throw options.failure;};
  const service=await loadTypeScript('src/services/ticketService.ts',{root,stubs:{
    '@/db/client':{db:{transaction:async fn=>{calls.push('transaction');return fn(tx);}}},'@/db/schema':{},
    '@/lib/permissions/roles':{requirePermission:(actual,permission)=>{calls.push('permission');assert.equal(actual,context);assert.equal(permission,'ticket:update');if(options.deny)throw options.failure;}},
    '@/lib/search/document-builder':{buildTicketSearchDocument:t=>({sourceVersion:2,id:t.id})},
    '@/lib/validation/ticketSchemas':{createTicketSchema:{},ticketListSchema:{},updateTicketStatusSchema:{}},
    '@/repositories/ticketRepository':repo,
    '@/repositories/searchSyncEventRepository':{enqueueSearchSyncEvent:async(data,client)=>{
      assert.equal(data.tenantId,'tenant-a');assert.equal(data.entityId,'t1');assert.equal(data.sourceVersion,2);assert.equal(data.operation,'UPSERT');effect('sync',client);
    }},
    '@/repositories/tenantSearchStateRepository':{touchTenantSourceChange:async(tenant,client)=>{assert.equal(tenant,'tenant-a');effect('touch',client);}},
    '@/repositories/indexingJobRepository':{ensureQueuedIncrementalJob:async(tenant,user,types,client)=>{assert.equal(tenant,'tenant-a');assert.equal(user,'user-1');assert.equal(JSON.stringify(types),'["TICKET"]');effect('job',client);}},
    '@/repositories/auditLogRepository':{createAuditLog:async(data,client)=>{
      assert.equal(data.tenantId,'tenant-a');assert.equal(data.actorUserId,'user-1');assert.equal(data.metadata.previousStatus,'OPEN');assert.equal(data.metadata.nextStatus,'IN_PROGRESS');effect('audit',client);
    }}
  }});
  return {calls,updated,run:(nextStatus='IN_PROGRESS')=>service.updateTicketStatus(context,'t1',{nextStatus})};
}
test('foreign tenant fixture is refused through the scoped lookup without writes',async()=>{
  const f=await fixture({foreign:true});await assert.rejects(f.run(),e=>e.statusCode===404);assert.deepEqual(f.calls,['permission','transaction','find']);
});
test('real lifecycle rule rejects OPEN to RESOLVED before update',async()=>{
  const f=await fixture();await assert.rejects(f.run('RESOLVED'),e=>e.statusCode===409);assert.deepEqual(f.calls,['permission','transaction','find']);
});
test('repository empty result stops indexing and audit after update attempt',async()=>{
  const f=await fixture({noUpdate:true});await assert.rejects(f.run(),e=>e.statusCode===404);assert.deepEqual(f.calls,['permission','transaction','find','update']);
});
test('success carries tenant, actor and same transaction through every side effect',async()=>{
  const f=await fixture();assert.equal(await f.run(),f.updated);assert.deepEqual(f.calls,['permission','transaction','find','update','sync','touch','job','audit']);
});
test('permission refusal prevents transaction entry',async()=>{
  const failure=new Error('denied'),f=await fixture({deny:true,failure});await assert.rejects(f.run(),e=>e===failure);assert.deepEqual(f.calls,['permission']);
});
test('sync and audit failures preserve identity at their distinct stopping points',async()=>{
  for(const failAt of ['sync','audit']) {
    const failure=new Error(failAt),f=await fixture({failAt,failure});await assert.rejects(f.run(),e=>e===failure);
    const expected=['permission','transaction','find','update','sync'];if(failAt==='audit')expected.push('touch','job','audit');assert.deepEqual(f.calls,expected);
  }
});
''',encoding='utf-8')
f=b/'specs/5df5911fc343.json';s=json.loads(f.read_text(encoding='utf-8-sig'));s['summary']=['Preserve the reviewed ticket status production path and add a runnable six-case fault-injection teaching lab.','Exercise actual transition policy and error classes, scoped repository arguments, transaction-handle propagation, successful side-effect order and refusal/failure boundaries.'];s['changedFiles']=[n for n in s['changedFiles'] if not n.startswith('astraupskill/evidence/')];s['limits']=['No production source was changed. The lab executes actual ticket service, status policy and error classes with explicit permission, validation, document-builder, repository and transaction adapters.','Six runtime cases do not execute native Drizzle/PostgreSQL, HTTP, real authorization policy, indexing worker or transaction rollback. An empty update result is simulated, not proof of concurrent mutation safety.'];f.write_text(json.dumps(s,indent=2),encoding='utf-8')
