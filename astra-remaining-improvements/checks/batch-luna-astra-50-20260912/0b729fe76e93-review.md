# Master3 independent Astra review

Decision: CHANGES REQUIRED — source design accepted; service regression coverage and bounded teaching corrections requested from Luna A.

## Source findings

Reviewed actual `ticketService.ts`, domain roles, route/shared contracts, tests and all nine course guides. `updateTicket` now rejects non-operational roles before its first Prisma lookup. Priority-only, tags-only and empty viewer PATCH input therefore cannot bypass a field-specific status/assignment gate. `getTicket` and successful updates use the shared role-aware include; viewer reads retain the PUBLIC predicate, while operational actors retain both comment visibilities. Existing tenant-filtered preflight queries and transaction writes remain in place.

The implemented scope is PATCH authority and consistent response include construction. `createTicket` has no operational-role gate in the current source/route; it is unchanged and must not be described as operational-only. Priority validation occurs in the route's Zod schema, not as runtime validation inside the service.

## Evidence inspected

All four before snapshots match their baseline SHA-256 values. `verify-02.json` and its raw log show a completed exit-0 typecheck, nine pure domain tests in one file, and TypeScript/Vite build. No PostgreSQL integration or service-call regression ran in that evidence. The new helper test would remain green if the service's authorization guard were removed, so it does not establish the chosen repair's wiring.

## Required bounded repairs

1. Add tests that invoke the actual service with a mocked db module. Viewer priority/tags/empty PATCH must reject with 403 before ticket lookup or transaction, and no write mocks should run. A permitted staff update must reach tenant-filtered lookup and expected update/audit/outbox interactions. Actual `getTicket` calls must select PUBLIC comments for viewers and unrestricted comments for staff, retaining tenant scope. Describe these as mock interaction tests, not HTTP or durable persistence proof.
2. Chapter 06 must give complete matched answers to the existing exercises: exact synthetic header/context values, full role-aware include implementation and use sites, and the five-row response/mutation/audit/outbox/comments matrix. Remove the unsupported operational-only create claim.
3. Correct chapter 03's priority-validation ownership and identify an operational actor in chapter 07's cross-tenant 404 trace; viewers hit 403 before querying. Update check counts/coverage only after actual service tests complete.

These requests were sent directly to Luna A. No additional source redesign or PostgreSQL setup is requested for this bounded repair.

## Final Astra review

The final service tests invoke the actual functions and assert three viewer PATCH shapes reject before lookup or transaction; permitted agent update reaches the tenant-scoped query and expected ticket, audit and outbox calls; viewer and agent reads select the appropriate comment predicate. Root inspected the completed verify-06 record and raw output: fourteen tests in two files, type checking and the production build all passed. The four snapshots were previously verified against the immutable baseline and remain unchanged.

Course corrections now distinguish route-owned Zod validation, unchanged create behavior, operational cross-tenant 404 versus viewer 403, and mocked interaction evidence versus HTTP/durable PostgreSQL proof. Chapter06 includes the complete role-aware include helper and its two use sites; VERIFICATION resolves the stale nine-test claim and links to actual final output. Synthetic exercise ids are explicitly distinguished from the mocked fixture. No executable changes followed final verification. Prepared delivery contains 21 files, nine guides, 3751 course words and 26 checked local course links. Accepted for canonical delivery.
