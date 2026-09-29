"""Write source-linked junior SWE courses for the ten implemented changes."""
from pathlib import Path
import json,re
BASE=Path(__file__).resolve().parent/'stage'
NAMES=json.loads((BASE.parent/'projects.json').read_text())
COURSES=[
dict(title='Task Board: persistent undo',focus='identity, immutable updates and atomic local persistence',source='app.js',test='test/undo.test.cjs',symbol='commitBoard',
 flow=['Delete button passes the task id','deleteTask finds the record and its original index','commitBoard writes tasks and the deleted record together','render updates the cards and undo availability','loadBoard restores the saved recovery record after reload','undoDelete reinserts the same identity and consumes recovery once'],
 model='The v2 document is {version: 2, tasks: [...], deleted: {task, index} | null}. A legacy array becomes a document with deleted: null. The task id is stable across delete and restore; its array position is not its identity.',
 before='Deletion previously filtered the task out and saved the smaller array. The information needed to reverse deletion was lost.',
 after='One localStorage value now holds both the visible tasks and the most recent deleted task. Delete and undo persist before publishing their new in-memory state. Undo clears old filters so the restored task is visible.',
 example='Start with task ids [a, b, c]. Delete b: visible ids become [a, c] and recovery stores b at index 1. Reload. Undo: ids become [a, b, c], and recovery becomes null. A second undo changes nothing.',
 concept='An inverse operation needs enough information to reconstruct the prior intent. Saving just an id would not restore the title, date or notes. Saving the entire old array would be equally troublesome: undo could erase a task added after deletion. Keeping one deleted record and its insertion position preserves unrelated work. This is a small command-history design, not a full event log. The product policy is deliberately one-level undo: deleting c after deleting a replaces the recovery record for a. A stack of multiple deletions is a separate exercise. localStorage writes one string atomically; two separate keys would allow a task list and an undo record to disagree if the second write failed. Publishing the UI only after a successful write makes the failure behavior easy to reason about.',
 exercises=['Add an accessible announcement that names the restored task.','Add a two-level undo history while preserving unrelated edits.','Handle malformed saved JSON without silently overwriting the original value.','Design a multi-tab conflict policy for two tabs deleting different tasks.'],
 answers=['Use the existing role=status element and the saved task title; assign textContent rather than interpolate user text into HTML.','Store a bounded array of {task,index} entries in the same document; push on deletion and pop only after a successful restore write. Test two deletions, two restores and an intervening edit.','Catch parsing separately from writing, show a recovery message, and offer export/reset choices. Keep the corrupt raw value until the user chooses recovery.','The current app has last-writer-wins localStorage. A storage event can detect changes, but a read-then-write is not a compare-and-swap transaction. Describe conflict detection before claiming true multi-tab safety.']),
dict(title='Contact Book: duplicate-email validation',focus='normalization, validation and edit identity',source='app.js',test='test/duplicates.test.cjs',symbol='saveContact',
 flow=['The form submits a contact payload','saveContact trims required fields','A normalized email is compared with other records','The edited record is excluded by id','A duplicate focuses the email field and stops before mutation','A valid create/update is saved and rendered'],
 model='A contact has id, name, email, phone, company and relationship. Email comparison uses trim().toLowerCase(), but the displayed email retains the user’s spelling. The unique key for editing remains id, not email.',
 before='The form checked required fields but allowed two contacts with the same email. A naive uniqueness check would also reject an unchanged email while editing its owner.',
 after='Creates and edits reject case-insensitive, whitespace-normalized duplicates in another record. The message identifies the existing contact, marks the email invalid for assistive technology, focuses it, and leaves stored data unchanged.',
 example='Ada owns Ada@Example.com. Creating Other with " ada@example.COM " fails. Editing Ada’s phone while keeping Ada@Example.com succeeds. Changing Bob’s email to ADA@example.com fails.',
 concept='Normalization and validation answer different questions. Normalization chooses a comparison form; validation decides whether a candidate obeys a rule. Lowercasing here is a documented address-book policy, not a claim that every email provider treats all addresses identically. Do not add provider-specific dot removal or plus-address stripping: those transformations would merge potentially distinct addresses. The self-exclusion rule is the central edit insight: an existing contact is not a duplicate of itself. Comparing ids makes that distinction reliable even if the user changes the name or email. A useful validation error protects data and helps the person recover; a red outline alone is insufficient. The current array scan is linear in contact count, which is appropriate for this small local directory. A server-backed version would also require a database uniqueness strategy because two concurrent requests can both pass an application-only check.',
 exercises=['Clear the duplicate message when the user corrects the address, without hiding unrelated errors.','Add a case-insensitive company filter without mutating stored company names.','Implement a duplicate-review screen for legacy contacts already sharing an email.','Design the corresponding server-side uniqueness constraint.'],
 answers=['Track the error’s field/type rather than clearing every message on every keystroke; keep aria-invalid synchronized with that error.','Normalize the search query and a temporary comparison string. Store the original company for display and editing.','Group contacts by the same comparison policy, show the records, and let the user choose a merge. Never silently delete a record because its email collides.','Use a normalized email column or expression index with a documented collation/policy. Catch the uniqueness violation and translate it into a helpful conflict response.']),
dict(title='Focus Timer: elapsed time and state machines',focus='deadlines, delayed callbacks and one-time completion',source='app.js',test='test/timer.test.cjs',symbol='tick',
 flow=['Start records a deadline and schedules one interval','Each callback reads deadline minus Date.now()','The UI rounds remaining seconds upward for display','Pause captures the exact fractional remainder','Resume builds a new deadline from that remainder','Completion clears scheduling and moves out of running before logging'],
 model='The timer has mode (idle/running/paused), remaining seconds, deadline milliseconds, duration seconds and intervalId. Session records are separate persisted history. A running timer is in-memory; page reload does not resume an active run.',
 before='Each interval callback subtracted one second, so a throttled background tab could show a large amount of time remaining even after the session’s real duration had elapsed.',
 after='The interval is a wake-up mechanism. The deadline determines remaining time. Delayed callbacks catch up, pausing preserves fractions of a second, repeated starts do not stack intervals, and late callbacks cannot log the same completion twice.',
 example='A 60-second session starts at t=0. The browser delays callbacks until t=45: one tick must display 00:15, not 00:59. At t=75 the next tick completes once. If paused at 1.25 seconds, 58.75 seconds remain; a two-minute pause does not consume them.',
 concept='Scheduled callbacks are opportunities to run code, not a guarantee about elapsed time. Tabs can be throttled and the event loop can be busy. The equation remaining = max(0, (deadline - now) / 1000) separates measurement from scheduling. Keep fractional seconds internally and round only at the display boundary; rounding the stored remainder on every pause would let repeated pauses add time. The mode guard is an idempotency mechanism: after the first completion leaves running, another queued callback becomes harmless. Date.now is a wall clock and can jump if the system clock changes; this implementation fixes delayed-callback drift, not every possible clock-adjustment problem. A monotonic performance clock or a persisted wall-clock deadline each has different tradeoffs. The lesson is to state the clock assumption and test the failure mode you actually promised to fix.',
 exercises=['Add a five-minute break phase with exactly one transition from focus.','Persist a running timer across reload and specify how downtime counts.','Replace the clock with an injectable monotonic clock for an in-tab-only timer.','Add a test that repeatedly pauses at fractional-second boundaries.'],
 answers=['Extend the mode/state model explicitly; do not start a new interval from render. Record which phase completes before scheduling the next phase.','Store phase, deadline and original duration. On load compare the deadline with now and choose resume or completion according to a documented product policy. Test an expired deadline.','Pass a now function into the timer logic. performance.now values are meaningful only within the page’s time origin, so they cannot be blindly persisted across reload.','Advance a fake clock by noninteger seconds and verify elapsed active time, not the number of callbacks or pauses, determines completion.']),
dict(title='Finance Dashboard: validated expense editing',focus='form modes, stable identities and derived totals',source='app.js',test='test/expense-edit.test.cjs',symbol='editExpense',
 flow=['The ledger Edit button passes an expense id','editExpense pre-fills the existing modal and fixes its type to expense','handleEntrySubmit constructs and validates a candidate','A new state replaces only the matching expense while retaining its id','Storage succeeds before state is published','render derives totals and charts from the updated state'],
 model='The saved document contains expenses, incomes, budgets, bills, goals and investments. An expense has id, owner, date, category, description and amount. Editing changes its fields, not its id or the number of expenses.',
 before='Expenses could be added and deleted, but there was no edit action. The shared submit handler also accepted some malformed amounts without useful feedback.',
 after='The existing modal supports an expense-edit mode with prefilled values, positive finite two-decimal amounts, real calendar dates and nonblank descriptions. Failed validation or storage keeps the original expense and the editor open. Totals continue to be derived from state.',
 example='The fixture contains one $10.00 expense and no paid bills. Edit it to $12.50. There must still be exactly one expense with the same id, monthly spending must be $12.50, and reload must retain $12.50. Trying -1 or 1.001 must leave $10.00 unchanged in a fresh fixture.',
 concept='Create and edit look similar in the UI but have different identity semantics. Reusing a form is reasonable only when its mode is explicit. A new id on edit would turn an update into an accidental duplicate; replacing the entire expense array with a one-record array would erase unrelated data. The map operation expresses a precise replacement. Deriving totals avoids a second state variable that can become stale after editing. Persistence-before-publish is used on the new edit path so storage failure does not pretend success. Existing add and other dashboard workflows have their own behavior and are not a general transactional storage engine. Amounts remain JavaScript numbers in this educational app; validation limits decimal places, but robust financial systems commonly use integer minor units or decimal arithmetic. This exercise is about software state and validation, not financial advice.',
 exercises=['Display an explicit saved confirmation after an edit.','Add a category-change regression that checks both category and overall totals.','Refactor create and edit to share a storage-first commit helper.','Migrate expense amounts to integer cents with a versioned saved-data migration.'],
 answers=['Use a persistent role=status message outside the modal; announce the expense description and avoid relying on the closed dialog.','Move a fixture from Food to Travel and assert Food decreases, Travel increases and total spending stays the same.','Construct a complete candidate state for each operation and centralize the write-before-publish step; keep form-specific validation near the form boundary.','Define a storage version, convert existing decimal amounts once with explicit rounding, and test 0.10 + 0.20 = 30 cents. Preserve a backup before migrating real data.']),
dict(title='Recipeweb: editable shopping quantities',focus='React state ownership, storage validation and accessible controls',source='src/store/shoppingState.ts',test='test/shopping-state.test.ts',symbol='normalizeShoppingState',
 flow=['ShoppingListPage reads shared shopping-list context','Each ingredient has a stable slug:index key','A labeled text input sends a quantity override to setQuantity','Normalization retains only known recipe/ingredient keys','The provider saves the state to localStorage','Display and clipboard both use ingredientsWithQuantities'],
 model='Shopping state contains recipeSlugs, checked and quantities. Quantity overrides are strings keyed by slug:index. An absent override uses the source recipe quantity; an explicit empty string means the shopper intentionally removed the quantity text.',
 before='The shopping list persisted recipe selection and checkmarks, but quantities came only from recipe data and could not be adjusted. Storage checking was shallow.',
 after='Shoppers can edit quantities using labeled keyboard-accessible controls. Overrides persist, removal cleans up stale keys, and copied text uses the same effective quantities as the screen. Old saved selections/checkmarks are retained and malformed keys are removed.',
 example='The source ingredient says "1 cup". Change it to "2 1/2 cups" in the shopping list. Reload and copy the list: both still say "2 1/2 cups". The source recipe continues to say "1 cup". Remove the recipe and its override disappears.',
 concept='The cookbook is reference data; the shopping list is user state. Mutating the recipe’s ingredient array would mix those responsibilities and could change the recipe-detail screen unintentionally. A keyed override is smaller and preserves the source. Quantity strings are intentionally not automatically parsed or scaled because values can contain fractions, ranges, package sizes and phrases such as "to taste". The nullish-coalescing operator matters: override ?? original respects an empty string, while override || original would silently restore text the user cleared. TypeScript checks source code at compile time, but JSON from localStorage is unknown runtime data, so normalization is still required. A pure normalization function is easy to test without mounting React; interaction and keyboard checks then verify the wiring around it. Storage failure is disclosed rather than hidden behind a claim that progress was saved.',
 exercises=['Add a reset-to-recipe-quantity button beside each override.','Add a recipe-level servings multiplier only for an explicitly supported numeric format.','Test removal and re-adding a recipe without resurrecting its old checkmarks.','Add cross-tab synchronization with a stated conflict policy.'],
 answers=['Delete the override key rather than assign an empty string. Empty is a valid explicit override; absence means fallback.','Introduce a structured quantity model for the supported subset and leave unparseable quantities unchanged with clear feedback. Never multiply arbitrary strings by guessing.','Remove the slug and every slug:index entry from both checked and quantities, then add the recipe again and assert source quantities and unchecked state.','Listen to storage events, normalize incoming data, and define whether a local in-progress edit wins. Synchronization alone does not solve concurrent-edit conflicts.']),
dict(title='Daybook: validated application backups',focus='runtime schemas, atomic imports and asynchronous write ordering',source='src/jobBackup.js',test='test/jobBackup.test.js',symbol='parseJobBackup',
 flow=['Export serializes the displayed applications with a versioned envelope','Import reads a bounded JSON file','parseJobBackup validates every application and rejects duplicate ids','The operation joins the existing write queue','commitJobBackup writes one complete application-array value','Only a successful write replaces React state; calendar data is separate'],
 model='The exchange format is {format: "daybook.jobs", version: 1, applications: [...]}. The stored application key remains jobtracker:data and contains an array. Calendar events use timetrack:events and are not part of this applications-only backup.',
 before='The local app persisted edits but had no validated application backup flow. A naive importer could replace good data before discovering that a later record was invalid.',
 after='The application section exports a versioned JSON backup and imports it as an explicitly labeled replacement. It validates field types, bounded lengths, ids, status, dates and URLs before writing. A failed parse or rejected host write leaves the displayed applications unchanged.',
 example='A backup with a valid Acme application followed by another record with the same id is rejected as a whole. The storage set function must not be called. A valid two-record backup is written once; importing it again still yields two records with their original ids.',
 concept='A file is an input boundary, even when the user exported it from their own computer. JSON.parse proves syntax, not meaning: an array of numbers is valid JSON but is not an application list. The envelope distinguishes this format from calendar data and gives future migrations a version to branch on. Validation completes before persistence, so invalid row 500 cannot leave the first 499 rows saved. Atomicity here is one key-value write: the browser shim uses localStorage.setItem. A custom host must honor that operation’s contract; a host that writes and then falsely rejects cannot be repaired by client-side promise handling alone. The existing write queue prevents an earlier asynchronous edit from finishing after import and overwriting it. The import UI is disabled while the replacement is in progress. Import is replacement rather than merge, which is explicitly stated beside the file input.',
 exercises=['Add a preview showing imported count before replacement.','Support merging backups with an explicit duplicate-id conflict rule.','Add a separate calendar-backup format and validator.','Test an old queued edit followed by a successful import using deferred promises.'],
 answers=['Parse into a temporary preview value and commit that exact validated value only after the user chooses replacement; keep the existing list until then.','Define whether identical ids are skipped, replaced or reviewed. Preserve ids and make replay deterministic; generating new ids during import causes duplicates.','Use a different format identifier and validate event-specific fields such as title, date, start/end and done. Do not call an applications backup a full Daybook backup.','Control when each fake storage promise resolves. Assert import is scheduled after the old write and final UI/storage contain the imported records.']),
dict(title='Task Manager API: a complete CRUD boundary',focus='HTTP contracts, service validation and real SQL persistence',source='server/src/services/taskService.js',test='server/test/tasks.test.cjs',symbol='buildUpdatePayload',
 flow=['React submits a task payload through its API service','Express routes select the controller','The controller delegates to taskService','Validation normalizes supported fields and rejects invalid input','taskModel writes with Knex and returns the stored row','The client refreshes tasks and stats from API responses'],
 model='A SQL task includes id, title, description, priority, status, due_date and completion timestamps. The database id is a positive integer. A partial update distinguishes an omitted field from a supplied null or value.',
 before='The project already had CRUD routes and validation. It lacked executable regression coverage for the complete path, allowed unsafe integer ids and overlong titles to reach deeper layers, and could reject editing an overdue task when its unchanged date was resubmitted.',
 after='The API rejects unsafe ids and titles longer than the database column. An unchanged existing due date remains editable; new or changed due dates still follow the future-date rule. Tests call real HTTP routes and inspect PostgreSQL rows, including completion timestamps and deletion.',
 example='Create a high-priority task due 2099-01-01, filter for high priority, mark it done, reopen it and delete it. Separately seed a task due 2020-01-01: editing its title with that same due date succeeds, but changing it to another past date fails.',
 concept='Each layer has a specific responsibility. A route chooses which operation handles a URL; a controller adapts HTTP input/output; a service enforces rules; a model issues SQL. Following one request is easier than reading every file alphabetically. The database is still the final authority for constraints, but expected bad input should produce a useful client error before a database exception. Number.isSafeInteger rejects values JavaScript cannot represent precisely; Number.isInteger alone is insufficient. Updates require context: the rule for setting a new due date should not prevent maintaining an already-overdue task. The unchanged-date exception is therefore narrow and compares against the stored date. The date column is a calendar date, so normalize it to YYYY-MM-DD instead of comparing display-formatted strings. Real HTTP-plus-database tests prove more than a mocked service test, but they still do not prove that every browser interaction is correct.',
 exercises=['Add a task title search filter with bound SQL parameters.','Test clearing an optional due date without changing the title.','Add optimistic concurrency for two users editing the same task.','Trace a server validation message into the client form and improve its wording.'],
 answers=['Validate a bounded search string in the service and use Knex where/whereILike binding rather than interpolating raw SQL. Test a quote and a percent sign according to the search policy.','Submit due_date:null and assert the stored column becomes null while omitted fields retain their values.','Add a version field, update only where id and expected version match, and return a conflict when no row matches. Test two updates based on the same version.','Follow apiClient → useTasks → form/page error rendering. Preserve a useful domain message and avoid exposing database internals.']),
dict(title='Contact Book API: atomic CSV import',focus='parsing state machines, batch validation and transactions',source='server/src/utils/csv.js',test='server/test/import.test.cjs',symbol='csvToContacts',
 flow=['The import endpoint receives CSV text','csvToContacts tokenizes quoted fields and validates headers/row widths','The service validates every contact and tag name','importContactBatch opens one transaction','Contacts, tags and junction rows are written through that transaction','A failure rolls everything back; success returns the created batch'],
 model='Contacts and tags have a many-to-many relationship through contact_tags. CSV headers are a supported allowlist; first_name and last_name are required. The tags field uses pipe-separated names. Email uniqueness also exists in PostgreSQL.',
 before='The old parser split lines and commas directly, corrupting quoted commas and multiline fields. Import inserted one contact at a time, skipped some invalid rows and did not make the whole batch atomic.',
 after='The parser supports quoted commas, doubled quotes, multiline text, CRLF and a BOM. It rejects malformed quoting, duplicate/unsupported headers and inconsistent field counts. The complete batch is validated before a single transaction writes contacts and tags. A late uniqueness failure rolls back earlier rows.',
 example='Import a company "Labs, Inc." and notes containing a newline and the words She said "hello". The stored strings must be intact. In another batch, insert a new email and TemporaryTag, then repeat that email in row two: no contact or TemporaryTag from that batch may remain.',
 concept='CSV looks like a string-splitting problem until a delimiter appears inside a value. Quoting changes how the next character must be interpreted, which makes a small state machine a good fit. Inside quotes, a newline belongs to the field; outside quotes, it ends a record. Two quotes inside a quoted field represent one literal quote. Parsing and domain validation are separate: a record can be syntactically correct CSV and still lack a required surname. Database constraints are a third boundary because a concurrent writer or existing email can invalidate an otherwise valid batch. All writes must use the transaction object; accidentally calling the global db for tag creation would let a tag survive rollback. Import is atomic, not globally idempotent: reimporting an existing non-null email fails as a whole, while contacts without unique emails can still be duplicated. Pagination also needs a stable id tie-breaker when many contacts share a surname.',
 exercises=['Return a preview of row errors without writing any data.','Define a duplicate-email import policy that supports deliberate updates.','Add a quoted carriage-return round-trip fixture.','Investigate CSV spreadsheet-formula handling for a separate export policy.'],
 answers=['Keep parsing and validation pure, collect bounded row-numbered errors, and reserve the transaction for a separately confirmed valid batch.','Choose skip/update/reject explicitly. An upsert must specify which fields may change and what happens to tags; do not silently reinterpret an import as destructive replacement.','Include a quoted field containing a carriage return and verify export quotes it and import preserves its content.','A spreadsheet may evaluate a leading =, +, - or @ even when CSV quoting is correct. Define whether this app exports raw data or spreadsheet-safe text and test that policy independently from CSV syntax.']),
dict(title='Expense Tracker API: trustworthy reports',focus='aggregation, calendar boundaries and deterministic fixtures',source='server/src/models/expenseModel.js',test='server/test/reports.test.cjs',symbol='byCategory',
 flow=['Stats routes receive a month or date range','The service validates month/date/filter input','The model selects only grouped fields and aggregates','PostgreSQL computes sums and counts over the selected window','The controller returns the success envelope','The client renders totals and chart series'],
 model='Each expense belongs to one category and has a date and decimal amount. Monthly windows are half-open: first day inclusive, next month’s first day exclusive. Category range filters currently include both supplied start_date and end_date.',
 before='The category report reused a base query that selected expenses.* and then added GROUP BY categories.id. PostgreSQL cannot choose an arbitrary expense row for each category, so that report could fail. Date filters and amount edge cases also needed validation.',
 after='The category query clears the base projection before selecting category fields, SUM and COUNT. Report inputs reject malformed months, impossible dates and reversed ranges. The test fixture proves monthly, daily and category results agree at leap-day and month boundaries.',
 example='For February 2024 use Food 10.10 on Feb 1, Food 20.20 on Feb 29 and Travel 4.70 on Feb 15. Put 99 on Jan 31 and 777 on Mar 1. February total is 35.00 across three expenses; Food is 30.30 and Travel is 4.70. Adjacent-month rows must not leak in.',
 concept='A grouped query changes the meaning of a row. Before grouping, a row represents an expense. After grouping by category, it represents a category summary. Raw expense fields no longer have one well-defined value, which is why clearing the inherited SELECT list is necessary. A hand-calculated fixture is a stronger oracle than comparing two functions that share the same bug. The leap-day case makes the time boundary concrete; using a fixed 30-day month would be wrong. Half-open ranges compose cleanly because a boundary date belongs to exactly one month. PostgreSQL decimal columns preserve decimal arithmetic during aggregation, while the API currently casts results to floating-point numbers; tests compare currency totals carefully, and a future money-model exercise can return integer cents or decimal strings. Empty datasets must produce stable zero totals rather than null values that confuse the UI.',
 exercises=['Add a year-to-date summary with an explicit end boundary.','Make an empty category appear with zero spending using a LEFT JOIN.','Test a week that crosses December into January.','Return report amounts as integer cents without changing displayed values.'],
 answers=['Define inclusive/exclusive semantics first, then seed rows just before, inside and at the excluded boundary. Use SQL date operations rather than a fixed day count.','Start from categories and place expense date predicates in the join condition; a WHERE filter on the optional expense row can accidentally turn the left join into an inner join.','Use fixed dates spanning the year boundary and assert exactly seven calendar dates are eligible under the half-open interval.','Convert at a clearly documented boundary, avoid repeatedly rounding intermediate values, and update API types and chart formatting together.']),
dict(title='Recipe Manager: ownership and transactional graphs',focus='authentication versus authorization, runtime validation and rollback',source='server/src/services/recipeService.ts',test='server/test/ownership.test.ts',symbol='updateRecipeForUser',
 flow=['The auth middleware verifies the access token and supplies a user id','The service opens a transaction for replacement','The recipe row is locked and its owner is checked','parseRecipeInput validates every ingredient and step','saveRecipeGraph replaces parent and child rows through the transaction','Commit publishes the graph; a later failure restores the original graph'],
 model='A recipe belongs to a user and has ingredients, steps and category links. Authentication identifies the caller. Authorization compares that caller with the stored owner. A graph replacement must commit the recipe and every dependent row together.',
 before='Ownership checks and transactions already existed, but the update ownership read happened outside the replacement transaction. Input parsing filtered some invalid child records instead of rejecting them and could throw ordinary TypeErrors for malformed values.',
 after='The update locks and checks ownership within the transaction. Nested input is validated without silently dropping invalid children. The model update also scopes by owner. Real HTTP tests deny a signed-in nonowner, and real foreign-key failures prove both create and replacement rollback.',
 example='Alice creates a private Soup recipe with Water and a Boil step. Bob sends a valid token and a body claiming Alice’s user_id: the update must still fail with 403. Alice then attempts a replacement with a nonexistent category id; after failure, the original title, ingredient ids and steps must still exist unchanged.',
 concept='Being logged in is not permission to edit every record. The trusted caller identity comes from the verified token, while the ownership fact comes from the stored recipe; neither should come from a body field supplied by the caller. A row lock keeps the authorization read and replacement coordinated with competing writes. It does not provide an automatic user-facing merge strategy: two authorized sequential updates can still replace one another unless a version policy is added. Runtime validation is required even with TypeScript because an HTTP body is untyped external data. Silently removing blank ingredients can turn an apparently complete request into an empty recipe, so each nested element is rejected with a domain error instead. The rollback test intentionally fails late, after parent/child writes have begun, using a foreign-key constraint. An early validation-only test would not prove transaction atomicity.',
 exercises=['Add version-based conflict detection for concurrent owner edits.','Return field-path validation errors such as ingredients[2].name.','Add an ownership regression for private favorites.','Test rollback when replacing both steps and categories fails late.'],
 answers=['Accept an expected version and condition the update on it inside the transaction; increment on success and return a conflict for a stale version. A row lock alone does not tell the client that its edit was stale.','Carry the array index into validation helpers and collect a structured path/message; keep errors free of SQL or secret data.','Create a private recipe, authenticate a different user and call favorite; assert denial and no favorites row.','Snapshot all child tables, force a late FK/constraint failure through a valid-shaped payload, and compare the complete graph after rollback, including original ids.']),
]

def source(n,path):return (BASE/n/path).read_text(encoding='utf-8')
def excerpt(text,symbol,limit=85):
 lines=text.splitlines();start=next((i for i,l in enumerate(lines) if re.search(r'\b'+re.escape(symbol)+r'\s*\(',l) and ('function ' in l or 'const ' in l)),0)
 end=min(len(lines),start+limit)
 for i in range(start+1,end):
  if re.match(r'^(?:export )?(?:async )?function\s',lines[i]):end=i;break
 return '\n'.join(lines[start:end]),start+1
def write(n,file,text):
 p=BASE/n/'astraupskill'/file;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')

for i,c in enumerate(COURSES,1):
 n=f'{i:02}';name=NAMES[i-1]
 testcmd='npm test' if i<=6 else 'cd server\nnpm test'
 setup='Open index.html directly in a browser for the app. For the automated DOM tests, run `npm install`, then `npm test` from this project folder.' if i<=4 else ('Run `npm install` and `npm run dev` from this project folder. Run `npm test` for its automated checks and `npm run build` for the production build.' if i<=6 else 'Install dependencies separately in `server` and `client`. Follow the root README and `.env.example` for the development database and ports. Run migrations only against your chosen development database. The regression tests use a separate database through `ASTRA_TEST_DATABASE_URL`; see chapter 4.')
 code,line=excerpt(source(n,c['source']),c['symbol']);tests=source(n,c['test'])
 lang='typescript' if c['source'].endswith(('.ts','.tsx')) else 'javascript'
 links=[('01-CODEBASE-MAP.md','Codebase map and reading order'),('02-CONCEPTS.md','Concepts explained from first principles'),('03-WORKED-CHANGE.md','Worked implementation and examples'),('04-TESTING-AND-DEBUGGING.md','Tests, failure cases and debugging'),('05-PRACTICE.md','Guided and independent exercises'),('06-SOLUTIONS-AND-REVIEW.md','Solutions, tradeoffs and review rubric'),('VERIFICATION.md','Actual verification results and limits')]
 write(n,'README.md',f'''# {c['title']}

This is a hands-on course for a junior software engineer using the actual project in `{name}`. The central skill is **{c['focus']}**. The implementation is already present: use it as a worked example, then recreate a small variation independently.

## What you will be able to do

- Explain the purpose of the changed code and the data it owns.
- Trace an action from input through validation, state/persistence and output.
- Predict a success case and a failure case before running either.
- Read the regression tests and explain what each assertion proves.
- Implement a related change without copying the worked answer.
- Explain a limitation and a reasonable next step without overstating readiness.

## Prerequisites

Be comfortable with variables, arrays, objects, functions, conditionals and calling a function. For React projects, review props, state and event handlers. For API projects, review JSON, HTTP methods and promises, then learn the relevant SQL operations as you trace the request. You do not need to memorize the whole repository first.

## Start the project

{setup}

The commands are run from this project’s folder, not from the Desktop inventory repository. Existing README/Fable material remains available. This folder teaches the implemented change and points to executable source and tests rather than replacing older guides.

## Reading and practice order

'''+ '\n'.join(f'{j}. [{title}]({file})' for j,(file,title) in enumerate(links,1))+f'''

## Your first session

1. Open the app or its tests and reproduce one normal workflow.
2. Read chapter 1 while keeping [{c['source']}](../{c['source']}) open.
3. Write a prediction for the worked example in chapter 3 before executing it.
4. Run the focused test suite and explain one assertion aloud.
5. Complete the first practice exercise, then check the solution discussion.

Keep a short learning log with four fields: prediction, observed result, explanation and next question. A mismatch is useful evidence: find the exact layer where your mental model diverged from the program. Use a disposable browser profile or local test database for failure experiments so your own records are not part of the fixture.

## Scope

{c['after']} This is one bounded improvement, not certification of every feature. Read VERIFICATION.md for checks actually executed. Exercises are intentionally future practice; do not confuse them with completed implementation.
''')
 extras=[]
 for p in (BASE/n).rglob('*'):
  if p.is_file() and p.suffix in ['.js','.jsx','.ts','.tsx'] and not any(x in p.parts for x in ['node_modules','test','astraupskill','dist']):extras.append(p.relative_to(BASE/n).as_posix())
 write(n,'01-CODEBASE-MAP.md',f'''# Codebase map and reading order

[Course index](README.md)

## The problem this project solves

{c['before']} The improvement you will study is: {c['after']}

## Data model

{c['model']}

An object is a named collection of fields. An array is an ordered collection of values. An id answers “which record?”; an index answers “where is it in this array right now?” Those questions are different whenever the list can be filtered, reordered or edited. Persisted data is the form that must survive a process/page restart. Derived data can be recomputed from that persisted state.

## Trace one action

'''+ '\n'.join(f'{j}. {step}.' for j,step in enumerate(c['flow'],1))+f'''

```mermaid
flowchart LR
    A[Input or user action] --> B[Validate and normalize]
    B --> C[Compute intended change]
    C --> D[Persist through the project boundary]
    D --> E[Return or render observed state]
    B --> F[Explain invalid input]
    D --> G[Handle a failed write]
```

This diagram names responsibilities, not necessarily separate files. A small browser program can keep them in app.js. A larger API spreads them across controllers, services and models. Follow the actual sequence above rather than assuming every repository has the same architecture.

## Where to read first

1. [{c['source']}](../{c['source']}): locate `{c['symbol']}` and read its inputs, branches and return/side effects.
2. [{c['test']}](../{c['test']}): read the scenario names before the helper code.
3. The root [README](../README.md): connect setup and the larger application workflow.

## Source navigation

'''+ '\n'.join(f'- [{path}](../{path})' for path in sorted(extras))+f'''

## A practical reading technique

At each function boundary, write down the value coming in, the value going out and any side effect. A side effect includes a storage write, SQL query, network request, timer registration or DOM update. If a function calls another function, inspect only that next dependency until you can finish the chosen trace. Return to unrelated files later.

For this lesson, start with: **{c['example']}** Mark where the id, time, amount or other important value changes representation. For example, JSON serializes values into text; a date field may be a calendar string; SQL aggregates may return a different type from individual rows. Representation changes are common bug locations.

## Check your understanding

Without reading the solution, answer: Who owns the mutable state? Which input is untrusted? Which function first decides whether the operation is valid? What survives reload or restart? What observation would prove that the operation partially failed? Point to a source file for each answer, rather than describing a generic app from memory.
''')
 write(n,'02-CONCEPTS.md',f'''# Concepts explained from first principles

[Course index](README.md)

## The central idea: {c['focus']}

{c['concept']}

## Invariants: a precise way to describe correctness

An invariant is a rule that must remain true before and after an operation. “The app works” is too broad to test. “A failed import writes no records” or “editing preserves the record id” gives you something observable. For this project, derive your invariants from this behavior:

> {c['after']}

Turn each sentence into a small state table. The columns are initial state, input, expected final state and expected feedback. Include one rejected input and one retry/repeated action where relevant. A useful invariant should be meaningful even if the implementation changes from an array to a database or from one UI component to another.

## Validation versus normalization

Validation rejects values the operation cannot accept. Normalization converts acceptable values to the representation the rest of the program expects. Trimming a comparison string is normalization; rejecting an empty required field is validation. Neither operation should silently invent facts. If a quantity is free-form text, do not guess a numerical interpretation. If an imported record is malformed, do not quietly save only the convenient subset unless that is the explicit product policy.

Apply this distinction to the data model:

{c['model']}

Which fields can be omitted? Which can be empty? Which have a bounded vocabulary? Which have stable identity? Write those answers down before adding another conditional. A schema is simply an explicit description of that expected shape and meaning.

## State transitions and failure boundaries

Every change has an ordering. If memory changes first and persistence fails, the UI can show data that will disappear after reload. If persistence succeeds first and rendering fails, the stored data may be correct while the screen is stale. There is no universal answer for every feature, but the choice must be deliberate and observable. The worked change makes one specific promise; the tests check that promise.

A promise represents an operation that completes later. `await` does not make it infallible or atomic; it gives the caller a place to handle success and rejection. Similarly, calling several functions inside one `try` block does not create a database transaction. Atomicity must come from a storage operation or transaction boundary that actually provides it.

## Identity, representation and derived values

Keep a stable id when updating an existing record. Compute display-only values from authoritative data when feasible, so there are fewer independently mutable facts to keep synchronized. Be careful when converting between strings and numbers: `Number('')` is zero, JSON cannot faithfully represent Infinity, and a date string can have different semantics from a timestamp. The specific conversions in this lesson are visible in the worked source, so step through them with a concrete value.

## Small design decisions deserve explanations

Before extracting a new abstraction, explain what repeated responsibility it would own. A helper that merely renames one expression may add little. A pure validator or one transaction boundary can make an important guarantee easier to test. Prefer an explanation tied to this project’s behavior over a rule such as “all code must use a particular pattern.”

Write a short decision note: “We chose X because it preserves Y under Z. It does not yet solve W.” Use the limitations in the worked example to fill in those letters. This is the beginning of engineering judgment: choosing a bounded solution and accurately describing its limits.
''')
 write(n,'03-WORKED-CHANGE.md',f'''# Worked implementation and examples

[Course index](README.md)

## Before and after

**Before:** {c['before']}

**After:** {c['after']}

## Predict this example

{c['example']}

Before running anything, write the exact expected stored values and visible response. Include ids or record counts where they matter. Then run the focused tests and reproduce the matching UI/API action. Do not settle for seeing a success message: inspect the authoritative stored result as well.

## Actual implementation excerpt

The excerpt below comes from [{c['source']}](../{c['source']}) near line {line}. It is a teaching snapshot; the linked source is authoritative if you later edit the project. Read surrounding code for callers and setup.

```{lang}
{code}
```

## How to reason through the code

1. Identify the inputs. Distinguish data supplied by a caller from state read from storage or a trusted context.
2. Find the guard clauses. For each early return or thrown error, describe which invariant it protects and whether anything has already been written.
3. Find the candidate state or query. Explain whether it mutates an existing object or constructs a replacement.
4. Locate the persistence operation. For asynchronous code, follow the promise through success and rejection; for transactions, check that all related writes use the same transaction object.
5. Find the output or state publication. Ask what a repeated invocation would do after the first invocation succeeds.

Use this project-specific reasoning as your guide:

{c['concept']}

## Three variations to work through

**Normal variation:** change one ordinary value in the successful fixture while preserving its shape. Predict which fields should change and which should remain identical. Execute it and explain any difference.

**Invalid variation:** use the invalid case from the tests. Predict the error and the exact number of writes that should happen. Compare the state before and after; error text alone does not prove data integrity.

**Boundary variation:** repeat the action, reload, delay a callback or force a late write failure as appropriate to this lesson. Explain why the boundary differs from the happy path. The test file below contains a concrete example you can adapt rather than inventing an unrealistic failure.

## Executable examples

These are the actual regression tests in [{c['test']}](../{c['test']}). Read each test as arrange → act → assert. Setup creates a controlled initial state, the action exercises the application code, and assertions compare observable behavior with an independently stated expectation.

```{'typescript' if c['test'].endswith('.ts') else 'javascript'}
{tests}
```

## Explain it back

Give a five-minute walkthrough: the original problem, one invariant, the exact changed function, the most revealing failure test, and one remaining limitation. You should be able to explain why the implementation is correct for the worked example without reading the code aloud line by line.
''')
 dbguide='''
## Running the database tests safely

Create a separate local PostgreSQL database whose name starts with `astra_test_`, for example `astra_test_learning`. The tests refuse a differently named database. In PowerShell, set your own local test connection:

```powershell
$env:ASTRA_TEST_DATABASE_URL = 'postgres://YOUR_TEST_USER:YOUR_TEST_PASSWORD@127.0.0.1:5432/astra_test_learning'
cd server
npm install
npm test
```

Replace the placeholders with your local test credentials; they are not application defaults. The user must be able to create a schema in that database. Each run creates a uniquely named schema, runs the existing migrations there, and drops only its own schema after the tests. It does not use the development database’s data as a fixture. If a run is interrupted, a uniquely named test schema may remain; inspect the test database before cleaning it up.

The helper configures the app before importing its database module. That order matters: configuration is captured when modules are loaded. The suite exercises actual PostgreSQL constraints and transaction rollback, rather than substituting a JavaScript array for SQL behavior.
''' if i>=7 else ''
 write(n,'04-TESTING-AND-DEBUGGING.md',f'''# Testing and debugging

[Course index](README.md)

## Run the checks

{setup}

```text
{testcmd}
```
{dbguide}
## What the test suite proves

Read [{c['test']}](../{c['test']}). The suite targets **{c['focus']}** and uses the worked fixture:

{c['example']}

The expectation should not be copied from the function being tested. Hand-calculate counts, amounts, identities or elapsed time first. Otherwise the same mistake can appear in both implementation and expected result. Tests that exercise only a mocked dependency prove a narrower contract than tests against the real dependency; read the helper to understand which kind you are running.

For the plain browser projects, jsdom runs the actual app.js against its HTML. The helper supplies browser APIs missing from jsdom and a controllable timer clock. It does not replace the app’s business functions. A real browser check is still useful for layout, focus visibility and native interaction. For React state helpers, pure tests verify data behavior; component/browser checks verify that controls call those helpers correctly.

## Debugging workflow

1. Reproduce the smallest failing case with the exact input saved in your notes.
2. Inspect the relevant event/request. Confirm the intended handler actually ran.
3. Pause at `{c['symbol']}` and inspect input types as well as values.
4. Follow validation branches, noting whether any state or persistence changed before rejection.
5. Inspect the write result and the subsequent render/response. Separate storage correctness from display correctness.
6. Add a regression reproducing the failure, make the smallest justified fix, then run the focused suite and relevant broader checks.

Avoid changing several layers at once when you do not yet know where the failure starts. A correct backend with a stale UI needs a different fix from a malformed query or an invalid saved document.

## Failure experiments

- Reuse the invalid fixture from the tests and verify no unintended records or fields change.
- Reload or restart after a successful operation to distinguish persistence from temporary screen state.
- Repeat the operation and explain whether it should be idempotent, rejected or intentionally create another record.
- Simulate the relevant timing or storage failure only in a disposable fixture. Restore normal behavior after the experiment.

## Reading an assertion failure

“Expected 3, received 4” is evidence about one observation, not a complete diagnosis. Ask whether the fixture created an extra record, the operation ran twice, an old record survived, or the assertion looked at an unfiltered collection. Start from the state table and trace the first point where the actual value diverges. A stack trace identifies where the program noticed a problem, which may be later than the code that caused it.

## Verification record

The companion [VERIFICATION.md](VERIFICATION.md) records checks actually run for this implementation. Record your own command, date, result and any environmental prerequisite when practicing. A passing test does not imply every route, browser, dependency version or production deployment has been exercised.
''')
 write(n,'05-PRACTICE.md',f'''# Guided and independent practice

[Course index](README.md) · [Solutions](06-SOLUTIONS-AND-REVIEW.md)

## Exercise 0 — reconstruct the existing behavior

Draw the data shape and trace this fixture without running it:

{c['example']}

Write one assertion for success and one for a rejected or failed operation. Then read the existing test and compare its observation with yours. Explain why a message alone would or would not prove the invariant.

## Exercise 1 — guided extension

{c['exercises'][0]}

Start by locating the current input, handler and output. Write an acceptance example before editing. Make one small change, run the focused tests, and demonstrate it through the same public UI/API a user would use. Add one meaningful regression if the behavior can break in a way the existing suite would miss.

## Exercise 2 — independent variation

{c['exercises'][1]}

Close the worked-change chapter while implementing. Describe your design in three sentences: the data you will add or reuse, the rule it must preserve, and the observation that proves it. Compare your answer with the solution only after an independent attempt. If you get stuck, request a hint about the next boundary rather than a complete implementation.

## Exercise 3 — failure-focused extension

{c['exercises'][2]}

Create a failing example in a disposable fixture. Capture the state before the operation and after the failure. Identify what must remain unchanged and what feedback the caller needs. A correct result includes understandable recovery behavior, not just throwing an exception.

## Exercise 4 — stretch design

{c['exercises'][3]}

Write a short design note before coding. List the current guarantee, the stronger guarantee you want and the new failure modes the change introduces. If this requires a larger architectural change, stop at a concrete proposal and test design until you understand the prerequisite. The earlier exercises should remain understandable and runnable.

## Exercise 5 — teach the codebase

Give a five-minute walkthrough to another learner, or record yourself. Use [{c['source']}](../{c['source']}) and one test. Explain the application problem, the data model, the call path, one success case, one failure case and the tradeoff. Ask the listener to predict a new input’s result. Their questions reveal which part of your explanation needs work.

## Exercise 6 — review your own change

Inspect the diff as if you were a teammate encountering it for the first time. Remove unrelated edits. Check names, error feedback, preservation of ids/data, and the order of writes. Update the learning note if the actual code differs from the plan. Record what was tested and what remains an assumption.

## Completion rubric

Score each item 0 (cannot explain), 1 (can explain with help) or 2 (independent): data model, control flow, validation, persistence/failure behavior, regression test design, and tradeoff explanation. Aim for 2 on the first five before taking the stretch exercise. Revisit a weak area with a changed-input example rather than rereading every page.
''')
 write(n,'06-SOLUTIONS-AND-REVIEW.md',f'''# Solutions and engineering review

[Course index](README.md) · [Practice prompts](05-PRACTICE.md)

Attempt each exercise before using these notes. These are solution approaches and review criteria, not claims that every extension has been implemented. The actual completed behavior is described in the worked-change chapter.

## Existing implementation

{c['after']}

The key model is: {c['model']}

The worked fixture should behave as follows: {c['example']}

## Extension solutions

'''+ '\n\n'.join(f'### Exercise {j}\n\n**Prompt:** {prompt}\n\n**Approach:** {answer}\n\n**Review:** Demonstrate an ordinary case and a case that would break a naive implementation. Explain which existing invariant remains unchanged. Keep the code and the learner-facing explanation in agreement.' for j,(prompt,answer) in enumerate(zip(c['exercises'],c['answers']),1))+f'''

## Review questions with answer guidance

**Why not trust input just because it came from this UI?** A caller can bypass the UI, a saved file can be edited, and older data can have a different shape. Validate at the boundary that owns the operation.

**Why keep the id stable?** It identifies the same domain record across views and edits. Changing it can create duplicates, disconnect child records or make reconciliation impossible.

**What makes the failure test meaningful?** It observes the promised state invariant. For this project, explain exactly why the failing scenario in [{c['test']}](../{c['test']}) would detect the original or a plausible regression.

**What does the test not prove?** A bounded suite does not prove all concurrency, browsers, deployment configurations or unrelated domain behavior. Name the real limitation from this lesson instead of adding a generic disclaimer.

**When should you extract a helper?** When it isolates a coherent responsibility, makes an invariant clearer or enables a meaningful test without duplicating application logic. A pure validator and a shared persistence boundary are common examples, but do not abstract solely to increase the number of files.

## A sample change explanation

“The previous behavior was: {c['before']} I changed the implementation so that: {c['after']} The strongest evidence is the regression that exercises the worked fixture and checks authoritative state. A remaining design question is the final stretch exercise.”

Replace that explanation with your own words and actual test results. A strong junior engineer can connect a concrete user problem to code, verification and a clearly stated limit. Completing that explanation independently is the final checkpoint for this course.
''')
 # Add a stable entrypoint without replacing any older tutorial.
 p=BASE/n/'README.md';text=p.read_text(encoding='utf-8')
 if '(astraupskill/README.md)' not in text:p.write_text(text.rstrip()+f'\n\n## Junior SWE learning course\n\n[Start the detailed Astra upskilling course](astraupskill/README.md): {c["focus"]}, with a codebase map, worked implementation, executable examples, debugging labs, exercises and solution discussions.\n',encoding='utf-8')

(BASE.parent/'courses.json').write_text(json.dumps(COURSES,indent=2),encoding='utf-8')
print('Generated 70 detailed learning chapters plus course metadata; verification pages follow executed checks.')
