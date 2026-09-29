# Astra source plan: buildasana

Canonical `_Organized Desktop/02 Build Projects/buildasana`, ID `e09d7ae4ffff`. ASP.NET layered work-management backend with three existing xUnit tests and a React/Vite frontend. Check applicable ancestor instructions before staging. Preserve existing course material.

## Confirmed defects and bounded repairs

CreateAutomationRuleAsync saves a rule without checking its project or action value. AutomationRule accepts undefined enum values, and MoveToStatus uses Enum.TryParse alone: numeric strings such as 999 can parse into undefined TaskStatus values. The execution loop records automation.executed even when no action matched. Validate the referenced project, name, trigger/action enums and supported status value before any rule or audit write. Preserve the existing valid CreateApproval behavior and document that its action value is not used. Execute and audit only an action that actually ran; do not silently label a skipped invalid rule as executed.

WorkTask.ChangeStatus accepts undefined enum values. Plan assigns priority/date/estimate and clears tags before enumerating/validating all tags, so a later invalid/null tag sequence can leave partial object changes. Validate and normalize candidate values first, then assign. Inspect the in-memory repository's reference behavior to distinguish real stored-state impact from isolated-object impact. Service validation should produce a deliberate client failure instead of an unhandled argument exception/500. Retain authorization before mutation and test that denied users add neither data nor audit records.

CreateGoalAsync also omits the owner existence check already present for project creation. Add the analogous reference check before saving. Do not invent a new business policy for negative metrics without evidence; focus on the confirmed missing relationship validation.

## Verification

Extend existing real repository/service tests: invalid project/action/trigger/status yields unchanged rules/tasks/audits; numeric unknown enums reject; a valid case-insensitive status action runs with the expected audit; CreateApproval still works; late invalid task-plan input preserves all fields; missing goal owner does not save. Include an HTTP boundary check for invalid enum/request input and the chosen failure status, preserving actual frontend wire contracts. Keep the in-memory and demo-header identity limitations explicit.

Run backend restore/build/full tests and frontend install/type/build/lint as applicable with actual terminal JSON/log/TRX evidence. Use declared framework/runtime honestly and document explicit roll-forward if native runtime is unavailable. No live external integration or production data is needed.

Nine detailed astraupskill guides (~4,000 substantive words) with exact source snapshots, validated-command flow, enum parsing pitfalls, reference integrity, audit accuracy, failure-before-mutation reasoning, complete runnable examples and matched exercises/solutions. Root reviews and applies canonical changes; Luna stages only.
