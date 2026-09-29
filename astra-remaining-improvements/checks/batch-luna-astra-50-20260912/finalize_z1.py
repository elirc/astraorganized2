from pathlib import Path
import hashlib,json,os,shutil
B=Path(__file__).resolve().parents[2];ID='f27db87d9d3a';P=B/'stage'/ID;U=P/'astraupskill';C=B/'checks'/ID;E=U/'evidence';E.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
labels=['root-install-01','z1-tests-final-03','root-typecheck-final-02','root-lint-final-02','z1-build-final-01']
for label in labels:
 r=read(C/(label+'.json'));assert r['status']=='complete' and r['exitCode']==0,r
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
log=(C/'z1-tests-final-03.log').read_text(encoding='utf-8');assert '# tests 16' in log and '# pass 16' in log and '# fail 0' in log
base=read(B/'baselines'/f'{ID}.json')['files'];canonical=B.parent.parent/'_Organized Desktop/05 Numbered Experiments/z1'
for n in base:
 if n.endswith('.tsbuildinfo'):
  assert sha(canonical/n)==base[n];shutil.copyfile(canonical/n,P/n)
result={'passed':True,'total':16,'tests':16,'failed':0,'checks':labels,'scope':'16 actual service tests using the production JSON store in unique OS temporary directories; full typecheck/lint/Next build pass. No live HTTP, cookie-auth, browser, crash consistency or multiple-process tests.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
(U/'VERIFICATION.md').write_text('''# Verification and repeatable setup

Run from the z1 project root with Node22.16 or a compatible Node22 environment. The existing package scripts resolve the installed TypeScript test runner, compiler, ESLint and Next builder. No parent audit folder or Python runner is needed to reproduce the project checks.

```powershell
npm ci
npm test
npm run typecheck
npm run lint
npm run build
```

The [final service test log](evidence/z1-tests-final-03.log) reports sixteen tests, sixteen passes and zero failures. It exercises the production request/workflow/admin services and file-backed JSON store. Each case chooses a unique directory under the OS temporary folder through RAP_DATA_DIRECTORY and removes that owned directory in finally. No canonical request database is reset. The fixture activates delegation dates relative to today where necessary so an expired static seed interval does not invalidate the intended actor scenario.

Tests cover positive submission, delegation, sequential approvals, resubmission, reassignment, comments, admin rules and reporting. New rejection assertions cover future approvers, terminal retries, malformed or missing update IDs, invalid type/intent/action, incomplete resubmissions, unsafe reassignment targets, invalid rule candidates and overlapping delegations. Internal-note markers are checked in both comments and timeline DTOs, including a manager who is also the requester. Serialized before/after values demonstrate unchanged persisted state following these rejected operations.

The [typecheck](evidence/root-typecheck-final-02.log), [full lint](evidence/root-lint-final-02.log) and [production build](evidence/z1-build-final-01.log) passed. The build preceded the final test-only assertion additions; production source did not change afterward. Typecheck and lint were repeated against the final test source. [results.json](evidence/results.json) lists the exact labels; metadata and logs are copied locally beside it. The original changed files have exact byte snapshots, and generated tsbuildinfo content is restored before delivery. Dependencies and build output are excluded.

The JSON store clones before invoking a queued callback and persists only after success. That protects these single-process rejection scenarios; it is not a crash-safe filesystem transaction or a lock across server processes. A clone may have been modified and discarded, so value equality is not proof that no in-memory mutation occurred. Service errors here are plain Error objects: the suite does not establish an HTTP status mapping, cookie authentication, browser behavior or external identity integration. Requester exclusion also applies to admin/support requesters, while internal-note creation retains its existing role permission. See the complete [fixture and solutions](06-SOLUTIONS-AND-REVIEW.md) to inspect these precise boundaries before extending them.
''',encoding='utf-8')
p=P/'README.md';t=p.read_text(encoding='utf-8-sig') if p.exists() else '# z1 request approvals\n'
if 'astraupskill/README.md' not in t:t+='\n## Request approval engineering course\n\nFollow the [detailed learning course](astraupskill/README.md) for current-step authority, delegation, safe request DTOs, runtime validation and sixteen actual service tests. [Verification](astraupskill/VERIFICATION.md) provides local commands and precise coverage limits.\n'
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
spec={'summary':['Binds workflow action permission to the current pending step, preserving both delegated and original assignee authority and existing admin/support override.','Filters internal comments before creating requester comments and timeline DTOs, including requesters with operational roles.','Distinguishes create from explicit missing/blank update IDs, validates request type/intent/action and resubmission fields, and rejects unsafe reassignment targets.','Validates workflow SLA, steps and delegation intervals before persistence; adds sixteen actual file-store service tests and nine detailed chapters with complete fixtures.'],'changedFiles':changed+new+[p.relative_to(P).as_posix() for folder in [S,E] for p in folder.iterdir() if p.is_file()],'checks':{'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':16},'limits':['Single-process JSON clone-before-write and serialized-value assertions do not establish crash consistency or cross-process locking.','No HTTP server, cookie authentication or browser coverage; service Error does not itself establish a particular HTTP status.','Requester exclusion also applies to operational/admin requesters; existing permission to create an internal note is separate from read filtering.','Demo identity and existing file-store architecture remain; this increment does not introduce durable database transactions.']}
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
(C/'root-review-source-hashes.json').write_text(json.dumps({'files':{n:sha(P/n) for n in changed+new if not n.endswith('.md')}},indent=2),encoding='utf-8')
print(json.dumps({'changed':changed,'new':new,'tests':16,'files':len(spec['changedFiles'])+9}))
