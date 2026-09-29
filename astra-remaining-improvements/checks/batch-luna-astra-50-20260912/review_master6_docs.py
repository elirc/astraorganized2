from pathlib import Path
B=Path(__file__).resolve().parents[2];P=B/'stage/3e4e08e349a1';U=P/'astraupskill'
for p in U.glob('*.md'):
 t=p.read_text(encoding='utf-8-sig').replace('stage root','project root').replace('at this stage','in this project').replace('the seven actual cases','the thirteen learner route cases')
 t=t.replace('eight reading checkpoints and one verification page','seven core reading chapters, this overview and one verification page')
 t=t.replace('A handler must not use a caller-provided organization after that check.','A handler uses the caller-selected organization only after that membership check passes.')
 t=t.replace('Progress timestamps express a monotonic learner story.','Progress timestamps distinguish the initial start from the current completion state.')
 t=t.replace('A completion write sets `completedAt` once and preserves it on later updates.','A repeated COMPLETED write preserves an existing completedAt; changing the status back to IN_PROGRESS clears it.')
 p.write_text(t,encoding='utf-8')
p=U/'01-CODEBASE-MAP.md';t=p.read_text(encoding='utf-8');t+='\nAll route paths in this chapter are relative to learnerRouter. The actual app mounts it at /learner in apps/api/src/app.ts, so the HTTP enrollment path is POST /learner/courses/:courseId/enroll. Production requireAuth verifies a bearer JWT and loads current memberships from Prisma; the route test replaces that middleware. The organization header selects a tenant within those memberships and is not itself authentication.\n';p.write_text(t,encoding='utf-8')
p=U/'02-CONCEPTS.md';t=p.read_text(encoding='utf-8');t+='\nExplicit requiredLessonIds and requiredAssignmentIds are enforced whenever supplied, even if the broad boolean is false. In legacy domain calls with no explicit IDs, requireAllLessons requires nonempty progress with every row completed; the API supplies the enrolled version’s IDs when deriving all lessons, so a missing row cannot disappear from that comparison. An explicitly empty list overrides the broad flag. Completion and certificate eligibility are separate: a rule can permit completion without all lesson rows complete, while the existing certificate helper still requires 100 percent of materialized progress. A course with no lesson progress has zero percent and can complete under empty requirements without receiving a certificate.\n';p.write_text(t,encoding='utf-8')
(U/'04-TESTING-AND-DEBUGGING.md').write_text('''# Testing the real learner boundary

The API suite runs fourteen cases: thirteen in [learner.routes.test.ts](../apps/api/src/routes/learner.routes.test.ts) and one existing app-construction case. The domain suite runs fifteen separate cases. The focused thirteen-case command is a subset of the fourteen-case API run; do not add it again when reporting the total of twenty-nine distinct tests. Web and worker test commands explicitly permit zero test files and contribute zero tests.

The learner fixture imports the actual Express router. Vitest hoists mocks for Prisma, authentication, events and audit before that import. A small dispatch helper provides method, url, originalUrl, headers, body, query and params, then calls router.handle. Its response recorder resolves a promise on json; the next callback captures errors. This executes actual handler guards and branches without opening a network port or running production JWT parsing. The complete fixture is reproduced in [the solutions](06-SOLUTIONS-AND-REVIEW.md).

The positive completion case supplies a completed lesson, passed quiz and graded assignment, then checks its certificate and side-effect counts. The terminal guard case begins with an already-completed enrollment and proves that no new transaction or event is requested. It does not first execute completion and then reload from a database. Separate absent quiz, absent assignment and absent progress cases stop before a transaction. Other cases cover foreign actor/organization or content version, malformed stored score configuration, timestamp preservation, explicitly empty assessments, published pointer selection and duplicate enrollment conflict.

The transaction argument is a Proxy distinct from the default Prisma object, forwarding the same delegate methods. Assertions verify that completion passes this callback client to audit and event helpers. Those helpers are spies in the router suite: the test does not execute actual DomainEvent/OutboxMessage insertion or prove SQL rollback. The production helper source does use its optional client for those writes; a later database integration test must establish the relational behavior. Scope-aware findUnique checks ID, actor and organization, while the findFirst fixture checks actor and organization and is not a complete database query engine.

Debug a failing request by identifying its first boundary. A403 means tenant membership failed. A404 may mean a missing enrollment or a version mismatch. A409 completion result means the required work did not qualify. A500 for the deliberately malformed stored score is an internal configuration failure. For a successful mutation, check the transaction and side-effect arguments as well as the response. A no-op or terminal request legitimately has zero transactions; zero is not automatically a failure.

Run from the project root after the installation and generation steps in [verification](VERIFICATION.md):

```powershell
npm run test --workspace @lms/api
npm run test --workspace @lms/domain
```

The domain tests load source directly. API Vitest configuration and TypeScript paths also resolve the domain source, while production runtime imports need its compiled package. The ordered build emits domain output before application packages. Neither a successful compile nor mocked request establishes PostgreSQL availability, Redis delivery, browser interaction or certificate PDF generation. Keep those operational claims separate from this suite's concrete control-flow evidence.
''',encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8');t+='''
## Replay and remaining behavior

The terminal test starts from an already-completed fixture. It proves the guard returns its existing certificate and skips new work. The first completion response contains the updated scalar enrollment row, while a later response includes the relations loaded by findUnique. Stable status and certificate identity do not imply byte-identical response bodies. Concurrent first completions can both pass the pre-read guard; database uniqueness may reject one, and no retry/error policy for that race is added here.

Certificate.enrollmentId and verificationCode already have unique constraints. The existing code derives verificationCode from the last eight enrollment-ID characters, so a collision can fail the transaction; uniqueness prevents duplicate codes but does not implement a collision retry. artifactUrl names a PDF without generating it in this command. Existing progress/submission endpoints can still change work after enrollment completion, and completion is not restricted to ACTIVE status. These remain separate lifecycle work. Quiz count-plus-one is not a proven concurrent retake limit. Production JWT verification exists, but the default development secret and generic error middleware are unchanged; this suite does not validate production identity or error disclosure.

## Complete executed learner fixture

This is the complete current thirteen-case file. Modify the existing file rather than adding a duplicate beside it. The one app-construction test and fifteen domain cases are separate. The actual event/audit helpers are intentionally mocked here; transaction-client argument assertions show the route passes the right object, not that a database committed or rolled back those records.

```ts
'''+(P/'apps/api/src/routes/learner.routes.test.ts').read_text(encoding='utf-8')+'```\n';p.write_text(t,encoding='utf-8')
p=U/'07-TRACE-LAB.md';t=p.read_text(encoding='utf-8');t+='\nThese are router-relative paths. Prefix /learner when sending a real HTTP request through createApp. The trace is a worked sequence, while the recorded fixture tests the individual request boundaries using controlled records; it does not run a database-backed learner journey or execute a real quiz-to-submission-to-certificate flow. A COMPLETED terminal fixture proves guard behavior, with stable stored certificate identity rather than identical relation-rich response shape.\n';p.write_text(t,encoding='utf-8')
print('Master6 course reviewed; complete fixture and precise evidence boundaries added')
