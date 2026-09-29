# Nethris review checkpoint

> Historical pre-implementation checkpoint. Nethris has since been delivered; see [DELIVERED.md](DELIVERED.md) for final changes, checks, file counts and cleanup limitations.

ID `71e7b036865c`; canonical `_Organized Desktop/01 Net Workspaces/.nethris`.
Stage: `astra-remaining-improvements/stage/71e7b036865c`.

The full collection goal remains active: **38/239 delivered; 201 remaining**. This turn made progress by delivering the Stripe-style billing workshop and starting Nethris. Nethris is **not delivered** and its original folder is untouched. No blocker exists.

## Completed review and baseline work

- Staged 75 original files with immutable baseline hashes. No AGENTS.md was found in this project or the checked `_Organized Desktop` / `01 Net Workspaces` ancestors. The nested `.nethris/client` contains only excluded dependency content and produced no additional source files in staging.
- Read the complete API Program, contracts, EF context, employee/department/job-role/user/PTO/enums models, seed logic, password/JWT helpers, complete React App, API client, TypeScript types, package/tooling metadata, original README, risk register and verification log.
- Also read `Domain/AuditLog.cs`, the full client CSS and `demoData.ts`; all application source has now been inspected. Broader existing course pages remain available for reference.
- Confirmed the configured JWT key is a 60-character development placeholder without printing it. Original seed passwords are the documented `Password123!` fixture value. No real secret was encountered.
- `preserve_originals.py` ran successfully once: all **75 text files** preserved byte-for-byte in stage `docs/original/<relative>.txt`. Do not rerun it after edits.
- `baseline-api-01`: original .NET 8 API builds, 0 warnings/errors, 169.49 seconds.
- `baseline-install-01`: locked frontend install passed, 69 packages, 278.37 seconds. Do not repeat this install without a dependency change.
- `baseline-web-01`: TypeScript/Vite build passed (exitCode 0 in its saved JSON), 109.89 seconds, Vite 5.4.21, 1,583 modules. The wrapper subsequently failed printing Unicode to a CP1252 console; the build itself succeeded. The wrapper now explicitly uses UTF-8. Do not rerun this baseline merely because the wrapper process returned 1.
- `baseline_probe.py` ran once against a fresh temporary database, using the original net8.0 assembly with `DOTNET_ROLL_FORWARD=Major`. Its server stopped and temporary database was removed. Do not rerun the one-shot probe; preserve its evidence.

## Observed runtime defects

`baseline-probe.json` records:

- Login returns numeric role `2`, while the TypeScript UI expects named role strings.
- Department, job-role, employee and org-chart reads return 200.
- PTO and audit reads return 500. Server logs confirm SQLite cannot ORDER BY the existing DateTimeOffset mapping.
- An HR session creates an employee with Admin account role: POST returns 201; the new account logs in with role `3`. This confirms privilege escalation through the PeopleOps employee route.
- A one-day 9,999-hour PTO request is accepted (201), demonstrating missing request/balance bounds.
- Direct HR approval returns 500 because EF issues UPDATE for a newly constructed PtoApproval with a supplied Guid instead of INSERT; it throws DbUpdateConcurrencyException. The balance remains 132 because SaveChanges rolls back. **Do not claim a negative balance was observed**. The source would subtract without a balance guard once the insertion bug is corrected.

Additional source findings to turn into regressions:

- Default-password account provisioning and a shared config signing key; JWT role/activity claims are not refreshed from current database state; sign-out only clears React state.
- No strict enum/string/body bounds, no record versions or durable operation receipts, unbounded employee/org reads and sparse errors.
- Department and job-role APIs are read-only; employee create/update APIs have no corresponding browser editor or deletion workflow.
- Manager chains can form cycles; self-manager update silently clears the relationship, and recursive org rendering has no cycle/depth guard.
- PTO has no pending edit/delete/cancel workflow, overlap/reservation checks, self-approval guard or explicit separation of manager/HR decisions.
- Directory DTOs expose everyone's PTO balance and job-role salary bands to any signed-in account.
- React login silently falls back to demo credentials after rejected or failed API login. Mutation handlers lack catch/finally and busy protection, synthesize local audit/approval data, and use `event.currentTarget` after await.
- Existing historical notes identify several of these issues. Do not confuse proposed fixes in those notes with implemented behavior.
- The historical claim of UI mojibake was not confirmed in the actual UTF-8 source: App.tsx contains three correct middle dots, no `U+00C2 U+00B7` sequence and no replacement characters. PowerShell's default decoding can make correct UTF-8 look broken. Do not make a speculative encoding edit.

## Working implementation direction

Keep this a **single-organization HRIS** using its existing EF Core relational models and visual vocabulary. Multi-tenant SaaS scaffolding is not necessary for this project. Preserve directory, profiles, org chart and PTO domain behavior while completing CRUD and making the real API authoritative.

1. Align API/test runtime and dependencies with installed .NET 10; current verified package candidates are EF/JWT 10.0.10, SQLitePCLRaw.bundle_e_sqlite3 2.1.13 and Swashbuckle.AspNetCore 10.2.3. Restore/build/audit before claiming compatibility; pin/lock the tested frontend tree.
2. Use a fresh default learning database path, schema identification and explicit refusal of unknown existing files. Do not silently migrate or overwrite an original nethris.db. There was no database file in the canonical API root during review. Consider UTC integer timestamps for SQL ordering and fixed integer quarter-hour/money storage with validation. Any legacy migration must be explicit and independently tested.
3. Replace shared default credentials with local bootstrap/generated private signing material. Current account activity/role must be rechecked server-side, including inside write transactions. Add revocable sessions/logout and Admin-only account grants; protect the last active Admin. Keep browser tokens in memory and remove automatic demo fallback.
4. Add versioned employee, department and job-role CRUD with uniqueness, reference, lead-department and manager-cycle checks. Archive/protect referenced records. Separate account grants from HR employee editing. Restrict balances/salary projections to the intended roles/subjects.
5. Define PTO transitions before coding: bounded quarter-hour quantities and dates, overlap/reservation checks, own pending edit/delete/cancel, no self-approval, manager/direct-report scope, an explicit HR finalization rule, atomic balance and approval writes. Explicitly add new approval entities (or configure assigned keys) so EF inserts them. Test retries/concurrent approvals and cancellation/refund policy if implemented.
6. Add strong ETags and transactionally stored operation receipts/audits for CRUD and PTO mutations; pagination/filtering before limits; bounded/cycle-safe org traversal; same-origin API proxy, loopback/body/JSON boundaries and meaningful errors.
7. Extend the existing React UI with real CRUD editors and authoritative refresh, stale-draft handling, exact retries, accessible labels, pending/error/empty states and role-correct controls. Preserve useful org/profile visuals; inspect source encoding before correcting alleged mojibake.
8. Add meaningful domain/SQLite/HTTP tests, packaged real-browser tests, local scripts, and nine detailed `astraupskill` guides. Mark historical documentation clearly. Then prepare/apply a finite manifest and refresh all reports.

These are working design choices, not extra user requirements. Keep the implementation coherent and bounded; do not grow this into payroll, legal policy, messaging, federated identity or a production HR product.

## Primary references already checked

- https://learn.microsoft.com/en-us/ef/core/providers/sqlite/limitations — DateTimeOffset/decimal query limitations; the observed ORDER BY exception matches this provider constraint.
- https://www.nuget.org/packages/Swashbuckle.AspNetCore/ — version 10.2.3 exists; runtime compatibility still needs local restore/build checks.

## Collection reports and prior delivery

`astradocs/PROJECT_CHANGES_AND_COMPLETION_REPORT.md` now has 38 entries, including Stripe. `NEW_PROJECTS_CHANGE_REPORT.md` and the `astrdocs` queue are refreshed and link-verified. Read-only audit: 1,981 files across 38 delivered projects, 0 missing, 37 families match their delivered hashes. The nine later JSProjectLearn differences remain preserved and explicitly noted in the report.

Stripe is finished: see `checks/stripe/DELIVERED.md`. Never regenerate its staged manifest or modify its delivered source as part of Nethris.

All baseline build/install/probe handles are terminal. No server is left running. No Nethris application implementation changes have been made yet; only its staged original snapshot and external review/evidence helpers were added.
