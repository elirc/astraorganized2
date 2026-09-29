from pathlib import Path
import json
from course_writer import write_course

api='services/Fulfil/Services/ReadApi.cs'
test='tests/Fulfil.Tests/RefundHealthTests.cs'
ui='src/lib/health.ts'
chapters={}
def add(name,title,body,file=test,anchor='',count=80):
    chapters[name]=(title,body,[(file,anchor,count)])

add('README.md','Make refund health actionable','''
Stockade's health view previously treated pending refunds as one undifferentiated group. That hides an operational distinction: some refunds remain eligible for worker retries, while others have reached the retry limit and need the existing authorized recovery action. The change exposes both counts and gives the latter group a concrete next step.

The API retains pendingRefunds and adds retryableRefunds and stuckRefunds. All three queries remain scoped to the authenticated account's merchant. A pending refund with fewer than twelve attempts is retryable; a pending refund with twelve or more attempts belongs in the recovery group. Successful refunds are excluded regardless of their historical attempt count.

The healthStats function converts these fields into visible labels and recovery guidance, and the panel renders that mapping. A small frontend regression protects the distinction and the zero-inventory-difference display. A new PostgreSQL test exercises the actual ReadApi health branch with two merchants and boundary values on both sides of twelve.

Follow the map from authenticated account to filtered counts, then use Concepts to calculate the boundary examples. The worked change separates query behavior from presentation. Practice and its separate solutions explore tenant isolation and retry eligibility. Verification explains exactly which local checks ran; neither provider refunds nor the operational retry workflow are executed by these tests. Existing recovery authorization remains the authority for taking action.
''')
add('01-CODEBASE-MAP.md','Follow account scope into the health panel','''
ReadApi.List resolves the authenticated account through Session.Account before handling the requested resource. The health branch uses that account's MerchantId in every operational count and in the reconciliation history query. Client-supplied display data does not choose the merchant whose refunds are counted.

The branch returns pendingRefunds for compatibility and the two more useful partitions. The worker's retry selection uses the same attempt boundary, while the existing order action remains responsible for explicitly retrying an exhausted refund. The dashboard guides a user toward that action instead of trying to perform it from a summary card.

On the frontend, src/lib/health.ts exports HealthStat and healthStats. The Panels component calls this mapping and renders label, value, and optional help. Keeping the mapping in a small pure function makes the semantics testable without starting a browser or importing the full panel tree.

RefundHealthTests creates two merchants, their owner accounts, orders, and refund fixtures in an isolated PostgreSQL database. It calls the real API function with authenticated claims and reads the returned result object. The helper script creates that database and enables the guarded test. An ordinary unit invocation skips this database case unless the owned-environment marker is present. Trace these boundaries independently when a count, label, or authorization result is wrong.
''',file=api,anchor='        if (resource == "health")',count=45)
add('02-CONCEPTS.md','Partition pending work at the retry boundary','''
Let pending refunds be the set of rows whose state is pending for one merchant. Divide that set at twelve attempts. Values zero through eleven belong to retryableRefunds. Values twelve and above belong to stuckRefunds. These subsets do not overlap and, for a stable database snapshot, their counts add to pendingRefunds.

State and attempt count both matter. A succeeded refund with twenty attempts is historical success, not pending recovery work. Testing only the attempt comparison would allow an implementation that accidentally includes successful rows. The fixture therefore includes successful examples above the threshold as well as pending examples at eleven and twelve.

Merchant scoping is another independent predicate. Correct arithmetic over the entire table would still leak another merchant's operational information. The regression gives the two merchants different expected counts so a missing scope predicate cannot accidentally pass with symmetric fixtures.

These counts are separate database queries, not an atomic reporting snapshot. A worker changing rows between queries can temporarily make their values reflect different instants. This improvement does not add a reporting transaction or promise snapshot consistency. Its contract is correct per-query classification and account scope. Similarly, a retryable count means eligible by this attempt rule; it is not proof that a provider will accept the next refund or that a worker is currently healthy.
''',file=api,anchor='        if (resource == "health")',count=35)
add('03-WORKED-CHANGE.md','Separate query classification from presentation','''
The backend change preserves the old pending total and introduces two explicit CountAsync predicates. Each includes MerchantId and pending state. The only difference between the new predicates is Attempts less than twelve versus greater than or equal to twelve. Keeping that difference visible makes the boundary straightforward to review against the worker policy.

The frontend no longer presents all pending refunds as though they require the same response. healthStats emits Retryable refunds from retryableRefunds and Refunds needing retry from stuckRefunds. The latter includes help directing the user to the order's authorized Retry refund action. This is guidance, not a new mutation endpoint or an authorization bypass.

The mapping preserves the existing stuck-payment, dead-letter, and inventory-difference entries. It checks for an actual reconciliation item before reading differences, so a recorded zero remains zero while absent history uses the existing unknown marker. The presentation regression covers that zero case alongside the two refund labels.

Review the API and mapping together. A correct backend field paired with an old UI key can silently show the wrong number. Conversely, changing a label without changing the underlying query would preserve the operational confusion. The tests exercise these two responsibilities separately, and their combined evidence does not imply a browser click or provider refund was performed.
''',file=ui,count=100)
add('04-TESTING-AND-DEBUGGING.md','Use asymmetric merchant fixtures','''
The PostgreSQL fixture seeds merchant A with pending attempt counts zero, eleven, twelve, and thirteen, plus a succeeded refund at twenty. It expects four pending, two retryable, and two requiring recovery. Merchant B has pending eleven and twelve plus succeeded twelve, producing two, one, and one. Different totals make cross-merchant counting visible.

The test creates owner accounts and orders because refunds participate in real foreign-key relationships. EnsureCreated builds the model in a fresh helper-owned database. The actual ReadApi.List method resolves claims through the application's session logic and executes its EF queries against PostgreSQL. This is not an EF in-memory substitute or a fake list returned by a repository mock.

After both successful reads, the test combines owner A's account identifier with merchant B's claim. The account lookup must reject that mismatched identity with DomainError. This checks the binding that produces the query scope; it does not replace broader authentication and role-policy tests.

If the test is skipped, inspect the helper invocation and ownership marker before claiming database coverage. If seeding fails, inspect required relationships and constraints. If counts fail, compare state, attempt threshold, and merchant predicates independently. The frontend test can diagnose mapping mistakes without a database, but cannot establish query isolation on its own.
''',anchor='public class RefundHealthTests',count=100)
add('05-PRACTICE.md','Calculate counts before changing code','''
Exercise one: for merchant A, classify pending refunds with attempt counts zero, eleven, twelve, and thirteen. Then add a succeeded refund at twenty. Predict all three API counts and the two visible refund cards. State why the successful row changes none of those counts.

Exercise two: give merchant B one pending refund at eleven and one at twelve. Remove MerchantId from only the stuckRefunds query in a disposable copy. Predict the incorrect value merchant A would see and identify which assertion detects it. Restore the predicate before accepting any test result.

Exercise three: change the comparison from less than twelve to less than or equal to twelve while leaving the recovery predicate unchanged. Explain why a refund at twelve appears in both groups. Describe the smallest boundary fixture that catches this overlap without relying on a large production dataset.

Exercise four: combine an account identifier from one merchant with another merchant claim. Predict whether the health query should execute and which existing identity lookup is responsible for the answer. Avoid assuming that merely possessing two syntactically valid identifiers grants access.

Exercise five: a refund succeeds between the three count queries. Explain why the returned total and partition counts may temporarily disagree even though each predicate is correct. Propose the extra reporting contract needed before introducing a transaction, and distinguish that proposal from the bounded change implemented here.
''',anchor='        db.Refunds.AddRange(',count=65)
add('06-SOLUTIONS-AND-REVIEW.md','Check the arithmetic and the authority','''
Merchant A has four pending refunds: two below twelve and two at or above twelve. The succeeded row at twenty is excluded because all refund-health queries require pending state. The frontend therefore shows two retryable refunds and two needing retry guidance.

Removing merchant scope from the recovery query would include merchant B's pending refund at twelve, yielding three for A. The asymmetric fixture detects this directly. Symmetric one-row fixtures could conceal some query mistakes, so distinct expected totals are deliberate test data rather than decoration.

Using less than or equal to twelve for eligibility overlaps the greater-than-or-equal recovery group. A single pending refund with exactly twelve attempts exposes the error, but the full fixture also protects lower and higher values and state exclusion. The correct boundary divides the set without overlap when observed at one stable instant.

The mismatched claims fail account resolution and must not produce a health result. Authority comes from the account-and-merchant binding, not from a caller's chosen display filter. Recovery still requires the existing authorized order action.

Separate queries can observe different instants while a worker updates state. Snapshot-consistent reporting would require an explicit additional design decision, such as a suitable transaction or combined query. The present tests establish predicate behavior and isolation with stable fixtures; they do not establish an atomic dashboard snapshot, provider success, worker liveness, or browser interaction. Keep these distinctions in review summaries.
''',anchor='        var a = await ReadHealth',count=70)
add('07-TRACE-LAB.md','Trace one exhausted refund to its label','''
Start with merchant A's authenticated owner and a pending refund whose attempt count is twelve. Follow Session.Account to the resolved merchant identifier. Enter the health branch and evaluate each refund predicate against that row. It contributes one to pendingRefunds, zero to retryableRefunds, and one to stuckRefunds.

Pass the returned object into healthStats. Locate the card whose value reads stuckRefunds and record its label and help text. The card directs the operator to an order action; it does not submit that action itself. Mark that separation on your trace so a summary view is not mistaken for a recovery command.

Repeat with the same row at eleven attempts. Its contribution moves to the retryable group. Then change state to succeeded while leaving attempts at twelve. It contributes to neither pending group. Finally, switch to merchant B's authenticated owner and confirm A's row contributes nothing to B's counts.

For a debugging exercise, replace the returned recovery field with the old pending total only in a local fixture and run the presentation assertion. Explain which part of the visible behavior changes and why a backend-only test would not detect the mapping error. Restore the fixture afterward. This trace connects identity, query classification, and presentation without assuming that a live payment provider or browser session participated in the check.
''',file=ui,count=100)
add('VERIFICATION.md','Distinguish database coverage from provider execution','''
The backend helper completed twenty-eight tests with no failures or skips. Its TRX records the new merchant-isolation case alongside the existing Fulfil suite. The helper-owned environment marker ensured the PostgreSQL health test ran instead of being skipped. The accepted frontend checks, when appended below, identify their own exact commands and outcomes.

The new database case uses PostgreSQL and actual EF queries through ReadApi.List. It covers pending-state filtering, attempt values on both sides of twelve, distinct merchant totals, and rejection of mismatched account and merchant claims. It calls the API function directly, so it does not certify HTTP routing, cookies, or browser rendering.

The frontend regression calls healthStats with a local object. It checks the two refund labels, recovery guidance, and preservation of a zero inventory-difference value. That is presentation-mapping evidence, not a screenshot or a successful click through the order workflow. Type checking verifies the integration of the mapping into the existing panel source.

No real refund, external provider call, deployment, or production data mutation is part of this acceptance scope. Counts remain separate reads and do not promise an atomic reporting snapshot under concurrent worker updates. Original snapshots and recorded commands accompany the changed source. Earlier captured backend checks remain historical evidence; the fresh twenty-eight-case run is the evidence for the newly added database test, and repeated cases are not counted twice.
''',file='scripts/test-refund-health.py',count=100)
write_course('37844e1ec56d',chapters,'Follow merchant-scoped refund health, retry boundaries, presentation guidance, and PostgreSQL regression evidence.')
b=Path(__file__).resolve().parent.parent
(b/'specs/37844e1ec56d.json').write_text(json.dumps({'changedFiles':[],'summary':['Separated pending refunds into retryable and exhausted groups while retaining merchant-scoped totals.','Displayed distinct operational counts and guidance toward the authorized order recovery action.','Added a real PostgreSQL merchant/boundary regression, frontend mapping coverage, and nine source-based guide chapters.'],'limits':['Health counts are separate reads, not an atomic reporting snapshot.','Database tests call the API function directly; frontend tests cover mapping, not browser interaction or provider refunds.']},indent=2),encoding='utf-8')
