from pathlib import Path
import json,hashlib,shutil,xml.etree.ElementTree as ET,os
B=Path(__file__).resolve().parents[2];ID='028086674b89';P=B/'stage'/ID;U=P/'astraupskill';E=U/'evidence';C=B/'checks'/ID
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
E.mkdir(exist_ok=True)
labels=['luna-restore-01','luna-test-10','root-build-01']
for label in labels:
 r=read(C/(label+'.json'));assert r['status']=='complete' and r['exitCode']==0,r
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
trx=P/'tests/Netgum.Tests/TestResults/netgum-luna-test-10.trx'; counts=ET.parse(trx).find('.//{*}Counters').attrib
assert counts['total']==counts['passed']=='11' and counts['failed']=='0';shutil.copyfile(trx,E/'netgum-tests.trx')
result={'passed':True,'total':11,'tests':11,'failed':0,'checks':labels,'scope':'Eight application cases using real repositories and EF InMemory with counting gateway/email/unit-of-work doubles, plus three domain cases. Release solution build passed. net8 tests ran with Major roll-forward on net10; no relational transaction or real provider test.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
p=U/'README.md';t=p.read_text(encoding='utf-8');t+='''
## Open the code while studying

Follow the [map](01-CODEBASE-MAP.md), [concepts](02-CONCEPTS.md), [worked repair](03-WORKED-CHANGE.md), [tests](04-TESTING-AND-DEBUGGING.md), [practice](05-PRACTICE.md), [solutions](06-SOLUTIONS-AND-REVIEW.md), [trace](07-TRACE-LAB.md), and [verification](VERIFICATION.md). Compare the [actual checkout service](../src/Netgum.Application/Checkout/CheckoutService.cs), [order aggregate](../src/Netgum.Domain/Orders/Order.cs), and [executable regression fixture](../tests/Netgum.Tests/Application/CheckoutServiceTests.cs). A sequential repeat of an already-paid order avoids another email; this does not mean concurrent pending requests or a failed email send have durable delivery guarantees.
''';p.write_text(t,encoding='utf-8')
p=U/'07-TRACE-LAB.md';t=p.read_text(encoding='utf-8').replace('grants ten percent with a five-dollar minimum discount','grants ten percent with a maximum of five redemptions and no fixed-dollar discount')
t=t.replace('The money value rounds according to the domain money implementation, producing the total asserted by the successful test.','Money.Create rounds 2.205 away from zero to 2.21, producing 46.31 USD total. The existing no-coupon success case asserts 51.45 USD; this coupon trace is a worked calculation, while its repeated-completion test asserts the side-effect counters and stock/redemption state.')
t=t.replace('If `email.Calls` becomes two, the email send is below the terminal guard.','If `email.Calls` becomes two, inspect whether a terminal call can reach the email send instead of returning from the guard.')
p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8');start=t.index('## Complete unavailable-variant solution');end=t.index('## Complete repeated-completion assertions',start)
t=t[:start]+'''## Complete executable fixture

The following is the complete current `tests/Netgum.Tests/Application/CheckoutServiceTests.cs`, including imports, namespace, fixture graph and helper doubles. These tests already exist: modify the original methods when practicing instead of adding duplicate method names. Sold-out and inactive variants are separate cases so one guard cannot hide a failure in the other. The original no-coupon case provides a positive total assertion; the valid coupon case covers reservation, redemption and sequential repeated completion.

```csharp
'''+(P/'tests/Netgum.Tests/Application/CheckoutServiceTests.cs').read_text(encoding='utf-8')+'```\n\n'+t[end:]
t+='''
## What a receipt retry cannot guarantee yet

The service saves Paid before sending the receipt. If the sender throws, the order is already paid; a later call returns early and does not retry the email. Two callers that both loaded Pending can also reach provider/save/email work concurrently because no database version predicate coordinates them. The eleven tests cover sequential service calls, not either failure window. A future outbox should persist a unique order-paid delivery record with the state change and let a retrying worker record delivery attempts; provider idempotency and database concurrency need separate tests. Do not move the email before SaveChanges as a shortcut: that creates a receipt for an order whose paid state may never commit.

Product names are read from the current product on each successful receipt response; they are not frozen on the order. Sequential equivalence in the test assumes the product name has not changed. Coupon eligibility uses the captured command time both before and after the provider await, and the second preflight inspects the same tracked object. It neither refreshes another DbContext's writes nor establishes wall-clock expiry at payment-provider completion.
''';p.write_text(t,encoding='utf-8')
p=U/'VERIFICATION.md';t=p.read_text(encoding='utf-8');t+='''
The authoritative [results summary](evidence/results.json), [test output](evidence/luna-test-10.log), [TRX counters](evidence/netgum-tests.trx), and [Release build output](evidence/root-build-01.log) are included locally. Eleven discovered cases passed: eight application cases and three domain cases. Earlier failed or empty-output attempts are not the final evidence. No tests were added for production identity, the email failure window, two simultaneous pending completions, or relational rollback. Read the failure-ledger limits in the solutions before treating sequential idempotency as a stronger guarantee.
''';p.write_text(t,encoding='utf-8')
base=read(B/'baselines'/f'{ID}.json')['files'];changed=[n for n,h in base.items() if not(P/n).is_file() or sha(P/n)!=h]
canonical=B.parent.parent/'_Organized Desktop/01 Net Workspaces/.netgum'
for n in changed:
 assert sha(canonical/n)==base[n],n
 if n!='README.md' and not any(sha(q)==base[n] for q in (U/'snapshots').iterdir() if q.is_file()):shutil.copyfile(canonical/n,U/'snapshots'/(n.replace('/','__')+'.before.txt'))
new=[]
for root,dirs,files in os.walk(P):
 dirs[:]=[d for d in dirs if d not in {'node_modules','.git','bin','obj','TestResults','astraupskill','.vs'}]
 for f in files:
  n=(Path(root)/f).relative_to(P).as_posix()
  if n not in base:new.append(n)
assert not new,new
spec={'summary':['Validates customer, product, variant and coupon inputs before the payment gateway and constructs a valid pending order before inventory/coupon mutations.','Introduces reusable domain preflight methods and converts malformed email parsing into the expected DomainException contract.','Returns persisted paid/failed receipts before repeating provider, save or email work on sequential completion retries.','Adds real application regression cases with EF repositories, state assertions and gateway/email/save counters, plus nine detailed learning chapters and complete test examples.'], 'changedFiles':changed+[p.relative_to(P).as_posix() for folder in [U/'snapshots',E] for p in folder.iterdir() if p.is_file()], 'checks':{'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':11}, 'limits':['EF InMemory tests do not establish SQL constraints, transactions, cross-context stock concurrency or provider compensation.','Captured-time revalidation reads the same tracked aggregate after the provider await; a created provider intent can remain after later rejection or save failure.','Sequential terminal retries are covered; concurrent pending completions can duplicate work. Paid is saved before email, so a failed send is not retried by completion; no durable outbox is added.','Product mutation endpoints retain demo authentication gaps; download remains an ID-holder capability after paid status. No real payment or email provider was used.']}
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
(C/'root-review-source-hashes.json').write_text(json.dumps({'files':{n:sha(P/n) for n in changed if not n.endswith('.md')}},indent=2),encoding='utf-8')
print(json.dumps({'changed':changed,'tests':11,'files':len(spec['changedFiles'])+9}))
