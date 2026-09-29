from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/5007ac6ecdec'
t=P/'tests/runtime-review-cycle.test.mjs';s=t.read_text()
s=s.replace("class HttpError extends Error { constructor(status, message) { super(message); this.status = status; } }",'')
s=s.replace("{ root, stubs:","{ root, aliasRoot: root, stubs:")
s=s.replace("    '@/src/lib/http/errors': { HttpError },\n",'')
s=s.replace('e instanceof HttpError && e.status === 409',"e.name === 'HttpError' && e.status === 409")
s+='''
test('real repository includes organization, id and PENDING in its update predicate',async()=>{
 const {reviewCycleRepository}=await loadTypeScript('src/repositories/reviewCycleRepository.ts',{root,aliasRoot:root});
 const input={decision:'CERTIFIED',decidedByUserId:'user-1',decidedAt:new Date()};let calls=0;
 const result=await reviewCycleRepository.decideItem({reviewItem:{updateMany:async arg=>{calls++;assert.deepEqual(JSON.parse(JSON.stringify(arg.where)),{organizationId:'org-1',id:'item-1',decision:'PENDING'});assert.equal(arg.data,input);return {count:0};}}},'org-1','item-1',input);
 assert.equal(result.count,0);assert.equal(calls,1);
});
test('certification returns reread result without grant revocation and preserves transaction arguments',async()=>{
 const f=makeFixture();const {createReviewCycleService}=await serviceFor(f);
 const result=await createReviewCycleService({runner:f.runner,reviewCycleRepository:f.review,accessRequestRepository:f.access,auditLogRepository:f.audit}).decideItem(session,'cycle-1','item-1',{decision:'CERTIFIED'});
 assert.equal(result.decision,'CERTIFIED');assert.deepEqual(f.calls.map(c=>c[0]),['find','decide','find','audit']);
 for(const call of f.calls)assert.equal(call[1],'transaction');
 assert.deepEqual(f.calls[0].slice(2),['org-1','cycle-1','item-1']);assert.deepEqual(f.calls[2].slice(2),['org-1','cycle-1','item-1']);assert.equal(f.calls[3][2],'review-item.certified');
});
test('decision write failure preserves error and stops reread, revocation and audit',async()=>{
 const f=makeFixture();const error=new Error('write unavailable');f.review.decideItem=async()=>{f.calls.push(['decide']);throw error;};
 const {createReviewCycleService}=await serviceFor(f);
 await assert.rejects(createReviewCycleService({runner:f.runner,reviewCycleRepository:f.review,accessRequestRepository:f.access,auditLogRepository:f.audit}).decideItem(session,'cycle-1','item-1',{decision:'REVOKED'}),e=>e===error);
 assert.deepEqual(f.calls.map(c=>c[0]),['find','decide']);
});
'''
t.write_text(s,encoding='utf-8')
sp=B/'specs/5007ac6ecdec.json';spec=json.loads(sp.read_text())
spec['changedFiles']=[x for x in spec['changedFiles'] if '/evidence/' not in x]
spec['limits']=['Six runtime cases execute actual review service, HttpError and the changed repository predicate builder. Explicit database/transaction/repository adapters verify arguments and ordering; no native Prisma provider or concurrent database run.', 'The conditional write guards organization, item id and PENDING, but does not atomically guard review-cycle OPEN status. Native rollback, route authorization and simultaneous reviewer behavior remain unexecuted.', 'Normal application typecheck and provider-backed integration were not run after dependency cleanup.']
sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
