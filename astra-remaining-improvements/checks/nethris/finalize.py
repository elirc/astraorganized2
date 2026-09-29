"""Create a finite delivery specification only after all recorded checks pass."""
from pathlib import Path
import hashlib
import json
import os
import re
import xml.etree.ElementTree as ET

C = Path(__file__).resolve().parent
B = C.parents[1]
S = B / 'stage/71e7b036865c'
P = C / 'package-browser-03'
pid = '71e7b036865c'
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
progress = read(B / 'progress.json')
assert next(row for row in progress['projects'] if row['id'] == pid)['status'] != 'complete'
reports = list((C / 'foundation-final-results').glob('*.trx'))
assert len(reports) == 1
counters = ET.parse(reports[0]).find('.//{*}Counters').attrib
assert int(counters['total']) == int(counters['passed']) == 13 and int(counters['failed']) == 0
http = read(C / 'http-final-evidence.json')
browser = read(C / 'browser-final-evidence.json')
for result, script in [(http, 'check_api.py'), (browser, 'check_browser.py')]:
    assert result['passed'] is True and result['count'] == len(result['checks'])
    assert result['count'] == len(re.findall(r"\bcheck\('[^']+'\)", (S / 'scripts' / script).read_text(encoding='utf-8')))
for name in ['package-01', 'frontend-final']:
    assert read(C / (name + '.json'))['exitCode'] == 0
review = read(C / 'images-reviewed.json')
assert review['reviewed'] is True
for name in ['desktop.png', 'narrow.png']:
    assert review['sha256'][name] == digest(S / 'astraupskill/images' / name)
dist = {p.relative_to(S / 'client/dist').as_posix(): digest(p) for p in (S / 'client/dist').rglob('*') if p.is_file()}
published = {p.relative_to(P / 'wwwroot').as_posix(): digest(p) for p in (P / 'wwwroot').rglob('*') if p.is_file()}
assert dist and dist == published
assert not any(p.suffix.lower() in {'.db', '.sqlite', '.sqlite3'} for p in P.rglob('*'))
assert digest(P / 'Nethris.Api.dll') == digest(S / 'server/Nethris.Api/bin/Release/net10.0/Nethris.Api.dll')
baseline = read(B / 'baselines' / (pid + '.json'))['files']
for relative, sha in baseline.items():
    assert digest(S / 'docs/original' / (relative + '.txt')) == sha
npm = read(C / 'npm-audit-evidence.json')
nuget = read(C / 'nuget-audit-evidence.json')
assert npm['metadata']['vulnerabilities']['total'] == 0
assert all(not framework.get('topLevelPackages') and not framework.get('transitivePackages') for project in nuget['projects'] for framework in project.get('frameworks', []))
limits = [
    'Loopback-only single-organization SQLite learning application; no production hosting, payroll, external HR service, notification delivery, account recovery or production abuse-control system.',
    'PTO uses calendar dates including weekends, quarter-hour amounts, at most eight hours per date and an inclusive span of at most 31 dates. This is simplified workshop policy.',
    'Approved PTO is immutable: no approved cancellation/refund. Pending requests can be edited/deleted only before decisions; cancellation retains history. Manager reassignment requires cancellation/resubmission when captured and current managers differ.',
    'Limits: 2,000 employees, 200 departments, 200 job roles, 10,000 PTO requests and 32 manager levels. Selectors load bounded reference lists; SQLite NOCASE indexes use SQLite collation semantics.',
    'Browser sessions and pending operation snapshots stay in memory; reload requires login and loses the browser retry snapshot. Server sessions last eight hours; CRUD receipts last 24 hours. Setup/login/logout are outside the receipt protocol.',
    'Admin account provisioning and password reset are implemented; self-service password change, recovery and federated identity are exercises or out of scope.',
    'Unknown database files are refused. There is no automatic migration or reset of original data; schema changes require a new learning path or a separately reviewed migration.',
    'Original files and historical course pages are preserved and labeled. Proposed exercises are not counted as implemented functionality; focused browser checks are not an exhaustive accessibility or security audit.',
    'One synthetic temporary SQLite file from an earlier failed cleanup remains outside the project because automatic approval review blocked its removal. Cleanup of an older generated browser bundle was also blocked, so verification used a fresh package folder and preserved the earlier build. The harness connection-lifetime bug was corrected; see checks/nethris/cleanup-limitation.json in the central audit workspace.'
]
package_checks = ['locked restores and package build pass', 'published browser assets exactly match the final client build', 'package contains no private database and matches the published API assembly']
total = 13 + http['count'] + browser['count'] + len(package_checks)
result = {'passed': True, 'count': total, 'foundationTests': 13, 'httpChecks': http['checks'], 'browserChecks': browser['checks'],
          'packageChecks': package_checks, 'dependencyAdvisories': {'npm': 0, 'nuget': 0}, 'originalFilesPreserved': len(baseline),
          'historicalPagesMarked': 46, 'imagesReviewed': review, 'limits': limits,
          'commands': ['powershell -NoProfile -ExecutionPolicy Bypass -File scripts/package.ps1',
                       'dotnet test tests/Nethris.Tests/Nethris.Tests.csproj --no-restore',
                       'python scripts/check_api.py', 'python scripts/check_browser.py'],
          'notes': ['Scenario groups contain multiple assertions; repetitions are not added to the distinct count.',
                    'All runtime checks used fresh temporary databases and owned local servers; original databases were not opened.']}
(C / 'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
(S / 'astraupskill/evidence.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
required = ['README.md', '01-CODEBASE-MAP.md', '02-CONCEPTS.md', '03-WORKED-CHANGE.md', '04-TESTING-AND-DEBUGGING.md', '05-PRACTICE.md', '06-SOLUTIONS-AND-REVIEW.md', '07-TRACE-LAB.md', 'VERIFICATION.md']
skip = {'.git', 'node_modules', 'bin', 'obj', 'dist', 'artifacts', '__pycache__', '.learning-results'}
changed = []
for folder, directories, files in os.walk(S):
    directories[:] = [name for name in directories if name not in skip]
    for name in files:
        path = Path(folder) / name
        relative = path.relative_to(S)
        if relative.as_posix() in ['astraupskill/' + name for name in required]:
            continue
        if digest(path) != baseline.get(relative.as_posix()):
            changed.append(relative.as_posix())
summary = [
    'Replaced demo fallback, shared JWT configuration and automatic default-password accounts with real workshop bootstrap, private database signing material, revocable sessions, current-role authorization and separate Admin account administration.',
    'Completed employee, department and job-role CRUD with bounded validation, versioned edits, uniqueness, active/archive choices, manager-cycle and lead-department checks, protected deletion and role-sensitive balance/salary views.',
    'Fixed SQLite timestamp ordering and approval insertion, added exact quarter-hour/cents storage, and implemented PTO bounds, overlap/reservation checks, pending edit/delete/cancel and captured-manager plus distinct-HR approval with atomic balance/history writes.',
    'Added strong ETags, transactional 24-hour receipts and audit records, paginated lists, bounded org traversal and responsive real-API forms that preserve stale drafts, recover exact operations after response loss, and invalidate delayed reads/cached views on session changes.',
    f'Added nine detailed source-grounded CRUD learning guides, preserved 75 exact original files, labeled 46 historical pages, pinned/locked dependencies and supplied local package/check scripts. Verified 13 foundation tests, {http["count"]} HTTP scenarios, {browser["count"]} browser workflows and three packaging checks, with reviewed desktop/narrow images.'
]
spec = {'id': pid, 'changedFiles': sorted(changed), 'summary': summary,
        'checks': {'format': 'json', 'resultsFile': 'checks/nethris/results.json', 'expectedTests': total}, 'limits': limits}
(B / 'specs' / (pid + '.json')).write_text(json.dumps(spec, indent=2), encoding='utf-8')
print(json.dumps({'changedFilesPlusGuides': len(changed) + 9, 'checks': total, 'http': http['count'], 'browser': browser['count']}))
