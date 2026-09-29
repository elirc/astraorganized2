from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/829e8e7b8605/astraupskill'
docs={
'README.md':'''# Message orchestration workshop

This course follows [postChannelMessage](../src/services/messageService.ts), which turns a channel post into a message, notifications, a sync event, optional attachment associations and an audit entry. No production behavior changes. The improvement is a runnable actual-source lab that makes these responsibilities inspectable without installing the application stack.

Start by predicting the successful trace. Next run [the six-case lab](../tests/message-post-runtime.test.mjs) and compare payloads, not just the returned message id. Then attempt the refusal and failure exercises before opening the solutions. A final design exercise asks how persisted sync events could support recovery after realtime delivery fails.

The lab loads the real role policy and error classes. Repository, channel-access, transaction and realtime adapters expose control flow. It checks content normalization, guest refusal, parent validation, private-channel notification filtering, attachment ownership arguments and audit failure ordering. It does not open Prisma or establish network confidentiality, transaction rollback or exactly-once publication. This distinction is part of the lesson: senior review must identify what a test observes and what the persistence or transport layer must still guarantee.''',
'01-CODEBASE-MAP.md':'''# Source and responsibility map

[messageService.ts](../src/services/messageService.ts) begins posting with canPostMessage from [policy.ts](../src/lib/permissions/policy.ts). A guest is refused before channel access. The channel service resolves access before the transaction starts. Those are separate authorization boundaries; the runtime lab executes the role function but adapts channel lookup.

Inside the transaction, an optional parent is resolved using workspaceId and messageId. Missing or foreign-channel parents produce 404; a parent that is itself a reply produces 409. A valid root has its reply count incremented before the new message is inserted. Message content is trimmed, and normalizedContent also lowercases it.

Workspace members and private-channel memberships determine eligible notification recipients. The sync repository returns an event with an id used later as the realtime cursor. Attachment lookup receives the sender membership and workspace before associations are written. Audit follows these operations. Only after the transaction response does the service call publishWorkspaceRealtimeEvent. Follow workspaceId, membershipId, channelId, messageId and sync id separately: they identify different resources, and substituting one for another can hide a scoping error.''',
'02-CONCEPTS.md':'''# Membership, visibility and durability

Permission to post does not imply that every workspace member may receive a notification. In a private channel, the service permits members represented by channel membership plus workspace owners and administrators. It intersects candidate notifications with eligible membership ids. Mention syntax uses membership identifiers, while the visibility calculation passes through user identifiers; these are related but distinct identities.

The service deduplicates mentions with a Set and removes self-mentions. If a thread author was already mentioned, it avoids adding a second THREAD_REPLY notification for that author. The private-thread fixture combines these rules: duplicated visible mention, self mention, invisible member and thread author.

Transaction grouping is another independent concept. The service passes one client through message, notification, sync, attachment and audit calls. The adapter can verify that discipline and error ordering. It cannot demonstrate a database rollback. Realtime publication is outside that callback, so a committed sync event and a delivered websocket update are different outcomes. A recovery design should name the durable source of truth and replay cursor rather than treating a publish call as proof every client received the message.''',
'03-WORKED-CHANGE.md':'''# Worked addition: observe the real service

The production snapshot is [messageService.ts.original.txt](snapshots/messageService.ts.original.txt). The new test loads that same service behavior through a TypeScript VM bridge. Its fixture supplies a transaction object, records operation arguments and returns realistic message and sync-event objects. Returning only a message is insufficient: after the transaction, the service reads the sync event id, type, entity id and payload.

For content ` Hello `, expect content `Hello` and normalizedContent `hello`. The successful root trace is channel, tx, create, members, notify, sync, audit, tx-done, publish. The published cursor is the event id, not the message id. Exact payload assertions verify workspace and author membership as well as text.

The private-thread case adds parent lookup, reply-count increment and private-membership lookup. It verifies one MENTION for the visible peer despite duplicate syntax and an existing thread relationship. The attachment case checks the query includes uploadedByMembershipId and only returned pending ids are associated. These additions teach orchestration through concrete observations instead of duplicating business rules in the fixture. All production source remains unchanged.''',
'04-TESTING-AND-DEBUGGING.md':'''# Diagnose the first incorrect boundary

Run `node --experimental-vm-modules --test tests/message-post-runtime.test.mjs` from the project directory. Each case creates its own fixture. The transaction adapter records tx-done only after the callback resolves; an injected audit exception therefore prevents both that marker and publish. It does not simulate database rollback.

If guest refusal records a channel lookup, inspect policy ordering. If a foreign-channel parent reaches create, inspect the parent channel comparison. If a duplicate thread notification appears, compare mention deduplication with the thread-author condition. If an invisible member is notified, inspect the user-id to membership-id filtering step before altering the expected result.

A missing property after tx-done usually means the adapter returned an incomplete contract. Read the production consumer first: syncEvent.id is required for the cursor. Do not patch production to accommodate an unrealistic test double. Likewise, the real errors carry status, so assertions inspect that field rather than introducing a different fake error shape. For a database follow-up, fail audit insertion and inspect persisted message, reply count and sync rows from another connection; a rejected callback alone cannot prove those rows rolled back.''',
'05-PRACTICE.md':'''# Prediction and design exercises

Complete these before reading the solutions. Write a call sequence and expected payload for each; include the first call that must be absent on refusal.

1. A MEMBER posts ` Hello ` without a parent or attachments. Predict both stored text fields and the identifier used as realtime cursor.
2. A GUEST submits the same request. Predict the status and whether channel access or transaction creation occurs.
3. A MEMBER replies to a missing parent, a parent in another channel, and a reply rather than a root. Compare the three failures and any counter writes.
4. In a private thread, mention the visible author twice, yourself once and an invisible member once. Predict recipients and notification types.
5. Supply attachment ids owned and foreign, while the pending lookup returns only owned. Write its scope arguments and the eventual association list.
6. Inject an audit failure. Mark attempted operations, transaction completion and realtime publication separately.

For the design challenge, propose a durable replay mechanism after realtime publication fails. Explain how a client cursor and persisted sync event could cooperate, then identify the integration tests needed before claiming reliable delivery.''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Solutions and review criteria

The root post stores trimmed content Hello and lowercase normalizedContent hello. Its publish payload uses sync id 7 as cursor and m1 as entityId. Guest posting throws the real AuthorizationError with status403 before any recorded operation. Missing and foreign-channel thread roots return404; a reply parent returns409. All stop after parent lookup, before increment or create.

The private fixture produces one MENTION for the visible peer. Duplicate mentions collapse, self is excluded, the invisible member is filtered, and the mentioned thread author receives no additional THREAD_REPLY. Attachment lookup includes workspace w and the sender membership; only owned is associated from the returned fixture. These assertions verify service arguments, not the repository implementation.

An audit error preserves error identity and prevents tx-done and publish. Earlier calls have been attempted; persistence rollback remains unverified. Grade solutions on exact ids, operation order, real error status, transaction-client reuse and stated limits. Reject conclusions that equate a sync row with network delivery or copied permission logic with actual authorization coverage. A replay proposal needs durable cursor semantics, duplicate handling and reconnect integration tests, not just another publish invocation.''',
'07-TRACE-LAB.md':'''# Trace worksheet

Create columns for step, input ids, transaction client, return object and externally visible effect. Populate the successful root trace using the runtime call array. The channel access step is outside tx; create through audit share the supplied client; publish occurs after tx-done. The returned message and returned sync event serve different consumers.

| Scenario | Last relevant boundary | Later operations absent |
|---|---|---|
| Guest | real role guard | channel and tx |
| Access adapter failure | channel | tx and writes |
| Invalid thread parent | parent lookup | increment and create |
| Audit failure | audit attempt | tx-done and publish |
| Successful root | publish | none in this flow |

For the private case, annotate how workspace user ids become a valid membership-id set. For attachments, annotate the difference between requested ids and returned owned ids. Compare your worksheet with [the source test](../tests/message-post-runtime.test.mjs), then label each conclusion as actual service execution, adapter observation or unexecuted provider guarantee. This exercise makes partial failures visible without pretending the fixture is a database. Extend it later with a genuine transaction trace and realtime reconnect experiment.''',
'VERIFICATION.md':'''# Verification and limits

Command: `node --experimental-vm-modules --test tests/message-post-runtime.test.mjs` from this project directory. Six cases execute the production posting service, real role policy and real error classes. They cover normalized payload and post-transaction publish, guest/access refusal, invalid-parent matrix, private mention filtering, attachment scope arguments and audit failure ordering.

Channel access, repositories, transaction execution and realtime transport are explicit adapters. A shared client assertion ensures the service passes the same supplied object; it does not establish Prisma atomicity. The attachment adapter returns an owned row by construction, so the test proves forwarding of the ownership filter and returned ids, not SQL filtering. The private-channel fixture checks the service notification calculation, not the confidentiality of an actual transport connection.

No Next route, live Prisma, database rollback, concurrent thread counter update, network delivery or reconnect replay ran. Production code is unchanged and preserved in the linked source snapshot. Before a release, run provider-backed failure and concurrency tests and verify realtime replay semantics separately. The focused lab supports the specific six cases and the documented source call order only.'''
}
for name,text in docs.items():
 (P/name).write_text(text+'\n',encoding='utf-8')
 print(name,len(text.split()))
