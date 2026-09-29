# Curated learning path (Fable's pick)

84 projects were marked `core` by reviewers. That is a pool, not a path. This is the sequence a junior should follow to become dependable
at CRUD web development on JS/TS/React/Node/Next and C#/.NET. Do one project at a time; do not do siblings of a project you have finished.
Each entry links to its review; the course itself is at `<project>/astraupskill/README.md`. Fix the listed blocker before starting where one is given.

Rule of thumb from the reviews: read the chapters `01-CODEBASE-MAP`, `03-WORKED-CHANGE` and `07-TRACE-LAB` closely (they are project-specific),
skim `02-CONCEPTS` and `05-PRACTICE` in wave-1 courses (they are template), and always diff Astra's backup against the project with
`diff -r --strip-trailing-cr -w` to see the real change.

## Stage 0 — browser CRUD reasoning (2 short sessions)

| Project | Teaches | Review |
|---|---|---|
| JS1/task-board | persist-then-publish ordering, undo that survives reload, storage-failure handling | [review](reviews/js1-task-board.md) |
| JS1/note-vault | same ideas against an Express + JSON-file API | [review](reviews/js1-note-vault.md) |

## Stage 1 — Express + Postgres fundamentals (newcodexJS 01-05)

| Project | Teaches | Review |
|---|---|---|
| newcodexJS/01-task-manager | request validation, 400 vs 500, disposable-schema test harness | [review](reviews/newcodexjs-01-task-manager.md) |
| newcodexJS/02-contact-book | CSV import as a state machine, transaction across three tables, pagination tie-breaker | [review](reviews/newcodexjs-02-contact-book.md) |
| newcodexJS/03-expense-tracker | money validation, partial updates | [review](reviews/newcodexjs-03-expense-tracker.md) |
| newcodexJS/04-notes-app | search/filter that does not match ids and timestamps | [review](reviews/newcodexjs-04-notes-app.md) |
| newcodexJS/05-recipe-manager | **ownership**: authn vs authz, `SELECT ... FOR UPDATE` inside the update, FK rollback test. Blocker: `isPublic` defaults to public when omitted (fix noted in review). | [review](reviews/newcodexjs-05-recipe-manager.md) |

## Stage 2 — TypeScript, transactions and concurrency (Postgres)

| Project | Teaches | Review |
|---|---|---|
| JS1/org-explorer | TOCTOU race closed with `LOCK TABLE ... SHARE ROW EXCLUSIVE` and re-check under lock; `Promise.all` race test | [review](reviews/js1-org-explorer.md) |
| JS1/room-booking | overlap prevention with `tstzrange` + `EXCLUDE USING gist` | [review](reviews/js1-room-booking.md) |
| JS1/warehouse-ledger | concurrent stock issue, `[201, 400]` race assertion with exact final balance | [review](reviews/js1-warehouse-ledger.md) |
| newcodexJS/13-ecommerce-storefront | lock ordering (`orderBy("id").forUpdate()`), trigger-injected rollback test | [review](reviews/newcodexjs-13-ecommerce-storefront.md) |
| newcodexJS/14-appointment-booking | overlap invariant inside the transaction, fault-injection rollback | [review](reviews/newcodexjs-14-appointment-booking.md) |
| newcodexJS/11-survey-builder | capacity counter with `FOR UPDATE` before increment, Zod at the boundary | [review](reviews/newcodexjs-11-survey-builder.md) |
| newcodexJS/07-blog-platform | partial-update semantics (undefined vs null vs absent), JSONB, 404 semantics. Do only this one of 07-10. | [review](reviews/newcodexjs-07-blog-platform.md) |
| newcodexJS/16-team-project-management | archive/restore, bulk audit. Do only this one of 16-20. | [review](reviews/newcodexjs-16-team-project-management.md) |
| JS1/secure-notes | token auth basics. Blocker: add session expiry (review lists it). | [review](reviews/js1-secure-notes.md) |
| JS1/learning-paths | one status transition in one `withTransaction` with audit row; DATE type parser. Do only this one of JS1 41-50 TS variants. | [review](reviews/js1-learning-paths.md) |

## Stage 3 — Prisma apps with real tenancy and versioning

| Project | Teaches | Review |
|---|---|---|
| grokbuildorderproject | optimistic concurrency via conditional `updateMany` on `(id, version)` + stock floor | [review](reviews/grokbuildorderproject.md) |
| grokbuildteamproject | compound FKs `(assigneeId, organizationId)` so the DB rejects cross-tenant writes even if the service is bypassed | [review](reviews/grokbuildteamproject.md) |
| grokbuildhrproject | approval chains, advisory locks (and when they are too coarse) | [review](reviews/grokbuildhrproject.md) |
| master4 | stock reservation with duplicate-SKU handling; ships a real worked solution | [review](reviews/master4.md) |
| buildcrmpyjs | privilege escalation via public register, Express error-handler arity bug. Blocker: no CRUD routes exist yet; treat as an auth lesson. | [review](reviews/buildcrmpyjs.md) |
| appmakertrack | 409 conflict semantics, ordered moves, instant parsing | [review](reviews/appmakertrack.md) |

## Stage 4 — Next.js

| Project | Teaches | Review |
|---|---|---|
| e6 | authorization projection before pagination in Next route handlers | [review](reviews/e6.md) |
| b1 | membership and referential integrity in route handlers with async `params` | [review](reviews/b1.md) |
| ww37 | PATCH semantics + concurrency; Next 15 async `params` migration | [review](reviews/ww37.md) |
| z3/customer-feedback-board | `"use server"` actions, SQLite `BEGIN IMMEDIATE`, `revalidatePath` after commit | [review](reviews/z3-customer-feedback-board.md) |
| z3/founder-crm-lite | read-then-write races inside the serialization boundary; session handling | [review](reviews/z3-founder-crm-lite.md) |
| z7 | what leaks into the RSC payload vs a hidden element; `React.cache` per request | [review](reviews/z7.md) |
| d1 | Drizzle atomic `version + 1` returning; Socket.IO and `next/headers` misuse fixed | [review](reviews/d1.md) |
| jdtrrain2.1 | Prisma + Next CRUD with conditional updates | [review](reviews/jdtrrain2-1.md) |
| job track/restaurant-kitchen-display-system | Express + SQLite + Socket.IO CRUD; best-scored React app in the set | [review](reviews/job-track-restaurant-kitchen-display-system.md) |

## Stage 5 — C# / .NET

| Project | Teaches | Review |
|---|---|---|
| meterforge | idempotent ingestion, replay vs 409, Problem Details; perfect score. Add the DB mapping the review asks for. | [review](reviews/meterforge.md) |
| borrowbox | domain rules and validation in a clean .NET service | [review](reviews/borrowbox.md) |
| netgum | EF Core (InMemory) + real xUnit; value-object validation | [review](reviews/netgum.md) |
| nethris | EF Core + SQLite with real transactions; EF tracking bug with caller-supplied Guid | [review](reviews/nethris.md) |
| campusops | stock reservation + history committed together; four red-then-green isolation tests | [review](reviews/campusops.md) |
| missioncontrol | EF Core + SQLite concurrency (WAL, busy_timeout, Serializable → BEGIN IMMEDIATE) | [review](reviews/missioncontrol.md) |
| netzen | authorization pushed into the query, not after pagination | [review](reviews/netzen.md) |
| buildjira | PATCH with omitted-vs-null JSON handling; live-singleton mutation bug | [review](reviews/buildjira.md) |
| geminiorganized/OpenSource_Upskilling_.Stripe | capstone: raw ADO.NET + SQLite transactions, Playwright-verified | [review](reviews/geminiorganized-opensource-upskilling-stripe.md) |

## Electives (pick by gap, not in sequence)

- **Browser-only but well taught:** buildsubbox, buildgum, JSProjectLearn, recipeweb, jobtrack, finance-dashboard, JS1/kanban-flow, JS1/poll-studio, astra4.2, buildsql (a React app, not a SQL course).
- **Realtime / queues:** job track/live-chat-support-platform, job track/task-queue-system, buildwhiteboard, e6.
- **Bigger .NET / TS codebases for reading:** nettrello, netpastebin, buildasana, netvg (fix the `checked`/decimal sentence first), formforge, e20, e12, jstrain3.0, jstrain2.3, master2, master3, master7, master 6, grokbuildecommerceproject, grokbuildmultitenantproject, grokbuildppmproject, buildantigVG, lucasrouter, aiheartbeat, buildbusinesses, z1, globgame (after code blocks are added).
- **Reference only (off the target stack, strong ideas):** j1, j2, j3, j4, j5, j7 (Java), e14, e15, aiapplybot (Python), andie (Shopify tool), buildsmallplates (React Native).

Note: the project folder `04 JavaScript Training/react` is a vanilla-JS quiz board, **not a React course**; it now carries an HTTP companion chapter (08) and belongs with the browser-CRUD electives, not with React.

## Skip (duplicates of something above)

JS1/library-lending, gym-membership, campaign-planner, volunteer-coordinator (clones of equipment-maintenance); JS1/field-service,
research-studies (clones of subscription-billing); JS1/travel-requests, vendor-contracts, quality-audits, grant-manager, incident-response
(clones of learning-paths); JS1/procurement-portal, property-rentals, patient-intake (clones of project-risks); newcodexJS/08, 09, 10
(clones of 07); newcodexJS/17, 18, 19, 20 (clones of 16). The code in these is fine; the lesson is identical.

## Fix before use

JS1/pulse-analytics (fixture wrong in seven files), JS1/forum-search (verification narrative does not match the test), w24 (fabricated
worked excerpt), z9 and zz8 (chapters mis-filed), e13 (archived test reseeds `dev.db`), ww27 (verification cites superseded logs).
