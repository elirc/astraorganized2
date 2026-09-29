from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/79c315026b95/astraupskill'
for p in P.glob('*.md'):
 t=p.read_text()
 for a,b in {'repository?s':"repository's",'worker?s':"worker's",'lab?s':"lab's",'module?s':"module's",'from the staged project':'from the project directory','evidence/astra-crud-b07-ww6.log':'evidence/crud-b07-astra-runtime.log','evidence/results-crud-b07.json':'evidence/results.json','claims pending work':'attempts a RUNNING transition','failures transition to FAILED':'the catch directly writes FAILED','every terminal refusal':'representative terminal refusals','rollups':'allocation result rows','rollup replacement':'allocation result replacement'}.items():t=t.replace(a,b)
 t=t.replace('The project also has a conditional claim in its queue/worker path, but this lab does not execute it.','The inspected worker uses a read then update transition; it has no conditional count-one claim in this path.')
 t=t.replace('supplies only the error boundary needed for module evaluation','loads the real error classes while adapting unused repository/engine exports and queue registration')
 t=t.replace('The state guard prevents a worker or caller from skipping required phases or reopening a terminal record accidentally.','The state guard refuses skipped phases and terminal reopening when a caller invokes it. The worker catch bypasses it to write FAILED.')
 t=t.replace('The worker must also claim only PENDING rows and check an update count so two processors cannot both proceed.','A stronger worker design would claim only PENDING rows conditionally and check an update count. That safeguard is not implemented by this policy lab.')
 t=t.replace('with an explicit error double and no copied algorithm','with the actual ValidationError and no copied policy algorithm')
 t=t.replace('Another should force computation failure and assert FAILED plus audit while preserving result consistency.','Another should force computation failure and inspect the direct FAILED update; this worker does not emit an audit in the shown processing function.')
 t=t.replace('find, claim, compute, replace, terminal update','read, RUNNING update, compute, replace, completion read and update')
 t=t.replace('A worker sees PENDING but its conditional update count is zero. Predict computation and audit behavior.','Design a future conditional claim that returns count zero. Predict which operations it should prevent, and contrast it with the current read-then-update code.')
 t=t.replace('Level 3 means no computation or audit because claim ownership was not obtained.','Level 3 proposes no computation after a failed conditional claim; this is a future design requirement, not current runtime evidence.')
 t=t.replace('| PENDING | RUNNING | allowed | conditional claim |','| PENDING | RUNNING | allowed | current worker reads then updates |').replace('| RUNNING | FAILED | allowed | failure record and audit |','| RUNNING | FAILED | allowed | catch directly writes failure |')
 t=t.replace('An allowed PENDING-to-RUNNING transition still requires a count-one claim.','An allowed PENDING-to-RUNNING transition does not create an atomic claim; the current worker uses a separate read and update.')
 t=t.replace('The test does not trace', 'The test does not trace')
 repeated=['Use the same trace vocabulary when discussing API retries so reviewers can compare policy and persistence clearly.','The exact command and result count make this boundary reviewable for junior and senior readers alike.']
 for sentence in repeated:
  while t.count(sentence)>1:t=t.replace(sentence,'',1)
 if p.name=='VERIFICATION.md':t+='\nThe actual ValidationError exposes statusCode422 and code VALIDATION_ERROR. Queue registration is adapted to prevent import-time worker scheduling. The worker catch writes FAILED directly, even after a transition error; therefore the helper tests do not prove terminal records cannot be downgraded by the worker. That behavior requires a separate guarded-failure design and runtime tests.\n'
 if p.name=='01-CODEBASE-MAP.md':t+='\nThe queue is an in-process setTimeout callback, not durable storage. A process restart can lose queued execution even though the run record exists. Registration and scheduling are not exercised here.\n'
 if p.name=='06-SOLUTIONS-AND-REVIEW.md':t+='\nInspection supplies one concrete answer: failure marking does bypass the transition guard, and there is no atomic claim in the shown worker. A reviewer must not extend terminal-policy test results to those unguarded writes.\n'
 if p.name=='07-TRACE-LAB.md':t+='\nRead the catch separately: it records a failure message and writes FAILED without calling assertValidRunTransition. Successful failure recording is swallowed by the worker; a failure of that write can escape. This trace is inspected source, not executed worker evidence.\n'
 p.write_text(t,encoding='utf-8')
