from pathlib import Path
import re
D=Path(__file__).resolve().parent.parent/'stage/39fabfbc58f5/astraupskill'
chapters={
'README.md':'''# Master1: a repeated save should not rewrite history

A task's completion time describes when the task became done. It should not
silently become the time of the latest edit to an already completed task.
This lesson repairs that behavior in the actual
[TasksService](../apps/api/src/modules/tasks/tasks.service.ts), where every
request containing status DONE previously assigned a fresh Date. An ordinary
repeat save could therefore change the historical completion timestamp.

The repaired service distinguishes a transition into DONE from a repeated
DONE value. A newly completed task receives a timestamp. A task already DONE
retains its existing completedAt value. Reopening clears that value, and an
update that omits status leaves completion fields out of the write payload.
This is a small CRUD change with a larger lesson: fields describing events
should be driven by transitions, not merely by the latest submitted state.

Study the course in three passes. First trace the controller, DTO and service
without changing code. Next compare the original service snapshot with the
changed conditional and predict the update payload for each transition.
Finally run the focused regression and complete the exercises before reading
the answers. The trace table is intended for handwritten predictions, while
the review exercise asks you to defend the distinction between repeated state
and repeated side effects.

The tests invoke the production service logic through a local TypeScript
loader and explicit Prisma and audit doubles. They make timestamp and payload
decisions visible without reinstalling the monorepo dependency tree. They do
not run Nest's HTTP pipeline, class-validator decorators, generated Prisma
queries or a real database. Read the evidence chapter before interpreting
what a passing result establishes.

Completion of this lesson means being able to explain the preserved timestamp,
the reopen behavior and the omitted-field behavior separately. It also means
recognizing the remaining concurrency limitation: another writer can change
the task between this service's read and write. This bounded repair improves
sequential repeated edits; it does not claim that all task updates are atomic
or that the entire request has no repeated side effects.
''',
'01-CODEBASE-MAP.md':'''# Locate the transition decision

The [TasksController](../apps/api/src/modules/tasks/tasks.controller.ts) exposes
list, create and update operations. Its update method obtains request context,
reads the route identifier and forwards an UpdateTaskDto to TasksService.update.
The controller is guarded by authentication and platform roles. These are
platform task operations; do not assume that a missing organization filter
is automatically a defect without understanding those roles and their scope.

The [update DTO](../apps/api/src/modules/tasks/dto/update-task.dto.ts) describes
optional status, priority, assignee and due-date inputs. Its supported status
values include OPEN, IN_PROGRESS, BLOCKED, DONE and CANCELLED. The service
receives a partial edit, so absence of status must not reset completion time.
Read the DTO together with the service rather than treating the TypeScript
optional marker as a complete description of runtime validation.

TasksService.update first reads the existing task, constructs a Prisma update
payload, performs the update, writes an audit record and returns the updated
task. The existing record is already available for deciding whether DONE is
a new transition. The patch therefore needs no new database query or schema
field. It changes the completedAt decision inside the existing status branch.

Audit logging records the before and after status and priority. It remains a
separate awaited operation following persistence. The repair does not make
the task write and audit write transactional, and it does not suppress audit
events for repeat saves. Keep those facts separate from preservation of the
completion timestamp.

The focused regression lives in [the service test](../tests/tasks-service-completion.test.mjs).
It supplies the task read result, records update arguments and records audit
calls. Its local loader removes standalone Nest decorator syntax before
Node's TypeScript transformation; the method body being exercised is the
actual service source. Draw the flow with four observations: prior status,
requested status, generated completedAt field and returned task. That map
makes the intended transition behavior inspectable without needing the entire
platform running at once.
''',
'02-CONCEPTS.md':'''# State equality is different from an event

An enum value describes current state. A timestamp such as completedAt
describes an event in the resource's history. Assigning status DONE does not
necessarily mean a completion event just occurred: the task may already have
been done when the user opened the form. This distinction matters whenever
an edit screen submits all displayed fields, including values the user did
not change.

Consider a task completed Monday morning. On Tuesday someone changes its
priority and the form also sends DONE. The old service replaces Monday's
completion time with Tuesday's save time. No task work was completed on
Tuesday, yet reports using completedAt could now tell that story. The repaired
branch looks at both the before state and requested state, preserving the
existing value when both are DONE.

Entering DONE from another supported state is different. That is the point
where this service should create a new completion timestamp. Leaving DONE
clears the value under the existing product convention. Omitting status is
different again: this partial request does not express a status operation,
so it should not include status or completedAt in the update payload.

This behavior is a narrow form of repeat stability. Repeating DONE no longer
changes completedAt. It does not make the entire request idempotent in every
observable way: audit events still occur, and database-maintained edit times
may change. Be precise about which state is stable rather than labeling the
whole API idempotent from one assertion.

There is also a data-quality question. If an already DONE row contains a null
completion time, preserving it does not invent a historical timestamp. Repairing
such rows would require a separate policy and evidence. Similarly, the current
read-then-update sequence can race with another writer. A timestamp decision
based on stale before state is a concurrency problem distinct from this
sequential repeat-save defect. Naming those limits helps you propose focused
follow-ups instead of expanding one small fix into an unreviewable rewrite.
''',
'03-WORKED-CHANGE.md':'''# Use the before state already in hand

Open the original service snapshot and find the data object passed to
prisma.task.update. Before this repair, the status branch used the requested
value alone: DONE selected new Date, and another supplied status selected
null. That correctly handled first completion and reopening, but it could
not distinguish a repeat DONE save from a new completion.

The method already reads the task into before. The repaired expression uses
that record when dto.status is DONE. If before.status is also DONE, assign
before.completedAt. Otherwise assign a new Date. For another supplied status,
retain the existing null behavior. Keep the outer optional-status branch so
ordinary priority, assignee or due-date edits do not add completion fields.

Work through a concrete example with a saved timestamp of January 2 at 03:04.
Supply status DONE again and inspect the update arguments. The timestamp
should be the original value, even though execution happens much later.
Then supply OPEN: the generated payload should clear completedAt. Finally
omit status and change priority: the payload should contain the requested
priority without either status or completedAt.

The fix changes neither the task identifier predicate nor the audit sequence.
The returned value continues to be the updated task from Prisma. These
neighboring contracts matter because a timestamp repair should not accidentally
return the stale before record, add extra reads or skip existing audit behavior.
Tests record those effects where relevant rather than relying only on a
comparison of one local variable.

Review runtime input behavior as well as the typed DTO. Replacing a truthiness
check with a presence-only check can change how null or empty input reaches
persistence, even if those values are absent from the TypeScript union. Avoid
that unrelated change unless its intended contract is established and tested.
The smallest useful patch expresses the transition rule while preserving
the surrounding update semantics. Compare the final diff with the original
snapshot and explain every changed condition in terms of observable behavior.
''',
'04-TESTING-AND-DEBUGGING.md':'''# Assert payloads, not merely Date-shaped values

The focused suite constructs TasksService with explicit task repository and
audit doubles. The task read returns a known prior record; the update double
captures the data object and returns the resulting record. This makes it
possible to observe what would be sent to persistence without needing a
database or the full Nest application. The service method itself remains
the actual source under test.

For repeat DONE, use a fixed historical completion time and assert exact
preservation in the update payload. For first completion, a controlled clock
lets the fixture assert the intended current instant rather than merely
checking that an object has a getTime method. For reopening, assert null.
For omitted status, assert absence of the completedAt key rather than treating
undefined and null as interchangeable values.

Those distinctions catch different regressions. A test that accepts any Date
would let the original repeat-save defect pass. A test that checks only the
returned task could hide an incorrect write if the double returned a canned
object. A test that ignores key presence could miss an unintended null field
being sent during a priority-only update. Record and inspect the actual
arguments at the persistence boundary.

If a case fails, inspect the before status and requested status first. Then
inspect the selected branch and generated data. Only after that inspect the
repository or transport adapter. The order keeps a small business-rule bug
from turning into an unfocused debugging session across the whole monorepo.

The loader removes standalone decorator syntax because the dependency-free
Node transformer does not execute Nest decorators. DTO classes, Prisma and
audit dependencies are substituted. Consequently, these checks do not prove
HTTP validation, dependency injection, authentication or SQL behavior. A later
integration test should submit a real PATCH through the configured application
and inspect persisted completion time. Keep that proposed experiment separate
from the captured focused run, and retain failed attempts instead of presenting
them as evidence that the final implementation passed.
''',
'05-PRACTICE.md':'''# Predict the transition before editing

Exercise one is a payload prediction. Start with a DONE task whose completion
time is a fixed historical instant. Predict data for four requests: DONE
again, OPEN, priority HIGH with status omitted, and an empty update. Identify
which payloads include completedAt and whether the value is preserved, cleared
or absent. Do not collapse absent and null into the same answer.

Exercise two is a regression-design task. A teammate checks that saving DONE
returns an object with a completedAt property. Explain why that test would
not catch the original bug. Replace it with an assertion that distinguishes
the historical instant from the time of this save. Add a first-completion
case that would fail if the implementation always reused before.completedAt.

Exercise three is a review task. Someone proposes removing the initial task
read and always setting completedAt from the request body. Explain the trust
and history problems this creates. If performance motivates the proposal,
describe the repository-level evidence needed before moving the transition
decision into a database expression. Do not assume deleting a read is always
an improvement.

Exercise four asks about repeat behavior. The completion time remains stable
on repeated DONE, but an audit entry is still written. Is the whole request
idempotent? Write a precise answer that names the stable field and the
remaining side effects. Give one example where repeated audit entries might
be acceptable and one where deduplication would require its own contract.

Exercise five explores concurrency. Writer A reads OPEN. Writer B completes
the task and saves. Writer A then sends DONE using its earlier before state.
Draw the sequence and explain why this patch alone does not guarantee the
earliest completion time survives. Propose an optimistic version predicate
or transaction experiment, including the observable failure it should detect.

Finally, consider a legacy row that is DONE with completedAt null. Decide
whether preserving null, stamping now or recovering an audit timestamp is
appropriate for a separate repair. List the evidence your choice requires.
The objective is disciplined reasoning about history, not inventing a date
because a nullable field looks inconvenient.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Answers: preserve the meaning of each field

For a repeated DONE request, data includes status DONE and the existing
completion timestamp. Reopening with OPEN includes status OPEN and completedAt
null. A priority-only edit includes priority but no completion fields. An
empty update contains no new completion decision. These predictions describe
the service's generated payload; database behavior for an otherwise empty
update belongs to its own integration contract.

The property-existence test is weak because both the original fresh Date and
the correct historical value satisfy it. Use a specific saved timestamp and
assert that exact value reaches the update. A separate transition from OPEN
to DONE should use the controlled current instant. Together they distinguish
preserving an old completion from creating a new one, preventing an overly
broad fix that always preserves null.

Letting the client dictate completedAt would turn a historical server decision
into ordinary editable input. It also fails to establish whether a transition
occurred. Moving the decision into SQL could be reasonable, but requires a
clear mutation expression, returned-row semantics and database-backed tests.
Removing the read without replacing its information is not equivalent behavior.

The entire request should not be called side-effect free on repeats. Its
completion timestamp is stable, while audit logging still records the save.
That may be appropriate when the audit describes user actions. If downstream
billing or notifications must occur once, they need their own idempotency or
deduplication rule; timestamp preservation does not automatically protect them.

In the concurrency example, A's earlier OPEN record leads it to generate a
fresh completion after B has already completed the task. A version-qualified
write could reject A if the task changed since its read. Test that with two
controlled writers and inspect both the final completion time and rejection
behavior. A focused sequential fixture cannot establish that stronger guarantee.

For legacy nulls, the bounded repair preserves the existing value on repeated
DONE. Stamping the current time would invent a completion event. A separate
data repair might recover a trustworthy audit event if one exists, but its
policy must address absent or conflicting history. Good review notes separate
the current request defect, legacy data quality and concurrent writes instead
of pretending one conditional solves all three problems.
''',
'07-TRACE-LAB.md':'''# Trace state, event time and audit separately

Let the original completion time be T1 and the current clock be T2. Keep
those symbols distinct even if a quick manual run would produce nearby
timestamps. The purpose of the lab is to expose the semantic difference
between completion history and the moment another save request executes.

| Before | Requested status | completedAt in update | Meaning |
| --- | --- | --- | --- |
| OPEN, no completion | DONE | T2 | Enter completed state |
| DONE, completion T1 | DONE | T1 | Preserve existing history |
| DONE, completion T1 | OPEN | null | Reopen the task |
| DONE, completion T1 | omitted | absent | No status operation |
| DONE, completion null | DONE | null | Preserve legacy value |

First trace the second row in the original snapshot. The requested value
selects new Date without considering before.status, so T2 replaces T1. Now
trace the corrected method: the before record selects its existing value
instead. The number of repository reads and writes does not need to change
to repair this sequential decision.

Next trace the omitted-status row while priority changes. The status branch
contributes no fields, so completedAt should not appear in the data object.
Follow the returned updated task into audit logging. The audit still records
before and after status and priority, then the method returns the updated
record. Timestamp stability does not imply that no audit effect occurs.

For the advanced trace, pause writer A after its initial read and allow writer
B to complete the task. Resume A and note that its before record remains
stale. The current patch reasons correctly from the record it read but does
not prevent that interleaving. Mark the gap between read and update on your
diagram and label the additional database evidence needed to close it.

Finish by explaining each row aloud without using the phrase “sets the date
correctly.” Name the state transition, the field presence and the selected
value. That level of specificity turns a vague code review into a falsifiable
claim another engineer can test.
''',
'VERIFICATION.md':'''# Evidence and limits of the completion-time fix

The production change is confined to the task update service. Its original
file is retained in astr au pskill snapshots for direct comparison; use the
actual snapshots folder beside these chapters. The regression loads the
service's method body, provides controlled prior records and inspects update
and audit calls. Captured execution evidence is attached after the final
reviewed run, with its command, exit status and actual test count.

Run the focused suite from the project root using the local Node loader:

```text
node --experimental-vm-modules --test tests/tasks-service-completion.test.mjs
```

The loader transforms TypeScript with Node and removes standalone decorator
syntax. It does not run Nest's dependency-injection or routing system. Explicit
DTO, Prisma and audit substitutes make service decisions observable without
installing all workspace packages. Those substitutions must remain visible
when reporting the result; a passing service case is not a passing HTTP or
database integration suite.

The intended evidence covers repeated DONE preserving the saved instant,
entering DONE creating a completion value, reopening clearing it and omitted
status leaving completion fields out of the payload. Review also checks that
the existing persistence and audit sequence remains intact. The final captured
test file and log establish which concrete variants executed; proposed
exercises are not added to the passing-case total.

No real database, generated Prisma client, class-validator pipeline or full
platform build is claimed by this focused check. Concurrent read/write races,
atomic task-and-audit persistence and legacy timestamp repair remain separate
questions. The platform role guard is inspected for context but is not tested
by these service doubles.

Before extending this work, run a real application PATCH against a prepared
database row with a known historical completion time and inspect the persisted
value after a repeat save. Then coordinate competing writers if you intend
to claim concurrency protection. Mechanical baseline, snapshot and link checks
support delivery integrity, while source reasoning and executed behavior
support the bounded fix. Keep those evidence types distinct in your own
engineering report so that the next reviewer knows precisely what to trust.
'''
}
D.mkdir(exist_ok=True)
for name,text in chapters.items():
    text=text.replace('astr au pskill snapshots','the original-file')
    words=len(re.findall(r"\b[\w'-]+\b",text))
    assert words>=250,(name,words)
    (D/name).write_text(text,encoding='utf-8')
    print(name,words)
