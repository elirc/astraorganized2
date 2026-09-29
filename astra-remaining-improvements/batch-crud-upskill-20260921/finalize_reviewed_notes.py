from pathlib import Path
import json,shutil,re
B=Path(__file__).resolve().parent.parent
for pid in ['7a758c622d3c','200c3e641a36','6e522cf7fdc9','0f37c14f6d60','fb1267045788']:
    f=B/'specs'/f'{pid}.json';s=json.loads(f.read_text())
    s['limits']=[v for v in s['limits'] if not any(x in v.lower() for x in ['canonical','staged files only','astra review'])]
    if pid=='0f37c14f6d60':
        s['limits']+=['Five Node runtime tests exercise actual service and permission source with explicit persistence/integration doubles; no real HTTP, Prisma or outbox execution.', 'Optional missing-viewer trusted internal bypass remains; this is an organization-field update guard, not a complete tenant-security audit.']
    if pid in ['7a758c622d3c','200c3e641a36','6e522cf7fdc9']:
        s['limits']+=['Full typecheck/build, real HTTP authorization and live database concurrency were not executed.']
    if pid=='200c3e641a36':
        s['limits']+=['Status comparison does not detect ACTIVE-to-ARCHIVED-to-ACTIVE changes, body edits or permission changes between read and write.']
    f.write_text(json.dumps(s,indent=2),encoding='utf-8')
    d=B/'stage'/pid/'astraupskill'
    for p in d.glob('*.md'):
        t=p.read_text()
        t=re.sub(r'Run from `astra-remaining-improvements/stage/[^`]+`:', 'Run from this project root:', t)
        t=t.replace('A service-level test with dependency injection would additionally verify that count zero prevents activity.', 'The executed service runtime test additionally verifies that count zero prevents activity and parent-summary writes.')
        if pid=='200c3e641a36' and p.name=='03-WORKED-CHANGE.md':
            t+='\nThis is a comparison of status values, not a complete version token. If another writer archives and then restores ACTIVE before this request writes, the predicate can match again. Body edits and permission changes also do not change this predicate. Those cases require a broader version or authorization design and remain outside the implemented fix.\n'
        if pid=='6e522cf7fdc9' and p.name=='03-WORKED-CHANGE.md':
            t+='\nThe successful lookup contains a nested lead used by authorization elsewhere. Before returning, the service removes that nested relation and keeps the owner relation, preserving the old update response shape. The runtime success case checks completed status, owner retention and absence of lead; the extra read is not permission to expand the API response.\n'
        if pid=='fb1267045788':
            t=t.replace('The source change remains isolated under `astra-remaining-improvements/stage/fb1267045788`; no canonical project files were edited.', 'The checks ran in an isolated copy; the report records delivery separately and preserves exact original source snapshots.')
            t=t.replace('limited to the three fake-boundary cases and static schema review', 'limited to nine fake-boundary cases and static schema review')
            if p.name=='04-TESTING-AND-DEBUGGING.md':
                t+='\nThe expanded recovery suite invokes the real scrape entry point, including pagination and a 501-row import interrupted at the second batch. It verifies recovery after an HTTP failure following parent creation and preserves seeded parsed fields under the explicitly modeled duplicate-ignore contract. Run both suites from backend with `python -m unittest discover -s tests -p "test_scraper*.py" -v`. The database double records and models the requested API contract; it cannot certify SQL isolation or migration execution.\n'
            if p.name=='VERIFICATION.md':
                t+='\nApply the separate [existing-database migration](../supabase/migrations/20260921_job_comment_unique.sql) before using the new conflict target on an existing installation. It deliberately fails if duplicate logical keys already exist: review those rows rather than deleting parsed records automatically. Fresh installs declare the same named constraint in schema.sql. No migration was applied to a live database during this task.\n'
        p.write_text(t,encoding='utf-8')

pid='fb1267045788';C=B/'checks'/pid;D=B/'stage'/pid/'astraupskill'
label='astra-crud-b01-all-scraper';record=json.loads((C/f'{label}.json').read_text())
assert record['passed'] and record['status']=='complete'
log=(C/f'{label}.log').read_text();assert 'Ran 9 tests' in log and '\nOK' in log
s=json.loads((B/'specs'/f'{pid}.json').read_text())
result={'passed':True,'executedTests':9,'checks':[record],'limits':s['limits']}
(C/'results-crud-b01.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
E=D/'evidence';E.mkdir(exist_ok=True)
shutil.copyfile(C/f'{label}.log',E/f'{label}.log');shutil.copyfile(C/'results-crud-b01.json',E/'results.json')
for n in [f'astraupskill/evidence/{label}.log','astraupskill/evidence/results.json']:
    if n not in s['changedFiles']:s['changedFiles'].append(n)
(B/'specs'/f'{pid}.json').write_text(json.dumps(s,indent=2),encoding='utf-8')
v=D/'VERIFICATION.md';v.write_text(v.read_text()+f'\nAccepted evidence: [nine-test output](evidence/{label}.log), [exact command and limits](evidence/results.json).\n',encoding='utf-8')
print('Reviewed notes finalized')
