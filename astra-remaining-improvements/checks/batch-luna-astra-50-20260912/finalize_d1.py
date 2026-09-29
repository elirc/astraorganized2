from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parents[2];ID='61d919e84af9';P=B/'stage'/ID;C=B/'checks'/ID;U=P/'astraupskill';E=U/'evidence'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
labels=['root-test-01','root-lint-02','root-build-05']
for label in labels:
 r=read(C/(label+'.json'));assert r['status']=='complete' and r['exitCode']==0
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
assert '# tests 4' in (C/'root-test-01.log').read_text(encoding='utf-8')
css=list((P/'.next/static/css').glob('*.css'));allcss='\n'.join(p.read_text(encoding='utf-8') for p in css)
selectors=['.bg-accent-500','.shadow-soft','#0e89ff'];assert all(s in allcss for s in selectors)
cssResult={'passed':True,'selectors':selectors,'files':{p.relative_to(P).as_posix():sha(p) for p in css},'scope':'Generated stylesheet inspection, not browser visual verification.'}
(E/'css-inspection.json').write_text(json.dumps(cssResult,indent=2),encoding='utf-8')
result={'passed':True,'total':4,'tests':4,'failed':0,'checks':labels,'scope':'Four FakeSocket/update-argument tests, final ESLint and full Next production build with type validation. Custom accent/shadow CSS present. Keyboard card activation source-reviewed; no browser, database, Redis, socket listener or dispatcher.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
spec=read(B/'specs'/f'{ID}.json');spec['changedFiles']=list(dict.fromkeys(spec['changedFiles']+[p.relative_to(P).as_posix() for p in E.iterdir() if p.is_file()]));spec['checks']={'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':4}
spec['summary'].append('Repairs the Next/PostCSS/dependency setup, keeps schema migration separate from compilation, and preserves card keyboard focus and activation while delegating handled drag keys.')
spec['limits'].append('Empty patches, optimistic drag ordering, non-text filter behavior, concurrent joins and membership revocation after joins remain follow-up work. Card keyboard behavior was source-reviewed and compiled, not browser-tested.')
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
hashes={n:sha(P/n) for n in spec['changedFiles'] if not n.startswith('astraupskill/') and n!='README.md'};(C/'root-review-source-hashes.json').write_text(json.dumps({'files':hashes},indent=2),encoding='utf-8')
p=U/'VERIFICATION.md';t=p.read_text(encoding='utf-8');t+='''
## Final recorded checks

The [four-test run](evidence/root-test-01.log), [final lint run](evidence/root-lint-02.log), and [final production build](evidence/root-build-05.log) all returned zero. The final build includes the keyboard repair in `Card.tsx`: sortable attributes remain, the card has button semantics and a tab stop, and Enter/Space activate it unless the drag handler consumed the key. Compilation establishes that these event types fit the component; keyboard interaction still needs a browser check. The [CSS inspection](evidence/css-inspection.json) confirms the custom theme classes in the generated stylesheet. The [results summary](evidence/results.json) identifies these authoritative checks; earlier build failures are historical setup evidence.
''';p.write_text(t,encoding='utf-8')
print('D1 final evidence, CSS inspection, source hashes and spec ready')
