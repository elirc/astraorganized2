# Astra5 approved plan

The worker stops retrying orders and refunds after twelve attempts. Operational health already reports exhausted orders as `stuckSagas`, but `pendingRefunds` combines retryable and exhausted refunds. An operator therefore cannot see which refunds require the existing authorized `refund.retry` recovery command.

Preserve payment and refund semantics while extending the health contract with retryable and exhausted refund counts, retaining the existing aggregate for compatibility. Show an actionable exhausted-refund label in the health panel that points to the existing recovery path. Add database-backed backend coverage for merchant isolation and the attempt 11/12 boundary, plus focused frontend coverage for the health mapping where the current test setup supports it. Preserve all existing Fable fixes and avoid provider calls.

Verification is `dotnet test tests/Fulfil.Tests`, `npm test`, and `npm run typecheck`; production/browser checks are coordinated separately because of shared resource limits. The learning trace follows pending refund, worker cap, scoped health, and authorized manual retry, and clearly labels the payment simulator limitation.
