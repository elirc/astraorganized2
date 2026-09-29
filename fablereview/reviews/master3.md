# master3 (support-ticket modular monolith) — Fable review

- **Path:** `_Organized Desktop/03 Master Projects/master3`  ·  **Wave:** 2  ·  **Stack:** TypeScript / Express / Prisma+PostgreSQL / Vitest / Vite+React  ·  **Batch:** B14
- **Astra's change (one line):** Moves the ticket-edit role check to the first line of `updateTicket` so a VIEWER PATCH (including `{}`, tags-only, priority-only) is rejected before any Prisma lookup, and makes the PATCH response reuse the same role-aware comment include as GET so a successful update can no longer leak INTERNAL comments; also pins both ticket transactions to Serializable isolation.
- **Course size:** 3,751 words across 9 files (`wc -w astraupskill/*.md`)  ·  **Tests claimed:** 14 (9 domain + 5 service)  ·  **Tests found on disk:** 14 — `tests/domain/ticket-rules.test.ts` (9) + new `tests/api/ticket-service.test.ts` (5)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 4 | 5 | 4 | 5 | 4 | 5 | 4.5 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The defect is a genuine two-part CRUD bug, not a cosmetic edit. Before: `updateTicket` only consulted roles when `status`/`assignedUserId` were present, and the update used the unfiltered `ticketInclude` (see `astraupskill/snapshots/ticketService-before.ts.txt`, hash matches the backup copy exactly). After: `canEditTicket` gate at `ticketService.ts:149` plus `ticketIncludeForRole(auth.role)` on both read and update paths.
- The fix is factored the right way: the role predicate lives in `packages/domain/src/index.ts` as a pure function, and `canAssignTicket` is preserved rather than widened, so the narrower assignment rule is not accidentally relaxed.
- The new `tests/api/ticket-service.test.ts` asserts the *ordering* property that matters — `expect(mocks.prisma.ticket.findFirst).not.toHaveBeenCalled()` and `$transaction` not called — for three viewer body shapes, and asserts the two distinct comment predicates (`{visibility:"PUBLIC"}` vs `{}`). That is behavior, not "calls happened".
- Verification honesty is unusually good. `VERIFICATION.md` states plainly that the tests mock Prisma and "do not prove committed PostgreSQL counts, HTTP middleware, or worker delivery", and even discloses that "earlier command attempts included launcher failures" — the delivery JSON `limits[]` says the same thing.

## Problems found (evidence required)
- **[D2]** The change adds `{ isolationLevel: Prisma.TransactionIsolationLevel.Serializable }` to both `$transaction` calls (`ticketService.ts:145` and `:216`) and the course teaches serializable semantics in `02-CONCEPTS.md` ("either all commit or all roll back"), but nothing tests it. The mocked `$transaction` only asserts `isolationLevel: expect.anything()` (`tests/api/ticket-service.test.ts:78-80`) — it would pass with `ReadUncommitted`. Serializable also introduces real retry obligations (P2034) that the code has no handler for and the course never mentions.
- **[D2/D5]** No test touches a database. `deliveries/0b729fe76e93.json` `checks.environment` is explicit: "PostgreSQL is not contacted by the bounded verification". So the headline claim of the whole course — "zero audit rows, zero outbox rows" — is only proven against a `vi.fn()`.
- **[D3/D7]** Every file is unbroken prose paragraphs with no subheadings, bullets, or "stop here and predict" markers except in `05-PRACTICE.md`. `02-CONCEPTS.md` is four dense paragraphs. A junior gets no visual scaffolding to resume mid-chapter.
- **[D5]** `VERIFICATION.md` gives `npm ci` + `npm run verify`, but never tells the learner how to actually *run* the app to reproduce the traced 403 by hand. `docker-compose.yml` and `prisma/` exist in the repo; no `docker compose up` / `prisma migrate dev` / seed / port is given anywhere in the 9 files.

## Spot-checks performed
- Course claim: "`visibleCommentWhere("VIEWER")` produces `{ visibility: "PUBLIC" }`" -> read `ticketService.ts:22-25` and `prisma/schema.prisma:32-34` (`enum CommentVisibility { PUBLIC INTERNAL }`) -> matches.
- Course claim (`04-TESTING`): "verification command is `npm run verify`, which runs TypeScript checking, Vitest, and the Vite production build" -> `package.json:18` `"verify": "npm run typecheck && npm run test && npm run build"` -> matches.
- Course claim (`VERIFICATION.md`): "fourteen Vitest tests in two files" -> `astraupskill/evidence/verify-06.log:19-20` "Test Files 2 passed (2) / Tests 14 passed (14)", delivery JSON `expectedTests: 14`, `exitCode: 0` -> matches, no inflation.
- Course claim (`03-WORKED-CHANGE`): the role gate "runs before `prisma.ticket.findFirst`" -> diff of backup vs current shows the `canEditTicket` block inserted at the top of `updateTicket`, ahead of the lookup -> matches.
- Delivery `before_sha256` for `astraupskill/snapshots/ticketService-before.ts.txt` (`4cf802a7…`) equals the `before_sha256` of the live file -> the "exact original snapshot" claim is real, not a paraphrase.

## Improvements needed (ordered, concrete, actionable)
1. Add a disposable-Postgres integration test (`tests/integration/ticket-patch.int.test.ts`) that seeds two tenants, one ticket, one PUBLIC and one INTERNAL comment, then asserts `auditLog.count()` and `outboxEvent.count()` are unchanged after each of the three viewer PATCH shapes and `+1` after the agent PATCH. This is the exact fixture `04-TESTING-AND-DEBUGGING.md` already describes but does not ship. (effort: M)
2. Either add a P2034 serialization-failure retry wrapper around the two `$transaction` calls in `apps/api/src/modules/tickets/ticketService.ts`, or drop the `Serializable` level back to default and remove the serializable language from `02-CONCEPTS.md` / `07-TRACE-LAB.md`. Right now the course teaches an isolation level the code cannot survive under contention. (effort: M)
3. Add a "Run it yourself" section to `VERIFICATION.md`: `docker compose up -d`, `npx prisma migrate dev`, the seed command, the API port, and two ready-to-paste `curl` commands (viewer PATCH -> 403, agent PATCH -> 200). Without it `05-PRACTICE.md` Exercise 1 is a thought experiment. (effort: S)
4. Break `02-CONCEPTS.md` and `03-WORKED-CHANGE.md` into `##` subheadings with an explicit "Predict before you read on:" prompt per section. (effort: S)

## One-paragraph summary for the index
A tight, honest course built around one real authorization bug in a multi-tenant support-ticket API: a VIEWER could PATCH a ticket as long as the body avoided `status`/`assignedUserId`, and a successful PATCH returned internal comments that GET was careful to hide. The course explains why a partial body is still one authorized operation, why the role check belongs at the top of the service rather than in the route, and why response shaping is part of the endpoint contract — all of which transfer directly to any Node/Prisma CRUD API. Everything it claims about the code checks out, and it is refreshingly blunt that its 14 tests mock Prisma and prove nothing about committed rows. Do it, but expect to add the Postgres fixture yourself, and be aware it never shows you how to boot the app.
