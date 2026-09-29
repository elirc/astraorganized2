from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;P=B/'stage/e3ea1d9f41f1'
t=P/'tests/runtime-workflow-reconciliation-lab.test.mjs';s=t.read_text().replace('complete approval reaches APPROVED while an undecided file preserves its current stage','complete approval reaches APPROVED while pending decisions select CREDIT_DECISIONING')
s=s.replace("decisionOutcome: 'PENDING', currentStage: 'CREDIT_DECISIONING'","decisionOutcome: 'PENDING', currentStage: 'VERIFICATION'")
s+='''
test('funded-only and incomplete-intake snapshots select their earlier precedence branches',()=>{
 assert.equal(reconcileWorkflow(snap({disbursedAt:date})).nextStage,'DISBURSEMENT');
 const incomplete=reconcileWorkflow(snap({intakeCompletedAt:null}));assert.equal(incomplete.nextStage,'INTAKE');assert.match(incomplete.reason,/intake/i);
});
test('failed verification names the failure and referred decisions select decisioning',()=>{
 const failed=reconcileWorkflow(snap({verifications:passed.map(x=>x.type==='CREDIT_PULL'?{...x,status:'FAILED'}:x)}));
 assert.equal(failed.nextStage,'VERIFICATION');assert.match(failed.reason,/CREDIT_PULL/);
 const referred=reconcileWorkflow(snap({decisionOutcome:'REFER'}));assert.equal(referred.nextStage,'CREDIT_DECISIONING');assert.match(referred.reason,/referred/i);
});
'''
t.write_text(s,encoding='utf-8')
sp=B/'specs/e3ea1d9f41f1.json';spec=json.loads(sp.read_text())
spec['changedFiles']=[x for x in spec['changedFiles'] if '/evidence/' not in x]
spec['summary']=['Preserve production reconciliation and add an eight-case actual-source decision-table lab.', 'Teach lifecycle precedence, verification completeness, condition regression and disbursement gating without claiming persistence guarantees.']
spec['limits']=['Eight Node cases execute actual pure reconciler and disbursement guard without dependency doubles. No Prisma, Next, transaction, authorization or provider callback execution.', 'Stage regression to CONDITIONS is domain behavior, not database rollback. Pending and referred decisions explicitly select CREDIT_DECISIONING rather than generic current-stage fallthrough.', 'Local Next.js guides absent after cleanup; no framework code was changed. Full application typecheck and command integration remain unexecuted.']
sp.write_text(json.dumps(spec,indent=2),encoding='utf-8')
replacements={'six':'eight','Six':'Eight','lab?s':"lab's",'Node?s':"Node's",'project?s':"project's",'?transaction safe?':'transaction-safe','unchanged pending state':'pending-decision routing','unchanged-state behavior':'pending-decision routing','failed rollback':'failed-condition stage regression','before approval data is complete':'after earlier workflow gates pass','Conditions are considered only after approval data is complete.':'Conditions are considered after verification and the PENDING/REFER branches.','evidence/astra-crud-b05-ww10.log':'evidence/crud-b05-astra-runtime.log','evidence/results-crud-b05.json':'evidence/results.json','This course studies a sound workflow boundary':'This course studies a bounded workflow policy'}
for f in (P/'astraupskill').glob('*.md'):
 s=f.read_text(encoding='utf-8-sig')
 for a,b in replacements.items():s=s.replace(a,b)
 f.write_text(s,encoding='utf-8')
f=P/'astraupskill/VERIFICATION.md';f.write_text(f.read_text()+'''\nThe accepted expanded suite adds funded-only, incomplete-intake, failed-verification and referred-decision scenarios in two named cases. The pending case starts from VERIFICATION and expects CREDIT_DECISIONING, demonstrating explicit routing rather than preservation of the current stage. No test claims to execute the final fallback branch. A condition sending a workflow back to CONDITIONS is a domain stage change, not evidence of database rollback.\n''',encoding='utf-8')
