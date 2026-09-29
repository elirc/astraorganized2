from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/671a350f0386'
(P/'tests/runtime-workflow-same-status.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import {loadTypeScript} from './helpers/load-typescript.mjs';
const enums={WorkflowStatus:Object.fromEntries(['DRAFT','ACTIVE','PAUSED','ARCHIVED'].map(x=>[x,x])),WorkflowTriggerType:{EVENT:'EVENT',SCHEDULE:'SCHEDULE',MANUAL:'MANUAL'},UserRole:{ADMIN:'ADMIN',OPERATOR:'OPERATOR',ANALYST:'ANALYST'},WorkflowDefinition:{}};
async function fixture({status='ACTIVE',missing=false,fail=null}={}){
 const calls=[];const error=new Error('persistence unavailable');
 const workflow={id:'wf-1',status,name:'Ops',description:null,triggerType:'MANUAL',eventName:null,cronExpression:null,createdByUserId:'u-1',steps:[]};
 const {workflowDefinitionService}=await loadTypeScript('src/services/workflow-definition-service.ts',{root:path.resolve('.'),stubs:{
  'server-only':{},'@prisma/client':enums,
  '@/lib/workflow/schedule':{getNextScheduledAt:()=>{calls.push(['schedule']);return null;}},
  '@/repositories/workflow-repository':{workflowRepository:{findById:async(id,scope)=>{calls.push(['find',id,scope]);return missing?null:workflow;},updateStatus:async(...args)=>{calls.push(['update',...args]);if(fail==='update')throw error;return {...workflow,status:args[2]};}}},
  '@/repositories/workflow-run-repository':{workflowRunRepository:{createAuditEvent:async data=>{calls.push(['audit',JSON.parse(JSON.stringify(data))]);if(fail==='audit')throw error;}}}
 }});
 return {calls,workflow,error,run:(next='ACTIVE',actor={userId:'u-1',role:'OPERATOR'})=>workflowDefinitionService.transitionWorkflowStatus(actor,'wf-1',next)};
}
test('each equal-status request returns existing authorized record without write, audit or schedule',async()=>{
 for(const status of ['DRAFT','ACTIVE','PAUSED','ARCHIVED']){const f=await fixture({status});assert.equal(await f.run(status),f.workflow);assert.deepEqual(f.calls,[['find','wf-1','all']]);}
});
test('foreign operator cannot use same-status shortcut and missing record stays404',async()=>{
 const f=await fixture();await assert.rejects(f.run('ACTIVE',{userId:'other',role:'OPERATOR'}),e=>e.statusCode===403&&e.code==='WORKFLOW_SCOPE_VIOLATION');assert.equal(f.calls.length,1);
 const missing=await fixture({missing:true});await assert.rejects(missing.run(),e=>e.statusCode===404);assert.equal(missing.calls.length,1);
});
test('valid changed status persists exact arguments and audit metadata',async()=>{
 const f=await fixture();assert.equal((await f.run('PAUSED')).status,'PAUSED');
 assert.deepEqual(f.calls[1],['update','wf-1','u-1','PAUSED',null]);
 assert.deepEqual(f.calls[2][1].metadata,{previousStatus:'ACTIVE',nextStatus:'PAUSED'});assert.equal(f.calls[2][1].kind,'workflow.status.changed');
});
test('invalid changed edge fails with real conflict before persistence',async()=>{
 const f=await fixture();await assert.rejects(f.run('DRAFT'),e=>e.statusCode===409&&e.code==='INVALID_WORKFLOW_TRANSITION');assert.equal(f.calls.length,1);
});
test('new activation still checks readiness although active no-op does not revalidate',async()=>{
 const f=await fixture({status:'DRAFT'});await assert.rejects(f.run('ACTIVE'),e=>e.statusCode===422&&e.code==='WORKFLOW_STEP_REQUIRED');assert.equal(f.calls.length,1);
});
test('update error prevents audit and audit error follows attempted update',async()=>{
 for(const fail of ['update','audit']){const f=await fixture({fail});await assert.rejects(f.run('PAUSED'),e=>e===f.error);assert.deepEqual(f.calls.map(x=>x[0]),fail==='update'?['find','update']:['find','update','audit']);}
});
''')
s=B/'specs/671a350f0386.json';d=json.loads(s.read_text(encoding='utf-8-sig'));d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')];d['limits']=['Six cases execute actual service, ownership helper, status/readiness policy and AppError with repository/schedule and generated-enum adapters. No HTTP route, live Prisma, cron parsing or concurrency run.','Equal-status calls retain ownership checks but skip activation-readiness and schedule recalculation. Coarse route permission enforcement is outside this lab. Status update and audit have no enclosing service transaction.'];s.write_text(json.dumps(d,indent=2))
