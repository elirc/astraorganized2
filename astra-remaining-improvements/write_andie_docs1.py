from pathlib import Path
s=Path('astra-remaining-improvements/stage/cf8875344b43')
def w(n,c):
 p=s/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(c.strip()+'\n',encoding='utf-8')
w('README.md',r'''
# Andie metaobject migration learning lab

A dependency-free Node 22 utility for learning API boundaries, deterministic migration planning, pagination, conflicts and partial-failure recovery. Start with [the course](astraupskill/README.md).

The legacy script embedded Shopify credentials and immediately wrote to configured stores. The replacement has no automatic network action: importing it or running it without arguments only exposes functions or help. The embedded credentials have been removed from active source. **Revoke and replace the original tokens through the account owner; removing source text does not revoke a credential or erase historical copies.** No original token was used for verification.

## Start entirely offline

```powershell
npm test
npm run check
npm run plan:example
Get-Content plan.example.json
```

No npm install is needed: the project uses Node built-ins. The example plan contains two proposed creates, one definition and one entry. Output files must be new; choose a different `--out` path if an earlier plan already exists. Fixtures are synthetic and contain no credentials.

## Optional account workflow

`node scripts/populate-metaobjects.js help` explains all flags. `export --role source|target --out new-file.json` performs read-only requests using the matching `SHOPIFY_SOURCE_STORE`/`TOKEN` or `SHOPIFY_TARGET_STORE`/`TOKEN` environment variables. Store values are bare myshopify subdomains. `.env.example` is a template; the program does not load it automatically. Use newly provisioned credentials and a development target for any later account testing.

`plan --source source.json --target target.json --out plan.json` remains offline. Review its operations and conflicts. `apply --plan plan.json --confirm-target exact-target-name --journal new-journal.json` is an explicit remote-write command: it re-exports both stores, rebuilds the plan and rejects stale or changed plans before creating anything. Conflicts stop all creates. Successful creates are journaled sequentially. A partial failure can leave earlier resources on the target; re-export and reconcile instead of blindly retrying.

This implementation creates missing supported definitions and entries. It does not update or delete existing content. References, app-owned types, unsupported ownership and enabled online-store/renderable capabilities require a separate migration. The exporter covers the selected metaobject fields, not a full Shopify store backup. Archived theme assets and Storybook configs remain incomplete source remnants; no theme or Storybook build is claimed.

The query/input review targets API `2026-07`. Shopify's API versioning and input/output types need explicit compatibility review when upgrading. See [versioning](https://shopify.dev/docs/api/usage/versioning), [definition creation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/metaobjectDefinitionCreate), and [entry creation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/metaobjectCreate).

Verification passed 42 local tests and three syntax checks. It used controlled API responses and one real loopback HTTP server; it did not contact a live Shopify account. Read [the exact evidence and limits](astraupskill/VERIFICATION.md).
''')
w('astraupskill/README.md',r'''
# Build judgment around external CRUD integrations

This course turns a small migration script into a study of reliable integration work. The main skill is deciding what can safely be concluded from a request, a response or a snapshot. A junior engineer may focus on making a POST succeed; a mid-level engineer also considers incomplete exports, conflicting records, uncertain outcomes and recovery after the third operation fails.

Begin with [the root setup](../README.md). Node 22 is sufficient; there are no third-party runtime dependencies. Run `npm test`, `npm run check` and `npm run plan:example`. These commands use synthetic fixtures and local test boundaries. You do not need a Shopify account or token to complete the core course. The example plan proposes a definition followed by its entry and reports any conflicts separately.

Read [the code map](01-CODEBASE-MAP.md), then [concepts](02-CONCEPTS.md). Follow [the worked change](03-WORKED-CHANGE.md) while inspecting the planner and API client. Use [testing and debugging](04-TESTING-AND-DEBUGGING.md) to understand what the 42 cases establish. Attempt [practice](05-PRACTICE.md) before consulting [solutions and review](06-SOLUTIONS-AND-REVIEW.md). Finish with [the trace lab](07-TRACE-LAB.md) and [verification](VERIFICATION.md).

## A first experiment

Copy the source fixture and change its title value. Build a plan against an empty target fixture: the new value appears in the proposed create. Now make the target contain the same handle with a different value. The plan reports a conflict and does not propose overwriting it. Explain why an existing identity is not proof that the target already contains the intended content.

Next add a reference field to a copied fixture, updating both its definition and entry type consistently. The planner refuses to treat the source store's resource ID as portable. It reports a migration conflict instead of silently omitting the field. This makes an unsupported case visible before any write begins.

The original script contained embedded credentials. Active source now reads credentials only from process environment, and account operations require explicit commands. The old tokens still need revocation by the account owner; this course does not use or reproduce them. Error output avoids dumping request headers or remote bodies. These are responses to an observed source problem, not a claim that the repository's entire history has been sanitized.

The delivered tool supports read, compare and create workflows. Update policy, deletion, cross-store reference mapping, a browser review UI and durable job orchestration remain exercises. Keep that distinction in your notes. A migration plan is reviewable intent; a journal is partial evidence of execution; neither is an atomic transaction across two stores.
''')
w('astraupskill/01-CODEBASE-MAP.md',r'''
# Three boundaries: command, plan and transport

Start at [populate-metaobjects.js](../scripts/populate-metaobjects.js). Its `require.main === module` guard separates importing functions from executing a command. With no arguments, the command displays help. `parse` validates the command's allowed flags, rejects duplicates and requires complete options. The offline plan command reads two JSON snapshots and writes a new output file; it does not construct an authenticated client.

`clientFor` is used only by explicit account commands. It derives source or target configuration from process environment and creates a client. The CLI never contains a real token literal. `newOutput` uses exclusive creation so an existing plan, export or initial journal is not silently overwritten. `journalWriter` owns a newly created destination and replaces later journal snapshots through a temporary sibling file.

[client.js](../scripts/lib/client.js) contains fixed GraphQL documents and the HTTP boundary. Store validation prevents an arbitrary URL from receiving the token header. Query variables carry types and cursors, keeping opaque cursor text out of the document string. The client checks HTTP status, optional served-version headers, JSON parsing and GraphQL errors before accepting data. Mutation handling separately checks `userErrors` and a returned resource ID.

`pages` follows a connection until `hasNextPage` is false. It rejects a missing or repeated cursor and enforces a maximum page count. `exportSnapshot` pages definitions, then pages entries for each definition. It returns a selected metadata projection, not all store resources. The export is sequential and does not represent an atomic snapshot while other writers are active.

[planner.js](../scripts/lib/planner.js) is mostly pure data transformation. `normalizeSnapshot` validates identities, fields, values and supported structure, then sorts collections for deterministic comparison. `buildPlan` identifies missing resources, unchanged entries, conflicts and target-only entries. It never mutates the input fixtures. `applyPlan` performs fresh exports, rebuilds the plan, compares it with the reviewed artifact and rejects any conflict before the first mutation. It then executes creates in order and records receipts.

[The fixtures](../fixtures/source.json) provide a small definition with one title field and one draft entry. [The tests](../test/migration.test.js) cover pure plans, simulated API responses, filesystem behavior, child-process commands and a real local HTTP exchange. Read one case from each group and state which dependency it replaces.

The `shopify` assets and `.storybook` files are retained remnants of a larger theme workspace. They do not provide a complete runnable theme application here. The current package scripts intentionally describe the implemented migration utility. Do not infer a frontend build from the presence of fonts or a Storybook configuration filename.
''')
w('astraupskill/02-CONCEPTS.md',r'''
# Determinism, uncertainty and API contracts

A deterministic planner produces the same operations from equivalent snapshots. This implementation normalizes ordering before hashing and comparison. Definition types and entry handles form business identities; field keys identify values inside an entry. Duplicate identities are rejected because otherwise a later lookup might arbitrarily select one of two records. Stable output makes review and regression testing easier.

A hash detects changed normalized content; it is not authorization or a digital signature. Apply does not trust a caller who edits the operations while keeping an old hash. It re-exports source and target, rebuilds the entire plan and compares the resulting artifact. This prevents a changed plan from becoming a general arbitrary-mutation file. The check is still a preflight snapshot: another writer can change the remote store after export and before a create.

## Three kinds of success

An HTTP 200 means the transport received a response. The GraphQL envelope may still contain top-level errors. A mutation payload may also contain `userErrors` or lack a created resource ID. The client checks these layers before recording success. Shopify's create payloads expose business errors separately from their created resource. See [definition creation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/metaobjectDefinitionCreate) and [entry creation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/metaobjectCreate).

A timeout after sending a mutation creates uncertainty. The remote service may have committed even though the client did not receive its ID. Automatic retry could create a duplicate or encounter an existing handle. Therefore mutation transport failures stop execution and require a fresh export. Read retries are bounded and apply only to selected HTTP status codes or explicit GraphQL throttling. Retrying every error would hide validation problems and amplify outages.

## Output models are not input models

The old script copied fetched objects into mutation variables and deleted fields in place. That both changed the shared source object and assumed every returned field was accepted on create. The new planner constructs explicit inputs. For example, merchant-owned `PUBLIC_READ_WRITE` admin access is an output value absent from the create-input enum, so it is not echoed into the mutation. Non-public ownership is treated as a separate migration case. Compare the [output enum](https://shopify.dev/docs/api/admin-graphql/latest/enums/MetaobjectAdminAccess) with the [input enum](https://shopify.dev/docs/api/admin-graphql/latest/enums/MetaobjectAdminAccessInput).

Reference values add another boundary: a product ID belongs to its source store. Copying it into another store does not establish a valid relationship. The current planner blocks those definitions rather than dropping reference fields. Similarly, target-only entries are reported and retained because absence from a source export is not enough evidence to delete them.

The journal records confirmed creates, but it cannot roll back earlier remote operations. Treat it as a recovery aid. A failed journal write after a successful create leaves a real resource that may be missing from the disk receipt, so reconciliation must still inspect the remote target.
''')
print('Andie setup and first three course files written')
