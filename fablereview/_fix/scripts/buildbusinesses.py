import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'buildbusinesses'; P = fe.REG[S]['abs']; os.chdir(P); done = []
def src(path):
    return open(path, encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
def block(lines, start_pat, end_pat=None, extra=0, limit=90):
    a = next(i for i, l in enumerate(lines) if re.search(start_pat, l))
    if end_pat:
        b = next(i for i in range(a + 1, len(lines)) if re.search(end_pat, lines[i])) + extra
    else:
        b = a + extra
    return a + 1, '\n'.join(lines[a:min(b, a + limit)])

# --- review#3: Ticket 1 worked solution, end to end
open('src/lib/contact-filter.ts', 'w', encoding='utf-8', newline='\n').write('''import type { Workspace } from "./ledger-schema";

export type Contact = Workspace["contacts"][number];
export type ContactRole = Contact["role"];
export const CONTACT_ROLES = ["customer", "supplier", "helper", "lender", "other"] as const satisfies readonly ContactRole[];

/**
 * Derived presentation: the rows the People table shows for a role and a literal query.
 * The query is plain text (no pattern engine): "[" and ".*" match themselves.
 * The accepted collection stays the only source of truth; nothing here is persisted.
 */
export function matchContacts(contacts: readonly Contact[], role: ContactRole | "all", query: string): Contact[] {
  const needle = query.toLocaleLowerCase("en-US");
  return contacts.filter(
    (c) =>
      (role === "all" || c.role === role) &&
      Object.values(c).some((value) => String(value).toLocaleLowerCase("en-US").includes(needle)),
  );
}

/** Clamp a 1-based page into the range the current match count allows. */
export function clampPage(page: number, count: number, pageSize = 12): { pageCount: number; currentPage: number } {
  const pageCount = Math.max(1, Math.ceil(count / pageSize));
  return { pageCount, currentPage: Math.min(Math.max(1, page), pageCount) };
}
''')
comp = 'src/components/LocalOperationsApp.tsx'
def component(t):
    imp = 'import { type Command, totals } from "@/lib/ledger-domain";'
    assert imp in t
    t = t.replace(imp, imp + '\nimport { CONTACT_ROLES, clampPage, matchContacts, type ContactRole } from "@/lib/contact-filter";', 1)
    old = '    [page, setPage] = useState(1),'
    assert old in t
    t = t.replace(old, old + '\n    [role, setRole] = useState<ContactRole | "all">("all"),', 1)
    old = '''  const matching =
    workspace && entity
      ? workspace[entity].filter((row) =>'''
    new = '''  const matching =
    workspace && entity === "contacts"
      ? matchContacts(workspace.contacts, role, query)
      : workspace && entity
      ? workspace[entity].filter((row) =>'''
    assert old in t
    t = t.replace(old, new, 1)
    old = '''  const pageCount = Math.max(1, Math.ceil(matching.length / 12)),
    currentPage = Math.min(page, pageCount),
    visible = matching.slice((currentPage - 1) * 12, currentPage * 12);'''
    new = '''  const { pageCount, currentPage } = clampPage(page, matching.length),
    visible = matching.slice((currentPage - 1) * 12, currentPage * 12);'''
    assert old in t
    t = t.replace(old, new, 1)
    old = '''                      onChange={(e) => {
                        setQuery(e.target.value);
                        setPage(1);
                      }}
                    />
                  </label>'''
    new = old + '''
                  {entity === "contacts" && (
                    <label>
                      Role
                      <select
                        aria-label="Filter by role"
                        value={role}
                        onChange={(e) => {
                          setRole(e.target.value as ContactRole | "all");
                          setPage(1);
                        }}
                      >
                        <option value="all">All roles</option>
                        {CONTACT_ROLES.map((r) => (
                          <option key={r} value={r}>
                            {r}
                          </option>
                        ))}
                      </select>
                    </label>
                  )}'''
    assert old in t
    return t.replace(old, new, 1)
fe.rw(comp, component)
def tests(t):
    add = '''
import { clampPage, matchContacts } from "../src/lib/contact-filter";

test("ticket 1: role filter composes with literal search and never treats the query as a pattern", () => {
  const base = { phone: "", email: "", notes: "", createdAt: "2026-01-01", updatedAt: "2026-01-01" };
  const contacts = [
    { id: "1", name: "Mira Supplies", role: "supplier", ...base },
    { id: "2", name: "Mira Customer", role: "customer", ...base },
    { id: "3", name: "Mira .*", role: "supplier", ...base },
  ] as unknown as Parameters<typeof matchContacts>[0];
  assert.deepEqual(matchContacts(contacts, "supplier", "mira").map((c) => c.id), ["1", "3"]);
  assert.deepEqual(matchContacts(contacts, "all", "mira").map((c) => c.id), ["1", "2", "3"]);
  assert.deepEqual(matchContacts(contacts, "all", ".*").map((c) => c.id), ["3"]);
  assert.deepEqual(matchContacts(contacts, "all", "[").map((c) => c.id), []);
});

test("ticket 1: deleting the last row on the last page clamps to a valid page", () => {
  assert.deepEqual(clampPage(3, 25), { pageCount: 3, currentPage: 3 });
  assert.deepEqual(clampPage(3, 24), { pageCount: 2, currentPage: 2 });
  assert.deepEqual(clampPage(3, 0), { pageCount: 1, currentPage: 1 });
  assert.deepEqual(clampPage(0, 5), { pageCount: 1, currentPage: 1 });
});
'''
    return t.rstrip('\n') + '\n' + add
fe.rw('tests/domain.test.ts', tests)
fe.append_section(S, '06', '## Ticket 1, worked end to end', """This is the one complete reference answer; tickets 2-5 stay yours.

**Pure helper** (`src/lib/contact-filter.ts`): `matchContacts(contacts, role, query)` derives the visible rows from the accepted collection, a role or `"all"`, and a *literal* query (`includes`, never `RegExp`). `clampPage(page, count)` turns any requested page into one that exists. Neither touches storage: filtering is presentation, so there is no command and no revision bump.

**Component change** (`src/components/LocalOperationsApp.tsx`): one new piece of state, `role`; the `matching` calculation uses `matchContacts` when the entity is `contacts` and the old generic filter otherwise; `pageCount`/`currentPage` come from `clampPage`; a `<select aria-label="Filter by role">` next to the search box resets the page on change, exactly as the search box does. No second filtered list is stored.

**Tests** (`tests/domain.test.ts`, two cases): the role filter composes with search and `.*` / `[` match themselves; deleting the last row of the last page moves to the new last page (25 rows on page 3, then 24).

**What to review in your own version:** did you reset the page in *both* handlers? Does export still say which set it exports (the matching set)? Did you add a `useMemo` you cannot justify with a measurement?""", before='## ')
done.append('review#3 Ticket 1 implemented end to end: src/lib/contact-filter.ts (matchContacts, clampPage), role select + derived matching in the component, two node:test cases, worked solution in 06')

# --- review#2: load-bearing code inline
st = src('src/lib/ledger-storage.ts'); sc = src('src/lib/ledger-schema.ts')
wl, wcode = block(st, r'private write\(', r'tx\.onabort', extra=8)
il, icode = block(sc, r'for \(const t of w\.transactions\)', None, extra=5)
dl, dcode = block(sc, r'export function decimal\(', r'^export function ', extra=0)
fe.append_section(S, '02', '## The compare-and-set write, in code', f"""`src/lib/ledger-storage.ts:{wl}`. Read it top to bottom once: one transaction, a `get`, the revision comparison, the synchronous `change`, validation, the optional backup, the `put`, and the abort path that carries the reason out.

```typescript
{wcode}
```

## Exact decimals, in code

`src/lib/ledger-schema.ts:{dl}`. The string is checked against a pattern first, then split into whole and fraction and turned into an integer count of the smallest unit. No `parseFloat`, no `toFixed`.

```typescript
{dcode}
```""", before='## Stock is a derivation')
fe.append_section(S, '03', '## The overpayment invariant, in code', f"""`src/lib/ledger-schema.ts:{il}`. This runs inside `validateWorkspace`, which runs inside the write transaction, so a payment that would exceed its transaction never reaches storage:

```typescript
{icode}
```""", before='## Teach the failure path')
done.append('review#2 write() and decimal() inlined in 02, the overpayment invariant in 03, each with file:line anchors read from the current source')

# --- review#1: reproduce the browser evidence
vb = open('scripts/verify_browser.py', encoding='utf-8-sig').read()
out = re.search(r'OUT\s*=\s*(.+)', vb)
outv = out.group(1).strip() if out else 'the OUT path at the top of the script'
fe.append_section(S, '04', '## Reproduce the browser evidence', f"""The delivery's browser run is reproducible; it is not part of `npm test`.

```powershell
python --version                      # 3.11+ used for the recorded run
pip install playwright
python -m playwright install chromium
npm run build
python scripts/verify_browser.py      # starts the built app, drives Chromium, writes evidence
```

Output lands under `{outv}` (see the top of the script): `results.json` plus numbered screenshots (`01-payment-rejection.png`, `02-inventory.png`, `03-reminders.png`, `04-conflict-draft.png`) and `failure-tab-N.png` when a step fails. The recorded run took about 222 seconds on the delivery machine, most of it the build and the second-tab conflict scenario. If Chromium fails to launch, run `python -m playwright install --with-deps chromium` once.""", before='## ')
done.append('review#1 04 "Reproduce the browser evidence" with prerequisites, command, output location and duration')

# --- review#4 glossary
fe.append_section(S, '02', '## Glossary', """*Aggregate invariant*: a rule that spans several records (payments never exceed their transaction) and is checked on the whole workspace before a write. *Command / reducer*: `applyCommand` takes the current workspace and a command and returns the next workspace; nothing else mutates state. *Expected revision*: the revision the tab last saw; the write refuses if storage has moved on. *Compare-and-set*: read, compare the expected revision, write in one transaction. *IndexedDB transaction lifetime*: a transaction auto-commits when no requests are pending, so an `await` on unrelated work deactivates it. *`durability: "strict"`*: ask the browser to flush to disk before reporting success. *BroadcastChannel*: how tabs tell each other the workspace changed. *Schema migration*: `ledger-migration.ts` upgrading an older stored shape before validation. *Recovery snapshot*: the backup row written before a reviewed replacement (20 retained).""")
done.append('review#4 02 glossary')

# --- review#5 parity table, review#6 scope statement
new = open(comp, encoding='utf-8-sig').read().lower()
def where(keys, note):
    return note if any(k in new for k in keys) else 'not found in the rewrite: dropped'
rows = [
 ('Dashboard', where(['operating picture'], 'the "Your operating picture" hero, `totals()`')),
 ('People', where(['contacts'], 'the People entity table (`labels`), now with the role filter')),
 ('Money', where(['transactions', 'payments'], 'transactions + payments tables and "Recorded commitments"')),
 ('Inventory', where(['stock to review'], '"Stock to review" and the inventory entity table; stock is derived')),
 ('Reminders', where(['reminders'], 'the reminders table, "Due work", recurring successors')),
 ('Daily Log', where(['closing'], 'daily closing records ("Earlier closing records")')),
 ('Planning', where(['budget review'], '"Budget review" per month')),
 ('Reports', where(['csv'], 'per-entity CSV export of the matching set (no report screen)')),
 ('Assets', where(['assets'], 'the assets entity table')),
]
table = '| original section | where it lives now |\n|---|---|\n' + '\n'.join(f'| {a} | {b} |' for a, b in rows)
fe.append_section(S, 'README', '## Parity and scope', f"""The component went from 3,398 lines to 1,444. Audit it with this table (built by searching the rewrite for each original section):

{table}

**This course covers no server, HTTP, SQL or auth.** Everything runs in one browser against IndexedDB. That is deliberate (the storage and invariant lessons are the point), but it means the CRUD stack you are training for is only sketched here in Ticket 4. Do a server-side course next: `newcodexJS/07` (Express + Postgres) or `buildCRMPYJS` chapter 8 (Prisma contacts CRUD through an auth gate).""", before='## ')
done.append('review#5 README parity table (old sections -> new location, or dropped); review#6 README states the no-server scope and points at server-side courses')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
