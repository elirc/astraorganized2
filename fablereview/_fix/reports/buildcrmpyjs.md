# _Organized Desktop/02 Build Projects/buildCRMPYJS — fix report (B13)

Fable, 2026-09-18.

## Done
- review#2 registerSchema rejects role with the message "role cannot be set during registration" (superRefine); the existing test asserts the message
- review#1 contacts module (schemas, service, controller, routes) mounted at /api/contacts: Zod validation, authMiddleware + contacts:write permission for writers (READ_ONLY reads only), pagination with validated bounds, soft delete, conditional updateMany, P2003 -> 400, output allowlist; 7 supertest tests in contacts.test.ts
- review#3 03 explains admin provisioning via prisma/seed.ts and the users:manage gap
- review#4 02 TOCTOU paragraph; review#6 02 glossary; review#5 04 harness walk-through (vi.hoisted, .js specifier, Once-queueing, supertest)
- review#1 08-CRUD-CONTACTS.md chapter (route table, six decisions, four exercises) linked from README

## Skipped
- the contacts module is verified against the mocked Prisma client only (like the delivered auth tests); no migration was run against PostgreSQL

## Verification
- backend: npx vitest run via junctioned stage node_modules: 2 files, 16 tests passed (9 auth incl. the message assertion + 7 contacts); npm run typecheck exit 0 after switching req.params.id to String(...) for Express 5 typings; npm run lint exit 0; junctions removed

## Course/code consistency check
- Chapter 08 route table matches contacts.routes.ts; 04 harness walk-through describes the vi.hoisted/vi.mock pattern both test files use; permissions.ts carries contacts:write for the three explicit writer roles and SYSTEM_ADMIN by spread.
