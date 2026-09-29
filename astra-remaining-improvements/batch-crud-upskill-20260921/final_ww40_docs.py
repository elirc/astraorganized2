from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/7a06d436fe48/astraupskill'
docs={
'README.md':'''# Job posting review workshop

Study [createJobPostingService](../src/services/jobPostingService.ts) through a portable [five-case runtime lab](../tests/job-posting-service-runtime.test.mjs). The existing service submits employer postings, scopes employer detail reads, and approves or rejects reviewable postings. Production source is unchanged.

The learning sequence combines payload prediction, state matrices, failure injection and review questions. Begin with SUBMITTED and FLAGGED: both permit approval or rejection. Then compare APPROVED, REJECTED and missing records. Finally inspect the gap between a review write and its audit call. Tests execute the real ApiError and service while adapting persistence; they do not certify route authorization, database isolation or audit durability.''',
'01-CODEBASE-MAP.md':'''# Follow the service boundary

submitEmployerJobPosting builds an explicit repository payload. organizationId and submittedById come from the actor, while title, description, location, employment type and salary fields come from input. It audits the returned id with JOB_POSTING_SUBMITTED.

approveJobPosting and rejectJobPosting first call findById, reject missing records404 and reject states outside the reviewableStatuses Set409. updateReview then receives reviewer id, target status and a null or supplied rejection reason. Audit follows the update. getEmployerJobPosting instead calls findByIdForOrganization with both identifiers. The service receives trusted actor context but does not itself assert reviewer role; route guards must be reviewed separately. All these persistence calls are distinct adapter operations in the lab.''',
'02-CONCEPTS.md':'''# State eligibility differs from authorization

A posting can be reviewable without every caller being authorized to review it. The service's SUBMITTED/FLAGGED Set controls lifecycle eligibility. It does not check reviewer.role. Passing a MODERATOR fixture therefore does not demonstrate authentication or role enforcement.

Submission ownership is another boundary: the service explicitly derives organization and submitter fields from the actor instead of copying arbitrary input keys. A tenant-scoped detail read forwards the organization to the repository; only a repository or database test can establish actual filtering.

Update then audit is not an atomic transaction in this service. If audit fails, a review write may already have occurred. The failure lab observes that ordering without simulating rollback. This distinction matters for retry policy and operational history.''',
'03-WORKED-CHANGE.md':'''# Worked approval and rejection

Take job-1 in FLAGGED with reviewer-1. Approval sends status APPROVED, reviewedById reviewer-1 and rejectionReason null. Rejection sends REJECTED and the supplied reason. Both audit the prior FLAGGED state after the repository returns.

The runtime addition verifies both decisions from both permitted states. It also exercises actor-derived submission scope, employer detail arguments and error propagation. No new parallel policy module is introduced: the actual service owns the decisions. Compare [the baseline snapshot](snapshots/jobPostingService.ts.original.txt) with [the test](../tests/job-posting-service-runtime.test.mjs). The fixture returns deterministic records so the assertions can concentrate on meaningful payloads and call order rather than merely checking that a promise exists.''',
'04-TESTING-AND-DEBUGGING.md':'''# Debug with operation prefixes

Run `node --experimental-vm-modules --test tests/job-posting-service-runtime.test.mjs`. Each fixture owns its calls and injected error. Missing or nonreviewable records should record find only. A successful decision records find, review, audit. A review error stops before audit; an audit error follows the attempted review.

Inspect actual ApiError.status rather than replacing the error class with an approximate double. For a submission scope failure, compare actor.organizationId with the create payload. For an employer detail failure, inspect both id and organization arguments. None of these checks runs Prisma queries. A follow-up integration test should verify real organization filtering and what persists when audit insertion fails.''',
'05-PRACTICE.md':'''# Exercises before answers

1. Submit a payload containing an untrusted organizationId. Identify the organization and submitter values sent to persistence.
2. Build a matrix for SUBMITTED, FLAGGED, APPROVED, REJECTED and missing records against approve and reject.
3. Predict rejectionReason for approval and for rejection with Missing details.
4. Trace a detail request for job-1 in org-2 when the scoped repository returns null.
5. Inject an error at review, then at audit. Distinguish attempted operations from persisted records.

For a design review, locate the route guard that should authorize moderation. Propose an expected-status update predicate and a transaction or reconciliation strategy for review/audit consistency. Label these proposals as future work rather than guarantees of this service lab.''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Answers and assessment

Submission derives org-1 and reviewer-1 from the actor even if an extra organizationId appears in the input object. SUBMITTED and FLAGGED allow both decisions; APPROVED and REJECTED yield409, while missing yields404. Approval clears rejectionReason to null; rejection forwards Missing details.

The employer detail call forwards job-1/org-2 and maps a missing scoped result to404. Review failure preserves the injected error without audit. Audit failure also propagates, after the review attempt. Grade answers on exact fields, real status codes and operation prefixes. Do not award authorization or rollback credit: the service does not check reviewer role or wrap review and audit together. Those require separate route and persistence verification.''',
'07-TRACE-LAB.md':'''# Trace the decision matrix

| Input | Calls | Outcome |
|---|---|---|
| Submission | create, audit | created posting |
| FLAGGED approval | find, review, audit | APPROVED |
| SUBMITTED rejection | find, review, audit | REJECTED |
| APPROVED review | find |409 |
| Missing review | find |404 |
| Review failure | find, review | original error |
| Audit failure | find, review, audit | original error |

Annotate each review payload with actor id and rejection reason. Then draw a separate employer detail trace containing organization scope. The table describes service calls through adapters; it does not show committed rows. Extend it with database observations before claiming atomicity or concurrent-review protection.''',
'VERIFICATION.md':'''# Verification and limits

Run `node --experimental-vm-modules --test tests/job-posting-service-runtime.test.mjs`. Five cases cover actor-derived submission fields, the two-by-two review success matrix, missing/nonreviewable refusals, employer detail scoping arguments and injected review/audit failures. The actual service and ApiError execute; repository and audit persistence are adapters.

No Next route authentication, Prisma query, database constraint, transaction or concurrent reviewer ran. A role on a test actor is not evidence of role enforcement. The service reads status before separate update/audit calls and has no enclosing transaction. Production source remains unchanged; the delivered improvement is a focused executable lab and source-specific teaching material. Provider tests should address audit failure and stale review state separately.'''
}
for name,t in docs.items():(P/name).write_text(t+'\n',encoding='utf-8')
