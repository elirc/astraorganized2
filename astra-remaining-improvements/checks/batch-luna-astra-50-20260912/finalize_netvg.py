from pathlib import Path
import json,hashlib,shutil,xml.etree.ElementTree as ET
B=Path(__file__).resolve().parents[2]; ID='9e7b2d32e0fb'; P=B/'stage'/ID; U=P/'astraupskill'; E=U/'evidence'; C=B/'checks'/ID
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig')); sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
E.mkdir(exist_ok=True)
labels=['root-restore-01','root-dotnet-test-02','root-request-tests-01','root-web-build-03','root-api-build-02']
for label in labels:
 r=read(C/(label+'.json')); assert r['status']=='complete' and r['exitCode']==0,r
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
trx=P/'tests/PeblClone.Application.Tests/TestResults/root-tests-02.trx'
counts=ET.parse(trx).find('.//{*}Counters').attrib
assert counts['total']==counts['passed']=='14' and counts['failed']=='0'
shutil.copyfile(trx,E/'application-tests.trx')
assert '# tests 3' in (C/'root-request-tests-01.log').read_text() and '# pass 3' in (C/'root-request-tests-01.log').read_text()
result={'passed':True,'total':17,'tests':17,'failed':0,'checks':labels,'scope':'14 application xUnit cases (13 calculator and one dashboard), three actual RequestGate Node cases using deferred promises; API Release and web builds passed. No mounted React or HTTP integration test.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
for p in U.glob('*.md'):
 t=p.read_text(encoding='utf-8').replace('the staged project','the project').replace('the staged profile','the demo profile').replace('the staged project root','the project root')
 t=t.replace('Explain why only one case may use a mock fallback.','Explain why none of these quote-creation cases may use a mock fallback, while dashboard loading has a different contract.')
 t=t.replace('The recorded root check is 14 xUnit tests passing with TRX.','The recorded suite has 14 xUnit cases passing with TRX: 13 calculator cases shown above and one existing dashboard composition case.')
 t=t.replace('This fixture proves exact totals, availability text, enum guarding, compensation rejection, normalization, rounding, copied requirements, and syntax validation.','This fixture checks exact totals, availability text, enum guarding, compensation rejection, normalization, ordinary rounding, copied requirements, and invalid inputs. The rounding sample is not a midpoint, so it does not distinguish AwayFromZero from ToEven. The two-character D! sample reaches unsupported-country lookup rather than a letter-only syntax gate.')
 p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md'; t=p.read_text(encoding='utf-8')
start=t.index('Exercise 7:'); end=t.index('For review,',start)
t=t[:start]+'''Exercise 7's overlapping-request trace permits token 1's initial loading reset and token 2's newer loading reset. Token 2 may commit success and clear loading. Token 1's later success and finally block are both suppressed. In the edit trace, invalidation immediately clears the preview and loading state; the old rejection must not add an error. Gating only try/catch leaves a bug: token 1's finally could stop the spinner while token 2 is still pending.

Exercise 8's verification note should name root-dotnet-test-02 (14 cases), root-request-tests-01 (three cases), and root-web-build-03 (compilation and bundle). No component was mounted, so alert rendering and browser navigation remain untested. EUR and USD are labels on synthetic values with no conversion. The later root-api-build-02 also passed after an OpenAPI dependency patch; a build is not an additional unit test.

''' + t[end:];p.write_text(t,encoding='utf-8')
p=U/'VERIFICATION.md';t=p.read_text(encoding='utf-8');t=t.replace('cd src/PeblClone.Web','dotnet build src/PeblClone.Api/PeblClone.Api.csproj -c Release\ncd src/PeblClone.Web',1)
start=t.index('Before handoff,');end=t.index('**Exercise 8.**',start)
t=t[:start]+'''Read the [portable results](evidence/results.json), [application test log](evidence/root-dotnet-test-02.log), [Node test log](evidence/root-request-tests-01.log), [web build](evidence/root-web-build-03.log), and [API build](evidence/root-api-build-02.log). These files preserve the recorded run; their absolute working directories describe the review environment, while the commands above work from this project's root. Inspect application-tests.trx alongside the log when checking discovery counts. The application suite includes thirteen calculator cases and one existing dashboard case.

The API initially failed restore because Microsoft.OpenApi 2.0.0 triggered warning-as-error NU1903. The final project explicitly selects 2.7.5 in Directory.Packages.props and references it in the API project. This is the patched 2.x release identified in [Microsoft's advisory](https://github.com/microsoft/OpenAPI.NET/security/advisories/GHSA-v5pm-xwqc-g5wc); warning enforcement stays enabled. The final API build restored dependencies and passed. This targeted repair is not a claim that every dependency has been independently security-audited.

''' +t[end:];p.write_text(t,encoding='utf-8')
p=P/'README.md';t=p.read_text(encoding='utf-8-sig')
if 'astraupskill/README.md' not in t:p.write_text(t+'\n\n## CRUD engineering learning course\n\nFollow the [workforce quote course](astraupskill/README.md) for server validation, honest API errors, stale response handling, complete test examples, exercises, and recorded verification.\n',encoding='utf-8')
base=read(B/'baselines'/f'{ID}.json')['files']; changed=[n for n,h in base.items() if not(P/n).is_file() or sha(P/n)!=h]
new=['src/PeblClone.Web/src/services/requestGate.ts','src/PeblClone.Web/tests/request-gate.test.mjs']
canonical=B.parent.parent/'_Organized Desktop/01 Net Workspaces/.netvg'
for n in changed:
 assert sha(canonical/n)==base[n],n
 if n!='README.md' and not any(sha(q)==base[n] for q in (U/'snapshots').iterdir() if q.is_file()):shutil.copyfile(canonical/n,U/'snapshots'/(n.replace('/','__')+'.before.txt'))
spec=read(B/'specs'/f'{ID}.json')
spec['changedFiles']=changed+new+[p.relative_to(P).as_posix() for folder in [U/'snapshots',E] for p in folder.iterdir() if p.is_file()]
spec['checks']={'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':17}
spec['summary'].append('Repairs API restore by selecting patched Microsoft.OpenApi 2.7.5 without suppressing warnings; final API and web builds pass.')
spec['limits']=['Country profiles, pricing rates and currency labels are synthetic; no currency conversion or payroll/compliance verification.','No authentication, quote persistence, database, audit log or external provider is added. Dashboard retains its labeled mock fallback.','The three Node tests exercise the real request gate with deferred promises, not mounted React; endpoint HTTP behavior and browser interactions remain source-reviewed.','Decimal costs are rounded to two places but compensation and total retain submitted precision. Current arithmetic case is not a midpoint-specific rounding test; cancellation and duplicate-profile invariants are untested extensions.']
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
(C/'root-review-source-hashes.json').write_text(json.dumps({'files':{n:sha(P/n) for n in changed+new if n!='README.md'}},indent=2),encoding='utf-8')
print(json.dumps({'changed':changed+new,'tests':17,'files':len(spec['changedFiles'])+9}))
