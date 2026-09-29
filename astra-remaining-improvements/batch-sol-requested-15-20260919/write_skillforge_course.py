from pathlib import Path
import json
from course_writer import write_course

service='src/server/completion.ts'
test='tests/unit/completion.test.ts'
chapters={}
def add(name,title,body,file=service,anchor='',count=100):
    chapters[name]=(title,body,[(file,anchor,count)])

add('README.md','Commit a lesson and its rewards together','''
Skillforge completion is more than a checkbox. A completed lesson seeds review items, updates learner progress, records XP, advances quests, and may unlock an achievement. If these writes happen independently, a late failure can leave a completed lesson without its rewards or a reward without the matching completion. Retried requests can also award the same lesson twice.

The new completion service makes this one transactional decision. It checks lesson eligibility, inserts the unique learner-and-lesson completion, seeds review state, and calls the award helpers with the same transaction client and captured time. A duplicate completion returns a no-award summary. Recognized SQLite contention receives a small bounded retry; unrelated failures remain errors.

This course traces that service and the real temporary-SQLite tests. Read the map to find the authenticated action and nested helpers, then Concepts to distinguish uniqueness from rollback. The worked change explains client propagation. Practice and its separate answer chapter focus on concurrent requests and failures after nested quest or achievement writes.

The verification scope is local persistence and award behavior. It does not execute a lesson in an external code runner, certify browser interaction, or assess a learner's knowledge. The isolated helper and ownership guard keep these destructive fixture tests away from an ordinary application database.
''')
add('01-CODEBASE-MAP.md','Follow the authenticated action through nested awards','''
The lesson action resolves the current user, calls completeLessonForUser, and revalidates the affected views. The service owns the transaction rather than leaving the action to coordinate several independent writes. CompletionOptions supports an injected client and clock for tests and a late beforeCommit failure seam used to verify rollback.

The service reads the lesson's knowledge-item count before inserting LessonCompletion. Empty and unknown lessons are rejected. The completion table's unique learner-and-lesson key decides whether this is a new contribution. seedLessonReviewStates and awardActivity receive the transaction client, so review rows and gamification changes participate in the same commit.

Nested quest and achievement helpers must keep passing that client. Returning to the module-level Prisma singleton in one nested branch would escape the transaction and undermine rollback even if the outer function appeared correct. The fixture deliberately reaches quest and achievement rewards so those branches are exercised.

The local helper creates a uniquely named temporary directory, points Prisma at its SQLite file, applies the schema, and runs only the guarded completion suite. The tests check the ownership marker and path before enabling database cleanup hooks. Ordinary test runs skip these cases; passing an unrelated unit suite therefore cannot be reported as completion transaction coverage.
''',file=test,anchor='const ownedPath',count=105)
add('02-CONCEPTS.md','Uniqueness and atomicity solve different problems','''
The unique completion row is the one-award gate. Two requests may both find an eligible lesson, but both cannot insert the same learner-and-lesson pair. The losing request recognizes only the relevant P2002 conflict and returns a summary without adding a second contribution. A unique violation from another model or key must not be silently treated as an already-completed lesson.

Atomicity protects the winner's collection of writes. Completion, review state, XP events, quests, achievements, and progress must either commit together or roll back together. Uniqueness alone cannot prevent a late failure from leaving half of that collection persisted if helper calls use separate clients.

A captured clock makes related timestamps coherent across the operation and across a contention retry. The service passes the same now value into review seeding and award logic. This is a deterministic operation-time choice, not a claim that the system clock is globally monotonic.

Contention retry is bounded and selective. The code recognizes particular Prisma timeout or write-conflict errors with SQLite-related messages, waits briefly, and retries the entire transaction at most three times. It does not retry arbitrary business validation or programming failures. Explain these three mechanisms separately when reviewing a new completion path.
''',anchor='function isCompletionUniqueConflict')
add('03-WORKED-CHANGE.md','Keep every nested write on the transaction client','''
completeLessonForUser captures its client and time once, then starts the transaction. Eligibility is checked before any completion or award write. Inserting LessonCompletion establishes the unique gate. Review seeding and awardActivity receive tx explicitly, and the service returns newlyCompleted true only after the transaction commits.

The award helpers now accept the supplied database client and pass it into deeper quest, progress, ledger, and achievement operations. This propagation is the essential part of the repair: wrapping only the top-level call in a transaction would be cosmetic if nested helpers still used the global client.

The catch branch distinguishes a duplicate completion from recognized temporary contention and all other failures. Duplicate completion calls noAwardSummary with the same selected client. Contention retries the whole operation with the captured clock; unrelated errors propagate. The beforeCommit seam executes after preceding work and intentionally throws in the rollback regression.

Inspect the service excerpt and then follow every helper it calls. Mark each database write with the client used. A single escaped write can produce an XP event or achievement that survives a rejected completion. The test fixture's low daily goal and seeded achievement are designed to exercise those nested paths, rather than proving rollback only for the first inserted row.
''',anchor='export async function completeLessonForUser',count=100)
add('04-TESTING-AND-DEBUGGING.md','Fail after quest and achievement work','''
The fixture creates one learner, a course hierarchy, a lesson with two knowledge items, a low daily XP goal, and a seeded achievement. A fixed timestamp makes review due dates predictable. Successful completion must produce one lesson contribution, one quest reward, one achievement reward, and one earned-achievement row, with two review states due at the captured time.

The late-failure case throws from beforeCommit after awardActivity has run. It then checks that completion, review, XP, quest, and earned-achievement rows are absent and progress remains zero. These are real SQLite queries after a rejected transaction, not assertions against mocked method call counts.

The concurrency case starts two completions together and requires one newlyCompleted result and one duplicate result. It then repeats completion sequentially and checks that the result is still duplicate. Durable counts remain one contribution per reward kind, with unchanged quest progress and review seeds.

Eligibility cases cover both an empty lesson and a missing identifier. When debugging a failure, first confirm the owned database guard enabled the suite. Then inspect whether the failure concerns eligibility, uniqueness, client propagation, or a contention error outside the retry classification. Do not weaken durable-state assertions merely because the service returned the expected boolean.
''',file=test,anchor='  it("commits completion',count=100)
add('05-PRACTICE.md','Predict the ledger before running the test','''
Exercise one: submit completion for a valid lesson twice concurrently, then once after both requests finish. Predict newlyCompleted for all three results, the number of LessonCompletion rows, review-state count, and lesson XP events. Explain which database constraint chooses the winner.

Exercise two: throw after quest and achievement rewards have been calculated but before commit. List every table whose new rows must disappear. Explain why asserting only that LessonCompletion is absent would miss a helper that accidentally used the global Prisma client.

Exercise three: pass an empty lesson and then an unknown identifier. Identify where rejection occurs and which writes must not happen. Compare that failure with a duplicate completion for an eligible lesson: they have different meanings and should not share a broad catch-all success path.

Exercise four: inject a P2002 error for an unrelated unique key. Predict whether it should return newlyCompleted false. Inspect the model and target checks before answering. Then inject a recognized busy error twice and success on the third attempt; count transactions and describe which timestamp each attempt uses.

Exercise five: run the ordinary unit command without the ownership marker. Explain why skipped completion tests are the correct result and why that command alone cannot substantiate the transaction claims in this course.
''',file=test,anchor='  it("rolls back real completion',count=100)
add('06-SOLUTIONS-AND-REVIEW.md','Find escaped writes and overbroad retries','''
The concurrent pair has one true and one false newlyCompleted result; the later repeat is false. There is one completion, two review states for the fixture, and one lesson XP event. The nested quest and achievement rewards also occur once. The unique learner-and-lesson insertion gates all subsequent award work within the transaction.

After late failure, completion, review, XP, quest, and earned-achievement writes roll back, while the original progress fixture remains at zero XP. Checking the full set matters because an escaped helper write could survive while the completion itself correctly disappears. The fixture deliberately makes nested rewards eligible to expose that mistake.

An empty or missing lesson fails eligibility before the completion insert. It is not a harmless retry. An unrelated P2002 must propagate rather than masquerade as an already-completed lesson; the classifier checks the relevant model and key fields.

Two recognized contention failures followed by success use three transaction attempts and one captured now value. Further contention is surfaced after the bounded attempts. Arbitrary exceptions are not retried. Without the owned marker, the suite stays skipped and its destructive fixture hooks are not enabled.

During review, follow the client argument through every nested award helper, verify the unique gate precedes rewards, and compare stored rows after both success and failure. Browser behavior and lesson correctness require separate evidence and are not established by this persistence suite.
''',anchor='function isKnownSqliteBusy',count=100)
add('07-TRACE-LAB.md','Trace a failed award and a later retry','''
Begin with the fixture learner at zero XP and an eligible lesson containing two knowledge items. Enter the transaction and record the new completion row. Follow review seeding and note that both due times equal the captured now. Continue through the lesson award, daily quest reward, and eligible achievement reward, marking every write as belonging to tx.

At beforeCommit, throw the injected error. Cross out all newly created transactional rows. Query the database outside the rejected operation and compare the result with the original fixture: no completion, review, XP, quest, or earned-achievement rows survive, and progress remains zero.

Now retry without the injected failure. The unique completion insert succeeds because the prior transaction rolled back. The award collection commits once. Send one more identical request and follow the relevant unique-conflict branch to noAwardSummary. No additional award rows should appear.

For a review exercise, imagine that the achievement helper uses the global client while all other helpers use tx. Explain the resulting broken trace and which durable assertion catches it. Also consider SQLite lock contention caused by that escaped write: a timeout is not evidence that the outer transaction correctly contained the operation. The trace must account for both client ownership and final persisted state.
''',file=test,anchor='  it("makes concurrent/repeated',count=100)
add('VERIFICATION.md','Use the owned-database command as evidence','''
The completion integration command is node scripts/test-completion-local.mjs. It creates a temporary SQLite database, supplies an ownership marker, applies the schema, and runs the five completion cases. It validates the temporary path before cleanup. The exact accepted command and terminal result are appended below only after execution succeeds.

These cases cover empty and unknown eligibility, successful completion with deterministic review dates and nested rewards, late rollback, and concurrent plus repeated completion. Ordinary unit runs intentionally skip the guarded suite when the owned environment is absent. Skips must not be counted as passing database regressions or added to a distinct passing-test total.

The ordinary unit command passed twenty-three cases and skipped seventeen: the five separately verified completion cases and twelve C# runner cases. The accepted distinct total is twenty-eight when combined with the owned SQLite run. No C# runner verification is claimed for this change.

The first helper attempt stopped before schema setup because the installed Prisma package root resolved to a missing exported file. The helper now resolves prisma/package.json and invokes its declared build/index.js CLI. The next attempt reached the owned database but reported a generic schema-engine error. A diagnostic rerun enables RUST_LOG=info; this setting alone does not establish the underlying cause or prove any test passed.

The diagnostic run initialized SQLite and passed four cases, but the concurrent case exceeded Prisma's default five-second transaction timeout by 164 milliseconds. The fixture now injects its own PrismaClient with sixty-second transaction and acquisition limits, and its runner allows ninety seconds per case. Application defaults and durable-state assertions are unchanged. Accepted results therefore establish atomicity under those test limits, not a production latency bound or unlimited contention tolerance.

The transaction assertions use actual SQLite through Prisma. They do not establish PostgreSQL behavior, a remote code-runner result, browser UI recovery, or learning mastery. The helper's fixed fixture isolates award semantics from the application's regular learner database, which is never used for destructive test cleanup.

Type checking complements behavioral evidence by verifying the added client parameters and action result shape. It cannot prove atomicity by itself. Failed installation, generation, or test attempts remain in the campaign history rather than being rewritten as successes. Original snapshots and the source-linked exercises allow review of the transaction change without discarding earlier project work. The bounded contention policy remains a local retry strategy, not a guarantee that every overloaded environment will eventually succeed.
''',file='scripts/test-completion-local.mjs',count=100)
write_course('9d3b119f40a0',chapters,'Trace atomic lesson completion, nested rewards, deterministic review seeds, and real SQLite rollback.')
b=Path(__file__).resolve().parent.parent
(b/'specs/9d3b119f40a0.json').write_text(json.dumps({'changedFiles':[],'summary':['Made completion, review seeding, XP, quests, achievements and progress one transaction with a unique completion gate.','Propagated transaction clients and one captured time through nested award helpers, with selective bounded SQLite contention retries.','Added guarded temporary-SQLite regressions and nine source-based guide chapters.'],'limits':['SQLite tests do not exercise browsers or external code runners.','Ordinary unit runs skip the destructive completion suite unless the owned-database helper enables it.']},indent=2),encoding='utf-8')
