from pathlib import Path
P=Path(__file__).resolve().parent/'stage/d9a27fa7f308';D=P/'astraupskill';D.mkdir(exist_ok=True)
def doc(name,text): (D/name).write_text(text.strip()+'\n',encoding='utf-8')
doc('README.md',r'''
# Expense tracker: reliable CRUD before a web framework

This course uses the four Java classes that actually run this project. You will create, read, update, delete, save, and reload expenses, then reason about which guarantees survive when the same behavior becomes a web API. The application is still a local command-line program. An HTTP adapter, authentication, database, and browser interface are later exercises, not features silently implied by the word CRUD.

The useful starting question is: can a user trust that a successfully saved expense will still exist next time? The original implementation failed this question for the ordinary case of an empty optional note. The new regression suite reproduces that defect and protects the correction. Learning to find a small destructive edge case is more valuable here than memorizing a framework's folder layout.

## Run and test

Use JDK 17 or newer. Set `JAVA_HOME` to your installed JDK directory if Java is not on PATH; do not copy another person's installation path. From the project root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -Test
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -DataPath .\data\learning-expenses.txt
```

The script compiles with `--release 17 -Xlint:all`. `-Test` runs 23 dependency-free regression tests with temporary files. The second command starts an isolated learning dataset, so your normal expense file is not used. Relative `DataPath` values resolve from your current directory. With no override, the script uses the project's `data/expenses.txt`. Direct invocation of `App` instead defaults relative to the Java process's working directory.

Add Lunch, amount `12.30`, category `food`, date `2026-01-02`, and a blank note. Choose 7 to save and exit. Restart with the same path and list expenses. Now use 8 to replace its editable fields and 9 to delete it after confirmation. Menu 7 retains its existing exit role; the new operations are appended.

## Suggested sequence and evidence

1. Read the [code map](01-CODEBASE-MAP.md) and locate the only live list.
2. Study [invariants and boundaries](02-CONCEPTS.md), then predict a rejected update's result.
3. Follow the [worked change](03-WORKED-CHANGE.md) through parsing and saving.
4. Run the [testing guide](04-TESTING-AND-DEBUGGING.md) and [trace lab](07-TRACE-LAB.md).
5. Complete the [practice ladder](05-PRACTICE.md), using [review guidance](06-SOLUTIONS-AND-REVIEW.md) after your own attempt.
6. Read [verification and limits](VERIFICATION.md) before claiming production readiness.

Allow several focused sessions rather than finishing every exercise at once. A useful review artifact contains the input, expected result, actual observation, relevant source method, and a regression test. Explain why a failed update cannot partly change a stored expense, why a missing file differs from a corrupt file, and why atomic file replacement does not make two simultaneous application instances safe. Those explanations connect this small project to mid-level CRUD development.

The implemented improvements include immutable replacement updates, explicit deletion confirmation, domain-level money precision, whole-file validation, guarded identity allocation, consistent category normalization, and atomic save replacement. They preserve the project's small scale while making its behavior teachable and testable.
''')
doc('01-CODEBASE-MAP.md',r'''
# Trace the live data through four classes

Start in [App.java](../src/expensetracker/App.java), specifically `main`. It chooses a file path, creates `ExpenseManager` and `ExpenseFileStorage`, then runs the menu. These constructor calls are a small composition root: the application decides which objects collaborate. A future web server could build the same service and a different adapter, although sharing this manager across request threads would require a concurrency design first.

`App.run` first calls `loadExpenses`. Success allows the menu to start. Failure prints a diagnostic and returns before entering the save-on-exit `finally` block. This order matters: loading a broken file must not initialize an empty session that later overwrites the original. During a valid session, EOF is handled as the end of input. Fully completed changes are saved; a command interrupted halfway through collecting its fields has not yet called the manager.

[ExpenseManager.java](../src/expensetracker/ExpenseManager.java) owns the live `List<Expense>` and `nextId`. Follow these operations:

| User action | Manager method | Main result |
|---|---|---|
| Add | `addExpense` | New validated value and allocated ID |
| List | `getAllExpenses` | Copy of the collection |
| Look up ID | `findExpense` | `Optional<Expense>` |
| Update | `updateExpense` | Replacement value with the same ID |
| Delete | `deleteExpense` | Whether anything was removed |
| Summarize | `getTotalSpending`, `getSpendingByCategory` | Values derived from current records |
| Restore | `loadExpenses` | Validated replacement collection |

The model in [Expense.java](../src/expensetracker/Expense.java) is immutable: every field is final, and there are no setters. A list copy alone would not protect state if its elements were mutable. Here, callers can hold the old expense after an update without observing an object that changes underneath them. The manager replaces the list entry with a new valid instance.

[ExpenseFileStorage.java](../src/expensetracker/ExpenseFileStorage.java) translates between model objects and six tab-separated fields. `escape` writes backslashes and control characters as visible escape sequences. `splitPreservingEscapes` finds physical tabs without discarding escape pairs; `unescape` decodes each text field. The loader skips comments and genuinely blank lines, but parses each record's original line so a final empty field remains present.

Saving snapshots the input, validates duplicate identities, and serializes all records before creating a temporary sibling file. Only after writing succeeds does `Files.move` attempt atomic replacement of the destination. The cleanup block removes a leftover temporary file after a failed move. No database, repository framework, dependency injection library, or background autosave is hidden behind this code.

The [regression harness](../test/expensetracker/RegressionTests.java) constructs objects directly and uses real temporary files. Read `update and delete survive persisted reload` first: it joins model, manager, and storage in one observable scenario. Then read the smaller tests to understand which layer rejects each invalid input. Draw the path `menu -> manager -> Expense -> list`, followed later by `list -> storage -> file`; the time gap before saving is an intentional limitation you should be able to explain.
''')
doc('02-CONCEPTS.md',r'''
# Invariants, identity, snapshots, and commit boundaries

An invariant is a rule that must hold for every accepted state. In this project an expense has a positive ID, nonblank title and category, a valid date, and a positive amount representable at two decimal places. An optional note may be empty. The constructor enforces these rules because records can enter from either the menu or a file; validating only menu input would leave the file-loading path unprotected.

Money uses decimal arithmetic:

```java
new BigDecimal("12.30"); // decimal input is preserved
new BigDecimal("1.001").setScale(2, RoundingMode.UNNECESSARY);
// throws: silently rounding would change the accepted input
```

`12.300` is accepted because reducing its scale to two requires no rounding. `0.001` is rejected, and zero or negative values are rejected separately. This is a teaching application's single-currency rule, not a universal claim that every currency has two fractional digits. When designing a real expense service, make currency and supported precision explicit.

Identity answers which record this is; editable fields answer what it currently contains. Changing Lunch to Bus must retain its ID so references remain meaningful. `updateExpense` constructs a candidate before calling `expenses.set`. If parsing the date fails, the old object stays in the collection and all derived totals remain unchanged. This pattern is the small-scale equivalent of validating a command before committing a database transaction.

```java
Expense old = manager.findExpense(1).orElseThrow();
manager.updateExpense(1, "Bus", "2.50", "Travel", "2026-02-03", "");
// old still describes the previous immutable value.
// manager.findExpense(1) now returns the replacement.
```

A copied list is a collection snapshot, not a durable commit. Clearing the returned list cannot remove the manager's entries. Saving writes the current collection to disk, while updates before exit remain in memory. A forced process termination can lose those unsaved edits. There is also no persisted identity counter: after a restart, the next ID is reconstructed from remaining records. A deleted highest ID can therefore be reused across sessions; preventing that requires a format change or an independent identity strategy.

Whole-file validation establishes another boundary. Duplicate IDs or a malformed line reject the entire load. Returning only the good rows would make a partially recovered dataset look complete. A repair workflow should instead preserve the original, show diagnostics, and ask a person to review a separate recovered copy. That workflow is proposed practice, not automatic behavior.

Atomic replacement prevents readers from observing a partially rewritten destination on filesystems that support the requested operation. It does not provide a cross-process lock, compare-and-swap version check, or guaranteed survival of power loss. Two app instances can still overwrite each other's snapshots. Map this distinction to web development: a transaction protects a particular unit of work, while optimistic concurrency protects a user's edit against someone else's intervening update. You need to identify both boundaries before choosing a database library.

Finally, normalization is a policy. Categories collapse whitespace and use `Locale.ROOT` case conversion on both construction and menu entry, so saved data and newly entered data aggregate consistently. This is intentionally a simple label policy; it is not a full internationalized category identity system.
''')
doc('03-WORKED-CHANGE.md',r'''
# Worked change: stop empty notes from deleting saved expenses

Reproduce the smallest failure before reading the solution. Create one expense whose note is the empty string, save it, load it, and assert that one record comes back. The original application returned zero records. A typical manual test with a note such as `lunch with team` did not expose this bug, which is why optional fields deserve deliberate coverage.

The saved record consists of six fields. Written with visible markers, it looks like this:

```text
1<TAB>Lunch<TAB>12.30<TAB>Food<TAB>2026-01-02<TAB><NEWLINE>
```

The last tab is meaningful: it introduces an empty sixth field. The old loader called `line.trim()` and passed that result into the parser. Trimming removed the trailing tab. The parser then saw five fields and rejected the record. The surrounding catch printed a message and continued, making the returned collection look successfully loaded despite missing data.

The correction separates inspection from parsing:

```java
String trimmedLine = line.trim();
if (trimmedLine.isEmpty() || trimmedLine.startsWith("#")) {
    continue;
}
Expense expense = parseLine(line); // original physical separators
```

This is a general parsing lesson: normalization appropriate for recognizing an empty line can be destructive when applied to structured data. In a web app, the analogous mistake might be trimming an entire signed payload, coercing an empty field to a missing field, or replacing zero with a fallback using a truthiness check. Normalize individual fields according to their contract.

The second correction changes failure policy. A malformed row now throws `IOException` with its line number instead of returning a partial collection. Duplicate IDs are checked while reading. The application responds by stopping before the menu and before save-on-exit. These layers work together: strict parsing without changing startup behavior could still lead to an empty collection overwriting the original.

The third correction changes saving. Previously, opening the destination writer could truncate existing content before every record was serialized. Now the method validates and builds all lines, writes a temporary sibling, and atomically replaces the target. Invalid input never touches the destination. A failed move leaves the prior destination in place in the tested scenarios and cleans the temporary sibling. Unsupported atomic replacement produces an explicit save failure; the code does not silently downgrade to a weaker operation.

The CRUD extension follows the same validate-before-mutation principle. `updateExpense` finds the ID, constructs a complete replacement, then changes exactly one list entry. A bad date does not partially change title or amount. `deleteExpense` returns a boolean, while the menu checks existence and asks for `yes` before calling it. Service methods remain independent of interactive confirmation so a later adapter can apply its own interaction policy.

Review the [tests](../test/expensetracker/RegressionTests.java) named `empty optional note survives a save and load`, `corrupt record rejects the entire file`, and `invalid update preserves previous value`. Each asserts an externally observable contract. The first four regression cases failed against the original source; the final suite passes. A useful commit explanation would lead with preserved data and accepted behavior, then describe these implementation details as the reason the behavior is reliable.
''')
doc('04-TESTING-AND-DEBUGGING.md',r'''
# Test boundaries, not just happy-path menu output

Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -Test` from the project root. The harness uses a small named-test wrapper, prints PASS or FAIL, and exits nonzero if any check fails. It does not require Maven, Gradle, JUnit, network access, or a database. That simplicity keeps attention on arranging a meaningful state and observing the result. A future test-framework migration should preserve these contracts rather than replace them with assertions about private implementation details.

The 23 tests cover several different failure boundaries. Domain cases check precision and category normalization. Manager cases verify identity, invalid-update preservation, copy isolation, exhaustion, and deletion. Storage cases use real temporary files to exercise empty fields, escapes, corruption, duplicate IDs, repeated replacement, and failed moves. The end-to-end Java case updates and deletes records, saves them, constructs a new manager, and inspects the restored state.

For example, this assertion is stronger than merely expecting an exception:

```java
rejects(IllegalArgumentException.class,
    () -> manager.updateExpense(1, "Bus", "2.50", "Travel", "2026-02-30", "changed"));
equal("original", manager.findExpense(1).orElseThrow().getNote());
equal(new BigDecimal("12.30"), manager.getTotalSpending());
```

It checks the failure and proves that existing state survived. Likewise, `invalid save preserves existing bytes` snapshots the prior file and compares its complete contents after rejection. The failed-move test uses a nonempty directory at the destination path, then checks that its existing child remains and no temporary sibling leaked. These tests cover predictable filesystem failures; they do not emulate a sudden machine power cut.

When a save/reload test fails, inspect the physical file before changing the manager. Use `Get-Content -LiteralPath .\data\learning-expenses.txt`, then render tabs visibly if needed:

```powershell
(Get-Content -LiteralPath .\data\learning-expenses.txt) -replace "`t", '<TAB>'
```

The end of a record with an empty note must still contain the sixth-field separator. Put breakpoints in `load`, `parseLine`, and `splitPreservingEscapes`. Compare `line` with `trimmedLine` and count fields. A breakpoint in `App.loadExpenses` then shows whether a load error can reach the menu or the save block.

For update failures, break before `new Expense` and before `expenses.set`. The latter must not execute if construction fails. Hold a reference to the old immutable expense and verify its fields remain unchanged even after a later successful replacement.

The delivery verification also exercised five CLI scenarios in separate Java processes, including EOF and corrupt-startup preservation. Those orchestration checks are recorded in the central implementation evidence; the project's portable runner executes the 23 Java cases. Do not confuse a manually described lab with an automatically executed browser test: this project currently has neither a browser nor an HTTP server.

If `--release 17` reports a compiler-resource error in a restricted environment, first verify the JDK installation and its filesystem access. The reviewed full-access verification passed here. Do not weaken application validation to work around a tooling problem, and do not treat a compilation failure as a passing test run.
''')
doc('05-PRACTICE.md',r'''
# Practice ladder toward a CRUD web application

Complete one exercise at a time. For each, write the behavior contract, add a failing test, implement the smallest coherent change, and explain what is still outside its guarantee. The exercises below are proposals; they are not included features. Keep learning data separate from any existing expense file.

## 1. Add an explicit save command

The current menu saves on exit or EOF. Add a command that saves without ending the session and reports whether saving succeeded. Acceptance example: add Lunch, save, add Tea, then simulate ending the process without another save. A new instance should see Lunch but not Tea. Make the failure result visible rather than printing success unconditionally. Hint: `saveExpenses` currently returns no result, so consider how the menu can distinguish success from failure. Do not claim that this command creates automatic per-operation durability.

## 2. Preserve identity allocation across restarts

Today `nextId` is reconstructed from the maximum remaining ID. Deleting the largest record and restarting can reuse that ID. Propose a versioned file header containing the next allocation value, or a different identity type. Acceptance example: create IDs 1 and 2, delete 2, save, restart, create another record; it must not receive 2. Also test an old-format file, a corrupt header, and exhausted identity space. Hint: an optional new header needs an explicit migration rule; silently guessing after a corrupt header defeats the guarantee.

## 3. Add a filtered, deterministic page

Implement a query that accepts a month, offset, and limit and returns records ordered by date then ID. Use two expenses on the same date to force a tie. Reject negative offset and unreasonable page sizes. An empty page is a valid result. Explain why an in-memory list scan is acceptable at this scale and why a database implementation would need a matching filter/order/index strategy. Do not optimize by storing a second mutable aggregate before you can keep it consistent.

## 4. Add optimistic concurrency to updates

Introduce a version value and require the caller to supply the version it read. Two callers read version 1. The first update succeeds and produces version 2; the second receives a conflict and leaves the first update intact. Add a deterministic competing-update test. Merely checking then replacing without synchronization is insufficient when requests run on different threads. Decide whether a lock, a transactional repository, or another mechanism owns the compare-and-update boundary.

## 5. Build the first HTTP adapter

Expose create, list, get-by-ID, replacement update, and delete operations. Keep transport parsing outside the domain. Define a consistent response body for invalid fields, missing IDs, and stale versions. For example, a proposed `PUT /expenses/1` sends the full editable record, including an empty note when the user wants to clear it. Distinguish that from a future partial `PATCH` contract. Add actual HTTP tests for status, body, and persisted reload; a service unit test alone cannot verify routing or JSON behavior.

## 6. Move persistence into a database-backed unit of work

Replace save-on-exit with a transaction per accepted mutation, preserving the service's validation behavior. Add rollback tests, unique identity constraints, and version conflict checks. Then add owner scoping before exposing real personal records: every read and write must use the authenticated owner, not a caller-supplied owner field. Demonstrate that one user's identifier cannot retrieve another user's expense. Authentication, authorization, persistence, and concurrency are separate responsibilities; explain where each is enforced in your final design.

Finish by reviewing the [solution guidance](06-SOLUTIONS-AND-REVIEW.md) and recording a short demonstration. A mid-level result includes failure behavior and operational limits, not just a screenshot of a successful form submission.
''')
doc('06-SOLUTIONS-AND-REVIEW.md',r'''
# Solution guidance and a practical review rubric

Use these notes after attempting the [practice exercises](05-PRACTICE.md). They describe design directions, not finished code that the application already contains. Your implementation can differ if it satisfies the same observable contracts and you can explain its tradeoffs.

For explicit save, a useful result is a boolean or a small outcome object returned from the adapter's save operation. The menu should remain open after failure and should preserve in-memory edits so the user can retry. Test a writable temporary file and a destination that cannot be replaced. A weak solution always prints `Saved` after calling a method that swallowed an exception. A stronger solution reports the actual outcome and avoids clearing the current collection.

For durable allocation, keep the saved records and next-ID metadata in the same atomic snapshot. Writing the counter to a second unrelated file introduces a two-write consistency problem. A versioned header might be `# format=2 nextId=3`, but define escaping, range validation, and old-format migration before implementing it. Never reset an invalid counter to one. If you choose UUIDs instead, explain why the public ID type and existing saved records need migration rather than silently changing a field's meaning.

For paging, order before slicing:

```java
// Sketch for an exercise, not an existing method:
matching.stream()
    .sorted(Comparator.comparing(Expense::getDate)
        .thenComparingLong(Expense::getId))
    .skip(offset)
    .limit(limit)
    .toList();
```

The tie-breaker makes equal dates deterministic. Validate offset and limit before processing. If the collection changes between page requests, offset pagination can still skip or repeat records. Explain this limitation and consider a date-and-ID cursor only when the exercise needs it.

For optimistic concurrency, compare the expected version and replace the value within one protected operation. A Java lock can demonstrate the concept for one process. A database adapter might perform `UPDATE ... WHERE id = ? AND owner_id = ? AND version = ?`, then inspect the affected-row count. A zero count must be interpreted carefully: missing, forbidden, or stale state may have different internal causes even if your public error policy deliberately hides some distinctions.

For the HTTP exercise, write a contract table before coding controllers. A reasonable proposed mapping is create 201 with a readable Location, get 200 or 404, invalid body 400, stale version 409, and delete 204 under a documented repeated-delete policy. These are design choices for the exercise, not existing endpoints. Keep amounts as validated decimal strings or another explicitly documented representation so the browser does not accidentally decide the domain's rounding policy.

During review, ask the author to demonstrate an invalid update, a stale edit, a denied cross-owner lookup, and a persistence failure. Then inspect the tests that preserve those behaviors. Award credit for a clear boundary even when the implementation is small. Do not award concurrency credit for a test that starts tasks sequentially, or durability credit for a test that reads the same in-memory object immediately after writing.

A useful final explanation names the authoritative state, the validation layer, the commit point, the error contract, and the remaining limitation. In this delivered CLI, those answers are the manager's collection, the domain and manager, successful atomic save replacement, printed adapter diagnostics or method exceptions, and the absence of multi-process coordination and per-command persistence.
''')
doc('07-TRACE-LAB.md',r'''
# Trace lab: create, replace, delete, reload, and reject corruption

This lab uses the delivered CLI. It is safe to repeat with a dedicated learning file. Use a new filename if a previous run already contains records, because the example IDs assume an empty dataset. Do not point a corruption experiment at your normal expense file. The automatic regression harness creates its own temporary data; this manual exercise lets you see the same boundaries directly.

Start from the project root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -DataPath .\data\trace-expenses.txt
```

Choose 1 and enter `Lunch`, `12.30`, `food`, `2026-01-02`, and a blank note. The application reports the assigned ID. Choose 2 and inspect the normalized category and two-place amount. Choose 7 to save and exit. Read the file with `Get-Content`; the final tab introduces the empty note. Restart with the same command. The loaded count should be one, and listing should still show Lunch. Record why passing the original line into the parser is essential here.

Choose 8 and enter the displayed ID, `Bus`, `2.50`, `Travel`, `2026-02-30`, and a blank note. The date is impossible. Listing must still show Lunch at 12.30. Repeat with `2026-02-03`; now the ID remains the same while title, amount, category, and date change. Choose 5 and 6 to verify that summaries derive from current records rather than retaining a cached Lunch total.

Choose 9 with the same ID, answer `no`, and list again. Bus must remain. Choose 9 again and answer `yes`; the record disappears. Exit, restart, and verify the empty state survived. Explain the difference between confirmation in the CLI and `deleteExpense` in the manager: the service performs a deterministic operation, while the adapter asks the human before invoking it.

For the corruption trace, first add and save one record again, then exit. Copy the dataset to a separate file:

```powershell
Copy-Item -LiteralPath .\data\trace-expenses.txt -Destination .\data\trace-corrupt.txt
Add-Content -LiteralPath .\data\trace-corrupt.txt -Value 'broken'
$beforeHash = (Get-FileHash -LiteralPath .\data\trace-corrupt.txt).Hash
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -DataPath .\data\trace-corrupt.txt
$afterHash = (Get-FileHash -LiteralPath .\data\trace-corrupt.txt).Hash
$beforeHash -eq $afterHash
```

The application should identify the invalid line, stop startup, and leave the file hash unchanged. It should not offer the normal menu or claim that expenses were saved. Keep the valid source copy for recovery. This is fail-closed loading, not an automatic repair feature.

Finally, inspect the [regression suite](../test/expensetracker/RegressionTests.java) and map each observation to a named test. Write a five-sentence review: what input triggered the original loss, which parser boundary changed, why failed updates preserve state, when a successful edit becomes durable, and what would happen if two processes saved different snapshots. If any answer is vague, revisit the relevant method before beginning the HTTP exercise.
''')
doc('VERIFICATION.md',r'''
# Verification record and limits

The implementation was reviewed and tested in an isolated copy before delivery to this project's original folder. Existing user data was not used as a fixture or replaced. Delivery is recorded in the repository's `astrdocs/REMAINING_PROJECTS_IMPLEMENTATION_REPORT.md` and finite hash-verified manifest for project ID `d9a27fa7f308`; original changed files are backed up by that workflow.

## Executed checks

The environment used Microsoft OpenJDK 17.0.10. The project runner compiled production and test source with `--release 17 -Xlint:all`. The initial restricted compiler invocation could not close compiler resources; the reviewed full-access invocation succeeded. This was a tooling-access issue, not a reason to omit the compilation gate.

Four initial regression tests failed against the original implementation: an empty optional note disappeared after saving and reloading; a malformed row did not reject the whole load; duplicate IDs replaced existing manager state; and the model accepted sub-cent precision. After the changes, all **23 Java regression tests passed**. They use real temporary files and cover escaped text, invalid saved precision, duplicate identities, missing files, preservation after invalid saves, atomic replacement cleanup, CRUD behavior, ID exhaustion, locale-independent category normalization, and collection isolation.

A separate verification script ran **five CLI scenarios across Java processes**, for **28 checks total**. These confirmed empty-note reload, persisted update, deletion cancellation followed by confirmed deletion, EOF during an unfinished command, and unchanged file bytes when startup encounters corruption. The project-local `run.ps1 -Test` command runs the 23 Java cases; the five orchestration scenarios and logs are retained in the central implementation evidence under `astra-remaining-improvements/checks/j5/`.

## What the checks do not establish

This is a single-process CLI learning project. No web framework, browser UI, authenticated owner model, database, or HTTP contract was implemented or tested. The [practice ladder](05-PRACTICE.md) proposes those next steps explicitly. The manager is not thread-safe, and multiple application instances can overwrite each other's complete file snapshots.

Changes remain in memory until normal exit, EOF handling, or an explicit call to storage. A force-killed process can lose unsaved edits. Atomic replacement is requested without a non-atomic fallback; a filesystem that does not support it produces a visible save failure. The tests cover ordinary replacement and a failed move, not power-loss durability or every network filesystem's behavior.

Identity allocation is guarded against numeric wraparound, but its counter is reconstructed from the remaining saved records. Deleting the highest ID and restarting can reuse it. The course includes a migration exercise to address that limitation. Category normalization intentionally changes case and collapses spaces; it is a simple demonstration policy rather than a comprehensive internationalized taxonomy.

Strict loading may now refuse a file that the old implementation partly accepted. This is intentional preservation behavior: repair a separate copy and review rejected records rather than silently dropping them. There is no automatic salvage command. The CLI prints startup/save failures but does not yet expose a structured process-exit contract for automation. These limits should remain visible in a review so a learner can distinguish verified behavior from future work.
''')
# Correct stale descriptions in the existing detailed README rather than discard it.
p=P/'README.md';s=p.read_text(encoding='utf-8')
s=s.replace('You can add expenses, list them, filter them, and view spending summaries.', 'You can add, list, update, and delete expenses, filter them, and view spending summaries.')
s=s.replace('If loading fails, it shows a message and starts with an empty list.', 'If loading fails, it reports the error and stops before the menu or any save, preserving the original file.')
s=s.replace('### `ExpenseManager.calculateNextId`','### Identity allocation in `ExpenseManager.loadExpenses`')
s=s.replace('1. Add expense deletion by id.','1. Extend the implemented deletion flow with an undo design.')
s=s.replace('2. Add expense editing by id.','2. Extend the implemented replacement update with version conflict detection.')
s='''> **Updated learning path:** [Start the detailed CRUD and persistence course](astraupskill/README.md). Update and confirmed delete are implemented as menu options 8 and 9. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\\run.ps1 -Test` for 23 regression tests. Loading now rejects corrupt or duplicate records without saving; saving validates first and atomically replaces the file. See the course verification record for limits and five additional CLI verification scenarios.\n\n'''+s
p.write_text(s,encoding='utf-8')
