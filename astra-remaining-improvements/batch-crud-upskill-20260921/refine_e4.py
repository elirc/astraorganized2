from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/1cf37faa32e8'
(P/'tests/runtime-newsletter-state.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadTypeScript } from './helpers/load-typescript.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
async function harness(status='draft',failure=null) {
 const data={newsletters:[{id:'news-1',status,recipients:0,deliveries:{queued:0}}],subscribers:[{id:'s1',email:' A@example.test '},{id:'s2',email:'b@example.test'}]};
 const calls={jobs:[],audits:[]};
 const mod=await loadTypeScript('src/server/newsletters/service.ts',{root,aliasRoot:path.join(root,'src'),stubs:{
  '@/lib/db':{prisma:{}},'@/lib/env':{isDatabaseConfigured:false},'@/server/auth/service':{},
  '@/server/audit/service':{recordAuditLog:async a=>{calls.audits.push(a);}},
  '@/server/dev-store':{devStore:data},
  '@/server/queues':{queueNewsletterDeliveryJob:async j=>{calls.jobs.push(j);if(failure)throw failure;}}
 }});
 return {data,calls,queue:()=>mod.queueNewsletter('news-1',{userId:'actor-1'})};
}
test('draft queues exact recipient payloads with actual normalized dedupe keys and audit',async()=>{
 const h=await harness();assert.equal(await h.queue(),h.data.newsletters[0]);
 assert.equal(h.data.newsletters[0].status,'queued');assert.equal(h.data.newsletters[0].recipients,2);assert.equal(h.data.newsletters[0].deliveries.queued,2);
 assert.deepEqual(JSON.parse(JSON.stringify(h.calls.jobs)),[{newsletterId:'news-1',recipientId:'s1',dedupeKey:'news-1:a@example.test',email:' A@example.test '},{newsletterId:'news-1',recipientId:'s2',dedupeKey:'news-1:b@example.test',email:'b@example.test'}]);
 assert.deepEqual(JSON.parse(JSON.stringify(h.calls.audits)),[{actorId:'actor-1',action:'newsletter.queued',resourceType:'newsletter',resourceId:'news-1'}]);
 await assert.rejects(h.queue,/Only draft newsletters/);assert.equal(h.calls.jobs.length,2);assert.equal(h.calls.audits.length,1);
});
test('non-draft matrix rejects before state change, jobs or audit',async()=>{
 for(const status of ['queued','sent','failed']) {const h=await harness(status);const before=JSON.stringify(h.data);await assert.rejects(h.queue,/Only draft newsletters/);assert.equal(JSON.stringify(h.data),before);assert.deepEqual(h.calls,{jobs:[],audits:[]});}
});
test('missing newsletter rejects without side effects',async()=>{
 const h=await harness();h.data.newsletters=[];await assert.rejects(h.queue,/Newsletter not found/);assert.deepEqual(h.calls,{jobs:[],audits:[]});
});
test('queue failure propagates and exposes existing queued-before-await recovery limitation',async()=>{
 const error=new Error('queue unavailable');const h=await harness('draft',error);
 await assert.rejects(h.queue,e=>e===error);assert.equal(h.data.newsletters[0].status,'queued');assert.equal(h.calls.jobs.length,2);assert.equal(h.calls.audits.length,0);
 await assert.rejects(h.queue,/Only draft newsletters/);assert.equal(h.calls.jobs.length,2);
});
''',encoding='utf-8')
sp=B/'specs/1cf37faa32e8.json';spec=json.loads(sp.read_text(encoding='utf-8-sig'))
spec['changedFiles']=[x for x in spec['changedFiles'] if '/evidence/' not in x]
spec['limits']=['Four actual-service runtime cases load the real dedupe-key helper with explicit dev store, queue, audit, database and environment adapters. No native Prisma, Redis, HTTP or worker execution.', 'The development branch changes status before awaiting queued jobs. A queue failure leaves queued state and prevents retry through this function; recovery/outbox redesign is not included. No durable delivery, atomicity or concurrency guarantee is claimed.']
sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
