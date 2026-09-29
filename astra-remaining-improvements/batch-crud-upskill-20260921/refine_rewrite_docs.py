from pathlib import Path
p=Path(__file__).resolve().parent.parent/'stage/c81c4e873d3b/astraupskill'
for f in p.glob('*.md'):
 s=f.read_text(encoding='utf-8-sig')
 replacements={
 'then reads the route source to ensure the slug crosses the layer boundary':'then executes the registered DELETE handler with router and response doubles to check the slug crossing the layer boundary',
 '?does this row exist anywhere??':'"does this row exist anywhere?"',
 'The data layer does not need to repeat the slug on deletion because the guarded read already established the relation for this bounded operation; a transaction would be a further concurrency hardening outside this change.':'The write still uses only the id after that guarded read. This demonstrates the sequential path, but does not atomically preserve the read conditions if another operation changes the relationship or author before deletion. Conditional writes and database isolation require a separate design and test.',
 "`findFirst` is intentional: Prisma cannot use a relation predicate in `findUnique`'s unique-only selector.":'`findFirst` makes both identity predicates explicit in the read. The choice here does not establish which other selector shapes a particular Prisma version supports.',
 'The source assertion catches the latter seam in this dependency-free run.':'The executed handler case catches that seam without mounting Express.',
 '?expected implementation?':'"expected implementation"',
 'The fourth reads `articles.ts` and checks that the route actually passes `req.params.slug`.':'The fourth loads `articles.ts`, captures the registered nested DELETE callback using a router double, and executes it with the real repository. It checks the passed slug, 204/404/403 outcomes, success-only deletion, and forwarding of the exact delete error to `next`.',
 'route-source assertion':'handler assertion',
 'crud-b03-rewritepy2js-runtime1':'crud-b03-astra-runtime',
 '?returned false but still deleted?':'"returned false but still deleted"',
 '?not demonstrated?':'"not demonstrated"',
 '?false?':'"false"',
 'supplies a Prisma double and reads route text rather than mounting Express':'supplies Prisma, Express router, middleware and response doubles instead of mounting an Express server',
 'cases 1?3 cover the repository states, and case 4 covers the route argument wiring.':'cases 1-3 cover repository states, and case 4 executes the route callback and actual repository together across success, missing, forbidden and delete-error outcomes.',
 'The test loads actual staged TypeScript and stubs only the Prisma module.':'The test loads actual staged repository and route TypeScript with explicit Prisma, router, middleware, schema and response adapters.',
 'They do not count source inspection as a runtime behavior test except for the route wiring assertion, which is labeled separately in the test name.':'All four now execute production behavior. The earlier fourth case was a source-text assertion; root replaced it with actual handler execution and captured a new run.',
 }
 for a,b in replacements.items():s=s.replace(a,b)
 f.write_text(s,encoding='utf-8')
