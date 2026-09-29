from pathlib import Path
import json, hashlib, shutil
B=Path(__file__).resolve().parents[2]
ID='4ac741261ad5'; P=B/'stage'/ID; U=P/'astraupskill'; C=B/'checks'/ID
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
frozen=read(C/'root-review-source-hashes.json')['files']
assert all(sha(P/n)==h for n,h in frozen.items())
labels=['prisma_validate_v2','root-generate-01','root-verify-01']
E=U/'evidence'; E.mkdir(exist_ok=True)
for label in labels:
 r=read(C/(label+'.json')); assert r['status']=='complete' and r['exitCode']==0
 for ext in ['.json','.log']: shutil.copyfile(C/(label+ext),E/(label+ext))
result={'passed':True,'total':30,'tests':30,'failed':0,'domainTests':5,'apiServiceTests':16,'apiRouteTests':9,'checks':labels,'scope':'Mocked Prisma service tests, actual Express router and shared error middleware with mocked service/auth, domain tests, schema validation, client generation, workspace typechecks and builds. No live database or provider.'}
(C/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
(E/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
(U/'VERIFICATION.md').write_text('''# Verification and remaining limits

Run these commands from the project root after installing Node.js and npm. The recorded environment used Node 22.16.0. The connection string below is deliberately synthetic: generating a Prisma client and validating a schema do not establish a database connection. These checks did not run database push, migrations, seed, Redis, worker jobs, or a payment provider.

```powershell
npm ci
$env:DATABASE_URL = "postgresql://test:test@127.0.0.1:65432/unused"
npm run db:generate
node node_modules/prisma/build/index.js validate --schema packages/db/prisma/schema.prisma
npm run verify
```

`verify` first builds the domain and database packages so workspace imports can resolve their compiled entry points, then typechecks the workspaces, runs their tests, and builds all packages and applications. Running an API test directly before building its workspace dependencies can fail for setup reasons even when its source is valid. Read the first failing command rather than treating every later missing-import error as a separate bug.

The final [verification record](evidence/root-verify-01.json) and [complete output](evidence/root-verify-01.log) report exit code zero. All **30 tests passed**: five existing domain tests, sixteen payment-service tests, and nine HTTP-route tests. The service suite checks tenant ownership, changed-payload replay, valid payment failure, late failure after success, missing invoices, rejected draft/void invoice transitions, valid uncollectible payment, strict payload rejection, and bounded retries for Prisma conflict codes. The route suite exercises an actual Express router, JSON parser, and the shared error middleware; its payment service and permission function are mocked. It verifies expected domain errors remain useful 400/403/409 responses while unexpected errors become a safe 500 response.

The [schema validation](evidence/prisma_validate_v2.log) and [client generation](evidence/root-generate-01.log) also passed. The full build compiled API, worker, shared packages, and the Vite frontend. These are compilation results; they do not demonstrate browser interaction or a running worker. [The machine-readable summary](evidence/results.json) states the same scope and test counts.

Prisma transaction callbacks are mocked in the service tests. They prove calls, arguments, decisions, and retry limits, but cannot prove PostgreSQL rollback, concurrent serialization, row locks, or durability. A separate disposable PostgreSQL test database is the next useful integration exercise: inject an audit-write failure and verify no payment, invoice, event, or outbox write commits; then race two identical provider event IDs. The current synthetic provider route has no real signature verification, and demo headers are not production authentication. Full application membership wiring is not covered by the route fixture. Subscription idempotency and count-based invoice numbering retain their pre-existing race risks. Review these boundaries before describing the project as production-ready.
''',encoding='utf-8')
p=U/'03-WORKED-CHANGE.md'; t=p.read_text(encoding='utf-8'); p.write_text(t.replace('independently authorized integration environment','separate disposable PostgreSQL test database'),encoding='utf-8')
baseline=read(B/'baselines'/f'{ID}.json')['files']
changed=[n for n,h in baseline.items() if not (P/n).exists() or sha(P/n)!=h]
assert set(changed)==set(frozen).intersection(baseline)|{'README.md'},changed
spec={'summary':[
'Scopes mock payment processing to the organization and validates global provider-event ownership and payload identity before replay.',
'Keeps payment, invoice, provider event, audit and outbox writes in one Serializable transaction with bounded conflict retries, and prevents invalid invoice transitions or late failure regression.',
'Maps explicit domain and HTTP errors to useful client responses while sanitizing unexpected failures; preserves expected money, permission, subscription and idempotency errors.',
'Adds 25 API regression tests alongside five domain tests, with nine detailed learning chapters, complete worked test examples, exact original snapshots and portable evidence.'
], 'changedFiles':list(dict.fromkeys(changed+list(frozen)+[p.relative_to(P).as_posix() for folder in [U/'snapshots',E] for p in folder.iterdir() if p.is_file()])), 'checks':{'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':30},'limits':[
'Synthetic payment provider and demo header authentication; no provider signature verification or external service was exercised.',
'Mock Prisma callbacks establish control-flow and write arguments, not database rollback, durability or concurrency guarantees.',
'HTTP tests use the actual router/parser/shared error handler with mocked service and permissions; full application membership wiring and browser interaction remain untested.',
'Subscription idempotency and count-based invoice numbering retain pre-existing race risks; no live database, migration, worker or Redis was run.'
]}
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
print(json.dumps({'changedBaseline':changed,'files':len(spec['changedFiles']),'courseWords':sum(len(p.read_text(encoding='utf-8').split()) for p in U.glob('*.md') if p.name in ['README.md','01-CODEBASE-MAP.md','02-CONCEPTS.md','03-WORKED-CHANGE.md','04-TESTING-AND-DEBUGGING.md','05-PRACTICE.md','06-SOLUTIONS-AND-REVIEW.md','07-TRACE-LAB.md','VERIFICATION.md'])}))
