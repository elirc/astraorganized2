# Astra1 approved plan

The incident-to-repair workflow already verifies eligibility, checklist order, fresh telemetry, successful completion, and idempotent repetition. The missing evidence is a late failure after completion has begun mutating inventory, crew, work-order, incident, audit, and postmortem rows.

Add a real `helios_test` PostgreSQL regression in `tests/integration/repair.test.ts`. A test-owned temporary trigger will reject the postmortem insert. The test will capture the exact pre-existing audit baseline, invoke `complete_repair`, and assert rollback leaves the work order verifying, incident acknowledged, crew unavailable, reservation intact, postmortem absent, audit count unchanged, and command receipt absent. Cleanup runs in `finally`. Removing the failpoint and retrying the same command id must create exactly one completion, consumption, resolution, receipt, and postmortem. Application code changes only if this exposes a defect.

Verification follows `AGENTS.md`: targeted real-PostgreSQL integration, `npm run check`, relevant API smoke, and the repair browser workflow. The execution record will report actual evidence and limitations. No original database or external service is used.
