from course_writer import write_course
chapters={
'README.md':('Stable training completion and assignment history',"""
This compliance learning demo assigns courses and learning paths to organization members, records assessment outcomes and issues certificates. The completed work makes successful completion a stable terminal event and keeps assignment changes from silently erasing learner history.

Previously, a completed enrollment could move back to IN_PROGRESS when a later failing score arrived. Its completion fields could be cleared while its certificate remained. A second passing score could instead create another certificate and replace dates. The completed service validates the direct score, reads enrollment and ownership inside its transaction, and returns an already completed record unchanged. A first completion uses a conditional organization, learner and expected-status update before issuing its certificate and audit.

A unique enrollmentId index now expresses one certificate per enrollment in the Prisma schema and an additive SQL migration. Existing duplicate records must be reviewed before applying that index; the migration deliberately does not delete history. No original database was changed by this delivery.

Assignment commands now validate the selected item type, exclusive target ID, unique assignees, real future due date and boolean flag. False remains false. Assignment expansion checks tenant-owned targets in the transaction, and enrollment upsert updates only the due date when the record already exists. Cancellation conditions its write on ACTIVE and commits its audit together while preserving linked learner progress and certificates.

The expiry helper uses UTC calendar months and clamps to the final day of the destination month. Null means no expiry; zero or malformed month counts are invalid. Assessment scores are still supplied by a trusted demo caller, so this is not a secure exam-grading implementation. Read the tests and verification limits with that distinction in mind.
""", [('src/services/serviceHelpers.ts','export function addMonths',50)]),
'01-CODEBASE-MAP.md':('Trace assessment and bulk-assignment commands',"""
submitAssessment in enrollmentService.ts owns the completion workflow. It applies the existing permission map, obtains the actor organization and parses the direct score before opening a transaction. Inside that transaction, findEnrollmentById includes organizationId next to the enrollment ID. Learner ownership is checked before terminal status is returned, so a completed record does not become an authorization shortcut.

updateEnrollmentAttempt in enrollmentRepository.ts carries organization, enrollment, user and expected status into updateMany. Count zero is a stale-command conflict; the service does not fall back to an unrestricted update. A successful result is reread through the scoped repository. Certificate creation and the assessment audit follow within the same transaction.

assignmentService.ts parses a strict direct command and resolves users, courses and learning paths using the transaction client. It preserves the existing published-course and organization checks, then expands the assignment to enrollment records. The upsert update branch changes only dueDate, preserving status, assessment score and completion evidence.

cancelAssignment performs its scoped lookup, ACTIVE check, conditional update and audit in one transaction. Linked enrollments are deliberately retained. This cancellation policy concerns the assignment record, not revocation of historical learning or certificates.

serviceHelpers.ts contains the shared actor-organization guard and UTC month-clamping function. The Prisma schema and additive migration define the persistence uniqueness boundary. Both application orchestration and database constraints matter; a service test alone cannot demonstrate that an index has been deployed.
""", [('src/repositories/enrollmentRepository.ts','export async function updateEnrollmentAttempt',48)]),
'02-CONCEPTS.md':('Terminal events, conditional writes and UTC month clamping',"""
Completion is an event with durable historical meaning. Once an enrollment is COMPLETED, valid repeated assessment requests return the saved record without changing its score, dates, certificate or audit count. Validation still runs first, and actor scope still applies. Terminal idempotency is not permission to accept malformed commands or reveal another learner's record.

The transition policy is explicit: NOT_STARTED, IN_PROGRESS and OVERDUE can become IN_PROGRESS after a failed score or COMPLETED after a passing score. COMPLETED stays COMPLETED. EXPIRED rejects this submission path and requires a separate reassignment or recertification workflow. Unknown statuses fail rather than silently joining an allowed branch.

A read followed by an unconditional update cannot establish one winner. updateMany repeats organization, user and expected status at the mutation boundary. Once one passing request changes the row to COMPLETED, another request holding an earlier status cannot match. Certificate and audit writes occur only after a successful update, and the unique enrollmentId index adds a database-level backstop.

Calendar months are not fixed day counts and local setMonth can overflow January 31 into March. addMonths temporarily selects UTC day one, advances the month, determines its final day and restores the smaller of the original day and that limit. UTC time-of-day and milliseconds remain unchanged. Positive integer months from one through 120 are accepted; null explicitly means no expiry.
""", [('src/services/serviceHelpers.ts','export function addMonths',50),('prisma/migrations/202609190001_one_certificate_per_enrollment/migration.sql',None,10)]),
'03-WORKED-CHANGE.md':('Commit completion, certificate and audit together',"""
Begin with an IN_PROGRESS enrollment that awards a certificate. The service reads it inside the transaction and verifies learner ownership. It validates the stored passing-score rule, compares the accepted submitted score, computes the next state and derives expiry from the course's recertification configuration.

The repository receives the expected status from that scoped read. Its conditional update writes completion fields, the original-or-new startedAt, the score and certificate issue time only if the row still matches. Count zero produces a conflict before certificate or audit creation. The caller must refresh instead of forcing the stale write through.

After a winning update, createCertification stores the issue time and expiry for that specific enrollment. createAuditLog records the submitted score and pass result in the same transaction. A failure in either later operation rolls back the enrollment change as well, avoiding a completed row without its intended certificate or audit.

A later valid request finds COMPLETED after its scope checks and returns immediately. Even a failing score cannot reverse the historical completion. The saved score is the score that completed the enrollment, not the latest retry value.

The fixture tests invoke actual service and repository functions. They check the query predicate, stable retries, a conditional loser and a final audit failure. Their cloned-state transaction model is explicit; a separately serialized fixture test demonstrates orchestration but is not presented as a live PostgreSQL race.
""", [('src/services/enrollmentService.ts','export async function submitAssessment',100)]),
'04-TESTING-AND-DEBUGGING.md':('Match assertions to the boundary they prove',"""
The completion-workflows suite calls the actual assessment and assignment services with a transaction-scoped Prisma-shaped fixture. Real repositories build the query arguments and operate against cloned fixture state. A successful transaction commits that graph; a thrown audit or lifecycle error discards it. This makes whole-state rollback comparisons meaningful while keeping the persistence limitation visible.

Assessment scenarios cover failure followed by success, repeated passing and failing submissions after completion, malformed scores before transaction entry, wrong learner and organization, expired state, a conditional update loser and final audit failure. The fixture-serialized pair of passing submissions must leave one certificate and one success audit. Query assertions verify the real organization, user and expected-status fields.

Assignment scenarios reject unknown item types, contradictory targets, duplicate or empty assignees, impossible dates and string booleans. A valid false isMandatory is persisted unchanged. An upsert replay changes dueDate while leaving a completed enrollment and certificate intact. Cancellation tests inspect ACTIVE and tenant predicates, preserve linked history, reject a repeat and restore state after a late audit failure.

Expiry tests use January 31 in leap and nonleap years, a leap-day anniversary and explicit no-expiry. Invalid zero, negative, fractional, nonfinite or excessive month counts fail. Existing permission, tenant, schema and expired-state tests remain in the full suite. Consult the accepted runner total and logs below rather than counting shell commands as tests.
""", [('tests/completion-workflows.test.ts','describe(',75)]),
'05-PRACTICE.md':('Completion and assignment review exercises',"""
Exercise one: submit a failing score to a fresh enrollment, then a passing score. Save the complete enrollment, certificate list and audit list. Submit another pass and then a failure. Predict which fields may change after the first completion and assert that the entire saved state remains equal afterward.

Exercise two: simulate an IN_PROGRESS read followed by an updateMany result with count zero. Confirm that no certificate or success audit is created. Inspect the production repository query and identify every predicate that must remain present. Explain why retrying an update by enrollment ID alone would undo the protection.

Exercise three: create a course assignment with isMandatory false and one valid assignee. Repeat with an unknown itemType, both target IDs, duplicate assignees, an impossible future calendar date and a string false. Distinguish runtime input validation from the later organization and published-course lookups.

Exercise four: replay upsertAssignmentEnrollment against a completed record using a different due date. Verify that status, score, completion time and certificate issue time do not reset. Cancel its assignment and explain why cancellation does not erase learning history. Then force the cancellation audit to fail and compare the complete transaction state.

Exercise five: add one month to January 31 at 23:45 UTC in 2024 and 2025. Preserve seconds and milliseconds. Contrast the expected February dates with native local setMonth rollover. Finally inspect the unique-index migration and write an upgrade plan that reviews existing duplicate enrollment IDs without silently deleting any certificate records.
""", [('src/lib/validation/assignmentSchemas.ts','export const createAssignmentSchema',100)]),
'06-SOLUTIONS-AND-REVIEW.md':('Expected states and upgrade decisions',"""
A failed fresh attempt becomes IN_PROGRESS without a certificate. The first passing attempt becomes COMPLETED and, when configured, receives one certificate and one assessment audit for that attempt. Later valid retries return the saved completed record. No score, issue time, completion time, expiry or event count changes. A malformed retry still fails validation before that terminal shortcut.

A conditional loser is a conflict. The repository returns null when updateMany affects no row, and the service stops before certificate or audit creation. The predicate contains enrollment ID, organization ID, learner ID and the expected nonterminal status. The code does not infer a successful mutation from an earlier read.

The assignment schema accepts a real boolean false. It rejects an unknown target kind, both IDs, missing selected ID and duplicate normalized assignees. Organization membership and published-course rules are then checked through transaction-bound repositories. Existing enrollment replay changes only the due date; assignment cancellation changes only the assignment lifecycle and its audit, retaining historical progress.

January 31 plus one month becomes February 29 in 2024 and February 28 in 2025, preserving UTC time and milliseconds. Null yields no expiry, whereas zero is rejected. A twelve-month leap-day anniversary clamps to February 28 when the destination year is not a leap year.

For migration review, group Certification rows by enrollmentId and identify duplicate groups before applying the unique index. Resolve them according to an explicit historical-data policy. The supplied SQL intentionally fails on duplicates instead of selecting a survivor or deleting evidence automatically.
""", [('src/repositories/assignmentRepository.ts','export async function cancelAssignment',40),('src/repositories/enrollmentRepository.ts','export async function upsertAssignmentEnrollment',40)]),
'07-TRACE-LAB.md':('Trace cancellation without erasing learner history',"""
Start with an administrator or compliance manager in an organization and an ACTIVE assignment. Its linked enrollment has already completed and owns a certificate. The cancellation service first applies the existing capability map, derives organizationId from the session and parses the assignment ID.

Inside the transaction, findAssignmentById scopes the lookup to that organization. A missing row becomes not found without any mutation. A non-ACTIVE assignment becomes a conflict. For an active row, the repository repeats organization, ID and ACTIVE in its updateMany predicate. That condition decides whether this request is still allowed to make the transition.

On success, the repository rereads the assignment through the same scoped client. The service records assignment.cancelled in the transaction and returns the updated row. It does not call enrollment expiry or certificate deletion. Cancellation stops the assignment record while preserving the learner's completed work as a historical fact.

Now arrange a final audit failure. The fixture must show the assignment change was attempted, then restore the entire previous graph. A partially canceled assignment without its audit should not remain. Repeat the successful cancellation and confirm that a second request fails the ACTIVE check rather than creating another cancellation event.

Finish by replaying the enrollment upsert with a new due date. Its update branch contains only dueDate, so completion remains intact. This separates assignment administration from assessment lifecycle instead of letting either operation reset the other's history through a convenient but overly broad update object.
""", [('src/services/assignmentService.ts','export async function cancelAssignment',65)]),
'VERIFICATION.md':('Accepted checks and deployment limits',"""
The accepted records below identify terminal test, type-check, Prisma-generation and production-build results. Test counts come from the runner's actual total. Failed setup or validation attempts remain in the campaign logs and are excluded from the passing evidence. The final checks must correspond to the final source and generated Prisma relation types.

The service tests exercise real repository calls with a Prisma-shaped cloned transaction fixture. They establish direct validation, actor scope, conditional write predicates, stable terminal behavior, certificate and audit sequencing, rollback, assignment replay preservation and UTC month clamping. The fixture serializes its paired calls; it is not evidence of a live PostgreSQL concurrent transaction schedule.

The schema now models a single optional certification on an enrollment and a unique enrollmentId on Certification. The additive migration creates the corresponding unique index. On an existing installation, baseline its existing schema before introducing this migration and review any duplicate certificates first. The migration does not delete or merge history. For a new disposable development database, the current schema can be created with the project's normal setup procedure. No original database was reset or upgraded here.

Completion is terminal for this submission endpoint. EXPIRED enrollments still require a separate reassignment or recertification path; cancellation retains linked learning history. Null recertificationMonths means no expiry, and positive integer values are bounded at 120 months.

The submitted score remains a demo trust boundary. Validation prevents malformed values but does not prove a learner earned that score. Secure assessment would require server-owned questions, answer evaluation and attempt authorization beyond this change. Preserve that limitation with the exact source snapshots and accepted verification evidence.
""", [('prisma/migrations/202609190001_one_certificate_per_enrollment/migration.sql',None,10),('src/services/enrollmentService.ts','export function transitionEnrollmentStatus',18)]),
}
write_course('c178c034b3ed',chapters,'Stable terminal completion, one certificate per enrollment, scoped conditional writes, assignment history preservation and UTC expiry. Read the unique-index upgrade requirements and trusted-score demo limits before deployment.')
