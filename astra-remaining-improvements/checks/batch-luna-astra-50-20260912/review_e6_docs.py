from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parents[2];ID='20574f0b81b4';P=B/'stage'/ID;U=P/'astraupskill'
for p in U.glob('*.md'):
 t=p.read_text(encoding='utf-8').split('## Source-grounded review notes')[0].strip()+'\n'
 t=t.replace('\ufffd', "'")
 t=t.replace('keeps PATCH omission and null distinct','preserves omitted PATCH fields')
 t=t.replace('Tests use a factory-created seed state and synthetic Fastify/socket fixtures.', 'Tests use a factory-created seed state and registered handlers with a fake socket transport. No Fastify HTTP request is injected by the delivered suite.')
 t=t.replace('Candidate `statusId` and `assigneeMemberId` are checked against workspace-owned records.', 'The caller must be a workspace member. Candidate `statusId` must belong to the existing issue type and workspace; `assigneeMemberId` must belong to the workspace.')
 p.write_text(t,encoding='utf-8')
extras={
'README.md':'''## Start with one observable behavior

Begin with an authorized title edit. Find the seeded workspace, an issue in that workspace, and its current status. Call `updateIssue` with only a title. The title changes, while omitted status and assignee fields retain their values. Next, try the same edit with a status from another issue type. The entire edit is rejected before the title or planner state changes. This pair teaches a useful review habit: state what should happen on success, then state what must remain unchanged on rejection.

Run the command in the verification chapter before attempting the exercises. Open [the store](../apps/api/src/data/store.ts), [the registered socket handlers](../apps/api/src/realtime/socket-server.ts), and [the boundary tests](../apps/api/tests/boundaries.test.ts) together. Chapter 03 contains a complete executed test; chapter 06 contains the full socket fixture and its assertions. The original store snapshot in `snapshots` lets you compare the missing guard with the repaired implementation.

Work through the course in three sessions: first membership and relations, then projections and mutation ordering, then asynchronous socket cleanup. Explain the reason for every guard before copying it into another project. A project ID, member ID, status ID, and socket ID all look like strings, but they establish different relationships. Treating them as interchangeable is the source of the defects this course repairs.
''',
'01-CODEBASE-MAP.md':'''## Follow the ownership of state

The web workspace calls the API; the API delegates to one module-level `store`. The new test factory creates an independent `MemoryStore` instead of changing that singleton. Supplying an explicit seed gives a test access to synthetic state for before/after assertions. This is dependency injection at a small scale: the production path keeps its existing construction, while tests control their own inputs.

`registerSocketHandlers` is now a callable registration function. The real `attachSocketServer` constructs Socket.IO, creates one `PresenceRegistry` for that server instance, and calls the function on connection. Tests pass a fake socket and fake room emitter to the same registration function. They therefore exercise the actual payload parsing, store lookups, identity derivation and disconnect callback rather than a copied algorithm.

`presence-types.ts` describes one entry. `presence-registry.ts` indexes entries by document and socket, and separately tracks which documents each socket owns. Removing a socket returns the changed document lists, including an empty list for the last departure. The transport broadcasts each returned list. Follow both indexes when debugging a leak: removing a value from the document map while retaining a stale socket key can make later cleanup inconsistent.
''',
'02-CONCEPTS.md':'''## Omission, rejection, and identity

Omission means a caller did not ask to change a field. It is different from sending an empty string or null. The current tracker update schema accepts optional strings; explicit null clearing is a future contract change, not a feature of this repair. A title-only request therefore preserves the status. A supplied status is checked against the issue's existing `issueTypeId`, not merely the workspace: two types in the same workspace can have different workflows.

Validation ordering provides a narrow atomicity property. A bad relation cannot cause this synchronous method to modify the title and then fail. It does not establish a database transaction, rollback after arbitrary failures, or durable writes. The planner helper runs after issue mutation, and the store retains mutable object references. A persistence implementation would need to define how both records commit together.

A socket identity and member identity also serve different purposes. The demo store supplies the member acting in the workspace; the transport supplies `socket.id`, which owns that connection's presence. Two tabs for the same member have different socket IDs. Disconnecting one must preserve the other tab's entry. A client-provided `memberId` is ignored because accepting it would let the client choose who appears in the room.
''',
'04-TESTING-AND-DEBUGGING.md':'''## What actually ran

The delivered suite contains seven Node tests across `security.test.ts` and `boundaries.test.ts`. Four cover settings denial, invalid create relations, recipient-scoped updates, and registry cleanup. Three further tests execute isolated-store positive CRUD and inbox filtering, rejected updates with unchanged records, and the real registered socket handlers with a fake transport. The suggestions above about Fastify `app.inject`, repeated client message IDs and additional planner assertions are extension exercises unless present in those files.

The fake transport implements only `on`, `join`, `emit`, a trigger helper, and a room emitter. A trigger awaits the registered callback, which matters after `workspace:join` was changed to await its room join. Sending null with a nonfunction acknowledgment argument must finish without a second exception in the catch branch. Sending malformed cursor coordinates must emit `doc:error` and leave the broadcast count unchanged.

When a negative assertion passes, inspect the positive fixture. The socket test first creates valid presence and asserts the actual derived member ID. It then sends invalid input and checks that no new broadcast appears. Finally it adds a second socket, removes the first, and verifies one entry remains before removing the second and expecting an empty list. These intermediate observations prevent a broken handler that never registers presence from passing a cleanup test.
''',
'05-PRACTICE.md':'''## Acceptance criteria before implementation

For exercises 1-5, capture independent snapshots with `structuredClone`. A variable that points to the same issue object is not a before snapshot because `Object.assign` mutates that object. Require at least one notification for another recipient before testing a forbidden update, and at least one current-recipient row before checking the allowed projection. State exactly which arrays should remain unchanged after each rejected operation.

For exercises 6-8, record emitted events and room names. A successful join should name `workspace:<workspaceId>`. A denied join must not add a room, even when the supplied acknowledgment is not a function. A presence event for a valid document should contain the store-derived member identity. A malformed cursor or unknown document must not add a broadcast. Keep one other socket active while disconnecting the first; only then disconnect the last and require an empty list.

Exercise 7's duplicate-message behavior is an exploration of the existing implementation, not a newly delivered guarantee. Inspect `createMessage` and define the required scope of a `clientMessageId` before testing it. Should uniqueness apply to a channel, member or entire workspace? Write that contract first. The current repair checks channel ownership but does not introduce durable idempotency or a database unique constraint.
''',
'07-TRACE-LAB.md':'''## Trace a rejection and a last disconnect

Use a concrete title edit: `PATCH /api/workspaces/<workspaceId>/tracker/issues/<issueId>` with `{"title":"Renamed"}`. Replace the placeholders with IDs from a local seed. The route validates the body, the store establishes membership, the issue lookup establishes workspace ownership, and the update applies only supplied fields. Add a status ID from another type to the same body. Validation must now reject before the title changes. The executed update test compares the issue and planner arrays with independent originals to establish that boundary.

For the socket trace, begin with two sockets in the same workspace. Both announce the same document. The registry stores two entries, one per socket. Disconnect socket A: `removeSocket` removes its entry, returns the remaining entry, and the handler broadcasts a one-element list. Disconnect B: the registry removes its final document map and returns an empty list; the handler still broadcasts that empty list. Omitting the final broadcast would leave clients showing a participant who has gone away.

Now consider a rejected asynchronous join. `socket.join` can return a promise when adapters perform asynchronous work. The handler awaits it inside the try block so a rejection can produce an acknowledgment failure instead of an unhandled promise. The finite fake join resolves; a rejecting adapter and a multi-process adapter remain integration exercises. The implementation improves error handling without claiming a distributed-delivery guarantee.
'''
}
for n,extra in extras.items():
 p=U/n;p.write_text(p.read_text(encoding='utf-8')+'\n'+extra,encoding='utf-8')
test=(P/'apps/api/tests/boundaries.test.ts').read_text(encoding='utf-8')
p=U/'03-WORKED-CHANGE.md';t=p.read_text(encoding='utf-8');case=test[test.index('test("issue update'):test.index('class FakeSocket')];t+='''
## Complete executed update regression

This case belongs in `apps/api/tests/boundaries.test.ts`. Keep that file's imports for `node:test` and `node:assert/strict`, plus its `fixture()` helper, which returns a fresh seed, store and workspace ID. The case is already included in the delivered suite; modify it in place rather than pasting a duplicate. Notice that it asserts both the issue and planner state. A guard that rejects only after changing the title will fail this test even when the number of issues remains unchanged.

```ts
'''+case+'```\n';p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8');t+='''
## Runnable fixtures and solutions for the store and socket boundaries

The following is the complete `apps/api/tests/boundaries.test.ts` file. Its imports and helpers are included so the fake transport has a clear contract. It supplies concrete solutions for exercises 1-3, 5, 6 and 8, plus the malformed-cursor case. The create-relation matrix for exercise 4 remains in `security.test.ts`. Exercise 7's duplicate-message extension and exercise 9's HTTP integration are not counted as executed coverage.

Read the final test in stages. The first valid join proves the handler can call the adapter. The spoofed presence request proves membership comes from the store. Two invalid requests then prove the failure path does not emit a valid presence update. The two disconnect assertions establish per-socket ownership and the empty final broadcast separately. These are deliberate observable assertions, not a claim that a fake transport reproduces packet ordering or reconnection behavior.

```ts
'''+test+'```\n';p.write_text(t,encoding='utf-8')
print(json.dumps({p.name:len(p.read_text(encoding='utf-8').split()) for p in U.glob('*.md')}))
