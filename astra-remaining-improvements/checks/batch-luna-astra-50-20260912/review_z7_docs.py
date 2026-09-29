from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parents[2]; ID='3ecd02656197'; P=B/'stage'/ID; U=P/'astraupskill'
for p in U.glob('*.md'):
 t=p.read_text(encoding='utf-8-sig')
 t=t.replace('cross-year activity/interview ordering','January/December activity/interview ordering and a separate year-boundary case')
 t=t.replace('raw timestamp ordering across year boundaries','raw timestamp ordering across month and year boundaries')
 t=t.replace('four tests','seven tests').replace('four focused regression scenarios','seven focused regression scenarios')
 t=t.replace('The examples below are complete method bodies when marked `[Fact]`; short code fences are labeled excerpts.', 'The examples below use Vitest. Complete `it(...)` cases run inside the existing test file; partial source expressions are labeled excerpts.')
 t=t.replace('{real-guid}', '{applicationId}')
 t=t.replace('The original source snapshots are under `astraupskill/snapshots/`. They are byte-exact copies of the canonical baseline for every changed original file.', 'The original source snapshots are under `astraupskill/snapshots/`. They preserve the six changed feature and formatter files byte-for-byte; package setup and the README are recorded in the delivery manifest.')
 t=t.replace('The final spec and evidence records live under the batch checks directory, maintained by the orchestrator.', 'Portable command records and output are under `astraupskill/evidence`; each record distinguishes the command result from the behavior it actually exercised.')
 t=t.replace('Expected limitations: .NET or database claims do not apply; this is a TypeScript Next app.', 'This TypeScript Next app has a deliberately bounded read-side scope.')
 t=t.replace('The deterministic tie policy is also a debugging aid. Two records with equal epoch milliseconds should always appear in ID order, even when the runtime locale changes.', 'The deterministic tie policy is also a debugging aid. Two records with equal epoch milliseconds appear in ID order within the configured runtime. The current ASCII identifiers are predictable; locale-aware comparison of future non-ASCII IDs would need an explicit locale or code-point comparator for cross-runtime guarantees.')
 p.write_text(t,encoding='utf-8')
p=U/'README.md';t=p.read_text(encoding='utf-8');t+='''
## Open the source while reading

Follow the [codebase map](01-CODEBASE-MAP.md), [concepts](02-CONCEPTS.md), [worked change](03-WORKED-CHANGE.md), [debugging guide](04-TESTING-AND-DEBUGGING.md), [practice](05-PRACTICE.md), [solutions](06-SOLUTIONS-AND-REVIEW.md), [trace lab](07-TRACE-LAB.md), and [verification](VERIFICATION.md). Compare the [actual regression suite](../src/features/shared/server/page-data.test.ts) with the [original decisions projection](snapshots/get-decisions-page-data-before.ts.txt). The tests added during review include every role, timezone offsets, equal timestamps, invalid instants, and historical-only stages.
''';p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8');t+='''
## Complete offset, tie, and year-boundary regression

Append this complete case inside the existing `describe` block in `src/features/shared/server/page-data.test.ts`. It uses that file's `snapshotClone`, `recruiter`, `expect`, and builder imports. It is already present in the delivered test file, so read or modify it there rather than adding a duplicate. Both builders execute their formatter as well as their comparator. That matters because a comparator can handle `NaN` correctly while a later formatter still throws. The expected ID lists deliberately encode the different ascending and descending tie policies.

```ts
'''+(P/'src/features/shared/server/page-data.test.ts').read_text(encoding='utf-8').split('  it("orders offsets,')[1].split('\n  it("excludes historical-only')[0]
# Restore the opening split token, retaining the complete case from source.
t=t.replace('```ts\n year boundaries,','```ts\n  it("orders offsets, year boundaries,') if '```ts\n year boundaries,' in t else t
# The source starts with a space after the comma; reconstruct directly if necessary.
start=t.rfind('```ts\n'); source=(P/'src/features/shared/server/page-data.test.ts').read_text(encoding='utf-8');case=source[source.index('  it("orders offsets,'):source.index('  it("excludes historical-only')]
t=t[:start]+'```ts\n'+case+'```\n\nThe role-matrix and empty-job cases in the same file extend exercises 1, 4, 5 and 9. Exercise 7 remains a proposed write design: no persistence command was introduced. Exercise 8 should identify the GET response as current-user metadata and aggregate counts, not a complete dataset or mutation endpoint.\n'
p.write_text(t,encoding='utf-8')
baseline=json.loads((B/'baselines'/f'{ID}.json').read_text())['files'];spec=json.loads((B/'specs'/f'{ID}.json').read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changed=[n for n,h in baseline.items() if not(P/n).is_file() or sha(P/n)!=h]
print(json.dumps({'baselineChanges':changed,'unlisted':[n for n in changed if n not in spec['changedFiles']]}))
files={n:sha(P/n) for n in spec['changedFiles'] if not n.startswith('astraupskill/') and n!='README.md'}
(B/'checks'/ID/'root-review-source-hashes.json').write_text(json.dumps({'files':files},indent=2),encoding='utf-8')
