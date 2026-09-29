from pathlib import Path
import json

C = Path(__file__).resolve().parent
B = C.parent.parent
S = B / 'stage/676bcb38df2b'
read = lambda p: json.loads(p.read_text(encoding='utf-8'))
tests = read(C / 'test-final-04-results.json')
run = read(C / 'test-final-04.json')
types = read(C / 'typecheck-final-03.json')
assert tests['success'] and tests['numTotalTests'] == tests['numPassedTests'] == 92
assert tests['numFailedTests'] == tests['numPendingTests'] == 0
assert run['exitCode'] == types['exitCode'] == 0
assert (C / 'npm-ci-01-exit.txt').read_text(encoding='utf-8-sig').strip() == '0'
evidence = {
    'passed': True, 'total': 92, 'passedTests': 92, 'failed': 0, 'notExecuted': 0,
    'testRun': run, 'typecheckRun': types,
    'install': {'command': 'npm ci --no-audit --no-fund --cache=<private project cache> --loglevel=verbose', 'exitCode': 0, 'packages': 544, 'log': str(C / 'npm-ci-01.log'), 'normalInstallScripts': True},
    'rawTests': str(C / 'test-final-04-results.json'),
    'environment': 'Windows; Node 22.16.0; npm 10.9.2; Expo 57.0.7; React Native 0.86.0; TypeScript 6.0.3; Vitest 4.1.10',
    'limits': ['Repository tests use a mocked database seam; no native SQLite/device/emulator run was performed.', 'No UI or release build verification is claimed.', 'Final suite uses one worker and a 30-second test bound. An earlier parallel run exceeded the default five-second bound in the existing deterministic plate-math property test; all assertions remain enabled.']
}
(C / 'results.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
(S / 'astraupskill/evidence.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')
spec = read(B / 'specs/676bcb38df2b.json')
for name in ['README.md', 'astraupskill/evidence.json']:
    if name not in spec['changedFiles']: spec['changedFiles'].append(name)
spec['checks'].update(expectedTests=92, environment=evidence['environment'], command='Locked npm ci; node node_modules/vitest/vitest.mjs run --maxWorkers=1 --testTimeout=30000 --reporter=json; node node_modules/typescript/bin/tsc --noEmit')
spec['summary'] = [
    'Set updates validate numeric values, preserve undefined versus null patch semantics, return affected-row results and notify subscribers only after actual mutations.',
    'Workout completion now guards service orchestration as well as persistence, preventing repeated or missing completions from advancing and saving program progression again.',
    'Program creation binds and returns the same timestamp; regression tests cover stale mutations, notifications, validation and real progression orchestration through database seams.',
    'Nine learning guides explain the actual repository/service flow with worked code, exercises, executable solution examples and exact original source snapshots.'
]
spec['limits'] += [limit for limit in evidence['limits'] if limit not in spec['limits']]
(B / 'specs/676bcb38df2b.json').write_text(json.dumps(spec, indent=2), encoding='utf-8')
readme = S / 'README.md'
text = readme.read_text(encoding='utf-8')
text = text.replace('**Vitest** — 70 unit tests over the pure core (no RN imports in `core/`, `engine/`, `content/`)', '**Vitest** — 92 tests across core calculations, repository seams and workout orchestration; see the [verification record](astraupskill/VERIFICATION.md) for the captured command and limits')
if '## CRUD learning course' not in text:
    text += '\n## CRUD learning course\n\nStart with [astraupskill/README.md](astraupskill/README.md) for nine source-grounded guides, before-and-after examples, progressive exercises and worked test solutions. Exact original repository and service snapshots support comparison.\n'
readme.write_text(text, encoding='utf-8')
worked = S / 'astraupskill/03-WORKED-CHANGE.md'
text = worked.read_text(encoding='utf-8')
text += '\n`completedAt` is a numeric timestamp. It is exempt from the set-number validation policy; it is not a nonnumeric field. The other exemptions preserve the existing text, enum and boolean contracts.\n'
worked.write_text(text, encoding='utf-8')
(S / 'astraupskill/VERIFICATION.md').write_text('''# Verification and limits

The final staged source passed **92 tests** and TypeScript checking on Windows with Node 22.16.0, npm 10.9.2, Expo 57.0.7, React Native 0.86.0, TypeScript 6.0.3 and Vitest 4.1.10. A normal locked `npm ci` completed with exit zero and installed 544 packages. Install scripts were enabled. A private package cache was used; no global cache cleanup or dependency migration was needed.

## Reproduce the checks

From this project's root, install the lockfile and run:

```powershell
npm ci --no-audit --no-fund
npm test -- --maxWorkers=1 --testTimeout=30000
npm run typecheck
```

The recorded test command directly invoked the installed Vitest CLI with those worker/time bounds and a JSON reporter. It passed all 92 cases with zero failures and zero pending cases in 35.46 seconds. The type check directly invoked the installed TypeScript CLI with `--noEmit`, exited zero and took 88.64 seconds. These are elapsed times on this machine, not performance guarantees. [Machine-readable evidence](evidence.json) records exact commands, exits and central raw-report locations.

The 30-second test limit is deliberate. An earlier parallel run passed 91 cases but the existing seeded plate-math property test ran for 6.66 seconds, beyond the default five-second limit. The final run uses one worker and retains all three gyms, 200 targets per gym and three rounding modes. It does not skip assertions or substitute an expected pass count. Earlier test-mock type errors were corrected before the successful type check.

## What the evidence establishes

The tests exercise numeric validation, mixed undefined patches, explicit null clearing, stale update/delete results, change-notification counts, one timestamp used for persistence and return values, and program progression saved only once across repeated completion. Existing core tests remain enabled. Repository tests use the project's database seam and mocked responses. The completion regression calls the actual progression code with an existing program while controlling persistence collaborators.

This is **not a native SQLite or device verification**. A mocked `runSync` response establishes the JavaScript contract; it cannot prove SQLite foreign-key cascades, filesystem durability or native module behavior. No Android/iOS release build, emulator run, UI interaction or browser run is claimed. Before release, use a disposable native database to test cascades, restart persistence and user-visible error recovery, then exercise the workout screen on a device.

## Preservation and remaining boundaries

The exact original [repository](snapshots/repos-before.ts.txt) and [workout service](snapshots/workoutFlow-before.ts.txt) are preserved as noncompiling text snapshots. Compare them with the live source and the worked-change guide. The application remains local-only: no account system, server authorization, remote synchronization, off-device backup or concurrent-device conflict handling was added. Finishing a workout prevents an ordinary repeat from advancing progression again, but completion and subsequent program-state writes are not a new multi-write transaction. Native failure recovery across those writes remains a separate engineering exercise.
''', encoding='utf-8')
print(json.dumps({'verifiedTests': 92, 'typecheckPassed': True, 'sourceUnchanged': True}))
