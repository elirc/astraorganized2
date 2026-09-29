from pathlib import Path
import json,re,shutil,hashlib
B=Path(__file__).resolve().parent.parent;pid='f5bd710b171f';P=B/'stage'/pid;C=B/'checks'/pid
label='crud-b02-go-harness-final'
r=json.loads((C/f'{label}.json').read_text());log=(C/f'{label}.log').read_text()
assert r['status']=='complete' and r['passed'] and r['exitCode']==0
cases=re.findall(r'^\s+--- PASS: TestUpdateChannelTContracts/(\S+) ',log,re.M)
assert len(cases)==6 and len(set(cases))==6 and '--- FAIL' not in log and '--- SKIP' not in log
assert '\nPASS\n' in log
s=B/'specs'/f'{pid}.json';j=json.loads(s.read_text())
j['limits']=['Six Go subtests execute the exact extracted updateChannelT method and row-count helper with explicit SQL, model and error contracts.','The native Mattermost package test, PostgreSQL integration, model validation and unique-constraint classification were not executed.','Outer Update transaction finalization and public-channel propagation were reviewed in source only; the harness does not execute them.']
result={'passed':True,'executedTests':6,'cases':cases,'checks':[r],'limits':j['limits']}
(C/'results-crud-b02.json').write_text(json.dumps(result,indent=2))
E=P/'astraupskill/evidence';E.mkdir(exist_ok=True)
for src,name in [(C/f'{label}.log',f'{label}.log'),(C/'results-crud-b02.json','results.json'),(B/'batch-crud-upskill-20260921/toolchains/go1.27.1/verification.json','toolchain-verification.json')]:
    shutil.copyfile(src,E/name)
    rel='astraupskill/evidence/'+name
    if rel not in j['changedFiles']:j['changedFiles'].append(rel)
s.write_text(json.dumps(j,indent=2))
f=P/'astraupskill/VERIFICATION.md';t=f.read_text()
t=t.replace('The final check JSON must record the actual portable toolchain output and numeric test count when C completes it.','The captured portable run completed successfully with six passing subtests and no failed or skipped cases. The parent Go test is not counted as a seventh case.')
t+='\n## Captured execution\n\nRead the [Go output](evidence/crud-b02-go-harness-final.log), [command and six-case results](evidence/results.json), and [verified portable toolchain metadata](evidence/toolchain-verification.json). The earlier failed launch and incomplete-toolchain attempt remain separate workspace records. The successful run uses Go 1.27.1 from the checksum-verified official archive; no native Mattermost dependency suite was installed or claimed.\n'
f.write_text(t,encoding='utf-8')
baseline=json.loads((B/'baselines'/f'{pid}.json').read_text())['files']
assert hashlib.sha256((P/'astraupskill/snapshots/channel_store.go.original.txt').read_bytes()).hexdigest()==baseline['mattermost/server/channels/store/sqlstore/channel_store.go']
print(json.dumps({'id':pid,'cases':cases,'snapshotVerified':True}))
