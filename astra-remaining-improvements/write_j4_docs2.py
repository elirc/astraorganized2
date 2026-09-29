from pathlib import Path
s=Path('astra-remaining-improvements/stage/06325f8ab263')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('astraupskill/04-TESTING-AND-DEBUGGING.md',r'''
# Verify persistence, conflict and interruption

Run `./run.ps1 -Test` with JDK 17 on PATH. The suite is a plain Java executable with explicit assertions, so there is no test framework dependency to install. Compilation uses `--release 17 -Xlint:all`. [QuestionBankTest](../test/quiz/QuestionBankTest.java) creates its own temporary directory and cleans only descendants of that directory. Never change the fixture path to the checked-in question file to make a failing test easier to inspect.

The 28 Java cases cover legacy loading without rewriting bytes, durable create/update/delete, deletion of the final question, duplicate identity, stale instances, outside edits, held locks, failed destination reads, temporary-file cleanup, Unicode and delimiter round-trips, empty explanations, malformed formats, duplicate legacy rows, immutable snapshots, choice bounds and interrupted quizzes. These are behavioral checks: they assert what survives on disk or what the caller can observe, rather than merely repeating an implementation expression.

The separate verification harness adds nine process-level scenarios. A create in one JVM is read by a new JVM. Updates and confirmed deletes are also reloaded. Cancelled deletion and incomplete input preserve exact bytes. Corrupt startup does not rewrite the file. A final concurrency scenario starts two JVM workers, waits until both have loaded the same bank, releases their saves together and expects one saved result and one rejection. A subsequent process sees exactly the original question plus one winner.

## Investigate a stale-save report

First compare what each process loaded with what is currently on disk. Do not delete the lock file as a general fix. A stale bank must reopen even if no process currently holds the lock, because its remembered bytes no longer match. The lock solves overlapping cooperating writes; the byte comparison solves edits based on an older snapshot. They address different problems.

For a malformed bank, copy the file before investigation. Check the header, final count and encoded fields. A truncated final row should stop the entire load, not leave a partly usable bank that later overwrites omitted questions. Base64 errors and invalid UTF-8 are rejected. The old loader also rejects duplicate IDs and malformed later rows instead of returning earlier valid records.

For a quiz interrupted by EOF, inspect planned, answered and unanswered counts separately. One answered question is not a completed two-question quiz. The percentage is computed over answered attempts and the UI says so. Test input such as `A` followed by EOF to expose this distinction.

The suite does not test physical power loss, network filesystems or arbitrary editors ignoring locks. It also does not test a browser or HTTP server because none is implemented. Keep those limits with the passing evidence when describing the project to a reviewer.
''')
w('astraupskill/05-PRACTICE.md',r'''
# Practice toward a database-backed CRUD application

The following tasks are proposed extensions. Complete them after tracing the delivered file-backed commands. Each exercise should include a short user story, an invariant, a failing test and an explanation of the chosen boundary.

## 1. Search and page questions

Add a case-insensitive prompt search and a bounded page size. Preserve stable ordering so moving between pages does not randomly repeat records. Decide whether IDs participate in search. Test zero matches, the final short page and invalid page numbers. Keep search results immutable so a caller cannot bypass create/update/delete by modifying a returned collection. In a future API, map this behavior to validated query parameters rather than accepting raw database expressions.

## 2. Export without changing the authoritative bank

Add a human-readable export command that writes to a separate user-selected path. It should report failures without changing the loaded bank or its remembered bytes. Include delimiter characters and non-ASCII text. Explain why exporting to the current authoritative path would interfere with stale-file checks, and either reject that destination or define a safe explicit operation. Do not describe Base64 as protection for correct answers.

## 3. Save quiz-attempt history

Introduce an AttemptSession containing a stable ID, start time, planned count, immutable question snapshots and completed answers. Define how an interrupted session is represented. Do not infer “incorrect” from “unanswered.” Decide whether later question edits should affect older results; a historical snapshot usually gives clearer review behavior. Test reload after interruption and validate the relationship between planned count and actual attempts. Keep question-bank editing and attempt-history storage as separate responsibilities.

## 4. Add a real HTTP boundary

Expose question create/read/update/delete through a Java HTTP framework of your choice. Validate request bodies and return explicit 201, 200, 204, 400, 404 and conflict outcomes. Keep correct answers out of the learner-facing quiz response if you intend a server-scored experience. Use distinct teacher and learner response models. A route must not dump every field from Question merely because it is convenient. Add real HTTP tests for unknown fields, missing IDs and failed saves before building a browser form.

## 5. Move to SQL with per-record versions

Design Question and Choice tables, unique identity constraints and a version column. Replace whole-file byte comparison with a conditional update under the version the editor read. A transaction must replace a question's choices and correct-answer relationship together. Demonstrate that two users editing different questions can both succeed, while two stale edits of the same question have one winner. This exercise makes the cost of the current coarse file-level conflict policy visible.

## 6. Add ownership and operational checks

Design teacher ownership or class membership from authenticated server identity. Test that knowing another teacher's question ID does not grant edit access. Add a migration plan for legacy banks and a backup/restore drill using disposable copies. Separate a process being alive from its storage being writable. End by documenting which failure modes you tested and which assumptions still depend on the deployment filesystem or database.
''')
w('astraupskill/06-SOLUTIONS-AND-REVIEW.md',r'''
# Review guidance and solution sketches

Use these sketches to evaluate [practice work](05-PRACTICE.md), not as a substitute for implementing and testing it. A good solution can use different classes while preserving the same observable guarantees.

For search, normalize the comparison policy once and preserve an explicit order, such as insertion order or stable ID order. Compute the page after filtering. Reject negative offsets and unreasonable limits before slicing. Return an immutable list. Test a page boundary with more records than the selected page size; a three-record fixture cannot demonstrate a twenty-record paging bug.

For export, separate serialization from authoritative replacement. An export operation should not update the bank's remembered original bytes. Resolve the destination and compare it with the authoritative file before writing. Decide what to do when a destination already exists and make replacement explicit. A test should capture the bank's exact bytes, trigger an export failure and prove both the file and in-memory questions remain unchanged.

For session history, retain the question content used during the attempt. If Q1 is edited tomorrow, yesterday's answer should still be judged against yesterday's question. Store planned count and answered attempts separately, with a clear completion flag or derivable status. Validate impossible combinations on load. Show a partial session as partial rather than using a high answered-only percentage as evidence of completion.

For HTTP CRUD, keep untrusted request parsing outside the immutable domain constructor but still let the constructor enforce domain invariants. Translate known failures deliberately. A missing record can become 404; an invalid answer label becomes 400; a stale version becomes 409 or a documented conditional-request status. Unexpected storage errors should produce a generic server failure with diagnostic context kept in logs. A creation response should identify a readable resource. A 204 response has no JSON body, so browser code must not always call `response.json()`.

For SQL persistence, a useful update resembles “update Question where ID and version match; increment version; replace choices in the same transaction.” Zero affected rows requires distinguishing absence from a stale version according to your API policy. Add foreign keys and uniqueness rules that protect choice identity and ownership. A transaction alone does not prevent a read-then-write lost update; the condition at the write boundary matters.

For authorization, derive the owner from trusted identity, not a form field. Scope reads as well as writes, including nested choice IDs and attempt sessions. Review access with two users and copied resource IDs. Be explicit about which responses reveal correct answers and which are safe for learners taking a quiz.

In code review, ask the author to demonstrate one late failure and one competing edit. Check that success messages follow the durable boundary, incomplete inputs cannot mutate records, and old data has a migration path. Ask which assumption would fail on a network filesystem or with a writer that ignores the lock. Precise limits are a sign that the design has been understood.
''')
w('astraupskill/07-TRACE-LAB.md',r'''
# Trace a durable edit and a competing writer

Prepare a disposable copy of `data/questions.txt` and launch the app with `-DataPath` pointing to it. Keep the source open at [App.edit](../src/quiz/App.java) and [QuestionBank.commit](../src/quiz/QuestionBank.java). This lab changes only the copy you choose. Do not use your only copy of a bank while experimenting with malformed content.

Create question `TRACE1` with two choices and an empty explanation. Before submitting the final line, identify what exists only in local form variables. Once the command succeeds, inspect the selected file: it now starts with `QUIZ-BANK` and format version `1`, contains encoded fields and ends with a question count. The first edit converted the legacy representation. Restart and confirm that the empty explanation and choices survive.

Update TRACE1 with a prompt containing a pipe and a choice containing a semicolon. The versioned format can represent these characters because fields are encoded, rather than treating those characters as separators inside the text. The CLI reads single-line values; the underlying model and storage also support multiline strings, which the regression tests exercise. Do not infer that the interactive form has a multiline editor.

Now start a second app process against the same copy. Both load the same bank. In the first, create TRACE2. In the second, attempt an update to TRACE1. Expect a “Not saved” conflict. The second process still holds its earlier snapshot; reopening it is necessary before reapplying the intended edit. Explain why a completed first save can cause rejection even after its file lock has already been released.

Try delete twice: first answer `no`, then `yes`. Compare file bytes after the cancelled attempt and inspect the list after restart following the confirmed attempt. The confirmation is a UI decision before the command; the persistence boundary is still in the bank. A future API would need its own authorization and version checks regardless of what a browser confirmation dialog says.

End input halfway through a create form. The application reports that the incomplete edit was not applied. End input during a quiz and inspect the partial result. Record planned, answered, correct, incorrect and unanswered counts in a table. Explain why unanswered questions are neither valid QuestionAttempts nor automatically wrong answers.

Finish by writing a trace with seven stages: collect input, construct the domain object, validate identity, build candidate state, lock and compare, replace storage, publish memory and report success. Mark the possible failures beside each stage. Then propose where those responsibilities would live in an HTTP controller, service and SQL repository. Keep the mapping conceptual; those web layers remain an exercise in this project.
''')
w('astraupskill/VERIFICATION.md',r'''
# Executed evidence and remaining boundaries

Final verification passed 37 checks: 28 Java regression cases and nine separate-process scenarios. Compilation used Microsoft OpenJDK 17.0.10 with `--release 17 -Xlint:all`. The project runner reproduces the Java suite with `./run.ps1 -Test`. The central improvement workspace retains the broader process harness, logs, result JSON and delivery manifest for this project.

The regression suite exercised real temporary files rather than a mocked save method. It verified legacy loading without a rewrite, persistent create and update, deletion of the final record, duplicate identity rejection, immutable snapshots, stale saves, a held cooperating lock, a destination-read failure and cleanup of temporary artifacts. Format cases covered delimiter and Unicode round-trips, empty explanations, malformed Base64, invalid UTF-8, unknown versions, truncated footers and duplicate or malformed legacy rows.

The quiz cases verified the A–Z choice range, valid attempt labels, retry after invalid input and EOF before or during the quiz. Planned and answered counts remain separate. A partial result cannot be described as a completed quiz merely because its answered-only percentage is high. The CLI also reports incomplete forms without applying a partial create.

Process checks started fresh JVMs to verify that create, update and delete survive restart. They compared exact bytes after cancelled deletion, incomplete input and corrupt startup. The empty-bank scenario reloaded successfully and offered guidance instead of trying to run an empty quiz. For concurrency, two JVM workers loaded the same bank before a shared gate released their saves. Exactly one saved and one was rejected; a new process observed the expected two-record bank. This supports the cooperating-writer protocol on the tested Windows filesystem.

The original `data/questions.txt` was not changed by implementation or tests. Tests create their own temporary paths and remove only their owned descendants. Delivery backs up changed source files and verifies their hashes separately from the runtime persistence tests. No existing personal bank was migrated during this improvement pass.

Limits remain explicit. The application is a Java CLI with file storage, not an HTTP service, browser application or SQL database. There is no authentication, per-record ownership, persisted quiz-attempt history or network-filesystem test. Sidecar locks coordinate writers that follow the protocol; arbitrary external editors can ignore them. Atomic replacement is required, and unsupported filesystems fail the command instead of falling back to a weaker write. No power-loss durability claim is made. The first accepted edit converts a legacy file to the new format, which older binaries cannot read. Startup reports errors in text but does not currently return a distinct failure exit status. Those are useful, concrete subjects for later engineering work.
''')
print('All nine quiz course files written')
