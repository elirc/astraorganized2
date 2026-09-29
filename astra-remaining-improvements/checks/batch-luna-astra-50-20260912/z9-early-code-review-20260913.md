# z9 early code review — 2026-09-13

Read-only review of the frozen candidate stage against `80b4407b2971-plan.md`.

## Concrete issue to fix

`POST /api/auth/login` returns the complete result of `authService.login`, and `createSession` includes `sessionId` in that result. Thus the opaque bearer token is exposed in the JSON response even though the cookie is `httpOnly`. Keep the token only in the server cookie/session actor; return a public user-shaped payload (or otherwise remove `sessionId`) and add a route/service regression asserting the login body cannot disclose it. The login page does not use `sessionId`.

## Coverage gaps before freeze

- `dashboard-overview.test.ts` is a direct service test, as the plan admits. Add route-level coverage for the actual `GET /api/dashboard/overview` caller: missing/forged cookie must be 401, an authenticated client must receive the scoped projection, and an unknown runtime role must fail closed at the route/service boundary.
- The current dashboard assertions use only the seeded state. They do not prove a client cannot receive a foreign client, project, invoice, or proposal contribution, nor do they exercise an unlinked user. Use a test-only state fixture/mutation or explicit second-client fixture and assert foreign IDs/counts/totals are absent. Include a mismatched invoice/project relationship so filtering is shown to use the invoice's client membership and project scope rather than incidental seed data.
- The service correctly filters client entities through `state.users[user.id].clientIds` and time through allowed project IDs, and returns zeroed time totals for clients. Preserve that contract in the panel/API type and test the absence of raw time-entry details.
- Session tests cover random token, forged token, expiry, logout replay, and missing user creation. Add assertion that the login response itself omits `sessionId`; add a missing-user re-resolution test after a session is created if the demo store can be changed. `getCurrentSession` should discard an orphaned session entry when user re-resolution fails (small lifecycle hygiene issue).

## Reviewed behavior that currently aligns

Opaque UUIDs are stored as `userId` records with expiry and are re-resolved on each read; unknown roles are rejected by dashboard service and permission lookup fails closed; the dashboard route passes the trusted session actor and asserts `dashboard.read` before aggregation. Admin/team broad views and client time redaction match the stated plan.

Do not accept/apply until the response-token disclosure is removed and the route/foreign-scope regressions are present in the final source and terminal evidence.
