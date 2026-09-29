import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'js1-live-chat'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# --- tests: decouple (review #1) and add the two bound tests (review #3)
def patch_test(t):
    old_before = """before(async () => {
  h = await database();
});"""
    new_before = """before(async () => {
  h = await database();
  // Each test must be runnable on its own: the study room is fixture, not a side effect of test 1.
  await h.admin.query(
    "INSERT INTO rooms (slug, name) VALUES ('study', 'Study') ON CONFLICT (slug) DO NOTHING",
  );
});"""
    assert old_before in t
    t = t.replace(old_before, new_before, 1)
    old_create = """  assert.equal(
    (
      await request(h.origin, "/api/rooms", "POST", {
        slug: "study",
        name: "Study",
      })
    ).status,
    201,
  );"""
    new_create = """  assert.equal(
    (
      await request(h.origin, "/api/rooms", "POST", {
        slug: "seminar",
        name: "Seminar",
      })
    ).status,
    201,
  );"""
    assert old_create in t
    t = t.replace(old_create, new_create, 1)
    add = '''
async function openSocket(slug: string) {
  const socket = new WebSocket(h.origin.replace("http", "ws") + "/?room=" + slug);
  await new Promise<void>((resolve, reject) => {
    socket.on("message", (raw) => {
      if (JSON.parse(String(raw)).type === "presence") resolve();
    });
    socket.on("error", reject);
  });
  return socket;
}
function nextMessage(socket: WebSocket, timeoutMs = 5000) {
  return new Promise<any>((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("Missing broadcast")), timeoutMs);
    socket.on("message", (raw) => {
      const event = JSON.parse(String(raw));
      if (event.type === "message") {
        clearTimeout(timer);
        resolve(event.message);
      }
    });
  });
}
test("an oversize frame closes only that socket; the server keeps serving", async () => {
  const socket = await openSocket("study");
  const closed = new Promise<number>((resolve) => socket.on("close", (code) => resolve(code)));
  socket.send("x".repeat(17 * 1024));
  assert.equal(await closed, 1009); // ws maxPayload: 16384 -> "message too big"
  assert.equal((await request(h.origin, "/api/rooms")).status, 200);
  const again = await openSocket("study");
  again.terminate();
});
test("a body over 2000 characters is dropped and never persisted", async () => {
  const socket = await openSocket("study");
  try {
    const before = (await request(h.origin, "/api/rooms/study/messages")).data.length;
    socket.send(JSON.stringify({ type: "message", author: "Learner", body: "y".repeat(2001) }));
    const received = nextMessage(socket);
    socket.send(JSON.stringify({ type: "message", author: "Learner", body: "after the oversize body" }));
    const message = await received;
    assert.equal(message.body, "after the oversize body");
    const history = (await request(h.origin, "/api/rooms/study/messages")).data;
    assert.equal(history.length, before + 1);
    assert.ok(history.every((m: { body: string }) => m.body.length <= 2000));
  } finally {
    socket.terminate();
  }
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('test/chat.test.ts', patch_test)
done.append('review#1 tests decoupled: the study room is created in before(); test 1 creates "seminar" for its 201 and keeps the duplicate-slug 409')
done.append('review#3 two new tests: >16KB frame closes that socket with 1009 while HTTP keeps serving; a 2001-character body is dropped and never persisted')

# --- 02: LISTEN/NOTIFY section (review #2)
schema = open('server/db/schema.sql', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
i = next(i for i, l in enumerate(schema) if 'CREATE OR REPLACE FUNCTION notify_new_message' in l)
j = next(j for j, l in enumerate(schema) if 'EXECUTE FUNCTION notify_new_message' in l)
trig = '\n'.join(schema[i:j + 1])
fe.append_section(S, '02', '## LISTEN/NOTIFY: how a row insert becomes a broadcast', """The server never pushes a chat message to sockets directly. It inserts a row, and PostgreSQL tells it, and every other server instance, that the row exists. The mechanism is a trigger in `server/db/schema.sql`:

```sql
""" + trig + """
```

Three facts to hold onto before you read `startListener` in `server/src/index.ts`:

1. **`pg_notify` fires on commit, not on execution.** If the transaction that inserted the message rolled back, no notification is sent. That is why the broadcast is a reliable signal that the row is durable.
2. **The listener needs its own, non-pooled client.** `createListenerClient()` opens a dedicated `pg.Client` and runs `LISTEN chat`. A pooled connection would be returned to the pool and the `LISTEN` would silently stop applying. The `error` handler ends the client and schedules `startListener()` again after 1 s.
3. **A disconnected listener loses notifications, not rows.** Notifications are not queued for a client that is not connected. That is the whole reason the browser re-reads history over HTTP (`GET /api/rooms/:slug/messages`) when it reconnects, and why exercise 4 (acknowledged delivery and replay) is a design problem rather than a bug fix.

Predict, then check with `psql` on your dev database: run `INSERT INTO messages (room_id, author, body) SELECT id, 'psql', 'hello from sql' FROM rooms WHERE slug = 'general'` while the app is open on the General room. The message appears in the browser without the Node server having received any WebSocket frame.""")
done.append('review#2 02-CONCEPTS teaches LISTEN/NOTIFY with the real trigger before it is used')

B = [
("the composer decides what to send",
 "`client/src/App.tsx`: `send` (line 72) trims `draft`, refuses to send if the socket is not `OPEN`, and calls `socket.send(JSON.stringify({ type: \"message\", author, body }))`. Room creation goes through `handleCreateRoom` (line 80) and plain HTTP. Notice what the client does not do: it does not add the message to `messages` itself. It waits for the broadcast, so the sender sees exactly what the database accepted."),
("the frame leaves the browser",
 "The effect at line 30 opens `new WebSocket(WS_URL + \"/?room=\" + slug)` (`client/src/api.ts` exports `WS_URL`), re-fetches history with `listMessages(slug)`, and reconnects after 1 s on `onclose` unless the effect was torn down. `onmessage` appends `type: \"message\"` events and updates presence counts. A frame is just text: nothing in the browser proves it is a valid event."),
("the server guards the event shape",
 "`connectSocket` (`server/src/index.ts:108`) first resolves the room from the query string and closes with `4404` for an unknown slug. On every frame it `JSON.parse`s and returns silently on failure, checks `type === \"message\"` and that `author` and `body` are strings, then enforces `author.length <= 40` and `body.length <= 2000` (line 140) before trimming. The `WebSocketServer` itself has `maxPayload: 16384` (line 95): a bigger frame closes that socket with 1009 before any handler runs. Malformed input is dropped, never answered, which is why the tests assert on what happens *after* the bad frames."),
("the handler writes the row and nothing else",
 "The only side effect of a valid frame is `INSERT INTO messages (room_id, author, body)` through `query` (line 150). The comment there is the lesson: the handler does not broadcast. If the insert throws, the socket is closed with 1011 `Message could not be saved` and nothing was delivered, so a client can retry from a known state."),
("the database commits and notifies",
 "`messages_notify` (`server/db/schema.sql`) runs `AFTER INSERT` and calls `pg_notify('chat', json_build_object(...))`. The notification is delivered on commit to every connection that ran `LISTEN chat`, including a second server instance or a `psql` session. The dedicated listener client in `startListener` (line 204) receives it on the `notification` event; a pooled client would not."),
("the broadcast is the response",
 "`broadcast(roomId, event)` (line 183) serializes once and sends to every open socket in `roomClients.get(roomId)`. That includes the sender, which is how the composer learns its message was stored. The second test waits for that broadcast (a real event, not a `setTimeout`), then re-reads `/api/rooms/study/messages` over HTTP and asserts the ids match: the socket event and the row are the same fact seen two ways."),
]
fe.set_boundaries(S, B); done.append('review#4 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the draft must be marked sending when `socket.send` is called and cleared only when the broadcast with the same body arrives; a socket that is not `OPEN` must show an error state instead of silently dropping the draft (`send` currently returns early); your test must simulate a closed socket and assert the draft is still there.",
"the endpoint must be `PATCH /api/rooms/:slug` changing only `name`, validated like `createRoom`; the `id` and `slug` must be provably unchanged (compare the row before and after), open sockets must keep working because `roomClients` is keyed by `id`, and a rename to the same name should be a no-op that still returns 200.",
"open two sockets on two rooms, send in one, and assert the other receives nothing within a bounded wait (use a `setTimeout` race that resolves to `\"no message\"`), then assert the first did receive it; explain why the guarantee comes from `roomClients` being keyed by the room id in the notification payload, not from the socket that sent the frame.",
"your design must state what the server stores per client (last acknowledged message id), how reconnect asks for `?after=<id>`, why replay reads rows over HTTP or SQL rather than replaying notifications (they are not queued), and what happens to a message whose insert committed but whose broadcast was lost while the listener was reconnecting.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')

code = open('server/src/index.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
excerpt = '\n'.join(code[125:157]) + '\n\n// server/src/index.ts:204\n' + '\n'.join(code[203:216])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/57/server/src/index.ts` with `diff --strip-trailing-cr -w`): the event-shape guard in `connectSocket` that drops malformed or oversize events instead of crashing, the insert-only handler with a 1011 close on failure, and the listener's reconnect loop. `maxPayload: 16384` on the `WebSocketServer` is the other bound. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows the changed connectSocket guard and listener')

fe.set_variations(S, """**Normal variation — a message from SQL.** With the app open on General, run `INSERT INTO messages (room_id, author, body) SELECT id, 'psql', 'from sql' FROM rooms WHERE slug='general'` in `psql`. Predict: the browser shows it within a second with no WebSocket frame sent by any browser. Explain which line delivered it (the trigger, then `startListener`'s `notification` handler, then `broadcast`).

**Invalid variation — a frame the guard drops.** From the browser console, `socketRef`-style access is awkward, so use the test harness: send `{"type":"message","author":3,"body":{}}` then a valid message. Predict: no broadcast for the first, one for the second, and history length +1. Then send `{"type":"message","author":"Learner","body":"   "}`: predict what `body.trim()` does and whether a row is written.

**Boundary variation — the listener dies.** Stop the listener connection from `psql` with `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE query = 'LISTEN chat'`. Predict: the server logs `Listener error`, reconnects after 1 s, and any message inserted during that second is stored but never broadcast. Send one in that window, then reload the browser: the history request shows it. That is the gap exercise 4 is about."""); done.append('2.4 three concrete variations')

fe.add_exercise(S, 'ownership and authorization',
"""Any socket can post under any `author`, and any HTTP client can create rooms. Bind identity to the connection instead of trusting the frame.

1. Add a `POST /api/sessions` route that takes `{ name }` (2-40 characters) and returns an opaque token; keep sessions in a `Map` for now.
2. Require `?token=` on the WebSocket URL: in `connectSocket`, resolve the session before joining and close with `4401` when it is missing or unknown. Take `author` from the session, and ignore `event.author` entirely.
3. Add `created_by` to `rooms` (`server/db/schema.sql`) and set it from the session on `POST /api/rooms` (which must now require `Authorization: Bearer <token>` and answer 401 otherwise). Only the creator may rename a room in exercise 2.

Acceptance, written first: a frame with a spoofed `author` is stored under the session's name; a socket without a token is closed with 4401 and nothing is stored; room creation without a token is 401; a rename by a non-creator is 403 and the row is unchanged.""",
"""Reference (the identity comes from the connection, so the frame cannot lie):

```typescript
const sessions = new Map<string, { name: string }>();
app.post("/api/sessions", (req, res) => {
  const name = typeof req.body?.name === "string" ? req.body.name.trim() : "";
  if (name.length < 2 || name.length > 40) return res.status(400).json({ error: "Name must be 2-40 characters." });
  const token = crypto.randomUUID();
  sessions.set(token, { name });
  res.status(201).json({ token, name });
});
// connectSocket, before join():
const session = sessions.get(url.searchParams.get("token") ?? "");
if (!session) { socket.close(4401, "Sign in first"); return; }
// message handler: const author = session.name; (event.author is ignored)
```

Reference test skeleton: open a socket with a valid token, send `{ type: "message", author: "Impostor", body: "hi" }`, await the broadcast and assert `message.author` equals the session name; open a socket without a token and assert the close code is 4401 and `count(*)` on `messages` is unchanged.

Review: explain why moving `author` from the payload to the connection is authorization and not validation, why the close code is 4401 (application range) rather than 1008, and what a real app would replace the in-memory `sessions` map with."""); done.append('2.5 ownership/authz exercise 7 (05, 06)')

fe.append_section(S, '04', "## This project's test harness: `test/database.ts` and waiting for a real broadcast", """`database()` refuses any `ASTRA_TEST_DATABASE_URL` whose database name does not start with `astra_test_`, creates a private schema, loads `server/db/schema.sql` into it (stripping `DROP` and `CREATE EXTENSION`, so `pgcrypto` must already exist), sets `process.env.DATABASE_URL`, and only then imports the server and calls `startRuntime(0)`. The import order matters because `server/src/db.ts` builds its pool from `DATABASE_URL` at load time, and `startRuntime` is what opens the dedicated `LISTEN` client, so a test that imported the app first would listen on the wrong database. `close()` calls `stopRuntime()` (terminates sockets, ends the listener) and drops the schema.

The socket tests never `sleep`. They first wait for the `presence` event that proves the server has joined the socket to the room, then register a promise for the next `type: "message"` event with a 5 s timeout, send the frames, and await that promise. Asserting after a real event, not after a delay, is what makes the suite fast on a good day and honest on a bad one. Run with `$env:ASTRA_TEST_DATABASE_URL = "postgres://user@127.0.0.1:5432/astra_test_yourname"` then `npm test`.""", before='## '); done.append('review#5 harness walkthrough (04)')

pj = json.load(open('package.json', encoding='utf-8'))
pins = {"cors": "^2.8.6", "dotenv": "^16.6.1", "express": "^4.22.2", "pg": "^8.23.0", "react": "^18.3.1", "react-dom": "^18.3.1", "ws": "^8.21.3",
        "@types/cors": "^2.8.19", "@types/express": "^4.17.23", "@types/node": "^22.19.0", "@types/pg": "^8.15.5", "@types/react": "^18.3.27", "@types/react-dom": "^18.3.7", "@types/ws": "^8.18.1",
        "@vitejs/plugin-react": "^6.1.1", "concurrently": "^9.2.1", "tsx": "^4.23.13", "typescript": "^5.9.3", "vite": "^8.2.2"}
for sec in ('dependencies', 'devDependencies'):
    for k in pj.get(sec, {}):
        pj[sec][k] = pins.get(k, pj[sec][k])
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(pj, indent=2) + '\n')
done.append('review#6 / 2.7 dependencies pinned to the versions Astra verified with (ws 8.21.3)')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **2**.", "Automated test cases: **2** delivered by Astra, plus **2** added in the fix pass (oversize frame, oversize body), for 4 in `test/chat.test.ts`; the study room is now created in `before()` so each test runs alone.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
