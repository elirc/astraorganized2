from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/4e19ba5b5028/astraupskill'
for p in P.glob('*.md'):
 t=p.read_text()
 for word in ['test','user','recipient','code','service']:
  t=t.replace(word+'?s',word+"'s")
 for a,b in {'Four cases':'Six cases','four-case':'six-case','evidence/astra-crud-b06-ww29.log':'evidence/crud-b06-astra-runtime.log','evidence/results-crud-b06.json':'evidence/results.json','from the staged project':'from the project directory','The lab uses status doubles':'The lab uses status read adapters and actual repository status derivation functions','the real permission matrix, while':'the real permission matrix, error class and status derivation functions, while'}.items():t=t.replace(a,b)
 if p.name=='README.md':t+='\nTwo additional cases exercise actual PARTIAL_FAILURE derivation for mixed statuses and an aggregate update failure after delivery/opened-at writes. The latter demonstrates partial progress: this open operation has no encompassing transaction.\n'
 if p.name=='VERIFICATION.md':t+='\nThe added cases verify mixed OPENED/FAILED delivery aggregation and propagate an injected notification-status failure after the delivery and timestamp calls. No batch update or audit follows that failure. Real ApiError and both derivation functions execute; generated enum values and an unused ZodError export are adapters. This proves call ordering, not persisted rollback: the source has no encompassing open transaction.\n'
 if p.name=='06-SOLUTIONS-AND-REVIEW.md':t+='\nWhen status refresh fails, delivery and timestamp calls have already completed; audit is not reached. The source offers no enclosing transaction to undo those calls. A future change must choose transactional persistence or explicit reconciliation. Mixed OPENED and FAILED statuses yield PARTIAL_FAILURE under the actual helper.\n'
 if p.name=='07-TRACE-LAB.md':t+='\nAdditional recorded traces: mixed OPENED/FAILED states lead to PARTIAL_FAILURE updates; an injected notification-status failure stops before batch update and audit, after the two opening writes. These distinguish computed status policy from failure recovery.\n'
 p.write_text(t,encoding='utf-8')
