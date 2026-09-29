import sys, json, os, re, glob, shutil
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
HERE = os.path.dirname(__file__)
def rd(p): return open(p, encoding='utf-8-sig').read()
def w(p, s):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True); open(p, 'w', encoding='utf-8', newline='\n').write(s)
def finish(S, done):
    json.dump(done, open(os.path.join(HERE, S + '.done.json'), 'w')); print(f'== {S}\n' + '\n'.join(done))
ONLY = sys.argv[1:]  # optional: run only these slugs

# ---------------------------------------------------------------- buildwhiteboard
S = 'buildwhiteboard'
if not ONLY or S in ONLY:
    os.chdir(fe.REG[S]['abs']); done = []
    fe.append_section(S, '01', '## Formatting', """The client (`client/src/App.tsx`) and `server/index.js` are formatted with Prettier at 100 columns (fix pass); the delivered files had several 500-900 character lines in the JSX. If you reformat again, keep 100 columns so diffs stay reviewable.""", before='## ')
    done.append('review#1 App.tsx and server/index.js reformatted with prettier at 100 columns in the pipeline; 01 notes the width')
    fe.append_section(S, '02', '## Two channels, one document', """```
   client A                      server                        client B
   ────────                      ──────                        ────────
   POST /api/documents  ──HTTP──▶ validate, version+1, persist ◀──HTTP──  GET /api/documents/:id
        (metadata: title, version; 409 on a stale version)
   ┌─────────────────────────── WebSocket (y-websocket) ───────────────────────────┐
   │ sync step 1: "here is my state vector"  ──▶  server replies with the missing updates │
   │ sync step 2: client applies them; both now hold the same Yjs document                 │
   │ update: every keystroke is a CRDT update broadcast to every peer in the room          │
   │ awareness: cursors and names, ephemeral, never persisted                              │
   │ persist: the server writes the Yjs state to disk on a timer / on room close            │
   └────────────────────────────────────────────────────────────────────────────────────────┘
                                   ▲ "Live ≠ durable": a peer can see your text before the server has persisted it
```

**Glossary.** *State vector*: a compact summary of which updates a peer already has, per client id; sync step 1 sends it. *Sync step 1 / step 2*: the handshake in which a joining client states what it has and receives what it lacks, then confirms. *Update*: one CRDT delta, applied in any order with the same result. *Awareness*: presence data (cursor, name) shared over the same socket but not part of the document. *Versioned metadata*: the title and version row behind `POST /api/documents`, with the compare-and-set check; the text is not versioned this way because the CRDT resolves it. *Live ≠ durable*: the gap between what peers see and what the server has written; practice ticket 2 closes it with an acknowledged persistence status.""", before='## ')
    done.append('review#2 02 message-flow diagram (HTTP versioned metadata vs WebSocket sync/update/awareness/persist) with the live-vs-durable gap and a glossary box')
    def rm(t):
        t = t.replace('npm.cmd ci\nnpm.cmd ci --prefix client\nnpm.cmd ci --prefix server\nnpm.cmd run dev:server', 'npm.cmd run install:all        # = npm ci in client, server and the root\nnpm.cmd run dev:server', 1)
        if 'Docker files are unverified' not in t:
            t = t.replace('## Start locally\n', '## Start locally\n\n**Before anything else:** copy `.env.example` where the README says and set the two URLs; every "cannot connect" report in this course comes from skipping it. The `docker-compose.yml` and `Dockerfile.*` at the root are unverified scaffolding (Docker was not run in the recorded verification); start with Node locally, not with Docker.\n', 1)
        return t
    fe.rw('astraupskill/README.md', rm)
    fe.rw('README.md', lambda t: t.replace('Docker scaffolding remains available through `docker compose up --build`, with the client exposed on port 8080. Docker execution was not verified in this environment.', 'Docker scaffolding remains available through `docker compose up --build`, with the client exposed on port 8080. **The Docker files are unverified scaffolding**: Docker execution was not verified in this environment, so start locally with Node first.', 1))
    done.append('review#3 README uses install:all and moves the .env.example warning to the top of the section; review#4 both READMEs mark the Docker files as unverified scaffolding')
    fe.rw('astraupskill/05-PRACTICE.md', lambda t: t.replace('## 3. Improve editor selection and composition behavior\n', """## 3. Improve editor selection and composition behavior

*Why the callback form.* Find-and-replace must call `text.replace(search, () => replacement)` (or `split(search).join(replacement)`), never `text.replace(search, replacement)`: with a string replacement, JavaScript interprets `$&` (the match), `$1`, `` $` `` and `$'` inside it. A user replacing `foo` with `$&bar` would get `foobar` instead of the literal `$&bar`. Add this browser scenario to `tests/collaboration.spec.ts` as part of this ticket: type `foo foo`, search `foo`, replace with `$&x`, click replace, and expect the document text to be exactly `$&x $&x`.

""", 1))
    fe.rw('astraupskill/05-PRACTICE.md', lambda t: t.replace('## 5. Add authenticated ownership and sharing\n', """## 5. Add authenticated ownership and sharing

Acceptance criteria (this ticket is the one that turns the project into the target stack, so it gets the same precision as tickets 1 and 2):

1. The owner of a document is derived from the session on the server (`req.session.userId` or a verified token), never from the request body or the room name.
2. `GET /api/documents/:id` for a known id by a non-member answers **404**, not 403: a caller must not learn that a document exists. Members get 200; the owner can add members with `POST /api/documents/:id/members`.
3. The WebSocket join is authorized the same way: a socket for a room the user is not a member of is closed before sync step 1 runs.
4. A server test proves isolation: create a document as user A, attempt `GET` and the socket join as user B, assert 404 and a closed socket, then add B as a member and assert both succeed. A second test proves A cannot read B's document either (symmetry).
5. The existing `documents.test.js` cases still pass with a default test session.

""", 1))
    done.append('review#5 05 ticket 3 explains the callback form of replace with the $& example and names the browser scenario; review#6 ticket 5 has five concrete acceptance criteria (session-derived owner, 404 not 403, socket authorization, isolation tests)')
    finish(S, done)

# ---------------------------------------------------------------- buildsql
S = 'buildsql'
if not ONLY or S in ONLY:
    os.chdir(fe.REG[S]['abs']); done = []
    if not os.path.isdir('src/views'):
        src = rd('src/App.tsx').replace('\r\n', '\n')
        lines = src.split('\n')
        def fn_range(name):
            start = next(i for i, l in enumerate(lines) if re.match(rf'(export )?function {name}\b', l))
            # top-level functions end at the next line that is exactly "}" at column 0
            end = next(i for i in range(start + 1, len(lines)) if lines[i] == '}')
            return start, end
        imports_end = next(i for i, l in enumerate(lines) if l.startswith('const worldTone'))
        import_block = '\n'.join(lines[:imports_end]).rstrip('\n')
        import_block_views = import_block.replace('from "./', 'from "../')
        helper_names = ['compactTitle', 'missionTitle', 'briefingCore', 'Loading', 'SectionTitle']
        # shared.tsx: worldTone const + helpers
        wt_start = imports_end
        wt_end = next(i for i in range(wt_start, len(lines)) if lines[i] == '};')
        shared_parts = ['\n'.join(lines[wt_start:wt_end + 1]).replace('const worldTone', 'export const worldTone')]
        removed = [(wt_start, wt_end)]
        for h in helper_names:
            a, b = fn_range(h); removed.append((a, b))
            shared_parts.append('\n'.join(lines[a:b + 1]).replace(f'function {h}', f'export function {h}', 1))
        w('src/views/shared.tsx', import_block_views + '\n\n' + '\n\n'.join(shared_parts) + '\n')
        views = ['HomeView', 'WorldCard', 'JourneyView', 'MissionView', 'ReviewsView']
        view_texts = {}
        for v in views:
            a, b = fn_range(v); removed.append((a, b))
            view_texts[v] = '\n'.join(lines[a:b + 1]).replace(f'function {v}', f'export function {v}', 1)
        for v in views:
            body = view_texts[v]
            uses_shared = [n for n in helper_names + ['worldTone'] if re.search(rf'\b{n}\b', body)]
            uses_views = [n for n in views if n != v and re.search(rf'\b{n}\b', body)]
            imp = import_block_views + '\n'
            if uses_shared: imp += 'import { ' + ', '.join(uses_shared) + ' } from "./shared";\n'
            for n in uses_views: imp += f'import {{ {n} }} from "./{n}";\n'
            w(f'src/views/{v}.tsx', imp + '\n' + body + '\n')
        # rebuild App.tsx without the moved ranges, with imports for what App() uses
        keep = [l for i, l in enumerate(lines) if not any(a <= i <= b for a, b in removed)]
        app_src = '\n'.join(keep)
        app_body = app_src[len(import_block):]
        extra = ''
        used_helpers = [n for n in helper_names + ['worldTone'] if re.search(rf'\b{n}\b', app_body)]
        if used_helpers: extra += 'import { ' + ', '.join(used_helpers) + ' } from "./views/shared";\n'
        for v in views:
            if re.search(rf'\b{v}\b', app_body): extra += f'import {{ {v} }} from "./views/{v}";\n'
        app_src = import_block + '\n' + extra + re.sub(r'\n{3,}', '\n\n', app_body)
        w('src/App.tsx', app_src)
        done.append(f'review#1 src/App.tsx split: HomeView, WorldCard, JourneyView, MissionView, ReviewsView moved to src/views/<Name>.tsx and the shared helpers (worldTone, compactTitle, missionTitle, briefingCore, Loading, SectionTitle) to src/views/shared.tsx; App.tsx keeps routing and the workspace hook ({len(app_src.splitlines())} lines)')
    fe.rw('astraupskill/01-CODEBASE-MAP.md', lambda t: t.replace('| `src/PracticeView.tsx`      | Controlled project form, list, search, filter and pagination   | What happens to input after rejection?                   |', '| `src/App.tsx`               | Routing, the workspace hook, and view selection (about 400 lines after the fix pass) | Which view owns which piece of state?                    |\n| `src/views/*.tsx`           | `HomeView`, `JourneyView`, `MissionView`, `ReviewsView`, `WorldCard`; `shared.tsx` holds the helpers they share | What does each view read from the workspace, and what does it write back? |\n| `src/PracticeView.tsx`      | Controlled project form, list, search, filter and pagination   | What happens to input after rejection?                   |', 1))
    fe.append_section(S, '01', '## House style', """`src/progression.ts` (and a few other files) declare several constants in one `const a = ..., b = ...;` statement. It is a style choice, not a trick: read each comma as a new declaration. If you touch such a file, split it into one declaration per line in the same change; the fix pass left the existing ones alone so the diff stays about behavior.""", before='## ')
    done.append('review#1 01 table points at App.tsx and src/views/; review#5 01 house-style note on multi-declarator constants')
    fe.append_section(S, '02', '## The three states a project passes through', """```
  form draft ──(apply: putProject in progression.ts)──▶ workspace draft ──(save: commit in storage.ts)──▶ accepted IndexedDB state
  (PracticeView local state)                            (useWorkspace draft, "unsaved", still revision N)   (revision N+1, what a reload shows)
        ▲ validateProject rejects here: the form keeps its values, the draft is untouched
```

Three functions, three transitions: `putProject` validates and produces the next project list inside the workspace draft; `useWorkspace`'s apply marks the draft unsaved; `commit` in `storage.ts` compares the revision and writes. Trace A in `07-TRACE-LAB.md` asks you to name each of them; this is the chain.""", before='## ')
    done.append('review#3 02 ASCII chain form draft -> workspace draft -> accepted state with the function per transition')
    fe.rw('README.md', lambda t: t if 'not itself a SQL course' in t else t.replace('# IPSKILL: six-track curriculum and applied CRUD practice\n', '# IPSKILL: six-track curriculum and applied CRUD practice\n\n**This is IPSKILL, a React app.** It displays a SQL/TS/Node/React/C#/.NET lesson archive; it is not itself a SQL course, despite the folder name `buildsql`.\n', 1))
    done.append('review#4 root README first paragraph says what the project is (a React app displaying an archive, not a SQL course)')
    w('astraupskill/08-BACKEND-TICKET.md', """# 08. Backend ticket: the contacts API behind practice ticket 3

[Course index](README.md)

Practice ticket 3 asks for a real backend. This chapter scaffolds it so the course's ideas (expected versions, rejected-write UX, shared validation) reach Node. Everything here runs with Node 22 and no packages except Express; the schema is SQLite via `node:sqlite`.

## Schema (`api/schema.sql`)

```sql
CREATE TABLE IF NOT EXISTS contacts (
  id         TEXT PRIMARY KEY,
  name       TEXT NOT NULL CHECK (length(name) BETWEEN 1 AND 120),
  email      TEXT NOT NULL,
  goal       TEXT NOT NULL DEFAULT '',
  status     TEXT NOT NULL CHECK (status IN ('planned', 'active', 'complete')),
  version    INTEGER NOT NULL DEFAULT 1,
  updated_at TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS contacts_email_ci ON contacts (lower(email));
```

## Router (`api/contacts.js`)

```js
import { Router } from 'express';
import { randomUUID } from 'node:crypto';
import { validateContact } from '../src/contracts.js';        // shared validation: the same rules the React form uses

export function contactsRouter(db) {
  const r = Router();
  const etag = (v) => `"${v}"`;
  const expected = (req) => { const m = /^"(\\d+)"$/.exec(req.get('if-match') ?? ''); return m ? Number(m[1]) : null; };

  r.get('/', (req, res) => {
    const page = Math.max(1, Number(req.query.page) || 1), size = 20;
    const q = String(req.query.q ?? '').trim().toLowerCase();
    const where = q ? `WHERE lower(name) LIKE ? OR lower(email) LIKE ?` : '';
    const args = q ? [`%${q}%`, `%${q}%`] : [];
    const total = db.prepare(`SELECT count(*) AS n FROM contacts ${where}`).get(...args).n;
    const items = db.prepare(`SELECT * FROM contacts ${where} ORDER BY name, id LIMIT ? OFFSET ?`).all(...args, size, (page - 1) * size);
    res.json({ items, page, size, total });
  });

  r.post('/', (req, res) => {
    const errors = validateContact(req.body); if (errors.length) return res.status(400).json({ errors });
    const row = { id: randomUUID(), ...req.body, version: 1, updated_at: new Date().toISOString() };
    try { db.prepare('INSERT INTO contacts (id, name, email, goal, status, version, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)').run(row.id, row.name, row.email, row.goal ?? '', row.status, 1, row.updated_at); }
    catch (e) { if (String(e.message).includes('UNIQUE')) return res.status(409).json({ error: 'A contact with this email already exists.' }); throw e; }
    res.status(201).set('ETag', etag(1)).json(row);
  });

  r.get('/:id', (req, res) => {
    const row = db.prepare('SELECT * FROM contacts WHERE id = ?').get(req.params.id);
    return row ? res.set('ETag', etag(row.version)).json(row) : res.status(404).end();
  });

  r.put('/:id', (req, res) => {
    const v = expected(req); if (v === null) return res.status(428).json({ error: 'Send If-Match with the version you loaded.' });
    const errors = validateContact(req.body); if (errors.length) return res.status(400).json({ errors });
    const result = db.prepare('UPDATE contacts SET name = ?, email = ?, goal = ?, status = ?, version = version + 1, updated_at = ? WHERE id = ? AND version = ?')
      .run(req.body.name, req.body.email, req.body.goal ?? '', req.body.status, new Date().toISOString(), req.params.id, v);
    if (result.changes === 0) return db.prepare('SELECT 1 FROM contacts WHERE id = ?').get(req.params.id) ? res.status(409).json({ error: 'Changed since you loaded it. Reload and reapply your edit.' }) : res.status(404).end();
    res.set('ETag', etag(v + 1)).json({ ...req.body, id: req.params.id, version: v + 1 });
  });

  r.delete('/:id', (req, res) => { res.status(db.prepare('DELETE FROM contacts WHERE id = ?').run(req.params.id).changes ? 204 : 404).end(); });
  return r;
}
```

## Reference integration test for the 409 (`api/contacts.test.js`, node:test + supertest)

```js
test('a stale If-Match is refused and the row is unchanged', async () => {
  const created = await request(app).post('/contacts').send({ name: 'Ada', email: 'ada@example.com', status: 'planned' }).expect(201);
  await request(app).put(`/contacts/${created.body.id}`).set('If-Match', '"1"').send({ ...created.body, name: 'Ada L.' }).expect(200);
  const stale = await request(app).put(`/contacts/${created.body.id}`).set('If-Match', '"1"').send({ ...created.body, name: 'Ada X' });
  assert.equal(stale.status, 409);
  const row = await request(app).get(`/contacts/${created.body.id}`).expect(200);
  assert.equal(row.body.name, 'Ada L.'); assert.equal(row.body.version, 2);
});
```

Add the other four (400 from the shared validator, 409 on a duplicate email differing only by case, 428 without `If-Match`, 404 after delete) and connect `PracticeView` to it: the form's rejected-write UX (keep the draft, show the message) is unchanged, only the acceptance moves to the server.
""")
    done.append('review#2 08-BACKEND-TICKET.md scaffolds practice ticket 3 (schema with lowercased-email unique index and version, Express router with If-Match/409/428, reference 409 integration test)')
    finish(S, done)

# ---------------------------------------------------------------- formforge
S = 'formforge'
if not ONLY or S in ONLY:
    os.chdir(fe.REG[S]['abs']); done = []
    fe.append_section(S, 'README', '## If this fails, it means', """| symptom | cause | do this |
|---|---|---|
| `pnpm install --offline` stops with a missing package | the offline store lacks one dependency (seen in the recorded run) | run the locked online install once: `pnpm.cmd install --frozen-lockfile` |
| Turbo errors about an ancestor directory or permissions | Turbo walks up from the project looking for a workspace root and hits a protected folder | run from an unrestricted path (not under a synced or system directory) |
| an API test fails with a 5 s timeout on the first parallel run | cold-start cost of the Fastify app under full parallelism | use `pnpm.cmd -r --workspace-concurrency=1 exec vitest run --maxWorkers=2` |
| `pnpm : File ... cannot be loaded` in PowerShell | the PowerShell shim is blocked by the execution policy | call `pnpm.cmd` instead of `pnpm` |""", before='## Course sequence')
    done.append('review#1 README "if this fails, it means" table for the four known environment failure modes')
    w('astraupskill/00-PREREQS.md', """# 00. Prerequisites: four things this course assumes

[Course index](README.md)

## pnpm workspaces

`pnpm-workspace.yaml` lists the packages (`apps/*`, `packages/*`). One `pnpm install` at the root installs all of them and links `@formforge/core` into `apps/api` and `apps/web` as if it were published, so a change in `packages/core` is visible to both apps immediately. `pnpm -r exec <cmd>` runs a command in every package; `pnpm --filter web exec vitest run` runs it in one. The lockfile is shared, which is why the install is one step and why `--frozen-lockfile` is the reproducible form.

## Turbo's task graph

`turbo.json` declares tasks (`build`, `lint`, `typecheck`, `test`) and their dependencies, for example that `build` in an app depends on `build` in the packages it imports (`"dependsOn": ["^build"]`). `turbo run test` computes that graph, runs independent tasks in parallel and caches outputs by input hash, so an unchanged package's task is replayed from cache. When something looks stale, `turbo run build --force` bypasses the cache. `--concurrency=2` bounds the parallelism on a small machine.

## `app.inject()`

The API tests never start a listening server. Fastify's `app.inject({ method, url, headers, payload })` pushes a synthetic request through the whole app (routing, hooks, validation, handlers, serialization) and returns the response object, in-process. It is faster, needs no free port, and cannot be affected by another test's server. The trade-off: anything that only happens on a real socket (TLS, keep-alive, proxies) is not covered, and you must remember that a passing `inject` test says nothing about the deployment in front of it.

## What a workspace, a form and a publication are here

A *workspace* owns forms (`x-workspace-id` names it in this demo; chapter 06 explains why that header is not authentication). A *form schema* is the editable draft with a version; a *publication* freezes one version under a slug, and the slug-ownership invariant (one slug, one workspace) is what the worked change protects. Keep those three nouns straight and the rest of the course reads easily.
""")
    fe.rw('astraupskill/README.md', lambda t: t.replace('## Course sequence\n', '## Course sequence\n\nRead [00-PREREQS.md](00-PREREQS.md) first if pnpm workspaces, Turbo, `app.inject()` or the workspace/form/publication nouns are new to you.\n', 1))
    done.append('review#2 00-PREREQS.md (pnpm workspaces, Turbo task graph, app.inject, the three nouns) linked from README')
    def t6(t):
        if 'superseded save reports a conflict' in t: return t
        add = """
  it("ignores a conflict from a superseded save and lets the queued edit surface it with the committed version", async () => {
    vi.useFakeTimers();
    const first = deferred<DraftSaveResult>();
    const save = vi.fn<DraftSaver>().mockImplementationOnce(() => first.promise).mockResolvedValueOnce({ status: "conflict", serverVersion: 3 });
    render(<RaceHarness save={save} />);
    await act(async () => screen.getByRole("button", { name: "Edit one" }).click());
    await act(async () => vi.advanceTimersByTime(300));           // first save in flight
    await act(async () => screen.getByRole("button", { name: "Edit two" }).click());
    await act(async () => vi.advanceTimersByTime(100));           // newer edit queued
    await act(async () => first.resolve({ status: "conflict", serverVersion: 3 }));
    // The superseded save's conflict is not shown: the newer edit is what the user cares about.
    expect(screen.getByRole("status")).toHaveTextContent("Changes queued");
    await act(async () => vi.advanceTimersByTime(200));
    // The queued save is sent with the still-committed version 0 (a conflict does not advance it) and surfaces the conflict itself.
    expect(save.mock.calls[1]).toEqual([expect.objectContaining({ title: "Edit two" }), 0]);
    expect(screen.getByRole("status")).toHaveTextContent("Save conflict with server version 3");
  });
"""
        idx = t.rstrip().rfind('});')
        return t[:idx] + add.lstrip('\n') + t[idx:]
    fe.rw('apps/web/src/useAutosave.test.tsx', t6)
    fe.rw('astraupskill/03-WORKED-CHANGE.md', lambda t: t if 'superseded save' in t else t.replace('committed version is still retained', 'committed version is still retained. A related decision, pinned by the sixth autosave test (fix pass): when a *superseded* save comes back with a conflict after a newer edit was queued, the hook drops that status on purpose. The newer save will run with the same committed version and produce the same conflict, so the user sees one conflict for the edit they actually care about instead of a stale one for text they already changed; and because a conflict never advances `version.current`, nothing is lost by ignoring the first. Dropping it silently would be wrong only if the queued save could *succeed* against the moved server version, which it cannot', 1))
    done.append('review#3 sixth autosave test (superseded conflict is ignored; the queued edit resends with the committed version and surfaces the conflict); 03 records the decision')
    fe.append_section(S, '05', '## 7. Make publications durable', """Replace `InMemoryPublicationRepository` with a SQLite (or PostgreSQL) implementation behind the existing `PublicationRepository` interface in `apps/api`. The slug-ownership invariant moves from a `Map` check into the database: `CREATE UNIQUE INDEX publications_slug ON publications (slug)` plus a `workspace_id` column, so a second workspace publishing an existing slug fails on the index inside the transaction, not on a check that two concurrent requests can both pass. Acceptance: the existing `app.test.ts` publish cases pass unchanged against the new repository (the interface was the seam); a new test fires two publishes of the same slug from two workspaces concurrently (`Promise.all`) and asserts exactly one 201 and one 409 with one row; and the in-memory repository stays for the unit tests, selected by an environment variable, not by editing code.""", before='## Capstone')
    fe.append_section(S, '06', '## Why a header-as-identity demo must never ship, and what replacing it looks like', """`x-workspace-id` is read straight from the request; anyone can send any value, so the "authorization" in the publish route is a suggestion. The capstone replaces it with a minimal session lookup: a `sessions` table (`id`, `user_id`, `expires_at`), a `Cookie: session=<id>` set by a `POST /login` fixture, a Fastify `onRequest` hook that loads the session and its memberships, and a route check `if (!request.user.workspaces.includes(request.params.workspaceId)) return reply.code(404).send()` (404, so a non-member cannot enumerate workspaces). The header disappears entirely; tests use `app.inject` with the cookie from the login fixture. The lesson is not the session table, it is the direction of trust: identity must come from something the server issued and can verify, never from something the caller typed.""", before='## ')
    done.append('review#4 05 item 7: durable publication repository with the unique index and a concurrency test; review#5 06 explains replacing the header with a session lookup and why')
    finish(S, done)

# ---------------------------------------------------------------- geminiorganized-llm-generated-helper
S = 'geminiorganized-llm-generated-helper'
if not ONLY or S in ONLY:
    os.chdir(fe.REG[S]['abs']); done = []
    if not os.path.isdir('practice-journal'):
        os.makedirs('practice-journal/test', exist_ok=True)
        shutil.move('src/practice', 'practice-journal/src')
        for tf in ['practice.test.js', 'practice-http.test.js']:
            shutil.move(f'test/{tf}', f'practice-journal/test/{tf}')
            fe.rw(f'practice-journal/test/{tf}', lambda t: t.replace('../src/practice/', '../src/').replace('"../src/shared/', '"../../src/shared/'))
        for sf in glob.glob('practice-journal/src/*.js'):
            fe.rw(sf, lambda t: t.replace('"../shared/', '"../../src/shared/'))
        w('practice-journal/package.json', json.dumps({"name": "practice-journal", "private": True, "version": "1.0.0", "description": "Local CRUD practice journal: profiles, questions, sessions and scored attempts with revision checks and a writer lease.", "scripts": {"setup": "node src/setup.js", "start": "node src/server.js", "test": "node --test test/"}, "engines": {"node": ">=22"}}, indent=2) + '\n')
        pk = json.load(open('package.json', encoding='utf-8-sig'))
        pk['description'] = 'AI Call Assistant: a local Electron audio assistant (legacy). The learning app lives in practice-journal/.'
        pk['scripts']['practice:setup'] = 'node practice-journal/src/setup.js'; pk['scripts']['practice'] = 'node practice-journal/src/server.js'; pk['scripts']['test:practice'] = 'node --test practice-journal/test/'
        w('package.json', json.dumps(pk, indent=2) + '\n')
        fe.rw('verification/run-tests.js', lambda t: t.replace('.readdirSync(directory)', '.readdirSync(directory)', 1))
        for f in glob.glob('astraupskill/*.md') + ['README.md']:
            fe.rw(f, lambda t: t.replace('src/practice/', 'practice-journal/src/').replace('test/practice.test.js', 'practice-journal/test/practice.test.js').replace('test/practice-http.test.js', 'practice-journal/test/practice-http.test.js'))
        fe.rw('README.md', lambda t: t.replace('# Practice Journal and AI Call Assistant\n\nStart with **Practice Journal**, a local CRUD web app', '# AI Call Assistant\n\nThis repository is the AI Call Assistant, a local Electron audio assistant (see `docs/` for its original documentation; `npm start` launches it, `npm test` runs its suites).\n\n## Learning app: Practice Journal\n\nA separate learning application lives in [`practice-journal/`](practice-journal/) with its own `package.json`: **Practice Journal**, a local CRUD web app', 1))
        done.append('review#1 the journal moved to practice-journal/ (own package.json: setup/start/test), root package.json describes the AI Call Assistant again with practice:*/test:practice scripts pointing at the new folder; README leads with the assistant and links the journal; astraupskill paths updated')
    fe.rw('astraupskill/01-CODEBASE-MAP.md', lambda t: t if 'contracts (validation)' in t else t.rstrip('\n') + """

## Inside `practice-journal/src/domain.js`

The file is one module, but it has four sections with different jobs; read it as four files. (Splitting it physically is practice material: the four groups below are the boundaries, and `module.exports` at the bottom is the only public surface.)

| section | lines (approx.) | contents | boundary |
|---|---|---|---|
| contracts (validation) | `KINDS` .. `payload()` | field limits, required/immutable fields, `text()`, `payload()` | what a record may contain |
| relations | `find()`, `validateState()`, `references()` | reference and scope rules between profiles, questions, sessions, attempts | what may point at what |
| lifecycle | `createState()`, `authenticate()`, `bootstrap()` | workspace creation, token check, snapshot bootstrap | when the state exists and who may touch it |
| service | `createService()` | read/create/update/delete with the revision check and the writer lease | how a change becomes durable |
""")
    done.append('review#2 PARTIAL: domain.js is not split; 01 documents its four sections as the boundaries a split would follow (the physical split is left as practice)')
    fe.rw('astraupskill/03-WORKED-CHANGE.md', lambda t: t.replace("""```javascript
assert.throws(() => store.set({ resume: 'Rejected resume' }));
assert.equal(store.get('resume'), 'Accepted resume');
assert.deepEqual(fs.readFileSync(file), before);
```""", """The copy-pasteable form, as it appears in `practice-journal/test/practice.test.js` (the injection, the assertion matcher and the restore are all there; a learner reproducing it gets a green test):

```javascript
test("an injected replacement failure rolls back the resource and its activity entry", (t) => {
  let fail = false;
  const fsImpl = Object.create(fs);
  fsImpl.renameSync = (...args) => {
    if (fail) throw new Error("Synthetic replacement failure");
    return fs.renameSync(...args);
  };
  const f = fixture(t, { fsImpl });          // a disposable data file; nothing real is touched
  const before = fs.readFileSync(f.file);
  fail = true;
  assert.throws(() => f.create("profiles", { name: "Not accepted" }), /replacement failure/);
  assert.deepEqual(fs.readFileSync(f.file), before);
  assert.equal(f.service.read().value.activity.length, 0);
  fail = false;                              // restore: later tests in the file must write normally
});
```""", 1))
    done.append('review#4 03 snippet is now the real test with the renameSync injection, the /replacement failure/ matcher and the restore')
    banner = lambda which: f'> **Which app am I in?** {which}\n\n'
    fe.rw('astraupskill/02-CONCEPTS.md', lambda t: t if 'Which app am I in' in t else t.replace('\n\n', '\n\n' + banner('This chapter is about the **Practice Journal** (HTTP over loopback, `npm run practice`, tests in `practice-journal/test/`). The desktop settings store (Electron, `npm test`, mocked bridge) appears only where a section says so.'), 1))
    fe.rw('astraupskill/04-TESTING-AND-DEBUGGING.md', lambda t: t if 'Which app am I in' in t else t.replace('\n\n', '\n\n' + banner('Sections on HTTP, loopback and the journal use `npm run test:practice`; sections on the settings store and the mocked bridge use `npm test` (the Electron suites).'), 1))
    fe.rw('astraupskill/05-PRACTICE.md', lambda t: t if 'Which app am I in' in t else t.replace('\n\n', '\n\n' + banner('All six exercises target the **Practice Journal** in `practice-journal/`; none touch the Electron assistant.'), 1))
    done.append('review#5 "Which app am I in?" banners at the top of 02, 04 and 05')
    w('astraupskill/08-PORT-TO-A-FRAMEWORK.md', """# 08. Port three journal routes to a framework

[Course index](README.md)

The journal's `server.js` is hand-rolled `node:http`: routing by string matching, JSON parsing, content-type checks, and the interesting parts (revision check, writer lease, reference rules) all in one place. Porting three routes to Fastify with TypeScript and SQLite shows what a framework removes and what it does not.

## Schema (`practice-journal/port/schema.sql`)

```sql
CREATE TABLE workspaces (id TEXT PRIMARY KEY, owner TEXT NOT NULL, token_hash TEXT NOT NULL, revision INTEGER NOT NULL DEFAULT 0);
CREATE TABLE questions (id TEXT PRIMARY KEY, workspace_id TEXT NOT NULL REFERENCES workspaces(id), prompt TEXT NOT NULL CHECK (length(prompt) <= 2000), hint TEXT, created_at TEXT NOT NULL);
CREATE TABLE sessions  (id TEXT PRIMARY KEY, workspace_id TEXT NOT NULL REFERENCES workspaces(id), profile_id TEXT NOT NULL, state TEXT NOT NULL CHECK (state IN ('planned','active','closed')));
```

## Three routes (`practice-journal/port/app.ts`)

```ts
import Fastify from 'fastify';
import { DatabaseSync } from 'node:sqlite';
import { z } from 'zod';
import { payload, LIMITS } from '../src/domain.js';           // the same contracts module: validation is not the framework's job

const db = new DatabaseSync('journal.sqlite');
export const app = Fastify();

app.addHook('onRequest', async (req, reply) => {               // authenticate() from domain.js, as a hook
  const ws = db.prepare('SELECT id, token_hash FROM workspaces WHERE id = ?').get(String(req.headers['x-workspace'] ?? ''));
  if (!ws || !tokenMatches(req.headers.authorization, ws.token_hash)) return reply.code(401).send({ error: 'Unauthorized' });
  req.workspace = ws.id;
});

app.get('/questions', async (req) => db.prepare('SELECT * FROM questions WHERE workspace_id = ? ORDER BY created_at').all(req.workspace));

app.post('/questions', async (req, reply) => {
  const body = z.object({ expectedRevision: z.number().int(), question: z.unknown() }).parse(req.body);
  const record = payload('questions', body.question, true);    // throws the same messages the journal shows
  const tx = db.prepare('BEGIN IMMEDIATE'); tx.run();          // the writer lease becomes the write transaction
  try {
    const bumped = db.prepare('UPDATE workspaces SET revision = revision + 1 WHERE id = ? AND revision = ?').run(req.workspace, body.expectedRevision);
    if (bumped.changes === 0) { db.exec('ROLLBACK'); return reply.code(409).send({ error: 'Workspace changed elsewhere; reload before saving.' }); }
    db.prepare('INSERT INTO questions (id, workspace_id, prompt, hint, created_at) VALUES (?, ?, ?, ?, ?)').run(record.id, req.workspace, record.prompt, record.hint ?? null, record.createdAt);
    db.exec('COMMIT'); return reply.code(201).send({ ...record, revision: body.expectedRevision + 1 });
  } catch (e) { db.exec('ROLLBACK'); throw e; }
});

app.delete('/questions/:id', async (req, reply) => {
  const inUse = db.prepare('SELECT 1 FROM sessions s JOIN session_questions q ON q.session_id = s.id WHERE q.question_id = ? AND s.workspace_id = ? AND s.state <> ?').get(req.params.id, req.workspace, 'closed');
  if (inUse) return reply.code(409).send({ error: 'Question is referenced by an open session.' });   // references() rule, as SQL
  const gone = db.prepare('DELETE FROM questions WHERE id = ? AND workspace_id = ?').run(req.params.id, req.workspace);
  return reply.code(gone.changes ? 204 : 404).send();
});
```

## What the framework removed, and what it did not

| removed by Fastify | still yours |
|---|---|
| routing by method and path | which routes exist and what they refuse |
| body parsing and content-type negotiation (415 for non-JSON) | the shape (`payload()`), the limits, the messages |
| 404 for unknown routes, error serialization | the 409s: revision, references, lease |
| the listening server (`app.inject` in tests) | the transaction boundary and its ordering |

The revision check, the lease (now `BEGIN IMMEDIATE`), and the reference rules are domain concerns; no framework has an opinion about them. The port makes that visible: `domain.js` is imported unchanged.

## Exercise

Port `PUT /questions/:id` the same way (revision on the workspace, immutable fields from `IMMUTABLE` refused with 400), then run `practice-journal/test/practice.test.js` against a thin adapter over the SQLite version; the tests that still pass are the ones about rules, the ones that fail are about transport.
""")
    done.append('review#3 08-PORT-TO-A-FRAMEWORK.md: three Fastify + SQLite routes reusing domain.js, with the removed/still-yours table')
    finish(S, done)

# ---------------------------------------------------------------- buildsmallplates
S = 'buildsmallplates'
if not ONLY or S in ONLY:
    os.chdir(fe.REG[S]['abs']); done = []
    def aws(t):
        t = t.replace("""          onPress: () => {
            deleteWorkout(workout.id);
            navigation.goBack();
          },""", """          onPress: () => {
            if (!deleteWorkout(workout.id)) {
              Alert.alert('Already removed', 'This workout was already deleted; the list will refresh.');
            }
            navigation.goBack();
          },""", 1)
        t = t.replace("""                  onPress: () => {
                    deleteWorkout(workout.id);
                    navigation.goBack();
                  },""", """                  onPress: () => {
                    if (!deleteWorkout(workout.id)) {
                      Alert.alert('Already removed', 'This workout was already deleted; the list will refresh.');
                    }
                    navigation.goBack();
                  },""", 1)
        t = t.replace("""              onPress={() => {
                deleteSet(set.id);
                onClose();
              }}""", """              onPress={() => {
                // The repository reports whether a row changed; a false means another screen removed it first.
                if (!deleteSet(set.id)) {
                  Alert.alert('Already removed', 'This set was already removed; the workout will re-query.');
                }
                onClose();
              }}""", 1)
        return t
    fe.rw('src/screens/ActiveWorkoutScreen.tsx', aws)
    fe.rw('src/screens/WorkoutDetailScreen.tsx', lambda t: t.replace("""                onPress: () => {
                  deleteWorkout(workout.id);
                  navigation.goBack();
                },""", """                onPress: () => {
                  if (!deleteWorkout(workout.id)) {
                    Alert.alert('Already removed', 'This workout was already deleted; the list will refresh.');
                  }
                  navigation.goBack();
                },""", 1))
    assert rd('src/screens/ActiveWorkoutScreen.tsx').count("Alert.alert('Already removed'") == 3 and "Alert.alert('Already removed'" in rd('src/screens/WorkoutDetailScreen.tsx')
    fe.append_section(S, '05', '## Exercise 7: make `updateSet` honest in the UI', """The three delete call sites now branch on the repository's boolean (fix pass): `true` closes, `false` shows "already removed" and lets the screen re-query. `updateSet` returns the same boolean and the screen still ignores it (`ActiveWorkoutScreen.tsx`: the weight, reps and RPE handlers). Wire it: on `false`, show the stale message and re-query instead of leaving the control showing a value the database refused. Then justify, in one paragraph, why the repository must *not* own the copy (the text, the alert, the navigation): it knows whether a row changed, it does not know what screen you are on or what the user was doing; a repository that calls `Alert` cannot be tested with the mutation-contract suite. Acceptance: a test in `repos-mutations.test.ts` style proves `updateSet` returns `false` for a stale id without notifying; a screen-level test (or a manual trace in your notebook) shows the message and the re-query.""", before='## ')
    done.append('review#1 the three deleteWorkout/deleteSet call sites branch on the boolean (close on true, "already removed" alert on false); 05 exercise 7 asks the same for updateSet with the repository-must-not-own-the-copy argument')
    def repos(t):
        old = """  for (const [k, col] of Object.entries(mapping)) {
    if (k in fields) {
      const v = (fields as Record<string, unknown>)[k];
      if (v === undefined) continue;
      cols.push(`${col} = ?`);
      vals.push(typeof v === 'boolean' ? (v ? 1 : 0) : (v as string | number | null));
    }
  }
  if (cols.length === 0) return false;
  for (const [key, value] of Object.entries(fields)) {
    if (value === undefined) continue;
    if (value === null || key === 'note' || key === 'kind' || key === 'isFailure' || key === 'completedAt') continue;
    if (typeof value !== 'number') throw new Error(`${key} must be a number`);
    assertValidSetNumber(key as SetNumericField, value);
  }
"""
        new = """  // One pass over the mapping: validate as we bind, so the validated fields and the bound
  // columns are the same list by construction and cannot drift apart.
  const nonNumeric = new Set(['note', 'kind', 'isFailure', 'completedAt']);
  for (const [k, col] of Object.entries(mapping)) {
    if (!(k in fields)) continue;
    const v = (fields as Record<string, unknown>)[k];
    if (v === undefined) continue;
    if (v !== null && !nonNumeric.has(k)) {
      if (typeof v !== 'number') throw new Error(`${k} must be a number`);
      assertValidSetNumber(k as SetNumericField, v);
    }
    cols.push(`${col} = ?`);
    vals.push(typeof v === 'boolean' ? (v ? 1 : 0) : (v as string | number | null));
  }
  if (cols.length === 0) return false;
"""
        assert old in t, 'updateSet loops not found'
        return t.replace(old, new, 1)
    fe.rw('src/db/repos.ts', repos)
    def mtest(t):
        if 'field outside the mapping' in t: return t
        add = """
  it('ignores a field outside the mapping instead of validating it as a number', () => {
    // Validation and binding are one pass over the column mapping: an unknown, non-numeric field is
    // neither bound nor validated, so it cannot throw "must be a number" for a column that is never written.
    const result = updateSet('set-1', { actualReps: 5, ...( { nickname: 'heavy day' } as unknown as Record<string, never>) });
    expect(result).toBe(true);
    const sql = runSync.mock.calls.at(-1)?.[0] as string;
    expect(sql).toContain('actual_reps = ?');
    expect(sql).not.toContain('nickname');
  });
"""
        idx = t.rstrip().rfind('});')
        return t[:idx] + add.lstrip('\n') + t[idx:]
    fe.rw('src/db/__tests__/repos-mutations.test.ts', mtest)
    done.append('review#2 updateSet validates while it binds in one pass over the mapping; regression test: a field outside the mapping is neither validated nor bound')
    def reorder(path):
        t, crlf, bom = fe.read(path)
        parts = t.split('\n\n')
        if len(parts) >= 3 and parts[0].startswith('# ') and not parts[1].startswith('#') and not parts[2].startswith('#'):
            parts[1], parts[2] = parts[2], parts[1]
            # the drill paragraph goes last, after everything else
            drill = parts.pop(2)
            parts.append(drill)
            fe.write(path, '\n\n'.join(parts), crlf, bom); return True
        return False
    moved = [f for f in ['README', '01', '04', '07'] if reorder(fe.chapter(S, f))]
    done.append(f'review#3 orienting paragraph first, drill/summary paragraph last in {", ".join(moved)}')
    fe.rw('astraupskill/04-TESTING-AND-DEBUGGING.md', lambda t: re.sub(r'[^.\n]*Root(?: observed|\'s successful)[^.\n]*\.\s*', '', t))
    fe.rw('astraupskill/04-TESTING-AND-DEBUGGING.md', lambda t: t if 'locked `npm ci` of 544 packages' in t else t.replace('Do not confuse a test runner starting with tests passing.', 'The verified run used a locked `npm ci` of 544 packages; see VERIFICATION.md. Do not confuse a test runner starting with tests passing.', 1))
    done.append('review#4 the "Root observed / Root\'s successful locked install" sentences are gone; 04 states the locked install plainly')
    fe.rw('astraupskill/VERIFICATION.md', lambda t: t.replace('npm test -- --maxWorkers=1 --testTimeout=30000', 'npx vitest run --maxWorkers=1 --testTimeout=30000   # what package.json\'s "test" runs, with the recorded bounds', 1).replace('The recorded test command directly invoked the installed Vitest CLI with those worker/time bounds and a JSON reporter. It passed all 92 cases with zero failures and zero pending cases', 'The recorded run invoked the installed Vitest CLI with those worker/time bounds and a JSON reporter. It passed all 92 cases with zero failures and zero skipped cases', 1))
    done.append('review#6 VERIFICATION reproduce block uses the vitest command that package.json runs; Jest phrasing dropped')
    w('astraupskill/08-WEB-TRANSLATION.md', """# 08. The same change as a web handler

[Course index](README.md)

`updateSet` returns `true` when one row changed and `false` when none did; validation throws before SQL; a completed workout refuses edits. On an Express + Prisma server the same contract is a `PATCH /sets/:id` with four status codes.

```ts
import { Router } from 'express';
import { z } from 'zod';
import { Prisma, PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
const patchSet = z.object({
  actualWeightKg: z.number().min(0).max(1000).nullable().optional(),
  actualReps: z.number().int().min(0).max(1000).nullable().optional(),
  rpe: z.number().min(1).max(10).nullable().optional(),
  isFailure: z.boolean().optional(),
  completedAt: z.number().int().nullable().optional(),
  note: z.string().max(500).nullable().optional(),
}).strict().refine((v) => Object.values(v).some((x) => x !== undefined), { message: 'At least one field is required.' });

export const sets = Router();
sets.patch('/sets/:id', async (req, res) => {
  const parsed = patchSet.safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ error: parsed.error.issues[0].message });      // assertValidSetNumber, as a schema
  const set = await prisma.setEntry.findUnique({ where: { id: req.params.id }, select: { workout: { select: { finishedAt: true } } } });
  if (set?.workout.finishedAt) return res.status(409).json({ error: 'This workout is completed; sets are read-only.' });
  const result = await prisma.setEntry.updateMany({ where: { id: req.params.id, workout: { finishedAt: null } }, data: parsed.data });
  if (result.count === 0) return res.status(404).json({ error: 'Set not found (it may have been removed).' });   // changes === 0 -> false -> 404
  res.status(200).json(await prisma.setEntry.findUniqueOrThrow({ where: { id: req.params.id } }));               // changes === 1 -> true -> 200
});
```

| app (`repos.ts`) | server |
|---|---|
| throws before SQL on an invalid number | 400 from the Zod schema, no query |
| `changes === 1` returns `true`, listeners notified | 200 with the row; the client re-renders from the response |
| `changes === 0` returns `false`, no notification | 404; the client shows "already removed" and re-queries (exactly what the screens do after the fix pass) |
| the completed-workout guard | 409, and the `finishedAt: null` predicate inside `updateMany` so the check and the write are one statement |

The `updateMany` with the workout predicate is the server's version of "the repository decides, the screen reacts": the UI cannot skip it, and two clients racing to edit a set on a workout being completed get one 200 and one 409, never a stale write.

## Exercise

Write the four supertest cases (400, 404, 409, 200) and then the `DELETE /sets/:id` that mirrors `deleteSet`'s boolean as 204/404.
""")
    done.append('review#5 08-WEB-TRANSLATION.md: PATCH /sets/:id with 200/404/400/409 mapped onto the boolean contract')
    finish(S, done)

# ---------------------------------------------------------------- astra4-2
S = 'astra4-2'
if not ONLY or S in ONLY:
    os.chdir(fe.REG[S]['abs']); done = []
    if not os.path.isdir('service'):
        w('service/package.json', json.dumps({"name": "interlude-service", "private": True, "type": "module", "description": "Starter for 05-PRACTICE items 4-5: reminders behind HTTP + SQLite with per-row versions. Zero dependencies (node:http, node:sqlite).", "scripts": {"start": "node server.js", "test": "node --test test/"}, "engines": {"node": ">=22.5"}}, indent=2) + '\n')
        w('service/schema.sql', """CREATE TABLE IF NOT EXISTS reminders (
  id         TEXT PRIMARY KEY,
  owner      TEXT NOT NULL,
  title      TEXT NOT NULL CHECK (length(title) BETWEEN 1 AND 80),
  message    TEXT NOT NULL CHECK (length(message) <= 500),
  version    INTEGER NOT NULL DEFAULT 1,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS reminders_owner ON reminders (owner, updated_at);
""")
        w('service/server.js', """import { createServer } from 'node:http';
import { readFileSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';

// Starter for practice items 4-5. Same rules as extension/model.js applyMessage: a saved message
// carries an expectedRevision; here every row has its own version and PUT carries it in If-Match.
export function createApp(dbPath = ':memory:') {
  const db = new DatabaseSync(dbPath);
  db.exec(readFileSync(new URL('./schema.sql', import.meta.url), 'utf8'));
  const owner = (req) => String(req.headers['x-owner'] ?? '').trim();   // practice item 5 replaces this with a session
  const json = (res, status, body, headers = {}) => { res.writeHead(status, { 'content-type': 'application/json', ...headers }); res.end(JSON.stringify(body)); };
  const body = (req) => new Promise((resolve, reject) => { let raw = ''; req.on('data', (c) => { raw += c; if (raw.length > 64_000) reject(new Error('too large')); }); req.on('end', () => { try { resolve(raw ? JSON.parse(raw) : {}); } catch { reject(new Error('bad json')); } }); });
  const valid = (r) => typeof r.title === 'string' && r.title.trim().length >= 1 && r.title.length <= 80 && typeof r.message === 'string' && r.message.length <= 500;

  return createServer(async (req, res) => {
    const who = owner(req); if (!who) return json(res, 401, { error: 'x-owner required' });
    const url = new URL(req.url, 'http://localhost'); const m = /^\\/reminders(?:\\/([^/]+))?$/.exec(url.pathname);
    if (!m) return json(res, 404, { error: 'not found' });
    try {
      if (req.method === 'GET' && !m[1]) return json(res, 200, db.prepare('SELECT * FROM reminders WHERE owner = ? ORDER BY updated_at DESC').all(who));
      if (req.method === 'GET') { const row = db.prepare('SELECT * FROM reminders WHERE id = ? AND owner = ?').get(m[1], who); return row ? json(res, 200, row, { etag: `"${row.version}"` }) : json(res, 404, { error: 'not found' }); }
      if (req.method === 'POST' && !m[1]) {
        const r = await body(req); if (!valid(r)) return json(res, 400, { error: 'title 1-80 chars, message up to 500' });
        const row = { id: randomUUID(), owner: who, title: r.title.trim(), message: r.message, version: 1, updated_at: new Date().toISOString() };
        db.prepare('INSERT INTO reminders (id, owner, title, message, version, updated_at) VALUES (?, ?, ?, ?, ?, ?)').run(row.id, row.owner, row.title, row.message, 1, row.updated_at);
        return json(res, 201, row, { etag: '"1"' });
      }
      if (req.method === 'PUT' && m[1]) {
        const match = /^"(\\d+)"$/.exec(req.headers['if-match'] ?? ''); if (!match) return json(res, 428, { error: 'If-Match with the version you loaded is required' });
        const r = await body(req); if (!valid(r)) return json(res, 400, { error: 'title 1-80 chars, message up to 500' });
        const expected = Number(match[1]);
        const result = db.prepare('UPDATE reminders SET title = ?, message = ?, version = version + 1, updated_at = ? WHERE id = ? AND owner = ? AND version = ?').run(r.title.trim(), r.message, new Date().toISOString(), m[1], who, expected);
        if (result.changes === 0) return db.prepare('SELECT 1 FROM reminders WHERE id = ? AND owner = ?').get(m[1], who) ? json(res, 409, { error: 'Changed elsewhere. Reopen this view before saving; your draft is preserved.' }) : json(res, 404, { error: 'not found' });
        return json(res, 200, db.prepare('SELECT * FROM reminders WHERE id = ?').get(m[1]), { etag: `"${expected + 1}"` });
      }
      if (req.method === 'DELETE' && m[1]) { const r = db.prepare('DELETE FROM reminders WHERE id = ? AND owner = ?').run(m[1], who); res.writeHead(r.changes ? 204 : 404); return res.end(); }
      return json(res, 405, { error: 'method not allowed' });
    } catch (error) { return json(res, error.message === 'bad json' || error.message === 'too large' ? 400 : 500, { error: error.message }); }
  });
}

if (process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\\\/g, '/'))) {
  const port = Number(process.env.PORT ?? 4320);
  createApp(process.env.REMINDERS_DB ?? 'reminders.sqlite').listen(port, '127.0.0.1', () => console.log(`reminders service on http://127.0.0.1:${port}`));
}
""")
        w('service/test/reminders.test.js', """import test from 'node:test';
import assert from 'node:assert/strict';
import { createApp } from '../server.js';

async function withServer(fn) {
  const server = createApp(':memory:');
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${server.address().port}`;
  const call = (method, path, { body, headers = {} } = {}) => fetch(base + path, { method, headers: { 'content-type': 'application/json', 'x-owner': 'ada', ...headers }, body: body === undefined ? undefined : JSON.stringify(body) });
  try { await fn(call); } finally { server.close(); }
}

test('two competing PUTs: the loser gets 409 and the winner\\'s text stays', async () => {
  await withServer(async (call) => {
    const created = await (await call('POST', '/reminders', { body: { title: 'Stretch', message: 'Stand up' } })).json();
    const a = call('PUT', `/reminders/${created.id}`, { body: { title: 'Stretch', message: 'From tab A' }, headers: { 'if-match': '"1"' } });
    const b = call('PUT', `/reminders/${created.id}`, { body: { title: 'Stretch', message: 'From tab B' }, headers: { 'if-match': '"1"' } });
    const [ra, rb] = await Promise.all([a, b]);
    const statuses = [ra.status, rb.status].sort();
    assert.deepEqual(statuses, [200, 409]);
    const row = await (await call('GET', `/reminders/${created.id}`)).json();
    assert.equal(row.version, 2);
    const winner = ra.status === 200 ? 'From tab A' : 'From tab B';
    assert.equal(row.message, winner);
  });
});

test('validation and preconditions: 400 on a long title, 428 without If-Match, 404 for another owner', async () => {
  await withServer(async (call) => {
    assert.equal((await call('POST', '/reminders', { body: { title: 'x'.repeat(81), message: '' } })).status, 400);
    const created = await (await call('POST', '/reminders', { body: { title: 'Water', message: 'Drink' } })).json();
    assert.equal((await call('PUT', `/reminders/${created.id}`, { body: { title: 'Water', message: 'Drink more' } })).status, 428);
    assert.equal((await call('GET', `/reminders/${created.id}`, { headers: { 'x-owner': 'grace' } })).status, 404);
  });
});
""")
        w('astraupskill/08-SERVER-PORT.md', """# 08. Server port: reminders behind HTTP and SQLite

[Course index](README.md) · carries practice items 4 and 5 from proposal to scaffold

`service/` is a zero-dependency starter (`node:http`, `node:sqlite`, Node 22.5+): `service/server.js`, `service/schema.sql`, and `service/test/reminders.test.js`. Run it:

```powershell
cd service
npm test        # two node:test cases, in-memory database
npm start       # http://127.0.0.1:4320, file reminders.sqlite
```

## What maps to what

| extension (`applyMessage` in `extension/model.js`) | service |
|---|---|
| one `revision` for the whole snapshot; `expectedRevision` on every write | one `version` per row; `If-Match: "<version>"` on `PUT` |
| "Settings or saved messages changed elsewhere. Reopen this view before saving; your draft is preserved." | 409 with the same sentence; the client keeps its draft |
| `plain(message, keys)` refusing unknown keys | the `valid()` check, `CHECK (length(title) BETWEEN 1 AND 80)` in the schema as the last line of defense |
| the popup is the only writer, so a lease is unnecessary | SQLite's write transaction serializes the two competing `PUT`s in the reference test |
| `chrome.storage` quota failure keeps the draft | 400 for an oversized body; nothing written |

## The reference test

`two competing PUTs` fires two updates with the same `If-Match: "1"` at once and asserts exactly one 200 and one 409, `version` 2, and the winner's text on the row. It is the server-side form of the browser scenario "stale saved-message edit conflicts instead of replacing a newer revision".

## Practice item 5, from here

`x-owner` is a stand-in. Replace it with a session (a `sessions` table and a cookie), make `owner` come from the session, and keep every `WHERE ... AND owner = ?`; then add a background job boundary (a `jobs` table written in the same transaction as the reminder, drained by a worker) and the test that a job is never visible before its reminder is.
""")
        fe.rw('astraupskill/README.md', lambda t: t.rstrip('\n') + '\n\nChapter 08, [08-SERVER-PORT.md](08-SERVER-PORT.md), scaffolds practice items 4-5 as a runnable `service/` (HTTP + SQLite, per-row versions, a competing-PUT test).\n')
        done.append('review#1 08-SERVER-PORT.md + service/ starter (node:http + node:sqlite server, schema with version and title CHECK, two node:test cases incl. competing PUTs -> one 200 one 409)')
    fe.append_section(S, '01', '## Reading the dense style', """The repository is written in a deliberately compressed style: several statements per line, short names, handlers built inline. You are not missing a build step or a formatter; the delivered source looks like this on purpose to stay small. When a block is hard to follow, paste it into Prettier (or read this expansion of `renderPresets` in `src/app.js`):

```js
function renderPresets() {
  $('#preset-list').replaceChildren();
  for (const preset of presets) {
    const card = document.createElement('article');
    card.className = 'preset-card';
    const heading = document.createElement('h3');
    heading.textContent = preset.title;
    const text = document.createElement('p');
    text.textContent = preset.message;
    const actions = document.createElement('div');
    actions.className = 'preset-actions';
    const button = (label, handler) => {
      const node = document.createElement('button');
      node.type = 'button';
      node.className = 'secondary';
      node.textContent = label;
      node.addEventListener('click', handler);
      return node;
    };
    actions.append(
      button(`Use ${preset.title}`, () => {
        messageRevision = revision;
        $('#message-input').value = preset.message;
        updateMessagePreview();
        toast('Message copied into your draft. Save message to apply it.');
      }),
      // ... edit and delete buttons follow the same shape; delete sends
      // { type: 'preset', action: 'delete', id, expectedRevision: revision } and re-renders on success
    );
    card.append(heading, text, actions);
    $('#preset-list').append(card);
  }
}
```

The behavior is unchanged by the layout; only the reading cost is.""", before='## ')
    done.append('review#2 01 "Reading the dense style" with a prettified renderPresets excerpt and the statement that the compression is deliberate')
    fe.rw('astraupskill/04-TESTING-AND-DEBUGGING.md', lambda t: t if 'grep-invert' in t else t.replace('Use `npm.cmd run test:browser` for ten Chromium scenarios after building.', 'Use `npm.cmd run test:browser` for ten Chromium scenarios after building. The tenth scenario, `unpacked extension persists CRUD and reconciles real alarms and break windows`, loads the built extension into a real Chromium and needs a Chromium **channel** (Playwright\'s bundled Chromium or Chrome with `--load-extension` support); on a machine without it, run `npx.cmd playwright test --grep-invert "unpacked extension"` and read a 9/10 pass as "every page-level behavior verified, the real-alarm reconciliation not verified here".', 1))
    titles = re.findall(r"^test\('([^']+)'", rd('tests/browser/interlude.spec.js'), re.M)
    guards = {
        'timer settings and literal reminder persist across reload': 'settings CRUD survives a reload; the literal reminder is not templated',
        'saved messages create update use and delete without removing the active reminder': 'preset CRUD is independent of the active reminder',
        'stale reminder form keeps its proposal after another tab saves': 'the revision check refuses a stale save and keeps the draft',
        'stale saved-message edit conflicts instead of replacing a newer revision': 'per-preset stale edits conflict (the 409 of the server port)',
        'preview quota failure preserves active data and the reminder draft': 'a storage quota error loses nothing',
        'corrupt preview data can be exported and requires explicit reset': 'corrupt data is exportable and never silently reset',
        'expired preview deadline transitions once and snooze retains the completed count': 'timer transitions are idempotent; snooze keeps counters',
        'art selection upload and removal retain the existing image workflow': 'the image workflow regression guard',
        'dashboard and message library fit desktop and narrow layouts': 'responsive layout',
        'unpacked extension persists CRUD and reconciles real alarms and break windows': 'real chrome.alarms and windows reconcile with stored state',
    }
    table = '\n'.join(f'| {i + 1} | {t} | {guards.get(t, "see the spec")} |' for i, t in enumerate(titles))
    fe.append_section(S, 'VERIFICATION', '## The ten browser scenarios and what each guards', f"""| # | scenario (`tests/browser/interlude.spec.js`) | guards |
|---|---|---|
{table}

If you break something, the scenario in the right column is the one that should turn red; if it does not, that is a coverage gap worth a test.""", before='## ')
    done.append('review#3 04 documents the Chromium-channel prerequisite and the --grep-invert fallback with what 9/10 means; review#5 VERIFICATION maps the ten scenarios to the behavior each guards')
    fe.append_section(S, '02', '## Predict: what does `applyMessage` return or throw?', """Write your answer before running `node --test tests/model.test.js`. Answers are in [06](06-SOLUTIONS-AND-REVIEW.md#predictions-from-02-and-03).

1. `applyMessage(snapshot, { type: 'read' })` when `snapshot` is `undefined`.
2. `applyMessage(snapshot, { type: 'settings', settings: {}, expectedRevision: snapshot.revision })`.
3. `applyMessage(snapshot, { type: 'preset', action: 'update', id, preset, expectedRevision: snapshot.revision - 1 })`.""", before='## ')
    fe.append_section(S, '03', '## Predict: the stale form', """Before reading on: tab A and tab B both load revision 7. Tab A saves settings (revision becomes 8). Tab B, still showing 7, submits its form. (a) What does `applyMessage` throw? (b) What happens to tab B's typed text? (c) What must tab B do before its save can succeed? Answers in [06](06-SOLUTIONS-AND-REVIEW.md#predictions-from-02-and-03).""", before='## ')
    fe.append_section(S, '06', '## Predictions from 02 and 03', """**02.1** Returns the normalized default snapshot: `normalize(undefined)` fills defaults, and a `read` returns `current` without writing. **02.2** Throws `Settings patch is empty.`: the revision matches, but `plain()` accepts the empty object and the explicit emptiness check refuses it, so nothing changes. **02.3** Throws `Settings or saved messages changed elsewhere. Reopen this view before saving; your draft is preserved.`: the `expectedRevision` check runs before the action is even looked at.

**03 (a)** The same "changed elsewhere" error, because tab B's `expectedRevision` is 7 and the stored revision is 8. **(b)** Nothing: the error is thrown before any write and the form is not cleared; the popup shows the message next to the form. **(c)** Reopen (re-read the snapshot, which sets `presetRevision`/`messageRevision` to 8) and resubmit; the text it typed is still in the inputs.""", before='## ')
    done.append('review#4 three explicit predict boxes (02: applyMessage returns/throws; 03: the stale form) with answers in 06')
    finish(S, done)
