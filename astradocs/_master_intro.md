# Desktop projects: master SWE upskilling report

Reviewed September 6, 2026. This report combines the existing source inventory with a fresh static review and a recommended learning order. Scope: projects directly on the Desktop, `_Organized Desktop`, nested repositories such as `gitvg`, and the copied workspaces in `geminiorganized`.

## Start here

Use **one core project at a time**, with a small language/SQL practice lane alongside it. Your earlier [optimal upskill plan](../../master%20plan/optimal-upskill-plan.md) explicitly prioritizes **TypeScript/React/Node plus PostgreSQL first, with C#/.NET later**. This report follows that stack preference and recommends a smaller core route. It does not assume the old plan's 48-hour study week or promise its 16-week outcome.

Your route is:

**JSTut + selected JS1 exercises → a small React app → newcodexJS task manager + buildsql → one integrated CRUD app → grouphelpdesk → one reliability/tenant lab → harden grouphelpdesk into a portfolio capstone.**

Then, if C# remains part of your target, follow the .NET branch: **csharptut → BorrowBox → CampusOps → MeterForge**. The old plan introduced C# during its middle phase; putting it after one solid primary-stack capstone is this report's recommendation for reducing context switching.

Treat the other projects as substitutes, targeted labs, reference code, and later specializations. Having several versions of an issue tracker, billing system, or AI assistant is useful for comparison; it does not create a requirement to complete every version. Stage numbers in the catalog specify when a project becomes useful, not an obligation to finish it.

## Main route: TypeScript, React, Node, and PostgreSQL

| Order | Project(s) | Bounded assignment | Completion checkpoint |
|---|---|---|---|
| 1 | [JSTut](../../JSTut) and selected [JS1](../../JS1) exercises; [trainjs](../../_Organized%20Desktop/04%20JavaScript%20Training/trainjs) is an alternative structured course | Use task-board and contact-book for DOM/state/validation, then focus-timer for time/state. Learn promises and HTTP in the async lessons and API stage. | Build a small feature from a blank file, debug it, and explain its state and error paths. Skip fundamentals you can already demonstrate. |
| 2 | [recipeweb](../../recipeweb), or an early [FormForge](../../formforge) slice | Build one searchable, validated React UI with explicit state ownership. Add TypeScript gradually; the whole form platform is optional. | Explain props/state/effects; support keyboard use and loading, empty, error, and success states. |
| 3 | [newcodexJS/01-task-manager](../../newcodexJS/01-task-manager) plus [buildsql](../../buildsql) | Trace one browser → API → database workflow. Practice SQL joins, constraints and transactions before relying on an ORM. | Add one persisted feature and a meaningful API regression test; explain the SQL and HTTP behavior. |
| 4 | Choose [newcodexJS/05-recipe-manager](../../newcodexJS/05-recipe-manager) **or** [job track](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/job%20track) | Finish one integrated CRUD workflow with validation and authorization checks. Job track is the smaller JavaScript/React/Express + SQLite alternative. | Trace the request without a guide; test invalid input, a forbidden action, and persistence across restart. |
| 5 | [grouphelpdesk](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/grouphelpdesk); [gitjira-app](../../gitjira-app) is a larger alternative | Own one ticket lifecycle across the React client, shared contracts, and TypeScript/Express server. Inspect its SQLite/Prisma persistence, role rules, tests, CI and logs. | Extend one workflow independently and explain the module boundaries. Treat its learning-focused auth as a starting point that still needs hardening. |
| 6 | One targeted lab: [grokbuildmultitenantproject](../../grokbuildmultitenantproject) for tenant boundaries, or [ww26](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww26) for PostgreSQL locking | Implement one tenant-denial or concurrency regression. Apply the technique to the active project. Add an explicit PostgreSQL adapter/migration step because job track and grouphelpdesk use SQLite locally. | Demonstrate cross-tenant denial or conflict handling, durable PostgreSQL persistence, a clean migration, and safe retry behavior for the selected workflow. |
| 7 | Return to **grouphelpdesk** as the portfolio capstone | Complete a small product slice with real identity/session handling, authorization tests, durable data, reproducible setup, CI, useful logs, a demo and a short decision record. Keep external integrations clearly labeled. | Another developer can run it from the README; you can show success and failure paths, debug a broken request, and defend your design decisions. |
| 8 | One .NET bridge or one specialty below | Transfer the concepts you can already explain into C#, or add one AI/realtime/mobile capability. Choose one branch at a time. | Show what changed technically and why; verify the new failure mode rather than restarting your whole curriculum. |

Stages 2 and 3 cover client and server foundations; they can be learned in either order, but both precede integrated full-stack work.

## C#/.NET branch and completion checkpoints

Each row is a bounded learning assignment. A fifteen-sprint repository is a source of exercises; its entire published scope is not automatically the assignment.

| Order | Project(s) | Work to do | Move on when you can… |
|---|---|---|---|
| 1 | [csharptut](../../csharptut), supported by [JSTut](../../JSTut) | Use the C# and .NET fundamentals sequence. Practice functions, collections, nullability, exceptions, async, debugging, and small automated checks. Use JSTut for JavaScript/TypeScript/React explanations as those topics arise. | Write and debug a small program from a blank file, explain its data structures and error paths, and use Git to review a change. Skip material you can already demonstrate. |
| 2 | [JS1](../../JS1): use only missing prerequisites | Use a list/editor and filter/search exercise for DOM events, state, validation and local persistence. Study promises/HTTP with the first API exercise. Skip this step if you completed the primary route. | Implement a new requirement without copying a walkthrough; handle invalid input and persistence after refresh; explain state changes in the debugger. |
| 3 | [buildsql](../../buildsql), alongside the first backend project | Use the SQL lessons for joins, grouping, constraints, transactions, and indexes. Write queries yourself before revealing an answer. Reuse the same concepts on your project's actual schema. | Explain a join, detect duplicate rows, choose a uniqueness constraint, and show how a failed multi-step update is rolled back. Completing a lesson UI alone is insufficient. |
| 4 | [borrowbox](../../borrowbox) | Use the learner guide and early sprints for inventory → borrow → return. The default store is non-durable and teaching headers represent roles; SQLite is an adapter/exercise. Trace the request, rule, persistence boundary and response. | Explain the API contract; reject unavailable equipment; add or activate durable persistence for the slice; write a double-loan regression. Demo role headers demonstrate policy logic, not verified user identity. |
| 5 | [formforge](../../formforge), a limited frontend slice | Implement a form designer → validated response → response view flow. Learn React composition, TypeScript types, forms, and async UI. Defer the entire analytics/platform scope. [recipeweb](../../recipeweb) is a smaller client-focused substitute. | Describe ownership of state, validate on the appropriate boundary, support keyboard use, and handle loading, empty, error, and success states. |
| 6 | [campusops](../../campusops) | Build one facilities-request lifecycle end to end. Its default storage is non-durable; SQLite exists as an adapter. `X-Demo-Role` and `X-Demo-Campus` are teaching identity inputs. Add durable storage/migrations and real identity handling as scoped extensions. | Demonstrate actual identity and role/campus denials, a forbidden transition being blocked, a migration from a clean database, and a complete user-flow test. Rejecting a fabricated demo header alone is not an authentication milestone. |
| 7 | Pick **one**: [meterforge](../../meterforge), [.netramp](../../.netramp), or [globehire](../../globehire) | MeterForge: billing and tenant rules. Ramp: approvals. GlobeHire: workforce rules. Their teaching defaults include volatile data or simulated dependencies; MeterForge and GlobeHire do not provide production authentication. Add one durable, failure-sensitive workflow. | Explain retries, prevent duplicate processing, test tenant/role isolation as applicable, and recover from a partial failure. Document simulated integrations and what you added. |
| 8 | [netcleanarch](../../netcleanarch), then [.netarchitectureproject](../../.netarchitectureproject) as reading labs | Compare one completed feature with a reference design. Trace a request across layers/modules and write a short decision record. Refactor your own code only where a concrete coupling or testing problem justifies it. | Explain a boundary and its tradeoff, demonstrate a useful automated boundary check or isolated test, and avoid adding abstractions you cannot justify. |
| 9 | Return to **CampusOps or MeterForge** for a .NET portfolio slice | Finish one coherent slice with real authentication/authorization, durable persistence, reproducible setup, negative-path tests, CI, logs, configuration documentation and a demo. A migration runner, telemetry backend or recovery procedure must be added and verified if claimed; teaching-repo completion does not establish them. | Another developer can run the slice; you can demonstrate success and failure paths, identify limitations, and explain your own decisions. This is an optional second-stack portfolio exercise after the main route. |
| 10 | Choose one Stage 7 specialization after the capstone | Realtime collaboration: buildwhiteboard/netintercom. AI: netairag or one assistant project. Offline/mobile: recipeview/aral/buildsmallplates. Games: spacegame/spacegamev2. | Define the new correctness problem, build a small measurable experiment, and verify behavior beyond a successful demo. |

This ordering is an inference from your local projects. For a curriculum cross-check, MDN places semantic HTML, CSS, and JavaScript among the core web foundations, and Microsoft provides small API tutorials as an entry point to ASP.NET Core. Those references support learning the fundamentals before larger applications; they do not evaluate these local repositories. [MDN core curriculum](https://developer.mozilla.org/en-US/curriculum/core/), [Microsoft Minimal API tutorial](https://learn.microsoft.com/en-us/aspnet/core/tutorials/min-web-api?view=aspnetcore-10.0).

## How to use the stages

| Stage | Focus | Prerequisite | Appropriate result |
|---|---|---|---|
| 0 | Planning, learning aids, and reference collections | None for reading | Choose an exercise or retain a reference; do not turn organizing into the main project. |
| 1 | Language fundamentals and browser basics | Basic editor and Git use | Independently written small programs, DOM interactions, debugging, and small tests. |
| 2 | Client applications and state | Stage 1 | A usable, accessible UI with validation, state management, persistence, and error states. |
| 3 | HTTP APIs and SQL | Stage 1 plus basic HTTP | A tested API with a clear data model, constraints, and durable persistence. |
| 4 | Integrated full-stack applications | Stages 2 and 3 | A complete authenticated workflow with authorization and integration tests. |
| 5 | Domain rules and reliability | Stage 4 | Explicit state transitions, transactions, retries, auditability, and failure-path tests. |
| 6 | Architecture and advanced integrations | A completed Stage 5 slice | Justified module boundaries, a carefully scoped integration, and operational understanding. |
| 7 | AI, realtime, offline sync, desktop/mobile, and large-system specializations | Stage 4–6 as the project's specific risks require | One focused, evaluated specialty project. Mobile UI-only exercises can be used earlier in a mobile-focused track. |

Stage 0 does not mean that a reference codebase is technically simple. Large upstream repositories are usually Stage 6 reading labs. The catalog also identifies scaffolds, uncertain implementations, and candidate copies so that their apparent size is not confused with readiness.

Within a stage, use the core route first. An alternative replaces a core assignment with similar learning goals. A lab contributes one technique to the current project. A reference is primarily for reading. A candidate copy is another location/version to compare before choosing your working directory. Alphabetical listing within a location is navigation, not a finer-grained difficulty ranking.

## Alternatives and specializations

- **Additional TypeScript choices:** use JSTut and JS1, then selected `newcodexJS` apps, then a single issue tracker or teaching history such as `gitjira-app` or `netsnapshot`. Follow with one workflow project such as `buildevent`. Keep the SQL, testing, authorization, and reliability checkpoints. The C# branch can be added after completing a capstone in one backend stack.
- **Organized-subfolder route:** the full catalog places the training collections first, small CRUD/API labs next, business workflows after that, and architecture/AI/numbered advanced experiments later. Numbered folder names do not reliably indicate their difficulty or intended sequence.
- **Large upstream systems:** `.netopen2`, `.nettodo`, `netopen1`, `netopen3`, `netopen5`, `nopsolutionsnet`, `masteroutline`, and `masternocu` are useful for focused code reading. Pick one request, module, test, or issue to understand. Rebuilding or mastering the whole system is outside the core journey.
- **Realtime:** start with one connection and message lifecycle, then persistence, reconnects, ordering, presence, and concurrent edits. `buildwhiteboard`, `netintercom`, and the multiplayer games belong here after ordinary full-stack work.
- **AI and agents:** `netairag`, mission-control systems, coding agents, and assistant variants require explicit evaluation, failure handling, permissions, and external-service boundaries. A simulated provider or scaffold is useful practice, but it is not evidence that retrieval or autonomous execution works.
- **Mobile/offline:** use a small local-state app before client/server synchronization. `buildsmallplates`, `mobiletagalog`, `recipeview`, and `aral` offer different scopes; choose one based on the mechanism you want to learn.

## Working rhythm and portfolio evidence

Start each assignment by reading its entrypoint and tracing one user action through the source. Reproduce a small behavior, change one requirement, test a failure path, and record what you learned. Use a coding assistant to explain and review, then repeat a small part without the explanation visible. Being able to explain a generated codebase is a different milestone from being able to extend it independently; practice both.

Keep one application active and a small recurring practice lane for language fluency, SQL, Git, debugging, and interview exercises. Review progress by completed capabilities instead of the number of directories opened. No fixed deadline is assumed here because your starting proficiency and weekly availability are unknown.

For each portfolio project, retain a concise problem statement, architecture sketch, setup instructions, meaningful tests, a few decision records, a demo, and a candid limitations section. A small feature with demonstrable correctness is enough to move to the next learning goal; the surrounding clone's full advertised scope need not be finished.

## Review method and limits

The existing catalog was reviewed record by record and supplemented with fresh documentation, manifest, and source samples. It supplies broader file-discovery and historical inspection evidence; the new review corrects observed stale descriptions and missing coverage. These are static findings. No project was installed, built, tested, run, moved, or rewritten for this report. Source and test files demonstrate intent and structure, not passing behavior.

“Implementation present; unrun” means relevant source was found. “Tutorial/scaffold” means the folder primarily teaches or outlines an implementation; some of its code may still be substantial. “Uncertain” means the sample does not justify a stronger readiness claim. In-memory stores, mocked providers, demo authentication, and archived code remain explicit qualifications wherever the review found them. Binary learning documents and unrelated personal files were inventoried by location when applicable, not exhaustively read or reproduced.

The supporting [project review data](project-review.json) preserves each project's path, source evidence, assessment, and learning placement. The earlier [full source catalog](../project-catalog.json) retains deeper components and inspection details. The complete per-project catalog below is the practical reference for deciding what to open next.
