# gitjira-app approved change

Harden sprint assignment and completion at the project/state/concurrency boundary. Assignment accepts an optional `expectedUpdatedAt`, rejects completed destinations, performs a timestamp compare-and-swap, and advances `updatedAt` by at least one millisecond. The backlog UI supplies the timestamp and displays a rejected mutation. Completion validates its destination and performs the ACTIVE-state compare-and-swap, issue move, count, and persisted-sprint read in one transaction.

Regression coverage uses a helper-owned disposable PostgreSQL cluster and covers a valid assignment, authorization, stale competing assignment, invalid destination, cross-project completion, and duplicate completion. Verification: targeted API tests, the API suite, web tests, lint, and typecheck.
