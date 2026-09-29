# buildevent approved change

Make paid checkout retry-safe at the local/provider seam and make check-in atomic and event-scoped. Checkout validates ownership, pending state, expiry, and amount before provider calls; uses a stable per-order provider idempotency key; and conditionally persists the returned payment-intent id. Check-in binds the QR ticket to the URL event and changes VALID to CHECKED_IN with a one-winner conditional update, returning current check-in metadata to a losing repeat.

Unit tests use Prisma and Stripe fakes. They demonstrate application behavior and simulated provider idempotency, not a claim about actual Stripe exactly-once delivery. Verification: targeted API tests, the API suite, typecheck, and lint.
