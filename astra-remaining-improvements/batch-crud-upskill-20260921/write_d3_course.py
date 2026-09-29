from pathlib import Path
p=Path(__file__).resolve().parent.parent/'stage/43d6b6358f56/astraupskill'
chapters={
'README.md':'''# API-key lifecycle as a CRUD invariant

This course studies [apiKeys.ts](../lib/services/apiKeys.ts), an organization-scoped API-key service. Its create method stores a hash and returns a raw credential once; list excludes revoked and soft-deleted rows; revoke marks a timestamp. The exported verifier had two inconsistencies: it ignored extra dot-separated segments and did not exclude soft-deleted keys.

The patch requires exactly two nonempty segments and adds the deleted-at filter alongside the existing prefix, hash, organization and revocation predicates. The original is preserved in [this snapshot](snapshots/apiKeys.ts.original.txt). A source search found no production caller of `verifyApiKey` in this checkout. Accordingly, this is a tested service improvement and learning exercise, not a claim that an exposed authentication endpoint was repaired. Existing HTTP create/list routes use session authorization.

Read the value map and worked diff, then predict the negative cases before consulting the solutions. Four focused runtime cases execute production service code with real Node SHA-256 and explicit database/Drizzle adapters. They cover malformed input, active success, inactive or mismatched rows, and persistence failures. The course distinguishes service decisions from SQL execution, HTTP authentication and concurrent revocation. Those boundaries matter when transferring this pattern into a production CRUD system.
''',
'01-CODEBASE-MAP.md':'''# Map credential shape to a usage write

Start with `verifyApiKey(organizationId, keyWithPrefix)` in [apiKeys.ts](../lib/services/apiKeys.ts). Splitting the input produces parts. Length must be two, and neither prefix nor token may be empty. Only then does `hashApiKey` hash the token with SHA-256. The database read combines five requirements: matching prefix, matching hash, matching organization, null revoked timestamp and null deleted timestamp.

A missing match returns null before any write. A matching row leads to an update of `lastUsedAt` by the found id, followed by returning that row. The timestamp update is bookkeeping after the read; it is not an atomic recheck of every lifecycle predicate.

Compare `listApiKeys`, which already filters both lifecycle timestamps. Check the [schema](../lib/db/schema.ts) for `deletedAt`, then [hardDelete.ts](../lib/jobs/hardDelete.ts) for delayed physical deletion. This explains why a retained row cannot be treated as an active credential merely because it still exists.

The [HTTP routes](../app/api/api-keys/route.ts) call create and list with session permissions. No production verifier caller was found. Draw the service's argument boundary rather than inventing a header-extraction path. The [test](../tests/api-key-verify-boundary.test.mjs) invokes that exported verifier directly and records read and write decisions.
''',
'02-CONCEPTS.md':'''# Existence, eligibility and input grammar

Soft deletion separates retention from eligibility. A row may remain available for cleanup or audit while being ineligible for normal reads. Here, listing already encodes that distinction. Verification must apply the same lifecycle rule or a key hidden from the active list can still be accepted by the verifier.

Revocation and deletion are distinct fields. Keeping both null checks avoids assuming that every deletion also sets the revocation timestamp. Organization matching is another independent condition: a valid hash in another organization must not satisfy the requested organization's lookup.

Input grammar comes first. JavaScript destructuring silently ignores unused array elements, so taking the first two results of `split('.')` accepts a trailing segment. Checking the total part count closes that gap. This patch does not validate a particular prefix length or restrict token characters; generation rules and acceptance grammar are related but not identical contracts.

Finally, hashing is not authorization and a guarded read is not a transaction. The service hashes the secret to look up a row, then separately writes usage. Another operation could revoke or delete the row between those steps. The tests demonstrate the sequential contract with explicit predicates; they do not establish SQL isolation or correctness of every future caller's permission checks.
''',
'03-WORKED-CHANGE.md':'''# Make two missing conditions explicit

Before the patch, the verifier used:

```ts
const [prefix, token] = keyWithPrefix.split(".");
```

The replacement preserves both values while rejecting surplus segments:

```ts
const parts = keyWithPrefix.split(".");
if (parts.length !== 2) return null;
const [prefix, token] = parts;
if (!prefix || !token) return null;
```

The lookup also gains `isNull(apiKeys.deletedAt)` in the existing conjunction. Prefix, hash, organization and revoked-at conditions remain. Compare the [snapshot](snapshots/apiKeys.ts.original.txt) with the [service](../lib/services/apiKeys.ts) rather than evaluating the parser change in isolation.

For `sk_test.test-token.extra`, execution now stops before hashing and database access. For `sk_test.test-token`, it hashes the token and evaluates all five conditions. A soft-deleted matching row yields no eligible result, so no usage write occurs. An active matching row keeps the existing return and timestamp behavior.

Neither create nor revoke is rewritten. Revoke was already organization-scoped. The patch also leaves read/write concurrency unchanged: it is a sequential eligibility correction, not a guarantee that revocation cannot race verification. The tests make those observable differences explicit without substituting a copied verifier implementation.
''',
'04-TESTING-AND-DEBUGGING.md':'''# Test the production decision, model the database boundary

The [runtime test](../tests/api-key-verify-boundary.test.mjs) loads actual TypeScript service bytes through a local VM loader. It supplies real Node crypto, so the production hash function computes SHA-256. Drizzle expression builders and database methods are explicit adapters. A small predicate evaluator filters fixture rows using the expressions produced by the service; it does not generate or execute SQL.

Four named cases cover a malformed-input matrix, active success, a matrix of deleted/revoked/foreign/hash-or-prefix-mismatched/missing rows, and read/write error propagation. Negative cases assert zero usage writes. Success checks the hash input result, organization predicate, both lifecycle filters, update id and timestamp. Failure checks preserve the original error identity.

Debug from the earliest differing observation. No query for a valid shape suggests a parser issue. A returned deleted row suggests a missing lifecycle predicate. A write for a null match suggests a misplaced guard. A swallowed write error could incorrectly report verification success.

Run `node --experimental-vm-modules --test tests/api-key-verify-boundary.test.mjs` from the project root. The accepted capture is `crud-b04-astra-runtime`. These checks do not mount Next, execute native Drizzle, contact PostgreSQL or simulate a concurrent revoke. Keep any later integration result separate so the evidence remains attributable.
''',
'05-PRACTICE.md':'''# Predict the read and write ledger

For each input, write three answers before running the suite: is the token hashed, is the database queried, and is usage updated? Use a valid active row in the requested organization as the starting fixture.

1. Add a third segment to the key. Then try an empty prefix and an empty token. Identify the first guard that stops each input.
2. Keep the key well-formed but set `deletedAt`. Repeat with only `revokedAt` set. Explain why physical retention does not imply eligibility.
3. Move the row to another organization while keeping its prefix and hash unchanged. Name the predicate responsible for rejection.
4. Make the lookup throw a sentinel error. Then make the usage update throw instead. Predict which calls are recorded and whether null is returned.
5. Draw a race where the read succeeds and a concurrent revoke occurs before usage update. State exactly which claim the focused suite cannot establish.

For a review exercise, compare the generated-key format with the accepted-key grammar. Propose a stricter format rule only after considering compatibility for existing callers. Grade your answers on exact call order, zero-write assertions and separation of tested behavior from design proposals. Do not invent HTTP status codes for a service with no wired verifier route in this checkout.
''',
'06-SOLUTIONS-AND-REVIEW.md':'''# Answers and acceptance criteria

Extra segments fail the part-count guard. Empty prefix or token fails the existing nonempty guard. None reaches the hash or database. A well-formed deleted or revoked key is hashed and queried, but its lifecycle predicate prevents a match and no usage update occurs. A foreign organization's row fails organization equality even if its hash is correct.

A lookup error propagates before usage update. A usage-write error propagates after a match and attempted update. Neither is converted into a null result or a successful verification. Null represents no eligible match or invalid input, whereas an exception preserves an operational failure for the caller to handle.

In the race exercise, read eligibility can become stale before the separate update. The current code and harness do not atomically bind acceptance to the latest revocation state. A conditional write or transaction design needs a clear acceptance contract and database-level evidence; merely adding the word transaction to a comment is insufficient.

Award two points each for parser boundaries, lifecycle distinction, organization scope, error identity and concurrency limits. During review, require the exact original snapshot, actual-source execution and negative write assertions. Reject a claim of exposed endpoint repair: the inspected routes use session-based create/list actions, and no production caller of the verifier was found. This does not invalidate the service correction, but it limits its operational claim.
''',
'07-TRACE-LAB.md':'''# Separate parse, eligibility and bookkeeping

Use the following worksheet with `sk_test.test-token` and a fixture row whose prefix, SHA-256 hash and organization match. Record the service's returned value and each database call rather than reasoning only from the final test status.

| Scenario | Parse | Read outcome | Usage write | Service outcome |
|---|---|---|---|---|
| Extra segment | Reject | No read | None | null |
| Empty token | Reject | No read | None | null |
| Active matching row | Accept | Row | One timestamp update | Same row |
| Soft-deleted row | Accept | No eligible row | None | null |
| Revoked or foreign row | Accept | No eligible row | None | null |
| Read failure | Accept | Throws | None | Original error |
| Usage failure | Accept | Row | Attempt throws | Original error |

Now annotate each read predicate with the invariant it enforces. Prefix and hash identify the credential, organization constrains its context, and lifecycle timestamps constrain eligibility. No single condition replaces the others.

Add an eighth row for concurrent revocation after the read. Leave its durable outcome unresolved because the harness does not run two database transactions. This deliberate gap is part of the lesson: a useful trace marks the boundary of its evidence rather than guessing a guarantee from sequential control flow.
''',
'VERIFICATION.md':'''# Accepted evidence and limits

The accepted command is `node --experimental-vm-modules --test tests/api-key-verify-boundary.test.mjs`, captured as `crud-b04-astra-runtime`. Four named runtime cases execute actual [apiKeys.ts](../lib/services/apiKeys.ts): malformed shapes, active verification, ineligible or mismatched rows, and persistence-error identity. The expanded suite replaces the earlier two-case agent check.

Node's real crypto implementation computes the hash. Drizzle predicates, schema columns and database operations are explicit adapters; a fixture evaluator interprets the emitted conditions. This proves how the service constructs and uses its read contract, but not the SQL generated by Drizzle or the behavior of a live PostgreSQL database. No Next server, HTTP middleware or concurrency check ran.

The exact original is stored in [the snapshot](snapshots/apiKeys.ts.original.txt). Source review confirmed the deleted field, the existing list filters and the scheduled physical cleanup. It also found no production caller of `verifyApiKey`; the changed verifier is exercised directly by the learning suite. Existing API-key create/list/revoke authorization is not reimplemented or certified here.

Future work could connect a deliberately authorized endpoint and test persisted lifecycle states and revocation races. Those are separate changes. The current report claims only the service correction, four accepted runtime cases and the source-based learning material. Captured evidence follows below.
'''}
for name,body in chapters.items():
 (p/name).write_text(body,encoding='utf-8');print(name,len(body.split()))
