from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent;D=B/'stage/83297bdf668f/astraupskill'
changes={
'README.md': [('supplies explicit repository, policy, notification, payment, and error contracts.', 'loads the real order policy and ApiError class while supplying explicit repository, notification, payment and unused Zod-error contracts.'),('It proves success, stale conflict, seller ownership denial, and unrelated persistence rethrow.', 'Its six cases cover accepted admin and in-scope seller transitions, stale conflict, seller ownership denial, real-policy rejection and unrelated persistence rethrow.')],
'02-CONCEPTS.md': [('while the other later writes `SHIPPED` or repeats an event based on stale assumptions.', 'while the other later writes `REFUNDED` or repeats an event based on stale assumptions.'),('The runtime test demonstrates the distinction with four branches.', 'The runtime test demonstrates the distinction with six cases and the real transition policy.'),('Those assertions make state, authorization, and operational failure separate review concerns.', 'Additional cases preserve an in-scope seller fulfillment transition and reject an illegal transition through the real domain module. Those assertions make state, authorization, and operational failure separate review concerns. Status equality is not a general version check: it does not detect changes to other order fields or seller splits, or an intervening change back to the same status.')],
'03-WORKED-CHANGE.md': [('if (error?.code === "P2025") {','if (error && typeof error === "object" && "code" in error && error.code === "P2025") {')],
'04-TESTING-AND-DEBUGGING.md': [('The test stubs only its module contracts: a Prisma-like order repository, an `ApiError`, transition policy, notification function, refund function, and `server-only`.', 'The test loads the real transition policy and ApiError module. It substitutes the Prisma-like repository, notification and refund functions, `server-only`, and the unused Zod error class.'),('`updateArgs.where`','`updates[0].where`'),('`updateArgs.data.events.create`','`updates[0].data.events.create`')],
'05-PRACTICE.md': [('the actor is a buyer', 'the actor is an admin')],
'06-SOLUTIONS-AND-REVIEW.md': [('Status proves the row still has the state that policy and seller scope inspected.', 'Status requires the row to retain the state that the transition policy inspected. Seller scope is checked separately and is not revalidated by the status predicate.')],
'07-TRACE-LAB.md': [('Accepted buyer', 'Accepted admin'),('buyer path','admin path'),('`PLACED` | `PLACED` | `PLACED` | `PLACED`','`PLACED` | `PLACED` | `PAID` | `PLACED`'),('Change the actor to a seller owning a split and request `SHIPPED`; policy and ownership pass', 'For a separate accepted seller trace, start with an order already `PAID`, change the actor to a seller owning a split, and request `SHIPPED`; policy and ownership then pass')],
'VERIFICATION.md': [('Result: four tests passed and zero failed.', 'Final reviewed result: six tests passed and zero failed.'),('The fourth verified an unrelated persistence Error is rethrown unchanged and produces no side effects.', 'The fourth makes the update operation inside the catch throw an unrelated Error and verifies its identity is preserved. Two additional cases reject an illegal transition using the real domain rule and preserve the in-scope seller fulfillment path.'),('explicit contracts for Prisma, order policy, errors, payment, notification, and `server-only`.', 'actual order-policy and ApiError modules plus explicit contracts for Prisma, payment, notification, unused Zod error handling and `server-only`.')]
}
for name,pairs in changes.items():
    p=D/name;t=p.read_text(encoding='utf-8')
    for old,new in pairs:
        assert old in t,(name,old)
        t=t.replace(old,new)
    p.write_text(t,encoding='utf-8')
p=B/'specs/83297bdf668f.json';s=json.loads(p.read_text())
s['summary'][2]='Add six production-source runtime cases using the real transition policy and ApiError class, plus a source-specific CRUD course on state, seller scope and side effects.'
s['limits'].append('Status equality does not detect unrelated field or seller-split changes, or a status changing away and back. The transaction double does not prove real rollback; HTTP role/session and Zod validation are outside the executed suite.')
p.write_text(json.dumps(s,indent=2),encoding='utf-8')
print('Corrected actor and transition examples, six-case evidence and status-only limits.')
