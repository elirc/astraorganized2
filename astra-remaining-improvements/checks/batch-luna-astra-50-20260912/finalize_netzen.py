from pathlib import Path
import json,hashlib,shutil,xml.etree.ElementTree as ET
B=Path(__file__).resolve().parents[2];ID='1bb35a95be79';P=B/'stage'/ID;U=P/'astraupskill';E=U/'evidence';C=B/'checks'/ID
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
E.mkdir(exist_ok=True)
labels=['root-dotnet-test-01','root-web-types-01','root-web-build-02']
for label in labels:
 r=read(C/(label+'.json'));assert r['status']=='complete' and r['exitCode']==0,r
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
trx=P/'support-ticketing-app/backend/SupportDesk.Api.Tests/TestResults/root-tests.trx'; counts=ET.parse(trx).find('.//{*}Counters').attrib
assert counts['total']==counts['passed']=='3' and counts['failed']=='0';shutil.copyfile(trx,E/'ticket-safety-tests.trx')
result={'passed':True,'total':3,'tests':3,'failed':0,'checks':labels,'scope':'Actual domain and in-memory search regression cases. API compiled through test project; frontend TypeScript and Vite build passed. .NET8 tests ran with Major roll-forward on .NET10. No live hub, HTTP server or browser tests.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
for p in U.glob('*.md'):
 t=p.read_text(encoding='utf-8').replace('the staged project','the project')
 t=t.replace('after React types and `vite-env` were added','after React type dependencies were added; the existing `vite-env.d.ts` is retained')
 t=t.replace('using the committed `package-lock.json`','using the included `package-lock.json`')
 t=t.replace('Add a diagnostic assertion to the search test showing that `result.Items[0].Number` is `T-000001`, then explain','Locate the diagnostic assertion in the search test showing that `result.Items[0].Number` is `T-000001`, then explain')
 p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8');start=t.index('Exercise 6:');end=t.index("Exercise 8's",start)
t=t[:start]+'''Exercise 6's database replacement must define one authorized result population before Count, Skip and Take. Express the existing read policy in the query, keep internal comment bodies out of customer text matches, and use a deterministic order with an ID tie-breaker. Test the same 121-ticket case against a disposable database and add page-boundary, total-count, role, team and internal-marker cases. Document whether pages are a snapshot or may shift during writes; the current implementation does not promise a cross-page snapshot. Public-comment-only text search currently applies to staff too, so restoring internal-note search for staff requires an explicit actor-aware query rather than removing the predicate globally.

Exercise 7's timeline starts with an authorized agent submitting an internal note at version 3. The store locks, validates version, mutates a copy, then commits version 4. The notifier emits only tickets.changed. Each browser refetches its authorized list and selected detail. The hub callback calls setSelected for a current detail response while leaving commentBody and the other draft variables unchanged. A second writer holding version 3 fails at the store version comparison before its mutation; no successful notification follows that rejected command. A notification arriving during downtime is not durably replayed: reconnect rejoins and refetches current state instead.

''' +t[end:];p.write_text(t,encoding='utf-8')
p=U/'VERIFICATION.md';t=p.read_text(encoding='utf-8');start=t.index('Before handoff,');end=t.index('**Exercise 8.**',start)
t=t[:start]+'''Read the [results summary](evidence/results.json), [backend test output](evidence/root-dotnet-test-01.log), [TRX report](evidence/ticket-safety-tests.trx), and [frontend build output](evidence/root-web-build-02.log). The logs preserve their actual review working directories; use the portable commands above on your copy. Verify that the test run discovers three cases rather than assuming an empty successful command ran tests. The build includes two Rollup comments about SignalR purity annotations; they did not prevent the bundle from being produced.

Search text currently excludes internal comments for every actor, including agents. This avoids the customer marker leak but makes staff internal-note search unavailable. Browser request counters protect list refreshes and hub-triggered detail refreshes; the existing user-driven openTicket and mutation completion paths do not share a universal request coordinator. Tests have not established behavior for every selection or mutation race. Capture those cases before extending the UI so a locally correct change does not claim broader guarantees.

''' +t[end:];p.write_text(t,encoding='utf-8')
base=read(B/'baselines'/f'{ID}.json')['files'];changed=[n for n,h in base.items() if not(P/n).is_file() or sha(P/n)!=h]
canonical=B.parent.parent/'_Organized Desktop/01 Net Workspaces/.netzen'
for n in changed:
 assert sha(canonical/n)==base[n],n
 if not any(sha(q)==base[n] for q in (U/'snapshots').iterdir() if q.is_file()):shutil.copyfile(canonical/n,U/'snapshots'/(n.replace('/','__')+'.before.txt'))
new=['support-ticketing-app/backend/SupportDesk.Api.Tests/SupportDesk.Api.Tests.csproj','support-ticketing-app/backend/SupportDesk.Api.Tests/TicketSafetyTests.cs','support-ticketing-app/frontend/package-lock.json']
entry=P/'support-ticketing-app/README.md'
if entry.exists():
 t=entry.read_text(encoding='utf-8-sig')
 if '../astraupskill/README.md' not in t:entry.write_text(t+'\n\n## Ticket engineering course\n\nRead the [detailed CRUD learning course](../astraupskill/README.md) for safe mutations, permissions, pagination, live refreshes, complete test examples and practice solutions.\n',encoding='utf-8');changed.append(entry.relative_to(P).as_posix())
spec=read(B/'specs'/f'{ID}.json');spec['changedFiles']=changed+new+[p.relative_to(P).as_posix() for folder in [U/'snapshots',E] for p in folder.iterdir() if p.is_file()]
spec['summary']=['Materializes normalized tags before mutation and rejects undefined status, priority and comment visibility values.','Filters the authorized population across source pages before final pagination and excludes internal-comment text from search.','Replaces broad ticket payloads with data-free SignalR invalidations, refetches selected detail, rejoins on reconnect, and suppresses stale list and hub detail refreshes while preserving drafts.','Adds real domain/search regression tests, missing React type dependencies, a frontend lockfile and nine detailed learning chapters with worked examples and matched exercises.']
spec['checks']={'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':3}
spec['limits']=['In-memory storage and demo identity headers remain; no real authentication, database, tenant hardening or durable outbox.','Search aggregates all source pages in memory and is not an atomic snapshot across writes. Internal-comment text is excluded for staff too.','Three focused backend tests do not establish the complete actor policy, HTTP behavior, SignalR connection behavior or browser rendering.','Request counters cover list and hub detail refreshes; existing user-driven selection and mutation races remain. Creation-time priority fallback remains unchanged.']
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
(C/'root-review-source-hashes.json').write_text(json.dumps({'files':{n:sha(P/n) for n in changed+new if not n.endswith('.md')}},indent=2),encoding='utf-8')
print(json.dumps({'changed':changed+new,'tests':3,'files':len(spec['changedFiles'])+9}))
