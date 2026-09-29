from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/7a06d436fe48'
(P/'tests/job-posting-service-runtime.test.mjs').write_text('''import test from 'node:test';import assert from 'node:assert/strict';import path from 'node:path';import {loadTypeScript} from './helpers/load-typescript.mjs';
const actor={id:'reviewer-1',role:'MODERATOR',organizationId:'org-1'};
const {createJobPostingService}=await loadTypeScript('src/services/jobPostingService.ts',{root:path.resolve('.'),stubs:{'@/repositories/jobPostingRepository':{jobPostingRepository:{}},'@/repositories/auditLogRepository':{auditLogRepository:{}}}});
function fixture({status='FLAGGED',missing=false,fail=null}={}){
 const calls=[];const error=new Error('write unavailable');
 const record=(name,data)=>{calls.push([name,JSON.parse(JSON.stringify(data))]);if(fail===name)throw error;};
 const repository={createSubmittedJobPosting:async data=>{record('create',data);return {id:'job-1',status:'SUBMITTED',...data};},findById:async id=>{record('find',{id});return missing?null:{id,status};},findByIdForOrganization:async(id,org)=>{record('scoped',{id,org});return missing?null:{id};},updateReview:async data=>{record('review',data);return data;}};
 return {calls,error,service:createJobPostingService({jobPostingRepository:repository,auditLogRepository:{create:async data=>record('audit',data)}})};
}
test('submission derives organization and actor fields then audits created id',async()=>{
 const f=fixture();const input={title:'QA',description:'Test',location:'Remote',employmentType:'FULL_TIME',salaryMin:1,salaryMax:2,organizationId:'untrusted'};
 const result=await f.service.submitEmployerJobPosting(input,actor);assert.equal(result.organizationId,'org-1');assert.equal(result.submittedById,'reviewer-1');assert.deepEqual(f.calls.map(x=>x[0]),['create','audit']);assert.equal(f.calls[1][1].action,'JOB_POSTING_SUBMITTED');assert.equal(f.calls[1][1].entityId,'job-1');
});
test('both reviewable states allow approve and reject with exact review/audit data',async()=>{
 for(const status of ['SUBMITTED','FLAGGED'])for(const decision of ['approve','reject']){const f=fixture({status});const result=decision==='approve'?await f.service.approveJobPosting('job-1',actor):await f.service.rejectJobPosting('job-1','Missing details',actor);
  assert.deepEqual(result,{id:'job-1',status:decision==='approve'?'APPROVED':'REJECTED',reviewedById:'reviewer-1',rejectionReason:decision==='approve'?null:'Missing details'});
  assert.deepEqual(f.calls.map(x=>x[0]),['find','review','audit']);assert.equal(f.calls[2][1].metadata.previousStatus,status);
 }
});
test('missing and nonreviewable states reject both decisions before writes',async()=>{
 for(const [opts,code] of [[{missing:true},404],[{status:'APPROVED'},409],[{status:'REJECTED'},409]])for(const method of ['approveJobPosting','rejectJobPosting']){const f=fixture(opts);await assert.rejects(method==='approveJobPosting'?f.service[method]('job-1',actor):f.service[method]('job-1','reason',actor),e=>e.status===code);assert.deepEqual(f.calls.map(x=>x[0]),['find']);}
});
test('employer detail forwards organization scope and preserves not-found',async()=>{
 const f=fixture({missing:true});await assert.rejects(f.service.getEmployerJobPosting('job-1','org-2'),e=>e.status===404);assert.deepEqual(f.calls,[['scoped',{id:'job-1',org:'org-2'}]]);
});
test('review failure prevents audit while audit failure follows attempted review',async()=>{
 for(const fail of ['review','audit']){const f=fixture({fail});await assert.rejects(f.service.approveJobPosting('job-1',actor),e=>e===f.error);assert.deepEqual(f.calls.map(x=>x[0]),fail==='review'?['find','review']:['find','review','audit']);}
});
''')
s=B/'specs/7a06d436fe48.json';d=json.loads(s.read_text(encoding='utf-8-sig'));d['changedFiles']=[n for n in d['changedFiles'] if not n.startswith('astraupskill/evidence/')];d['limits']=['Five actual service cases use real ApiError and repository/audit adapters. No route authentication, generated Prisma, SQL scoping or concurrency run.','Service review reads state before separate update and audit calls; no enclosing transaction or expected-status predicate is proved. The service does not itself assert reviewer role. No production code changed.'];s.write_text(json.dumps(d,indent=2))
