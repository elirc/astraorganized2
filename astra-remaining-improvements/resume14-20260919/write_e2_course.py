from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
P=B/'stage/f98b34acf094'
chapters={
'README.md':('Northstar CMS: publication and validation boundaries',"""
This course follows a real CMS request from a Next.js handler into a process-local content store. The improvement has two connected purposes: public readers must not obtain drafts by choosing a query parameter, and rejected writes must leave entries, revisions and audit history unchanged. You will study working code rather than treating the presence of a Prisma schema as evidence of database persistence. The running services still use JavaScript collections on globalThis.

Start with JavaScript objects, promises, HTTP status codes and TypeScript unions. You should be comfortable reading an object spread and explaining the difference between a missing property and one explicitly set to null. You do not need prior knowledge of content management systems. A content type defines fields; an entry supplies values; a revision captures a previous accepted state; an actor is the user or API token associated with a request. See contracts.ts, store.ts and cms-api.ts for these definitions.

Install from the project root with `npm ci`, then use `npm test`, `npm exec tsc -- --noEmit`, `npm run lint` and `npm run build`. Run `npm run dev` for the local learning UI. Use the local login endpoint for a fresh session; the seeded session can expire. The CLI and browser assume the same single process, and restarting that process resets mutations to seeded data.

Read chapters 01 through 04 before changing anything. Work through the three exercises in chapter 05, compare your results with chapter 06, and then trace a request without running it using chapter 07. VERIFICATION separates observed checks from untested deployment properties. The API tests stub fetch, so they cannot accidentally call configured webhook destinations. Demo credentials, reset previews and simulated administration remain learning scaffolding; this change is not a production authentication redesign.
""",None),
'01-CODEBASE-MAP.md':('Code map and reading order',"""
Read `src/app/api/[uid]/route.ts` first. Its GET handler awaits the dynamic uid parameter, copies the query, resolves the actor only when preview is requested, and removes unauthorized preview before calling listEntries. This placement matters: filtering after pagination could reveal an inaccurate total or return an empty page even when published entries exist. POST delegates identity to requirePermission before reading and validating the request body.

Continue with the sibling `[id]/route.ts`. GET hides deleted entries from every actor and hides unpublished entries from callers lacking read permission. PUT selects publish, unpublish, archive or ordinary update. Publication failures are mapped to a 400 response before JSON serialization; missing entries produce 404. These route modules export only supported HTTP handlers, matching the installed Next documentation.

`src/lib/server/cms-api.ts` translates cookies and bearer tokens into RequestActor. Token scope and user permission are separate branches. A write-only API token does not automatically gain preview access. `src/lib/config/env.ts` makes x-demo-role opt-in and disables it in production. Ordinary local sessions remain usable without that header.

`src/lib/cms/store.ts` owns entries, content types, revisions and audit logs. `entry-validation.ts` validates a candidate without mutating these collections. `query.ts` handles filtering, paging, sorting and public projections. This split makes it possible to test primitive conversions independently and still test actual HTTP entry points. The `tests/cms-boundaries.test.ts` suite does both.

The source snapshots under this course preserve the original files for comparison. Existing docs describe the larger scaffold; this course focuses on changed request and state boundaries. Store accessors used by trusted server code still expose mutable state, so do not export those objects to new callers as an unrestricted write API. Public list projections now clone nested values.
""",('src/app/api/[uid]/route.ts',1,27)),
'02-CONCEPTS.md':('Permission, presence and candidate validation',"""
A query parameter is a requested representation, not proof of authority. A caller can ask for preview, but the handler decides whether that caller may read drafts. For users this means entries:read; for API tokens it means read or manage scope. The same principle applies to identifiers: knowing a draft ID does not grant access to the draft. A useful test compares collection reads with single-item reads so one route cannot bypass the other.

Validation must happen before mutation. Constructing a candidate first allows a rejected number, locale or field name to return an error without increasing the entry version or adding a revision. Testing only the error message is weaker than comparing an independent snapshot of the entire store. A snapshot must clone nested objects; holding another reference to the original store would conceal a mutation.

Presence has its own meaning. An omitted field may receive its configured default during creation. Explicit null requests a clear and must not silently turn into the default. False and zero are real values rather than missing values. Partial updates merge the existing accepted values with the provided patch before validating the candidate, so omission preserves existing content. Arrays and strings are not accepted as values maps.

Coercion should be small and deliberate. Numeric strings can become finite numbers, and the strings true and false can become booleans. Arrays, objects and whitespace do not become zero. Invalid JSON text is rejected; a quoted JSON string is valid JSON and remains a string after parsing. The recursive JSON check rejects nonfinite numbers and cyclic objects for direct service callers.

Finally, a public DTO should be detached from storage. Copying only the outer attributes object is insufficient when SEO data contains nested arrays. structuredClone in the projection prevents a caller mutating a nested result from changing the accepted entry. This is object ownership, not a database transaction or a cross-process concurrency mechanism.
""",('src/lib/cms/query.ts',172,200)),
'03-WORKED-CHANGE.md':('Worked change: validate before publishing state',"""
The original validator selected values with nullish coalescing. That treated an explicit null like an omitted field and could restore a default unexpectedly. Boolean coercion converted every value other than true into false. As a result, malformed values could become apparently valid state. The staged draft also left publication free to resurrect archived or deleted entries and did not revalidate entries after a content-type change.

The new entry-validation module checks the outer shape, rejects unknown field names and uses own-property presence to choose a default. It then validates field-specific types and bounds before producing a separate candidate map. Creating an entry performs locale validation before allocating a record. Updating checks the original lifecycle and validates merged values before replacing the existing map. The audit and revision functions are reached only after validation succeeds.

Publication reuses the current content-type rules. If a new required field was added since an entry was drafted, publication returns an error without changing status, timestamps or revision count. Archived and deleted records cannot be implicitly restored by publish or unpublish. Repeating publication of an already published, valid entry returns the existing record and does not duplicate its history.

Use the excerpt below as part of the actual store module, not as a standalone program: its helpers and module state are defined earlier in that file. Run `npm test -- -t "prevents invalid partial edits"` from the project root to exercise the workflow. The test creates an entry, tries an invalid edit, changes its schema, attempts publication, then verifies a valid publish and a refused archived-state update. It compares whole-store snapshots at the failure points.

A meaningful variation is to alter the default-value selection back to nullish coalescing. The explicit-null assertion should then fail. Restore the implementation before continuing. This mutation demonstrates why the presence test matters rather than merely asserting that a helper returns a particular value.
""",('src/lib/cms/store.ts','export const publishEntry =','export const unpublishEntry =')),
'04-TESTING-AND-DEBUGGING.md':('Tests that observe routes and state',"""
The regression file imports the actual GET, POST and PUT handlers. NextRequest constructs real request objects, and route parameters are promises, as required by this version of Next. Assertions check status codes, nonempty successful results, filtered totals and exact saved values. A test that only called every on an empty array would pass without proving public data remained accessible; the suite requires a real published result.

The suite restores a deep-cloned store baseline before every test. It replaces global fetch with a deterministic response and restores globals afterwards. This prevents webhook execution from depending on the network and makes rejected-write assertions stronger: invalid input must cause no fetch call at all. The fixture uses a freshly authenticated local session rather than relying on the seeded session's expiration date.

Failure-state tests compare complete independent snapshots, including entries, revisions and audits. Query tests use numeric versions 2 and 10, plus equal values with different IDs, to distinguish numeric ordering from lexical ordering and expose unstable ties. Detached-result tests mutate an SEO array in a returned DTO and assert the stored array is unchanged.

Run the full test command before the build. If the preview test fails, inspect which actor branch was resolved; check cookie name, expiration, token scope and permission before changing visibility logic. If a state snapshot differs after rejected input, find the first write preceding validation. If TypeScript rejects a test helper, repair the fixture to match real interfaces rather than widening production input types to silence it.

These checks prove process-local behavior and handler contracts. They do not demonstrate durable transactions, multi-worker shared state, reliable webhook delivery or browser end-to-end flows. A passing production build demonstrates compilation and route generation, not deployment safety. Keep those distinctions when extending the course to a real repository layer.
""",('tests/cms-boundaries.test.ts','  it("exercises authorized create','describe("CMS validation')),
'05-PRACTICE.md':('Three focused exercises',"""
Exercise 1: add an optional rating field to a cloned content-type fixture, using number type with min zero and max five. Write table-driven tests for 0, 5, negative one, six, a numeric string, whitespace, a boolean and Infinity. Predict which inputs normalize and which are rejected before running the tests. Check errors and the normalized candidate together. Do not change the real seeded content type for this exercise. The acceptance condition is that invalid candidates cause no store mutation when passed through createEntry.

Exercise 2: extend the authorization matrix. Create a manage token and a write-only token with issueApiToken. Give both the same draft detail URL and preview collection URL. Expect manage to read the draft and write-only to see the same public projection as an anonymous caller. Then mark the draft deleted in a controlled fixture and show that neither actor can read it. Use a nonempty published control record so hiding all entries cannot accidentally satisfy the exercise.

Exercise 3: add a regression for a missing required field after the content type changes. Create an accepted draft, append a required field to the test store's type, and invoke the actual PUT publish route with a write token. Assert 400 and compare a deep store snapshot taken after the schema change but before publication. Update the draft with the required field, publish successfully, and assert that a second publish does not add a revision or audit. Restore all fixture state afterwards.

For each exercise, write a short explanation of the first rejected boundary, the observable HTTP or service result, and the state that must remain stable. Include the exact command you ran. A screenshot or an error message alone is insufficient evidence. Keep fetch stubbed and work only with cloned or resettable demo state. These exercises extend the existing suite; they do not require a real database, external webhook destination or production credentials. Solutions and review hints are in chapter 06.
""",None),
'06-SOLUTIONS-AND-REVIEW.md':('Solutions and review criteria',"""
For exercise 1, extend only the fixture's fields array. A rating of zero must survive because the validator tests presence and type, not truthiness. Five is accepted at the upper boundary; negative one and six are rejected by min and max. The string zero normalizes to number zero. Whitespace, booleans and Infinity fail coercion. Assert against values.rating after successful normalization and require a nonempty errors list for each rejected candidate. Then call createEntry using a controlled type registered in the test store and compare the store snapshot for one invalid case.

For exercise 2, use the API-token factory already present in cms-boundaries.test.ts. The helper calls the real issueApiToken service and returns the plaintext token only to the test. Send it in an Authorization bearer header. The read permission branch explicitly accepts manage and read scope. A write-only token fails that branch even though it can submit edits. Both list and item routes must hide deleted entries. Do not add a production shortcut that treats any token as a reader simply to make the test pass.

For exercise 3, use the existing publication regression as a service-level reference and the create/update route test as the HTTP reference. Construct a NextRequest with method PUT and action=publish in its URL. Take the snapshot after adding the new schema field, so the assertion isolates publication's effect rather than expecting the intentional schema change to disappear. A successful correction uses updateEntry before publication, preserving the original ID and incrementing revisions only for accepted operations.

Review a solution by tracing validation and mutation order. The test must reach the intended failure, not stop earlier because the token is invalid or the body is malformed. Error assertions should be accompanied by state assertions. Parameterized primitive tests and real route tests complement each other: one isolates conversion semantics, while the other verifies that the application actually uses the boundary. Treat extra authentication, uniqueness or persistence features as separate exercises with their own contracts.
""",('tests/cms-boundaries.test.ts','  it("preserves defaults','  it.each([true')),
'07-TRACE-LAB.md':('Trace a preview read and a rejected publication',"""
Trace A begins with GET /api/article?publicationState=preview&pageSize=1 and no credentials. Predict the handler's result before execution. The uid resolves to the article content type. resolveActor returns null, so the handler removes preview from its copied query. listEntries passes the store and type to applyEntryQuery. That function filters to published entries before calculating total and before selecting the one requested item. The response therefore describes the public collection, not a page selected from drafts and subsequently filtered.

Repeat the trace with a valid read token. Token resolution checks its stored hash, revocation and expiration. The handler retains preview because read scope is allowed. Deleted entries are still removed by the preview filter. A write-only token follows the anonymous visibility outcome; it is not equivalent to a read token. At each branch, record the actor kind, effective publicationState, total and returned IDs.

Trace B begins with a draft that was valid when created. An administrator changes its type by adding a required field. A caller now sends a publish request. requirePermission first establishes permission to publish. publishEntry obtains the current entry and current type, checks lifecycle, and validates the values against that current definition. The missing field produces an error. The route responds with 400; status, version, timestamps, revisions, audits and webhook deliveries remain unchanged.

Now supply the field through an accepted update and retry publication. The successful path changes status and metadata, snapshots the values, records the audit and attempts webhook fan-out. This last action is outside a durable transaction: the in-memory mutation is not rolled back by an external delivery failure. Explain that boundary without claiming a database guarantee.

Finish by tracing a public query result back to its source entry. Change one nested result value in a test. The clone breaks object identity with the store, so this change cannot bypass createEntry or updateEntry. Draw the two distinct object graphs and label which one is authoritative within this single process.
""",None),
'VERIFICATION.md':('Verification and repeatable commands',"""
The final delivery records terminal results for the actual test suite, TypeScript check, lint and Next production build. This chapter is updated from the saved command records only after they complete successfully. The initial resumed test run caught an expired seeded-session fixture; the corrected fixture obtains a fresh local session. Earlier four-check summaries counted commands, not four independently sufficient correctness cases, and are superseded by the expanded suite.

Repeat from the canonical project root using the checked-in package lock: npm ci, npm test, npm exec tsc -- --noEmit, npm run lint, and npm run build. Node 22 was used for the local checks. No original database was initialized or reset. The current store is process memory, even though prisma/schema.prisma describes an intended future data model. Do not interpret a successful build as a migration or a durable storage test.

The tests import actual route handlers, construct NextRequest objects, await promised parameters and compare actual JSON responses. They also call the real services for malformed-value and lifecycle matrices. Fetch is replaced during tests, so webhook destinations are never contacted. Numeric ordering, stable ID ties and detached nested projections are exercised directly. Tests restore the baseline between scenarios so one invalid or successful write cannot contaminate another case.

Limits remain explicit. Authentication scaffolding includes demo accounts and reset previews and is suitable for local learning. x-demo-role is disabled unless explicitly enabled outside production; this does not redesign every administration endpoint. Store getters used by trusted server modules still expose mutable objects. Webhook signing still uses the existing header convention and delivery state is not durable; no HMAC or exactly-once claim is made. No deployment, live provider or browser end-to-end run is included in these regression results.

Original snapshots and the delivery manifest identify what changed. The report records failures as well as the passing final checks. Future edits should rerun the relevant contract tests and refresh the evidence rather than retaining this completion claim unchanged.
""",None),
}
nav='\n\n## Course navigation\n\n'+' / '.join(f'[{k.removesuffix(".md")}]({k})' for k in chapters)+'\n'
for name,(title,body,excerpt) in chapters.items():
 text='# '+title+'\n\n'+body.strip()+'\n'
 if excerpt:
  filename,start,end=excerpt;source=(P/filename).read_text(encoding='utf-8-sig')
  if isinstance(start,int):sample='\n'.join(source.splitlines()[start-1:end])
  else:sample=source[source.index(start):source.index(end,source.index(start))].rstrip()
  text+='\n## Source excerpt\n\nFrom ['+filename+'](../'+filename.replace('[','%5B').replace(']','%5D')+'). The surrounding imports and setup are in the linked file.\n\n```ts\n'+sample+'\n```\n'
 text+=nav
 assert len(text.split())>=250,(name,len(text.split()))
 (P/'astraupskill'/name).write_text(text,encoding='utf-8')
 print(name,len(text.split()))
readme=P/'README.md';text=readme.read_text(encoding='utf-8')
if 'astraupskill/README.md' not in text:
 text+='\n## CMS boundary learning course\n\n[Start the source-based course](astraupskill/README.md) for public publication rules, typed content validation, atomic rejection and the regression suite.\n'
 readme.write_text(text,encoding='utf-8')
