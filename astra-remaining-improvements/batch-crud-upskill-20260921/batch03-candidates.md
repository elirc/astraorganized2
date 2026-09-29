# Batch 03 read-only CRUD candidates

Prepared 2026-09-21 from the original project trees named in `campaign.json`. No project was staged or modified. I found no project-local `AGENTS.md` in the inspected roots. Protected families and completed Fable/Astra work were excluded.

## 2cdf30cead55 — masterrnative

Entry points: `src/context/AppDataContext.tsx` and `src/services/storageService.ts`; validation lives in `src/utils/validation.ts`, with existing unit coverage in `tests/*.test.ts`. Candidate: every `update*` callback maps an id and silently succeeds when the id is absent, leaving the UI and storage unchanged while the caller believes a CRUD update worked. Bound the fix with a shared replace-by-id result that returns a typed not-found failure before persistence, preserving add/delete behavior. Lightweight check: Jest/Vitest pure helper tests for existing id replacement, missing id rejection, and no storage write on rejection; no Expo runtime needed.

## 7649d96533a4 — MasterStore

Entry point is `storefront`; webhook CRUD side effects are in `storefront/src/lib/webhooks/handlers.ts`, with product query mapping in `storefront/src/lib/utils/product-query.ts`. Candidate: webhook idempotency is an in-memory `Set`, so a process restart or a second worker can resend an order email. A bounded improvement is to move the event claim to the project’s durable store or make the handler accept a repository with an atomic claim, while keeping “mark only after successful send.” Lightweight check: a Node test with an injected claim repository proving duplicate delivery, failed send retry, and two handler instances share the claim; document that the current source has no durable repository until inspected further.

## a880d6aae28f — jep vs code

The active rebuild entry points are `jeopardy-rebuild/frontend/src/pages/GameSetupPage.tsx`, `GameEditorPage.tsx`, and the API client/session actions. Candidate: `handleAddPlayer` uses `setPlayers([...players, newPlayer])`, so two fast successful adds can close over the same old array and lose one player in local CRUD state even though both server rows exist. Use a functional update and reconcile from the returned session when appropriate. Lightweight check: React component test with two deferred `sessionApi.addPlayer` resolutions, asserting both players remain; separately assert remove preserves unrelated players. Keep the backend as the source of truth.

## 612cdbaa5aa0 — jsdrill_sync_20260223_125137

Entry points: `src/lib/db/schema.ts`, `src/lib/sessionBuilder.ts`, and `src/lib/executor.ts`; existing data logic is Drizzle SQLite. Candidate: `userCards` is documented as “one per user×problem” but the schema has no composite unique constraint on `(userId, problemId)`. Concurrent review completion or repeated creation can produce duplicate cards and ambiguous due dates. Add the composite uniqueness boundary and make the completion write use an idempotent upsert/update path after inspecting its caller. Lightweight check: a SQLite migration/schema test inserting the same pair twice, then an executor regression showing one card and deterministic due state; run with the cached Node toolchain, no external API.

## efb20378d966 — jstrain1

The tenant CRUD entry points are `server/src/controllers/usersController.js` and `server/src/services/userService.js`; role CRUD is in `server/src/services/roleService.js`. Candidate: `roleIds` are validated by array length, but duplicate ids can pass tenant existence checks and then be sent to membership-role replacement, creating a misleading count or unique-row failure. Normalize with `Array.from(new Set(roleIds))` before validation and persistence, or reject duplicates explicitly according to the API contract. Lightweight check: Node service tests with repository/Prisma doubles for duplicate role ids, cross-tenant role ids, and an empty list, asserting no partial membership write.

## abcd8cc338ec — jstrain2

The workflow CRUD routes are `src/app/api/workflows/route.ts` and `src/app/api/workflows/[id]/route.ts`; schema and tenant auth are under `src/lib/db`. Candidate: PUT updates the workflow, deletes all old steps, and inserts new steps as separate database calls without a transaction. A failed step insert leaves the workflow changed and steps empty, violating the CRUD aggregate boundary. Wrap workflow update, step replacement, and version increment in one transaction using the project’s Drizzle transaction API. Lightweight check: route test with a transaction double that fails on step insert, asserting update and deletion roll back; also test success replaces exactly the submitted ordered steps and tenant mismatch returns the existing null/authorization behavior.

## 2906d0b177f3 — jstrain2.4

This project is a dashboard prototype with Prisma schema at `prisma/schema.prisma`, client state in `lib/store.js`, and app selectors under `components/app-selector.jsx`. Candidate: selection state accepts an arbitrary environment or deployment id after an app changes; downstream panels can display records from an old app or issue a query with a stale foreign key. Keep the existing reset-on-app-change rule but validate dependent selections against the current app’s loaded collections before committing them. Lightweight check: store tests for app→environment→deployment transitions, stale environment rejection/reset, and same-app selection preservation. This is a UI-state CRUD boundary; native Prisma coverage is not implied.

## 4bda479c4c50 — jstrain3

The strongest bounded CRUD surface is `deskpilot-clean/src/lib/store.ts` plus `src/lib/state-machine.ts`. Candidate: `updateTicketFields` writes `updatedAt` even when no mutable field changed, making a no-op PATCH appear as a real update while emitting no event. Preserve the no-op timestamp and return the unchanged ticket, or reject an empty patch at the API boundary. Lightweight check: source-linked Node tests with a temporary data file asserting no event and unchanged timestamp for an empty patch, one event for a real change, and tenant mismatch returns null. Keep merged-ticket and status-transition rules separate.

## c81c4e873d3b — rewritepy2js

The actual FastAPI app is nested at `fastapi-realworld-example-app`; CRUD routes include `app/api/routes/articles.py`, `comments.py`, and `user.py`, with API tests already under `tests/api`. Candidate: comment deletion authorizes the comment author or article author, but the route should also ensure the comment belongs to the requested article slug before deleting. Otherwise a valid comment id paired with another article path can create an ownership/resource-boundary confusion. Add an article-id/slug consistency check in the repository lookup or route. Lightweight check: existing pytest API fixtures for correct article, wrong article slug, non-author, and author success; no package install if cached.

## 3c142f8c1521 — D2

Review creation is in `src/app/api/reviews/route.ts`; persistence is `src/lib/db/schema.ts` and `src/lib/db/client.ts`, with review detail at `src/app/api/reviews/[id]/route.ts`. Candidate: POST inserts a pending review, then separately updates project rules and review metadata. A rules/template failure can leave a pending review without the metadata needed to process it. Make the aggregate preparation and review row update transactional where the Drizzle client supports it, or explicitly mark the row failed on preparation error. Lightweight check: route test with a transaction double that fails during rule/template preparation and asserts no orphan pending row; success test asserts metadata and status are consistent. Auth/provider/GitHub calls remain out of scope.

These are candidates only. Each requires a fresh staged baseline and source review before implementation, and each check should execute the real bounded production path with explicit repository doubles rather than a copied predicate.
