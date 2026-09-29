from pathlib import Path
import json,re,hashlib,shutil
B=Path(__file__).resolve().parent.parent;pid='e0e5886e8464';P=B/'stage'/pid;C=B/'checks'/pid
labels=['crud-b01-boundaries','crud-b01-typecheck-installed']
records=[]
for label in labels:
    r=json.loads((C/f'{label}.json').read_text())
    assert r['status']=='complete' and r['passed'] and r['exitCode']==0,(label,r)
    records.append(r)
log=(C/'crud-b01-boundaries.log').read_text(encoding='utf-8')
assert re.search(r'^# tests 46$',log,re.M) and re.search(r'^# pass 46$',log,re.M) and re.search(r'^# fail 0$',log,re.M)
lint=json.loads((C/'crud-b01-lint-installed.json').read_text())
assert lint['status']=='complete' and lint['passed'] is False
lint['reviewNote']='Stopped by Astra after 652 seconds without diagnostics; not a passing lint result.'
summary={'passed':True,'executedTests':46,'checks':records,'uncompletedChecks':[lint],'limits':['Focused production-module tests; Next HTTP adapter/browser/provider integration not executed.','No database exists in this flow. Storage recovery validates and filters on read without rewriting saved collections.','Changed-file ESLint was stopped after more than ten minutes without diagnostics; no lint pass is claimed.']}
result=C/'results-crud-b01.json';result.write_text(json.dumps(summary,indent=2),encoding='utf-8')
E=P/'astraupskill/evidence';E.mkdir(exist_ok=True)
for label in labels:shutil.copyfile(C/f'{label}.log',E/f'{label}.log')
shutil.copyfile(result,E/'results.json')
ver=P/'astraupskill/VERIFICATION.md';t=ver.read_text()
if '## Accepted evidence' not in t:
    t+='\n## Accepted evidence\n\n- [Result records](evidence/results.json): 46 passed, zero failed.\n- [Boundary test output](evidence/crud-b01-boundaries.log).\n- [TypeScript check output](evidence/crud-b01-typecheck-installed.log): exit 0, incremental disabled.\n- Changed-file ESLint produced no diagnostics after more than ten minutes and was stopped; its unsuccessful command record is retained in results.json. No lint pass is claimed.\n'
    ver.write_text(t,encoding='utf-8')
changed=['app/api/recipes/route.ts','lib/storage.ts','package.json','tsconfig.json','lib/validation.ts','lib/generation.ts','tests/boundaries.test.mjs']
changed += [f.relative_to(P).as_posix() for f in sorted((P/'astraupskill/snapshots').iterdir())]
changed += [f.relative_to(P).as_posix() for f in sorted(E.iterdir())]
spec={'summary':['Validate recipe requests before provider calls and validate nested provider output before success.','Recover valid browser history/favorites from mixed or malformed persisted JSON without rewriting data during reads.','Add 46 production-module regressions and nine source-based teaching chapters with original snapshots, debugging exercises, traces and separate solutions.'],'changedFiles':changed,'checks':{'format':'json','resultsFile':f'checks/{pid}/results-crud-b01.json'},'limits':summary['limits']+['Existing process-local rate limiting, session-storage navigation failure, SDK-internal retries and dietary/culinary accuracy are not certified by this change.','Full production build and browser end-to-end tests were not run; project typecheck passed.']}
(B/'specs'/f'{pid}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
print(json.dumps({'id':pid,'changedFiles':len(changed),'tests':46}))
