# Astra early review: Master2

Pending final freeze. Read new payment service/routes/auth/error-handler and six service tests. Correct tenant predicates, permission guard, event/payload identity, serializable transaction and late-failure protection present.

Required: reset mock implementations with void beforeEach and restore transaction callback after reset. Test actual Express route per plan, same-tenant changed payload, missing invoice, malformed JSON/body, legitimate failed payment. Successful retry after failure must clear stale failureCode/message. Exhausted recognized Prisma contention currently raw-rethrows ->500; final claim_conflict line unreachable. Use explicit409 for supported contention. Global error handler changed expected generic client failures from other routes to500; classify those deliberately and sanitize readiness endpoint if claiming whole API errors safe. No realPG concurrency proof; fake tx just invokes callback.
