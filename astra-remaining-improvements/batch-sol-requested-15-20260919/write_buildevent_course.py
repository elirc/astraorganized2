from pathlib import Path
import json
from course_writer import write_course

order='apps/api/src/services/order.service.ts'
checkin='apps/api/src/services/checkin.service.ts'
test='apps/api/tests/order-checkin.test.ts'
chapters={}
def add(name,title,body,file=order,anchor='',count=100):
    chapters[name]=(title,body,[(file,anchor,count)])

add('README.md','Make checkout, completion, and scanning retry-safe','''
BuildEvent connects an order to payment setup, inventory consumption, issued tickets, and venue check-in. Repeated requests occur naturally at each boundary. A retry should not create a different payment intent, consume reserved stock twice, or admit the same ticket twice. A signed ticket for another event must not become valid merely because a staff member can scan at the current event.

The improvement uses a stable provider idempotency key for checkout, a conditional local payment-intent binding, a one-winner order-completion update, and an event-scoped ticket state transition. It also validates payment amounts before any provider call and checks the actual final state when a free checkout loses a completion race.

This course follows those mechanisms through the service code and controlled regressions. Start with the map, then distinguish provider idempotency from local transactions and conditional updates. Practice asks you to predict races and rejected requests; the separate solutions explain the final state and caller response.

The new tests simulate Prisma operations, payment responses, and QR verification. They establish service contracts and predicates, not real Stripe exactly-once delivery, cryptographic verification, or database isolation. The verification chapter records the commands that actually ran and preserves those limits rather than treating every passing fixture as an external integration test.
''')
add('01-CODEBASE-MAP.md','Find three different state boundaries','''
createOrderService exposes checkout and completeOrder. checkout loads the order, checks owner, pending state, and expiry, then chooses free completion or paid payment setup. Paid checkout validates the amount, reuses an existing intent when present, or creates one using a key derived from the stable order identifier.

The returned intent is bound with an updateMany predicate including owner, PENDING state, amount, captured updatedAt, and a null existing intent. A losing caller reloads the order and reconciles with the persisted intent rather than overwriting it unconditionally.

completeOrder performs the order claim, inventory changes, and ticket inserts within one Prisma transaction. QR generation follows commit. The check-in route authorizes staff for the route event and passes that event identifier into createCheckinService. The service binds both the decoded payload and stored ticket to that event before attempting VALID-to-CHECKED_IN.

The regression file supplies stateful fakes at these boundaries. Its conditional-update simulations expose competing requests and record the predicates used. When investigating a failure, separate provider intent creation, local order completion, QR generation, and scanning; success in one does not automatically establish success in the others.
''',file=checkin)
add('02-CONCEPTS.md','Idempotency keys are not database transactions','''
Two paid checkout requests may both reach paymentIntents.create. The stable order-derived key asks the provider to associate those requests with the same operation. The local fake intentionally observes two calls with one key, so the test does not claim that the application prevented every duplicate HTTP request.

Conditional persistence protects the local association. The order must still match its captured state before a newly returned intent is stored. A competing winner's intent is reread when necessary. A provider effect and the local update are separate systems; losing the local predicate does not prove the provider created nothing.

Order completion uses a different mechanism. PENDING-to-COMPLETED is claimed inside the same transaction as stock and ticket writes. Only the winner proceeds with those changes. Check-in needs a single conditional ticket update scoped to event and VALID status; a loser reads the stored check-in metadata.

Amount validation protects both new and existing-intent paths. Finite positive totals must convert to safe integer cents of at least one. Exact zero follows the free path. A cancelled free order cannot be reported completed merely because the original snapshot was pending. These contracts complement one another and require different assertions.
''',anchor='      const totalAmount =')
add('03-WORKED-CHANGE.md','Bind the decision to the state-changing write','''
Paid checkout now creates an intent with an idempotency key based on order.id. The local update includes the captured owner, status, amount, version, and empty intent field. If no row changes, the service reloads the order, rejects incompatible state, or returns the already persisted intent's client secret. The amount guard runs before retrieving an existing intent as well as before creating one.

Completion reloads the full order within a transaction and claims only PENDING. A zero-row claim returns false before inventory or ticket writes. The winning transaction increments sold stock, decrements reservations, advances tier versions, and creates the required tickets. QR storage occurs afterward and remains a separate failure boundary.

The free checkout caller now examines a lost completion result. It reports success only if a reread confirms the same owner's order is actually COMPLETED. A concurrent cancellation produces a conflict rather than a false success message.

Check-in verifies the payload event and stored ticket event, then changes only a VALID ticket for the route event. A losing scan refetches current status and staff metadata. Review each predicate against the corresponding pre-read; retaining a precondition only in the read phase would reopen the race it is meant to prevent.
''',anchor='    async completeOrder',count=100)
add('04-TESTING-AND-DEBUGGING.md','Use stateful fakes and state their limits','''
The checkout fake lets two callers read the same pending snapshot. It records both provider keys and simulates a one-winner intent binding. The assertions check the key and every important update predicate, then verify both callers return the same fixture client secret. This is provider-contract simulation, not a live payment run.

Invalid amount cases include nonfinite, negative, unsafe-cent, and invalid-existing-intent inputs. Both create and retrieve must remain unused. The free-checkout cancellation case changes the transaction's order view to CANCELLED and requires a conflict instead of a completed response.

The completion fake records inventory updates and ticket rows while its conditional claim chooses one winner. The scan fake similarly retains checked-in time and staff identity so the losing request must report stored metadata. A foreign-event QR is rejected before any ticket mutation.

These fakes do not implement a database's locking or rollback engine. They prove that the service issues the intended conditional operations and handles their outcomes. Separate database integration would be needed to certify isolation and transactional rollback. QR verification is mocked in this file, so the event-binding assertion must not be described as a cryptographic test. Preserve these boundaries when summarizing a successful run.
''',file=test,anchor="describe('checkout retry safety",count=110)
add('05-PRACTICE.md','Predict each competing request','''
Exercise one: start two paid checkouts for the same pending order. Both call the provider before either stores the intent. Predict the idempotency keys, local update counts, and returned secret when the provider returns the same intent for both. Explain why two provider calls are compatible with this test's contract.

Exercise two: change the order amount or cancel it after the provider call but before the local binding. Identify which predicate prevents the stale association and what the service should report. Describe the remote uncertainty that remains outside the local database operation.

Exercise three: race two completeOrder calls for an order containing two tickets. Predict the boolean results, number of inventory updates, and issued ticket count. Then make a free order become cancelled during completion and predict the checkout response.

Exercise four: scan one valid ticket concurrently with two staff identities. State how many successes are allowed and where the losing request gets its timestamp and staff name. Explain why returning the losing scanner's own identity would be misleading.

Exercise five: present a correctly decoded QR whose event differs from the authorized route event. Identify the rejection point and which database mutation must remain unused. Distinguish event binding from the separate signature-verification responsibility.
''',file=test,anchor="  it('lets one concurrent completion",count=105)
add('06-SOLUTIONS-AND-REVIEW.md','Review the winner and the losing response','''
Both paid requests use order:<id>:payment-intent. One local binding wins and the other reconciles with the stored association. The fake provider can receive two calls while returning one logical fixture intent. That demonstrates key reuse and local response handling, not a universal exactly-once guarantee.

A changed amount, version, status, owner, or existing intent can prevent the captured update from matching. The reread determines whether to return the persisted winner or report conflict. A local rejection cannot undo an already created provider object; operational reconciliation remains a separate concern.

Concurrent completion yields one true and one false result, one inventory adjustment for the fixture tier, and two tickets. A free checkout that loses to cancellation must return conflict. Losing to an already completed state can safely return completion only after checking the current owner's order.

Concurrent scans allow one success. The loser reads stored checkedInAt and checkedInBy details from the winning transition. A QR bound to another event is rejected before mutation, even if its decoding succeeded and the staff member is authorized for the route event.

Reviewers should distinguish transaction-contained stock and ticket writes from post-commit QR work, and simulated conditional updates from real database isolation. The test names and final report should retain those limits rather than imply provider, cryptographic, or deployed workflow certification.
''',file=checkin,count=100)
add('07-TRACE-LAB.md','Follow a scan that loses the race','''
Start with a ticket in VALID state for event-1. Both staff requests decode a payload naming that ticket, matching event, and ticket code. They load the same initial ticket snapshot. Mark these reads as observations rather than ownership of the future transition.

Let staff A execute the conditional update first. The database predicate includes ticket identifier, event-1, and VALID. Its successful update stores CHECKED_IN, a timestamp, and A's staff identifier. Staff B's identical state predicate now changes zero rows.

Follow B into the reread branch. The response reports Already checked in using the persisted timestamp and staff relation. It must not invent a second successful admission or use B's own attempted values. Compare this trace with the stateful fake, which records the predicate and preserves the winner's metadata.

Repeat with a payload naming event-2 while the route is event-1. The service stops before looking up or changing the ticket. Repeat with matching payload but a stored ticket from another event; the second binding check rejects it. These traces show why both payload and stored relationships are checked. They do not replace a real signature test because the fixture controls QR decoding directly.
''',file=checkin,anchor='      const checkedInAt',count=100)
add('VERIFICATION.md','Keep simulated and external guarantees separate','''
The accepted API tests and type checks are recorded below with their exact command arguments and terminal results. Installation or Prisma client generation is setup evidence, not a passing behavioral suite. Failed attempts remain in the campaign history and are not silently converted into successes.

The first API attempt could not resolve the ticket-renderer package before its compiled output existed. Building both local packages resolved that setup failure. A later lint run found unused parameters in the new provider fake; the final fixture uses them to assert the exact amount, currency, metadata, and stable idempotency key. The full API suite then passed eleven cases. Workspace lint retains three existing web image-usage warnings, so this is not a claim of a warning-free application.

The added regression file simulates Prisma, Stripe intent calls, and QR verification. It checks stable provider keys, conditional binding predicates, amount guards, one-winner completion, the free-checkout cancellation response, event binding, and competing scan metadata. Its stateful fakes are deliberately stronger than unconditional mock returns but still do not implement real database rollback or provider idempotency storage.

No payment is charged and no live Stripe webhook is exercised. No cryptographic claim follows from the mocked QR decoder. The route's existing event-access middleware remains responsible for staff authorization; the service additionally binds the ticket and payload to that event.

QR generation occurs after the completion transaction. A failure there does not roll back committed inventory and tickets, and this change does not add a recovery worker for that separate boundary. Provider effects can likewise outlive a failed local binding. These limits are part of the result, alongside original snapshots and source-linked exercises. They identify where additional integration or operational work would need its own concrete contract and evidence.
''',file=test,anchor="describe('event-scoped atomic check-in",count=110)
write_course('af5130b3aad2',chapters,'Trace checkout idempotency, conditional completion, free-order race handling, and event-bound scanning.')
b=Path(__file__).resolve().parent.parent
(b/'specs/af5130b3aad2.json').write_text(json.dumps({'changedFiles':[],'summary':['Used stable checkout provider keys, guarded amount validation and conditional payment-intent persistence.','Made inventory/ticket completion and event-bound check-in choose one winner, and rejected falsely successful cancelled free checkout.','Added stateful provider/persistence regressions and nine source-based guide chapters.'],'limits':['Tests simulate Prisma, Stripe and QR verification; they do not establish real database isolation, cryptographic verification or provider exactly-once delivery.','QR generation remains post-commit; remote provider effects and QR recovery are separate operational boundaries.']},indent=2),encoding='utf-8')
