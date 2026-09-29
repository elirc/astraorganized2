from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/1d0b328c6621'
(P/'tests/runtime-protocol-activation.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {loadTypeScript} from './helpers/load-typescript.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
async function fixture(auditFailure=null){
 const state={protocolVersions:[{id:'draft',protocolCode:'P',versionNumber:2,status:'DRAFT',visitTemplates:[]},{id:'active',protocolCode:'P',versionNumber:1,status:'ACTIVE',visitTemplates:[]},{id:'retired',protocolCode:'P',versionNumber:0,status:'RETIRED',visitTemplates:[]},{id:'other',protocolCode:'OTHER',versionNumber:1,status:'ACTIVE',visitTemplates:[]}],participants:[{id:'participant',protocolVersionId:'active'}]};
 const audits=[];
 const {protocolService}=await loadTypeScript('src/services/protocolService.ts',{root,stubs:{
  '@/lib/mock-db/store':{getMockDb:()=>state},'@/lib/mock-db/ids':{nextId:()=> 'unused'},
  '@/services/auditService':{auditService:{record:async record=>{audits.push(record);if(auditFailure)throw auditFailure;}}}
 }});
 return {state,audits,activate:id=>protocolService.activateProtocolVersion({user:{id:'u1'}},id)};
}
test('ACTIVE and RETIRED refuse before real repository mutation or audit',async()=>{
 for(const id of ['active','retired']){const f=await fixture();const before=JSON.stringify(f.state);await assert.rejects(()=>f.activate(id),/Only draft/);assert.equal(JSON.stringify(f.state),before);assert.equal(f.audits.length,0);}
});
test('draft activation retires same-code sibling, preserves other protocol and participant pins, and audits exact actor',async()=>{
 const f=await fixture();const other=f.state.protocolVersions[3];const participant=f.state.participants[0];const result=await f.activate('draft');
 assert.equal(result.status,'ACTIVE');assert.equal(result.id,'draft');assert.equal(f.state.protocolVersions.find(x=>x.id==='active').status,'RETIRED');assert.equal(f.state.protocolVersions.find(x=>x.id==='other'),other);assert.equal(f.state.participants[0],participant);assert.equal(participant.protocolVersionId,'active');
 assert.deepEqual(JSON.parse(JSON.stringify(f.audits)),[{entityType:'protocolVersion',entityId:'draft',action:'PROTOCOL_VERSION_ACTIVATED',actorUserId:'u1',participantId:null,metadataJson:{protocolCode:'P',versionNumber:2}}]);
});
test('missing target leaves populated state and audit unchanged',async()=>{
 const f=await fixture();const before=JSON.stringify(f.state);await assert.rejects(()=>f.activate('missing'),/not found/);assert.equal(JSON.stringify(f.state),before);assert.equal(f.audits.length,0);
});
test('audit error propagates after existing nontransactional repository mutation',async()=>{
 const error=new Error('audit unavailable');const f=await fixture(error);await assert.rejects(()=>f.activate('draft'),e=>e===error);assert.equal(f.state.protocolVersions.find(x=>x.id==='draft').status,'ACTIVE');assert.equal(f.state.protocolVersions.find(x=>x.id==='active').status,'RETIRED');assert.equal(f.audits.length,1);
});
''',encoding='utf-8')
sp=B/'specs/1d0b328c6621.json';spec=json.loads(sp.read_text(encoding='utf-8-sig'))
spec['changedFiles']=[x for x in spec['changedFiles'] if '/evidence/' not in x]
spec['limits']=['Four runtime cases execute actual protocol service, rules and repository with only mock-state, id and audit adapters. Same-code retirement, unrelated protocol preservation and unchanged participant pins are observed in fixture state.', 'No route auth, native application, concurrent activation or durable audit was executed. The real repository mutates state before audit; audit failure leaves activation applied. No rollback guarantee is added.']
sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
