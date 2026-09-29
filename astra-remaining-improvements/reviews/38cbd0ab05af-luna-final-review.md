# Final review: w24 (`38cbd0ab05af`)

Decision: **REJECTED — do not deliver**.

The frozen source and manifest hashes are internally consistent for the seven declared changed source/test files (the only additional baseline delta is generated `tsconfig.tsbuildinfo`). The recorded Node test run, typecheck, lint, and build are successful. The implementation still misses required security behavior at real caller and service boundaries:

1. `src/app/api/feature-configs/[featureConfigId]/route.ts` resolves an actor with `requireActorWithPermission`, then calls `featureConfigService.getConfigDetail(featureConfigId)` without passing that actor. The service signature makes the actor optional and only suppresses the audit trail when it receives a `SUPPORT_VIEWER`. Therefore a support viewer can call the actual detail endpoint and receive the full `auditTrail`, despite the service-only test passing when an actor is supplied. The plan explicitly requires actor threading through routes/server callers and consistent audit projection.

2. `src/services/evaluation-service.ts` does not call `assertPermission` in `debugEvaluate`. The route guard protects the HTTP route, but a direct service caller can invoke the debug operation with an actor lacking `evaluations:debug`; this violates the required service-entry enforcement. The same plan requires all mutating/debug service entry points to enforce the permission map.

3. `src/lib/auth/permissions.ts` indexes `rolePermissions[role]` and immediately calls `.includes`. A runtime actor with an unknown role causes a `TypeError` instead of failing closed with the existing `FORBIDDEN:evaluations:debug`/permission error. The typed `PlatformRole` does not protect untrusted runtime actor data, and no test covers this boundary.

Required repair evidence: make `getConfigDetail` require and use the resolved actor, pass the actor from the detail route (and any other real caller), assert `evaluations:debug` at `debugEvaluate` service entry, make unknown roles return false/forbidden, and add route/service tests for support audit suppression, direct debug denial, and unknown-role fail-closed behavior. Re-freeze the complete changed-file manifest and rerun the focused tests plus typecheck/build before requesting review again.

Reviewed source: `stage/38cbd0ab05af`; canonical target was not modified. No delivery was applied.
