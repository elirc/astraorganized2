"""Assemble evidence and a finite manifest only after final checks pass."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,shutil,sys
from urllib.parse import unquote

C=Path(__file__).resolve().parent;B=C.parents[1];S=B/'stage/ca549816cdd1'
baseline=json.loads((B/'baselines/ca549816cdd1.json').read_text(encoding='utf-8'))
full=json.loads((C/'full-01.json').read_text(encoding='utf-8'))
delta=json.loads((C/'final-delta-01.json').read_text(encoding='utf-8'))
encoding=json.loads((C/'encoding-01.json').read_text(encoding='utf-8'))
browser=json.loads((C/'browser-04/result.json').read_text(encoding='utf-8'))
package=json.loads((C/'package-02/result.json').read_text(encoding='utf-8'))
quality=json.loads((C/'quality-final.json').read_text(encoding='utf-8'))
assert full['exitCode']==delta['exitCode']==encoding['exitCode']==0
assert '105 passed' in (C/'full-01.log').read_text(encoding='utf-8')
assert '18 passed' in (C/'final-delta-01.log').read_text(encoding='utf-8')
assert browser['passed'] and browser['serverStopped'] and len(browser['checks'])==12
assert package['passed'] and len(package['checks'])==4 and quality['passed']
evidence={
    'passed':True,'verifiedAt':datetime.now(timezone.utc).isoformat(),
    'pythonDistinctTests':106,'browserWorkflowChecks':12,'packagingChecks':4,'totalChecks':122,
    'pythonEvidence':{'fullSuite':105,'focusedFinalRegressionRun':18,'note':'The focused run repeats 17 existing cases and adds one trace-alert stream regression. Encoding assertions were added to an existing HTTP case and rerun separately.'},
    'browserChecks':browser['checks'],'packaging':package['checks'],'quality':quality,
    'originalDatabaseOpened':False,'externalNotificationsSent':False,
    'screenshotsReviewed':['desktop.png','mobile.png'],
    'limitations':['Local single-node SQLite application; no public deployment or distributed scheduler.', 'Dashboard configuration editor, not a rendered chart engine; OTLP aliases use custom envelopes.', 'JSON merges operate per field; CRUD creates have no general operation receipts.', 'Webhook tests use fake senders and mocked DNS, with no live provider delivery.', 'Migration verified on synthetic historical schemas; legacy naive timestamps are interpreted as UTC.', 'Direct dependency versions pinned; no complete operating-system or transitive dependency lock.'],
}
(C/'results.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
(S/'astraupskill/evidence.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
images=S/'astraupskill/images';images.mkdir(exist_ok=True)
for name in ['desktop.png','mobile.png']:shutil.copyfile(C/'browser-04'/name,images/name)
required=['README.md','01-CODEBASE-MAP.md','02-CONCEPTS.md','03-WORKED-CHANGE.md','04-TESTING-AND-DEBUGGING.md','05-PRACTICE.md','06-SOLUTIONS-AND-REVIEW.md','07-TRACE-LAB.md','VERIFICATION.md']
for name in required:
    p=S/'astraupskill'/name;text=p.read_text(encoding='utf-8');assert len(text.split())>=250
    for url in re.findall(r'\]\(([^)]+)\)',text):
        if re.match(r'[a-z]+:|#',url,re.I):continue
        assert (p.parent/unquote(url.split('#')[0])).exists(),(name,url)
preserved=list((S/'docs/original').rglob('*.txt'));assert len(preserved)==30
for p in preserved:
    original=p.relative_to(S/'docs/original').as_posix()[:-4]
    assert hashlib.sha256(p.read_bytes()).hexdigest()==baseline['files'][original],original
changed=[]
for p in sorted(S.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(S);parts=rel.parts
    if any(part in {'.git','__pycache__','.pytest_cache','.ruff_cache','build','dist','data','learning-data','.venv'} or part.endswith('.egg-info') for part in parts):continue
    if p.suffix in {'.db','.sqlite','.pyc','.log'}:continue
    name=rel.as_posix()
    if name in {'astraupskill/'+item for item in required}:continue
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    if baseline['files'].get(name)!=digest:changed.append(name)
spec={
    'id':'ca549816cdd1','changedFiles':changed,
    'summary':[
        'Added a responsive browser workspace and complete tenant-scoped CRUD for streams, dashboards, alerts, pipelines and saved queries, with bounded pagination, atomic audits, protected references and explicit revision conflict review.',
        'Strengthened current-user/token authorization, privilege grant limits, expiring sessions, strict typed and nested configuration validation, finite JSON, raw request limits and local host/origin boundaries.',
        'Made ingestion deduplication, derived metrics, pipeline history and organization retention transactional; fixed partial pipeline output, selected manual runs, trace cycles and cross-trace log correlation.',
        'Bounded SQL with an isolated tenant subset, authorizer and timeout; corrected filter-before-limit behavior, UTC grouping, mixed label grouping and alert counts/stream selection. Moved notifications to a default-simulated durable outbox with explicit operator delivery.',
        'Pinned tested direct dependencies, verified an installed wheel with browser assets, added explicit additive migration and preserved 30 original text files. Added nine detailed junior-to-mid-level CRUD guides with examples, exercises, solutions and reviewed screenshots; verified 106 distinct Python cases, 12 real-browser workflows and four packaging checks, plus lint/format/JavaScript syntax.',
    ],
    'checks':{'format':'json','resultsFile':'checks/e14/results.json','expectedTests':122},
    'limits':evidence['limitations']+['Original user database was not opened, migrated or replaced. Existing data requires explicit backup/migration or a separate fresh learning database.', 'User/token management remains API-based; account recovery and general user membership editing are not implemented.', 'Uncertain or crashed notification claims require operator investigation and are not automatically retried.'],
}
(B/'specs/ca549816cdd1.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
print(json.dumps({'changedFiles':len(changed)+9,'courseWords':sum(len((S/'astraupskill'/name).read_text(encoding='utf-8').split()) for name in required),'checks':122,'preservedOriginals':len(preserved)}))
