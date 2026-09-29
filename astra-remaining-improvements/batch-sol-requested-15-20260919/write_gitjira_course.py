from pathlib import Path
import json
from course_writer import write_course

service='apps/api/src/services/sprint.service.js'
test='apps/api/test/sprint.test.js'
chapters={}
def add(name,title,body,file=service,anchor='',count=70):
    chapters[name]=(title,body,[(file,anchor,count)])

add('README.md','Keep sprint assignment and completion consistent','''
GitJira lets project members plan issues into sprints and complete active sprints by moving unfinished work elsewhere. These operations share state. If assignment and completion race, an issue must not remain assigned to a sprint that has already completed. A stale browser must also receive a conflict instead of silently replacing a newer assignment.

The improvement coordinates these paths with serializable transactions, bounded retries for recognized database conflicts, and conditional updates. Completion validates its destination inside the transaction and changes only an active source sprint. Assignment checks destination state and can compare the issue's updatedAt value supplied by the browser. The next timestamp advances even when the wall clock has not moved forward.

This course follows the service and its real PostgreSQL regressions. Read the map to connect browser input, authorization, state transitions, and database writes. Concepts separates transaction isolation from optimistic concurrency. The worked example follows completion; the exercises ask you to predict competing requests and inspect durable state after rejection.

Tests run in a helper-owned temporary PostgreSQL cluster. The verification chapter records accepted commands and distinguishes them from failed attempts. No deployed service, external queue, or browser interaction is certified by the API checks. Existing project documentation remains useful background; these chapters focus on the specific state transitions changed in this improvement.
''',anchor='async function serializable')
add('01-CODEBASE-MAP.md','Trace browser intent to database predicates','''
The backlog page forms sprint assignment requests. Its current issue timestamp accompanies the chosen sprint so the API can detect a stale edit. The shared assignment schema permits the version value, and the issue route passes validated input to the sprint controller. The service is the point where project membership, allowed action, destination state, and persistence meet.

loadProject finds the project and calls authorize. A nonmember receives the existing concealed-project 404 response. A member whose role lacks the requested action receives the policy's denial. Those checks must precede mutation; destination identifiers supplied by the client do not establish ownership.

The serializable helper surrounds start, completion, and assignment work. It retries Prisma P2034 conflicts at most three attempts, then returns a domain conflict. The sprint state machine still defines valid lifecycle transitions, and the database's partial unique index still enforces one active sprint per project.

The sprint test file opts out of the usual transaction rollback proxy. Competing operations need separate real transactions to exercise isolation and constraints. Its setup creates project members, workflow columns, issues, and sprints inside the isolated database. When debugging, follow the request through the controller into this service, then compare the persisted issue and sprint with the response. A status assertion alone can miss stranded work.
''',anchor='async function loadProject')
add('02-CONCEPTS.md','Separate isolation, state guards, and stale edits','''
Serializable isolation addresses interactions among concurrent transactions. Assignment and completion can each read valid state at the beginning, yet their combined writes could violate the lifecycle contract. Running both through the same isolation policy lets the database reject an incompatible interleaving. A bounded retry repeats the entire transaction against a fresh view; it does not merely repeat the last statement.

A conditional update answers a different question: does this row still have the state required for this transition? Completion updates only ACTIVE. Assignment optionally matches the version the browser originally saw. A zero-row update becomes a conflict, preserving a meaningful response for a losing caller.

Timestamp advancement must be strict. If two assignments occur within one clock millisecond, assigning the current wall time again could leave the version unchanged. The new value is the greater of wall time and the previous timestamp plus one millisecond. The regression places the stored timestamp in the future and verifies an exact one-millisecond advance.

Authorization and destination validation remain independent of these concurrency mechanisms. A serializable transaction cannot make a foreign sprint an allowed target. The service requires the destination to belong to the same project, and completion accepts only a planned destination other than itself. Each mechanism protects a distinct invariant and should retain its own test.
''',anchor='export async function assignIssueToSprint')
add('03-WORKED-CHANGE.md','Complete the sprint and move work together','''
Completion first resolves the authorized project, then enters a serializable transaction. It loads the source sprint within that project and asks the state machine for the completion transition. A supplied destination is checked for self-reference, project ownership, and PLANNED state. The backlog is represented by a null destination.

The handler identifies DONE workflow columns and claims the source transition with updateMany restricted to ACTIVE. If another request already completed the sprint, the conditional update changes zero rows and the service rejects the request. Unfinished issues then move in one bulk update within the same transaction. The response returns the persisted sprint, including its completion timestamp, and the actual moved count.

This sequence prevents a partial success in which the sprint becomes completed but unfinished issues remain stranded because a later write failed. It also ensures destination rejection occurs before mutation. Concurrent assignment uses the same serializable boundary so it cannot commit an incompatible assignment after completion's view of unfinished work.

Read the excerpt and mark every database statement. Identify which predicates scope data to the project, which express lifecycle state, and which select unfinished work. Do not describe the transaction as an external side-effect guarantee: this path coordinates local database changes, while other infrastructure has separate delivery semantics.
''',anchor='export async function completeSprint')
add('04-TESTING-AND-DEBUGGING.md','Test real competing transactions','''
The sprint suite creates fixtures through the API and exercises actual PostgreSQL transactions. The stale-token race sends two assignments with the same captured version and requires one success and one conflict. It inspects the winning sprint and verifies that the returned timestamp changed. The future-clock case protects strict advancement independently of scheduler timing.

The completion race sends two completion requests and requires a single winner with one moved issue. Another regression races assignment against completion and checks that the issue is ultimately in the backlog. Cross-project destination rejection checks both the source sprint's ACTIVE state and the issue's retained assignment after the error.

The nonmember test expects the service's intentional 404 and reads the issue afterward to prove the denied request changed neither sprint nor version. This is stronger than accepting any error status. Separate socket tests now await presence or join-error events instead of guessing that a short sleep was enough; clients close after each test even when an assertion fails.

The local helper creates and removes its own PostgreSQL cluster and streams command output into the recorded log. Resource-sensitive timeouts are supplied on the command line for this machine. Failed commands remain visible in campaign evidence. Inspect their actual assertions before deciding whether a failure concerns application behavior, test synchronization, or environment capacity.
''',file=test,anchor="  it('allows exactly one assignment")
add('05-PRACTICE.md','Predict winners and unchanged rows','''
Exercise one: two browser tabs load issue version T. Tab A assigns sprint S1 and tab B assigns S2 using the same version. Predict the two statuses and final assignment. State why simply reading T before an unconditional update would leave a race even inside otherwise well-structured service code.

Exercise two: place the issue timestamp one minute ahead of the wall clock. Assign it with that exact expected timestamp. Calculate the next stored value and explain how a subsequent stale request is rejected. Contrast this with assigning Date.now without comparing the previous value.

Exercise three: complete an active sprint while another request assigns a previously unassigned issue to it. Enumerate the acceptable assignment outcomes and the final issue location. Identify why both paths need compatible transactional behavior; protecting completion alone cannot control an unrelated writer.

Exercise four: use a destination sprint in another project, then the source itself, then a completed destination. Predict which validation rejects each request and which durable rows remain unchanged. Separate project concealment from lifecycle conflict.

Exercise five: force repeated recognized serialization conflicts. Count the maximum transaction attempts and identify the final outward error. Then consider an unrelated programming exception: explain why retrying it under the same policy would hide defects or repeat work unnecessarily. Locate the exact error-code check before proposing a change.
''',file=test,anchor="  it('rejects cross-project completion")
add('06-SOLUTIONS-AND-REVIEW.md','Review the transition contract','''
For the shared-version race, one assignment succeeds and one returns a conflict. The final sprint belongs to the winner, and the timestamp advances. The version belongs in the update predicate because a prior read can become stale before the write. Serializable retry may rerun the transaction, but the unchanged expected version must still lose against the winner's update.

With a future stored timestamp, the next value is precisely the previous value plus one millisecond. This retains a strictly advancing version without assuming a monotonic wall clock. The test compares the exact difference, so replacing the expression with Date.now would be detected.

In the assignment-versus-completion race, assignment can succeed before completion moves it or can lose with a conflict. In either accepted ordering, the final issue cannot remain assigned to the completed sprint. Checking only the assignment response would miss that essential final-state property.

A foreign destination is not found within the authorized project. Self-reference and nonplanned completion destinations are conflicts. The source remains active and its issue remains assigned after rejection. A nonmember receives the established project-concealing 404, with no mutation.

The retry helper permits three attempts only for P2034. After exhaustion it reports a conflict; unrelated errors propagate. Reviewers should check the scope of the entire retry, the state-qualified writes, destination ownership, and the browser's version handling. Passing isolated API tests does not establish the user's browser recovery experience, which requires its own workflow verification.
''',anchor='async function serializable',count=85)
add('07-TRACE-LAB.md','Interleave assignment and completion','''
Draw one column for assignment and another for completion. Begin with an ACTIVE sprint containing one unfinished issue and a second issue in the backlog. Both callers are authorized project members. Record the point at which each transaction reads the sprint and the issue versions.

First let assignment commit before completion finishes its view of the work. Completion must either include the newly assigned unfinished issue in its move or encounter a serialization conflict and retry against the committed state. After successful completion, both unfinished issues belong to the chosen destination.

Now let completion commit first. Assignment cannot successfully leave its issue on the completed sprint. On retry it observes COMPLETED and rejects; a conflicting transaction can also exhaust retries and return a conflict. The regression allows the appropriate assignment status but always reads the final issue and requires the backlog result for its fixture.

Finally race two completions. Both may initially read ACTIVE, but only one can complete the transition. The loser cannot report a second successful move. Compare the state-qualified update, the surrounding isolation policy, and the final response fields to explain this result.

Use the actual test requests below to annotate your timeline. Avoid inserting arbitrary sleeps to force the desired winner; the invariant must hold regardless of which request reaches the database first. If a failure occurs, retain response bodies and inspect committed rows before changing timeouts or weakening assertions.
''',file=test,anchor="  it('never strands a concurrent assignment")
add('VERIFICATION.md','Read the API evidence and its boundaries','''
The command evidence appended below identifies accepted checks by exact arguments and terminal exit status. A dependency install or a running process is not a test pass. Counts refer to distinct tests, and targeted reruns do not create additional cases. Earlier failed attempts remain available in the campaign records.

The API helper uses a fresh PostgreSQL cluster bound to loopback with a dedicated test role and database. Migrations run there before tests. The helper stops the cluster and validates its temporary directory before cleanup. It never reuses the user's application database. This makes the concurrency regressions database-backed rather than mocked transactions.

The first complete API attempt exposed an incorrect 403 expectation for nonmembers, a socket test's fixed-delay race and leaked client after assertion failure, and an issue-creation concurrency failure that needed a clearer response assertion. The revised tests preserve the application's authorization contract, synchronize on actual socket events, clean up clients, and report HTTP failures before attempting to read missing issue data.

The full API suite passed 95 cases. After adding the issue-list timestamp projection, the targeted issue and sprint suite passed all 17 cases; these are reruns of existing cases, not extra tests. An intervening run crossed a long host interruption and failed two timeouts and a concurrent request. Its failures remain recorded. The final targeted run and lint passed without a production timeout workaround.

The frontend and shared run passed 17 and 35 cases respectively. Earlier frontend workers exceeded Vitest's fixed startup limit, so the local dependency runner temporarily used START_TIMEOUT=300000 and WORKER_START_TIMEOUT=330000. Its original bytes were restored afterward, and no dependency patch is delivered. Test assertions remained intact. The backlog regression now waits up to 30 seconds for the actual loaded row and rejected-change alert instead of relying on Testing Library's one-second default on this constrained host. These are component tests with intercepted HTTP responses, not a real browser session.

The accepted scope must be read from the final commands, not inferred from this course. Redis workers, deployment, external providers, and browser behavior are separate concerns. Source snapshots permit review of each changed baseline file. The exercises and explanations support learning but do not claim that a reader has demonstrated mastery merely by opening the documentation or running the software tests.
''',file='scripts/test-local.py',count=90)
title, body, excerpts = chapters['01-CODEBASE-MAP.md']
chapters['01-CODEBASE-MAP.md'] = (title, body + '\nThe issue-list projection now includes updatedAt, so the backlog actually receives the token it sends. The stale-assignment regression obtains that token from the list endpoint before racing its requests; a service-only test using a creation response would miss this wiring gap.\n', excerpts + [('apps/api/src/services/issue.service.js', '// Backlog assignment sends this version', 8)])
write_course('5be7edf43612',chapters,'Trace sprint transactions, stale-write protection, and real PostgreSQL concurrency regressions.')
b=Path(__file__).resolve().parent.parent
(b/'specs/5be7edf43612.json').write_text(json.dumps({'changedFiles':[],'summary':['Coordinated sprint assignment, start and completion with bounded serializable transactions and state-qualified writes.','Validated completion destinations and protected browser assignments with strictly advancing timestamp comparisons.','Added real PostgreSQL regressions and made socket test synchronization and cleanup deterministic; added nine source-based guide chapters.'],'limits':['API database checks do not certify deployed Redis workers or browser end-to-end behavior.']},indent=2),encoding='utf-8')
