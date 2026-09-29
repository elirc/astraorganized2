# Batch04 read-only candidate review

Reviewed 2026-09-21 against the ten pending campaign entries. The protected families and completed projects were excluded. No canonical source, stage, spec, or evidence file was modified during this review. `e17` and `g1` contain project `AGENTS.md`; those instructions must be read again before any staged implementation.

## 43d6b6358f56 - D3

Candidate: harden the API-key revoke path in `actions/api-key-actions.ts` and `lib/services/apiKeys` so revocation is idempotent and organization scoped. The action already checks `manage_api_keys`, while the service exposes create/revoke/list. Inspect whether a second revoke reports success, targets a key outside `ctx.organizationId`, or writes an audit event after a missing row. A dependency-free test can execute the service with repository doubles and assert denied cross-organization ids cause zero writes, first revoke changes state, and repeated revoke has a defined result. Preserve existing permission wrapper behavior and do not claim database uniqueness without a DB check.

## 3b0530b090c4 - e11

Candidate: complete the asset CRUD read path. `server/app.ts` accepts multipart `POST /api/assets`, calls `saveAssetBuffer`, and returns `/api/assets/:id`, but the GET route currently returns 501. Inspect `server/store.ts` for the stored buffer contract, then implement a bounded GET that returns the persisted bytes with content type/name or a truthful 404. Runtime Supertest cases can POST a small asset, GET its returned id, check bytes and missing-id behavior, and retain the existing missing-file 400 case. No large install is needed if the existing server test dependencies are cached.

## 2f59a0d07a85 - e17

Candidate: inspect forum reply/update/delete authorization in `src/lib/forum-core.ts` and its API/server-action callers. The onboarding map identifies `createReply`, hidden/deleted/staff-only states, and permission checks. A bounded gap would be a mutation that finds a reply by id without tenant/community ownership in its update or delete predicate. Read `AGENTS.md` and the relevant Next guide first. A service runtime harness with explicit Prisma repository doubles should prove same-scope success, cross-scope denial, missing-row behavior, and zero writes on refusal; avoid inventing a new auth architecture.

## 330bb6feda2f - e3

Candidate: inspect the local CRUD service for records whose update/delete operation reports success when an id is absent. The project has `app`, `components`, `lib`, `tests`, and typed domain models. Start with `lib/` repository/service files and existing Vitest tests, find a concrete `map`/`filter` or unchecked update result, and add a focused runtime test through the real service with an in-memory repository double. Keep the fix to one entity and preserve current response shapes; do not stage until the source confirms a gap.

## 1cf37faa32e8 - e4

Candidate: review the notification or recipient delivery CRUD boundary described by `docs/onboarding/00-codebase-map.md` and `src/server`. The map says a service creates or upserts recipient/delivery rows and routes trigger revisions. Look for an update/delete path that is not scoped by the owning publication or that treats an absent row as success. A lightweight Node/TypeScript service harness can assert owner mismatch produces no repository or outbox write, valid owner mutation succeeds, and missing id is explicit. Native Prisma/Next tests are optional and should not be installed just for this check.

## d7c9faad43d9 - g1

Candidate: inspect admin city/shop CRUD under `src/app/api/admin` and its Drizzle repositories. The project prompt requires admin-secret protection and says shops upsert by city plus slug. A bounded correctness gap is an update/delete route that accepts an id without verifying the admin secret or city ownership, or an upsert that treats city+slug inconsistently. Read `AGENTS.md` and the current Next guide before staging. Test the actual route/service with explicit auth and repository doubles: unauthorized requests must produce zero writes; same-city update succeeds; duplicate city+slug has one defined outcome. Do not claim a durable uniqueness fix without executing the Drizzle database.

## 195e77d61335 - rn1

Candidate: inspect the social-app profile mutation query lifecycle around `src/state/queries` and the documented profile mutation example in `social-app/CLAUDE.md`. A bounded CRUD gap likely sits where profile update success does not invalidate or update the profile query key, leaving stale profile data after a write. Confirm in actual source first. A dependency-free test can execute the mutation function with a mocked agent and query client, assert the write payload and exact invalidation key, and assert failures do not publish a success update. Avoid modifying generated/native code or claiming a mounted React Native test.

## 06f66ec88e8d - w21

Candidate: audit `src/services/admin/gateway-route-service.ts` lifecycle transitions and repository predicates. The service already checks role, accessible route, legal transition, and active-policy presence. A bounded gap to verify is the update result: if `updateGatewayRouteStatus` returns no row after the pre-read, does the service report success? If so, convert it to an explicit not-found/conflict result while preserving the transaction. Runtime tests can call the actual service with Prisma/permission/repository doubles for legal transition, illegal transition, policy refusal, and zero-write missing-update behavior. Existing admin authorization architecture should remain intact.

## 529eba39810c - w22

Candidate: inspect `src/services/paymentService.ts` and payment event/reconciliation paths for a bounded replay or status persistence mismatch. The create flow already requires an idempotency key, fingerprints payloads, uses a transaction, and stores a response snapshot. Verify whether provider `PARTIAL_SUCCESS` or `NETWORK_UNKNOWN` creates a payment/event state that can be replayed consistently, or choose a narrower validation/state transition gap confirmed in source. A service harness with repository/provider doubles should assert first create, completed replay, same-key different-payload refusal, and the selected failure state without charging a real provider or installing the full stack.

## 5df5911fc343 - w23

Candidate: inspect ticket update/delete and search document synchronization in `src/services/ticketService.ts` and repositories. Ticket creation and status updates already use transactions, tenant predicates, audit logs, and incremental indexing events. Confirm whether any update/delete path can return success after a repository no-op or enqueue a search event for a missing ticket. A focused service harness should prove tenant mismatch and missing id perform zero writes, valid mutation writes the source row plus audit/sync records, and search state remains scoped. Do not broaden into a search rebuild or auth rewrite.

## Shared check strategy

Prefer existing Node/Vitest or Python standard-library checks after confirming cached tooling. For TypeScript services, use the project-local VM loader pattern with explicit repository and auth doubles, executing the production function or route. For Express e11, use its existing Supertest tests. For Prisma/Drizzle projects, keep database claims separate from double-based service evidence and document native runner limits. Each implementation should snapshot every changed baseline file before edits and preserve existing learning documents.
