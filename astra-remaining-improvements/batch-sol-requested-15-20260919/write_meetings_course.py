from pathlib import Path
import json
from course_writer import write_course

base='modular-monolith-with-ddd/src/Modules/Meetings/'
test=base+'Tests/UnitTests/Meetings/MeetingTermCommandHandlerTests.cs'
domain=base+'Tests/UnitTests/Meetings/MeetingTermTests.cs'
create=base+'Application/Meetings/CreateMeeting/CreateMeetingCommandHandler.cs'
change=base+'Application/Meetings/ChangeMeetingMainAttributes/ChangeMeetingMainAttributesCommandHandler.cs'
chapters={}
def add(name,title,body,file,anchor='',count=65):
    chapters[name]=(title,body,[(file,anchor,count)])

add('README.md','Preserve the requested meeting interval','''
A meeting requested from nine until eleven should retain both boundaries. The create and change handlers previously passed the start date twice when constructing MeetingTerm. That mapping silently discarded the requested end. Fixing only a user interface would leave both application entry points capable of constructing the wrong interval.

The repair has two parts. Both handlers now pass TermEndDate as the second argument. The value object also rejects an end equal to or earlier than its start through the repository's business-rule mechanism. This places the invariant at the shared domain boundary, while the handler regressions prove the requested values actually reach that boundary.

Read the codebase map before running the exercises. Concepts explains strict interval ordering; the worked change follows the two argument mappings. Testing shows how the actual internal handlers are invoked without changing their production visibility. Practice asks you to predict repository and aggregate behavior, and the separate solutions explain those predictions.

The accepted suite contains ninety-seven unit tests, including the added interval and handler cases. Repository substitutes keep this check local. It does not establish database transaction rollback, HTTP response formatting, or deployed scheduling behavior. Treat those as separate boundaries when extending the project. The original source snapshots and recorded command evidence accompany this course so the change can be reviewed against the prior implementation.
''',test)
add('01-CODEBASE-MAP.md','Find the two mapping boundaries','''
The Meetings application module receives CreateMeetingCommand and ChangeMeetingMainAttributesCommand. Each command carries TermStartDate and TermEndDate. The create handler loads the meeting group, translates host identifiers, constructs domain values, asks the group to create a meeting, and adds that meeting through IMeetingRepository. The change handler loads an existing meeting and calls ChangeMainAttributes with newly constructed values.

MeetingTerm lives in the domain module. Its public factory delegates to a private constructor. The constructor checks MeetingTermMustEndAfterStartRule before assigning either boundary. The rule compares the supplied dates and provides the business-facing error message through IBusinessRule.

The unit test project now covers both levels. MeetingTermTests checks preservation and rejection directly. MeetingTermCommandHandlerTests constructs real aggregates and invokes the actual application handlers with substituted repositories and member context. The fixture accepts a meeting group proposal and sets a future expiration so unrelated group rules do not obscure the interval behavior under test.

When tracing a defect, first inspect the command values, then the factory arguments, then the aggregate's retained term. A successful domain factory test alone cannot detect a handler passing the wrong parameter. Conversely, a handler example with a valid interval does not establish rejection at the shared factory. These tests deliberately cover both responsibilities rather than assuming one layer proves the other.
''',create)
add('02-CONCEPTS.md','An interval must have positive duration','''
The invariant is end greater than start. Equal boundaries describe zero duration and are rejected; reversed boundaries are rejected for the same reason. A positive interval preserves the exact dates supplied by the caller. This change does not normalize time zones, round minutes, impose a maximum duration, or alter RSVP timing.

A value object is a useful place for this rule because every ordinary factory caller receives the same validation. The factory cannot return an invalid MeetingTerm and hope that a later handler remembers to check it. The established CheckRule mechanism throws BusinessRuleValidationException with the broken rule attached, keeping the failure consistent with other domain invariants.

Parameter mapping remains a separate concern. Passing start twice produces an invalid term even when the original command contains a valid end. Adding validation without correcting that mapping would turn valid create and change requests into errors. Correcting mapping without validation would still permit other callers to supply nonpositive intervals.

Consider a request starting at nine with an end at twelve. The handler must preserve twelve, and the value object must accept it. Now replace twelve with nine: construction must fail before repository addition or aggregate mutation. These two examples explain why both the mapping tests and the boundary tests are necessary. Read the assertions below and identify which responsibility each assertion protects.
''',domain,count=100)
add('03-WORKED-CHANGE.md','Correct creation and modification together','''
The create handler now constructs MeetingTerm from request.TermStartDate and request.TermEndDate before calling the meeting group's creation method. The repository add occurs only after domain construction succeeds. Its regression captures the aggregate passed to AddAsync and inspects the retained start and end, so a mere successful handler return cannot hide a mapping error.

The change handler receives the same argument correction. It evaluates the new MeetingTerm before invoking ChangeMainAttributes. If interval construction throws, the aggregate mutation method is never entered. The invalid-change regression confirms the original term remains present after the failed command.

The new business rule is intentionally small: the end must be strictly after the start. It uses the existing domain validation pattern instead of adding a parallel exception type or application-only conditional. Existing meeting authorization, group availability, RSVP term, fee, and attendee rules remain responsible for their own decisions.

The tests invoke internal handlers through reflection because the repository's architecture keeps module internals hidden. They do not add InternalsVisibleTo or expose a production handler merely to make testing convenient. Reflection is confined to the test fixture; the invoked Handle method is the real implementation. This preserves the module boundary while still detecting the original application mapping defect at its actual call site.
''',change)
add('04-TESTING-AND-DEBUGGING.md','Exercise actual handlers with controlled repositories','''
The fixture builds an accepted meeting group owned by the current member. Its repositories return known aggregates, and its member context supplies the matching identifier. These arrangements satisfy unrelated business prerequisites so the assertions focus on interval mapping and rejection. They are not database adapters and should not be described as persistence integration coverage.

The create success case captures the object supplied to AddAsync and checks both boundaries. Two invalid-create cases use equal and reversed ends, expect BusinessRuleValidationException, and verify AddAsync was not called. This establishes that rejection happens before the handler publishes an aggregate to its repository.

The change success case begins with an existing meeting and checks that a new, longer interval reaches it. The invalid-change case retains the original dates and verifies they survive the failed attempt. That assertion concerns in-memory aggregate mutation, not SQL rollback.

When a test fails during setup, inspect group ownership and expiration before changing the interval rule. When reflection reports a missing type or method, compare the helper's fully qualified handler name with the application assembly. Await the returned Task so asynchronous domain exceptions are observed. The recorded successful command builds the relevant project references and runs the unit test assembly; earlier style failures remain separate failed attempts in the campaign history.
''',test,'        private static Fixture CreateFixture()',75)
add('05-PRACTICE.md','Predict the boundary and the side effects','''
Exercise one: supply a command whose start is October first at nine and whose end is eleven. Trace the two values through the create handler and MeetingTerm factory. Identify the assertion that would fail if a developer accidentally restored the old start/start mapping. Explain why checking only the returned meeting identifier would be insufficient.

Exercise two: change the end to nine, then to eight fifty-nine. Predict the exception type, broken rule, and number of repository additions for each request. Locate the point at which execution stops. Keep your explanation about the handler's repository call separate from any assumption about a database transaction.

Exercise three: create a valid meeting, then attempt to change it to a zero-duration interval. Predict the aggregate's stored term after the exception. Explain how argument evaluation before ChangeMainAttributes makes this possible. What additional assertions would be needed before claiming every other attribute also remains unchanged?

Exercise four: move validation from the value object into only the create handler. List the entry points that would no longer receive that protection. Then restore shared validation and remove the handler mapping corrections. Explain why valid requests would fail despite the invariant being correct.

Exercise five: review the reflection helper. Find how it locates the application type, supplies constructor dependencies, invokes Handle, and awaits the result. Propose a clear failure message for a future handler rename without changing production accessibility.
''',test,'        [TestCase(0)]',60)
add('06-SOLUTIONS-AND-REVIEW.md','Explain the expected outcomes','''
The valid create request retains nine and eleven in the captured aggregate. The end-date equality assertion detects the old mapping directly. An identifier assertion would merely prove that some aggregate was created, leaving the incorrect duration invisible.

Both equal and reversed ends break MeetingTermMustEndAfterStartRule and surface as BusinessRuleValidationException. No repository addition occurs because constructing the value object fails before group creation and AddAsync. This is an ordering guarantee within the tested handler, not evidence that a database rolled back a previously issued write.

The failed change retains the original term. The new MeetingTerm must be evaluated before the aggregate method can be invoked, and that evaluation throws. The regression explicitly inspects the dates; it should not be summarized as comprehensive verification of every meeting property or every exceptional path.

Validation only in creation would miss modification and other factory callers. Validation without the mapping fixes would reject valid requests because the handlers would still construct equal start and end values. The two changes therefore address different defects and need complementary tests.

The reflection helper loads the internal handler type from the application assembly and uses its constructor and Handle method. Awaiting the returned task observes asynchronous failures. During review, check that no production visibility was widened, that tests invoke real handlers, and that repository substitutes are described accurately. Future persistence tests should use an isolated database and prove their own transactional behavior rather than inheriting that claim from these unit results.
''',test,'        private static MeetingTerm GetTerm',60)
add('07-TRACE-LAB.md','Follow a failed modification','''
Begin with a valid meeting scheduled for tomorrow for one hour. Write down the original start and end from its private term, as the test fixture does. Configure the repository to return this exact aggregate when the handler requests the meeting identifier. Configure the member context with the group owner so authorization is not the cause of failure.

Construct a change command starting three days from now with its end equal to its start. Enter Handle and record the repository lookup. Next, evaluate the arguments intended for ChangeMainAttributes. The MeetingTerm factory delegates to its constructor, which checks the new rule. At this point the comparison detects equality and throws.

Mark the aggregate mutation call as not entered. Observe the rejected task through Assert.ThrowsAsync, then read the original aggregate again. Its dates should still equal the original values. The regression does not need a timing delay because the awaited task defines the completion boundary.

Repeat the trace with an end four hours after the requested start. Construction succeeds, the aggregate method runs, and the new interval is retained. Finally, deliberately substitute TermStartDate for TermEndDate in a disposable copy and predict the valid-change test failure. This mutation demonstrates why the handler assertion protects the original bug rather than merely restating the new rule. Restore the correct mapping before accepting any evidence or packaging the project.
''',test,'        public void ChangeMeeting_InvalidDuration',40)
add('VERIFICATION.md','Interpret the unit test evidence','''
The accepted command completed with ninety-seven passing unit tests and no failures or skips. The attached TRX gives machine-readable outcomes, while the command log shows the referenced assemblies built for the run. The selected target is the Meetings domain unit test project; its references include application and infrastructure assemblies needed by the existing suite.

The added tests cover exact positive interval preservation, equal and reversed interval rejection, both application handler mappings, prevention of repository addition after invalid creation, and preservation of the existing term after invalid modification. Reflection invokes the actual internal handlers, while repository and member-context substitutes isolate their dependencies.

No SQL integration suite was executed for this improvement. A project reference with IntegrationTests in its name is not evidence that a database integration test ran. No deployment, migration, external service, or browser workflow is included in this acceptance claim. The course separates those boundaries so future work can choose the appropriate environment deliberately.

Earlier attempts exposed source-style violations and were corrected before the accepted run. Long Windows paths also produced assembly-cache warnings in an earlier build attempt. The successful final command is the acceptance evidence; failed attempts remain in the working history. Original snapshots accompany changed source files, and the delivery process verifies their canonical hashes before copying. Reading these guides or passing software tests does not establish human mastery of the architectural concepts.
''',domain,count=100)
write_course('209d90f0603b',chapters,'Trace meeting interval mapping, domain validation, and actual handler regressions.')
b=Path(__file__).resolve().parent.parent
(b/'specs/209d90f0603b.json').write_text(json.dumps({'changedFiles':[],'summary':['Preserved requested meeting end dates in create and change handlers.','Rejected zero or reversed meeting intervals through a shared domain business rule.','Added actual handler and value-object regressions; passed 97 unit tests and added nine source-based guide chapters.'],'limits':['Repository substitutes establish handler and aggregate behavior, not SQL transaction rollback or HTTP/browser behavior.']},indent=2),encoding='utf-8')
