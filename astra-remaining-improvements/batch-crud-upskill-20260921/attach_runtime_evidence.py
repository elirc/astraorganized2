"""Attach a reviewed, captured Node test run without counting static checks."""
from pathlib import Path
import json, shutil, sys, re
B=Path(__file__).resolve().parent.parent
pid,label,count=sys.argv[1:];count=int(count)
C=B/'checks'/pid;P=B/'stage'/pid
record=json.loads((C/f'{label}.json').read_text())
assert record['status']=='complete' and record['exitCode']==0 and record['passed']
log=(C/f'{label}.log').read_text(encoding='utf-8')
for field,value in [('tests',count),('pass',count),('fail',0),('skipped',0)]:
    assert re.search(rf'^# {field} {value}$',log,re.M),(field,value)
specpath=B/'specs'/f'{pid}.json';spec=json.loads(specpath.read_text())
result={'passed':True,'executedTests':count,'checks':[record],'limits':spec['limits']}
resultpath=B/spec['checks']['resultsFile']
assert resultpath.resolve().parent == C.resolve()
resultpath.write_text(json.dumps(result,indent=2),encoding='utf-8')
E=P/'astraupskill/evidence';E.mkdir(exist_ok=True)
shutil.copyfile(C/f'{label}.log',E/f'{label}.log')
shutil.copyfile(resultpath,E/'results.json')
for name in [f'astraupskill/evidence/{label}.log','astraupskill/evidence/results.json']:
    if name not in spec['changedFiles']:spec['changedFiles'].append(name)
specpath.write_text(json.dumps(spec,indent=2),encoding='utf-8')
v=P/'astraupskill/VERIFICATION.md';t=v.read_text()
marker='## Astra execution evidence'
if marker not in t:
    t+=f'\n{marker}\n\nThe captured focused production-source suite executed {count} tests: all passed, zero failed and zero skipped. Read the [captured output](evidence/{label}.log) and [exact command and limits](evidence/results.json). Earlier check records remain preserved in the workspace.\n'
    v.write_text(t,encoding='utf-8')
print(json.dumps({'id':pid,'executedTests':count,'label':label}))
