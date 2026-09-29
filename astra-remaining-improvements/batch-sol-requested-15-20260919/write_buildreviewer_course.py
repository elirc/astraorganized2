from pathlib import Path
import json
from course_writer import write_course

service='apps/api/src/modules/publish/publish.service.ts'
test='apps/api/test/api.e2e.spec.ts'
chapters={}
def add(name,title,body,file=service,anchor='',count=85):
    chapters[name]=(title,body,[(file,anchor,count)])

add('README.md','Publish one review and preserve uncertain outcomes','''
ReviewDeck collects a local review session and publishes one batch to a code-host provider. The local database and the provider cannot share one transaction. A request can therefore create a remote review and fail before the local application records success. Blindly returning the session to DRAFT would make a duplicate publication possible.

This improvement claims DRAFT sessions atomically before provider work. Competing publishers cannot both pass a preliminary read and submit the same session. Definite pre-publication failures can release the claim; uncertain outcomes remain protected and return PUBLISH_AMBIGUOUS with reconciliation guidance. A successful result records the session and comment identifiers together locally.

The course follows that distinction through the service, the fake-provider integration tests, and the failure exercises. Read the map and concepts before tracing the worked change. Practice asks which outcomes are safe to retry, and the separate solutions explain the retained state. Verification records executed commands rather than assuming that source inspection proves runtime behavior.

The tests use a local SQLite database and a fake provider. They can prove the application's response to modeled failures, not GitHub's live behavior or exactly-once remote delivery. Human reconciliation remains necessary when the remote outcome is uncertain; no automatic reconciliation service is added here.
''',anchor='  async publish(')
add('01-CODEBASE-MAP.md','Locate the claim and the external boundary','''
PublishService receives a session identifier and the head SHA the user confirmed. It loads the local session, checks DRAFT, and attempts an updateMany restricted to that status. The update count decides whether this request owns the publication attempt. After claiming, it reloads the session and comments inside the protected error-handling block.

The GitHub service supplies the live pull-request head and creates the remote review. Local validation rejects empty submissions, head drift, and invalid self-review verdicts before createReview. The payload includes the captured commit, severity-prefixed comments, and a summary tally. reviewAttempted marks the point after which an unclassified failure may mean the provider accepted the request.

Local finalization runs in a Prisma transaction, storing PUBLISHED state and returned provider identifiers. The catch block classifies failures. markFailedCommentsAndRelease handles the modeled 422 rejection by annotating comments and releasing the claim in one transaction.

The integration suite starts the real Nest application and replaces only the provider factory with FakeProvider. Its SQLite database is recreated inside the staged project's test-data directory. Deferred provider promises control concurrency, and a test-owned SQLite trigger injects a recovery failure. These seams target different boundaries and should not be conflated with a fully mocked service.
''',anchor='    const claim =')
add('02-CONCEPTS.md','A failed request does not prove no remote effect','''
An atomic claim prevents two local callers from owning the same DRAFT session. It does not make the remote request transactional with SQLite. The session therefore needs an honest representation of uncertainty: PUBLISHING remains a retry gate when the application cannot establish whether publication happened.

Before createReview is attempted, a validation or head-check failure has no review-creation effect from this attempt. The service conditionally releases its claim. After the attempt begins, ordinary transport errors are ambiguous. A timeout can occur after the provider accepted the request, and local finalization can fail after a successful provider response. Both cases require reconciliation before another publication.

The adapter's definite rejection codes form a narrower category. Unauthorized, forbidden, and rate-limited responses release the claim. The modeled unprocessable rejection also records comment failure explanations. Its comment updates and release must commit together; otherwise the UI could display partially changed drafts while the claim has an unrelated state.

Conditional release prevents a stale recovery path from overwriting a state it no longer owns. If recovery itself fails, the original provider error remains visible and the claim stays conservative. This is controlled retry behavior, not a claim of exactly-once delivery across the network.
''',anchor='    } catch (e)')
add('03-WORKED-CHANGE.md','Move ownership into the write predicate','''
The initial DRAFT read remains useful for a clear error, but it cannot arbitrate concurrent requests. The new updateMany predicate performs that arbitration: only a row still in DRAFT changes to PUBLISHING. A zero count causes the caller to load current state and return SESSION_NOT_DRAFT before reaching the provider.

The winning request reloads data inside try, so even a failed reload enters recovery logic. It validates the live head and submission, builds the payload, marks reviewAttempted, and calls createReview. Success stores the session and all publishable comment results in one local transaction.

Failure handling now separates safe release from ambiguity. A generic error after the external attempt returns PUBLISH_AMBIGUOUS and leaves the existing state protected. A modeled 422 invokes transactional annotation plus conditional release. If that transaction cannot complete, its annotations roll back and the provider rejection is preserved rather than replaced by a secondary database error.

Read the claim, attempted flag, and catch branches as one protocol. Moving the flag after the awaited provider call would misclassify a transport failure. Moving the reload outside try would strand a claim without the intended recovery handling. Replacing updateMany with an unconditional update would reopen the concurrent-publication race.
''',anchor='    const rollback =')
add('04-TESTING-AND-DEBUGGING.md','Control the provider and fail a real transaction','''
The concurrent-publication regression holds createReview behind a promise after signaling that the first request arrived. While that request is suspended, the second publication must return SESSION_NOT_DRAFT. Releasing the first promise completes a modeled rejection and checks that the session can return to DRAFT without a created review.

The ambiguous-error regression injects a transport-style failure and checks PUBLISH_AMBIGUOUS, retained PUBLISHING, and rejection of an immediate retry. A separate case lets the fake provider record success, then makes local finalization fail. It verifies that the remote fixture recorded one review while the local claim still blocks another request.

The recovery-rollback regression uses SQLite itself. A temporary trigger rejects the PUBLISHING-to-DRAFT update during 422 handling. The preceding comment annotations must roll back with it. The test compares comment status and failure reason with the original rows, checks the retained claim, and removes the trigger in finally.

These tests model precise boundaries. They do not contact a live pull request. When debugging, inspect both provider fixture history and local database state; either alone can hide the split outcome. Preserve the original error when recovery fails, and keep test cleanup reliable so a failure-injection trigger cannot affect later cases.
''',file=test,anchor="    it('atomically claims")
add('05-PRACTICE.md','Decide when retry is safe','''
Exercise one: requests A and B read DRAFT, then A performs the conditional claim first. Predict B's update count, response code, and number of provider calls. Explain why a status check before an unconditional update is insufficient.

Exercise two: the live head differs from the confirmed SHA. Predict the session state after rejection and whether createReview was attempted. Contrast that with a connection failure after the request body was sent.

Exercise three: the provider returns a review identifier, but the local transaction fails. Draw the remote and local states separately. Explain why resetting DRAFT would invite duplicate publication even though the caller saw an error.

Exercise four: a modeled 422 identifies invalid comment anchors. Predict comment statuses and session state after successful recovery. Then inject a failure on the release statement after annotations have executed. State what must roll back and which error should reach the caller.

Exercise five: propose a reconciliation workflow for an ambiguous session. List the evidence needed to associate a remote review with the local attempt before allowing another publication. Keep that proposal separate from this change: the current service blocks unsafe retry and reports uncertainty, but does not automatically resolve it.
''',file=test,anchor="    it('keeps an ambiguous")
add('06-SOLUTIONS-AND-REVIEW.md','Preserve the uncertainty in the result','''
Request B changes zero rows after A claims the session and returns SESSION_NOT_DRAFT. It never reaches createReview. The database predicate owns the decision; both callers having previously observed DRAFT does not grant both permission to publish.

Head drift occurs before reviewAttempted is set, so the claim can return to DRAFT. A generic failure after the external attempt is ambiguous and keeps the retry gate. The error code communicates that the operator must inspect the pull request before trying again.

After provider success and local transaction failure, the remote fixture has one review while the local session remains PUBLISHING. Returning DRAFT would incorrectly imply that another call is safe. The service reports PUBLISH_AMBIGUOUS instead of inventing a clean rollback across two systems.

Successful 422 recovery marks matching comments FAILED and releases the session atomically. If release fails, the annotations roll back, PUBLISHING remains, and the original GITHUB_UNPROCESSABLE response survives. The trigger regression proves this local transaction property with SQLite.

A future reconciliation design needs reliable evidence of whether the remote effect exists and which attempt produced it. Simply retrying after a delay does not supply that evidence. During review, check ownership predicates, flag placement, error classification, and transaction boundaries before evaluating presentation wording or convenience retries.
''',anchor='  private async markFailedCommentsAndRelease(',count=100)
add('07-TRACE-LAB.md','Trace success followed by local failure','''
Begin with one DRAFT session and three publishable comments. Let request A claim PUBLISHING, reload the session, and pass the live-head check. Write down the payload commit and local comment identifiers before the provider call. At this point request B must already be unable to claim the session.

Let the fake provider append one created review and return its identifiers. Immediately fail the local finalization transaction. The provider history still contains that review, while the local database lacks the successful finalization. Follow the catch block with reviewAttempted true and no definite-rejection code. The response becomes PUBLISH_AMBIGUOUS.

Send a second publication request. It sees PUBLISHING and returns SESSION_NOT_DRAFT without adding another provider review. This final assertion connects the error classification to its practical purpose: an uncertain first result must not silently permit a duplicate external effect.

Repeat the trace with a 422 rejection and the release-failure trigger installed. No review is recorded by the fake provider; comment updates begin locally, but release aborts their transaction. Compare the comment rows before and after, then remove the trigger. Explain why retaining the original rejection and conservative claim is more accurate than claiming recovery succeeded. Neither trace proves the behavior of a live provider.
''',file=test,anchor="    it('keeps the claim")
add('VERIFICATION.md','Read local and simulated evidence separately','''
The recorded commands appended below are the acceptance evidence. Dependency installation, a generated Prisma client, or a source review alone does not establish passing tests. Failed attempts remain in the campaign history, and each accepted command must finish with exit zero before delivery.

The API integration suite runs the real Nest endpoints and a local SQLite database with FakeProvider replacing the code-host boundary. Its concurrency gate controls when createReview returns. Its transport and finalization failures model uncertain outcomes. The recovery trigger tests actual SQLite rollback of comment annotations and claim release.

Earlier Jest attempts stopped during SQLite schema setup. Direct CLI and standalone setup diagnostics succeeded; the subsequent API command includes RUST_LOG=info and records successful fixture creation. The precise cause of the earlier engine error was not established. The setup helper now invokes the installed Prisma CLI through Node, avoids shell-based npx resolution, and reports process-launch errors. A later regression run found that the simulated successful publication advanced the shared fake review-ID counter; its cleanup now restores that counter along with the fake review list before the existing publication assertions run.

Frontend and shared-package checks cover their own transformations and types. They must not be summarized as live GitHub publication or production validation. No external review was sent as part of this improvement, and no credentials or user repositories are needed for the modeled provider behavior.

Known limits include manual reconciliation for ambiguous sessions and dependence on the adapter's classification of definite rejection. A process crash can also leave a PUBLISHING session requiring investigation. This change deliberately retains that uncertainty instead of treating every failure as retryable. Original snapshots, source links, exercises, and separate solutions accompany the implementation so a reviewer can trace each claim to code and evidence. Human learning remains unassessed by these software checks.
''',file=test,anchor="    it('rolls back failed-comment annotations",count=85)
write_course('3b9c30ec3ce2',chapters,'Study publication ownership, uncertain provider outcomes, and transactional recovery regressions.')
b=Path(__file__).resolve().parent.parent
(b/'specs/3b9c30ec3ce2.json').write_text(json.dumps({'changedFiles':[],'summary':['Atomically claimed draft reviews before publication and blocked competing callers.','Preserved ambiguous provider/local-finalization outcomes as a retry gate; made rejection annotations and release transactional.','Added controlled provider and SQLite rollback regressions plus nine source-based guide chapters.'],'limits':['External publication is simulated with a fake provider; no live GitHub review or exactly-once guarantee is established.','Ambiguous or interrupted publications still require manual reconciliation.']},indent=2),encoding='utf-8')
