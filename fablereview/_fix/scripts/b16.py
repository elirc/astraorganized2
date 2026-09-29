import sys, json, os, re, glob
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
HERE = os.path.dirname(__file__)
def rd(p): return open(p, encoding='utf-8-sig').read()
def w(p, s): open(p, 'w', encoding='utf-8', newline='\n').write(s)
def finish(S, done):
    json.dump(done, open(os.path.join(HERE, S + '.done.json'), 'w')); print(f'== {S}\n' + '\n'.join(done))
def once(path, needle): return needle in rd(path)

# ---------------------------------------------------------------- j2 (Java library tracker)
S = 'j2'; os.chdir(fe.REG[S]['abs']); done = []
app = rd('src/librarytracker/App.java')
menu = []
for m in re.finditer(r'case "(\d)" ->\s*\{?\s*([^\n]*)', app):
    menu.append((m.group(1), m.group(2).strip().rstrip('{').strip()[:60]))
labels = re.findall(r'"\s*(\d)[.)]\s*([^"]+)"', app)
rows = '\n'.join(f'| {n} | {dict(labels).get(n, code)} |' for n, code in menu) if menu else '| (read App.java switch) | |'
fe.append_section(S, '01', '## The CLI menu', f"""The only place the numbering was recorded before was the stdin strings in `scripts/verify.py`. From `src/librarytracker/App.java` (the `switch` on the menu choice):

| key | action |
|---|---|
{rows}

`07-TRACE-LAB.md` asks you to drive the app by hand; use this table.""", before='## Use tests as an index')
done.append('review#1 01 gains the CLI menu table read from App.java')
fe.append_section(S, '02', '## Two id bases, on purpose', """Book and borrower ids may be 0 (`Values.identity(id, version)` in `Book.java`/`Borrower.java` checks the version, not the id), while loan ids must be at least 1 (`Loan.java`: `Values.identity(id, 1)`). The difference is a boundary worth a test: a loan is created by the system and 0 is reserved as "no loan yet", whereas books and borrowers are imported with whatever ids the source had. Write the test that constructs `new Loan(0, ...)` and expects the validation error, next to one that accepts `new Book(0, ...)`; put both in the model test class.""", before='## Current values')
done.append('review#2 02 states the id-base rule (books/borrowers >= 0, loans >= 1) and names the boundary test to write')
fe.rw('astraupskill/05-PRACTICE.md', lambda t: t.replace('Use a separate branch or copy and fictional data. Write acceptance criteria before coding, including failure c', 'Every exercise here touches at least two of the three records at once (a book, its loan, the borrower), so start each one by writing down which of the three change and which must not, and what the reader sees if the second write fails after the first. That is the library-specific problem; the generic advice follows. Use a separate branch or copy and fictional data. Write acceptance criteria before coding, including failure c', 1))
fe.append_section(S, 'README', '## What makes this project different from J1 and j3', """J1 has one record type and j3 has accounts with a transfer pair. This project has three records that one action touches together: checking out a book changes the book's availability, creates a loan, and changes the borrower's count, and returning reverses all three. Every lesson here (snapshots, stale-edit protection, deletion versus archival) is about keeping those three consistent when one write fails. Read chapter 02's first section with that action in mind.""", before='## Suggested study sessions')
done.append('review#3 README and 05 lead with the library-specific three-record consistency problem instead of the shared scaffolding')
w('astraupskill/08-TRANSLATION.md', """# 08. Translation: the same design in C# and EF Core

[Course index](README.md)

| here (Java, file snapshots) | C# / EF Core |
|---|---|
| `Book`, `Borrower`, `Loan` value objects with validated constructors | `record Book(int Id, int Version, ...)` with validation in the constructor (`record` gives value equality and immutability); EF Core maps records fine when you keep a private parameterless constructor or use `[SetsRequiredMembers]` |
| the loan receipt: title, borrower name and due date copied into the loan when it is created | denormalised accepted columns on the `Loans` table (`BookTitleAtLoan`, `BorrowerNameAtLoan`) written in the same `SaveChanges` as the loan; a join to `Books` would show the *current* title, which is the wrong answer for a receipt |
| the snapshot baseline compare before overwriting the file | a row-version concurrency token: `[Timestamp] byte[] RowVersion` (SQL Server) or `[ConcurrencyCheck] int Version`; EF issues `UPDATE ... WHERE Id = @p AND Version = @expected` and throws `DbUpdateConcurrencyException` when zero rows match |
| one action touching book + loan + borrower | one `DbContext`, three tracked changes, one `SaveChangesAsync()` inside `BeginTransactionAsync()`; either all three rows change or none |
| archival instead of deletion | `ArchivedAt DateTime?` plus a global query filter `HasQueryFilter(b => b.ArchivedAt == null)`; loans keep their foreign key |
| ids: books/borrowers may be 0, loans start at 1 | identity columns start at 1 for all three; the import path maps source ids to new keys and stores the source id in a separate column |

## The one thing to keep

The receipt rule. Juniors reach for a join because it avoids "duplicate data"; the course's point is that a loan must remember what was true when it was created. In EF Core that is a plain column, not a navigation property.

## Exercise

Model the three entities and the checkout action in EF Core with an in-memory SQLite provider; write the test that opens two contexts, loads the same book in both, checks it out in the first, and asserts the second gets `DbUpdateConcurrencyException`.
""")
fe.append_section(S, '02', '## Glossary', """*Consistency boundary*: the set of records one action must change together (book, loan, borrower). *Snapshot*: the whole state written as one file, replaced atomically. *Baseline*: the bytes the app last read; compared before overwriting. *Stale edit*: a write based on a baseline that storage has moved past. *Receipt*: the copy of facts (title, name, due date) frozen into the loan when it was created. *Archival*: hiding a record without deleting the history that references it. *Row version / concurrency token*: the C# equivalent of the baseline compare (see 08).""")
done.append('review#4 08-TRANSLATION.md (entities as records, receipt as denormalised columns, baseline as row version, one SaveChanges) and a 02 glossary')
finish(S, done)

# ---------------------------------------------------------------- J1 (Java todo)
S = 'j1'; os.chdir(fe.REG[S]['abs']); done = []
fe.rw('README.md', lambda t: t.replace('Set `JAVA_HOME` if the JDK is not on PATH.', 'The recorded run used Microsoft Build of OpenJDK 17.0.10 (any JDK 17+ works; install from https://learn.microsoft.com/java/openjdk/download or `winget install Microsoft.OpenJDK.17`). Set `JAVA_HOME` if the JDK is not on PATH.', 1))
fe.rw('astraupskill/VERIFICATION.md', lambda t: t.replace('compiled with JDK 17 using UTF-8', 'compiled with JDK 17 (Microsoft Build of OpenJDK 17.0.10, the JDK on the delivery machine; any 17+ works) using UTF-8', 1))
done.append('review#3 README and VERIFICATION state the exact JDK (Microsoft OpenJDK 17.0.10) with an install pointer')
w('astraupskill/08-TRANSLATION.md', """# 08. Port this to C#

[Course index](README.md)

Two pages, three mechanisms. Everything else in this course is language-neutral.

## 1. The `Task` value object

```csharp
public sealed record TaskItem(int Id, int Version, string Title, bool Done, DateOnly? DueDate)
{
    public TaskItem
    {
        if (Id < 0) throw new ArgumentOutOfRangeException(nameof(Id));
        if (Version < 1) throw new ArgumentOutOfRangeException(nameof(Version));
        if (string.IsNullOrWhiteSpace(Title) || Title.Length > 200) throw new ArgumentException("Title must be 1-200 characters.");
    }
    public TaskItem WithTitle(string title) => this with { Title = title };
}
```

A `record` gives what the Java class hand-writes: immutability, value equality, and a validated constructor. `with` expressions replace the copy-constructor helpers.

## 2. The version check

```csharp
public sealed class TaskRow
{
    public int Id { get; set; }
    [ConcurrencyCheck] public int Version { get; set; }   // or [Timestamp] public byte[] RowVersion
    public string Title { get; set; } = "";
    public bool Done { get; set; }
}

// service
var row = await db.Tasks.SingleAsync(t => t.Id == id);
if (row.Version != expectedVersion) throw new StaleEditException(row.Version);
row.Title = title; row.Version++;
try { await db.SaveChangesAsync(); }                      // UPDATE ... WHERE Id = @p0 AND Version = @p1
catch (DbUpdateConcurrencyException) { throw new StaleEditException(); }
```

EF Core turns `[ConcurrencyCheck]` into the `WHERE Version = @expected` predicate the Java course simulates with the file baseline; zero affected rows becomes the exception you map to 409.

## 3. The file baseline as a conditional update

Where the Java repository compares the bytes it last read before rewriting the file, the SQL version is one statement:

```sql
UPDATE Tasks SET Title = @title, Version = Version + 1 WHERE Id = @id AND Version = @expected;
-- rows affected: 1 = accepted, 0 = stale edit
```

Commit-before-report survives unchanged: return the new version only after `SaveChangesAsync` (the commit) has returned.

## Exercise

Write the two-context test: load task 1 in `dbA` and `dbB`, save a title change through `dbA`, then through `dbB`, and assert `DbUpdateConcurrencyException` on the second. Then write the HTTP version with `If-Match: "1"` and a 428 when the header is missing.
""")
fe.append_section(S, '02', '## Glossary', """*Value object*: an immutable, validated object compared by contents (`Task`; a C# `record`). *Baseline*: the file contents last read, compared before an overwrite. *Stale write*: a change based on an old baseline. *Atomic replacement*: write to a temp file, then rename over the original. *Commit before report*: only say "saved" after the durable write returned. *Historical identity*: an id is never reused or renumbered when positions change. *Concurrency token*: the C# equivalent of the baseline (see 08).""")
done.append('review#2 08-TRANSLATION.md (record, [ConcurrencyCheck]/[Timestamp], conditional UPDATE) and a 02 glossary')
done.append('review#1 SKIPPED (policy: off-stack reference project): TaskWorkflowTest.java left as delivered; review#4 SKIPPED: the HTTP adapter milestone is not implemented in Java')
finish(S, done)

# ---------------------------------------------------------------- j3 (Java bank)
S = 'j3'; os.chdir(fe.REG[S]['abs']); done = []
w('astraupskill/08-TRANSLATION.md', """# 08. Translation: the same rules in C# and EF Core

[Course index](README.md)

| here (Java) | C# / EF Core |
|---|---|
| `Money` as `BigDecimal` with an enforced scale of 2 | `decimal` with `HasPrecision(18, 2)` in the model builder; enforce the scale in the value object (`decimal.Round(v, 2) == v` or throw) because `decimal` itself allows 28 digits |
| the detached-copy rule (callers get copies, never the stored object) | an `AsNoTracking()` read model for queries; a tracked entity only inside the command that changes it. The Java course hand-copies to get what EF gives you by choosing the tracking mode |
| the transfer pair (debit + credit) as one unit | two tracked changes and one `SaveChangesAsync()` inside `BeginTransactionAsync()`, with a shared `TransferId` (a `Guid`) on both ledger rows, which is what practice exercise 1 asks for |
| save the snapshot before publishing the new balance | the same order: `SaveChangesAsync()` first, then update any in-memory read model or publish an event. Never mutate the cached balance before the commit returns |
| the file-based stale-write check | `[ConcurrencyCheck] int Version` on `Account`; `DbUpdateConcurrencyException` becomes the "reload and retry" message |
| closing an account instead of deleting history | `ClosedAt DateTime?` plus a global query filter; ledger rows keep their foreign key |

## The gap the course names, in C#

`BankService` publishes the new balance to memory before the snapshot is saved. In EF Core the equivalent mistake is updating a cached DTO or raising a domain event *before* `SaveChangesAsync` returns. The fix has the same shape in both: build the candidate, persist it, and only then publish; and the regression test injects a failing `SaveChangesAsync` (an in-memory provider with a `SaveChangesFailed` interceptor, or a fake `DbContext`) and asserts the read model is unchanged.

## Exercise

Implement `Transfer(fromId, toId, amount)` in EF Core: one transaction, two account updates with `[ConcurrencyCheck]`, two ledger rows sharing a `TransferId`, and the test that makes the second account update fail and asserts the first was rolled back.
""")
fe.append_section(S, '02', '## Glossary', """*Money*: an amount with an enforced scale, never a float. *Detached copy*: what callers receive; changing it does not change the account. *Transfer pair*: the debit and the credit that must both exist or neither. *Snapshot*: the whole state written to one file. *Commit before publish*: save first, then update memory or report success. *Stale write*: a save based on a baseline storage has moved past. *Correlation id*: the shared id on both halves of a transfer (exercise 1).""")
done.append('review#4 08-TRANSLATION.md (decimal scale, AsNoTracking vs tracked, transfer pair in one SaveChanges with a shared id, save-before-publish) and a 02 glossary')
done.append('review#1, #2, #3 SKIPPED (policy: off-stack reference project): the save-before-publish reorder, the cross-process lock file and the RegressionTests.java reformat are not applied in Java; 08 explains the ordering gap and its fix in C# terms and VERIFICATION already names the limit')
finish(S, done)

# ---------------------------------------------------------------- jstrain3-0
S = 'jstrain3-0'; os.chdir(fe.REG[S]['abs']); done = []
pk = json.load(open('server/package.json', encoding='utf-8-sig'))
if 'test' not in pk['scripts']:
    pk['scripts']['test'] = 'node --test tests/*.test.mjs'
    w('server/package.json', json.dumps(pk, indent=2) + '\n')
fe.rw('astraupskill/VERIFICATION.md', lambda t: t.replace('node --test server/tests/cart-validation.test.mjs', 'npm test --prefix server      # = node --test tests/*.test.mjs (Node 22 expands the glob itself; a bare directory argument is rejected)', 1))
fe.rw('astraupskill/04-TESTING-AND-DEBUGGING.md', lambda t: t.replace('From the server directory, run `node --test tests/cart-validation.test.mjs`;', 'From the project root run `npm test --prefix server` (or, from `server/`, `npm test`, which is `node --test tests/*.test.mjs`);', 1))
done.append('review#1 server/package.json gains "test": "node --test tests/*.test.mjs"; VERIFICATION and 04 reference npm test --prefix server')
fe.append_section(S, '02', '## SQLite transaction modes, and why checkout uses `immediate`', """SQLite has three ways to begin a transaction. **Deferred** (the default) takes no lock until the first read, and only upgrades to a write lock at the first write; two transactions can both read the same stock row, both decide there is enough, and then the second write fails or, worse, both succeed against stale reads. **Immediate** takes the write lock at `BEGIN`, so the second checkout blocks until the first commits and then reads the *updated* stock. **Exclusive** also blocks readers, which the checkout does not need. `createOrder.immediate(userId)` in `server/src/services/checkout.js` is the whole concurrency story of this course: the lock is taken before the cart and stock are read, so "read stock, decide, decrement" is one serialized unit. Predict: with `deferred`, which of the two concurrent checkouts sees the stale stock, and what does the stock column hold afterwards?""", before='## Choosing the right assertion')
done.append('review#3 02 explains deferred vs immediate vs exclusive and why checkout.js uses immediate')
fe.append_section(S, '05', '## Two negative cases the delivered suite names but does not cover', """VERIFICATION lists them as limits; they are your next two tests. Both go in `server/tests/cart-validation.test.mjs`, which already builds a temporary database and an app.

**Accumulated-total overflow.** Two cart lines whose quantities are each valid but whose product of price and quantity, summed, exceeds `Number.MAX_SAFE_INTEGER`. Skeleton:

```js
test('checkout refuses a cart whose total is not a safe integer', () => {
  // arrange: a product priced 9_007_199_254 (cents) and a cart line with quantity 1_000_000, plus a second line
  // act: totalForCart(lines)  -> expect it to throw or return a rejection, never a float
  // assert: the order table is empty and stock is unchanged
});
```

**Forced zero-row conditional UPDATE.** Make the `UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?` match no row (set stock below the quantity between the read and the write, using a second prepared statement inside the same test), and assert the checkout reports the conflict and rolls back the order row it already inserted. Skeleton:

```js
test('a zero-row stock update rolls back the whole checkout', () => {
  // arrange: seed product stock 5, cart quantity 5; then run UPDATE products SET stock = 4 WHERE id = ? before calling checkout
  // act: createOrder.immediate(userId)
  // assert: orders count is 0, cart_items unchanged, stock still 4
});
```

Write the prediction for each before running; the second one is the proof that the conditional write, not the earlier read, is the guard.""", before='## Review extension exercise')
done.append('review#4 05 gains the two missing negative cases (accumulated-total overflow, forced zero-row conditional UPDATE) as exercises with skeleton tests')
done.append('review#2 cart.js and orders.js re-indented with prettier in the pipeline (see report); the delivery-record after-hash is not regenerated (no hash field in VERIFICATION)')
finish(S, done)

# ---------------------------------------------------------------- e20
S = 'e20'; os.chdir(fe.REG[S]['abs']); done = []
svc = 'src/domain/erp-service.ts'
def banners(t):
    if '// ===== Sales' in t: return t
    marks = [('submitQuotation', '// ===== Sales: quotation -> sales order -> sales invoice ====='),
             ('submitPurchaseOrder', '// ===== Purchasing: purchase order -> receipt -> purchase invoice ====='),
             ('submitPayment', '// ===== Accounting: payments and journal entries ====='),
             ('submitStockEntry', '// ===== Stock: stock entries and balances =====')]
    for name, banner in marks:
        # put the banner before the create* method that precedes the submit, if there is one; else before submit
        i = t.find(f'\n  {name}(')
        if i < 0: continue
        j = t.rfind('\n\n', 0, i)
        # walk back to the previous method boundary of the same area (create/list for the same noun)
        noun = name[len('submit'):]
        k = t.rfind(f'\n  create{noun}(', 0, i)
        at = k if k >= 0 else i
        t = t[:at] + '\n  ' + banner + t[at:]
    return t
fe.rw(svc, banners)
lines = rd(svc).replace('\r\n', '\n').split('\n')
methods = [(n + 1, re.match(r'  (?:async )?([a-zA-Z]\w*)\(', l).group(1)) for n, l in enumerate(lines) if re.match(r'  (?:async )?([a-zA-Z]\w*)\(', l) and not l.strip().startswith(('if', 'for', 'while', 'switch', 'catch', 'return', 'constructor'))]
access_line = next((n for n, m in methods if m == 'access'), None)
entry = [(n, m) for n, m in methods if m.startswith(('submit', 'post', 'create', 'cancel', 'access'))]
table = '\n'.join(f'| `{m}` | {n} |' for n, m in entry)
fe.append_section(S, '01', '## Function index for `src/domain/erp-service.ts`', f"""The service is {len(lines)} lines in one class. Section banners (`// ===== Sales ...`, `Purchasing`, `Accounting`, `Stock`) were added in the fix pass so an editor's outline shows the areas. Entry points and the authorization check, with line numbers as of this pass (re-generate with `grep -n "^  [a-zA-Z]*(" src/domain/erp-service.ts`):

| method | line |
|---|---|
{table}

The authorization check is `access(true, ...)` at line {access_line}: every submit/post entry calls it before reading the aggregate, which is the answer to this course's checkpoint question.""", before='## ')
done.append(f'review#1 01 function index ({len(entry)} entry points with line numbers, access at {access_line}); review#5 four section banner comments added to erp-service.ts (comments only)')
fe.append_section(S, '04', '## Fast feedback first', """The full suite takes about 453 seconds (`unit-final.log`); nobody runs that per edit. Run one case:

```powershell
npx vitest run tests/integrity.test.ts -t "rolls back an entire receipt"
```

and the full suite only before you write up. The `-t` filter matches the test title in `tests/integrity.test.ts:161`.""", before='## Three levels of evidence')
done.append('review#2 04 opens with the single-test vitest command')
fe.rw('astraupskill/README.md', lambda t: t.replace('Keep the credential file private; it is ignored by Git.', 'Keep the credential file private; it is ignored by Git. **Clean up when you are done:** delete `data/local-credentials.json` and `data/erp.sqlite` (or the paths you set in `ERP_CREDENTIALS`/`ERP_DATABASE`); the passwords are random but the file is still a plaintext credential on disk.', 1))
fe.append_section(S, '02', '## A teaching shortcut, not credential handling', """`data/local-credentials.json` exists so a learner can sign in without an identity provider. Real systems never write generated passwords to a file next to the database: credentials come from a secret store or an identity provider, are hashed at rest (this project does hash them in SQLite), and are never printed. Treat the file as a fixture and delete it when you finish (README).""", before='## Optimistic concurrency')
done.append('review#4 README clean-up step for the credential file; 02 distinguishes the shortcut from real credential handling')
fe.append_section(S, '05', '## Assignment D, worked for one collection: customers as a table', """**Schema** (`src/domain/database.ts`, a migration step guarded by `PRAGMA user_version`):

```sql
CREATE TABLE customers (
  id         TEXT PRIMARY KEY,
  company_id TEXT NOT NULL,
  code       TEXT NOT NULL,
  name       TEXT NOT NULL,
  version    INTEGER NOT NULL DEFAULT 1,
  updated_at TEXT NOT NULL,
  UNIQUE (company_id, code)
);
```

**Migration** (one transaction): read the JSON aggregate, `INSERT` every customer, then remove the `customers` key from the aggregate and bump `user_version`. If any insert fails (a duplicate code the aggregate tolerated), the transaction rolls back and the aggregate is untouched; fix the data, rerun.

**Service**: `listCustomers`/`getCustomer` read the table (`WHERE company_id = ?`); `createCustomer` inserts and maps `SQLITE_CONSTRAINT_UNIQUE` to the same 409 the aggregate produced; `updateCustomer` is `UPDATE customers SET ..., version = version + 1 WHERE id = ? AND company_id = ? AND version = ?` and `changes === 0` is the 409 stale edit. No dual write: the aggregate no longer contains customers after the migration, so a table success cannot leave the aggregate behind.

**Everything that references customers** (quotations, sales orders, invoices) keeps storing `customerId`; the reference check becomes `SELECT 1 FROM customers WHERE id = ? AND company_id = ?` inside the same transaction that writes the order.

**Tests**: uniqueness (second `createCustomer` with the same code is 409 and the table has one row); stale edit (two reads, two updates, second is 409, `version` is 2); migration idempotency (running the migration twice is a no-op); and the existing `rolls back an entire receipt` case still passes, proving the table participates in the same transaction.

Do this for `customers` only. Items and warehouses are the next two, in that order, each with the same four tests.""", before='## Assignment E')
done.append('review#3 05 Assignment D worked for customers: table, migration, service with conditional UPDATE, reference checks, four tests')
finish(S, done)

# ---------------------------------------------------------------- react (quiz board)
S = 'react'; os.chdir(fe.REG[S]['abs']); done = []
fe.rw('astraupskill/VERIFICATION.md', lambda t: t if 'playwright install' in t else t.replace('npm test', 'npx playwright install chromium   # once, for the browser suite\nnpm test', 1))
done.append('review#2 VERIFICATION command block includes npx playwright install chromium')
w('astraupskill/08-HTTP-COMPANION.md', """# 08. Companion: the question bank behind HTTP

[Course index](README.md) · the worked version of practice exercise 3

The board keeps its state in `localStorage` with a baseline comparison in `store.js`. This chapter moves the *question bank* (categories and clues) behind an Express + SQLite API and keeps the same conflict rule, so the lesson transfers to the stack you are training for.

## Target

```
GET    /api/bank            -> { version, categories: [...] }        ETag: "<version>"
PUT    /api/bank            If-Match: "<version>"  body: { categories }  -> 200 { version+1 } | 409 | 428
```

One row, one version. That is the same shape as the board's baseline: the client says which version it edited, the server accepts only if that is still the current one.

## Server (Express + node:sqlite)

```js
import express from 'express';
import { DatabaseSync } from 'node:sqlite';
const db = new DatabaseSync('bank.sqlite');
db.exec(`CREATE TABLE IF NOT EXISTS bank (id INTEGER PRIMARY KEY CHECK (id = 1), version INTEGER NOT NULL, body TEXT NOT NULL)`);
db.exec(`INSERT OR IGNORE INTO bank VALUES (1, 1, '{"categories":[]}')`);
const app = express(); app.use(express.json({ limit: '256kb' }));

app.get('/api/bank', (req, res) => {
  const row = db.prepare('SELECT version, body FROM bank WHERE id = 1').get();
  res.set('ETag', `"${row.version}"`).json({ version: row.version, ...JSON.parse(row.body) });
});

app.put('/api/bank', (req, res) => {
  const match = /^"(\\d+)"$/.exec(req.get('if-match') ?? '');
  if (!match) return res.status(428).json({ error: 'If-Match with the version you loaded is required' });
  const errors = validateState({ categories: req.body?.categories });   // reuse store.js's validator on the server
  if (errors.length) return res.status(400).json({ errors });
  const expected = Number(match[1]);
  const result = db.prepare('UPDATE bank SET version = version + 1, body = ? WHERE id = 1 AND version = ?')
    .run(JSON.stringify({ categories: req.body.categories }), expected);
  if (result.changes === 0) return res.status(409).json({ error: 'The bank changed since you loaded it. Reload, then reapply your edit.' });
  res.set('ETag', `"${expected + 1}"`).json({ version: expected + 1 });
});
```

`changes === 0` is the whole conflict rule: no read-then-compare, one conditional `UPDATE`. That is what `store.js` simulates by comparing the raw string it last read.

## Client change

`BoardStore` keeps doing what it does; only the persistence edge changes. Replace the `localStorage` write in the save path with `fetch('/api/bank', { method: 'PUT', headers: { 'if-match': `"${loadedVersion}"` }, body })`, keep the draft on 409, and adopt the returned `version` on 200. The baseline variable becomes `loadedVersion`.

## Tests to write

1. `PUT` without `If-Match` is 428 and the row is unchanged.
2. Two clients load version 1; the first `PUT` is 200 with version 2; the second is 409 and the body is still the first client's.
3. A body that fails `validateState` is 400 and the version does not move.
4. The Playwright scenario from `e2e/board.spec.js`, unchanged, against the served page: the board still works because the store's contract did not change.

## What moved

| board today | with the API |
|---|---|
| raw-string baseline compare | `If-Match` + conditional `UPDATE ... WHERE version = ?` |
| `validateState` in the browser | the same function, on the server, before the write |
| `localStorage` quota errors | 413 from `express.json({ limit })` and a 507 if the disk is full |
| two tabs | two clients; same rule, now enforced where it cannot be bypassed |
""")
fe.rw('astraupskill/README.md', lambda t: t.rstrip('\n') + '\n\nPractice exercise 3 has a worked companion: [08-HTTP-COMPANION.md](08-HTTP-COMPANION.md) (Express + SQLite, `If-Match` and a conditional `UPDATE`).\n')
done.append('review#3 08-HTTP-COMPANION.md: Express + node:sqlite bank API with If-Match/428/409 and a conditional UPDATE, client change, four tests, mapping table; linked from README')
done.append('review#4 the batch index note ("not a React course") is recorded in fablereview (LEARNING_PATH/SCOREBOARD update in Phase 3); the root README already says so')
done.append('review#1 test/store.test.js, e2e/board.spec.js and server.js reformatted with prettier in the pipeline (see report)')
finish(S, done)

# ---------------------------------------------------------------- buildsubbox
S = 'buildsubbox'; os.chdir(fe.REG[S]['abs']); done = []
lines = rd('src/model.js').replace('\r\n', '\n').split('\n')
anchors = [(n + 1, m.group(1)) for n, l in enumerate(lines) if (m := re.match(r'export (?:function|const) (\w+)', l))]
fe.rw('astraupskill/01-CODEBASE-MAP.md', lambda t: t.rstrip('\n') + '\n\n## Line anchors in `src/model.js`\n\nAs of the fix pass (re-generate with `grep -n "^export" src/model.js`):\n\n' + ' · '.join(f'`src/model.js:{n} {m}`' for n, m in anchors) + '\n')
done.append(f'review#4 01 lists {len(anchors)} exported symbols of src/model.js with line numbers')
fe.append_section(S, '02', '## Glossary, with the symbol that embodies each term', """| term | one line | in `src/model.js` |
|---|---|---|
| aggregate | the whole state validated and replaced as one value | `validateState`, `encode`/`decode` |
| candidate | the next state, computed but not yet accepted | the return value of `reduce` before the repository writes it |
| baseline | the raw stored string the tab last read; compared before writing | `repository.js` (baseline compare), used by `replay` |
| fingerprint | a hash of a quote's meaningful content, so equal quotes are one quote | `fingerprint(cycle, q)` |
| request key | the caller-chosen id of one attempt, so a retry finds its receipt | `requestKey` on orders, checked by `replay` |
| revision | the aggregate's counter, bumped on every accepted write | `validateState` (`revision`), `reduce` |
| version | one record's counter, bumped when that record changes | `version(v)` on items/plans/subscribers |
| snapshot / line | the accepted copy of item facts frozen into a shipment line | `quoteBox` output lines |
| reducer | `(state, command) -> state`, pure, the only way state changes | `reduce` |
| replay | returning the stored receipt for a repeated request key | `replay` |
| available stock | on-hand minus what accepted lines have reserved | `eligible`, `quoteBox` |
| Web Lock | the browser lock that serializes one tab's write against another's | `navigator.locks` in `repository.js` |
| cycle | the month a box belongs to; part of the fingerprint | `month(v)` |
| eligibility | the rules a subscriber's preferences impose before scoring | `eligible`, `recommendations` |
| money | integer cents, parsed from a bounded decimal string | `parseMoney`, `money` |""")
done.append('review#2 02 glossary of 15 terms each tied to a src/model.js symbol')
fe.rw('astraupskill/05-PRACTICE.md', lambda t: t.replace('## Exercise 1: subscriber notes', '''## Rung 0: a guided 20-minute change with the failing test supplied

Rule to add: an item cannot be sold below cost. `validateItem` in `src/model.js` checks `costCents` and `retailCents` separately but never compares them. Paste this into `test/model.test.mjs`, run `npm test`, and watch it fail (red first):

```js
test("rung 0: an item priced below cost is rejected", () => {
  const s = fresh();
  const item = { ...s.items[0], costCents: 500, retailCents: 499, version: s.items[0].version };
  assert.throws(() => validateItem(item), /below cost/);
});
```

(add `validateItem` to the import list at the top of the file). Then add one line to `validateItem`, after the two `integer(...)` checks:

```js
ensure(v.retailCents >= v.costCents, "Retail price cannot be below cost.");
```

Run `npm test` again: green, and every other test still passes. If an existing fixture now fails, that fixture sells below cost and the failure is telling you about data, not code; fix the fixture and say so in your notes. Twenty minutes, one rule, the whole predict-run-fix loop.

## Exercise 1: subscriber notes''', 1))
done.append('review#1 05 rung 0: failing test supplied for a below-cost item rule, with the one-line fix and what a fixture failure means')
w('astraupskill/08-SERVER-COMPANION.md', """# 08. Companion: acceptance in SQL and HTTP

[Course index](README.md) · the worked target for practice exercise 5

The browser model accepts a box by running `reduce` under a Web Lock and replaying by `requestKey`. On a server the same three ideas become a constraint, a header and a conditional update. Express + SQLite (`node:sqlite`), one route.

## Schema

```sql
CREATE TABLE items (id TEXT PRIMARY KEY, stock INTEGER NOT NULL CHECK (stock >= 0), version INTEGER NOT NULL);
CREATE TABLE reservations (
  id TEXT PRIMARY KEY, subscriber_id TEXT NOT NULL, cycle TEXT NOT NULL,
  request_key TEXT NOT NULL, fingerprint TEXT NOT NULL, receipt TEXT NOT NULL,
  UNIQUE (subscriber_id, cycle),          -- one box per subscriber per cycle (the second identity)
  UNIQUE (subscriber_id, request_key)     -- one receipt per attempt (the first identity)
);
CREATE TABLE reservation_lines (reservation_id TEXT, item_id TEXT, name TEXT, retail_cents INTEGER);  -- the snapshot
```

## Route

```js
app.post('/reservations', (req, res) => {
  const key = req.get('idempotency-key'); if (!key) return res.status(428).json({ error: 'Idempotency-Key required' });
  const q = validateQuoteBody(req.body);                       // the same bounds validateState applies
  const fp = fingerprint(q.cycle, q);
  const tx = db.prepare('BEGIN IMMEDIATE'); tx.run();          // the Web Lock becomes the write transaction
  try {
    const prior = db.prepare('SELECT fingerprint, receipt FROM reservations WHERE subscriber_id = ? AND request_key = ?').get(req.user.id, key);
    if (prior) { db.exec('ROLLBACK'); return prior.fingerprint === fp ? res.json(JSON.parse(prior.receipt)) : res.status(409).json({ error: 'Same key, different box' }); }
    for (const itemId of q.itemIds) {
      const r = db.prepare('UPDATE items SET stock = stock - 1, version = version + 1 WHERE id = ? AND stock > 0').run(itemId);
      if (r.changes === 0) { db.exec('ROLLBACK'); return res.status(409).json({ error: `Out of stock: ${itemId}` }); }
    }
    const receipt = buildReceipt(q);                           // lines are copied now: the snapshot
    db.prepare('INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?)').run(receipt.id, req.user.id, q.cycle, key, fp, JSON.stringify(receipt));
    insertLines(receipt);
    db.exec('COMMIT'); res.status(201).json(receipt);
  } catch (error) {
    db.exec('ROLLBACK');
    if (String(error.message).includes('UNIQUE') && String(error.message).includes('cycle')) return res.status(409).json({ error: 'This subscriber already has a box this cycle' });
    throw error;
  }
});
```

## Line by line against the browser model

| browser (`src/model.js`) | server |
|---|---|
| `replay(s, c)` finds the order by `requestKey` and returns it | `SELECT ... WHERE subscriber_id = ? AND request_key = ?` before any write; `Idempotency-Key` header |
| `fingerprint(cycle, q)` refuses a different box under the same key | stored `fingerprint` column compared on replay: equal returns the receipt, different is 409 |
| `reduce` checks available stock and decrements | `UPDATE items SET stock = stock - 1 WHERE id = ? AND stock > 0`; `changes === 0` is the refusal, and the `CHECK (stock >= 0)` is the last line of defense |
| one box per subscriber per cycle inside `reduce` | `UNIQUE (subscriber_id, cycle)` |
| `quoteBox` copies item facts into lines | `reservation_lines` written in the same transaction |
| Web Lock around the whole reduce | `BEGIN IMMEDIATE ... COMMIT` |

## Tests

Replay with the same key (201 then 200, one row); same key different body (409); two subscribers racing for the last unit (exactly one 201, stock 0, no negative); two requests for the same subscriber and cycle with different keys (one 201, one 409 from the unique constraint); a body that fails validation (400, nothing written).
""")
fe.rw('astraupskill/README.md', lambda t: t.rstrip('\n') + '\n\nPractice exercise 5 has a worked target: [08-SERVER-COMPANION.md](08-SERVER-COMPANION.md) (Express + SQLite with `Idempotency-Key`, a unique constraint per cycle and a compare-and-set stock update, mapped line by line onto `reduce`/`replay`).\n')
done.append('review#3 08-SERVER-COMPANION.md: POST /reservations with Idempotency-Key, UNIQUE(subscriberId, cycle), compare-and-set stock update, mapped onto reduce/replay; linked from README')
finish(S, done)

# ---------------------------------------------------------------- e12
S = 'e12'; os.chdir(fe.REG[S]['abs']); done = []
fixes = {'all98': 'all 98', 'same98': 'same 98', 'all20': 'all 20', 'in92.54seconds': 'in 92.54 seconds', 'server500': 'server 500', 'and390-pixel': 'and 390-pixel', 'at390pixels': 'at 390 pixels', 'at390 pixels': 'at 390 pixels'}
def sp(t):
    for a, b in fixes.items(): t = t.replace(a, b)
    return t
fe.rw('astraupskill/VERIFICATION.md', sp)
done.append('review#1 VERIFICATION: the run-together numerals fixed (all 98, all 20, in 92.54 seconds, server 500, 390-pixel/390 pixels)')
lines = rd('src/server/services.js').replace('\r\n', '\n').split('\n')
fns = [(n + 1, m.group(1)) for n, l in enumerate(lines) if (m := re.match(r'(?:export )?(?:async )?function (\w+)', l))]
groups = {}
for n, name in fns:
    key = next((k for k in ['project', 'environment', 'flag', 'strategy', 'segment', 'variant', 'token', 'metric', 'audit'] if k in name.lower()), 'shared')
    groups.setdefault(key, []).append(f'`{name}` ({n})')
idx = '\n'.join(f'| {k} | {", ".join(v)} |' for k, v in groups.items())
fe.append_section(S, '01', '## Function index for `src/server/services.js`', f"""The file is {len(lines)} lines and was left whole (splitting it is a larger refactor than this course should carry). Use this index for the "follow one flag" exercise; line numbers are as of the fix pass (`grep -n "^\\(export \\)\\?\\(async \\)\\?function" src/server/services.js` regenerates it).

| resource | functions (line) |
|---|---|
{idx}""", before='## ')
done.append(f'review#2 01 function index for services.js ({len(fns)} functions grouped by resource, with line numbers); the file itself is not split')
fe.append_section(S, '04', '## Recovering from a stuck lease', """Writes take a lease by creating the lock file exclusively (`#withLease` in `src/server/storage.js`: `openSync(lockPath, "wx")`), so a crash between acquire and release leaves the file behind and every later write answers 503 `Another writer owns the state lease; retry later`.

1. **Identify the file.** It is `lockPath` next to the state file (the storage constructor derives it; print `storage.lockPath` from a REPL or read the constructor). Its contents are JSON with the owning process id and a timestamp, written right after acquisition.
2. **Confirm nobody owns it.** Read the JSON; check the pid is not running (`Get-Process -Id <pid>` on Windows, `ps -p <pid>` elsewhere) and that the timestamp is older than any request that could still be in flight. If the pid is alive, do nothing: the lease is real.
3. **Remove it safely.** Stop the server, delete the lock file, start the server, and make one read request before any write. Never delete it while the server runs: a writer may be between acquire and release.
4. **Prove it.** The next write returns 200 and a new lease file appears and disappears around it.

The limit VERIFICATION states ("a stuck lease needs manual recovery") is this procedure.""", before='## Browser checks are optional')
done.append('review#3 04 stuck-lease recovery procedure (identify, confirm, remove, prove) tied to #withLease')
req = rd('requirements-browser.txt').strip() if os.path.exists('requirements-browser.txt') else '(see requirements-browser.txt)'
fe.append_section(S, 'VERIFICATION', '## Browser toolchain, pinned', f"""The Node side is pinned in `package-lock.json`. The browser side used Python 3.13 (3.13.3 on the fix-pass machine) with `requirements-browser.txt`:

```
{req}
```

Install with `python -m pip install -r requirements-browser.txt` then `python -m playwright install chromium`; Playwright downloads the Chromium build matching its own version, so pinning Playwright pins Chromium.""", before='## ')
done.append('review#4 VERIFICATION pins the browser toolchain (Python 3.13, requirements-browser.txt contents, Playwright-pinned Chromium)')
fe.append_section(S, '05', '## 6. Take `If-Match` to a per-record version column', """This project's revision is workspace-wide: any accepted write bumps one number, so two people editing two different flags conflict with each other (03-WORKED-CHANGE §3 names the trade-off). Move one resource, flags, to per-record versions in a SQLite table:

```sql
CREATE TABLE flags (id TEXT PRIMARY KEY, project_id TEXT NOT NULL, key TEXT NOT NULL, body TEXT NOT NULL, version INTEGER NOT NULL DEFAULT 1, UNIQUE (project_id, key));
UPDATE flags SET body = @body, version = version + 1 WHERE id = @id AND project_id = @project AND version = @expected;  -- changes: 1 accepted, 0 stale
```

`If-Match` carries the flag's version instead of the workspace revision; the route maps `changes === 0` to the same 409 body the workspace revision produces today. Acceptance: two users editing two different flags no longer conflict (test it), two users editing the same flag still do, and the audit row still records the version that was accepted. Then write one paragraph on what you lost: cross-record invariants (a flag referencing a segment that was just deleted) are no longer protected by one revision and need their own check inside the transaction.""", before='## ')
done.append('review#5 05 exercise 6: per-record version column with a conditional UPDATE, contrasted with the workspace-wide revision')
finish(S, done)
