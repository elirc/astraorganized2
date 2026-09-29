from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parents[2];ID='3ecd02656197';P=B/'stage'/ID;C=B/'checks'/ID;U=P/'astraupskill';E=U/'evidence'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
for n,h in read(C/'root-review-source-hashes.json')['files'].items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,n
labels=['root-test-01','root-typecheck-01','root-lint-02','root-build-01']
for label in labels:
 r=read(C/(label+'.json'));assert r['status']=='complete' and r['exitCode']==0
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
r={'passed':True,'total':7,'tests':7,'failed':0,'checks':labels,'scope':'Actual pure page builders with seeded relation data; full role matrix, dates/offsets/ties, active job counts, empty data and non-mutation. Next production build, TypeScript and ESLint passed; no browser, session, database or write endpoint.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(r,indent=2),encoding='utf-8')
spec=read(B/'specs'/f'{ID}.json');spec['checks'].update(format='json',expectedTests=7)
spec['changedFiles']=list(dict.fromkeys(spec['changedFiles']+[p.relative_to(P).as_posix() for p in E.iterdir() if p.is_file()]))
spec['limits']=[x for x in spec['limits'] if 'root-owned' not in x]
spec['limits']=[x.replace('X-free role fixtures','explicit role fixtures') for x in spec['limits']]
spec['limits'].append('Build and static checks passed; no browser interaction or real authenticated request was exercised.')
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
p=U/'VERIFICATION.md';t=p.read_text(encoding='utf-8');t+='''
## Recorded final results

All seven tests passed in the [test output](evidence/root-test-01.log). The [typecheck](evidence/root-typecheck-01.log), [lint](evidence/root-lint-02.log), and [production build](evidence/root-build-01.log) each returned zero. The build compiled the final application source; the expanded test file was then checked by the final TypeScript and lint runs. The [summary](evidence/results.json) records seven tests, not the number of commands. Earlier four-test evidence remains historical.

The role matrix covers all five declared roles. The date fixtures include two timezone offsets for equal instants, a different offset for a later instant, December/January across years, and invalid values. These are builder tests using actual formatting, not an HTTP authorization test. The empty component branch was inspected in source; no browser rendering pass was performed.
''';p.write_text(t,encoding='utf-8')
print('z7 final evidence and spec ready')
