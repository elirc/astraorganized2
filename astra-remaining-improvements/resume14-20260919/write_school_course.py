from course_writer import write_course
chapters={
'README.md':('School actions with session authority and atomic records',"""
This education demo manages sections, enrollments, coursework, attendance, support notes and heuristic agent reports. Its existing pure rules and permission matrix were useful, but many server actions trusted an actor ID supplied by the caller and wrote related records in separate operations. The completed change connects those rules to the actual mutation boundary.

Main actions now derive the active session, check a named capability and, where required, authorize the exact section or student. A teacher may grade work in the section they teach; merely seeing a student in another shared class does not authorize grading another teacher's assignment. Advisors create support records only for students within their permitted scope. Viewer accounts cannot invoke school or operations mutations by supplying an administrator ID.

schoolMutation coordinates one SQLite transaction for domain writes, required audits and queued jobs. Enrollment, drop, promotion, assignment publication and attendance use that shared boundary. Cache invalidation is collected during the transaction and runs only after commit. A failed final audit therefore leaves no partial enrollment, submission, attendance or queued success work.

Heuristic agent runs authorize their target before creating a Pending row or loading a full snapshot. Success output and audit commit together. Optional logger or notification failures cannot overwrite a successfully persisted run with Failed. Teacher and advisor snapshots respect private support-note visibility.

Identity remains a local simulation, enabled only by EDU_DEMO_MODE=true outside production. The cookie switcher and explicit local admin fallback are not real authentication. Tests use a fresh temporary SQLite database, actual actions and repositories, mocked Next request helpers and SQL failure triggers. No original database, external model or mail service is used.
""", [('src/packages/shared/school-mutation.ts',None,70)]),
'01-CODEBASE-MAP.md':('Find the session, capability, resource and transaction',"""
Start at src/app/actions.ts. Every exported school mutation either calls schoolMutation with an existing permission name or explicitly calls requireAction before operating the job queue. Notification read markers retain their existing owner-scoped updateMany predicates. The switcher delegates to setActiveUserCookie, which checks that local demo mode is enabled and the selected user exists.

shared/action-permissions.ts separates role capability from resource scope. requireAction obtains the current session and uses canPerformAction. requireSectionWrite checks a teacher relation against the exact section, while requireStudentWrite applies the existing advisor scope or a teacher's current enrolled roster. Neither helper accepts the caller's claimed actor as authority.

shared/school-mutation.ts opens the transaction and supplies transaction-bound audit and enqueue functions. audit.ts requires the audit row to persist; optional logging is isolated and is skipped inside a transaction because its separate SQLite connection could contend with the current writer. enqueueJob similarly accepts a transaction client.

shared/enrollment-workflows.ts contains the internal promotion and backfill operations shared by enrollment and drop paths. Public promotion still enters through an authorized action. The agent orchestrator performs its own authorization as well, so direct internal invocation cannot bypass target checks.

Several list pages contain inline creation actions. They now use the same transaction context and capability map, and callers no longer send page-render-time actor IDs. This keeps a changed active session authoritative when a form is eventually submitted.
""", [('src/packages/shared/action-permissions.ts',None,85)]),
'02-CONCEPTS.md':('Permission is not scope, and audit is part of the write',"""
A role capability answers whether a teacher may grade. Resource scope answers which assignment that teacher may grade. A student can belong to two teachers' sections, so broad student visibility is insufficient for grading. The action loads the assignment's section and checks the current teacher relation before updating the submission or attributing the grade.

Atomicity concerns the whole promised operation. Enrolling a student can create an enrollment, backfill published work, queue grade recalculation and append an audit. If only the first write commits, a later error leaves the application disagreeing with its own response. Passing the same Prisma transaction client to each write makes rollback cover that full set.

Conditional writes answer a separate concurrency question. A drop matches the previously read active enrollment status; publication matches the previous assignment status; promotion matches Waitlisted. A count-zero result is a stale command. Repeating a completed drop returns without freeing another seat, promoting another student or queuing more work.

SQLite serializes writers, and the application keeps capacity reads and enrollment writes within the transaction. The regression suite races two actual actions for the last seat and verifies that only one consumes it. A competing operation may receive a transaction conflict; the change does not promise transparent retries for every SQLite contention case.

The local session cookie is still intentionally switchable when demo mode is explicitly enabled. Server-derived identity prevents payload spoofing within that simulation, but it does not transform an unsigned demo cookie into production authentication.
""", [('src/app/actions.ts','export async function enrollStudentAction',60)]),
'03-WORKED-CHANGE.md':('Drop once, promote an eligible learner and backfill work',"""
A drop begins inside an authorized enrollment.manage transaction. The action reads the enrollment and returns immediately when it is already Dropped. Other unsupported terminal states reject the command. For an Enrolled or Waitlisted row, updateMany repeats the observed status before setting Dropped and its timestamp.

Only dropping an actually Enrolled student releases a seat and invokes the internal promotion helper. The helper recounts the roster after the drop within the same transaction. It loads waitlisted candidates in createdAt and ID order, applies the existing eligibility rule, and refuses promotion when the section's teacher is inactive.

The winning candidate is updated conditionally from Waitlisted to Enrolled. backfillStudentWork creates only missing submissions for Published and Closed assignments. Draft work remains unpublished, and students who are merely waitlisted receive no submission rows. Promotion audit and queued notification/grade jobs use the same transaction client as the enrollment change.

The real SQLite test drops the original student, checks the promoted learner's exact assignment IDs, then repeats the drop. The complete stored state must remain unchanged on that repeat. Another test places an inactive candidate first and verifies that the next eligible candidate receives the seat.

A real payment or email delivery would not be rolled back by this database transaction. Here queued records are local demo work; no external mail transport is called. That boundary is part of the implementation's contract.
""", [('src/packages/shared/enrollment-workflows.ts','export async function promoteWaitlistInTransaction',100)]),
'04-TESTING-AND-DEBUGGING.md':('Exercise real actions against a disposable SQLite database',"""
The npm test command invokes scripts/test-workflows.mjs. It creates an owned temporary directory and empty SQLite file, supplies an explicit DATABASE_URL, applies the schema only there and runs all Node test files with tsx. The finally block verifies the resolved cleanup path belongs to that exact temporary directory before removing it. The original development database is never the test target.

server-workflows.test.ts mocks only Next's cookie and cache helpers through the module loader. It invokes the actual exported actions, Prisma repositories, permission helpers and transaction code against SQLite. A seeded teacher, advisor, viewer, student roster and assignment set establish concrete scope cases. Every reset belongs to the disposable database established by the runner.

SQL triggers abort selected audit inserts after domain writes have occurred. Tests then reread enrollment, submission, assignment, attendance, audit and job tables to prove rollback. This is persistence evidence, not merely a mocked promise rejection. The last-seat case invokes two enrollment actions concurrently and asserts the final enrolled count cannot exceed capacity.

Agent tests deny foreign targets before a Pending row exists, force optional logger failures without changing Succeeded, and abort the success audit to verify output and success state roll back together. The original pure-rule suites remain in the same full run. Their fast mathematical checks complement the action-level persistence cases rather than substituting for them.
""", [('scripts/test-workflows.mjs',None,70)]),
'05-PRACTICE.md':('Review school authority and transactional workflows',"""
Exercise one: use a Viewer session and submit enrollStudentAction with actorId set to an administrator. Predict whether a row or audit should appear. Repeat with job retry and a student agent run. The role decision must come from the current session, and denial must occur before a Pending agent record is created.

Exercise two: enroll one student in sections taught by different teachers. Use the first teacher's session to grade the second teacher's assignment. Explain why a student-wide visibility query is insufficient. Then grade the teacher's own assignment and verify both gradedById and audit actorId equal the current session despite a conflicting payload field.

Exercise three: fill a one-seat class, waitlist two students and drop the enrolled student. Inspect the chosen candidate, submitted-work backfill, audit and queued jobs. Repeat the drop and assert complete state equality. Move an inactive student to the front of the queue and explain which candidate becomes eligible next.

Exercise four: publish a Draft assignment with one preexisting submission and two enrolled students. Expect one inserted gap, and compare the returned count with audit metadata. Add a trigger that rejects assignment.publish audits and verify the Draft state, submissions and jobs all return to their prior values.

Exercise five: submit attendance whose final record is not enrolled, then test duplicate students and February 30. No earlier attendance write should survive. Finally make the agent logger throw after a successful heuristic result; explain why optional observability cannot redefine the persisted business outcome.
""", [('src/app/actions.ts','export async function recordAttendanceAction',45)]),
'06-SOLUTIONS-AND-REVIEW.md':('Expected authority and rollback outcomes',"""
Payload actor IDs have no authority. The Viewer fails the capability gate, and the database remains unchanged. A permitted teacher still needs exact section scope for grading, attendance and assignment management. A permitted advisor must satisfy the student scope before creating a support note or intervention. Unknown or disabled local sessions fail before school mutations.

A successful grade attributes both the record and audit to the session actor. The course's demo identity remains switchable only under explicit local configuration, so those assertions establish server-action wiring, not production login security. Callers now omit actor fields, and retained optional legacy positional arguments are ignored.

Dropping an enrolled student can promote one eligible FIFO candidate and create their missing Published or Closed work. Repeating that drop performs no further promotion or audit. Dropping a waitlisted student does not release a seat. Publication reports the actual inserted gap count rather than the entire roster size, keeping its response and audit aligned with persistence.

Attendance validates the complete roster and date before its first row write. A late audit failure rolls every attendance and queued-job mutation back through the transaction. Trigger-based tests prove this against SQLite rather than assuming a fixture's rollback behavior.

Agent success and its audit are a required pair. A failed audit leaves the run Failed without persisted success output. Once that pair commits, optional logger or notification errors are contained and cannot change Succeeded. Reviewers should inspect both transaction-client propagation and error boundaries, because correct pure rules alone cannot establish those outcomes.
""", [('src/packages/observability/audit.ts','export async function recordAuditEvent',60),('src/packages/agents/core/orchestrator.ts','    await db.$transaction',55)]),
'07-TRACE-LAB.md':('Follow a denied feedback run and a successful one',"""
Start with a teacher requesting AssignmentFeedback for a submission belonging to another teacher's section. The orchestrator parses the known agent and target enums, verifies the capability and loads only the assignment's section identifier for authorization. requireSectionWrite rejects the foreign section. No Pending AgentRun, full input snapshot or heuristic result is produced.

Now choose a submission from the teacher's own section. Authorization succeeds and the orchestrator creates Pending with createdById taken from the session. It loads the assignment and submission facts, constructs the heuristic input and runs the existing deterministic feedback function. No external model request occurs.

The result is persisted as Succeeded with input, output, confidence and trace inside a transaction that also writes agent.run audit. If that audit insert fails, the success update rolls back. The outer failure path records Failed and the error, leaving success output absent rather than retaining a contradictory completed result.

After successful commit, optional informational logging and recommendation notifications run behind failure boundaries. Even if their logger throws, the persisted success remains Succeeded. This is the distinction between required historical evidence and an optional delivery channel for observability.

For student summary and risk agents, inspect noteScope. Teacher snapshots include TeacherOnly and Shared notes; Advisor snapshots include AdvisorOnly and Shared notes. The target student's scope is checked before snapshot collection, and private notes do not leak indirectly through counts or generated prose.
""", [('src/packages/agents/core/orchestrator.ts','  const { agentType, targetType, targetId }',65)]),
'VERIFICATION.md':('Accepted evidence and local-demo limits',"""
The accepted records below identify the complete test run, generated Prisma client, TypeScript check and production build. Counts refer to actual Node test cases, including the original pure-rule files and new server-action regressions. Failed setup attempts are retained separately and excluded from passing evidence. A running process is never treated as a completed check.

The new tests use a disposable SQLite database with the real Prisma schema and actual exported actions. They establish role and resource checks, session actor attribution, last-seat capacity behavior, eligible FIFO promotion, work backfill, stable repeated drops, accurate publication counts, complete attendance preflight and rollback after real SQL audit failures. They also test agent permission ordering, transactional success/audit and optional logging failures.

Only Next cookie and cache helpers are mocked. Those replacements provide deterministic sessions and capture invalidation calls; they do not replace domain rules or persistence. The runner checks its database path and cleanup directory. No original database is reset, seeded or migrated. DATABASE_URL is now configurable, and the runtime retains its legacy local-file fallback when no override is supplied.

The application remains a local teaching demo. EDU_DEMO_MODE must be explicitly true outside production for mock sessions. The unsigned cookie switcher and local administrator fallback are not real authentication. Heuristic agents are deterministic functions, guardian digest approval is a recorded decision, and queued EmailNotification work is simulated. No external model or mail service was invoked.

Concurrent SQLite writes may produce a conflict that callers must refresh and retry. The delivery proves the selected last-seat case and rollback paths, not unlimited throughput, distributed workers or production identity. Exact original snapshots and course links accompany changed source for review and future extension.
""", [('src/packages/shared/auth.ts','export function isLocalDemoEnabled',15),('src/packages/shared/school-mutation.ts','export async function schoolMutation',35)]),
}
write_course('26e6d2bd6c54',chapters,'Actual server-action authorization and SQLite transactions, disposable integration tests, exercises and exact verification evidence. Set DATABASE_URL for your local database and EDU_DEMO_MODE=true only for local development; simulated identity is disabled in production.')
