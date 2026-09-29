from pathlib import Path
import json,re
B=Path('astrafinalplan/implementation/batch04');courses=sorted([c for k in range(1,4) for c in json.loads((B/f'course-specific-{k}.json').read_text())],key=lambda c:c['stage']);assert len(courses)==25
for c in courses:
 n=c['stage'];root=B/'stage'/str(n)
 if n<=54:c['test']=c['test'].replace('domain.test','workflow.test')
 assert (root/c['source']).exists(),c;assert (root/c['test']).exists(),c
 if n in (51,56):
  c['setup']='''From the project root, use Node.js and npm:

```powershell
npm install
npm run dev
```

Open the Vite URL printed in the terminal. The React client and Express API both need to remain running. Run one project at a time if their ports conflict. In another terminal in this project:

```powershell
npm test
npm run build
```

The API data is in memory. Refreshing the browser keeps the API process alive; restarting the API rebuilds its initial data. Tests start a separate server on a random loopback port and close it afterward. No PostgreSQL service is required.'''
  c['dbguide']='The server memory owns records. Use the Network panel to compare request JSON and response JSON, then restart the API to distinguish process memory from durable storage. The regression helper imports the actual app and calls it through HTTP.'
  c['testcmd']='npm test\nnpm run build'
 elif 52<=n<=57:
  c['setup']='''Use Node.js, npm and a local PostgreSQL server with psql on PATH. From this project root:

```powershell
npm install
$env:DATABASE_URL = 'postgres://postgres:YOUR_LOCAL_PASSWORD@localhost:5432/astra_learning_sandbox'
psql $env:DATABASE_URL -f server/db/schema.sql
npm run dev
```

Create that empty learning database first with your local PostgreSQL account. The schema script resets the app tables and adds its sample records, so use a dedicated disposable learning database. The explicit PowerShell command avoids the inherited POSIX-style db:setup variable expansion. psql does not read a Node .env file automatically. Open the URL printed by Vite and keep the API/client running.

For regression tests, create a different database with an astra_test_ prefix:

```powershell
$env:ASTRA_TEST_DATABASE_URL = 'postgres://postgres:YOUR_LOCAL_PASSWORD@localhost:5432/astra_test_learning'
npm test
npm run typecheck
npm run build
```

The account must be able to create/drop schemas. The helper refuses a non-test database name, creates a unique schema, loads the actual app SQL there, assigns the connection before importing the app and removes its schema on normal completion. Tests use a random local port and never call your manually running API. The app build is a client build; the API still runs separately.'''
  c['dbguide']='Read [test/database.ts](../test/database.ts). PostgreSQL owns persistent rows; a unique search_path isolates each test schema. Failure triggers are created only inside that schema. If a process is interrupted, inspect its exact schema name before cleanup. The course never requires personal application data.'
  c['testcmd']='npm test\nnpm run typecheck\nnpm run build'
 elif 58<=n<=71:
  c['setup']='''The root package.json is an npm workspace joining client and server. Install from the project root so test dependencies and sibling packages resolve consistently:

```powershell
npm install
$env:DATABASE_URL = 'postgres://postgres:YOUR_LOCAL_PASSWORD@localhost:5432/astra_learning_sandbox'
npm run db:migrate
npm run db:seed
npm run dev
```

Create an empty, dedicated learning database before migrating. The seed command replaces sample tables, so use a disposable learning database. The DATABASE_URL environment variable must remain set in the terminal that starts the API. Vite prints the browser URL; the API is a separate process. The source README and server .env.example explain app-specific ports and optional settings. The new TypeScript database command runs through tsx, which loads the actual TypeScript migrations and seeds.

Use a separate pre-created test database for automated checks:

```powershell
$env:ASTRA_TEST_DATABASE_URL = 'postgres://postgres:YOUR_LOCAL_PASSWORD@localhost:5432/astra_test_learning'
npm test
npm run build
```

Tests create a random schema, run the real migrations, start the real HTTP API on a random loopback port, then close connections and drop that schema. The test database name must begin astra_test_ and the account needs schema creation rights. npm run build compiles the server and builds the React client. To start compiled API code, use npm run start --workspace server; this still needs DATABASE_URL and migrated tables. Client hosting is separate. Do not run seeds against valuable data.'''
  c['dbguide']='The [test/database.ts](../test/database.ts) helper demonstrates migration-based isolation. It sets DATABASE_URL before importing the Knex connection and uses a unique PostgreSQL schema. The root workspace also makes pg and tsx available to the root test directory. A source import ending in .js is intentional: TypeScript resolves its .ts source during development and emitted Node code resolves .js after compilation.'
  c['testcmd']='npm test\nnpm run build'
 elif n==72:
  c['setup']='''Use Node.js 22.16 or newer compatible with node:sqlite, and npm. From this project root:

```powershell
npm install
npm run dev
```

Open the Vite URL printed by the project. The API uses SQLite and creates its data directory when started; no PostgreSQL server is needed. RECIPE_LAB_DATA can point to a separate learning directory if you want another dataset. Keep the API and client running.

```powershell
npm test
npm run build
```

The regression suite assigns RECIPE_LAB_DATA to a fresh temporary directory before importing the database, runs the actual Express API through HTTP and removes only that temporary directory after closing SQLite. Existing recipe databases and photos are not fixtures.'''
  c['dbguide']='Read server/db.ts for DatabaseSync and tx. The relational database and search index commit together, while photo files have their own lifecycle. Read test/recipes.test.ts for a temporary-database example. The delivery evidence uses Node 22.16.0; this app depends on node:sqlite.'
  c['testcmd']='npm test\nnpm run build'
 elif n in (73,74):
  c['setup']='''From this project root, install its declared dependencies:

```powershell
npm install
npm run dev
```

Open the local Vite URL. This app stores its data in the browser, so no API process or PostgreSQL service is required. Keep using the same origin: changing the hostname or port selects a different browser storage area.

```powershell
npm test
npm run build
```

The existing Vitest suite runs alongside the new import regressions. Use synthetic records and a separate browser profile for practice resets. The test fixtures use fresh simulated storage. A browser check separately verifies the built app in Chromium. Export a copy of learning progress before experimenting with restore behavior.'''
  c['dbguide']='This app uses '+('Zustand/localStorage. parseBackup is pure and approves records before the calling UI replaces stores. Validation is not a transaction across the later storage writes.' if n==73 else 'Dexie/IndexedDB. validateImport checks the whole payload before importData opens a transaction across progress tables. The tests exercise the actual Dexie methods using fake-indexeddb.')
  c['testcmd']='npm test\nnpm run build'
 else:
  c['setup']='''Work in this job track folder, using only its root client and server packages. Other projects nested nearby are independent.

```powershell
npm install
npm run install:all
$env:JWT_SECRET = 'replace-with-a-long-local-learning-secret'
npm run dev
```

The Express API uses SQLite and the React client uses Vite. JWT_SECRET must be set for the API to start. JOB_TRACK_DATA_DIR optionally selects another data directory. Open the local URL printed by Vite.

```powershell
npm test
npm run build
```

The test suite creates a temporary database directory and synthetic JWT secret, registers synthetic users, and calls the real API on a random loopback port. It closes SQLite and removes only that temporary directory. The native better-sqlite3 dependency must match the Node version used to run the server; npm install normally handles that binding.'''
  c['dbguide']='SQLite stores applications with a user_id ownership predicate. Read server/src/db.js and test/applications.test.js to see the test data-directory override. The root npm test delegates to the server script. No PostgreSQL service or external account is required.'
  c['testcmd']='npm test\nnpm run build'
 if n in (73,74):c['flow']=['The Settings UI reads an uploaded JSON backup','JSON parsing yields unknown runtime values','The import validator checks nested records, identity and numeric/date constraints','A valid result reaches the existing replacement operation','The storage layer writes the accepted candidate according to its documented boundary','The UI reloads or renders the saved result and reports rejected input']
 else:c['flow']=['A React form, button or test sends a concrete operation','The client serializes editable values as an HTTP request'+(' or WebSocket event' if n==57 else ''),'The server validates runtime input and the relevant record relationships','The repository or model reads authoritative state and performs the documented change','The storage boundary commits or rejects the operation','The response or broadcast gives the client its observed result']
 c['limitations']=c['concept'].split('\n\n')[-1]
(B/'courses.json').write_text(json.dumps(courses,indent=2)+'\n')
s=(B.parent/'batch03/write_learning.py').read_text();s=s.replace('enumerate(COURSES,21)','enumerate(COURSES,51)').replace('NAMES[i-21]','NAMES[i-51]')
s=s.replace("p=BASE/n/'README.md';text=p.read_text(encoding='utf-8')","p=BASE/n/'README.md';text=p.read_text(encoding='utf-8') if p.exists() else '# '+c['title']+'\\n'")
s=s.replace("if p.is_file() and p.suffix", "if (i != 75 or p.relative_to(BASE/n).parts[0] in ['client','server']) and p.is_file() and p.suffix")
s=s.replace('For Poll Studio and Kanban Flow, jsdom runs the actual app.js against its HTML and fresh browser storage; the suite can force a storage-write failure. The other projects use their actual Express app over loopback HTTP. PostgreSQL projects additionally load a disposable schema. Chromium checks cover the real built clients and route their API requests to those isolated real servers through a local test proxy. These checks verify different boundaries; none replaces reading the test helper.','Questboard uses Vitest and simulated browser storage; DevDeck uses Vitest with fake-indexeddb for its actual Dexie methods. API projects run their real Express app through HTTP with disposable databases or fresh in-memory data. Live Chat also tests a real WebSocket and PostgreSQL notification. Browser checks exercise the built clients separately. Read the project verification page for the exact observed checks and limits.')
s=s.replace('Generated 210 detailed learning chapters plus course metadata; trace and verification pages follow.','Generated 175 detailed chapters; trace labs and verification follow.')
(B/'write_learning.py').write_text(s)
print('Prepared',len(courses),'courses')
