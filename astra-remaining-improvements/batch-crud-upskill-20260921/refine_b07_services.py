from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
# Preserve the original cases while replacing invented pure error/permission behavior.
P=B/'stage/482e93488b83';t=P/'tests/registration-session-selection.test.mjs'
s=t.read_text();s=s.replace("const AppError = class AppError extends Error { constructor(message, statusCode=400) { super(message); this.statusCode=statusCode; } };",'')
s=s.replace("new Date('2026-01-01')","new Date('2000-01-01')").replace("new Date('2026-12-31')","new Date('2100-01-01')")
s=s.replace("    '@/modules/shared/http': { AppError },","    'next/server': { NextResponse: {} }, 'zod': { z: {} },")
s=s.replace("    '@/modules/auth/permissions': { assertPermission: ()=>{} },",'')
s+='''
test('duplicate selections produce one reservation and forbidden role cannot mutate', async()=>{
 const d=deps(); const service=serviceModule.createRegistrationService(d);
 await service.createRegistration(actor,{eventId:'e1',sessionIds:['s1','s1']});
 assert.deepEqual(JSON.parse(JSON.stringify(d.calls.create[0].sessionSelections)),[{sessionId:'s1',status:'RESERVED'}]);
 assert.equal(d.calls.create[0].attendeeId,'u1');assert.equal(d.calls.create[0].eventId,'e1');
 const denied=deps();await assert.rejects(serviceModule.createRegistrationService(denied).createRegistration({...actor,role:'SPEAKER'},{eventId:'e1',sessionIds:['s1']}),e=>e.statusCode===403);assert.equal(denied.calls.create.length,0);
});
test('notification failure rejects after registration persistence and prevents audit',async()=>{
 const d=deps();d.repository.enqueueNotification=async()=>{throw Error('queue unavailable');};
 await assert.rejects(serviceModule.createRegistrationService(d).createRegistration(actor,{eventId:'e1',sessionIds:['s1']}),/queue unavailable/);
 assert.equal(d.calls.create.length,1);assert.equal(d.calls.audit.length,0);
});
''';t.write_text(s,encoding='utf-8')
for p in (P/'astraupskill').glob('*.md'):
 s=p.read_text(encoding='utf-8-sig').replace('three tests','five tests').replace('Three tests','Five tests').replace('three executable','five executable')
 s=s.replace('permission,','').replace('permission and','').replace('shared HTTP error constructors','NextResponse and zod imports (unused by the tested path)')
 s+='\nRuntime review addition: the real AppError and permission policy now execute. Duplicate session IDs produce one reservation; a SPEAKER is refused403. Notification failure follows the create adapter call and prevents audit; no enclosing service transaction is claimed.\n'
 p.write_text(s,encoding='utf-8')
# Deal service: real domain errors and additional independently asserted contracts.
P=B/'stage/5f8d9a364788';t=P/'tests/deal-stage-update-result.test.mjs';s=t.read_text()
s='\n'.join(l for l in s.splitlines() if not l.startswith('const errors='))
s=s.replace("'@/lib/http/errors':errors,",'')
s+='''
test('pipeline mismatch refuses before update, history and audit',async()=>{
 let writes=0;repo.update=async()=>{writes++;return {id:'d1'};};
 pipeline.requireStage=async()=>({id:'other',pipelineId:'p2',isClosed:false,isWon:false});
 await assert.rejects(m.dealService.moveDealStage(ctx,'d1',{stageId:'other'}),e=>e.status===409&&e.code==='stage_pipeline_mismatch');assert.equal(writes,0);
});
test('closed won stage derives status and close timestamp with shared transaction and scoped context',async()=>{
 pipeline.requireStage=async(context,client)=>{assert.equal(context,ctx);assert.equal(client,prisma);return {id:'won',pipelineId:'p1',isClosed:true,isWon:true,name:'Won'};};
 let payload,history,auditInput;
 repo.update=async(context,client,id,input)=>{assert.equal(context,ctx);assert.equal(client,prisma);assert.equal(id,'d1');payload=input;return {id:'d1',...input};};
 repo.createStageHistory=async(context,client,input)=>{assert.equal(context,ctx);assert.equal(client,prisma);history=input;};
 audit.logOrgEvent=async(context,client,input)=>{assert.equal(context,ctx);assert.equal(client,prisma);auditInput=input;};
 await m.dealService.moveDealStage(ctx,'d1',{stageId:'won',note:'signed'});
 assert.equal(payload.status,'WON');assert.equal(payload.stageId,'won');assert.ok(Number.isFinite(payload.closedAt.getTime()));
 assert.deepEqual(JSON.parse(JSON.stringify(history)),{dealId:'d1',fromStageId:'old',toStageId:'won',changedByMembershipId:'m1',note:'signed'});assert.equal(auditInput.action,'deal.stage.moved');
});
''';t.write_text(s+'\n',encoding='utf-8')
for p in (P/'astraupskill').glob('*.md'):
 s=p.read_text(encoding='utf-8-sig').replace('two tests','four tests').replace('Two tests','Four tests')
 s=s.replace('and the shared HTTP error constructors','while loading the real shared HTTP error constructors').replace('production-style status and code fields from error doubles','the real domain errors with status and code fields')
 s=s.replace('service?s',"service's").replace('repository?s',"repository's").replace('test?s',"test's").replace('?should not write?','"should not write"')
 s+='\nAdditional runtime coverage refuses a foreign-pipeline stage and checks WON status, close timestamp, exact history payload, and shared transaction/context arguments. Persistence remains adapted; these are service contract assertions.\n'
 p.write_text(s,encoding='utf-8')
for id in ['482e93488b83','5f8d9a364788']:
 p=B/'specs'/f'{id}.json';s=json.loads(p.read_text(encoding='utf-8-sig'));s['changedFiles']=[x for x in s['changedFiles'] if '/evidence/' not in x]
 if id=='482e93488b83':
  s['summary'][1]='Executes five actual-service cases with real permission and AppError code.'
  s['limits']=['Persistence, audit and DB singleton adapted; NextResponse and zod exports unused by tested path are stubs.','No database concurrency or notification delivery proof. Duplicate IDs allowed and deduplicated. Notification failure can follow persistence.']
 else:
  s['summary'][1]='Four actual-service cases use real errors for null reread, ordinary success, pipeline refusal and won-stage payload.'
 p.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
