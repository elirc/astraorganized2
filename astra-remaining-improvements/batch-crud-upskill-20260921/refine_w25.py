from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/13ccdfb915ff'
t=P/'tests/runtime-lock-service-lab.test.mjs';s=t.read_text()
s='\n'.join(line for line in s.splitlines() if not any(x in line for x in ['"@/domain/locks/types":','"@/services/lockStateMachine":','"@/lib/utils/time":']))+'\n'
s=s.replace('"acquisition contention returns a retry contract and records an audit"','"repository version conflict after eligible reacquire returns retry contract and audit"')
start=s.index('test("repository version');s=s[:start]+s[start:].replace('state: "ACTIVE"','state: "RELEASED"',1)
s += '''
test('active lock is refused by actual policy before repository contention writes',async()=>{
 const f=await fixture({id:'l1',ownerUserId:'owner',ownerService:'svc',state:'ACTIVE',version:1,scopeKey:'JOB:j1'});
 const result=await f.service.acquireLock(session('other'),{scopeType:'JOB',scopeId:'j1',resourceLabel:'Job',mode:'OPTIMISTIC',leaseDurationSeconds:20,fallbackAction:'QUEUE'});
 assert.equal(result.failure.code,'LOCK_HELD');assert.equal(result.failure.retryAfterMs,500);assert.equal(result.failure.fallbackAction,'QUEUE');assert.equal(f.saves.length,0);assert.equal(f.audits.length,0);
});
test('admin override releases another owner and real renewal helper returns an ISO timestamp',async()=>{
 const lock={id:'l1',ownerUserId:'owner',ownerService:'svc',state:'ACTIVE',version:1,scopeKey:'JOB:j1'};
 const f=await fixture(lock);const admin=session('admin');admin.user.role='ADMIN';
 assert.equal((await f.service.releaseLock(admin,'l1',{reason:'operator recovery'})).ok,true);
 assert.equal(f.audits[0].metadata.adminOverride,true);assert.equal(f.audits[0].actorUserId,'admin');
 const renew=await fixture(lock);const result=await renew.service.renewLock(session('owner'),'l1',{leaseDurationSeconds:30});
 assert.equal(result.ok,true);assert.equal(typeof result.lock.leaseExpiresAt,'string');assert.ok(Number.isFinite(Date.parse(result.lock.leaseExpiresAt)));assert.equal(result.lock.version,2);assert.equal(renew.audits[0].eventType,'LOCK_RENEWED');
});
'''
t.write_text(s,encoding='utf-8')
sp=B/'specs/13ccdfb915ff.json';spec=json.loads(sp.read_text())
spec['changedFiles']=[x for x in spec['changedFiles'] if '/evidence/' not in x]
spec['summary'][0]='Preserve the existing LockService production implementation and add a bounded executable learning lab.'
spec['limits']=['Six cases execute actual LockService, state machine, scope-key and time helpers with explicit repository/audit adapters. No Next route, actual repository persistence, expiry scan, multi-process contention or durable audit execution.', 'The draft incorrectly replaced canReacquire with always true and used a Date-returning time double. Accepted tests load the real modules and distinguish active-lock refusal from a repository version conflict after an eligible reacquire.', 'No production code is changed and this bounded lab is not a complete correctness certification of the lock system.']
sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
