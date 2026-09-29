from pathlib import Path
import re
D=Path(__file__).resolve().parent.parent/'stage/785c7da790a8/astraupskill'
chapters={
'README.md':'''# Master: protect relationships across CRUD operations

A task belongs to a user and a project. Those two relationships look ordinary
in a schema, but they encode a rule the application must enforce: the selected
project must belong to the authenticated task owner. A foreign key establishes
that a project exists. It does not establish that the current user may attach
their task to that project. This lesson repairs that distinction in task
creation and reassignment while preserving ordinary edits.

Open the [collection route](../src/app/api/tasks/route.ts) and the
[item route](../src/app/api/tasks/%5Bid%5D/route.ts). Follow POST and PATCH from
authentication through parsing to persistence. Before the change, POST trusted
the submitted project ID and PATCH protected the task row without protecting
its new project relationship. After the change, supplied destination IDs must
resolve inside the authenticated user's projects before a task write occurs.
Missing and foreign projects receive the same not-found response.

Use this course in three passes. On the first pass, read the map and concepts
without editing anything. Write down the identity used at each boundary. On
the second pass, compare the original snapshots with the repaired route and
predict the database calls for an owned project, a foreign project, and an
ordinary title edit. On the third pass, complete the exercises before opening
the answers. Keep predictions separate from observed test output.

The teaching methods deliberately vary: a worked patch explains the decision,
a trace table makes control flow visible, regression fixtures make forbidden
effects measurable, and a review exercise asks you to evaluate a proposed
shortcut. Senior-level judgment includes stating what a focused test cannot
prove. These tests load production route functions but replace authentication,
schema parsing, and Prisma boundaries. They do not certify the deployed app,
database constraints, cookie sessions, or concurrent ownership changes.

Your completion artifact is a short review note naming the invariant, the two
write paths that need it, one preserved behavior, and the next integration
test you would run. A passing command alone is not the learning objective.
''',
'01-CODEBASE-MAP.md':'''# Map the task write boundary

Start with [package.json](../package.json). This is a Next application using
Prisma, with its normal test command aimed at a timer test. The focused route
regression added for this lesson is a separate command; do not assume that
running the existing npm test automatically executes every new fixture.
Dependency manifests describe the application, while captured evidence tells
you which command actually ran for this change.

The [Prisma schema](../prisma/schema.prisma) defines User, Project and Task.
Project has userId; Task has both userId and projectId. Task's project relation
references the project identifier. Read those fields together and ask which
constraint expresses equal ownership. An ordinary project foreign key cannot
answer that question, so the route needs an authorization decision before
writing the relationship.

The collection route exports GET and POST. GET filters tasks by the current
user and can narrow by project. POST parses a task body and constructs a
create payload using the authenticated user ID. The supplied project ID is a
different trust boundary: it originated in the request and must be checked
against that same user. Merely sourcing task.userId from authentication does
not make every other field safe.

The item route exports PATCH and DELETE. PATCH uses a local optional-field
schema and updateMany constrained by task ID plus authenticated user ID.
DELETE archives a matching task. The change concerns POST and PATCH destination
selection; the archive behavior remains a useful neighboring path to inspect
without changing its product semantics.

Finally, [api.ts](../src/lib/api.ts) supplies withUser and handleError. withUser
obtains the authenticated user and produces an unauthorized response when
none exists. The focused fixture substitutes that dependency, so it checks
the route's response to an authentication result rather than session lookup.
Draw arrows from request to auth to parsing to project lookup to task write.
Label each arrow with its data, not just a function name. That diagram makes
it much easier to spot a request identifier crossing into persistence without
an ownership decision.
''',
'02-CONCEPTS.md':'''# Existence, ownership and optional fields

Consider user Alice, task A and project B. Task A belongs to Alice; project B
belongs to Bob. A PATCH constrained by task A's identifier and Alice's user ID
correctly protects the task row. It still permits a bad relationship if it
writes project B without checking who owns B. Authorization is therefore not
a single check at the beginning of the request. It must cover the resources
whose relationships the operation changes.

The destination lookup combines two predicates: the submitted project ID and
the authenticated user's ID. A result proves the requested relationship is
allowed at that moment. No result means either the project is absent or it is
outside the user's scope. Returning the same not-found shape avoids exposing
which of those explanations applies. The task write must still retain its
own user constraint; validating the destination does not authorize editing
somebody else's task.

PATCH introduces a second distinction: omitted versus supplied. Omitting
projectId means this request does not change that relationship. Supplying an
empty string is not omission. A truthiness guard would skip the lookup for
that value even though it remains in the data passed to persistence. Check
presence explicitly with projectId !== undefined, then resolve any supplied
identifier. This preserves title-only edits while preventing a bypass through
a falsy string. Validation may later reject empty IDs earlier, but authorization
should not depend on accidentally favorable coercion.

There is also a time boundary. A lookup followed by a write is not an atomic
proof that ownership cannot change between them. Whether that matters depends
on available project mutation paths and database transaction semantics. This
patch establishes the application guard; it does not claim to solve every
concurrent reassignment scenario. Advanced work should investigate those
paths before proposing a transaction, composite ownership key, or conditional
write. Choose a stronger mechanism from an actual invariant and failure
scenario, not from the assumption that adding a transaction label solves
all races automatically.
''',
'03-WORKED-CHANGE.md':'''# Repair create and reassign together

Read the original route snapshots before the changed files. In POST, trace
the submitted projectId into prisma.task.create. In PATCH, notice that the
existing updateMany already constrains the task by userId. That is valuable
behavior to preserve, but it covers the source task rather than the selected
destination. The smallest coherent repair validates the destination on both
write paths that accept it.

For creation, parse the body and resolve a project using both body.projectId
and auth.user.id. Select only the identifier because the decision requires
existence within that scope, not a full project object. If the lookup returns
null, return a project-not-found response before calling task.create. Otherwise
continue using the existing payload construction, defaults and success status.
Do not accept userId from the request as a shortcut for this lookup.

For PATCH, apply the same lookup only when projectId is supplied. The key
branch is presence, not truthiness. A title-only body must bypass the project
lookup and retain its existing edit behavior; a supplied empty identifier must
not slip into the write unexamined. After an allowed destination lookup, keep
the existing task ID and user ID predicate. A zero update count remains a
task-not-found outcome, and the existing success response remains intact.

Review the order of effects as carefully as the response text. The important
negative assertion is that the forbidden relationship produces no task write.
A handler that writes first and then returns 404 would have the same visible
status but violate the rule. The fixture therefore records persistence calls
and checks arguments, rather than testing the response status alone.

This implementation intentionally leaves neighboring GET filtering and DELETE
archival alone. It also avoids changing schema versions or installing an
entire dependency tree just to demonstrate the boundary. Those choices keep
the before-and-after comparison narrow enough to teach. When proposing a
follow-up, identify a separate observable failure and its regression instead
of growing this patch into a general rewrite of the task API.
''',
'04-TESTING-AND-DEBUGGING.md':'''# Test the forbidden effect

Open the [route regression](../tests/task-project-isolation.test.mjs). It loads
the actual TypeScript route using a local test loader and provides explicit
substitutes for infrastructure dependencies. This is more meaningful than
copying the ownership condition into a test helper: removing the guard from
production should cause the negative case to fail. It is still a focused
boundary test, not a running Next server or a real Prisma database test.

A useful fixture has three separate observations. First, record the project
lookup arguments and require both destination ID and authenticated user ID.
Second, record task writes and their predicates or payloads. Third, inspect
the response status and body. Combining these observations distinguishes a
correct rejection from a response that merely looks correct after an unwanted
write. On the success path, assert the destination actually reaches the write
and the authenticated identity remains authoritative.

For debugging, start with the earliest violated boundary. If a foreign project
case writes, inspect whether the project lookup was skipped or its null result
was ignored. If a title-only update unexpectedly fails, inspect whether the
new condition confuses omission with a required destination. If an empty
string skips authorization, inspect truthiness. If another user's task changes,
inspect the task update predicate independently of the destination query.

The schema substitute deliberately does not validate Zod behavior. Authentication
is supplied as a result, not reconstructed from a cookie. Database doubles
record calls, not SQL execution, constraints or transaction isolation. Explain
these substitutions when interpreting a green run. They isolate the route
decision but cannot prove that the surrounding adapters behave correctly.

As a mutation exercise, temporarily remove userId from the destination query
in a scratch copy. A strong argument assertion should fail even if the double
would otherwise return an owned project. Then restore it and try replacing
the presence check with truthiness. The empty-ID case should expose that
regression. Keep these experiments out of the delivered production files and
retain the original captured passing run as the verification record.
''',
'05-PRACTICE.md':'''# Practice before reading the answers

Exercise one is a prediction task. Draw a matrix whose rows are owned project,
foreign project, missing project, omitted projectId, and supplied empty ID.
Use separate columns for POST and PATCH. For each meaningful combination,
predict the response family and whether a project lookup and task write are
allowed. Mark combinations that cannot be described as a valid creation body
without invoking schema behavior. Do not invent validation results from the
test double, which deliberately passes parsed values through.

Exercise two is a test-design task. A teammate writes a fixture whose project
lookup returns null and checks only status 404. Explain two defects that this
fixture could miss. Improve it to record the exact lookup arguments and every
task write. Then add a positive case so that an implementation which rejects
all requests cannot pass the suite. State which assertion proves preserved
behavior rather than only rejection.

Exercise three is a code-review task. Review this proposal: “The task update
already filters by userId, so checking the project is redundant.” Write a
counterexample with two named users, one task and two projects. Your explanation
must distinguish authorization on the task row from authorization on the
new relationship. Finish with a concrete predicate for each resource.

Exercise four is an API semantics task. Compare an omitted projectId, an empty
string, and a null value. Explain what the actual PATCH schema permits and
what the new presence guard does. Separate schema rejection from resource
lookup rejection. Suggest how you would test real parsing if dependencies were
available, without claiming the current lightweight fixture covers it.

Exercise five is a design discussion. Imagine an administrator can transfer
project ownership while another request creates a task. Sketch the interleaving
between lookup and write. List the repository facts you would need before
selecting a database constraint or transaction strategy. Your answer should
include one integration test and a description of the invariant it proves.
Score your work on explicit identities, effect ordering, preserved success
behavior and honest test limits, rather than the amount of code proposed.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Answers and review criteria

For the prediction exercise, an owned destination allows the route to continue
to the task operation. A foreign or missing destination returns project not
found before a task write. PATCH omission performs no project lookup because
the relationship is unchanged. A supplied empty string must enter destination
checking; in an ordinary fixture with no matching project it is rejected.
POST requires its own schema-valid body, so do not use a permissive substitute
to infer how malformed creation input is handled in production.

The status-only test can miss an unscoped project query and a write that occurs
before rejection. Assert the lookup's id and userId together, then assert zero
task writes for a forbidden destination. The positive fixture should require
the expected create payload or update predicate, a single intended write and
the existing success status. This catches a simplistic implementation that
returns not found for every request while satisfying all negative tests.

For the review counterexample, Alice owns task A and project A; Bob owns project
B. Alice submits task A with destination B. Filtering the update by task A and
Alice succeeds, but project B still belongs to Bob. The project query therefore
needs destination B plus Alice's identity, while the task update continues to
need task A plus Alice's identity. Neither predicate replaces the other.

The PATCH schema uses an optional string for projectId. Omission is allowed;
empty string is still a string; null is not made nullable for this field.
The presence guard addresses supplied values. A real-schema test would import
the production route with actual Zod and check malformed inputs before any
database calls, rather than giving its parser an always-successful substitute.
Do not describe null rejection as an executed result of the current fixture.

For the concurrency discussion, ownership could change after a successful
lookup but before task creation. Investigate whether such transfer exists,
which database engine is used, and whether the schema can encode the ownership
relationship. A meaningful integration test coordinates two transactions and
asserts the final task/project owner relationship, not merely that each request
returned an expected status. The current patch does not claim that stronger
guarantee. Good review language says exactly which request boundary improved
and names the remaining database-level question.
''',
'07-TRACE-LAB.md':'''# Trace one request at a time

Use Alice as the authenticated user. Let task T belong to Alice, project P
belong to Alice, and project Q belong to Bob. Keep these identities written
beside the source while you trace. Changing several fixture identities at
once makes it harder to determine which predicate caused a rejection.

| Request | Destination lookup | Task effect | Expected route outcome |
| --- | --- | --- | --- |
| POST with P | P and Alice match | Create for Alice in P | Created |
| POST with Q | Q and Alice do not match | None | Project not found |
| PATCH T with P | P and Alice match | Update T constrained to Alice | Success if T exists |
| PATCH T with Q | Q and Alice do not match | None | Project not found |
| PATCH T, title only | No lookup | Update T constrained to Alice | Success if T exists |
| PATCH missing T with P | P and Alice match | Update count is zero | Task not found |

First trace the foreign-project PATCH in the original snapshot. Identify the
point where the submitted relationship reaches data without a destination
ownership decision. Now trace the changed route and stop at the early return.
Write the list of operations that are no longer reachable. The comparison
should explain the bug without relying on a database error to reject it.

Next trace a title-only edit. The optional project field is absent, so the
new lookup branch must not run. The task's existing ownership predicate still
decides whether an update is allowed. This neighboring path demonstrates why
a security repair needs positive preservation tests as well as rejection
tests. A guard that requires every PATCH to include a project would change
the API's meaning and break ordinary edits.

Finally, pause after a successful project lookup and imagine a second writer
changing that project's ownership. Resume the first request on paper. The
exercise exposes the difference between sequential control-flow evidence and
concurrency evidence. Do not alter the expected focused-test results to imply
the race was executed. Instead, turn the interleaving into a separate proposed
integration experiment, with explicit setup, synchronization and final-state
assertions. That is how a simple trace becomes a useful design review tool.
''',
'VERIFICATION.md':'''# Verification scope and reproducibility

The change is a bounded task relationship guard. The production files are
the collection POST route and item PATCH route. Original snapshots preserve
the exact pre-change files for comparison. The local regression and its
TypeScript loader are delivered beside the course so that the test does not
depend on a hidden helper outside the project. Captured evidence is attached
after the final reviewed run; use that record for the exact command, case
count and exit status rather than inferring execution from examples here.

The regression loads production route functions. It supplies explicit Prisma
methods that record queries and writes, an authentication result, a Next
request type stand-in, and a permissive schema substitute. Assertions target
the destination ownership predicate, absence of writes on rejection, preservation
of scoped task updates, and ordinary allowed behavior. This is useful evidence
that the handler places the guard before persistence and uses authenticated
identity in the decision.

It is not evidence that real Zod validation ran. It does not establish cookie
or session correctness, generated Prisma typing, SQL constraints, migrations,
Next routing, browser behavior, or transaction isolation. The ordinary package
test script targets other tests; the focused command must be run explicitly.
No full dependency reinstall is required for this lightweight check, but that
convenience does not convert its doubles into production adapters.

Before broadening the claim, run the original project's normal checks with
the appropriate dependencies, then add a database-backed create/reassign test
using two users. Verify both persisted ownership and returned responses. If
project transfers exist, coordinate a competing transfer with the task write
and inspect the final invariant. Record failures and environmental blockers
as results rather than replacing them with an unsupported pass statement.

Astra review also compares changed files against the staged baseline, checks
snapshot fidelity and local course links, and verifies canonical delivery
hashes. Those mechanical checks protect the integrity of the handoff; they
do not prove the application correct. Keep source reasoning, runtime evidence,
and delivery verification as separate claims so another engineer can assess
what was tested and what still needs investigation.
'''
}
D.mkdir(exist_ok=True)
for name,text in chapters.items():
    words=len(re.findall(r"\b[\w'-]+\b",text))
    assert words>=250,(name,words)
    (D/name).write_text(text,encoding='utf-8')
    print(name,words)
