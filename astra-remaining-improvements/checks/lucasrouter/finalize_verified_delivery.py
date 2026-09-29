from pathlib import Path
import hashlib
import json
import shutil

C = Path(__file__).resolve().parent
B = C.parent.parent
S = B / 'stage/52d78d4a92a2'
read = lambda p: json.loads(p.read_text(encoding='utf-8'))
tests = read(C / 'test-final-01-results.json')
test_run = read(C / 'test-final-01.json')
types = read(C / 'typecheck-final-01.json')
lint = read(C / 'lint-final-02.json')
build = read(C / 'build-scoped-01.json')
browser = read(C / 'browser-final-01/results.json')
assert tests['success'] and tests['numTotalTests'] == tests['numPassedTests'] == 166
assert tests['numFailedTests'] == tests['numPendingTests'] == 0
assert all(run['exitCode'] == 0 for run in [test_run, types, lint, build, browser])
assert browser['passedChecks'] == 56 and browser['failedChecks'] == 0 and browser['ownedServerStopped']
images = []
image_dir = S / 'astraupskill/images'
image_dir.mkdir(exist_ok=True)
for original, name, viewport in [('09-dispatch-desktop.png', 'dispatch-desktop.png', '1366x850, DPR 1'), ('07-driver-D2-mobile.png', 'driver-mobile.png', '375x812, DPR 2')]:
    source = S / 'e2e-screens' / original
    destination = image_dir / name
    shutil.copyfile(source, destination)
    images.append({'file': 'images/' + name, 'source': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'viewport': viewport, 'reviewed': True, 'review': 'Viewed desktop map/routes and mobile driver controls; layout and typography readable, expected scrolling, no missing style presentation.'})
evidence = {
    'passed': True, 'total': 222, 'passedTests': 222, 'failed': 0, 'notExecuted': 0,
    'counting': '166 unit/store tests plus 56 original browser smoke assertions; typecheck, lint and build are additional gates, not added to the case count.',
    'testRun': test_run, 'typecheckRun': types, 'lintRun': lint, 'buildRun': build, 'browserRun': browser,
    'rawTests': str(C / 'test-final-01-results.json'), 'images': images,
    'environment': 'Windows; Node 22.16.0; Next 16.3.1; React 19.2.8; TypeScript 5.9.3; Vitest 4.1.10; Tailwind 4.3.3; installed local browser selected by the original Puppeteer smoke script',
    'limits': ['This remains a browser-local demonstration with no authentication, tenant authorization or transactional server database.', 'Photo validation checks data URL structure and existing storage budget; it does not decode image pixels or validate MIME contents.', 'The final successful build uses the default Turbopack command after scoping Tailwind to src. Earlier unscoped Turbopack and Webpack attempts failed and remain recorded.', 'The final checks used the installed staged dependency tree. Root independently captured tests, typecheck, lint, production build and browser smoke, but did not recapture a clean pnpm installation.']
}
(C / 'results.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
(C / 'images-reviewed.json').write_text(json.dumps(images, indent=2), encoding='utf-8')
(S / 'astraupskill/evidence.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
spec = read(B / 'specs/52d78d4a92a2.json')
for file in ['README.md', 'astraupskill/evidence.json', 'astraupskill/images/dispatch-desktop.png', 'astraupskill/images/driver-mobile.png']:
    if file not in spec['changedFiles']: spec['changedFiles'].append(file)
spec['checks'].update(expectedTests=222, environment=evidence['environment'], command='Installed Vitest full suite --maxWorkers=1 --testTimeout=30000; tsc --noEmit; eslint . --max-warnings=0; default next build; original smoke-e2e.mjs against an owned local production server')
spec['summary'] = [
    'Delivery actions sanitize runtime proof inputs, bound names and notes, validate structured image data URLs and retain the existing photo-storage budget.',
    'Unknown failure reasons reject before mutation; valid failures store the same bounded note in the stop proof and activity event, preserving state/report consistency.',
    'Tailwind scans application source explicitly, fixing the observed Windows dependency-path build error and avoiding unrelated snapshot/artifact class candidates; the default production build now passes.',
    'Nine learning guides include real store/action traces, before-and-after code, executable exercise solutions, an exact original store snapshot and two reviewed production-browser screenshots.'
]
spec['limits'] = evidence['limits']
(B / 'specs/52d78d4a92a2.json').write_text(json.dumps(spec, indent=2), encoding='utf-8')
readme = S / 'README.md'
text = readme.read_text(encoding='utf-8')
if '## CRUD learning course' not in text:
    text += '\n## CRUD learning course\n\nStart with [astraupskill/README.md](astraupskill/README.md) for source-level walkthroughs, runtime validation examples, exercises and worked solutions. The [current verification record](astraupskill/VERIFICATION.md) covers 166 unit/store tests, 56 browser checks, type checking, lint and the default production build.\n'
readme.write_text(text, encoding='utf-8')
course = S / 'astraupskill/README.md'
text = course.read_text(encoding='utf-8')
text += '\n## Verified application views\n\nThese screenshots come from the successful production smoke run, using isolated demo browser data. Follow the stop from the dispatch map to the driver action and then the proof/activity event discussed in the trace lab.\n\n![Desktop dispatch with routes and stop status](images/dispatch-desktop.png)\n\n![Mobile driver next-stop controls](images/driver-mobile.png)\n'
course.write_text(text, encoding='utf-8')
(S / 'astraupskill/VERIFICATION.md').write_text('''# Verification and limits

The final delivery passed **166 unit/store tests and 56 browser smoke checks**, plus TypeScript checking, zero-warning lint and the normal production build. These are observed results from the staged application, not expected counts copied from a plan. [Machine-readable evidence](evidence.json) records commands, exits, durations, image hashes and central raw-report locations.

## Reproduce the verified workflow

The package declares pnpm 9.12.3. From the project root, use its lockfile, then run:

```powershell
pnpm install --frozen-lockfile
pnpm test --maxWorkers=1 --testTimeout=30000
pnpm typecheck
pnpm lint
pnpm build
pnpm start --hostname 127.0.0.1 --port 3000
```

In a second terminal, `pnpm smoke http://127.0.0.1:3000` runs the existing browser script. It discovers a locally installed Chrome or Edge and uses a fresh automated browser profile. It requires access to public OpenStreetMap tiles. Stop your local server afterward.

The captured checks invoked the installed CLIs directly. Vitest passed 166/166 tests, with zero failures or pending cases, in 35.31 seconds. Type checking exited zero in 75 seconds; lint exited zero in 74.95 seconds. The final default Next build exited zero in 120.6 seconds, including successful compilation in 14.6 seconds. Browser smoke passed all 56 checks in 66.03 seconds and its owned server stopped. These timings describe this machine and run; they are not general performance guarantees. The final verification used the installed staged dependencies; it does not claim a separately captured clean pnpm install.

## What was exercised

The helper/store tests include malformed optional proof fields, bounded text, rejected unknown failure reasons, no mutation on rejection, retained photo-budget behavior and matching stop-proof/activity-event data. Existing route, storage, report and application tests remain enabled.

The original production-browser smoke covers dispatch markers, optimization, reassignment, delivery confirmation, failure notes, skip ordering, activity history, reload persistence, double-tap protection, cross-tab behavior, route completion, resets, API error responses, real 404 responses and network/console checks. The run reported no console errors and only the app origin plus OpenStreetMap tile requests. Desktop dispatch and mobile driver screenshots were visually reviewed and included in the course. This is a smoke suite, not a complete accessibility or cross-browser audit.

## Build correction and earlier failures

An earlier Turbopack run failed while interpreting an extended Windows dependency path in the PostCSS transform. A Webpack attempt compiled, then exposed a new validator TypeScript narrowing error. That error was corrected. Tailwind source discovery is now explicitly scoped to `src` by `source("../")` in `src/app/globals.css`, so learning snapshots and dependency artifacts do not supply application utility classes. The [official Tailwind source documentation](https://tailwindcss.com/docs/detecting-classes-in-source-files#setting-your-base-path) explains this option. The successful final run uses the normal `pnpm build`; the extra `build:webpack` command remains available as a documented bundler option, but is not the final successful build evidence.

## Boundaries for the learner

The exact original [store snapshot](snapshots/useAppStore.ts.txt) supports before-and-after comparison. The app remains a browser-local demo: no accounts, server authorization, tenant isolation or transactional backend were added. Browser persistence retains its existing cross-tab and quota limitations. Optional malformed fields are dropped; invalid domain choices are rejected. Image checks validate data URL structure and size policy, not decoded pixels, MIME truth or media safety. A production CRUD service must enforce those boundaries independently on an authenticated server.
''', encoding='utf-8')
print(json.dumps({'verifiedChecks': 222, 'unitStoreTests': 166, 'browserChecks': 56, 'imagesReviewed': 2}))
