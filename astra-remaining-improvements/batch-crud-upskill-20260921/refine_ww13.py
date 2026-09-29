from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/2e356b8f3d9f'
f=P/'src/repositories/reportingRepository.ts';s=f.read_text();block='''    report.status = "APPROVED";
    report.approvedAt = new Date().toISOString();
    report.approvedByUserId = approvedByUserId;

''';assert block in s;s=s.replace(block,'');needle='''    // ⚠️ SENIOR NOTE: Parent period status must move with the child report''';assert needle in s;s=s.replace(needle,block+needle);f.write_text(s,encoding='utf-8')
t=P/'tests/runtime-report-submit-atomicity.test.mjs';s=t.read_text();s='\n'.join(line for line in s.splitlines() if not line.startswith('class NotFoundError') and "'@/lib/http/api-errors':" not in line)+'\n'
s+='''
test('orphan approval rejects before changing report status, approver or timestamp',()=>{
 const orphan={id:'orphan',reportingPeriodId:'missing',awardId:'award-1',status:'SUBMITTED',approvedAt:null,approvedByUserId:null};state.reports.push(orphan);
 const before=JSON.stringify(state);assert.throws(()=>mod.approveReport('orphan','reviewer'),e=>e.statusCode===404&&e.code==='NOT_FOUND');assert.equal(JSON.stringify(state),before);
 state.reports.pop();
});
test('valid approval updates child and parent and returns the same report',()=>{
 const report=state.reports.find(x=>x.id==='existing');const result=mod.approveReport('existing','reviewer');assert.equal(result,report);assert.equal(result.status,'APPROVED');assert.equal(result.approvedByUserId,'reviewer');assert.ok(Number.isFinite(Date.parse(result.approvedAt)));assert.equal(state.reportingPeriods[0].status,'APPROVED');
});
test('missing report rejects with real typed error and preserves populated state',()=>{
 const before=JSON.stringify(state);assert.throws(()=>mod.approveReport('absent','reviewer'),e=>e.statusCode===404&&e.code==='NOT_FOUND');assert.equal(JSON.stringify(state),before);
});
'''
t.write_text(s,encoding='utf-8')
sp=B/'specs/2e356b8f3d9f.json';spec=json.loads(sp.read_text(encoding='utf-8-sig'));spec['project']='_Organized Desktop/05 Numbered Experiments/ww13';spec['changedFiles']=[x for x in spec['changedFiles'] if '/evidence/' not in x]
spec['summary']=['Validate reporting-period existence before submission insertion and before approval changes the child report.', 'Add actual repository/error-class tests for both orphan paths and successful parent/child transitions.']
spec['limits']=['Five runtime cases execute actual repository and error classes with mutable-store and ID adapters. No live Next, authentication, persistence transaction, concurrency or full typecheck.', 'This prevents the known missing-parent partial mutations in submit and approve. It does not add idempotency, service authorization, rollback for arbitrary later failures or atomic audit persistence. IDs and submission timestamps are still allocated before parent lookup.']
sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
for f in (P/'astraupskill').glob('*.md'):
 s=f.read_text(encoding='utf-8-sig').replace(".''",".")
 s=s.replace('evidence/2e356b8f3d9f-runtime-report-submit.tap.txt','evidence/crud-b05-astra-runtime.log').replace('2 tests passed','5 tests passed').replace('numeric executed count two','numeric executed count five')
 s=s.replace('store, ID generator, error class, and type-only module','store, ID generator and type-only module; the actual error classes execute').replace('store, ID factory, errors, and type-only exports','store, ID factory and type-only exports')
 if f.name=='README.md':s+='''\nRoot review found the matching approval bug: approveReport changed status, approver and timestamp before finding the parent. The accepted patch moves that parent lookup before those child mutations as well. Five named cases cover submission and approval, including an orphan report already present in state. This extends the same invariant consistently across both repository write paths.\n'''
 if f.name=='03-WORKED-CHANGE.md':s+='''\nThe approval correction follows the same order: find report, find parent, reject if either is absent, then change child approval fields and parent status. Previously an orphan report could become APPROVED even though the call threw. The new test serializes the whole fixture before and after refusal, protecting status, approver and timestamp as well as collection size.\n'''
 if f.name=='05-PRACTICE.md':s+='''\nAdditional exercise: create a SUBMITTED report whose reportingPeriodId is absent. Predict approveReport's error and all three approval fields afterward. Explain why checking only array length would fail to detect the original approval corruption.\n'''
 if f.name=='06-SOLUTIONS-AND-REVIEW.md':s+='''\nThe orphan approval throws the real 404 NOT_FOUND error and leaves the report SUBMITTED with its old approver and timestamp. A valid approval returns the same report object and changes both child and parent to APPROVED. A missing report changes nothing. Whole-state equality is stronger than a count assertion for in-place updates.\n'''
 if f.name=='07-TRACE-LAB.md':s+='''\nFor approval, add a trace row: existing orphan report -> missing parent -> NotFoundError -> unchanged child. The successful row is existing child -> existing parent -> child approval fields -> parent APPROVED -> same child returned. These two new traces distinguish insertion corruption from in-place mutation corruption.\n'''
 if f.name=='VERIFICATION.md':s+='''\nThe accepted five-case capture crud-b05-astra-runtime adds orphan approval preservation, valid approval and missing-report refusal. Actual error classes supply statusCode 404 and NOT_FOUND. Approval was corrected during root review; the original snapshot covers both functions. Earlier two-case logs remain workspace evidence but are superseded for delivery.\n'''
 f.write_text(s,encoding='utf-8')
