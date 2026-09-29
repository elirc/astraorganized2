# e20 review checkpoint

Original project: `_Organized Desktop/05 Numbered Experiments/e20`, id `6130d1be1f04`. Staged 18 files; six audited source/test files. No applicable AGENTS.md or .openai/hosting.json found in project or ancestors. All source, original tests, root README and compiler/package setup reviewed; original service 1717 lines, app 203, models 353, store 270, tests 296.

## Observed defects

- Memory-only state resets at restart. Multiple submit methods mutate status before validation or posting completes, allowing partial acceptance on errors.
- Eight seed users share plaintext password `password`; deterministic email-derived permanent tokens exist before login. Company defaults silently to first membership.
- Customer/supplier/item/warehouse/lead/project/task/timesheet APIs offer create/read but no ordinary update/delete or version comparison.
- Sales order reservation does not check available stock. Sales invoices can make stock negative; current item standard cost is used instead of accepted line facts.
- Stock and GL posting deduplicate by equal values, dropping legitimate identical lines within one document. Document-level idempotency must replace value-level suppression.
- Missing or weak reference checks: quotation parties, linked order/quote ownership/status/party, purchase-order approval on related receipt/invoice, payment party/direction/reference/status/overpayment, task assignee, timesheet user/task-project relationships, stock-entry warehouses.
- Zero purchase rates are replaced by fallback prices (`line.rate || item.purchasePrice`). Monetary fields allow arbitrary decimal precision and unbounded amounts. Currency accepts unsupported values.
- Converting a completed quotation can create another order. Draft invoices are included in aging/outstanding dashboard totals. Account classification uses substring heuristics.
- Comments/attachment access only checks company membership and broad roles, bypassing entity-specific read rights. Search/dashboard can expose cross-module data to roles denied the corresponding lists.
- Attachment URLs and bodies are insufficiently validated; CSV text can start with spreadsheet formula characters.
- Server binds all interfaces; tsconfig emits dist/src/server.js while npm start points to dist/server.js. No browser CRUD UI.

## Intended implementation direction (not yet delivered)

Preserve the ERP domain and original flow coverage. Introduce a bounded strictly validated SQLite aggregate and synchronous read/transaction boundary around API handlers, with validation/authorization inside the transaction and rollback before accepted state changes. Generate exclusive local setup credentials; hash passwords and session tokens; enforce expiry/current active user/company scope. Add versioned master-data and project CRUD with reference guards, plus a local browser workbench with retained drafts and company-aware caches. Fix concrete posting/reference/idempotency issues before broader UI. Add meaningful HTTP/SQLite/restart/concurrency/browser evidence and nine project-specific course files. Exact scope and APIs may be refined during implementation.

The sales lifecycle baseline test currently submits an order with no stock. Once stock integrity is enforced, add a legitimate purchase receipt fixture instead of preserving negative stock behavior. Other original ledger total assertions should remain meaningful.
