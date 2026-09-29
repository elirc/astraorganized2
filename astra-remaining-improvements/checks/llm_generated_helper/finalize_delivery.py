from pathlib import Path
from urllib.parse import unquote
from datetime import datetime, timezone
import hashlib,json,re,shutil,subprocess

C=Path(__file__).resolve().parent;B=C.parents[1];S=B/'stage/44013f102ff1'
assert not (B/'deliveries/44013f102ff1.json').exists(), 'Delivery already prepared; inspect rather than regenerate'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline=read(B/'baselines/44013f102ff1.json')['files']
node=read(C/'final-01.json');assert node['exitCode']==0
output=(C/'final-01.log').read_text(encoding='utf-8')
assert '# tests 120' in output and '# pass 120' in output and '# fail 0' in output
before=read(C/'settings-before.json');assert before['exitCode']==1
assert '# fail 8' in (C/'settings-before.log').read_text(encoding='utf-8')
assert read(C/'settings-after.json')['exitCode']==0
browser=read(C/'browser-03/results.json');renderer=read(C/'renderer-02/results.json');clean=read(C/'clean-01/results.json')
assert browser['passed'] and len(browser['checks'])==14
assert renderer['passed'] and len(renderer['checks'])==6
assert clean['passed'] and clean['repeatedNodeTests']==120
# Clean-copy domain/server tests cover the final production modules. Only the
# separately rechecked renderer JS/CSS changed after that copy was made.
copy=C/'clean-01/source'
for p in (S/'src').rglob('*'):
    if p.is_file() and p.relative_to(S).as_posix() not in {'src/renderer/app.js','src/renderer/styles.css'}:
        assert digest(p)==digest(copy/p.relative_to(S)),p
syntax=subprocess.run(['node','--check','src/renderer/app.js'],cwd=S,capture_output=True,text=True)
assert syntax.returncode==0,syntax.stderr
images=S/'astraupskill/images';images.mkdir(exist_ok=True)
screens=[]
for directory,names in [('browser-03',browser['screenshots']),('renderer-02',['05-settings-draft.png'])]:
    for name in names:
        source=C/directory/name;target=images/name;shutil.copyfile(source,target)
        screens.append({'file':'images/'+name,'sha256':digest(target),'sourceRun':directory,'visuallyReviewed':True})
limits=[
    'Single-owner loopback JSON application; no distributed database, power-loss guarantee, import, token recovery or durable creation receipts.',
    'Global revision, bounded collections/file and rolling 1000-entry activity; stale writer leases require explicit investigation.',
    'Persisted structure/reference checks are not exhaustive history validation; standard JSON duplicate-key behavior remains.',
    'Desktop renderer uses a mocked preload bridge; native Electron, OS encryption, capture, live providers and Windows installer were not run.',
    'Existing Electron dependencies retained; no claim they are current. Provider streaming/body-limit behavior was not fully hardened.',
    'Browser checks cover Chromium desktop/mobile workflows, not all browsers or assistive technologies.'
]
results={
    'passed':True,'date':datetime.now(timezone.utc).isoformat(),'project':'geminiorganized/LLM_Generated_Helper',
    'distinctChecks':140,'nodeTests':120,'browserChecks':14,'mockedRendererChecks':6,
    'baselineNodeTests':73,'regressionsFailedBefore':8,'regressionsPassedAfter':8,
    'nodeRun':node,'browser':browser,'mockedRenderer':renderer,'freshSetup':clean,
    'countsNote':'140 = 120 Node + 14 real journal browser + 6 mocked desktop renderer checks. Four fresh-copy/setup groups are supplemental; the repeated 120 tests are not added again.',
    'finalRendererChanges':'After the clean-copy check, prevented textarea flex shrink and cleared stale saved status before a new save. renderer-02 passed all six checks including these assertions; final renderer syntax passed.',
    'failedBrowserRuns':'browser-01 and browser-02 stopped on assertions expecting different words than the correct rejection messages. Assertions were corrected; browser-03 passed all 14 workflows.',
    'screenshots':screens,'limits':limits,
    'sourceHashes':{p.relative_to(S).as_posix():digest(p) for p in (S/'src').rglob('*') if p.is_file()}
}
(C/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
(S/'astraupskill/verification-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
verification=S/'astraupskill/VERIFICATION.md'
text=verification.read_text(encoding='utf-8')
assert '## Reviewed screenshots' not in text
text+='''
## Reviewed screenshots

The final evidence includes 14 passing journal browser workflows and six passing desktop renderer checks, for 140 distinct checks together with the 120 Node tests. Four additional clean-copy/setup groups passed; their repeated test cases are not counted again. The last renderer layout/status adjustment was rechecked in Chromium and parsed after the clean-copy run.

- [Stale profile draft and accepted-state comparison](images/01-conflict-review.png)
- [Attempt editor, historical question and zero score](images/02-attempt.png)
- [Accepted profile and export confirmation](images/03-profile.png)
- [Narrow-screen journal after dependency-ordered deletion](images/04-mobile.png)
- [Mocked desktop settings: readable retained draft and failed-save notice](images/05-settings-draft.png)
'''
verification.write_text(text,encoding='utf-8')
course_names=['README.md','01-CODEBASE-MAP.md','02-CONCEPTS.md','03-WORKED-CHANGE.md','04-TESTING-AND-DEBUGGING.md','05-PRACTICE.md','06-SOLUTIONS-AND-REVIEW.md','07-TRACE-LAB.md','VERIFICATION.md']
required={'astraupskill/'+name for name in course_names}
changed=[]
for p in S.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(S).as_posix()
    assert not any(part in {'node_modules','data','__pycache__','.git'} for part in p.relative_to(S).parts),rel
    if rel not in required and digest(p)!=baseline.get(rel):changed.append(rel)
for name in course_names:
    p=S/'astraupskill'/name;assert len(p.read_text(encoding='utf-8').split())>=250
for p in [S/'README.md',*(S/'astraupskill').glob('*.md'),*(S/'docs').glob('*.md')]:
    if p.name=='ALTERNATIVE_APP_SPEC.md':continue
    for url in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if re.match(r'[a-z]+:|#',url,re.I):continue
        assert (p.parent/unquote(url.split('#')[0])).exists(),(p,url)
originals=list((S/'docs/original').rglob('*.txt'));assert len(originals)==27
for p in originals:
    rel=p.relative_to(S/'docs/original').as_posix()[:-4]
    assert digest(p)==baseline[rel],rel
spec={'changedFiles':sorted(changed),'summary':[
    'Added a dependency-free local CRUD Practice Journal for profiles, questions, sessions and scored attempts, with snapshots, lifecycle rules, archive/reference protection and authenticated export.',
    'Implemented bounded JSON persistence with exclusive writer leases and byte revisions, typed HTTP input, owner setup that refuses overwrite, and server search/pagination.',
    'Built the journal UI with typed edits, in-memory sign-in, retained drafts, explicit stale/uncertain-write review, responsive layout and a complete practice workflow.',
    'Repaired existing settings acceptance/encryption/error behavior; introduced write-only credential forms, trusted-frame IPC, cancellation, visible startup errors and readable settings layout.',
    'Added nine detailed learning guides, worked regressions, exercises/solutions, trace labs, reproducible verification and five reviewed screenshots; preserved 27 original code/documentation snapshots and updated documentation entry points.'
], 'checks':{'format':'json','resultsFile':'checks/llm_generated_helper/results.json','expectedTests':140},'limits':limits}
(B/'specs/44013f102ff1.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
print(json.dumps({'changedFilesIncludingCourse':len(changed)+9,'courseWords':sum(len((S/'astraupskill'/n).read_text(encoding='utf-8').split()) for n in course_names),'distinctChecks':140,'originalSnapshots':27,'imagesReviewed':len(screens)}),flush=True)
