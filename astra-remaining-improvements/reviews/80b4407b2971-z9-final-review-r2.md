# z9 final source review — pending repair

The frozen source fixes the earlier bearer-token response disclosure in `authService.login` by returning only `{ user }`; opaque token state remains server-side. Permission lookup fails closed for unknown roles, and the dashboard route threads the re-resolved session into the service. The seven listed original snapshots are stored with `.ts.original` suffixes, so they are not compiled by the broad TypeScript include.

## Required final test repair

`tests/integration/auth-login-route.test.ts` mocks `authService.login` to return a token-free object. That proves the route serializes the mock shape, but it does not exercise the actual service contract that previously leaked `sessionId`. Add a test at the service boundary or configure the mock to return `{ sessionId: "opaque", user: ... }` and assert the route response strips it; retain a direct real-service assertion that `authService.login` never returns the token.

The dashboard suite remains a direct `dashboardService` test. Add a route-level test with mocked `requireSession` for an unknown runtime role and assert a controlled 403 response, plus the authenticated client projection. Existing seeded counts demonstrate the intended scope but do not explicitly assert a foreign invoice/proposal/project cannot contribute or exercise an unlinked user fixture. Add those assertions before acceptance.

The implementation itself aligns with the plan’s session lifecycle, membership filtering, time redaction, and fail-closed permission requirements. Acceptance remains pending until the route/service regression evidence is present and the final course reaches the stated substantive target.
