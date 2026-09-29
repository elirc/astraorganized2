from pathlib import Path
p=Path(__file__).resolve().parent.parent/'stage/2906d0b177f3/astraupskill'
chapters={
'README.md':'''# Deployment creation needs a matching parent

This lesson follows the POST handler in [deployments/route.js](../app/api/deployments/route.js). A deployment request names an application and an environment. Previously, the handler looked up the environment only by its id, checked permissions against that environment's application, then passed both submitted ids to the creation service. A caller could therefore submit an inconsistent parent-child pair.

The lookup now includes `applicationId` alongside the unique environment id. A mismatch uses the existing 404 branch before team-role lookup or deployment creation. Successful matching requests retain the permission checks, environment policy and deployment lock checks.

Use the chapters as a progression: trace the request, distinguish identity from authorization, inspect the worked diff, predict test outcomes, then design stronger database evidence. The [runtime suite](../tests/runtime-deployment-ownership.test.mjs) executes the real POST function with explicit adapters and three named cases. The [original snapshot](snapshots/app-api-deployments-route.js.before) makes the missing predicate visible.

The correction is limited to this POST boundary. Other creation callers, GET behavior and transactional audit consistency are unchanged. A passing route harness is useful evidence about argument flow and side-effect order; it is not a live Prisma, Next or database test.
''',
'01-CODEBASE-MAP.md':'''# Trace both ids to the write

The [POST route](../app/api/deployments/route.js) first loads the actor, reads JSON and validates the creation payload. It then loads an environment with its application and team. The corrected `where` object contains both submitted identifiers, so the returned environment is required to belong to the requested application.

Next, `getTeamRole` receives the actor id and the loaded application's team id. `canPerform` checks the deploy action; `canDeployToEnvironment` checks the role against the environment slug. Environment-level `deployLocked` and application-level `deployFrozen` can stop the request with 423. Only after those guards does `createDeployment` receive parsed fields and the actor id.

Read [platform-service.js](../lib/platform-service.js): it reads prior versions, creates the deployment and writes an audit entry. Those are separate operations. This patch does not add a transaction around that workflow or change version allocation.

The [dashboard](../components/platform-dashboard.jsx) already repairs invalid dependent selection when the selected application changes. That client behavior improves the normal UI path but cannot enforce a server invariant for forged or stale requests. Draw two traces, one through the browser and one calling POST directly. Both must converge on the same server-side parent-child predicate before creation is allowed.
''',
'02-CONCEPTS.md':'''# Existence is not relationship validity

Two valid identifiers do not necessarily form a valid pair. The environment may exist and the application may exist while the environment belongs to a different application. A database schema with separate foreign keys can enforce each reference without proving that relationship between them. The route must express the intended parent-child constraint or rely on an equivalent durable constraint.

Authorization is a separate question. Checking the actor against the environment's team does not validate an independently submitted application id. The corrected lookup binds the ids before the existing role and operational-policy checks run. It preserves the established 404 response for a missing eligible environment rather than adding a new error format.

A deployment lock is yet another condition. It can refuse an otherwise correctly scoped and authorized request. Combining all three ideas into a vague permission check makes it difficult to explain which condition failed and whether a write should have occurred.

The lookup remains a read followed by later writes. It does not prove protection against a concurrent relationship change, audit failure or repeated submission. Treat these as additional design questions requiring their own tests. The current change supplies a precise sequential invariant: the environment returned to this POST handler matches the requested application before creation is invoked.
''',
'03-WORKED-CHANGE.md':'''# Add the parent to the selector

The original selector was:

```js
where: { id: parsed.data.environmentId }
```

The revised selector is:

```js
where: {
  id: parsed.data.environmentId,
  applicationId: parsed.data.applicationId,
}
```

The relation include remains because the route needs the application's team and freeze state. Compare the [original](snapshots/app-api-deployments-route.js.before) and [current handler](../app/api/deployments/route.js). No permission branch, response status or creation-service argument is removed.

For a concrete example, submit application A with an environment owned by B. The old selector could return B's environment and continue using permissions for B while forwarding A to creation. The new selector produces no eligible environment, so the route returns 404 before role lookup and before the service is called.

With A and its own environment, the route proceeds as before: role checks, environment policy, locks, creation and 201. The focused success case checks the team id and permission-call arguments as well as the forwarded application, environment, version and actor. The lock case checks that a matching environment can still be refused before creation. This keeps the fix narrow while making its new condition observable.
''',
'04-TESTING-AND-DEBUGGING.md':'''# Make the fixture respect the selector

The [test](../tests/runtime-deployment-ownership.test.mjs) loads the actual route through a local VM loader. Explicit adapters stand in for NextResponse, Zod, Prisma, session lookup, RBAC and the platform service. The environment adapter evaluates both selector fields against its fixture row rather than blindly returning a row regardless of `where`.

Three cases run. The mismatch case provides a real fixture environment from application B but submits A, then checks 404, the compound predicate, no team or policy calls, and no creation. The matching case checks 201, exactly one creation, actor and identifier forwarding, version preservation and the actual arguments sent to the role-policy adapters. The lock case checks 423 with no creation after a matching lookup.

When debugging, inspect the predicate before the final status. A fixture that always returns null can mask the relationship rule unless the predicate is also asserted. A fixture that always returns a row can violate its own database contract and produce misleading failures.

Run `node --experimental-vm-modules --test tests/runtime-deployment-ownership.test.mjs`. The suite proves route control flow and adapter calls; it does not execute real RBAC decisions, Zod behavior, Prisma SQL, authentication middleware or concurrent writes. Permission-denial branches remain source-reviewed rather than executed by these three cases.
''',
'05-PRACTICE.md':'''# Predict refusals before designing more tests

1. Submit application A with an environment owned by B. Write the exact lookup object, response status and expected counts for team lookup, policy checks and creation. Identify which existing branch produces the response.
2. Submit a matching pair, an allowed role and no lock. List the fields forwarded to `createDeployment`, including the actor id. Explain why the team id comes from the loaded relationship rather than an independent request field.
3. Keep the pair valid but enable `deployLocked`. Predict whether permissions are consulted and whether creation occurs. Then consider application-level `deployFrozen` as a source-reading extension.
4. Propose a real database test with two applications and two environments. Define setup, the mismatched request and the persisted-row assertion. Explain what this would add beyond a mocked selector.
5. Consider a deployment created successfully followed by a failed audit write. Read the service and describe the partial state; do not assume the route's lookup guard makes that workflow atomic.

Grade your predictions before reading the next chapter. Each answer should name the owning layer and an observable effect. Avoid vague claims such as secure or transaction-safe when the actual evidence concerns a specific selector and three route branches.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Answers and a reviewer rubric

The mismatched selector contains the environment id and application A's id. No row satisfies both, so the existing environment-not-found branch returns 404. Team lookup, policy calls and creation remain zero. This is relationship validation before authorization, not a replacement for authorization.

A matching request reaches the team-role and deploy-policy checks. Creation receives parsed application and environment ids, optional version or commit fields, and `actorUserId` from the actor. The team id is taken from the loaded environment's application. A matching locked environment still reaches permission checks, then returns 423 before creation.

For the database extension, seed A and B, place one environment under each, submit A with B's environment and assert both the response and zero new deployment rows. The real database adds evidence about selector interpretation and persistence, which the current fixture cannot provide. For audit failure, the service's separate create and audit calls can leave a created deployment when the later call fails; no transaction was added here.

Award two points each for the compound selector, guard order, creation arguments, negative write assertions and evidence limits. Reject a review that removes the relation include or bypasses existing role checks. Also reject a claim that these three cases exercised permission denials or all creation callers; they did not.
''',
'07-TRACE-LAB.md':'''# Follow the first stopping condition

Use this table with the route source open. The same requested deployment can be refused for a relationship mismatch, a policy decision or a lock. Record the first stopping condition instead of collapsing every refusal into an authorization failure.

| Case | Environment lookup | Role/policy | Lock | Creation | Result |
|---|---|---|---|---|---|
| A with B's environment | No eligible row | Skipped | Skipped | None | 404 |
| Matching allowed pair | Matching row | Allowed by adapters | Open | Once | 201 |
| Matching locked pair | Matching row | Allowed by adapters | Active | None | 423 |
| Matching denied role | Matching row | Denied | Not reached | None | 403, source-reading exercise |

The first three rows correspond to executed cases. The last is a prediction from inspected source and is deliberately labeled separately. Replace the role adapter in a future test to turn that prediction into runtime evidence.

Next, draw the creation service as three boxes: read versions, insert deployment, write audit. Mark where a later failure could leave partial state. The selector improvement happens before these boxes and does not merge them into one transaction. A senior review connects the corrected invariant to these remaining boundaries without claiming more than the change and tests establish.
''',
'VERIFICATION.md':'''# Reproduce the accepted route checks

Run from the project root:

```text
node --experimental-vm-modules --test tests/runtime-deployment-ownership.test.mjs
```

The accepted capture is `crud-b03-astra-runtime`: three named cases pass. They execute the actual POST module with explicit NextResponse, parser, Prisma, session, RBAC and platform-service adapters. The mismatch case checks the compound selector and early refusal; success checks team/policy arguments and creation payload; lock refusal checks zero creation.

The original route is preserved in [the snapshot](snapshots/app-api-deployments-route.js.before). The changed production surface is the environment selector. The loader and runtime suite are local learning aids, and the captured log plus JSON summary are included in the delivered evidence.

No native Next server, real Zod validation, authentication middleware, Prisma SQL, database foreign key, real RBAC policy, audit persistence or concurrency test ran. The existing create/audit workflow is not made atomic, and other deployment callers and GET behavior remain unchanged. A permission-denial case is discussed as an exercise but is not counted among the three accepted runtime cases. Keep those distinctions in future reports so a passing focused suite is not mistaken for full application certification.
'''}
for name,body in chapters.items():
 (p/name).write_text(body,encoding='utf-8');print(name,len(body.split()))
