# Luna implementation and Astra review

Updated 2026-09-13 14:46 UTC.

Two Luna agents implement separate projects; an Astra agent reviews their plans, code, learning material and test evidence. Root applies reviewed deliveries sequentially and updates the shared reports.

**Collection: 74 of 239 eligible families delivered; 165 remain.**

## missioncontrol

- Task updates reject blank titles and validate project visibility within the current workspace before mutating tracked task state.
- Task creation and project reassignment allocate project ticket numbers inside an EF-owned serializable SQLite transaction; task/activity writes commit before event publication.
- Prevalidation and metadata serialization prevent rejected updates from contaminating later valid saves in the same scoped service; regression tests cover recovery and mixed concurrent create/move allocation.
- Add a forward EF migration for thirteen existing platform entities omitted from the original model snapshot, allowing the test API host to apply the complete schema without suppressing pending-model checks.
- Isolate the two lifecycle scenarios in disposable test hosts, disable parallel API tests that share process environment, correct the security-scan route, and provide an explicit scheduler opt-out.
- A nine-file learning course explains actual request paths, EF tracking versus database transactions, worked examples, debugging, progressive exercises and their solutions; original source snapshots and verification evidence are included.

**Learning:** 9 guides; 5,136 words. [Start the course](../../missioncontrol/astraupskill/README.md).

**Verification:** 139 tests passed. [Delivery evidence and limits](../astra-remaining-improvements/deliveries/ee8b0b1a6855.json).

[Astra review](../astra-remaining-improvements/checks/batch-luna-astra-20260912-02/ee8b0b1a6855-review.md).

## aiheartbeat

- Guard direct workspace store callers with own-property collection allowlisting and positive safe-integer IDs before SQLite saves or deletes, preserving existing HTTP/Zod validation.
- Add seeded rejection regressions and verify all three workspaces:505 tests, type checking and the Next webpack dashboard build pass.
- Add nine source-grounded learning guides with complete practice examples, an import/export design exercise, exact original snapshots and captured verification evidence.

**Learning:** 9 guides; 4,258 words. [Start the course](../../aiheartbeat/astraupskill/README.md).

**Verification:** 505 recorded checks passed. [Delivery evidence and limits](../astra-remaining-improvements/deliveries/9e1958f807df.json).

[Astra review](../astra-remaining-improvements/checks/batch-luna-astra-20260912-02/9e1958f807df-review.md).

[All completed projects](FINISHED_PROJECTS_SUMMARY.md) · [Full change report](PROJECT_CHANGES_AND_COMPLETION_REPORT.md).
