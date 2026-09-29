from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/cd5a8a522511'
(P/'tests/onboarding-task-ownership.test.mjs').write_text('''import test from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { loadTypeScript } from './helpers/load-typescript.mjs';
const root=fileURLToPath(new URL('..',import.meta.url));
const actor={userId:'employee',role:'EMPLOYEE'};
async function setup({ownerRole='EMPLOYEE',userId='employee',status='NOT_STARTED',remaining=false,missing=false,failAudit=false}={}){
 const calls=[];
 const task={id:'task',title:'Sign packet',ownerRole,status,employeeProfile:{id:'profile',userId,stage:'PREBOARDING',onboardingTasks:[{requiredForStage:'PREBOARDING',status:remaining?'NOT_STARTED':'COMPLETED'}]}};
 const mod=await loadTypeScript('src/services/onboardingService.ts',{root,stubs:{
 'bcryptjs':{default:{hash:()=>{throw Error('unexpected hash');}}},
 '@/repositories/onboardingRepository':{onboardingRepository:{findTaskById:async id=>{calls.push(['find',id]);return missing?null:task;},updateTaskStatus:async input=>{calls.push(['write',JSON.parse(JSON.stringify(input))]);return {...task,status:input.nextStatus};},updateEmployeeStage:async(...args)=>calls.push(['stage',...args])}},
 '@/repositories/auditLogRepository':{auditLogRepository:{create:async input=>{calls.push(['audit',JSON.parse(JSON.stringify(input))]);if(failAudit)throw Error('audit unavailable');}}},
 '@/repositories/jobRepository':{jobRepository:{enqueue:async(...args)=>calls.push(['job',...args])}}
 }});return {mod,calls};
}
test('owned employee task completes and actual stage rule advances with exact audit',async()=>{
 const {mod,calls}=await setup();const result=await mod.onboardingService.completeTask(actor,'task','COMPLETED');
 assert.equal(result.nextStage,'ORIENTATION');assert.deepEqual(calls,[['find','task'],['write',{taskId:'task',nextStatus:'COMPLETED'}],['stage','profile','ORIENTATION'],['audit',{actorUserId:'employee',action:'onboardingTask.status_changed',entityType:'OnboardingTask',entityId:'task',summary:'Moved task to COMPLETED.'}]]);
});
test('foreign profile and HR or IT assignment refuse before any mutation',async()=>{
 for(const input of [{userId:'foreign'},{ownerRole:'HR_MANAGER'},{ownerRole:'IT_SUPPORT'}]){
 const {mod,calls}=await setup(input);await assert.rejects(mod.onboardingService.completeTask(actor,'task','COMPLETED'),e=>e.statusCode===403&&e.code==='FORBIDDEN');assert.deepEqual(calls,[['find','task']]);}
});
test('real capability policy refuses billing role before lookup',async()=>{
 const {mod,calls}=await setup();await assert.rejects(mod.onboardingService.completeTask({...actor,role:'BILLING_ANALYST'},'task','COMPLETED'),e=>e.statusCode===403);assert.equal(calls.length,0);
});
test('missing task and illegal repeat completion use real404 and409 errors',async()=>{
 for(const [input,code] of [[{missing:true},404],[{status:'COMPLETED'},409]]){const {mod,calls}=await setup(input);await assert.rejects(mod.onboardingService.completeTask(actor,'task','COMPLETED'),e=>e.statusCode===code);assert.deepEqual(calls,[['find','task']]);}
});
test('remaining required work keeps stage and audit failure propagates after task write',async()=>{
 const {mod,calls}=await setup({remaining:true,failAudit:true});await assert.rejects(mod.onboardingService.completeTask(actor,'task','COMPLETED'),/audit unavailable/);assert.deepEqual(calls.map(c=>c[0]),['find','write','audit']);
});
''',encoding='utf-8')
for p in (P/'astraupskill').glob('*.md'):
 s=p.read_text(encoding='utf-8-sig')
 s=s.replace('persistence, transitions, auditing, jobs, and permissions','persistence, auditing and jobs; real permissions, transitions and errors execute')
 s=s.replace('permission, repository, transition, audit, and job collaborators','repository, audit and job collaborators')
 s=s.replace('stubs only external collaborators','loads the real pure permission, transition and error modules with external I/O adapters')
 s=s.replace('have `deriveNextOnboardingStage` return ORIENTATION','let the real `deriveNextOnboardingStage` compute ORIENTATION')
 s=s.replace('reports three passing subtests','reports five passing subtests').replace('checks/cd5a8a522511/runtime-b072.log','astraupskill/evidence/crud-b07-astra-runtime.log')
 s=s.replace('HR managers and IT support retain the existing capability path and can still operate their assigned work.','HR managers and IT support retain the existing broader capability path; this change does not restrict their rows by ownerRole.')
 s+='\nReview extension: five cases execute real policy, state transitions and typed errors. They assert no mutation for employee profile/HR/IT mismatch, no lookup for billing role,404 for missing,409 for completed repeat, actual stage advancement and late audit failure. No encompassing service transaction or rollback guarantee is asserted.\n'
 p.write_text(s,encoding='utf-8')
p=B/'specs/cd5a8a522511.json';s=json.loads(p.read_text(encoding='utf-8-sig'));s['changedFiles']=[x for x in s['changedFiles'] if '/evidence/' not in x]
s['summary'][1]='Five actual-service cases execute real permission, transition and error modules, including no-write refusals, stage advance and audit failure.'
s['limits']=['Persistence, audit and job adapters; no Next, Prisma, database isolation or rollback execution.','Employee ownerRole restriction only; HR/IT broader existing capability behavior unchanged. No enclosing service transaction.']
p.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
