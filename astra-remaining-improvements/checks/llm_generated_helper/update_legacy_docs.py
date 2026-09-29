from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[2];S=B/'stage/44013f102ff1'
baseline=json.loads((B/'baselines/44013f102ff1.json').read_text(encoding='utf-8'))['files']
for name in ['README.md','ARCHITECTURE.md','TESTING.md','ONBOARDING.md','CODE_REVIEW.md','ALTERNATIVE_APP_SPEC.md']:
    p=S/'docs'/name;rel='docs/'+name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==baseline[rel],rel
    target=S/'docs/original/docs'/(name+'.txt');assert not target.exists();target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())

content={
'README.md':'''# Documentation

The current learning entry point is [Practice Journal's nine-part course](../astraupskill/README.md). It covers the implemented local CRUD web application and the repaired settings/IPC boundaries of the separate Electron assistant.

| Read this | For |
| --- | --- |
| [Root README](../README.md) | Dependency-free journal setup and optional desktop launch |
| [Codebase map](../astraupskill/01-CODEBASE-MAP.md) | Source responsibilities and one complete write |
| [Concepts](../astraupskill/02-CONCEPTS.md) | Typed PATCH, references, snapshots, revisions and secrets |
| [Worked change](../astraupskill/03-WORKED-CHANGE.md) | Eight settings regressions and the acceptance boundary |
| [Testing](../astraupskill/04-TESTING-AND-DEBUGGING.md) | Reproducible checks and useful failure injection |
| [Exercises](../astraupskill/05-PRACTICE.md) | Junior-to-mid-level practice with acceptance criteria |
| [Solutions](../astraupskill/06-SOLUTIONS-AND-REVIEW.md) | Review reasoning and future feature designs |
| [Trace lab](../astraupskill/07-TRACE-LAB.md) | Follow actual state across process boundaries |
| [Verification](../astraupskill/VERIFICATION.md) | Results, evidence limits and recovery |

Original documentation is retained in `original/docs/*.txt`. The older alternative-app specification remains a historical proposal; its larger CueDeck feature list is not the implemented scope.
''',
'ARCHITECTURE.md':'''# Current architecture

Practice Journal is a single-owner loopback web app. `src/practice/setup.js` initializes its private JSON file once. `server.js` validates and authenticates HTTP requests, `domain.js` defines the four resource contracts, and `src/shared/json-file.js` commits validated drafts under an exclusive lease and accepted-byte revision. `src/practice/ui/app.js` renders typed forms, retains drafts and requires explicit review after stale or uncertain writes.

Profiles provide a learning context; questions are profile-specific or shared; sessions move from planned to in-progress to completed; attempts preserve question wording and contain a written answer, feedback and optional score. Archive rules control future creation and reference checks protect deletion. Activity records action and field names, retaining the latest 1,000 entries. Export includes records without authentication internals.

The separate Electron workflow still starts at `src/main/main.js`. Its `store.js` is now an adapter around `settings-store.js`. The preload exposes `getSettings`, `saveSettings`, `ask`, `cancelAsk`, `onTranscript` and `onAnswerChunk`. Public settings contain a revision, resume, job description, window preference and credential-presence booleans. Save receives `{revision, changes}`; blank credential inputs preserve existing values while explicit clear controls remove them. Event subscriptions return cleanup functions.

`ipc-controller.js` requires the live window's exact main frame and local page URL. It validates payloads and cancels active provider work when the requester disappears or explicitly cancels. Provider modules remain separate from the journal, which performs no audio capture or external AI request.

See the [full source map](../astraupskill/01-CODEBASE-MAP.md), [request trace](../astraupskill/07-TRACE-LAB.md), and [limits](../astraupskill/VERIFICATION.md). The original architecture document is preserved in `original/docs/ARCHITECTURE.md.txt` for comparison.
''',
'TESTING.md':'''# Current verification entry points

Run `npm test` for the 120-case Node suite and `npm run syntax` to parse current JavaScript. Neither command needs Electron or an npm install. The launcher explicitly selects `test/*.test.js`, excluding preserved original snapshots. Fixtures use isolated temporary files, synthetic encryption and mocked provider requests.

For optional Chromium checks, follow [the testing chapter](../astraupskill/04-TESTING-AND-DEBUGGING.md). `verification/verify_browser.py` exercises the actual journal UI and HTTP service with disposable data. `verification/verify_renderer.py` exercises the desktop HTML with a synthetic preload bridge. Their evidence must remain distinguished: the latter does not launch native Electron or capture audio. `verification/verify_setup.py` copies a finite source set to a new evidence directory, repeats tests, checks explicit owner initialization/refusal, and starts the actual server CLI.

The [verification record](../astraupskill/VERIFICATION.md) and its JSON evidence contain final results and limitations. Tests include typed values, reference protection, lifecycle rules, corrupt files, failed replacement, stale revisions, held leases, IPC trust, body limits and lost browser responses. Baseline settings regressions failed first and passed after the implementation repair.

No check used real user settings, live credentials, provider requests or audio. Native Windows encryption, capture and installer behavior remain unverified. Repeated test runs are not counted as additional distinct cases. Keep failure artifacts and use a new evidence directory on a rerun.
''',
'ONBOARDING.md':'''# Start here

Use Node.js 22 or later. Read [the root setup](../README.md), run `npm test`, then initialize and start Practice Journal. You do not need Electron or API credentials for the journal. Create a profile, question, session and scored attempt before changing code; those interactions reveal why references and state transitions matter.

Follow [the course](../astraupskill/README.md) in its five stages. The first implementation trace is a profile write. The worked repair compares the original settings store with the new commit/publish ordering. Exercises then cover an optional field, related records, concurrent edits, recovery and a database migration proposal. Each exercise includes a failure case and a review artifact.

The current app has a new HTTP workflow and the preserved desktop workflow. Choose the relevant entry point deliberately: `npm run practice` opens the journal server; `npm start` invokes Electron after its dependencies are installed. The two workflows use different state files and credential models. Do not point training tests at real desktop user data or valuable journal records.

Before describing a feature as verified, read [the evidence boundaries](../astraupskill/VERIFICATION.md). The browser journal has real HTTP coverage; desktop renderer tests use a mocked bridge. Preserve historical material under `docs/original` and treat the older CueDeck specification as a separate proposal, not an automatic backlog that has already been completed.
''',
'CODE_REVIEW.md':'''# Implemented improvements and remaining review work

The new local Practice Journal provides CRUD for profiles, questions, sessions and attempts, with strict typed mutations, snapshots, lifecycle transitions, archive/reference rules, search/pagination, activity and authenticated export. The browser retains drafts and compares accepted state after stale revisions or uncertain responses.

The existing settings store now preserves unreadable/corrupt/undecryptable files, rejects plaintext encryption fallback, returns detached values and publishes memory only after accepted persistence. Privileged desktop messages validate the exact trusted main frame. Settings reads expose credential presence rather than secrets; saves require revisions and explicit changes. Active transcription/generation can be cancelled, and retry boundaries recheck cancellation. Startup settings errors are visible.

The [worked-change chapter](../astraupskill/03-WORKED-CHANGE.md) connects these changes to failing-then-passing regressions. The [verification record](../astraupskill/VERIFICATION.md) provides final evidence and limits.

Remaining work includes a designed import/token-recovery workflow, durable creation receipts, database migration, team authorization and full native Electron/provider verification. The JSON store is bounded local persistence, with a global revision and explicit stale-lock investigation. Duplicate JSON property rejection, exhaustive persisted-history validation and a full streaming-provider resource-limit review are not claimed. Existing Electron dependencies were retained; installer and actual OS encryption were not exercised.

Original review findings remain in `original/docs/CODE_REVIEW.md.txt`. They describe the earlier codebase and may now be resolved or superseded. Use this page and the current course as the implemented-state guide.
'''
}
for name,text in content.items():(S/'docs'/name).write_text(text,encoding='utf-8')
p=S/'docs/ALTERNATIVE_APP_SPEC.md';original=p.read_text(encoding='utf-8');p.write_text('''> Historical proposal, retained for reference. The current implemented scope is Practice Journal plus the desktop settings/IPC repairs documented in [the current course](../astraupskill/README.md). The autonomous-build contract and feature claims below describe a separate earlier proposal and are not a completion claim for this version. Original bytes are preserved in `original/docs/ALTERNATIVE_APP_SPEC.md.txt`.

'''+original,encoding='utf-8')
print('Preserved six original documentation files; updated five entry points and labeled the historical proposal.')
