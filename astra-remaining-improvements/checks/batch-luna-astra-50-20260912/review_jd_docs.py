from pathlib import Path
P=Path(__file__).resolve().parents[2]/'stage/2d739127d551';U=P/'astraupskill'
for p in U.glob('*.md'):
 t=p.read_text(encoding='utf-8').replace('the staged project','the project').replace('the staged source','the source').replace('the staged files','the source files').replace('staged `src` folder','project `src` folder')
 t=t.replace('and now rejects values below zero','and rejects values below zero or above 2,147,483,647, the supported signed 32-bit input range')
 t=t.replace('if (!Number.isSafeInteger(Number(value)) || Number(value) < 0) throw invalid(`Invalid ${field}`);','if (!Number.isSafeInteger(Number(value)) || Number(value) < 0 || Number(value) > 2147483647) throw invalid(`Invalid ${field}`);')
 t=t.replace('Request, Response, URL, setTimeout','Request, Response, URL, Date, setTimeout')
 t=t.replace('The seven tests currently prove:', 'The initial seven tests prove:')
 t=t.replace('and `expectedVersion` where applicable','and the absence of an expected-version precondition on this PATCH')
 t=t.replace('The all-pages or reorder algorithms remain appropriate for this small implementation;', 'The reorder algorithm is designed for this small implementation;')
 t=t.replace('**Exercise 4.** Add a test that sends `description: {}` after a valid title and proves `$transaction` was never called.','**Exercise 4.** Extend the malformed-field test with a valid title followed by `description: {}` and prove `$transaction` was never called.')
 p.write_text(t,encoding='utf-8')
p=U/'README.md';t=p.read_text(encoding='utf-8');start=t.index('The recorded executable evidence');end=t.index('The nine checkpoints',start)
t=t[:start]+'''The [recorded test output](evidence/root-handler-tests-01.log) contains eleven passing Node cases: two helper cases and nine actual route/API cases. The route suite loads production modules with vm.SourceTextModule and replaces Prisma, identity and framework seams. It checks successful and rejected PATCH, move and bulk-sprint paths, including a same-sized foreign population and an unchanged date represented with a different timezone offset. These checks establish observable handler behavior and database-call grouping. They do not establish real database rollback, concurrency or trusted identity. See [verification](VERIFICATION.md) for the full build and lint evidence.

''' +t[end:];p.write_text(t,encoding='utf-8')
p=U/'04-TESTING-AND-DEBUGGING.md';t=p.read_text(encoding='utf-8');t+='''
## What final review added

The final suite contains eleven tests, including a positive move that places an issue after two siblings, a successful bulk plan that updates only the one changed row, a same-sized foreign batch that rejects before writes, and missing/foreign PATCH relation checks. A no-op due date uses equivalent UTC and offset strings; the VM receives the host Date constructor so a host-built fixture date has the same instanceof semantics as a production Date. These positive controls make an implementation that rejects every request fail the suite.

The transaction callback is a mock seam. Capturing an activity on the transaction client proves the handler uses that client; it cannot prove SQLite rolls it back. The move activity still runs after its transaction. A SQL-backed follow-up should inject a failure after the first successful write and inspect the same tables from a separate connection, using a disposable database. Never interpret the current mutable fixture as a database isolation test.
''';p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8');start=t.index('Exercise 7:');end=t.index('Exercise 8:',start)
t=t[:start]+'''Exercise 7's trace table starts with parsing (JSON read, no writes), authorization (actor/project reads, no writes), candidate validation (issue and relation reads, no writes), commit (issue/activity/notification writes), and response (broadcast then 200 JSON). An array assignee stops at candidate validation with 400 and no transaction. A null clear reaches the transaction and writes an activity for a changed assignment, without an assignment notification. A same-value patch stops before the transaction and returns the existing record with 200. The 422-versus-302 wrapper example belongs to Exercise 5D, not the request-flow trace.

''' +t[end:]
t=t.replace('Keep `root-luna-jdtrrain-final-01` as the executable evidence label and report the earlier direct launch failure only as a tooling limitation if it is discussed.','Use root-handler-tests-01 as the final test evidence label. Earlier runs were intermediate checks, not additional test cases.')
t+='''
## Complete route test fixture

The following is the complete current `tests/issue-routes.test.mjs`. It contains imports, VM loading, framework stubs, fixture construction and all nine route/API cases. The two helper cases live in the separately linked issue-input.test.mjs file. These methods already exist in the project; modify them when practicing rather than pasting a second copy beside them. The production algorithms are loaded from their source files, while the fake persistence methods return records and capture writes.

```js
'''+(P/'tests/issue-routes.test.mjs').read_text(encoding='utf-8')+'```\n';p.write_text(t,encoding='utf-8')
(U/'VERIFICATION.md').write_text('''# Verification and limits

Run from the jdtrrain2.1 project root. Node 22.16 was used for the recorded tests, and package.json declares pnpm10.18. Use the included pnpm lockfile for installation. The test harness itself uses only Node built-ins, but the application build needs the installed Next and generated Prisma client packages.

```powershell
pnpm install --frozen-lockfile
$env:DATABASE_URL = 'file:./astra-validation-placeholder.db'
pnpm db:generate
pnpm test
pnpm lint
pnpm build
```

The placeholder database URL is used for client generation and compilation. These commands do not initialize, push, reset or seed a database. Do not run db:reset while reproducing this review: it is a separate destructive database command and is unnecessary for these checks. A learner running the full app later must configure an explicitly chosen local database and follow its setup instructions separately.

The final [handler test log](evidence/root-handler-tests-01.log) records eleven tests, eleven passes and zero failures. Two cases test the actual input helpers; nine load the actual route/API modules using vm.SourceTextModule and Node's experimental VM module flag. The package test script includes the required flag. Prisma, identity middleware, NextResponse and external event/Slack seams are replaced with controlled fixtures. The actual shared API body parsing and error handling still execute.

The suite covers malformed JSON, field types, nullable clears, unchanged values, integer bounds, equivalent date offsets, missing and foreign relations, positive PATCH side effects, positive destination ordering, changed-only bulk updates, foreign bulk populations, and sanitized unexpected errors. It cannot prove database rollback, isolation, row constraints, session authentication, browser rendering or a live Next adapter. Move activity remains outside its transaction; POST creation retains earlier relation and side-effect gaps. PATCH has no expected-version check, so concurrent editors can overwrite one another and audit old values from a stale read.

The final build and lint results are recorded in the evidence folder and summarized in results.json after review. A build proves module compilation and bundling, not an operational database. No Slack call, live account or deployed service was used. Review the [input helper](../src/lib/server/issue-input.js), [PATCH](../src/app/api/issues/route.js), and [test fixture](../tests/issue-routes.test.mjs) together when extending the contract. Numeric strings remain accepted intentionally; dueDate accepts JavaScript-parsable date strings rather than a strict calendar-date grammar.

**Exercise 8.** Write a verification note using the final eleven/eleven/zero counts, the VM module test mechanism, and the recorded build/lint outcomes. Name one conclusion supported by the actual handler calls and one that still requires a real database or browser check.
''',encoding='utf-8')
print('Updated actual contracts, portable verification, trace solution and complete fixture')
