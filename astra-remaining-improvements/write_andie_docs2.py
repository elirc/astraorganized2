from pathlib import Path
s=Path('astra-remaining-improvements/stage/cf8875344b43')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('astraupskill/03-WORKED-CHANGE.md',r'''
# Worked change: replace automatic copying with reviewed intent

The old script immediately iterated configured target stores, created missing definitions and copied missing entries. It fetched only the first definition page, interpolated cursors into GraphQL strings, mutated shared source fields while preparing inputs and logged some mutation requests as successful without checking their business errors. The delivered workflow separates observation, decision and execution.

Open [planner.js](../scripts/lib/planner.js). A source snapshot and target snapshot enter `normalizeSnapshot`. The function checks format and API version, store identity, unique definition types, unique entry handles, unique field keys, required values and agreement between entry field types and their declarations. It constructs new objects, so planning for a second target cannot inherit deletions made while preparing the first target's variables.

`buildPlan` compares normalized definitions by type. A missing supported definition produces a createDefinition operation before its entries. An existing definition with changed structure produces a conflict. For entries, matching type and handle plus equal content becomes unchanged; equal identity with different content becomes a conflict; absence becomes createEntry. Target-only content is listed for review and is never converted into a delete operation.

Consider this small entry input:

```json
{
  "type": "size_guide",
  "handle": "general",
  "fields": [{"key": "title", "value": "Find your fit"}],
  "capabilities": {"publishable": {"status": "DRAFT"}}
}
```

The fetched field's type metadata is used for validation but omitted from this explicit mutation input. Required reference fields are not merely omitted: the whole affected definition is a conflict because cross-store ID mapping has not been implemented. The plan remains useful even when it cannot execute, since it identifies the missing engineering decision.

Apply requires an exact target confirmation and matching source/target clients. It exports both stores again, rebuilds the plan and compares the full artifact. A changed source, changed target or edited operation stops before mutation. Any remaining conflict also stops all creates, including otherwise valid missing resources. This prevents a mixed plan from being partly applied while hiding unresolved differences.

Execution is sequential. A definition must exist before its entry can be created. Each accepted response contributes a resource ID to the journal. If the next mutation or journal write fails, later operations stop. Earlier creates may remain remote, so the next step is a fresh export and reviewed plan, not replaying the old file.

Read the tests for forged plans, changed snapshots, partial failure and journal failure. Explain which would fail if apply only compared stored hashes, or if the loop swallowed an exception and continued. Then describe the remaining race: remote state can change after the preflight export because the utility has no transaction spanning both stores.
''')
w('astraupskill/04-TESTING-AND-DEBUGGING.md',r'''
# Test boundaries without touching a store

Run `npm test` and `npm run check` from this project root. The 42 Node tests use synthetic snapshots, controlled fetch responses, temporary output files, child processes and one real loopback HTTP server. No Shopify account credentials are required. The local transport case redirects the injected fetch boundary to its own server and uses a fixture-only token; it does not send an account token to a test service.

The pure planner cases verify operation order, source immutability, unchanged content, schema conflicts, value conflicts, target-only content, duplicate identities, required values and unsupported references or ownership. Input/output access mapping and enabled unsupported capabilities have explicit regressions. These tests check the planned behavior before introducing transport timing.

Pagination cases supply two pages and inspect the variables on the second request. The opaque cursor contains characters that would be unsafe to splice into a query string. Other cases repeat a cursor or omit connection metadata and require failure instead of accepting an incomplete snapshot. A finite page cap prevents an accidental endless loop, but exceeding it is an error, not permission to proceed with partial results.

HTTP cases cover bounded retry on selected transient read responses, GraphQL throttling, malformed JSON, version fallback and top-level errors. Mutation cases prove that HTTP or transport failure is not automatically retried, even when the document is passed without an explicit mutation option. User errors and missing IDs cannot become successful receipts. Error assertions also check that credential-like fixture text from a thrown transport error is not copied into the reported message.

Apply cases check exact target confirmation, stale source and target exports, forged operations, global conflict handling, partial remote failure and journal failure before or after a create. The assertions count actual calls through the controlled client. A test that merely checks a final error string would miss the more serious bug of sending writes before rejecting the plan.

For a real operational failure in a future authorized development-store trial, first preserve the plan and journal. Identify whether failure happened before mutation, during an uncertain transport outcome or after a confirmed create while saving its receipt. Re-export before deciding to retry. Do not add a catch-all retry around the whole apply command.

The suite verifies local orchestration and the selected protocol shapes. It does not establish live account scopes, actual Shopify throttling behavior, remote schema acceptance, store-wide consistency or power-loss durability of journals. Those boundaries are recorded in [verification](VERIFICATION.md), so passing tests cannot be confused with a completed live migration.
''')
w('astraupskill/05-PRACTICE.md',r'''
# Progressive integration and CRUD exercises

These features are future learning work. The delivered utility already provides offline planning, selected read exports and explicit creates. Build each extension with a user story, a rule for conflicts and a test for a late failure.

## 1. Improve the review artifact

Generate a Markdown summary beside the JSON plan with counts, definition names, entry handles and conflict reasons. Keep the JSON authoritative for machine comparison. Escape user-controlled text so a value containing pipes or Markdown syntax does not corrupt the table. Test an empty plan, a conflict-only plan and a long value. Avoid including credentials or dumping every rich-text field into an ordinary log.

## 2. Add deliberate update planning

Define which entry fields the source owns and which target fields must be preserved. An existing handle with a different value currently conflicts. Replace that rule only after specifying a reviewed update operation with expected prior content. Test that a target edit made after planning stops the update. Do not assume an API's update mutation offers compare-and-swap semantics; verify the supported contract and state any remaining race explicitly.

## 3. Design cross-store reference mapping

Create a mapping from source resource identity to verified target identity. Validate that every required reference resolves before the first create. Distinguish a missing mapping from an intentionally empty optional field. For references between metaobjects, consider dependency order and cycles. Add fixtures with a missing referenced object, two objects referring to each other and a stale mapping. A mapping file is data that needs validation, not an excuse to copy arbitrary IDs.

## 4. Build a local review web app

Wrap offline plan creation in a local HTTP service and a browser page. Upload synthetic snapshots, show validation errors and let the learner inspect creates, conflicts and retained target-only entries. Bound request size and reject malformed JSON. Keep account tokens on the server if you later add authenticated account integration; never put them in browser bundles or plan artifacts. Test the service boundary separately from the planner and add a browser case that retains the user's inputs after a validation error.

## 5. Add durable job state

Persist migration runs and operation receipts in a database. Model planned, running, stopped, uncertain and complete states. A worker restart must reconcile an operation whose remote outcome is unknown. Test a crash after remote success but before the local receipt commit. Explain why a database transaction cannot atomically include an unrelated external HTTP service. Consider an outbox for local scheduling, while keeping remote reconciliation as a separate responsibility.

## 6. Define deletion and rollback policy

Do not equate target-only content with garbage. Specify ownership, retention and a reviewed deletion set before adding destructive operations. A create rollback may be unsafe if another workflow has already referenced the new object. Build a dry-run policy evaluator and test target content owned by another process. Finish with an operational note explaining when automatic compensation is appropriate and when human review is required.
''')
w('astraupskill/06-SOLUTIONS-AND-REVIEW.md',r'''
# Solution sketches for a careful reviewer

Use these notes after attempting [practice](05-PRACTICE.md). Review the observable contract and failure sequence instead of prescribing a particular folder structure. A compact implementation can still be rigorous if its boundaries are explicit.

For a human-readable report, derive counts from the plan arrays rather than maintaining separate counters during export. Escape table delimiters, line breaks and markup in displayed values. Include the source and target identities and snapshot fingerprints so a reviewer can connect the report to its JSON artifact. Do not suggest that a fingerprint signs or authorizes the plan; it only identifies normalized content.

For updates, a good first design lists owned keys and expected prior values. Separate “missing” from an empty string or null. Preserve target-managed fields. Reject a stale preflight comparison and document whether the actual remote mutation has an atomic condition. If it does not, a second writer can still race after the comparison. The solution should state this limitation rather than naming a local hash an optimistic lock on a remote service.

For reference mapping, use stable source and target identifiers plus resource type. Verify target existence and compatibility before using a mapping. Plan dependent creates in an order that respects references. Cycles may require a two-phase create-then-link workflow, but that introduces a period of incomplete objects and requires recovery rules. A required reference must not vanish merely because its target has not been created yet. Tests should inspect the whole proposed operation set before allowing any execution.

For a review web app, keep plan construction pure and inject it into the service layer. Validate upload size and schema before expensive normalization. Return structured errors that the browser can display without losing the source and target selections. Use separate transport DTOs rather than exposing configuration objects containing credentials. A browser test should prove that a conflict is visible and that no apply request is sent merely by opening a plan.

For durable jobs, record an operation's intended identity before sending it and its confirmed remote ID afterward. A crash between those steps leaves uncertainty. On restart, inspect the remote resource by its business identity and compare content before deciding whether to accept, retry or stop. This is a reconciliation workflow, not exactly-once delivery. Test all three outcomes with controlled remote state.

For deletion, require evidence that the tool owns the target resource and that deletion will not break current consumers. A target-only report is insufficient. Review a separate deletion artifact and preserve a recovery record. Do not implement automatic rollback by deleting every resource created earlier in a failed run; another process may already be using one.

Ask an author to demonstrate a partial failure, show the last durable receipt and explain what the next run does. Check that errors do not print tokens, that source snapshots remain unchanged, and that unsupported capabilities are visible. Accurate recovery behavior is more valuable than a success message that hides uncertainty.
''')
w('astraupskill/07-TRACE-LAB.md',r'''
# Trace an offline plan and a simulated partial apply

Run `npm run plan:example` and inspect the resulting JSON. If the file already exists, select a new output path with the explicit plan command rather than overwriting the earlier review artifact. The source fixture has one `size_guide` definition and a draft entry with handle `general`; the target fixture is empty. Find the definition create followed by the entry create.

Trace `main` into `readJson`, `buildPlan` and `newOutput`. No client is constructed along this branch, and no token is required. In the test suite, the offline CLI is launched in a child process with fetch replaced by a function that throws. It still succeeds. This demonstrates the absence of a network dependency more directly than calling the command a dry run while allowing hidden reads.

Copy the fixtures into a temporary directory. Make the target definition and entry identical to the source except for its store identity. Build a new plan and observe zero operations and one unchanged entry. Change the target title, then build again: the entry becomes a conflict. The planner does not decide which business value should win. Write the update policy you would need before changing that behavior.

Add a reference field in both the source definition and entry. Keep its types consistent so structural validation passes. Planning now reports a reference-mapping conflict and proposes no creates for that definition. Explain the difference between a malformed snapshot and a valid snapshot describing an unsupported migration.

Read the apply tests without running an account command. Follow the fake client's read responses, the fresh plan comparison, the initial journal write and the first confirmed create. In the partial-failure case, the second create throws. The result retains the first receipt and execution stops. In the journal-failure case, a confirmed create can exist while its disk receipt is incomplete. Both situations require re-export and reconciliation.

Draw a small timeline with source export, target export, plan comparison, create request, remote commit, response and journal replacement. Mark the window where a network timeout makes the outcome unknown. Mark the separate window where another writer can change a target after preflight. These are different uncertainties and need different tests.

Finish with a one-page review note: proposed creates, conflicts, retained target-only content, source/target fingerprints, tested recovery paths and unverified live-account assumptions. Include the fact that active credentials were removed from the original script but must be revoked by the account owner. Do not copy token strings into the note. The objective is to explain a reliable workflow, not to perform a live store migration during the course.
''')
w('astraupskill/VERIFICATION.md',r'''
# What was actually verified

Final local verification passed 42 Node tests and three JavaScript syntax checks under Node 22.16.0. There are no third-party package dependencies. `npm test` reproduces the test suite and `npm run check` checks the three implementation files. The central improvement workspace records TAP output, result JSON and the finite delivery manifest.

Tests cover deterministic plans, immutable source inputs, missing and unchanged resources, existing-value and schema conflicts, duplicate identities, required values, reference fields, ownership boundaries, output-to-input admin access mapping and unsupported capabilities. Cursor cases verify variable binding, repeated-cursor rejection and a finite page bound. Selected read failures retry within limits; mutation failures do not retry automatically. GraphQL errors, mutation userErrors and missing IDs cannot be recorded as success.

Apply verification uses controlled source and target clients. It proves that mismatched confirmation, edited plans, changed source snapshots, changed target snapshots and unresolved conflicts cause zero mutations. Partial-failure cases preserve earlier confirmed receipts and stop later operations. Journal failures before the first create prevent writes; a journal failure after a confirmed create stops the next one and exposes the need for reconciliation.

Filesystem tests use temporary output paths and verify exclusive file creation and journal replacement. Child-process tests prove importing the script has no side effects and offline planning succeeds with network access deliberately replaced by a throwing function. One test uses a real loopback HTTP server to inspect the posted GraphQL variables and response envelope. No test contacted a Shopify account or used an original embedded credential.

The selected API documents were reviewed against Shopify's published `2026-07` reference during this pass. Definition and entry connections support the pagination used by the exporter; see [definitions](https://shopify.dev/docs/api/admin-graphql/latest/queries/metaobjectDefinitions) and [entries](https://shopify.dev/docs/api/admin-graphql/latest/queries/metaobjects). This documentation review and local simulation do not establish live scope permissions or acceptance of every store-specific definition. Future API upgrades require a fresh compatibility review.

The delivered source contains no embedded Shopify token literals. Removing those literals does not revoke the original credentials, remove repository history or sanitize backup copies. The account owner should revoke and replace them. Verification did not attempt account administration.

Remaining limits: no live migration, updates, deletes, cross-store reference mapping, app-owned migration, enabled online-store/renderable capability migration, complete store backup, browser UI or durable job database. Exports are selected projections and are not atomic while remote writers are active. Fresh preflight does not eliminate a race before mutation. Journals are recovery aids with no power-loss guarantee. Existing theme assets and Storybook configs do not constitute a verified frontend build. The project is substantially improved as an integration learning utility, with those boundaries stated explicitly.
''')
print('All nine Andie course files written')
