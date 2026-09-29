import sys, json, os
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'js1-legal-case-tracker'
P = fe.REG[S]['abs']
os.chdir(P)
done = []
B = [
("the React form or status button decides what to send",
 "`client/src/App.jsx`: `handleSubmit` (line 88) sends the whole `form` object to `createItem` or `updateItem` depending on `editingId`; `changeStatus(item, status)` (line 120) sends only the new status. Neither handler validates anything itself: the browser's input types are the only client-side guard, and any server error surfaces through `setMessage(error.message)`. Write down which of the eight form fields reach the server on an edit (all of them, re-sent as a full object) versus a status change (one field)."),
("the client serializes the operation as an HTTP request",
 "`client/src/api.js`: `updateStatus(id, status)` builds `PATCH /api/cases/:id/status` with body `{ status }`; `updateItem` builds `PUT /api/cases/:id` with the full record. The shared `request()` helper sets `Content-Type: application/json`, returns `null` on 204, and throws `new Error(data.error || \"Request failed.\")` when `response.ok` is false. So the text you see in the UI on a rejection is the server's `error` string, verbatim. Note that the client never sends an actor or version: nothing here identifies who is editing."),
("the route parses and validates runtime input",
 "`server/server.js:50` `app.patch(\"/api/cases/:id/status\")` checks `STATUSES.includes(req.body.status)` inline and answers 400 `Choose a valid status.` otherwise. Create and full edit go through the `validateItem` middleware (line 97): type checks on every field, `validDate` for `dueDate` (line 349 rejects 2027-02-29 because the parsed components do not round-trip), the priority allowlist, then `normalizeItem` (line 151), then the length, status, category and `Number.isFinite(amount) && amount >= 0` checks. On success it replaces `req.body` with the normalized object, so the handler after it never sees raw client data."),
("the repository applies the documented change to authoritative state",
 "`createRepository().setStatus(id, status)` (line 290) is the changed function. It finds the record, returns the existing record untouched when `existing.status === status` (the idempotency guard: no `updatedAt` change, no activity entry), otherwise builds `updated`, builds one `activityEntry(id, \"status\", ...)`, replaces the record in `items` and unshifts the entry onto `activity`. Compare with `update(id, input)` (line 280), which always writes an `updated` entry; before Astra's change `setStatus` delegated to `update`, which is why every status click used to add a misleading history row."),
("the storage boundary commits or rejects",
 "There is no database: `items` and `activity` are arrays captured in the `createRepository` closure. `items = items.map(...)` and `activity.unshift(entry)` run synchronously with no `await` between them, so within one Node process no other request can observe the record changed but the history missing. That is the only reason the concurrent-PATCH test passes. Restarting the process reseeds from the two hard-coded cases; a real store would need a transaction to keep the same guarantee."),
("the response tells the client what actually happened",
 "The route answers `res.json(item)` with the updated record, or 404 `{ error: \"CaseFile not found.\" }`. `changeStatus` in `App.jsx` then calls `refresh()` and, if the row is selected, `loadActivity(item.id)`: the UI re-reads the list and the activity feed from the server instead of trusting the PATCH response. That re-read is what makes the \"one status entry\" behavior visible in the browser."),
]
fe.set_boundaries(S, B); done.append('review#2 / 2.2 six distinct trace-lab boundaries (07)')
R = [
"your acceptance example must state whether the window is computed on the server from a query parameter or on the client, and whether both ends are inclusive; test a record due exactly on the boundary day; and show that `total` and page clamping still count only the filtered rows (the filter must run inside `query()` before `total` is computed, not after the slice).",
"the reason must be stored on the `status` activity entry only, never on the record; a repeat with the same status must write nothing (no entry, no `updatedAt` change) even when a reason is supplied; a blank reason must be rejected with 400 without changing the status; and you must decide, and document, whether a `PUT` that changes `status` still bypasses the reason rule.",
"after deleting the only row on page 2 of a filtered list, requesting page 2 again must clamp to page 1 with the remaining rows and `total` 2; a filter that now matches nothing must return `total` 0 and `page` 1 with an empty `items`; assert on the ids returned, not only on `items.length`.",
"the check must live in `update()` before `items = items.map(...)`, comparing a client-supplied `updatedAt` (or a new `version` counter) with the stored one; a mismatch answers 409 without mutating the record or adding activity; your test must send two sequential `PUT`s with the same stale value and assert the second is 409 and the stored record equals the first result.",
]
fe.set_reviews(S, R); done.append('review#3 / 2.3 per-exercise review criteria (06)')
code = open('server/server.js', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
excerpt = '\n'.join(code[289:303]) + '\n\n// validateItem, server/server.js:147\n' + '\n'.join(code[146:149]) + '\n\n// server/server.js:349\n' + '\n'.join(code[348:356])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/51/server/server.js` with `diff --strip-trailing-cr -w`). `setStatus` (line 290) no longer delegates to `update`, so a repeated status writes nothing and a real change writes exactly one `status` entry together with the record; `validateItem` gained the finite, nonnegative amount check (line 147) and `validDate` (line 349) rejects calendar-impossible dates. The linked source is authoritative if you later edit the project.", excerpt, 'javascript'); done.append('2.4 excerpt now shows changed lines')
fe.set_variations(S, """**Normal variation — a real edit.** `PUT /api/cases/:id` with the full valid fixture but `priority: "High"`. Predict: 200, the returned record has `priority: "High"`, a new `updatedAt`, and `GET /activity` shows one more `updated` entry; `status` is unchanged. Run it and confirm the entry count moved by exactly one.

**Invalid variation — an impossible date.** `PUT` the same record with `dueDate: "2027-02-29"`. Predict: 400 with `Use a real date in YYYY-MM-DD format.`, and `GET /api/cases/:id` deep-equals the record from before the edit (the test in `test/workflow.test.js` does exactly this comparison). Count activity entries before and after: zero writes must have happened.

**Boundary variation — the same status twice, at once.** Send two `PATCH /status` requests with `{ status: "Discovery" }` in a `Promise.all`. Predict: both 200, exactly one `status` activity entry, `updatedAt` set once. Then `PATCH` with `{ status: "Unknown" }`: 400 and nothing written. Explain why the synchronous body of `setStatus` makes the first case safe in one process, and what a PostgreSQL version would need (`SELECT ... FOR UPDATE` or a conditional `UPDATE ... WHERE status <> $1`) to keep the same guarantee."""); done.append('2.4 three concrete variations')
fe.add_exercise(S, 'ownership and authorization',
"""Every record already has an `owner` string, but any browser can edit any record. Add an actor to each request and enforce ownership.

1. Read a caller identity from the `X-Actor` request header in one small middleware (`server/server.js`, before the routes) and attach it as `req.actor`. A missing or blank header on `POST`, `PUT`, `PATCH` or `DELETE` answers 401 `{ error: "Sign in to change records." }`. `GET` routes stay open.
2. In `PUT /api/cases/:id`, `PATCH /api/cases/:id/status` and `DELETE /api/cases/:id`, load the existing record first; if `existing.owner !== req.actor` answer 403 `{ error: "Only the owner can change this case." }` and do not call the repository.
3. On `POST`, force `owner` to `req.actor` regardless of the body, so a caller cannot create a record on someone else's behalf.
4. In `client/src/api.js`, send `X-Actor` from a small "signed in as" input in the form panel.

Acceptance: write the four assertions before coding: cross-owner `PUT` is 403 and the stored record deep-equals the original; cross-owner `PATCH /status` is 403 with no new activity; owner `PATCH` still 200; missing header is 401. Then extend `test/http.js`'s `request()` to accept a headers argument and write the test.""",
"""Reference implementation (keep it small; the point is where the check lives, not the header format):

```javascript
// server/server.js, after app.use(express.json())
app.use((req, _res, next) => {
  req.actor = String(req.get("X-Actor") || "").trim();
  next();
});
function requireActor(req, res, next) {
  if (!req.actor) return res.status(401).json({ error: "Sign in to change records." });
  next();
}
function requireOwner(req, res, next) {
  const existing = repository.find(req.params.id);
  if (!existing) return res.status(404).json({ error: "CaseFile not found." });
  if (existing.owner !== req.actor)
    return res.status(403).json({ error: "Only the owner can change this case." });
  next();
}
app.post("/api/cases", requireActor, validateItem, (req, res) =>
  res.status(201).json(repository.create({ ...req.body, owner: req.actor })),
);
app.put("/api/cases/:id", requireActor, requireOwner, validateItem, (req, res) =>
  res.json(repository.update(req.params.id, req.body)),
);
app.patch("/api/cases/:id/status", requireActor, requireOwner, (req, res) => { /* unchanged body */ });
app.delete("/api/cases/:id", requireActor, requireOwner, (req, res) => { /* unchanged body */ });
```

Reference test (after adding a `headers = {}` parameter to `request()` in `test/http.js` and spreading it into `fetch`'s headers):

```javascript
test("only the owner can change a case", async () => {
  const mine = { "X-Actor": "Junior Learner" }, other = { "X-Actor": "Someone Else" };
  const made = await call(route, "POST", valid, mine);
  const path = route + "/" + made.data.id;
  assert.equal((await call(path, "PUT", { ...valid, title: "Hijacked" }, other)).status, 403);
  assert.deepEqual((await call(path)).data, made.data);
  assert.equal((await call(path + "/status", "PATCH", { status: "Discovery" }, other)).status, 403);
  assert.equal((await call(path + "/activity")).data.filter((x) => x.kind === "status").length, 0);
  assert.equal((await call(path + "/status", "PATCH", { status: "Discovery" }, mine)).status, 200);
  assert.equal((await call(path, "PUT", { ...valid })).status, 401);
});
```

Review: the 403 must be decided before any repository call, and `POST` must overwrite `owner` from the header (a body `owner` of someone else is not an error, it is simply ignored). Explain why 403, not 404, is the right answer here, and when a 404 would leak less information."""); done.append('2.5 ownership/authz exercise 7 with reference code and test (05, 06)')
fe.append_section(S, '04', "## This project's test harness", """`test/http.js` imports the exported `app` from `server/server.js`, listens on port 0 of 127.0.0.1 (the OS picks a free port), and returns `{ origin, close }`. `request(origin, path, method, body)` is a thin `fetch` wrapper that returns `{ status, data }` and never throws on a 4xx, which is why the tests can assert `status === 400` and then re-read the record. The server module is loaded once per test process, so all three tests share one in-memory repository; run the suite with `npm test` (which is `node --test test/`, the directory form that works in PowerShell and cmd.exe alike).""", before='## '); done.append('review#6 harness description (04)')
pj = json.load(open('package.json', encoding='utf-8'))
pins = {"@vitejs/plugin-react": "^5.1.2", "concurrently": "^9.2.1", "cors": "^2.8.6", "express": "^4.22.2", "react": "^19.2.8", "react-dom": "^19.2.8", "vite": "^6.4.3"}
for k in pj['dependencies']:
    pj['dependencies'][k] = pins.get(k, pj['dependencies'][k])
pj['scripts']['test'] = "node --test test/"
open('package.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(pj, indent=2) + '\n')
done.append('review#4 / 2.7 dependencies pinned (react 19.2.8, vite 6.4.3, express 4.22.2, cors 2.8.6, plugin-react 5.1.2, concurrently 9.2.1)')
done.append('review#5 npm test = node --test test/')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
