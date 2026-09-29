from pathlib import Path
import re
D=Path(__file__).resolve().parent.parent/'stage/c10fc180fa35/astraupskill'
chapters={
'README.md':'''# From C# fundamentals to a versioned CRUD API

The existing bootcamp teaches language fundamentals through small offline
exercises. This companion lab connects those skills to an actual HTTP service.
It lives in [guides/crud-web-lab](../guides/crud-web-lab/Program.cs), outside the
numbered exercise modules, so it does not change their authoring format or
their scoreboard. The lab uses the .NET 10 shared framework and no third-party
package references. You can study it after the collections and methods modules.

The resource is a task with an identifier, title, completion flag and version.
You can create, list, read, replace and delete tasks. The interesting rule is
that a replacement or deletion must name the version the client observed.
This lets you reproduce a common CRUD failure: two browser tabs read the same
record, then the second save silently overwrites the first. The corrected
store compares and changes the version in one locked section.

Start with the concepts chapter and predict the two-editor result. Then read
the route map, follow the worked example and run the HTTP checks. They start
a real local server on an ephemeral loopback port, send requests, inspect
responses and stop the server. They are not merely assertions against copied
service logic. Read the verification chapter before interpreting their scope.

Practice uses several methods: a request trace table, a deliberately proposed
broken implementation for review, small mutation experiments, and a database
design discussion. The answer chapter is separate so you can explain your
prediction before checking it. Keep a notebook of expected state, actual
state and the assertion that distinguishes them.

This is a single-process learning service with no authentication and no durable
storage. Restarting loses tasks. It is not a production starter or a complete
HTTP conditional-request implementation. Those limits are useful teaching
boundaries: they let you isolate validation and lost-update behavior before
adding identity, persistence and deployment. A strong completion explanation
names both the guarantee demonstrated here and the stronger guarantee a real
database application would need.
''',
'01-CODEBASE-MAP.md':'''# Follow the request through three files

The [project file](../guides/crud-web-lab/CrudWebLab.csproj) targets .NET 10 with
the web SDK, nullable checking and warnings treated as errors. There are no
PackageReference entries. This companion is deliberately separate from the
bootcamp's file-based exercise runner: an HTTP application has a host lifecycle
that would distract from the original single-function exercise format.

[Program.cs](../guides/crud-web-lab/Program.cs) constructs the application,
registers one TaskStore and maps five CRUD operations. GET collection returns
an ordered snapshot. GET item returns a representation and ETag or not found.
POST validates the title, creates a task, and returns Created with Location
and an initial ETag. PUT and DELETE parse a required If-Match version before
asking the store to mutate a matching item.

[TaskStore.cs](../guides/crud-web-lab/TaskStore.cs) holds immutable TaskItem
records in a dictionary. A single lock protects dictionary access, identifier
allocation and version comparisons. Replace returns an outcome plus the new
record; Delete returns an outcome. Neither method decides HTTP status codes.
The route translates Missing, Conflict and Saved into transport responses.
This separation lets you discuss storage behavior without embedding an HTTP
dependency in every operation.

[HttpChecks.cs](../guides/crud-web-lab/HttpChecks.cs) uses HttpClient against
the running app. Its helpers create a resource, issue a conditional write and
report named cases. Each case creates its own task where needed. The app's
self-test branch starts Kestrel on an available loopback port, runs the checks,
and stops and disposes the host in a finally block. Ordinary execution listens
on the fixed local lab port instead.

Draw the path request -> binding -> title/header checks -> store -> response.
Place the lock only inside the store. Then draw a second client entering the
same store with an old version. The two arrows reveal why a lock around only
the dictionary assignment would be insufficient: comparison and mutation must
share the protected region. Keep this map beside the code when you attempt
the exercises; it is a reasoning aid, not a substitute for reading the branch
that returns each outcome.
''',
'02-CONCEPTS.md':'''# A version is part of the write contract

Suppose two clients read task 7 at version 1. Client A changes the title and
saves. Client B, still holding the original representation, changes the done
flag and sends a full replacement. An unconditional write would erase A's
title change. This lab requires each writer to include the version it read,
so the server can distinguish a current edit from an outdated one.

The API exposes the version as a quoted numeric ETag. A client sends that
value in If-Match on PUT or DELETE. In this deliberately narrow protocol,
missing preconditions return 428, unsupported or malformed tag syntax returns
400, and a valid but outdated version returns 412. Missing resource IDs have
their own not-found path. Learn these as this lab's explicit contract rather
than assuming it implements every conditional-request combination defined by
HTTP. Wildcards, weak tags and lists are intentionally unsupported here.

The crucial operation is compare-and-change. Reading a version, releasing the
lock, and later taking another lock to assign the item still permits two
writers to pass the comparison. TaskStore.Replace holds one lock while it
finds the current item, compares expected and actual versions, constructs the
replacement and stores it. Exactly one of two writers carrying the same
current version can advance that item in this process.

Validation is a different concern. A blank or oversized title is rejected
before the store mutates anything. A valid title does not prove a version is
current, and a current version does not make a blank title acceptable. Keep
those decisions separate so tests can isolate them. Trimming occurs before
the title length contract is evaluated and before storage.

Finally, a process-local lock is not a distributed database concurrency
mechanism. Two application instances would have separate locks and separate
dictionaries. Durable implementation requires the database operation itself
to express the expected version, plus an outcome for no matching row. This
lab supplies the observable behavior you can later preserve when replacing
the in-memory adapter with a real repository.
''',
'03-WORKED-CHANGE.md':'''# Work through a lost-update repair

The bootcamp previously had language exercises but no executable HTTP CRUD
companion. This addition supplies a complete small reference implementation,
not a claim that an existing production API was repaired. To understand its
central design, first imagine a naive Replace implementation that looks up
an item and assigns the submitted title and done flag unconditionally.

Create a task titled Learn CRUD. Its first representation carries version 1,
and the response exposes that version in an ETag. Give the same representation
to clients A and B. A submits title Study HTTP with the original tag. Inside
the store lock, the current version equals the expected version, so the store
constructs a new immutable record with version 2 and returns it. The route
returns that record and its new tag.

B then submits its old tag with title Study SQL. The store finds version 2,
compares it to B's expected version 1, and returns Conflict without assigning
anything. The route translates that outcome into 412. A subsequent GET still
returns Study HTTP at version 2. That final read matters: status alone would
not expose an implementation that writes the losing request before rejecting it.

The same version rule protects deletion. A stale delete must not remove a
task that another client has changed. A current delete returns no content;
a later read confirms the resource is gone. The lab does not automatically
retry a rejected write because a retry with the new version could overwrite
changes the user has not reviewed.

Compare this path with an invalid title. Validation returns before entering
the write operation, leaving both fields and version unchanged. Then compare
an unknown identifier with a well-formed tag: it reaches the store and produces
Missing. These neighboring paths teach why one generic failure branch is less
useful than explicit outcomes. Keep the data transition, HTTP response and
client recovery decision separate in your explanation of the example.
''',
'04-TESTING-AND-DEBUGGING.md':'''# Observe HTTP and stored state together

Run the companion with the --self-test argument shown in the verification
chapter. The checks execute through real HTTP against a local Kestrel host.
That includes request binding, route selection, headers, JSON serialization
and the in-memory store. Unlike the focused dependency-double tests in some
larger projects, these checks do not substitute the route or store. They still
do not exercise a durable database, browser interface or authenticated session.

Each named test should answer an observable question. Does creation return
the resource location and initial tag? Does an invalid title leave collection
size unchanged? Does a replacement advance the version and retain the ID?
Does a stale writer receive rejection while the winner's state survives?
These assertions connect transport behavior with state rather than treating
an expected status code as sufficient proof.

The concurrent-editor test issues two replacement requests with the same tag
and checks that exactly one succeeds and one receives 412. It accepts either
winner, avoiding an assumption about scheduling order. The final representation
must have version 2 and one submitted title. This is one executed overlapping
request scenario, not exhaustive stress testing of every possible interleaving.
The store lock and code review supply additional reasoning about the invariant.

When a check fails, identify its layer before editing. A 400 from malformed
JSON may happen before your handler is entered. A missing ETag points to the
response construction. Two successful concurrent writes point to comparison
and mutation being separated or the expected version being ignored. A 412
with changed state points to the rejection occurring too late.

For a mutation exercise, work in a scratch copy and remove the expected-version
comparison. The stale-writer and competing-writer checks should fail. Restore
it, then move comparison outside the lock and reason about an interleaving
even if one short run happens to pass. Tests can demonstrate a failure, but
a passing schedule cannot prove that an incorrectly synchronized implementation
is safe. Explain both the observed result and the code-level reason for it.
''',
'05-PRACTICE.md':'''# Exercises: predict, implement, review

First, predict a request sequence on paper. Create a task, read it twice,
replace it using the first reader's tag, attempt deletion using the second
reader's old tag, then read it again. Record status, title, done flag and
version after every step. Make your prediction before running any commands.
Explain which request changes state and which merely observes or rejects it.

Second, extend a scratch copy with a description field. Decide whether PUT
requires a full replacement and how omission should behave. Add success and
stale-write checks that inspect both title and description. Do not silently
turn PUT into partial update just because optional fields seem convenient.
Write the contract first, then compare the implementation against it.

Third, review a teammate's concurrency proposal: read the current version
under a lock, release it, compare outside the lock, and take a second lock
to save. Draw two writers passing the comparison before either assignment.
Explain why thread-safe dictionary access alone does not protect the larger
business operation. Identify the smallest region that must remain indivisible.

Fourth, add a malformed JSON HTTP check and a null-title check. Verify both
the response and absence of mutation. Distinguish framework binding rejection
from application title validation. Keep these as new observations rather than
assuming that the existing title-boundary test covers every malformed request.

Fifth, design the database version. Sketch a table with identifier, title,
done flag and version. Write a conditional update that changes only the row
whose identifier and version match. Describe how to distinguish no matching
resource from a stale version if the API needs both outcomes. Include a
two-client integration test that checks final stored state, not only responses.

For a final review exercise, propose a user interface response to 412. Consider
showing the current server record beside the unsaved draft. Explain why blindly
retrying with the latest version can defeat the very protection the API offers.
Score your answer on a clear invariant, explicit request semantics and useful
recovery behavior rather than on the number of frameworks added.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Worked answers and review rubric

The sequence begins with a created task at version 1. Both readers receive
the same representation and tag. The first conditional replacement succeeds
and returns version 2. The second reader's delete still carries version 1,
so it is rejected and leaves the updated task intact. The final GET returns
the first writer's fields at version 2. A new read does not itself increment
the version because it does not change the resource.

For the description extension, choose an explicit replacement contract. If
PUT describes the whole editable resource, omission can mean the declared
default or be rejected, but it should not accidentally inherit arbitrary
old values. A partial-update endpoint needs its own omitted-versus-supplied
rules. Whichever contract you choose, the stale request must change neither
field nor version. The fixture should inspect the complete resulting record.

The two-lock proposal is incorrect because both writers can read version 1
and pass their comparisons before either saves. Serializing only assignments
still lets the second assignment erase the first. In this lab, lookup,
comparison, construction and assignment share one protected region. In a
database implementation, the expected version belongs in the mutation predicate
rather than only in an earlier SELECT.

A malformed JSON check should send invalid JSON through HttpClient and inspect
the framework response, then confirm collection state is unchanged. A null
title is a valid JSON shape but fails the lab's title rule. These exercise
different boundaries. Do not infer real HTTP behavior from directly calling
TaskStore.Create, which expects already validated input in this design.

A database sketch can update title, done and version where id equals the
requested ID and version equals the expected value. One affected row means
the conditional mutation succeeded. Zero rows requires the chosen missing
versus conflict policy; any follow-up read has its own timing limitations.
Use actual database concurrency tests before claiming equivalence to the
single-process lock.

For the UI, preserve the user's unsaved draft and fetch the current record.
Let the user review differences before submitting a new intent. Automatically
replaying a full replacement with a fresh tag simply recreates the lost-update
problem under a different sequence of requests. Good recovery design keeps
the user's decision visible rather than hiding a conflict behind retries.
''',
'07-TRACE-LAB.md':'''# Trace competing edits and rejected deletes

Use a single task so every state transition is visible. Its initial title
is Learn CRUD, done is false and version is 1. Two clients have read that
same record. Neither client can infer that another client has edited it until
the server compares their expected version with the current one.

| Step | Client request | Version before | Store action | Result |
| --- | --- | --- | --- | --- |
| 1 | A reads task | 1 | Return snapshot | ETag for 1 |
| 2 | B reads task | 1 | Return snapshot | ETag for 1 |
| 3 | A replaces using 1 | 1 | Compare, assign, increment | Success, version 2 |
| 4 | B replaces using 1 | 2 | Comparison fails | 412, no assignment |
| 5 | B deletes using 1 | 2 | Comparison fails | 412, item retained |
| 6 | B reads again | 2 | Return current snapshot | A's saved fields |

Trace step three through Program.cs and TaskStore.Replace. Mark where title
validation happens, where the header is parsed, and where the store lock is
acquired. The response's ETag is derived from the returned immutable record,
not from a separate reread that could observe a later writer. That detail
keeps the response tied to this successful mutation.

Now pause two replacement requests immediately before entering the lock.
Choose either as the first entrant. After it advances the version, the second
entrant sees the new value and rejects its old expectation. Reverse their
arrival order and repeat. The winning title changes, but the one-winner
property remains the same. The HTTP test therefore asserts the property
without requiring a particular scheduling winner.

Finally, trace an invalid title carrying the correct tag. It returns before
the mutation operation, so it does not consume a version. Then trace a missing
If-Match header with a valid title: the header check rejects it before store
mutation. Different early returns protect different rules. Write a short
explanation of why each rejected request leaves state unchanged, pointing to
the exact branch rather than merely quoting the response code from the table.
''',
'VERIFICATION.md':'''# Run the lab and interpret its evidence

From the project root, execute:

```text
dotnet run --project guides/crud-web-lab --configuration Release -- --self-test
```

For manual local exploration, omit the --self-test arguments. The ordinary
host listens on loopback port 5088. Stop it when finished; its tasks live only
in memory. The self-test path chooses an available loopback port, starts the
same mapped application, sends requests with HttpClient, and shuts the host
down in a finally block. The command returns failure if any named check fails.

The project uses the installed .NET 10 shared web framework and has no external
package references. This does not mean compilation is unnecessary: the SDK
still builds the application and may create local bin and obj folders. Those
generated outputs are excluded from the reviewed source delivery. The original
bootcamp exercise files, solutions and scoreboard are not rewritten by this
companion lab.

Captured evidence is attached after the final run. It is the authority for
the executed case count, command and exit status. The checks cover task
creation and title validation, response locations and version tags, reads,
conditional replacement, stale-write preservation, conditional deletion and
one overlapping two-writer scenario. Several cases also read state after
rejection so that a correct status cannot hide an unwanted mutation.

These are actual local HTTP checks, but their storage is still the in-memory
TaskStore. They do not establish database durability, multi-instance safety,
authentication, authorization, browser behavior or complete HTTP conditional
request compliance. No deployment is performed. If you replace the store with
a database, keep these behavior checks and add tests that coordinate real
transactions before claiming equivalent concurrency protection.

Review includes source inspection, course-link checks, baseline comparison
and delivery hash verification. Compilation with warnings treated as errors
helps catch mistakes in this new lab; it does not validate all pre-existing
bootcamp exercises. Treat each evidence statement at its stated scope. A
useful engineering report says what executed, what changed and what remains
unproven, allowing the next learner to reproduce the work without guessing.
'''
}
D.mkdir(exist_ok=True)
for name,text in chapters.items():
    words=len(re.findall(r"\b[\w'-]+\b",text))
    assert words>=250,(name,words)
    (D/name).write_text(text,encoding='utf-8')
    print(name,words)
