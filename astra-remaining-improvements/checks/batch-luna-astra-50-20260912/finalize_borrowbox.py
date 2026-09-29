from pathlib import Path
import json,hashlib,shutil,xml.etree.ElementTree as ET
B=Path(__file__).resolve().parents[2];ID='5426644ec395';P=B/'stage'/ID;C=B/'checks'/ID;U=P/'astraupskill';E=U/'evidence';D=B.parent.parent/'borrowbox'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
labels=['luna-restore-01','luna-test-04','root-build-02']
for label in labels:
 r=read(C/(label+'.json'));assert r['status']=='complete' and r['exitCode']==0
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
suites=[]
for p in P.rglob('borrowbox-luna-test-04.trx'):
 c=ET.parse(p).find('.//{*}Counters');assert c is not None
 assert int(c.attrib['total'])==int(c.attrib['passed']) and int(c.attrib['failed'])==0
 name=p.parents[1].name+'.trx';shutil.copyfile(p,E/name);suites.append({'suite':p.parents[1].name,'tests':int(c.attrib['total']),'evidence':'astraupskill/evidence/'+name})
assert len(suites)==3 and sum(x['tests'] for x in suites)==29,suites
result={'passed':True,'total':29,'tests':29,'failed':0,'suites':suites,'checks':labels,'scope':'6 Core,19 Infrastructure and4 in-process API tests; in-memory stores and existing fake race seam. Full Release build passed. No durable database transaction, production authentication or browser test.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
for p in U.glob('*.md'):
 t=p.read_text(encoding='utf-8').replace('a .NET 8 equipment lending demo','a .NET 10 equipment lending demo')
 t=t.replace('Authorization: Bearer demo','X-Demo-Role: Student')
 t=t.replace('and requires the Staff policy.', 'and requires an authenticated demo identity; both Student and Staff satisfy this endpoint\'s default policy.')
 t=t.replace('The current API’s `RequireAuthorization` policy is a coarse Staff gate.', 'These reservation and loan endpoints use the default authenticated-user policy. The named Staff policy is applied separately to selected administrative endpoints, such as equipment retirement.')
 t=t.replace('The repaired method then computes `var reservedAt = (clock ?? new SystemClock()).UtcNow` and constructs a `Reservation` using that time and the requested expiry.', 'The repaired method constructs a `Reservation` with one `(clock ?? new SystemClock()).UtcNow` read and the requested expiry.')
 t=t.replace('The service also checks `equipment.Status == CheckedOut` before changing the loan.', 'The service first preserves the `loan.already_returned` rejection, then checks `equipment.Status == CheckedOut` before changing the active loan.')
 t=t.replace('It loads loan and equipment, checks equipment is CheckedOut, and calls `Loan.Return(now)`.', 'It loads the loan, rejects an already returned loan, then loads equipment, checks CheckedOut state, and calls `Loan.Return(now)`.')
 t=t.replace('The candidate constructor is the final fallible step before an equipment state transition.', 'The candidate constructor validates input before an equipment state transition; the equipment operation can still reject an unavailable item.')
 p.write_text(t,encoding='utf-8')
p=U/'README.md';p.write_text(p.read_text(encoding='utf-8')+'''\n## Follow the code with the course

Open the [map](01-CODEBASE-MAP.md), [concepts](02-CONCEPTS.md), [worked change](03-WORKED-CHANGE.md), [debugging guide](04-TESTING-AND-DEBUGGING.md), [practice](05-PRACTICE.md), [solutions](06-SOLUTIONS-AND-REVIEW.md), [trace lab](07-TRACE-LAB.md) and [verification](VERIFICATION.md). Compare the [loan workflow](../src/BorrowBox.Core/Loans/Loan.cs) with its [original snapshot](snapshots/Loan-before.cs.txt), then read the [actual checkout tests](../tests/BorrowBox.Infrastructure.Tests/Loans/CheckoutTests.cs). The final test run includes 29 tests across three projects.
''',encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8');t+='''\n## Complete reservation fixture

This is the complete current `tests/BorrowBox.Infrastructure.Tests/Reservations/ReservationTests.cs`, including imports and its fixed clock. The cases already exist in the delivered project: read or modify them there rather than adding duplicates. They demonstrate the successful cancel path, invalid expiry before equipment mutation, and a mismatched equipment state. The return excerpt above belongs inside `CheckoutTests` with the setup shown in `ReturnBeforeCheckout_DoesNotChangeEitherEntity`; it is an assertion excerpt, not a standalone test.

```csharp
'''+(P/'tests/BorrowBox.Infrastructure.Tests/Reservations/ReservationTests.cs').read_text(encoding='utf-8')+'```\n';p.write_text(t,encoding='utf-8')
(U/'VERIFICATION.md').write_text('''# Verification and limits

Run from the BorrowBox project root with the .NET 10 SDK installed. The checked-in `global.json` selects SDK 10.0.302 with patch roll-forward. The project target is net10.0; the recorded tests used the installed .NET 10 runtime, so the explicit `DOTNET_ROLL_FORWARD=Major` in the command record did not require a newer target runtime.

```powershell
dotnet restore BorrowBox.slnx
dotnet test BorrowBox.slnx --configuration Release --no-restore --logger "trx;LogFileName=local-tests.trx"
dotnet build BorrowBox.slnx --configuration Release --no-restore
```

Restore must finish before testing. A test command issued with missing test SDK assets can return zero without running tests. Require an actual test summary and inspect the TRX counters. The authoritative [test output](evidence/luna-test-04.log) and [results summary](evidence/results.json) establish **29 passed tests**: six Core tests, nineteen Infrastructure tests and four API tests. Each suite's TRX file is included beside the output. The [final Release build](evidence/root-build-02.log) also passed. Earlier empty-output runs do not establish a passing test count.

The infrastructure cases exercise invalid expiry, invalid due date, early return, repeated return, mismatched cancellation/expiry state, positive lifecycle paths, and existing checkout competition. The competition test uses a coordinated fake equipment-store implementation; it verifies that the service respects a single winner from `TryCheckOutAsync`. It does not establish database serialization or borrower-limit atomicity across different equipment.

The four API tests use `WebApplicationFactory` and an in-process test server. They exercise equipment create/get, readiness metadata, and unauthorized/forbidden retirement. They do start the application test host, whose registered hosted services participate in its lifecycle, but do not establish periodic expiry-worker reliability. No external listener, live account or production service was used.

For a narrower repeat after restore, quote the filter so PowerShell does not interpret its pipe:

```powershell
dotnet test tests/BorrowBox.Infrastructure.Tests/BorrowBox.Infrastructure.Tests.csproj --configuration Release --no-restore --filter "FullyQualifiedName~Reservations|FullyQualifiedName~Loans"
```

The default stores hold mutable references and lose state on restart. Validation ordering prevents the expected rejected inputs from changing equipment first; it does not roll back a later `SaveAsync` or `AddAsync` failure. SQLite equipment persistence is not selected. Reservation and loan stores have no transaction/save contract. Real authentication, borrower-to-actor authorization, tenant scoping, multi-record durability and a shared coordinator remain follow-up work. The future versioned command in the exercises is a design proposal, not an implemented feature.
''',encoding='utf-8')
base=read(B/'baselines'/f'{ID}.json')['files'];changed=[n for n,h in base.items() if not(P/n).is_file() or sha(P/n)!=h]
for n in changed:
 assert sha(D/n)==base[n],n
 if not any(sha(q)==base[n] for q in (U/'snapshots').iterdir() if q.is_file()):shutil.copyfile(D/n,U/'snapshots'/(n.replace('/','__')+'.before.txt'))
p=P/'README.md';t=p.read_text(encoding='utf-8-sig')
if 'astraupskill/README.md' not in t:p.write_text(t+'\n\n## Lifecycle learning course\n\nRead the [nine-chapter CRUD engineering course](astraupskill/README.md) for validation ordering, time boundaries, complete tests, exercises and verified limits.\n',encoding='utf-8');changed.append('README.md')
spec=read(B/'specs'/f'{ID}.json');spec['changedFiles']=list(dict.fromkeys(changed+[p.relative_to(P).as_posix() for folder in [U/'snapshots',E] for p in folder.iterdir() if p.is_file() and not p.name.startswith('test-02')]))
spec['checks']={'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':29}
spec['limits']=[s.replace('Demo header Staff policy', 'Demo header authentication and selected Staff policies') for s in spec['limits']]
spec['limits'].append('API tests use an in-process application host; lifecycle endpoint date/error mapping and browser behavior remain source-reviewed rather than newly integrated HTTP tests.')
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
(C/'root-review-source-hashes.json').write_text(json.dumps({'files':{n:sha(P/n) for n in changed if n!='README.md'}},indent=2),encoding='utf-8')
print(json.dumps({'changed':changed,'tests':29,'suites':suites}))
