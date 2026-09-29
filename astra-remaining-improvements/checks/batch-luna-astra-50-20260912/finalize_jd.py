from pathlib import Path
import json,hashlib,shutil,os
B=Path(__file__).resolve().parents[2]; ID='2d739127d551'; P=B/'stage'/ID; U=P/'astraupskill'; C=B/'checks'/ID; E=U/'evidence'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
labels=['root-install-01','root-generate-01','root-handler-tests-02','root-lint-02','root-build-01']
for label in labels:
 r=read(C/(label+'.json'));assert r['status']=='complete' and r['exitCode']==0,r
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
log=(C/'root-handler-tests-02.log').read_text(encoding='utf-8');assert '# tests 11' in log and '# pass 11' in log and '# fail 0' in log
for p in U.glob('*.md'):
 t=p.read_text(encoding='utf-8-sig').replace('root-handler-tests-01','root-handler-tests-02').replace('null, arrays, primitive bodies,','null and array bodies,').replace('The staged route test','The route test')
 p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8');start=t.index('```js',t.index('## Complete route test fixture'));t=t[:start]+'```js\n'+(P/'tests/issue-routes.test.mjs').read_text(encoding='utf-8')+'```\n'
t=t.replace('Exercise 8: review the remaining limits.','Exercise 8: a suitable verification note is: Eleven tests passed, with zero failures, using Node VM modules to load the actual API handlers and mock Prisma/framework/identity seams. The production build and lint passed. Positive and rejected requests demonstrate handler contracts, but database rollback and browser behavior require separate checks. Review the remaining limits:')
p.write_text(t,encoding='utf-8')
p=U/'VERIFICATION.md';t=p.read_text(encoding='utf-8').replace('The final build and lint results are recorded in the evidence folder and summarized in results.json after review.','The [production build](evidence/root-build-01.log) and [lint](evidence/root-lint-02.log) both passed; [results.json](evidence/results.json) summarizes the final records. Lint originally rejected two VM loader variable names; the final test-only rename was followed by all eleven tests and a fresh lint run. The application source is unchanged from the passing build.')
p.write_text(t,encoding='utf-8')
p=P/'README.md';t=p.read_text(encoding='utf-8-sig')
if 'astraupskill/README.md' not in t:t+='\n## CRUD engineering learning course\n\nStart the [detailed learning course](astraupskill/README.md) for issue validation, scoped relations, transaction clients, regression fixtures and review exercises. The local verification record distinguishes tested handler behavior from database and identity limitations.\n'
p.write_text(t,encoding='utf-8')
result={'passed':True,'total':11,'tests':11,'failed':0,'checks':labels,'scope':'Two input-helper cases and nine real route/API cases loaded with Node VM modules and Prisma/identity/framework doubles. Production Next build and lint passed; no real database rollback, auth or browser test.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
base=read(B/'baselines'/f'{ID}.json')['files'];changed=[n for n,h in base.items() if not(P/n).is_file() or sha(P/n)!=h]
canonical=B.parent.parent/'_Organized Desktop/12 Other Projects/jdtrrain2.1'
for n in changed:
 assert sha(canonical/n)==base[n],n
 if n!='README.md' and not any(sha(q)==base[n] for q in (U/'snapshots').iterdir() if q.is_file()):shutil.copyfile(canonical/n,U/'snapshots'/(n.replace('/','__')+'.before.txt'))
new=[]
for root,dirs,files in os.walk(P):
 dirs[:]=[d for d in dirs if d not in {'node_modules','.git','.next','astraupskill','coverage'}]
 for f in files:
  n=(Path(root)/f).relative_to(P).as_posix()
  if n not in base:new.append(n)
assert all(n.endswith(('.js','.mjs','.json','.md')) for n in new),new
spec={'summary':['Validates issue PATCH fields and project-scoped relations before writes, preserving explicit nulls, zero values and no-op semantics with Prisma Int bounds.','Groups PATCH issue/activity/notification writes and bulk-sprint activity with their transaction client; validates full bulk populations before any updates.','Scopes move targets to the project board, validates IDs and positions, and provides safe API body/error responses.','Adds eleven input and actual route/API regression cases, passing production build/lint and nine source-specific learning chapters with complete examples.'],'changedFiles':changed+new+[p.relative_to(P).as_posix() for folder in [U/'snapshots',E] for p in folder.iterdir() if p.is_file()], 'checks':{'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':11},'limits':['Prisma and identity are mocked in tests; no database rollback, cross-request isolation, browser, Slack or authenticated session test.','Demo actor selection remains unauthenticated; PATCH has no expected-version protection.','Move activity remains outside its transaction and source-column position gaps/concurrent ordering remain; POST creation retains existing relation and side-effect gaps.','Dates accept JavaScript-parsable strings and numeric strings are intentionally accepted for optional integer inputs.']}
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
(C/'root-review-source-hashes.json').write_text(json.dumps({'files':{n:sha(P/n) for n in changed+new if not n.endswith('.md')}},indent=2),encoding='utf-8')
print(json.dumps({'changed':changed,'new':new,'tests':11,'files':len(spec['changedFiles'])+9}))
