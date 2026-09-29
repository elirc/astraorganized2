from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/7b18281f562f/astraupskill'
for f in P.glob('*.md'):
    if f.name.startswith('08-'):continue
    t=f.read_text(encoding='utf-8-sig').replace('â†’','→').replace('â€™','’')
    t=t.replace('Afterward, only `AppError` is converted.','Afterward, an `AppError` is converted only when its code is not `INTERNAL_ERROR`.')
    t=t.replace('An `AppError` represents a known business result:', 'An `AppError` with a non-`INTERNAL_ERROR` code represents an expected refusal here:')
    t=t.replace('Rethrowing allows the action layer and logging wrapper to classify the incident as a system failure.','Rethrowing rejects the bulk operation at its caller. The unchanged logging wrapper has its own classification policy, which these tests do not execute.')
    t=t.replace('uses shared VM contracts for the real `AppError` class, domain decisions, permission, audit, and logging.','loads the real `AppError` class in the same VM through [bulk-enroll-entry.ts](../tests/bulk-enroll-entry.ts). Domain decisions, permission, audit, and logging are explicit doubles. The transaction double returns or rejects without executing its callback, so enrollment persistence and audit are not exercised.')
    t=t.replace('Native integration should later verify that real Prisma errors reach the action boundary and are logged as failures.','Native integration should later verify how real Prisma errors reach the action boundary and how the unchanged logger records them.')
    t=t.replace('| Event | AppError | unexpected Error |','| Event | Non-INTERNAL_ERROR AppError | unexpected Error |')
    t=t.replace('A per-student `AppError` from `enrollStudent` is different and becomes a failed row.','A per-student non-`INTERNAL_ERROR` `AppError` from `enrollStudent` is different and becomes a failed row.')
    t=t.replace('If a later student has a business refusal after earlier success, the earlier transaction stays committed because transactions are per student.','If a later student has either a business refusal or an operational failure after earlier success, the earlier transaction stays committed because transactions are per student. An operational rejection returns no normal result list; it does not undo that earlier work. The test only retains simulated successes, so this database conclusion comes from transaction-boundary inspection.')
    t=t.replace('node --experimental-vm-modules --test astra-remaining-improvements/stage/7b18281f562f/tests/runtime-bulk-enroll.test.mjs','node --experimental-vm-modules --test tests/runtime-bulk-enroll.test.mjs')
    t=t.replace('Executed from the workspace root:','Run from this project root (the captured check ran from its staged project root):')
    t=t.replace('verified that a real `AppError` becomes one failed student result with its user message.','verified that each of the four expected real `AppError` codes becomes an ordered failed student result with its user message.')
    if f.name=='06-SOLUTIONS-AND-REVIEW.md':
        t+='\nFor the true-or-false review: every AppError is a row refusal is false because INTERNAL_ERROR escapes; an AppError has a user message is true; per-student transactions imply one atomic batch is false; an escaping error can reach the outer logger is true, without asserting its severity; a fake proves Prisma rollback is false. Award two points per correct answer with a source-based explanation. A complete answer also separates pre-loop permission rejection from exceptions caught during an individual enrollment.\n'
    f.write_text(t,encoding='utf-8')
