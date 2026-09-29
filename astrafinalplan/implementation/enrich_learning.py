from pathlib import Path
BASE=Path(__file__).resolve().parent
chapters=[
'''# Trace lab: restoring one deleted task

[Course index](README.md)

## Identity and position are different

An id belongs to a task; an index describes its current position. Start with ids `[a, b, c]`, delete b, and store b's complete object with insertion index 1. The visible list becomes `[a, c]`. Reload and undo should restore `[a, b, c]` and consume recovery once.

```javascript
const index = tasks.findIndex(task => task.id === 'b');
const remaining = tasks.filter(task => task.id !== 'b');
```

This reduced example creates a new array, but retained objects are still references to the old objects. `filter` is not a deep copy.

Now rename c between deletion and undo. Its new title must survive. Restoring an old snapshot of the entire board would erase that edit. Keeping one deleted object restores the intended record without replacing unrelated work.

## Follow the failure branch

Open `commitBoard` in [app.js](../app.js). It serializes tasks and recovery together, writes one storage value, and only then publishes memory state. A `try` block alone is not atomicity: the useful boundary is the single storage operation. Splitting tasks and recovery between two keys would allow the first write to succeed and the second to fail.

Predict a failed undo. The deleted task should remain recoverable, so the user can retry. Run the failure fixture in the test linked in chapter 3 and inspect saved state, not only error text.

One-level undo deliberately replaces the older recovery record when another deletion succeeds. A stack can store more history, but you must still decide whether renames and moves enter that history and what each inverse means. Explain these four distinct safeguards: stable id, insertion position, one storage value, and write-before-publication.
''',
'''# Trace lab: duplicate emails during creation and editing

[Course index](README.md)

## Choose the comparison rule

This app trims outside whitespace and compares lowercase email strings. It preserves display spelling. This is the application's matching policy, not a claim about every email provider's account rules.

```javascript
const key = email => email.trim().toLowerCase();
key(' Maya@Example.com ') === key('maya@example.com'); // true
```

Suppose record 11 contains Maya's email and record 12 contains Lin's. Adding a new record with MAYA@example.com must fail. Renaming record 11 while keeping its email must succeed. Changing record 12 to Maya's email must fail.

```javascript
const duplicate = contacts.some(contact =>
  contact.id !== editingId && key(contact.email) === key(candidateEmail)
);
```

This reduced pattern excludes the current record. Without that exclusion, every unchanged-email edit finds itself and looks like a duplicate. Find the actual implementation and representation of a new-contact editing id in [app.js](../app.js).

## Validate before mutation

A visible error does not prove rejection happened before saving. Compare the contact count and stored values before and after the rejected action. Moving validation after an array mutation would require rollback and complicate the failure path.

The invalid email field receives focus and `aria-invalid`; the message is associated with it. Correct the address and explain where the stale invalid state is cleared. These details help keyboard and assistive-technology users recover.

For a future server, two concurrent requests could both pass an array-like duplicate check. A uniqueness constraint on the chosen normalized representation would provide a separate database safeguard. First understand this local boundary before extending it.
''',
'''# Trace lab: elapsed time is not callback count

[Course index](README.md)

## Hand-calculate a delayed callback

A 60-second session starts at clock 100,000 milliseconds. Its deadline is 160,000. The next callback occurs at 145,000: only 15 seconds remain even if just one callback ran.

```javascript
const deadline = 100000 + 60000;
const remainingMs = Math.max(0, deadline - 145000); // 15000
const seconds = Math.ceil(remainingMs / 1000); // 15
```

Decrementing a counter once per callback would show 59, which describes callback delivery rather than elapsed time. Write units beside every variable: minutes, seconds and milliseconds are different representations.

## Preserve fractional time across pause

Pause at 145,250: there are 14,750 milliseconds left. Resume at 200,000: the new deadline should be 214,750. Paused time must not count. Keep the fractional duration in state even when display text rounds it upward.

Trace interval creation, clearing, pause and resume in [app.js](../app.js). Explain why repeatedly pressing Start cannot create stacked intervals.

## Complete exactly once

A delayed callback and a visibility refresh may both notice an expired deadline. The first completion must leave the running state before another call can append another log. The regression moves the fake clock beyond the deadline and invokes the updater twice; it expects one completion.

A fake clock replaces the time dependency, not the app's business functions. It makes a minute-long scenario immediate and repeatable.

This improvement handles delayed callbacks. It does not preserve an active session across reload or promise protection from system-clock changes. Completed session records retain their existing persistence. A resume-after-reload extension needs a saved state format and a policy for sessions that expired while the page was closed.
''',
'''# Trace lab: expense editing is replacement, not insertion

[Course index](README.md)

## Calculate the expected total

Start with expense e7 for 20 and expense e8 for 30. Edit e7 to 12.50. The ids must remain e7 and e8; the total changes from 50 to 42.50.

```javascript
const after = before.map(expense => expense.id === 'e7'
  ? { ...expense, amount: 12.50 }
  : expense);
```

This is a reduced replacement pattern. Adding a new record would double-count the unchanged original. Trace the real `editingExpenseId`, modal fields and stored object in [app.js](../app.js).

## Conversion is not validation

HTML inputs provide text. `Number('')` is zero, `Number('abc')` is NaN, and `Number('Infinity')` is infinite. Check positive finite amounts and the supported two-decimal precision. Predict rejection for 0, -3, 1.234 and Infinity. A blank description is invalid, and 2026-02-30 is not a real date even though its characters match a date-shaped pattern.

## Locate the commit point

Follow candidate expense, candidate complete state, storage write, publication and render. If storage fails, the old amount remains authoritative and the editor stays available with feedback. A success message alone would not prove that reload will retain the edit.

The expense array is authoritative; displayed totals are derived. Change the expense date to another month in a disposable fixture and predict which month's total changes. Use the month picker before interpreting an absent filtered row as deletion.

JavaScript floating-point arithmetic is not a general-purpose financial ledger. A later exact-currency exercise should deliberately use a representation such as integer minor units throughout calculation, conversion and display.
''',
'''# Trace lab: overrides without rewriting the cookbook

[Course index](README.md)

## Separate source facts from user choices

The cookbook owns the source quantity. Shopping state owns a user's current override. A key combines recipe slug and ingredient index. For an illustrative key adobo:0:

```typescript
const source = '1 cup';
const overrides: Record<string, string> = { 'adobo:0': '' };
const key = 'adobo:0';
const quantity = Object.hasOwn(overrides, key) ? overrides[key] : source;
```

The empty override intentionally clears the quantity. Using `overrides[key] || source` would incorrectly restore the original. Use a real source slug when running the app.

Quantities remain bounded text: `2 1/2 cups`, `to taste` and `a pinch` are not one uniform numeric grammar. A servings multiplier needs an explicitly supported parsing rule; silently interpreting 1 1/2 as 1 would be wrong.

## Follow React state to two outputs

Typing invokes `onChange`, updates the store and triggers rendering and persistence. The resolved ingredient quantities feed both the screen and clipboard formatter. Open [shoppingState.ts](../src/store/shoppingState.ts), then follow callers into the store and page.

TypeScript does not validate JSON loaded from storage. The normalizer checks known recipes, ingredient keys, booleans and bounded text. Older saved state without overrides falls back to source quantities. Removing a recipe clears its overrides and checks.

## Verify the visible contract

Add a recipe, keyboard-edit its quantity, reload and copy the list. Screen and clipboard should agree; the source recipe should retain its original quantity. This app uses hash routing, so the shopping route ends in `/#/shopping-list`.

Ingredient indices are convenient for this static cookbook. A remotely edited cookbook that reorders ingredients would need stable ingredient ids and a saved-data migration policy.
''',
'''# Trace lab: backup replacement has one commit point

[Course index](README.md)

## Recognize the envelope

Valid JSON can still be the wrong document. The importer expects `format: "daybook.jobs"`, version 1, and an applications array. Records preserve their ids; restoration does not invent a second identity. Calendar events use separate storage and are excluded.

Suppose row one is valid and row two repeats its id. Reject the whole document. Saving each row while validating would leave a partial import. Other rejection examples include an unknown status, 2026-02-30, object-valued notes and a javascript: URL.

The 2 MB file bound, 10,000-record bound and field text limits in [jobBackup.js](../src/jobBackup.js) serve a different purpose from shape and domain validation. Explain what each protects.

## Follow the asynchronous sequence

```text
read file -> validate every record -> await queued storage write
          -> publish replacement state -> show success
```

`parseJobBackup` is pure: it returns records or throws. `commitJobBackup` writes one complete value only after validation. Import joins the existing write queue so a pending ordinary save does not later overwrite the restored data. Controls are disabled during import.

`await` pauses this function, not the browser. It does not guarantee success. Follow the error branch for file reading, JSON parsing and storage rejection.

## Observe absence of mutation

With an existing application in a disposable profile, import malformed JSON. Check the error and the saved original company. Then import a valid replacement, export again and compare id and company in the downloaded file.

An empty valid applications array intentionally clears the current list; a missing applications field is invalid. The UI explicitly labels import as replacement. Export first when you want a recovery copy.

A future version-two envelope needs an explicit migration or clear rejection policy. A version number alone does not transform old records.
''',
'''# Trace lab: one task through its HTTP lifecycle

[Course index](README.md)

## Follow the layers

A route selects a controller, the service enforces rules and the model performs SQL. Responses return through those layers. Use chapter 3's actual CRUD test to find the endpoint, payload and response envelope rather than assuming a generic API shape.

Create a task, capture its returned id, read it, edit that id, delete it and read again. Expect the same identity through editing and absence after deletion. A successful status code without a read-back would not prove persistence.

## Match validation to storage

JavaScript can represent integers larger than a PostgreSQL integer column accepts. IDs must be positive whole numbers no greater than 2,147,483,647. Reject -1, 1.5 and 2147483648 before SQL. Titles are bounded to 255 characters to match the schema.

Service validation provides helpful feedback. Database constraints remain a final safeguard; neither layer makes the other redundant.

## Understand an unchanged overdue date

A task was created with a future date that is now yesterday. Today the user changes only its title. Resubmitting that unchanged stored due date should not block the title edit.

Distinguish creating a past-dated task, changing a date to a new past value, and resubmitting an existing unchanged overdue date. The first two remain rejected; the third is accepted. Validation therefore needs stored state as well as request data.

## Explain test ownership

The helper creates a unique schema in a dedicated astra_test_* database, migrates it and starts the HTTP app on an available local port. Cleanup drops only that test schema. A schema is a namespace inside a database; all migration and request queries must use the same configured namespace.

Point to an assertion that would catch returning success without writing, then one that would catch creating a duplicate instead of updating. These demonstrate why a connected lifecycle test teaches more than four disconnected successful requests.
''',
'''# Trace lab: commas, quotes and transaction rollback

[Course index](README.md)

## Parse context, not characters alone

```csv
name,email,company,notes
Maya,maya@example.com,"Labs, Inc.","She said ""hello"""
```

The company decodes to Labs, Inc. and notes to She said "hello". Splitting on every comma would break the company. A newline inside a quoted field belongs to that value rather than ending its record.

Mark whether the parser is inside quotes. Outside, a comma ends a field and a newline ends a row. Inside, those characters are content. A doubled quote appends one quote; a closing quote returns to the outside state. This changing interpretation is why the parser uses a state machine.

Trace the parser linked in chapter 3 character by character, then remove the closing quote. Rejection is preferable to guessing later row boundaries.

## Separate structure and domain rules

Valid quoting does not guarantee supported unique headers, consistent row widths or acceptable contact fields. Tag names use the documented pipe separator. Make four invalid fixtures: malformed quoting, repeated header, missing required field and excessive record count. Locate the layer that rejects each before insertion.

## Fail late to prove rollback

Let row one create a new contact and TemporaryTag, then let row two violate a duplicate-email database constraint. After failure, neither the new contact, tag nor contact-tag link may remain.

An early invalid-field test cannot prove transaction rollback because no writes have started. Both tests matter, but they establish different guarantees.

Every contact, tag and junction operation must use the same transaction object. An accidental ordinary connection can write outside rollback. Catching an error inside the transaction and silently continuing can also undermine the contract.

Run [import.test.cjs](../server/test/import.test.cjs). Explain the counts before the batch, the writes attempted before failure, and the counts after rollback. A failed response alone does not prove atomicity.
''',
'''# Trace lab: calculate report results before running SQL

[Course index](README.md)

## Use an independent fixture

| Date | Category | Amount |
|---|---|---:|
| 2024-01-31 | Food | 99.00 |
| 2024-02-01 | Food | 10.10 |
| 2024-02-15 | Travel | 4.70 |
| 2024-02-29 | Food | 20.20 |
| 2024-03-01 | Food | 777.00 |

February has three expenses, Food 30.30, Travel 4.70 and total 35.00. The conspicuous neighboring values make leaked boundaries obvious. Derive expectations from this table rather than copying the query's filter into the test.

## Understand intervals and projection

The monthly window includes February 1 and excludes March 1. Leap day falls inside naturally. The category range endpoint instead includes both supplied start and end dates; callers need that distinction.

An ordinary list selects every expense field. A grouped report returns one row per category. Which individual expense description would represent the whole category? Retaining expenses.* makes the selection ambiguous and causes the PostgreSQL error addressed here.

The model calls clearSelect() before adding grouped fields, SUM and COUNT. It replaces the projection while retaining needed joins and filters. Open [expenseModel.js](../server/src/models/expenseModel.js) and annotate each clause.

## Inspect boundary values and representations

Reject month 2024-13, impossible date 2026-02-30, year zero and reversed ranges. Amounts must be finite, positive, bounded and within supported decimal precision.

Database decimal aggregates can arrive as strings. Inspect service conversion before comparing or formatting them. SQL decimals and JavaScript numbers have different representation guarantees.

Run [reports.test.cjs](../server/test/reports.test.cjs). Change one fixture amount on paper and predict the category, month and daily totals affected. Independently derived views agreeing provides stronger evidence than a single plausible chart.
''',
'''# Trace lab: authorization and recipe graph replacement

[Course index](README.md)

## Separate three identities

The route id identifies a recipe, the verified token identifies its caller, and stored data identifies its owner. A body user_id is caller-supplied data, not proof.

Alice owns recipe 10. Bob signs in and supplies Alice's id in an update body. The server must compare Bob's trusted identity to the stored owner and deny the update. Authentication answers who made the request; authorization answers whether that caller may change this resource.

## Read ownership inside the transaction

The update locks and checks the stored recipe within the transaction that replaces it. The model write also scopes by owner. A row lock coordinates competing writers during that transaction; it does not merge sequential edits or warn Alice that her browser has stale content. Version checking is a separate extension.

## TypeScript does not validate network JSON

A client can send difficulty as ["easy"], a string instead of an ingredient object, negative duration or blank step text regardless of compile-time interfaces. Runtime parsing checks every nested element. Silently filtering invalid children could store a recipe missing the content the caller thought was accepted.

Find parseRecipeInput through chapter 3 and invent one minimal invalid value per guard. The actual domain errors expose a code; do not assume their JavaScript name was overridden.

## Prove graph consistency

The recipe includes ingredients, steps and category links. A late foreign-key failure after replacing parent/children must restore the entire previous graph. Checking only a failed response would miss partial deletion.

Creation and replacement have different postconditions: failed creation leaves no partial graph; failed replacement preserves the existing graph. Run [ownership.test.ts](../server/test/ownership.test.ts), inspect both fixtures, and explain which assertions detect trusting a spoofed owner and which detect a write outside the transaction.
'''
]
for i,text in enumerate(chapters,1):
    folder=BASE/'stage'/f'{i:02}'/'astraupskill'
    (folder/'07-TRACE-LAB.md').write_text(text,encoding='utf-8')
    index=folder/'README.md'
    s=index.read_text(encoding='utf-8')
    if '07-TRACE-LAB.md' not in s:
        s=s.replace('## Your first session','8. [Step-by-step trace lab and concrete examples](07-TRACE-LAB.md)\n\n## Your first session')
        index.write_text(s,encoding='utf-8')
print('Added ten project-specific trace labs and index links.')
