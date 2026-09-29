from pathlib import Path
s=Path('astra-remaining-improvements/stage/993e7c3b44d7');d=s/'astraupskill';d.mkdir(exist_ok=True)
docs={
'README.md':'''# GlobGame: learn CRUD by publishing a daily puzzle

This course follows a complete vertical feature through a Next.js application: an author creates a puzzle draft, edits its categories, resolves stale saves, publishes an immutable edition, and archives it later. The public game reads published data through Prisma and PostgreSQL. Its browser session has a separate persistence boundary, so one project teaches both server transactions and local recovery.

Begin with the [project README](../README.md) and a fresh learning database. Generate an author token for your own local server; the studio keeps the entered token only in memory. Open `/studio`, create a title and date, and enter four categories of four words. Every word must be unique across the sixteen-word puzzle, ignoring case. Add a final theme connecting the categories. Save the draft and verify that its version changes only after a successful response.

A useful first puzzle groups programming concepts: HTTP methods, SQL operations, test types, and data structures. Choose words that are genuinely distinct; a duplicated “update” across two categories should be rejected because players need an unambiguous board. Describe the learning objective in a separate engineering note, then use the application to test the puzzle itself.

Follow [the codebase map](01-CODEBASE-MAP.md) to trace the editor through its route, runtime validation, transaction, and database constraints. Read [the core concepts](02-CONCEPTS.md), then reproduce [the worked change](03-WORKED-CHANGE.md). Run the failure experiments in [testing and debugging](04-TESTING-AND-DEBUGGING.md) before attempting [the practice tasks](05-PRACTICE.md). Use [the review guide](06-SOLUTIONS-AND-REVIEW.md) after writing your own implementation, and finish with [the trace lab](07-TRACE-LAB.md).

The progression should produce evidence rather than only notes. For each session, record a small change, the invariant it preserves, an observed failure case, and a passing check. For example: “A stale version returns a conflict before category replacement, so the other author's committed words remain intact.” That explanation connects user behavior to the transaction boundary.

Publication is deliberately consequential: an edition's words, date, and locale become permanently read-only. Archive hides it from public play while retaining its history. Only never-published drafts without results can be deleted. This makes lifecycle rules concrete without pretending that every record should support unrestricted updates forever.

The author token is a local workshop access mechanism, not a multi-user account system. The browser receives puzzle relationships and can inspect answers; there is no protected leaderboard or server grading claim. [Verification](VERIFICATION.md) records what was executed and what remains a practice extension.
''',
'01-CODEBASE-MAP.md':'''# Trace the authoring and gameplay boundaries

The authoring page is [studio/page.js](../src/app/studio/page.js). It supplies the page structure and renders [PuzzleStudio.js](../src/components/globs/PuzzleStudio.js), the client component that owns token entry, library filters, and the active editor. The editor retains the version it originally loaded. Input changes affect its draft, while successful server responses replace the accepted editor snapshot. Errors leave the fields available for correction or export.

The collection route at [api/studio/puzzles/route.js](../src/app/api/studio/puzzles/route.js) handles listing and creation. The identifier route handles reading, updating, and deleting one puzzle; its publication subroute changes visibility. Routes remain thin: they authenticate, parse bounded JSON, call a domain operation, and translate the result. They do not contain the category editor's rendering logic or manually reconstruct SQL statements.

[http.js](../src/lib/http.js) owns the request boundary. It checks the configured bearer token, rejects cross-origin authoring requests when an Origin header is present, limits JSON bodies to 32 KiB, and assigns request identifiers. Error responses distinguish validation, missing records, conflicts, and unavailable storage. Unexpected database text is not copied into the response or application log.

[validation.js](../src/lib/puzzles/validation.js) validates plain JavaScript values at runtime. It checks real calendar dates, supported locales, string bounds, exact category/member counts, uniqueness, unknown properties, and repeated query parameters. [authoring.js](../src/lib/puzzles/authoring.js) owns lifecycle decisions and Prisma transactions. Creation builds a root plus four child groups. Updating checks the captured version before replacing draft groups. Publication freezes content; archive preserves that freeze. Audit rows are written in the same transaction as each accepted mutation.

[The Prisma schema](../prisma/schema.prisma) defines puzzles, groups, results, and retained authoring audit records. Date/locale/size/type uniqueness prevents two editions occupying the same slot. Result references prevent deleting their puzzle history. The audit table intentionally retains the puzzle identifier after a draft is deleted.

The public path starts in [page.js](../src/app/page.js), passes through the strict daily filters and [resolveDailyPuzzle.js](../src/lib/puzzles/resolveDailyPuzzle.js), then builds a validated hierarchical payload. Demo mode is explicit and visibly labeled. [GameClient.js](../src/components/globs/GameClient.js) uses the pure merge engine and reducer. Session validation checks saved leaf coverage, ancestry, counters, and history; the storage adapter coordinates writes between tabs and supports raw recovery exports. These browser rules protect local continuity, while server rules protect authored editions. Neither boundary can replace the other.
''',
'02-CONCEPTS.md':'''# Concepts that turn a form into a reliable CRUD feature

## Runtime validation and database constraints

A browser form can prevent an empty title, but an HTTP client can bypass that form. `puzzleDraft` therefore checks the same business requirements at the server boundary. It accepts only editable fields, rejects unknown properties, validates actual calendar days, and checks all sixteen members for case-insensitive uniqueness. The database adds a different guarantee: two concurrent requests cannot occupy the same locale, size, date, and puzzle type. An application-only “does this date exist?” query would race.

## Optimistic concurrency

An editor reads version 3 and submits version 3 with its proposed changes. The service reads the current record, verifies lifecycle rules, then performs a conditional update matching both identifier and version. It increments the version inside that statement. If another request has already committed version 4, the conditional update affects zero rows and the transaction fails with a conflict.

The earlier read is useful for meaningful errors, but the conditional write is the concurrency boundary. Merely checking the version in JavaScript and then issuing an unconditional update is insufficient. Both requests could pass the check before either writes.

## Atomicity across related records

A puzzle update changes metadata, replaces its draft groups, and creates an audit row. These actions form one accepted operation. If category insertion or auditing fails, the transaction rolls back all of them. The learner should never see a new title paired with half the old groups. The audit-failure test uses a real PostgreSQL trigger to prove rollback after the operation has already begun.

## Lifecycle rules

CRUD does not imply that every operation is valid in every state. A published puzzle may already have saved player sessions, so its content becomes immutable. Archive changes visibility while retaining the edition. Delete applies only to never-published drafts without results. This is a domain rule, not simply a disabled button. The server checks it even when called directly.

## Two kinds of persistence

The studio persists authored records in PostgreSQL. The game persists one player's board in local storage. Its Web Lock and exact saved-value comparison coordinate cooperating tabs. A failed local write keeps the accepted board unchanged and exposes the proposed move for export. A fresh reset generation prevents an old save from accidentally appearing current again.

These local guarantees do not create server authorization. Conversely, an authenticated API does not preserve a browser draft automatically. Mid-level implementation work requires identifying which boundary owns each invariant and testing it at that boundary. Also distinguish a rejected request from an uncertain response: a network interruption can occur after the server commits. Reload current records before retrying an uncertain creation; durable idempotency is a later exercise.
''',
'03-WORKED-CHANGE.md':'''# Worked change: safely replace a puzzle draft's categories

Start with a saved, never-published mini puzzle. Open it in the studio and record its identifier and version. Change the title and one category's words. Before pressing Save, fetch the record in another tab or through the authenticated API. The database should still contain the original values: the editor is a proposal until the server accepts it.

Follow the Save handler in [PuzzleStudio.js](../src/components/globs/PuzzleStudio.js). Existing records send a PUT containing `version` and `draft`. The route rejects extra wrapper properties, and `puzzleDraft` validates every editable field. The client does not send `isPublished`, audit timestamps, generated group identifiers, or its own next version. Those values belong to server operations.

Inside [updatePuzzle](../src/lib/puzzles/authoring.js), the transaction first locates the puzzle and checks that the captured version matches. It rejects a previously published edition. The conditional metadata update then matches identifier, version, and draft lifecycle state, incrementing the version atomically. If it affects no row, another request has changed the record and the operation stops.

Only after acquiring that versioned update does the transaction remove the old draft groups and insert the replacement root and children. Their identifiers are generated on the server. Draft group identities may change during editing because no published game should depend on them yet. Once published, those groups become immutable. Finally, the transaction inserts the audit row and returns the committed detail representation.

Now create a conflict deliberately. Keep the original editor open, update the same record through a second client, and then save the first editor. Expect a conflict, retained fields, and no category replacement. Use Export editor draft before Load current puzzle. Loading current data asks for confirmation because it replaces the open proposal. Reapply the intended change against the new version after reviewing what the other writer changed.

For a rollback experiment, run the disposable database tests. Their temporary audit trigger rejects UPDATE audit rows. The test verifies that title, version, categories, and audit count all remain at their previous accepted values. Checking only the HTTP status would not establish this invariant.

Your extension is a short author-facing description. Add it to the schema, runtime validator, form, detail response, and migration. Decide whether it freezes at publication with the words. Test a boundary-length description, a stale update, and rollback after the metadata statement. Explain why the returned server representation is the source of the new version rather than a client-side increment.
''',
'04-TESTING-AND-DEBUGGING.md':'''# Test the boundary that can break the requirement

Run `npm test` for the dependency-light Node model suite. It checks authoring input, query parsing, hierarchy validity, deterministic payloads, successful and rejected merges, session restoration, raw-data preservation, competing local writers, quota failures, and HTTP request boundaries. These tests do not require a running PostgreSQL database. They are useful when changing a validator or a pure engine rule.

Use `npm run test:database` for real transaction checks. The helper creates a new temporary PostgreSQL cluster bound to loopback, selects a free port, creates its own database, generates Prisma, applies migrations, and runs the model and database suites. It then seeds twice, stops PostgreSQL, and removes only its verified temporary directory. Set `POSTGRES_BIN` if your PostgreSQL command-line binaries are installed elsewhere. The helper replaces its own DATABASE_URL; it does not run tests against a personal configured database.

Use `npm run verify` for the complete path, including lint, a production Next.js build, and Chromium workflows against the built server. Install the browser runtime once with `npx playwright install chromium`. Browser tests use isolated contexts and a helper-owned database. This verifies actual form behavior and downloads rather than asserting that a handler function was called.

## Reproduce a stale edit

Open a draft in two authoring clients. Change different fields without saving. Save A, then B. B should show a conflict and retain its input. Export B's editor draft and inspect the downloaded JSON. Fetch the accepted record and confirm that A's title, categories, and version remain unchanged by B's rejected save. Then load current data in B after confirming the discard.

## Reproduce a local save failure

In a disposable game context, replace storage writes with a function that throws a quota error. Attempt a valid merge. The accepted board should remain intact, the error should stay visible, and Export pending move should contain the proposed result. A success-looking board followed by lost progress on reload would violate the intended behavior.

## Diagnose an unavailable database

The public API reports unavailability rather than silently claiming a sample is today's edition. Use the response's request identifier to correlate a minimal server failure record. The browser displays an actionable setup message. Explicit demo mode is a separate configuration choice and labels the sample in the page. Avoid copying raw SQL errors or environment secrets into a screenshot or bug report.

Read [verification](VERIFICATION.md) for the executed results and remaining limits. A passing model suite does not prove transaction rollback; a passing database suite does not prove that a failed form retains its fields. Each layer contributes different evidence.
''',
'05-PRACTICE.md':'''# Practice sequence toward mid-level web application work

## 1. Add a draft description

Introduce an optional description with a clear maximum length and a migration default for existing rows. Decide whether whitespace-only input becomes an empty description or a validation error. Keep the field in the captured editor draft. Test direct HTTP input as well as the HTML form. Demonstrate that an invalid description cannot partially replace categories.

## 2. Improve library navigation

Add a date-range filter with inclusive beginning and exclusive end semantics. Validate both calendar dates and reject reversed ranges. Combine it with the existing title and publication-state filters. Keep ordering stable when two records share a date by retaining an identifier tie-breaker. Test a result exactly at the end boundary and a page after records are deleted. Explain when offset pagination becomes expensive and how a date-plus-identifier cursor would change the contract.

## 3. Introduce individual authors

Replace the shared local workshop token with an explicit account/session design. Add author ownership to drafts and define who may publish. Enforce authorization in every server read and write, including list filters and lifecycle routes. A hidden button is insufficient. Test another author's identifier, a revoked session, and a role change. Keep credentials out of browser persistent storage according to your chosen session design and document the related CSRF assumptions.

## 4. Make creation safely retryable

Design an idempotency key for POST creation. Scope it to the authenticated author, store a canonical request fingerprint and accepted response, and commit the receipt with the puzzle and audit row. Reusing the same key and payload should return the original result. Reusing the key with different categories should produce a conflict. Test two concurrent identical requests and an interrupted response after commit. Do not simply cache responses in one server process and claim durability across restarts.

## 5. Separate publishing from notifications

Add a requirement to notify subscribers when an edition is published. Keep the publication and durable notification intent in one SQL transaction, then deliver externally through a separate worker. Give each message a stable identity and make retries safe. Inject an external delivery failure and show that the published edition remains valid while the notification remains retryable. Explain why an email call inside the database transaction creates a difficult failure boundary.

## 6. Support a larger puzzle format

Design the hierarchy before increasing form fields. Specify allowed levels, branch sizes, leaf limits, and a unique root. Extend the schema validator, authoring UI, payload builder, game tests, and saved-session compatibility checks together. Test malformed graphs, duplicate identifiers, missing parents, and leaf coverage after every merge. Preserve existing mini editions and saved boards.

For each task, write acceptance criteria before implementation and finish with a focused review note. Describe one rejected approach and the concrete requirement that made it unsuitable. The goal is to make informed changes while preserving existing behavior, not to accumulate technologies.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Review the reasoning behind the solution

For a description field, the strongest implementation starts with the domain decision: is the description public puzzle content or private author metadata? Public content should normally freeze with publication in this project. That choice determines the validator, update contract, editor disabled state, and tests. A database column alone does not complete the feature, and a form-only maximum does not protect direct API calls.

For date-range filtering, normalize valid calendar strings to UTC boundaries. A range ending at the start of the following day avoids inventing a final millisecond and makes adjacent ranges compose cleanly. Keep count and list queries on the same snapshot if the UI presents them as one coherent result. The current list service uses a repeatable-read transaction for that reason. Stable ordering prevents arbitrary record movement between requests, although offset pagination still shifts when data changes.

For individual authors, make the ownership predicate part of the database operation. Checking ownership once and later updating only by identifier leaves a gap if ownership can change concurrently. Decide whether inaccessible records appear missing or forbidden, then apply the policy consistently. The current shared token does not identify an individual actor, so its audit trail describes operations rather than proving which person performed them. State that limitation instead of assigning a fictional username.

For idempotent creation, distinguish a record version from an operation identity. Version 4 describes the accepted state of a puzzle; an idempotency key identifies one requested creation attempt. A durable receipt should include a fingerprint so the same key cannot silently accept different words. The receipt and puzzle must commit together. Otherwise a crash can leave a receipt without a puzzle or a puzzle without its receipt.

For notifications, an outbox row records intent in the publication transaction. A worker later attempts delivery and records acknowledgement. The external service and database do not share one atomic commit, so duplicate delivery remains a design question. Explain the receiver's deduplication or the limits of the chosen delivery guarantee. Avoid claiming “exactly once” merely because a retry loop has a unique identifier.

For larger puzzles, validate the hierarchy before recursive counting or payload generation. Strictly increasing parent levels rule out cycles and make ancestry checks easier to reason about. Preserve every original leaf exactly once in a board snapshot. A saved tile should not claim leaves from another group merely because its label looks plausible.

A useful review asks for one successful trace, one stale trace, and one rollback trace. The author should identify the exact conditional SQL write, the transaction containing audit insertion, and the UI state retained on rejection. Screenshots help assess clarity; they do not replace those traces.
''',
'07-TRACE-LAB.md':'''# Trace lab: a puzzle edition from draft to archive

Use the disposable verification database or a separate learning database. Keep a record of each action with columns for puzzle identifier, version, lifecycle state, category count, audit count, and visible editor title. The exercise is complete when you can explain why every accepted or rejected action produced those values.

## Trace A: create and edit

Create a draft in `/studio`. Inspect the POST response: it should contain the generated identifier, version 1, and the root plus four child groups. The response also supplies a Location header for the new record. Read the record again and compare the returned draft with the form values. Edit the title and one category, then submit version 1. Verify version 2 and one additional audit record. Record why draft group identifiers can change at this stage.

## Trace B: conflict without partial writes

Open the version-2 draft in a second client. Save version 3 from the first. Submit the older version from the second and inspect the conflict response and request identifier. The second editor should retain its title and words. Export its proposal, then inspect the database: version, metadata, groups, and audit count must reflect only accepted changes. Follow the conditional `updateMany` in the service to identify the statement that prevents the stale write.

## Trace C: publish and archive

Publish the current version after confirming the content freeze. Read the daily public endpoint for its date. It should return a database-sourced payload with the edition's identifier and sixteen tiles. Attempt a direct update and delete; both should fail even if you bypass the disabled form controls. Archive the edition and confirm that the daily resolver no longer returns it. Its `publishedAt` remains populated, so archiving does not turn it back into an editable draft.

## Trace D: local gameplay persistence

Play a valid merge and inspect the local session envelope. Its snapshot changes only after storage accepts the write. Open a second tab before another move, save in the first, then attempt a move in the second. Compare the raw baseline with current storage and explain why the stale board is preserved rather than silently merged. Export the pending move before loading current data.

## Trace E: rollback evidence

Run the database audit-failure test and inspect its log. The injected trigger rejects the audit insertion after update work has started. The assertions reread the puzzle, groups, and audit table to establish that the whole transaction rolled back. Describe what a test using only mocked Prisma calls would fail to prove.

Finish by proposing one operational metric and one alert for a deployed version. Tie each to an observable user problem, such as sustained save failures, rather than collecting every possible event. Keep puzzle words, bearer tokens, and connection strings out of operational logs.
''',
'VERIFICATION.md':'''# Verification scope and limitations

The application changes are prepared in an isolated copy and delivered through an explicit changed-file manifest after validation. The central implementation report records the final executed results. This document explains what each check establishes and the assumptions that remain. Reproduce the model suite with `npm test`, the database suite with `npm run test:database`, and the complete production/browser workflow with `npm run verify`.

The model tests cover draft normalization, invalid dates and locales, member uniqueness, repeated query parameters, hierarchical payload validation, deterministic shuffling, complete merge sequences, undo, hints, saved-board validation, damaged raw storage, serialized competing writers, quota rejection, reset generations, bearer-token checks, request size limits, and error mapping. They execute the real pure modules and injected storage adapters without requiring a personal browser profile.

The database suite uses a fresh helper-owned PostgreSQL cluster. It exercises CRUD, retained audits, concurrent versioned updates, date uniqueness, publication immutability, archival behavior, legacy published rows, stale mutations, injected audit failure with rollback, result-history protection, bounded paging, and explicit outage/demo behavior. The helper also runs the seed twice. Existing sample rows should remain unchanged, and creation of a missing sample and its groups belongs to one transaction.

The Chromium suite targets a built Next.js server with an isolated browser context and test database. It covers HTTP authorization/filter boundaries, structured editor creation and publication, stale draft export/reload, deletion confirmation, sign-out, retained inputs on server errors, gameplay reload, corrupt-session export/reset, quota failure, and desktop/narrow layouts. Screenshots are written under `astraupskill/images/` for visual inspection. A screenshot cannot establish database isolation or authorization correctness.

The initial migration is intended for an empty learning database. No existing personal database is migrated during verification. An older database needs a deliberate baseline and upgrade plan; do not erase it merely to make migration commands succeed. The helper stops its own PostgreSQL process before deleting its verified temporary directory and retains the cluster if shutdown cannot be confirmed.

The studio currently supports daily mini authoring with four categories of four words. Its shared local token is not a full account, role, revocation, or multi-tenant system. It has no durable create-idempotency receipts, notification worker, hosted deployment verification, crash/power-loss testing, or full accessibility certification. Public puzzle data includes relationships, so the client is not an anti-cheating boundary. Browser session protection coordinates cooperating clients and cannot prevent deliberate local manipulation. These are documented extension points for the practice sequence, not claims of completed production functionality.
'''
}
for name,text in docs.items():
 (d/name).write_text(text,encoding='utf-8');print(name,len(text.split()))
(s/'README.md').write_text('''# GlobGame — daily puzzles and an authoring studio

A Next.js, React, Prisma and PostgreSQL learning project. `/studio` now supports validated daily-mini puzzle CRUD, version conflicts, publication and archival. `/` plays published editions. The structured editor uses four categories of four unique words and one final theme.

## Local setup

Use Node 22+ and a **fresh local PostgreSQL database**. Install dependencies and generate the client:

```powershell
npm ci
npm run prisma:generate
Copy-Item .env.example .env
```

Set `DATABASE_URL` in `.env` to that empty learning database. Generate a local author token and keep it in your own environment or `.env`:

```powershell
node -e "console.log(require('node:crypto').randomBytes(32).toString('hex'))"
```

Set `GLOBS_AUTHOR_TOKEN` to the generated value. Then apply the initial schema and start:

```powershell
npm run prisma:deploy
npm run dev
```

Open `http://localhost:3000/studio`, enter your local token, and create today's edition. The token stays in page memory and clears on reload/sign-out. Publishing permanently freezes the words, date and locale. Archive removes the edition from public play while retaining history. Delete is limited to never-published drafts without results.

The initial migration targets an empty database. Existing databases require a reviewed migration/baseline plan. These instructions do not authorize erasing existing data. The optional `npm run prisma:seed` creates the preserved sample for **2026-02-18** and leaves an existing sample untouched; open `/?date=2026-02-18` to play it.

## Explicit sample mode

Set `GLOBS_DEMO_MODE=true` to play a visibly labeled sample for a requested date without reading PostgreSQL. Set it back to `false` to play published database editions. Database failures are otherwise reported as errors, not silently replaced with a sample. The authoring studio still requires PostgreSQL in either mode.

## Save behavior

Studio fields stay as drafts until an accepted response. Conflicts and server failures retain the editor; export it before loading current data. A timed-out creation may already have committed, so reload the library before retrying. There are no durable idempotency receipts yet.

Game moves are adopted only after local storage accepts them. Web Locks and saved-value comparisons detect competing tabs. Damaged sessions remain available for raw export before a confirmed reset. Pending move exports are diagnostic/recovery material; there is no session-import UI. Use localhost or HTTPS with a browser supporting Web Locks.

## Verification and learning

```powershell
npm test
npm run test:database
npx playwright install chromium
npm run verify
```

The database helper creates its own loopback PostgreSQL cluster and replaces its test DATABASE_URL. It never selects an existing personal database. Set `POSTGRES_BIN` to your PostgreSQL binary directory if needed; the Windows default is `C:\\Program Files\\PostgreSQL\\18\\bin`. Complete verification runs real transaction tests, seeds twice, lints, builds with webpack, runs Chromium, and stops/removes its owned test cluster. Logs default to `.verification/`.

Read the [detailed CRUD learning course](astraupskill/README.md) for code maps, worked changes, examples, debugging labs, and exercises in account ownership, idempotency, SQL transactions, and notification outboxes. The earlier [roadmap](docs/globs-plan-v2.md) is historical planning material; this README and course describe the implemented scope.

This is a local authoring workshop with a shared token, not a complete multi-user service. Public payloads expose puzzle relationships. There is no protected leaderboard, account management, deployment verification, or production-security certification.
''',encoding='utf-8')
