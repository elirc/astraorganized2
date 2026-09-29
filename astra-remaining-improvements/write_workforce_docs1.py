from pathlib import Path
s=Path(__file__).resolve().parent/'stage/56044dcd81ce';d=s/'astraupskill';d.mkdir(exist_ok=True)
docs={
'README.md':'''# GlobalWorkforce: learn a tenant-scoped CRUD application

This course follows the implemented worker directory from a React form to a Nest controller, a Prisma transaction and a PostgreSQL row. It starts with a junior developer's familiar create/edit/delete workflow and builds toward mid-level concerns: ownership, competing edits, state transitions, rollback, truthful responses and reproducible verification. The surrounding EOR schema contains many future domains; their presence does not mean payroll or compliance automation has been implemented.

Run the local app using the root setup guide. Sign in as the seeded Acme administrator with the password you chose for the disposable demo database. Create a worker named Ada Learner with a unique email and an active company. Save, edit the job title and refresh the directory. Each successful mutation should have a corresponding entry in Recent worker activity. A failed proposal should leave the form available and should not create another audit record.

Read [the map](01-CODEBASE-MAP.md) first. Then study [the concepts](02-CONCEPTS.md), follow [the worked change](03-WORKED-CHANGE.md), and run [the testing exercises](04-TESTING-AND-DEBUGGING.md). Attempt [practice changes](05-PRACTICE.md) before reading [review guidance](06-SOLUTIONS-AND-REVIEW.md). Finish with [the trace lab](07-TRACE-LAB.md) and compare your evidence with [verification](VERIFICATION.md).

Your first milestone is explaining a successful create without skipping the authorization boundary. The second is reproducing a stale update in two tabs and explaining why automatically retrying would lose data. The third is showing that a database failure during audit insertion rolls back the worker change. The fourth is designing a new feature with tests for both its happy path and its ownership/concurrency boundaries.

Keep an engineering notebook with small request/response examples, observed versions and the database rows affected. Avoid copying real employee data into this learning project. The demo uses synthetic people; country codes are format-checked labels, not legal eligibility decisions. Moving a worker to ACTIVE is a local workflow exercise, not a verified employment or payroll operation.

You are ready to move on when you can review another developer's change and identify the invariant, the commit boundary, the failure response and the remaining limitation. Do not judge your progress by how many endpoints you can generate. A small directory that reliably rejects the wrong edit teaches more useful reasoning than a large schema whose advertised workflows do not exist.
''',
'01-CODEBASE-MAP.md':'''# Follow one request through the source

[apps/web/src/App.tsx](../apps/web/src/App.tsx) owns sign-in, the accepted directory page, filters, the worker editor and activity display. Its `draft` is separate from `editing`: the former contains proposed profile fields, while the latter holds the accepted identity and version captured when Edit was chosen. A failed save changes the error message but retains both. `profileOf` in [api.ts](../apps/web/src/api.ts) selects editable fields rather than spreading the whole database record into a request.

The request helper sends a bearer token from memory and translates a non-success response into an `ApiError`. It does not persist tokens in browser storage. Reloading therefore signs the learner out. Directory requests use an effect generation and cleanup flag so an older response cannot replace a later search or a new workspace session. Mutations disable relevant controls while pending; a successful response closes the editor and refreshes accepted data.

[apps/api/src/app.ts](../apps/api/src/app.ts) builds a reusable Nest application, applies the `/api` prefix, assigns a request reference and limits JSON body size. `main.ts` loads an optional local environment file and listens only on loopback. The application factory is also used by integration tests, so those tests exercise the actual controller/filter/guard composition.

[auth.ts](../apps/api/src/auth.ts) handles password verification, JWT issuance and the guard. The guard reloads the user and tenant on every protected request, checks their active state and allows the three operations roles. It derives the tenant from that database relationship. A caller-supplied tenant ID is never an authorization source. `password.ts` implements salted scrypt hashes using Node's asynchronous crypto API.

[workers.ts](../apps/api/src/workers.ts) contains controllers and the worker service. Read the service before adding routes: create/update/status/delete pair their worker mutation with an audit insert inside one transaction. Profile input, version bounds, query parsing and the status graph live in [validation.ts](../apps/api/src/validation.ts). Error translation lives in `errors.ts`; database details are not sent to the browser.

The Prisma schema declares the worker version, per-tenant email uniqueness and the composite company/tenant relationship. The migration materializes those constraints in PostgreSQL. Existing contracts, onboarding and payroll models remain available for later exercises. The seed creates two isolated sample workspaces and preserves existing demo records on repeat runs. Finally, the [verification harness](../scripts/test-database.mjs) owns a temporary PostgreSQL cluster, applies migrations, runs tests and stops it before removing only its own temporary directory.
''',
'02-CONCEPTS.md':'''# Ownership, versions and atomic acceptance

A tenant-scoped application must answer two different questions: who is calling, and which records may that caller operate on? Sign-in proves knowledge of a password and returns a short-lived signed token. The guard uses its subject to reload the account, role and tenant. Every worker query then includes that tenant ID. Knowing a foreign worker's UUID does not grant access; item operations return not found when the row is outside the caller's workspace.

The current console accepts INTERNAL_OPS, CLIENT_ADMIN and CLIENT_HR within their assigned tenant. It has no global administrator switch or worker self-service flow. Suspended accounts and tenants are rejected on subsequent requests even if a previously issued token has not expired. This is request-time revocation checking, not a promise to cancel a transaction already in progress when an administrator changes a role.

Worker identity and worker version serve different purposes. Identity says which record; version says which accepted state the editor saw. A versioned update uses a conditional database statement conceptually equivalent to:

```sql
UPDATE "Worker"
SET "firstName" = 'Grace', version = version + 1
WHERE id = :id AND "tenantId" = :tenant AND version = :expected;
```

The actual implementation uses Prisma parameters and also protects terminated profiles. If two requests submit the same version, only one conditional update can affect the row. Zero affected rows becomes a conflict; the losing editor retains its proposal. Reading the version and then issuing an unconditional update would reintroduce the race.

The company relation includes both company ID and tenant ID. Application validation gives a useful error for a foreign or inactive company, while the composite foreign key prevents a direct database write from assigning a company owned elsewhere. These protections complement each other. Similarly, the normalized email and tenant form a unique database key, so concurrent creates cannot both claim the same address inside one workspace.

Audit insertion shares the worker transaction. If it fails, the worker change rolls back. A successful HTTP response therefore describes both accepted records. This does not make a later external notification atomic with the database; that would require an outbox or another explicitly designed delivery mechanism.

The lifecycle graph is another invariant. Drafts can enter onboarding; active workers can pause or terminate; terminated profiles remain read-only. Deletion is limited to unlinked drafts and remains subject to foreign-key history protection. These are learning workflow rules, not evidence that statutory employment requirements have been checked. The [Nest authentication guide](https://docs.nestjs.com/security/authentication) describes the bearer-token/guard pattern; this project's tenant and transaction rules come from its own source and tests.
''',
'03-WORKED-CHANGE.md':'''# Worked change: update a worker without losing another edit

Create a draft worker through the UI and open Edit. Read the response in the network panel: the record includes a UUID, its tenant, company, employment status and version 1. The editor copies only profile fields into `draft` and retains the accepted record in `editing`. Type a different job title. Nothing has reached PostgreSQL yet, even though the input visibly changed.

The Save worker handler sends a complete editable profile plus the captured version. A shortened teaching example looks like this:

```json
{
  "firstName": "Ada",
  "lastName": "Learner",
  "email": "ada@example.test",
  "companyId": "a1111111-1111-4111-8111-111111111111",
  "countryCode": "US",
  "jobTitle": "Software developer",
  "department": "Engineering",
  "version": 1
}
```

Use the actual company ID from your seed or company selector; this example ID belongs to the documented disposable seed. The request goes to `PUT /api/workers/:id` with the token in the Authorization header. There is no tenant or employment-status field in the editable profile. Adding one causes strict validation to reject the body rather than accidentally changing ownership or bypassing the status graph.

The guard authenticates the caller. The service validates input, starts a transaction and looks up the worker inside the actor's tenant. It rejects a terminated profile and verifies that the selected company is active in the same workspace. The conditional update matches the expected version and increments it. After retrieving the accepted row, the service inserts WORKER_UPDATED with the actor, worker identity and resulting version. Only the transaction's successful completion returns that row to the controller.

Now repeat with two tabs signed into the same workspace. Both open revision 1. A changes the title and saves, producing revision 2. B submits a different title with revision 1 and receives a conflict. The UI displays the message and reference, keeps B's fields and leaves its captured version unchanged. Refresh directory does not secretly rebase the open editor. Load current worker requires confirmation before replacing it with the saved profile.

Inspect the audit table after this sequence: create and A's update exist; B's rejected attempt did not become a successful audit event. A security-event log of rejected requests would be a separate feature. Do not confuse recording accepted domain changes with logging every attempted request. The implementation intentionally stores minimal audit metadata instead of duplicating the whole employee profile in another table.
''',
'04-TESTING-AND-DEBUGGING.md':'''# Verify the database behavior you rely on

Use the helper-owned PostgreSQL harness for API integration tests. It refuses to use an arbitrary configured database: the test module checks the loopback host, special test database name and ownership marker before destructive fixture setup. The harness creates a new cluster, applies the migration and shuts the cluster down in a finally block. A shutdown failure retains the directory rather than deleting files beneath a possibly running server.

The API suite uses the real Nest application, guards, validation, exception filter and Prisma client. It covers authentication, suspended users/tenants, unsupported roles, creation, request Location, strict input bounds, per-tenant uniqueness, filtering/pagination, cross-tenant item access, company ownership, inactive companies, stale updates, simultaneous updates, lifecycle restrictions, deletion and request body limits. The concurrency tests issue competing requests with the same version and expect exactly one winner.

One test creates a temporary PostgreSQL trigger that rejects WORKER_UPDATED audit inserts. The worker update executes first inside the same transaction, then the trigger fails. The response must be a generic server failure with a request reference; querying the worker afterward must show the original name and version. The test removes its trigger in finally. This is direct evidence of rollback in the tested database, not an in-memory approximation of transaction behavior.

Browser tests add another layer. They check that the interface preserves failed drafts, requires deletion confirmation, retains accepted changes after signing in again, rejects a stale second-tab edit, limits lifecycle actions, clears data when switching workspaces and renders markup-like names literally. A synthetic unavailable response tests failure presentation without taking down a real service. Screenshots examine desktop and narrow layouts, including intentional horizontal scrolling inside the directory table.

When debugging, start with the request reference shown in the UI and identify the last completed boundary. A 400 suggests parsing or validation; 401 concerns session/account state; 403 concerns permitted role; 404 may mean absent or foreign identity; 409 describes a uniqueness, relationship, status or version conflict. A 500 confirms no success response, and the transactional test demonstrates rollback for the injected audit failure. A network disconnection after commit remains an uncertain outcome: refresh before retrying a create.

Avoid increasing test timeouts as a first response to a race. Await an accepted row, response or loading completion. Check which database and browser profile a test owns before adding cleanup. The verification report separates observed results from proposed exercises and from untested deployment, crash-recovery and high-load behavior.
'''}
for name,text in docs.items():(d/name).write_text(text,encoding='utf-8')
print({name:len(text.split()) for name,text in docs.items()})
