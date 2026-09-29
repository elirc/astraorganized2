from pathlib import Path
P=Path(__file__).resolve().parent/'stage/d0778f38946f';D=P/'astraupskill';D.mkdir(exist_ok=True)
def doc(name,text): (D/name).write_text(text.strip()+'\n',encoding='utf-8')
doc('README.md',r'''
# Bank simulator: consistent commands and durable snapshots

This course turns a small Java CLI into a focused lesson about state ownership, related writes, and meaningful CRUD rules. It simulates balances and transactions locally. There are no real funds, bank integrations, HTTP endpoints, or browser screens. The next-step exercises explain how to build a CRUD web adapter without mistaking the CLI's guarantees for database transactions or production authorization.

The starting defect is easy to demonstrate: the original `getAccountById` returned the service's actual mutable account. A caller could increase its balance without creating a transaction. Copying only the surrounding list did not solve that problem, because the list still contained the same mutable objects. The delivered service now owns its account instances and returns detached copies. This is the first boundary to understand before adding controllers.

A second boundary is persistence. Previously, the CLI wrote accounts and transaction history to separate files. Failure between those writes could leave one newer than the other. The application now captures both collections together and saves one versioned snapshot through atomic replacement. Old `accounts.txt` and `transactions.txt` files are read for initial migration and retained unchanged; once `bank.snapshot.txt` exists, it is authoritative.

## Start with a separate learning dataset

Install JDK 17 or newer and set `JAVA_HOME` to your JDK directory if needed. From the project root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -Test
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -DataPath .\data\learning-bank
```

The second path is a directory, not a filename. The runner compiles the Java packages and passes that directory to `App`. With no override, it uses the project's `data` directory. The test command executes 28 regression tests, using temporary data for storage cases. It does not connect to external services.

Create Alice and Bob, deposit 10.00 into Alice, then transfer 2.50 to Bob. After a restart, inspect both balances and both sides of the transfer history. Rename Alice through menu 8. Try menu 9 on Alice and observe the refusal: an account with history cannot be deleted even after its balance later returns to zero. Create a separate unused account to exercise confirmed deletion.

## Learning sequence

Read the [code map](01-CODEBASE-MAP.md), then the [concepts](02-CONCEPTS.md) and [worked implementation](03-WORKED-CHANGE.md). Run the [tests and debugging exercises](04-TESTING-AND-DEBUGGING.md) and [CLI trace](07-TRACE-LAB.md). Attempt the [practice ladder](05-PRACTICE.md) before consulting [solution guidance](06-SOLUTIONS-AND-REVIEW.md). Finish with the [verification record](VERIFICATION.md), which distinguishes executed checks from future features.

A strong outcome is the ability to explain five things: who owns mutable state, which related changes happen together, when a command becomes durable, why deletion has domain restrictions, and where concurrency protection stops. The implementation is intentionally small enough to trace every method involved. Its in-memory synchronization and atomic file replacement are useful foundations, while request idempotency, cross-process concurrency, database transactions, transfer correlation IDs, and authenticated ownership remain explicit next steps.
''')
doc('01-CODEBASE-MAP.md',r'''
# Follow an operation from menu input to snapshot replacement

[App.java](../src/bankapp/App.java) constructs `FileStorage`, calls `loadSnapshot`, and initializes `BankService` from the returned accounts and transactions. Startup must finish loading before the menu appears. A storage error is reported by `main`; the application does not recover by silently replacing the dataset with an empty one.

The menu is a transport adapter. It gathers strings, parses decimal input, calls a service operation, saves the resulting snapshot, and only then prints the operation's success message. Menu 8 renames a holder. Menu 9 asks for confirmation and invokes restricted deletion. EOF is handled without treating an incomplete prompt sequence as a completed command. A save failure exits the CLI through its existing IOException path rather than allowing more operations to continue on an unsaved state.

[BankService.java](../src/bankapp/service/BankService.java) owns a map of accounts and a list of transactions. Its public reads and commands are synchronized on the service instance. It copies input accounts during construction and copies accounts returned by create, read, list, rename, or saving-related methods. `requireAccount` is private and returns the owned instance only to internal command implementations.

Trace a transfer in this order: require distinct existing accounts, normalize the positive amount, check available balance, construct both immutable transaction values, debit and credit, then append both history entries. Because the entire method is synchronized, another operation on this instance cannot observe the halfway state. `snapshot` is synchronized too, so it captures accounts and history under the same monitor rather than performing unrelated reads around an intervening command.

[BankAccount.java](../src/bankapp/model/BankAccount.java) still has balance adjustment methods, but they enforce valid amounts and prevent negative balances. [Transaction.java](../src/bankapp/model/Transaction.java) is immutable and validates amount, type, and related-account shape. [Money.java](../src/bankapp/model/Money.java) centralizes decimal normalization and required-text checks used by the models. Two-place precision is an explicit simulator rule.

[BankSnapshot.java](../src/bankapp/model/BankSnapshot.java) groups both collections. Its constructor copies account objects, and its account accessor returns fresh copies again. The transaction list is immutable because transaction objects themselves expose no mutation. This extra copy boundary prevents a caller from changing a previously captured snapshot before or after another component receives it.

[FileStorage.java](../src/bankapp/storage/FileStorage.java) is the format and filesystem adapter. It reads either the authoritative versioned snapshot or, when that file is absent, the complete legacy pair. It validates loaded records through the service's constructor, rejecting duplicate IDs and references to missing accounts. It writes header, account records, transaction records, and an `END` footer containing both counts to a temporary sibling, then atomically replaces the destination.

The [regression harness](../test/bankapp/RegressionTests.java) uses direct service calls, an executor for competing commands, and real temporary files. Start with `returned account cannot change service balance`, then `competing withdrawals cannot overdraw one service`, then `legacy migration retains original files and makes snapshot authoritative`. Together they show ownership, in-process concurrency, and durable format transition without requiring a framework.
''')
doc('02-CONCEPTS.md',r'''
# Ownership, transactions, and why CRUD has business rules

A service should be the authority for its own state. If another object can mutate an account obtained from a read method, the service's deposit and withdrawal rules become optional. The original implementation had exactly this problem. A defensive list copy protected only the list structure; the elements were still shared references.

```java
BankAccount view = service.getAccountById("A");
view.increaseBalance(new BigDecimal("5.00"));
// The delivered service's balance and history do not change.
// view is a detached object owned by the caller.
```

This is distinct from immutability. `BankAccount` remains mutable, but owned service instances never escape. `Transaction` is immutable. A snapshot combines detached account values and immutable transaction values. When designing an API, serializing a DTO often provides a natural boundary, but internal components still need an ownership policy before serialization happens.

A transfer changes multiple related facts: source balance, destination balance, outgoing history, and incoming history. The relevant invariant is that the accepted transfer moves the same positive amount between accounts and records both directions. `synchronized` protects those related changes within one service instance. It also protects snapshot capture. Without synchronized capture, reading balances and then history in two calls could observe different points in time even if each individual command were internally correct.

Atomic persistence is a different boundary. The snapshot file is replaced as one unit, preventing the previous two-file split where balances could be newer than history. A footer records expected account and transaction counts so a normally truncated or incomplete file is rejected. The footer is not a cryptographic integrity check and does not prove that balances reconcile with all historical events.

Neither boundary creates a cross-process database transaction. Two application instances still have independent service locks and can overwrite the same destination with stale snapshots. Likewise, a save error occurs after the in-memory command has executed. The CLI exits without reporting success, but a future reusable web service should coordinate command mutation and durable commit more deliberately.

Decimal amounts are validated with `RoundingMode.UNNECESSARY`. A submitted `1.001` is rejected rather than silently changed to `1.00`. Model validation also applies when records arrive from disk. Zero is allowed for an account balance but not for a deposit, withdrawal, or transfer amount. This difference illustrates why a field's type alone rarely captures all domain rules.

CRUD does not mean every resource supports arbitrary physical deletion. `renameAccount` changes holder text while retaining identity, creation time, balance, and history. `deleteUnusedAccount` permits removal only when balance is zero and no transaction references the account. A used zero-balance account still carries history and cannot be deleted through this command. An archive or close-account workflow would be a separate state transition with its own rules.

Finally, a transfer's two records currently have distinct transaction IDs and reciprocal account references, but no shared transfer ID. Timestamps and amounts are insufficient to correlate identical repeated transfers reliably. Recognizing this remaining limitation is part of the learning objective: build guarantees around explicit identifiers rather than guesses based on similar-looking records.
''')
doc('03-WORKED-CHANGE.md',r'''
# Worked change: commit balances and history as one file

Consider the original `App.saveData`: it called `saveAccounts` and then `saveTransactions`. Imagine a transfer has changed both balances and appended two history records in memory. Writing accounts succeeds, but writing transactions fails. On the next launch, the application sees the new balances and the old history. Reordering the two calls only reverses which half can become stale; it does not solve the two-write problem.

The delivered design introduces `BankSnapshot`, captured by `BankService.snapshot` under the same monitor used for commands. The storage adapter accepts that single value through `saveSnapshot`. It validates the account and transaction collections together, serializes everything, and only then touches a temporary file. The final replace operation changes the authoritative file as one unit.

The format is deliberately inspectable:

```text
# bank-snapshot-v1
A|A|Alice|7.50|2026-01-02T03:04
A|B|Bob|2.50|2026-01-02T03:04
T|out-id|A|TRANSFER_OUT|2.50|2026-01-02T03:05|Lunch|B
T|in-id|B|TRANSFER_IN|2.50|2026-01-02T03:05|Lunch|A
END|2|2
```

This is an illustrative snapshot fragment, not a claim that the listed history explains the opening balance. The `A` and `T` tags distinguish record shapes. Text fields escape backslashes, pipes, line feeds, and carriage returns. The footer counts parsed accounts and transactions. A missing footer, unexpected record type, bad amount, duplicate ID, or missing referenced account rejects the load.

Migration is explicit. When `bank.snapshot.txt` is absent, the loader accepts a complete `accounts.txt` and `transactions.txt` pair, or an entirely new directory with neither file. Only one legacy file is an error. The first successful save creates the snapshot and leaves both legacy files unchanged. Subsequent launches use the snapshot even if someone edits a legacy file. A corrupt authoritative snapshot does not trigger fallback to older legacy data, because that would silently roll the application backward.

The ownership correction complements persistence. The service constructor copies loaded account objects rather than retaining caller references. Every outward account read returns a copy. `BankSnapshot.accounts()` also returns copies, so a consumer cannot alter the stored snapshot through a getter. Immutable transaction objects can be shared safely through an immutable list.

The command correction constructs transaction values before changing balances. Input failures therefore occur before the balance mutations. The synchronized transfer then debits, credits, and appends both events without allowing another command or snapshot read on the same instance to interleave. This is an in-memory critical section, not a database transaction.

Read the [tests](../test/bankapp/RegressionTests.java) for invalid-save byte preservation, failed replacement cleanup, migration authority, and competing withdrawals. Notice the evidence each provides: real file contents establish persistence behavior, while concurrent service calls establish only the single-instance lock boundary. The future database exercise must replace both the persistence approach and the command/commit coordination rather than simply wrapping this CLI service in an HTTP controller.
''')
doc('04-TESTING-AND-DEBUGGING.md',r'''
# Regression tests that expose ownership and consistency failures

Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -Test`. The Java 17 runner compiles production and test sources with `--release 17 -Xlint:all`. The dependency-free harness reports each named case and exits nonzero on failure. It runs 28 cases; the delivery's separate CLI orchestration adds seven more scenarios in new Java processes.

Six initial checks failed against the original source: a returned account could mutate service balance, constructor input remained shared, duplicate account IDs were accepted, orphan transactions were accepted, sub-cent deposits were silently rounded, and negative model balances were allowed. These failures describe behavior, not the number of getters or classes in the implementation.

The ownership test deliberately calls a valid mutator on a returned account and then rereads the authoritative service state. Merely comparing object references would be weaker: it would prove different objects, but not necessarily that every relevant nested value was isolated. The suite repeats the check through list, creation, saving, and snapshot access paths because each is a possible escape route.

The competing-withdrawal test begins with a balance of 10.00 and submits 64 withdrawals of 1.00 through eight worker threads. A latch releases the queued work, and every future is observed with a timeout. Exactly ten operations must succeed, balance must finish at zero, and history must contain ten entries. A second case captures snapshots while transfers run and checks that total balance and paired history remain internally consistent. These tests exercise one shared service instance; they say nothing about two independent processes sharing a file.

For storage debugging, inspect three boundaries: parsed model values, validated snapshot, and destination replacement. A malformed amount is converted into an IOException with file and line context; it should not leak as an uncaught number parser failure. An invalid snapshot passed to saving is rejected before the previous file changes. A nonempty directory at the destination forces a move failure, allowing the test to verify preservation and temporary-file cleanup.

A useful debugger sequence is:

1. Break in `transfer` before transaction construction and inspect both balances.
2. Step through debit, credit, and history append while observing the held service monitor.
3. Break in `snapshot` and inspect a detached result.
4. Break before `Files.move` and compare the old destination with the temporary sibling.
5. Restart the process and inspect `loadSnapshot`, not the old in-memory object.

To investigate corruption, work on a copied learning directory. Remove the footer from its snapshot and start the CLI. It should report a load error before displaying the welcome menu. Compare the file hash before and after; startup must not rewrite the rejected file. The [trace lab](07-TRACE-LAB.md) provides a step-by-step manual version.

Keep the test scope honest. No browser, HTTP routing, database rollback, request retry, or multi-process lock is verified here. The compiler required reviewed full-access execution in this environment because restricted `--release` compilation could not close resources. That successful compilation and all test results are recorded centrally; a tooling error should never be counted as an application test pass.
''')
doc('05-PRACTICE.md',r'''
# Practice ladder: from local commands to a mid-level CRUD service

These are proposed extensions, not delivered features. Start each with an observable contract and a failing test. Preserve existing learning data and use a separate directory for format experiments. Work through the earlier exercises before adding an HTTP framework so you can explain the guarantees your controller is exposing.

## 1. Introduce a shared transfer identifier

Each accepted transfer currently produces two different transaction IDs. Add a shared transfer ID while preserving the individual record IDs. Two transfers with identical accounts, amount, description, and timestamp must still be distinguishable. Acceptance tests should retrieve exactly two matching sides for one transfer and reject a malformed imported pair. Plan a versioned snapshot migration; do not infer old pairs solely from matching timestamps or amounts. Explain whether incomplete historical pairs are reported, quarantined, or left explicitly uncorrelated.

## 2. Add account closing instead of deleting history

Introduce an account status and a `closeAccount` command. Decide whether closing requires zero balance and which operations remain allowed afterward. A reasonable exercise keeps history readable while rejecting new deposits, withdrawals, and transfers involving a closed account. Rename behavior should be an explicit policy too. Test every entry point, including transfers where the closed account is the destination. A UI-only disabled button is not enforcement.

## 3. Inject time and identity generation

Replace direct `LocalDateTime.now()` and UUID generation with narrow dependencies or constructor-supplied collaborators. Write deterministic tests for transaction ordering and transfer correlation. Do not make time a global mutable test switch: parallel tests should be able to use different clocks. Explain the distinction between an event timestamp, a stable ordering key, and a request idempotency key; none automatically substitutes for the others.

## 4. Make command persistence one unit of work

The current CLI mutates memory and then saves. Design a command handler that either publishes a fully persisted new state or leaves the previous state authoritative. One local approach constructs a candidate service from a snapshot, runs the command, saves the candidate, and then swaps the live reference under a single coordinator. Test a failed save and a competing command. Explain why swapping without coordination can lose updates, and why this approach is still limited to one process.

## 5. Build a database-backed HTTP adapter

Expose account creation, listing, lookup, rename, restricted deletion or closing, deposits, withdrawals, and transfers. Define JSON amount representation and error responses before writing controllers. Move related balance/history changes into one database transaction with appropriate row/version protection. Test insufficient balance, invalid precision, missing destination, repeated deletion, and rollback after a deliberately failed history insert. Source-level unit tests do not prove your HTTP status codes or database constraints.

## 6. Add authenticated ownership and idempotent commands

Scope every query and command to an authenticated principal. A transfer's source must belong to the caller under your explicit simulation policy. Add an idempotency key for money-changing requests: the same key and normalized payload returns the original outcome, while the same key with a different payload conflicts. Store the idempotency result in the same transaction as the operation. Test two simultaneous retries, not just two sequential calls.

Finish with a review that names the validation boundary, consistency boundary, persistence boundary, and authorization boundary. Demonstrate one failure at each. The goal is a small service whose behavior you can defend under invalid input, retries, and concurrent requests, with clear limits rather than a long list of unverified framework features.
''')
doc('06-SOLUTIONS-AND-REVIEW.md',r'''
# Solution guidance: make each guarantee explicit

Try the [practice ladder](05-PRACTICE.md) before reading these suggestions. They are design sketches for future work. The delivered simulator does not yet contain transfer correlation IDs, closed-account status, injected clocks, a database, HTTP endpoints, ownership, or request idempotency.

For transfer correlation, create one operation ID before building the outgoing and incoming records, then include it in both. Validate that a completed transfer has exactly one outgoing and one incoming entry with matching amount and reciprocal accounts. Keep the individual transaction IDs unique. A migration must identify old records as uncorrelated when pairing cannot be proven. Guessing a pair because two timestamps match can produce a false history explanation.

For account closing, use a state transition method with a small policy table. For example, an open zero-balance account can close; a closed account remains readable; commands that change balance reject closed source or destination accounts. Test both transfer directions. Physical deletion remains appropriate only for genuinely unused records under the current rule. The difference is a domain decision, not a limitation of the delete button.

For deterministic time, inject a `Clock` and derive timestamps with an explicit zone policy. Inject an ID supplier independently. A fixed clock is excellent for testing ties, but ordering still needs a stable secondary key. UUID ordering is deterministic for a captured dataset but does not establish true event sequence. If sequence matters, model a sequence number or database ordering contract deliberately.

A candidate-state unit of work might follow this sketch:

```text
acquire coordinator lock
  capture current state
  construct isolated candidate service
  apply validated command to candidate
  persist candidate snapshot
  replace authoritative service reference
release coordinator lock
return accepted result
```

A failed save must skip replacement and return failure. Every reader and writer must respect the coordinator; otherwise the live reference can escape and bypass the boundary. This is a local teaching design. A database implementation should generally express the related writes and idempotency record in one database transaction instead of cloning the entire dataset for every request.

For HTTP responses, define contracts from the domain's outcomes. An invalid decimal amount might map to 400, a missing visible account to 404, and an account-state or version conflict to 409. A successful create should return an identity that can be read through a corresponding endpoint. Avoid exposing a raw exception stack or trusting an owner ID merely because it appears in JSON. Controllers translate; the command path enforces.

For idempotency, store a normalized request fingerprint with the accepted result. Reusing the key with the same payload should replay that result; a different payload must not silently create another operation. A unique database constraint and transactional result storage are stronger than an in-memory `if not found then insert` check. Include an ambiguous-response test where the operation committed but the client did not receive the response.

Review the final work by asking for demonstrations: a rejected sub-cent amount, a denied closed-account transfer, a failed persistence operation, a cross-owner lookup, and two competing identical retries. Require the author to explain which test exercises each behavior and which boundary owns it. Mid-level understanding appears in these failure explanations, not in the number of layers added to the folder tree.
''')
doc('07-TRACE-LAB.md',r'''
# Trace lab: balances, history, migration, and refusal paths

Use a new learning directory so this exercise cannot change the normal dataset. From the project root, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -DataPath .\data\trace-bank
```

Create Alice and Bob through menu 1 and record their displayed IDs. Menu 2 should show both with zero balances. Deposit `10.00` into Alice through menu 3, including a short description. Transfer `2.50` from Alice to Bob through menu 5. List the accounts: Alice should have 7.50 and Bob 2.50. View each account's history through menu 6 and identify the outgoing and incoming records.

Exit with 7, restart with the same directory, and repeat the reads. This matters because reading the same service object immediately after a command does not test persistence. Inspect `data/trace-bank/bank.snapshot.txt`: it should contain the version header, account records, transaction records, and a final footer with both record counts. The transaction IDs are distinct; explain why there is currently no reliable shared transfer ID for correlating otherwise identical repeated transfers.

Now submit a deposit of `1.001`. The CLI should reject the amount and preserve both balance and history. Try a transfer larger than Alice's available balance and a transfer from Alice to herself. Both should fail without partial movement. Use menu 8 to rename Alice; restart and verify that the name changed while identity, balance, and history remained.

Try deleting Alice with menu 9 and confirmation `yes`. The service must refuse. Even if you later withdraw the balance to zero, history still protects the account from deletion. Create a third unused account, first cancel its deletion with `no`, then confirm with `yes`. Verify its absence after restarting. This demonstrates a domain-specific delete contract rather than indiscriminate removal of referenced records.

For a corruption experiment, close the application and copy the learning directory to a fresh destination. Use an unused destination name; `Copy-Item` into an existing directory can create a different nesting layout than expected.

```powershell
Copy-Item -LiteralPath .\data\trace-bank -Destination .\data\trace-bank-corrupt -Recurse
Add-Content -LiteralPath .\data\trace-bank-corrupt\bank.snapshot.txt -Value 'broken'
$beforeHash = (Get-FileHash -LiteralPath .\data\trace-bank-corrupt\bank.snapshot.txt).Hash
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -DataPath .\data\trace-bank-corrupt
$afterHash = (Get-FileHash -LiteralPath .\data\trace-bank-corrupt\bank.snapshot.txt).Hash
$beforeHash -eq $afterHash
```

Startup should report a storage error before the welcome menu and preserve the file hash. Keep the valid source directory as your recovery copy. Do not delete the authoritative snapshot merely to force legacy fallback; the legacy files may represent an older state.

Finally, run the [regression harness](../test/bankapp/RegressionTests.java). Compare the migration test with the manual corruption trace: one proves that a first snapshot can be created without overwriting the old pair, while the other proves that an existing invalid snapshot is not silently replaced. Write down the exact commit point and explain why a second simultaneously running application instance remains outside the tested guarantee.
''')
doc('VERIFICATION.md',r'''
# Verification record and remaining boundaries

This project was improved and tested in an isolated copy before applying a finite reviewed delivery to its original folder. Existing account data, transaction data, compiled artifacts, and Git history are not included in the delivery manifest. The central implementation report and project manifest `d0778f38946f` record the changed files, backups, checks, and hashes.

The compiler was Microsoft OpenJDK 17.0.10. The runner compiled with `--release 17 -Xlint:all`. As with the previous Java project, restricted compiler access produced a resource-close error; reviewed full-access verification succeeded. The test result is based on that successful compilation and execution, not on ignoring the failed tool invocation.

Six initial regression checks failed against the original source, covering escaped mutable state, retained caller references, duplicate account identity, orphan history, silent amount rounding, and invalid negative balances. The final suite passed **28 Java regression tests**. These include all outward account-copy paths, snapshot isolation, model guards, duplicate transaction IDs, transfer reference validation, conservation and paired history, rejected transfer preservation, 64 competing withdrawals, concurrent snapshot capture, rename behavior, restricted deletion, legacy migration, corruption and truncation rejection, real temporary-file replacement, and failure cleanup.

The separate orchestration script passed **seven CLI scenarios in new Java processes**, for **35 checks total**. It verified create/reload, persisted balances and paired transfer history, precision rejection, rename persistence, protected deletion and confirmation, EOF during an incomplete account prompt, and byte preservation on corrupt startup. The project runner executes the 28 Java cases; central logs and CLI evidence live under `astra-remaining-improvements/checks/j3/`.

These results establish local simulator behavior. No HTTP server, browser, database, authenticated owner model, external bank connection, or real transfer was involved. The synchronization boundary is one `BankService` instance. Two independent services or processes can still race when saving the same file, and the file format has no compare-and-swap version protocol.

Commands mutate service memory before the CLI saves. Success is printed only after saving, and IOException ends the CLI, but the service itself has no transactional persistence dependency or rollback mechanism. Power-loss durability and filesystems without atomic replacement support were not established. Unsupported atomic replacement fails visibly; the implementation does not silently fall back to a partial overwrite.

Loaded data is checked for valid fields, duplicate IDs, references, header, and record counts. It is not fully reconciled against historical balances, and the footer is not a checksum or tamper-proof signature. Transfer records still lack a shared operation ID. Those limitations are explicit practice topics rather than hidden claims of completeness.

Migration leaves legacy files unchanged and makes the first successfully written snapshot authoritative. Old application binaries do not understand that new authority; use the delivered source/runner and do not alternate old and new programs against the same directory. The CLI currently reports failures as text without a structured nonzero exit contract. Review these boundaries before adapting this foundation into a multi-user CRUD web application.
''')
(P/'README.md').write_text(r'''# Bank Account Simulator

A Java 17 command-line learning project for accounts, deposits, withdrawals, transfers, and transaction history. It now includes holder renaming, restricted deletion, consistent snapshots, and regression tests. Start the detailed [junior-to-mid-level CRUD course](astraupskill/README.md) for source explanations, worked examples, debugging, exercises, and review guidance.

## Run and test

Install JDK 17 or newer. Set `JAVA_HOME` to the JDK directory if Java is not on PATH. From this project root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -Test
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -DataPath .\data\learning-bank
```

`-Test` runs 28 dependency-free Java regression tests. `DataPath` is a directory; use a separate learning directory for experiments. Without an override the runner uses the project's `data` directory. The runner recompiles all source; existing old `out` binaries should not be used as the current implementation.

Manual compilation remains possible:

```powershell
javac --release 17 -Xlint:all -d out (Get-ChildItem -Recurse -Path src -Filter *.java | ForEach-Object FullName)
java -cp out bankapp.App .\data\learning-bank
```

## Structure and responsibilities

- `App`: gathers input, invokes commands, saves, then reports success.
- `BankService`: owns accounts/history, validates references, serializes operations on one service instance, and captures consistent snapshots.
- `BankAccount`: account value with guarded balance adjustments and detached copying.
- `Transaction` and `TransactionType`: immutable validated history entries and allowed event types.
- `Money`: shared decimal and required-text validation.
- `BankSnapshot`: accounts and transactions captured together, with defensive account copies.
- `FileStorage`: strict parsing, legacy migration, versioned snapshot writing, and atomic file replacement.
- `test/bankapp/RegressionTests.java`: behavior, concurrency, migration, and filesystem regression cases.

The [code map](astraupskill/01-CODEBASE-MAP.md) traces these collaborators method by method.

## Menu and behavior

Options 1–7 retain create, list, deposit, withdraw, transfer, history, and exit. Option 8 renames the account holder without changing identity or history. Option 9 deletes only a zero-balance account with no transaction references, after confirmation. Used accounts remain protected even when their balance returns to zero.

Amounts must be positive and exactly representable with two decimal places. Sub-cent inputs are rejected rather than rounded silently. Accounts may have a zero balance. Invalid operations preserve balances and history. Service reads return detached accounts so callers cannot bypass command history by mutating a returned object.

## Persistence and migration

The current file is `data/bank.snapshot.txt`, or that filename inside the selected directory. It contains a version header, tagged account/history records, and count footer. Saving validates and serializes a complete snapshot, writes a temporary sibling, and atomically replaces the destination. A failed or unsupported atomic replacement is reported; there is no non-atomic fallback.

When no snapshot exists, a complete legacy pair of `accounts.txt` and `transactions.txt` is loaded. A new directory with neither file starts empty. Only one legacy file is an error. The first successful save writes the snapshot while preserving the legacy files. Thereafter the snapshot is authoritative, and corruption does not silently fall back to stale legacy data. Old binaries still use the old format; do not alternate versions against the same dataset.

## Verification and next steps

Delivery verification passed 28 Java tests and seven separate-process CLI scenarios. See [verification](astraupskill/VERIFICATION.md) for evidence and limits. This remains a local simulator: it has no HTTP API, browser UI, authentication, or database. The [practice ladder](astraupskill/05-PRACTICE.md) develops those skills through correlation IDs, account closing, deterministic dependencies, units of work, transactions, ownership, and idempotent requests.

Synchronization is limited to one service instance. Atomic replacement does not prevent stale saves from independent processes or prove power-loss durability. In-memory commands precede persistence; a save failure exits the CLI without reporting success. Historical balance reconciliation and shared transfer IDs remain future work.
''',encoding='utf-8')
