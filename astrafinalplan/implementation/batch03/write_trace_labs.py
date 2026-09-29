from pathlib import Path
import json,re
B=Path(__file__).resolve().parent
courses=json.loads((B/'courses.json').read_text(encoding='utf-8'))
tables={
21:[('Remove starter Mobile app','Surviving Public API=7 and Dark mode=2; total 9'),('Rename surviving option','Same id and votes'),('Add new option','Fresh id and zero votes'),('API and api labels','Rejected duplicate'),('Storage write fails','Saved state and current draft retained')],
22:[('A,B in todo; C in doing; move A before C','todo B=0; doing A=0,C=1'),('Self-drop A before A','No-op'),('Unknown column','Rejected before save'),('Write throws','Previous card state preserved'),('Keyboard movement','Same move boundary, focus restored')],
23:[('Create code with surrounding spaces and lowercase','Normalized uppercase code'),('Another id reuses normalized code','409 conflict'),('Same id retains its code','Allowed edit'),('Capacity 2, enrolled 3','400; record unchanged'),('Fractional count','Rejected whole-number field')],
24:[('2028-02-29','Valid calendar date'),('2027-02-29','Rejected impossible date'),('Capacity 5, registered 5','Valid boundary'),('Capacity 5, registered 6','Rejected cross-field invariant'),('Object-valued location','400 before string operations')],
25:[('A March 2, B blank, C February 29','C then A then B'),('Equal next-step dates','Stable id tie-breaker'),('Clear optional date','Undated application'),('Impossible date','400; previous record unchanged'),('Change search','Only matches enter the sorted view')],
26:[('5 matches, pageSize 2','3 pages'),('Request page 999','Clamped last page, one item'),('No matching products','Usable first page with total zero'),('Fractional stock','Rejected'),('Equal primary sort values','Deterministic id tie-breaker')],
27:[('Salt, salt, Water','Salt, Water; first spelling retained'),('Blank ingredient','Rejected'),('Object ingredient','Whole payload rejected'),('Fractional servings','Rejected'),('Free-form ingredient text','No automatic quantity or unit conversion')],
28:[('R1 obtains structural lock','R2 waits'),('R1 moves root A under root B','One acyclic change commits'),('R2 tries B under A','Reads changed graph and rejects cycle'),('Missing parent','Rejected'),('Direct SQL bypasses API policy','Outside this cycle guarantee')],
29:[('Comment C belongs to post B','B/C is the valid pair'),('Delete C through post A','C remains on B'),('Delete post B','Its comments are removed'),('Object comment body','Controlled validation error'),('Author text','Descriptive label, not authenticated identity')],
30:[('Actual test revenue window','10, 0, 30'),('Cumulative','10, 10, 40'),('Moving average','10, 5, 13.33'),('Delta','null, -10, 30'),('Raw insert then refresh','Stale true, then false')],
31:[('Same status twice','One actual status event'),('Same assignment twice','No redundant assignment event'),('Missing agent reference','Rejected relationship'),('Late related write fails','Earlier transactional work rolls back'),('Different concurrent commands','Serialized changes; scheduling order is not predetermined')],
32:[('High AND Backlog AND text','Intersection of all predicates'),('All priorities','Status and text remain active'),('Clear search','Priority and status remain active'),('Client URL','Includes priority parameter'),('Malformed text','Rejected before mutation')],
33:[('6 matches, pageSize 5','Second page has one item'),('Delete final matching item','Five matches remain'),('Request old page 2','Page 1 with five rows'),('Count and rows','One request snapshot'),('Slow-old search response','Separate client race remains an exercise')],
34:[('2 x 12.34, tax 0','24.68'),('Quantity [2]','Rejected shape despite JavaScript coercion'),('Price 12.345','Rejected precision'),('Issue date 2027-02-29','Rejected calendar date'),('Late replacement line failure','Original invoice and lines remain')]
}
for c in courses:
 n=c['stage'];root=B/'stage'/str(n);test=(root/c['test']).read_text(encoding='utf-8');extra=''
 if n in tables:rows=tables[n]
 else:
  d=c['domain'];s0,s1=d['statuses'][:2];route=d['route']
  rows=[(f'{s0} to {s1}','One new status event'),(f'{s1} to {s1}','No new status event'),('Invalid calendar-date edit','400; old record unchanged'),('3 matches, size 2, page 999','Page 2, one item'),('Empty matching set','Page 1, total zero')]
  if c['sql']:
   extra='''## Concurrency and rollback schedule

| Step | Request A | Request B |
|---|---|---|
| 1 | Begins and locks the record | Begins, waits for the row |
| 2 | Reads old status, writes new status and event | Still waiting |
| 3 | Commits | Acquires lock and reads committed status |
| 4 | Returns changed record | Same-value guard skips another event |

The two Promise.all requests in the regression do not require A to win. They require the same invariant whichever connection gets the lock first. All related writes use the transaction client. Using the global pool for the event insert would move that write outside the transaction and break the guarantee.

The final test installs a trigger that rejects status activity inserts. The status UPDATE executes first; the later insert fails. ROLLBACK restores the previous status and timestamp. The following successful request proves that the failure did not leave the operation permanently unusable. Compare record and history after failure: a 500 response alone cannot prove rollback.

The seed dueDate mapping and PostgreSQL DATE parser address representation, separately from concurrency. A JSON field named dueDate does not automatically populate a SQL record field named due_date. Follow the explicit mapping and verify the resulting label at the API and date input. Calendar labels differ from the timestamps used for activity chronology.
'''
  else:
   extra='''## Follow the in-memory boundary

The repository status method executes synchronously inside one Node process. It finds the record, compares status, changes the object and appends history without an intervening await. A later request sees the latest live value. This reasoning explains repeat-safe behavior in this scaffold; it does not establish database durability or coordination across several server processes.

Restart the development server after adding a synthetic record. The repository reconstructs its seeds and that new record disappears. A page reload alone does not restart the API, which can make temporary server state look durable. Distinguish browser lifetime, server lifetime and database lifetime in your explanation.

If you add an asynchronous file write, two calls can interleave at await and a failed write can leave memory ahead of disk. Design a new commit boundary explicitly. If you migrate to PostgreSQL, place record and history in a transaction and define a concurrency rule for comparing current status. Copying the same-value if statement alone does not solve those additional failure modes.
'''
  source=(root/c['source']).read_text(encoding='utf-8');match=re.search(r'PORT\s*(?:\?\?|\|\|)\s*(\d+)',source);assert match,(n,'port')
  payload=dict(title=c['fixture_title'],owner='Junior Learner',category=d['categories'][0],status=s0,priority='Medium',amount=12.50,dueDate='2028-02-29',notes='Synthetic trace-lab fixture')
  body=json.dumps(payload).replace("'","''")
  extra+=f'''
## Manual HTTP example

Start the local development server using the course index. This example creates a synthetic record in that learning instance. Use the port printed by your server if you override its default. Automated tests use their own ephemeral port instead.

```powershell
$api = 'http://localhost:{match.group(1)}'
$body = '{body}'
$record = Invoke-RestMethod -Uri "$api{route}" -Method Post -ContentType 'application/json' -Body $body
$change = @{{ status = '{s1}' }} | ConvertTo-Json
Invoke-RestMethod -Uri "$api{route}/$($record.id)/status" -Method Patch -ContentType 'application/json' -Body $change
Invoke-RestMethod -Uri "$api{route}/$($record.id)/status" -Method Patch -ContentType 'application/json' -Body $change
$history = Invoke-RestMethod -Uri "$api{route}/$($record.id)/activity"
@($history | Where-Object {{ $_.kind -eq 'status' }}).Count
```

Expected final count: 1. The created entry remains present but is excluded by the kind filter. Edit the dueDate to the impossible 2027-02-29 in a separate request and verify rejection without a changed record. Remove the synthetic record through the app after the exercise if you want to restore your learning dataset.
'''
 names=re.findall(r"test\(['\"]([^'\"]+)",test)
 text=f'''# Trace lab: {c['focus']}

[Course index](README.md) · [Worked source](03-WORKED-CHANGE.md)

## Prepare a prediction

Open [{c['source']}](../{c['source']}) and [{c['test']}](../{c['test']}) side by side. Use the source as the authoritative implementation; this lab is a snapshot of the delivered change. Use synthetic fixtures so a deliberate failure is easy to repeat.

Start with this concrete scenario:

{c['example']}

Draw the data before the action. Label stable identity separately from position, title or other editable attributes. Write the requested value next to the old value. Now trace the request/event one boundary at a time: input, validation, computation, state change, output. Put a mark next to every side effect. A local draft can be invalid while the authoritative record remains valid; do not merge those two states in your diagram.

## Expected observations

| Action or input | Expected result |
|---|---|
'''+ '\n'.join(f'| {a} | {b} |' for a,b in rows)+f'''

Pick one row and hand-calculate its expected result. For a count, list the ids that participate. For an amount or average, write the arithmetic before running the app. For a rejected change, name every field that should remain identical. Error wording alone does not prove that state stayed intact.

## Follow the implementation's reasoning

{c['concept']}

Pause near `{c['symbol']}` and inspect both types and values. A client-side TypeScript type does not validate incoming HTTP JSON. A number-like string may be acceptable for a particular field while an array with a similar coercion is not. In the browser-only apps, saved JSON and controls likewise need deliberate shape and identity handling.

After the successful path, repeat with the failure case. Identify the last operation allowed to occur before rejection. If anything writes earlier, explain how the code avoids or reverses partial state. A try/catch explains control flow; it does not by itself create a transaction. For a repeated command, determine whether the second invocation should be a no-op or another real change before looking at the result.

{extra}

## Connect the trace to executable evidence

The actual regression scenarios are:

'''+ '\n'.join(f'- {name}' for name in names)+f'''

Run the command in the course index and read one scenario from arrangement through cleanup. Distinguish seed data from records created by the test. Identify assertions about HTTP status, domain data and before/after state. A count of three is useful only when you can explain why exactly three matching records exist.

Change one meaningful fixture value without changing its shape. Predict the result before executing. Choose a boundary that exposes a naive implementation: duplicate identity, impossible date, tied sort key, repeated command or late failed write, as applicable here. Keep the test's expected answer independent of the function under test; copying the implementation's calculation can copy the same bug.

## Independent checkpoint and answer guidance

Close the worked chapter and explain the initial state, action, invariant, result and one limitation in your own words. Locate the point where the result becomes authoritative: a successful localStorage write, a synchronous memory method or a committed SQL transaction. Explain what survives a page reload and a server restart. Consult the data model in chapter 1 if those lifetimes are unclear.

If stored state and the screen disagree, inspect the storage/network result first. A correct record with stale rendering needs a different fix from a failed write. Ask a reviewer to change one input while you predict the result aloud. If your prediction is wrong, find the first guard, query or representation change where the model diverged.

Your final learning log should contain the exact input, expected output, observed output, responsible source boundary and next question. A strong answer cites the actual helper or query and a specific limit from this lesson. Finish by attempting the first domain exercise without copying its solution; the exercise is future practice, not a feature already delivered.
'''
 (root/'astraupskill/07-TRACE-LAB.md').write_text(text,encoding='utf-8')
print('Generated thirty detailed trace labs')
