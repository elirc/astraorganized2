from pathlib import Path
B=Path(__file__).resolve().parent.parent
names=['README.md','01-CODEBASE-MAP.md','02-CONCEPTS.md','03-WORKED-CHANGE.md','04-TESTING-AND-DEBUGGING.md','05-PRACTICE.md','06-SOLUTIONS-AND-REVIEW.md','07-TRACE-LAB.md','VERIFICATION.md']
courses={
'40905c751e8c':[
'''# Derived onboarding progress

Study [OnboardingProgressService](../backend/src/modules/onboardingCases/onboardingProgress.service.ts), which turns task rows into a stored case percentage and lifecycle status. The [runtime lab](../tests/onboarding-progress-runtime.test.mjs) loads the existing implementation with a Prisma-shaped adapter. Production behavior is unchanged.

This workshop combines arithmetic prediction, payload inspection, a history-preservation exercise and failure tracing. Begin with COMPLETED, SKIPPED and IN_PROGRESS tasks. Then compare a newly complete case with a previously completed case whose tasks reopen. The important distinction is between returning a number and persisting a case update: the empty-task branch returns zero without writing. The tests make that boundary explicit instead of claiming database correctness from an in-memory adapter.''',
'''# From task rows to case write

recalculateOnboardingProgress accepts caseId and an optional transaction client, defaulting to the imported prisma singleton. It queries onboardingTask.findMany with onboardingCaseId. With no tasks it returns zero immediately. Otherwise COMPLETED and SKIPPED rows count toward Math.round(completed / total * 100).

The service next reads the case status and completedAt. It always prepares progressPercent for nonempty task sets. At100 it marks COMPLETED and adds a timestamp only if absent. Below100 it changes an already completed case to IN_PROGRESS without clearing history. onboardingCase.update receives the same case id. The runtime fixture records these calls; it does not open a transaction merely because a client argument is named tx.''',
'''# Derived values and historical fields

Progress percentage is derived data, while completedAt records history. Recomputing percentage does not mean every related column should be overwritten. The service preserves an existing completion timestamp even when tasks reopen, and it avoids replacing that timestamp on repeated completion.

An empty set illustrates another distinction: a return value can differ from stored state. Returning zero does not reset a previously stored percentage because that branch performs no case update. Discuss whether product behavior should retain or clear the old value before changing the implementation. The service also assumes a case exists after a nonempty task read; the lab does not invent a missing-case domain error that this source does not provide.''',
'''# Work through two of three tasks

Set tasks to COMPLETED, SKIPPED and IN_PROGRESS, with case status IN_PROGRESS and no completion date. Two rows count as finished, so the result rounds to67. The expected write is {where:{id:'case1'},data:{progressPercent:67}}. There is no status or completedAt property in that payload.

The runtime case asserts both the task filter and the selected case fields before checking the exact update payload. Now change the last task to COMPLETED. Predict100, a COMPLETED status and a new timestamp. Compare this with an already dated case, where completedAt is omitted to preserve history. These are exercises over existing production behavior; the delivered change adds executable teaching material, not a new progress algorithm.''',
'''# Debug percentages and write boundaries

Run node --experimental-vm-modules --test tests/onboarding-progress-runtime.test.mjs from the project root. The loader evaluates the real service and substitutes only its relative Prisma import. The fake client records query arguments and update data, so an unexpected percentage can be traced back to task statuses rather than a copied implementation.

Check rounding separately from status decisions:67 is Math.round of two thirds, not a stored decimal. Check property presence for timestamps rather than comparing a fabricated clock. The explicit-client test supplies a different client and asserts that the default adapter was untouched. Neither this check nor a successful callback proves database commit, isolation, or authorization.''',
'''# Practice before reading answers

First predict the return and update payload for one SKIPPED task and two NOT_STARTED tasks. Include whether status and completedAt appear when the case is already COMPLETED. Then predict an empty task list for that same case, separating return value from persisted state.

Next extend the fixture with all tasks complete and an old completion date. Write an assertion that catches accidental timestamp replacement without relying on exact current time. Finally propose a concurrent experiment where a task changes between the list query and case update. Identify the two persisted values you would inspect and explain why an adapter-only unit test cannot prove the resulting database invariant.''',
'''# Answers and review criteria

One SKIPPED row out of three gives33. If the case was COMPLETED, the payload includes progressPercent33 and status IN_PROGRESS; completedAt is omitted. An empty list instead returns zero and performs no case read or update, so previous persisted state may remain.

For repeated completion, assert that the payload has no completedAt property when a date already exists. A concurrency experiment should inspect both final task statuses and the stored case percentage after synchronized writes. Reviewers should ask whether recalculation runs inside the caller's transaction and what isolation that client provides. Passing a transaction-shaped object in this lab proves client selection only. Avoid claiming that the service itself starts a transaction.''',
'''# Trace a late write failure

Supply an explicit client whose task query returns one COMPLETED row and whose case query returns IN_PROGRESS with no completion date. Make its case update throw write unavailable. Predict the promise rejection and verify the default prisma adapter records no calls.

The trace reaches task read, case read, payload construction and attempted case write. A returned percentage never reaches the caller because the awaited write rejects first. This observation does not tell us whether a real provider partially committed anything. For a follow-up database exercise, wrap recalculation in the application's actual transaction and inspect the stored case after an injected failure. Keep that proposed integration experiment distinct from the executed unit trace.''',
'''# Verification boundaries

Five cases execute the actual progress service: rounded percentage and query scope, empty-task early return, first and repeated completion, reopening with historical timestamp preservation, and explicit-client late failure. The source snapshot is [the original service](snapshots/onboardingProgress.service.ts.original.txt). No production implementation changed.

The evidence covers service control flow and exact adapter payloads. It does not execute Prisma, HTTP authorization, database locks, task mutation routes or concurrent recalculation. Missing cases after a nonempty task query are not modeled as a safe domain response. The empty-task branch intentionally documents current behavior instead of silently changing product policy. Use the runtime command in the debugging chapter and read terminal results alongside these limits.'''
],
'859e461c9fd8':[
'''# Helpdesk permission policy workshop

Read the actual [hasPermission helper](../backend/src/shared/utils/permissions.ts) and run [the permission lab](../tests/permissions-errors.test.mjs). This is a focused authorization lesson for CRUD operations: creation, broad reading, own-record reading, updating, deletion and administrative actions have different permission strings. Production policy is unchanged.

Start with a role-action table, predict each boolean, then examine two tricky cases: REQUESTER has ticket:read:own but not ticket:read, while OWNER's wildcard accepts even an unknown permission name. The exercises connect policy lookup to the separate responsibility of filtering rows. A boolean permission helper cannot prove that a requester sees only their own tickets; that guarantee must be checked where records are queried.''',
'''# Map roles to exact strings

PERMISSIONS defines OWNER, ADMIN, AGENT and REQUESTER arrays. hasPermission reads the selected array or falls back to an empty array for an unknown role. It first checks for the wildcard string, then checks exact membership of the requested permission.

OWNER has wildcard access. ADMIN includes ticket deletion and user management. AGENT can update and assign tickets but lacks ticket deletion. REQUESTER can create tickets, read own tickets and create comments. The module imports Prisma's Role type; the lab supplies enum values while executing the actual function. No repository, session or route runs. Follow callers separately before interpreting ticket:read:own as an enforced database ownership condition.''',
'''# Capability differs from row scope

The helper answers whether a role has a named capability. It receives neither a ticket nor a user id, so it cannot decide which ticket belongs to a requester. ticket:read:own is a vocabulary entry whose enforcement depends on downstream code that adds a requester predicate.

Exact string matching also matters. Ticket:read differs from ticket:read, and an unknown name is denied for ADMIN. OWNER bypasses that distinction because wildcard is checked first. That is existing behavior, not validation of permission names. During review, separate role authorization, permission spelling and record filtering. Testing one dimension does not prove the others, even when all appear in the same route.''',
'''# Work through requester and agent decisions

Call hasPermission('REQUESTER','ticket:read:own'): the array contains that exact value, so the result is true. Change only the permission to ticket:read and the result becomes false. Now use AGENT with ticket:update and ticket:delete; the results are true and false respectively.

The runtime test asserts these paired decisions directly against the existing source. This paired fixture prevents a misleading broad statement such as requesters can read tickets from hiding the distinction between own and all records. The teaching addition also checks unknown roles and permission spelling. It adds no new role or runtime authorization rule. Use the preserved source snapshot when comparing any future permission expansion.''',
'''# Debug the smallest policy boundary

Run node --experimental-vm-modules --test tests/permissions-errors.test.mjs. The test loads backend/src/shared/utils/permissions.ts and supplies only the Prisma enum import. Assertions examine boolean results from the real hasPermission implementation; there is no fake allow-all guard.

When a result surprises you, inspect the role array, wildcard branch and exact permission spelling in that order. For an unknown role, the fallback array should deny access. For OWNER, unknown names still return true because wildcard comes first. A passing helper test says nothing about session authenticity or whether a route invokes this helper. Those are distinct integration boundaries and should be named explicitly in a code review.''',
'''# Practice without the answer table

Predict OWNER, ADMIN, AGENT and REQUESTER results for ticket:delete, user:manage, comment:create and ticket:read:own. Do not infer missing entries from a role's name. Write the table before running additional assertions.

Next compare an unknown role with an unknown permission supplied to OWNER. Explain which branch determines each result. Finally sketch a ticket query for a requester that uses the authenticated user id to restrict rows. Identify what must happen before that query and what a cross-user regression fixture should contain. Keep the query sketch separate from this helper lab: it is a proposed integration exercise, not code already verified by the five executed cases.''',
'''# Answers and review prompts

OWNER permits every listed action through wildcard. ADMIN permits deletion and user management but has neither comment:create nor ticket:read:own in its array. AGENT permits comment creation but not deletion, user management or own-read. REQUESTER permits comment creation and own-read, but not deletion or user management.

Unknown roles use an empty array and deny. OWNER with an unknown permission still permits because wildcard is evaluated first. A requester query must derive the requester id from authenticated context and include it in the database predicate; user-supplied ownership fields are insufficient. Review whether callers use the intended broad or own-read permission, and whether missing actions reflect deliberate product policy before changing this matrix.''',
'''# Trace wildcard and fail-closed paths

For UNKNOWN plus ticket:read, the map lookup returns undefined, the fallback supplies an empty array, wildcard is absent and exact membership is false. For OWNER plus typo, the array contains wildcard, so the function returns true before it checks the unknown name.

Record those two traces beside the requester own-read pair. They demonstrate why unknown role handling and permission-name validation are different properties. As an extension, temporarily remove OWNER's wildcard in a local fixture and predict which assertion fails. Restore the source after the experiment. The delivered tests read actual source; they do not mutate production permission lists or simulate HTTP sessions. A route-level test is still needed to show this helper is used.''',
'''# What the five cases establish

The runtime cases cover owner wildcard success, requester administrative refusal, unknown-role denial, own-read versus broad-read and agent update versus delete, plus exact spelling and owner handling of unknown permission names. The [snapshot](snapshots/permissions.ts.original.txt) preserves the original policy; no production rule was changed.

Only Prisma enum values are adapted. The permission lookup itself executes from the existing TypeScript file. There is no database, session, HTTP route or resource ownership check in this run. The workshop deliberately teaches those limits so a role matrix is not mistaken for complete access control. Follow the practice query exercise with a real route/repository regression before claiming cross-user data isolation.'''
],
'bcde1b4da8c5':[
'''# Inventory product CRUD workshop

Use [ProductsService](../backend/src/modules/products/products.service.ts) to follow create, read, update and soft deactivation through a Prisma boundary. The [runtime lab](../tests/products-service.test.mjs) executes the existing service and its real AppError class with an explicit persistence adapter. Production behavior remains unchanged.

The course uses concrete SKU fixtures, exact payload checks, refusal prediction and failure injection. Compare create's duplicate-SKU precheck with update's missing-product precheck, then inspect deactivate, which writes isActive:false directly. These methods do not all share the same error path. A useful review explains what each one proves and where database constraints, input validation and authorization must still be investigated.''',
'''# Five methods, different boundaries

getAll delegates to product.findMany. getById queries by id and throws PRODUCT_NOT_FOUND with status404 if absent. create first queries by sku, throws PRODUCT_SKU_EXISTS400 for a match, then forwards data to product.create. update queries by id before forwarding data to product.update.

deactivate differs: it directly updates the given id with isActive:false and performs no preliminary read. Provider failures therefore propagate from that write. AppError comes from backend/src/shared/errors/AppError.ts and executes in the lab. The service accepts data:any and contains no role check; this lesson does not invent validation or authorization guarantees. The Prisma adapter records exact arguments to make the existing responsibilities visible.''',
'''# Preconditions and database constraints

A duplicate-SKU precheck provides a friendly refusal for a record already visible to the query. It cannot prevent two concurrent creates from both observing absence. Database uniqueness remains a separate requirement that this adapter lab does not execute.

Similarly, an id lookup before update does not guarantee the row remains present until the write. The late-failure test records that provider errors propagate rather than being relabeled as not-found. Soft deactivation changes a boolean while retaining the product row; it does not establish that every list query filters inactive records. getAll currently delegates without an isActive predicate. These distinctions turn basic CRUD reading into a review of contracts, race windows and lifecycle behavior.''',
'''# Create a scanner with a new SKU

Call ProductsService.create with {sku:'SKU-1',name:'Scanner'} while the lookup adapter returns null. Predict two calls: findUnique({where:{sku:'SKU-1'}}), then create({data:{sku:'SKU-1',name:'Scanner'}}). The fixture returns id p1 and the supplied fields, and the test checks the complete call payload.

Now return an existing product for the same SKU. The service throws the real AppError with PRODUCT_SKU_EXISTS and status400 before create is reached. This paired example teaches precondition ordering without replacing the service method under test. The delivered change is a runtime lesson and source snapshot, not a new inventory policy. A concurrent duplicate-create experiment would need the real database constraint.''',
'''# Debug calls rather than invented behavior

Run node --experimental-vm-modules --test tests/products-service.test.mjs from the project root. The loader replaces the service's relative Prisma import with an explicit adapter and loads the real AppError module. Inspect statusCode on that error, not a guessed status property.

For a duplicate failure, check that the final call is lookup and that no create follows. For a missing update, inspect the initial id lookup. For a late write failure, seed an existing product and make update reject, so the test actually reaches the persistence boundary. The soft-deactivation test expects one direct update. No adapter result proves Prisma constraints, HTTP response mapping, user authorization or committed persistence.''',
'''# Practice with separate predictions

First predict the calls and error for getById when the adapter returns null. Then write the expected update payload for product p3 with name Renamed, including its where predicate. Compare those operations with deactivate('p3') and explain whether a lookup occurs.

Next design a getAll fixture containing one inactive product. Predict whether the current service filters it. Finally propose a two-caller duplicate-SKU experiment: both reads should observe absence before either create completes. State which database outcome would demonstrate a uniqueness constraint and which service error behavior remains unspecified. Do not solve this exercise by making a fake adapter reject duplicates automatically; the question concerns actual persistence behavior.''',
'''# Answers and code-review criteria

Missing getById throws PRODUCT_NOT_FOUND404 after findUnique({where:{id}}). Updating p3 sends {where:{id:'p3'},data:{name:'Renamed'}} after a successful lookup. Deactivate sends {where:{id:'p3'},data:{isActive:false}} directly, with no service-side missing check. getAll forwards findMany results and applies no inactive filter.

A concurrent duplicate-SKU test should allow both prechecks to finish, then observe whether the database admits only one insert. The current service has no explicit translation of a uniqueness error from create. Review the schema and HTTP error mapping separately before deciding the expected client response. Also inspect validation upstream: data:any and payload forwarding do not prove a safe field allowlist in this service.''',
'''# Trace refusal and late failure

Trace an update of a missing id: findUnique returns null, the real AppError is thrown, and product.update is not called. Contrast an existing id whose update adapter throws database unavailable: the lookup succeeds, the write is attempted and the same failure reaches the caller.

These traces have different implications for retries. A precondition refusal has no attempted write in the service trace. A provider failure may need investigation before retrying because the lab cannot determine real commit state. For deactivation, only the write boundary exists. Record call arguments and failure timing in your notes rather than claiming every error means no persistence occurred. The lab does not emulate a database rollback mechanism.''',
'''# Runtime evidence and remaining limits

Five cases execute actual ProductsService code and AppError: exact successful creation, duplicate-SKU refusal, missing-update refusal and late provider failure, getById/update payloads, and direct soft deactivation. The [source snapshot](snapshots/products.service.ts.original.txt) preserves the unchanged implementation for comparison.

The injected Prisma adapter observes call order and data. It does not run database uniqueness, transactions, HTTP routes, validation schemas, authorization or concurrent writes. Auxiliary error-constructor tests remain available, but the reported five-case run targets the product service. The course now describes inventory behavior directly; it makes no claims about employee profiles, onboarding stages or permissions absent from this source. Reproduce the command from the debugging chapter to inspect the terminal evidence.'''
]}
for id,chapters in courses.items():
 assert len(chapters)==9
 for name,text in zip(names,chapters):(B/'stage'/id/'astraupskill'/name).write_text(text+'\n',encoding='utf-8')
