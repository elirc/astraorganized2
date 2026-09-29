# Before and after

Before, the where clause contained only environment id, while createDeployment received the submitted application id.

After, where includes environment id and application id; include and all later checks remain unchanged.

The mismatch fixture records the predicate and zero service calls; matching fixtures preserve actor, IDs, 201, and 423.

Source anchors are app/api/deployments/route.js, components/platform-dashboard.jsx, lib/platform-service.js, tests/runtime-deployment-ownership.test.mjs, tests/helpers/load-typescript.mjs, and astr aupskill/snapshots/app-api-deployments-route.js.before. The route?s environment lookup is the ownership boundary; getTeamRole and canPerform are authorization boundaries; deployLocked and deployFrozen are state boundaries. A useful review table is: relationship mismatch | lookup null | later checks skipped | create zero | 404; owned open | row | policy passes | create once | 201; owned locked | row | lock fails | create zero | 423. These tests execute production route control flow with explicit contracts. They do not execute database SQL or prove transaction isolation. A follow-up integration should POST through the running application with two applications and inspect deployment and audit rows.

Exercises for Before and after: predict the Prisma where object and side-effect count before running the command. Then inspect the exact source and snapshot. Answer: ownership must be established by the compound lookup, and a mismatch must return before createDeployment. Separate source behavior from harness limits; do not call a mocked permission or service contract a live integration result.
 Preserve response compatibility and record numeric executed tests.
 Preserve response compatibility and record numeric executed tests.
 Preserve response compatibility and record numeric executed tests.
 Preserve response compatibility and record numeric executed tests.
