from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/7dde79c7a4c0/astraupskill'
docs={
'README.md':'''# Issue creation workshop

Follow [issueService.createIssue](../src/services/issues/issueService.ts) from project permission through configuration checks to transactional writes. The new [runtime lab](../tests/issue-service-runtime.test.mjs) executes the existing service, real permission map, workflow helpers, custom-field validation and error classes. Production behavior is unchanged.

Begin with a prediction: where should an invalid assignee stop? Run the lab, compare call order, then try the custom-field and failure exercises. This course combines source mapping, concrete payload tracing, boundary tests and a review rubric. Repository and automation adapters make calls observable; they do not prove database rollback or worker delivery. Use the separate verification chapter when deciding what a passing result supports.''',
'01-CODEBASE-MAP.md':'''# Map the creation path

The service calls assertProjectPermission before getProjectSetup. The real permission helper reads organizationRole and projectRole, not a generic role field. Organization administrators can bypass project-role restrictions; an OBSERVER lacks issue:create.

Setup supplies workflow statuses and custom-field definitions. An assignee is checked through an organization/project-scoped member lookup. validateCustomFieldValues checks configured types and required values; requireInitialWorkflowStatus rejects a workflow without an initial status. These reads and checks occur before the transaction.

Inside the callback, sequence allocation precedes createIssue, optional custom values, createActivity and enqueueIssueEvent. Every persistence adapter receives the same tx object. The response contains issue id and the project-key/sequence combination, such as OPS-8.''',
'02-CONCEPTS.md':'''# Configuration is part of validation

An issue payload alone cannot determine whether a custom field is valid. The service uses the project's definitions, rejecting unknown field ids, missing required values, wrong primitive types and invalid select options. Similarly, the client does not choose the initial workflow status; project configuration supplies it.

Authorization and configuration validation answer different questions. OBSERVER refusal is403, missing workflow404, no initial status409 and invalid assignee/custom value400. Keeping these real errors visible teaches callers how to respond.

Grouping writes under a transaction is distinct from proving atomicity. The test observes client identity and call ordering. A database test must establish rollback and sequence allocation under contention. Pre-transaction membership and setup reads can become stale; the lab does not resolve that concurrency question.''',
'03-WORKED-CHANGE.md':'''# Worked lab addition

Use project OPS, actor user-1 and sequence8. Successful creation sends organizationId org-1, projectId project-1, workflowId wf-1, initial status todo and reporterId user-1 to the issue repository. Activity describes OPS-8, and automation receives ISSUE_CREATED with toStatusId todo. The response is `{id: "issue-8", key: "OPS-8"}`.

The new fixture records setup, tx, sequence, create, activity and event. Adding a valid required numeric custom field inserts custom persistence between create and activity. No separate invented validator was added to application code: the test loads the existing service implementation. The [snapshot](snapshots/issueService.ts.original.txt) preserves the reviewed baseline for future experiments.''',
'04-TESTING-AND-DEBUGGING.md':'''# Find the first unexpected call

Run `node --experimental-vm-modules --test tests/issue-service-runtime.test.mjs` from the project directory. If OBSERVER reaches setup, inspect actual project permission mapping. If a foreign assignee reaches tx, inspect the scoped member query and user-id comparison. If required points accepts a string, inspect the NUMBER branch of validateCustomFieldValues.

An activity failure should occur after attempted issue creation and before automation enqueue. The injected error must propagate unchanged. The fixture does not erase previous calls to imitate rollback; those calls are evidence of attempted operations only. To verify durability, inject a real activity insertion failure and read issue/custom rows from another database connection. To verify sequence safety, coordinate concurrent creates explicitly.''',
'05-PRACTICE.md':'''# Prediction exercises

1. Predict the exact create payload and returned key for OPS with sequence8.
2. Change projectRole from LEAD to OBSERVER while organizationRole remains ORG_MEMBER. Identify the first forbidden call and error status.
3. Supply an outsider assignee. Write the member lookup predicate and the operations that must remain absent.
4. Configure required numeric points. Compare omitted values, text three, an unknown field id and number3.
5. Remove the workflow's initial status. Explain why this differs from a missing workflow.
6. Make createActivity throw. Trace attempted writes and the absent automation event.

For the design exercise, propose a concurrent sequence-allocation test and a rollback test. State which guarantees each adds beyond the adapter-based lab before reading the solutions.''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Answers and review rubric

Creation uses the server-supplied workflow and initial status; the key is OPS-8. OBSERVER receives403 before setup. The outsider case receives400 after setup and a lookup containing org-1/project-1, before tx. Missing or mistyped required points and foreign field ids receive400; numeric3 reaches custom persistence. A missing workflow is404, while a workflow without an initial status is409.

Activity failure preserves the injected error after sequence and create attempts, with no event enqueue. Grade answers on scope ids, actual error classes, exact order and the distinction between attempted writes and committed rows. The service's transaction-client discipline is tested; database rollback, sequence uniqueness and automation execution are not. A strong review names that missing evidence without changing expectations to make a mock pass.''',
'07-TRACE-LAB.md':'''# Trace worksheet

| Case | Recorded prefix | Result |
|---|---|---|
| Normal create | setup, tx, sequence, create, activity, event | OPS-8 |
| OBSERVER | none |403 |
| Invalid assignee | setup, members |400 |
| Invalid custom value | setup |400 |
| No initial status | setup |409 |
| Activity failure | setup, tx, sequence, create, activity | injected error |

Annotate every row with actor, organization, project and issue identifiers. Mark setup and membership reads as outside tx. In the successful custom-field case, add a custom step before activity. Compare your worksheet with the test call arrays, then mark which facts came from real policy execution and which came from adapter returns. This prevents a trace diagram from implying unobserved database behavior.''',
'VERIFICATION.md':'''# Verification and limits

Command: `node --experimental-vm-modules --test tests/issue-service-runtime.test.mjs`. Five test cases execute actual createIssue, permission mapping, workflow helpers, custom-field validation and error classes. They cover exact success payloads, permission/configuration refusals, scoped assignee lookup, required/type/foreign-field validation and activity failure ordering.

Generated enum exports and JsonNull are adapted, as are repositories, transactions and automation persistence. Same-client assertions verify arguments, not Prisma commit or rollback. No route parsing, database visibility predicate, sequence contention or automation worker ran. Project setup and membership reads precede the transaction, so concurrent configuration changes remain outside this result. Production source is unchanged; the course and portable runtime lab are the delivered improvements.'''
}
for name,t in docs.items():(P/name).write_text(t+'\n',encoding='utf-8')
