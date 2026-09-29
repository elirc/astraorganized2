from pathlib import Path
import json,hashlib,shutil,os,xml.etree.ElementTree as ET
B=Path(__file__).resolve().parents[2]; ID='a0a0ff059e64'; P=B/'stage'/ID; U=P/'astraupskill'; C=B/'checks'/ID; E=U/'evidence'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
labels=['restore-tests-4','backend-tests-6','root-backend-build-01','root-frontend-install-01','root-frontend-build-01']
for label in labels:
 r=read(C/(label+'.json'));assert r['status']=='complete' and r['exitCode']==0,r
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
trx=P/'backend/ExpenseManagement.Api.Tests/TestResults/a0a0ff059e64-6.trx'; counts=ET.parse(trx).find('.//{*}Counters').attrib
assert counts['total']==counts['executed']==counts['passed']=='10' and counts['failed']=='0';shutil.copyfile(trx,E/'expense-tests.trx')
for p in U.glob('*.md'):
 t=p.read_text(encoding='utf-8-sig').replace('copy of the staged project','copy of the project').replace('The staged project','The project')
 p.write_text(t,encoding='utf-8')
source=(P/'backend/Services/ExpenseService.cs').read_text(encoding='utf-8');start=source.index('    public Expense StartReimbursement');end=source.index('    /// <summary>Re-runs policy',start)
p=U/'03-WORKED-CHANGE.md';t=p.read_text(encoding='utf-8');a=t.index('```csharp');z=t.index('```',a+3);t=t[:a]+'```csharp\n'+source[start:end].rstrip()+'\n'+t[z:];p.write_text(t,encoding='utf-8')
p=U/'07-TRACE-LAB.md';t=p.read_text(encoding='utf-8');t=t.replace('| 2 | `ExpenseService.GetForActor` | Expense exists and Finance can view it | Missing id is `NotFoundException` |\n| 3 | `DataStore.GetExpenseLock` | Per-expense gate is acquired | Worker and command serialize field changes |','| 2 | `DataStore.GetExpenseLock` | Per-expense gate is acquired before lookup | Expense commands and reimbursement worker serialize their changes |\n| 3 | `ExpenseService.GetForActor` | Current expense exists and Finance can view it | Missing or already-deleted id is `NotFoundException` |')
t+='\nThe test invokes two duplicate jobs with a zero delay. Task.WhenAll collects their tasks, but those delegates can finish synchronously before the second invocation starts; this is duplicate-execution evidence, not a forced overlapping-worker test. The lock is visible in production source, while a controlled two-thread test would be required to demonstrate a particular interleaving. Receipt uploads and direct mutation through returned entities do not participate in this coordination.\n';p.write_text(t,encoding='utf-8')
p=U/'05-PRACTICE.md';t=p.read_text(encoding='utf-8').replace('Then flip to `Accept = true`, call again,','Then create a second queue with `Accept = true` and a second service using the same store, call again,').replace('The second call should throw because the entity is already reimbursing;','A third call using the accepting service should throw because the entity is already reimbursing;')
t=t.replace('In `ExpenseService.ValidateAndNormalize`, add a test that calls `Create`','Extend the existing Create invalid-field test for `ExpenseService.ValidateAndNormalize` by calling `Create`')
p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8').replace('Exercise 1 is solved by calling the same private normalization path that `Create` and `Update` use.','Exercise 1 calls the public Create method, which reaches the private normalization path shared with Update. The existing invalid-field matrix already supplies the whitespace and undefined-enum examples.')
t+='''
## Exercise 2: complete additional regression

Add this method inside ExpenseWorkflowTests, where the existing Fixture, AddExpense and Service helpers are in scope. It is a proposed exercise answer, not an eleventh test in the recorded ten-case run.

```csharp
[Fact]
public void Overlong_rejection_reason_leaves_submitted_expense_unchanged()
{
    var (store, employee, manager, _) = Fixture();
    var expense = AddExpense(store, employee, ExpenseStatus.Submitted);
    var before = Snapshot(expense);
    var service = Service(store, new RecordingQueue());
    Assert.Throws<DomainException>(() =>
        service.Reject(manager, expense.Id, new string('x', 501)));
    Assert.Equal(before, Snapshot(expense));
}
```

## Exercise 3: admission sequence answer

RecordingQueue.Accept is init-only, so use two queue instances. First construct a rejecting queue and service over the fixture store. After its exception, assert Approved, empty history and empty Work. Construct an accepting queue and service over that same store; the next call succeeds with one Reimbursing event and one captured delegate. Call the accepting service once more: the state precondition throws before TryEnqueue, so Work remains at one. The complete recorded fixture below contains the rejection, acceptance and repeated-command assertions in separate tests. Combining them is an exercise, not additional executed evidence.

## Exercise 4: non-reimbursing worker answer

Use Fixture and AddExpense with Submitted. Build a ServiceCollection with AddLogging and AddSingleton(store), capture Snapshot(expense), await ProcessReimbursement(expense.Id, TimeSpan.Zero)(provider, CancellationToken.None), and compare the snapshot. Repeat in a fresh fixture with Reimbursing and assert its single terminal event. The recorded suite checks the state-machine restrictions and duplicate successful worker execution; it does not include this separate Submitted-delegate scenario.

## Exercise 5: asynchronous admission answer

An await cannot remain inside the current C# lock statement. An asynchronous admission design would need an async-compatible coordination mechanism or an explicit reservation/compensation state; the controller would await a Task-returning service. Cancellation before admission should leave Approved and no job. Cancellation after admission requires a defined contract, because cancellation does not remove an already queued delegate. A full queue is a capacity decision, while a canceled request is an interruption. Test each before proposing a durable outbox that records the state change and work request together.

## Complete executed fixture

This is the complete current ExpenseWorkflowTests.cs, including imports, users, real store, queue double and all ten facts. Modify that existing file for the exercises. The direct service tests do not exercise HTTP authorization, MVC binding or the hosted service loop. The snapshot string checks field values and list counts; the submit test additionally copies immutable flag/history entries, so it can detect replacement of list contents as well.

```csharp
'''+(P/'backend/ExpenseManagement.Api.Tests/ExpenseWorkflowTests.cs').read_text(encoding='utf-8')+'```\n';p.write_text(t,encoding='utf-8')
(U/'VERIFICATION.md').write_text('''# Verification and boundaries

Run these commands from the project root. The application targets net8.0; the recorded environment supplied the .NET 10 SDK/runtime, so tests explicitly enabled major-version roll-forward. A machine with the .NET 8 runtime can use its normal target runtime instead. The frontend was installed with Node22.16 and now includes a package lock for repeatable installation.

```powershell
$env:DOTNET_ROLL_FORWARD = 'Major'
dotnet restore backend/ExpenseManagement.Api.Tests/ExpenseManagement.Api.Tests.csproj
dotnet test backend/ExpenseManagement.Api.Tests/ExpenseManagement.Api.Tests.csproj --no-restore --logger 'trx;LogFileName=expense.trx' --results-directory TestResults
dotnet build backend/ExpenseManagement.Api.csproj --no-restore -c Release
npm ci --prefix frontend
npm run build --prefix frontend
```

The [final test log](evidence/backend-tests-6.log) and [TRX counters](evidence/expense-tests.trx) record ten discovered, executed and passed tests with zero failures. The [backend Release build](evidence/root-backend-build-01.log) and [frontend production build](evidence/root-frontend-build-01.log) passed. The [results summary](evidence/results.json) links the authoritative check labels. Earlier failed compilation and smaller passing attempts may remain in evidence, but they are not counted as extra tests or the final result.

The suite invokes production ExpenseService and BackgroundJobs with real in-memory entities. It covers candidate validation/normalization, failed reject/update/submit state, rejected and throwing queues, repeated reimbursement commands, duplicate worker completion, the actual capacity-one channel and system-only transitions. The duplicate job has zero delay and does not force two threads to overlap. No live HTTP adapter, authenticated session, receipt file, payment rail, hosted worker or database was exercised. A successful frontend bundle does not establish browser interaction behavior.

The six changed baseline production files have exact original-byte snapshots. The new xUnit project is excluded from the parent Web SDK compile and content globs. The frontend package-lock.json is a new setup artifact; application frontend source is unchanged. Generated bin, obj and TestResults directories are local check output and are not delivered; the portable TRX above is included deliberately.

The dictionary and queue remain process-local and non-durable. Expense commands retrieve their current object under the same per-expense gate used by reimbursement, so a completed delete cannot leave those commands editing an earlier detached reference. No controlled delete-versus-submit interleaving test is included. Receipt upload, RefreshPolicy and mutable readers remain outside that guarantee. Lock entries are retained for the lifetime of the store, including deleted expense IDs. A database migration needs repository changes, a transaction/concurrency policy and durable work delivery; an in-memory lock cannot supply them. Queue failure leaves state unchanged because admission occurs before mutation, without a compensation write.
''',encoding='utf-8')
p=U/'README.md';t=p.read_text(encoding='utf-8');t+='\n## Open the learning sequence\n\nFollow the [map](01-CODEBASE-MAP.md), [concepts](02-CONCEPTS.md), [worked change](03-WORKED-CHANGE.md), [testing](04-TESTING-AND-DEBUGGING.md), [practice](05-PRACTICE.md), [answers and complete fixture](06-SOLUTIONS-AND-REVIEW.md), [trace](07-TRACE-LAB.md), and [verification](VERIFICATION.md). Compare the [expense service](../backend/Services/ExpenseService.cs), [queue](../backend/Background/BackgroundTaskQueue.cs), [worker](../backend/Background/BackgroundJobs.cs), and [actual tests](../backend/ExpenseManagement.Api.Tests/ExpenseWorkflowTests.cs). The final evidence includes both backend and frontend builds.\n';p.write_text(t,encoding='utf-8')
p=P/'README.md';t=p.read_text(encoding='utf-8-sig')
if 'astraupskill/README.md' not in t:t+='\n## CRUD workflow learning course\n\nRead the [detailed expense workflow course](astraupskill/README.md) for validation, authorization, mutable state, queue admission, actual regression fixtures and review exercises. [Verification](astraupskill/VERIFICATION.md) includes the ten-test result and build evidence.\n'
p.write_text(t,encoding='utf-8')
result={'passed':True,'total':10,'tests':10,'failed':0,'checks':labels,'scope':'Actual in-memory expense service, reimbursement delegate and capacity-one queue; ten xUnit facts, backend Release and frontend production builds. No HTTP/receipt/payment/database or controlled thread interleaving test.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
base=read(B/'baselines'/f'{ID}.json')['files'];changed=[n for n,h in base.items() if not(P/n).is_file() or sha(P/n)!=h]
canonical=B.parent.parent/'geminiorganized/OpenSource_Upskilling_.Ramp'
for n in changed:
 assert sha(canonical/n)==base[n],n
 if n!='README.md' and not any(sha(q)==base[n] for q in (U/'snapshots').iterdir() if q.is_file()):shutil.copyfile(canonical/n,U/'snapshots'/(n.replace('/','__')+'.before.txt'))
new=[]
for root,dirs,files in os.walk(P):
 dirs[:]=[d for d in dirs if d not in {'node_modules','.git','bin','obj','TestResults','dist','astraupskill'}]
 for f in files:
  n=(Path(root)/f).relative_to(P).as_posix()
  if n not in base:new.append(n)
assert set(new)=={'frontend/package-lock.json','backend/ExpenseManagement.Api.Tests/ExpenseManagement.Api.Tests.csproj','backend/ExpenseManagement.Api.Tests/ExpenseWorkflowTests.cs'},new
spec={'summary':['Validates and normalizes expense candidates and evaluates policy before mutating stored entities; rejected updates, submissions and reasons leave state unchanged.','Coordinates current-entity lookup, deletion, expense commands and reimbursement completion with a shared per-expense gate.','Adds nonblocking bounded-queue admission and worker-only transitions; rejected/throwing queues and repeated reimbursement commands avoid false state changes.','Adds ten actual service/worker/queue regressions, frontend lockfile, passing backend/frontend builds and nine detailed learning guides with complete examples.'],'changedFiles':changed+new+[p.relative_to(P).as_posix() for folder in [U/'snapshots',E] for p in folder.iterdir() if p.is_file()], 'checks':{'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':10},'limits':['Data and queue are in-memory and process-local; no durable outbox, real payment rail, database or cross-process guarantee.','Receipt upload, policy refresh and mutable readers retain races; lock entries remain for the store lifetime.','Tests call actual services/delegates with injected users, not HTTP/auth/hosted-worker/browser layers; duplicate jobs do not force simultaneous threads.']}
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
(C/'root-review-source-hashes.json').write_text(json.dumps({'files':{n:sha(P/n) for n in changed+new if not n.endswith('.md')}},indent=2),encoding='utf-8')
print(json.dumps({'changed':changed,'new':new,'tests':10,'files':len(spec['changedFiles'])+9}))
