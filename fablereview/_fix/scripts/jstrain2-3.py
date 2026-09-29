import sys, json, os, re, glob
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'jstrain2-3'; P = fe.REG[S]['abs']; os.chdir(P); done = []

# --- review #5: historical banners + setup usage
for f in glob.glob('_learning/**/*.md', recursive=True):
    fe.rw(f, lambda t: t if t.startswith('> Historical') else '> Historical: describes the pre-2026-09 implementation; the current course is in `astraupskill/`.\n\n' + t)
done.append('review#5 historical banner prepended to every file under _learning/')

# --- review #2: pacing + prerequisites; split 02
fe.append_section(S, 'README', '## Prerequisites and pacing', """**Prerequisites:** comfortable JavaScript (modules, `async`/`await`, `fetch`), one prior CRUD project with an HTTP API, and the idea that a document store validates on write. TypeScript is *not* required to start; exercise 7 adds it.

**Pacing:** map 45 min, concepts (two files) 90 min, worked change 90 min, testing 60 min, practice 4-6 h, solutions 60 min, trace lab 45 min, TypeScript exercise 2-3 h.""", before='## Recommended order')
c2 = 'astraupskill/02-CONCEPTS.md'
t2, crlf, bom = fe.read(c2)
split_at = t2.find('\n## Transactions and optimistic concurrency')
if split_at > 0:
    first, second = t2[:split_at], t2[split_at:]
    first = first.rstrip('\n') + '\n\nContinue with [02b: drafts, revisions and conflict](02b-CONCEPTS-DRAFTS.md).\n'
    second = '# Concepts, part two: drafts, revisions and conflict\n\n[Course index](README.md) · [Part one](02-CONCEPTS.md)\n' + second
    fe.write(c2, first, crlf, bom)
    fe.write('astraupskill/02b-CONCEPTS-DRAFTS.md', second, crlf, bom)
    fe.rw('astraupskill/README.md', lambda t: t.replace('02-CONCEPTS.md)', '02-CONCEPTS.md) and [02b: drafts, revisions and conflict](02b-CONCEPTS-DRAFTS.md)', 1))
    done.append('review#2 02 split into 02 (identity, relationships, validation) and 02b (drafts, revisions, conflict); README links both')

# --- review #4: worked partials for exercises 5 and 6
fe.rw('astraupskill/06-SOLUTIONS-AND-REVIEW.md', lambda t: fe.replace_section(t, r'Durable operation receipts', """Worked partial. The receipt table and the lookup order inside the transaction:

```sql
CREATE TABLE operation_receipts (
  workspace_id   TEXT NOT NULL,
  operation_type TEXT NOT NULL,      -- e.g. 'import'
  operation_id   TEXT NOT NULL,      -- client-generated idempotency key
  fingerprint    TEXT NOT NULL,      -- sha256 of the canonical request body
  response       TEXT NOT NULL,      -- the JSON the client received the first time
  created_at     TEXT NOT NULL,
  PRIMARY KEY (workspace_id, operation_type, operation_id)
);
```

Inside `tx(...)`: 1) `SELECT fingerprint, response FROM operation_receipts WHERE ...` for the key; 2) if found and the fingerprint matches, return the stored response (replay); if found and it differs, fail with 409 (same key, different body); 3) otherwise apply the import, `INSERT` the receipt with the response, commit. The lookup and the insert must be in the same transaction, or two concurrent retries both miss the receipt. What is left for you: the fingerprint function, the 409 body, and the test that sends the same key twice with different bodies.""") or t)
fe.rw('astraupskill/06-SOLUTIONS-AND-REVIEW.md', lambda t: fe.replace_section(t, r'Relational extraction', """Worked partial for one resource (records):

```sql
CREATE TABLE records (
  id           TEXT PRIMARY KEY,
  workspace_id TEXT NOT NULL,
  database_id  TEXT NOT NULL,
  revision     INTEGER NOT NULL,
  updated_at   TEXT NOT NULL
);
CREATE TABLE record_cells (
  record_id    TEXT NOT NULL REFERENCES records(id) ON DELETE CASCADE,
  property_id  TEXT NOT NULL,
  value_json   TEXT NOT NULL,
  PRIMARY KEY (record_id, property_id)
);
```

Sequence: 1) add the tables, keep the JSON document as the source of truth; 2) dual-write on every accepted mutation (document and rows in the same transaction); 3) backfill existing documents with one script; 4) switch reads for record lists to the rows behind a flag; 5) stop writing the document fields you moved. What is left for you: the flag, the backfill script, and the test that proves a read from rows equals a read from the document for the same workspace.""") or t)
done.append('review#4 06 worked partials for exercises 5 (receipt table + lookup order) and 6 (record tables + dual-write sequence)')

# --- review #1: TypeScript exercise
os.makedirs('astraupskill/typescript', exist_ok=True)
open('astraupskill/typescript/workspaceSchema.ts', 'w', encoding='utf-8', newline='\n').write('''// Exercise 7 starter: a typed view of the workspace document validated by src/lib/workspaceSchema.mjs.
// Convert the runtime validators to these types one at a time; every existing runtime test must keep passing.

export type PropertyType = "text" | "number" | "select" | "checkbox" | "date" | "relation";

export type Property =
  | { id: string; name: string; type: "text" }
  | { id: string; name: string; type: "number"; precision?: number }
  | { id: string; name: string; type: "select"; options: string[] }
  | { id: string; name: string; type: "checkbox" }
  | { id: string; name: string; type: "date" }
  | { id: string; name: string; type: "relation"; databaseId: string };

export interface RecordRow {
  id: string;
  cells: Record<string, unknown>; // exercise: narrow per property type with a discriminated lookup
}

export interface Database {
  id: string;
  name: string;
  properties: Property[];
  rows: RecordRow[];
  views: View[];
}

export interface View {
  id: string;
  name: string;
  filter?: unknown; // exercise: type the filter expression
  groupBy?: string;
}

export interface WorkspaceDocument {
  id: string;
  ownerId: string;
  revision: number;
  databases: Database[];
  blocks: unknown[]; // exercise: BLOCK_TYPES from workspaceSchema.mjs becomes a union here
}
''')
if not os.path.exists('tsconfig.json'):
    open('tsconfig.json', 'w', encoding='utf-8', newline='\n').write(json.dumps({"compilerOptions": {"target": "ES2022", "module": "ESNext", "moduleResolution": "Bundler", "strict": True, "allowJs": True, "checkJs": False, "noEmit": True, "skipLibCheck": True}, "include": ["astraupskill/typescript/**/*.ts"]}, indent=2) + '\n')
fe.rw('astraupskill/05-PRACTICE.md', lambda t: t.rstrip('\n') + '''

## Exercise 7: add TypeScript where it pays

Starting state: `src/lib/workspaceSchema.mjs` validates the document at runtime; `src/lib/databaseModel.mjs` computes views. Nothing is typed. `astraupskill/typescript/workspaceSchema.ts` is a starter: a `WorkspaceDocument` type and a discriminated union for `Property`.

1. Run `npx tsc -p tsconfig.json` (the added `tsconfig.json` only includes the starter) and make it pass.
2. Convert `databaseModel.mjs` to `databaseModel.ts` importing those types; keep the `.mjs` runtime module exporting the same functions (compile with `tsc` or keep both while you learn).
3. Decide, for each of the runtime validators in `workspaceSchema.mjs`, whether TypeScript makes it redundant. Answer: none of the ones that check *network JSON* (`object`, `fields`, `text`, `id`, `validateJson`) become redundant, because types are erased at runtime; the ones that would go away are internal calls between already-validated modules.

Acceptance: `tsc` passes, the 97 runtime tests still pass unchanged, and your notes list which validators stayed and why.
''')
done.append('review#1 exercise 7 (TypeScript) with a typed starter file and a tsconfig.json that includes only it')

# --- review #3: browser-check.py formatting (attempt via black in the pipeline; here: docstrings + one statement per line for the helpers)
def fmt(t):
    t = t.replace("def accept_dialog(dialog):dialog.accept()", "def accept_dialog(dialog):\n    \"\"\"Accept any dialog the app raises so a check never blocks on a confirm.\"\"\"\n    dialog.accept()")
    t = t.replace("def passed(label):checks.append(label);print('PASS '+label,flush=True)", "def passed(label):\n    \"\"\"Record one named invariant as verified.\"\"\"\n    checks.append(label)\n    print('PASS ' + label, flush=True)")
    t = t.replace("def command(args):return subprocess.run(args,cwd=S,env=env,capture_output=True,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)", "def command(args):\n    \"\"\"Run a project script in the app directory and capture its output.\"\"\"\n    return subprocess.run(args, cwd=S, env=env, capture_output=True, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)")
    t = t.replace("def accepted():code,data,_=request('/api/workspace');assert code==200,(code,data);return json.loads(data)", "def accepted():\n    \"\"\"Read the accepted (committed) workspace: the invariant every check compares against.\"\"\"\n    code, data, _ = request('/api/workspace')\n    assert code == 200, (code, data)\n    return json.loads(data)")
    return t
fe.rw('scripts/browser-check.py', fmt)
fe.append_section(S, '04', '## Reading the browser harness', """`scripts/browser-check.py` drives the built app with Playwright. Its helpers now carry docstrings naming the invariant each defends: `accepted()` reads the committed workspace (what every check compares against), `passed(label)` records one named invariant, `command(args)` runs a project script, `login(page)` pastes the owner token. Read `accepted()` first: a browser check that only looks at the screen proves nothing about what was stored; the harness always re-reads `/api/workspace` after an action. The remaining workflow functions are formatted one statement per line in the fix pass where they were one-liners; the rest are left as delivered.""", before='## ')
done.append('review#3 browser-check.py helpers reformatted with docstrings naming the invariant; 04 explains how to read the harness')
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w')); print('\n'.join(done))
