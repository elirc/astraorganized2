from pathlib import Path
s=Path('astra-remaining-improvements/stage/06325f8ab263')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
p=s/'README.md';t=p.read_text();p.write_text('''# Quiz Engine: current learning edition

Start with [astraupskill](astraupskill/README.md) for the current code map, detailed lessons, worked changes, practice and verification. The original walkthrough below describes the earlier read-only edition; this section records the implemented additions.

The app now supports question-bank CRUD: menu 4 lists questions, 5 creates, 6 updates by stable ID and 7 deletes after explicit confirmation. Original options 1–3 remain quiz, count and exit. Each accepted edit saves immediately using a candidate snapshot, cooperating file lock, stale-file check and atomic replacement. A failed command preserves the in-memory bank. Legacy question files remain readable; the first accepted edit converts the selected file to the versioned format. That format supports delimiter characters and multiline text through Base64-encoded UTF-8 fields. Base64 is encoding, not encryption. The old program cannot read the new format; keep a personal backup before using an older binary again.

EOF during a form discards the incomplete command. EOF during a quiz reports answered and unanswered counts separately and labels the score as applying only to answered questions. Duplicate IDs, impossible choice labels, invalid attempts and malformed files are rejected.

```powershell
# JDK 17+ on PATH, from the project root:
.\\run.ps1 -Test
.\\run.ps1
# Use a separate copy for experimentation:
Copy-Item -LiteralPath data/questions.txt -Destination "$env:TEMP/quiz-learning.txt"
.\\run.ps1 -DataPath "$env:TEMP/quiz-learning.txt"
```

The test runner uses only temporary banks. The checked-in example data was not modified. This remains a local Java CLI; the course maps its command and persistence boundaries to future HTTP/SQL CRUD work without claiming a web application exists. File locks coordinate cooperating writers; arbitrary external editors and power-loss durability are outside the verified guarantee.

---

## Original read-only edition walkthrough

'''+t,encoding='utf-8')
w('astraupskill/README.md',r'''
# Learn reliable CRUD with a small question bank

This project is small enough to read completely, yet it now demonstrates problems that appear in larger CRUD applications: stable identity, validated replacement, conflicting editors, durable saves, corrupt input and user cancellation. Your goal is to explain why a successful command is safe to display, then carry those habits into an HTTP service and database later.

Read the current setup at the top of [README](../README.md). Use JDK 17 or newer and run `./run.ps1 -Test`. The runner compiles the source with Java 17 compatibility and all compiler warnings, then executes the regression suite against temporary question files. For interactive work, copy `data/questions.txt` to a disposable location and pass it with `-DataPath`. The supplied example data remains unchanged by this improvement pass.

## Your first useful session

List the bank with menu 4. Create a question using menu 5: choose ID `CRUD1`, prompt “What does an atomic save preserve?”, two choices, answer `A`, and an optional explanation. Exit, restart with the same path and list again. The record survives because the create command persisted it before announcing success. Update it through menu 6 without changing its ID. Cancel a deletion once, verify the question remains, and then confirm deletion by typing `yes`.

The bank can become empty after deleting its final question. An empty versioned bank is valid data; starting a quiz then offers guidance to create a question. A missing or malformed file is a different state and stops startup. Learning to distinguish absence, emptiness and corruption will help you design clearer web APIs.

Follow [the map](01-CODEBASE-MAP.md), [concepts](02-CONCEPTS.md), [worked change](03-WORKED-CHANGE.md) and [testing guide](04-TESTING-AND-DEBUGGING.md). Attempt [practice](05-PRACTICE.md) before reading [solution guidance](06-SOLUTIONS-AND-REVIEW.md). Finish with [the trace lab](07-TRACE-LAB.md) and compare your understanding with [verification](VERIFICATION.md).

Keep a short note for every change: user intent, accepted input, invariant, persistence boundary, failure message and test evidence. For example, “An incomplete question form must not add a half-built record” leads to gathering all fields first, constructing a validated Question, and only then calling create. End-of-input tests prove the boundary.

This is a local CLI and file repository, not an implemented web service. There is no login, database, browser or quiz-attempt history persistence. The course uses the actual Java code to prepare for those next steps. A mid-level engineer should be able to name the delivered guarantees and explain exactly which assumptions stop them from extending to arbitrary deployment environments.
''')
w('astraupskill/01-CODEBASE-MAP.md',r'''
# Read by responsibility and data ownership

Start with [Question.java](../src/quiz/Question.java). A Question has stable identity, prompt, choices, correct answer and explanation. It is now final and immutable: input choices are copied and normalized, and getters expose an immutable list. There can be two through twenty-six choices because labels run from A through Z. A constructor that accepts an unreachable twenty-seventh choice would create invalid state even if the menu usually prevents it.

[QuestionAttempt.java](../src/quiz/QuestionAttempt.java) associates an immutable question snapshot with one valid selected answer. It rejects a label outside that question's choices. [QuizResult.java](../src/quiz/QuizResult.java) owns an immutable list of attempts and the planned question count. Answered, incorrect and unanswered are distinct values. A partial session with one correct answer out of two planned questions has one unanswered question and a 100% score on answered questions; the UI labels that denominator explicitly.

[QuizEngine.java](../src/quiz/QuizEngine.java) handles the interaction loop. Invalid input retries the same question. End-of-input returns a partial result instead of throwing Scanner's exception or fabricating a wrong answer. It receives questions as a list and does not read files. This makes it possible to test scoring and interruption independently of storage.

[QuestionLoader.java](../src/quiz/QuestionLoader.java) is the legacy parser. It reads the original pipe/semicolon format, skips comments, validates every row and rejects duplicate IDs. [QuestionBank.java](../src/quiz/QuestionBank.java) owns the current question collection and persistence commands. It accepts the legacy format on load and writes a versioned format on the first successful edit. Its public create, update and delete methods build candidate collections. Its private commit method owns locking, stale-file comparison and atomic replacement.

[App.java](../src/quiz/App.java) maps menu choices into commands. It gathers a complete form before constructing a Question, asks for deletion confirmation and prints success only after the bank accepts the save. The optional data path allows tests and learners to keep their data separate. [run.ps1](../run.ps1) compiles and launches the selected mode.

Trace a create in this order: App.edit collects fields; Question validates them; QuestionBank.create rejects duplicate identity; commit serializes a candidate; the lock and original-byte comparison arbitrate stale writers; atomic move replaces the file; the bank publishes the new immutable collection; App prints success. Then compare [QuestionBankTest.java](../test/quiz/QuestionBankTest.java) with each step. Find tests that would fail if validation, conflict detection or delayed memory publication were removed.

The lock file is a coordination artifact, not the database. It can remain after the process exits; operating-system lock ownership is tied to the open channel. Deleting the filename while another process uses it is not the intended recovery procedure.
''')
w('astraupskill/02-CONCEPTS.md',r'''
# Identity, snapshots and durable command boundaries

CRUD means creating, reading, updating and deleting records, but reliable behavior depends on rules around those verbs. A question ID identifies one record. An update replaces allowed content under the same ID; it does not quietly create a new record when the ID is missing. A duplicate create fails. A delete of a missing ID returns false, while the CLI tells the learner the record was not found before asking for confirmation.

An immutable object cannot change after construction. Question copies and normalizes its choices and validates its correct answer. QuestionBank exposes immutable lists, so a caller cannot append a record without passing through its persistence commands. Earlier lists remain stable snapshots when the bank accepts another command. This is useful for a quiz already using a particular question set and for tests that need predictable history.

## Candidate state before publication

Suppose create first appends to the visible list and then attempts to write the file. If the write fails, the app would display a question that disappears after restart. The delivered bank instead builds a candidate list, serializes it and persists it before assigning the visible list. Validation failures happen before this boundary. File-read, lock or replacement failures leave the previous in-memory collection intact.

Atomic replacement means the destination switches from one complete file to another through a filesystem operation. The temporary file is created beside the destination so it is on the same filesystem. There is no fallback to an ordinary replacement if atomic move is unsupported. This protects the stated all-or-nothing replacement contract; it is not a proof that bytes survive sudden power loss. The implementation does not force file and directory metadata to stable storage.

## Stale editors and cooperating locks

Two processes can load the same bank. Each remembers its original bytes. During commit, a writer acquires the sidecar lock and compares current bytes with its remembered version. After the first writer saves, the second either encounters the lock or detects changed bytes. It must reopen before trying again. This is analogous to optimistic version checking in a database API, but the scope is the whole file, so unrelated question edits still conflict.

Locks coordinate programs that follow this protocol. A text editor that ignores the sidecar can write between the comparison and replacement. Therefore “no lost updates between arbitrary writers” would be an unsupported claim. State the cooperating-writer assumption clearly.

The versioned format uses a header, encoded fields and a count footer. Base64 allows pipes, semicolons, tabs and newlines without inventing ambiguous escaping. It does not hide answers. Strict UTF-8 decoding and whole-file validation reject malformed content rather than skipping records. A valid empty bank is represented explicitly, while an incomplete footer is treated as corruption. These distinctions translate directly into schema versioning, input validation and migration decisions in larger applications.
''')
w('astraupskill/03-WORKED-CHANGE.md',r'''
# Worked change: save a question without lying about success

The earlier program loaded questions and ran quizzes. Adding CRUD creates a new responsibility: after “Question created and saved,” restarting must recover that question. This walkthrough follows [QuestionBank](../src/quiz/QuestionBank.java) and [App](../src/quiz/App.java) to show where that promise is made.

Begin with a complete user command. App.edit reads the ID, prompt, choice count, each choice, correct answer and optional explanation into local variables. If input ends at any step, it reports that the incomplete edit was not applied. Only after all fields exist does it construct a Question. Constructor validation catches blank text, invalid counts and answer labels. The bank has not changed yet.

Create checks the ID against the current bank, copies the existing list and appends the new immutable Question. Update verifies both existence and unchanged identity, then replaces the matching element in a candidate list. Delete filters the candidate after confirmation in the CLI. All three commands call the same commit boundary, so storage guarantees are not duplicated in three menu branches.

Commit serializes the whole candidate first. It opens the sidecar lock file and attempts a lock. A contending cooperating writer causes a clear failure. With the lock held, it reads the authoritative file and compares it to the bytes captured when this bank loaded or last saved. If they differ, the command is stale. It does not merge records or silently overwrite another writer's changes.

Next it creates a temporary sibling, writes the complete serialized bytes and requests atomic replacement of the destination. Cleanup removes the temporary file if it still exists. Only after successful replacement does the bank update its remembered bytes and publish the new immutable list. Returning from the bank allows App to print success. Follow that order with a debugger and identify every point where an exception leaves the old visible state in place.

## Example failure

Open two copies of the app against the same disposable bank. Both initially contain Q1. The first creates Q2. The second tries to create Q3. Its save must be rejected because it was based on the old file; Q2 remains on disk, and the second app's memory remains its earlier snapshot. Reopen that app, review current questions and reapply Q3 deliberately.

The test suite exercises duplicate identity, failed destination reads, stale instances and held locks. The verification harness also gates two separate JVMs after both load, then releases their saves together and expects one winner. This is stronger than running two saves sequentially and calling the result a concurrency test. The limitation remains explicit: programs that ignore the sidecar lock are outside the protocol, and atomic replacement alone is not power-loss durability.
''')
print('First four quiz course files written')
