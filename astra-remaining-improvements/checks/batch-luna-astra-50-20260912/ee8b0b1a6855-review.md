# Astra review: MissionControl

Decision: **APPROVED for canonical delivery**.

The full Release run `checks/ee8b0b1a6855/tests-07.json` completed with exit zero: 113 unit tests and 26 API tests passed, with no failures or skips. Root independently read both TRX counters and the terminal process log. Application, test and dependency-lock hashes in the final run record match the staged files. No later executable changes were made.

## Source and regression findings

Task create and update open an EF-owned serializable SQLite transaction before allocating project ticket numbers. Update resolves a changed project through the workspace-filtered DbSet, validates fields and serializes collections before assigning tracked properties. It saves task, counter and activity changes, commits, then publishes events. Same-project updates retain the counter. Rejected late-field and cyclic-metadata updates are followed by a valid save in the same service scope to detect contaminated tracked state. Concurrent request tests cover both creates and mixed creates/moves.

The forward migration creates thirteen existing platform-entity tables missing from the original snapshot. Root inspected its additive Up operations; it does not suppress the pending-model warning or replace migrations with EnsureCreated. Fresh disposable test databases exercise it. Existing production-data migration was not tested.

Two lifecycle tests now use isolated hosts and databases. Their engine calls use the same isolated host as their fake LLM and HTTP client. Parallel API tests are disabled because fixtures modify process environment; disposal restores prior values. Test hosts remove background hosted services. The application scheduler opt-out only skips scheduler hosting, not ordinary webhook hosting. The security scan regression now calls the actual `/api/security-scan/text` route while retaining secret, injection and redaction assertions.

## Teaching review

Root corrected HTTP examples to the actual 422 mapping, replaced an inaccurate worked-code excerpt with the real preflight block, added the complete passing scoped-context regression, removed an unrelated comment-filter example, and repaired text encoding. Five original source snapshots were checked against immutable baseline hashes; two draft snapshots were replaced with exact originals. Raw test hashes remain preserved and the verification guide explains the documentation-only snapshot correction.

The course distinguishes database rollback from EF tracking, request-scoped concurrency from long-lived context caching, post-commit events from a durable outbox, and nullable assignment from an explicit clear operation. No real LLM, webhook destination, user database, deployment or browser workflow was exercised. These limits are recorded in the delivery specification and course.
