# _Organized Desktop/03 Master Projects/master2 — fix report (B14)

Fable, 2026-09-18.

## Done
- review#2 02 paragraph and a route comment: webhook tenancy must not come from caller-supplied headers
- review#3 4 inline Exercise/Solution pairs in 01-04 now keep only the prompt with a link; review#5 06 has a "Solutions to the chapter exercises" section with one ### anchor per chapter ahead of the existing walkthrough sections
- review#4 VERIFICATION "Run the app": compose, push, seed, dev, a success webhook and its replay
- review#1 payments.integration.test.ts written (skips unless TEST_DATABASE_URL): audit trigger injection proves all-or-nothing; two identical concurrent events yield exactly one processed and one 409/duplicate with one event and one outbox row

## Skipped
- (none)

## Verification
- npm test --workspace @billing/api via junctioned stage node_modules: 2 files passed with the integration file skipped; then with TEST_DATABASE_URL against a disposable PostgreSQL 18 database (prisma db push on master2_int) payments.integration.test.ts: 2 passed (audit-trigger injection rolls back payment/invoice/event/outbox; two identical concurrent events -> one processed, one 409/duplicate, one event and one outbox row); npm run typecheck --workspace @billing/api exit 0; junctions removed (apps/api/node_modules is a pre-existing real directory, untouched)

## Course/code consistency check
- Chapter prompts link to the 06 anchors that exist (### Chapter 0N exercise); VERIFICATION run section uses the compose credentials and API_PORT default from config.ts.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (tenant context, permission guard, tenant scope, parse and normalize, event identity, payload hash, identity conflict, duplicate / replay, claim, late failure, audit and outbox intent, contention retry). Verified every term against the source before citing it: the files `apps/api/src/shared/auth.ts`, `apps/api/src/app.ts`, `apps/api/src/modules/payments.service.ts`, `apps/api/src/shared/`, and the symbols and identifiers `attachTenantContext`, `requirePaymentPermission`, `where: { id: body.paymentId, organizationId: tenant.organizationId }`, `payments.service.ts`, `webhookSchema`, `parseMockWebhook`, `providerEventId`, `tx.webhookEvent.findUnique`, `hashRequestPayload(body)`, `webhook.identity_conflict`, `existing.processedAt`, `tx.webhookEvent.update({ ... processedAt })`, `payment.failed.ignored`, `writeAuditLog`, `writeOutboxEvent`, `["P2002", "P2034"]`, `webhook.claim_conflict`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 04, 07. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **04** - apps/api/src/modules/payments.service.test.ts (beforeEach reset hook)
- **07** - apps/api/src/modules/payments.service.ts (webhook transaction early exits)

No source code was changed; only the chapter Markdown.
