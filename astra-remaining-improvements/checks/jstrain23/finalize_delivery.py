from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import unquote
import json,hashlib,os,re,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
C=Path(__file__).resolve().parent;B=C.parents[1];S=B/'stage/58c5c289a8ce';ID='58c5c289a8ce'
run=sys.argv[1];assert run.replace('-','').isalnum()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (B/'deliveries'/f'{ID}.json').exists(),'Inspect existing delivery rather than preparing twice'
node=read(C/'final-01.json');assert node['exitCode']==0
nodeLog=(C/'final-01.log').read_text(encoding='utf-8');assert '# tests 97' in nodeLog and '# pass 97' in nodeLog and '# fail 0' in nodeLog
lint=read(C/'lint-05.json');build=read(C/'build-06.json');assert lint['exitCode']==build['exitCode']==0
browser=read(C/run/'result.json');assert browser['passed'] and len(browser['checks'])==browser['count']
baseline=read(B/'baselines'/f'{ID}.json')['files']
for p in (S/'docs/original').rglob('*.txt'):
    rel=p.relative_to(S/'docs/original').as_posix()[:-4];assert digest(p)==baseline[rel],rel
package=read(S/'package.json');lock=read(S/'package-lock.json');assert package['dependencies']==lock['packages']['']['dependencies'];assert package['devDependencies']==lock['packages']['']['devDependencies']
assert package['dependencies']['next']==package['devDependencies']['eslint-config-next']=='16.3.3'
images=S/'astraupskill/images';images.mkdir(exist_ok=True)
screens=[]
for name in browser['screenshots']:
    shutil.copyfile(C/run/name,images/name);screens.append({'file':'images/'+name,'sha256':digest(images/name),'visuallyReviewed':True})
# Ship the exact exercised harness with only project-local path/Chromium discovery
# adaptation. It creates a fresh database and never opens the configured user DB.
harness=(C/'browser_check.py').read_text(encoding='utf-8')
harness=harness.replace("C=Path(__file__).resolve().parent;S=C.parents[1]/'stage/58c5c289a8ce'","S=Path(__file__).resolve().parents[1];C=S/'.browser-checks';C.mkdir(exist_ok=True)")
harness=harness.replace("executable=os.environ.get('ASTRA_BROWSER_EXECUTABLE',str(C.parents[1]/'playwright-browsers/chromium-1223/chrome-win64/chrome.exe'))","executable=os.environ.get('ASTRA_BROWSER_EXECUTABLE')")
(S/'scripts/browser-check.py').write_text(harness,encoding='utf-8');compile(harness,'scripts/browser-check.py','exec')
ignore=S/'.gitignore';ignore.write_text(ignore.read_text(encoding='utf-8')+'\n/.browser-checks/\n',encoding='utf-8')
limits=[
 'Local single-owner workspace; visibility labels are metadata, and presence is limited to same-origin tabs.',
 'No durable operation receipts, account recovery, encrypted browser draft storage or general JSON restore UI.',
 'Bounded whole-document JSON model, rolling server activity and bounded snapshots; standard duplicate-key JSON parsing remains.',
 'Legacy adoption is explicit, validates accepted content and preserves legacy tables; incompatible existing data requires deliberate investigation, not automatic repair.',
 'Markdown import/export covers a block subset and table text, not a lossless workspace round trip.',
 'Chromium desktop/mobile checks on Windows; not all browsers, operating systems or assistive technologies. One network failure is deliberately simulated.',
 'Fresh database setup and installed lock consistency verified; no separate full clean-copy dependency installation was performed after the version update.',
 'Original user database was not opened, migrated or replaced during this delivery.'
]
results={'passed':True,'date':datetime.now(timezone.utc).isoformat(),'project':'_Organized Desktop/04 JavaScript Training/jstrain2.3','distinctChecks':97+browser['count'],'nodeTests':97,'browserWorkflowGroups':browser['count'],'countsNote':'Node tests plus the enumerated browser/HTTP/setup workflow groups. Repeated and failed runs are not counted again. Build and lint are additional checks.','node':node,'lint':lint,'build':build,'browser':browser,'screenshots':screens,'limits':limits,'sourceHashes':{p.relative_to(S).as_posix():digest(p) for p in (S/'src').rglob('*') if p.is_file()}}
(C/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');(S/'astraupskill/verification-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
p=S/'astraupskill/VERIFICATION.md';text=p.read_text(encoding='utf-8')
text=text.replace('The final run and reviewed screenshots are attached when this project is delivered. Until that final evidence exists, this staged working copy is not a completed delivery.','The final run passed all '+str(browser['count'])+' enumerated browser/HTTP/setup workflow groups. Together with 97 Node tests, that is '+str(results['distinctChecks'])+' recorded checks. The production build and lint also passed. The reviewed screenshots and exact results are attached below.')
text+='''
## Final recorded evidence

- [Machine-readable results, checks and limits](verification-results.json)
- [Accepted workspace at desktop width](images/workspace-desktop.png)
- [Workspace at 390-pixel width](images/workspace-mobile.png)

The final browser run exercised real two-tab stale writes, explicit conflict choices, independent draft keys, unreviewed-draft retention across sign-out, offline recovery using actual IndexedDB, comment creation/editing/replies/resolution and related-data deletion. Early harness runs exposed selector assumptions; a later run exposed a real stale save-status bug when a view was changed back to the already accepted setting. That behavior was fixed and added to the Node regressions before the final run. The original user database was never used as a fixture.

To rerun the optional browser harness, first build the app. Use Python with Playwright 1.59.0 and its Chromium installation, or set `ASTRA_BROWSER_EXECUTABLE` to a compatible installed Chromium executable. Run `python scripts/browser-check.py review-01`. Choose a new run name each time: the harness refuses to overwrite evidence. It starts and stops its own loopback Next server, creates a new database under `.browser-checks`, and retains logs/screenshots for inspection. The shipped harness differs from the recorded working harness only in project-local paths and Chromium discovery; those adaptations are syntax-checked.
'''
p.write_text(text,encoding='utf-8')
required={'astraupskill/'+name for name in ['README.md','01-CODEBASE-MAP.md','02-CONCEPTS.md','03-WORKED-CHANGE.md','04-TESTING-AND-DEBUGGING.md','05-PRACTICE.md','06-SOLUTIONS-AND-REVIEW.md','07-TRACE-LAB.md','VERIFICATION.md']}
files=[]
for directory,folders,names in os.walk(S):
    folders[:]=[name for name in folders if name not in {'node_modules','.next','.data','.git','.browser-checks','__pycache__'}]
    for name in names:
        p=Path(directory)/name;rel=p.relative_to(S).as_posix()
        if rel not in required and digest(p)!=baseline.get(rel):files.append(rel)
for p in [S/'README.md',*(S/'astraupskill').glob('*.md'),S/'_learning/README.md']:
    for url in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if re.match(r'[a-z]+:|#',url,re.I):continue
        assert (p.parent/unquote(url.split('#')[0])).exists(),(p,url)
summary=[
 'Reworked the existing Next/SQLite knowledge workspace with explicit owner setup/adoption, loopback request boundaries, bearer authorization, strict relational JSON validation and atomic revision-checked writes.',
 'Integrated accepted-state save status, generation-aware autosave, independent retained drafts for each editing session, explicit saved-draft recovery and three-way conflict review; cross-tab notices no longer overwrite drafts.',
 'Improved page/subtree, block and comment CRUD; typed database records, property cleanup, filters/sorts and usable table/board/calendar/list/gallery views; authenticated exports and fenced-code Markdown import.',
 'Added paginated snapshot inspection, restore and deletion; restored content preserves current hierarchy and visibility labels. Updated Next and its lint package to 16.3.3 and removed seven unused direct dependencies.',
 f'Added nine detailed junior-to-mid-level CRUD learning guides with worked examples, source traces, failure labs, exercises and review outlines; preserved 46 original text files and marked older learning notes as historical. Verified 97 Node tests and {browser["count"]} browser/HTTP/setup workflow groups, plus build and lint.'
]
spec={'id':ID,'changedFiles':sorted(files),'summary':summary,'checks':{'format':'json','resultsFile':'checks/jstrain23/results.json','expectedTests':results['distinctChecks']},'limits':limits}
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
print(json.dumps({'files':len(files)+len(required),'courseWords':sum(len((S/name).read_text(encoding='utf-8').split()) for name in required),'checks':results['distinctChecks'],'readyForFinitePreparation':True}))
