from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/330bb6feda2f/astraupskill'
replacements={
'one person?s':'one person\'s',
'The patch checks both forms against the set':'The patch independently checks both fields against the set',
'anonymizes event IDs':'anonymizes event distinct IDs',
'The identifier set is a project-scoped authorization boundary as well as a privacy boundary.':'The identifier set controls mutation scope; authorization remains the route layer\'s responsibility.',
'The before/after comparison also changes no-found behavior: a missing person still receives an audit but no records are touched. That preserves an idempotent operational response while making the found-person path comprehensive.':'A missing person does not imply missing history. The service falls back to the requested identifier and still scrubs matching event/raw rows and removes matching aliases. Only a wholly unmatched request leaves every existing row unchanged and adds an audit.',
'A missing person causes no event, raw, person, or alias mutation but still appends the privacy.delete audit.':'With no person, exact matching event/raw history and aliases still change; unrelated rows remain. Every call appends a privacy.delete audit.',
'Trace other-user: every project record fails set membership.':'Trace an unmatched id: no existing row matches, so only the audit is appended.',
'Mutation lab removes alias expansion; the alias event stays identifiable and the test fails.':'Mutation lab removes alias expansion: the mapped-only event in the expanded fixture stays identifiable and its assertion fails. Removing expansion would not fail the original device-7 fixture because that value was already in person.identifiers.',
'two tests against actual lib/server/privacy.ts: full alias deletion and unknown-ID audit-only behavior.':'four tests against actual lib/server/privacy.ts, including mixed raw identifiers and cross-project preservation.',
'numeric executedTests 2':'numeric executedTests 4',
'distinguish the two executed tests':'distinguish the four executed tests',
'payload.distinct_id or payload.user_id, and explains why both are included.':'independent membership checks for payload.distinct_id and payload.user_id, and explains why short-circuit preference could miss a target.',
}
extra={
'README.md':'This is a repair to the existing identifier scrubber, not a complete erasure implementation. It retains other properties, derived records and requested identifiers in audit metadata. Use this limitation as a senior review exercise: inventory every copy of identity before defining a broader deletion contract.',
'01-CODEBASE-MAP.md':'Read the [delete route](../app/api/privacy/delete/route.ts): it requires a user and Admin project role before calling the service. Ingest prefers user_id when resolving a canonical person, which makes a raw payload with both identifier fields an important regression case. The accepted deletion predicate checks either field independently.',
'02-CONCEPTS.md':'The canonical value is explicitly included even when identifiers contains only an alias. Alias rows pointing to that canonical value contribute additional history identifiers. This is one project-local resolution step, not a general graph traversal. The existing audit intentionally retains the requested identifier, so anonymized event fields must not be described as total removal of identity.',
'03-WORKED-CHANGE.md':'A review fixture adds raw distinct_id=other-device with user_id=user-1. The previous fallback expression selected other-device and missed the target. Independent membership tests now match user-1 and scrub both raw identifier fields. Another fixture places mapped-only in an alias row but outside the person identifiers, so removing the expansion loop produces a meaningful failing assertion.',
'04-TESTING-AND-DEBUGGING.md':'The expanded suite has a real counterexample for each discovery branch: canonical-only identity, an alias absent from identifiers, and mixed raw fields. It asserts removal of contact fields as well as anonymized distinct ids. A foreign-project event and alias retain object identity, providing a stronger preservation check than an empty-array fixture.',
'05-PRACTICE.md':'Score two points each for identifier discovery, mixed-field matching, project isolation, no-person behavior and evidence limits. Add an event with no matching person and explain why it still changes. Then inspect userProperties and sessionsIndex and write a separate follow-up inventory; the current tests do not certify their erasure.',
'06-SOLUTIONS-AND-REVIEW.md':'For a missing person with device-7 history, only that exact history is scrubbed; user-1 remains because no person links the identifiers. For mixed raw fields, either target match is enough. Another project with device-7 remains intact. These answers require examining concrete predicates rather than assuming that a successful delete response means every associated field was erased.',
'07-TRACE-LAB.md':'''Record these additional rows:

| Case | Relevant match | Expected result |
|---|---|---|
| Alias request | Person identifiers | Canonical and mapped history included |
| Mixed raw fields | user_id matches | Raw payload scrubbed |
| Other project | Project mismatch | Row preserved |
| Orphan history | Requested id only | Exact history scrubbed |

Track audit creation separately: repeated unmatched requests still create audit rows, so the whole operation is not a literal no-op.''',
'VERIFICATION.md':'The accepted capture is crud-b04-astra-runtime. Four named cases pass with real privacy.ts and store/clock/id adapters. No legal compliance claim follows from these tests: event userProperties, other payload fields, sessions, derived tables and audit identity need separate review if the application later requires comprehensive erasure.'
}
for name,addition in extra.items():
 f=P/name;s=f.read_text(encoding='utf-8-sig')
 for old,new in replacements.items():s=s.replace(old,new)
 s=s.replace('The source links and evidence remain available for review.','')
 f.write_text(s.strip()+'\n\n'+addition+'\n',encoding='utf-8')
