from pathlib import Path
import json
from course_writer import write_course

test='tests/integration/repair.test.ts'
ops='src/server/operations.ts'
chapters={}
def add(name,title,body,file=test,anchor='test("late completion failure',count=105):
    chapters[name]=(title,body,[(file,anchor,count)])

add('README.md','Prove late repair failure rolls back and can recover','''
Helios already completes a repair through a PostgreSQL transaction. The existing workflow consumes reserved inventory, completes the work order, releases the crew, resolves the incident, records audit history, creates a postmortem, and saves the command receipt. The improvement adds evidence for a failure after most of those effects have been attempted.

The new regression installs a test-owned trigger that rejects the postmortem insert. It then invokes the real complete_repair operation and checks that earlier writes rolled back. After removing the trigger, it retries the exact same command identifier and payload, then replays that command again. The successful retry must complete once, and the replay must return the stored result without consuming inventory twice.

This is a focused verification improvement to the existing application, not a replacement of the completed local workflow program. Its prior source, prompts, and execution record remain intact. The new owned-database helper provides a reproducible environment for the repository checks, local API smoke, and affected repair browser flow.

Read the map and transaction concepts, then trace the failure through the worked example. Practice and the separate answers distinguish rollback from idempotent replay. Software verification does not establish human mastery; these lessons remain available for later review without interrupting the local build work.
''')
add('01-CODEBASE-MAP.md','Locate the command receipt and the maintenance transaction','''
executeOperation validates the command and delegates to idempotentCommand. That wrapper checks operator authority, starts a transaction, and takes an advisory transaction lock scoped to organization and command identifier. It looks for a previous receipt whose actor and payload must match. A valid replay returns the saved result before executing the domain operation again.

New commands run operationTx on the same PoolClient. Repair actions reach maintenanceCommandTx, which applies the existing work-order, checklist, crew, inventory, and verification rules. Only after work succeeds does idempotentCommand insert operation_commands. That receipt therefore belongs to the same transaction as the repair effects.

The integration test uses repairFixture and command helpers to create a legitimate VERIFYING repair with reserved stock, an assigned crew, completed tasks, and fresh nominal telemetry. The failure is injected at the database postmortem boundary rather than replacing the domain function with a mock.

scripts/test-owned-postgres.py creates a fresh loopback helios_test database with a dedicated role. Its modes run the full check, API smoke, or affected browser case sequentially. The existing application database and packaged preview are not part of this fixture. Follow these boundaries when distinguishing the new regression from the historical completed program.
''',file=ops,anchor='export async function idempotentCommand',count=100)
add('02-CONCEPTS.md','Rollback leaves no receipt; replay requires one','''
A command receipt is evidence that an operation committed. If a repair fails late, saving its receipt anyway would make the next request appear already complete even though the domain effects rolled back. Conversely, committing domain effects without the receipt would let a retry repeat work. Keeping both in one transaction binds the replay decision to durable success.

Rollback and replay are different outcomes. The injected failure should leave the work order VERIFYING, incident ACKNOWLEDGED, crew unavailable, and inventory still reserved. It must create neither a postmortem nor a command receipt, and it must not add audit rows. Retrying after removing the failure is therefore a new successful execution, not a replay.

After that execution commits, sending the same command again returns replayed true. The saved actor and payload must match; the existing wrapper rejects reuse of an identifier for different input or another actor. The advisory lock coordinates concurrent use of the same command key within the organization.

The regression checks database state after the exception instead of assuming that a rejected promise proves rollback. A function can throw after some independent writes have committed. Only durable-state assertions across the affected tables substantiate the atomicity contract being exercised here.
''',file=ops,anchor='export async function idempotentCommand',count=100)
add('03-WORKED-CHANGE.md','Fail at the final postmortem insert','''
The new test first prepares a valid repair using the existing application commands. It reserves one local item, assigns an eligible crew member, starts repair, completes checklist tasks in order, begins verification, and supplies fresh nominal telemetry. This setup avoids confusing a prerequisite rejection with the intended late database failure.

It captures the organization's audit count and creates a PostgreSQL trigger function that raises an injected exception before postmortem insertion. The real executeOperation call must reject with that message. The test then queries work-order status, incident status, crew availability, inventory counts, postmortems, audit rows, and the command receipt.

The trigger and function are removed in finally so an assertion failure cannot leave failure injection active for later tests. The same command object is then submitted twice: first recovery, then replay. Assertions check replay flags, one inventory consumption, resolved incident state, one postmortem, and one receipt.

Production repair code already contains the transaction and is preserved. The added helper and regression make that behavior reviewable under a concrete late failure. The execution plan records this bounded scope separately from the prior local M01–M15 completion record, avoiding a claim that the earlier application was rebuilt in this pass.
''')
add('04-TESTING-AND-DEBUGGING.md','Inspect all effects after the rejected transaction','''
The regression runs on real PostgreSQL. Its trigger executes inside the transaction that attempts to insert the postmortem, causing the preceding repair writes to roll back. Repository mocks or an in-memory model could imitate those final values without exercising the database behavior, so they are not substituted here.

The audit assertion compares with a captured baseline rather than requiring an empty table. Fixture setup legitimately creates audit history. The command-receipt assertion uses the exact command identifier, while postmortem checks use the fixture incident. Those scopes distinguish this attempted repair from unrelated setup effects.

When the expected exception is missing, verify that the postmortem insert was reached and that the trigger was installed in the owned test database. When an earlier prerequisite fails, inspect checklist completion and fresh telemetry rather than weakening the late-failure assertion. When cleanup fails, keep that failure visible because an active trigger can contaminate subsequent tests.

The repository's broader acceptance commands include lint, type generation, unit tests, integration tests, a production build, local API smoke, and the coolant-repair browser flow. Each provides different evidence. The trigger regression proves a local persistence property; browser success demonstrates an affected visible workflow but does not replace the database rollback assertions.
''',anchor='  const auditBefore',count=100)
add('05-PRACTICE.md','Separate failed execution, recovery, and replay','''
Exercise one: list the expected state of the work order, incident, crew, inventory, postmortem table, audit count, and command receipt immediately after the injected failure. Explain why the correct inventory result is still reserved rather than consumed or released.

Exercise two: remove the trigger and resend the exact command object. Predict replayed and the durable receipt count. Then send it again and predict the second replay flag and inventory values. State why changing the command identifier between these calls would fail to test the intended recovery contract.

Exercise three: move receipt insertion outside the transaction in a disposable copy. Describe two possible inconsistencies depending on whether the receipt or domain effects commit first. Identify which existing assertions would catch the late-failure version of that defect.

Exercise four: omit finally cleanup and let an assertion fail. Explain how the next test could fail for an unrelated reason. Propose a cleanup strategy that removes only the test-owned trigger and function without resetting the user's development database.

Exercise five: compare a passing targeted integration test with a passing browser repair flow. Identify what each establishes and what remains unverified about deployment, real physical equipment, external models, and the learner's understanding. Keep those claims separate in a review report.
''',anchor='  try {\n    await assert.rejects(executeOperation(actor, input, pool)',count=105)
add('06-SOLUTIONS-AND-REVIEW.md','Read the receipt as a commit witness','''
After failure, the work order remains VERIFYING, the incident remains ACKNOWLEDGED, and the assigned crew remains unavailable. The local stock is one on hand and one reserved. No postmortem or receipt exists for the attempted completion, and the organization's audit count equals its captured baseline. Those values show that earlier repair effects did not escape the failed transaction.

The recovery request uses the same identifier and payload and returns replayed false because the failed attempt left no receipt. The next identical request returns replayed true. Stock is consumed once, the incident is resolved, and the fixture has one postmortem and one command receipt. A new identifier would exercise another command rather than prove recovery of the original one.

Saving a receipt independently can claim success for rolled-back work or leave committed effects without replay protection. The wrapper's transaction ties receipt insertion to the domain operation. Finally cleanup removes the specifically named failure trigger and function, preventing contamination even when assertions fail.

The targeted test establishes rollback and replay in the owned PostgreSQL environment. The browser flow establishes the visible repair sequence under the configured local simulation. Neither certifies real-world equipment, public deployment, live-model behavior, or human mastery. Review the new execution plan and accepted logs without rewriting the historical baseline's claims.
''',file=ops,anchor='export async function idempotentCommand',count=100)
add('07-TRACE-LAB.md','Trace the same command through three attempts','''
Draw three columns labeled failed attempt, recovery, and replay. Use one command identifier across all columns. In the first, acquire the organization-scoped advisory lock, observe no receipt, and execute the real maintenance operation. Mark the inventory, work-order, crew, incident, and audit writes as tentative until commit.

At the postmortem insert, fire the test trigger. Roll back the transaction and query the database from outside it. Record the original VERIFYING repair and reserved inventory, unchanged audit count, and absent receipt. The exception alone is not your evidence; the stored values are.

Remove the trigger and start the second column with the same input. Again there is no receipt, so the operation executes. This time the postmortem and receipt are written and the transaction commits. Record replayed false and one durable completion effect.

In the third column, find the saved receipt before executing maintenance. Confirm actor and payload match, then return its result with replayed true. No second inventory consumption or postmortem should occur. For a final thought experiment, alter the payload while keeping the identifier and trace the existing IDEMPOTENCY_CONFLICT branch. That is a rejected identifier reuse, not a valid replay of the same command.
''',anchor='  const recovered = await executeOperation',count=100)
add('VERIFICATION.md','Preserve the baseline and report new evidence','''
The new acceptance evidence belongs to execution plan 003. The prior local workflow program and its recorded results remain historical baseline evidence. This improvement adds one late-failure PostgreSQL regression, an owned local verification helper, and source-based learning material; it does not claim to reimplement the completed application.

The helper creates a fresh helios_test database bound to loopback, supplies fixture-only model and session settings, and runs requested checks there. API smoke starts an owned local application on a free port, waits for health, runs the existing smoke programs, and stops that process. Browser verification uses the existing Playwright configuration and the affected coolant-repair case. Database and browser modes run sequentially because they reset fixture data.

The first full check passed lint, types, and eleven unit tests, then correctly stopped at the integration isolation guard because the new launcher supplied identical application and test URLs. The corrected launcher creates separate helios and helios_test databases inside its owned temporary cluster. Integration assertions remain unchanged. Only the isolated HTTP smoke server is pointed at the test fixture after those checks; no existing database is used.

The recorded commands below determine which of these checks completed successfully. A dependency install, a partial build, or pending browser process must not be described as acceptance. Test counts use distinct cases, while smoke programs are identified separately. Missing or failed verification remains explicit until resolved.

The curriculum also appears under upskilling/repair-rollback to follow this repository's learning-material convention. Original prompts and prior learning records are preserved. Passing software checks is not evidence of human mastery, and no quiz or approval interruption is required for this local BUILD task. External providers and the existing packaged preview are outside the owned test environment.
''',file='scripts/test-owned-postgres.py',anchor='try:',count=100)
write_course('a8435f7ed53c',chapters,'Trace a late PostgreSQL repair failure, same-command recovery, and idempotent replay.')
b=Path(__file__).resolve().parent.parent
p=b/'stage/a8435f7ed53c'
learning=p/'upskilling/repair-rollback';learning.mkdir(parents=True,exist_ok=True)
for name in chapters:
    text=(p/'astraupskill'/name).read_text(encoding='utf-8').replace('](../','](../../')
    (learning/name).write_text(text,encoding='utf-8')
(b/'specs/a8435f7ed53c.json').write_text(json.dumps({'changedFiles':[],'summary':['Added a real PostgreSQL late-postmortem failure regression proving repair effects and command receipt roll back together.','Verified same-command recovery and replay without rewriting the existing repair implementation.','Added an owned PostgreSQL/API/browser verification helper and source-based guides, including the repository upskilling location.'],'limits':['Local fixture workflows do not certify real physical systems, external model providers or public deployment.','Human learning remains unassessed; prior completed program evidence is preserved separately.']},indent=2),encoding='utf-8')
