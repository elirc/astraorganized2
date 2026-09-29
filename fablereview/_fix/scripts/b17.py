import sys, json, os, re, glob
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
HERE = os.path.dirname(__file__)
def rd(p): return open(p, encoding='utf-8-sig').read()
def w(p, s): open(p, 'w', encoding='utf-8', newline='\n').write(s)
def finish(S, done):
    json.dump(done, open(os.path.join(HERE, S + '.done.json'), 'w')); print(f'== {S}\n' + '\n'.join(done))
def strip_bom(folder='astraupskill'):
    n = 0
    for f in glob.glob(f'{folder}/*.md'):
        t, crlf, bom = fe.read(f)
        if bom: fe.write(f, t, crlf, False); n += 1
    return n
def node_pins(engines=True, nvmrc=True):
    if nvmrc and not os.path.exists('.nvmrc'): w('.nvmrc', '22.16.0\n')
    pk = json.load(open('package.json', encoding='utf-8-sig'))
    if engines and 'engines' not in pk:
        pk['engines'] = {'node': '>=22'}; w('package.json', json.dumps(pk, indent=2) + '\n')
    return pk
POSIX = """
Non-Windows shells (macOS, Linux, WSL): the same commands without the `.cmd` suffix:

```bash
npm ci
npm run install:all
npm test
npm run build
```
"""

# ---------------------------------------------------------------- j4 (Java quiz bank)
S = 'j4'; os.chdir(fe.REG[S]['abs']); done = []
if not os.path.exists('astraupskill/08-PORT-TO-THE-WEB.md'):
    fe.rw('test/quiz/QuestionBankTest.java', lambda t: t.replace('CafÃ©', 'Café'))
    done.append('review#4 the mojibake CafÃ© literal in QuestionBankTest.java is now Café')
    fe.rw('run.ps1', lambda t: t if '$compiler' in t else t.replace("$ErrorActionPreference = 'Stop'\n", "$ErrorActionPreference = 'Stop'\n$compiler = if ($env:JAVA_HOME) { Join-Path $env:JAVA_HOME 'bin/javac.exe' } else { (Get-Command javac -ErrorAction Stop).Source }\n$runtime = Join-Path (Split-Path $compiler) 'java.exe'\n", 1).replace('& javac --release 17', '& $compiler --release 17', 1).replace('& java -cp $buildPath quiz.QuestionBankTest', '& $runtime -cp $buildPath quiz.QuestionBankTest', 1).replace('& java -cp $buildPath quiz.App', '& $runtime -cp $buildPath quiz.App', 1))
    fe.append_section(S, '04', '## Without PowerShell', """```bash
    javac --release 17 -Xlint:all -d out $(find src/quiz test/quiz -name '*.java')
    java -cp out quiz.QuestionBankTest        # the tests; or: java -cp out quiz.App data/questions.txt
    ```""", before='## Investigate a stale-save report')
    done.append('review#3 run.ps1 falls back to $env:JAVA_HOME/bin/javac like j5; 04 has the two-line javac/java invocation for other shells')
    fe.append_section(S, '07', '## Expected results for the end-of-input cases', """Fill your own table first, then compare. With `data/questions.txt` copied to a scratch file (three questions Q1-Q3):

    | case | planned | answered | correct | incorrect | unanswered | bank file |
    |---|---|---|---|---|---|---|
    | input ends halfway through a create form | - | - | - | - | - | byte-identical to before ("not applied" is printed, nothing was committed) |
    | input ends during a quiz after answering Q1 correctly and Q2 incorrectly | 3 | 2 | 1 | 1 | 1 | unchanged (a quiz never writes) |
    | input ends before the first answer | 3 | 0 | 0 | 0 | 3 | unchanged |

    Unanswered questions are not `QuestionAttempt`s: an attempt records a chosen letter, and there is none. They are not automatically wrong either; "wrong" is a comparison between a choice and the answer, and there is no choice. That is why the result reports five numbers rather than a score.""", before='## ')
    done.append('review#2 07 expected-results table for the EOF cases')
    w('astraupskill/08-PORT-TO-THE-WEB.md', """# 08. Port `QuestionBank.commit` to the web

    [Course index](README.md)

    `commit` gives three guarantees: an id is unique in the bank, a save based on a stale snapshot is refused, and memory is published only after the file is durably replaced. Here is the same contract as an Express route over SQLite, then the one SQL statement that carries the stale check.

    ## The route

    ```ts
    import express from 'express';
    import { DatabaseSync } from 'node:sqlite';
    const db = new DatabaseSync('bank.sqlite');
    db.exec(`CREATE TABLE IF NOT EXISTS questions (id TEXT PRIMARY KEY, prompt TEXT NOT NULL, choices TEXT NOT NULL, answer TEXT NOT NULL, explanation TEXT NOT NULL, version INTEGER NOT NULL DEFAULT 1)`);
    const app = express(); app.use(express.json({ limit: '64kb' }));

    app.post('/questions', (req, res) => {
      const q = validateQuestion(req.body);                       // the same rules as the Question constructor
      try {
        db.prepare('INSERT INTO questions (id, prompt, choices, answer, explanation) VALUES (?, ?, ?, ?, ?)')
          .run(q.id, q.prompt, JSON.stringify(q.choices), q.answer, q.explanation);
      } catch (error) {
        if (String(error.message).includes('UNIQUE')) return res.status(409).json({ error: 'Duplicate question id.' });   // guarantee 1
        throw error;
      }
      res.status(201).set('ETag', '"1"').json({ ...q, version: 1 });
    });

    app.put('/questions/:id', (req, res) => {
      const match = /^"(\\d+)"$/.exec(req.get('if-match') ?? '');
      if (!match) return res.status(428).json({ error: 'Send If-Match with the version you loaded.' });
      const q = validateQuestion({ ...req.body, id: req.params.id });
      const result = db.prepare('UPDATE questions SET prompt = ?, choices = ?, answer = ?, explanation = ?, version = version + 1 WHERE id = ? AND version = ?')
        .run(q.prompt, JSON.stringify(q.choices), q.answer, q.explanation, q.id, Number(match[1]));   // guarantee 2
      if (result.changes === 0) {
        const exists = db.prepare('SELECT 1 FROM questions WHERE id = ?').get(q.id);
        return exists ? res.status(409).json({ error: 'Question bank changed. Reload before saving; your edit was not applied.' })
                      : res.status(404).json({ error: 'Question not found.' });
      }
      res.set('ETag', `"${Number(match[1]) + 1}"`).json({ ...q, version: Number(match[1]) + 1 });    // guarantee 3: respond after the commit
    });
    ```

    ## Mapping

    | Java `commit` | web |
    |---|---|
    | `find(id).isPresent()` before create | `PRIMARY KEY` and the `UNIQUE` failure mapped to 409 (the database does the check atomically) |
    | `Arrays.equals(original, Files.readAllBytes(file))` | `WHERE version = ?` on the `UPDATE`; `changes === 0` is the refusal |
    | `FileLock.tryLock()` | not needed: the conditional `UPDATE` is atomic; use a transaction when several rows change together |
    | temp file + `ATOMIC_MOVE` | the SQLite transaction commit |
    | `original = serialized; questions = List.copyOf(candidate)` after the move | the response is sent after `run()` returns; the client adopts the new `ETag` |

    The differences are what to notice: the file version needs a lock because compare and replace are two steps; the SQL version compares and writes in one statement. The 428 for a missing `If-Match` has no Java equivalent because the CLI always holds a snapshot.

    ## Exercise

    Write the three tests: duplicate id is 409 with one row; stale `If-Match` is 409 and the row is unchanged; a fresh `If-Match` is 200 and the `ETag` moved. Then write the same route in ASP.NET minimal API with EF Core and `[ConcurrencyCheck] int Version`.
    """)
    fe.append_section(S, '02', '## Glossary', """*Snapshot*: the bank as one file, read whole and replaced whole. *Candidate*: the next list of questions, built and validated before anything is written. *Advisory lock*: `FileLock.tryLock()` on a sibling `.lock` file; cooperating editors respect it, nothing enforces it. *Atomic replace*: write a temp file, then `ATOMIC_MOVE` over the original. *Stale write*: a commit whose `original` bytes no longer match the file. *Publication*: assigning `questions` and `original` only after the move succeeded. *Aggregate*: the whole bank treated as one unit of consistency. *Baseline*: the bytes last read (`original`). *Identity check*: an id must be unique and an update cannot change it. *Serialization*: the tab-separated format with `END` footer and count. *Footer*: the last line that lets a truncated file be detected. *Attempt*: a recorded answer in a quiz; unanswered is not an attempt. *EOF*: the input ending; a half-typed command is discarded. *Escape*: `encode`/`unpack` turning tabs and newlines into literals. *ETag / If-Match*: the web equivalents of the baseline (see 08).""")
    done.append('review#1 08-PORT-TO-THE-WEB.md (Express + SQLite route, UPDATE ... WHERE version, 409/428 mapping table, exercise); review#5 02 glossary (15 terms)')
    finish(S, done)

# ---------------------------------------------------------------- j7 (Java order management)
S = 'j7'; os.chdir(fe.REG[S]['abs']); done = []
os.makedirs('data/sample', exist_ok=True); os.makedirs('data/sample-corrupt', exist_ok=True)
sample = """# oms-snapshot-v1
C|c-100|Ada Lovelace|ada@example.com|555-0100|2026-01-05T09:00
C|c-101|Grace Hopper|grace@example.com|555-0101|2026-01-06T09:30
P|p-200|Notebook|NB-001|10.00|true
P|p-201|Pen|PN-002|2.50|true
P|p-202|Desk lamp|DL-003|35.00|true
O|o-300|c-100|DRAFT|5.00|2026-02-01T10:00|2026-02-01T10:05
I|o-300|p-200|Notebook|2|10.00
O|o-301|c-101|PAID|0.00|2026-02-02T11:00|2026-02-02T11:30
I|o-301|p-201|Pen|4|2.50
I|o-301|p-202|Desk lamp|1|35.00
END|2|3|2|3
"""
w('data/sample/oms.snapshot.txt', sample)
w('data/sample-corrupt/oms.snapshot.txt', sample.replace('END|2|3|2|3', 'END|2|3|2|2'))
w('data/sample/README.md', '# Sample data\n\n`data/sample/` loads a snapshot with two customers, three products, one DRAFT order with a 5.00 discount and one PAID order. `data/sample-corrupt/` is the same file with a wrong item count in the footer, so the loader refuses it ("Missing footer or incorrect record counts"). Run `./run.ps1 -DataPath data/sample` (copy the directory first if you intend to save).\n')
fe.rw('astraupskill/07-TRACE-LAB.md', lambda t: t.replace('# ', '# ', 1) if 'Predict, run, reveal' in t else t.replace('\n## ', '\n## Predict, run, reveal\n\nStart from `data/sample` (copy it first): the DRAFT order `o-300` for Ada already has 2 notebooks at 10.00 and a 5.00 discount, so the lab begins at the interesting state instead of at data entry. For every step below, write your predicted figure *before* running; the figures quoted in the steps are the reveal. If you prefer not to see them, read the steps with the numbers covered and check the answers section at the end.\n\n## ', 1))
figs = re.findall(r'[^.\n]*\b\d+\.\d\d\b[^.\n]*\.', rd('astraupskill/07-TRACE-LAB.md'))
fe.rw('astraupskill/07-TRACE-LAB.md', lambda t: t.rstrip('\n') + '\n\n<details>\n<summary>Answers: the expected figures, collected</summary>\n\n' + '\n'.join(f'- {f.strip()}' for f in figs[:12]) + '\n\n</details>\n')
done.append('review#2 data/sample (2 customers, 3 products, DRAFT order with discount, PAID order) and data/sample-corrupt (bad footer count); review#3 07 opens with predict-run-reveal from the sample and ends with a collapsed answers section')
fe.append_section(S, '04', '## Without PowerShell', """```bash
javac --release 17 -Xlint:all -d out $(find src test -name '*.java')
java -cp out oms.RegressionTests            # tests
java -cp out oms.App data/sample            # the app against the sample directory
```""", before='## ')
done.append('review#5 04 non-PowerShell run path')
w('astraupskill/08-THE-SAME-ORDER-IN-CSHARP.md', """# 08. The same order in C# and EF Core

[Course index](README.md)

## Entities

```csharp
public enum OrderStatus { Draft, Submitted, Paid, Shipped, Cancelled }

public sealed class Order
{
    public string Id { get; private set; } = default!;
    public string CustomerId { get; private set; } = default!;
    public OrderStatus Status { get; private set; }
    public decimal DiscountAmount { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public DateTime UpdatedAt { get; private set; }
    [ConcurrencyCheck] public int Version { get; private set; }
    private readonly List<OrderItem> _items = new();
    public IReadOnlyList<OrderItem> Items => _items;          // the aggregate root owns its lines
    public decimal Subtotal => _items.Sum(i => i.LineTotal);
    public decimal Total => Math.Max(0, Subtotal - DiscountAmount);
}

[Owned] public sealed class OrderItem                            // owned: no identity outside its order
{
    public string ProductId { get; private set; } = default!;
    public string ProductName { get; private set; } = default!;   // price snapshot: copied at add time
    public int Quantity { get; private set; }
    public decimal UnitPrice { get; private set; }               // never re-read from Product
    public decimal LineTotal => UnitPrice * Quantity;
}
```

`modelBuilder.Entity<Order>().OwnsMany(o => o.Items, b => { b.ToTable("OrderItems"); b.WithOwner().HasForeignKey("OrderId"); b.Property(i => i.UnitPrice).HasPrecision(18, 2); });` and `Property(o => o.DiscountAmount).HasPrecision(18, 2)`.

## The restoration bug, reproduced

The bug Astra fixed was an order restored from disk without its items and then re-saved, silently dropping lines. In EF Core the same bug is one missing `Include`:

```csharp
var order = await db.Orders.SingleAsync(o => o.Id == id);        // Items not loaded: the list is empty
order.ApplyDiscount(5m);
await db.SaveChangesAsync();                                      // owned collection: nothing deleted, but Subtotal was computed as 0
```

With an owned collection EF will not delete the rows, but every rule that reads `Items` (subtotal, "cannot submit an empty order") runs against an empty list. The fix is the same as in Java: load the aggregate whole (`db.Orders.Include(o => o.Items)`), or better, a repository method `LoadOrder(id)` that always includes, so no caller can forget.

## Refusals mapped to HTTP

| rule in `OrderService` | C# | status |
|---|---|---|
| discount larger than subtotal | `throw new DomainException(...)` from `ApplyDiscount` | 422 |
| quantity change on a non-DRAFT order | `if (Status != OrderStatus.Draft) throw ...` | 409 |
| terminal status transition (`PAID -> DRAFT`) | `OrderStatus.CanTransitionTo` table, refused | 409 |
| stale save | `DbUpdateConcurrencyException` from `[ConcurrencyCheck]` | 409 |
| unknown product or customer | `FirstOrDefaultAsync` returns null | 404 |
| body fails validation | `ValidationProblem` | 400 |

## Exercise

Write the test that loads an order without `Include`, applies a discount, saves, reloads with `Include`, and asserts the items are still there and the total is right; then break it by making `Items` a plain (non-owned) navigation with `DeleteOrphans` semantics and watch what changes.
""")
fe.append_section(S, '02', '## Glossary', """*Aggregate*: the order and its lines as one unit of change. *Aggregate root*: the object (Order) through which every change to the lines must go. *Detached read*: a copy handed out for reading that cannot change the stored state. *Invariant*: a rule that must hold after every operation (total never negative, no lines on a non-draft order change). *Price snapshot*: the unit price and name copied into the line when it was added, so later catalog edits do not rewrite history. *Terminal status*: a status with no allowed transitions out of it (CANCELLED, SHIPPED). *Owned entity*: the C# way of saying a line has no identity outside its order (see 08).""")
done.append('review#1 08-THE-SAME-ORDER-IN-CSHARP.md (entities with owned line snapshot, the missing-Include restoration bug, refusal-to-status table); review#4 02 glossary')
finish(S, done)

# ---------------------------------------------------------------- job-track-task-queue-system
S = 'job-track-task-queue-system'; os.chdir(fe.REG[S]['abs']); done = []
w('docker-compose.yml', "services:\n  redis:\n    image: redis:7-alpine\n    ports:\n      - \"6379:6379\"\n    command: [\"redis-server\", \"--save\", \"\", \"--appendonly\", \"no\"]\n")
pk = node_pins()
pk['scripts']['redis:up'] = 'docker compose up -d redis'; pk['scripts']['redis:down'] = 'docker compose down'
w('package.json', json.dumps(pk, indent=2) + '\n')
fe.append_section(S, 'README', '## Running the Redis half', """The tests need no Redis. The application (`npm run dev`: API, worker, client) does. Start a disposable one:

```powershell
npm run redis:up      # docker compose up -d redis  (redis:7-alpine on 6379, no persistence)
npm run redis:down
```

**No Docker on Windows?** Two realistic alternatives: Redis under WSL2 (`wsl sudo apt install redis-server && wsl redis-server --port 6379`), or [Memurai](https://www.memurai.com/) (a native Windows Redis-compatible server; the free Developer edition is enough). Either way the API and worker connect to `127.0.0.1:6379` by default.""" + POSIX, before='## What the delivery changes')
fe.append_section(S, 'README', '## Prerequisites', """This is the hardest course in the job-track set. Do `restaurant-kitchen-display-system` first (single-database transactions, the outbox idea in one process), and be comfortable with `db.transaction` in better-sqlite3, HTTP status semantics (400/409/503), and React effects with cleanup. Node 22 (`.nvmrc`).""", before='## Course route')
done.append('review#1 docker-compose.yml (redis:7-alpine) + redis:up/down scripts + README Docker-alternatives paragraph; review#2 README prerequisites (kitchen course first, hardest course); review#5 .nvmrc, engines, POSIX block')
fe.append_section(S, '05', '## 7. Bound the outbox and the broker history', """`queue_outbox` (`server/src/lib/outbox.js`) keeps every dispatched row forever, and `stageQueueJob` sets `removeOnComplete: false, removeOnFail: false` so BullMQ keeps every job too. Add retention: delete or archive `queue_outbox` rows with `dispatched_at` older than N days, and give the queue a `removeOnComplete: { age: 24 * 3600, count: 1000 }` policy (see `server/src/queues/index.js` for the shape used elsewhere). Then argue, in writing, why an outbox row may be deleted only after the broker has acknowledged the job (`dispatched_at` set) and never before: the row *is* the retry intent, and deleting it before the ack turns a lost acknowledgement into a lost job. Test: a row with `dispatched_at = NULL` older than N days survives the cleanup; a dispatched one older than N days does not; the tracking rows are untouched.""", before='## ')
done.append('review#3 05 exercise 7: outbox retention + removeOnComplete policy with the delete-only-after-ack argument')
fe.append_section(S, '04', '## Which tests are regressions, and which are specifications', """Two of the nineteen tests are true regressions: they were run against the old code and failed there (VERIFICATION): `validation failure returns null after writing the error response` and `unavailable queue keeps dispatch intent and campaign tracking for retry`. The other seventeen were written alongside the new outbox, dispatcher and worker and describe the intended behavior; they never had an old implementation to fail against. The distinction matters for what a green test proves: a regression test proves a bug is gone; a specification test proves the code matches the author's understanding, which may share the author's blind spots. When you add a test, say which kind it is in its name or a comment.""", before='## Run a focused scenario')
done.append('review#4 04 marks the two regressions versus the seventeen specification tests')
n = strip_bom(); done.append(f'review#5 UTF-8 BOM stripped from {n} course files')
finish(S, done)

# ---------------------------------------------------------------- job-track-live-chat-support-platform
S = 'job-track-live-chat-support-platform'; os.chdir(fe.REG[S]['abs']); done = []
def sock(t):
    old = """      const target = db.prepare('SELECT rowid AS sequence, created_at FROM messages WHERE id = ? AND room_id = ?')
        .get(payload.uptoMessageId, payload.roomId);
      if (!target) return reject(ack, 'Message not found in this room');
      const rows = db.prepare(`SELECT id FROM messages WHERE room_id = ?
        AND (created_at < ? OR (created_at = ? AND rowid <= ?))`)
        .all(payload.roomId, target.created_at, target.created_at, target.sequence);
      const now = new Date().toISOString();
      db.transaction(() => { for (const row of rows) markRead.run(row.id, state.userId, now); })();"""
    new = """      // The range read and the receipt writes are one transaction: a message committed by another
      // connection between them cannot be missed or half-marked (the seventh defect in chapter 03).
      const marked = db.transaction(() => {
        const target = db.prepare('SELECT rowid AS sequence, created_at FROM messages WHERE id = ? AND room_id = ?')
          .get(payload.uptoMessageId, payload.roomId);
        if (!target) return null;
        const rows = db.prepare(`SELECT id FROM messages WHERE room_id = ?
          AND (created_at < ? OR (created_at = ? AND rowid <= ?))`)
          .all(payload.roomId, target.created_at, target.created_at, target.sequence);
        const now = new Date().toISOString();
        for (const row of rows) markRead.run(row.id, state.userId, now);
        return rows.length;
      })();
      if (marked === null) return reject(ack, 'Message not found in this room');"""
    assert old in t, 'mark_read block not found'
    return t.replace(old, new, 1)
fe.rw('server/src/socket.js', sock)
def t14(t):
    add = """
test('read-through computes its range inside the transaction: a message committed afterwards with an earlier timestamp is not marked', async () => {
  const socket = await client(); await join(socket);
  const sender = randomUUID(); ensureUser(sender, 'Other Person', 'customer');
  const insert = db.prepare('INSERT INTO messages (id, room_id, sender_id, content, created_at) VALUES (?, ?, ?, ?, ?)');
  const first = randomUUID(), target = randomUUID(), late = randomUUID();
  insert.run(first, roomId, sender, 'first', '2026-01-01T00:00:01.000Z');
  insert.run(target, roomId, sender, 'target', '2026-01-01T00:00:02.000Z');
  await next(socket, ['read_update'], () => socket.emit('mark_read', { roomId, userId: user.userId, uptoMessageId: target }));
  // Committed after the read-through, backdated before the target: it was not part of the range the transaction saw.
  insert.run(late, roomId, sender, 'late', '2026-01-01T00:00:00.500Z');
  const receipts = db.prepare('SELECT message_id FROM read_receipts WHERE user_id = ?').all(user.userId).map(row => row.message_id);
  assert.deepEqual(new Set(receipts), new Set([first, target]));
  // A second read-through up to the same target now includes it: the range is computed fresh each time.
  await next(socket, ['read_update'], () => socket.emit('mark_read', { roomId, userId: user.userId, uptoMessageId: target }));
  const again = db.prepare('SELECT message_id FROM read_receipts WHERE user_id = ?').all(user.userId).map(row => row.message_id);
  assert.deepEqual(new Set(again), new Set([first, target, late]));
});
"""
    return t.rstrip('\n') + '\n' + add
fe.rw('test/socket.test.cjs', t14)
fe.append_section(S, '03', '## A seventh defect, found while writing this course', """The delivered `mark_read` handler read the target row and the range of earlier messages *outside* the transaction and only wrapped the receipt inserts. Between the range read and the inserts another connection could commit a message that belonged in the range (same room, earlier or equal timestamp), and the loop would never mark it; the acknowledgement would still say "read up to here". The fix pass moves the two reads and the writes into one `db.transaction` (`server/src/socket.js`, the `marked` block), so the range and the receipts are computed against the same committed state, and a fourteenth test pins the boundary: a message committed after the read-through with an earlier timestamp is not marked by that read-through, and is marked by the next one. better-sqlite3 transactions are synchronous, so in one process the interleaving cannot happen; the boundary matters the moment a second process (a worker, a migration) writes to the same file. A course that finds a bug in its own fix is telling you the truth about how bugs work.""", before='## ')
done.append('review#1 mark_read range read + receipt writes are one db.transaction; 14th test pins the read-through boundary; 03 documents it as the seventh defect')
n = strip_bom(); pk = node_pins()
pk['scripts']['reset:db'] = 'node -e "for (const f of [\'server/data/chat.db\',\'server/data/chat.db-wal\',\'server/data/chat.db-shm\']) require(\'fs\').rmSync(f, { force: true }); console.log(\'chat.db removed; the server recreates an empty database on start\')"'
w('package.json', json.dumps(pk, indent=2) + '\n')
fe.append_section(S, 'README', '## Start the trace lab from an empty database', """The committed `server/data/chat.db` carries whatever the last session left. Run `npm run reset:db` (deletes `chat.db` and its `-wal`/`-shm` files; the server recreates the schema on start) before `07-TRACE-LAB.md`, so the sequence numbers and presence counts you record are yours.""" + POSIX, before='## Delivered behavior and boundaries')
fe.append_section(S, 'README', '## Before you start', """Do `restaurant-kitchen-display-system` (transactions, outbox) and `task-queue-system` (dispatch intent, acknowledgement loss) first; this course assumes both. Node 22 (`.nvmrc`).""", before='## Course route')
fe.append_section(S, '02', '## Glossary', """*Presence reference*: the count of open connections behind one user; the user is present while it is above zero. *Connection identity*: the user a socket was bound to at join; it cannot be changed by a later payload. *Ordering barrier*: the rule that a message is broadcast only after its transaction committed. *Read-through*: marking every message up to a target as read in one operation. *Tie-breaker*: `rowid` deciding order between messages with the same `created_at`. *Ack*: the callback that tells the sender whether the server accepted the event. *Idempotency key*: a client-chosen id that makes a retried send safe (practice exercise). *Cursor*: the (timestamp, rowid) pair a page continues from. *Receipt*: the `read_receipts` row for one user and one message. *Room*: the conversation a socket joined; also the broadcast target. *Agent room*: the `agents` broadcast group for staff notifications. *Validation before mutation*: parsing the payload with the schema before any state changes. *Committed state*: what a transaction has made durable; the only thing the server broadcasts. *Range read*: the query that selects the messages a read-through covers. *Backdated message*: a row whose `created_at` is earlier than its commit time; the reason the range read belongs in the transaction. *Demo identity*: the name/role pair used instead of authentication in this project. *Attachment policy*: allowed URL schemes and size for message attachments. *Reconnect*: a new socket for the same identity; presence must not double-count it. *WAL*: SQLite's write-ahead log, the `-wal`/`-shm` files next to `chat.db`. *Reset*: `npm run reset:db`, an empty database for the trace lab.""")
done.append(f'review#2 UTF-8 BOM stripped from {n} files; review#3 .nvmrc, engines, POSIX block; review#4 02 glossary (20 terms) and README prerequisite gate; review#5 npm run reset:db and the README note')
finish(S, done)

# ---------------------------------------------------------------- astra2
S = 'astra2'; os.chdir(fe.REG[S]['abs']); done = []
eng = rd('tests/engine.test.ts')
m = re.search(r'^\s*it\.skipIf\(!existsSync\(\'artifacts/late-game-save\.json\'\)\).*$', eng, re.M)
if m:
    fe.rw('tests/engine.test.ts', lambda t: t.replace(m.group(0) + '\n', '', 1))
    w('tests/late-game.fixture.test.ts', """import { describe, expect, it } from 'vitest';
import { existsSync, readFileSync } from 'node:fs';
import { parseSave } from '../src/save';

// Fixture-gated: this case needs artifacts/late-game-save.json, which tests/progression.test.ts writes when it
// reaches victory. It runs only through `npm run test:fixture`, so the counted suite has no conditional.
describe('late-game fixture', () => {
  it('accepts the previously exported earned late-game fixture', () => {
    if (!existsSync('artifacts/late-game-save.json')) throw new Error('Run `npm test` first: progression.test.ts regenerates artifacts/late-game-save.json');
    const s = parseSave(readFileSync('artifacts/late-game-save.json', 'utf8'));
    expect(s.victory).toBe(true);
    expect(s.ships).toHaveLength(6);
    expect(s.islands.filter((i) => i.settled).reduce((n, i) => n + i.buildings.length, 0)).toBe(101);
  });
});
""")
    imp = re.search(r"import \{[^}]*parseSave[^}]*\} from '([^']+)'", eng)
    if imp: fe.rw('tests/late-game.fixture.test.ts', lambda t: t.replace("from '../src/save'", f"from '{imp.group(1)}'", 1))
    fe.rw('vitest.config.ts', lambda t: t.replace("include: ['tests/**/*.test.ts'],", "include: ['tests/**/*.test.ts'],\n    exclude: ['**/node_modules/**', 'tests/late-game.fixture.test.ts'],   // fixture-gated case runs via npm run test:fixture", 1))
    w('vitest.fixture.config.ts', "import { defineConfig } from 'vitest/config';\n\nexport default defineConfig({\n  test: { include: ['tests/late-game.fixture.test.ts'], maxWorkers: 1, testTimeout: 30_000 },\n});\n")
    pk = json.load(open('package.json', encoding='utf-8-sig')); pk['scripts']['test:fixture'] = 'vitest run --config vitest.fixture.config.ts'; w('package.json', json.dumps(pk, indent=2) + '\n')
    fe.rw('astraupskill/VERIFICATION.md', lambda t: t.replace('| Current unit/domain suite | 44 of 44 passed; four test files; process exit 0 |', '| Current unit/domain suite | 43 unconditional cases passed (four test files, exit 0) + 1 fixture-gated case run separately by `npm run test:fixture` (it needs `artifacts/late-game-save.json`, which the progression test regenerates) |', 1))
    done.append('review#2 the fixture-gated late-game case moved to tests/late-game.fixture.test.ts, excluded from the default run and executed by npm run test:fixture; VERIFICATION restates 43 unconditional + 1 fixture-gated')
w('astraupskill/08-THE-SAME-REPOSITORY-BEHIND-AN-API.md', """# 08. The same repository behind an API

[Course index](README.md)

`src/voyages.ts` already has the right shape: a repository with `list`, `read`, `create`, `edit(id, revision, ...)`, `archive`, `replace`, `delete`, and one error type with four codes. Only the transport is missing. Here it is as Express route handlers over SQLite; the repository semantics do not change.

## Error codes to status codes

| `VoyageError.code` | meaning in the repository | HTTP |
|---|---|---|
| `invalid` | the input failed validation before any write | 400 |
| `missing` | the id does not exist (or was deleted) | 404 |
| `conflict` | the revision the caller sent is not the current one, or a duplicate checkpoint | 409 |
| `storage` | the store is unavailable, blocked or closed | 503 (retryable), 500 if it is a bug |

One mapping function, used by every route:

```ts
function send(res: Response, error: unknown) {
  if (error instanceof VoyageError) {
    const status = { invalid: 400, missing: 404, conflict: 409, storage: 503 }[error.code];
    return res.status(status).json({ code: error.code, message: error.message });
  }
  res.status(500).json({ code: 'internal', message: 'Unexpected failure.' });
}
```

## Routes

```ts
app.get('/voyages', async (req, res) => {
  const q = String(req.query.q ?? '').trim().toLowerCase();
  const page = Math.max(1, Number(req.query.page ?? 1) || 1), size = 20;
  const all = (await repo.list()).filter((v) => !q || v.title.toLowerCase().includes(q));
  res.json({ items: all.slice((page - 1) * size, page * size), total: all.length, page, size });
});

app.get('/voyages/:id', async (req, res) => {
  try { const { voyage } = await repo.read(req.params.id); res.set('ETag', `"${voyage.revision}"`).json(voyage); }
  catch (error) { send(res, error); }
});

app.patch('/voyages/:id', express.json({ limit: '16kb' }), async (req, res) => {
  const match = /^"(\\d+)"$/.exec(req.get('if-match') ?? '');
  if (!match) return res.status(428).json({ code: 'precondition_required', message: 'Send If-Match with the revision you loaded.' });
  try {
    const voyage = await repo.edit(req.params.id, Number(match[1]), String(req.body.title ?? ''), String(req.body.notes ?? ''));
    res.set('ETag', `"${voyage.revision}"`).json(voyage);
  } catch (error) { send(res, error); }
});
```

`repo.edit` already refuses a stale revision with `conflict`; the route only carries the revision in `If-Match` instead of a form field. On SQLite the repository's IndexedDB transaction becomes `UPDATE voyages SET title = ?, notes = ?, revision = revision + 1 WHERE id = ? AND revision = ?` with `changes === 0` mapped to `conflict`.

## What stays in the browser

Validation for fast feedback, the draft kept on 409, and the "adopt only what the server returned" rule from `voyageLibrary.ts`. What moves: the size limit, the revision check and the storage failure handling, because a client can bypass all three.

## Exercise

Write the four tests (400, 404, 409, 428) with supertest against an in-memory SQLite repository that implements the same `VoyageRepository` interface, then run the existing `tests/voyages.test.ts` against your SQLite implementation: if it passes unchanged, the abstraction was right.
""")
fe.append_section(S, '01', '## About the rendering in `voyageLibrary.ts`', """`src/voyageLibrary.ts` renders with `innerHTML` and a hand-rolled `escape()`. That is a deliberate no-framework choice for this project (no build-time dependency for the UI, and the repository boundary is the lesson), and it is *not* the pattern to carry into React work: frameworks escape by default and make the escaping impossible to forget. Practice exercise 6 asks you to re-render the list with a framework while leaving `voyages.ts` untouched; if you can, the boundary was in the right place.""", before='## 5. Integration and rendering')
fe.append_section(S, '05', '## Exercise 6: re-render the library with a framework, repository untouched', """Replace the `innerHTML` rendering in `src/voyageLibrary.ts` with a component in a framework of your choice (React, Preact, Svelte) that consumes `VoyageRepository` as-is. Acceptance: `src/voyages.ts` has no diff; `tests/voyages.test.ts` passes unchanged; the conflict path still keeps the draft and shows the message; and `escape()` is deleted because the framework escapes for you. Write one paragraph on what the repository boundary bought you during the swap.""", before='## Finish with a review package')
done.append('review#1 08 chapter: Express routes over the existing repository with If-Match/428 and a code-to-status table; review#3 01 note on innerHTML + exercise 6')
fe.append_section(S, 'README', '## Time and hardware budget', """| chapter | minutes |
|---|---|
| 01 map | 40 |
| 02 concepts | 60 |
| 03 worked change | 90 |
| 04 testing | 45 |
| 05 practice | 60-90 per exercise |
| 06 solutions | 40 |
| 07 trace lab | 45 |

`npm ci` and `npm run build` take about 4 minutes together on a laptop. `npm run test:library` and `test:browser` need Chrome with WebGL2 (the game renders to a canvas); on a machine without it, skip them and rely on `npm test`. The `$env:TIDEBOUND_URL` lines in the browser checks are PowerShell; on macOS/Linux use `TIDEBOUND_URL=http://127.0.0.1:4173 npm run test:library`.""", before='## What you should know first')
ev = 'astraupskill/evidence.json'
if os.path.exists(ev):
    fe.rw(ev, lambda t: t.replace('42 exact original text snapshots', '42 original text files preserved unchanged (the originalTextFilesPreserved count)', 1))
done.append('review#4 README time/hardware budget with the POSIX env line; review#5 evidence.json summary phrase reconciled with originalTextFilesPreserved')
finish(S, done)

# ---------------------------------------------------------------- andie
S = 'andie'; os.chdir(fe.REG[S]['abs']); done = []
def cl(t):
    if 'function redact(' in t: return t
    t = t.replace("function storeName(value)", """const SECRET = /shpat_[A-Za-z0-9]+/g;
// Error detail is kept, never headers, and any token-shaped substring is masked before it can reach a log.
function redact(value) {
  if (typeof value === 'string') return value.replace(SECRET, 'shpat_[redacted]');
  if (Array.isArray(value)) return value.map(redact);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, redact(item)]));
  return value;
}
function detailed(message, details) { const error = new Error(message); error.details = redact(details); return error; }
function storeName(value)""", 1)
    old = "        throw new Error('Shopify returned GraphQL errors; no successful result was accepted.');"
    new = "        throw detailed('Shopify returned GraphQL errors; no successful result was accepted.', payload.errors.map(error => ({ message: error.message, code: error.extensions?.code ?? null })));"
    assert old in t; t = t.replace(old, new, 1)
    old = "  if (payload.userErrors.length) throw new Error('Shopify rejected the mutation with userErrors; inspect the plan and schema.');"
    new = "  if (payload.userErrors.length) throw detailed('Shopify rejected the mutation with userErrors; inspect the plan and schema.', payload.userErrors.map(error => ({ field: error.field ?? null, code: error.code ?? null, message: error.message })));"
    assert old in t; t = t.replace(old, new, 1)
    t = t.replace("module.exports = { API_VERSION, storeName,", "module.exports = { API_VERSION, redact, storeName,", 1)
    return t
fe.rw('scripts/lib/client.js', cl)
def cltest(t):
    if 'redact(' in t: return t
    add = """
test('error detail is attached and redacted, never discarded', async () => {
  const { createClient, redact } = require('../scripts/lib/client.js');
  assert.deepEqual(redact({ message: 'token shpat_abc123 leaked', nested: ['shpat_zzz'] }), { message: 'token shpat_[redacted] leaked', nested: ['shpat_[redacted]'] });
  const fetchImpl = async () => new Response(JSON.stringify({ errors: [{ message: 'Field bad shpat_secret999', extensions: { code: 'GRAPHQL_VALIDATION_FAILED' } }] }), { status: 200, headers: { 'X-Shopify-API-Version': '2026-07' } });
  const client = createClient({ store: 'demo-store', token: 'shpat_testtoken', fetchImpl });
  await assert.rejects(client.query('query { shop { id } }'), error => {
    assert.match(error.message, /GraphQL errors/);
    assert.deepEqual(error.details, [{ message: 'Field bad shpat_[redacted]', code: 'GRAPHQL_VALIDATION_FAILED' }]);
    return true;
  });
});
"""
    return t.rstrip('\n') + '\n' + add
fe.rw('test/migration.test.js', cltest)
done.append('review#2 client.js attaches redacted GraphQL error and userErrors detail (field/code/message) to thrown errors via a shared redact() that masks shpat_ tokens and never includes headers; one test added')
if not os.path.exists('.prettierrc'): w('.prettierrc', '{\n  "printWidth": 100,\n  "singleQuote": true\n}\n')
pk = json.load(open('package.json', encoding='utf-8-sig')); pk['scripts']['format:check'] = 'npx prettier --check "scripts/**/*.js" "test/**/*.js"'; pk['scripts']['format'] = 'npx prettier --write "scripts/**/*.js" "test/**/*.js"'; w('package.json', json.dumps(pk, indent=2) + '\n')
done.append('review#1 .prettierrc (100 cols, single quotes) + format / format:check scripts; planner.js, client.js and migration.test.js reformatted in the pipeline (see report)')
fe.append_section(S, '04', '## Safe error detail', """The delivered client threw one-line errors ("Shopify returned GraphQL errors") and discarded the payload's `userErrors` and `extensions.code`, which made every failure look the same. The opposite habit, attaching the whole response, leaks tokens into logs. The fix pass takes the middle: `detailed(message, details)` attaches only the fields that help (`field`, `code`, `message`), passes them through `redact()` (which masks anything shaped like `shpat_...` at any depth), and never touches headers. The trade-off is the lesson: a log line must be useful to the person debugging at 2 a.m. and harmless if the log is shared. Test both halves, as `test/migration.test.js` now does: the detail is present, and the token is not.""", before='## ')
done.append('review#2 04 "Safe error detail" section')
w('astraupskill/10-WHAT-THIS-LOOKS-LIKE-IN-A-WEB-APP.md', """# 10. What this looks like in a web app

[Course index](README.md)

The migration script's two ideas, *plan then apply* and *cursor pagination with a stall guard*, are exactly what a CRUD API needs for any bulk operation. Here they are as Express routes over a SQL table.

## Plan, then apply

```ts
// POST /migrations  -> compute a plan from source and target snapshots, store it, return it with a hash
app.post('/migrations', async (req, res) => {
  const { source, target } = parseSnapshots(req.body);                     // Zod, strict
  const operations = plan(source, target);                                  // pure, same function as the CLI
  const hash = sha256(JSON.stringify(operations));
  const id = randomUUID();
  await db.migration.create({ data: { id, hash, operations, status: 'planned' } });
  res.status(201).json({ id, hash, operations });
});

// POST /migrations/:id/apply  -> execute exactly the plan the client reviewed; 409 if it is stale
app.post('/migrations/:id/apply', async (req, res) => {
  const { hash } = z.object({ hash: z.string().length(64) }).parse(req.body);
  const claimed = await db.migration.updateMany({ where: { id: req.params.id, hash, status: 'planned' }, data: { status: 'applying' } });
  if (claimed.count === 0) return res.status(409).json({ error: 'Plan is stale or already applied. Re-plan and review again.' });
  const m = await db.migration.findUniqueOrThrow({ where: { id: req.params.id } });
  const results = [];
  for (const op of m.operations) results.push(await applyOne(op));          // each op idempotent by natural key
  await db.migration.update({ where: { id: m.id }, data: { status: 'applied', results } });
  res.json({ id: m.id, results });
});
```

The `hash` is the client saying "this is the plan I looked at"; the conditional `updateMany` on `(id, hash, status)` is the same compare-and-set as the CLI's plan file check, and it also makes a double click safe (the second claim finds `status = 'applying'` and gets 409).

## Cursor pagination with a stall guard

```ts
app.get('/entries', async (req, res) => {
  const after = req.query.after ? decodeCursor(String(req.query.after)) : null;
  const rows = await db.entry.findMany({ where: after ? { id: { gt: after.id } } : {}, orderBy: { id: 'asc' }, take: 101 });
  const page = rows.slice(0, 100);
  const next = rows.length > 100 ? encodeCursor({ id: page[page.length - 1].id }) : null;
  res.json({ items: page, next });
});
```

The client loop is the script's `pages()`: follow `next` until null, keep a `seen` set of cursors, and fail if a cursor repeats or the page count exceeds a limit. A server bug that returns the same cursor forever must be detected by the client, exactly as with Shopify.

## Exercise

Implement both routes against SQLite, then write three tests: applying with a stale hash is 409 and changes nothing; applying twice concurrently yields one 200 and one 409; a paginated read over 250 rows makes exactly three requests and stops.
""")
w('REPO-CONTENTS.md', """# Repository contents

Only these parts are the exercise: `scripts/populate-metaobjects.js` (the CLI), `scripts/lib/planner.js` and `scripts/lib/client.js` (the pure planner and the Shopify GraphQL client), `test/migration.test.js`, `fixtures/`, and the course in `astraupskill/`.

`shopify/`, `.storybook/` and `shopify/.shopify/metafields.json` are inert remnants of the original theme project. They are not read by the scripts, not covered by the tests, and not part of any chapter; ignore them.
""")
fe.rw('astraupskill/VERIFICATION.md', lambda t: t if 'backups/cf8875344b43' in t else t.replace('The delivered source contains no embedded Shopify token literals.', 'The delivered source contains no embedded Shopify token literals. **For the follow-up owner:** a copy of the original `scripts/populate-metaobjects.js` with the token literals survives at `AstraOrganized2/astra-remaining-improvements/backups/cf8875344b43/` (the review pass replaced the three literals there with a redaction marker, but the file existed with the real values before that and may exist in other copies); revoke the token in the Shopify admin regardless.', 1))
done.append('review#3 10-WHAT-THIS-LOOKS-LIKE-IN-A-WEB-APP.md (plan/apply routes with a hash compare-and-set, cursor pagination with a stall guard); review#4 REPO-CONTENTS.md; review#5 VERIFICATION names the backup location for the token revocation')
finish(S, done)

# ---------------------------------------------------------------- j5 (Java expense tracker)
S = 'j5'; os.chdir(fe.REG[S]['abs']); done = []
os.makedirs('data', exist_ok=True)
w('data/expenses.txt', "# id\ttitle\tamount\tcategory\tdate\tnote\n1\tGroceries\t42.15\tFood\t2026-03-01\tWeekly shop\n2\tBus pass\t30.00\tTransport\t2026-03-02\t\n3\tCoffee beans\t12.50\tFood\t2026-03-03\tGift for\\tthe office\n4\tElectricity\t88.20\tUtilities\t2026-03-05\tFebruary bill\n5\tNotebook\t3.99\tSupplies\t2026-03-06\t\n6\tCinema\t15.00\tLeisure\t2026-03-07\tTwo tickets\n")
w('data/corrupt-example.txt', "# id\ttitle\tamount\tcategory\tdate\tnote\n1\tGroceries\t42.15\tFood\t2026-03-01\tWeekly shop\n2\tBus pass\tthirty\tTransport\t2026-03-02\t\n")
w('data/README.md', '# Fixtures\n\n`expenses.txt` has six rows: one with an empty note (row 2 and 5) and one whose note contains an escaped tab (row 3, `Gift for\\tthe office`). `corrupt-example.txt` has a non-numeric amount on row 2, so loading it must fail without touching any existing file. Copy either before pointing the app at it.\n')
done.append('review#2 data/expenses.txt (6 rows incl. empty note and escaped tab) and data/corrupt-example.txt shipped with a README')
fe.append_section(S, '02', '## Dual write, or two-write consistency', """A *dual write* is one logical change that needs two separate durable writes: for example the expense rows in `expenses.txt` and a next-id counter kept in a second file. Two writes can fail independently, so after a crash you can have the rows without the counter (ids get reused) or the counter without the rows (ids skip). The fix is never "write more carefully"; it is to make it one write: keep both in the same file (one atomic move), or in a database, one transaction. `06-SOLUTIONS-AND-REVIEW.md` uses this term for practice exercise 2.""", before='## ')
fe.rw('astraupskill/06-SOLUTIONS-AND-REVIEW.md', lambda t: t.replace('For durable allocation, keep the saved records and next-ID metadata in the sam', 'For durable allocation (see "Dual write" in [02-CONCEPTS.md](02-CONCEPTS.md)), keep the saved records and next-ID metadata in the sam', 1))
done.append('review#3 02 defines dual write / two-write consistency; 06 links to it')
fe.append_section(S, '04', '## Without PowerShell', """```bash
javac --release 17 -Xlint:all -d out $(find src test -name '*.java')
java -cp out expensetracker.RegressionTests
```""", before='## ')
fe.rw('astraupskill/VERIFICATION.md', lambda t: t.replace('astrdocs/REMAINING_PROJECTS_IMPLEMENTATION_REPORT.md`', 'astrdocs/REMAINING_PROJECTS_IMPLEMENTATION_REPORT.md` (that report lives outside this project, in the delivery workspace; it is not needed to verify anything here: the `-Test` run above is the evidence)', 1))
done.append('review#4 04 non-Windows commands; review#5 VERIFICATION states that the astrdocs report lives outside the project')
w('astraupskill/08-SAME-RULES-IN-EXPRESS.md', """# 08. The same rules in Express

[Course index](README.md)

`ExpenseManager.updateExpense` builds a valid replacement before touching the list, and `ExpenseFileStorage.save` serializes a snapshot to a temp file and moves it atomically. In TypeScript + Express + SQLite the validation becomes a Zod schema and the atomic move becomes a transaction; the rules do not change. About sixty lines:

```ts
import express from 'express';
import { z } from 'zod';
import { DatabaseSync } from 'node:sqlite';

const db = new DatabaseSync('expenses.sqlite');
db.exec(`CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, title TEXT NOT NULL, amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
  category TEXT NOT NULL, date TEXT NOT NULL, note TEXT NOT NULL DEFAULT '', version INTEGER NOT NULL DEFAULT 1)`);

const money = z.string().regex(/^\\d+(\\.\\d{1,2})?$/, 'Amount must use at most 2 decimal places.').transform((s) => Math.round(Number(s) * 100)).refine((c) => c > 0, 'Amount must be greater than zero.');
const day = z.string().regex(/^\\d{4}-\\d{2}-\\d{2}$/).refine((s) => !Number.isNaN(Date.parse(s)) && new Date(s).toISOString().startsWith(s), 'Date must be a real calendar day.');
const expenseBody = z.object({ title: z.string().trim().min(1).max(120), amount: money, category: z.string().trim().min(1).max(60), date: day, note: z.string().max(500).default('') }).strict();

const app = express(); app.use(express.json({ limit: '16kb' }));

app.put('/expenses/:id', (req, res) => {
  const id = Number(req.params.id);
  if (!Number.isInteger(id) || id < 1) return res.status(400).json({ error: 'Invalid id.' });
  const parsed = expenseBody.safeParse(req.body);                                  // parseAmount/parseDate, as one schema
  if (!parsed.success) return res.status(400).json({ error: parsed.error.issues[0].message });
  const expected = Number(req.get('if-match')?.replace(/"/g, ''));                 // exercise 4's version, as a header
  if (!Number.isInteger(expected)) return res.status(428).json({ error: 'Send If-Match with the version you loaded.' });
  const e = parsed.data;
  const result = db.prepare('UPDATE expenses SET title = ?, amount_cents = ?, category = ?, date = ?, note = ?, version = version + 1 WHERE id = ? AND version = ?')
    .run(e.title, e.amount, e.category, e.date, e.note, id, expected);          // the atomic move, as one statement
  if (result.changes === 0) {
    return db.prepare('SELECT 1 FROM expenses WHERE id = ?').get(id)
      ? res.status(409).json({ error: 'Expense changed since you loaded it. Reload and retry.' })
      : res.status(404).json({ error: `Expense #${id} does not exist.` });
  }
  res.status(204).set('ETag', `"${expected + 1}"`).end();
});

app.delete('/expenses/:id', (req, res) => {
  const result = db.prepare('DELETE FROM expenses WHERE id = ?').run(Number(req.params.id));
  res.status(result.changes ? 204 : 404).end();
});
```

## Mapping

| Java | Express |
|---|---|
| `parseAmount` (scale 2, positive) and `parseDate` | the `money` and `day` schemas; `.strict()` refuses unknown fields the CLI could never send |
| "build a valid replacement before touching the live collection" | `safeParse` before `UPDATE`; a 400 touches nothing |
| `NoSuchElementException` | 404 after a `changes === 0` that is not a version conflict |
| `save`: snapshot, temp file, `ATOMIC_MOVE` | the single `UPDATE` inside SQLite's implicit transaction; several rows would be `BEGIN IMMEDIATE ... COMMIT` |
| (practice exercise 4) optimistic concurrency | `If-Match` + `WHERE version = ?`, 409 on `changes === 0` |
| the CLI's confirmation prompt before delete | nothing: the server cannot rely on a client prompt; authorization goes here instead |

## Exercise

Write the four tests: invalid amount is 400 and the row is unchanged; unknown id is 404; stale `If-Match` is 409; a good update is 204 and the `ETag` moved. Then load `data/expenses.txt` into the table with one script and prove the escaped-tab note round-trips.
""")
done.append('review#1 08-SAME-RULES-IN-EXPRESS.md: ~60-line Express + SQLite port with Zod, 400/404/409/428/204 and the mapping table')
finish(S, done)

# ---------------------------------------------------------------- job-track-restaurant-kitchen-display-system
S = 'job-track-restaurant-kitchen-display-system'; os.chdir(fe.REG[S]['abs']); done = []
n = strip_bom(); node_pins()
fe.rw('astraupskill/README.md', lambda t: t.replace("The API defaults to port 4300. Check the client package's dev script and its environment example for the browser URL; the API's default allowed client origin is `http://localhost:5177`.", "The API defaults to port 4300. The client dev server runs on port 5177 (`client/package.json`: `vite --port 5177`), so the browser URL is `http://localhost:5177`, which is also the API's default allowed origin.", 1))
fe.append_section(S, 'README', '## Prerequisites', """SQL aggregates (`COUNT`, `GROUP BY` for the board summary), React effect cleanup (the socket subscription), and Zod basics (`safeParse`, `issues`). Node 22 (`.nvmrc`).""" + POSIX, before='## Start here')
fe.append_section(S, '04', '## Without `.cmd`', """```bash
npm ci && npm run install:all
npm test            # server tests, KDS_DB_PATH=:memory:
```""", before='## Run the smallest useful scenario')
done.append(f'review#1 .nvmrc, engines, POSIX blocks in README and 04; review#3 UTF-8 BOM stripped from {n} files; review#4 README states port 5177 and the URL literally; review#5 README prerequisites')
api = rd('server/src/routes/api.js').replace('\r\n', '\n').split('\n')
a = next(i for i, l in enumerate(api) if "router.patch('/orders/:orderId/priority'" in l)
snippet = '\n'.join(api[a:a + 14])
fe.append_section(S, '02', '## The check that is outside the transaction', f"""`server/src/routes/api.js:{a + 1}`:

```js
{snippet}
```

The `SELECT id FROM orders WHERE id = ?` that produces the 404 runs *before* `db.transaction`. Write the interleaving: request A reads the row (exists); a delete or a shift-close removes the order; request A's transaction then updates zero rows and still answers 200 with whatever it read afterwards. With better-sqlite3 in one process the window is tiny, but it is a window, and the same shape in a multi-process service is a real bug. The fix is not to move the `SELECT` inside (that only shrinks the window); it is to make the write conditional and read its row count: `UPDATE orders SET priority = ?, updated_at = ? WHERE id = ? AND updated_at = ?` with the `updated_at` the client loaded, `changes === 0` meaning "gone or changed", then decide 404 versus 409 with one more read. That is practice exercise 7.

## Glossary

*Aggregate summary*: the counts per station and status the board shows, computed by `GROUP BY`, never stored. *Audit event*: the row that records who changed what, written in the same transaction. *86*: the kitchen word for "no longer available"; `is_eighty_sixed` marks the items it affected. *Terminal state*: a status with no transitions out (served, cancelled). *Best-effort notification*: a socket emit after commit that may be lost; the database row is the truth. *Outbox*: the row that turns a best-effort notification into a retried one (capstone). *Compare-and-set*: an update whose `WHERE` carries the value the client last saw (exercise 7).""", before='## Parent state is a derived business rule')
fe.append_section(S, '05', '## 7. Make the priority change a compare-and-set', """Starting state: `PATCH /orders/:orderId/priority` checks existence outside the transaction (02, "The check that is outside the transaction"). Change the route so the client sends the `updated_at` it loaded (body field or `If-Unmodified-Since`), the `UPDATE` carries `AND updated_at = ?`, and `changes === 0` becomes 404 when the row is gone and 409 when it changed. Acceptance: a test that updates the row's `updated_at` between the client's read and its PATCH gets 409 and the priority is unchanged; a test that deletes the order in between gets 404; the existing priority tests still pass; the audit row is written only on the 200 path.""", before='## ')
done.append(f'review#2 02 "The check that is outside the transaction" quotes api.js:{a + 1} and asks for the interleaving; 05 exercise 7 implements the updated_at compare-and-set')
finish(S, done)
