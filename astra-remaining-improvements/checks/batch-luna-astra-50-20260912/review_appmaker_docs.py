from pathlib import Path

B=Path(__file__).resolve().parents[2]
P=B/'stage/b7429e8bf71d'
U=P/'astraupskill'
replacements={
'01-CODEBASE-MAP.md':[
('For a production application, those messages should be sanitized consistently; this slice records the distinction between intended validation responses and unexpected driver failures without introducing a new logging service.', 'These modified routes use safeErrorResponse: InputError returns its intended 400 diagnostic, SyntaxError maps to generic Invalid JSON with 400, and unexpected errors return a route-specific generic 500. Server logs retain diagnostics. Other API routes were not audited by this increment.'),
],
'02-CONCEPTS.md':[
('range updates plus ticket update','contiguous sibling-position rewrite plus ticket update'),
('The project-wide running check','The application-wide running check'),
],
'03-WORKED-CHANGE.md':[
('The current helper is pure and the test plan is explicit about generated temporary clients, but the singleton in `lib/db.ts` still follows the schema’s development URL. A factory would make route tests more direct while preserving normal Next startup.', 'The manual/start handler factories already accept an injected client. The other route wrappers still import the singleton in `lib/db.ts`, which follows the schema’s development URL. Extending that seam to stop/PATCH/move wrappers would enable direct response tests without mutating the real singleton; it would not by itself prove SQLite transactions.'),
],
'04-TESTING-AND-DEBUGGING.md':[
('They use fakes for Prisma method arguments where a generated client is unavailable;', 'They use deliberately injected Prisma fakes, although client generation also passes;'),
('and let root capture the Next build', 'and run npm run build'),
],
'06-SOLUTIONS-AND-REVIEW.md':[
('then the route loads B1 and compares', 'then the service opens its transaction, loads B1 and compares'),
('The mismatch throws before `$transaction`; status is 400', 'The mismatch returns invalid-target from inside `$transaction`, before any updates; the route maps that result to status 400'),
('compare project ids, and throw before opening the write transaction.', 'compare project ids inside the transaction, and return invalid-target before the first write.'),
('For a foreign target, parse first, read the ticket, read the target column,', 'For a foreign target, parse first, enter the transaction, read the ticket, read the target column,'),
],
'07-TRACE-LAB.md':[
('The route awaits params, parses JSON,', 'The route awaits params, verifies that the ticket exists (otherwise 404), parses JSON,'),
('2700 is a safe integer; notes stays undefined.', '2700 fits Prisma Int; notes stays undefined in the parser and becomes null in create data.'),
('The demo’s fallback identity remains outside this trace.', 'There is no trusted actor resolver in these routes; project consistency does not establish user authorization.'),
],
}
for name,pairs in replacements.items():
 p=U/name;t=p.read_text(encoding='utf-8-sig')
 for a,b in pairs:t=t.replace(a,b)
 p.write_text(t,encoding='utf-8')

p=U/'03-WORKED-CHANGE.md';t=p.read_text(encoding='utf-8')
marker='## Follow the actual conditional write'
if marker not in t:
 source=(P/'lib/time-entry-service.ts').read_text(encoding='utf-8-sig')
 block=source[source.index('export async function stopRunningEntry'):source.index('export async function startTimer')].strip()
 t+='\n'+marker+'\n\nThe executable service below is copied from lib/time-entry-service.ts. Read each await as a point where another request may run. The conditional update protects the running-to-stopped transition. The final lookup can observe a subsequent notes/duration edit, so this code does not promise a byte-identical replay or lock the returned representation.\n\n```ts\n'+block+'\n```\n\nFor a deterministic exercise, call this with start 2025-01-01T10:00:00Z and requested end 2025-01-01T10:00:05Z. The update data must contain duration 5. Passing undefined notes omits the property, whereas null includes it. The tests below observe these exact Prisma arguments. A losing count returns a conflict before the final lookup.\n'
 p.write_text(t,encoding='utf-8')
p=U/'06-SOLUTIONS-AND-REVIEW.md';t=p.read_text(encoding='utf-8')
marker='## Complete executable companion'
if marker not in t:
 fixture=(P/'tests/time-entry-validation.test.ts').read_text(encoding='utf-8-sig')
 t+='\n'+marker+'\n\nThis is the complete delivered test file, including imports and all doubles. Run the existing file with npm test; if experimenting, change that file rather than adding a second duplicate suite. The partial doubles intentionally use any only in this test file. They demonstrate argument shapes and branch behavior, not generated database constraints or transaction rollback. The board fake mutates objects immediately and has no rollback implementation.\n\n```ts\n'+fixture.rstrip()+'\n```\n\nThe foreign-target case performs no updates. The same-column and cross-column cases assert identity ordering and numeric positions. A production database failure midway through parking or rewriting is not simulated here. Ticket positions have no unique schema constraint, so temporary negative positions should not be presented as proof that a future uniqueness migration is safe.\n\nExercise 8 remains a proposed integration task: create a unique OS temp directory, construct a PrismaClient with an absolute SQLite datasource override, apply the schema to that same URL, seed only that client, and disconnect before removing only that owned directory. Do not run the existing destructive demo seed or assume DATABASE_URL overrides the hardcoded schema URL. Exercise 9 is executed in the complete manual handler case above: a thrown SyntaxError maps to Invalid JSON/400 and a driver Error with a synthetic secret maps to the generic create fallback/500.\n'
 p.write_text(t,encoding='utf-8')
print('Reviewed Appmaker course corrections and complete fixture written.')
