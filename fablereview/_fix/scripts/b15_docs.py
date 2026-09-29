import sys, json, os, re, glob, datetime
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
HERE = os.path.dirname(__file__)
TODAY = '2026-09-18'
def rd(p): return open(p, encoding='utf-8-sig').read()
def w(p, s): open(p, 'w', encoding='utf-8', newline='\n').write(s)
def finish(S, done):
    json.dump(done, open(os.path.join(HERE, S + '.done.json'), 'w')); print(f'== {S}\n' + '\n'.join(done))
def count_tests(root):
    fns = par = 0
    for f in glob.glob(os.path.join(root, '**', 'test_*.py'), recursive=True):
        t = rd(f); fns += len(re.findall(r'^\s*(?:async )?def test_', t, re.M)); par += t.count('parametrize(')
    return fns, par

# ---------------------------------------------------------------- e15
S = 'e15'; os.chdir(fe.REG[S]['abs']); done = []
fns, par = count_tests('tests')
w('astraupskill/08-TRANSLATION.md', f"""# 08. Translation: the same mechanisms in JS/TS and C#/.NET

[Course index](README.md)

This project is Python (FastAPI + SQLAlchemy). Every mechanism it teaches has a direct equivalent on the stacks you are training for. Read this after chapter 03 and keep it open during the practice exercises.

| here (Python) | Express / Prisma (TypeScript) | ASP.NET Core / EF Core (C#) |
|---|---|---|
| `check_expected_version` (`app/main.py:168`): missing `If-Match` is 428, mismatch is 409 | a middleware that reads `req.header("if-match")`, answers 428 when absent, and passes the parsed version to the service; the service's `updateMany({{ where: {{ id, version }} }})` returning `count: 0` is the 409 | an action filter or `[FromHeader(Name = "If-Match")] string? ifMatch` on the action; `Results.StatusCode(428)` when absent; the concurrency token check below produces the 409 |
| `Versioned` mixin (`app/models.py:21`): a `version` column bumped on every update | `version Int @default(1)` in the Prisma schema, incremented in the same conditional `updateMany` (`data: {{ ..., version: {{ increment: 1 }} }}`) | `[Timestamp] public byte[] RowVersion` (SQL Server) or `[ConcurrencyCheck] public int Version`; EF throws `DbUpdateConcurrencyException`, which you map to 409 |
| `build_ticket_filters` (`app/services.py:861`): one filter object reused for the count and the page | one `where` object passed to both `prisma.ticket.count({{ where }})` and `prisma.ticket.findMany({{ where, skip, take }})`, ideally inside one transaction so total and rows agree | one `IQueryable<Ticket>` built once, then `.CountAsync()` and `.Skip().Take().ToListAsync()` from the same query |
| `app/static/app.js` sequence invalidation (`detailSequence`, `listSequence`): a late response for an old request is ignored | the identical race in a React `useEffect`: keep a `let cancelled = false` flag (or an `AbortController`) and ignore the response after cleanup | the same idea in Blazor with a `CancellationTokenSource` per navigation |
| Pydantic request models rejecting unknown fields | Zod `.strict()` at the route; the service receives the parsed type, never `req.body` | explicit DTO classes bound by the model binder; unknown JSON members are ignored unless you enable `UnmappedMemberHandling.Disallow` |
| SQLAlchemy session as the unit of work | `prisma.$transaction(async (tx) => ...)`: every write of one operation through `tx` | `DbContext.Database.BeginTransactionAsync()` or one `SaveChangesAsync()` for all tracked changes |

## What does not translate

FastAPI dependency injection of the current user has no one-to-one Express equivalent; the closest is a middleware that sets `req.user` and route-level guards. Alembic migrations map to `prisma migrate` and EF Core migrations, with one difference worth remembering: Prisma will not run data migrations for you, so a "preserve existing rows" step (chapter 03) is a hand-written SQL migration on that stack.

## Exercise

Take the rejected-update walkthrough in chapter 03 and write it as an Express route with Zod plus Prisma, then as an ASP.NET minimal API with EF Core. Both versions must answer 428, 409 and 200 for the same three requests. Compare the line count of the version check in each; the check should be one conditional write, never a read-then-compare.
""")
verif = rd('astraupskill/VERIFICATION.md')
fe.rw('astraupskill/VERIFICATION.md', lambda t: t.replace('156 backend tests,', f'156 backend tests (collected cases: {fns} test functions under `tests/` expanding through {par} `parametrize` decorators; check with `pytest --collect-only -q | tail -1`),', 1))
done.append(f'review#2 VERIFICATION restates the backend number as {fns} test functions expanding to 156 collected cases ({par} parametrize decorators), measured from tests/')
fe.rw('astraupskill/03-WORKED-CHANGE.md', lambda t: t.replace('## Follow the rejected update\n', '## Follow the rejected update\n\n![The conflict review the second tab sees after the first tab saved](images/03-conflict-review.png)\n\n', 1).replace('## Reproduce the problem with a disposable customer\n', '## Reproduce the problem with a disposable customer\n\n![The customer editor used for the disposable record and the hostile-text check](images/02-customer-editor.png)\n\n', 1))
done.append('review#3 03 embeds 03-conflict-review.png under "Follow the rejected update" and 02-customer-editor.png under the reproduce section')
fe.append_section(S, 'README', '## Prerequisites and pacing', """**Prerequisites:** Python 3.13 with a virtual environment (`python -m venv .venv`, then install from `requirements.lock`), basic SQL, and the HTTP status codes 409/412/428.

**Pacing:** map + concepts about 2 h; the worked change about 3 h with the app running; one evening per practice exercise; the trace lab 1 h. **Optional depth:** the business-calendar and SLA material (calendar arithmetic, timers) is not needed for the CRUD core; skip it on a first pass and return after practice exercise 2.

**Not your stack?** Read [08-TRANSLATION.md](08-TRANSLATION.md) after chapter 03: it maps every mechanism here to Express/Prisma and ASP.NET/EF Core.""", before='## A practical learning route')
done.append('review#1 08-TRANSLATION.md (six-row mechanism table, what does not translate, exercise); review#4 README prerequisites, pacing, optional SLA depth')
finish(S, done)

# ---------------------------------------------------------------- grokbuildppmproject (already applied on disk; verify)
S = 'grokbuildppmproject'; os.chdir(fe.REG[S]['abs']); done = []
checks = [('review#1 README says taskController was deliberately not changed', 'deliberately **not** changed' in rd('astraupskill/README.md')),
          ('review#2 05 opens with the workspace note', 'Set up a workspace first' in rd('astraupskill/05-PRACTICE.md')),
          ('review#3 02 has the Express 4 rejected-async-handler section', 'rejected async handler vanishes' in rd('astraupskill/02-CONCEPTS.md')),
          ('review#4 05 exercise 8 proves one claim against a real database', 'against a real database' in rd('astraupskill/05-PRACTICE.md'))]
for label, ok in checks:
    assert ok, label
    done.append(label + ' (present on disk before this pass; verified)')
finish(S, done)

# ---------------------------------------------------------------- grokbuildteamproject
S = 'grokbuildteamproject'; os.chdir(fe.REG[S]['abs']); done = []
fe.rw('astraupskill/03-WORKED-CHANGE.md', lambda t: t.replace('The repository finds the task with its task ID, project ID, and selected organization ID.', 'The repository ([projectRepository.ts](../backend/src/repositories/projectRepository.ts)) finds the task with its task ID, project ID, and selected organization ID. Note that `backend/src/repositories/taskRepository.ts` and `backend/src/services/taskService.ts` are deliberate nine-line re-export shims; the transaction you are looking for lives in `projectRepository.ts`.', 1))
done.append('review#1 03 section 2 links projectRepository.ts by name and warns that taskRepository.ts/taskService.ts are re-export shims')
msg403 = 'You are not a member of that organization.'
m = re.search(r'403,\s*"([^"]+)"', rd('backend/src/middleware/tenantContext.ts'))
if m: msg403 = m.group(1)
fe.append_section(S, '02', '## One forged request, traced end to end', f"""| step | value | what happens |
|---|---|---|
| token subject | `demo_member` (a Cedar member) | `authenticate` verifies the signature and sets `req.userId` |
| header | `x-org-id: maple` (an organization the caller does not belong to) | `attachTenantContext` parses the header as an identifier |
| membership lookup | `organizationMember.findUnique({{ userId: "demo_member", organizationId: "maple" }})` | returns `null`: no row |
| decision | 403 `{msg403}` | thrown before any project or task query runs |
| Maple data touched | none | the only query was the membership lookup, keyed by the caller |

Change one thing at a time and predict again: no header at all (400 before the membership lookup); a valid Maple member with a Cedar task id in the path (404, because the repository's `where` carries `organizationId` and the row is invisible); a Cedar member who was removed from Cedar an hour ago (403, because the membership row is gone even though the token is still valid). Selection is not authorization: the header selects, the membership row authorizes.""", before='## Record identity')
done.append('review#3 02 traces one forged request (demo_member + x-org-id: maple) end to end in a table with three variations')
fe.append_section(S, 'README', '## Prerequisites and pacing', """**Prerequisites:** React state and effects, `fetch` with headers, basic SQL, what a foreign key and a compound foreign key are.

**Pacing:** map + concepts about 2 h, the worked change about 3 h with the app running, one evening per practice exercise, the trace lab 1 h.""", before='## A practical learning sequence')
done.append('review#2 README prerequisites and pacing')
ver = rd('astraupskill/VERIFICATION.md')
if 'docker' not in ver.lower():
    fe.append_section(S, 'VERIFICATION', '## The Docker path is unverified', """`docker-compose.yml` was not exercised in the recorded run or in the fix pass. The verified path is `npm run setup:local` followed by the local PostgreSQL steps in the root README. Treat `docker compose up -d postgres` as untested until you have run it once and recorded the result here.""", before='## Boundaries not claimed')
fe.rw('README.md', lambda t: t.replace('docker compose up -d postgres\n', 'docker compose up -d postgres   # unverified path: prefer npm run setup:local (see astraupskill/VERIFICATION.md)\n', 1))
done.append('review#4 root README marks the Docker path unverified and VERIFICATION says so explicitly')
finish(S, done)

# ---------------------------------------------------------------- buildgum
S = 'buildgum'; os.chdir(fe.REG[S]['abs']); done = []
compiles = '.verification' in rd('scripts/test.mjs') if os.path.exists('scripts/test.mjs') else False
fe.rw('astraupskill/03-WORKED-CHANGE.md', lambda t: t.replace('## Step 5: explain the remaining gap', """### The three outcomes of one checkout

| outcome | what storage holds | what the user sees | what `replay()` does on retry with the same `requestKey` |
|---|---|---|---|
| write rejected (validation, budget, stale baseline) | nothing new | the error; the draft is kept | nothing to replay: the retry is a first attempt again |
| write succeeded, response delivered | one order + one receipt | the receipt | returns the stored receipt, creates nothing |
| write succeeded, acknowledgement lost (tab closed, storage event missed) | one order + one receipt | nothing, or a spinner that died | finds the receipt by key and returns it: the user sees the order they already have, not a second one |

The third row is the one that matters: the client cannot tell "rejected" from "acknowledgement lost" by itself, so the retry must be safe under both. The `requestKey` is what makes it safe. A retry with a *new* key after a lost acknowledgement creates a second order, which is why the key is generated when the attempt is frozen (Step 2), not when the button is pressed.

## Step 5: explain the remaining gap""", 1))
done.append('review#1 03 Step 4 gains a three-outcome table (rejected / delivered / acknowledgement lost) with what replay() does')
fe.append_section(S, '02', '## What this becomes on a server', """`requestKey` becomes an `Idempotency-Key` header, and the receipt becomes a row in an idempotency table with a unique index on `(customerId, key)`, written in the same database transaction as the order; a replay reads that row and returns the stored response. The raw-baseline compare becomes `If-Match` with an ETag, or a `version` column with a conditional `UPDATE ... WHERE id = ? AND version = ?` whose row count is the answer. `navigator.locks` becomes the database transaction (and, for cross-process serialization, an advisory lock keyed by the customer and key). The `encode()` bounds become a request-size limit at the server plus schema validation at the route (Zod `.strict()`, or a DTO in ASP.NET). Everything this course does in one tab against storage, a Node or .NET service does across a network against PostgreSQL; the invariants are the same, only the boundary moves.""", before='## Receipts preserve')
done.append('review#2 02 "What this becomes on a server" (Idempotency-Key + table, If-Match/version, transaction, size limits + schema)')
fe.append_section(S, 'README', '## Toolchain and setup', f"""```powershell
node --version                       # 22.x
npm ci
npm run dev                          # Vite
npm test                             # {'compiles the tests into .verification/ first, then runs node --test; ' if compiles else ''}running node --test test/model.cjs alone will not work
npm run build
python -m pip install playwright==1.59.0   # optional browser verifier
python -m playwright install chromium
python scripts/verify_browser.py           # needs port 5180 free; see 04
```""", before='## Start and observe')
fe.rw('astraupskill/README.md', lambda t: t.replace('Budget several focused sessions. A useful junior milestone is implementing a validated field and proving it survives reload. A useful mid-level milestone is explaining what happens when two clients write at once, a response is uncertain, or an imported backup is older than an open editor.', 'Budget four sessions of about two hours. **Junior milestone:** add a validated `supportUrl` field to the catalog item, prove it survives export and import, and show the test that rejects a `javascript:` URL. **Mid-level milestone:** explain, with the receipt table open, why a retried checkout with the same `requestKey` returns one receipt while a retry with a new key returns two, and which of the two a user who lost the acknowledgement actually wants.', 1))
done.append('review#3 README toolchain block incl. the Python/Playwright steps and the .verification note; review#4 generic framing replaced with buildgum-specific junior and mid-level milestones')
finish(S, done)

# ---------------------------------------------------------------- jsprojectlearn
S = 'jsprojectlearn'; os.chdir(fe.REG[S]['abs']); done = []
def cnt(path, pat): return len(re.findall(pat, rd(path), re.M)) if os.path.exists(path) else 0
e_it, s_it, s_each, l_test = cnt('src/game/engine.test.ts', r'^\s*it\('), cnt('src/game/storage.test.ts', r'^\s*it\('), cnt('src/game/storage.test.ts', r'it\.each'), cnt('tests/learning.spec.ts', r'^\s*test\(')
fe.append_section(S, 'README', '## Setup, in one block', """```powershell
node --version                    # 22.x
npm ci
npx playwright install chromium   # only for the browser suite
npm test                          # vitest, src/**
npm run build
npm run verify:content
npm run test:browser              # playwright, tests/
```""", before='## Suggested learning sequence')
done.append('review#1 README setup block: Node 22, npm ci, playwright install, the four commands')
fe.append_section(S, 'VERIFICATION', '## What was counted, and when', f"""As of {TODAY} (fix pass), counted from the tree: `src/game/engine.test.ts` has {e_it} `it(` cases; `src/game/storage.test.ts` has {s_it} `it(` cases plus {s_each} `it.each` blocks that expand at run time; `tests/learning.spec.ts` has {l_test} `test(` scenarios. Vitest and Playwright report expanded counts, so a rerun shows more cases than these literal counts; if your numbers differ from the "Executed result" section, re-count with `grep -c "^\\s*it(" src/game/*.test.ts` before assuming drift.""", before='## Executed result')
done.append(f'review#2 VERIFICATION stamped {TODAY} with literal per-file counts ({e_it}/{s_it}+{s_each} it.each/{l_test})')
fe.append_section(S, '02', '## The server-side analogue of each local mechanism', """This is the one on-stack project in its batch, so name the bridge explicitly. The `revision` compare-and-swap in `storage.ts` is `If-Match` with an ETag, or a `version` column with a conditional `UPDATE ... WHERE id = ? AND version = ?` on an Express or Next route; the row count is the answer, and 0 rows is the 409 the local code raises. `navigator.locks` is a database transaction (or a row lock, `SELECT ... FOR UPDATE`) around the read-modify-write. `normalizeProgress` is a Zod schema at the route handler: parse the body, never touch `req.body` directly. "Preserve corrupt raw bytes" is the rule that a server never overwrites a row it failed to parse: read, fail loudly, leave the row, and let a migration or an operator decide. Draft-versus-accepted state is the React form's local state versus the last server response, with the same adoption rule: only adopt what the server accepted. Do the `newcodexJS/07` course next and map each of these five sentences to a line in it.""", before='## Transfer to a CRUD API')
done.append('review#3 02 names the server-side analogue of each local mechanism')
fe.append_section(S, '01', '## In scope and out of scope in `src/game/`', """| file | scope | why |
|---|---|---|
| `notes.ts`, `schema.ts`, `storage.ts` (+ `storage.test.ts`) | **in** | the CRUD, validation, revision and persistence lessons |
| `drafts.ts` (+ `drafts.test.ts`) | in, second pass | draft-versus-accepted state |
| `engine.ts` (+ `engine.test.ts`), `lab.ts`, `lesson.ts` | out | game mechanics; read only if a test you touch imports them |
| `catalog.ts` and the 334-mission archive | out | content, not behavior |""", before='## ')
done.append('review#4 01 in-scope/out-of-scope table for src/game/')
finish(S, done)

# ---------------------------------------------------------------- e14
S = 'e14'; os.chdir(fe.REG[S]['abs']); done = []
fns, par = count_tests('tests')
w('astraupskill/08-TRANSLATION.md', f"""# 08. Translation: each enforced invariant on JS/TS and C#/.NET

[Course index](README.md)

Read this after chapter 03. Every invariant this Python service enforces has a named equivalent on the stacks you are training for; the table is the contract, the paragraphs after it are the differences that bite.

| invariant here | where | Express + Prisma (TypeScript) | ASP.NET Core + EF Core (C#) |
|---|---|---|---|
| a record is reachable only inside the caller's organization | `scoped_record()` (`app/crud.py:88`) | every query carries `where: {{ id, organizationId }}`; put it in one repository function so no route can forget it | an EF Core global query filter `HasQueryFilter(r => r.OrganizationId == tenant.Id)` plus the same predicate on writes |
| unknown request fields are refused | `model_config = ConfigDict(extra="forbid")` on the Pydantic models | Zod `.strict()` at the route; the service receives the parsed type | explicit DTO classes; `JsonSerializerOptions {{ UnmappedMemberHandling = Disallow }}` if you want the same strictness |
| a stale edit cannot overwrite a newer one | `version_id_col` (`app/models.py:103`, `:179`) | `updateMany({{ where: {{ id, organizationId, version }}, data: {{ ..., version: {{ increment: 1 }} }} }})` and treat `count: 0` as 409 | `[ConcurrencyCheck] int Version` or `[Timestamp] byte[] RowVersion`; catch `DbUpdateConcurrencyException` and answer 409 |
| the client must say which version it saw | `If-Match` required (428) and parsed (400) in `app/crud.py` | the identical headers: a middleware answers 428 when `if-match` is absent and passes the version down | `[FromHeader(Name = "If-Match")]` on the action; `Results.StatusCode(428)` when null |
| side effects are recorded with the change and delivered later | the notification outbox (`app/services/notification_outbox.py`, `app/deliver.py`) | the same table, written on the transaction client; a worker with `SELECT ... FOR UPDATE SKIP LOCKED` | the same table; a `BackgroundService` polling with `FOR UPDATE SKIP LOCKED` (`FromSqlRaw`) |
| deduplication happens before transformation, in one transaction | pipeline ingest in the trace lab | one `$transaction` that checks the dedupe key, inserts the log, runs the transformation, writes the metric | one `DbContext` transaction doing the same four steps |
| queries have resource budgets | the SQL sandbox limits | `statement_timeout` set per session plus a row cap on `take` | `CommandTimeout` on the context plus `Take()` |

## Where the stacks differ

- **Query filters are global in EF Core and local in Prisma.** EF's filter applies to every read automatically (and can be bypassed with `IgnoreQueryFilters()`, which is the audit point); Prisma has no such thing, so the repository function *is* the guard.
- **SQLAlchemy bumps `version` for you; Prisma does not.** The `increment` in the conditional `updateMany` is the whole mechanism on Prisma; forget it and the second edit silently succeeds.
- **Pydantic's `extra="forbid"` is the default nowhere else.** Both `express.json()` and ASP.NET's binder accept unknown members unless told otherwise.

## Exercise

Port `scoped_record()` and the `If-Match` handling to an Express route with Zod and Prisma (about 40 lines), then to an ASP.NET minimal API with EF Core. Both must return 428, 400, 404 (foreign organization) and 409 (stale version) for the same four requests. Keep the two files next to this one.
""")
for path in ['astraupskill/VERIFICATION.md']:
    fe.rw(path, lambda t: re.sub(r'106 distinct Python (?:test )?cases', f'{fns} test functions expanding to 106 collected cases ({par} parametrize decorators)', t))
ev = json.load(open('astraupskill/evidence.json', encoding='utf-8-sig'))
ev['pythonTestFunctions'] = fns; ev['pythonParametrizeDecorators'] = par; ev['pythonCollectedCases'] = ev.get('pythonDistinctTests', 106)
ev['note'] = f'{fns} test functions under tests/ expand to {ev["pythonCollectedCases"]} collected cases through {par} parametrize decorators; verify with pytest --collect-only -q'
json.dump(ev, open('astraupskill/evidence.json', 'w', encoding='utf-8'), indent=2)
done.append(f'review#1 08-TRANSLATION.md (seven-invariant table, stack differences, exercise); review#2 VERIFICATION/evidence.json restate {fns} test functions -> 106 collected cases ({par} parametrize), measured')
# split 02
t2, crlf, bom = fe.read('astraupskill/02-CONCEPTS.md')
cut = t2.find('\n## A retry is not always a new operation')
if cut > 0 and not os.path.exists('astraupskill/02b-CONCEPTS-BEFORE-PRACTICE-3.md'):
    first = t2[:cut].rstrip('\n') + '\n\nThe remaining concepts (retries, query budgets, delivery through the outbox) are in [02b](02b-CONCEPTS-BEFORE-PRACTICE-3.md); read them before practice exercise 3.\n'
    second = '# Concepts, part two: read before practice exercise 3\n\n[Course index](README.md) · [Part one](02-CONCEPTS.md)\n' + t2[cut:]
    fe.write('astraupskill/02-CONCEPTS.md', first, crlf, bom); fe.write('astraupskill/02b-CONCEPTS-BEFORE-PRACTICE-3.md', second, crlf, bom)
    done.append('review#3 02 split: tenancy/validation/transactions/revision stay in 02; retry/budgets/outbox delivery move to 02b, linked')
# promote the two session experiments into 07
rt = rd('astraupskill/README.md')
m1 = re.search(r'^For your first session.*$', rt, re.M); m2 = re.search(r'^For your second session.*$', rt, re.M)
if m1 and m2 and 'predict-then-run' not in rd('astraupskill/07-TRACE-LAB.md'):
    exp = f"## 0. Two predict-then-run experiments (do these first)\n\n**First session.** {m1.group(0)[len('For your first session, '):]}\n\n**Second session.** {m2.group(0)[len('For your second session, '):]}\n\nWrite your prediction before each run; the lab below assumes you have seen both outcomes.\n"
    fe.append_section(S, '07', exp.split('\n', 1)[0], exp.split('\n', 2)[2], before='## 1. Create a pipeline')
    fe.rw('astraupskill/README.md', lambda t: t.replace(m1.group(0), 'Your first two sessions are the two predict-then-run experiments at the top of [07-TRACE-LAB.md](07-TRACE-LAB.md).', 1).replace(m2.group(0) + '\n', '', 1).replace(m2.group(0), '', 1))
    done.append('review#4 the two session experiments moved from README to the top of 07 (README keeps a pointer)')
fe.append_section(S, 'README', '## Prerequisites and pacing', """**Prerequisites:** Python 3.13; a virtual environment (`python -m venv .venv`) and an editable install (`pip install -e .`, which makes `app` importable from anywhere in the tree); basic SQL; the status codes 400/404/409/428.

**Pacing:** map + concepts (02, then 02b before practice 3) about 3 h; the worked change about 3 h with the app running; one evening per practice exercise; the trace lab 2 h.

**Not your stack?** [08-TRANSLATION.md](08-TRANSLATION.md) maps every invariant here to Express/Prisma and ASP.NET/EF Core.""", before='## Start with a separate learning database')
done.append('review#3 README prerequisites and pacing')
finish(S, done)

# ---------------------------------------------------------------- aiapplybot
S = 'aiapplybot'; os.chdir(fe.REG[S]['abs']); done = []
fe.append_section(S, 'README', '## Environment first', """Nothing below works on a clean machine until this block has run:

```powershell
python -m venv .venv
./.venv/Scripts/python -m pip install -r requirements.txt
./.venv/Scripts/python -m pip install -r requirements-dev.txt
./.venv/Scripts/python -m playwright install chromium
./.venv/Scripts/python -m applybot init
./.venv/Scripts/python -m pytest -q
```

Use `./.venv/Scripts/python -m ...` for every command in this course so the interpreter with the dependencies is the one that runs.""", before='## Learning sequence')
done.append('review#1 README opens with the environment block (venv, requirements, requirements-dev, Playwright Chromium, init, pytest)')
w('astraupskill/08-TRANSLATION.md', """# 08. Translation: the three portable mechanisms

[Course index](README.md)

| here (Python + SQLite) | Express / Prisma (TypeScript) | ASP.NET Core / EF Core (C#) | React client |
|---|---|---|---|
| the `{ version, application }` request wrapper: the client states which version it edited | an `If-Match` header, or a `version` field in a Zod-validated body (`.strict()`, so the wrapper is the only shape accepted) | `[FromHeader(Name = "If-Match")]` or a `Version` property on the DTO | the form keeps the loaded record's `version` in state and sends it back unchanged |
| `UPDATE applications SET ..., version = version + 1 WHERE id = ? AND version = ?` and `rowcount != 1` is the 409 (`application_store.py`) | `prisma.application.updateMany({ where: { id, version }, data: { ...fields, version: { increment: 1 } } })` and `count === 0` is the 409 | `[ConcurrencyCheck] int Version`; EF issues the same `WHERE ... AND Version = @p` and throws `DbUpdateConcurrencyException`, which you map to 409 | on 409 keep the draft, show the message, offer to reload |
| `app.js` captured baseline and `adopt()`: the form adopts only what the server returned | the same rule in any client of the route | the same | `const [draft, setDraft] = useState(loaded); const [accepted, setAccepted] = useState(loaded)`; on 200, `setAccepted(response)` and rebase the draft; never `setAccepted(draft)` |

## The one difference that matters

SQLite holds a database-wide write lock for the duration of a write transaction, which is why `application_store.py` validates the input *before* opening the transaction (chapter 02). PostgreSQL locks rows, not the database, so a Prisma or EF service can afford to validate inside the transaction; it still should not, because a validation failure inside a transaction is a wasted round trip and a held connection. Keep the rule: parse first, then transact.

## Exercise

Write the `update` method as an Express route with Zod and Prisma (one conditional `updateMany`, a 409 with the same message as the Python store), then port the `adopt()` rule into a React form with two pieces of state. The test for both: two tabs, the second submit is 409, the second tab's draft text is still on screen.
""")
done.append('review#2 08-TRANSLATION.md mapping the wrapper, the conditional UPDATE + rowcount, and the baseline/adopt rule to Express/Prisma, ASP.NET/EF Core and React')
fe.append_section(S, '02', '## The two-tab sequence, with the numbers', """| step | tab | shown version | submitted version | DB version after | result |
|---|---|---|---|---|---|
| 1 | A | 1 | - | 1 | both tabs load the record at version 1 |
| 2 | B | 1 | - | 1 | |
| 3 | A | 1 | 1 | 2 | `rowcount == 1`: accepted, A adopts version 2 |
| 4 | B | 1 | 1 | 2 | `WHERE id = ? AND version = 1` matches nothing, `rowcount == 0`: 409, B keeps its draft |
| 5 | B | 2 (after reload) | 2 | 3 | accepted |

The row that decides is step 4: no read-then-compare, just a conditional write whose row count is the verdict.

## Why validation runs outside the transaction

`update` in `application_store.py` computes `expected, data = version_input(version), application_input(value)` *before* `with self.transaction()`. SQLite has one writer at a time: a write transaction holds the database-wide lock until commit, so every millisecond spent inside it (parsing, validating, raising) is a millisecond every other writer waits, and a validation error raised inside would have taken the lock for nothing. Validate first, hold the lock only for the read-check-write. The same discipline is right on PostgreSQL for a different reason (a held connection), which is why chapter 08 keeps the rule.""", before='## Identity and optimistic concurrency')
done.append('review#3 02 two-tab table with versions and a paragraph on why validation runs outside the SQLite write transaction')
fe.append_section(S, '01', '## Out of scope for this course', """`applybot/browser.py`, `llm.py`, `ats.py` and `tracker.py` (the Playwright automation, the LLM adapter, the ATS detectors and the legacy tracker) are not part of this course. The four modules to read are `application_store.py`, `web/app.js`, `web/` route wiring in `dashboard.py`, and `cli.py` only where it calls the store. Ignore the rest until the practice exercises send you there.""", before='## ')
done.append('review#4 01 marks browser/llm/ats/tracker out of scope and names the four modules to read')
finish(S, done)
