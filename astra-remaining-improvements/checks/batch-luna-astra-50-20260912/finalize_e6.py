from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parents[2];ID='20574f0b81b4';P=B/'stage'/ID;U=P/'astraupskill';C=B/'checks'/ID;E=U/'evidence'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
labels=['root-build-01','root-api-build-03','root-test-05']
for label in labels:
 r=read(C/(label+'.json'));assert r['status']=='complete' and r['exitCode']==0
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
assert '# tests 8' in (C/'root-test-05.log').read_text(encoding='utf-8')
result={'passed':True,'total':8,'tests':8,'failed':0,'checks':labels,'scope':'Synthetic independent stores, actual socket handler registration with fake transport, actual Fastify app.inject GET/PATCH responses and close hook. Full original frontend/domain/worker build plus final changed API build passed. No real database, network listener, worker or browser.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
p=U/'README.md';t=p.read_text(encoding='utf-8').replace('No Fastify HTTP request is injected by the delivered suite.', 'A further test injects three requests into the real Fastify app and closes it afterward, without opening a listener.');p.write_text(t,encoding='utf-8')
p=U/'04-TESTING-AND-DEBUGGING.md';t=p.read_text(encoding='utf-8').replace('seven Node tests','eight Node tests').replace('The suggestions above about Fastify `app.inject`, repeated client message IDs and additional planner assertions are extension exercises unless present in those files.', 'The eighth test uses real Fastify `app.inject` calls to verify a valid bootstrap (200), denied workspace (403), and missing issue (404). Repeated client message IDs and additional planner assertions remain extension exercises unless present in those files.');p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8');start=t.index('```ts\n',t.index('## Runnable fixtures'));end=t.index('```',start+6);test=(P/'apps/api/tests/boundaries.test.ts').read_text(encoding='utf-8');t=t[:start]+'```ts\n'+test+'```'+t[end+3:];t=t.replace("Exercise 7's duplicate-message extension and exercise 9's HTTP integration are not counted as executed coverage.", "Exercise 7's duplicate-message extension remains proposed. Exercise 9 now has a real HTTP injection case at the end of this file; it verifies the status mapping but does not start a network listener or database.");t=t.replace('Exercise 9 remains proposed because app.inject and a fake store do not certify a real database or distributed socket adapter.', 'Exercise 9 now includes real Fastify injection in the complete file below. It does not certify a real database or distributed socket adapter.');p.write_text(t,encoding='utf-8')
(U/'VERIFICATION.md').write_text('''# Verification and remaining limits

Run these commands from the project root with Node.js and npm installed. The recorded runtime used Node 22.16.0. The API stores synthetic records in memory; the checks below do not need PostgreSQL, Redis, Slack, a payment provider or a browser. The workspace build compiles the domain, API, Next web application and worker. It does not start the worker or apply a database schema.

```powershell
npm ci
npm run build
node node_modules/tsx/dist/cli.mjs --test apps/api/tests/security.test.ts apps/api/tests/boundaries.test.ts
```

Building the domain first makes its compiled workspace entry point available to the API and tests. For a focused API repeat after that initial build, use `npm run build --workspace @workspace/api`. Tests are invoked explicitly because the original root package has no test script. They use Node's test runner through the installed `tsx` loader, not Vitest or a browser runner.

The final [test record](evidence/root-test-05.json) and [complete test output](evidence/root-test-05.log) show **eight tests passed**. Four tests cover settings denial, create-reference rejection, recipient-scoped notification updates and per-socket registry cleanup. Three cover isolated-store positive CRUD and inbox projection, rejected updates with unchanged state, and actual socket registration with a fake transport. The eighth injects real requests into Fastify, checks successful bootstrap and 403/404 error responses, and closes the app in a `finally` block. It does not bind a network port.

The [full workspace build](evidence/root-build-01.log) passed before the final API-only review fixes. The [final API build](evidence/root-api-build-03.log) compiled those fixes, including typed store errors, issue-type status validation and the callable socket registration seam. The frontend, worker and domain source did not change after their successful build. The [results summary](evidence/results.json) records this distinction rather than implying the earlier full build included later API edits.

Expected access and missing-record failures in the repaired store paths carry `statusCode` through `StoreError`, which Fastify maps to useful client responses. Existing endpoints outside those paths retain their prior policies. The demo still uses a fixed current user and simulated authentication; no test establishes a real user session or tenant isolation across authenticated accounts. In-memory records remain mutable references and disappear on restart. The planner side effect is not a durable transaction. Presence is local to one server instance, and fake socket tests do not establish Redis adapter, reconnection or packet-order behavior. Explicit null clearing, durable idempotency and a complete per-endpoint permission matrix remain follow-up exercises.
''',encoding='utf-8')
p=P/'README.md';t=p.read_text(encoding='utf-8-sig') if p.exists() else '# e6 Workspace Platform\n'
if 'astraupskill/README.md' not in t:p.write_text(t+'\n\n## Learning course\n\nFollow the [CRUD engineering course](astraupskill/README.md) for membership, relation validation, inbox projections, socket ownership, worked tests and verification limits.\n',encoding='utf-8')
baseline=read(B/'baselines'/f'{ID}.json')['files'];changed=[n for n,h in baseline.items() if not(P/n).is_file() or sha(P/n)!=h]
new=['README.md','apps/api/src/data/store-error.ts','apps/api/src/realtime/presence-registry.ts','apps/api/src/realtime/presence-types.ts','apps/api/tests/security.test.ts','apps/api/tests/boundaries.test.ts']
files=list(dict.fromkeys(changed+new+[p.relative_to(P).as_posix() for folder in [U/'snapshots',E] for p in folder.iterdir() if p.is_file()]))
spec={'summary':[
'Adds isolated MemoryStore construction, workspace membership and owner/maintainer guards, recipient-scoped inbox projections, and pre-mutation tracker relation checks.',
'Rejects unauthorized issue updates and statuses belonging to another issue type before changing issue/planner state; repaired expected failures map to Fastify 403/404 responses.',
'Registers socket handlers through a testable seam, validates payloads/cursors, awaits room joins, derives member identity and broadcasts socket-owned presence cleanup including the final empty list.',
'Adds eight finite store, socket and real Fastify injection tests, plus nine source-grounded chapters with complete executed examples and exact original snapshots.'
],'changedFiles':files,'checks':{'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':8},'limits':[
'Fixed demo identity and simulated auth remain; no real authenticated tenant/session boundary was exercised.',
'Mutable in-memory state is not durable or transactional; planner side effects and count-derived issue identifiers retain existing limits.',
'Socket tests use real registration with a fake transport; no live socket listener, Redis adapter, distributed presence, worker or browser was run.',
'Eight tests cover the repaired paths; other endpoints retain existing policies, and explicit null clearing/durable message idempotency remain follow-up work.'
]}
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
hashes={n:sha(P/n) for n in files if not n.startswith('astraupskill/') and n!='README.md'};(C/'root-review-source-hashes.json').write_text(json.dumps({'files':hashes},indent=2),encoding='utf-8')
print(json.dumps({'changedBaseline':changed,'courseWords':sum(len(p.read_text(encoding='utf-8').split()) for p in U.glob('*.md')),'files':len(files)}))
