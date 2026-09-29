# Cookie boundary testing

This guide follows the z9 portal code in the linked source files. Begin at the request boundary and identify the trusted actor before reading any business collection. A browser cookie is an attacker controlled input, so a value that contains a user identifier must never be treated as proof of identity. The implementation creates a random token and keeps the user identifier in a server side map with an expiry. Each request looks up the token, rejects unknown or expired entries, and resolves the current user again. Logout removes the token before expiring the browser cookie. This separates authentication material from profile data and makes role changes visible on the next request.

Read the implementation and then run the focused test file. Change one invariant at a time: forge a token, expire a valid token, remove a user, and replay a logged out token. The expected result is null or a 401 response, never another user session. For dashboard work construct an administrator and a client actor, then compare the aggregates. The administrator can see operational totals. The client receives only records whose client id belongs to the server side membership list. Projects are filtered through those clients, and invoices, proposals, and time entries cannot reintroduce foreign records. A client role has no time permission, so the explicit zero summary is a stable redacted contract rather than a leaked total. Unknown roles fail closed.

A useful review question is where an identifier becomes trusted. The route obtains the session, checks permission, and passes the session object to the service. The service does not accept a client id from query parameters and does not infer broad access from every value other than CLIENT. This is a small but critical distinction: authorization is a positive allowlist of known roles and known memberships. Keep the exact original snapshot beside the changed file so a reviewer can inspect the before and after behavior. The tests use a mocked Next cookie store and the real session functions; they do not claim a database or multi instance deployment. Seed passwords remain demo fixtures and must not be copied into production.

## Exercise

Trace one request from cookie parsing through the service result. Write down the token, user id, role, allowed client ids, allowed project ids, and the final fields. Then alter the input to use a forged payload or a foreign invoice and predict the result before running the test. Confirm that the prediction matches the regression suite and record the exact command and exit code in the delivery evidence. This exercise is intentionally small enough to repeat after a refactor and specific enough to catch an accidental broad query.

## Sources

- [Session implementation](snapshots/src__lib__auth__session.ts.original)
- [Dashboard implementation](../src/modules/dashboard/service.ts)
- [Source plan](../../../checks/batch-luna-astra-50-20260912/80b4407b2971-plan.md)

