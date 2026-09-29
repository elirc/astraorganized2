from pathlib import Path
s=Path(__file__).resolve().parent/'stage/56044dcd81ce';d=s/'astraupskill'
docs={
'05-PRACTICE.md':'''# Extend one reliable vertical flow at a time

These are proposed exercises. None should be described as implemented until your branch includes code, a user flow and relevant evidence. Start with the smallest change, retain the existing tenant/concurrency tests and use the disposable database harness. A feature is complete when its failure behavior is understandable as well as its successful behavior.

## 1. Add a department filter

Extend the strict query schema with a bounded department string, add a tenant-scoped condition and connect a labeled UI control. Preserve the count/list transaction so total and rows describe the same filtered view. Reset pagination when the filter changes. Evidence: two tenants with the same department name remain isolated, empty departments behave deliberately and a late response from a previous filter cannot overwrite the current page.

## 2. Add a contact field end to end

Choose a non-sensitive field such as preferred display name. Define whether empty means absent or an intentionally blank label. Add a migration, input validation, response field, editor control and one read-after-update test. Existing records need a safe default or nullable representation. Test a stale update involving the new field; merely adding it to the form must not bypass the captured version.

## 3. Implement company maintenance

The delivered UI only selects active companies. Add company create/update/archive with its own version and audit events. Decide what archiving means for current workers. A concurrent worker create and company archive require a transaction/locking rule if your invariant forbids new assignments to an archived company. Test both operations racing in real PostgreSQL. Do not assume the current read-then-create company check covers a future company mutation API.

## 4. Add onboarding tasks

Use the existing plan/task models but implement a narrow task checklist first. Scope every plan and task through the actor's tenant and verify parent ownership. Decide whether completing all required tasks permits activation automatically or merely enables an explicit action. If activation and completion are coupled, commit the relevant changes and audit together. Test a foreign plan ID and two people completing the same task simultaneously.

## 5. Make retryable creation explicit

The current create endpoint has no idempotency key. Design a per-tenant request key, normalized payload fingerprint and retained response. A repeated key with identical content should return the original outcome; a changed payload should conflict. Commit the receipt with worker creation and audit. Simulate a client losing the response after commit, then retrying. Email uniqueness alone is insufficient because it does not prove that an existing worker belongs to that request.

For a larger capstone, introduce a notification outbox and a worker self-service role. Keep them separate changes: ownership policy and delivery reliability require different tests. Present a short design before implementation containing the invariant, database constraint, transaction boundary and expected failure response. Use the review guide to challenge your first design rather than treating it as a checklist of files to copy.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Review the invariant before the controller

For department filtering, a strong implementation adds the condition to the same `where` object used by count and list. A common regression applies it only to rows, leaving the displayed total incorrect. Another lets the client send a tenant ID alongside the new filter. The actor's tenant must remain authoritative regardless of the filter shape. Test a page boundary as well as a single matching result.

For a new contact field, distinguish migration compatibility from form validation. A required browser input does not populate existing rows or protect API callers. A nullable database field may require mapping null to an empty editor string without accidentally treating it as a request to erase data. In this application's complete-profile update, the request explicitly carries every editable field. If you switch to PATCH, define omission and null separately and still require a version.

Company archiving exposes a race that does not exist in the delivered read-only company selector. An assignment transaction can read ACTIVE while an archive transaction changes the company. One design locks the company row in both operations and checks the state under that lock. Another models allowed assignments differently. Whichever you choose, give reviewers an interleaving and a real database test proving your rule. A composite foreign key checks tenant ownership, not active status.

Onboarding tasks need parent checks as well as task checks. An ID from another tenant must not become usable just because the submitted task body contains the caller's tenant. If a task completion increments a plan version, explain whether unrelated task completions should conflict. If every task has its own version, explain how the plan-complete invariant is evaluated atomically. Do not add broad automatic activation until you can state exactly which requirements it represents.

An idempotency receipt should be scoped to the authenticated tenant and operation. Store the normalized request fingerprint and accepted response inside the same transaction. If receipt insertion loses a uniqueness race, retrieve the committed receipt and compare fingerprints; do not independently create another worker. Define receipt retention and what happens after deletion. This is a larger behavior contract than catching a duplicate-email error and returning the existing row.

When reviewing the delivered source, ask four concrete questions. Can a caller escape tenant scope through an item ID or company ID? Can two saves both accept the same version? Can an audit failure leave an unaudited worker change? Can the UI claim success while retaining only a local proposal? The integration and browser suites address these boundaries. Other concerns remain, including identity-provider integration, distributed rate limiting, token revocation sessions, pagination under changing datasets and migration of existing populated installations. A mid-level review states those limits precisely without describing every unimplemented feature as a defect in a bounded learning application.
''',
'07-TRACE-LAB.md':'''# Trace authorization, conflict and rollback

Begin with a disposable database and the two seeded administrator accounts. Sign into Acme, create a worker and copy its UUID from the create response. Sign out and sign into Globex. The directory and recent activity should show Globex data. Send a GET for the copied UUID using Globex's token through a local HTTP client. The response is not found. Repeat with update, status and delete using otherwise valid payloads. The server should never adopt a tenant ID from the request body to make the foreign row accessible.

Read the guard and list the inputs it trusts. The token signature validates the subject, but the role and tenant used for authorization are loaded from PostgreSQL. In the isolated test fixture, suspend the user after issuing a token. The next protected request should fail. Explain the remaining race: a request whose guard already completed is not retroactively canceled by a later suspension. Stronger immediate revocation would require an explicit transaction or session policy.

Next, sign into Acme in two separate tabs and open the same draft worker. Record its version. Submit a title change from A, then a different title from B. Observe the 409 and preserved fields in B. Refresh directory and verify that it does not silently replace the open form's captured version. Cancel Load current worker once, then accept it. The explicit accepted reload replaces the proposal and establishes the current version for a deliberate new edit.

For the rollback trace, run the integration case that creates a rejecting audit trigger. Write down the transaction steps before running it: fetch scoped worker, check state/company, conditional update, read resulting row, insert audit, trigger exception, rollback, generic error response. Query both worker and audit afterward. The worker should retain its old version and the rejected audit should not exist. The request reference ties the visible error to the server event without exposing SQL or employee details.

Finally, follow a successful lifecycle: DRAFT to ONBOARDING to ACTIVE to PAUSED to ACTIVE to TERMINATED. Try deleting after onboarding begins and editing after termination. These failures protect the declared local workflow history. They do not check contracts or country compliance, because those services have not been built. Record a table with actor tenant, worker tenant, expected version, requested action, response and final row version. Include one success, one ownership failure, one conflict and one rollback. This makes your understanding reviewable and exposes where an assumption differs from observed behavior.
'''}
for name,text in docs.items():(d/name).write_text(text,encoding='utf-8')
print({name:len(text.split()) for name,text in docs.items()})
(s/'README.md').write_text('''# GlobalWorkforce OS

A local learning application with a working tenant-scoped worker directory: sign-in, profile CRUD, version conflicts, bounded search/pagination, guarded status transitions and transactional worker audit records. Start the detailed [junior-to-mid-level course](astraupskill/README.md).

## Implemented scope

The Nest API and React UI now operate on PostgreSQL records. INTERNAL_OPS, CLIENT_ADMIN and CLIENT_HR can operate within their assigned active tenant. Worker self-service and global administrator access are not implemented. Companies are selectable active records; company maintenance is a future exercise. Contracts, payroll, benefits, documents, support and compliance remain schema/roadmap material. Status changes are learning workflow rules and do not perform real employment or payroll actions.

## Local setup

Use Node 22.12 or newer within Node 22, npm, and a disposable PostgreSQL database. Docker is optional; a local PostgreSQL installation works.

```powershell
npm.cmd ci
Copy-Item apps/api/.env.example apps/api/.env
```

Edit `apps/api/.env`: set DATABASE_URL to your disposable database, JWT_SECRET to at least 32 random characters, and DEMO_PASSWORD to a chosen password of at least 12 characters. Do not retain the JWT placeholder. Then run:

```powershell
npm.cmd run prisma:generate
npm.cmd run prisma:deploy
npm.cmd run prisma:seed
npm.cmd run dev
```

Open http://127.0.0.1:5173. The API listens on loopback port 3000. For Docker's supplied local fixture, database credentials are `user` / `password`; align DATABASE_URL with the Compose file or use your own local database credentials. The first migration creates the full schema and is intended for an empty database. No existing personal database was migrated during implementation; populated installations need a reviewed migration/baselining plan.

Sign in with `client.admin@acme.example.com` or `client.admin@globex.example.com` and your DEMO_PASSWORD. Repeating the seed preserves existing records and passwords rather than resetting them. Legacy bcrypt-hashed demo accounts are not silently converted by this new scrypt seed; use a fresh learning database or design an explicit credential migration. Tokens stay in UI memory and expire after 30 minutes. Reloading signs out; saved database records remain.

## Daily workflow

Create a draft worker, edit its profile, then move through onboarding, active, paused and terminated states. Only unlinked draft workers can be deleted, subject to related-history constraints. Terminated profiles are read-only. Failed saves keep the editor. A conflict requires reviewing current data; Load current worker confirms before replacing the proposal. Directory refresh does not rebase the open editor. Audit entries describe accepted changes and retain minimal metadata.

## Verification

```powershell
npx.cmd playwright install chromium
npm.cmd run test:e2e -- verify
```

The harness creates its own temporary PostgreSQL cluster on loopback, applies migrations, runs API tests, builds both apps, checks the frontend and exercises Chromium. Set POSTGRES_BIN when PostgreSQL binaries are elsewhere; on Windows its default is `C:\\Program Files\\PostgreSQL\\18\\bin`. It does not use your DATABASE_URL. Set WORKFORCE_VERIFY_RESULTS_DIR for retained logs/screenshots and PLAYWRIGHT_BROWSERS_PATH for an existing browser installation. See [evidence and limits](astraupskill/VERIFICATION.md).

The app is a local learning edition. It has no refresh-token sessions, MFA, production deployment, distributed rate limiter, outbox, create-idempotency receipt or comprehensive employment workflow. Request references and generic server errors support debugging without returning database details.
''',encoding='utf-8')
(s/'apps/web/README.md').write_text('# Workforce operations UI\n\nRun setup from the [repository README](../../README.md). This React/Vite app calls the loopback Nest API through the Vite `/api` proxy. The API supplies authenticated tenant scope, workers, active companies and recent worker audit events. The UI holds its token in memory and preserves failed profile drafts. Refreshing the page requires signing in again.\n\nUse `npm run dev:web` from the repository root. Use the root verification harness to test both services with an isolated PostgreSQL database. See the [source walkthrough](../../astraupskill/01-CODEBASE-MAP.md) and [verification report](../../astraupskill/VERIFICATION.md).\n',encoding='utf-8')
replacements={
'01-product-overview.md':('Product scope','The delivered product is the worker operations directory. Sign-in, tenant-scoped profile CRUD, status transitions and accepted-change audit are implemented. The broader EOR platform remains a roadmap; its schema is not evidence of working payroll, contracts or compliance services.','README.md'),
'02-architecture.md':('Architecture','React sends bearer-authenticated requests to Nest. The guard derives tenant scope from the current database account. Prisma transactions commit each worker mutation and audit together; PostgreSQL constraints protect email uniqueness and company ownership.','01-CODEBASE-MAP.md'),
'03-domain-model.md':('Domain model','Worker version is the optimistic concurrency token. Tenant plus normalized email is unique. Company ID and tenant ID form the referenced company key. Unlinked drafts may be deleted unless related history prevents it; terminated profiles remain read-only.','02-CONCEPTS.md'),
'04-auth-security-rbac.md':('Authentication and authorization','The implemented operations roles are INTERNAL_OPS, CLIENT_ADMIN and CLIENT_HR within the assigned active tenant. Login uses salted scrypt hashes and signed thirty-minute JWTs. Each protected request reloads account and tenant status. There is no global admin workspace switch, worker self-service flow, MFA or refresh-session service.','02-CONCEPTS.md'),
'05-api-reference.md':('API reference','All paths use /api. POST /auth/login accepts email/password. Authenticated GET /me, /companies and /audit return current identity, up to 100 active company choices and the latest 30 worker events. GET /workers supports page, limit (maximum 50), q and status. POST /workers creates a draft. GET /workers/:id reads it. PUT /workers/:id accepts the complete editable profile plus version. POST /workers/:id/status accepts version/status. DELETE /workers/:id accepts a JSON body with version. Unknown body/query fields are rejected. Item access is tenant-scoped.','03-WORKED-CHANGE.md'),
'06-testing-strategy.md':('Testing strategy','The API suite uses a fresh helper-owned PostgreSQL cluster and actual Nest routes. Competing updates, foreign tenant IDs and a database audit-rejection trigger exercise the important boundaries. Chromium scenarios cover drafts, CRUD, lifecycle, workspace changes, failure presentation and responsive layout.','04-TESTING-AND-DEBUGGING.md'),
'07-local-development.md':('Local development','Follow the repository README for Node 22, a disposable PostgreSQL database, explicit secrets, migrations, seed and dev servers. Docker is optional. The automated harness owns a separate temporary cluster and never applies migrations to your personal database. The initial migration is for an empty database.','README.md'),
'08-learning-guide-for-junior-to-mid-level-engineers.md':('Learning sequence','Begin with the new source-based course. Trace one create, reproduce a stale edit, prove audit rollback and then attempt a small extension. Each exercise separates implemented behavior from proposed work and requires ownership/concurrency evidence.','README.md'),
'09-extension-roadmap.md':('Extension roadmap','Proposed extensions include department filtering, additional profile fields, versioned company maintenance, onboarding tasks, idempotent creation, worker self-service and an outbox. None is counted as delivered by this worker-directory implementation. Each needs a clear invariant, database migration where relevant, user flow and failure tests.','05-PRACTICE.md')}
for name,(title,body,link) in replacements.items():(s/'docs'/name).write_text(f'# {title}\n\n{body}\n\nSee the current [detailed learning guide](../astraupskill/{link}) and [setup instructions](../README.md). This page replaces the earlier scaffold description so advertised behavior matches the implemented worker slice.\n',encoding='utf-8')
