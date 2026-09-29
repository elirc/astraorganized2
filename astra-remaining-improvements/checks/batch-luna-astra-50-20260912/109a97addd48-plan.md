# Astra implementation plan: ww37 Inventory Reservation

Canonical: `_Organized Desktop/05 Numbered Experiments/ww37`; ID `109a97addd48`. Source inspected directly. No applicable AGENTS.md or CLAUDE.md found in project or checked ancestors. Use shared staging/baseline helper before editing.

## Confirmed defects

`inventoryService.updateItem` constructs a patch containing all four optional keys, including values of `undefined`. The repository spreads that patch over the existing item. A rename-only request therefore erases SKU, unit and reorder point. The same unfiltered spread exists in repository update methods; distinguish omitted fields from intentional clearing instead of globally dropping undefined where a caller uses it to clear `clearedAt`.

Reservation creation, release and stock adjustment read a cloned item, await, then write a stale calculated value. Concurrent holds can oversubscribe stock or lose increments; simultaneous release can subtract twice or race with a hold. Sequential tests cannot prove concurrency safety. Storage is in-memory and resets on process restart. Existing comments already identify the missing transaction boundary.

## Implement

1. Correct item PATCH omission semantics with a precise field allowlist that includes only supplied values; test name-only and reorder-point zero updates, empty/unknown/invalid bodies and direct service validation. Preserve immutable IDs and stock fields in metadata updates.
2. Add a repository-owned serialized mutation boundary used by all relevant service mutation sequences on that repository instance (including alerts), or implement equivalent atomic domain operations. Keep one owner for the boundary to avoid nested lock deadlocks. Define failure behavior explicitly: if claiming rollback, stage changes and restore on callback failure with tests; a mutex alone only serializes and does not roll back. Do not call this a database/distributed transaction.
3. Validate direct service input before stock arithmetic and writes. Retain route authorization and intended role behavior. Ensure available stock stays nonnegative, reservations agree with reserved quantities, and duplicate releases reject.
4. Make the existing four Node tests actually run TypeScript and aliases on Node 22, add a finite test command/typecheck and functional lint configuration/lockfile. Fix only relevant startup/build blockers; avoid broad upgrades.
5. Add deterministic concurrent tests using real in-memory repository factories: two holds exceeding availability allow one; sufficient holds preserve sum; double release has one success; hold versus stock decrement cannot violate reserved <= onHand. Verify rejected operations preserve state, queue recovers after rejection, and alert state corresponds to final stock without duplicate open alerts. Include same-repository distinct service instances so a service-local lock cannot falsely pass.

## Course and handoff

Nine prescribed learning chapters (~4,000 substantive words) with exact source snapshots, CRUD request trace, partial-update examples, concurrency interleaving tables, debugging, complete runnable practice/solution pairs and a clear in-memory persistence limitation. Record actual tests/typecheck/lint/build terminal JSON/log evidence. Root owns final evidence review and canonical delivery; Luna stages only. Keep any larger database migration as a documented extension, not fabricated implemented behavior.
