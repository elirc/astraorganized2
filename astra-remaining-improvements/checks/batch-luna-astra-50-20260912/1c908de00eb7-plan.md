# Astra implementation plan: Founder CRM Lite

Canonical: `_Organized Desktop/05 Numbered Experiments/z3/founder-crm-lite`; ID `1c908de00eb7`. Source inspected directly before assignment. No applicable AGENTS.md or CLAUDE.md found in project or checked ancestors. Stage with the shared helper before editing; preserve original source snapshots.

## Confirmed behavior and defects

The Next 15 application uses server actions, Zod schemas, a service layer and a JSON repository. `listLeads`, `getLeadDetail` and exports restrict sales representatives to owned leads. `globalSearch` currently returns matching leads without that restriction. Dashboard recent activity also reads global events before the eight-row limit, even when its other collections are owner scoped. `createTask` and `addNote` check only a write role, permitting a representative to attach content to another owner's record. The demo cookie selects a user; this is not production authentication.

`convertLead` reads outside the JSON write queue, then performs five separate writes. Two concurrent conversions can both pass the unconverted check, and an intermediate failure can leave only some related records. `updateJsonFile` already serializes updater callbacks per file within one process, but uses a direct file write, not a crash-safe database transaction.

## Implement

1. Introduce a small reusable, pure ownership policy for the existing entity types. Keep the existing analyst read-all and founder-admin behavior. Apply lead visibility consistently to search and activity; filter activity before limiting. For representative task/note creation, require an existing permitted target and own task ownership before the first write. Keep intentionally shared company listings explicit rather than silently changing unrelated UI contracts.
2. Convert a lead in one `updateCrmDatabase` callback: find current lead, authorize, check already converted, construct company/contact/deal/updated lead/activity and return one new database value. Do not reuse a stale read before the queue. Preserve fields and existing messages where practical. Describe this as one serialized in-process update, not cross-process or crash-safe transactionality.
3. Repair the unusable lint script with a real compatible setup, add a finite test command and lockfile, and resolve build/type errors needed to run the learning app. Avoid broad upgrades.
4. Test real service paths with a clearly isolated repository fixture or temporary JSON file. Mock bindings must be the exact modules consumed by the service; verify read/write interception if mocked. Include hidden lead search/activity; admin/analyst permitted reads; denied task/note writes leave all collections unchanged; valid owned writes retain expected activity; concurrent conversion creates exactly one linked company/contact/deal and one conversion event; retry rejects without writes; denied conversion leaves all collections unchanged.

## Teaching and verification

Nine prescribed `astraupskill` files, roughly 4,000 substantive words total, actual file maps and complete runnable examples. Match every practice exercise with a solution and explain authorization, serialization queues, stale reads, relationship integrity and failure boundaries. Preserve exact `.txt` source snapshots. Run finite tests, typecheck, full lint and production build with actual terminal JSON/log evidence via `run_project_check.py`. Never use original user data for test fixtures. Root reviews, normalizes the delivery spec and applies; Luna does not modify canonical folders or progress.
