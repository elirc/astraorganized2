import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'newcodexjs-12-chat-polling'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# --- review #1 / P4: read receipt with a missing messageId must be 400, not 500
def patch_routes(t):
    old = """    if (req.path.endsWith("/read") && req.method === "POST") {
      const read = await db("messages")
        .where({ id: req.body.messageId, conversation_id: conversationId })
        .first();"""
    new = """    if (req.path.endsWith("/read") && req.method === "POST") {
      // The guard runs before validateBody(readSchema); reject a missing or
      // malformed id here so the lookup below never sees undefined (500).
      const messageId = Number(req.body?.messageId);
      if (!Number.isSafeInteger(messageId) || messageId < 1)
        throw new ValidationError("messageId must be a positive whole number");
      const read = await db("messages")
        .where({ id: messageId, conversation_id: conversationId })
        .first();"""
    assert old in t
    return t.replace(old, new, 1)
assert fe.rw('server/src/routes/chatRoutes.ts', patch_routes)
def patch_test(t):
    add = '''
test("a read receipt without a message id is a 400, not a crash", async () => {
  for (const body of [{}, { messageId: "abc" }, { messageId: 0 }, { messageId: 1.5 }]) {
    const r = await api(`/conversations/${room}/read`, "POST", body, 2);
    assert.equal(r.status, 400, JSON.stringify(body));
  }
  assert.equal((await api(`/conversations/${room}/read`, "POST", { messageId: message }, 2)).status, 200);
  assert.equal(
    (await h.db("conversation_members").where({ conversation_id: room, user_id: 2 }).first()).last_read_message_id,
    message,
  );
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('test/membership.test.ts', patch_test)
done.append('review#1 / P4: the membership guard now validates messageId before the lookup; POST /conversations/:id/read with {} is 400 (test added)')

# --- review #3: path-regex dispatch paragraph
fe.append_section(S, '02', '## One guard for every route: what the path regex buys and costs', """`chatRouter.use` at the top of `server/src/routes/chatRoutes.ts` runs before every handler. It reads the demo user, matches `/^\\/(conversations|messages)\\/(\\d+)(?:\\/|$)/` against the path, resolves the conversation (directly, or through the message's `conversation_id`), and refuses non-members with a 404 that does not reveal whether the conversation exists. Two extra rules ride on the same match: group management (`PUT /conversations/:id` and anything containing `/members`) needs `role = 'admin'`, and a read receipt must reference a message from this conversation.

What that buys: a new route under `/conversations/:id/...` is protected the moment it is added; nobody can forget the membership check. What it costs: dispatch by string matching. `req.path.includes("/members")` would also match a future `/conversations/7/membership-history`, silently demanding admin; and the guard cannot express per-route differences (a read receipt needs a member, a rename needs an admin, a message edit needs the author) except by more string tests. The read-receipt branch is a good example of the trade-off: it runs before `validateBody(readSchema)`, so it had to grow its own `messageId` check.

The per-route alternative looks like this:

```typescript
const requireMember = (idFrom: (req: Request) => number) => wrap(async (req, _res, next) => { /* membership lookup */ next(); });
const requireAdmin = (idFrom: (req: Request) => number) => wrap(async (req, _res, next) => { /* membership + role */ next(); });
chatRouter.put("/conversations/:id", requireAdmin(paramId), validateBody(groupUpdateSchema), wrap(controller.updateGroup));
chatRouter.post("/conversations/:id/read", requireMember(paramId), validateBody(readSchema), wrap(controller.markRead));
```

Predict before reading exercise 7: which of the two designs makes it easier to forget a check, and which makes it easier to over-match?""")
done.append('review#3 02-CONCEPTS explains path-regex dispatch vs per-route middleware')

B = [
("the chat screen decides what to send",
 "`client/src/App.tsx`: the conversation list is a `useQuery` with `refetchInterval: 5000` (line 10); the open room loads history with `chatApi.getMessages` (line 73) and polls `newMessages` for rows after the last known id (line 75). Sending a message, reacting, typing and marking read are `useMutation`s that call `client/src/services/api.ts`. The demo identity is a header the client chooses; nothing on the client can prove membership."),
("the request leaves the browser",
 "`client/src/services/api.ts`: every call goes through one axios instance that adds `x-demo-user-id`; `markRead(conversationId, messageId)` (line 38) posts `{ messageId }` to `/conversations/:id/read`, `getMessages` reads `/conversations/:id/messages`, polling reads `?after=<id>`. The envelope is unwrapped by `unwrap()`; a 404 from the guard becomes `Error(\"Conversation not found\")` in the UI."),
("the guard decides who may touch which conversation",
 "`server/src/routes/chatRoutes.ts` `chatRouter.use` (line 18): parses the demo user, matches the path, resolves the conversation (via `messages.conversation_id` for `/messages/:id` paths), checks `conversation_members`, demands `role = 'admin'` for group management, and for `POST .../read` validates `messageId` and checks the message belongs to this conversation. All of it before `validateBody` and before any controller; outsiders get 404, non-admins 400, malformed receipts 400."),
("the service and model apply the change",
 "`controllers/chatController.ts` `markRead` (line 178) calls `model.markRead(conversationId, userId, messageId)` (`models/chatModel.ts:224`), a single `UPDATE conversation_members SET last_read_message_id = ?` scoped by conversation and user. Message CRUD is scoped the same way: `updateMessage(id, userId, content)` and `deleteMessage(id, userId)` carry the author in the `WHERE`, so a member cannot edit another member's message even though the guard let them into the room."),
("PostgreSQL commits the row",
 "Each of these operations is one statement; there is no explicit transaction, so the row is either updated or not. Polling relies on `messages.id` being monotonic: `listMessagesAfter` (`chatModel.ts:117`) is `WHERE id > ? ORDER BY id ASC LIMIT 100`, and unread counts are `count(*) WHERE id > last_read_message_id`. That is why the read receipt stores an id, not a timestamp."),
("the envelope tells the client what happened",
 "`utils/http.ts` `sendSuccess` returns `{ success: true, data }`; `middleware/errors.ts` maps `ValidationError` to 400, `NotFoundError` to 404, everything else to 500. After `markRead` succeeds the client invalidates the `conversations` query so the unread badge is recomputed from the server, not decremented locally."),
]
fe.set_boundaries(S, B); done.append('review#2 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the feedback must be driven by the server: when the polling query or `getMessages` returns the guard's 404, the room must switch to a \"you no longer have access\" state and stop polling (`enabled: false` or `refetchInterval` off); a client test should mock the 404 and assert the state and that no further poll request is issued.",
"the badge must come from the `role` in the membership rows the server returns, never from local assumptions; when an admin demotes a member the badge must change on the next poll; assert with a server test that `listMembers` exposes `role` and a client test that the badge re-renders after the query refetches.",
"insert user 2's membership, open a poll cursor, remove the membership via the admin route, then poll again: the response must be 404 and the unread count for user 2 must not change; explain that the guard re-checks membership on every request, which is exactly why polling (not a long-lived socket) makes removal take effect within one interval.",
"the design must replace `x-demo-user-id` with a server-issued session (cookie or bearer), keep the guard's membership lookup unchanged (only `user` comes from the session now), and state what happens to the `DEMO_USER_ID` fallback (delete it: a missing session must be 401, not a silent default user).",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')

routes = open('server/src/routes/chatRoutes.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
j = next(j for j, l in enumerate(routes) if 'chatRouter.use(async' in l)
k = next(k for k, l in enumerate(routes) if l.startswith('chatRouter.get("/conversations"'))
excerpt = '\n'.join(routes[j:k - 1])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/63/server/src/routes/chatRoutes.ts` with `diff --strip-trailing-cr -w`): the router-level membership guard that resolves the conversation from either path shape, hides non-membership behind 404, restricts group management to admins and validates read receipts. The `messageId` check inside the read-receipt branch was added in this course's fix pass. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows the changed guard')

fe.set_variations(S, """**Normal variation — a member reads, an outsider cannot.** As user 2, `GET /api/conversations/<room>/messages`: predict 200 with the seeded message. As user 3 (not a member): predict 404 `Conversation not found`, and explain why the guard chose 404 over 403 (it does not confirm that the room exists).

**Invalid variation — a receipt for the wrong room.** As user 2, `POST /api/conversations/<room>/read` with the id of the `Other` room's message. Predict 400 `Read receipt must reference this conversation` and `last_read_message_id` unchanged. Then send `{}`: predict 400 `messageId must be a positive whole number` (before the fix pass this was a 500).

**Boundary variation — polling after removal.** As admin user 1, remove user 2 with the members route, then as user 2 poll `?after=0`. Predict 404 within the same second, because the guard re-reads `conversation_members` on every request. Then read exercise 7 to see the one window where that is not true."""); done.append('2.4 three concrete variations')

fe.add_exercise(S, 'make the TOCTOU window visible',
"""The guard checks membership, then the handler runs. Between those two moments the membership row can disappear. The course states this; make it observable.

1. Add a test-only hook in `server/src/routes/chatRoutes.ts`: `export const hooks: { afterGuard?: () => Promise<void> } = {};` and `await hooks.afterGuard?.();` as the last line of the guard before `next()`. It is a no-op in production.
2. In a new test, set `hooks.afterGuard` to a function that deletes user 2's membership row, then as user 2 request `GET /conversations/<room>/messages`. Predict the status before running it.
3. Observe: 200 with the history, even though user 2 is no longer a member when the handler runs.
4. Close the window for the read path only: make the controller's history query join `conversation_members` (`WHERE conversation_id = ? AND EXISTS (SELECT 1 FROM conversation_members WHERE ... user_id = ?)`), and show the same test now returns an empty list or 404. Discuss why the polling design makes the remaining window (one request) acceptable.""",
"""Reference hook and test:

```typescript
// chatRoutes.ts (top level)
export const hooks: { afterGuard?: () => Promise<void> } = {};
// last lines of the guard, before next():
await hooks.afterGuard?.();
next();
```

```typescript
test("membership removed between guard and handler", async () => {
  const { hooks } = await import("../server/src/routes/chatRoutes.js");
  hooks.afterGuard = async () => {
    await h.db("conversation_members").where({ conversation_id: room, user_id: 2 }).delete();
  };
  try {
    const r = await api(`/conversations/${room}/messages`, "GET", undefined, 2);
    console.log("status after removal inside the window:", r.status); // 200 before the fix in step 4
  } finally {
    hooks.afterGuard = undefined;
    await h.db("conversation_members").insert({ conversation_id: room, user_id: 2, role: "member" });
  }
});
```

Review: the point is not to eliminate every window (a read that started while you were a member is arguably fine) but to know where the check happens relative to the read, and to move the check into the query for writes that must not succeed for a non-member (sending a message, reacting). Explain which routes you would harden and why."""); done.append('review#4 exercise 7: TOCTOU window made observable with a test hook (05, 06)')

fe.add_exercise(S, 'unread counts and cursors, by the numbers',
"""Polling and unread badges are pure arithmetic on `messages.id`. Prove you can do it by hand.

1. In the room, insert messages with ids 10, 11, 12 (or read the real ids). Set user 2's `last_read_message_id` to 10 by calling the read route with 10.
2. Predict the unread count the conversation list returns for user 2 (2), what `GET ...?after=10` returns (ids 11 and 12, ascending), and what `getMessages` with `before=12` returns (ids up to 11, newest last).
3. Mark 12 as read and predict both again (0; empty).
4. Now delete message 11 (soft delete). Predict whether the unread count changes and whether `?after=10` still returns it; then read `listMessagesAfter` and `is_deleted` handling to check.

Write your predictions as a small table before running anything.""",
"""Answers: unread is `count(*) WHERE conversation_id = ? AND id > last_read_message_id AND NOT is_deleted` (check the model for the exact predicate; if `is_deleted` is not in it, that is a finding to fix and test). `listMessagesAfter(room, 10)` is `WHERE id > 10 ORDER BY id ASC LIMIT 100`, so 11 and 12. `listMessages(room, 12)` is `WHERE id < 12 ORDER BY id DESC LIMIT 30`, then reversed, so ... 10, 11 oldest-first. After reading 12, unread is 0 and `?after=12` is empty. The cursor is an id, not a timestamp, because ids are assigned once and never collide, while two messages can share a `created_at`.

Review: show the table with predictions and observations side by side; any mismatch must be explained by pointing at the SQL that produced it."""
, number=8); done.append('review#5 exercise 8: cursor and unread-count arithmetic (05, 06)')

fe.append_section(S, '04', "## Chat-specific debugging: cursors, receipts and the guard", """Three things go wrong in this project and none of them look like a crash. **A message never appears for a poller**: check that the poll uses the highest id it has seen (`?after=<id>`), not a timestamp, and that the server's `listMessagesAfter` orders ascending; a client that keeps the first page's cursor will poll from the wrong place. **An unread badge is wrong**: read `last_read_message_id` for that member in `psql` and compute `count(*) WHERE id > that` yourself; the badge is a projection of that one column. **A request is 404 that you expected to work**: the guard hides three different causes behind one status (no such conversation, not a member, message from another conversation); reproduce with `h.db` in a test and assert on the membership row, not on the message text.

`test/database.ts` creates a private schema, migrates it, imports the app and returns `h.db` (the same Knex instance) and `request(origin, path, method, body, headers)`; the `api()` helper in `test/membership.test.ts` adds `x-demo-user-id` so one test can act as three users. Run with `$env:ASTRA_TEST_DATABASE_URL = "postgres://user@127.0.0.1:5432/astra_test_yourname"` then `npm test`.""", before='## '); done.append('review#5 chat-specific debugging section (04)')

rp = json.load(open('package.json', encoding='utf-8'))
rp['name'] = 'chat-polling-workspace'
rp.setdefault('devDependencies', {}).update({"pg": "^8.23.0", "tsx": "^4.23.13"})
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(rp, indent=2) + '\n')
done.append('root package renamed from astra-crud-workspace-63; pg and tsx declared at the root')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **3**.", "Automated test cases: **3** delivered by Astra, plus **1** added in the fix pass (read receipt without a message id is 400), for 4 in `test/membership.test.ts`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
