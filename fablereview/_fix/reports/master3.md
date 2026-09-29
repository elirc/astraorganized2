# _Organized Desktop/03 Master Projects/master3 — fix report (B14)

Fable, 2026-09-18.

## Done
- review#2 withSerializableRetry (3 attempts, P2034 only) wraps every Serializable $transaction in ticketService; three unit tests (retry-then-succeed, give up after three, no retry for P2002)
- review#4 02 and 03 split into ## sections, each opening with a "Predict before you read on" prompt
- review#3 VERIFICATION "Run it yourself": compose, migrate, seed, dev, two curl commands
- review#1 tests/integration/ticket-patch.int.test.ts written (skips unless TEST_DATABASE_URL is set): two tenants, one ticket, PUBLIC+INTERNAL comments, three viewer shapes leave audit/outbox counts unchanged, agent PATCH adds exactly one of each, cross-tenant id is 404

## Skipped
- (none)

## Verification
- npx vitest run via junctioned stage node_modules: 17 unit tests passed (14 delivered + 3 retry tests) with the integration file skipped; then with TEST_DATABASE_URL against a disposable PostgreSQL 18 database (prisma db push on master3_int at 127.0.0.1:55439) tests/integration/ticket-patch.int.test.ts: 2 passed (viewer shapes leave audit/outbox unchanged, agent PATCH adds one of each, cross-tenant 404); npm run typecheck exit 0; junction removed. Note: the first wrapper pass dropped addTicketComment by a script bug; the service was restored from the stage copy and re-wrapped, and the typecheck confirms the file is whole

## Course/code consistency check
- The retry wrapper is described in 02 and exercised by the unit tests; VERIFICATION run-it-yourself uses the compose port read from docker-compose.yml; 02/03 headings correspond to their paragraphs in order.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (actor / auth context, tenant scope, role gate, response policy, comment visibility, transition guard, audit row, outbox event, outbox drain, serializable transaction, serialization failure retry, SLA state). Verified every term against the source before citing it: the files `apps/api/src/middleware/auth.ts`, `apps/api/src/modules/tickets/ticketService.ts`, `packages/domain/src/index.ts`, `prisma/schema.prisma`, `apps/worker/src/worker.ts`, and the symbols and identifiers `authMiddleware`, `x-tenant-slug`, `where: { id, tenantId: auth.tenantId }`, `canEditTicket`, `canAssignTicket`, `visibleCommentWhere`, `ticketIncludeForRole`, `ticketService.ts`, `visibility CommentVisibility`, `model TicketComment`, `canTransitionTicket`, `assertTicketTransition`, `tx.auditLog.create`, `updateTicket`, `model AuditLog`, `tx.outboxEvent.create`, `ticket.updated`, `prisma.outboxEvent.findMany`, `Prisma.TransactionIsolationLevel.Serializable`, `withSerializableRetry`, `P2034`, `getSlaState`, `enrichTicket`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 04, 07. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **04** - tests/domain/ticket-rules.test.ts (canEditTicket case)
- **07** - apps/api/src/modules/tickets/ticketService.ts (updateTicket)

No source code was changed; only the chapter Markdown.
