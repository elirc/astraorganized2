from pathlib import Path
import os

root=Path(__file__).parent/'stage/19110bf39fcf'
course=root/'astraupskill';course.mkdir(exist_ok=True)
docs={
'README.md':r'''# Help Desk: from junior CRUD work to reliable support workflows

This course uses the real Help Desk application in this folder. You will work with customers, tickets, messages, teams, channels, business calendars, service level agreements, automation rules, and canned replies. The aim is to become comfortable delivering a change that remains correct when input is wrong, two people edit at once, a connection fails, or existing data needs an upgrade. A working happy-path form is the beginning of that work, rather than its completion.

Start with the [project setup](../README.md). Use a new `HELPDESK_DATA_DIR` for your learning session. Choose explicit demo setup if you want staff, customer, and integration identities already available. Choose owner setup if you want to build the configuration yourself. Merely starting the server creates the known schema; it never creates a known password. This distinction matters because installation and account authorization have different responsibilities.

## A practical learning route

1. Spend one session using the app. Create a customer in Administration, then create a ticket in Staff workspace. Edit its subject, set it pending, reply publicly, and add an internal note. Sign in as the demo customer in a separate browser context and compare the information visible there. Explain why an internal note must be filtered on the server even if the interface has no button for it.
2. Read the [codebase map](01-CODEBASE-MAP.md) and follow one request from the HTML form to SQLite. Keep a small notebook of the file, function, input, output, and failure case at each boundary.
3. Work through [the concepts](02-CONCEPTS.md) and [the worked change](03-WORKED-CHANGE.md). Repeat their examples yourself. Predict the response before sending a stale version or a duplicate submission.
4. Use [testing and debugging](04-TESTING-AND-DEBUGGING.md) to reproduce a failure without modifying your normal database. Explain what the assertion proves and which assumptions remain untested.
5. Complete [the exercises](05-PRACTICE.md), compare your reasoning with [the review guide](06-SOLUTIONS-AND-REVIEW.md), and finish [the trace lab](07-TRACE-LAB.md).

Allow several focused sessions. Do not measure progress only by files read. A useful milestone is being able to describe why a particular rejected request made no durable change and identify the test demonstrating that fact.

## Your evidence notebook

For every exercise, record a short product requirement, one accepted example, one rejected example, the relevant source functions, the smallest meaningful test, and a screenshot or request/response excerpt. Use synthetic names and messages. Never put real customer conversations, passwords, session cookies, or integration tokens into a learning report.

For example, “prevent stale customer edits” becomes: Alice reads customer version 4; Bob saves a new note and produces version 5; Alice submits her older draft with `If-Match: 4`; the server returns 409; Bob's note remains stored; Alice's browser retains her draft. That is specific enough for another developer to reproduce. “Added concurrency support” is not.

## What this project deliberately teaches

The app uses server-rendered page shells, ordinary JavaScript forms, FastAPI, SQLAlchemy, and SQLite. You do not need a large frontend framework to learn request contracts, authorization, transaction boundaries, migrations, or user-visible failure recovery. The same ideas transfer to other stacks.

It is a local learning application. It records email/webhook intake but does not operate a mail server, deliver outbound messages, run a scheduler, or provide a production identity-management service. Customer identity changes with linked sign-in accounts are refused because transferring access deserves its own verified workflow. Browser drafts stay in memory and are not silently copied into localStorage. Read [verification and limits](VERIFICATION.md) before treating an exercise as an operational guarantee.

Your mid-level readiness milestone is a reviewable pull-request-sized change: clear requirement, correct boundary behavior, preserved data, understandable code, meaningful failure tests, and an honest explanation of the remaining limitations.
''',
'01-CODEBASE-MAP.md':r'''# Read the code by following a request

Begin with [the application entry point](../app/main.py), but do not try to memorize every route. Trace one operation, then generalize. Creating a customer is a useful first path because it has a form, a strict contract, a resource service, a database transaction, an audit event, and an accepted response.

## The main pieces

| File | Responsibility | Question to ask while reading |
| --- | --- | --- |
| `app/templates/admin.html` | Page structure, labels, list and editor containers | Can a keyboard user identify each field? |
| `app/static/app.js` | Fetching, form capture, drafts, versions, rendering | What happens if the response never arrives? |
| `app/main.py` | HTTP routes, authentication dependencies, error responses | Who may call this operation? |
| `app/contracts.py` | Bounded types and cross-field validation | Is omitted data different from explicit null? |
| `app/management.py` | Configuration CRUD and relationship checks | Can this edit break a referenced record? |
| `app/services.py` | Ticket lifecycle, visibility, reports, intake and history | Which business invariants must all callers share? |
| `app/models.py` | Tables, relationships, versioned rows | Which constraints does the database enforce? |
| `app/db.py` | Connections and request transaction lifetime | When is the write lock obtained and released? |

Open [the browser code](../app/static/app.js) at `bindForm`. It creates `FormData` before disabling the form controls. Disabled controls are excluded from normal form submission, so reversing that order can accidentally send an empty request. It also retains the original form element before awaiting network work; an event's `currentTarget` is not a durable reference to use after an asynchronous pause.

Follow `initAdmin` into its save callback. A new customer uses POST. An existing customer uses PUT and includes the version originally loaded into the editor. `payload` converts a number field to a number, a checkbox to a boolean, and an optional blank field to null. The server still validates those values; browser conversion improves usability but does not establish trust.

The route calls [management.save_record](../app/management.py). That function selects an explicit resource specification, validates the body, checks duplicates and references, assigns known fields, flushes, and creates an audit entry. The route commits before returning the accepted record. A successful flush alone is not a successful transaction: later work can still fail and roll back everything.

## A second path: public intake

Public intake starts in the portal form and reaches `portal_ticket_create`. Its UUID operation key is checked by [receipts.py](../app/receipts.py). The normalized payload is hashed so a later retry can be compared with the original operation. A matching receipt returns the existing ticket identifier. Different content with the same key returns a conflict. The customer helper does not overwrite an existing profile just because someone supplied its email address.

The ticket and receipt share a database transaction. This is the crucial connection between idempotency and persistence: a receipt without a ticket is unusable, and a ticket without its retry receipt can lead to duplicate work after a lost response. The request dependency obtains SQLite's write transaction before reading either the next ticket number or an existing receipt.

## Supporting boundaries

[http_boundary.py](../app/http_boundary.py) bounds incoming bodies, rejects duplicate JSON keys and non-finite numbers, and checks browser origins. [references.py](../app/references.py) resolves team and assignee relationships before mutation. [attachments.py](../app/attachments.py) streams bounded files, tracks new paths for rollback cleanup, and checks download containment. [business_time.py](../app/business_time.py) owns calendar arithmetic so routes do not each invent their own time rules.

Startup calls [migrations.py](../app/migrations.py), which recognizes the known SQLite layouts and preserves a consistent backup before upgrading a legacy database. Account creation belongs to [setup.py](../app/setup.py), not ordinary server startup. Read these two paths separately: changing a schema does not imply permission to create identities or replace data.

As an exercise, draw a five-box sequence for a reply: form, HTTP route, authorization/version checks, message/timer service, commit/response. Add the attachment file beside the database transaction and explain why a process crash can leave an unreferenced file even though ordinary rollback cleanup works. That explanation is more useful than copying an entire class diagram.
''',
'02-CONCEPTS.md':r'''# The concepts behind reliable CRUD

CRUD means create, read, update, and delete, but each verb carries a contract. “Update this customer” must specify which fields may change, who may change them, which previous version the user reviewed, and what happens when another request wins first. Read [the contracts](../app/contracts.py) alongside [the management service](../app/management.py) while working through these examples.

## Validate shape before changing state

The server accepts actual integers for identifier fields and actual booleans for switches. A JSON boolean is not an acceptable identifier even though Python's `bool` is a subclass of `int`. Unknown fields are rejected: misspelling `resolution_minutes` should not produce a successful response that quietly preserves the old setting. Business minutes include zero, so `value or default` is the wrong way to choose a default. It treats a valid zero as missing.

PATCH ticket updates preserve omission. Sending `{"subject":"New subject"}` does not clear the assignee. Sending `{"assignee_id":null}` explicitly removes the assignee. Administration uses full PUT replacement: its form submits all editable fields, and omitted optional values use their defaults. That difference is intentional and should appear in your API documentation and tests.

## Authentication, authorization, and visibility

Authentication identifies the caller. Authorization decides whether that caller may perform the operation. Visibility decides which records and fields the caller can read. These are related but not interchangeable. An integration bot can submit authenticated intake and still have no staff queue access. A light agent can add an internal note but cannot send a public response. A customer can read public messages on their own tickets but cannot read a private attachment merely by guessing its numeric identifier.

[services.py](../app/services.py) uses the same visibility policy for list queries, detail checks, and reporting. This prevents a common information leak: securing the detail route while allowing aggregate counts or CSV exports to include hidden records. The customer serializer is an explicit smaller representation, excluding internal notes, routing metadata, followers, and staff actor identifiers.

## Optimistic concurrency and transaction serialization

Suppose a ticket has version 8. Two people read it. The first PATCH includes `If-Match: 8`, succeeds, and advances the version. The second PATCH still includes 8 and receives 409. Its browser retains the draft and offers a latest-record review. The application never silently updates the header and resends an old draft over someone else's work.

SQLite also permits one writer at a time. `BEGIN IMMEDIATE` obtains that write position before the application chooses the next ticket number or checks a creation receipt. This serialization protects operations within the current request. The version header protects a human's earlier review across requests. You need both ideas; a write lock acquired today cannot tell you what a person read five minutes ago.

The [Versioned mixin](../app/models.py) gives SQLAlchemy a database-level compare-and-swap condition. If a row changes between an ORM read and flush, a stale update fails instead of overwriting it. Versions are monotonic identifiers, not timestamps, and may advance more than once during a complex transaction with multiple flushes.

## Idempotency and uncertain outcomes

Imagine the server commits a new ticket, but the network drops before the browser receives its identifier. Retrying with a new UUID can create a second ticket. Retrying the same normalized content with the same UUID allows [the receipt service](../app/receipts.py) to return the first ticket. Editing the content while retaining that UUID produces 409, because it is now a different proposed operation.

Replies use a reviewed ticket version rather than a creation receipt. If a reply succeeded but its response was lost, repeating the old version fails. The user reviews the conversation to determine whether the message already exists before accepting a fresh version. A timeout does not mean “nothing happened.” Good interfaces make that uncertainty understandable.

## Deletion and time are domain decisions

Deleting a ticket removes it from active access but preserves its conversation and receipt history. Deleting referenced configuration is refused. Terminal ticket states clear active deadlines; reopening begins a new resolution window. Pending states pause selected timers according to policy. [The calendar module](../app/business_time.py) calculates elapsed business time in an explicit timezone, handles weekends and split shifts, and rejects ambiguous configuration rather than silently falling back to UTC.

These choices are not universal laws. They are documented product rules for this app. Mid-level engineering includes making those rules explicit and applying them consistently in manual edits, automation, reports, and tests.
''',
'03-WORKED-CHANGE.md':r'''# Worked change: prevent one customer editor from overwriting another

The product requirement is concrete: if two administrators open the same customer, saving the older editor must preserve the newer accepted record and keep the older draft available for review. Follow this example through [the UI](../app/static/app.js), [the route](../app/main.py), [the resource service](../app/management.py), and [the ORM model](../app/models.py).

## Reproduce the problem with a disposable customer

Create a customer called “Concurrency learner” in Administration. Use a synthetic email address such as `concurrency@example.invalid`. Open the customer in two browser tabs. In the first tab, change the staff note to “Confirmed address by phone” and save. In the second tab, change the company to “Learning Company” and save. The second operation must show a conflict, retain the company draft, and leave the accepted note unchanged in storage.

The request that reads a customer returns its identifier and version together with editable fields. For example:

```json
{
  "id": 12,
  "version": 4,
  "name": "Concurrency learner",
  "email": "concurrency@example.invalid",
  "phone": null,
  "company": null,
  "notes": "Original note"
}
```

These identifiers are illustrative; use the values returned by your own run. The editor stores the reviewed version separately from the field inputs. It must not read a fresh version immediately before every save, because that would erase evidence that the person edited an older record.

## Follow the accepted update

The first PUT sends a complete editable body and a header:

```http
PUT /manage/customers/12
If-Match: 4
Content-Type: application/json

{"name":"Concurrency learner","email":"concurrency@example.invalid",
 "phone":null,"company":null,"notes":"Confirmed address by phone"}
```

Authentication and the administration dependency run before the resource service. `check_expected_version` compares 4 with the current row. Missing headers receive 428, malformed versions receive 422, and a version mismatch receives 409. Passing this check allows validation and assignment, but the ORM still includes its own version condition when writing the row. This second protection matters for code paths with independent sessions or future changes to transaction behavior.

The route commits the transaction and returns the accepted customer. The browser renders that response and clears the draft's dirty marker. It does not display “saved” merely because the submit button was clicked or a request was dispatched.

## Follow the rejected update

The second tab still submits `If-Match: 4`. The database row now has a newer version. The request is rejected before assigning the submitted company or note. The browser's `bindForm` catches the error, reenables the controls, and leaves their values intact.

Click “Review latest while keeping draft.” The latest stored record appears separately from the editable inputs. The old draft still contains the old note as well as the proposed company. Because administration uses full replacement, accepting the new version and immediately saving could replace that newer note. Read the comparison and update your draft to combine the intended company change with the accepted note. Only then acknowledge the reviewed version and save.

This is deliberately a human review step. Automatically merging arbitrary text or always preferring the current tab would hide a product decision. A future exercise can offer field-level merge assistance, but it needs explicit rules and tests.

## Verify the change

Run the focused example in [test_crud_and_files.py](../tests/test_crud_and_files.py). It creates a customer, performs an accepted edit, attempts a stale edit, and verifies the stored result. The browser verifier additionally demonstrates retained input and the review interaction. Both layers matter: a correct API can still have a frontend that clears the user's work after 409.

Now vary the example. Submit an unknown field, a duplicate customer email, an inactive assignee on a ticket, or a delete request for a referenced customer. Predict the status and unchanged state before running it. Your review notes should describe which boundary rejects each case and why no partial update is committed.
''',
'04-TESTING-AND-DEBUGGING.md':r'''# Test behavior, then investigate failures at the right boundary

Run tests only against disposable data. The shared [test fixture](../tests/conftest.py) creates a new SQLite database and upload directory under pytest's temporary directory, overrides the application's database dependency, and disposes the engine afterward. It does not delete or reset the configured application database. It explicitly creates synthetic demo records; server startup itself no longer seeds accounts.

## Start with the smallest relevant suite

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_contracts.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_creation_receipts.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_crud_and_files.py -q
.\.venv\Scripts\python.exe -m pytest -q
```

Contract tests are useful for type, omission, null, length, and unknown-field cases. Receipt tests cover same-key retries, conflicting content, simultaneous requests, legacy receipts, and rollback when the receipt cannot be stored. CRUD tests exercise authorization, stale versions, protected references, timer transitions, attachment download, and file cleanup after an injected failure. The full suite also covers calendar boundaries, migration rollback, report visibility, password parsing, token expiry, and history movement.

Do not replace production verification with a fake “always succeeds” function merely to make tests fast. The fixture caches a real password hash for synthetic identities, reducing repeated setup work while leaving the production password verifier active. This is different from bypassing authentication. Real owner/demo setup still creates password hashes through the normal code path.

## Inspect a request failure

Use browser developer tools to inspect the request method, URL, body, response status, and `If-Match` or `Idempotency-Key` header. Do not copy session cookies or tokens into issue reports. The response includes a request identifier to help correlate an observed failure with server activity.

For 422, compare the submitted value with [the declared contract](../app/contracts.py). Is `member_ids` an array of integers or a comma-separated string? Is the duration zero, blank, or a string? Did a misspelled action name reach the server? For 409, identify the conflicting state: row version, existing name, receipt content, linked identity, or a referenced record. Repeatedly clicking save without understanding the conflict is not a fix.

For 503 storage-busy responses, retain the draft and retry after the competing write finishes. If the response was lost, inspect the latest record before retrying a non-idempotent operation. The UI explains that the server may already have accepted the change.

## Test the failure after a file is written

A particularly useful test uploads a valid attachment and then injects a failure in automation before commit. The database transaction rolls back, and the session rollback listener removes the newly written file. Assert both sides: no accepted message references it, and the upload directory matches its previous contents. Testing only the response code would miss an orphan file.

Process termination is different from an ordinary exception. Cleanup code cannot run after the process has stopped. Use [the storage audit](../app/storage_audit.py) to list unreferenced files and missing or mismatched attachment records. It is read-only and does not automatically delete evidence. A recovery policy needs review before destructive cleanup.

## Browser and migration checks

[verify_browser.py](../verification/verify_browser.py) creates its own demo dataset, starts a loopback server, runs real forms in Chromium, saves screenshots, and stops only the server process it created. [verify_rendering.py](../verification/verify_rendering.py) probes dynamic rendering with hostile strings. These serve different purposes: one checks workflows, the other isolates DOM safety.

[Migration tests](../tests/test_migrations.py) use the retained legacy schema fixture, never a user's live database. They verify a consistent backup, additive columns, repeat startup, concurrent startup, unsupported-schema refusal, and rollback after injected DDL failure. A passing migration test does not establish power-loss durability on every filesystem or compatibility with unknown schema extensions. Record those limits in your change description.
''',
'05-PRACTICE.md':r'''# Practice projects, ordered from small changes to mid-level work

Use a separate branch or copy for each exercise and a fresh learning data directory. Keep the accepted implementation available so you can compare behavior. Each exercise below asks for a small product change and evidence that it preserves an existing rule. Read [the solution discussion](06-SOLUTIONS-AND-REVIEW.md) only after writing your own design notes.

## 1. Add a useful queue filter

Add a “Resolved” option to the staff queue selector. Follow the option through the URL query into `build_ticket_filters` in [services.py](../app/services.py). The filter must still respect the existing user's visibility and pagination. Create visible and hidden resolved tickets in a test fixture. Verify that the filtered result contains only visible resolved records, and that the reported total uses exactly the same filter.

Acceptance examples: an agent sees their team's resolved ticket; a customer cannot call the staff queue; an agent does not gain access to another team's ticket by using the filter. This is a good first exercise because the change is small but the authorization invariant is substantial.

## 2. Improve customer lookup without changing identity

The staff ticket form searches customers by name or email. Add a clear result count and an empty-state explanation. Retain the selected customer if a background search finishes after the user has already selected a result. Include a browser test that deliberately delays one search response, starts a second search, and confirms the older result cannot replace the newer choices.

Do not implement this by changing the customer's stored name to match the latest search text. Search inputs, draft inputs, and persisted profiles are separate state. Use the sequence checks already present in [app.js](../app/static/app.js) as a starting point, and explain exactly what each sequence invalidates.

## 3. Add field-level conflict assistance

Administration currently shows the latest record beside the retained full-replacement draft. Add a comparison table with “originally loaded,” “my draft,” and “latest stored” values. Highlight fields changed in both the draft and the stored record. Offer an explicit choice for conflicting fields; do not automatically overwrite either value.

Use the customer example in [the worked change](03-WORKED-CHANGE.md). A meaningful test has two editors change different fields, then two editors change the same note. Verify that the resolved submission still includes the reviewed latest version, and that another intervening write can produce another conflict. A comparison screen does not eliminate concurrency.

## 4. Add ticket restoration as a reviewed operation

Ticket deletion currently preserves history and receipts while hiding the ticket from active access. Design a manager-only restoration workflow. It needs a separate deleted-record query, an explicit version check, an audit event, and a decision about status and SLA deadlines after restoration. Do not expose the deleted queue through ordinary customer routes.

Write the behavior before the code. Should restoration return the previous state or reopen the ticket? What happens to a merged source? Which deadline origin is appropriate? Test unauthorized access, stale restoration, repeated restoration, preserved messages, and creation-receipt retries after deletion and restoration.

## 5. Make attachment recovery reviewable

Extend the read-only [storage audit](../app/storage_audit.py) into a proposed recovery report. Include the file, record identifier if any, problem category, observed size, and a suggested action. The first version should still make no changes. Add tests for missing files, unexpected size, paths outside the configured directory, and orphan blobs left by a simulated interrupted request.

If you later implement cleanup, require an explicit selected plan whose inputs are rechecked immediately before action. Never infer that every unreferenced file is disposable. A database restore can temporarily make valid later files appear orphaned.

## 6. Design an outbound delivery boundary

The app records replies but does not send email. Design an outbox table and a worker contract without connecting a real provider. The reply and outbox entry should commit together. The worker needs a retry identifier, bounded backoff, a terminal failure state, and a way to distinguish accepted delivery from uncertain transport results.

Use a fake adapter that can accept, reject, time out before acceptance, and accept before losing its acknowledgment. Document what is guaranteed locally and what depends on the external provider. This exercise combines transactions, idempotency, observability, and operational judgment—the kind of reasoning expected beyond basic CRUD implementation.
''',
'06-SOLUTIONS-AND-REVIEW.md':r'''# Solutions, tradeoffs, and a useful review standard

This guide gives reasoning and test expectations for [the exercises](05-PRACTICE.md). It intentionally does not provide a paste-and-submit replacement for the work. Your goal is to explain why an implementation satisfies a requirement under failure, rather than reproduce a particular syntax.

## Queue filtering

Start from `staff_ticket_query(user)`, because that statement already contains the visibility predicate. Add the resolved-status condition to the existing statement. Build the count and the paginated rows from the same filtered query. Avoid creating a second “simpler” query for totals, since that can reveal hidden records or display a page count inconsistent with the list.

A good assertion compares actual ticket identifiers, not only the number of results. Two queries can return the same count while one contains an unauthorized ticket. Also check an empty page and a search string containing `%` or `_`; those characters should be literal user input, not accidental SQL wildcard control. See [visibility tests](../tests/test_visibility.py) and [the list implementation](../app/management.py).

## Customer lookup races

Keep an increasing request sequence or use an abort controller plus a result-generation check. When the user changes search text, invalidate the older request before waiting for the debounce timer. An aborted request alone is not enough: it may have already produced a result. Applying a result should also verify that it still belongs to the current search and selection state.

The test should control response ordering rather than sleep and hope for a race. Hold response A, finish response B, then release A. Assert that the interface still shows B's choices and preserves a deliberate customer selection. This turns a timing bug into a reproducible behavioral test.

## Conflict assistance

Keep three snapshots: the original accepted record, the current editable draft, and the newly fetched stored record. For each field, compare original-to-draft and original-to-latest. If only one side changed, suggest that change. If both changed to the same value, the choice is straightforward. If both changed differently, ask the user to choose or edit a combined value.

The resolved form is still just a proposal. Send the version attached to the reviewed latest snapshot; never fetch and substitute a newer version immediately before save. Another 409 is a legitimate outcome. Preserve the resolved draft again rather than treating a second conflict as an exceptional impossibility. The [worked customer example](03-WORKED-CHANGE.md) shows why full PUT replacement makes this visible.

## Restoration and historical records

A reasonable policy is to restore only a normally deleted, unmerged ticket, leave its historical messages intact, mark it open, and start a new resolution window at restoration time. That is a proposed product rule, not an existing feature. Another policy can be valid if it is explicit and consistent with reporting.

Authorize the deleted-record lookup before returning its content. Protect the mutation with the record's version. Preserve receipt mappings so a retried old creation cannot become a new ticket. Record who restored it and the previous state in the audit log. Test the policy at the API and service layers; hiding a button does not protect the route.

## Recovery and outbox design

Recovery proposals should capture evidence, not only filenames. A plan created at noon may be stale by the time it is executed. Recheck identifiers, sizes, containment, and reference state before moving or deleting anything. Keep a recoverable copy when the action can destroy the only remaining evidence. The current [read-only audit](../app/storage_audit.py) deliberately stops before that decision.

For an outbox, use one database transaction for the message and delivery intent, then a separate worker transaction for attempts and results. Do not hold SQLite's write lock while waiting for a provider. A unique operation identifier helps avoid duplicate delivery, but external exactly-once behavior requires support from the provider; a local table cannot guarantee it alone.

## Review your final change

A reviewer should be able to answer: What user problem changed? Which records and roles are affected? What happens on invalid input, stale state, duplicate requests, and interruption? How was existing data preserved? Which tests demonstrate the claims? Which limitations remain?

Prefer a short, concrete explanation supported by a few meaningful tests over a large test count that mirrors every assignment statement. Include before-and-after examples and a reproducible command. That is the difference between code that happens to work on your screen and a change another engineer can confidently maintain.
''',
'07-TRACE-LAB.md':r'''# Trace lab: explain accepted, rejected, and uncertain operations

This lab connects the interface, server, database, and filesystem. Use the explicit disposable demo setup from [the project README](../README.md). Keep developer tools open and use synthetic content. Record request metadata without saving authentication cookies or tokens in your notebook.

## Trace A: a normal ticket creation

Create a new customer in Administration, then create a ticket for that customer in Staff workspace. In the network panel, identify the POST to `/tickets`, its JSON body, and its UUID `Idempotency-Key`. Find the corresponding code in [app.js](../app/static/app.js), `ticket_create` in [main.py](../app/main.py), and [receipts.py](../app/receipts.py).

Write down the order: validate the payload, look up the receipt, resolve references, create the ticket and initial message, run matching automation, store the receipt, commit, and return the result. Find where the request's write transaction begins. Explain why the ticket number and receipt lookup happen after obtaining the write position.

Now inspect the returned identifier and number. An identifier is a database key; a ticket number is a human-facing sequence. They need not be equal. Do not hard-code either in application logic or tests that create their own data.

## Trace B: accepted creation with a lost response

Read the lost-response case in [the browser verifier](../verification/verify_browser.py). Its route handler forwards the request to the real local server, waits for that response, and then aborts delivery to the browser. This simulates a specific failure: the server accepted the operation, but the client did not receive acknowledgment.

Observe that the form retains both the draft and its operation key. A retry with the same content returns the original ticket, and the server-side search still finds one matching ticket. Changing the draft while retaining that key should conflict. Starting a separate submission is explicit because it can create another ticket.

Draw two timelines, one for the server and one for the browser. Mark the commit on the server timeline and the connection interruption on the browser timeline. This makes it clear why a client-side error cannot prove that no server-side change happened.

## Trace C: an internal attachment

As staff, add an internal note with a small text file. Follow `ticket_note`, `add_message`, and [save_attachments](../app/attachments.py). The file is read in bounded chunks, written under a generated blob name, flushed, and associated with an attachment record. The original filename remains display metadata and is not used as a filesystem path.

Download the file and inspect the response headers. The route checks the ticket's visibility, the message kind for customers, and whether the stored path is contained in the configured upload directory. It returns the file as a download with an octet-stream content type. A customer must receive a rejection for an internal attachment even if they know its identifier.

Next read the rollback-injection test. A file can be written before later transaction work fails. The rollback listener removes only newly tracked blob paths. Explain the remaining crash window and why [the storage audit](../app/storage_audit.py) lists potential orphans without deleting them automatically.

## Trace D: pending, reply, and deadline changes

Place a ticket in pending status. Inspect the paused timer metadata and cleared active deadlines. Have the customer reply, then inspect the reopened status and new next-response deadline. Have staff reply and verify that the outstanding response deadline is cleared.

Trace the ordering in `public_reply_state` and `refresh_sla`. Paused timers must be resumed before applying the new reply's deadline effects; otherwise a restored old deadline can overwrite the correct new result. Read [the focused timer regressions](../tests/test_reply_timers.py) and explain the deliberately different expected outcome for a customer reply and a staff reply.

Finish with a one-page explanation of one accepted operation, one rejected operation, and one uncertain operation. Include the invariant, transaction boundary, user-visible result, and supporting test for each. If you can do that without relying on vague phrases such as “the framework handles it,” you are practicing the reasoning this project is designed to teach.
''',
'VERIFICATION.md':r'''# Verification record and practical limits

The implementation is being checked with isolated Python tests, actual local browser workflows, rendering probes, and setup/package checks. This file is finalized with exact results before delivery. A test that has been written but has not completed is not counted as passing.

## Evidence available during the implementation

The complete backend run named `full-01` passed 154 tests. It covers the original ticket workflows as well as contract boundaries, authentication parsing and expiry, calendar arithmetic, migration preservation and rollback, scoped visibility and reports, intake receipts, customer/history behavior, configuration CRUD, attachment access and rollback cleanup, and explicit setup/storage audit. Its pytest time was 411.14 seconds in this Windows environment. The surrounding command completed successfully with exit code zero.

After that run, review found an ordering issue when resuming paused response timers during a reply. The focused [timer tests](../tests/test_reply_timers.py) were added with a correction. Their result and the accompanying regression run are recorded below when complete. The earlier complete run is evidence for the version it executed; it is not presented as proof of a later untested edit.

The real browser verifier is [verification/verify_browser.py](../verification/verify_browser.py). It provisions a new demo data directory, starts its own loopback server, exercises administrator, staff, anonymous intake, and customer workflows, saves screenshots, and stops the server it created. It includes a simulated lost response after accepted intake, stale edits with retained drafts, public replies, a private attachment download, and narrow-screen checks. Screenshot review is performed separately; assertions alone do not establish that a page is readable.

## Reproduce the checks

From the project root, use the virtual environment described in [setup](../README.md):

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe verification\verify_browser.py
.\.venv\Scripts\python.exe verification\verify_rendering.py
```

Each browser verification directory must be new. Set `HELPDESK_BROWSER_OUTPUT` or `HELPDESK_RENDER_OUTPUT` to a new output path when rerunning. The scripts refuse to overwrite an existing verification directory. `ASTRA_BROWSER_EXECUTABLE` optionally selects an already installed Chromium executable; otherwise Playwright uses its installed browser. These tools do not need a real email provider or a live customer account.

## Limits that remain part of the learning design

This is a local SQLite application. It has no production deployment configuration, distributed writer coordination, external email delivery, automated worker scheduling, account invitation service, password reset service, or provider-backed identity verification. The explicit demo uses known credentials and belongs in a disposable loopback dataset. Owner setup avoids those demo identities.

SQLite transaction tests and consistent backups do not certify behavior under every power-loss or filesystem failure. Ordinary request rollback removes tracked new uploads; abrupt process termination can leave orphan files, which the read-only audit reports. Attachments are bounded and downloaded rather than rendered, but there is no malware scanning service.

In-memory drafts survive handled errors and conflict review while the page stays open. Navigation prompts reduce accidental loss; they are not persistent offline storage. Review snapshots can themselves become stale, so a subsequent save may legitimately conflict again. Administration uses full replacement, and users must review retained fields before accepting a newer version.

Configuration reference selectors display bounded result sets. The staff customer lookup supports searching to narrow its first hundred results. Unknown legacy database layouts are refused for manual review rather than automatically rewritten. Historical onboarding pages describe the original implementation and link to this current course; they should not be treated as current setup instructions.

Final result placeholders: focused timer/regression run pending; browser run and screenshot review pending; final rendering probe pending; clean setup/package validation pending. These placeholders must be replaced with actual outcomes before this project is marked delivered.
'''
}
for name,text in docs.items():
    (course/name).write_text(text.strip()+'\n',encoding='utf-8')
for path in (root/'docs/onboarding').rglob('*.md'):
    text=path.read_text(encoding='utf-8')
    relative=os.path.relpath(course/'README.md',path.parent).replace('\\','/')
    if not text.startswith('> Historical original-code notes.'):
        path.write_text(f'> Historical original-code notes. Setup, transaction handling, request contracts, and UI behavior have changed. Use the [current learning course]({relative}) for the improved implementation.\n\n'+text,encoding='utf-8')
print({name:len(text.split()) for name,text in docs.items()})
