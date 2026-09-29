from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/1cf37faa32e8/astraupskill'
extras={
'01-CODEBASE-MAP.md':'''The actual caller is the admin newsletters action; the reviewed source search did not find a worker calling queueNewsletter. Its queue helper uses the dedupe key as BullMQ jobId when Redis exists, but returns without enqueueing when Redis is unavailable. This distinction matters for a local learning app: changing a row to queued does not establish that an email will be sent. Follow [the helper](../src/server/queues.ts) and separate service state, queue acceptance and worker delivery on your diagram. The root suite executes the actual dedupe helper and substitutes the queue boundary.''',
'05-PRACTICE.md':'''Before reading the solutions, inject a queue rejection and predict three observations: the newsletter status, the number of attempted jobs and whether audit runs. Then call the function again. Explain why the new guard cannot also serve as a recovery mechanism. Use two points each for guard parity, first-call payloads, normalized keys, failure order and evidence limits. Propose an outbox or explicit recovery workflow as a design exercise, listing what must be committed atomically and what a worker may retry. Do not implement a silent reset to draft without considering already-accepted jobs.''',
'02-CONCEPTS.md':'''Dedupe keys and state guards solve different problems. The real helper trims and lowercases email for the key, while the job retains the original email payload. A successful queue adapter proves only that a call was attempted with these values. It cannot prove delivery, and a rejection after state mutation leaves recovery work for another operation.''',
'03-WORKED-CHANGE.md':'''The review expands verification without widening the source patch. Separate fixtures now isolate non-draft and missing cases; the successful case also retries in the same fixture. This combines a realistic sequence with independently runnable rejection checks. The test loads the real normalization helper instead of a lookalike key generator.''',
'04-TESTING-AND-DEBUGGING.md':'''The accepted four cases cover successful payloads and retry, a non-draft status matrix, missing lookup and queue failure. Each fixture is independent. For the failure case both subscriber jobs are attempted by Promise.all, audit is skipped and status stays queued. The test records this existing limitation rather than asserting a rollback that the service does not implement.''',
'06-SOLUTIONS-AND-REVIEW.md':'''On queue rejection, the stored status remains queued because assignment precedes the await. Promise.all starts both subscriber calls; rejection does not undo them. No success audit is recorded, and a later queueNewsletter call is refused. Full credit distinguishes retrying a delivery job from rerunning newsletter preparation. The patch preserves the database branch's state rule but does not solve distributed atomicity.''',
'07-TRACE-LAB.md':'''Add a failure row:

| Scenario | Status after call | Job attempts | Audit calls |
|---|---|---|---|
| First draft call | queued | Two | One |
| Non-draft refusal | Unchanged | Zero new | Zero new |
| Queue rejects | queued | Two | Zero |

The last row is deliberately not a success. Trace the await after the in-memory assignments and explain why adding a catch alone cannot prove that previously accepted jobs were cancelled.''',
'README.md':'''The expanded four-case lab includes a failed queue handoff. Treat it as a lesson in partial effects: local state changes can precede an external operation, and state parity alone does not make those operations atomic. This is a useful progression from basic CRUD guards to service-boundary and recovery design.''',
'VERIFICATION.md':'''The accepted label is crud-b04-astra-runtime with four passing named cases. Actual service and dedupe-key source execute; dev store, queue, audit, environment and database are adapters. The failure case explicitly observes queued state after rejection and blocked preparation retry. It is a documented existing limitation, not a durable rollback or delivery test.'''
}
for name,extra in extras.items():
 f=P/name;s=f.read_text(encoding='utf-8-sig')
 s=s.replace('Review the state transition against the exact source and preserve the existing error contract.','')
 s=s.replace('callers include the admin action and worker-facing paths','the admin action calls it')
 s=s.replace('The fixture starts draft, records two jobs and one audit, then retries.','The successful fixture starts draft, records two jobs and one audit, then retries; other cases use fresh fixtures.')
 s=s.replace('explicit db, env, store, audit, idempotency, and queue contracts','the actual dedupe helper and explicit db, env, store, audit and queue contracts')
 s=s.replace('three cases: first queue, repeated queue, and missing ID','four cases covering success/retry, non-draft states, missing ID and queue failure')
 s=s.replace('three tests pass','four tests pass').replace('value is three','value is four').replace('three executed tests','four executed tests')
 s=s.replace('astr au pskill/evidence/1cf37faa32e8','astraupskill/evidence').replace('service?s',"service's").replace(' now.','')
 s=s.replace('[evidence](../astraupskill/evidence/1cf37faa32e8/runtime-newsletter-state.tap.txt)','[accepted evidence](evidence/crud-b04-astra-runtime.log)')
 s=s.replace('Answer key is in the next chapter: draft produces two jobs and one audit; queued produces none; missing produces none.','Use a fresh fixture for each prediction, then compare with the separate solutions chapter.')
 s='\n\n'.join(x.strip() for x in s.split('\n\n') if x.strip())+'\n\n'+extra+'\n'
 f.write_text(s,encoding='utf-8');print(name,len(s.split()))
