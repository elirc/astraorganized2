from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/829e8e7b8605'
(P/'tests/message-post-runtime.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import {loadTypeScript} from './helpers/load-typescript.mjs';
const self='c'+'a'.repeat(24),peer='c'+'b'.repeat(24),outsider='c'+'c'.repeat(24);
const plain=x=>JSON.parse(JSON.stringify(x));
async function fixture({visibility='PUBLIC',parent=null,fail=null}={}){
 const calls=[];const tx={};const error=new Error('injected failure');const context={workspaceId:'w',membershipId:self,role:'MEMBER'};
 const record=(name,data,client)=>{assert.equal(client,tx);calls.push([name,plain(data)]);if(fail===name)throw error;};
 const {messageService}=await loadTypeScript('src/services/messageService.ts',{root:path.resolve('.'),stubs:{
  '@/lib/db':{db:{$transaction:async fn=>{calls.push(['tx']);const result=await fn(tx);calls.push(['tx-done']);return result;}}},
  '@/lib/realtime/realtimeBus':{publishWorkspaceRealtimeEvent:data=>calls.push(['publish',plain(data)])},
  '@/services/channelService':{channelService:{requireChannelAccess:async(c,id)=>{calls.push(['channel',id]);if(fail==='channel')throw error;return {id:'ch1',visibility,workspaceId:'w'};}}},
  '@/repositories/messageRepository':{messageRepository:{findById:async(data,client)=>{record('parent',data,client);return parent;},incrementThreadReplyCount:async(data,client)=>record('increment',data,client),createMessage:async(data,client)=>{record('create',data,client);return {id:'m1',...data};}}},
  '@/repositories/workspaceRepository':{workspaceRepository:{listWorkspaceMembers:async(id,client)=>{record('members',{id},client);return [{id:self,userId:'u1',role:'MEMBER'},{id:peer,userId:'u2',role:'MEMBER'},{id:outsider,userId:'u3',role:'MEMBER'}];}}},
  '@/repositories/channelRepository':{channelRepository:{findById:async(data,client)=>{record('private',data,client);return {memberships:[{userId:'u1'},{userId:'u2'}]};}}},
  '@/repositories/notificationRepository':{notificationRepository:{createMany:async(data,client)=>record('notify',data,client)}},
  '@/repositories/syncRepository':{syncRepository:{appendEvent:async(data,client)=>{record('sync',data,client);return {id:7,...data};}}},
  '@/repositories/auditRepository':{auditRepository:{write:async(data,client)=>record('audit',data,client)}},
  '@/repositories/attachmentRepository':{attachmentRepository:{findPendingByIds:async(data,client)=>{record('pending',data,client);return [{id:'owned'}];},attachToMessage:async(data,client)=>record('attach',data,client)}}
 }});
 return {calls,error,run:(input={},role='MEMBER')=>messageService.postChannelMessage({...context,role},{channelId:'ch1',content:' Hello ',attachmentIds:[],...input})};
}
test('member payload is normalized and realtime publishes only after transaction result',async()=>{
 const f=await fixture();const result=await f.run();assert.equal(result.id,'m1');
 assert.deepEqual(f.calls.map(x=>x[0]),['channel','tx','create','members','notify','sync','audit','tx-done','publish']);
 const data=f.calls[2][1];assert.deepEqual(data,{workspaceId:'w',authorMembershipId:self,channelId:'ch1',content:'Hello',normalizedContent:'hello'});
 assert.equal(f.calls.at(-1)[1].cursor,7);assert.equal(f.calls.at(-1)[1].entityId,'m1');
});
test('real guest policy and rejected access stop before transaction',async()=>{
 const guest=await fixture();await assert.rejects(guest.run({},'GUEST'),e=>e.status===403);assert.deepEqual(guest.calls,[]);
 const denied=await fixture({fail:'channel'});await assert.rejects(denied.run(),e=>e===denied.error);assert.deepEqual(denied.calls,[['channel','ch1']]);
});
test('missing, foreign-channel and nested thread parents refuse before creation',async()=>{
 for(const [parent,status] of [[null,404],[{id:'p1',channelId:'other'},404],[{id:'p1',channelId:'ch1',parentMessageId:'root'},409]]){
  const f=await fixture({parent});await assert.rejects(f.run({parentMessageId:'p1'}),e=>e.status===status);assert.deepEqual(f.calls.map(x=>x[0]),['channel','tx','parent']);
 }
});
test('private thread mention deduplicates self and excludes invisible recipients',async()=>{
 const f=await fixture({visibility:'PRIVATE',parent:{id:'p1',channelId:'ch1',parentMessageId:null,authorMembershipId:peer}});
 await f.run({parentMessageId:'p1',content:`@[${peer}] @[${peer}] @[${self}] @[${outsider}]`});
 assert.deepEqual(f.calls.find(x=>x[0]==='notify')[1].notifications,[{recipientMembershipId:peer,type:'MENTION'}]);
 assert.equal(f.calls.filter(x=>x[0]==='increment').length,1);
});
test('attachments query is owner-scoped and only returned pending ids attach',async()=>{
 const f=await fixture();await f.run({attachmentIds:['owned','foreign']});
 assert.deepEqual(f.calls.find(x=>x[0]==='pending')[1],{workspaceId:'w',attachmentIds:['owned','foreign'],uploadedByMembershipId:self});
 assert.deepEqual(f.calls.find(x=>x[0]==='attach')[1].attachmentIds,['owned']);
});
test('audit failure propagates without completing transaction or publishing',async()=>{
 const f=await fixture({fail:'audit'});await assert.rejects(f.run(),e=>e===f.error);
 assert.equal(f.calls.at(-1)[0],'audit');assert.equal(f.calls.some(x=>x[0]==='publish'||x[0]==='tx-done'),false);
});
''')
s=B/'specs/829e8e7b8605.json';d=json.loads(s.read_text(encoding='utf-8-sig'));d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')];d['limits']=['Six actual message-service cases load real role policy and errors, with channel-access, repository, transaction and realtime adapters. No Next, Prisma rollback/isolation or network delivery execution.','Private notification filtering and attachment query arguments execute in the service; the adapters do not prove repository scoping or live transport confidentiality. Publishing follows the transaction response; persisted event does not prove delivery.'];s.write_text(json.dumps(d,indent=2))
