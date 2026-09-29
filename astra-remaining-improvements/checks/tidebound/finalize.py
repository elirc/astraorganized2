from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import struct

C = Path(__file__).resolve().parent
B = C.parents[1]
S = B / 'stage/4de416cd300b'
read = lambda path: json.loads(path.read_text(encoding='utf-8-sig'))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()

tests = read(C / 'tests-01-results.json')
assert tests['success'] and tests['numTotalTests'] == tests['numPassedTests'] == 44
assert tests['numFailedTests'] == tests['numPendingTests'] == 0
assert read(C / 'tests-01.json')['exitCode'] == 0
unit_names = [test['fullName'] for suite in tests['testResults'] for test in suite['assertionResults']]
assert len(unit_names) == len(set(unit_names)) == 44
library = read(C / 'library-03/results.json')
assert library['passed'] and len(library['checks']) == 19 and not library['errors']
assert read(C / 'browser-library-03.json')['exitCode'] == 0
original = read(C / 'original-browser-01/results.json')
assert original['passed'] and len(original['results']) == 3
assert all(item['exitCode'] == 0 for item in original['results'])
gameplay = read(C / 'original-browser-01/browser-report.json')
assert len(gameplay['checks']) == 13 and not gameplay['errors']
release = read(C / 'original-browser-01/release-report.json')
assert release['production'] and release['roofRaycastPassed'] and release['checklistComplete']
assert not release['externalRequests'] and not release['errors']
performance = read(C / 'original-browser-01/performance-report.json')
assert not performance['errors']
setup = read(C / 'clean-setup-01/results.json')
assert setup['passed'] and setup['normalInstallScriptsEnabled'] and setup['browserPackageMatchesCleanBuild']
assert all(item['exitCode'] == 0 for item in setup['commands'])
assert setup['lockSha256'] == sha(S / 'package-lock.json')
audit = read(C / 'npm-audit-02.log')
assert read(C / 'npm-audit-02.json')['exitCode'] == 0 and audit['metadata']['vulnerabilities']['total'] == 0
comparison = read(C / 'demolition-comparison.json')
assert comparison[0]['afterWood'] == 400 and comparison[1]['afterWood'] == 1000

preserved = read(S / 'docs/original/ORIGINAL_FILES.json')
assert len(preserved) == 42
for entry in preserved:
    assert sha(S / 'docs/original' / entry['file']) == entry['sha256']
images = read(C / 'images-reviewed.json')
for entry in images['images']:
    assert sha(S / 'astraupskill/images' / entry['file']) == entry['sha256']
game_images = []
for filename in ['desktop-game.png', 'mobile-game.png']:
    path = C / 'original-browser-01' / filename
    raw = path.read_bytes()
    width, height = struct.unpack('>II', raw[16:24])
    game_images.append({'file': filename, 'sha256': sha(path), 'width': width, 'height': height,
                        'review': 'Viewed by the agent. The game scene and responsive controls remain readable. Temporary invalid-import and subsequent successful-import toasts are visible from the tested scenario; these are transient notifications, not a current failed load.'})

summary = [
    'Added Tidebound’s persistent voyage library with named snapshots, learning notes, search and pagination, metadata edits, explicit snapshot replacement, archive/restore, confirmed deletion and game JSON export.',
    'Replaced overwrite-only save slots with atomic IndexedDB metadata/snapshot transactions, expected revisions, cross-tab conflict protection, preserved legacy saves, retained drafts and commit-before-load/import/new-game behavior.',
    'Fixed demolition refunds that consumed existing inventory when a paused warehouse left an island over capacity; corrected paused-warehouse capacity handling and preserved the final paused harbor.',
    'Pinned dependencies, updated Vitest to the patched 4.1.11 release, added 21 focused regressions, and added a production-browser library runner that owns its local preview and isolated synthetic data.',
    'Added nine detailed junior-to-mid-level guides, 42 exact original text snapshots, reviewed screenshots, real worked fixes, failure analysis, progressive CRUD exercises and review guidance.',
]
limits = [
    'Browser-local single-player application: no backend, accounts, server authorization, multi-tenancy or cloud synchronization. Collections are origin-specific and may be cleared or evicted.',
    'Game JSON exports contain the saved world, not checkpoint titles or learning notes. Periodic and visibility-change saves do not guarantee completion during browser shutdown.',
    'The original documented route-reassignment teleport simplification remains. This pass focuses on durable CRUD learning and the verified demolition accounting bug; it does not turn the simulation into a multiplayer service.',
    '76 counted cases comprise 44 unit/domain tests, 19 library browser workflows and 13 original gameplay workflows. Clean setup, build, audit, release checks, the source comparison and performance measurements are additional evidence, not inflated into this case count.',
    'Browser evidence is from Chrome 152.0.7977.76 on this Windows machine. Five-second graphics measurements are hardware-specific; the 101-building scene remains below 30 FPS in this run.',
    'Original canonical generated artifacts are preserved. New verification logs and additional gameplay captures remain in the central checks directory; two reviewed library screenshots and the consolidated evidence are included with the course.',
]
evidence = {
    'passed': True, 'project': 'astra2 / Tidebound', 'date': datetime.now(timezone.utc).isoformat(),
    'expectedTests': 76, 'unitTests': unit_names, 'libraryWorkflows': library['checks'], 'gameplayWorkflows': gameplay['checks'],
    'environment': {'node': '22.16.0', 'npmCleanInstall': '10.9.2', 'npmLockGeneration': '11.19.1',
                    'typescript': '5.9.3', 'vite': '7.3.6', 'vitest': '4.1.11', 'fakeIndexedDb': '6.2.5',
                    'playwright': '1.63.0', 'browser': library['browser']},
    'cleanSetup': setup, 'knownAdvisories': 0, 'release': release, 'graphicsMeasurements': performance,
    'demolitionComparison': comparison, 'originalTextFilesPreserved': 42, 'libraryImages': images,
    'additionalGameplayImagesReviewed': game_images, 'summary': summary, 'limits': limits,
}
(C / 'results.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
(S / 'astraupskill/evidence.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
(C / 'game-images-reviewed.json').write_text(json.dumps(game_images, indent=2), encoding='utf-8')

p = S / 'astraupskill/README.md'
t = p.read_text(encoding='utf-8')
old = '**Implementation checkpoint:** this course is being built alongside the isolated project changes. The final verification document must identify completed checks before this project is counted as delivered. Existing reports in the original `artifacts` directory describe earlier versions, not the new library.'
new = '**Verified implementation:** 44 unit/domain tests and 32 real-browser workflows passed. A normal clean install rebuilt the same assets used in the browser checks. Read the [verification record](VERIFICATION.md) for additional gates, exact scope and limits. Older reports in `artifacts` describe their recorded versions; their claims are not substituted for current evidence.'
assert old in t
t = t.replace(old, new)
t += '\n## The verified library\n\nThe production interface was exercised with real browser storage and inspected at both sizes. The narrow dialog scrolls vertically to keep its controls reachable.\n\n![Desktop voyage library](images/desktop.png)\n\n[View the narrow library screenshot](images/narrow.png).\n'
p.write_text(t, encoding='utf-8')

verification = f'''# Verification and practical limits

This course accompanies a verified source revision of Tidebound. Testing ran in an isolated copy using synthetic game data and fresh browser contexts. The original Desktop folder is updated through a finite manifest whose before/after hashes are checked separately. Browser profiles used for verification do not read a person's existing save collection.

## Recorded results

| Check | Result | What it establishes |
| --- | --- | --- |
| Current unit/domain suite | 44 of 44 passed; four test files; process exit 0 | Original simulation behavior plus 18 repository regressions and three demolition regressions |
| New production-library browser suite | 19 of 19 workflows passed | Real IndexedDB, retained drafts, cross-tab edits, CRUD lifecycle, slot integration and storage recovery |
| Original production-game browser suite | 13 of 13 workflows passed | Construction, research, trading, exploration, save/load, import/export, settings, keyboard controls, mobile layout and progress page |
| Normal clean installation | Passed with install scripts enabled | The committed package lock installs with ordinary npm 10.9.2 |
| TypeScript and production build | Passed | Full source/test type checking and both production page entries build |
| Clean-build reconciliation | All {len(setup['assets'])} emitted files match the browser-tested package byte-for-byte | Reinstallation did not change the verified production assets |
| Dependency audit | Zero known advisories reported | Registry advisory results for the locked dependency tree at verification time |
| Release script | Passed; no external requests or page errors | Original roof selection and original release checklist still work in the production build |
| Demolition source comparison | Original wood 1,000 → 400; current wood 1,000 → 1,000 | The reported negative-refund bug was reproduced and its accounting outcome corrected |

The **76 counted cases** are the 44 unit tests plus 19 library workflows plus 13 gameplay workflows. A workflow contains several related assertions. Repeated runs are not added together, and setup/audit/release/performance commands are additional evidence rather than extra counted cases. The [consolidated evidence](evidence.json) includes the case names, environment, package hashes, source comparison, measurements, and screenshot hashes.

## Reproduce the checks

From the project root, install dependencies, run the current suite, and build:

```powershell
npm ci
npm test
npm run build
npm run test:library
```

The library runner starts a production preview on an available loopback port, uses isolated browser contexts, and stops its own preview and browser. It writes `artifacts/library` by default; set `TIDEBOUND_EVIDENCE_DIR` to keep a separate run. `TIDEBOUND_BROWSER_PATH` selects an installed Chrome/Chromium executable. If no supported local executable is available, install the browser through Playwright as explained in the root README.

The original game scripts require a running game server. For production verification, start `npm run preview` in one terminal. In another PowerShell terminal:

```powershell
$env:TIDEBOUND_URL = 'http://127.0.0.1:5181/'
npm run test:browser
node scripts/release-check.mjs
npm run test:performance
```

Those scripts use fresh browser profiles but write generated evidence into `artifacts`. The release checklist describes the original game's 49 tasks and ten phases; it is not a task count for the new course. Exact original text reports and source are preserved in [docs/original](../docs/original/ORIGINAL_FILES.json).

## Environment and setup investigation

Verification used Node 22.16.0, TypeScript 5.9.3, Vite 7.3.6, Three 0.180.0, Vitest 4.1.11, fake-indexeddb 6.2.5, Playwright 1.63.0, and Chrome {library['browser']} on Windows. Direct package versions and their transitive resolution are pinned in the package files. A normal clean install and rebuild completed successfully; all resulting asset hashes matched the tested build.

The initial older-tooling baseline failed five tests whose recorded durations exceeded their configured wall-clock limits and also timed out during teardown. The current suite retains the original domain assertions, uses one worker, and supplies bounded timeouts appropriate to the complete progression benchmark. It passes all 44 cases with a successful process exit. This does not establish that changing the test runner alone caused a performance improvement; machine load and cold-start costs also affect wall time.

The old Vitest dependency was affected by [GHSA-82fw-gwwq-j7x9](https://github.com/advisories/GHSA-82fw-gwwq-j7x9). The lockfile was regenerated using the patched 4.1.11 version. npm 10 encountered an internal peer-resolution error while generating the new tree, and an npx bootstrap later encountered a shared-cache rename error. A locally extracted, registry-checksum-verified npm 11.19.1 generated the lockfile with normal peer checks and a private cache. Ordinary npm 10.9.2 then installed that lock successfully. No peer checks were disabled and no global npm installation or cache cleanup was required.

If your own installation reports a cache-path EEXIST/ENOENT error, use a fresh project-local cache, for example `npm ci --cache .npm-cache`. Do not clear saved browser data to troubleshoot package installation; they are separate storage systems.

## Browser investigation and visual review

An early browser run stalled when it tried to evaluate the hidden first WebGL tab after opening a second tab. The diagnostic still found the checkpoint in the second tab. The final workflow explicitly activates each tab before interacting, as a person would, then verifies the real competing edit and retained losing draft. The database revision rule was not relaxed to make the test pass.

The [desktop library](images/desktop.png) and [narrow library](images/narrow.png) were visually inspected. Text, notes, status messages and controls are readable; the narrow dialog scrolls vertically without horizontal overflow. Keyboard access from notes to Save and Escape dismissal passed. Additional original-game desktop/mobile captures were inspected, including the transient invalid-import and subsequent successful-import notifications produced by that scenario.

## Simulation and graphics measurements

The earned progression test again reached victory at 3,190 simulation seconds with three settlements, 96 residents, all twelve technologies, the monument, and 43 deliveries. The expanded 101-building/six-ship state processed 300 simulation seconds in 716 ms in the recorded unit run. This is simulation throughput, not a human play time or graphics frame rate.

The browser sampled frame callbacks for five seconds per scene at 1440×1000, device pixel ratio 1, on Intel UHD Graphics 620 through ANGLE/Direct3D11. It recorded {performance['initial']['averageFps']} FPS initially, {performance['lateGame']['averageFps']} FPS for the 101-building scene with shadows, and {performance['lateGameNoShadows']['averageFps']} FPS with shadows disabled. These are short, machine-specific observations. The large scene remains below 30 FPS in this run; no universal performance guarantee or renderer speedup is claimed.

## What this project does not provide

The application is a single-player, origin-local browser workshop. There is no server, account authentication, tenant authorization, cloud synchronization, or automatic off-device backup. Browser data may be cleared or evicted. Exports contain game state, while checkpoint titles and learning notes remain library metadata. Automatic writes are periodic and best-effort when visibility changes; asynchronous persistence is not guaranteed to finish during browser shutdown.

The library enforces 50 checkpoints including archived records, 5 MB per serialized world, and 50 MB of aggregate snapshot bytes. Actual browser quota can be lower. The game still uses its original documented simplifications, including route reassignment that repositions a vessel while preserving cargo. Optional server and conflict-merge exercises in this course are proposals, not implemented features.

Return to the [course index](README.md), [testing guide](04-TESTING-AND-DEBUGGING.md), or [trace lab](07-TRACE-LAB.md) to connect these results to the code and its boundaries.
'''
(S / 'astraupskill/VERIFICATION.md').write_text(verification, encoding='utf-8')

required = {'README.md', '01-CODEBASE-MAP.md', '02-CONCEPTS.md', '03-WORKED-CHANGE.md', '04-TESTING-AND-DEBUGGING.md',
            '05-PRACTICE.md', '06-SOLUTIONS-AND-REVIEW.md', '07-TRACE-LAB.md', 'VERIFICATION.md'}
baseline = read(B / 'baselines/4de416cd300b.json')['files']
changed = []
for parent, directories, files in os.walk(S):
    relative = Path(parent).relative_to(S)
    directories[:] = [name for name in directories if name not in {'node_modules', '.git', '__pycache__'} and
                      not (relative == Path('.') and name in {'dist', 'artifacts', '.dependency-refresh'})]
    for filename in files:
        path = Path(parent) / filename
        rel = path.relative_to(S).as_posix()
        if rel.startswith('astraupskill/') and path.name in required:
            continue
        if baseline.get(rel) != sha(path):
            changed.append(rel)
spec = {'id': '4de416cd300b', 'project': 'astra2', 'changedFiles': sorted(changed), 'summary': summary,
        'checks': {'format': 'json', 'resultsFile': 'checks/tidebound/results.json', 'expectedTests': 76,
                   'environment': 'Node 22.16.0; npm 10.9.2 clean install; Vite 7.3.6; Vitest 4.1.11; real Chrome 152.0.7977.76; isolated browser contexts',
                   'command': '44 unit/domain tests; 19 production library workflows; 13 original gameplay workflows; normal clean install/build; byte-identical assets; npm audit; release and performance scripts'},
        'limits': limits}
(B / 'specs/4de416cd300b.json').write_text(json.dumps(spec, indent=2), encoding='utf-8')
print(json.dumps({'passedCases': 76, 'changedFilesBeforeRequiredGuides': len(changed), 'preservedTextFiles': 42, 'images': 2}), flush=True)
