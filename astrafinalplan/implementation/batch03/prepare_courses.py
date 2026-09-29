from pathlib import Path
import json,re
B=Path(__file__).resolve().parent
courses=sorted([c for k in range(1,4) for c in json.loads((B/f'course-specific-{k}.json').read_text(encoding='utf-8'))],key=lambda c:c['stage'])
assert [c['stage'] for c in courses]==list(range(21,51))
ts={28,30,31,33,34,35,41,43,44,47,49,50}
for c in courses:
 n=c['stage'];root=B/'stage'/str(n)
 assert (root/c['source']).exists() and (root/c['test']).exists()
 pkg=json.loads((root/'package.json').read_text(encoding='utf-8-sig'))
 if n<23:
  c['setup']='''Install the test dependencies from this project folder:

```powershell
npm install
npm test
```

For the app, serve this folder locally with Python:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000 in a browser. Keep the terminal running; Ctrl+C stops the server. Use the same origin each time: localStorage belongs to an origin, so changing host or port creates a different storage area. The app itself has no backend or build step. `npm test` runs its actual HTML/app.js in jsdom with fresh test storage; it does not use your saved browser records.'''
  c['dbguide']='This project uses browser localStorage. In DevTools, inspect Application > Local Storage for the local origin. Refresh after an action and compare the saved JSON with the visible result. The tests create their own DOM and storage fixtures. A Node process with jsdom is useful for controlled write failures, while Chromium verifies native interaction.'
  c['testcmd']='npm test'
  c['flow']=['The browser loads index.html and app.js','An event handler reads the selected record and current form controls','Validation checks the intended operation before calculating candidate state','The shared save/move boundary attempts the localStorage write','A successful write publishes the candidate and rerenders; a rejected write keeps the promised previous state','A fresh read after reload reveals the saved result']
 elif n not in ts:
  c['setup']='''From this project folder, install dependencies and start the API plus React client:

```powershell
npm install
npm run dev
```

Open the local URL printed by Vite. Keep both processes running; Ctrl+C stops them. Run one learning project at a time because scaffolds may reuse ports. `npm run dev:server` and `npm run dev:client` start the two sides separately when you want separate logs.

In a second terminal, from the same project folder:

```powershell
npm test
npm run build
```

The server keeps records in memory. Creating a record changes the running process, but restarting it restores the seed dataset. The tests start a separate app instance on an ephemeral loopback port and close it after the suite. They do not call the manually running development server. The production client build is emitted under client/dist; it still needs an API to perform requests.'''
  c['dbguide']='No database service is required. Inspect the repository factory in server/server.js to see seed records, the live collection and methods that mutate it. Use the Network panel to inspect JSON, then restart the server to observe the persistence boundary. HTTP tests verify the actual Express app and repository; they are not database durability tests.'
  c['testcmd']='npm test\nnpm run build'
  c['flow']=['The React event handler reads controlled form or filter state','client/src/api.js serializes the request to the Express API','server/server.js validates caller-controlled fields and normalizes accepted values','The repository method reads or changes its in-memory records','The route returns JSON or a bounded validation error','React reloads or renders the response; server restart reconstructs seed state']
 else:
  c['setup']='''Use Node, npm and a local PostgreSQL installation with `psql` available. From this project folder:

```powershell
npm install
```

Create an empty disposable learning database using your local PostgreSQL account. Set the connection string explicitly in the same PowerShell terminal (replace the example credentials with your local ones):

```powershell
$env:DATABASE_URL = 'postgres://postgres:YOUR_LOCAL_PASSWORD@localhost:5432/astra_learning_sandbox'
psql $env:DATABASE_URL -f server/db/schema.sql
npm run dev
```

The schema script resets this app's tables and seeds sample records; use your dedicated learning database for that reset. The database must already exist. This direct PowerShell command avoids the inherited `db:setup` script's POSIX-style `$DATABASE_URL` expansion. You can instead configure DATABASE_URL in a local .env file for the Node server; `psql` does not automatically load .env, so set its environment value separately. Open the local client URL Vite prints. Run one project at a time to avoid shared development port conflicts.

For regression tests, use a separate existing database whose name begins `astra_test_`:

```powershell
$env:ASTRA_TEST_DATABASE_URL = 'postgres://postgres:YOUR_LOCAL_PASSWORD@localhost:5432/astra_test_learning'
npm test
npm run typecheck
npm run build
```

The test database account needs permission to create and drop its own schemas. The helper creates a unique schema, loads the app's schema/seed data there, starts the real API on an ephemeral loopback port, and drops that schema on normal completion. A test database with pgcrypto available matches the schema's UUID generation requirements. The helper refuses names without the test prefix. It does not use the manually running development server.'''
  c['dbguide']='Read [test/database.ts](../test/database.ts) before experimenting. It assigns DATABASE_URL to a unique search_path before importing the application pool, so the tests exercise isolated tables through real HTTP. SQL failure injection is installed only in that disposable schema. An interrupted process may leave a test schema behind; inspect and remove only the exact schema owned by that run. Reusing a development database name is intentionally rejected. The source uses parameters for values; never concatenate user strings into SQL in a practice extension.'
  c['testcmd']='npm test\nnpm run typecheck\nnpm run build'
  c['flow']=['The React handler collects form or filter state','client/src/api.ts sends typed client data as untyped JSON over HTTP','server/src/index.ts validates runtime values at the server boundary','server/src/db.ts supplies a pool or one transaction client for the relevant SQL','PostgreSQL constraints and the transaction boundary protect the stored relationships described in this lesson','The API maps rows to its JSON representation and React renders the observed result']
 if n>=35:
  c['after']+=' The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.'
(B/'courses.json').write_text(json.dumps(courses,indent=2),encoding='utf-8')
# Reuse the established chapter structure, with current sources and accurate environment descriptions.
s=(B.parent/'batch02/write_learning.py').read_text(encoding='utf-8')
a=s.index('def excerpt(');z=s.index('\ndef write(',a)
s=s[:a]+'''def excerpt(text,symbol,limit=85):
 lines=text.splitlines()
 if symbol.startswith('app.'):
  start=next(i for i,l in enumerate(lines) if symbol in l)
 else:
  definitions=[i for i,l in enumerate(lines) if re.search(r'\\b'+re.escape(symbol)+r'\\s*\\(',l) and ('function ' in l or 'const ' in l or re.match(r'\\s*'+re.escape(symbol)+r'\\s*\\(',l))]
  if definitions:start=definitions[0]
  else:
   hit=next(i for i,l in enumerate(lines) if symbol in l)
   starts=[i for i in range(hit+1) if lines[i].startswith('app.') or re.match(r'^(?:export )?(?:async )?function ',lines[i])]
   start=starts[-1] if starts else max(0,hit-8)
 end=min(len(lines),start+limit)
 for i in range(start+1,end):
  if re.match(r'^(?:export )?(?:async )?function\\s|^app\\.(?:get|post|put|patch|delete)\\(',lines[i]):end=i;break
 return '\\n'.join(lines[start:end]),start+1
''' + s[z:]
s=s.replace('enumerate(COURSES,11)','enumerate(COURSES,21)').replace('NAMES[i-11]','NAMES[i-21]')
s=s.replace("('VERIFICATION.md','Actual verification results and limits')","('07-TRACE-LAB.md','Detailed trace lab and independent checkpoint'),('VERIFICATION.md','Actual verification results and limits')")
s=s.replace('Persist through the project boundary','Commit at the state boundary')
s=s.replace('For the plain browser projects, jsdom runs the actual app.js against its HTML. The helper supplies browser APIs missing from jsdom and a controllable timer clock. It does not replace the app’s business functions. A real browser check is still useful for layout, focus visibility and native interaction. For React state helpers, pure tests verify data behavior; component/browser checks verify that controls call those helpers correctly.','For Poll Studio and Kanban Flow, jsdom runs the actual app.js against its HTML and fresh browser storage; the suite can force a storage-write failure. The other projects use their actual Express app over loopback HTTP. PostgreSQL projects additionally load a disposable schema. Chromium checks cover the real built clients and route their API requests to those isolated real servers through a local test proxy. These checks verify different boundaries; none replaces reading the test helper.')
s=s.replace('Generated 70 detailed learning chapters plus course metadata; verification pages follow executed checks.','Generated 210 detailed learning chapters plus course metadata; trace and verification pages follow.')
(B/'write_learning.py').write_text(s,encoding='utf-8')
print('Prepared thirty source-grounded courses and the chapter generator')
