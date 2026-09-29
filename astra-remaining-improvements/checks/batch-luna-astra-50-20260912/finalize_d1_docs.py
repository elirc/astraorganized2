from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parents[2]; ID='61d919e84af9'; P=B/'stage'/ID; U=P/'astraupskill'
(U/'VERIFICATION.md').write_text('''# Verification and limits

Start in the project root with Node.js and npm installed. The recorded environment used Node 22.16.0 and Next 14.2.30. Install the locked dependencies, then run the finite checks below. The synthetic connection string satisfies module configuration; these commands do not start PostgreSQL or connect a browser to the application.

```powershell
npm ci
$env:DATABASE_URL = "postgresql://test:test@127.0.0.1:65432/unused"
npm test
npm run typecheck
npm run lint
npm run build
```

The build now compiles the application without automatically running database generation or migration. Those operations are separate package scripts. The supported `next.config.mjs` is selected by this Next version; the original `next.config.ts` remains available as an inactive historical configuration. Tailwind 4 loads its PostCSS plugin and explicitly imports the existing theme configuration. The generated stylesheet was inspected for the custom accent color and soft shadow classes. That establishes stylesheet generation, not visual correctness in a browser.

The four finite Node tests in [socket-actions.test.ts](../tests/socket-actions.test.ts) use a FakeSocket and injected service functions. They establish authorization before room joins, preservation of a prior room after denied access, heartbeat membership checks, leave/disconnect cleanup calls, strict update payload validation, and omission versus explicit null handling. The fourth test verifies the exact object built for Drizzle's `.set` argument. It does not execute SQL. The additional move and asynchronous-error examples in the solutions chapter are proposed extensions and are not counted among those four tests.

Read the JSON command records together with their complete logs under `evidence`. Exit zero for a build means compilation, static generation and build tracing completed. It does not prove the custom server started, a real socket handshake authenticated, a database row committed, or an outbox message was delivered. Lint may report warnings while still returning zero; inspect them before claiming a warning-free project. The final machine-readable results identify the authoritative check labels.

Database integration remains the main next learning step. Create an isolated test database, perform an update followed by a deliberately failing audit insert, and assert that the transaction commits neither operation. Race two board changes and verify that the atomic SQL version increment allocates distinct versions. `appendBoardEvent` accepts either a transaction or the shared database executor: archive, restore, template and role paths still call it outside an enclosing transaction. They are not claimed to have full transactional atomicity.

Authentication still trusts demo headers and a fallback user. Presence is process-local; concurrent joins, revoked membership after a join, multiple tabs sharing one member, and distributed cleanup need additional integration coverage. Empty patches can still increment versions. Existing optimistic drag ordering and non-text filter behavior also remain separate exercises. The course explains these limits so you can distinguish a useful tested improvement from a complete production system.
''',encoding='utf-8')
readme=P/'README.md'; t=readme.read_text(encoding='utf-8-sig') if readme.exists() else '# Collaborative Kanban Board\n'
if 'astraupskill/README.md' not in t: readme.write_text(t+'\n\n## CRUD engineering learning course\n\nStart with the [nine-chapter learning course](astraupskill/README.md) for the socket boundary, update semantics, worked regression examples, exercises and verification limits.\n',encoding='utf-8')
s=B/'specs'/f'{ID}.json'; spec=json.loads(s.read_text(encoding='utf-8-sig'))
for n in ['README.md','next-env.d.ts']:
 if n not in spec['changedFiles']:spec['changedFiles'].append(n)
spec['checks']['format']='json'
s.write_text(json.dumps(spec,indent=2),encoding='utf-8')
print('D1 documentation updated; final evidence pending accessibility fix and checks.')
