from pathlib import Path
import hashlib,json,os,shutil
B=Path(__file__).resolve().parents[2];ID='b7429e8bf71d';P=B/'stage'/ID;U=P/'astraupskill';C=B/'checks'/ID;E=U/'evidence';E.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
labels=['root-install-02','luna-generate-final-20260912','luna-test-freeze-20260912','luna-typecheck-freeze-20260912','luna-lint-freeze-20260912','root-build-final-01']
for label in labels:
 r=read(C/(label+'.json'));assert r['status']=='complete' and r['exitCode']==0,r
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
log=(C/'luna-test-freeze-20260912.log').read_text(encoding='utf-8');assert '# tests 13' in log and '# pass 13' in log and '# fail 0' in log
base=read(B/'baselines'/f'{ID}.json')['files'];canonical=B.parent.parent/'_Organized Desktop/08 App And Product Projects/appmakertrack'
for n in base:
 if n.endswith('.tsbuildinfo'):
  assert sha(canonical/n)==base[n];shutil.copyfile(canonical/n,P/n)
summary=['Validates timer instants and Prisma Int durations, preserving zero, omitted notes and explicit null. Manual/start factories support actual handler tests and safe errors.','Protects the stop transition with an endTime-null conditional update; starts enforce the existing application-wide running check inside a transaction.','Moves board tickets using transaction-local reads, same-project targets, clamped insertion and contiguous sibling positions, including no-op moves.','Restores full-project ESLint with small unused-code cleanups, supplies thirteen passing regression cases and nine detailed learning chapters with complete executable examples.']
limits=['Tests use partial Prisma doubles and actual handler/service functions; no generated SQLite persistence, rollback, HTTP server, browser or authentication coverage.','No trusted actor resolver or per-user timer relation; project consistency is not user authorization.','Start and board concurrency across connections/processes is unverified; ticket positions have no uniqueness constraint.','Stop protects the transition but its later read may observe subsequent edits. Existing unrelated CRUD routes remain outside this increment.']
result={'passed':True,'total':13,'tests':13,'failed':0,'checks':labels,'scope':'13 Node test cases across actual parsers, manual/start handlers, stop/start services and board service with Prisma doubles; full lint/typecheck/Next build pass; no live database or browser.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
(U/'VERIFICATION.md').write_text('''# Verification and repeatable setup

Run these commands from the Appmakertrack project root with Node22.16 or a compatible Node22 runtime. Dependencies and generated Prisma types are needed even though the behavioral tests inject partial client doubles. Client generation does not initialize or seed a database.

```powershell
npm ci
npx prisma generate
npm test
npx tsc --noEmit
npm run lint
npm run build
```

The [test log](evidence/luna-test-freeze-20260912.log) records thirteen passing Node test cases, zero failures. Cases include strict ISO/calendar and integer boundaries, zero/null/omission semantics, manual/start success and failure responses, generic errors, conditional stop outcomes and actual board service mutations. The board case asserts identity order, numeric contiguous positions and no changes for a foreign target. These are executable production seams with intentionally partial Prisma doubles. They are not HTTP requests through a live Next server, generated SQLite transactions, browser interactions or authentication tests.

The [full project lint](evidence/luna-lint-freeze-20260912.log), [typecheck](evidence/luna-typecheck-freeze-20260912.log) and [production build](evidence/root-build-final-01.log) passed. The lint command is eslint .; lint:changed remains a convenience command and is not substituted for full lint. Small cleanup removes unused bindings/imports without removing seed operations or React hooks. The no-explicit-any exception is confined to the partial doubles in the test file. No global lint rule was disabled. [results.json](evidence/results.json) lists exact successful labels and scope, with command metadata and logs copied beside it.

The original schema points at a development SQLite file. Do not run db:push or db:seed as part of verification: the latter resets demo data. A future persistence fixture must construct a client and CLI setup with the same absolute URL beneath a unique temporary directory. Merely assigning DATABASE_URL does not override a literal schema URL. The delivered checks did not reset the canonical database. Baseline source snapshots are preserved under snapshots, while generated build output and dependencies are excluded from delivery.

The global running-timer policy remains application-wide. The code has no trusted actor resolver or user relation on TimeEntry. Compare-and-set prevents a losing stop from overwriting the transition, but the subsequent read can observe a later edit. Board transaction correctness under real SQLite failure or concurrent processes remains unverified; the test double has no rollback engine and ticket positions have no uniqueness constraint. The complete [solutions and fixture](06-SOLUTIONS-AND-REVIEW.md) distinguish demonstrated behavior from proposed integration work.
''',encoding='utf-8')
p=P/'README.md';t=p.read_text(encoding='utf-8-sig') if p.exists() else '# Appmakertrack\n'
if 'astraupskill/README.md' not in t:t+='\n## CRUD engineering course\n\nFollow the [detailed timer and board learning course](astraupskill/README.md) for validation, state transitions, transaction boundaries, thirteen executable regression cases and matched exercises. See [verification](astraupskill/VERIFICATION.md) for repeatable commands and coverage limits.\n'
p.write_text(t,encoding='utf-8')
changed=[n for n,h in base.items() if not(P/n).is_file() or sha(P/n)!=h]
S=U/'snapshots';S.mkdir(exist_ok=True)
for n in changed:
 assert sha(canonical/n)==base[n],n
 if n!='README.md' and not any(sha(q)==base[n] for q in S.iterdir() if q.is_file()):shutil.copyfile(canonical/n,S/(n.replace('/','__')+'.before.txt'))
new=[]
for root,dirs,files in os.walk(P):
 dirs[:]=[d for d in dirs if d not in {'node_modules','.git','.next','dist','coverage','astraupskill'}]
 for f in files:
  n=(Path(root)/f).relative_to(P).as_posix()
  if n not in base and not n.endswith('.tsbuildinfo'):new.append(n)
assert all(n.endswith(('.ts','.tsx','.json','.md','.mjs')) for n in new),new
spec={'summary':summary,'changedFiles':changed+new+[p.relative_to(P).as_posix() for folder in [S,E] for p in folder.iterdir() if p.is_file()],'checks':{'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':13},'limits':limits}
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
(C/'root-review-source-hashes.json').write_text(json.dumps({'files':{n:sha(P/n) for n in changed+new if not n.endswith('.md')}},indent=2),encoding='utf-8')
print(json.dumps({'changed':changed,'new':new,'tests':13,'files':len(spec['changedFiles'])+9}))
