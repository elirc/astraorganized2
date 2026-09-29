from pathlib import Path
P = Path(__file__).resolve().parent.parent / 'stage/8c8b7f90a8d2'
chapters = {
'README.md': ('Organization API keys: validate, serialize and audit', '''
This project is a Next.js and Prisma teaching application for organization-scoped API key management. The course focuses on creating, updating, revoking and rotating credentials without allowing stale operations to overwrite a revoked key. It also explains why an organization-wide key limit needs a serialization point, and why a one-time secret response must differ from ordinary metadata reads.

The implementation already had useful tenant predicates, role checks, response projection and transactional audit writes. The completed work extends those boundaries. Services now parse runtime inputs directly. Lifecycle reads and permission checks run inside their transaction. Configuration and rotation use conditional writes, and rotation compares the previous secret hash so two stale requests cannot both claim the same predecessor. Creation locks the organization row before counting its active keys.

You should understand async TypeScript functions, object schemas, HTTP status codes and basic database transactions. A tenant here is an organization. A conditional write succeeds only while its where predicate still matches. A transaction groups a credential change with its audit and rotation history. A DTO is the public response shape, intentionally excluding stored hashes. These terms have concrete implementations in apiKeyService.ts and apiKeyRepository.ts.

Install the project dependencies, generate the Prisma client, then run the finite Vitest suite, TypeScript check and production build recorded in VERIFICATION. Prisma generation creates code from the schema; it does not create or migrate your application database. The unit tests use repository and transaction fixtures and require no live PostgreSQL server. Running the application itself requires a dedicated development database and the existing local authentication setup.

Read chapters one through four before changing a lifecycle command. Attempt the practice cases before reading their solutions. Use the trace lab to explain exactly which statement decides a competing rotation, then compare that reasoning with the repository predicate and the test assertions.
''', None),
'01-CODEBASE-MAP.md': ('Locate authority, writes and public responses', '''
The routes under src/app/api/orgs/[orgId]/api-keys resolve the actor through withAuth, read route parameters and parse request bodies. PATCH uses a discriminated action schema: revoke has a reason, while update contains configuration fields. The route removes the action discriminator before calling the strict configuration service. That keeps the service's direct input contract independent of the HTTP command envelope.

apiKeyService.ts coordinates the workflow. It obtains membership through organizationRepository and delegates authorization to permissions.ts. Lifecycle methods read the key with both organization ID and key ID using the transaction client supplied by Prisma. Missing records become NotFoundError; a forbidden role or foreign developer-owned key becomes AuthorizationError. Those guards precede secret generation and writes.

apiKeyRepository.ts owns Prisma query construction. updateConfiguration requires ACTIVE status. rotate additionally requires the previously read secretHash. revoke already required ACTIVE and retains that rule. Services interpret an affected-row count of zero as ConflictError, then skip audit and history. Successful rotation records the previous hash and prefix only after winning its conditional write, using the same transaction client.

The service constructs public responses explicitly. Ordinary detail responses contain metadata and recent rotation descriptions, never previousSecretHash. Create and rotate have a separate one-time secret object. The stored secretHash travels into persistence but must not appear in the response or audit metadata. Read the security helper to distinguish plaintext, prefix, preview and hash before adding another credential-related field.

The test modules separate service orchestration from adapter queries. service-boundaries.test.ts injects repositories actually consumed by the service; data-isolation.test.ts calls the real adapter against a query-spying client. Their combined evidence connects business decisions to the persisted predicates.
''', ('src/repositories/apiKeyRepository.ts', '  updateConfiguration(', '  revoke(')),
'02-CONCEPTS.md': ('Three different concurrency boundaries', '''
An ACTIVE read is only a snapshot. Another request can revoke the key before a later update executes. Moving the read into a transaction is useful, but a transaction alone does not make an unconditional update reject that stale decision. The ACTIVE requirement must reach updateMany's where clause. A zero count then means the service did not win permission to perform that lifecycle mutation.

Rotation needs a stronger predicate than ACTIVE. Two requests can read the same active key and its old hash. If both later update by ID and status only, each can overwrite the other's new secret and each can write history claiming the same predecessor. Comparing expectedSecretHash makes only one of those stale writes match. A later request that rereads the new hash can legitimately perform a subsequent rotation; that is a different history step.

The active-key limit is an aggregate rule across rows. Each creation locks the same Organization row before counting ACTIVE keys and creating another. The parameterized SELECT FOR UPDATE supplies an organization-scoped serialization point. Requests for different organizations can use different rows. This rule depends on creation paths honoring that same lock; it is not a database constraint that automatically governs arbitrary external inserts.

Finally, transaction atomicity groups credential data, history and audit. An audit exception propagates out of the callback so Prisma can roll back the unit of work. The tests verify callback grouping with a rollback-capable fixture and inspect the actual conditional query arguments. They do not claim to have executed PostgreSQL lock contention or rollback against a live server.

Runtime validation solves a separate problem. TypeScript declarations disappear, so every mutating service parses the supplied value. Strict schemas reject unknown fields and empty patches. Parsed strings are normalized before persistence, and omitted optional fields remain distinct from explicit null.
''', ('src/repositories/apiKeyRepository.ts', '  rotate(', None)),
'03-WORKED-CHANGE.md': ('Make rotation history describe the winning predecessor', '''
Start with rotateApiKey and its original snapshot. Previously, a key could be read as ACTIVE before the transaction and then updated after another request had revoked it. The staged draft introduced a useful conditional predicate but still needed complete service validation, transaction-local authority checks and meaningful tests. The delivered service parses the reason before entering the transaction, reads membership and key through tx, and checks the existing role and lifecycle rules.

Secret generation happens only after those guards. The repository receives the observed secretHash as expectedSecretHash and the newly generated hash as nextSecretHash. It uses updateMany with organization ID, key ID, ACTIVE status and expected hash. The service requires exactly one affected row. A lost comparison throws ConflictError before creating a rotation history row or audit.

After success, apiKeyRotation.create stores the actual observed prefix and hash, and the service rereads the key inside the same transaction. The audit records safe prefix metadata and the operator reason. The response exposes the new plaintext only through its explicit one-time secret object. Hashes never belong in a browser DTO, even if the implementation considers them non-reversible.

Creation now parses its own schema and acquires the organization row lock before counting. Update parses a dedicated configuration schema that rejects an empty object. PATCH strips the HTTP action property before passing configuration to that strict schema. Expiry handling preserves undefined for an omitted field and null for an explicit clearing operation, so a name-only patch cannot accidentally erase expiry.

Use the source excerpt to locate the exact point after which history becomes legal. Removing the count check should break the stale-write tests; removing expectedSecretHash should break the real repository argument assertion.
''', ('src/services/apiKeyService.ts', '      const rotated =', '      return { rotatedKey')),
'04-TESTING-AND-DEBUGGING.md': ('Keep test doubles attached to the real boundaries', '''
Vitest hoists module mock factories. The original lifecycle test referenced ordinary top-level mock variables from a hoisted factory, which could fail before the test reached the service. Its fixtures now use vi.hoisted. Each service-boundary test resets mock behavior and supplies the actual repository exports imported by apiKeyService. The transaction mock invokes the callback with a distinct tx object, making accidental use of the outer Prisma client observable.

Positive tests create, update, rotate and revoke authorized keys. Negative tests reject missing membership, another developer's key, already revoked keys, unknown fields and invalid reasons. Input failures must happen before transaction entry or secret generation. Conditional-write failures must create neither history nor audit. Detail-response tests inspect nested recent rotations to ensure a previous hash does not leak through a seemingly harmless relation.

The two-rotation fixture returns detached snapshots with the same old hash, then lets the conditional mock accept only its current persisted hash. Exactly one call may fulfill, and only one history and audit may appear. This proves service orchestration under a controlled competing snapshot; the separate adapter test proves the expected hash actually enters Prisma's where clause. It is not a timing benchmark or live database stress test.

The rollback fixture mutates its simulated hash and history count, then throws from audit creation. Its transaction wrapper restores the snapshot and rethrows. The assertion demonstrates that the service keeps those operations inside one callback and propagates failure. PostgreSQL integration would be needed to observe provider rollback directly.

Debug failures by locating the boundary first. A short reason should fail schema validation, not reach a status conflict. A forbidden actor should never generate material. A zero conditional count should map to conflict, while an unrelated database outage remains an unexpected error. Keep these outcomes distinct when adding a retry strategy.
''', ('tests/service-boundaries.test.ts', '  it("allows just one simulated', '  it("rejects already revoked')),
'05-PRACTICE.md': ('Exercise expiry, authorization and contention', '''
Exercise one: add a service test for a configuration update containing only a future expiresAt value. Assert that it becomes a Date in the repository input and that description, name and scopes remain omitted. Follow it with an explicit null expiry and confirm that the repository receives null. Then pass an invalid date and verify that no transaction begins. Explain why treating a missing value and null as interchangeable would erase data during partial updates.

Exercise two: use an AUDITOR membership to attempt creation, rotation and revocation. Verify the real permission helper rejects each operation before secret generation, mutation, history or audit. Add an authorized DEVELOPER control that rotates a key they created, and a denied case with a different createdById. Do not mock the permission helper itself; that would remove the boundary the exercise intends to test.

Exercise three: extend the creation lock contract assertion. Check that the lock is parameterized with the requested organization ID, happens before countActiveByOrganization, and that the count uses the same tx object as create and audit. Demonstrate why a lock after the count allows two requests to observe twenty-four keys and both decide to insert. Describe the separate live-database test you would use to verify two concurrent creations at that boundary.

Exercise four: add a route-level PATCH test that distinguishes the update envelope from configuration fields. A valid action update with only name should reach the strict service without the action property. An action revoke must use the reason branch and never call updateApiKey. An unexpected client actor ID should fail schema validation rather than silently override the established actor.

For each exercise, state one accepted result and one rejected result, plus the state that must remain unchanged on rejection. Keep fresh fixtures between tests and avoid relying on call history from a previous scenario. Record the actual finite test result before describing an exercise as complete.
''', None),
'06-SOLUTIONS-AND-REVIEW.md': ('Expected reasoning and useful assertions', '''
For the expiry exercise, the parsed nonempty string is converted to an ISO representation at validation and then to Date for persistence. A missing property remains undefined. Explicit null survives reparsing and instructs Prisma to clear the column. The name-only regression already demonstrates preservation of omitted expiry and description, while its second call demonstrates explicit clearing. Build the future-date case around that test rather than introducing a second independent implementation of patch semantics.

For the authorization exercise, AUDITOR has read permissions and cannot mutate credentials. DEVELOPER can create, update and rotate, but lifecycle checks restrict update and rotation to keys they created. Revocation remains an administrative permission. PLATFORM_ADMIN retains the existing bypass. The service obtains membership and key using the transaction client, then invokes the real permission functions before generating new material. A mock that always authorizes would make the exercise meaningless.

For the capacity exercise, all normal creators acquire the same organization row lock before counting. With twenty-four active keys, the first accepted request creates the twenty-fifth. A waiting creator counts after acquiring the lock and should reject at twenty-five. The current query-contract test establishes ordering and parameterization; a future PostgreSQL integration test should synchronize independent connections and verify the final count. Do not describe the mocked assertion as observing that database schedule.

For the route exercise, narrow input.action first. The revoke branch reads its validated reason and returns. Only the update branch destructures away action and forwards the remaining fields. The service schema should stay strict: loosening it to accept every transport-only key would hide a boundary mistake instead of correcting the caller.

A final review checks response ownership, tenant scoping and the winning write. Require positive controls, ensure secrets appear only in explicit one-time responses, and verify audit failure propagates through the transaction. Document mock limitations beside the evidence so another maintainer can decide which integration checks to add later.
''', None),
'07-TRACE-LAB.md': ('Two rotations and a concurrent revoke', '''
Start with active key K in organization O, prefix P and hash H. Two authorized requests A and B enter separate transactions and read the same key snapshot. Both pass the role and ownership guards. A generates new material with hash H1; B generates different material with hash H2. Neither plaintext has been returned to a caller yet.

A executes updateMany with K, O, ACTIVE and secretHash H. It matches one row and changes the stored prefix and hash. A writes history describing P and H, rereads K and writes its audit. Its transaction commits, and only then does the service return A's plaintext. The response cannot accidentally contain H because it is assembled from selected fields and a separate secret object.

B's stale predicate still requires H. Once A's accepted write is visible, that predicate no longer matches. B receives count zero and throws ConflictError. It writes no history and no audit and returns no new plaintext. If B later refreshes and intentionally retries, it may observe H1 and perform a subsequent valid rotation. That later operation must describe H1 as its predecessor.

Now replace A with a revocation. The row becomes REVOKED. B's rotation fails its ACTIVE predicate even if the old hash is unchanged. A configuration update using the same stale ACTIVE snapshot also fails its conditional status check. This is why transaction-local reads alone were insufficient: the write needs the lifecycle condition too.

Finally, make the audit fail after a successful conditional rotation. The exception escapes the transaction callback, so the intended database outcome is rollback of the key update and history. The unit fixture models that rollback to verify grouping. Explain where a real PostgreSQL test would observe lock waiting and transaction rollback, and distinguish those observations from the controlled service test already present.
''', None),
'VERIFICATION.md': ('Evidence scope and reproduction', '''
The recorded checks for this delivery use the project's full finite Vitest suite, a TypeScript check and the Next production build. Dependency installation and Prisma client generation are preparation steps, not substitutes for tests. Exact command arguments, terminal exit codes and logs are linked below when packaging completes. Failed attempts remain in the campaign history and do not count as passing validation.

The tests execute the actual service functions and repository adapters with injected module fixtures. They cover successful authorized lifecycle operations, malformed direct calls, transaction-local reads, tenant predicates, expected-hash comparison, active-count lock ordering, one-time response projection and simulated rollback on audit failure. Existing permission and validation tests remain in the suite alongside the added regressions.

There is no live PostgreSQL concurrency claim in this verification. The capacity test checks the parameterized FOR UPDATE query and its position before count and create. The competing-rotation test controls the observed snapshots and conditional result through mocks. The repository test then checks the real Prisma query shape. These layers provide useful evidence about the application contract but do not observe provider isolation, lock scheduling or transaction timeouts.

To reproduce, install dependencies using the delivered lockfile, generate the Prisma client from prisma/schema.prisma, and run the command table. Generation does not migrate or seed a database. Use a dedicated development database if you run the application itself, following the existing project setup documentation. This work does not rotate an external account's credentials or contact a key-management provider; all test material is synthetic.

The application's existing local authentication mechanism is retained. The organization lock protects cooperating create paths, not arbitrary external inserts. Concurrent list and detail reads are not presented as a global snapshot. Keep these limits explicit when extending the demo into an operational system. Before reviewing later changes, compare the preserved original snapshots, rerun relevant checks and update evidence to match the new source.
''', None),
}
nav = '\n## Course navigation\n\n' + ' / '.join(f'[{n.removesuffix(".md")}]({n})' for n in chapters) + '\n'
(P / 'astraupskill').mkdir(exist_ok=True)
for name, (title, body, excerpt) in chapters.items():
    text = '# ' + title + '\n\n' + body.strip() + '\n'
    if excerpt:
        filename, start, end = excerpt; source = (P / filename).read_text(encoding='utf-8-sig'); index = source.index(start)
        sample = source[index:source.index(end, index) if end else len(source)].rstrip()
        text += f'\n## Source excerpt\n\nFrom [{filename}](../{filename}).\n\n```ts\n{sample}\n```\n'
    text += nav
    assert len(text.split()) >= 250, (name, len(text.split()))
    (P / 'astraupskill' / name).write_text(text, encoding='utf-8')
    print(name, len(text.split()))
p = P / 'README.md'; text = p.read_text(encoding='utf-8') if p.exists() else '# API key management portal\n'
if 'astraupskill/README.md' not in text: text += '\n## API key lifecycle course\n\n[Start the source-based course](astraupskill/README.md) for strict service inputs, organization locking, conditional rotation, one-time secrets and verification evidence.\n'
p.write_text(text, encoding='utf-8')
