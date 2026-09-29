from pathlib import Path
import json, hashlib, shutil, os
B=Path(__file__).resolve().parents[2]; ID='4c54d18d7d97'; P=B/'stage'/ID; U=P/'astraupskill'; C=B/'checks'/ID; E=U/'evidence'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p in U.glob('*.md'):
 t=p.read_text(encoding='utf-8-sig').replace('staged server directory','server directory').replace('staged route','current route').replace('staged version','current version')
 p.write_text(t,encoding='utf-8')
p=U/'01-CODEBASE-MAP.md'; t=p.read_text(encoding='utf-8')
t=t.replace('so a test can set `DB_PATH` to a temporary location before importing the module.','and the default connection is lazy. Tests pass a disposable database from the factory directly to the cart, order and app factories; they do not set DB_PATH.')
t=t.replace('`routes/orders.js` wraps checkout in `db.transaction`.','`routes/orders.js` calls [the checkout service](../server/src/services/checkout.js), which owns the database transaction and invokes its immediate mode.')
t=t.replace('route tests should build a temp DB before importing these modules','route tests should build a temp DB before invoking the injected factories')
t=t.replace('is matched together with `user_id` in every mutable query','is matched together with `user_id` in the ownership lookup before PATCH updates by the selected row id; DELETE includes both in its SQL predicate')
t=t.replace('`orders.js` reads it later','the checkout service reads it later')
p.write_text(t,encoding='utf-8')
p=U/'02-CONCEPTS.md';t=p.read_text(encoding='utf-8').replace('the focused test proves helper behavior and disposable-file isolation','the six focused cases exercise the real cart and checkout handlers, the app error middleware and a real SQLite rollback, with a disposable file')
t+='\nImmediate mode acquires the SQLite write lock before the cart read. The callback stays synchronous: placing an await inside it would leave work outside the intended transaction lifetime. Finite prices alone are insufficient: price 1e308 multiplied by quantity 2 overflows, so totalForCart rejects non-finite line totals and accumulated totals. The persisted-price regression exercises the line overflow through the actual checkout handler. There is no separate sum-only overflow regression yet.\n'
p.write_text(t,encoding='utf-8')
p=U/'05-PRACTICE.md';t=p.read_text(encoding='utf-8').replace('Seed two valid cart lines.','Seed two cart lines, with the second exceeding available stock.')
t=t.replace('both cart rows retained.','both cart rows retained. Explain why this is a preflight rejection before the first write. Then use two sellable lines and an AFTER INSERT trigger that aborts only for the second product to demonstrate rollback after the first line and stock update.')
t=t.replace('cart.js', 'cart.js')
p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8')
t=t.replace('Checkout may insert the order and line A before line B’s validation or conditional update fails, but the exception occurs inside `db.transaction`.','totalForCart validates the entire cart before the first INSERT, so this case rejects during preflight. It does not prove rollback of earlier writes. The executable trigger case below uses two sellable lines and aborts only the second product’s line INSERT, after the first line and stock decrement have executed; that case proves SQLite restores prior writes.')
t=t.replace('A broken schema or unexpected driver exception should be logged by the host and return the generic 500 response.','A broken schema or unexpected driver exception returns the generic 500 response. Structured host logging is a proposed addition; the current middleware does not implement it.')
t+='\n## Complete executable production-handler fixture\n\nThis is the full current server/tests/cart-validation.test.mjs. It contains all imports, fixture setup, request adapters, assertions and teardown. Modify the existing test file when practicing; do not paste duplicate tests into it. The adapter invokes real Express router/app handlers with an injected actor. It does not exercise a network listener or JWT decoding. Only cart and order routes accept the injected database; other application routes retain their default connection.\n\n```js\n'+(P/'server/tests/cart-validation.test.mjs').read_text(encoding='utf-8')+'```\n'
p.write_text(t,encoding='utf-8')
p=U/'04-TESTING-AND-DEBUGGING.md';t=p.read_text(encoding='utf-8')
t=t.replace('assert 400 and `error: "Insufficient stock"`','assert 400 and an error containing `Insufficient stock`')
t=t.replace('To exercise the database predicate, use two products and arrange the second line to fail;','To exercise rollback after writes, use two sellable products and a SQL trigger that aborts insertion of the second product’s order line;')
t=t.replace('inspect when `DB_PATH` was set','inspect whether a default connection was accessed instead of the injected temporary database')
t+='\nThe trigger regression does not force the conditional stock UPDATE to return zero and does not coordinate competing processes. The preflight stock test and rollback-after-write test support different claims. In the latter, both cart rows and both original stocks are asserted after the app maps the driver failure to a generic 500. The actual client production build also passed; it checks bundling of the unchanged client, not browser checkout interactions.\n'
p.write_text(t,encoding='utf-8')
labels=['install-02','luna-server-final-check-20260912','root-client-install-01','root-client-build-01']+[f'syntax-{n}-final-20260912' for n in ['cart','orders','checkout','validation','index']]
E.mkdir(exist_ok=True)
for label in labels:
 r=read(C/(label+'.json')); assert r['status']=='complete' and r['exitCode']==0,r
 for ext in ['.json','.log']:shutil.copyfile(C/(label+ext),E/(label+ext))
log=(C/'luna-server-final-check-20260912.log').read_text(encoding='utf-8'); assert '# tests 6' in log and '# pass 6' in log and '# fail 0' in log
result={'passed':True,'total':6,'tests':6,'failed':0,'checks':labels,'scope':'Real production cart/order/app handlers with disposable SQLite and injected identity; second-line SQL failure rolls back earlier stock writes. Client production build passed. No live HTTP/JWT/payment or multiprocess test.'}
for p in [C/'results.json',E/'results.json']:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
(U/'VERIFICATION.md').write_text('''# Verification and limits

Run these commands from the project root using Node 22.16, the version used for the recorded review. Installation uses each existing package lockfile. The server test uses better-sqlite3, so installation must complete before running it.

```powershell
npm ci --prefix server --prefer-offline
node --test server/tests/cart-validation.test.mjs
npm ci --prefix client --prefer-offline
npm run build --prefix client
```

The [server output](evidence/luna-server-final-check-20260912.log) records six discovered tests, six passes and zero failures. The [client build](evidence/root-client-build-01.log) completed successfully. Five additional syntax checks passed for the cart route, order route, checkout service, validator and server entry point. Exact commands, working directories, exit statuses and logs are bundled beside [results.json](evidence/results.json). These are finite local checks; the client build does not exercise a browser or deployed server.

The actual test fixture creates a unique directory under the operating system temporary directory, opens a SQLite file through createDatabase, initializes the actual schema and inserts explicit users/products. It injects this connection and an actor into real cart/order routers. The unexpected-error case invokes the real app factory and its error middleware. Teardown closes the connection before removing only the fixture directory. Importing the lazy default database and guarded entry point does not initialize the canonical server/data/store.db. No seed/reset command was run.

Coverage includes strict quantities, ownership-scoped PATCH, accumulated cart stock, a successful checkout, negative persisted quantity, persisted-price multiplication overflow, insufficient stock, and rollback after a second-line SQL trigger failure. The last case proves that earlier order/line writes and a first stock decrement are restored. Preflight validation alone would not prove that rollback behavior. There is no separate accumulated-total overflow test or forced zero-row conditional UPDATE test.

Identity is injected; JWT parsing and a real network listener are outside this suite. The app database seam applies to cart/order routes, while other demo routes retain default storage. REAL dollar amounts, demo JWT fallback, feature flags, payment integration, durable idempotency and cross-process contention are documented limits. Unexpected errors return generic 500 responses; durable structured error logging is not implemented. The immediate transaction coordinates SQLite writes on the current database, without making an external payment part of that transaction. Original source bytes are preserved in snapshots for the worked-change comparison.
''',encoding='utf-8')
p=U/'README.md';t=p.read_text(encoding='utf-8');t+='\n## Follow the implementation\n\nRead the [checkout service](../server/src/services/checkout.js), [validator](../server/src/services/cartValidation.js), and [complete regression fixture](../server/tests/cart-validation.test.mjs) alongside the nine chapters. The [verification record](VERIFICATION.md) includes the final six-test result and client build, with local logs. Start with malformed cart input, then follow persisted-state preflight, successful checkout and finally the injected second-line failure. Explain exactly which writes happened in each trace before discussing atomicity.\n';p.write_text(t,encoding='utf-8')
base=read(B/'baselines'/f'{ID}.json')['files']; changed=[n for n,h in base.items() if not(P/n).is_file() or sha(P/n)!=h]
canonical=B.parent.parent/'_Organized Desktop/04 JavaScript Training/jstrain3.0'
(U/'snapshots').mkdir(exist_ok=True)
for n in changed:
 assert sha(canonical/n)==base[n],n
 if n!='README.md' and not any(sha(q)==base[n] for q in (U/'snapshots').iterdir() if q.is_file()):shutil.copyfile(canonical/n,U/'snapshots'/(n.replace('/','__')+'.before.txt'))
new=[]
for root,dirs,files in os.walk(P):
 dirs[:]=[d for d in dirs if d not in {'node_modules','.git','dist','build','astraupskill','coverage'}]
 for f in files:
  n=(Path(root)/f).relative_to(P).as_posix()
  if n not in base:new.append(n)
assert all(n.endswith(('.js','.mjs','.json','.md')) for n in new),new
spec={'summary':['Validates typed cart inputs, joined product stock and ownership before mutations; rejects hostile persisted quantities and non-finite totals at checkout.','Moves checkout reads and all order/stock/cart writes into one immediate SQLite transaction with a conditional stock decrement.','Adds lazy database and injectable cart/order/app factories, an import-safe listener and safe unexpected-error responses.','Adds six production-handler SQLite regressions including second-line failure rollback, a passing client build, and nine detailed learning chapters with a complete fixture.'],'changedFiles':changed+new+[p.relative_to(P).as_posix() for folder in [U/'snapshots',E] for p in folder.iterdir() if p.is_file()], 'checks':{'format':'json','resultsFile':f'checks/{ID}/results.json','expectedTests':6},'limits':['Tests inject identity and call Express handlers directly; no live listener, JWT parser, payment provider or multiprocess contention test.','REAL dollar schema and demo authentication remain; order idempotency and durable logging are not implemented.','Database injection applies to cart/order routes, not every route; no canonical database or seed was used.']}
(B/'specs'/f'{ID}.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
(C/'root-review-source-hashes.json').write_text(json.dumps({'files':{n:sha(P/n) for n in changed+new if not n.endswith('.md')}},indent=2),encoding='utf-8')
print(json.dumps({'changed':changed,'new':new,'tests':6,'files':len(spec['changedFiles'])+9}))
