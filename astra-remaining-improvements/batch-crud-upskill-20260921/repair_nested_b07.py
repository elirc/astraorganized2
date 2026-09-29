from pathlib import Path
import json,hashlib,re
B=Path(__file__).resolve().parent.parent
# X1 root course lives outside the nested application; repair relative links.
P=B/'stage/1754dbb384b1'
for p in (P/'astraupskill').glob('*.md'):
 s=p.read_text(encoding='utf-8-sig').replace('](bagel-intel-platform/','](../bagel-intel-platform/')
 s=re.sub(r"'{2,3}(?=\s*$)",'',s)
 s=s.replace('from the staged project','from the bagel-intel-platform directory')
 p.write_text(s,encoding='utf-8')
# zz4 original project files and newly misplaced chapters are distinct.
id='f1f996eeb9e7';P=B/'stage'/id;D=P/'astraupskill';D.mkdir(exist_ok=True)
base=json.loads((B/'baselines'/f'{id}.json').read_text(encoding='utf-8-sig'))
canonical=Path('C:/Users/Owner/Desktop')/base['project']
chapters=['README.md','01-CODEBASE-MAP.md','02-CONCEPTS.md','03-WORKED-CHANGE.md','04-TESTING-AND-DEBUGGING.md','05-PRACTICE.md','06-SOLUTIONS-AND-REVIEW.md','07-TRACE-LAB.md','VERIFICATION.md']
for name in chapters:
 src=P/name
 s=src.read_text(encoding='utf-8-sig')
 s=s.replace('](../src/','](../zz4/src/').replace('](../tests/','](../zz4/tests/').replace('](snapshots/','](../zz4/astraupskill/snapshots/')
 (D/name).write_text(s,encoding='utf-8')
 if name in base['files']:
  raw=(canonical/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==base['files'][name]
  src.write_bytes(raw)
 else:
  # Only remove a known newly-created misplaced course file inside this exact stage.
  assert src.parent.resolve()==P.resolve() and name in chapters
  src.unlink()
f=P/'zz4/src/services/approvalService.ts';s=f.read_text()
s=s.replace('const pendingStage = request.stages\n      .filter((stage) => stage.status === "PENDING")\n      .sort((left, right) => left.sequence - right.sequence)[0];','const pendingStages = request.stages\n      .filter((stage) => stage.status === "PENDING")\n      .sort((left, right) => left.sequence - right.sequence);\n    const pendingStage = pendingStages[0];')
s=s.replace('const nextStage = request.stages.find((stage) => stage.sequence > pendingStage.sequence && stage.status === "PENDING");','const nextStage = pendingStages.find((stage) => stage.sequence > pendingStage.sequence);')
f.write_text(s,encoding='utf-8')
snapshot=P/'zz4/astraupskill/snapshots/src/services/approvalService.ts';snapshot.parent.mkdir(parents=True,exist_ok=True)
raw=(canonical/'zz4/src/services/approvalService.ts').read_bytes();assert hashlib.sha256(raw).hexdigest()==base['files']['zz4/src/services/approvalService.ts'];snapshot.write_bytes(raw)
t=P/'zz4/tests/approval-stage-order.test.mjs';s=t.read_text()
s=s.replace("'@/lib/auth/guards':{assertPermission:()=>{},canActOnStage:()=>true},'@/lib/auth/permissions':{PERMISSIONS:{VIEW_APPROVAL_QUEUE:'VIEW_APPROVAL_QUEUE',DECIDE_ASSIGNED_APPROVALS:'DECIDE_ASSIGNED_APPROVALS'}},","'next/navigation':{redirect:()=>{throw Error('unexpected redirect');}},'@/lib/auth/session':{getServerSession:async()=>null,requireServerSession:async()=>{throw Error('unexpected session lookup');}},")
s=s.replace("'@/lib/http/errors':{ConflictError:class ConflictError extends Error{},NotFoundError:class NotFoundError extends Error{}},",'')
s=s.replace("advanceCurrentStage:async()=>{seen.advanced.push(1)}","advanceCurrentStage:async(...args)=>{seen.advanced.push(args)}")
s=s.replace("stages:[{id:'stage-2'","stages:[{id:'stage-3',sequence:3,status:'PENDING',name:'Third',actorKind:'ROLE',requiredRole:'MANAGER',resolvedApproverId:null},{id:'stage-2'")
s=s.replace("assert.equal(seen.advanced.length,1);","assert.equal(seen.advanced.length,1);assert.equal(seen.advanced[0][1],2);")
s+='''
test('real capability and assignment checks reject before another decision',async()=>{
 const before=seen.decision.length;
 await assert.rejects(m.approvalService.decideRequest({userId:'u1',role:'EMPLOYEE'},'r1',{action:'APPROVE'}));
 await assert.rejects(m.approvalService.decideRequest({userId:'u1',role:'SECURITY'},'r1',{action:'APPROVE'}),/not assigned/);
 assert.equal(seen.decision.length,before);
});
test('approved history is skipped and one remaining pending stage finalizes',async()=>{
 const saved=request.stages;request.stages=[{...saved[2],status:'APPROVED'},{...saved[1]}];const before=seen.finalized.length;
 await m.approvalService.decideRequest({userId:'u1',role:'MANAGER'},'r1',{action:'APPROVE'});
 assert.equal(seen.decision.at(-1).stageId,'stage-2');assert.equal(seen.finalized.length,before+1);request.stages=saved;
});
''';t.write_text(s,encoding='utf-8')
for p in D.glob('*.md'):
 s=p.read_text().replace('two tests','four tests').replace('Two tests','Four tests').replace('two executable','four executable')
 s+='\nAstra review extension: both the current stage and next stage now use pending stages sorted by sequence. The three-stage shuffled fixture checks advancement to sequence2, not3. Four cases load real permissions, guards and domain errors; session lookup, navigation and persistence remain adapters. Run from the nested zz4 directory. Duplicate sequence policy and stale reads before the transaction remain outside this fix.\n'
 p.write_text(s,encoding='utf-8')
p=B/'specs'/f'{id}.json';s=json.loads(p.read_text(encoding='utf-8-sig'));s['changedFiles']=[x for x in s['changedFiles'] if '/evidence/' not in x]
s['summary']=['Sort pending stages consistently for both current approval and next-stage advancement.','Four actual-service runtime cases execute real capability/assignment guards and errors with database/session adapters.']
s['limits']=['No Prisma, Next session, SQL isolation or concurrent approvals executed.','Duplicate sequence policy unchanged; request read remains before transaction.']
p.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
