import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'js1-secure-notes'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# --- code: session expiry (review #1)
def patch_server(t):
    old_store = "const tokens = new Map(); // token -> userId"
    new_store = "const tokens = new Map(); // token -> { userId, expiresAt }\nconst DEFAULT_SESSION_TTL_MS = 8 * 60 * 60 * 1000;\nfunction sessionTtlMs() {\n  const configured = Number(process.env.SESSION_TTL_MS);\n  return Number.isFinite(configured) && configured > 0\n    ? configured\n    : DEFAULT_SESSION_TTL_MS;\n}"
    assert old_store in t
    t = t.replace(old_store, new_store, 1)
    old_auth = """  const token = header.startsWith("Bearer ") ? header.slice(7) : null;
  const userId = token && tokens.get(token);
  if (!userId) {
    return res.status(401).json({ error: "Sign in to continue." });
  }"""
    new_auth = """  const token = header.startsWith("Bearer ") ? header.slice(7) : null;
  const session = token ? tokens.get(token) : undefined;
  if (!session) {
    return res.status(401).json({ error: "Sign in to continue." });
  }
  if (session.expiresAt <= Date.now()) {
    // Expiry belongs to the session store: the note routes never see an expired caller.
    tokens.delete(token);
    return res.status(401).json({ error: "Session expired. Sign in again." });
  }
  const userId = session.userId;"""
    assert old_auth in t
    t = t.replace(old_auth, new_auth, 1)
    old_issue = """  const token = randomUUID();
  tokens.set(token, user.id);
  return { token, user: { id: user.id, email: user.email } };"""
    new_issue = """  const token = randomUUID();
  const expiresAt = Date.now() + sessionTtlMs();
  tokens.set(token, { userId: user.id, expiresAt });
  return {
    token,
    expiresAt: new Date(expiresAt).toISOString(),
    user: { id: user.id, email: user.email },
  };"""
    assert old_issue in t
    return t.replace(old_issue, new_issue, 1)
assert fe.rw('server/server.js', patch_server)
done.append('review#1: session expiry implemented in server/server.js (tokens store {userId, expiresAt}; requireAuth deletes an expired token and answers 401; SESSION_TTL_MS env for tests, default 8h)')

def patch_test(t):
    add = '''
test("an expired session is rejected and removed; logging in again works", async () => {
  process.env.SESSION_TTL_MS = "40";
  const short = (
    await api("/auth/login", "POST", { email: "b@example.com", password: "learn123" })
  ).data;
  delete process.env.SESSION_TTL_MS;
  assert.ok(short.expiresAt);
  assert.equal((await api("/auth/me", "GET", undefined, short.token)).status, 200);
  await new Promise((resolve) => setTimeout(resolve, 60));
  const expired = await api("/auth/me", "GET", undefined, short.token);
  assert.equal(expired.status, 401);
  assert.equal(expired.data.error, "Session expired. Sign in again.");
  assert.equal((await api("/auth/logout", "POST", {}, short.token)).status, 401);
  const fresh = (
    await api("/auth/login", "POST", { email: "b@example.com", password: "learn123" })
  ).data;
  assert.equal((await api("/auth/me", "GET", undefined, fresh.token)).status, 200);
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('test/notes.test.js', patch_test)
done.append('review#1: regression test for expiry (test/notes.test.js, 4th test)')

# --- README scope (review #2)
fe.rw(fe.chapter(S, 'README'), lambda t: t.replace(
    "Credentials and note text are typed and bounded, email normalization is consistent, and an owned note detail endpoint completes the read path. Owner checks protect read, update and delete; logout revokes its token.",
    "What Astra changed: a JSON-object guard for every write, typed and bounded credentials and note fields (password 6-128, title 2-200, body up to 20,000), email normalization applied identically on register and login, and a new owner-scoped `GET /api/notes/:id`. What already existed before the change and is used as the worked example: `requireAuth`, `findOwnedNote` owner checks on read, update and delete, and logout revoking its token. Added in this course's fix pass: sessions now expire (`expiresAt` returned on login, 401 `Session expired.` afterwards)."))
done.append('review#2 README scope separates pre-existing behavior from the delivered change')

# --- 02 concepts paragraph on expiry
fe.append_section(S, '02', '## Where session expiry belongs', """A note handler asks one question: does this note belong to `req.user`? It should never have to ask whether the caller's session is still fresh. That is why expiry lives in `requireAuth` and the `tokens` store (`server/server.js`): the store records `expiresAt` when `issueSession` runs, and `requireAuth` deletes a stale token and answers 401 before any note code executes. Two consequences to predict before you read the new test: logout on an expired token is also 401 (there is nothing left to revoke), and a fresh login after expiry works because `users` and `notes` were never touched. If expiry were checked inside `findOwnedNote`, every route would need the check and a future route could forget it.""")
done.append('review#1 02-CONCEPTS explains why expiry belongs to the session store')

B = [
("the React form decides what to send",
 "`client/src/App.jsx`: the auth card's `handleSubmit` (line 53) posts `{ email, password }` to `register` or `login`; the notes panel's `handleSubmit` (line 134) sends `form` (`title`, `body`) to `createNote` or `updateNote` depending on `editingId`, then `reset()` and `refresh()`. `remove(id)` (line 161) calls `deleteNote`. No note or credential is validated in the browser; every rejection arrives as `error.message` from the server."),
("the client serializes the request and attaches the session",
 "`client/src/api.js`: `login`/`register` store the returned `token` in `localStorage` under `js1-secure-notes-token` via `setToken`; every later call goes through `request()`, which adds `Authorization: Bearer <token>` when a token exists, sets the JSON header, and throws `Error(data.error)` on non-2xx. A 401 anywhere is turned into a sign-out on the client. Nothing else identifies the user: the token is the whole identity."),
("the middleware chain validates the caller and the input",
 "`server/server.js:16` rejects any write whose body is not a JSON object. `requireAuth` (line 141) reads the bearer token, looks it up in `tokens`, rejects a missing or expired session with 401, and attaches `req.user`. `validateNote` (line 157) then bounds `body` (string, at most 20,000) and `title` (2-200 characters). Register and login normalize the email (`trim().toLowerCase()`, lines 32 and 66) so `\" A@example.com \"` and `a@example.com` are the same account. All of this happens before any note is touched."),
("the handler applies the owner-scoped change",
 "`findOwnedNote(id, userId)` (line 187) is the whole authorization model: `notes.find(n => n.id === id && n.userId === userId)`. `GET /api/notes/:id` (line 94, the new endpoint), `PUT` (line 112) and `DELETE` (line 122) all call it and answer 404 `Note not found.` when it returns nothing, deliberately the same answer for a missing note and for someone else's note. `POST` (line 100) stamps `userId: req.user.id` from the session, ignoring anything the body says."),
("the storage boundary commits or rejects",
 "State is three in-memory structures: `users` (Map by email), `tokens` (Map by token) and the `notes` array. `PUT` mutates the found note object in place; `DELETE` splices it out; `POST` unshifts. Each handler runs synchronously to completion, so no other request can observe a half-applied change within one process. Restarting the server forgets every user, token and note; the trade-offs of moving this to a database are exercise 4."),
("the response tells the client what actually happened",
 "`POST` answers 201 with the note; `PUT` 200 with the mutated note; `DELETE` 204 with no body (`api.js` returns `null` for 204); `login` and `register` answer with `{ token, expiresAt, user }`. The client then calls `refresh()` and re-reads `/api/notes`, which is filtered by `notesFor(req.user.id)`, so the list you see is always the server's owner-scoped view, never the client's guess."),
]
fe.set_boundaries(S, B); done.append('review#3 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the empty state must be distinguishable from a failed request and from a not-yet-loaded list: show the three UI states in your test or screenshot, and prove that a 401 during the initial `refresh()` signs the user out instead of rendering an empty list.",
"`updatedAt` must change only on a successful `PUT` (set it right where the note is mutated in `server/server.js`); a rejected edit (title too short) must leave both `updatedAt` and the fields unchanged, and `createdAt` must never change; your test should compare the whole note object before and after the rejected edit.",
"the failed login must return the generic `Invalid email or password.` for a wrong password and for an unknown email alike, must not issue a token, and must not lock or alter the account; the following successful login must produce a token that works on `/api/auth/me`; add the malformed-body case (`{ email: 5 }`) and assert the process is still serving afterwards.",
"your design must name the owner foreign key on `notes`, show every note query carrying `WHERE user_id = $1`, store sessions with `expires_at` and delete expired rows, and keep password hashing (`scrypt` with a per-user salt) exactly as it is now; explain what `findOwnedNote` becomes in SQL and why a 404 is still the right answer for a foreign note.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')

code = open('server/server.js', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
def grab(start_marker, n):
    i = next(i for i, l in enumerate(code) if start_marker in l)
    return '\n'.join(code[i:i + n])
excerpt = grab('app.use((req, res, next) => {', 8) + '\n\n' + grab('app.post("/api/auth/register"', 17) + '\n\n' + grab('app.get("/api/notes/:id"', 5) + '\n\n' + grab('function validateNote', 18)
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/56/server/server.js` with `diff --strip-trailing-cr -w`): the JSON-object guard, the normalized email and bounded password in `register` (and the same normalization in `login`), the new owner-scoped `GET /api/notes/:id`, and the bounded `validateNote`. `requireAuth` and `findOwnedNote` were already there; session expiry was added in this course's fix pass (see chapter 2). The linked source is authoritative if you later edit the project.", excerpt, 'javascript'); done.append('2.4 excerpt shows the changed lines')

fe.set_variations(S, """**Normal variation — the same account, two spellings.** Register with `" A@example.com "` then log in with `a@example.com`. Predict: both succeed and `GET /api/auth/me` shows `a@example.com`. Then register `a@example.com` again: predict 409 `That email is already registered.` Point at the two lines in `server/server.js` that make the spellings equal.

**Invalid variation — a body that is not an object.** `PUT /api/notes/:id` with the JSON body `[]`, then with `{ title: "x" }`. Predict the two status codes and messages (400 `Send a JSON object.` from the guard at line 16; 400 `Title must contain 2-200 characters.` from `validateNote`), then `GET` the note and deep-equal it against the original: zero fields changed.

**Boundary variation — another user's note.** With user B's token, `GET`, `PUT` and `DELETE` user A's note. Predict 404 for all three and that A's note is intact afterwards. Then read exercise 7 to see why the answer is 404 and not 403, and what an attacker would learn if it were 403."""); done.append('2.4 three concrete variations')

fe.add_exercise(S, '404 or 403: choose deliberately',
"""Every owner check in `server/server.js` answers 404 `Note not found.` whether the note does not exist or belongs to someone else. Make the alternative concrete, then decide.

1. On a throwaway branch, change `PUT /api/notes/:id` so that a note that exists but is not yours answers 403 `Not your note.` (you will need a second lookup: `notes.find(n => n.id === id)` first, then the owner comparison).
2. Write a test in which user B tries to `PUT` a note id that does not exist and one that belongs to A, and record the two status codes.
3. Now play attacker: with only B's token, what can you learn about A's data from the difference between 403 and 404? Write the answer in one sentence (it is the existence of every note id you try).
4. Revert to 404 and add the test that pins the behavior: the two cases must be indistinguishable in status and body.

Acceptance: a test proving `PUT`, `GET` and `DELETE` on a foreign note and on a missing note return identical `{ status, data }`.""",
"""Reference test:

```javascript
test("a foreign note and a missing note are indistinguishable", async () => {
  const mine = (await api("/notes", "POST", { title: "Private", body: "" }, a)).data;
  for (const method of ["GET", "PUT", "DELETE"]) {
    const body = method === "PUT" ? { title: "Taken over", body: "" } : undefined;
    const foreign = await api("/notes/" + mine.id, method, body, b);
    const missing = await api("/notes/00000000-0000-4000-8000-000000000000", method, body, b);
    assert.deepEqual({ s: foreign.status, d: foreign.data }, { s: missing.status, d: missing.data });
  }
  assert.equal((await api("/notes/" + mine.id, "GET", undefined, a)).data.title, "Private");
});
```

Review: the point is not that 403 is always wrong (a shared-workspace app where members can see each other's ids may prefer it) but that the choice leaks or hides existence. Your write-up must say which information the 404 hides, and must show that the check still happens on the server even though the client never lists foreign ids."""); done.append('review#4 exercise 7: 404-vs-403 with enumeration experiment and test (05, 06)')

fe.append_section(S, '04', "## This project's test harness", """`test/http.js` imports the exported `app`, listens on port 0 of 127.0.0.1 and returns `{ origin, close }`; `close()` calls `server.closeAllConnections()` so keep-alive sockets do not hold the process open. `test/notes.test.js` defines its own `api(path, method, body, token)` helper that adds `Authorization: Bearer <token>` when a token is passed, and the `before` hook registers two users and keeps both tokens (`a`, `b`) for the whole file. That is how one test can act as the owner and as a stranger without re-logging. The new expiry test sets `SESSION_TTL_MS` only around one login call, because `issueSession` reads the variable at call time, not at import time. Run everything with `npm test` (`node --test test/*.test.js`; Node 22 expands the pattern itself).""", before='## '); done.append('review#5 harness description (04)')

pj = json.load(open('package.json', encoding='utf-8'))
pins = {"@vitejs/plugin-react": "^6.1.1", "concurrently": "^9.2.1", "cors": "^2.8.6", "express": "^4.22.2", "react": "^18.3.1", "react-dom": "^18.3.1", "vite": "^8.2.2"}
for k in pj['dependencies']:
    pj['dependencies'][k] = pins.get(k, pj['dependencies'][k])
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(pj, indent=2) + '\n')
done.append('review#6 / 2.7 dependencies pinned (kept the glob test script: Node 22 expands it; a bare directory is rejected)')

# VERIFICATION: note the new test count
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **3**.", "Automated test cases: **3** delivered by Astra, plus **1** added in the fix pass (session expiry), for 4 in `test/notes.test.js`.", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
