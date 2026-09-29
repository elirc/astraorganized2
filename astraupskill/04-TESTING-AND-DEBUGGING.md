# Runtime method

Run the Node VM test. It evaluates the actual route and stubs NextResponse, parser, Prisma, session, RBAC, and service imports.

Debug predicate first, response second, and side-effect count third. Cross-realm objects use serialized comparisons.

Mutation answer: removing applicationId lets mismatch reach creation and fails predicate or zero-call assertions. No live Next or SQL claim.

Source anchors are app/api/deployments/route.js, components/platform-dashboard.jsx, lib/platform-service.js, tests/runtime-deployment-ownership.test.mjs, tests/helpers/load-typescript.mjs, and astr aupskill/snapshots/app-api-deployments-route.js.before. The route?s environment lookup is the ownership boundary; getTeamRole and canPerform are authorization boundaries; deployLocked and deployFrozen are state boundaries. A useful review table is: relationship mismatch | lookup null | later checks skipped | create zero | 404; owned open | row | policy passes | create once | 201; owned locked | row | lock fails | create zero | 423. These tests execute production route control flow with explicit contracts. They do not execute database SQL or prove transaction isolation. A follow-up integration should POST through the running application with two applications and inspect deployment and audit rows.

Exercises for Runtime method: predict the Prisma where object and side-effect count before running the command. Then inspect the exact source and snapshot. Answer: ownership must be established by the compound lookup, and a mismatch must return before createDeployment. Separate source behavior from harness limits; do not call a mocked permission or service contract a live integration result.
 Preserve response compatibility and record numeric executed tests.
 Preserve response compatibility and record numeric executed tests.
 Preserve response compatibility and record numeric executed tests.
