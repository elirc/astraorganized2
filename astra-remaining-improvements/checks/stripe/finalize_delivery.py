"""Create a finite delivery specification from final, independently recorded evidence."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import unquote
import hashlib
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET

C = Path(__file__).resolve().parent
B = C.parents[1]
S = B / 'stage/af19f6e32dba'
browser_name = sys.argv[1]
baseline = json.loads((B / 'baselines/af19f6e32dba.json').read_text(encoding='utf-8'))
full = json.loads((C / 'full-01.json').read_text(encoding='utf-8'))
assert full['exitCode'] == 0
counter = ET.parse(C / 'full-01-results/full-01.trx').find('.//{*}Counters')
assert counter is not None
assert int(counter.attrib['total']) == int(counter.attrib['passed']) == 66
assert int(counter.attrib['failed']) == int(counter.attrib['notExecuted']) == 0
browser = json.loads((C / browser_name / 'result.json').read_text(encoding='utf-8'))
assert browser['passed'] and browser['serverStopped'] and len(browser['checks']) == 15 and not browser['pageErrors']
package = json.loads((C / 'package-checks.json').read_text(encoding='utf-8'))
assert package['passed'] and len(package['checks']) == 3
assert json.loads((C / 'package-01.json').read_text(encoding='utf-8'))['exitCode'] == 0
assert json.loads((C / 'package-02.json').read_text(encoding='utf-8'))['exitCode'] == 0
for name in ['web-audit-all-01', 'net-audit-01', 'lock-web-01', 'lock-net-01']:
    assert json.loads((C / (name + '.json')).read_text(encoding='utf-8'))['exitCode'] == 0
visual = json.loads((C / 'visual-review.json').read_text(encoding='utf-8'))
assert visual['passed'] and visual['browserRun'] == browser_name
quality = json.loads((C / 'quality.json').read_text(encoding='utf-8'))
assert quality['passed']
evidence = {
    'passed': True, 'verifiedAt': datetime.now(timezone.utc).isoformat(),
    'backendAndHttpTests': 66, 'browserWorkflowChecks': 15, 'packagingChecks': 3, 'totalChecks': 84,
    'browserChecks': browser['checks'], 'packaging': package['checks'], 'quality': quality,
    'dependencyAudits': 'npm full installed tree and NuGet API transitive tree reported no known advisories at verification time.',
    'screenshotsReviewed': visual, 'originalDatabaseOpened': False,
    'realPaymentsOrExternalMessages': False, 'originalTextFilesPreserved': 125,
    'limitations': [
        'Loopback-only single-node SQLite simulator; no public deployment, real payment provider, outgoing HTTP delivery or automatic billing scheduler.',
        'USD/EUR/GBP only; no taxes, proration, refunds, credit notes or currency conversion.',
        'Relational identity/relationship tables wrap immutable JSON records; some internal workflows materialize bounded collections. Limit: 5,000 domain records per workspace.',
        'Eight-hour in-memory browser session, 24-hour durable operation receipts; pending browser retry state is lost when the tab closes. Auth registration/login are outside the receipt protocol.',
        'Owner/Operator/Viewer membership management is implemented, but no password-change/recovery flow, invitation email, federated identity, existing-account workspace linking or owner transfer.',
        'Original data was not opened or replaced. Unknown database files are refused; migration requires separate reviewed work or a new learning database path.',
        'Provider callback signatures use a custom local HMAC protocol, not Stripe compatibility. Audit and provider-event history have no retention UI.',
        'Historical documentation is labeled and preserved; proposed course exercises are not counted as implemented functionality.'
    ]
}
(C / 'results.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
(S / 'astraupskill/evidence.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
images = S / 'astraupskill/images'
images.mkdir(exist_ok=True)
for name in ['desktop.png', 'narrow.png']:
    shutil.copyfile(C / browser_name / name, images / name)
required = ['README.md', '01-CODEBASE-MAP.md', '02-CONCEPTS.md', '03-WORKED-CHANGE.md', '04-TESTING-AND-DEBUGGING.md',
            '05-PRACTICE.md', '06-SOLUTIONS-AND-REVIEW.md', '07-TRACE-LAB.md', 'VERIFICATION.md']
for name in required:
    path = S / 'astraupskill' / name
    text = path.read_text(encoding='utf-8')
    assert len(text.split()) >= 250, name
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if re.match(r'[a-z]+:|#', link, re.I):
            continue
        assert (path.parent / unquote(link.split('#')[0])).exists(), (name, link)
preserved = list((S / 'docs/original').rglob('*.txt'))
assert len(preserved) == 125
for path in preserved:
    original = path.relative_to(S / 'docs/original').as_posix()[:-4]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == baseline['files'][original], original
changed = []
excluded = {'.git', 'node_modules', 'bin', 'obj', 'dist', 'wwwroot', '.artifacts', 'App_Data', '__pycache__', '.ruff_cache', 'TestResults'}
for path in sorted(S.rglob('*')):
    if not path.is_file():
        continue
    rel = path.relative_to(S)
    if any(part in excluded for part in rel.parts) or path.suffix in {'.sqlite', '.db', '.pyc', '.log', '.tsbuildinfo'}:
        continue
    name = rel.as_posix()
    if name in {'astraupskill/' + item for item in required}:
        continue
    if hashlib.sha256(path.read_bytes()).hexdigest() != baseline['files'].get(name):
        changed.append(name)
spec = {
    'id': 'af19f6e32dba', 'changedFiles': changed,
    'summary': [
        'Replaced volatile global state with durable SQLite workspaces, current-role authorization, revocable sessions, Owner/Operator/Viewer membership management, parameterized queries and protected cross-workspace relationships.',
        'Completed customer/plan/coupon CRUD, archive rules, subscription cancellation and unused-record deletion, pre-invoice usage editing/deletion, invoice inspection/voiding, searchable paginated lists and responsive React forms.',
        'Added strong ETag preconditions, preserved stale drafts and exact browser retries backed by transactional 24-hour receipts and atomic audit history; verified concurrent same-key requests and a response lost after commit.',
        'Fixed money bounds and serialization, mixed-currency totals, anchored billing catch-up, atomic invoice/usage/subscription/outbox updates, payment-attempt identity, terminal payment protection and signed event deduplication. All payments and outgoing events remain explicit local simulations.',
        'Fixed baseline builds, pinned and locked verified .NET/React dependencies, removed the shared default signing secret, added local run/check/package scripts, preserved 125 original text files, labeled 93 historical pages and added nine detailed CRUD learning guides. Verified 66 backend/HTTP tests, 15 real-browser workflows and three packaging checks, with reviewed desktop/narrow images.'
    ],
    'checks': {'format': 'json', 'resultsFile': 'checks/stripe/results.json', 'expectedTests': 84},
    'limits': evidence['limitations']
}
(B / 'specs/af19f6e32dba.json').write_text(json.dumps(spec, indent=2), encoding='utf-8')
print(json.dumps({'files': len(changed) + 9, 'guides': 9, 'courseWords': sum(len((S / 'astraupskill' / name).read_text(encoding='utf-8').split()) for name in required), 'checks': 84}))
