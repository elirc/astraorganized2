"""Build a delivery specification only from completed evidence and reviewed images."""
from pathlib import Path
import hashlib,json,shutil,subprocess,xml.etree.ElementTree as ET

B=Path(__file__).resolve().parent;S=B/'stage/19110bf39fcf';C=B/'checks/e15'
read=lambda path:json.loads(path.read_text(encoding='utf-8'))
hashfile=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()

def junit(path):
    tree=ET.parse(path)
    cases=tree.findall('.//testcase')
    assert all(not list(case) or all(child.tag not in {'failure','error','skipped'} for child in case) for case in cases),path
    return {(case.get('classname'),case.get('name')) for case in cases}

for name in ['full-01','reply-timers-01']:
    assert read(C/name/'execution.json')['exitCode']==0,name
backend=junit(C/'full-01/results.xml')|junit(C/'reply-timers-01/results.xml')
assert len(backend)==156,len(backend)
browser=read(C/'browser-05/results.json');render=read(C/'rendering-02/results.json')
assert browser['passed'] and browser['total']==15 and all(item['passed'] for item in browser['checks'])
assert render['passed'] and render['total']==5 and all(item['passed'] for item in render['checks'])
for name in ['browser-05','rendering-02']:
    assert read(C/f'{name}-execution.json')['exitCode']==0,name
install=read(C/'install-01/execution.json')
assert [item['name'] for item in install]==['venv','dependencies','editable','dependency-check','wheel','smoke']
assert all(item['exitCode']==0 for item in install)
assert len(junit(C/'install-01/results.xml'))==53
assert read(C/'install-01/package-check.json')['passed']
assert read(C/'wheel-final-assets.json')['passed']
qa=read(C/'screenshots-reviewed.json')
assert qa['passed'] and qa['directory']=='browser-05' and len(qa['files'])==9
images=S/'astraupskill/images';images.mkdir(exist_ok=True)
for item in qa['files']:
    source=C/'browser-05'/item['name']
    assert hashfile(source)==item['sha256'],source
    shutil.copyfile(source,images/item['name'])

command=['node','--check','app/static/app.js']
result=subprocess.run(command,cwd=S,capture_output=True,text=True)
assert result.returncode==0,result.stderr
(C/'syntax-final.json').write_text(json.dumps({'command':command,'exitCode':result.returncode},indent=2),encoding='utf-8')
evidence={'passed':True,'total':176,'backend':156,'browser':15,'rendering':5,
          'backendMethod':'Union of full-01 and reply-timers-01 test identities; repeated regression cases counted once.',
          'cleanInstall':{'passed':True,'smokeTests':53,'wheelAssets':7,'repeatedTestsCountedAgain':False},
          'screenshots':9,'gates':{'full':read(C/'full-01/execution.json'),
          'timerRegression':read(C/'reply-timers-01/execution.json'),
          'browser':read(C/'browser-05-execution.json'),'rendering':read(C/'rendering-02-execution.json'),
          'install':install},
          'limits':['Loopback local application; no production deployment or external message delivery.',
                    'No account invitation/password reset/verified identity migration or automation scheduler.',
                    'No all-browser, power-loss, unknown-schema or malware-scanning certification.']}
(C/'results.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
(S/'verification/validated-results.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')

p=S/'astraupskill/VERIFICATION.md'
text=p.read_text(encoding='utf-8')
start=text.index('## Evidence available during the implementation')
end=text.index('## Reproduce the checks',start)
text=text[:start]+'''## Completed evidence

The delivered implementation has **176 distinct passing checks**: 156 backend tests, 15 real browser workflow checks, and five isolated rendering probes. Repeated regression and clean-environment smoke cases are counted once. The machine-readable [validated results](../verification/validated-results.json) retain the executed commands and outcomes.

The complete backend run `full-01` passed 154 tests (411.14 pytest seconds). It covered the original workflows, contracts, authentication, calendar arithmetic, migration preservation and rollback, scoped reports, intake receipts, history movement, CRUD, attachments, setup, and storage audit. Subsequent timer review added two regressions. The 12-case focused run passed both new timer checks and ten existing CRUD/original-workflow checks; the union contains 156 backend cases.

The final Chromium run `browser-05` passed all 15 workflow checks against a new disposable dataset. It exercised administrator sign-in, customer and canned-reply CRUD, all seven administration forms, stale edits with retained drafts, staff ticket creation/edit/reply, a private attachment download, customer history/reply, deletion, and an accepted anonymous submission whose response was deliberately lost. No uncaught browser script errors were observed. The final five rendering probes passed hostile text through ticket lists, message bodies, attachment names, metadata, selectors, and the administration list helper.

A fresh virtual environment installed the 30-package version lock and this project. `pip check` passed. A wheel built successfully and contained all five templates and both static assets. Its clean-environment contract/boundary/timer smoke run passed 53 tests. These repeat cases strengthen setup evidence and are not added again to the distinct total. Node syntax validation passed. Python formatting preserved the parsed abstract syntax trees of all 33 checked Python files.

Earlier browser runs exposed an ambiguous administration selector label and a test timeout that still used Playwright's five-second assertion default. Those were corrected. Screenshot review then found low-contrast list text, stretched sidebar controls, and a mobile image captured before form initialization. A later run exposed an enabled Delete control whose handler was still busy refreshing after a save. The final run verifies that newly rendered fields and related actions remain disabled until the operation completes, along with the corrected presentation and readiness checks. All nine final screenshots were opened and reviewed for readable content and layout; page-width checks found no horizontal overflow at the tested viewports.

| Reviewed view | Screenshot |
| --- | --- |
| Empty login and navigation | [Desktop home](images/01-home-desktop.png) |
| Customer editor with literal hostile text | [Customer editor](images/02-customer-editor.png) |
| Retained draft and latest-record comparison | [Conflict review](images/03-conflict-review.png) |
| Administration list and form | [Desktop administration](images/04-administration-desktop.png) |
| Ticket fields and public conversation | [Desktop staff workspace](images/05-staff-desktop.png) |
| Ticket workspace at 390 pixels | [Mobile staff workspace](images/06-staff-mobile.png) |
| Loaded administration form at 390 pixels | [Mobile administration](images/07-administration-mobile.png) |
| Anonymous submission receipt | [Mobile portal](images/08-portal-mobile.png) |
| Signed-in public conversation | [Customer history](images/09-portal-history.png) |

''' +text[end:]
start=text.index('Final result placeholders:')
text=text[:start]+'''The recorded checks passed for this delivery. They do not replace the explicit operational limits above. Use a new data/output directory when reproducing an experiment, and retain its logs and results rather than overwriting previous evidence.
'''
p.write_text(text,encoding='utf-8')

baseline=read(B/'baselines/19110bf39fcf.json')['files']
changed=[]
for path in S.rglob('*'):
    if not path.is_file():continue
    rel=path.relative_to(S).as_posix();parts=path.relative_to(S).parts
    if any(part in {'__pycache__','.pytest_cache','.venv','build','dist'} or part.endswith('.egg-info') for part in parts):continue
    if parts[0] not in {'app','tests','verification','docs','astraupskill'} and rel not in {'README.md','pyproject.toml','.gitignore','requirements.lock'}:continue
    if rel.startswith('astraupskill/') and len(parts)==2 and path.suffix=='.md':continue
    if path.suffix in {'.pyc','.db','.sqlite3','.log'}:continue
    if baseline.get(rel)!=hashfile(path):changed.append(rel)
spec={'changedFiles':sorted(changed),'summary':[
    'Added strict request contracts, consistent role visibility/report scoping, active-token checks, safe rendering and explicit owner/demo setup.',
    'Implemented versioned ticket/configuration CRUD, retained-draft conflict review, same-transaction creation receipts, additive backed-up migration and serialized SQLite writes.',
    'Corrected terminal/reopen/pending reply timers, protected history/identity merges and references, bounded attachment handling with rollback cleanup and authorized downloads.',
    'Added nine detailed junior-to-mid-level learning guides, worked examples, trace labs, regression suites, a clean verified installation and nine reviewed browser screenshots.'
], 'checks':{'format':'json','resultsFile':'checks/e15/results.json','expectedTests':176,
             'environment':'Windows; Python 3.13; FastAPI 0.135.1; SQLAlchemy 2.0.48; Pydantic 2.13.4; pytest 9.0.2; Chromium 148 via Playwright 1.59.0'},
    'limits':[
        'Local loopback learning application; no outbound email/provider integration, scheduled worker, production hosting, account invitations or password reset.',
        'Customer identity transfers with linked sign-in accounts are refused; verified identity migration remains a separate exercise.',
        'Ticket deletion retains stored history; referenced configuration and the required default policy cannot be deleted.',
        'Drafts are in-memory; abrupt process termination may leave orphan uploads for the read-only audit. No malware scanning or power-loss/all-browser guarantee.',
        'Unknown legacy schemas are refused for manual review. Version lock reproduces tested Windows dependencies and is not hash-based.'
    ]}
(B/'specs/19110bf39fcf.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
print(json.dumps({'changedFilesBeforeCourse':len(changed),'distinctChecks':176,'courseWords':sum(len(p.read_text(encoding='utf-8').split()) for p in (S/'astraupskill').glob('*.md'))},indent=2))
