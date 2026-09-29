from pathlib import Path
B=Path(__file__).resolve().parent.parent
P=B/'stage/e0e5886e8464'
O=P/'astraupskill';O.mkdir(exist_ok=True)
chapters={
'README.md':'''# Weeknight: trustworthy boundaries in a small CRUD app

This course uses the recipe application that is actually in this repository. A user chooses ingredients, time and preferences; a server requests three recipes; the browser records history and favorites. That small flow contains several important engineering boundaries even though the application has no relational database or tenant model. We will not invent either one to make the diagram look more impressive.

Start with [the codebase map](01-CODEBASE-MAP.md), then read [the concepts](02-CONCEPTS.md). Predict the behavior of a JSON `null` request before opening [the worked change](03-WORKED-CHANGE.md). Run the focused checks described in [testing and debugging](04-TESTING-AND-DEBUGGING.md). Attempt [the practice tasks](05-PRACTICE.md) before opening [the solutions](06-SOLUTIONS-AND-REVIEW.md). Finally, complete [the trace lab](07-TRACE-LAB.md) and read [the verification limits](VERIFICATION.md).

The original API used TypeScript casts as if they validated runtime data. It also destructured a parsed request without establishing that the request was an object. A valid JSON document can still be the wrong shape. The delivered change introduces explicit parsing for requests, provider recipes, and saved records. Tests execute these production parsers and the generation orchestration directly; they do not ask a paid provider for deterministic output.

Three levels of learning are deliberately separated. At junior level, identify where data enters and explain a guard clause. At mid level, decide which layer owns validation, preserve existing valid records during recovery, and write boundary tests that assert side effects did not occur. At senior level, discuss the limits of retries, schema evolution, process-local rate limiting, observability and migration policy without claiming the current implementation solves all of them.

Use a notebook for predictions. For each exercise, record input, expected status, provider-call count, resulting browser state and the evidence that would change your conclusion. A successful answer is an executable explanation, not a list of fashionable architecture terms. Keep the existing README for installation and product context; this directory supplements it rather than replacing it.
''',
'01-CODEBASE-MAP.md':'''# Map the real request and persistence paths

Begin at [HomeClient](../app/HomeClient.tsx). Its state contains ingredients, a time limit and preferences. Submitting serializes those values to `/api/recipes`. The UI disables the visible submit control for too few ingredients, but that check cannot establish a server invariant: a caller can send HTTP directly, a saved client can be old, and browser state can be malformed.

The [route adapter](../app/api/recipes/route.ts) retains the existing process-local rate limiter and JSON decoding. It delegates domain-shaped input and provider results to [generation orchestration](../lib/generation.ts). The orchestration calls [validation](../lib/validation.ts), invokes the supplied provider function only after the request is accepted, and validates its output before returning a success body. The actual SDK adapter stays in the route; tests inject a deterministic function at this boundary.

```mermaid
flowchart LR
  Form[HomeClient form] --> Route[POST route / JSON decoding]
  Route --> Policy[generateRecipeResponse]
  Policy --> Input[parseGenerationInput]
  Policy --> Provider[provider adapter]
  Provider --> Output[parseRecipes]
  Output --> Browser[results and browser storage]
```

Follow the successful browser path separately. HomeClient builds a generation-result record, calls [saveToHistory](../lib/storage.ts), writes the current result to session storage, and navigates to the results page. History and favorites use different local-storage keys. They are local CRUD collections, not server-authoritative resources. Parsing saved records is still important because local storage persists across software versions and can contain values this version did not write.

The [type declarations](../lib/types.ts) describe trusted objects inside the program. They do not validate JSON. The new parsing functions turn unknown values into that trusted representation while dropping unrelated fields. Read each returned object literal and identify which fields are normalized, constrained or defaulted.

For a code-reading exercise, draw two columns labeled transport and policy. Place request JSON decoding, HTTP status creation, provider retry count, ingredient bounds and storage recovery in one column each. Explain any choice that could reasonably belong in both. Then locate the [tests](../tests/boundaries.test.mjs) that prove invalid requests do not cross the provider boundary. There is no database transaction to trace here; a later SQL exercise should explicitly add that new responsibility instead of pretending it already exists.
''',
'02-CONCEPTS.md':'''# Runtime contracts, side effects and recoverable local data

A TypeScript assertion says how the compiler should treat an expression. It does not inspect the expression at runtime. In the original route, `body as { ingredients: unknown; ... }` did not prevent `body` from being `null`. Likewise, asserting provider JSON as `Recipe[]` did not prove ingredient amounts were finite numbers or that step order was meaningful. The revised [parser](../lib/validation.ts) accepts `unknown` and establishes these properties before returning typed values.

Distinguish three contracts. The request contract follows the existing controls: two to twenty distinct ingredient strings, one of four time limits, one to six whole servings, supported dietary options, a skill choice and a real boolean. The recipe contract checks nested objects, positive amounts, finite numeric values, bounded text and consecutive step order. The collection contract checks exactly three distinct recipe IDs and compares time, servings and missing-ingredient declarations with the accepted request.

Those checks establish structural and some cross-field consistency. They do not establish nutritional suitability, culinary quality, factual ingredient provenance or whether the recipe truly satisfies a dietary preference. Do not turn a successful parser result into a stronger product claim than its code supports.

The side-effect boundary is equally important. A malformed request should result in zero provider calls. That is both a correctness property and a useful cost-control property. The [orchestrator](../lib/generation.ts) places parsing before its retry loop, so retrying cannot turn invalid input into a paid request. Two failed provider attempts return a generic error; private provider details are not copied into the response.

Local-storage recovery uses a different policy. Reading a collection with one malformed entry should not hide unrelated valid entries. [Storage parsing](../lib/storage.ts) validates entries individually and returns only accepted records, without rewriting the stored string during a read. This avoids destructive cleanup as an accidental side effect of rendering. Explicit writes retain the existing history cap and favorite-toggle semantics.

Compare fail-fast and recover-partially behavior. A provider response is one new generated collection and must satisfy the complete contract. Existing history is a collection of independent records, so partial recovery is useful. The policy difference comes from ownership and user expectations, not from an arbitrary preference for throwing errors or catching exceptions.
''',
'03-WORKED-CHANGE.md':'''# Worked change: validate before invoking the provider

Read the exact [original route](snapshots/app__api__recipes__route.ts.original.txt) before reading the revised [route](../app/api/recipes/route.ts). The original code caught invalid JSON syntax, then destructured the decoded value. That leaves a gap: `null` is valid JSON but is not a destructurable request object. The same file's old recipe validator checked a few truthy fields and two arrays, then returned a type assertion.

The revised design separates decoding from policy. The route still owns `request.json()` and `NextResponse`. A new [orchestrator](../lib/generation.ts) owns the order of operations. It first calls `parseGenerationInput`. Any failure returns status 400 without invoking the injected provider. Only a valid normalized input reaches the bounded two-attempt loop. Each result must pass `parseRecipes` before status 200 is possible.

Consider this trace. A request contains two valid ingredients but `servings: "2"`. The UI usually produces a number, yet an external caller can produce the string. Parsing rejects it instead of coercing it. The response describes invalid input, the provider-call counter remains zero, and the retry loop is never entered. That is a clearer contract than silently correcting arbitrary input and hoping later code agrees.

Now consider valid input followed by an invalid provider result. The first attempt returns three objects, one with a negative ingredient amount. Collection parsing rejects the result. A second valid result can succeed; a second failure produces a generic error without unchecked recipes. This preserves the original maximum of two application-level attempts while making the success condition explicit. SDK-internal retry behavior remains a separate concern.

The storage change follows the same trust-boundary principle but uses partial recovery. Compare the [original storage module](snapshots/lib__storage.ts.original.txt) with [the revised module](../lib/storage.ts). A syntactically valid object stored under the history key no longer escapes as an array. Individual bad entries are skipped while valid entries remain available. Reads do not mutate persistence, and invalid writes leave existing data untouched.

For review practice, explain why moving every check into HomeClient would not fix the route, and why adding a compiler interface alone would not fix saved JSON. Then identify the smallest regression that distinguishes the original behavior from the revised boundary. Avoid refactoring unrelated components while investigating that regression.
''',
'04-TESTING-AND-DEBUGGING.md':'''# Test the boundary and debug from observable effects

Run `npm test` from this project with Node 22.16 or the recorded compatible environment. The script uses Node's built-in test runner with TypeScript stripping. The [test file](../tests/boundaries.test.mjs) imports actual production modules, so changing the parser or orchestration changes the tested behavior. No browser, provider account or database is required for these focused checks. Native stripping executes syntax; it does not replace a separate TypeScript type check.

The invalid-request table tests null and array bodies, non-string and duplicate ingredients, unsupported times, fractional or out-of-range servings, invalid dietary choices and wrong boolean or skill types. Every such case asserts status 400 and a provider-call count of zero. The second assertion matters: an implementation that returns the correct error after making a paid request would still violate the intended boundary.

Provider tests use functions that return known values or throw. They check nested recipe shapes, repeated IDs, requested servings and time, missing-ingredient declarations, successful recovery on the second attempt, and a generic failure after two errors. These tests cannot prove network behavior or a real model's output quality. They establish how this application responds to provider outcomes.

Storage tests install a small in-memory localStorage fake and restore the original property after each synchronous scenario. They exercise invalid JSON, valid JSON of the wrong type, mixed valid and invalid entries, fifty-entry history retention, favorite toggling, denied storage and invalid writes. A key debugging observation is that reading a mixed collection must not rewrite the original storage string.

Try a fault-injection lab. Change the input parser to accept string servings, run the suite, and observe which assertion fails. Restore the code, then make the orchestrator return provider data without parsing. Find the test that distinguishes unchecked success from controlled failure. Finally, remove the array guard in storage and store `{}`. Trace the exception to its first consumer rather than adding catches to every component.

The [verification record](VERIFICATION.md) distinguishes executed evidence from limits. Type checking covers module integration and types when dependencies are available. Neither a passing focused suite nor type checking establishes browser rendering, accessibility, actual API credentials or deployment behavior. Preserve those distinctions in a pull-request description.
''',
'05-PRACTICE.md':'''# Practice before opening the solutions

Work in a separate branch or copy. Read the [map](01-CODEBASE-MAP.md), then close the worked-change chapter. Keep your answers beside test output so you can distinguish a prediction from something you learned after running the program. The tasks below increase in scope; finishing the first task carefully is more useful than sketching every advanced extension.

## Junior: classify incoming values

Create a table for `null`, an array, a request with a numeric ingredient, a request with string servings, and a valid request containing surrounding ingredient whitespace. Predict the parser result and provider-call count for each. Add one genuinely new boundary case, such as a duplicate dietary option, to the existing test table. Explain why a TypeScript interface would not make that test unnecessary.

## Mid: preserve useful history

Construct a stored history array with two valid results, one result with an invalid timestamp, and one plain string. Predict the returned records and whether localStorage changes during the read. Then design a recovery notice that can report ignored entries without overwriting them. Decide whether the notice belongs in parsing, a storage result type, or the UI. Preserve the current public interface until you can explain the migration cost.

## Mid: make errors useful without leaking internals

The generation response intentionally hides provider exception details. Design an internal structured event containing an attempt number, error category and a correlation identifier. Keep ingredient text, credentials and raw provider messages out of the proposed event. Write tests for the event shape and prove the browser still receives only the generic error. Do not send telemetry to an external service for this exercise.

## Senior: design an asynchronous extension

Suppose generation becomes a background job stored in SQL. Define create, inspect, retry and cancel operations. Specify who owns each record, what prevents duplicate jobs, how status transitions are validated and what happens when a worker finishes after cancellation. Draw a state table before choosing a queue library. Propose one invariant that requires a real database integration test rather than an in-memory fake.

## Review deliverable

Write a short change description containing the concrete trigger, previous behavior, new behavior, executed tests and limits. Include one rejected alternative and its tradeoff. Open [the solutions and rubric](06-SOLUTIONS-AND-REVIEW.md) only after your first attempt. An acceptable answer acknowledges uncertainty instead of treating a mock as evidence of distributed correctness.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Worked answers and a review rubric

For the classification exercise, null and array requests fail the object guard. Numeric ingredients fail text validation. String servings fail the numeric guard rather than being coerced. All four should produce status 400 with zero provider calls. A valid request with surrounding ingredient whitespace succeeds and passes trimmed strings to the provider. The existing [test helpers](../tests/boundaries.test.mjs) make it easy to add the duplicate-dietary case by changing only `preferences.dietary`; assert both response status and absence of the side effect.

For mixed history, only the two valid records should be returned. The invalid timestamp and string entry are rejected independently. The stored string should remain byte-for-byte unchanged during the read. A recovery notice could use a new storage result type containing accepted records and a rejected-entry count, but changing every consumer immediately is unnecessary for the present fix. Discuss a compatible wrapper or a separate diagnostic function before widening the public interface.

For internal error events, a useful shape contains a generated correlation identifier, attempt number and a bounded category such as parse_failure or transport_failure. Do not put the original exception message directly into the public response. A test should inject a distinctive private message and assert that it is absent from the response. The delivered suite already demonstrates that assertion for the generic provider failure. Adding observability would be a separate reviewed change, not an undocumented claim about current behavior.

For the asynchronous extension, candidate states include queued, running, succeeded, failed and cancelled. A cancellation request should not merely set a UI flag while a late worker can overwrite the stored state with success. One possible invariant is a version-qualified update: completion succeeds only if the job is still running with the claim version held by that worker. A unique idempotency key can prevent duplicate creates, but its scope and expiration need explicit product decisions. Test transaction conflicts with the actual database before claiming race safety.

Use this rubric when reviewing another learner. A junior answer identifies the exact boundary and supplies a reproducible example. A mid-level answer keeps responsibility in one layer and tests prohibited side effects. A senior-level answer separates deterministic local guarantees from operational assumptions, identifies migration costs, and narrows claims to evidence. Reject solutions that silently discard all history, retry invalid input, duplicate parser logic in tests, or claim dietary correctness from shape validation alone.
''',
'07-TRACE-LAB.md':'''# Trace lab: request, retry and stored-record recovery

Use [generation.ts](../lib/generation.ts), [validation.ts](../lib/validation.ts), and [storage.ts](../lib/storage.ts) as the only implementation references during the first pass. Draw a row for every function boundary. Record the value's trust level, the next operation and whether that operation can change external state. This exercise teaches a habit useful in larger CRUD systems: explain a transition precisely before proposing a layer or pattern.

| Scenario | Input parser | Provider calls | Output parser | Observable result |
|---|---|---:|---|---|
| JSON null | Rejects object shape | 0 | Not reached | Controlled 400 |
| Valid input, valid recipes | Accepts normalized input | 1 | Accepts | 200 with parsed recipes |
| Valid input, bad recipes, then good recipes | Accepts | 2 | Rejects then accepts | 200 after bounded retry |
| Valid input, two failures | Accepts | 2 | Fails or is not reached | Generic 500 |
| Mixed saved history | Not a new API request | 0 | Per-record validation | Only valid records returned |

Now trace the null case from the HTTP adapter. JSON decoding succeeds, which is different from a syntax error. The adapter delegates the decoded value. The object guard throws; the orchestrator catches that validation error and constructs a response. The route converts that result into an HTTP response. Locate the point where the original code instead destructured null using the [original snapshot](snapshots/app__api__recipes__route.ts.original.txt).

For the retry case, write the attempt counter before and after each provider call. Explain why parsing must happen inside the attempt's try block for invalid provider output to participate in the retry policy, while request parsing belongs before the loop. Then ask what would happen if the SDK independently retried transport errors. The application's two attempts are not necessarily two physical network requests; the current suite does not establish that network count.

For storage, identify the difference between corrupt JSON and a corrupt record inside valid JSON. The first returns an empty collection through the outer catch. The second is rejected inside the per-item parser while other records remain visible. Neither read removes persisted bytes. Finish by translating this policy into a hypothetical SQL import: which failures should abort one record, one batch, or the entire transaction? There is no universal answer; state the user-visible atomicity requirement first.
''',
'VERIFICATION.md':'''# Verification evidence and practical limits

The focused regression command is `node --experimental-strip-types --test tests/boundaries.test.mjs`, also exposed as `npm test`. It runs production request parsing, provider-response parsing, generation orchestration and browser-storage functions through Node's built-in test runner. The recorded run for this delivery uses Node 22.16.0. The command does not contact Anthropic, send notifications, access a database or require an installed browser. Read [the regression source](../tests/boundaries.test.mjs) rather than relying on a passing count alone.

The accepted result and captured output are linked in the final evidence section below. The suite contains forty-six cases covering invalid input, zero provider calls for rejected requests, normalization, malformed nested recipes, repeated IDs, requested time and servings, bounded retry, generic failures, corrupt storage, partial collection recovery, capped history and favorite toggling. These are runtime assertions against the modules used by the application, not searches for strings in the implementation.

A separate TypeScript check examines the project integration when its dependencies are installed. The explicit `.ts` imports used by the dependency-free tests are enabled by `allowImportingTsExtensions` with the existing no-emit configuration. TypeScript stripping alone does not perform that check. Installation and type-check records must be reported separately from test counts; installing packages is not a passing application test.

Several important limits remain. The focused tests do not execute the Next HTTP adapter, verify deployed proxy headers, certify the process-local rate limiter, render browser components, or validate a real provider response. They do not prove recipe quality or dietary suitability. Session-storage write failure in the existing submit flow and UI notification for local-storage failures are not redesigned in this bounded change. The provider SDK may also have its own retry policy independent of the application's two attempts.

Exact originals of the four changed baseline files are retained under [snapshots](snapshots). New production modules and tests are listed in the delivery manifest. Future maintainers should rerun the focused suite after changing validation bounds, public storage behavior or retry semantics, then add an integration check appropriate to any newly changed boundary. Do not silently upgrade the meaning of this evidence into a whole-application readiness claim.
'''
}
for name,body in chapters.items():
    (O/name).write_text(body,encoding='utf-8')
    print(name,len(body.split()))
