from pathlib import Path
import json,hashlib,shutil,os
B=Path(__file__).resolve().parents[2];ID='3e4e08e349a1';P=B/'stage'/ID;U=P/'astraupskill';E=U/'evidence';C=B/'checks'/ID
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
labels=['root-install-01','root-generate-01','root-luna-master6-domain-tests-final-02','root-luna-master6-api-tests-full-final-01','root-luna-master6-web-tests-final-01','root-luna-master6-worker-tests-final-01','root-luna-master6-typecheck-full-final-01','root-build-final-01']
E.mkdir(exist_ok=True)
for label in labels:
 r=read(C/(label+'.json'));assert r['status']=='complete' and r['exitCode']==0,r
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
assert 'Tests  15 passed (15)' in (C/'root-luna-master6-domain-tests-final-02.log').read_text(encoding='utf-8')
assert 'Tests  14 passed (14)' in (C/'root-luna-master6-api-tests-full-final-01.log').read_text(encoding='utf-8')
for label in ['root-luna-master6-web-tests-final-01','root-luna-master6-worker-tests-final-01']:
 assert 'No test files found' in (C/(label+'.log')).read_text(encoding='utf-8')
base=read(B/'baselines'/f'{ID}.json')['files'];canonical=B.parent.parent/'_Organized Desktop/03 Master Projects/master 6'
for n in base:
 if n.endswith('.tsbuildinfo'):
  assert sha(canonical/n)==base[n];shutil.copyfile(canonical/n,P/n)
p=U/'03-WORKED-CHANGE.md';t=p.read_text(encoding='utf-8');a=t.index('```ts',t.index('After that check'));z=t.index('```',a+3);source=(P/'apps/api/src/routes/learner.routes.ts').read_text(encoding='utf-8');start=source.index('      const enrollment = await prisma.$transaction');end=source.index('      response.status(201).json({ enrollment });',start)
t=t[:a]+'```ts\n'+source[start:end].rstrip()+'\n'+t[z:];p.write_text(t,encoding='utf-8')
p=U/'04-TESTING-AND-DEBUGGING.md';t=p.read_text(encoding='utf-8')
for x in ['403','404','409','500']:t=t.replace('A'+x,'A '+x)
p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8').replace('the default development secret and generic error middleware are unchanged','the default development secret is unchanged and the existing error middleware can expose unexpected Error.message text');p.write_text(t,encoding='utf-8')
(U/'VERIFICATION.md').write_text('''# Verification and reproducible setup

Run from the Master6 project root using Node22.16 or a compatible Node22 environment. The npm workspace lockfile was installed successfully. Prisma client generation uses a placeholder PostgreSQL URL; generation and compilation do not connect to or initialize that database.

```powershell
npm ci
$env:DATABASE_URL = 'postgresql://astra:astra@127.0.0.1:5432/astra_validation'
npm run db:generate
npm run typecheck
npm test
npm run build
```

Do not run db:migrate or db:seed as part of this reproduction. A learner starting the live application must deliberately configure a separate local database and any required Redis service. The recorded checks used neither. The root build now emits the domain package before API, web and worker builds. Typechecking uses the TypeScript source-path mapping and does not itself emit declarations. A source alias in the API Vitest configuration also points tests at the current domain implementation.

There are twenty-nine distinct executed cases: [fifteen domain tests](evidence/root-luna-master6-domain-tests-final-02.log) and [fourteen API tests](evidence/root-luna-master6-api-tests-full-final-01.log). The latter consists of thirteen learner-route cases and one existing app-construction case. The focused thirteen-case rerun is not an additional suite to add to that total. Web and worker commands completed with passWithNoTests and found zero test files. They contribute zero cases and provide no UI/worker behavioral coverage.

The [workspace typecheck](evidence/root-luna-master6-typecheck-full-final-01.log) and [ordered production build](evidence/root-build-final-01.log) passed. [results.json](evidence/results.json) contains the authoritative labels, counts and scope; command metadata and logs are copied locally beside it. Generated tsbuildinfo content was restored to the original baseline after checks, and build output is not delivered. The source change includes the ordered root build script, learner guards/rule evaluation, transaction-aware event/audit helpers and actual route fixtures.

The router fixture replaces Prisma delegates, JWT middleware and event/audit helpers. It verifies expected branches and the transaction client passed to helper spies; it does not establish real PostgreSQL rollback, unique constraint behavior, concurrent completion/retake limits or eventual outbox delivery. The terminal replay case starts from an already-completed record. Stable certificate identity does not imply an identical relation-rich response or serialized concurrent requests. The actual schema already makes enrollmentId and verificationCode unique, but the ID-suffix code generator has no collision retry.

No certificate PDF, payment, external message, browser session or Redis worker was generated/exercised. Existing post-completion progress edits, permissive completion source statuses, development JWT fallback and unexpected error-message disclosure remain outside this increment. These limits are discussed with the complete test fixture in [solutions](06-SOLUTIONS-AND-REVIEW.md). Original snapshots are available for each changed baseline source file, so compare the before and after code when practicing without relying on this explanation alone.
''',encoding='utf-8')
p=P/'README.md';t=p.read_text(encoding='utf-8-sig') if p.exists() else '# Master6 learning workspace\n'
if 'astraupskill/README.md' not in t:t+='\n## Learner workflow engineering course\n\nStart the [detailed CRUD learning course](astraupskill/README.md) for tenant/ownership checks, versioned requirements, transactions, real route regression fixtures and matched exercises. The [verification record](astraupskill/VERIFICATION.md) includes29 distinct tests, workspace checks and explicit operational limits.\n'
p.write_text(t,encoding='utf-8')
result={'passed':True,'total':29,'tests':29,'failed':0,'checks':labels,'scope':'15 actual domain cases plus14 API cases (13 production learner-router cases with Prisma/auth/event/audit spies, one app construction). Web/worker commands discover zero tests. Workspace typecheck and ordered production build pass; no live database/Redis/browser.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
changed=[n for n,h in base.items() if not(P/n).is_file() or sha(P/n)!=h]
for n in changed:
 assert sha(canonical/n)==base[n],n
 if n!='README.md' and not any(sha(q)==base[n] for q in (U/'snapshots').iterdir() if q.is_file()):shutil.copyfile(canonical/n,U/'snapshots'/(n.replace('/','__')+'.before.txt'))
new=[]
for root,dirs,files in os.walk(P):
 dirs[:]=[d for d in dirs if d not in {'node_modules','.git','.next','dist','coverage','astraupskill'}]
 for f in files:
  n=(Path(root)/f).relative_to(P).as_posix()
  if n not in base and not n.endswith('.tsbuildinfo'):new.append(n)
assert all(n.endswith(('.ts','.json','.md')) for n in new),new
spec={'summary':['Scopes learner writes to authenticated organization membership, actor-owned enrollment and content belonging to the enrolled course version; selects the current published version for enrollment.','Validates stored completion rules and required lesson/quiz/assignment sets, rejecting missing learner rows while supporting explicitly empty requirements.','Groups learner mutations with transaction-client events/outbox writes, completion audit/certificate writes and a terminal replay guard; preserves progress timestamp semantics.','Orders workspace builds, adds13 actual learner-router cases alongside existing tests, and supplies nine detailed chapters with complete fixtures and portable evidence.'],'changedFiles':changed+new+[p.relative_to(P).as_posix() for folder in [U/'snapshots',E] for p in folder.iterdir() if p.is_file()], 'checks':{'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':29},'limits':['Prisma/auth/event/audit are mocked in route tests; no SQL rollback, database uniqueness race, JWT verification, Redis delivery or browser coverage.','Terminal guard preserves status/certificate, not byte-identical response shape; concurrent first completion and quiz count-plus-one remain unverified.','Certificate IDs have existing uniqueness constraints but no suffix-collision retry; artifactUrl does not generate a PDF.','Work remains editable after completion and completion is not restricted to ACTIVE status; development JWT fallback and unexpected error disclosure remain unchanged.']}
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
(C/'root-review-source-hashes.json').write_text(json.dumps({'files':{n:sha(P/n) for n in changed+new if not n.endswith('.md')}},indent=2),encoding='utf-8')
print(json.dumps({'changed':changed,'new':new,'tests':29,'files':len(spec['changedFiles'])+9}))
