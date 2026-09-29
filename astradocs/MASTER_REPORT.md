# Desktop projects: master SWE upskilling report

**Final coverage check - September 7, 2026:** `_Organized Desktop` contributes **202 included project/resource records**, including 40 Master Projects and 84 Numbered Experiments. A fresh Desktop-wide scan found no additional project requiring a report entry. See the [dated coverage review](FINAL_REVIEW.md) for the full folder breakdown and exclusions.

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

## Coverage and corrections

**389 reviewed project/workspace and resource-collection records.** The earlier inventory contained 388; this review adds [astra4.2](../../astra4.2). Bundled teaching exercises stay beneath their parent workspaces rather than inflating this count.

| Location | Reviewed records |
|---|---:|
| Desktop / direct workspaces | 89 |
| Desktop / gitvg nested repositories | 18 |
| Desktop / jsharness nested repositories | 2 |
| _Organized Desktop/01 Net Workspaces | 9 |
| _Organized Desktop/02 Build Projects | 13 |
| _Organized Desktop/03 Master Projects | 40 |
| _Organized Desktop/04 JavaScript Training | 15 |
| _Organized Desktop/05 Numbered Experiments | 84 |
| _Organized Desktop/06 AI And Learning | 9 |
| _Organized Desktop/07 Anti Projects | 4 |
| _Organized Desktop/08 App And Product Projects | 9 |
| _Organized Desktop/09 Grav And VG Projects | 5 |
| _Organized Desktop/12 Other Projects | 14 |
| geminiorganized | 78 |

The historical discovery covered 108 Git roots, 100,421 directories, and 415,133 files after exclusions. Those are the earlier scan totals, not a claim that every file was freshly reread for this report. Its 56 candidate copy/version groups use selected file fingerprints, not complete directory comparisons. See [historical scan validation](../inventory-validation.json).

Corrections that materially affect your learning order:

- `.nettodo` is the eShopOnWeb reference storefront. `netopen3` is the Umbraco C#/.NET CMS source. Their names or stale framework tags should not place them among beginner CRUD apps.
- `astra4.2` is a browser break/timer extension with a local preview server; its implementation was missing from the earlier catalog.
- `newcodecjs2` contains five architecture scaffolds. `newcodexJS` contains 20 app folders. `newcodex3/apps` contains 25 numbered concepts with TypeScript and .NET variants (50 folders). README counts and project titles can overstate the implemented scope.
- `netsnapshot` and `netsnapshot1` teach TypeScript/Node + React through saved steps; the “net” prefix does not make them C# courses.
- The modular-monolith README describes shortcomings in other sample applications; its “not finished/no authentication” wording should not be attributed to `.netarchitectureproject` itself.
- A frontend connected to demo identity or a memory adapter can be an excellent learning artifact while still needing work before it demonstrates real authentication or durable persistence.

## Exercise collections: order inside the workspace

| Workspace | Suggested internal order and scope |
|---|---|
| [csharptut](../../csharptut) | Chapters 00–15 for language/data/async; 16–21 for I/O, HTTP, DI, EF, APIs and tests; 22 for the CRUD capstone. Use 23–24 for study guidance. The repository assumes general programming basics; start with a basic language lesson first if variables, loops, and functions are unfamiliar. |
| [JSTut](../../JSTut) | JS fundamentals first; Node, TypeScript, React and SQL as the active project requires; advanced and C#/.NET companion sections later. Use its workbooks for recall and independent implementation. |
| [JS1](../../JS1) | Selected path: task-board → contact-book → focus-timer → issue-desk → secure-notes → invoice-studio → room-booking. The README spans vanilla JS, React/Express, TypeScript/Postgres, richer workflows, and .NET variants. Move between tiers when the relevant checkpoint is met; do not complete all variants. |
| [JSProjectLearn](../../JSProjectLearn) | The current source is SkillForge Quest: 334 missions across 10 worlds, with 1,839 preserved source files recorded in its migration report. Use it as an alternative fundamentals campaign; sequential gates may require earlier unlocks. Its Gemini counterpart retains an older 165-exercise curriculum, so these are materially different versions. |
| [_Organized Desktop/04 JavaScript Training/trainjs](../../_Organized%20Desktop/04%20JavaScript%20Training/trainjs) | Follow foundations → functions/data → objects/modules/errors → DOM → async/fetch → Node/tooling → backend → testing → TypeScript → React → capstone. Defer advanced architecture until after an application slice. |
| [_Organized Desktop/04 JavaScript Training/jstrain2.2](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.2) | A large multi-track curriculum, not a small starter app. Choose a flight plan and relevant JS/TS/C# lessons; use its portfolio workspaces to apply them. |
| [newcodexJS](../../newcodexJS) | Start with 01-task-manager, then select a distinct data or workflow problem. Later apps often reuse CRUD/admin patterns; “realtime chat” and “marketplace” names do not prove sockets or payments are implemented. See the child catalog below. |
| [newcodecjs2](../../newcodecjs2) and [newcodex3](../../newcodex3) | Architecture/workflow reading scaffolds. Choose one business domain and one language variant after ordinary full-stack work; trace a feature and complete one missing durable behavior. See the child catalog below. |
| [netsnapshot](../../netsnapshot) and [netsnapshot1](../../netsnapshot1) | Start at 00-walking-skeleton and compare adjacent snapshots using NOTES/CHANGES. Predict the next change, inspect it, then independently implement a small variant. Saved copies are sequential course states, not separate capstones. |

## Complete per-project catalog

Each entry has a stage, purpose, stack, static assessment, learning value, prerequisite, next action, and source links. Main-route assignments above take priority; other entries are choices within their stated stage.

- [Desktop / direct workspaces](#location-desktop-direct-workspaces)
- [Desktop / gitvg nested repositories](#location-desktop-gitvg-nested-repositories)
- [Desktop / jsharness nested repositories](#location-desktop-jsharness-nested-repositories)
- [_Organized Desktop/01 Net Workspaces](#location-organized-desktop-01-net-workspaces)
- [_Organized Desktop/02 Build Projects](#location-organized-desktop-02-build-projects)
- [_Organized Desktop/03 Master Projects](#location-organized-desktop-03-master-projects)
- [_Organized Desktop/04 JavaScript Training](#location-organized-desktop-04-javascript-training)
- [_Organized Desktop/05 Numbered Experiments](#location-organized-desktop-05-numbered-experiments)
- [_Organized Desktop/06 AI And Learning](#location-organized-desktop-06-ai-and-learning)
- [_Organized Desktop/07 Anti Projects](#location-organized-desktop-07-anti-projects)
- [_Organized Desktop/08 App And Product Projects](#location-organized-desktop-08-app-and-product-projects)
- [_Organized Desktop/09 Grav And VG Projects](#location-organized-desktop-09-grav-and-vg-projects)
- [_Organized Desktop/12 Other Projects](#location-organized-desktop-12-other-projects)
- [geminiorganized](#location-geminiorganized)

<a id="location-desktop-direct-workspaces"></a>

### Desktop / direct workspaces

#### antigravupskill

**Stage 0: Planning and reference collections. reference.** [Open folder](../../antigravupskill)

Existing architecture reviews and learning notes for Antigravity projects; retained as reference material.

- **Stack:** languages: Python.
- **Review:** Existing generated review collection; do not treat prior audit claims as current source truth. Static review only; not built, tested or run.
- **Learn:** Prior architecture reviews and code-reading exercises
- **Before starting:** None; use alongside active project work.
- **Next:** Consult only the review matching the currently selected project.
- **Evidence:** [README.md](../../antigravupskill/masterdocs/README.md), [build_grok_reviews.py](../../antigravupskill/scripts/build_grok_reviews.py).

#### buildsql

**Stage 0: Planning and reference collections. Core supporting practice.** [Open folder](../../buildsql)

An active, gamified software-learning journey built with React and TypeScript.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: React; Vite; infrastructure: GitHub Actions; testing: Vitest.
- **Review:** Gamified React study application; large lesson counts do not demonstrate mastery. Static review only; not built, tested or run.
- **Learn:** Active recall, SQL and SWE mission practice
- **Before starting:** None; use alongside active project work.
- **Next:** Use missions for current curriculum gaps and produce code evidence.
- **Evidence:** [README.md](../../buildsql/README.md), [App.tsx](../../buildsql/src/App.tsx), [package.json](../../buildsql/package.json).

#### c#interview

**Stage 0: Planning and reference collections. reference.** [Open folder](../../c%23interview)

Ten-week C# upskilling and interview-preparation curriculum with drills and portfolio work.

- **Stack:** .
- **Review:** Curriculum documents rather than an application. Static review only; not built, tested or run.
- **Learn:** C# drills, interview explanations, ten-week structure
- **Before starting:** None; use alongside active project work.
- **Next:** Take a baseline drill, then use weak areas beside the current project.
- **Evidence:** [README.md](../../c%23interview/README.md).

#### claude docs

**Stage 0: Planning and reference collections. reference.** [Open folder](../../claude%20docs)

Software-engineering study plans, worked examples, and coding-practice guidance.

- **Stack:** .
- **Review:** Five substantive Markdown study guides; schedules are assumptions rather than personalized commitments. Static review only; not built, tested or run.
- **Learn:** Project-first learning, review habits, worked examples
- **Before starting:** None; use alongside active project work.
- **Next:** Use one project-first routine and apply its review checklist to an actual change.
- **Evidence:** [plan-1-project-first.md](../../claude%20docs/plan-1-project-first.md).

#### devdeck

**Stage 0: Planning and reference collections. study-helper.** [Open folder](../../devdeck)

A spaced-repetition flashcard PWA for learning software development in 5–15 minute sessions — on the bus, waiting for a delivery, wherever.

- **Stack:** languages: CSS; HTML; TypeScript; frameworks: React; Tailwind CSS; Vite; data: IndexedDB / Dexie; testing: Vitest.
- **Review:** Local IndexedDB PWA with source and tests; a smaller overlapping study helper. Static review only; not built, tested or run.
- **Learn:** Short recall sessions, spaced repetition, web fundamentals
- **Before starting:** None; use alongside active project work.
- **Next:** Choose this or ankijs for daily recall, not parallel card backlogs.
- **Evidence:** [README.md](../../devdeck/README.md), [App.tsx](../../devdeck/src/App.tsx), [package.json](../../devdeck/package.json).
- **Related versions/options:** [geminiorganized/General_Devdeck](../../geminiorganized/General_Devdeck). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### gitjira

**Stage 0: Planning and reference collections. reference.** [Open folder](../../gitjira)

Sprint plans and build instructions for the separate GitJira issue-tracker app.

- **Stack:** .
- **Review:** Planning repository with no application source; companion to gitjira-app. Static review only; not built, tested or run.
- **Learn:** Sprint planning, review choreography, issue-tracker specifications
- **Before starting:** None; use alongside active project work.
- **Next:** Use the relevant playbook beside gitjira-app and do exercises independently.
- **Evidence:** [README.md](../../gitjira/sprints/README.md).

#### GPTDocs

**Stage 0: Planning and reference collections. reference.** [Open folder](../../GPTDocs)

Software-engineering learning and reference documents.

- **Stack:** .
- **Review:** Two expanded Markdown reference guides, not an application. Static review only; not built, tested or run.
- **Learn:** Code review, production failure modes, worked examples
- **Before starting:** None; use alongside active project work.
- **Next:** Apply one rubric to the next project change.
- **Evidence:** [production-code-best-practices-expanded.md](../../GPTDocs/production-code-best-practices-expanded.md).

#### hermes

**Stage 0: Planning and reference collections. reference.** [Open folder](../../hermes)

Operating pack for using Hermes as a software engineering assistant.

- **Stack:** .
- **Review:** Operating documents plus helper/cleanup scripts; not a portfolio app. No cleanup scripts were executed. Static review only; not built, tested or run.
- **Learn:** Engineering rituals, prompts, note taking, assisted learning
- **Before starting:** None; use alongside active project work.
- **Next:** Choose one prediction-review-reflection routine and apply it to a real ticket.
- **Evidence:** [README.md](../../hermes/README.md).

#### master plan

**Stage 0: Planning and reference collections. reference.** [Open folder](../../master%20plan)

Project-based software-engineering study plans and a progression of practice projects.

- **Stack:** .
- **Review:** Prior planning documents; its eight-hour daily assumption is not a user commitment. Static review only; not built, tested or run.
- **Learn:** Existing sixteen-week ladder and study organization
- **Before starting:** None; use alongside active project work.
- **Next:** Use prior plans as context; adopt the new report's small project sequence.
- **Evidence:** [README.md](../../master%20plan/README.md).

#### readme

**Stage 0: Planning and reference collections. reference only.** [Open folder](../../readme)

Existing Desktop inventory document; listed as a reference artifact and not used to discover or assess projects.

- **Stack:** .
- **Review:** Inventory/reference repository containing README.md, not an application.
- **Learn:** Organizing evidence and locating previous project descriptions.
- **Before starting:** No application prerequisite; use alongside the journey.
- **Next:** Use only as historical orientation; prefer this newly verified master report for order.
- **Evidence:** [README.md](../../readme/README.md).

#### resume

**Stage 0: Planning and reference collections. career reference.** [Open folder](../../resume)

Career and résumé reference materials.

- **Stack:** .
- **Review:** Career reference repository containing resume reviews, role guides and rewritten variants; no application manifests.
- **Learn:** Translate verified project work into role-specific evidence.
- **Before starting:** No application prerequisite; use alongside the journey.
- **Next:** Choose target SWE role and replace broad claims with outcomes from projects you can explain and demonstrate.
- **Evidence:** [resume-review-index.md](../../resume/resume-review-index.md).

#### csharptut

**Stage 1: Language and browser foundations. .NET branch after the primary-stack capstone.** [Open folder](../../csharptut)

A practical, no-fluff path from "I can write basic code" to "I can be trusted on a real C# team doing CRUD/backend work."

- **Stack:** .
- **Review:** Sequential teaching documents with embedded exercises, not a built application. Static review only; not built, tested or run.
- **Learn:** C# fundamentals through EF Core, APIs and testing
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Work 00-15 then 16-21; independently rebuild the chapter 22 CRUD capstone.
- **Evidence:** [README.md](../../csharptut/README.md).
- **Related versions/options:** [geminiorganized/General_Csharptut](../../geminiorganized/General_Csharptut). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### finance-dashboard

**Stage 1: Language and browser foundations. alternative.** [Open folder](../../finance-dashboard)

A self-contained household finance dashboard for expenses, bills, savings goals, and investment tracking.

- **Stack:** languages: CSS; HTML; JavaScript.
- **Review:** Small three-source-file browser app; no backend or tests found in catalog. Static review only; not built, tested or run.
- **Learn:** Vanilla JavaScript, forms, derived totals, localStorage
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Add a validated expense edit and confirm totals survive reload.
- **Evidence:** [README.md](../../finance-dashboard/README.md), [app.js](../../finance-dashboard/app.js).
- **Related versions/options:** [geminiorganized/General_Finance-Dashboard](../../geminiorganized/General_Finance-Dashboard). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### grokjs

**Stage 1: Language and browser foundations. alternative.** [Open folder](../../grokjs)

JavaScript, .NET, and full-stack practice labs with worked explanations and exercises.

- **Stack:** languages: C#; HTML; JavaScript; Python; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Large multi-language collection with many examples; not one coherent application or a required linear course. Static review only; not built, tested or run.
- **Learn:** Language labs, JavaScript, Python, C#, full-stack exercises
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Pick one language lab and one exercise matching a current gap.
- **Evidence:** [README.md](../../grokjs/README.md), [Program.cs](../../grokjs/grokbuildc%23/backend/Program.cs), [package.json](../../grokjs/javascript-learning-lab/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Grokjs](../../geminiorganized/LLM_Generated_Grokjs). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### groktuts

**Stage 1: Language and browser foundations. alternative.** [Open folder](../../groktuts)

Collection of , hands-on upskilling laboratories.

- **Stack:** languages: C#; JavaScript; Python; SQL; TypeScript; frameworks: React; testing: Vitest; pytest; xUnit.
- **Review:** Multi-language teaching labs with source examples and some tests; unknown label does not mean empty. Static review only; not built, tested or run.
- **Learn:** JS/TS/React, Python, C#, SQL fundamentals
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Use one lab to close a measured fundamentals gap.
- **Evidence:** [README.md](../../groktuts/README.md), [Program.cs](../../groktuts/dotnet-upskilling-lab/csharp/01-lesson/Program.cs), [package.json](../../groktuts/web-dev-upskilling-lab/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Groktuts](../../geminiorganized/LLM_Generated_Groktuts). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### JS1

**Stage 1: Language and browser foundations. Core route.** [Open folder](../../JS1)

Standalone vanilla JavaScript CRUD apps live in this workspace.

- **Stack:** languages: C#; CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Express; Node.js; React; Vite; data: PostgreSQL.
- **Review:** Multi-tier exercise workspace; later tiers are study scaffolds and require their own dependencies/database. Static review only; not built, tested or run.
- **Learn:** Vanilla CRUD to React APIs, SQL and .NET practice
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Select task-board, contact-book, focus-timer, issue-desk, secure-notes, invoice-studio, room-booking in that order.
- **Evidence:** [README.md](../../JS1/README.md), [App.tsx](../../JS1/field-service/client/src/App.tsx), [package.json](../../JS1/asset-checkout/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Js1](../../geminiorganized/LLM_Generated_Js1). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### JSProjectLearn

**Stage 1: Language and browser foundations. study-helper.** [Open folder](../../JSProjectLearn)

SkillForge Quest turns the original software-engineering curriculum into an active, persistent campaign.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: React; Vite; testing: Vitest.
- **Review:** Current SkillForge Quest README reports 334 missions, 1,002 gates and 1,839 preserved files across 10 worlds, with sequential prerequisites and locked transitions. C# is optional; the primary campaign is JS/TS/React. Author-reported quality checks were not rerun in this static review.
- **Learn:** Recall, prediction, build evidence, prerequisite gates
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Use as an alternative fundamentals campaign; select relevant archived exercises while accounting for sequential mission unlocks. Do not add a second 334-item backlog.
- **Evidence:** [README.md](../../JSProjectLearn/README.md), [App.tsx](../../JSProjectLearn/src/App.tsx), [package.json](../../JSProjectLearn/package.json).

#### JSTut

**Stage 1: Language and browser foundations. Core supporting practice.** [Open folder](../../JSTut)

A tutorial for software engineers who want to build real fullstack fluency.

- **Stack:** .
- **Review:** Structured text curriculum; embedded examples require active practice rather than passive completion. Static review only; not built, tested or run.
- **Learn:** JavaScript, Node, TypeScript, React, SQL, C#/.NET concepts
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Use fundamentals Parts 1-9 alongside JS1; defer advanced parts until API work.
- **Evidence:** [README.md](../../JSTut/README.md).

#### AlanAndEliSoccer

**Stage 2: Client apps and state. alternative.** [Open folder](../../AlanAndEliSoccer)

A Next.js learning app for the 17 Laws of Soccer, World Cup context, and practical match tools.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS.
- **Review:** Recognizable content application; catalog found no tests. Treat sports content separately from code study. Static review only; not built, tested or run.
- **Learn:** Next.js routes, content modeling, search, local UI state
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Add a tested saved-law or referee-tool interaction.
- **Evidence:** [README.md](../../AlanAndEliSoccer/soccer-laws-app/README.md), [RefereeNotebook.tsx](../../AlanAndEliSoccer/soccer-laws-app/src/components/tools/RefereeNotebook.tsx), [package.json](../../AlanAndEliSoccer/soccer-laws-app/package.json).
- **Related versions/options:** [geminiorganized/General_Alanandelisoccer](../../geminiorganized/General_Alanandelisoccer). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### ankijs

**Stage 2: Client apps and state. study-helper.** [Open folder](../../ankijs)

A , local-first spaced-repetition web app for the spare minutes in your day.

- **Stack:** languages: CSS; HTML; Python; SQL; TypeScript; frameworks: React; Tailwind CSS; Vite; data: IndexedDB / Dexie; Supabase; infrastructure: GitHub Actions; testing: Playwright; Vitest.
- **Review:** Substantial local-first flashcard app with tests; optional Supabase sync is separate from offline study. Static review only; not built, tested or run.
- **Learn:** Spaced repetition, IndexedDB, offline state, optional sync
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Use short daily recall sessions; study one scheduling or sync invariant.
- **Evidence:** [README.md](../../ankijs/README.md), [App.tsx](../../ankijs/src/App.tsx), [package.json](../../ankijs/package.json).

#### astra4.2

**Stage 2: Client apps and state. alternative.** [Open folder](../../astra4.2)

Hourly focus timer with fullscreen art breaks and custom reminders, packaged as a Chrome Manifest V3 extension with a local Node preview.

- **Stack:** languages: JavaScript; HTML; CSS; frameworks: Chrome Extension Manifest V3; Node.js; data: Chrome storage / local browser state; infrastructure: esbuild; testing: Node test script; referenced test directory absent; integrations: Chrome alarms.
- **Review:** Partial implementation: timer state machine, extension background code and UI source are present. extension/assets is empty although app.js references artwork; generated extension/app.js and tests directory are absent. No build or runtime verification.
- **Learn:** State machines, timer correctness, persistence, browser extension events and packaging.
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Complete one focus/pause/break state test, supply local artwork or a fallback, and verify the bundle before using as an extension.
- **Evidence:** [app.js](../../astra4.2/src/app.js), [package.json](../../astra4.2/package.json).

#### buildbusinesses

**Stage 2: Client apps and state. alternative.** [Open folder](../../buildbusinesses)

LocalOps Ledger for keeping daily operating records for small local businesses.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS.
- **Review:** Small custom UI behind a stock Next.js README; backend durability is not established by the sample. Static review only; not built, tested or run.
- **Learn:** React forms, dashboard state, business record modeling
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Trace LocalOperationsApp state and add one validated record flow.
- **Evidence:** [README.md](../../buildbusinesses/README.md), [page.tsx](../../buildbusinesses/src/app/page.tsx), [package.json](../../buildbusinesses/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Buildbusinesses](../../geminiorganized/LLM_Generated_Buildbusinesses). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### calendar+jobtrack

**Stage 2: Client apps and state. alternative.** [Open folder](../../calendar%2Bjobtrack)

A personal calendar and a gamified job-application tracker in one local-first app.

- **Stack:** languages: CSS; HTML; TypeScript; frameworks: React; Tailwind CSS; Vite; testing: Vitest.
- **Review:** Local-only React app with test files; no account or backend by design. Static review only; not built, tested or run.
- **Learn:** TypeScript, Zustand, calendar state, local persistence
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Add one calendar conflict or job-stage validation case with a test.
- **Evidence:** [README.md](../../calendar%2Bjobtrack/README.md), [App.tsx](../../calendar%2Bjobtrack/src/App.tsx), [package.json](../../calendar%2Bjobtrack/package.json).

#### formforge

**Stage 2: Client apps and state. main-path.** [Open folder](../../formforge)

FormForge is a , schema-driven form builder and response analytics platform built as a fifteen-sprint React and TypeScript teaching repository.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Fastify; Node.js; React; Vite; infrastructure: GitHub Actions; testing: Vitest.
- **Review:** Substantial teaching app and tests; API repository adapters include in-memory storage. Static review only; not built, tested or run.
- **Learn:** TypeScript schemas, React reducers, validation, branching, tests
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Follow the fifteen-sprint sequence; add one field type with validation tests.
- **Evidence:** [README.md](../../formforge/README.md), [App.tsx](../../formforge/apps/web/src/App.tsx), [package.json](../../formforge/package.json).
- **Related versions/options:** [geminiorganized/General_Formforge](../../geminiorganized/General_Formforge). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### jobtrack

**Stage 2: Client apps and state. alternative.** [Open folder](../../jobtrack)

Daybook local-first calendar and job-application tracker.

- **Stack:** languages: HTML; JavaScript; frameworks: React; Vite; testing: Vitest.
- **Review:** Small Daybook app with tests; related concept to calendar+jobtrack but a separate implementation. Static review only; not built, tested or run.
- **Learn:** React state, local persistence, calendar and pipeline UX
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Add one reliable import/export or state-transition case.
- **Evidence:** [README.md](../../jobtrack/README.md), [App.jsx](../../jobtrack/src/App.jsx), [package.json](../../jobtrack/package.json).

#### lucasrouter

**Stage 2: Client apps and state. alternative.** [Open folder](../../lucasrouter)

Fleet and delivery-routing workspace with searchable stops, delivery status, and a driver interface.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; testing: Vitest.
- **Review:** Substantial Next.js demo with tests; README says historical Lighthouse figures are not current measurements. Static review only; not built, tested or run.
- **Learn:** Complex React state, maps, lazy loading, fleet UX
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Trace one stop status update and verify map/list/driver views agree.
- **Evidence:** [README.md](../../lucasrouter/README.md), [DriverRoutes.tsx](../../lucasrouter/src/components/dispatch/DriverRoutes.tsx), [package.json](../../lucasrouter/package.json).

#### recipeweb

**Stage 2: Client apps and state. Core route.** [Open folder](../../recipeweb)

A Filipino, Vietnamese, Thai & Spanish cookbook companion web app.

- **Stack:** CSS; HTML; JavaScript; TypeScript; React; Vite; GitHub Actions.
- **Review:** Static React cookbook with routing and shopping-list state. net/ contains planning documents for a .NET extension, not a backend implementation.
- **Learn:** Components, typed data, filters, context/local persistence and accessible list interactions.
- **Before starting:** JavaScript/TypeScript fundamentals, HTML/CSS and basic React.
- **Next:** Implement one shopping-list behavior and verify persistence/accessibility; use the net plan later as an API extension exercise.
- **Evidence:** [README.md](../../recipeweb/README.md), [App.tsx](../../recipeweb/src/App.tsx), [HomePage.tsx](../../recipeweb/src/pages/HomePage.tsx).
- **Related versions/options:** [geminiorganized/General_Recipeweb](../../geminiorganized/General_Recipeweb). Earlier catalog found matching multi-file samples with geminiorganized/General_Recipeweb; this is evidence of copies/versions, not a full-tree equality proof.

#### borrowbox

**Stage 3: APIs and SQL. .NET branch after the primary-stack capstone.** [Open folder](../../borrowbox)

BorrowBox is a beginner-friendly fifteen-sprint C#/.NET teaching repository for lending campus equipment such as laptops, cameras, calculators, and lab kits.

- **Stack:** languages: C#; SQL; frameworks: ASP.NET Core; data: Entity Framework Core; SQLite; infrastructure: GitHub Actions; testing: xUnit.
- **Review:** Beginner-focused teaching repository with source/tests. Default API storage is non-durable; SQLite is an adapter exercise. X-Demo-Role is a teaching header, not production authentication. Static review only; not built, tested or run.
- **Learn:** C# domain rules, minimal APIs, LINQ, DI, SQLite, tests
- **Before starting:** Language basics, HTTP/JSON, simple relational data and Git.
- **Next:** Follow the fifteen sprints; independently add a borrowing rule and its test.
- **Evidence:** [README.md](../../borrowbox/README.md), [Program.cs](../../borrowbox/src/BorrowBox.Api/Program.cs), [BorrowBox.Api.csproj](../../borrowbox/src/BorrowBox.Api/BorrowBox.Api.csproj).
- **Related versions/options:** [geminiorganized/General_Borrowbox](../../geminiorganized/General_Borrowbox). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### netsnapshot

**Stage 3: APIs and SQL. guided main-path reference.** [Open folder](../../netsnapshot)

NetAiOps is a simulated full-stack AI-powered IT operations platform built as a 15-step teaching history for a junior engineer.

- **Stack:** TypeScript; Node.js; React; teaching snapshots.
- **Review:** 15 full-copy chronological teaching snapshots of a simulated NetAiOps product. Sampled backend is TypeScript/Node and frontend React, despite .NET-sounding name.
- **Learn:** How a walking skeleton becomes CRUD, auth, service layers, tests and operational features.
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Start snapshots/00-walking-skeleton/NOTES.md; predict each change, compare adjacent copies, and recreate one increment in your own branch.
- **Evidence:** [README.md](../../netsnapshot/README.md), [server.ts](../../netsnapshot/snapshots/07-service-refactor/code/backend/src/server.ts), [App.tsx](../../netsnapshot/snapshots/07-service-refactor/code/frontend/src/app/App.tsx).
- **Related versions/options:** [geminiorganized/OpenSource_Upskilling_Snapshot](../../geminiorganized/OpenSource_Upskilling_Snapshot). Earlier catalog found matching multi-file samples with geminiorganized/OpenSource_Upskilling_Snapshot; this is evidence of copies/versions, not a full-tree equality proof.

#### netsnapshot1

**Stage 3: APIs and SQL. guided alternative to netsnapshot.** [Open folder](../../netsnapshot1)

Simulated fullstack teaching artifact for a TypeScript/Node backend and React frontend inspired by enterprise global workforce platforms.

- **Stack:** TypeScript; Node.js; React; teaching snapshots.
- **Review:** Chronological workforce-platform TypeScript/React teaching snapshots. Each snapshot is a full code copy, not a separate product to complete.
- **Learn:** Incremental development, domain modeling, auth context and service refactoring.
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Follow 00-walking-skeleton then implement one company workflow without copying its solution first.
- **Evidence:** [README.md](../../netsnapshot1/README.md), [App.tsx](../../netsnapshot1/snapshots/07-refactor-service-and-hooks/code/apps/web/src/App.tsx), [App.tsx](../../netsnapshot1/snapshots/02-backend-crud/code/apps/web/src/App.tsx).
- **Related versions/options:** [geminiorganized/OpenSource_Upskilling_Snapshot1](../../geminiorganized/OpenSource_Upskilling_Snapshot1). Earlier catalog found matching multi-file samples with geminiorganized/OpenSource_Upskilling_Snapshot1; this is evidence of copies/versions, not a full-tree equality proof.

#### newcodexJS

**Stage 3: APIs and SQL. Core route.** [Open folder](../../newcodexJS)

Progressive React/Express/Knex/PostgreSQL learning workspace containing 20 child apps.

- **Stack:** CSS; HTML; JavaScript; TypeScript; Express; Node.js; React; Vite; PostgreSQL.
- **Review:** 20 child React/Express/Knex/PostgreSQL apps. Maturity varies: 01 is small concrete CRUD; 05 includes JWT; several middle apps are generic scaffolds; 16-20 share admin CRUD patterns and titles overstate specialized capabilities.
- **Learn:** Progressive REST/SQL/client integration, then auth and business workflows.
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Begin 01-task-manager, then 05-recipe-manager; select one later domain challenge instead of completing all variants.
- **Evidence:** [README.md](../../newcodexJS/README.md), [App.jsx](../../newcodexJS/04-notes-app/client/src/App.jsx), [App.jsx](../../newcodexJS/01-task-manager/client/src/App.jsx).
- **Related versions/options:** [geminiorganized/General_Newcodexjs](../../geminiorganized/General_Newcodexjs). Earlier catalog found matching multi-file samples with geminiorganized/General_Newcodexjs; this is evidence of copies/versions, not a full-tree equality proof.

#### recipeview

**Stage 3: APIs and SQL. small full-stack alternative.** [Open folder](../../recipeview)

Local-first cooking journal organized as Dish, Recipe, and Cook Log, with SQLite persistence and photo uploads.

- **Stack:** CSS; HTML; SQL; TypeScript; Express; Node.js; React; Vite; SQLite (node:sqlite).
- **Review:** Local-first Recipe Lab application with React and Express source. server/db.ts uses Node node:sqlite DatabaseSync, transaction helper and search indexing.
- **Learn:** Relational modeling of dish/recipe/cook-log, SQL, file uploads and local-first UX.
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Trace creation of a recipe and cook log into SQLite, then test rollback and search-index consistency.
- **Evidence:** [README.md](../../recipeview/README.md), [index.ts](../../recipeview/server/index.ts), [App.tsx](../../recipeview/src/App.tsx).
- **Related versions/options:** [geminiorganized/General_Recipeview](../../geminiorganized/General_Recipeview). Earlier catalog found matching multi-file samples with geminiorganized/General_Recipeview; this is evidence of copies/versions, not a full-tree equality proof.

#### .netramp

**Stage 4: Integrated full-stack workflows. alternative.** [Open folder](../../.netramp)

A learning-oriented clone of Ramp / Expensify / Brex expense workflows, built with ASP.NET Core (C#) and React.

- **Stack:** languages: C#; CSS; HTML; JavaScript; frameworks: ASP.NET Core; React; Vite.
- **Review:** Teaching application with in-memory storage and no cataloged tests; README says source was not compiled in its generation environment. Static review only; not built, tested or run.
- **Learn:** Role-scoped expense workflows, state machines, uploads
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Persist one expense workflow and test approval transitions.
- **Evidence:** [README.md](../../.netramp/README.md), [App.jsx](../../.netramp/frontend/src/App.jsx), [package.json](../../.netramp/frontend/package.json).
- **Related versions/options:** [geminiorganized/OpenSource_Upskilling_.Ramp](../../geminiorganized/OpenSource_Upskilling_.Ramp). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### .nettodo

**Stage 4: Integrated full-stack workflows. reference.** [Open folder](../../.nettodo)

ASP.NET Core eShopOnWeb reference storefront demonstrating a monolithic web application.

- **Stack:** languages: C#; CSS; JavaScript; Razor; SCSS; frameworks: ASP.NET Core; Blazor; data: Entity Framework Core; SQL Server; infrastructure: Docker; GitHub Actions; testing: MSTest; xUnit.
- **Review:** eShopOnWeb upstream reference, not a todo app; README identifies successor repositories. Static review only; not built, tested or run.
- **Learn:** Layered ASP.NET application, EF Core, identity, storefronts
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Trace basket-to-order flow, then make one small tested change.
- **Evidence:** [README.md](../../.nettodo/eShopOnWeb/README.md), [Program.cs](../../.nettodo/eShopOnWeb/src/Web/Program.cs), [docker-compose.yml](../../.nettodo/eShopOnWeb/docker-compose.yml).
- **Related versions/options:** [geminiorganized/General_.Todo](../../geminiorganized/General_.Todo). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### gitjira-app

**Stage 4: Integrated full-stack workflows. main-path.** [Open folder](../../gitjira-app)

A Jira-style issue tracker, built in public as a teaching codebase — 15 sprints, each landing as one reviewed pull request full of learning artifacts. v1.0.0 .

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Express; Node.js; React; Vite; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Playwright; Vitest; integrations: BullMQ; Socket.IO.
- **Review:** Substantial Express/React teaching code and tests; README completion claim is not fresh runtime verification. Static review only; not built, tested or run.
- **Learn:** Full-stack issue tracking, auth, relational data, reviewable delivery
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Trace one issue request, fix one bug, and ship one independently explained feature.
- **Evidence:** [README.md](../../gitjira-app/README.md), [App.jsx](../../gitjira-app/apps/web/src/App.jsx), [package.json](../../gitjira-app/package.json).
- **Related versions/options:** [geminiorganized/General_Gitjira-App](../../geminiorganized/General_Gitjira-App). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### grokbuildecommerceproject

**Stage 4: Integrated full-stack workflows. alternative.** [Open folder](../../grokbuildecommerceproject)

A full-stack E-commerce Platform built for educational purposes to upskill to mid/senior SWE level.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Compact educational commerce slice with a few test files; breadth in docs exceeds what a sample proves. Static review only; not built, tested or run.
- **Learn:** React/API separation, cart/order rules, Prisma
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Complete and test one order flow before adding new domains.
- **Evidence:** [README.md](../../grokbuildecommerceproject/README.md), [App.tsx](../../grokbuildecommerceproject/frontend/src/App.tsx), [docker-compose.yml](../../grokbuildecommerceproject/docker-compose.yml).
- **Related versions/options:** [geminiorganized/LLM_Generated_Ecommerceproject](../../geminiorganized/LLM_Generated_Ecommerceproject). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### grokbuildhrproject

**Stage 4: Integrated full-stack workflows. alternative.** [Open folder](../../grokbuildhrproject)

Full-stack HR / People Operations Platform (Educational)

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Jest; Vitest.
- **Review:** Small Express/React/Prisma teaching implementation; advanced production claims are aspirational. Static review only; not built, tested or run.
- **Learn:** Employee data, leave workflows, pagination, RBAC
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Trace one leave request and test authorization.
- **Evidence:** [README.md](../../grokbuildhrproject/README.md), [App.tsx](../../grokbuildhrproject/frontend/src/App.tsx), [docker-compose.yml](../../grokbuildhrproject/docker-compose.yml).

#### grokbuildppmproject

**Stage 4: Integrated full-stack workflows. alternative.** [Open folder](../../grokbuildppmproject)

Project-portfolio management practice app with portfolios, programs, projects, and tasks.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Compact portfolio/project/task teaching app with tests; not a full enterprise PPM implementation. Static review only; not built, tested or run.
- **Learn:** Hierarchical domain models, relationships, permissions
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Add one hierarchy constraint and test an invalid relationship.
- **Evidence:** [README.md](../../grokbuildppmproject/README.md), [App.tsx](../../grokbuildppmproject/frontend/src/App.tsx), [docker-compose.yml](../../grokbuildppmproject/docker-compose.yml).

#### grokbuildsupportproject

**Stage 4: Integrated full-stack workflows. deferred-spec.** [Open folder](../../grokbuildsupportproject)

Full-stack Customer Support Ticketing + Knowledge Base Platform

- **Stack:** .
- **Review:** Documentation-only in inventory: no source or test files, despite full-stack wording in README. Static review only; not built, tested or run.
- **Learn:** Support domain modeling, API planning, ticket workflows
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Use the specification only if choosing to build a support vertical slice.
- **Evidence:** [README.md](../../grokbuildsupportproject/README.md).

#### grokbuildteamproject

**Stage 4: Integrated full-stack workflows. alternative.** [Open folder](../../grokbuildteamproject)

A full-stack Team / Project Management application built for educational purposes.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Jest; Vitest.
- **Review:** Compact educational full-stack app; overlaps many issue/project trackers. Static review only; not built, tested or run.
- **Learn:** Teams, project CRUD, JWT, validation, relational data
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Test one team-scoped API and its React loading/error states.
- **Evidence:** [README.md](../../grokbuildteamproject/README.md), [App.tsx](../../grokbuildteamproject/frontend/src/App.tsx), [docker-compose.yml](../../grokbuildteamproject/docker-compose.yml).

#### netlinear

**Stage 4: Integrated full-stack workflows. .NET main-path candidate.** [Open folder](../../netlinear)

NetLinear is a Linear/Jira-style issue tracker scaffold built with .NET 8, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Stack:** C#; CSS; HTML; TypeScript; ASP.NET Core; React; Vite; Entity Framework Core; PostgreSQL; Redis; Docker; GitHub Actions; xUnit.
- **Review:** Issue-tracker scaffold with workflow/concurrency code. Auth is explicitly a fixed demo-user dev-login endpoint; frontend obtains it automatically.
- **Learn:** REST, EF Core, filtered queries, optimistic mutations, xmin concurrency and workflow transitions.
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Complete an issue CRUD slice, then replace demo identity with authenticated users and prove stale-write conflict handling.
- **Evidence:** [README.md](../../netlinear/README.md), [AuthController.cs](../../netlinear/src/NetLinear.Api/Controllers/AuthController.cs), [IssuesController.cs](../../netlinear/src/NetLinear.Api/Controllers/IssuesController.cs).
- **Related versions/options:** [geminiorganized/OpenSource_Upskilling_Linear](../../geminiorganized/OpenSource_Upskilling_Linear). Earlier catalog found matching multi-file samples with geminiorganized/OpenSource_Upskilling_Linear; this is evidence of copies/versions, not a full-tree equality proof.

#### .netstripe

**Stage 5: Domain rules and reliability. alternative.** [Open folder](../../.netstripe)

A learning-oriented Stripe Billing / Chargebee style dashboard built with C#, .NET minimal APIs, and React.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite.
- **Review:** Compact billing simulation; in-memory stores and workers are not durable payment infrastructure. Static review only; not built, tested or run.
- **Learn:** Money, idempotency, background payments, signed webhooks
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Test duplicate payment requests and then persist idempotency state.
- **Evidence:** [README.md](../../.netstripe/README.md), [Program.cs](../../.netstripe/src/Billing.Api/Program.cs), [package.json](../../.netstripe/src/Billing.Web/package.json).
- **Related versions/options:** [geminiorganized/OpenSource_Upskilling_.Stripe](../../geminiorganized/OpenSource_Upskilling_.Stripe). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### campusops

**Stage 5: Domain rules and reliability. .NET branch after the primary-stack capstone.** [Open folder](../../campusops)

CampusOps is a fifteen-sprint teaching repository for learning business-heavy C#/.NET API development and React/TypeScript integration through a university facilities platform.

- **Stack:** languages: C#; CSS; HTML; SQL; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; SQLite; infrastructure: GitHub Actions; testing: Vitest; xUnit.
- **Review:** Fifteen-sprint .NET/React teaching repository. Default API storage is non-durable. X-Demo-Role and X-Demo-Campus are client-supplied teaching authentication headers; policy rejection is not proof of real identity. SQLite adapters are exercises. Static review only; not built, tested or run.
- **Learn:** Business API workflows, React integration, persistence, operations
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** After BorrowBox, implement one facilities workflow end to end with tests.
- **Evidence:** [README.md](../../campusops/README.md), [Program.cs](../../campusops/src/CampusOps.Api/Program.cs), [package.json](../../campusops/web/CampusOps.Web/package.json).
- **Related versions/options:** [geminiorganized/General_Campusops](../../geminiorganized/General_Campusops). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### globehire

**Stage 5: Domain rules and reliability. alternative.** [Open folder](../../globehire)

GlobeHire is a fifteen-sprint C#/.NET teaching repository for a fictional global workforce and employer-of-record platform.

- **Stack:** languages: C#; frameworks: ASP.NET Core; infrastructure: GitHub Actions; testing: xUnit.
- **Review:** Teaching system defaults to volatile in-memory storage and explicitly has no real authentication. Workforce rules are synthetic; curriculum completion does not mean deployable software. Static review only; not built, tested or run.
- **Learn:** Versioned rules, lifecycle changes, integration ports, API contracts
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** After CampusOps, change one fictional country rule without breaking API contracts.
- **Evidence:** [README.md](../../globehire/README.md), [Program.cs](../../globehire/src/GlobeHire.Api/Program.cs), [GlobeHire.Api.csproj](../../globehire/src/GlobeHire.Api/GlobeHire.Api.csproj).
- **Related versions/options:** [geminiorganized/General_Globehire](../../geminiorganized/General_Globehire). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### grokbuildmultitenantproject

**Stage 5: Domain rules and reliability. alternative.** [Open folder](../../grokbuildmultitenantproject)

A full-stack Multi-Tenant SaaS Starter built for educational purposes to upskill to mid/senior SWE level.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Vite; data: Prisma; infrastructure: Docker.
- **Review:** Compact multi-tenant teaching implementation with only a few cataloged test files. Static review only; not built, tested or run.
- **Learn:** Tenant isolation, organization roles, scoped queries
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Add a test proving one tenant cannot access another tenant's project.
- **Evidence:** [README.md](../../grokbuildmultitenantproject/README.md), [App.tsx](../../grokbuildmultitenantproject/frontend/src/App.tsx), [docker-compose.yml](../../grokbuildmultitenantproject/docker-compose.yml).

#### grokbuildorderproject

**Stage 5: Domain rules and reliability. alternative.** [Open folder](../../grokbuildorderproject)

Full-stack Order Management / Operations Platform (Educational)

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Jest; Vitest.
- **Review:** Small educational order-system slice; verify workflow completeness from source before expanding it. Static review only; not built, tested or run.
- **Learn:** Inventory, order transitions, transactional integrity
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Trace one inventory update and test rollback on failure.
- **Evidence:** [README.md](../../grokbuildorderproject/README.md), [App.tsx](../../grokbuildorderproject/frontend/src/App.tsx), [docker-compose.yml](../../grokbuildorderproject/docker-compose.yml).

#### meterforge

**Stage 5: Domain rules and reliability. .NET branch after the primary-stack capstone.** [Open folder](../../meterforge)

MeterForge is a fifteen-sprint C#/.NET teaching repository for a fictional multi-tenant usage-based subscription billing platform.

- **Stack:** languages: C#; SQL; frameworks: ASP.NET Core; data: PostgreSQL; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Substantial fifteen-sprint source/tests. Default runtime uses non-durable in-memory adapters; README explicitly excludes production auth, migration runner, telemetry backend and operated restore. Static review only; not built, tested or run.
- **Learn:** Money invariants, idempotency, concurrency, outbox, integrations
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** After CampusOps, prove duplicate usage does not double bill, then use a durable adapter.
- **Evidence:** [README.md](../../meterforge/README.md), [Program.cs](../../meterforge/src/MeterForge.Api/Program.cs), [docker-compose.yml](../../meterforge/docker-compose.yml).
- **Related versions/options:** [geminiorganized/General_Meterforge](../../geminiorganized/General_Meterforge). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### netdocu

**Stage 5: Domain rules and reliability. workflow alternative.** [Open folder](../../netdocu)

NetDocu is a DocuSign-style signing workflow application with a .NET 8 clean-architecture API, PostgreSQL persistence, JWT/refresh-token auth, and a React + TypeScript signing workspace.

- **Stack:** C#; CSS; HTML; JavaScript; TypeScript; ASP.NET Core; React; Vite; Entity Framework Core; PostgreSQL; Redis; Docker; GitHub Actions; xUnit.
- **Review:** Layered signing-workflow application with document/auth controllers, React workspace and test projects. Static inspection confirms application structure, not completed signing fidelity or deployed integrations.
- **Learn:** Document permissions, workflow state transitions, audit events, background processing.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Trace document creation to envelope completion; verify one unauthorized recipient and duplicate submission scenario.
- **Evidence:** [README.md](../../netdocu/README.md), [AuthController.cs](../../netdocu/src/NetDocu.Api/Controllers/AuthController.cs), [DocumentsController.cs](../../netdocu/src/NetDocu.Api/Controllers/DocumentsController.cs).
- **Related versions/options:** [geminiorganized/OpenSource_Upskilling_Docu](../../geminiorganized/OpenSource_Upskilling_Docu). Earlier catalog found matching multi-file samples with geminiorganized/OpenSource_Upskilling_Docu; this is evidence of copies/versions, not a full-tree equality proof.

#### netnotion

**Stage 5: Domain rules and reliability. content workflow alternative.** [Open folder](../../netnotion)

NetNotion is a Notion-style collaborative docs/wiki app built with .NET 8 Web API, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Stack:** C#; CSS; HTML; TypeScript; ASP.NET Core; React; Vite; Entity Framework Core; PostgreSQL; Redis; Docker; GitHub Actions; xUnit.
- **Review:** Collaborative-docs learning app with page/version/share controllers. README explicitly excludes realtime presence, templates and export stretch features.
- **Learn:** Recursive page trees, inherited permissions, block batching and immutable versions.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Trace page sharing and version restore; add an inherited-permission regression and reject tree cycles.
- **Evidence:** [README.md](../../netnotion/README.md), [AuthController.cs](../../netnotion/src/NetNotion.Api/Controllers/AuthController.cs), [PagesController.cs](../../netnotion/src/NetNotion.Api/Controllers/PagesController.cs).
- **Related versions/options:** [geminiorganized/OpenSource_Upskilling_Notion](../../geminiorganized/OpenSource_Upskilling_Notion). Earlier catalog found matching multi-file samples with geminiorganized/OpenSource_Upskilling_Notion; this is evidence of copies/versions, not a full-tree equality proof.

#### netshop

**Stage 5: Domain rules and reliability. .NET workflow main-path candidate.** [Open folder](../../netshop)

NetShopifyLite is a .NET 8 + React ecommerce admin and lightweight storefront scaffold.

- **Stack:** C#; CSS; HTML; TypeScript; ASP.NET Core; React; Vite; Entity Framework Core; PostgreSQL; Redis; Docker; GitHub Actions; xUnit.
- **Review:** Ecommerce learning scaffold with order/auth controllers, idempotency contracts and domain state transitions. Payment provider is fake; integration tests are described as a skeleton.
- **Learn:** Money modeling, transactional inventory, idempotent checkout/refunds and domain invariants.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Prove duplicate checkout/refund behavior and stock consistency with a real persistence integration test.
- **Evidence:** [README.md](../../netshop/README.md), [AuthController.cs](../../netshop/src/NetShopifyLite.Api/Controllers/AuthController.cs), [OrdersController.cs](../../netshop/src/NetShopifyLite.Api/Controllers/OrdersController.cs).
- **Related versions/options:** [geminiorganized/OpenSource_Upskilling_Shop](../../geminiorganized/OpenSource_Upskilling_Shop). Earlier catalog found matching multi-file samples with geminiorganized/OpenSource_Upskilling_Shop; this is evidence of copies/versions, not a full-tree equality proof.

#### newcodecjs2

**Stage 5: Domain rules and reliability. reference bundle.** [Open folder](../../newcodecjs2)

Five focused SaaS architecture learning scaffolds: Planr, Bookr, Payr, Blockr and Helpkit.

- **Stack:** TypeScript; Next.js; Node.js; React; Vite; Drizzle; Vitest.
- **Review:** Five architecture-oriented SaaS learning scaffolds. Root README explicitly says they are not wired for installation/deployment; sampled routes are plain functions over in-memory stores.
- **Learn:** Focused domain algorithms, policy checks, optimistic state and integration boundaries.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Choose one child by missing skill and turn one domain behavior into an independently verified vertical slice.
- **Evidence:** [README.md](../../newcodecjs2/README.md), [routes.ts](../../newcodecjs2/payr/src/server/routes.ts), [package.json](../../newcodecjs2/blockr/package.json).
- **Related versions/options:** [geminiorganized/General_Newcodecjs2](../../geminiorganized/General_Newcodecjs2). Earlier catalog found matching multi-file samples with geminiorganized/General_Newcodecjs2; this is evidence of copies/versions, not a full-tree equality proof.

#### newcodex3

**Stage 5: Domain rules and reliability. reference bundle.** [Open folder](../../newcodex3)

Learning workspace with 25 software topics numbered 16-40, each in TypeScript/React and .NET/React variants (50 child apps).

- **Stack:** C#; CSS; HTML; TypeScript; Express; Node.js; React; Vite; Prisma; Redis; Vitest.
- **Review:** 50 child learning apps: 25 topics numbered 16-40 in TypeScript and .NET variants. Root five-project/title wording is stale. Many .NET and later TS versions use in-memory collections; architecture prose is not proof of durable services.
- **Learn:** Compare equivalent domain patterns across TypeScript and C#; study one difficult invariant at a time.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Choose one topic and one language implementation; document gaps between scaffold code and production notes before extending it.
- **Evidence:** [README.md](../../newcodex3/README.md), [Program.cs](../../newcodex3/apps/27-ats-lite-net/server/Program.cs), [Program.cs](../../newcodex3/apps/18-team-chat-net/server/Program.cs).
- **Related versions/options:** [geminiorganized/General_Newcodex3](../../geminiorganized/General_Newcodex3). Earlier catalog found matching multi-file samples with geminiorganized/General_Newcodex3; this is evidence of copies/versions, not a full-tree equality proof.

#### perch

**Stage 5: Domain rules and reliability. workflow main-path candidate.** [Open folder](../../perch)

Perch is a Greenhouse/Lever-style applicant tracking system and a teaching repository for junior engineers.

- **Stack:** CSS; HTML; JavaScript; TypeScript; Fastify; Node.js; React; Vite; Prisma; GitHub Actions; Vitest.
- **Review:** Substantial teaching ATS with Fastify routes, React UI, pure domain tests and repository interfaces. Deterministic in-memory adapters are active; Prisma/Postgres production model and external provider intent boundaries remain separate.
- **Learn:** Multi-actor workflow, object authorization, state machines, bulk actions, ports/adapters and test design.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Follow one sprint playbook and implement a persistent repository adapter while retaining the authorization tests.
- **Evidence:** [README.md](../../perch/README.md), [app.ts](../../perch/apps/api/src/app.ts), [index.ts](../../perch/packages/db/src/index.ts).
- **Related versions/options:** [geminiorganized/General_Perch](../../geminiorganized/General_Perch). Earlier catalog found matching multi-file samples with geminiorganized/General_Perch; this is evidence of copies/versions, not a full-tree equality proof.

#### skillforgejs

**Stage 5: Domain rules and reliability. Next.js full-stack alternative.** [Open folder](../../skillforgejs)

Skillforge is a web-first coding-skills learning platform built with Next.js App Router, TypeScript, Prisma/PostgreSQL, Auth.js, Tailwind, CodeMirror, server-side spaced repetition, and gamification.

- **Stack:** CSS; JavaScript; SQL; TypeScript; Next.js; Node.js; React; Tailwind CSS; Prisma; Docker; GitHub Actions; Playwright; Vitest.
- **Review:** Substantial Next.js learning platform source with catalog server rendering, auth/data models, spaced-repetition modules, content validation and unit/E2E test configuration. Catalog content and runtime were not executed.
- **Learn:** App Router/server boundaries, Prisma, content schema validation, pure scheduling logic and tests.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Trace lesson completion into review state and add a deterministic scheduler/transaction test.
- **Evidence:** [README.md](../../skillforgejs/README.md), [page.tsx](../../skillforgejs/src/app/page.tsx), [layout.tsx](../../skillforgejs/src/app/layout.tsx).
- **Related versions/options:** [geminiorganized/General_Skillforgejs](../../geminiorganized/General_Skillforgejs). Earlier catalog found matching multi-file samples with geminiorganized/General_Skillforgejs; this is evidence of copies/versions, not a full-tree equality proof.

#### .netarchitectureproject

**Stage 6: Architecture and advanced integrations. .NET branch reference, after a working project.** [Open folder](../../.netarchitectureproject)

Full Modular Monolith .NET application with Domain-Driven Design approach.

- **Stack:** languages: C#; HTML; SQL; frameworks: ASP.NET Core; data: SQL Server; infrastructure: Docker; GitHub Actions.
- **Review:** Large upstream reference with source and tests. The old catalog's unfinished/authentication caveat misquotes a discussion of OTHER examples. Static review only; not built, tested or run.
- **Learn:** DDD boundaries, domain events, modular monoliths
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Trace one meeting command across module boundaries and explain its transaction.
- **Evidence:** [README.md](../../.netarchitectureproject/modular-monolith-with-ddd/README.md), [Program.cs](../../.netarchitectureproject/modular-monolith-with-ddd/src/Database/DatabaseMigrator/Program.cs), [docker-compose.yml](../../.netarchitectureproject/modular-monolith-with-ddd/docker-compose.yml).
- **Related versions/options:** [geminiorganized/General_.Architectureproject](../../geminiorganized/General_.Architectureproject). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### .netopen2

**Stage 6: Architecture and advanced integrations. reference.** [Open folder](../../.netopen2)

Orchard Core is an open-source, modular, multi-tenant application framework and CMS for ASP.NET Core.

- **Stack:** languages: C#; CSS; HTML; JavaScript; Razor; SCSS; TypeScript; frameworks: ASP.NET Core; Vite; Vue; infrastructure: Docker; GitHub Actions; testing: Moq; xUnit.
- **Review:** Large upstream Orchard Core checkout; useful after API fundamentals, not a beginner build target. Static review only; not built, tested or run.
- **Learn:** Extensible CMS, tenants, dependency injection, mature code navigation
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Study one small module and propose one bounded fix.
- **Evidence:** [README.md](../../.netopen2/OrchardCore/README.md), [Program.cs](../../.netopen2/OrchardCore/src/OrchardCore.Cms.Web/Program.cs), [package.json](../../.netopen2/OrchardCore/package.json).
- **Related versions/options:** [geminiorganized/General_.Open2](../../geminiorganized/General_.Open2). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### astra1

**Stage 6: Architecture and advanced integrations. capstone.** [Open folder](../../astra1)

A persistent station and enterprise operations simulation for practicing AI-assisted engineering.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; data: PostgreSQL; infrastructure: Docker; GitHub Actions; testing: Playwright.
- **Review:** Broad operations simulation with app and test code; simulated providers remain simulations. Static review only; not built, tested or run.
- **Learn:** Operational workflows, telemetry, durable jobs, failure recovery
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Finish one incident-to-remediation slice and explain failure recovery.
- **Evidence:** [README.md](../../astra1/README.md), [instrumentation.ts](../../astra1/src/instrumentation.ts), [package.json](../../astra1/package.json).

#### buildevent

**Stage 6: Architecture and advanced integrations. alternative.** [Open folder](../../buildevent)

TypeScript monorepo for a ticketing platform with a Next.js frontend, Fastify API, Prisma/PostgreSQL data layer, Redis-backed jobs, Stripe checkout hooks, signed QR tickets, and mobile check-in.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Fastify; Next.js; Node.js; React; Tailwind CSS; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Vitest; integrations: BullMQ; Stripe.
- **Review:** Full-stack source with external service seams; only one cataloged test file, no integration runtime verification. Static review only; not built, tested or run.
- **Learn:** Ticket inventory, checkout hooks, queues, signed QR check-in
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Test duplicate checkout and repeat check-in behavior.
- **Evidence:** [README.md](../../buildevent/README.md), [server.ts](../../buildevent/apps/api/src/server.ts), [package.json](../../buildevent/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Buildevent](../../geminiorganized/LLM_Generated_Buildevent). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### buildreviewer

**Stage 6: Architecture and advanced integrations. alternative.** [Open folder](../../buildreviewer)

A web-based code-review workspace for GitHub pull requests, inspired by ReviewFlow.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: NestJS; Node.js; React; Tailwind CSS; Vite; data: Prisma; testing: Jest; Vitest.
- **Review:** NestJS/React review workspace with tests; GitHub publication integration unverified. Static review only; not built, tested or run.
- **Learn:** GitHub APIs, local drafts, transactional publishing, review UX
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Trace local draft persistence and implement a failed-publish recovery case.
- **Evidence:** [README.md](../../buildreviewer/README.md), [Review.tsx](../../buildreviewer/apps/web/src/routes/Review.tsx), [package.json](../../buildreviewer/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Buildreviewer](../../geminiorganized/LLM_Generated_Buildreviewer). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### masternocu

**Stage 6: Architecture and advanced integrations. reference.** [Open folder](../../masternocu)

NocoBase extensible low-code application platform.

- **Stack:** languages: CSS; HTML; JavaScript; SCSS; SQL; TypeScript; frameworks: React; data: MySQL; PostgreSQL; infrastructure: Docker; GitHub Actions; testing: Vitest; integrations: LangChain.
- **Review:** Large NocoBase upstream checkout with many tests; advanced reference despite old unknown label. Static review only; not built, tested or run.
- **Learn:** Plugin architecture, schemas, permissions, large codebases
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Study one small plugin after owning a full-stack app.
- **Evidence:** [README.md](../../masternocu/nocobase/README.md), [server.ts](../../masternocu/nocobase/packages/plugins/%40nocobase/plugin-error-handler/src/server/server.ts), [package.json](../../masternocu/nocobase/package.json).
- **Related versions/options:** [geminiorganized/General_Masternocu](../../geminiorganized/General_Masternocu). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### missioncontrol

**Stage 6: Architecture and advanced integrations. alternative.** [Open folder](../../missioncontrol)

A self-hosted control plane for fleets of AI agents — a C# / .NET 10 recreation of builderz-labs/mission-control per the Fleet Command — C# / .NET Technical Specification.

- **Stack:** languages: C#; CSS; Razor; frameworks: ASP.NET Core; data: Entity Framework Core; SQLite; testing: xUnit.
- **Review:** README states only roadmap phases 1-4 core of 8 are implemented; source is a partial control plane. Static review only; not built, tested or run.
- **Learn:** Agent control-plane APIs, auth, EF Core, scheduling
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Trace task claim concurrency and test two workers claiming one task.
- **Evidence:** [README.md](../../missioncontrol/README.md), [Program.cs](../../missioncontrol/src/FleetCommand.Host/Program.cs), [FleetCommand.Contracts.csproj](../../missioncontrol/src/FleetCommand.Contracts/FleetCommand.Contracts.csproj).
- **Related versions/options:** [geminiorganized/General_Missioncontrol](../../geminiorganized/General_Missioncontrol). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### netauth

**Stage 6: Architecture and advanced integrations. security specialization.** [Open folder](../../netauth)

Standalone identity provider for learning OAuth2/OIDC, JWT signing, refresh-token rotation, RBAC, MFA, and audit logging.

- **Stack:** C#; CSS; HTML; TypeScript; ASP.NET Core; React; Vite; Entity Framework Core; PostgreSQL; Redis; Docker; GitHub Actions; xUnit.
- **Review:** Educational identity-provider implementation with OAuth/OIDC controllers and MFA/session models. Authorize controller visibly accepts query user_id; authentication/consent safety needs focused review before treating this as an identity template.
- **Learn:** OAuth grants, PKCE, token rotation/replay, signing keys, resource authorization.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Follow one authorization-code exchange and write a threat model plus negative tests around identity binding and replay.
- **Evidence:** [README.md](../../netauth/README.md), [AuthController.cs](../../netauth/src/NetAuth0.Api/Controllers/AuthController.cs), [OAuthController.cs](../../netauth/src/NetAuth0.Api/Controllers/OAuthController.cs).
- **Related versions/options:** [geminiorganized/OpenSource_Upskilling_Auth](../../geminiorganized/OpenSource_Upskilling_Auth). Earlier catalog found matching multi-file samples with geminiorganized/OpenSource_Upskilling_Auth; this is evidence of copies/versions, not a full-tree equality proof.

#### netcleanarch

**Stage 6: Architecture and advanced integrations. .NET branch reference, after a working project.** [Open folder](../../netcleanarch)

ASP.NET Core Clean Architecture starter/reference application.

- **Stack:** C#; HTML; JavaScript; SCSS; TypeScript; ASP.NET Core; Entity Framework Core; PostgreSQL; SQL Server; SQLite; GitHub Actions; Moq; NUnit.
- **Review:** Upstream Clean Architecture solution template; current local README targets .NET 10 and Aspire. User identity endpoint and multiple test-layer projects exist.
- **Learn:** Dependency boundaries, CQRS, integration testing, architecture tradeoffs.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Compare one simple endpoint and handler against your own completed CRUD app; adopt only a justified pattern.
- **Evidence:** [README.md](../../netcleanarch/CleanArchitecture/README.md), [Users.cs](../../netcleanarch/CleanArchitecture/src/Web/Endpoints/Users.cs), [App.jsx](../../netcleanarch/CleanArchitecture/src/Web/ClientApp-React/src/App.jsx).
- **Related versions/options:** [geminiorganized/General_Cleanarch](../../geminiorganized/General_Cleanarch). Earlier catalog found matching multi-file samples with geminiorganized/General_Cleanarch; this is evidence of copies/versions, not a full-tree equality proof.

#### netdrop

**Stage 6: Architecture and advanced integrations. storage specialization.** [Open folder](../../netdrop)

Personal/team cloud storage built with .NET 8 Web API, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Stack:** C#; CSS; HTML; JavaScript; TypeScript; ASP.NET Core; React; Vite; Entity Framework Core; PostgreSQL; Redis; Docker; GitHub Actions; xUnit.
- **Review:** Substantial cloud-storage learning app with owner-scoped file service and upload/storage abstractions. README describes resumable chunks, content hashing and queued scans; scanning is explicitly simulated.
- **Learn:** File metadata versus blobs, quotas, resumability, checksums, async processing.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Trace an interrupted upload through resume, finalization and quota accounting; add failure/retry tests.
- **Evidence:** [README.md](../../netdrop/README.md), [AuthController.cs](../../netdrop/src/NetDropbox.Api/Controllers/AuthController.cs), [FilesController.cs](../../netdrop/src/NetDropbox.Api/Controllers/FilesController.cs).
- **Related versions/options:** [geminiorganized/OpenSource_Upskilling_Drop](../../geminiorganized/OpenSource_Upskilling_Drop). Earlier catalog found matching multi-file samples with geminiorganized/OpenSource_Upskilling_Drop; this is evidence of copies/versions, not a full-tree equality proof.

#### netopen1

**Stage 6: Architecture and advanced integrations. upstream architecture reference.** [Open folder](../../netopen1)

A reference .NET application implementing an e-commerce website using a services-based architecture using .NET Aspire.

- **Stack:** C#; CSS; HTML; JavaScript; Python; Razor; TypeScript; ASP.NET Core; Blazor; Entity Framework Core; PostgreSQL; GitHub Actions; Playwright.
- **Review:** Local upstream eShop reference application; README identifies .NET 9, Aspire and service-based commerce. Identity API and service/test roots are present.
- **Learn:** Service boundaries, distributed workflows, integration events and observability.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Follow checkout across services and diagram failure/retry boundaries after completing a monolith first.
- **Evidence:** [README.md](../../netopen1/eShop/README.md), [Program.cs](../../netopen1/eShop/src/Identity.API/Program.cs), [Program.cs](../../netopen1/eShop/src/Ordering.API/Program.cs).

#### netopen3

**Stage 6: Architecture and advanced integrations. upstream CMS reference.** [Open folder](../../netopen3)

Umbraco content management system and its administration interface.

- **Stack:** C#; ASP.NET Core; TypeScript; web components; Vite; SQL Server/SQLite persistence projects; Playwright.
- **Review:** Substantial upstream Umbraco CMS source with .NET Management API and TypeScript web-component backoffice. Earlier catalog Next.js/unknown label is misleading for the core product.
- **Learn:** Large-repo navigation, extension architecture, management APIs, content caching and testing.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Select one management endpoint or backoffice component and trace its tests; scope a small contribution.
- **Evidence:** [README.md](../../netopen3/Umbraco-CMS/.github/README.md), [Program.cs](../../netopen3/Umbraco-CMS/src/Umbraco.Web.UI/Program.cs), [Umbraco.Cms.Api.Management.csproj](../../netopen3/Umbraco-CMS/src/Umbraco.Cms.Api.Management/Umbraco.Cms.Api.Management.csproj).
- **Related versions/options:** [geminiorganized/General_Open3](../../geminiorganized/General_Open3). Earlier catalog found matching multi-file samples with geminiorganized/General_Open3; this is evidence of copies/versions, not a full-tree equality proof.

#### nopsolutionsnet

**Stage 6: Architecture and advanced integrations. upstream commerce reference.** [Open folder](../../nopsolutionsnet)

nopCommerce ecommerce application with storefront, administration, and plugins.

- **Stack:** C#; CSS; HTML; JavaScript; Razor; SQL; Express; PostgreSQL; SQL Server; Docker; GitHub Actions.
- **Review:** Local upstream nopCommerce source: ASP.NET Core storefront/admin with service libraries, plugins and tests. Local README describes .NET 9.
- **Learn:** Large modular commerce application, plugin boundaries and order lifecycle.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Trace a single order service method and its callers/tests; compare it with the smaller netshop domain.
- **Evidence:** [README.md](../../nopsolutionsnet/nopCommerce/README.md), [OrderService.cs](../../nopsolutionsnet/nopCommerce/src/Libraries/Nop.Services/Orders/OrderService.cs), [Program.cs](../../nopsolutionsnet/nopCommerce/src/Presentation/Nop.Web/Program.cs).
- **Related versions/options:** [geminiorganized/General_Nopsolutions](../../geminiorganized/General_Nopsolutions). Earlier catalog found matching multi-file samples with geminiorganized/General_Nopsolutions; this is evidence of copies/versions, not a full-tree equality proof.

#### aiapplybot

**Stage 7: Specializations. specialization.** [Open folder](../../aiapplybot)

AI-assisted job application filler for company career sites (Greenhouse, Lever, Ashby, Workday, and custom forms).

- **Stack:** languages: Python; testing: Playwright; integrations: Anthropic API; OpenAI API.
- **Review:** Small Python application with source; browser/provider integration remains unverified. Static review only; not built, tested or run.
- **Learn:** Python browser automation, form extraction, LLM integration
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Test mapping against a local synthetic form before live sites.
- **Evidence:** [README.md](../../aiapplybot/README.md), [ats.py](../../aiapplybot/applybot/ats.py), [requirements.txt](../../aiapplybot/requirements.txt).
- **Related versions/options:** [geminiorganized/LLM_Generated_Applybot](../../geminiorganized/LLM_Generated_Applybot). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### aicallhelper

**Stage 7: Specializations. alternative.** [Open folder](../../aicallhelper)

A push-to-record interview copilot for Windows.

- **Stack:** languages: CSS; HTML; Rust; TypeScript; frameworks: React; Vite; testing: Vitest.
- **Review:** Substantial desktop/UI source and test files; frontend mock bridge is not proof of native capture. Static review only; not built, tested or run.
- **Learn:** Desktop audio streams, typed event bridges, UI state
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace recording cancellation and test event-order races.
- **Evidence:** [README.md](../../aicallhelper/README.md), [App.tsx](../../aicallhelper/src/App.tsx), [package.json](../../aicallhelper/package.json).

#### aicallhelper2

**Stage 7: Specializations. alternative.** [Open folder](../../aicallhelper2)

A push-to-record interview copilot for Windows.

- **Stack:** languages: CSS; HTML; Python; TypeScript; frameworks: React; Vite; infrastructure: GitHub Actions; testing: Vitest.
- **Review:** Substantive implementation and tests despite old unknown label; native behavior unverified. Static review only; not built, tested or run.
- **Learn:** Audio pipeline state, desktop IPC, recovery
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Compare one recording flow with aicallhelper and choose one maintained variant.
- **Evidence:** [README.md](../../aicallhelper2/README.md), [App.tsx](../../aicallhelper2/frontend/src/App.tsx), [pyproject.toml](../../aicallhelper2/pyproject.toml).

#### aiheartbeat

**Stage 7: Specializations. specialization.** [Open folder](../../aiheartbeat)

Pulse is a locally-run agentic loop.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; testing: Vitest.
- **Review:** Node daemon and dashboard source exist; requires its local agent CLI setup. Static review only; not built, tested or run.
- **Learn:** Agent scheduling, ticket memory, SQLite, failure recovery
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace one ticket through daemon wakeup, execution, and recovery.
- **Evidence:** [README.md](../../aiheartbeat/README.md), [cli.ts](../../aiheartbeat/packages/core/src/cli.ts), [package.json](../../aiheartbeat/package.json).

#### aihelper

**Stage 7: Specializations. alternative.** [Open folder](../../aihelper)

A Windows desktop app (Electron) that helps you answer questions during your own live calls and interviews.

- **Stack:** languages: CSS; HTML; JavaScript; frameworks: Electron.
- **Review:** Small Electron implementation with tests; service and native audio behavior unverified. Static review only; not built, tested or run.
- **Learn:** Electron IPC, audio transcription, streamed responses
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Explain preload isolation and handle one failed provider request.
- **Evidence:** [README.md](../../aihelper/README.md), [preload.js](../../aihelper/src/preload.js), [package.json](../../aihelper/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Helper](../../geminiorganized/LLM_Generated_Helper). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### aral

**Stage 7: Specializations. specialization.** [Open folder](../../aral)

React PWA language-learning app with client-side SQLite, a progress-event log, and a thin synchronization backend.

- **Stack:** languages: CSS; HTML; Java; JavaScript; SQL; TypeScript; frameworks: Hono; Node.js; React; Tailwind CSS; Vite; data: Drizzle; testing: Vitest.
- **Review:** PWA/Capacitor monorepo with source and tests; sync service and mobile behavior unverified. Static review only; not built, tested or run.
- **Learn:** Offline SQLite, event logs, synchronization, shared schemas
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace one progress event from device storage to sync and rebuilt state.
- **Evidence:** [README.md](../../aral/README.md), [App.tsx](../../aral/packages/app/src/App.tsx), [package.json](../../aral/package.json).
- **Related versions/options:** [geminiorganized/General_Aral](../../geminiorganized/General_Aral). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### astra2

**Stage 7: Specializations. specialization.** [Open folder](../../astra2)

A playable 3D archipelago colony and maritime trade simulator, built with TypeScript, JavaScript, Three.js, Vite, HTML and CSS.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Vite; testing: Playwright; Vitest.
- **Review:** Local 3D simulator with substantive code; optional game specialization after web fundamentals. Static review only; not built, tested or run.
- **Learn:** Three.js, simulation state, persistence, rendering performance
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Modify one resource-production rule and verify save/reload behavior.
- **Evidence:** [README.md](../../astra2/README.md), [data.ts](../../astra2/src/data.ts), [package.json](../../astra2/package.json).

#### astraspacegameweb

**Stage 7: Specializations. specialization.** [Open folder](../../astraspacegameweb)

Persistent browser strategy game with construction, recruitment, scouting, battles, support, conquest, resource caravans, tribes, diplomacy, forums, private messages and rankings.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Fastify; Node.js; React; Tailwind CSS; Vite; data: Drizzle; PostgreSQL; Redis; infrastructure: Docker; GitHub Actions; testing: Playwright; Vitest; integrations: BullMQ.
- **Review:** Broad Fastify/React strategy game; PostgreSQL, Redis and background jobs increase setup complexity. Static review only; not built, tested or run.
- **Learn:** Persistent multiplayer state, queues, strategy simulation
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace construction completion across database and worker boundaries.
- **Evidence:** [README.md](../../astraspacegameweb/README.md), [App.tsx](../../astraspacegameweb/apps/web/src/App.tsx), [package.json](../../astraspacegameweb/package.json).

#### buildermentor

**Stage 7: Specializations. study-helper.** [Open folder](../../buildermentor)

A mastery-tracking study engine for junior software engineers leveling up to mid/senior and preparing for interviews.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Fastify; Node.js; React; Tailwind CSS; Vite; data: Drizzle; PostgreSQL; infrastructure: Docker; GitHub Actions; testing: Playwright; Vitest; integrations: Anthropic API.
- **Review:** Substantial Fastify/React/PostgreSQL app; E2E material includes scaffolding and AI integrations require setup. Static review only; not built, tested or run.
- **Learn:** Retrieval pipelines, mastery models, full-stack source ingestion
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Use only after basic study habits work; trace one ingestion and retrieval path.
- **Evidence:** [README.md](../../buildermentor/README.md), [server.ts](../../buildermentor/apps/api/src/server.ts), [package.json](../../buildermentor/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Buildermentor](../../geminiorganized/LLM_Generated_Buildermentor). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### buildsmallplates

**Stage 7: Specializations. specialization.** [Open folder](../../buildsmallplates)

Small Plates mobile weightlifting log with workout progression and on-device storage.

- **Stack:** languages: TypeScript; frameworks: Expo; React; React Native; testing: Vitest.
- **Review:** Substantial local mobile app; purchase flow is explicitly a stubbed seam. Static review only; not built, tested or run.
- **Learn:** React Native, local SQLite, progression algorithms
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Test one progression rule and database migration with retained workouts.
- **Evidence:** [README.md](../../buildsmallplates/README.md), [App.tsx](../../buildsmallplates/App.tsx), [package.json](../../buildsmallplates/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Buildsmallplates](../../geminiorganized/LLM_Generated_Buildsmallplates). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### buildwhiteboard

**Stage 7: Specializations. alternative.** [Open folder](../../buildwhiteboard)

Collaborative Markdown editor using React, TypeScript, Yjs and WebSockets, with local document storage, preview, and presence.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: React; Vite; infrastructure: Docker; GitHub Actions; testing: Playwright.
- **Review:** Small collaborative editor with source and one cataloged test file; runtime convergence unverified. Static review only; not built, tested or run.
- **Learn:** Yjs, WebSockets, collaborative editing, persistence
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Demonstrate two-client convergence after disconnect/reconnect.
- **Evidence:** [README.md](../../buildwhiteboard/README.md), [App.tsx](../../buildwhiteboard/client/src/App.tsx), [package.json](../../buildwhiteboard/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Buildwhiteboard](../../geminiorganized/LLM_Generated_Buildwhiteboard). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### fableaihelperv2

**Stage 7: Specializations. alternative.** [Open folder](../../fableaihelperv2)

CueDeck is a free, local-first conversation practice and disclosed-assistance coach for Windows.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Electron; React; Vite; testing: Playwright; Vitest.
- **Review:** CueDeck implementation with tests; part of a related desktop-assistant family. Static review only; not built, tested or run.
- **Learn:** Electron architecture, disclosed conversation coaching, streaming
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace one audio-to-response flow and compare recovery against finalcallhelp.
- **Evidence:** [README.md](../../fableaihelperv2/cuedeck/README.md), [App.tsx](../../fableaihelperv2/cuedeck/src/renderer/App.tsx), [package.json](../../fableaihelperv2/cuedeck/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Fablehelperv2](../../geminiorganized/LLM_Generated_Fablehelperv2). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### fableaihelperv3

**Stage 7: Specializations. alternative.** [Open folder](../../fableaihelperv3)

Push-to-record interview copilot for Windows.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Electron; Vite; testing: Vitest; integrations: Anthropic API.
- **Review:** README calls this the v2 rewrite of aihelper despite folder name v3. Static review only; not built, tested or run.
- **Learn:** Low-latency streaming, Electron bridges, cancellation
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Measure and explain one mocked stream/cancel path before provider integration.
- **Evidence:** [README.md](../../fableaihelperv3/README.md), [preload.ts](../../fableaihelperv3/src/preload.ts), [package.json](../../fableaihelperv3/package.json).
- **Related versions/options:** [geminiorganized/LLM_Generated_Fablehelperv3](../../geminiorganized/LLM_Generated_Fablehelperv3). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### finalcallhelp

**Stage 7: Specializations. alternative.** [Open folder](../../finalcallhelp)

CueDeck desktop conversation-assistance and practice application.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Electron; React; Vite; testing: Playwright; Vitest.
- **Review:** Expanded CueDeck source with tests; folder name alone does not prove it is the canonical version. Static review only; not built, tested or run.
- **Learn:** Desktop IPC, provider adapters, conversation practice
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Choose one CueDeck baseline after comparing tests and setup requirements.
- **Evidence:** [README.md](../../finalcallhelp/README.md), [App.tsx](../../finalcallhelp/cuedeck/src/renderer/App.tsx), [package.json](../../finalcallhelp/cuedeck/package.json).

#### masteroutline

**Stage 7: Specializations. reference.** [Open folder](../../masteroutline)

A fast, collaborative, knowledge base for your team built using React and Node.js.Try out Outline using our hosted version at www.getoutline.com.

- **Stack:** languages: HTML; JavaScript; TypeScript; frameworks: React; Vite; data: PostgreSQL; Redis; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Vitest; integrations: MCP; Socket.IO.
- **Review:** Large Outline upstream codebase; useful for bounded contribution after simpler collaboration projects. Static review only; not built, tested or run.
- **Learn:** Mature collaborative editor, Koa, PostgreSQL, Redis, policies
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace one document permission rule and its tests.
- **Evidence:** [README.md](../../masteroutline/outline/README.md), [App.tsx](../../masteroutline/outline/app/components/Sidebar/App.tsx), [package.json](../../masteroutline/outline/package.json).
- **Related versions/options:** [geminiorganized/General_Masteroutline](../../geminiorganized/General_Masteroutline). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### mobiletagalog

**Stage 7: Specializations. specialization.** [Open folder](../../mobiletagalog)

A Duolingo-style app teaching Tagalog to English speakers, built with React Native + Expo.

- **Stack:** languages: JavaScript; TypeScript; frameworks: Expo; React; React Native.
- **Review:** Standalone port from tagalog; optional backend, no recorded audio clips yet, and no cataloged test files. Static review only; not built, tested or run.
- **Learn:** Expo navigation, device SQLite, offline course content
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Test offline progress and one guest-to-account synchronization scenario.
- **Evidence:** [README.md](../../mobiletagalog/README.md), [AuthScreen.tsx](../../mobiletagalog/src/components/AuthScreen.tsx), [package.json](../../mobiletagalog/package.json).
- **Related versions/options:** [geminiorganized/General_Mobiletagalog](../../geminiorganized/General_Mobiletagalog). Existing catalog comparison candidates only; sampled similarity is not full-tree identity or a canonical-version decision.

#### netairag

**Stage 7: Specializations. advanced capstone alternative.** [Open folder](../../netairag)

IT-operations learning platform with a .NET/React foundation and planned RAG, agent, mock integration and evaluation extensions.

- **Stack:** C#; CSS; HTML; TypeScript; ASP.NET Core; React; Vite; Entity Framework Core; PostgreSQL; Docker; GitHub Actions; xUnit.
- **Review:** Substantial .NET/React foundation and IT-operations CRUD; README and roadmap still reserve RAG, agents, MCP mocks and evaluation for future phases. Treat AI completion as unverified.
- **Learn:** Layered .NET, RBAC, operational data, retrieval and evaluation design.
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace one ticket request through UI/API/persistence, then implement one documented retrieval slice with a small evaluation set.
- **Evidence:** [README.md](../../netairag/README.md), [AuthController.cs](../../netairag/src/Api/Controllers/AuthController.cs), [UsersController.cs](../../netairag/src/Api/Controllers/UsersController.cs).
- **Related versions/options:** [geminiorganized/LLM_Generated_Rag](../../geminiorganized/LLM_Generated_Rag). Earlier catalog found matching multi-file samples with geminiorganized/LLM_Generated_Rag; this is evidence of copies/versions, not a full-tree equality proof.

#### netintercom

**Stage 7: Specializations. realtime specialization.** [Open folder](../../netintercom)

A two-sided live chat (Intercom-style): an embeddable visitor widget plus an agent inbox for support teams.

- **Stack:** C#; CSS; HTML; TypeScript; ASP.NET Core; React; Vite; Entity Framework Core; PostgreSQL; Docker; GitHub Actions; xUnit.
- **Review:** Two React clients and .NET API with visitor-scoped widget endpoints, SignalR and Hangfire wiring; unit/integration project structure present. Runtime reliability unverified.
- **Learn:** Realtime rooms, visitor versus agent auth, routing, presence and SLA jobs.
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace visitor session to agent reply and verify conversation authorization plus reconnect behavior.
- **Evidence:** [README.md](../../netintercom/README.md), [AuthController.cs](../../netintercom/src/NetIntercom.Api/Controllers/AuthController.cs), [WidgetController.cs](../../netintercom/src/NetIntercom.Api/Controllers/WidgetController.cs).
- **Related versions/options:** [geminiorganized/OpenSource_Upskilling_Intercom](../../geminiorganized/OpenSource_Upskilling_Intercom). Earlier catalog found matching multi-file samples with geminiorganized/OpenSource_Upskilling_Intercom; this is evidence of copies/versions, not a full-tree equality proof.

#### netopen5

**Stage 7: Specializations. upstream media specialization.** [Open folder](../../netopen5)

Jellyfin The Free Software Media System

- **Stack:** C#; CSS; HTML; ASP.NET Core; Entity Framework Core; SQLite; GitHub Actions.
- **Review:** Local upstream Jellyfin server source with C# API controllers, database and media-domain modules. Treat as advanced source-reading/contribution material.
- **Learn:** Media services, background libraries, API compatibility and large codebase maintenance.
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace one user/library request into service and storage boundaries, then choose a narrow tested fix.
- **Evidence:** [README.md](../../netopen5/jellyfin/README.md), [UserController.cs](../../netopen5/jellyfin/Jellyfin.Api/Controllers/UserController.cs), [UserViewsController.cs](../../netopen5/jellyfin/Jellyfin.Api/Controllers/UserViewsController.cs).
- **Related versions/options:** [geminiorganized/General_Open5](../../geminiorganized/General_Open5). Earlier catalog found matching multi-file samples with geminiorganized/General_Open5; this is evidence of copies/versions, not a full-tree equality proof.

#### spacegame

**Stage 7: Specializations. game/mobile specialization.** [Open folder](../../spacegame)

A server-authoritative, Tribal Wars-style multiplayer strategy game.

- **Stack:** JavaScript; SQL; TypeScript; Expo; Fastify; Node.js; React; React Native; Prisma; Redis; Docker; Vitest.
- **Review:** Server-authoritative multiplayer strategy code with Fastify API, Expo client, shared formulas, Prisma, BullMQ/Redis and Socket.IO. Runtime correctness unverified.
- **Learn:** Deterministic simulation, concurrency, queues, reconciliation and mobile/realtime state.
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace one build/combat timer from command to worker to client, including duplicate delivery.
- **Evidence:** [README.md](../../spacegame/README.md), [auth.ts](../../spacegame/apps/server/src/routes/auth.ts), [misc.ts](../../spacegame/apps/server/src/routes/misc.ts).
- **Related versions/options:** [geminiorganized/General_Spacegame](../../geminiorganized/General_Spacegame). Earlier catalog found matching multi-file samples with geminiorganized/General_Spacegame; this is evidence of copies/versions, not a full-tree equality proof.

#### spacegamev2

**Stage 7: Specializations. game/mobile variant.** [Open folder](../../spacegamev2)

A server-authoritative, Tribal Wars-style multiplayer strategy game.

- **Stack:** JavaScript; SQL; TypeScript; Expo; Fastify; Node.js; React; React Native; Prisma; Redis; Docker; GitHub Actions; Playwright; Vitest.
- **Review:** Warband variant nested at spacegamev2/spacegamev2. Fresh auth source differs from spacegame with session/logout/revocation imports; additional CI/E2E structure exists. Not established as a byte-for-byte duplicate or guaranteed better version.
- **Learn:** Session lifecycle, game consistency, recovery testing and version comparison.
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Compare auth and timer behavior with spacegame, choose one baseline, and test duplicate/replayed game commands.
- **Evidence:** [README.md](../../spacegamev2/spacegamev2/README.md), [auth.ts](../../spacegamev2/spacegamev2/apps/server/src/routes/auth.ts), [misc.ts](../../spacegamev2/spacegamev2/apps/server/src/routes/misc.ts).

#### tagalog

**Stage 7: Specializations. offline/mobile specialization.** [Open folder](../../tagalog)

A free Duolingo-style app teaching Tagalog to English speakers.

- **Stack:** CSS; JavaScript; SQL; TypeScript; Expo; Fastify; Next.js; Node.js; React; React Native; Drizzle; Docker; Vitest.
- **Review:** Aral multi-client learning app with Next.js, Expo, Fastify, shared pure TS game engine and Drizzle/Postgres schema. README documents guest mode, mobile SQLite outbox and simplifications.
- **Learn:** Shared domain core, content compiler, offline event sync, idempotency and cross-platform delivery.
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace one lesson progress event through guest storage and authenticated sync; verify duplicate/offline replay handling.
- **Evidence:** [README.md](../../tagalog/README.md), [auth.ts](../../tagalog/apps/api/src/routes/auth.ts), [me.ts](../../tagalog/apps/api/src/routes/me.ts).

<a id="location-desktop-gitvg-nested-repositories"></a>

### Desktop / gitvg nested repositories

#### gitvg/astra

**Stage 0: Planning and reference collections. reference.** [Open folder](../../gitvg/astra)

Software-engineering curriculum with onboarding, learning modules, handbooks, capstone templates, and a validation script.

- **Stack:** languages: Python.
- **Review:** Curriculum with 96 stories, 16 modules, and three capstones; checker is tooling, not a separate app. Static review only; not built, tested or run.
- **Learn:** Team onboarding, scoped tickets, reviewable contributions
- **Before starting:** None; use alongside active project work.
- **Next:** Use onboarding and select stories matching the current application.
- **Evidence:** [README.md](../../gitvg/astra/README.md), [check_curriculum.py](../../gitvg/astra/scripts/check_curriculum.py).

#### gitvg/storefront

**Stage 4: Integrated full-stack workflows. alternative.** [Open folder](../../gitvg/storefront)

E-commerce teaching app with customer browsing/cart/order flows and seller product, inventory, order, and image management.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; infrastructure: Docker; GitHub Actions; testing: Playwright; Vitest.
- **Review:** Compact Next.js/PostgreSQL teaching app with source and tests. Static review only; not built, tested or run.
- **Learn:** Next.js full-stack boundaries, SQL, commerce, caching
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Trace product-to-order flow and add one access-control test.
- **Evidence:** [README.md](../../gitvg/storefront/README.md), [catalog.ts](../../gitvg/storefront/server/services/catalog.ts), [package.json](../../gitvg/storefront/package.json).

#### gitvg/agora

**Stage 5: Domain rules and reliability. alternative.** [Open folder](../../gitvg/agora)

Single-store e-commerce teaching application with customer catalog/cart/checkout flows and an administrative back office.

- **Stack:** languages: C#; CSS; HTML; JavaScript; TypeScript; frameworks: ASP.NET Core; React; Tailwind CSS; Vite; data: Entity Framework Core; PostgreSQL; SQLite; infrastructure: Docker; GitHub Actions; testing: Vitest; xUnit.
- **Review:** C#/.NET plus React teaching repository; not simply the TypeScript version of agora-net. Static review only; not built, tested or run.
- **Learn:** Commerce invariants, C# application layers, React, transactions
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Follow one checkout slice and add a stock-reservation test.
- **Evidence:** [README.md](../../gitvg/agora/README.md), [Program.cs](../../gitvg/agora/src/Agora.Api/Program.cs), [docker-compose.yml](../../gitvg/agora/docker-compose.yml).

#### gitvg/agora-net

**Stage 5: Domain rules and reliability. alternative.** [Open folder](../../gitvg/agora-net)

C#/.NET e-commerce backend for catalog, inventory, carts, checkout reservations, and fulfillment-related rules.

- **Stack:** languages: C#; frameworks: ASP.NET Core; data: Entity Framework Core; SQLite; testing: xUnit.
- **Review:** Backend-only .NET commerce implementation with tests; no frontend implied. Static review only; not built, tested or run.
- **Learn:** Backend checkout, inventory reservations, JWT, EF Core
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Add one checkout failure or concurrent reservation test.
- **Evidence:** [README.md](../../gitvg/agora-net/README.md), [Program.cs](../../gitvg/agora-net/src/Agora.Api/Program.cs), [Agora.Api.csproj](../../gitvg/agora-net/src/Agora.Api/Agora.Api.csproj).

#### gitvg/atlas

**Stage 5: Domain rules and reliability. alternative.** [Open folder](../../gitvg/atlas)

Employer-of-record teaching platform for hiring, onboarding, paying, and managing an international workforce.

- **Stack:** languages: C#; frameworks: ASP.NET Core; data: Entity Framework Core; PostgreSQL; SQLite; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Large C# teaching platform; domain examples are educational and runtime unverified. Static review only; not built, tested or run.
- **Learn:** Employment workflows, C# domain modeling, persistence
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Trace one onboarding-to-payroll workflow and test a rejected transition.
- **Evidence:** [README.md](../../gitvg/atlas/README.md), [Program.cs](../../gitvg/atlas/src/Atlas.Api/Program.cs), [docker-compose.yml](../../gitvg/atlas/docker-compose.yml).

#### gitvg/atlas-net

**Stage 5: Domain rules and reliability. alternative.** [Open folder](../../gitvg/atlas-net)

An Employer-of-Record (EOR) platform backend, in the style of Velocity Global / Deel, built with C# and .NET 10.

- **Stack:** languages: C#; frameworks: ASP.NET Core; data: Entity Framework Core; SQLite; testing: xUnit.
- **Review:** Separate backend-focused .NET variant with tests, not an automatically redundant folder. Static review only; not built, tested or run.
- **Learn:** Backend lifecycle modeling, client-scoped auth, payroll
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Compare one lifecycle slice with Atlas and choose one implementation to study.
- **Evidence:** [README.md](../../gitvg/atlas-net/README.md), [Program.cs](../../gitvg/atlas-net/src/Atlas.Api/Program.cs), [Atlas.Api.csproj](../../gitvg/atlas-net/src/Atlas.Api/Atlas.Api.csproj).

#### gitvg/bazaar-app

**Stage 5: Domain rules and reliability. alternative.** [Open folder](../../gitvg/bazaar-app)

Shopify-style e-commerce teaching app with a customer storefront and administrative catalog/order workflows.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; SQLite; testing: Vitest; xUnit.
- **Review:** Full-stack .NET variant; stack differs from gitvg/bazaar. Static review only; not built, tested or run.
- **Learn:** .NET/React commerce, identity, fulfillment, EF Core
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Trace one return or fulfillment slice and test its permissions.
- **Evidence:** [README.md](../../gitvg/bazaar-app/README.md), [App.tsx](../../gitvg/bazaar-app/client/src/App.tsx), [package.json](../../gitvg/bazaar-app/client/package.json).

#### gitvg/tracer-net

**Stage 5: Domain rules and reliability. alternative.** [Open folder](../../gitvg/tracer-net)

A Linear-clone issue tracker backend built with C# / .NET 10 and ASP.NET Core.

- **Stack:** languages: C#; frameworks: ASP.NET Core; data: Entity Framework Core; SQLite; testing: xUnit.
- **Review:** Backend-only .NET issue tracker with substantial tests; choose as backend alternative to frontend-heavy courses. Static review only; not built, tested or run.
- **Learn:** Issue state machines, ranking, search, EF Core
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Test one invalid workflow transition and ordering edge case.
- **Evidence:** [README.md](../../gitvg/tracer-net/README.md), [Program.cs](../../gitvg/tracer-net/src/Tracer.Api/Program.cs), [Tracer.Api.csproj](../../gitvg/tracer-net/src/Tracer.Api/Tracer.Api.csproj).

#### gitvg/bazaar

**Stage 6: Architecture and advanced integrations. alternative.** [Open folder](../../gitvg/bazaar)

Bazaar is a Shopify-lite commerce platform and a fifteen-sprint systems-design course.

- **Stack:** languages: JavaScript; SQL; TypeScript; frameworks: Fastify; Next.js; Node.js; React; infrastructure: GitHub Actions; testing: Vitest.
- **Review:** TypeScript systems-design course with source/tests; in-memory fakes in tests do not establish live integration behavior. Static review only; not built, tested or run.
- **Learn:** Cache coherence, inventory consistency, commerce systems design
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Explain stale storefront versus fresh merchant state and test invalidation.
- **Evidence:** [README.md](../../gitvg/bazaar/README.md), [cart-service.ts](../../gitvg/bazaar/apps/api/src/cart-service.ts), [package.json](../../gitvg/bazaar/package.json).

#### gitvg/harbor-net

**Stage 6: Architecture and advanced integrations. alternative.** [Open folder](../../gitvg/harbor-net)

An Intercom-style customer-messaging platform — C#/.NET backend only.

- **Stack:** languages: C#; frameworks: ASP.NET Core; data: Entity Framework Core; SQLite; testing: xUnit.
- **Review:** Backend-only .NET support platform with test coverage files; integration behavior unverified. Static review only; not built, tested or run.
- **Learn:** SLA workflows, assignment, signed webhooks, outbox
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Test one SLA deadline and duplicate webhook delivery.
- **Evidence:** [README.md](../../gitvg/harbor-net/README.md), [Program.cs](../../gitvg/harbor-net/src/Harbor.Api/Program.cs), [Harbor.Api.csproj](../../gitvg/harbor-net/src/Harbor.Api/Harbor.Api.csproj).

#### gitvg/pulse

**Stage 6: Architecture and advanced integrations. alternative.** [Open folder](../../gitvg/pulse)

Product-analytics learning project with event ingestion, consumers, jobs, and a web interface.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Fastify; Node.js; React; Vite; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Vitest; integrations: BullMQ.
- **Review:** Substantial course source/tests; README says live DB/queue/stream wiring is not exercised by CI. Static review only; not built, tested or run.
- **Learn:** Event ingestion, analytics, identity merge, queues
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Trace one event through ingestion to query and test duplicate handling.
- **Evidence:** [README.md](../../gitvg/pulse/README.md), [App.tsx](../../gitvg/pulse/apps/web/src/App.tsx), [package.json](../../gitvg/pulse/package.json).

#### gitvg/pulse-net

**Stage 6: Architecture and advanced integrations. alternative.** [Open folder](../../gitvg/pulse-net)

A PostHog/Mixpanel-style product-analytics platform — C#/.NET backend only.

- **Stack:** languages: C#; frameworks: ASP.NET Core; data: Entity Framework Core; SQLite; testing: xUnit.
- **Review:** Backend-only .NET analytics system with SQLite and worker tests. Static review only; not built, tested or run.
- **Learn:** Durable ingestion, dead letters, analytics SQL, identity merge
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Test restart and replay of one captured event.
- **Evidence:** [README.md](../../gitvg/pulse-net/README.md), [Program.cs](../../gitvg/pulse-net/src/Pulse.Api/Program.cs), [Pulse.Api.csproj](../../gitvg/pulse-net/src/Pulse.Api/Pulse.Api.csproj).

#### gitvg/relay

**Stage 6: Architecture and advanced integrations. alternative.** [Open folder](../../gitvg/relay)

Workflow-automation teaching platform with triggers, actions, connectors, and durable-execution concepts across a fifteen-sprint curriculum.

- **Stack:** languages: JavaScript; TypeScript; frameworks: Fastify; Next.js; Node.js; React; data: Prisma; Redis; infrastructure: GitHub Actions; testing: Vitest; integrations: BullMQ.
- **Review:** TypeScript course implementation with API/web/source tests; external connector behavior unverified. Static review only; not built, tested or run.
- **Learn:** Workflow engines, connectors, retries, durable execution
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Trace one failed workflow step and prove retry behavior is bounded.
- **Evidence:** [README.md](../../gitvg/relay/README.md), [server.ts](../../gitvg/relay/apps/api/src/server.ts), [package.json](../../gitvg/relay/package.json).

#### gitvg/relay-app

**Stage 6: Architecture and advanced integrations. alternative.** [Open folder](../../gitvg/relay-app)

A Zapier-style integrations / connectors platform.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; SQLite; testing: Vitest; xUnit.
- **Review:** .NET/React implementation explicitly simulates external actions in process. Static review only; not built, tested or run.
- **Learn:** .NET workflow execution, logs, permissions, retries
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Replace one simulated action with a controlled adapter and contract test.
- **Evidence:** [README.md](../../gitvg/relay-app/README.md), [App.tsx](../../gitvg/relay-app/client/src/App.tsx), [package.json](../../gitvg/relay-app/client/package.json).

#### gitvg/folio

**Stage 7: Specializations. capstone.** [Open folder](../../gitvg/folio)

Collaborative document-editor teaching app covering blocks, concurrent editing, offline merge, comments, permissions, and version history.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Fastify; Node.js; React; Vite; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Vitest.
- **Review:** Advanced course implementation with substantial source/tests; a stale scaffolding note conflicts with broader existing code. Static review only; not built, tested or run.
- **Learn:** CRDTs, offline merge, permissions, collaborative editors
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Complete one two-client conflict scenario after simpler realtime exercises.
- **Evidence:** [README.md](../../gitvg/folio/README.md), [App.tsx](../../gitvg/folio/apps/web/src/App.tsx), [package.json](../../gitvg/folio/package.json).

#### gitvg/folio-app

**Stage 7: Specializations. alternative.** [Open folder](../../gitvg/folio-app)

A Notion-style collaborative docs & knowledge base — full-stack monorepo.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; SQLite; testing: Vitest; xUnit.
- **Review:** Separate .NET/React document system; verify actual realtime semantics before equating it with Folio CRDT course. Static review only; not built, tested or run.
- **Learn:** Block editing, document permissions, versions, .NET APIs
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace a page edit through authorization and version history.
- **Evidence:** [README.md](../../gitvg/folio-app/README.md), [App.tsx](../../gitvg/folio-app/client/src/App.tsx), [package.json](../../gitvg/folio-app/client/package.json).

#### gitvg/harbor

**Stage 7: Specializations. capstone.** [Open folder](../../gitvg/harbor)

Customer-messaging and support-inbox learning project with API, web, worker, and retrieval components.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Fastify; Node.js; React; Vite; data: Prisma; infrastructure: GitHub Actions; testing: Vitest.
- **Review:** Source and tests exist; CI intentionally uses fake infrastructure and mock models. Static review only; not built, tested or run.
- **Learn:** Support workflows, retrieval, evaluation, LLM cost controls
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Reproduce one failed answer evaluation with a mock model and improve it.
- **Evidence:** [README.md](../../gitvg/harbor/README.md), [App.tsx](../../gitvg/harbor/apps/web/src/App.tsx), [package.json](../../gitvg/harbor/package.json).

#### gitvg/tracer

**Stage 7: Specializations. alternative.** [Open folder](../../gitvg/tracer)

An offline-first, real-time issue tracker (a Linear-style clone) — and a 15-sprint upskilling curriculum built entirely as pull requests.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Fastify; Node.js; React; Vite; data: Prisma; infrastructure: Docker; GitHub Actions; testing: Vitest.
- **Review:** Advanced TypeScript issue-tracker course; frontend and sync source exist. Static review only; not built, tested or run.
- **Learn:** Offline synchronization, real-time presence, issue workflows
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** After gitjira-app, test conflicting offline edits and recovery.
- **Evidence:** [README.md](../../gitvg/tracer/README.md), [App.tsx](../../gitvg/tracer/apps/web/src/App.tsx), [package.json](../../gitvg/tracer/package.json).

<a id="location-desktop-jsharness-nested-repositories"></a>

### Desktop / jsharness nested repositories

#### jsharness/ctvodejs

**Stage 7: Specializations. specialization.** [Open folder](../../jsharness/ctvodejs)

A TypeScript port of VTCode, built as a sequence of reviewable vertical slices.

- **Stack:** languages: JavaScript; TypeScript; infrastructure: GitHub Actions; testing: Vitest.
- **Review:** Early TypeScript port explicitly not feature complete; substantial source and tests exist. Static review only; not built, tested or run.
- **Learn:** TypeScript agent runtimes, event contracts, parity testing
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Port one bounded VTCode behavior and add a parity fixture.
- **Evidence:** [README.md](../../jsharness/ctvodejs/README.md), [index.ts](../../jsharness/ctvodejs/apps/cli/src/index.ts), [package.json](../../jsharness/ctvodejs/package.json).

#### jsharness/VTCode

**Stage 7: Specializations. reference.** [Open folder](../../jsharness/VTCode)

VTCode Rust terminal coding-agent workspace.

- **Stack:** languages: JavaScript; Python; Ruby; Rust; TypeScript; frameworks: Axum; infrastructure: GitHub Actions.
- **Review:** Large Rust upstream coding-agent workspace; research-preview behavior and local runtime unverified. Static review only; not built, tested or run.
- **Learn:** Rust CLI architecture, tools, agent protocols, terminal UI
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace one command from CLI parsing to tool execution and compare the TS port.
- **Evidence:** [README.md](../../jsharness/VTCode/README.md), [main.rs](../../jsharness/VTCode/src/main.rs), [Cargo.toml](../../jsharness/VTCode/Cargo.toml).

<a id="location-organized-desktop-01-net-workspaces"></a>

### _Organized Desktop/01 Net Workspaces

#### _Organized Desktop/01 Net Workspaces/csbootcamp

**Stage 1: Language and browser foundations. Foundations exercise collection.** [Open folder](../../_Organized%20Desktop/01%20Net%20Workspaces/csbootcamp)

A personal coding bootcamp for levelling up C# and .NET fundamentals.

- **Stack:** languages: C#.
- **Review:** Source implementation is indexed; runtime behavior remains unverified. Limits: Exercise TODO stubs are intentional learner work, not evidence of an abandoned app. README expects .NET 10 file-based apps.
- **Learn:** C# language semantics, delegates, LINQ, strings/time, local test feedback
- **Before starting:** Editor, terminal, Git basics; variables, loops, and functions.
- **Next:** Read FLIGHTPLAN.md; study modules 01 language core, 02 methods/delegates, 03 collections/LINQ, 04 strings/time; solve prompts before solutions.
- **Evidence:** [README.md](../../_Organized%20Desktop/01%20Net%20Workspaces/csbootcamp/README.md), [verify.cs](../../_Organized%20Desktop/01%20Net%20Workspaces/csbootcamp/bootcamp/verify.cs), [06-ordering.cs](../../_Organized%20Desktop/01%20Net%20Workspaces/csbootcamp/bootcamp/03-collections-and-linq/exercises/06-ordering.cs).

#### _Organized Desktop/01 Net Workspaces/.netpastebin

**Stage 3: APIs and SQL. Alternative practice project.** [Open folder](../../_Organized%20Desktop/01%20Net%20Workspaces/.netpastebin)

Small C#/ASP.NET Core paste-sharing API and UI learning project.

- **Stack:** languages: C#; CSS; HTML; JavaScript; TypeScript; frameworks: ASP.NET Core; React; Vite.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** Language fluency, HTTP/JSON, SQL CRUD, and asynchronous code.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/01%20Net%20Workspaces/.netpastebin/README.md), [Program.cs](../../_Organized%20Desktop/01%20Net%20Workspaces/.netpastebin/backend/Program.cs), [package.json](../../_Organized%20Desktop/01%20Net%20Workspaces/.netpastebin/frontend/package.json).

#### _Organized Desktop/01 Net Workspaces/.nethris

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/01%20Net%20Workspaces/.nethris)

A compact HRIS / employee directory platform inspired by BambooHR and Rippling.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; SQLite.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** tenant isolation, approval rules, audit history, module boundaries
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one employee approval and test both cross-tenant access and invalid state changes.
- **Evidence:** [README.md](../../_Organized%20Desktop/01%20Net%20Workspaces/.nethris/README.md), [Program.cs](../../_Organized%20Desktop/01%20Net%20Workspaces/.nethris/server/Nethris.Api/Program.cs), [App.tsx](../../_Organized%20Desktop/01%20Net%20Workspaces/.nethris/client/src/App.tsx).

#### _Organized Desktop/01 Net Workspaces/.nettrello

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/01%20Net%20Workspaces/.nettrello)

NetTrello is a Trello-style kanban starter built with C#, ASP.NET Core, React, and TypeScript.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; infrastructure: Docker.
- **Review:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: README explicitly describes seeded in-memory persistence. Adding durable storage is a learning exercise.
- **Learn:** relational CRUD, ordering, optimistic UI, project permissions
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Implement one board/task operation and test ordering plus permission boundaries.
- **Evidence:** [README.md](../../_Organized%20Desktop/01%20Net%20Workspaces/.nettrello/README.md), [Program.cs](../../_Organized%20Desktop/01%20Net%20Workspaces/.nettrello/src/NetTrello.Api/Program.cs), [App.tsx](../../_Organized%20Desktop/01%20Net%20Workspaces/.nettrello/client/src/App.tsx).

#### _Organized Desktop/01 Net Workspaces/.netzen

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/01%20Net%20Workspaces/.netzen)

A learning-oriented Zendesk/Intercom-style inbox built with C#, ASP.NET Core, SignalR, and React.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/01%20Net%20Workspaces/.netzen/support-ticketing-app/README.md), [Program.cs](../../_Organized%20Desktop/01%20Net%20Workspaces/.netzen/support-ticketing-app/backend/SupportDesk.Api/Program.cs), [App.tsx](../../_Organized%20Desktop/01%20Net%20Workspaces/.netzen/support-ticketing-app/frontend/src/App.tsx).

#### _Organized Desktop/01 Net Workspaces/.netcalendy

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/01%20Net%20Workspaces/.netcalendy)

A Calendly-style booking SaaS built with C# / .NET 9 and React.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; PostgreSQL; infrastructure: Docker; testing: xUnit.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** date/time modeling, interval conflicts, transactional booking, cancellation
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Test overlapping bookings and a daylight-saving boundary on one booking flow.
- **Evidence:** [README.md](../../_Organized%20Desktop/01%20Net%20Workspaces/.netcalendy/README.md), [Program.cs](../../_Organized%20Desktop/01%20Net%20Workspaces/.netcalendy/src/NetCalendy.Api/Program.cs), [App.tsx](../../_Organized%20Desktop/01%20Net%20Workspaces/.netcalendy/web/src/App.tsx).

#### _Organized Desktop/01 Net Workspaces/.netgum

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/01%20Net%20Workspaces/.netgum)

Netgum is a learning-oriented, clone of Gumroad built with C# and .NET 8.

- **Stack:** languages: C#; frameworks: ASP.NET Core; data: Entity Framework Core; SQL Server; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational modeling, pricing, stock reservations, order state transitions
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace an order/reservation and test invalid transitions or repeated submissions.
- **Evidence:** [README.md](../../_Organized%20Desktop/01%20Net%20Workspaces/.netgum/README.md), [Program.cs](../../_Organized%20Desktop/01%20Net%20Workspaces/.netgum/src/Netgum.Api/Program.cs), [Dockerfile](../../_Organized%20Desktop/01%20Net%20Workspaces/.netgum/src/Netgum.Api/Dockerfile).

#### _Organized Desktop/01 Net Workspaces/.netvg

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/01%20Net%20Workspaces/.netvg)

AtlasWork is a teaching application for global workforce hiring, payment, and employee/contractor management.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; infrastructure: GitHub Actions; testing: xUnit.
- **Review:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: README describes seeded in-memory read models and deterministic mock frontend fallback data.
- **Learn:** tenant isolation, approval rules, audit history, module boundaries
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one employee approval and test both cross-tenant access and invalid state changes.
- **Evidence:** [README.md](../../_Organized%20Desktop/01%20Net%20Workspaces/.netvg/README.md), [Program.cs](../../_Organized%20Desktop/01%20Net%20Workspaces/.netvg/src/PeblClone.Api/Program.cs), [package.json](../../_Organized%20Desktop/01%20Net%20Workspaces/.netvg/src/PeblClone.Web/package.json).

#### _Organized Desktop/01 Net Workspaces/.netslack

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/01%20Net%20Workspaces/.netslack)

NetSlack is a Slack-style collaboration app built with ASP.NET Core, EF Core, SignalR, and React.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; SQLite; infrastructure: Docker; testing: xUnit.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event/state modeling, real-time synchronization, validation, reconnect behavior
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Isolate a game/message state transition and specify duplicate-event/reconnect tests.
- **Evidence:** [README.md](../../_Organized%20Desktop/01%20Net%20Workspaces/.netslack/README.md), [Program.cs](../../_Organized%20Desktop/01%20Net%20Workspaces/.netslack/src/NetSlack.Api/Program.cs), [App.tsx](../../_Organized%20Desktop/01%20Net%20Workspaces/.netslack/client/src/App.tsx).

<a id="location-organized-desktop-02-build-projects"></a>

### _Organized Desktop/02 Build Projects

#### _Organized Desktop/02 Build Projects/buildgum

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildgum)

Buildgum is a Gumroad-style creator commerce prototype built with Vite, React, TypeScript, and lucide-react.

- **Stack:** languages: CSS; HTML; TypeScript; frameworks: React; Vite.
- **Review:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Frontend commerce prototype; do not infer an operational payment/backend system from screens.
- **Learn:** relational modeling, pricing, stock reservations, order state transitions
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Trace an order/reservation and test invalid transitions or repeated submissions.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildgum/README.md), [index.html](../../_Organized%20Desktop/02%20Build%20Projects/buildgum/index.html), [App.tsx](../../_Organized%20Desktop/02%20Build%20Projects/buildgum/src/App.tsx).

#### _Organized Desktop/02 Build Projects/buildsubbox

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildsubbox)

ParcelPilot subscription-box UI prototype for subscriber preferences, billing, curation, and fulfillment.

- **Stack:** languages: CSS; HTML; JavaScript; frameworks: React; Vite.
- **Review:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Frontend prototype with backend/API/testing work discussed as a next layer.
- **Learn:** money arithmetic, idempotency, webhook processing, transaction boundaries
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Trace a charge or webhook and design a replay test that cannot double-apply it.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildsubbox/docs/upskill/README.md), [index.html](../../_Organized%20Desktop/02%20Build%20Projects/buildsubbox/index.html), [App.jsx](../../_Organized%20Desktop/02%20Build%20Projects/buildsubbox/src/App.jsx).

#### _Organized Desktop/02 Build Projects/buildasana

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildasana)

BuildAsana is an Asana-inspired work management system built for learning production-quality C#, .NET, and React patterns.

- **Stack:** languages: C#; CSS; HTML; JavaScript; TypeScript; frameworks: ASP.NET Core; React; Vite; testing: xUnit.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Learn:** relational CRUD, ordering, optimistic UI, project permissions
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Implement one board/task operation and test ordering plus permission boundaries.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildasana/README.md), [Program.cs](../../_Organized%20Desktop/02%20Build%20Projects/buildasana/backend/src/BuildAsana.Api/Program.cs), [App.tsx](../../_Organized%20Desktop/02%20Build%20Projects/buildasana/frontend/src/App.tsx).

#### _Organized Desktop/02 Build Projects/buildCRMPYJS

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildCRMPYJS)

Full-stack internal CRM and sales-pipeline application.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Vite; data: Prisma; Redis; infrastructure: Docker; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational data, lifecycle transitions, tenant-scoped queries, audit history
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace a lead/deal transition and test tenant isolation plus invalid transitions.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildCRMPYJS/README.md), [auth.routes.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildCRMPYJS/backend/src/modules/auth/auth.routes.ts), [App.tsx](../../_Organized%20Desktop/02%20Build%20Projects/buildCRMPYJS/frontend/src/App.tsx).

#### _Organized Desktop/02 Build Projects/buildjira

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildjira)

C#/React issue tracker; JavaScript predecessor is archived and current authentication uses demo actor impersonation.

- **Stack:** languages: C#; CSS; HTML; JavaScript; TypeScript; frameworks: ASP.NET Core; infrastructure: Docker.
- **Review:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: README states x-user-id impersonation/default seeded actor is a local-development identity model, not production authentication.
- **Learn:** relational CRUD, ordering, optimistic UI, project permissions
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Implement one board/task operation and test ordering plus permission boundaries.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildjira/README.md), [health.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildjira/apps/api/src/routes/health.ts), [App.tsx](../../_Organized%20Desktop/02%20Build%20Projects/buildjira/apps/web/src/App.tsx).

#### _Organized Desktop/02 Build Projects/buildaffiliate

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildaffiliate)

Multi-tenant platform connecting brands with affiliates: click tracking, attribution, commissions, fraud review, and payouts.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Fastify; Next.js; Node.js; React; Tailwind CSS; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Vitest; integrations: BullMQ.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event modeling, aggregation, reporting queries, deduplication
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Validate one metric against a small hand-calculated dataset including duplicates.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildaffiliate/README.md), [error-handler.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildaffiliate/apps/api/src/lib/error-handler.ts), [server.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildaffiliate/apps/api/src/server.ts).

#### _Organized Desktop/02 Build Projects/buildanalytics

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildanalytics)

Full-stack internal dashboard platform for KPI tracking, operational analytics, audit visibility, monitoring dashboards, CSV exports, and role-aware internal operations workflows.

- **Stack:** languages: CSS; HTML; SQL; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Playwright; Vitest; integrations: BullMQ.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildanalytics/README.md), [auth.routes.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildanalytics/backend/src/modules/auth/auth.routes.ts), [App.tsx](../../_Organized%20Desktop/02%20Build%20Projects/buildanalytics/frontend/src/App.tsx).

#### _Organized Desktop/02 Build Projects/buildecom

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildecom)

MarketForge is a multi-vendor marketplace codebase.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; data: Prisma; Redis; testing: Playwright; Vitest; integrations: Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational modeling, pricing, stock reservations, order state transitions
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace an order/reservation and test invalid transitions or repeated submissions.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildecom/README.md), [service.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildecom/src/server/orders/service.ts), [package.json](../../_Organized%20Desktop/02%20Build%20Projects/buildecom/package.json).

#### _Organized Desktop/02 Build Projects/buildScedulingPYJS

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildScedulingPYJS)

Full-stack scheduling platform scaffolded with React, TypeScript, Express, Prisma, PostgreSQL, Redis, BullMQ, JWT auth, RBAC, and scheduling-focused backend architecture.

- **Stack:** languages: CSS; HTML; TypeScript; frameworks: Express; Node.js; React; Vite; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Vitest; integrations: BullMQ.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** date/time modeling, interval conflicts, transactional booking, cancellation
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Test overlapping bookings and a daylight-saving boundary on one booking flow.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildScedulingPYJS/README.md), [auth.routes.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildScedulingPYJS/backend/src/modules/auth/auth.routes.ts), [server.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildScedulingPYJS/backend/src/server.ts).

#### _Organized Desktop/02 Build Projects/buildagenthelpdesk

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildagenthelpdesk)

TypeScript modular monolith that emulates a mid-size internal enterprise platform.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; data: Prisma; infrastructure: Docker; GitHub Actions; testing: Vitest.
- **Review:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Agent behavior uses deterministic local mocks.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildagenthelpdesk/README.md), [auth.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildagenthelpdesk/apps/web/lib/auth.ts), [jobs.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildagenthelpdesk/packages/domain/src/jobs.ts).

#### _Organized Desktop/02 Build Projects/buildagentteachGEM

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildagentteachGEM)

A school operations cockpit built as a software engineering training laboratory.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; data: Prisma.
- **Review:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Agent layer is documented as five deterministic mock-LLM analysts.
- **Learn:** enrollment/progress data, scoped permissions, policy rules, modular services
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one enrollment-to-completion flow and test an ineligible certification.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildagentteachGEM/README.md), [page.tsx](../../_Organized%20Desktop/02%20Build%20Projects/buildagentteachGEM/src/app/page.tsx), [auth.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildagentteachGEM/src/packages/shared/auth.ts).

#### _Organized Desktop/02 Build Projects/buildagentteaching

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildagentteaching)

Agentic Education Operations is a TypeScript modular-monolith learning project that emulates the start of a internal education operations and LMS platform.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; data: Prisma; infrastructure: Docker; GitHub Actions; testing: Vitest.
- **Review:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Agent behavior uses deterministic local mocks.
- **Learn:** enrollment/progress data, scoped permissions, policy rules, modular services
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one enrollment-to-completion flow and test an ineligible certification.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildagentteaching/README.md), [handlers.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildagentteaching/packages/application/src/jobs/handlers.ts), [job-service.ts](../../_Organized%20Desktop/02%20Build%20Projects/buildagentteaching/packages/application/src/services/job-service.ts).

#### _Organized Desktop/02 Build Projects/buildantigVG

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/02%20Build%20Projects/buildantigVG)

Multi-tenant Employer of Record teaching app; document uploads are simulated metadata updates.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: NestJS; Node.js; React; Vite; data: Prisma; infrastructure: Docker; testing: Jest.
- **Review:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Document upload is currently a simulated metadata update; storage integration is proposed work.
- **Learn:** tenant isolation, approval rules, audit history, module boundaries
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one employee approval and test both cross-tenant access and invalid state changes.
- **Evidence:** [README.md](../../_Organized%20Desktop/02%20Build%20Projects/buildantigVG/README.md), [App.tsx](../../_Organized%20Desktop/02%20Build%20Projects/buildantigVG/apps/web/src/App.tsx), [package.json](../../_Organized%20Desktop/02%20Build%20Projects/buildantigVG/package.json).

<a id="location-organized-desktop-03-master-projects"></a>

### _Organized Desktop/03 Master Projects

#### _Organized Desktop/03 Master Projects/master

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/master)

Personal planning app connecting areas, goals, projects, tasks, daily checklists, and time tracking.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: IndexedDB / Dexie; Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/master/README.md), [api.ts](../../_Organized%20Desktop/03%20Master%20Projects/master/src/lib/api.ts), [auth.ts](../../_Organized%20Desktop/03%20Master%20Projects/master/src/lib/auth.ts).

#### _Organized Desktop/03 Master Projects/master 6

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/master%206)

A enterprise learning management and certification platform built as a TypeScript modular monolith learning codebase.

- **Stack:** languages: CSS; TypeScript; frameworks: Express; Next.js; Node.js; React; data: Prisma; Redis; infrastructure: Docker; testing: Vitest; integrations: BullMQ.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** enrollment/progress data, scoped permissions, policy rules, modular services
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one enrollment-to-completion flow and test an ineligible certification.
- **Evidence:** [auth.routes.ts](../../_Organized%20Desktop/03%20Master%20Projects/master%206/apps/api/src/routes/auth.routes.ts), [package.json](../../_Organized%20Desktop/03%20Master%20Projects/master%206/package.json).

#### _Organized Desktop/03 Master Projects/master1

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/master1)

GlobalWork is a fictional Employer of Record SaaS platform built as a TypeScript modular monolith.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: NestJS; Next.js; Node.js; React; data: Prisma; Redis; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Jest; Playwright; Vitest; integrations: BullMQ.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** tenant isolation, approval rules, audit history, module boundaries
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one employee approval and test both cross-tenant access and invalid state changes.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/master1/README.md), [auth.service.ts](../../_Organized%20Desktop/03%20Master%20Projects/master1/apps/api/src/modules/auth/auth.service.ts), [package.json](../../_Organized%20Desktop/03%20Master%20Projects/master1/package.json).

#### _Organized Desktop/03 Master Projects/master2

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/master2)

A learning-oriented multi-tenant SaaS billing and subscription platform.

- **Stack:** languages: CSS; HTML; TypeScript; frameworks: Express; Node.js; React; Vite; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Vitest; integrations: BullMQ.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** money arithmetic, idempotency, webhook processing, transaction boundaries
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace a charge or webhook and design a replay test that cannot double-apply it.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/master2/README.md), [async-handler.ts](../../_Organized%20Desktop/03%20Master%20Projects/master2/apps/api/src/shared/async-handler.ts), [App.tsx](../../_Organized%20Desktop/03%20Master%20Projects/master2/apps/web/src/App.tsx).

#### _Organized Desktop/03 Master Projects/master3

**Stage 6: Architecture and advanced integrations. Core journey candidate.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/master3)

TypeScript support/CRM modular-monolith teaching app with demo header-based tenant/user resolution.

- **Stack:** languages: CSS; HTML; TypeScript; frameworks: Express; Node.js; React; Vite; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Vitest.
- **Review:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: README states x-tenant-slug/x-user-email resolve demo identity; the auth layer is not production authentication.
- **Learn:** route/service/repository boundaries, permissions, queue filters, workflow rules
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace ticket creation to storage; test forbidden transitions and unauthorized access.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/master3/README.md), [health.ts](../../_Organized%20Desktop/03%20Master%20Projects/master3/apps/api/src/routes/health.ts), [App.tsx](../../_Organized%20Desktop/03%20Master%20Projects/master3/apps/web/src/App.tsx).

#### _Organized Desktop/03 Master Projects/master4

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/master4)

Atlas Fulfillment is a TypeScript operations platform for warehouse and ecommerce inventory, orders, and fulfillment.

- **Stack:** languages: CSS; HTML; TypeScript; frameworks: Express; Node.js; React; Vite; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational modeling, pricing, stock reservations, order state transitions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace an order/reservation and test invalid transitions or repeated submissions.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/master4/README.md), [orders.service.ts](../../_Organized%20Desktop/03%20Master%20Projects/master4/src/server/modules/orders/orders.service.ts), [App.tsx](../../_Organized%20Desktop/03%20Master%20Projects/master4/src/App.tsx).

#### _Organized Desktop/03 Master Projects/master7

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/master7)

Teaching codebase for growing a enterprise learning management and certification platform through documented feature slices.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; Redis; infrastructure: Docker; testing: Playwright; Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** enrollment/progress data, scoped permissions, policy rules, modular services
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one enrollment-to-completion flow and test an ineligible certification.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/master7/README.md), [services.ts](../../_Organized%20Desktop/03%20Master%20Projects/master7/apps/api/src/services.ts), [package.json](../../_Organized%20Desktop/03%20Master%20Projects/master7/package.json).

#### _Organized Desktop/03 Master Projects/mastercal

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/mastercal)

The community-driven, open-source scheduling platform.

- **Stack:** languages: CSS; HTML; JavaScript; PHP; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Playwright; Vitest; integrations: Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** date/time modeling, interval conflicts, transactional booking, cancellation; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/mastercal/cal.diy/README.md), [server.ts](../../_Organized%20Desktop/03%20Master%20Projects/mastercal/cal.diy/packages/i18n/server.ts), [App.tsx](../../_Organized%20Desktop/03%20Master%20Projects/mastercal/cal.diy/packages/app-store-cli/src/App.tsx).

#### _Organized Desktop/03 Master Projects/masterdidy

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterdidy)

Dify LLM application platform with workflow, knowledge-retrieval, and agent components.

- **Stack:** languages: CSS; HTML; JavaScript; PHP; Python; SQL; TypeScript; frameworks: FastAPI; Flask; Hono; Next.js; Node.js; React; Tailwind CSS; Vite; data: MySQL; PostgreSQL; Redis; Supabase; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Playwright; Vitest; pytest; integrations: Anthropic API; Celery.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterdidy/dify/README.md), [app.py](../../_Organized%20Desktop/03%20Master%20Projects/masterdidy/dify/api/controllers/web/app.py), [package.json](../../_Organized%20Desktop/03%20Master%20Projects/masterdidy/dify/package.json).

#### _Organized Desktop/03 Master Projects/masterdub

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterdub)

The open-source link attribution platform.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; Vite; data: MySQL; Prisma; infrastructure: Docker; GitHub Actions; testing: Playwright; Vitest; integrations: Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event modeling, aggregation, reporting queries, deduplication; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterdub/dub/README.md), [use-click-handlers.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterdub/dub/packages/ui/src/hooks/use-click-handlers.ts), [server.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterdub/dub/apps/web/lib/axiom/server.ts).

#### _Organized Desktop/03 Master Projects/masterfinisc

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterfinisc)

The open-source secret management platform: Sync secrets/configs across your team/infrastructure and prevent secret leaks.

- **Stack:** languages: CSS; HTML; JavaScript; Python; Rust; TypeScript; frameworks: Express; Fastify; Node.js; React; Tailwind CSS; Vite; data: MongoDB; MySQL; PostgreSQL; Redis; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Vitest; integrations: BullMQ; MCP.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterfinisc/infisical/README.md), [auth-dal.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterfinisc/infisical/backend/src/services/auth/auth-dal.ts), [package.json](../../_Organized%20Desktop/03%20Master%20Projects/masterfinisc/infisical/package.json).

#### _Organized Desktop/03 Master Projects/masterflag

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterflag)

Flagsmith feature-flag and remote-configuration platform.

- **Stack:** languages: CSS; HTML; JavaScript; Python; SCSS; SQL; TypeScript; frameworks: Django; Express; Node.js; React; data: PostgreSQL; Redis; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Jest; Playwright; pytest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** rule evaluation, rollout consistency, cache invalidation, audit history; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterflag/flagsmith/README.md), [useRole.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterflag/flagsmith/frontend/common/services/useRole.ts), [Dockerfile](../../_Organized%20Desktop/03%20Master%20Projects/masterflag/flagsmith/Dockerfile).

#### _Organized Desktop/03 Master Projects/masterform

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterform)

Formbricks survey and experience-management platform.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; Vite; data: Prisma; Redis; infrastructure: AWS SDK; Azure SDK; Docker; GitHub Actions; testing: Playwright; Vitest; integrations: Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterform/formbricks/README.md), [service.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterform/formbricks/packages/cache/src/service.ts), [App.tsx](../../_Organized%20Desktop/03%20Master%20Projects/masterform/formbricks/apps/storybook/src/App.tsx).

#### _Organized Desktop/03 Master Projects/masterhop

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterhop)

Open Source API Development Ecosystem

- **Stack:** languages: Go; HTML; JavaScript; Rust; SCSS; SQL; TypeScript; Vue; frameworks: Express; NestJS; Node.js; Tailwind CSS; Vite; Vue; data: PostgreSQL; Prisma; infrastructure: Docker; GitHub Actions; testing: Jest; Vitest.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterhop/hoppscotch/README.md), [App.vue](../../_Organized%20Desktop/03%20Master%20Projects/masterhop/hoppscotch/packages/hoppscotch-agent/src/App.vue).

#### _Organized Desktop/03 Master Projects/masteridur

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masteridur)

Open Source ERP / CRM Accounting Invoice Quote

- **Stack:** languages: CSS; HTML; JavaScript; frameworks: Express; Node.js; React; Vite; data: MongoDB; infrastructure: AWS SDK; GitHub Actions; integrations: OpenAI API.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational data, lifecycle transitions, tenant-scoped queries, audit history; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masteridur/idurar-erp-crm/README.md), [routes.jsx](../../_Organized%20Desktop/03%20Master%20Projects/masteridur/idurar-erp-crm/frontend/src/router/routes.jsx), [server.js](../../_Organized%20Desktop/03%20Master%20Projects/masteridur/idurar-erp-crm/backend/src/server.js).

#### _Organized Desktop/03 Master Projects/masterindicoPYJS

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterindicoPYJS)

Indico event and conference management platform.

- **Stack:** languages: CSS; HTML; JavaScript; Python; SCSS; TypeScript; frameworks: Flask; React; data: PostgreSQL; Redis; SQLAlchemy; infrastructure: GitHub Actions; testing: Jest; integrations: Celery.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterindicoPYJS/indico/README.md), [controllers.py](../../_Organized%20Desktop/03%20Master%20Projects/masterindicoPYJS/indico/indico/modules/api/controllers.py), [app.py](../../_Organized%20Desktop/03%20Master%20Projects/masterindicoPYJS/indico/indico/web/flask/app.py).

#### _Organized Desktop/03 Master Projects/masterlink

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterlink)

Linkwarden bookmark collection and webpage-archiving reference application.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Expo; Next.js; Node.js; React; React Native; Tailwind CSS; data: Prisma; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Jest; Playwright; Vitest; integrations: Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterlink/linkwarden/README.md), [getUsers.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterlink/linkwarden/apps/web/lib/api/controllers/users/getUsers.ts), [package.json](../../_Organized%20Desktop/03%20Master%20Projects/masterlink/linkwarden/package.json).

#### _Organized Desktop/03 Master Projects/mastermatter

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/mastermatter)

Mattermost team messaging and collaboration platform.

- **Stack:** languages: CSS; Go; HTML; JavaScript; SCSS; SQL; TypeScript; frameworks: Express; Node.js; React; data: PostgreSQL; Redis; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Cypress; Jest; Playwright.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event/state modeling, real-time synchronization, validation, reconnect behavior; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/mastermatter/mattermost/README.md), [main.go](../../_Organized%20Desktop/03%20Master%20Projects/mastermatter/mattermost/api/server/main.go).

#### _Organized Desktop/03 Master Projects/mastermayan

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/mastermayan)

Mayan EDMS is a document management system.

- **Stack:** languages: CSS; HTML; JavaScript; Python; data: Redis; infrastructure: Docker; integrations: Celery.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** file validation, access control, asynchronous processing, retries; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/mastermayan/Mayan-EDMS/README.md), [handlers.py](../../_Organized%20Desktop/03%20Master%20Projects/mastermayan/Mayan-EDMS/mayan/apps/ocr/handlers.py), [requirements.txt](../../_Organized%20Desktop/03%20Master%20Projects/mastermayan/Mayan-EDMS/requirements.txt).

#### _Organized Desktop/03 Master Projects/mastermorphic

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/mastermorphic)

An AI-powered search engine with a generative UI.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Drizzle; Redis; Supabase; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/mastermorphic/morphic/README.md), [keyboard-shortcut-handler.tsx](../../_Organized%20Desktop/03%20Master%20Projects/mastermorphic/morphic/components/keyboard-shortcut-handler.tsx), [server.ts](../../_Organized%20Desktop/03%20Master%20Projects/mastermorphic/morphic/lib/supabase/server.ts).

#### _Organized Desktop/03 Master Projects/masternext

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masternext)

NextCRM is an open-source CRM built with Next.js 16, React 19, TypeScript, PostgreSQL (Prisma 7), and shadcn/ui.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: MongoDB; PostgreSQL; Prisma; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Jest; Playwright; integrations: MCP; OpenAI API.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational data, lifecycle transitions, tenant-scoped queries, audit history; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masternext/nextcrm-app/README.md), [nav-user.tsx](../../_Organized%20Desktop/03%20Master%20Projects/masternext/nextcrm-app/app/%5Blocale%5D/%28routes%29/components/nav-user.tsx), [package.json](../../_Organized%20Desktop/03%20Master%20Projects/masternext/nextcrm-app/package.json).

#### _Organized Desktop/03 Master Projects/masternovu

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masternovu)

Novu notification infrastructure and in-app inbox platform.

- **Stack:** languages: CSS; HTML; JavaScript; Python; SQL; TypeScript; frameworks: Express; NestJS; Next.js; Node.js; React; Tailwind CSS; Vite; data: MongoDB; Redis; infrastructure: AWS SDK; Azure SDK; Docker; GitHub Actions; testing: Jest; Playwright; Vitest; integrations: BullMQ; Socket.IO.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masternovu/novu/README.md), [auth.tsx](../../_Organized%20Desktop/03%20Master%20Projects/masternovu/novu/apps/dashboard/src/routes/auth.tsx), [user.service.ts](../../_Organized%20Desktop/03%20Master%20Projects/masternovu/novu/playground/nestjs/src/user.service.ts).

#### _Organized Desktop/03 Master Projects/masteropen

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masteropen)

The open-source status page and uptime monitoring platform.

- **Stack:** languages: CSS; Go; JavaScript; SQL; TypeScript; frameworks: Astro; Hono; Next.js; Node.js; React; Tailwind CSS; data: Drizzle; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Playwright; integrations: MCP; Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event schemas, ingestion, aggregation, alerting, operational failure states; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masteropen/openstatus/README.md), [server.ts](../../_Organized%20Desktop/03%20Master%20Projects/masteropen/openstatus/apps/server/src/routes/mcp/server.ts), [package.json](../../_Organized%20Desktop/03%20Master%20Projects/masteropen/openstatus/package.json).

#### _Organized Desktop/03 Master Projects/masteropenedxPYJS

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masteropenedxPYJS)

Purpose The Open edX Platform enables the authoring and delivery of online learning at any scale.

- **Stack:** languages: CSS; HTML; JavaScript; Python; SCSS; TypeScript; frameworks: Django; React; infrastructure: GitHub Actions; testing: Jest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [services.py](../../_Organized%20Desktop/03%20Master%20Projects/masteropenedxPYJS/openedx-platform/xmodule/services.py), [README.rst](../../_Organized%20Desktop/03%20Master%20Projects/masteropenedxPYJS/openedx-platform/README.rst).

#### _Organized Desktop/03 Master Projects/masterpaper

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterpaper)

Paperless-ngx is a document management system that transforms your physical documents into a searchable online archive so you can keep, well, less paper.

- **Stack:** languages: CSS; HTML; JavaScript; Python; SCSS; TypeScript; frameworks: Angular; Django; Tailwind CSS; data: MySQL; PostgreSQL; Redis; infrastructure: Docker; GitHub Actions; testing: Jest; Playwright; integrations: Celery; OpenAI API.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** file validation, access control, asynchronous processing, retries; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterpaper/paperless-ngx/README.md), [chat.service.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterpaper/paperless-ngx/src-ui/src/app/services/chat.service.ts), [Dockerfile](../../_Organized%20Desktop/03%20Master%20Projects/masterpaper/paperless-ngx/Dockerfile).

#### _Organized Desktop/03 Master Projects/masterplane

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterplane)

Modern project management for all teams

- **Stack:** languages: CSS; HTML; JavaScript; Python; TypeScript; frameworks: Express; Node.js; React; Vite; data: Redis; infrastructure: Docker; GitHub Actions; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational CRUD, ordering, optimistic UI, project permissions; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterplane/plane/README.md), [user.service.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterplane/plane/apps/live/src/services/user.service.ts), [server.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterplane/plane/apps/live/src/server.ts).

#### _Organized Desktop/03 Master Projects/masterpload

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterpload)

Payload TypeScript CMS and application framework.

- **Stack:** languages: CSS; HTML; JavaScript; SCSS; TypeScript; frameworks: Express; Next.js; Node.js; React; Tailwind CSS; data: Drizzle; MongoDB; PostgreSQL; SQLite; infrastructure: AWS SDK; Azure SDK; Docker; GitHub Actions; testing: Playwright; Vitest; integrations: MCP.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** content modeling, revisions, authorization, search, optimistic concurrency; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterpload/payload/README.md), [index.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterpload/payload/packages/next/src/routes/index.ts), [confirmOrder.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterpload/payload/packages/plugin-ecommerce/src/endpoints/confirmOrder.ts).

#### _Organized Desktop/03 Master Projects/masterpostiz

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterpostiz)

Postiz social-media scheduling and publishing application.

- **Stack:** languages: CSS; JavaScript; SCSS; TypeScript; frameworks: NestJS; Next.js; Node.js; React; Tailwind CSS; Vite; data: Prisma; Redis; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Jest; Vitest; integrations: MCP; OpenAI API; Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** date/time modeling, interval conflicts, transactional booking, cancellation; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterpostiz/postiz-app/README.md), [auth.service.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterpostiz/postiz-app/libraries/helpers/src/auth/auth.service.ts), [package.json](../../_Organized%20Desktop/03%20Master%20Projects/masterpostiz/postiz-app/package.json).

#### _Organized Desktop/03 Master Projects/masterpre

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterpre)

pretalx conference proposal, speaker, and schedule management.

- **Stack:** languages: CSS; HTML; JavaScript; Python; Vue; frameworks: Django; Vite; Vue; data: Redis; infrastructure: GitHub Actions; testing: pytest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** date/time modeling, interval conflicts, transactional booking, cancellation; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [auth.py](../../_Organized%20Desktop/03%20Master%20Projects/masterpre/pretalx/src/pretalx/api/auth.py), [README.rst](../../_Organized%20Desktop/03%20Master%20Projects/masterpre/pretalx/README.rst).

#### _Organized Desktop/03 Master Projects/mastersaleorPY

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/mastersaleorPY)

Commerce that works with your language and stack

- **Stack:** languages: HTML; Python; frameworks: Django; data: PostgreSQL; Redis; infrastructure: Docker; GitHub Actions; testing: pytest; integrations: Celery; Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational modeling, pricing, stock reservations, order state transitions; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/mastersaleorPY/saleor/README.md), [asgi_handler.py](../../_Organized%20Desktop/03%20Master%20Projects/mastersaleorPY/saleor/saleor/asgi/asgi_handler.py), [app.py](../../_Organized%20Desktop/03%20Master%20Projects/mastersaleorPY/saleor/saleor/graphql/app/dataloaders/app.py).

#### _Organized Desktop/03 Master Projects/mastershadcn

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/mastershadcn)

A set of components that you can customize, extend, and build on.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Astro; Next.js; Node.js; React; Tailwind CSS; Vite; infrastructure: GitHub Actions; testing: Vitest; integrations: MCP.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/mastershadcn/ui/README.md), [routes.ts](../../_Organized%20Desktop/03%20Master%20Projects/mastershadcn/ui/templates/react-router-app/app/routes.ts), [App.tsx](../../_Organized%20Desktop/03%20Master%20Projects/mastershadcn/ui/templates/vite-app/src/App.tsx).

#### _Organized Desktop/03 Master Projects/MasterStore

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/MasterStore)

A , headless ecommerce storefront for Spree Commerce, built with Next.js 16, React 19, and the Spree REST API.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; infrastructure: GitHub Actions; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational modeling, pricing, stock reservations, order state transitions; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/MasterStore/storefront/README.md), [handlers.ts](../../_Organized%20Desktop/03%20Master%20Projects/MasterStore/storefront/src/lib/webhooks/handlers.ts), [package.json](../../_Organized%20Desktop/03%20Master%20Projects/MasterStore/storefront/package.json).

#### _Organized Desktop/03 Master Projects/mastersupa

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/mastersupa)

Supabase is the Postgres development platform.

- **Stack:** languages: CSS; Dart; HTML; JavaScript; Kotlin; SQL; TypeScript; Vue; frameworks: Next.js; Node.js; Nuxt; React; Tailwind CSS; Vite; Vue; data: Supabase; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Playwright; Vitest; integrations: MCP; OpenAI API; Twilio.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/mastersupa/supabase/README.md), [routes.ts](../../_Organized%20Desktop/03%20Master%20Projects/mastersupa/supabase/apps/lite-studio/app/routes.ts), [server.ts](../../_Organized%20Desktop/03%20Master%20Projects/mastersupa/supabase/apps/ui-library/registry/default/clients/nextjs/lib/supabase/server.ts).

#### _Organized Desktop/03 Master Projects/mastertea

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/mastertea)

Manage Your Data & Connect Your Team Teable uses a simple, spreadsheet-like interface to create database applications.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Express; NestJS; Next.js; Node.js; React; Tailwind CSS; data: PostgreSQL; Prisma; Redis; infrastructure: AWS SDK; GitHub Actions; testing: Playwright; Vitest; integrations: BullMQ.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/mastertea/teable/README.md), [UserLookupService.ts](../../_Organized%20Desktop/03%20Master%20Projects/mastertea/teable/packages/v2/core/src/ports/UserLookupService.ts), [App.tsx](../../_Organized%20Desktop/03%20Master%20Projects/mastertea/teable/apps/nextjs-app/src/features/app/blocks/App.tsx).

#### _Organized Desktop/03 Master Projects/mastertool

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/mastertool)

ToolJet is the open-source foundation of ToolJet AI - the AI-native platform for building and deploying internal tools, workflows and AI agents.

- **Stack:** languages: CSS; HTML; JavaScript; SCSS; TypeScript; frameworks: NestJS; Node.js; React; Tailwind CSS; data: PostgreSQL; Redis; infrastructure: Docker; GitHub Actions; Terraform; testing: Cypress; Jest; integrations: Anthropic API; BullMQ; Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/mastertool/tooljet/README.md), [AuthRoute.jsx](../../_Organized%20Desktop/03%20Master%20Projects/mastertool/tooljet/frontend/src/Routes/AuthRoute.jsx), [App.jsx](../../_Organized%20Desktop/03%20Master%20Projects/mastertool/tooljet/frontend/src/App/App.jsx).

#### _Organized Desktop/03 Master Projects/mastertwenty

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/mastertwenty)

Twenty open-source CRM with customer records, workflows, and team views.

- **Stack:** languages: CSS; HTML; JavaScript; Python; SQL; TypeScript; frameworks: Electron; Express; Node.js; React; Vite; infrastructure: GitHub Actions; Terraform; testing: Jest; Playwright; Vitest; integrations: Anthropic API; OpenAI API.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/mastertwenty/twenty/README.md), [AuthService.ts](../../_Organized%20Desktop/03%20Master%20Projects/mastertwenty/twenty/packages/twenty-front/src/modules/auth/services/AuthService.ts), [server.js](../../_Organized%20Desktop/03%20Master%20Projects/mastertwenty/twenty/packages/twenty-companion/src/server.js).

#### _Organized Desktop/03 Master Projects/mastertypebot

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/mastertypebot)

Typebot is a Fair Source chatbot builder.

- **Stack:** languages: CSS; JavaScript; PHP; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; Vite; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Playwright; integrations: OpenAI API; Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** external API boundaries, streaming, deterministic evaluation, retries, human review; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/mastertypebot/typebot.io/README.md), [index.tsx](../../_Organized%20Desktop/03%20Master%20Projects/mastertypebot/typebot.io/apps/landing-page/src/routes/index.tsx), [getUsersHandler.ts](../../_Organized%20Desktop/03%20Master%20Projects/mastertypebot/typebot.io/packages/forge/blocks/blink/src/handlers/getUsersHandler.ts).

#### _Organized Desktop/03 Master Projects/masterumami

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterumami)

Umami is a simple, fast, privacy-focused alternative to Google Analytics.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; data: PostgreSQL; Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Cypress; Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event modeling, aggregation, reporting queries, deduplication; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterumami/umami/README.md), [auth.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterumami/umami/src/lib/auth.ts), [App.tsx](../../_Organized%20Desktop/03%20Master%20Projects/masterumami/umami/src/app/%28main%29/App.tsx).

#### _Organized Desktop/03 Master Projects/masterzulipPY

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterzulipPY)

Zulip is an open-source organized team chat app with unique [topic-based threading][why-zulip] that combines the best of email and chat to make remote work productive and delightful.

- **Stack:** languages: CSS; HTML; JavaScript; Python; Ruby; SQL; TypeScript; frameworks: Astro; Django; Vite; data: Firebase; MongoDB; PostgreSQL; Redis; SQLAlchemy; infrastructure: AWS SDK; Docker; GitHub Actions; integrations: OpenAI API; Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event/state modeling, real-time synchronization, validation, reconnect behavior; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/03%20Master%20Projects/masterzulipPY/zulip/README.md), [click_handlers.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterzulipPY/zulip/web/src/click_handlers.ts), [package.json](../../_Organized%20Desktop/03%20Master%20Projects/masterzulipPY/zulip/package.json).

#### _Organized Desktop/03 Master Projects/masterrnative

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/03%20Master%20Projects/masterrnative)

Expo farm-batch tracker for feed, mortality, expenses, and sales.

- **Stack:** languages: JavaScript; TypeScript; frameworks: Expo; React; React Native; testing: Playwright.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** Expo/React Native forms, farm-batch data, local/mobile persistence, mobile UX
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Trace one feed/expense record through the mobile UI and storage; handle interrupted input and offline state.
- **Evidence:** [storageService.ts](../../_Organized%20Desktop/03%20Master%20Projects/masterrnative/src/services/storageService.ts), [App.tsx](../../_Organized%20Desktop/03%20Master%20Projects/masterrnative/App.tsx).

<a id="location-organized-desktop-04-javascript-training"></a>

### _Organized Desktop/04 JavaScript Training

#### _Organized Desktop/04 JavaScript Training/jstrain2.2

**Stage 1: Language and browser foundations. Core journey candidate.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.2)

A personal coding bootcamp for leveling up software engineering fundamentals, in two languages.

- **Stack:** languages: C#; CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Express; Node.js; React; Vite; data: SQLite; infrastructure: Docker; GitHub Actions; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified. Limits: This is a large curriculum workspace, not one app to complete end-to-end. Exercise TODOs are intentional.
- **Learn:** 29 JS modules, Node/SQL/testing, a TypeScript track, nested C# web curriculum, and three portfolio workspaces
- **Before starting:** Editor, terminal, Git basics; variables, loops, and functions.
- **Next:** Use FLIGHTPLAN.md for core JS, then FLIGHTPLAN-NODE-TS.md for Node/TypeScript; select reinforcement modules as needed, then one of three portfolio projects.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.2/README.md), [07-error-handler.js](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.2/bootcamp/18-node-http-apis/exercises/07-error-handler.js), [App.tsx](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.2/portfolio-projects/01-inventory-orders/apps/web/src/App.tsx).

#### _Organized Desktop/04 JavaScript Training/trainjs

**Stage 1: Language and browser foundations. Core journey candidate.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/trainjs)

Docs-first JavaScript training course for a learner who already understands basic programming ideas but needs stronger JavaScript skills to become competitive for a junior software engineering role.

- **Stack:** .
- **Review:** Learning/reference material; no source implementation indexed.
- **Learn:** language fluency, decomposition, collections, errors, debugging, test feedback
- **Before starting:** Editor, terminal, Git basics; variables, loops, and functions.
- **Next:** Follow lessons 01-10 in order, complete labs before solutions, then build the capstone; defer advanced lesson 11 until the full-stack milestone.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/trainjs/README.md), [course-overview.md](../../_Organized%20Desktop/04%20JavaScript%20Training/trainjs/docs/course-overview.md).

#### _Organized Desktop/04 JavaScript Training/jstrain2.3

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.3)

A Notion-style collaborative workspace built with Next.js (App Router), SQLite, Zustand, dnd-kit, and Fuse.js.

- **Stack:** languages: CSS; JavaScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; SQLite.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** content modeling, revisions, authorization, search, optimistic concurrency
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Trace an edit and test a stale revision or forbidden share.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.3/README.md), [page.js](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.3/src/app/page.js), [package.json](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.3/package.json).

#### _Organized Desktop/04 JavaScript Training/react

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/react)

Small browser-based Jeopardy game.

- **Stack:** languages: CSS; HTML; JavaScript.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event/state modeling, real-time synchronization, validation, reconnect behavior
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Isolate a game/message state transition and specify duplicate-event/reconnect tests.
- **Evidence:** [data.js](../../_Organized%20Desktop/04%20JavaScript%20Training/react/data.js).

#### _Organized Desktop/04 JavaScript Training/jsdrillapp

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/jsdrillapp)

Reps coding-practice app for building programming fluency through repeated exercises.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Drizzle; SQLite.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/jsdrillapp/reps/README.md), [fsrs.ts](../../_Organized%20Desktop/04%20JavaScript%20Training/jsdrillapp/reps/src/lib/fsrs.ts), [package.json](../../_Organized%20Desktop/04%20JavaScript%20Training/jsdrillapp/reps/package.json).

#### _Organized Desktop/04 JavaScript Training/jstrain1

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain1)

Full-stack JavaScript practice application for tenant-scoped administrative operations.

- **Stack:** languages: CSS; HTML; JavaScript; frameworks: Express; Node.js; React; Vite; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** sessions, tenant isolation, schemas, validation, authorization
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one protected mutation and design cross-tenant read/write denial tests.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain1/README.md), [authRoutes.js](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain1/server/src/routes/authRoutes.js), [App.jsx](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain1/web/src/App.jsx).

#### _Organized Desktop/04 JavaScript Training/jstrain5

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain5)

OpsForge is an internal operations dashboard for NovaCom (fictional telecom/SaaS company).

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Drizzle; PostgreSQL; Redis; infrastructure: Docker; integrations: BullMQ.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain5/README.md), [service.ts](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain5/src/lib/runbooks/service.ts), [package.json](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain5/package.json).

#### _Organized Desktop/04 JavaScript Training/rewritepy2js

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/rewritepy2js)

FastAPI codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the RealWorld spec and API.

- **Stack:** languages: Python; SQL; TypeScript; frameworks: Express; FastAPI; Node.js; data: PostgreSQL; Prisma; SQLAlchemy; infrastructure: Docker; testing: Jest; pytest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/rewritepy2js/fastapi-realworld-example-app/README.md), [auth.ts](../../_Organized%20Desktop/04%20JavaScript%20Training/rewritepy2js/fastapi-realworld-example-app/src/routes/auth.ts), [main.py](../../_Organized%20Desktop/04%20JavaScript%20Training/rewritepy2js/fastapi-realworld-example-app/app/main.py).

#### _Organized Desktop/04 JavaScript Training/jsdrill_sync_20260223_125137

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/jsdrill_sync_20260223_125137)

A Next.js app for deliberate JavaScript practice with spaced repetition, pattern tracking, and progress analytics.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Drizzle; SQLite.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event modeling, aggregation, reporting queries, deduplication
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Validate one metric against a small hand-calculated dataset including duplicates.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/jsdrill_sync_20260223_125137/README.md), [fsrs.ts](../../_Organized%20Desktop/04%20JavaScript%20Training/jsdrill_sync_20260223_125137/src/lib/fsrs.ts), [package.json](../../_Organized%20Desktop/04%20JavaScript%20Training/jsdrill_sync_20260223_125137/package.json).

#### _Organized Desktop/04 JavaScript Training/jstrain2

**Stage 5: Domain rules and reliability. Core journey candidate.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2)

Workflow automation app with retries, queues, and execution logs; its README also documents an agent watchdog.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Drizzle; PostgreSQL; Redis; infrastructure: Docker; testing: Playwright; Vitest; integrations: BullMQ.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2/README.md), [route.ts](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2/src/app/api/webhooks/incoming/%5BendpointId%5D/route.ts), [package.json](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2/package.json).

#### _Organized Desktop/04 JavaScript Training/jstrain2.4

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.4)

Internal developer platform MVP inspired by Heroku/Vercel workflows.

- **Stack:** languages: CSS; JavaScript; SQL; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.4/README.md), [route.js](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.4/app/api/audit/route.js), [platform-service.js](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.4/lib/platform-service.js).

#### _Organized Desktop/04 JavaScript Training/jstrain3

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain3)

Workspace with three DeskPilot variants; root README is a generic Next.js starter, so compare nested implementations before choosing one.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Redis; infrastructure: Docker.
- **Review:** Source implementation is indexed; runtime behavior remains unverified. Limits: Fresh source check: root page is the default Next.js starter; deskpilot-clean auth selects a fixed seeded user, not a login session.
- **Learn:** event modeling, aggregation, reporting queries, deduplication
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Compare deskpilot, deskpilot-app, and deskpilot-clean; select one implemented flow and replace demo identity only as a later exercise.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain3/README.md), [page.tsx](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain3/src/app/page.tsx), [auth.ts](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain3/deskpilot-clean/src/lib/auth.ts).

#### _Organized Desktop/04 JavaScript Training/jstrain3.0

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain3.0)

Ecommerce practice app with feature flags and experiments.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; frameworks: Express; Node.js; React; Vite; data: SQLite.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** rule evaluation, rollout consistency, cache invalidation, audit history
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Test deterministic targeting, rollback, and stale configuration behavior.
- **Evidence:** [auth.js](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain3.0/server/src/routes/auth.js), [App.jsx](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain3.0/client/src/App.jsx).

#### _Organized Desktop/04 JavaScript Training/reactbullet

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/reactbullet)

A simple, scalable, and architecture for building production ready React applications.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Next.js; Node.js; React; Tailwind CSS; Vite; infrastructure: GitHub Actions; testing: Playwright; Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/reactbullet/bulletproof-react/README.md), [landing.tsx](../../_Organized%20Desktop/04%20JavaScript%20Training/reactbullet/bulletproof-react/apps/react-vite/src/app/routes/landing.tsx), [users.tsx](../../_Organized%20Desktop/04%20JavaScript%20Training/reactbullet/bulletproof-react/apps/react-vite/src/app/routes/app/users.tsx).

#### _Organized Desktop/04 JavaScript Training/jep vs code

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/04%20JavaScript%20Training/jep%20vs%20code)

A full-stack Jeopardy game web application with a React frontend and Node.js/Express backend.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Express; Node.js; React; Vite; data: Prisma; testing: Jest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event/state modeling, real-time synchronization, validation, reconnect behavior
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Isolate a game/message state transition and specify duplicate-event/reconnect tests.
- **Evidence:** [README.md](../../_Organized%20Desktop/04%20JavaScript%20Training/jep%20vs%20code/Jeopardy-Game/README.md), [auth.ts](../../_Organized%20Desktop/04%20JavaScript%20Training/jep%20vs%20code/jeopardy-rebuild/backend/src/routes/auth.ts), [App.jsx](../../_Organized%20Desktop/04%20JavaScript%20Training/jep%20vs%20code/Jeopardy-Game/frontend/src/App.jsx).

<a id="location-organized-desktop-05-numbered-experiments"></a>

### _Organized Desktop/05 Numbered Experiments

#### _Organized Desktop/05 Numbered Experiments/J1

**Stage 1: Language and browser foundations. Optional Java fundamentals project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/J1)

CLI To-Do Manager: plain-Java task CRUD with OOP separation and text-file persistence.

- **Stack:** languages: Java.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Learn:** language fluency, decomposition, collections, errors, debugging, test feedback
- **Before starting:** Editor, terminal, Git basics; variables, loops, and functions.
- **Next:** Follow the documented exercise order; solve one prompt before reading its solution.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/J1/README.md), [App.java](../../_Organized%20Desktop/05%20Numbered%20Experiments/J1/src/todo/App.java), [TaskManager.java](../../_Organized%20Desktop/05%20Numbered%20Experiments/J1/src/todo/service/TaskManager.java).

#### _Organized Desktop/05 Numbered Experiments/j2

**Stage 1: Language and browser foundations. Optional Java fundamentals project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/j2)

Library Book Tracker: plain-Java CLI for books, borrowers, checkout/return, and local file persistence.

- **Stack:** languages: Java.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Learn:** language fluency, decomposition, collections, errors, debugging, test feedback
- **Before starting:** Editor, terminal, Git basics; variables, loops, and functions.
- **Next:** Follow the documented exercise order; solve one prompt before reading its solution.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/j2/README.md), [App.java](../../_Organized%20Desktop/05%20Numbered%20Experiments/j2/src/librarytracker/App.java), [LibraryManager.java](../../_Organized%20Desktop/05%20Numbered%20Experiments/j2/src/librarytracker/service/LibraryManager.java).

#### _Organized Desktop/05 Numbered Experiments/j3

**Stage 1: Language and browser foundations. Optional Java fundamentals project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/j3)

Java command-line bank-account simulator with saved account data.

- **Stack:** languages: Java.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** language fluency, decomposition, collections, errors, debugging, test feedback
- **Before starting:** Editor, terminal, Git basics; variables, loops, and functions.
- **Next:** Follow the documented exercise order; solve one prompt before reading its solution.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/j3/README.md), [App.java](../../_Organized%20Desktop/05%20Numbered%20Experiments/j3/src/bankapp/App.java), [BankService.java](../../_Organized%20Desktop/05%20Numbered%20Experiments/j3/src/bankapp/service/BankService.java).

#### _Organized Desktop/05 Numbered Experiments/j4

**Stage 1: Language and browser foundations. Optional Java fundamentals project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/j4)

Small command-line quiz application written in plain Java.

- **Stack:** languages: Java.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** language fluency, decomposition, collections, errors, debugging, test feedback
- **Before starting:** Editor, terminal, Git basics; variables, loops, and functions.
- **Next:** Follow the documented exercise order; solve one prompt before reading its solution.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/j4/README.md), [App.java](../../_Organized%20Desktop/05%20Numbered%20Experiments/j4/src/quiz/App.java).

#### _Organized Desktop/05 Numbered Experiments/j5

**Stage 1: Language and browser foundations. Optional Java fundamentals project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/j5)

A small command-line Java project for recording expenses, filtering them, and viewing spending summaries.

- **Stack:** languages: Java.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Learn:** language fluency, decomposition, collections, errors, debugging, test feedback
- **Before starting:** Editor, terminal, Git basics; variables, loops, and functions.
- **Next:** Follow the documented exercise order; solve one prompt before reading its solution.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/j5/README.md), [App.java](../../_Organized%20Desktop/05%20Numbered%20Experiments/j5/src/expensetracker/App.java).

#### _Organized Desktop/05 Numbered Experiments/j7

**Stage 1: Language and browser foundations. Optional Java fundamentals project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/j7)

A beginner-friendly command-line Order Management System written in plain Java 17.

- **Stack:** languages: Java.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** language fluency, decomposition, collections, errors, debugging, test feedback
- **Before starting:** Editor, terminal, Git basics; variables, loops, and functions.
- **Next:** Follow the documented exercise order; solve one prompt before reading its solution.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/j7/README.md), [OrderService.java](../../_Organized%20Desktop/05%20Numbered%20Experiments/j7/src/oms/service/OrderService.java).

#### _Organized Desktop/05 Numbered Experiments/g1

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/g1)

Bagel Atlas directory for exploring bagel shops and cities.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Drizzle; integrations: Anthropic API.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** forms, client state, data transforms, search/filtering, API error states
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Build or explain one complete user interaction with empty/loading/error behavior.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/g1/README.md), [env.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/g1/src/lib/env.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/g1/package.json).

#### _Organized Desktop/05 Numbered Experiments/X1

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/X1)

A TypeScript app for discovering, ranking, and operating bagel shop data across multiple cities.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: SQLite.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** forms, client state, data transforms, search/filtering, API error states
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Build or explain one complete user interaction with empty/loading/error behavior.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/X1/bagel-intel-platform/README.md), [db.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/X1/bagel-intel-platform/src/lib/db.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/X1/bagel-intel-platform/package.json).

#### _Organized Desktop/05 Numbered Experiments/z9

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/z9)

Freelancer and agency operations portal.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Learn:** semantic HTML, component composition, forms, integration boundaries
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Review one page/form for keyboard use and predictable validation; isolate one integration.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/z9/README.md), [service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/z9/src/modules/auth/service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/z9/package.json).

#### _Organized Desktop/05 Numbered Experiments/D1

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/D1)

Real-time kanban project-board application.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Drizzle; PostgreSQL; Redis; integrations: Socket.IO.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational CRUD, ordering, optimistic UI, project permissions
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Implement one board/task operation and test ordering plus permission boundaries.
- **Evidence:** [auth.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/D1/src/lib/services/auth.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/D1/package.json).

#### _Organized Desktop/05 Numbered Experiments/D3

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/D3)

Scaffold with Next.js 14, TypeScript, Auth.js v5, PostgreSQL, Drizzle, Stripe, Resend, Zod, and Tailwind.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Drizzle; integrations: Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/D3/README.md), [audit.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/D3/lib/services/audit.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/D3/package.json).

#### _Organized Desktop/05 Numbered Experiments/e11

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e11)

Roughflow visual board/editor application.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Vite; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [App.tsx](../../_Organized%20Desktop/05%20Numbered%20Experiments/e11/src/App.tsx), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/e11/package.json).

#### _Organized Desktop/05 Numbered Experiments/e15

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e15)

A pragmatic MVP for a multi-team support desk.

- **Stack:** languages: CSS; HTML; JavaScript; Python; frameworks: FastAPI; data: SQLAlchemy; testing: pytest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** route/service/repository boundaries, permissions, queue filters, workflow rules
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace ticket creation to storage; test forbidden transitions and unauthorized access.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/e15/README.md), [services.py](../../_Organized%20Desktop/05%20Numbered%20Experiments/e15/app/services.py), [main.py](../../_Organized%20Desktop/05%20Numbered%20Experiments/e15/app/main.py).

#### _Organized Desktop/05 Numbered Experiments/e17

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e17)

Forum application with moderation, trust levels, and discussion threads.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; SQLite; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/e17/README.md), [db.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/e17/src/lib/db.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/e17/package.json).

#### _Organized Desktop/05 Numbered Experiments/e2

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e2)

Northstar CMS is a learning-oriented, Strapi-style headless CMS scaffold built with Next.js and TypeScript.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS.
- **Review:** Teaching app with documented in-memory/mock persistence; database/schema claims do not establish durable storage. Runtime unverified.
- **Learn:** content modeling, revisions, authorization, search, optimistic concurrency
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace an edit and test a stale revision or forbidden share.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/e2/README.md), [page.tsx](../../_Organized%20Desktop/05%20Numbered%20Experiments/e2/src/app/page.tsx), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/e2/package.json).

#### _Organized Desktop/05 Numbered Experiments/e4

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e4)

Northstar Publish is a production-oriented publication platform built with Next.js, React, TypeScript, Prisma, PostgreSQL, Stripe, and BullMQ.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; Redis; infrastructure: AWS SDK; testing: Playwright; Vitest; integrations: BullMQ; Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** content modeling, revisions, authorization, search, optimistic concurrency
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace an edit and test a stale revision or forbidden share.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/e4/README.md), [service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/e4/src/server/auth/service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/e4/package.json).

#### _Organized Desktop/05 Numbered Experiments/e6

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e6)

Multi-tenant team-workspace scaffold for full-stack practice.

- **Stack:** languages: CSS; TypeScript; frameworks: Fastify; Next.js; Node.js; React; data: Prisma; integrations: Socket.IO.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Learn:** sessions, tenant isolation, schemas, validation, authorization
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one protected mutation and design cross-tenant read/write denial tests.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/e6/README.md), [auth.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/e6/apps/api/src/routes/auth.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/e6/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww12

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww12)

Omnichannel customer communications platform built with Next.js, TypeScript, PostgreSQL, Prisma, Tailwind, Zod, React Query, and REST APIs.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww12/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww12/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww12/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww16

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww16)

Channel Compass partner-relationship management scaffold with separated routes, validation, and business logic.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational data, lifecycle transitions, tenant-scoped queries, audit history
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace a lead/deal transition and test tenant isolation plus invalid transitions.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww16/docs/architecture/README.md), [mdfService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww16/src/services/mdfService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww16/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww17

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww17)

SignalDesk is a learning-oriented customer success and health scoring platform built with Next.js, TypeScript, React Query, Zod, and Prisma-style repository boundaries.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Learn:** relational data, lifecycle transitions, tenant-scoped queries, audit history
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace a lead/deal transition and test tenant isolation plus invalid transitions.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww17/README.md), [account-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww17/src/services/account-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww17/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww30

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww30)

QueryForge Workbench is a backend-first Next.js app for building safe dynamic queries over a constrained orders dataset.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww30/docs/architecture/README.md), [datasetService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww30/src/services/datasetService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww30/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww4

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww4)

WorkGrid is a Jira-like work management platform built to teach backend-oriented product engineering.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational CRUD, ordering, optimistic UI, project permissions
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Implement one board/task operation and test ordering plus permission boundaries.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww4/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww4/src/services/auth/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww4/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww40

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww40)

Single-platform job board admin dashboard built for backend-oriented CRUD learning.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** CRUD, filtering, authentication, validation, status transitions
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace a create/update flow and test ownership, validation, and one invalid transition.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww40/docs/architecture/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww40/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww40/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww43

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww43)

Notes application with version history, sharing, and conflict-aware saves.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** content modeling, revisions, authorization, search, optimistic concurrency
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace an edit and test a stale revision or forbidden share.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww43/README.md), [auth-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww43/src/services/auth-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww43/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww45

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww45)

Internal knowledge base built with Next.js, TypeScript, Prisma, PostgreSQL, Zod, Tailwind, and React Query.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** content modeling, revisions, authorization, search, optimistic concurrency
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace an edit and test a stale revision or forbidden share.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww45/README.md), [tagService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww45/src/services/tagService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww45/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww46

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww46)

Multi-tenant SaaS starter built with Next.js, TypeScript, Prisma, Tailwind, Zod, React Query, and REST APIs.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** sessions, tenant isolation, schemas, validation, authorization
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one protected mutation and design cross-tenant read/write denial tests.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww46/README.md), [auth-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww46/src/services/auth-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww46/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww48

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww48)

CRM lead pipeline built with Next.js, TypeScript, PostgreSQL, Prisma, Zod, Tailwind, React Query, and REST APIs.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational data, lifecycle transitions, tenant-scoped queries, audit history
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace a lead/deal transition and test tenant isolation plus invalid transitions.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww48/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww48/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww48/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww50

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww50)

API key management portal built around explicit tenant boundaries, service-layer business rules, and auditability.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww50/docs/architecture/README.md), [apiKeyService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww50/src/services/apiKeyService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww50/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww55

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww55)

Next.js admin dashboard for reviewing job postings, resolving moderation cases, and storing private saved searches.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** CRUD, filtering, authentication, validation, status transitions
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace a create/update flow and test ownership, validation, and one invalid transition.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww55/docs/architecture/README.md), [serviceDeps.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww55/src/services/serviceDeps.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww55/package.json).

#### _Organized Desktop/05 Numbered Experiments/z3

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/z3)

Two practice apps: a founder CRM and a customer-feedback board.

- **Stack:** languages: CSS; TypeScript; frameworks: Next.js; Node.js; React.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational data, lifecycle transitions, tenant-scoped queries, audit history
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace a lead/deal transition and test tenant isolation plus invalid transitions.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/z3/README.md), [service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/z3/founder-crm-lite/src/modules/crm/service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/z3/customer-feedback-board/package.json).

#### _Organized Desktop/05 Numbered Experiments/z6

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/z6)

Northstar Atlas is a internal team wiki / knowledge base built to be both usable software and a studyable codebase.

- **Stack:** languages: CSS; SQL; TypeScript; frameworks: Next.js; Node.js; React; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** content modeling, revisions, authorization, search, optimistic concurrency
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace an edit and test a stale revision or forbidden share.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/z6/README.md), [service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/z6/src/modules/knowledge-base/service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/z6/package.json).

#### _Organized Desktop/05 Numbered Experiments/z7

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/z7)

Hiring-pipeline tracker.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** CRUD, filtering, authentication, validation, status transitions
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace a create/update flow and test ownership, validation, and one invalid transition.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/z7/README.md), [hiring-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/z7/src/features/shared/server/hiring-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/z7/package.json).

#### _Organized Desktop/05 Numbered Experiments/z8

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/z8)

Event-operations dashboard.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; infrastructure: Docker.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/z8/README.md), [auth.service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/z8/src/modules/auth/auth.service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/z8/package.json).

#### _Organized Desktop/05 Numbered Experiments/zz2

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz2)

A customer support ticketing system built to practice backend-heavy product engineering with Next.js, TypeScript, PostgreSQL, Prisma, Zod, React Query, and REST APIs.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** route/service/repository boundaries, permissions, queue filters, workflow rules
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace ticket creation to storage; test forbidden transitions and unauthorized access.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz2/README.md), [app-services.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz2/src/server/app-services.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz2/package.json).

#### _Organized Desktop/05 Numbered Experiments/zz3

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz3)

Support Hub is a customer support ticketing and queue management application for a single company.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: PostgreSQL; Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** route/service/repository boundaries, permissions, queue filters, workflow rules
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace ticket creation to storage; test forbidden transitions and unauthorized access.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz3/README.md), [sla-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz3/src/services/sla-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz3/package.json).

#### _Organized Desktop/05 Numbered Experiments/zz6

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz6)

Policy-management and acknowledgment portal with exceptions and reporting.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz6/README.md), [policy-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz6/src/services/policy-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz6/package.json).

#### _Organized Desktop/05 Numbered Experiments/zz9

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz9)

Internal case-management application with team queues and audit trails.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** case lifecycles, permissions, queues, audit trails
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace case assignment and test unauthorized queue access.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz9/docs/architecture/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz9/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz9/package.json).

#### _Organized Desktop/05 Numbered Experiments/B1

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/B1)

Incident-response workspace with runbooks and incident-management components.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event schemas, ingestion, aggregation, alerting, operational failure states
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one event or check into a dashboard and test duplicate/missing/late data.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/B1/README.md), [http.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/B1/src/lib/http.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/B1/package.json).

#### _Organized Desktop/05 Numbered Experiments/e1

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e1)

Pulseboard Scheduler is a dependency-light Next.js foundation for a Cal.com-style scheduling SaaS.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Redis; infrastructure: Docker.
- **Review:** Teaching app with documented in-memory/mock persistence; database/schema claims do not establish durable storage. Runtime unverified.
- **Learn:** date/time modeling, interval conflicts, transactional booking, cancellation
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Test overlapping bookings and a daylight-saving boundary on one booking flow.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/e1/README.md), [proxy.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/e1/src/proxy.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/e1/package.json).

#### _Organized Desktop/05 Numbered Experiments/e12

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e12)

A dependency-light reference implementation of a multi-project feature flag platform.

- **Stack:** languages: CSS; HTML; JavaScript.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** rule evaluation, rollout consistency, cache invalidation, audit history
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Test deterministic targeting, rollback, and stale configuration behavior.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/e12/README.md), [services.js](../../_Organized%20Desktop/05%20Numbered%20Experiments/e12/src/server/services.js), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/e12/package.json).

#### _Organized Desktop/05 Numbered Experiments/e13

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e13)

Headless commerce practice platform with multiple sales-channel concepts.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; SQLite; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational modeling, pricing, stock reservations, order state transitions
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace an order/reservation and test invalid transitions or repeated submissions.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/e13/README.md), [env.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/e13/src/lib/env.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/e13/package.json).

#### _Organized Desktop/05 Numbered Experiments/e14

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e14)

Single-node MVP for a multi-tenant observability platform covering logs, metrics, traces, dashboards, alerts, and pipelines.

- **Stack:** languages: Python; frameworks: FastAPI; data: SQLAlchemy; testing: pytest.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Learn:** event schemas, ingestion, aggregation, alerting, operational failure states
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one event or check into a dashboard and test duplicate/missing/late data.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/e14/README.md), [auth.py](../../_Organized%20Desktop/05%20Numbered%20Experiments/e14/app/services/auth.py), [main.py](../../_Organized%20Desktop/05%20Numbered%20Experiments/e14/app/main.py).

#### _Organized Desktop/05 Numbered Experiments/e3

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e3)

Signal Desk is a PostHog-style product analytics MVP built with Next.js, React, TypeScript, and Node-style server modules.

- **Stack:** languages: CSS; TypeScript; frameworks: Next.js; Node.js; React; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event modeling, aggregation, reporting queries, deduplication
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Validate one metric against a small hand-calculated dataset including duplicates.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/e3/README.md), [page.tsx](../../_Organized%20Desktop/05%20Numbered%20Experiments/e3/app/page.tsx), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/e3/package.json).

#### _Organized Desktop/05 Numbered Experiments/w22

**Stage 5: Domain rules and reliability. Core journey candidate.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/w22)

Next.js App Router application that teaches payment-system correctness through a service and repository split.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** money arithmetic, idempotency, webhook processing, transaction boundaries
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Read schema, permissions, paymentService, webhookService, reconciliationService in that order; test replayed creation and late provider events.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/w22/docs/architecture/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/w22/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/w22/package.json).

#### _Organized Desktop/05 Numbered Experiments/w24

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/w24)

Learning project for dynamic product behavior: versioned JSON configs, runtime rule evaluation, safe rollout, rollback, audit history, caching, and an admin UI that explains why a rule applied.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** rule evaluation, rollout consistency, cache invalidation, audit history
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Test deterministic targeting, rollback, and stale configuration behavior.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/w24/README.md), [audit-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/w24/src/services/audit-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/w24/package.json).

#### _Organized Desktop/05 Numbered Experiments/w25

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/w25)

Backend-heavy Next.js application that teaches distributed locking through a web product shape.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified. Limits: Architecture explicitly uses mockStore and x-demo-user-id; Prisma schema describes the production-shaped model, not deployed persistence.
- **Learn:** concurrency, leases, ownership tokens, failure recovery
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Study acquire/renew/release invariants, then compare ww26 for actual Prisma-backed locking boundaries.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/w25/docs/architecture/README.md), [lockService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/w25/src/services/lockService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/w25/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww1

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww1)

Workforce Access Ops combines Employer of Record workflows with identity and entitlement management in one multi-tenant SaaS codebase.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww1/docs/architecture/README.md), [workerService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww1/src/services/workerService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww1/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww10

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww10)

Loan origination and underwriting platform built with Next.js, TypeScript, PostgreSQL, Prisma, Tailwind, Zod, React Query, and REST APIs.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: PostgreSQL; Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; lifecycle transitions, scoped approvals and workflow invariants
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww10/README.md), [route-handler.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww10/src/lib/http/route-handler.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww10/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww11

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww11)

Next.js + TypeScript clinical trial participant tracking system with a backend-centered design.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; lifecycle transitions, scoped approvals and workflow invariants
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww11/docs/architecture/README.md), [auditService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww11/src/services/auditService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww11/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww13

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww13)

FluxGrant is a grant and funding lifecycle management platform built as a learning artifact for backend-oriented product engineering.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS.
- **Review:** Teaching app with documented in-memory/mock persistence; database/schema claims do not establish durable storage. Runtime unverified. Limits: README explicitly states Prisma/PostgreSQL/Zod/React Query were intentionally not installed; actual teaching implementation uses in-memory repositories and handwritten validation.
- **Learn:** code navigation, contracts, validation, testing; lifecycle transitions, scoped approvals and workflow invariants
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww13/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww13/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww13/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww14

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww14)

Multi-tenant learning management system focused on backend-oriented product engineering.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** enrollment/progress data, scoped permissions, policy rules, modular services
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one enrollment-to-completion flow and test an ineligible certification.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww14/docs/architecture/README.md), [courseService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww14/src/services/courseService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww14/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww15

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww15)

ClosingHub is a Next.js App Router application for real estate transaction and deal management.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; lifecycle transitions, scoped approvals and workflow invariants
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww15/docs/architecture/README.md), [listing-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww15/src/services/listing-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww15/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww18

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww18)

Tenant-aware quote-to-cash application built to teach backend product engineering.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational data, lifecycle transitions, tenant-scoped queries, audit history; lifecycle transitions, scoped approvals and workflow invariants
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace a lead/deal transition and test tenant isolation plus invalid transitions.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww18/docs/architecture/README.md), [order-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww18/src/services/order-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww18/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww19

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww19)

Flowkeeper is a Temporal-lite orchestration app built as one Next.js codebase with a separate worker entrypoint.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww19/docs/architecture/README.md), [auth-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww19/src/services/auth-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww19/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww26

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww26)

Locksmith Dashboard is a Next.js application that teaches distributed coordination with a database-backed lock manager, explicit RBAC, and an operational dashboard.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** concurrency, leases, ownership tokens, failure recovery
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** After w25, trace lockCoordinatorService through lockScopeRepository row locking and lockLeaseRepository; test stale ownership and contention.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww26/docs/architecture/README.md), [dashboardService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww26/src/services/dashboardService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww26/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww28

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww28)

Learning scaffold for a distributed file storage system with tenant isolation, multipart uploads, retries, signed downloads, quota tracking, and duplicated chunk storage.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** file validation, access control, asynchronous processing, retries
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one upload through storage and processing; specify retry and access-denial cases.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww28/docs/architecture/README.md), [fileService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww28/src/services/fileService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww28/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww29

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww29)

Next.js application for sending queued notifications over email, SMS, and push with retry logic, delivery history, user preferences, rate limiting, and an admin monitoring surface.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: PostgreSQL; Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event schemas, ingestion, aggregation, alerting, operational failure states
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one event or check into a dashboard and test duplicate/missing/late data.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww29/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww29/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww29/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww31

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww31)

Flagship is a Next.js control plane for runtime feature rollout.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** rule evaluation, rollout consistency, cache invalidation, audit history
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Test deterministic targeting, rollback, and stale configuration behavior.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww31/docs/architecture/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww31/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww31/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww34

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww34)

StayBound is a Next.js App Router application for searching listings, requesting bookings, approving stays, capturing mock payments, applying cancellation policies, and creating post-stay reviews.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Learn:** money arithmetic, idempotency, webhook processing, transaction boundaries
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace a charge or webhook and design a replay test that cannot double-apply it.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww34/docs/architecture/README.md), [reviewService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww34/src/services/reviewService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww34/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww35

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww35)

Appointment-booking application.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** date/time modeling, interval conflicts, transactional booking, cancellation
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Test overlapping bookings and a daylight-saving boundary on one booking flow.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww35/docs/architecture/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww35/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww35/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww36

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww36)

Single-store inventory reservation app.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational modeling, pricing, stock reservations, order state transitions
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace an order/reservation and test invalid transitions or repeated submissions.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww36/docs/architecture/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww36/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww36/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww37

**Stage 5: Domain rules and reliability. Core journey candidate.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww37)

This app is a small-store inventory reservation system built around three core workflows: create a hold, release a hold, and keep low-stock alerts in sync when inventory changes.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS.
- **Review:** Teaching app with documented in-memory/mock persistence; database/schema claims do not establish durable storage. Runtime unverified. Limits: Fresh architecture review explicitly confirms mocked in-memory persistence and fake session headers. Use it for business rules; use a durable follow-on for concurrency claims.
- **Learn:** relational modeling, pricing, stock reservations, order state transitions
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Test hold/release invariants in the small in-memory app; then compare ww36 or implement durable transactional storage.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww37/docs/architecture/README.md), [alertService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww37/src/services/alertService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww37/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww39

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww39)

Support-ticket workflow application with service and repository layers.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww39/docs/architecture/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww39/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww39/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww47

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww47)

Next.js application for event ingestion, daily aggregation jobs, and protected analytics views.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event modeling, aggregation, reporting queries, deduplication
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Validate one metric against a small hand-calculated dataset including duplicates.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww47/README.md), [auth-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww47/src/services/auth-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww47/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww49

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww49)

Order-operations dashboard with coupons, fulfillment, refunds, and audit services.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** relational modeling, pricing, stock reservations, order state transitions
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace an order/reservation and test invalid transitions or repeated submissions.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww49/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww49/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww49/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww5

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww5)

Workday-like enterprise People + Operations platform with explicit backend boundaries for employees, org hierarchy, compensation workflow, approvals, tasks, reporting, audit logs, and admin settings.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww5/docs/architecture/README.md), [taskService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww5/src/services/taskService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww5/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww6

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww6)

Cloud-cost allocation and chargeback dashboard.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event modeling, aggregation, reporting queries, deduplication
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Validate one metric against a small hand-calculated dataset including duplicates.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww6/README.md), [budgetService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww6/src/services/budgetService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww6/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww7

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww7)

FlowForge is a learning project for workflow automation.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww7/README.md), [auth-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww7/src/services/auth-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww7/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww8

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww8)

LedgerFlow is a document processing pipeline built with Next.js, TypeScript, Prisma, PostgreSQL, Zod, Tailwind, and React Query.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** file validation, access control, asynchronous processing, retries
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one upload through storage and processing; specify retry and access-denial cases.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww8/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww8/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww8/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww9

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww9)

WW9 is a scheduling and booking engine built with Next.js, TypeScript, Prisma, PostgreSQL, React Query, Tailwind, and Zod.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** date/time modeling, interval conflicts, transactional booking, cancellation
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Test overlapping bookings and a daylight-saving boundary on one booking flow.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww9/README.md), [bookingService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww9/src/services/bookingService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww9/package.json).

#### _Organized Desktop/05 Numbered Experiments/z1

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/z1)

Internal request-and-approval workflow application with mocked infrastructure.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/z1/README.md), [admin-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/z1/src/lib/services/admin-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/z1/package.json).

#### _Organized Desktop/05 Numbered Experiments/zz1

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz1)

Multi-tenant CRM with deal workflows and service-layer authorization.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz1/docs/architecture/README.md), [jobService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz1/src/services/jobService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz1/package.json).

#### _Organized Desktop/05 Numbered Experiments/zz4

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz4)

A enterprise workflow app for access requests, purchase requests, onboarding requests, and policy exceptions.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: PostgreSQL; Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz4/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz4/zz4/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz4/package.json).

#### _Organized Desktop/05 Numbered Experiments/zz55

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz55)

OpsPilot is a learning project that combines subscription billing administration with employee onboarding operations.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** money arithmetic, idempotency, webhook processing, transaction boundaries
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace a charge or webhook and design a replay test that cannot double-apply it.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz55/README.md), [jobService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz55/src/services/jobService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz55/package.json).

#### _Organized Desktop/05 Numbered Experiments/zz7

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz7)

Procurement dashboard for vendors, sourcing, purchase orders, and reporting.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; lifecycle transitions, scoped approvals and workflow invariants
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz7/README.md), [authService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz7/src/services/authService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz7/package.json).

#### _Organized Desktop/05 Numbered Experiments/zz8

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz8)

HRIS and employee-performance review workflows in one workspace.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: PostgreSQL; Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** state machines, workers, retry policies, idempotency, execution logs
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Specify a workflow retry after a partial failure and add one focused recovery test.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz8/README.md), [review-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz8/src/services/review-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz8/package.json).

#### _Organized Desktop/05 Numbered Experiments/e20

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/e20)

Modular ERP MVP foundation for small-to-mid-sized businesses, built as a TypeScript/Fastify API with a shared master-data and document engine.

- **Stack:** languages: TypeScript; frameworks: Fastify; Node.js; testing: Vitest.
- **Review:** Teaching app with documented in-memory/mock persistence; database/schema claims do not establish durable storage. Runtime unverified. Limits: README explicitly says the in-memory store resets when the server restarts.
- **Learn:** ERP domain modeling, document lifecycle, module contracts, transaction boundaries
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one documented user flow from entry point to stored state and make one bounded improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/e20/README.md), [erp-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/e20/src/domain/erp-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/e20/package.json).

#### _Organized Desktop/05 Numbered Experiments/rn1

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/rn1)

Bluesky social-app source workspace, including mobile/web client components.

- **Stack:** languages: CSS; Go; HTML; JavaScript; Kotlin; Swift; TypeScript; frameworks: Expo; Express; Node.js; React; React Native; Tailwind CSS; Vite; data: PostgreSQL; Redis; infrastructure: Docker; GitHub Actions; testing: Jest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code navigation, contracts, validation, testing; reading established code and bounded contributions
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/rn1/social-app/README.md), [routes.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/rn1/social-app/src/routes.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/rn1/social-app/package.json).

#### _Organized Desktop/05 Numbered Experiments/w21

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/w21)

PulseGate is a Next.js full-stack control plane and gateway runtime.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** API contracts, versioning, caching, indexing, service boundaries
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Follow one request across its boundary and test backward compatibility or cache invalidation.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/w21/docs/architecture/README.md), [page.tsx](../../_Organized%20Desktop/05%20Numbered%20Experiments/w21/src/app/routes/page.tsx), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/w21/package.json).

#### _Organized Desktop/05 Numbered Experiments/w23

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/w23)

Multi-tenant search and indexing system built with Next.js, TypeScript, Drizzle, PostgreSQL, Zod, and React Query.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Drizzle; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** API contracts, versioning, caching, indexing, service boundaries
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Follow one request across its boundary and test backward compatibility or cache invalidation.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/w23/docs/architecture/README.md), [searchService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/w23/src/services/searchService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/w23/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww27

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww27)

Learning app for evolving a public REST API over time without freezing the system in place.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** API contracts, versioning, caching, indexing, service boundaries
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Follow one request across its boundary and test backward compatibility or cache invalidation.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww27/docs/architecture/README.md), [api-version-service.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww27/src/services/api-version-service.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww27/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww3

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww3)

Next.js + React + TypeScript learning build for employer-of-record operations.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** tenant isolation, approval rules, audit history, module boundaries
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one employee approval and test both cross-tenant access and invalid state changes.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww3/docs/architecture/README.md), [jobService.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww3/src/services/jobService.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww3/package.json).

#### _Organized Desktop/05 Numbered Experiments/D2

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/D2)

This project implements a maintainable Next.js 14 application that runs structured AI code review in streaming mode.

- **Stack:** languages: CSS; TypeScript; frameworks: Next.js; Node.js; React; data: Drizzle; PostgreSQL; integrations: Anthropic API.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** external API boundaries, streaming, deterministic evaluation, retries, human review
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Use a deterministic provider fixture to specify success, cancellation, and failure behavior.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/D2/README.md), [page.tsx](../../_Organized%20Desktop/05%20Numbered%20Experiments/D2/src/app/page.tsx), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/D2/package.json).

#### _Organized Desktop/05 Numbered Experiments/ww32

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww32)

Workspace Wire Slack-style messaging application with route, service, and repository boundaries; see the assessment for implementation limits.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest; integrations: Socket.IO.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** event/state modeling, real-time synchronization, validation, reconnect behavior
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Isolate a game/message state transition and specify duplicate-event/reconnect tests.
- **Evidence:** [README.md](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww32/docs/architecture/README.md), [routeHandler.ts](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww32/src/lib/routeHandler.ts), [package.json](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww32/package.json).

<a id="location-organized-desktop-06-ai-and-learning"></a>

### _Organized Desktop/06 AI And Learning

#### _Organized Desktop/06 AI And Learning/ailearningpath

**Stage 0: Planning and reference collections. Learning/reference collection.** [Open folder](../../_Organized%20Desktop/06%20AI%20And%20Learning/ailearningpath)

Applied architecture and project-based software-engineering learning plans in two ODT documents.

- **Stack:** .
- **Review:** Learning/reference material; no source implementation indexed.
- **Learn:** architecture study and project-based learning planning
- **Before starting:** Language basics and the prior roadmap milestone.
- **Next:** Read the two ODT plans and choose one exercise linked to the current milestone.
- **Evidence:** [Codebase-Mastery-Applied-Architecture-Plan.odt](../../_Organized%20Desktop/06%20AI%20And%20Learning/ailearningpath/Codebase-Mastery-Applied-Architecture-Plan.odt).

#### _Organized Desktop/06 AI And Learning/learnpathclaude

**Stage 0: Planning and reference collections. Learning/reference collection.** [Open folder](../../_Organized%20Desktop/06%20AI%20And%20Learning/learnpathclaude)

Project-Based Architecture Learning Path: TypeScript/React/Next.js curriculum with one primary project, four reinforcement projects, and mini-exercises per phase.

- **Stack:** .
- **Review:** Learning/reference material; no source implementation indexed.
- **Learn:** study planning and reference organization
- **Before starting:** Language basics and the prior roadmap milestone.
- **Next:** Read the collection contents and attach one concrete coding exercise to the active milestone.
- **Evidence:** [project-based-learning-path.md](../../_Organized%20Desktop/06%20AI%20And%20Learning/learnpathclaude/project-based-learning-path.md).

#### _Organized Desktop/06 AI And Learning/claudeailab-temp

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab-temp)

Next.js starter retained alongside the AI-lab project; substantive app behavior was not established.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Drizzle; SQLite.
- **Review:** Source implementation is indexed; runtime behavior remains unverified. Limits: Generic Next.js starter.
- **Learn:** Next.js starter structure
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Prefer claudeailab for domain work; use this only for a clean scaffold comparison.
- **Evidence:** [README.md](../../_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab-temp/README.md), [next.config.ts](../../_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab-temp/next.config.ts), [page.tsx](../../_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab-temp/src/app/page.tsx).

#### _Organized Desktop/06 AI And Learning/claudeailab

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab)

A personal experiment tracker and skill progression system for evaluating AI-assisted coding tools, workflows, and techniques.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Drizzle; SQLite.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** experiment data modeling, CRUD, progress tracking, evaluation criteria
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Define one measurable experiment and trace how its result is stored and summarized.
- **Evidence:** [README.md](../../_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab/README.md), [seed.ts](../../_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab/src/db/seed.ts), [package.json](../../_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab/package.json).

#### _Organized Desktop/06 AI And Learning/ai-observer-reference

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/06%20AI%20And%20Learning/ai-observer-reference)

Track token usage, costs, API latency, error rates, and session activity across all your AI coding assistants in one unified dashboard—with real-time updates and zero external dependencies.

- **Stack:** languages: CSS; Go; HTML; JavaScript; TypeScript; frameworks: React; Tailwind CSS; Vite; infrastructure: Docker; GitHub Actions; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** telemetry collection, event normalization, metrics, operational dashboards
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace a session event into usage metrics and test duplicate-event handling.
- **Evidence:** [README.md](../../_Organized%20Desktop/06%20AI%20And%20Learning/ai-observer-reference/README.md), [App.tsx](../../_Organized%20Desktop/06%20AI%20And%20Learning/ai-observer-reference/frontend/src/App.tsx), [routes.go](../../_Organized%20Desktop/06%20AI%20And%20Learning/ai-observer-reference/backend/internal/server/routes.go).

#### _Organized Desktop/06 AI And Learning/aiapplybot

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybot)

ApplyPilot-derived job-application automation workspace with a six-stage pipeline and an extended auto-apply stage.

- **Stack:** languages: HTML; Python; infrastructure: GitHub Actions; testing: Playwright; pytest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** Python CLI pipelines, browser automation, LLM boundaries, review checkpoints
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Map the six pipeline stages; isolate stage-six automation behind deterministic fixtures.
- **Evidence:** [README.md](../../_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybot/ApplyPilot-main/README.md), [cli.py](../../_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybot/ApplyPilot-main/src/applypilot/cli.py), [jobspy.py](../../_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybot/ApplyPilot-main/src/applypilot/discovery/jobspy.py).

#### _Organized Desktop/06 AI And Learning/aiapplybotjs

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybotjs)

TypeScript/Node CLI implementing a six-stage job-search and application pipeline.

- **Stack:** languages: HTML; SQL; TypeScript; data: Drizzle; SQLite; testing: Playwright; Vitest; integrations: Anthropic API; OpenAI API.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** TypeScript CLI pipelines, async orchestration, provider adapters
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Compare one pipeline stage to the Python version and test retry/cancellation behavior.
- **Evidence:** [README.md](../../_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybotjs/README.md), [jobs.ts](../../_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybotjs/src/db/jobs.ts), [package.json](../../_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybotjs/package.json).

#### _Organized Desktop/06 AI And Learning/codehelper

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/06%20AI%20And%20Learning/codehelper)

Coding-assistance workspace combining an editor and LLM chat with uploaded-codebase browsing and generated explanations.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Express; Fastify; Next.js; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Vitest; integrations: OpenAI API.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** editor integration, code ingestion, API streaming, LLM error boundaries
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Trace upload-to-code-view and test one malformed archive or failed provider response.
- **Evidence:** [README.md](../../_Organized%20Desktop/06%20AI%20And%20Learning/codehelper/README.md), [chat.ts](../../_Organized%20Desktop/06%20AI%20And%20Learning/codehelper/server/routes/chat.ts), [server.ts](../../_Organized%20Desktop/06%20AI%20And%20Learning/codehelper/ww20/services/gateway/src/server.ts).

#### _Organized Desktop/06 AI And Learning/think

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/06%20AI%20And%20Learning/think)

TraceVault is a local-first trace platform for AI coding assistant conversations.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Fastify; Node.js; React; Vite; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** local trace ingestion, normalization, storage, search, privacy-aware tooling
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Trace one conversation import and design a repeat-import deduplication test.
- **Evidence:** [README.md](../../_Organized%20Desktop/06%20AI%20And%20Learning/think/README.md), [service.ts](../../_Organized%20Desktop/06%20AI%20And%20Learning/think/packages/core/src/service.ts), [App.tsx](../../_Organized%20Desktop/06%20AI%20And%20Learning/think/apps/web/src/App.tsx).

<a id="location-organized-desktop-07-anti-projects"></a>

### _Organized Desktop/07 Anti Projects

#### _Organized Desktop/07 Anti Projects/antiinv

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/07%20Anti%20Projects/antiinv)

Frontend/backend starter with a generic sign-in screen; its intended inventory domain remains unverified.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; Redis; infrastructure: Docker; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified. Limits: Generic sign-in frontend/backend starter; the intended inventory domain is unverified.
- **Learn:** frontend/backend contract exploration; domain clarification
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Establish the actual domain by reading schema and routes before expanding the starter.
- **Evidence:** [README.md](../../_Organized%20Desktop/07%20Anti%20Projects/antiinv/frontend/README.md), [auth.routes.ts](../../_Organized%20Desktop/07%20Anti%20Projects/antiinv/backend/src/modules/auth/auth.routes.ts), [App.tsx](../../_Organized%20Desktop/07%20Anti%20Projects/antiinv/frontend/src/App.tsx).

#### _Organized Desktop/07 Anti Projects/antihelpdesk

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/07%20Anti%20Projects/antihelpdesk)

Enterprise SaaS helpdesk system for learning purposes.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** ticket CRUD, role rules, service boundaries, UI/server contracts
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one ticket transition and test both validation and authorization.
- **Evidence:** [README.md](../../_Organized%20Desktop/07%20Anti%20Projects/antihelpdesk/README.md), [auth.routes.ts](../../_Organized%20Desktop/07%20Anti%20Projects/antihelpdesk/backend/src/modules/auth/auth.routes.ts), [App.tsx](../../_Organized%20Desktop/07%20Anti%20Projects/antihelpdesk/frontend/src/App.tsx).

#### _Organized Desktop/07 Anti Projects/antiemponb

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/07%20Anti%20Projects/antiemponb)

Welcome to the HRFlow Onboarding Platform Educational Lab.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; Redis; infrastructure: Docker; testing: Vitest; integrations: BullMQ.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** onboarding workflows, authorization, module boundaries, audit history
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one onboarding step and test invalid ordering and unauthorized completion.
- **Evidence:** [README.md](../../_Organized%20Desktop/07%20Anti%20Projects/antiemponb/docsclaude/README.md), [auth.routes.ts](../../_Organized%20Desktop/07%20Anti%20Projects/antiemponb/backend/src/modules/auth/auth.routes.ts), [App.tsx](../../_Organized%20Desktop/07%20Anti%20Projects/antiemponb/frontend/src/App.tsx).

#### _Organized Desktop/07 Anti Projects/antitestbuild

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/07%20Anti%20Projects/antitestbuild)

GlobalWorkforce OS is a secure, multi-tenant Employer of Record (EOR) operations platform designed as a modular monolith.

- **Stack:** languages: CSS; HTML; TypeScript; frameworks: NestJS; Node.js; React; Vite; data: Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** tenant isolation, workforce workflows, modular-monolith boundaries
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one cross-module employee workflow and test cross-tenant isolation.
- **Evidence:** [README.md](../../_Organized%20Desktop/07%20Anti%20Projects/antitestbuild/README.md), [api.ts](../../_Organized%20Desktop/07%20Anti%20Projects/antitestbuild/apps/web/src/services/api.ts), [App.tsx](../../_Organized%20Desktop/07%20Anti%20Projects/antitestbuild/apps/web/src/App.tsx).

<a id="location-organized-desktop-08-app-and-product-projects"></a>

### _Organized Desktop/08 App And Product Projects

#### _Organized Desktop/08 App And Product Projects/recipegen-app

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app)

Weeknight recipe app that suggests dinner ideas from available ingredients.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; integrations: Anthropic API.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** forms, client state, ingredient transforms, loading/error states
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Trace ingredients to suggestions and define empty-input and failed-request behavior.
- **Evidence:** [README.md](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app/README.md), [page.tsx](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app/app/page.tsx), [package.json](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app/package.json).

#### _Organized Desktop/08 App And Product Projects/recipegen-temp

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-temp)

Next.js starter retained alongside the recipe app.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS.
- **Review:** Source implementation is indexed; runtime behavior remains unverified. Limits: Generic Next.js starter.
- **Learn:** Next.js starter structure
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Prefer recipegen-app for domain work; use this only for a scaffold comparison.
- **Evidence:** [README.md](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-temp/README.md), [next.config.ts](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-temp/next.config.ts), [page.tsx](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-temp/src/app/page.tsx).

#### _Organized Desktop/08 App And Product Projects/appmakertrack

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/appmakertrack)

A single-user project management application with kanban boards, project-scoped team members, and time tracking.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** project/task modeling, kanban ordering, time tracking
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace a task move or time-entry save and test invalid project scope.
- **Evidence:** [README.md](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/appmakertrack/README.md), [page.tsx](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/appmakertrack/app/page.tsx), [package.json](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/appmakertrack/package.json).

#### _Organized Desktop/08 App And Product Projects/grouphelpdesk

**Stage 4: Integrated full-stack workflows. Core route.** [Open folder](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/grouphelpdesk)

HelpDesk is a learning-focused full-stack internal support ticket system.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; GitHub Actions; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** React/Express TypeScript contracts, SQLite/Prisma, workflow validation, RBAC, Vitest/Supertest, logging
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace ticket creation and assignment through shared contracts; add an unauthorized transition test.
- **Evidence:** [README.md](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/grouphelpdesk/README.md), [auth.ts](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/grouphelpdesk/packages/server/src/routes/auth.ts), [App.tsx](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/grouphelpdesk/packages/client/src/App.tsx).

#### _Organized Desktop/08 App And Product Projects/HNJOBTRACK

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK)

A full-stack job browser for Hacker News "Who's Hiring" threads.

- **Stack:** languages: CSS; JavaScript; Python; SQL; TypeScript; frameworks: FastAPI; Next.js; Node.js; React; Tailwind CSS; data: Supabase; integrations: OpenAI API.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** API ingestion, search/filtering, parsing, UI server-state
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace one imported posting and test malformed or repeated source records.
- **Evidence:** [README.md](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK/README.md), [main.py](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK/backend/app/main.py), [package.json](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK/frontend/package.json).

#### _Organized Desktop/08 App And Product Projects/job track

**Stage 4: Integrated full-stack workflows. Core journey candidate.** [Open folder](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/job%20track)

Full-stack JavaScript app for tracking job applications with auth, protected routes, validation, CRUD, filtering/sorting, workflow transitions, and dashboard stats.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Vite; data: SQLite; integrations: Socket.IO.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** React/Express JavaScript, SQLite, JWT auth, validation, CRUD, workflow transitions
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace application creation then test ownership and an invalid status transition.
- **Evidence:** [README.md](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/job%20track/README.md), [App.jsx](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/job%20track/client/src/App.jsx), [package.json](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/job%20track/package.json).

#### _Organized Desktop/08 App And Product Projects/hnrandom

**Stage 5: Domain rules and reliability. Alternative practice project.** [Open folder](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/hnrandom)

AI Observer is a self-hosted observability backend and dashboard for AI coding workflows.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; infrastructure: Docker; GitHub Actions; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** observability ingestion, aggregation, diagnostics, dashboards
- **Before starting:** One complete authenticated app; transactions, test isolation, and failure handling.
- **Next:** Trace one telemetry event and verify how duplicates and errors affect metrics.
- **Evidence:** [README.md](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/hnrandom/README.md), [routes.ts](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/hnrandom/backend/src/api/routes.ts), [App.tsx](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/hnrandom/frontend/src/App.tsx).

#### _Organized Desktop/08 App And Product Projects/eliapplybot

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot)

A local, personal Chrome extension that fills in the repetitive parts of job application forms — name, email, phone, links, education, work history — from a profile you control.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: React; Vite; infrastructure: GitHub Actions; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** browser extensions, DOM matching, content-script messaging, user-controlled profiles
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Use local form fixtures to test matching and filling while preserving user review.
- **Evidence:** [README.md](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot/README.md), [serviceWorker.ts](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot/src/background/serviceWorker.ts), [package.json](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot/package.json).

#### _Organized Desktop/08 App And Product Projects/eliapplybot-python

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot-python)

A local-first, review-first Python rebuild of the eli apply mate idea.

- **Stack:** languages: CSS; HTML; Python; frameworks: FastAPI; testing: Playwright; pytest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** Python browser automation, profile models, adapters, explicit review flow
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Compare form mappings with the extension and isolate browser effects behind fixtures.
- **Evidence:** [README.md](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot-python/README.md), [main.py](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot-python/src/eliapplybot/main.py), [pyproject.toml](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot-python/pyproject.toml).

<a id="location-organized-desktop-09-grav-and-vg-projects"></a>

### _Organized Desktop/09 Grav And VG Projects

#### _Organized Desktop/09 Grav And VG Projects/grav1pretalx

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/grav1pretalx)

pretalx conference proposal, speaker, and schedule management.

- **Stack:** languages: CSS; HTML; JavaScript; Python; Vue; frameworks: Django; Vite; Vue; data: Redis; infrastructure: GitHub Actions; testing: pytest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** Django domain modeling, proposal workflows, scheduling, established code navigation
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Compare its local contents with masterpre, then choose one bounded pretalx feature to trace.
- **Evidence:** [auth.py](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/grav1pretalx/pretalx/src/pretalx/api/auth.py), [README.rst](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/grav1pretalx/pretalx/README.rst).

#### _Organized Desktop/09 Grav And VG Projects/graveopenjspy

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/graveopenjspy)

OpenSlides is a free, web based presentation and assembly system for managing and projecting agenda, motions and elections of an assembly.

- **Stack:** languages: CSS; Go; HTML; JavaScript; Python; SCSS; SQL; TypeScript; infrastructure: Docker; GitHub Actions.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** assembly workflows, distributed service boundaries, permissions, event updates
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one motion or vote across its API, data, authorization, and tests.
- **Evidence:** [README.md](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/graveopenjspy/OpenSlides/README.md), [main.go](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/graveopenjspy/OpenSlides/openslides-icc-service/main.go).

#### _Organized Desktop/09 Grav And VG Projects/gravreviewboardjspy

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/gravreviewboardjspy)

Review Board is an open source, web-based code and document review tool built to help companies, open source projects, and other organizations keep their quality high and their bug count low.

- **Stack:** languages: C; C++; CSS; HTML; JavaScript; Python; SQL; TypeScript; frameworks: Django; data: MySQL; PostgreSQL; infrastructure: Docker.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** Django review workflows, diffs, access policy, extension points
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace a review-request change and select one narrow bug or test contribution.
- **Evidence:** [services.py](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/gravreviewboardjspy/reviewboard/reviewboard/avatars/services.py), [README.rst](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/gravreviewboardjspy/reviewboard/README.rst).

#### _Organized Desktop/09 Grav And VG Projects/vg

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/vg)

Employer-of-record (EOR) platform MVP built with Next.js, Node.js, and PostgreSQL.

- **Stack:** languages: CSS; JavaScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; Redis; infrastructure: Docker; integrations: BullMQ; Stripe.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** multi-tenant workforce modeling, scoped APIs, approval workflows
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one employee approval and test cross-tenant access denial.
- **Evidence:** [README.md](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/vg/README.md), [context.js](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/vg/src/services/context.js), [auth.service.js](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/vg/src/services/auth.service.js).

#### _Organized Desktop/09 Grav And VG Projects/VGdemo

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/VGdemo)

This folder is a structured code review of the globalhire-lite codebase, written with a specific goal: take a junior software engineer and pull them toward mid/senior level for CRUD web-app development jobs.

- **Stack:** languages: C#; CSS; HTML; JavaScript; TypeScript; frameworks: ASP.NET Core; Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Vitest; xUnit.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** code-review practice, CRUD architecture, data/auth boundaries
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Follow the structured globalhire-lite review and implement one small finding in an isolated copy later.
- **Evidence:** [README.md](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/VGdemo/fable/README.md), [auth.routes.ts](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/VGdemo/globalhire-lite/apps/api/src/modules/auth/auth.routes.ts), [App.tsx](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/VGdemo/globalhire-lite/apps/web/src/App.tsx).

<a id="location-organized-desktop-12-other-projects"></a>

### _Organized Desktop/12 Other Projects

#### _Organized Desktop/12 Other Projects/Obsidian

**Stage 0: Planning and reference collections. Learning/reference collection.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/Obsidian)

Obsidian JS Fund note collection with a learning prompt and welcome note; not an implemented app.

- **Stack:** .
- **Review:** Learning/reference material; no source implementation indexed.
- **Learn:** personal knowledge organization and reference navigation
- **Before starting:** Language basics and the prior roadmap milestone.
- **Next:** Read JS Fund/llm prompt.md as study context, then practice in trainjs or jstrain2.2.
- **Evidence:** [llm prompt.md](../../_Organized%20Desktop/12%20Other%20Projects/Obsidian/JS%20Fund/llm%20prompt.md), [Welcome.md](../../_Organized%20Desktop/12%20Other%20Projects/Obsidian/JS%20Fund/Welcome.md).

#### _Organized Desktop/12 Other Projects/3buildhyper

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/3buildhyper)

HyperNova agency website with service pages, content tooling, and Amplify/HubSpot integration material.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; infrastructure: AWS SDK; GitHub Actions; testing: Jest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** React/Next page composition, accessibility, forms, content/integration boundaries
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Compare with hypernova-inc-main and complete one bounded page/form improvement.
- **Evidence:** [README.md](../../_Organized%20Desktop/12%20Other%20Projects/3buildhyper/README.md), [services.tsx](../../_Organized%20Desktop/12%20Other%20Projects/3buildhyper/pages/services.tsx), [package.json](../../_Organized%20Desktop/12%20Other%20Projects/3buildhyper/package.json).

#### _Organized Desktop/12 Other Projects/FinalJep

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/FinalJep)

Convex/React app variants with chat components; a Jeopardy implementation was not established in the inspected samples.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; Vite.
- **Review:** Source implementation is indexed; runtime behavior remains unverified. Limits: Sampled components are chat-oriented; the name does not establish a Jeopardy implementation.
- **Learn:** React/Convex workspace comparison and scope identification
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Compare the two app variants and locate actual game logic before selecting a build target.
- **Evidence:** [README.md](../../_Organized%20Desktop/12%20Other%20Projects/FinalJep/finaljep-app/README.md), [App.tsx](../../_Organized%20Desktop/12%20Other%20Projects/FinalJep/finaljep-app/src/App.tsx), [package.json](../../_Organized%20Desktop/12%20Other%20Projects/FinalJep/finaljep-app/package.json).

#### _Organized Desktop/12 Other Projects/GlobGame

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/GlobGame)

Globs is a daily hierarchical merge puzzle game built with Next.js, JavaScript, Prisma, and PostgreSQL.

- **Stack:** languages: CSS; JavaScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** pure game rules, deterministic state transitions, persistence
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Extract and test a merge rule including invalid moves and repeat daily play.
- **Evidence:** [README.md](../../_Organized%20Desktop/12%20Other%20Projects/GlobGame/README.md), [page.js](../../_Organized%20Desktop/12%20Other%20Projects/GlobGame/src/app/page.js), [package.json](../../_Organized%20Desktop/12%20Other%20Projects/GlobGame/package.json).

#### _Organized Desktop/12 Other Projects/hypernova-inc-main

**Stage 2: Client apps and state. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/hypernova-inc-main)

HyperNova agency website with service pages, content tooling, and Amplify/HubSpot integration material.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; infrastructure: GitHub Actions; testing: Jest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** page composition, accessibility, content, forms/integration boundaries
- **Before starting:** Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Next:** Compare with 3buildhyper and choose one canonical branch for a small page/form task.
- **Evidence:** [README.md](../../_Organized%20Desktop/12%20Other%20Projects/hypernova-inc-main/README.md), [services.tsx](../../_Organized%20Desktop/12%20Other%20Projects/hypernova-inc-main/pages/services.tsx), [package.json](../../_Organized%20Desktop/12%20Other%20Projects/hypernova-inc-main/package.json).

#### _Organized Desktop/12 Other Projects/aaa1

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/aaa1)

This is a multi-tenant CRM built with Next.js App Router, TypeScript, Prisma, PostgreSQL, Tailwind, Zod, React Query, and REST APIs.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; testing: Vitest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** tenant-aware CRM schemas, services, Zod validation, REST contracts
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace lead/deal mutation and test cross-tenant data access.
- **Evidence:** [README.md](../../_Organized%20Desktop/12%20Other%20Projects/aaa1/docs/architecture/README.md), [opsService.ts](../../_Organized%20Desktop/12%20Other%20Projects/aaa1/src/services/opsService.ts), [noteService.ts](../../_Organized%20Desktop/12%20Other%20Projects/aaa1/src/services/noteService.ts).

#### _Organized Desktop/12 Other Projects/cc

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/cc)

CMS web-application prototype.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** CMS content modeling, edit workflows, API/UI separation
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Establish one implemented content workflow and test validation and permission boundaries.
- **Evidence:** [db.ts](../../_Organized%20Desktop/12%20Other%20Projects/cc/src/lib/db.ts), [auth.ts](../../_Organized%20Desktop/12%20Other%20Projects/cc/src/lib/auth.ts).

#### _Organized Desktop/12 Other Projects/jdtrrain2.1

**Stage 4: Integrated full-stack workflows. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/jdtrrain2.1)

Full-stack JavaScript project management platform built with Next.js App Router, Prisma, SQLite, React Query, dnd-kit, and Recharts.

- **Stack:** languages: CSS; JavaScript; frameworks: Next.js; Node.js; React; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** Next.js CRUD, Prisma/SQLite, drag-and-drop, React Query, reporting
- **Before starting:** API + SQL project; schema design, validation, sessions, and basic tests.
- **Next:** Trace a task move into persistence and test ordering plus invalid project references.
- **Evidence:** [README.md](../../_Organized%20Desktop/12%20Other%20Projects/jdtrrain2.1/README.md), [cn.js](../../_Organized%20Desktop/12%20Other%20Projects/jdtrrain2.1/src/lib/cn.js), [package.json](../../_Organized%20Desktop/12%20Other%20Projects/jdtrrain2.1/package.json).

#### _Organized Desktop/12 Other Projects/andie

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/andie)

Shopify-related scripting workspace, including a metaobject population utility.

- **Stack:** languages: JavaScript.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** Shopify API scripting, data transformations, integration validation
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Inspect the metaobject utility inputs and design a dry-run plus idempotent update strategy.
- **Evidence:** [main.js](../../_Organized%20Desktop/12%20Other%20Projects/andie/.storybook/main.js).

#### _Organized Desktop/12 Other Projects/pp8

**Stage 6: Architecture and advanced integrations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/pp8)

This repository recreates a unified HR platform in a Python-first stack so its backend architecture can be compared over time with a TypeScript-first version.

- **Stack:** languages: CSS; JavaScript; Python; TypeScript; frameworks: FastAPI; Next.js; Node.js; React; Tailwind CSS; data: PostgreSQL; SQLAlchemy; infrastructure: Docker; testing: pytest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** Python-first HR architecture, service boundaries, comparison with TypeScript
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one HR use case and compare its validation/auth/data boundaries with the TypeScript version.
- **Evidence:** [README.md](../../_Organized%20Desktop/12%20Other%20Projects/pp8/README.md), [main.py](../../_Organized%20Desktop/12%20Other%20Projects/pp8/backend/app/main.py), [docker-compose.yml](../../_Organized%20Desktop/12%20Other%20Projects/pp8/docker-compose.yml).

#### _Organized Desktop/12 Other Projects/pyhealth

**Stage 6: Architecture and advanced integrations. Reference/contribution project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/pyhealth)

Healthchecks is a cron job monitoring service.

- **Stack:** languages: CSS; HTML; JavaScript; Python; frameworks: Django; data: PostgreSQL; infrastructure: Docker; GitHub Actions.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** Django scheduled-job monitoring, alert state, operations, established code reading
- **Before starting:** A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Next:** Trace one incoming ping into check state and alert processing; select one bounded test or fix.
- **Evidence:** [README.md](../../_Organized%20Desktop/12%20Other%20Projects/pyhealth/healthchecks/README.md), [apps.py](../../_Organized%20Desktop/12%20Other%20Projects/pyhealth/healthchecks/hc/api/apps.py), [requirements.txt](../../_Organized%20Desktop/12%20Other%20Projects/pyhealth/healthchecks/requirements.txt).

#### _Organized Desktop/12 Other Projects/appmaketrck

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/appmaketrck)

A real-time air quality monitoring web application with an interactive 3D globe visualization.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; testing: Playwright; Vitest; integrations: MCP.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** API-fed geospatial data, 3D visualization, client rendering performance
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Trace one air-quality reading to the globe and handle unavailable/stale data.
- **Evidence:** [README.md](../../_Organized%20Desktop/12%20Other%20Projects/appmaketrck/airwatch/README.md), [notes.ts](../../_Organized%20Desktop/12%20Other%20Projects/appmaketrck/obsidian-claude/packages/server/src/api/routes/notes.ts), [App.tsx](../../_Organized%20Desktop/12%20Other%20Projects/appmaketrck/airwatch/src/App.tsx).

#### _Organized Desktop/12 Other Projects/curse

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/curse)

A full-stack Jeopardy game web application with user accounts, friends system, game sharing, and real-time gameplay.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; frameworks: Express; Node.js; React; Vite; data: Prisma; testing: Jest.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** Jeopardy game state, user/friend relations, real-time events
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Trace a game event and specify duplicate-event/reconnect behavior.
- **Evidence:** [README.md](../../_Organized%20Desktop/12%20Other%20Projects/curse/Jeopardy-Game/README.md), [authRoutes.js](../../_Organized%20Desktop/12%20Other%20Projects/curse/Jeopardy-Game/backend/src/routes/authRoutes.js), [App.jsx](../../_Organized%20Desktop/12%20Other%20Projects/curse/Jeopardy-Game/frontend/src/App.jsx).

#### _Organized Desktop/12 Other Projects/finaljepgame

**Stage 7: Specializations. Alternative practice project.** [Open folder](../../_Organized%20Desktop/12%20Other%20Projects/finaljepgame)

Jeopardy game builder and player workspace.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma.
- **Review:** Source implementation is indexed; runtime behavior remains unverified.
- **Learn:** game-builder schemas, gameplay state, UI/server synchronization
- **Before starting:** Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Next:** Trace question creation into gameplay and test one invalid state transition.
- **Evidence:** [README.md](../../_Organized%20Desktop/12%20Other%20Projects/finaljepgame/jeopardy-maker/README.md), [auth.ts](../../_Organized%20Desktop/12%20Other%20Projects/finaljepgame/jeopardy-maker/src/lib/auth.ts), [package.json](../../_Organized%20Desktop/12%20Other%20Projects/finaljepgame/jeopardy-maker/package.json).

<a id="location-geminiorganized"></a>

### geminiorganized

#### geminiorganized/FableDocs_Projects_Hermes

**Stage 0: Planning and reference collections. Related copy / alternative location.** [Open folder](../../geminiorganized/FableDocs_Projects_Hermes)

Operating pack for using Hermes as a software engineering assistant.

- **Stack:** .
- **Review:** Teaching/reference workspace; runtime not verified.
- **Learn:** Engineering rituals, prompts, note taking, assisted learning
- **Before starting:** None; use alongside active project work.
- **Next:** Choose one prediction-review-reflection routine and apply it to a real ticket.
- **Evidence:** [README.md](../../geminiorganized/FableDocs_Projects_Hermes/README.md).
- **Related versions/options:** [hermes](../../hermes). A corresponding learning option exists at hermes. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_C#Interview

**Stage 0: Planning and reference collections. Related copy / alternative location.** [Open folder](../../geminiorganized/General_C%23Interview)

Ten-week C# upskilling and interview-preparation curriculum with drills and portfolio work.

- **Stack:** .
- **Review:** Teaching/reference workspace; runtime not verified.
- **Learn:** C# drills, interview explanations, ten-week structure
- **Before starting:** None; use alongside active project work.
- **Next:** Take a baseline drill, then use weak areas beside the current project.
- **Evidence:** [README.md](../../geminiorganized/General_C%23Interview/README.md).
- **Related versions/options:** [c#interview](../../c%23interview). A corresponding learning option exists at c#interview. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Devdeck

**Stage 0: Planning and reference collections. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Devdeck)

A spaced-repetition flashcard PWA for learning software development in 5–15 minute sessions — on the bus, waiting for a delivery, wherever.

- **Stack:** languages: CSS; HTML; TypeScript; frameworks: React; Tailwind CSS; Vite; data: IndexedDB / Dexie; testing: Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Short recall sessions, spaced repetition, web fundamentals
- **Before starting:** None; use alongside active project work.
- **Next:** Choose this or ankijs for daily recall, not parallel card backlogs.
- **Evidence:** [README.md](../../geminiorganized/General_Devdeck/README.md), [App.tsx](../../geminiorganized/General_Devdeck/src/App.tsx), [package.json](../../geminiorganized/General_Devdeck/package.json).
- **Related versions/options:** [devdeck](../../devdeck). A corresponding learning option exists at devdeck. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Gitjira

**Stage 0: Planning and reference collections. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Gitjira)

Sprint plans and build instructions for the separate GitJira issue-tracker app.

- **Stack:** .
- **Review:** Static sample does not establish runtime readiness.
- **Learn:** Sprint planning, review choreography, issue-tracker specifications
- **Before starting:** None; use alongside active project work.
- **Next:** Use the relevant playbook beside gitjira-app and do exercises independently.
- **Evidence:** [README.md](../../geminiorganized/General_Gitjira/sprints/README.md).
- **Related versions/options:** [gitjira](../../gitjira). A corresponding learning option exists at gitjira. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_MasterPlan

**Stage 0: Planning and reference collections. Related copy / alternative location.** [Open folder](../../geminiorganized/General_MasterPlan)

Project-based software-engineering study plans and a progression of practice projects.

- **Stack:** .
- **Review:** Teaching/reference workspace; runtime not verified.
- **Learn:** Existing sixteen-week ladder and study organization
- **Before starting:** None; use alongside active project work.
- **Next:** Use prior plans as context; adopt the new report's small project sequence.
- **Evidence:** [README.md](../../geminiorganized/General_MasterPlan/README.md).
- **Related versions/options:** [master plan](../../master%20plan). A corresponding learning option exists at master plan. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Readme

**Stage 0: Planning and reference collections. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Readme)

Existing Desktop inventory document; listed as a reference artifact and not used to discover or assess projects.

- **Stack:** .
- **Review:** Static sample does not establish runtime readiness. No readable text/source evidence was available; this entry is a directory/resource inventory only.
- **Learn:** Organizing evidence and locating previous project descriptions.
- **Before starting:** No application prerequisite; use alongside the journey.
- **Next:** Use only as historical orientation; prefer this newly verified master report for order.
- **Evidence:** Directory/resource inventory only; no readable implementation evidence was established.
- **Related versions/options:** [readme](../../readme). A corresponding learning option exists at readme. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Resume

**Stage 0: Planning and reference collections. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Resume)

Career and résumé reference materials.

- **Stack:** .
- **Review:** Static sample does not establish runtime readiness. No readable text/source evidence was available; this entry is a directory/resource inventory only.
- **Learn:** Translate verified project work into role-specific evidence.
- **Before starting:** No application prerequisite; use alongside the journey.
- **Next:** Choose target SWE role and replace broad claims with outcomes from projects you can explain and demonstrate.
- **Evidence:** Directory/resource inventory only; no readable implementation evidence was established.
- **Related versions/options:** [resume](../../resume). A corresponding learning option exists at resume. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Buildsql

**Stage 0: Planning and reference collections. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Buildsql)

SQL Dojo: a 51-lesson PostgreSQL course with SQL exercises and pytest-based grading, from SELECT statements to query-plan tuning.

- **Stack:** languages: Python; SQL; data: PostgreSQL; infrastructure: Docker; GitHub Actions; testing: pytest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Active recall, SQL and SWE mission practice
- **Before starting:** None; use alongside active project work.
- **Next:** Use missions for current curriculum gaps and produce code evidence.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Buildsql/README.md), [conftest.py](../../geminiorganized/LLM_Generated_Buildsql/conftest.py), [README.md](../../geminiorganized/LLM_Generated_Buildsql/lessons/14_ctes/README.md).
- **Related versions/options:** [buildsql](../../buildsql). A corresponding learning option exists at buildsql. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_ClaudeDocs

**Stage 0: Planning and reference collections. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_ClaudeDocs)

Software-engineering study plans, worked examples, and coding-practice guidance.

- **Stack:** .
- **Review:** Static sample does not establish runtime readiness. No readable text/source evidence was available; this entry is a directory/resource inventory only.
- **Learn:** Project-first learning, review habits, worked examples
- **Before starting:** None; use alongside active project work.
- **Next:** Use one project-first routine and apply its review checklist to an actual change.
- **Evidence:** Directory/resource inventory only; no readable implementation evidence was established.
- **Related versions/options:** [claude docs](../../claude%20docs). A corresponding learning option exists at claude docs. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Gptdocs

**Stage 0: Planning and reference collections. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Gptdocs)

Software-engineering learning and reference documents.

- **Stack:** .
- **Review:** Static sample does not establish runtime readiness. No readable text/source evidence was available; this entry is a directory/resource inventory only.
- **Learn:** Code review, production failure modes, worked examples
- **Before starting:** None; use alongside active project work.
- **Next:** Apply one rubric to the next project change.
- **Evidence:** Directory/resource inventory only; no readable implementation evidence was established.
- **Related versions/options:** [GPTDocs](../../GPTDocs). A corresponding learning option exists at GPTDocs. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Csharptut

**Stage 1: Language and browser foundations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Csharptut)

A practical, no-fluff path from "I can write basic code" to "I can be trusted on a real C# team doing CRUD/backend work."

- **Stack:** .
- **Review:** Teaching/reference workspace; runtime not verified.
- **Learn:** C# fundamentals through EF Core, APIs and testing
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Work 00-15 then 16-21; independently rebuild the chapter 22 CRUD capstone.
- **Evidence:** [README.md](../../geminiorganized/General_Csharptut/README.md), [README.md](../../geminiorganized/General_Csharptut/react-tutorial/README.md).
- **Related versions/options:** [csharptut](../../csharptut). A corresponding learning option exists at csharptut. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Finance-Dashboard

**Stage 1: Language and browser foundations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Finance-Dashboard)

A self-contained household finance dashboard for expenses, bills, savings goals, and investment tracking.

- **Stack:** languages: CSS; HTML; JavaScript.
- **Review:** Static sample does not establish runtime readiness.
- **Learn:** Vanilla JavaScript, forms, derived totals, localStorage
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Add a validated expense edit and confirm totals survive reload.
- **Evidence:** [README.md](../../geminiorganized/General_Finance-Dashboard/README.md), [app.js](../../geminiorganized/General_Finance-Dashboard/app.js), [index.html](../../geminiorganized/General_Finance-Dashboard/index.html).
- **Related versions/options:** [finance-dashboard](../../finance-dashboard). A corresponding learning option exists at finance-dashboard. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Jstut

**Stage 1: Language and browser foundations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Jstut)

A tutorial for software engineers who want to build real fullstack fluency.

- **Stack:** .
- **Review:** Teaching/reference workspace; runtime not verified. Local documentation: - Days 21–23: Part 9 (SQL). Replace your in-memory data with Postgres.
- **Learn:** JavaScript, Node, TypeScript, React, SQL, C#/.NET concepts
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Use fundamentals Parts 1-9 alongside JS1; defer advanced parts until API work.
- **Evidence:** [README.md](../../geminiorganized/General_Jstut/README.md), [README.md](../../geminiorganized/General_Jstut/dotnet-crud-extension/README.md).
- **Related versions/options:** [JSTut](../../JSTut). A corresponding learning option exists at JSTut. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Grokjs

**Stage 1: Language and browser foundations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Grokjs)

JavaScript, .NET, and full-stack practice labs with worked explanations and exercises.

- **Stack:** languages: C#; HTML; JavaScript; Python; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Language labs, JavaScript, Python, C#, full-stack exercises
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Pick one language lab and one exercise matching a current gap.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Grokjs/README.md), [Program.cs](../../geminiorganized/LLM_Generated_Grokjs/grokbuildc%23/backend/Program.cs), [README.md](../../geminiorganized/LLM_Generated_Grokjs/grokbuildjs/README.md).
- **Related versions/options:** [grokjs](../../grokjs). A corresponding learning option exists at grokjs. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Groktuts

**Stage 1: Language and browser foundations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Groktuts)

Collection of , hands-on upskilling laboratories.

- **Stack:** languages: C#; JavaScript; Python; SQL; TypeScript; frameworks: React; testing: Vitest; pytest; xUnit.
- **Review:** Static sample does not establish runtime readiness.
- **Learn:** JS/TS/React, Python, C#, SQL fundamentals
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Use one lab to close a measured fundamentals gap.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Groktuts/README.md), [Program.cs](../../geminiorganized/LLM_Generated_Groktuts/dotnet-upskilling-lab/csharp/01-lesson/Program.cs), [README.md](../../geminiorganized/LLM_Generated_Groktuts/sql-upskilling-lab/README.md).
- **Related versions/options:** [groktuts](../../groktuts). A corresponding learning option exists at groktuts. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Js1

**Stage 1: Language and browser foundations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Js1)

Standalone vanilla JavaScript CRUD apps live in this workspace.

- **Stack:** languages: C#; CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Express; Node.js; React; Vite; data: PostgreSQL.
- **Review:** Relevant implementation is present; runtime not verified. Local documentation: These folders are full-stack learning scaffolds with a React client and Express; Core five (REST + in-memory data):
- **Learn:** Vanilla CRUD to React APIs, SQL and .NET practice
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Select task-board, contact-book, focus-timer, issue-desk, secure-notes, invoice-studio, room-booking in that order.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Js1/README.md), [App.tsx](../../geminiorganized/LLM_Generated_Js1/field-service/client/src/App.tsx), [README.md](../../geminiorganized/LLM_Generated_Js1/mini-blog/README.md).
- **Related versions/options:** [JS1](../../JS1). A corresponding learning option exists at JS1. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Jsprojectlearn

**Stage 1: Language and browser foundations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Jsprojectlearn)

Older 165-exercise refactoring curriculum spanning JavaScript, React, and TypeScript; compare with the newer direct Desktop version.

- **Stack:** languages: HTML; JavaScript; TypeScript.
- **Review:** Teaching/reference workspace; runtime not verified. This copy differs from current Desktop JSProjectLearn, a 334-mission campaign.
- **Learn:** JavaScript refactoring first, then React and TypeScript; this local README describes the older 165-exercise curriculum.
- **Before starting:** Basic computer/file skills and willingness to type and debug examples.
- **Next:** Compare an original/refactored example and implement the change independently. Compare this older curriculum with the current direct Desktop SkillForge Quest before choosing a course.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Jsprojectlearn/README.md), [server.js](../../geminiorganized/LLM_Generated_Jsprojectlearn/65-rest-api/refactored/server.js), [README.md](../../geminiorganized/LLM_Generated_Jsprojectlearn/react/README.md).
- **Related versions/options:** [JSProjectLearn](../../JSProjectLearn). A corresponding learning option exists at JSProjectLearn. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Alanandelisoccer

**Stage 2: Client apps and state. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Alanandelisoccer)

A Next.js learning app for the 17 Laws of Soccer, World Cup context, and practical match tools.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Next.js routes, content modeling, search, local UI state
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Add a tested saved-law or referee-tool interaction.
- **Evidence:** [README.md](../../geminiorganized/General_Alanandelisoccer/soccer-laws-app/README.md), [RefereeNotebook.tsx](../../geminiorganized/General_Alanandelisoccer/soccer-laws-app/src/components/tools/RefereeNotebook.tsx), [package.json](../../geminiorganized/General_Alanandelisoccer/soccer-laws-app/package.json).
- **Related versions/options:** [AlanAndEliSoccer](../../AlanAndEliSoccer). A corresponding learning option exists at AlanAndEliSoccer. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Ankijs

**Stage 2: Client apps and state. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Ankijs)

Recall is a local-first spaced-repetition PWA with quick capture, inbox triage, and offline study.

- **Stack:** languages: CSS; HTML; SQL; TypeScript; frameworks: React; Tailwind CSS; Vite; data: IndexedDB / Dexie; Supabase; testing: Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Spaced repetition, IndexedDB, offline state, optional sync
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Use short daily recall sessions; study one scheduling or sync invariant.
- **Evidence:** [README.md](../../geminiorganized/General_Ankijs/README.md), [App.tsx](../../geminiorganized/General_Ankijs/src/App.tsx), [README.md](../../geminiorganized/General_Ankijs/net/README.md).
- **Related versions/options:** [ankijs](../../ankijs). A corresponding learning option exists at ankijs. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Formforge

**Stage 2: Client apps and state. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Formforge)

FormForge is a , schema-driven form builder and response analytics platform built as a fifteen-sprint React and TypeScript teaching repository.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Fastify; Node.js; React; Vite; infrastructure: GitHub Actions; testing: Vitest.
- **Review:** Relevant implementation is present; runtime not verified. Local documentation: API --> Data[@formforge/data\nrepository contracts + in-memory adapters]
- **Learn:** TypeScript schemas, React reducers, validation, branching, tests
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Follow the fifteen-sprint sequence; add one field type with validation tests.
- **Evidence:** [README.md](../../geminiorganized/General_Formforge/README.md), [App.tsx](../../geminiorganized/General_Formforge/apps/web/src/App.tsx), [package.json](../../geminiorganized/General_Formforge/package.json).
- **Related versions/options:** [formforge](../../formforge). A corresponding learning option exists at formforge. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Recipeweb

**Stage 2: Client apps and state. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Recipeweb)

A Filipino, Vietnamese, Thai & Spanish cookbook companion web app.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: React; Vite; infrastructure: GitHub Actions.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Components, typed data, filters, context/local persistence and accessible list interactions.
- **Before starting:** JavaScript/TypeScript fundamentals, HTML/CSS and basic React.
- **Next:** Implement one shopping-list behavior and verify persistence/accessibility; use the net plan later as an API extension exercise.
- **Evidence:** [README.md](../../geminiorganized/General_Recipeweb/README.md), [App.tsx](../../geminiorganized/General_Recipeweb/src/App.tsx), [package.json](../../geminiorganized/General_Recipeweb/package.json).
- **Related versions/options:** [recipeweb](../../recipeweb). A corresponding learning option exists at recipeweb. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Buildbusinesses

**Stage 2: Client apps and state. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Buildbusinesses)

LocalOps Ledger for keeping daily operating records for small local businesses.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** React forms, dashboard state, business record modeling
- **Before starting:** JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Next:** Trace LocalOperationsApp state and add one validated record flow.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Buildbusinesses/README.md), [page.tsx](../../geminiorganized/LLM_Generated_Buildbusinesses/src/app/page.tsx), [README.md](../../geminiorganized/LLM_Generated_Buildbusinesses/docs/upskill/README.md).
- **Related versions/options:** [buildbusinesses](../../buildbusinesses). A corresponding learning option exists at buildbusinesses. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Borrowbox

**Stage 3: APIs and SQL. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Borrowbox)

BorrowBox is a beginner-friendly fifteen-sprint C#/.NET teaching repository for lending campus equipment such as laptops, cameras, calculators, and lab kits.

- **Stack:** languages: C#; SQL; frameworks: ASP.NET Core; data: Entity Framework Core; SQLite; infrastructure: GitHub Actions; testing: xUnit.
- **Review:** Relevant implementation is present; runtime not verified. Local documentation: BorrowBox.Infrastructure in-memory and SQLite storage; OpenAPI is available at /openapi/v1.json in Development. Inventory reads and health endpoints are public. Mutating inventory uses the teaching header X-Demo-Role: Staff; borrowing accepts Student or Staff. This header is not production authentication.
- **Learn:** C# domain rules, minimal APIs, LINQ, DI, SQLite, tests
- **Before starting:** Language basics, HTTP/JSON, simple relational data and Git.
- **Next:** Follow the fifteen sprints; independently add a borrowing rule and its test.
- **Evidence:** [README.md](../../geminiorganized/General_Borrowbox/README.md), [Program.cs](../../geminiorganized/General_Borrowbox/src/BorrowBox.Api/Program.cs), [BorrowBox.Api.csproj](../../geminiorganized/General_Borrowbox/src/BorrowBox.Api/BorrowBox.Api.csproj).
- **Related versions/options:** [borrowbox](../../borrowbox). A corresponding learning option exists at borrowbox. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Newcodexjs

**Stage 3: APIs and SQL. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Newcodexjs)

This workspace is organized around the Tier 1 web development curriculum: 15 self-contained full-stack apps for building junior-to-mid-level engineering patterns.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Vite; data: PostgreSQL.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Progressive REST/SQL/client integration, then auth and business workflows.
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Begin 01-task-manager, then 05-recipe-manager; select one later domain challenge instead of completing all variants.
- **Evidence:** [README.md](../../geminiorganized/General_Newcodexjs/README.md), [App.jsx](../../geminiorganized/General_Newcodexjs/04-notes-app/client/src/App.jsx), [README.md](../../geminiorganized/General_Newcodexjs/04-notes-app/README.md).
- **Related versions/options:** [newcodexJS](../../newcodexJS). A corresponding learning option exists at newcodexJS. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Recipeview

**Stage 3: APIs and SQL. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Recipeview)

Local-first cooking journal organized as Dish, Recipe, and Cook Log, with SQLite persistence and photo uploads.

- **Stack:** languages: CSS; HTML; SQL; TypeScript; frameworks: Express; Node.js; React; Vite.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Relational modeling of dish/recipe/cook-log, SQL, file uploads and local-first UX.
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Trace creation of a recipe and cook log into SQLite, then test rollback and search-index consistency.
- **Evidence:** [README.md](../../geminiorganized/General_Recipeview/README.md), [App.tsx](../../geminiorganized/General_Recipeview/src/App.tsx), [package.json](../../geminiorganized/General_Recipeview/package.json).
- **Related versions/options:** [recipeview](../../recipeview). A corresponding learning option exists at recipeview. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/OpenSource_Upskilling_Snapshot

**Stage 3: APIs and SQL. Related copy / alternative location.** [Open folder](../../geminiorganized/OpenSource_Upskilling_Snapshot)

NetAiOps is a simulated full-stack AI-powered IT operations platform built as a 15-step teaching history for a junior engineer.

- **Stack:** languages: CSS; HTML; TypeScript; infrastructure: GitHub Actions.
- **Review:** Teaching/reference workspace; runtime not verified. Local documentation: NetAiOps is a simulated full-stack AI-powered IT operations platform built as a 15-step teaching history for a junior engineer. Browse snapshots/ in order; each folder contains a full copy of the codebase at that moment plus NOTES.md and CHANGES.md.
- **Learn:** How a walking skeleton becomes CRUD, auth, service layers, tests and operational features.
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Start snapshots/00-walking-skeleton/NOTES.md; predict each change, compare adjacent copies, and recreate one increment in your own branch.
- **Evidence:** [README.md](../../geminiorganized/OpenSource_Upskilling_Snapshot/README.md), [server.ts](../../geminiorganized/OpenSource_Upskilling_Snapshot/snapshots/07-service-refactor/code/backend/src/server.ts), [README.md](../../geminiorganized/OpenSource_Upskilling_Snapshot/snapshots/14-polish-and-docs/code/README.md).
- **Related versions/options:** [netsnapshot](../../netsnapshot). A corresponding learning option exists at netsnapshot. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/OpenSource_Upskilling_Snapshot1

**Stage 3: APIs and SQL. Related copy / alternative location.** [Open folder](../../geminiorganized/OpenSource_Upskilling_Snapshot1)

Simulated fullstack teaching artifact for a TypeScript/Node backend and React frontend inspired by enterprise global workforce platforms.

- **Stack:** languages: CSS; HTML; TypeScript.
- **Review:** Teaching/reference workspace; runtime not verified. Local documentation: This repository is a simulated fullstack teaching artifact for a TypeScript/Node backend and React frontend inspired by enterprise global workforce platforms. Each folder under snapshots is a complete copy of the codebase at that moment in the project, not a diff, so a junior engineer can read the s
- **Learn:** Incremental development, domain modeling, auth context and service refactoring.
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Follow 00-walking-skeleton then implement one company workflow without copying its solution first.
- **Evidence:** [README.md](../../geminiorganized/OpenSource_Upskilling_Snapshot1/README.md), [App.tsx](../../geminiorganized/OpenSource_Upskilling_Snapshot1/snapshots/07-refactor-service-and-hooks/code/apps/web/src/App.tsx), [README.md](../../geminiorganized/OpenSource_Upskilling_Snapshot1/snapshots/14-polish-docs/code/README.md).
- **Related versions/options:** [netsnapshot1](../../netsnapshot1). A corresponding learning option exists at netsnapshot1. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_.Todo

**Stage 4: Integrated full-stack workflows. Related copy / alternative location.** [Open folder](../../geminiorganized/General_.Todo)

ASP.NET Core eShopOnWeb reference storefront demonstrating a monolithic web application.

- **Stack:** languages: C#; CSS; JavaScript; Razor; SCSS; frameworks: ASP.NET Core; Blazor; data: Entity Framework Core; SQL Server; infrastructure: Docker; GitHub Actions; testing: MSTest; xUnit.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Layered ASP.NET application, EF Core, identity, storefronts
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Trace basket-to-order flow, then make one small tested change.
- **Evidence:** [README.md](../../geminiorganized/General_.Todo/eShopOnWeb/README.md), [Program.cs](../../geminiorganized/General_.Todo/eShopOnWeb/src/Web/Program.cs), [README.md](../../geminiorganized/General_.Todo/eShopOnWeb/fabledocs/README.md).
- **Related versions/options:** [.nettodo](../../.nettodo). A corresponding learning option exists at .nettodo. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Gitjira-App

**Stage 4: Integrated full-stack workflows. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Gitjira-App)

A Jira-style issue tracker, built in public as a teaching codebase — 15 sprints, each landing as one reviewed pull request full of learning artifacts. v1.0.0 .

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Express; Node.js; React; Vite; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Playwright; Vitest; integrations: BullMQ; Socket.IO.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Full-stack issue tracking, auth, relational data, reviewable delivery
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Trace one issue request, fix one bug, and ship one independently explained feature.
- **Evidence:** [README.md](../../geminiorganized/General_Gitjira-App/README.md), [App.jsx](../../geminiorganized/General_Gitjira-App/apps/web/src/App.jsx), [README.md](../../geminiorganized/General_Gitjira-App/docs/adr/README.md).
- **Related versions/options:** [gitjira-app](../../gitjira-app). A corresponding learning option exists at gitjira-app. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Ecommerceproject

**Stage 4: Integrated full-stack workflows. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Ecommerceproject)

A full-stack E-commerce Platform built for educational purposes to upskill to mid/senior SWE level.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** React/API separation, cart/order rules, Prisma
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Complete and test one order flow before adding new domains.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Ecommerceproject/README.md), [App.tsx](../../geminiorganized/LLM_Generated_Ecommerceproject/frontend/src/App.tsx), [docker-compose.yml](../../geminiorganized/LLM_Generated_Ecommerceproject/docker-compose.yml).
- **Related versions/options:** [grokbuildecommerceproject](../../grokbuildecommerceproject). A corresponding learning option exists at grokbuildecommerceproject. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Hrproject

**Stage 4: Integrated full-stack workflows. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Hrproject)

Full-stack HR / People Operations Platform (Educational)

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Jest; Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Employee data, leave workflows, pagination, RBAC
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Trace one leave request and test authorization.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Hrproject/README.md), [App.tsx](../../geminiorganized/LLM_Generated_Hrproject/frontend/src/App.tsx), [docker-compose.yml](../../geminiorganized/LLM_Generated_Hrproject/docker-compose.yml).
- **Related versions/options:** [grokbuildhrproject](../../grokbuildhrproject). A corresponding learning option exists at grokbuildhrproject. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Ppmproject

**Stage 4: Integrated full-stack workflows. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Ppmproject)

Project-portfolio management practice app with portfolios, programs, projects, and tasks.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Hierarchical domain models, relationships, permissions
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Add one hierarchy constraint and test an invalid relationship.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Ppmproject/README.md), [App.tsx](../../geminiorganized/LLM_Generated_Ppmproject/frontend/src/App.tsx), [docker-compose.yml](../../geminiorganized/LLM_Generated_Ppmproject/docker-compose.yml).
- **Related versions/options:** [grokbuildppmproject](../../grokbuildppmproject). A corresponding learning option exists at grokbuildppmproject. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Supportproject

**Stage 4: Integrated full-stack workflows. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Supportproject)

Full-stack Customer Support Ticketing + Knowledge Base Platform

- **Stack:** .
- **Review:** Static sample does not establish runtime readiness. Local documentation: This project is designed for learning, not production. The comments, journal, and plans are the main value.
- **Learn:** Support domain modeling, API planning, ticket workflows
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Use the specification only if choosing to build a support vertical slice.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Supportproject/README.md).
- **Related versions/options:** [grokbuildsupportproject](../../grokbuildsupportproject). A corresponding learning option exists at grokbuildsupportproject. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Teamproject

**Stage 4: Integrated full-stack workflows. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Teamproject)

A full-stack Team / Project Management application built for educational purposes.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Jest; Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Teams, project CRUD, JWT, validation, relational data
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Test one team-scoped API and its React loading/error states.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Teamproject/README.md), [App.tsx](../../geminiorganized/LLM_Generated_Teamproject/frontend/src/App.tsx), [docker-compose.yml](../../geminiorganized/LLM_Generated_Teamproject/docker-compose.yml).
- **Related versions/options:** [grokbuildteamproject](../../grokbuildteamproject). A corresponding learning option exists at grokbuildteamproject. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/OpenSource_Upskilling_.Ramp

**Stage 4: Integrated full-stack workflows. Related copy / alternative location.** [Open folder](../../geminiorganized/OpenSource_Upskilling_.Ramp)

A learning-oriented clone of Ramp / Expensify / Brex expense workflows, built with ASP.NET Core (C#) and React.

- **Stack:** languages: C#; CSS; HTML; JavaScript; frameworks: ASP.NET Core; React; Vite.
- **Review:** Teaching/reference workspace; runtime not verified. Local documentation: Storage/ In-memory DataStore (singleton) + demo seeding; background Channel, JSON) ships with the .NET SDK. Swapping the in-memory
- **Learn:** Role-scoped expense workflows, state machines, uploads
- **Before starting:** One local client app plus one API with persistence and basic tests.
- **Next:** Persist one expense workflow and test approval transitions.
- **Evidence:** [README.md](../../geminiorganized/OpenSource_Upskilling_.Ramp/README.md), [App.jsx](../../geminiorganized/OpenSource_Upskilling_.Ramp/frontend/src/App.jsx), [README.md](../../geminiorganized/OpenSource_Upskilling_.Ramp/docs/upskill/README.md).
- **Related versions/options:** [.netramp](../../.netramp). A corresponding learning option exists at .netramp. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/OpenSource_Upskilling_Linear

**Stage 4: Integrated full-stack workflows. Related copy / alternative location.** [Open folder](../../geminiorganized/OpenSource_Upskilling_Linear)

NetLinear is a Linear/Jira-style issue tracker scaffold built with .NET 8, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; PostgreSQL; Redis; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Teaching/reference workspace; runtime not verified. Local documentation: NetLinear is a Linear/Jira-style issue tracker scaffold built with .NET 8, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.
- **Learn:** REST, EF Core, filtered queries, optimistic mutations, xmin concurrency and workflow transitions.
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Complete an issue CRUD slice, then replace demo identity with authenticated users and prove stale-write conflict handling.
- **Evidence:** [README.md](../../geminiorganized/OpenSource_Upskilling_Linear/README.md), [Program.cs](../../geminiorganized/OpenSource_Upskilling_Linear/src/NetLinear.Api/Program.cs), [README.md](../../geminiorganized/OpenSource_Upskilling_Linear/docs/upskill/README.md).
- **Related versions/options:** [netlinear](../../netlinear). A corresponding learning option exists at netlinear. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Campusops

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Campusops)

CampusOps is a fifteen-sprint teaching repository for learning business-heavy C#/.NET API development and React/TypeScript integration through a university facilities platform.

- **Stack:** languages: C#; CSS; HTML; SQL; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; SQLite; infrastructure: GitHub Actions; testing: Vitest; xUnit.
- **Review:** Relevant implementation is present; runtime not verified. Local documentation: CampusOps.Infrastructure in-memory, SQLite, and integration adapters
- **Learn:** Business API workflows, React integration, persistence, operations
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** After BorrowBox, implement one facilities workflow end to end with tests.
- **Evidence:** [README.md](../../geminiorganized/General_Campusops/README.md), [Program.cs](../../geminiorganized/General_Campusops/src/CampusOps.Api/Program.cs), [package.json](../../geminiorganized/General_Campusops/web/CampusOps.Web/package.json).
- **Related versions/options:** [campusops](../../campusops). A corresponding learning option exists at campusops. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Globehire

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Globehire)

GlobeHire is a fifteen-sprint C#/.NET teaching repository for a fictional global workforce and employer-of-record platform.

- **Stack:** languages: C#; frameworks: ASP.NET Core; infrastructure: GitHub Actions; testing: xUnit.
- **Review:** Relevant implementation is present; runtime not verified. Local documentation: Infrastructure adapters (in-memory teaching adapters today); Use the HTTP examples, inspect /openapi/v1.json in Development, and check /health/live and /health/ready. The readiness response intentionally discloses that storage is in-memory and non-durable.
- **Learn:** Versioned rules, lifecycle changes, integration ports, API contracts
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** After CampusOps, change one fictional country rule without breaking API contracts.
- **Evidence:** [README.md](../../geminiorganized/General_Globehire/README.md), [Program.cs](../../geminiorganized/General_Globehire/src/GlobeHire.Api/Program.cs), [GlobeHire.Api.csproj](../../geminiorganized/General_Globehire/src/GlobeHire.Api/GlobeHire.Api.csproj).
- **Related versions/options:** [globehire](../../globehire). A corresponding learning option exists at globehire. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Meterforge

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Meterforge)

MeterForge is a fifteen-sprint C#/.NET teaching repository for a fictional multi-tenant usage-based subscription billing platform.

- **Stack:** languages: C#; SQL; frameworks: ASP.NET Core; data: PostgreSQL; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Relevant implementation is present; runtime not verified. Local documentation: In-memory, PostgreSQL, and simulated provider adapters; OpenAPI is available at /openapi/v1.json in Development. Check /health/live and /health/ready; readiness explicitly reports that the default runtime uses non-durable in-memory adapters. docker compose up postgres starts the local database used by the PostgreSQL adapter exercise.
- **Learn:** Money invariants, idempotency, concurrency, outbox, integrations
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** After CampusOps, prove duplicate usage does not double bill, then use a durable adapter.
- **Evidence:** [README.md](../../geminiorganized/General_Meterforge/README.md), [Program.cs](../../geminiorganized/General_Meterforge/src/MeterForge.Api/Program.cs), [docker-compose.yml](../../geminiorganized/General_Meterforge/docker-compose.yml).
- **Related versions/options:** [meterforge](../../meterforge). A corresponding learning option exists at meterforge. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Newcodecjs2

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Newcodecjs2)

This workspace contains five separate learning codebases generated from the pasted SaaS clone specs.

- **Stack:** languages: TypeScript; frameworks: Next.js; Node.js; React; Vite; data: Drizzle; testing: Vitest.
- **Review:** Static sample does not establish runtime readiness. Local documentation: Each project is intentionally scaffolded as a production-shaped TypeScript/React/Node app, but it is not wired for installation or deployment. The goal is reading, tracing, and modifying the architecture.
- **Learn:** Focused domain algorithms, policy checks, optimistic state and integration boundaries.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Choose one child by missing skill and turn one domain behavior into an independently verified vertical slice.
- **Evidence:** [README.md](../../geminiorganized/General_Newcodecjs2/README.md), [routes.ts](../../geminiorganized/General_Newcodecjs2/payr/src/server/routes.ts), [README.md](../../geminiorganized/General_Newcodecjs2/payr/README.md).
- **Related versions/options:** [newcodecjs2](../../newcodecjs2). A corresponding learning option exists at newcodecjs2. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Newcodex3

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Newcodex3)

This workspace contains five learning projects built with JavaScript, React, TypeScript, and Node patterns.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: Express; Node.js; React; Vite; data: Prisma; Redis; testing: Vitest; integrations: Socket.IO.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Compare equivalent domain patterns across TypeScript and C#; study one difficult invariant at a time.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Choose one topic and one language implementation; document gaps between scaffold code and production notes before extending it.
- **Evidence:** [README.md](../../geminiorganized/General_Newcodex3/README.md), [Program.cs](../../geminiorganized/General_Newcodex3/apps/27-ats-lite-net/server/Program.cs), [README.md](../../geminiorganized/General_Newcodex3/apps/27-ats-lite/README.md).
- **Related versions/options:** [newcodex3](../../newcodex3). A corresponding learning option exists at newcodex3. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Perch

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Perch)

Perch is a Greenhouse/Lever-style applicant tracking system and a teaching repository for junior engineers.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Fastify; Node.js; React; Vite; data: Prisma; infrastructure: GitHub Actions; testing: Vitest.
- **Review:** Static sample does not establish runtime readiness. Local documentation: Ports --> Memory[Deterministic in-memory adapters]; - packages/db: repository contracts, in-memory adapters, Prisma schema, demo seed.
- **Learn:** Multi-actor workflow, object authorization, state machines, bulk actions, ports/adapters and test design.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Follow one sprint playbook and implement a persistent repository adapter while retaining the authorization tests.
- **Evidence:** [README.md](../../geminiorganized/General_Perch/README.md), [App.tsx](../../geminiorganized/General_Perch/apps/web/src/App.tsx), [package.json](../../geminiorganized/General_Perch/package.json).
- **Related versions/options:** [perch](../../perch). A corresponding learning option exists at perch. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Skillforgejs

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Skillforgejs)

Skillforge is a web-first coding-skills learning platform built with Next.js App Router, TypeScript, Prisma/PostgreSQL, Auth.js, Tailwind, CodeMirror, server-side spaced repetition, and gamification.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; data: Prisma; infrastructure: Docker; GitHub Actions; testing: Playwright; Vitest; integrations: Stripe.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** App Router/server boundaries, Prisma, content schema validation, pure scheduling logic and tests.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Trace lesson completion into review state and add a deterministic scheduler/transaction test.
- **Evidence:** [README.md](../../geminiorganized/General_Skillforgejs/README.md), [auth.ts](../../geminiorganized/General_Skillforgejs/src/lib/auth.ts), [README.md](../../geminiorganized/General_Skillforgejs/docs/upskill/README.md).
- **Related versions/options:** [skillforgejs](../../skillforgejs). A corresponding learning option exists at skillforgejs. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Multitenantproject

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Multitenantproject)

A full-stack Multi-Tenant SaaS Starter built for educational purposes to upskill to mid/senior SWE level.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Vite; data: Prisma; infrastructure: Docker.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Tenant isolation, organization roles, scoped queries
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Add a test proving one tenant cannot access another tenant's project.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Multitenantproject/README.md), [App.tsx](../../geminiorganized/LLM_Generated_Multitenantproject/frontend/src/App.tsx), [docker-compose.yml](../../geminiorganized/LLM_Generated_Multitenantproject/docker-compose.yml).
- **Related versions/options:** [grokbuildmultitenantproject](../../grokbuildmultitenantproject). A corresponding learning option exists at grokbuildmultitenantproject. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Orderproject

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Orderproject)

Full-stack Order Management / Operations Platform (Educational)

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Express; Node.js; React; Tailwind CSS; Vite; data: Prisma; infrastructure: Docker; testing: Jest; Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Inventory, order transitions, transactional integrity
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Trace one inventory update and test rollback on failure.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Orderproject/README.md), [App.tsx](../../geminiorganized/LLM_Generated_Orderproject/frontend/src/App.tsx), [docker-compose.yml](../../geminiorganized/LLM_Generated_Orderproject/docker-compose.yml).
- **Related versions/options:** [grokbuildorderproject](../../grokbuildorderproject). A corresponding learning option exists at grokbuildorderproject. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/OpenSource_Upskilling_.Stripe

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/OpenSource_Upskilling_.Stripe)

A learning-oriented Stripe Billing / Chargebee style dashboard built with C#, .NET minimal APIs, and React.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite.
- **Review:** Teaching/reference workspace; runtime not verified. Local documentation: The backend uses an in-memory store so the project stays dependency-free and easy to study. In a production system, the store boundary is where a relational database, durable job queue, distributed idempotency table, and transactional outbox would be added.
- **Learn:** Money, idempotency, background payments, signed webhooks
- **Before starting:** A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Next:** Test duplicate payment requests and then persist idempotency state.
- **Evidence:** [README.md](../../geminiorganized/OpenSource_Upskilling_.Stripe/README.md), [Program.cs](../../geminiorganized/OpenSource_Upskilling_.Stripe/src/Billing.Api/Program.cs), [README.md](../../geminiorganized/OpenSource_Upskilling_.Stripe/docs2/README.md).
- **Related versions/options:** [.netstripe](../../.netstripe). A corresponding learning option exists at .netstripe. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/OpenSource_Upskilling_Docu

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/OpenSource_Upskilling_Docu)

NetDocu is a DocuSign-style signing workflow application with a .NET 8 clean-architecture API, PostgreSQL persistence, JWT/refresh-token auth, and a React + TypeScript signing workspace.

- **Stack:** languages: C#; CSS; HTML; JavaScript; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; PostgreSQL; Redis; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Teaching/reference workspace; runtime not verified. Local documentation: The initial test scaffold enforces core project reference direction:
- **Learn:** Document permissions, workflow state transitions, audit events, background processing.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Trace document creation to envelope completion; verify one unauthorized recipient and duplicate submission scenario.
- **Evidence:** [README.md](../../geminiorganized/OpenSource_Upskilling_Docu/README.md), [App.tsx](../../geminiorganized/OpenSource_Upskilling_Docu/frontend/src/App.tsx), [README.md](../../geminiorganized/OpenSource_Upskilling_Docu/frontend/README.md).
- **Related versions/options:** [netdocu](../../netdocu). A corresponding learning option exists at netdocu. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/OpenSource_Upskilling_Notion

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/OpenSource_Upskilling_Notion)

NetNotion is a Notion-style collaborative docs/wiki app built with .NET 8 Web API, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; PostgreSQL; Redis; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Teaching/reference workspace; runtime not verified.
- **Learn:** Recursive page trees, inherited permissions, block batching and immutable versions.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Trace page sharing and version restore; add an inherited-permission regression and reject tree cycles.
- **Evidence:** [README.md](../../geminiorganized/OpenSource_Upskilling_Notion/README.md), [App.tsx](../../geminiorganized/OpenSource_Upskilling_Notion/client/src/routes/App.tsx), [README.md](../../geminiorganized/OpenSource_Upskilling_Notion/docs/fable/README.md).
- **Related versions/options:** [netnotion](../../netnotion). A corresponding learning option exists at netnotion. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/OpenSource_Upskilling_Shop

**Stage 5: Domain rules and reliability. Related copy / alternative location.** [Open folder](../../geminiorganized/OpenSource_Upskilling_Shop)

NetShopifyLite is a .NET 8 + React ecommerce admin and lightweight storefront scaffold.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; PostgreSQL; Redis; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Teaching/reference workspace; runtime not verified. Local documentation: NetShopifyLite is a .NET 8 + React ecommerce admin and lightweight storefront scaffold. It follows a layered architecture:
- **Learn:** Money modeling, transactional inventory, idempotent checkout/refunds and domain invariants.
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Prove duplicate checkout/refund behavior and stock consistency with a real persistence integration test.
- **Evidence:** [README.md](../../geminiorganized/OpenSource_Upskilling_Shop/README.md), [App.tsx](../../geminiorganized/OpenSource_Upskilling_Shop/frontend/src/App.tsx), [README.md](../../geminiorganized/OpenSource_Upskilling_Shop/docs/upskill/README.md).
- **Related versions/options:** [netshop](../../netshop). A corresponding learning option exists at netshop. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_.Architectureproject

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_.Architectureproject)

Full Modular Monolith .NET application with Domain-Driven Design approach.

- **Stack:** languages: C#; HTML; SQL; frameworks: ASP.NET Core; data: SQL Server; infrastructure: Docker; GitHub Actions.
- **Review:** Teaching/reference workspace; runtime not verified.
- **Learn:** DDD boundaries, domain events, modular monoliths
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Trace one meeting command across module boundaries and explain its transaction.
- **Evidence:** [README.md](../../geminiorganized/General_.Architectureproject/modular-monolith-with-ddd/README.md), [Program.cs](../../geminiorganized/General_.Architectureproject/modular-monolith-with-ddd/src/Database/DatabaseMigrator/Program.cs), [README.md](../../geminiorganized/General_.Architectureproject/modular-monolith-with-ddd/docs/catalog-of-terms/README.md).
- **Related versions/options:** [.netarchitectureproject](../../.netarchitectureproject). A corresponding learning option exists at .netarchitectureproject. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_.Open2

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_.Open2)

Orchard Core is an open-source, modular, multi-tenant application framework and CMS for ASP.NET Core.

- **Stack:** languages: C#; CSS; HTML; JavaScript; Razor; SCSS; TypeScript; frameworks: ASP.NET Core; Vite; Vue; infrastructure: Docker; GitHub Actions; testing: Moq; xUnit.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Extensible CMS, tenants, dependency injection, mature code navigation
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Study one small module and propose one bounded fix.
- **Evidence:** [README.md](../../geminiorganized/General_.Open2/OrchardCore/README.md), [Program.cs](../../geminiorganized/General_.Open2/OrchardCore/src/OrchardCore.Cms.Web/Program.cs), [README.md](../../geminiorganized/General_.Open2/OrchardCore/src/docs/README.md).
- **Related versions/options:** [.netopen2](../../.netopen2). A corresponding learning option exists at .netopen2. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Cleanarch

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Cleanarch)

ASP.NET Core Clean Architecture starter/reference application.

- **Stack:** languages: C#; HTML; JavaScript; SCSS; TypeScript; frameworks: ASP.NET Core; data: Entity Framework Core; PostgreSQL; SQL Server; SQLite; infrastructure: GitHub Actions; testing: Moq; NUnit.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Dependency boundaries, CQRS, integration testing, architecture tradeoffs.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Compare one simple endpoint and handler against your own completed CRUD app; adopt only a justified pattern.
- **Evidence:** [README.md](../../geminiorganized/General_Cleanarch/CleanArchitecture/README.md), [Program.cs](../../geminiorganized/General_Cleanarch/CleanArchitecture/src/Web/Program.cs), [README.md](../../geminiorganized/General_Cleanarch/CleanArchitecture/fabledocs/README.md).
- **Related versions/options:** [netcleanarch](../../netcleanarch). A corresponding learning option exists at netcleanarch. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Gitvg

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Gitvg)

Relay workflow-automation teaching platform with triggers, actions, connectors, and execution-engine exercises.

- **Stack:** languages: C#; CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Next.js; Node.js; React; Tailwind CSS; Vite; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Playwright; Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Workflow engines, connectors, retries, durable execution
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Trace one failed workflow step and prove retry behavior is bounded.
- **Evidence:** [README.md](../../geminiorganized/General_Gitvg/relay/README.md), [App.tsx](../../geminiorganized/General_Gitvg/folio-app/client/src/App.tsx), [README.md](../../geminiorganized/General_Gitvg/pulse/README.md).
- **Related versions/options:** [gitvg/relay](../../gitvg/relay). A corresponding learning option exists at gitvg/relay. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Masternocu

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Masternocu)

NocoBase extensible low-code application platform.

- **Stack:** languages: CSS; HTML; JavaScript; SCSS; SQL; TypeScript; frameworks: React; data: MySQL; PostgreSQL; infrastructure: Docker; GitHub Actions; testing: Vitest; integrations: LangChain.
- **Review:** Static sample does not establish runtime readiness.
- **Learn:** Plugin architecture, schemas, permissions, large codebases
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Study one small plugin after owning a full-stack app.
- **Evidence:** [README.md](../../geminiorganized/General_Masternocu/nocobase/README.md), [server.ts](../../geminiorganized/General_Masternocu/nocobase/packages/plugins/%40nocobase/plugin-error-handler/src/server/server.ts), [README.md](../../geminiorganized/General_Masternocu/nocobase/docs/README.md).
- **Related versions/options:** [masternocu](../../masternocu). A corresponding learning option exists at masternocu. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Missioncontrol

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Missioncontrol)

A self-hosted control plane for fleets of AI agents — a C# / .NET 10 recreation of builderz-labs/mission-control per the Fleet Command — C# / .NET Technical Specification.

- **Stack:** languages: C#; CSS; Razor; frameworks: ASP.NET Core; data: Entity Framework Core; SQLite; testing: xUnit.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Agent control-plane APIs, auth, EF Core, scheduling
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Trace task claim concurrency and test two workers claiming one task.
- **Evidence:** [README.md](../../geminiorganized/General_Missioncontrol/README.md), [Program.cs](../../geminiorganized/General_Missioncontrol/src/FleetCommand.Host/Program.cs), [FleetCommand.Contracts.csproj](../../geminiorganized/General_Missioncontrol/src/FleetCommand.Contracts/FleetCommand.Contracts.csproj).
- **Related versions/options:** [missioncontrol](../../missioncontrol). A corresponding learning option exists at missioncontrol. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Nopsolutions

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Nopsolutions)

nopCommerce ecommerce application with storefront, administration, and plugins.

- **Stack:** languages: C#; CSS; HTML; JavaScript; Razor; SQL; frameworks: Express; data: PostgreSQL; SQL Server; infrastructure: Docker; GitHub Actions.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Large modular commerce application, plugin boundaries and order lifecycle.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Trace a single order service method and its callers/tests; compare it with the smaller netshop domain.
- **Evidence:** [README.md](../../geminiorganized/General_Nopsolutions/nopCommerce/README.md), [Program.cs](../../geminiorganized/General_Nopsolutions/nopCommerce/src/Presentation/Nop.Web/Program.cs), [README.md](../../geminiorganized/General_Nopsolutions/nopCommerce/fabledocs/README.md).
- **Related versions/options:** [nopsolutionsnet](../../nopsolutionsnet). A corresponding learning option exists at nopsolutionsnet. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Open1

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Open1)

A reference .NET application implementing an e-commerce website using a services-based architecture using .NET Aspire.

- **Stack:** languages: C#; CSS; HTML; JavaScript; Razor; TypeScript; frameworks: ASP.NET Core; Blazor; data: Entity Framework Core; PostgreSQL; infrastructure: GitHub Actions; testing: Playwright.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Service boundaries, distributed workflows, integration events and observability.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Follow checkout across services and diagram failure/retry boundaries after completing a monolith first.
- **Evidence:** [README.md](../../geminiorganized/General_Open1/eShop/README.md), [Program.cs](../../geminiorganized/General_Open1/eShop/src/WebApp/Program.cs), [README.md](../../geminiorganized/General_Open1/eShop/tests/README.md).
- **Related versions/options:** [netopen1](../../netopen1). A corresponding learning option exists at netopen1. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Open3

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Open3)

Umbraco content management system and its administration interface.

- **Stack:** languages: C#; TypeScript; JavaScript; frameworks: ASP.NET Core; Umbraco CMS; note: Upstream CMS reference; frontend tooling is one component..
- **Review:** Static sample does not establish runtime readiness.
- **Learn:** Large-repo navigation, extension architecture, management APIs, content caching and testing.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Select one management endpoint or backoffice component and trace its tests; scope a small contribution.
- **Evidence:** [README.md](../../geminiorganized/General_Open3/Umbraco-CMS/.github/README.md), [Program.cs](../../geminiorganized/General_Open3/Umbraco-CMS/src/Umbraco.Web.UI/Program.cs), [readme.md](../../geminiorganized/General_Open3/Umbraco-CMS/templates/readme.md).
- **Related versions/options:** [netopen3](../../netopen3). A corresponding learning option exists at netopen3. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Buildevent

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Buildevent)

TypeScript monorepo for a ticketing platform with a Next.js frontend, Fastify API, Prisma/PostgreSQL data layer, Redis-backed jobs, Stripe checkout hooks, signed QR tickets, and mobile check-in.

- **Stack:** languages: CSS; JavaScript; TypeScript; frameworks: Fastify; Next.js; Node.js; React; Tailwind CSS; data: Prisma; Redis; infrastructure: Docker; GitHub Actions; testing: Vitest; integrations: BullMQ; Stripe.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Ticket inventory, checkout hooks, queues, signed QR check-in
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Test duplicate checkout and repeat check-in behavior.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Buildevent/README.md), [server.ts](../../geminiorganized/LLM_Generated_Buildevent/apps/api/src/server.ts), [README.md](../../geminiorganized/LLM_Generated_Buildevent/docs/upskill/README.md).
- **Related versions/options:** [buildevent](../../buildevent). A corresponding learning option exists at buildevent. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Buildreviewer

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Buildreviewer)

A web-based code-review workspace for GitHub pull requests, inspired by ReviewFlow.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: NestJS; Node.js; React; Tailwind CSS; Vite; data: Prisma; testing: Jest; Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** GitHub APIs, local drafts, transactional publishing, review UX
- **Before starting:** Domain workflows, persistence, concurrency basics and operational debugging.
- **Next:** Trace local draft persistence and implement a failed-publish recovery case.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Buildreviewer/README.md), [Review.tsx](../../geminiorganized/LLM_Generated_Buildreviewer/apps/web/src/routes/Review.tsx), [package.json](../../geminiorganized/LLM_Generated_Buildreviewer/package.json).
- **Related versions/options:** [buildreviewer](../../buildreviewer). A corresponding learning option exists at buildreviewer. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/OpenSource_Upskilling_Auth

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/OpenSource_Upskilling_Auth)

Standalone identity provider for learning OAuth2/OIDC, JWT signing, refresh-token rotation, RBAC, MFA, and audit logging.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; PostgreSQL; Redis; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Teaching/reference workspace; runtime not verified. Local documentation: The current machine did not have the .NET SDK installed when this scaffold was created, so EF migration files were not generated locally. The infrastructure project includes a design-time AppDbContext factory; run the migration command in infra/postgres/README.md after installing .NET.
- **Learn:** OAuth grants, PKCE, token rotation/replay, signing keys, resource authorization.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Follow one authorization-code exchange and write a threat model plus negative tests around identity binding and replay.
- **Evidence:** [README.md](../../geminiorganized/OpenSource_Upskilling_Auth/README.md), [App.tsx](../../geminiorganized/OpenSource_Upskilling_Auth/frontend/src/routes/App.tsx), [README.md](../../geminiorganized/OpenSource_Upskilling_Auth/docs2/README.md).
- **Related versions/options:** [netauth](../../netauth). A corresponding learning option exists at netauth. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/OpenSource_Upskilling_Drop

**Stage 6: Architecture and advanced integrations. Related copy / alternative location.** [Open folder](../../geminiorganized/OpenSource_Upskilling_Drop)

Personal/team cloud storage built with .NET 8 Web API, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Stack:** languages: C#; CSS; HTML; JavaScript; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; PostgreSQL; Redis; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Teaching/reference workspace; runtime not verified. Local documentation: - Background processing pipeline with queued scan jobs, retry/dead-letter state, simulated EICAR detection, text extraction, image thumbnail generation, quarantine, and janitor cleanup.
- **Learn:** File metadata versus blobs, quotas, resumability, checksums, async processing.
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Trace an interrupted upload through resume, finalization and quota accounting; add failure/retry tests.
- **Evidence:** [README.md](../../geminiorganized/OpenSource_Upskilling_Drop/README.md), [App.tsx](../../geminiorganized/OpenSource_Upskilling_Drop/web/src/App.tsx), [README.md](../../geminiorganized/OpenSource_Upskilling_Drop/docs/upskill/README.md).
- **Related versions/options:** [netdrop](../../netdrop). A corresponding learning option exists at netdrop. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Aral

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Aral)

React PWA language-learning workspace with client-side SQLite, a progress-event log, and a thin synchronization backend.

- **Stack:** languages: CSS; HTML; Java; JavaScript; SQL; TypeScript; frameworks: Hono; Node.js; React; Tailwind CSS; Vite; data: Drizzle; testing: Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Offline SQLite, event logs, synchronization, shared schemas
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace one progress event from device storage to sync and rebuilt state.
- **Evidence:** [README.md](../../geminiorganized/General_Aral/README.md), [App.tsx](../../geminiorganized/General_Aral/packages/app/src/App.tsx), [package.json](../../geminiorganized/General_Aral/package.json).
- **Related versions/options:** [aral](../../aral). A corresponding learning option exists at aral. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Jsharness

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Jsharness)

VTCode Rust terminal coding-agent workspace.

- **Stack:** languages: JavaScript; Python; Ruby; Rust; TypeScript; frameworks: Axum; infrastructure: GitHub Actions; testing: Vitest.
- **Review:** Relevant implementation is present; runtime not verified. Local documentation: Scaffolds vtcode.toml, .vtcode/, and AGENTS.md in your project; vtcode init scaffold project config + AGENTS.md
- **Learn:** Rust CLI architecture, tools, agent protocols, terminal UI
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace one command from CLI parsing to tool execution and compare the TS port.
- **Evidence:** [README.md](../../geminiorganized/General_Jsharness/VTCode/README.md), [main.rs](../../geminiorganized/General_Jsharness/VTCode/src/main.rs), [README.md](../../geminiorganized/General_Jsharness/ctvodejs/README.md).
- **Related versions/options:** [jsharness/VTCode](../../jsharness/VTCode). A corresponding learning option exists at jsharness/VTCode. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Masteroutline

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Masteroutline)

A fast, collaborative, knowledge base for your team built using React and Node.js.Try out Outline using our hosted version at www.getoutline.com.

- **Stack:** languages: HTML; JavaScript; TypeScript; frameworks: React; Vite; data: PostgreSQL; Redis; infrastructure: AWS SDK; Docker; GitHub Actions; testing: Vitest; integrations: MCP; Socket.IO.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Mature collaborative editor, Koa, PostgreSQL, Redis, policies
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace one document permission rule and its tests.
- **Evidence:** [README.md](../../geminiorganized/General_Masteroutline/outline/README.md), [App.tsx](../../geminiorganized/General_Masteroutline/outline/app/components/Sidebar/App.tsx), [README.md](../../geminiorganized/General_Masteroutline/outline/fabledocs/README.md).
- **Related versions/options:** [masteroutline](../../masteroutline). A corresponding learning option exists at masteroutline. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Mobiletagalog

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Mobiletagalog)

A Duolingo-style app teaching Tagalog to English speakers, built with React Native + Expo.

- **Stack:** languages: JavaScript; TypeScript; frameworks: Expo; React; React Native.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Expo navigation, device SQLite, offline course content
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Test offline progress and one guest-to-account synchronization scenario.
- **Evidence:** [README.md](../../geminiorganized/General_Mobiletagalog/README.md), [AuthScreen.tsx](../../geminiorganized/General_Mobiletagalog/src/components/AuthScreen.tsx), [package.json](../../geminiorganized/General_Mobiletagalog/package.json).
- **Related versions/options:** [mobiletagalog](../../mobiletagalog). A corresponding learning option exists at mobiletagalog. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Open5

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Open5)

Jellyfin The Free Software Media System

- **Stack:** languages: C#; CSS; HTML; frameworks: ASP.NET Core; data: Entity Framework Core; SQLite; infrastructure: GitHub Actions.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Media services, background libraries, API compatibility and large codebase maintenance.
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace one user/library request into service and storage boundaries, then choose a narrow tested fix.
- **Evidence:** [README.md](../../geminiorganized/General_Open5/jellyfin/README.md), [Program.cs](../../geminiorganized/General_Open5/jellyfin/Jellyfin.Server/Program.cs), [README.md](../../geminiorganized/General_Open5/jellyfin/fuzz/README.md).
- **Related versions/options:** [netopen5](../../netopen5). A corresponding learning option exists at netopen5. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Spacegame

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Spacegame)

A server-authoritative, Tribal Wars-style multiplayer strategy game.

- **Stack:** languages: JavaScript; SQL; TypeScript; frameworks: Expo; Fastify; Node.js; React; React Native; data: Prisma; Redis; infrastructure: Docker; testing: Vitest; integrations: BullMQ; Socket.IO.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Deterministic simulation, concurrency, queues, reconciliation and mobile/realtime state.
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace one build/combat timer from command to worker to client, including duplicate delivery.
- **Evidence:** [README.md](../../geminiorganized/General_Spacegame/README.md), [auth.ts](../../geminiorganized/General_Spacegame/apps/server/src/routes/auth.ts), [package.json](../../geminiorganized/General_Spacegame/package.json).
- **Related versions/options:** [spacegame](../../spacegame). A corresponding learning option exists at spacegame. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/General_Tagalog

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/General_Tagalog)

A free Duolingo-style app teaching Tagalog to English speakers.

- **Stack:** languages: CSS; JavaScript; SQL; TypeScript; frameworks: Expo; Fastify; Next.js; Node.js; React; React Native; data: Drizzle; infrastructure: Docker; testing: Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Shared domain core, content compiler, offline event sync, idempotency and cross-platform delivery.
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace one lesson progress event through guest storage and authenticated sync; verify duplicate/offline replay handling.
- **Evidence:** [README.md](../../geminiorganized/General_Tagalog/README.md), [auth.ts](../../geminiorganized/General_Tagalog/apps/api/src/routes/auth.ts), [README.md](../../geminiorganized/General_Tagalog/docs/upskill/README.md).
- **Related versions/options:** [tagalog](../../tagalog). A corresponding learning option exists at tagalog. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Applybot

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Applybot)

AI-assisted job application filler for company career sites (Greenhouse, Lever, Ashby, Workday, and custom forms).

- **Stack:** languages: Python; testing: Playwright; integrations: Anthropic API; OpenAI API.
- **Review:** Static sample does not establish runtime readiness.
- **Learn:** Python browser automation, form extraction, LLM integration
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Test mapping against a local synthetic form before live sites.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Applybot/README.md), [ats.py](../../geminiorganized/LLM_Generated_Applybot/applybot/ats.py), [requirements.txt](../../geminiorganized/LLM_Generated_Applybot/requirements.txt).
- **Related versions/options:** [aiapplybot](../../aiapplybot). A corresponding learning option exists at aiapplybot. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Buildermentor

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Buildermentor)

A mastery-tracking study engine for junior software engineers leveling up to mid/senior and preparing for interviews.

- **Stack:** languages: CSS; HTML; JavaScript; SQL; TypeScript; frameworks: Fastify; Node.js; React; Tailwind CSS; Vite; data: Drizzle; PostgreSQL; infrastructure: Docker; GitHub Actions; testing: Playwright; Vitest; integrations: Anthropic API.
- **Review:** Relevant implementation is present; runtime not verified. Local documentation: - E2E scaffold in e2e/ (Playwright): cd e2e && pnpm install && npx playwright install chromium && npx playwright test with the dev stack running.
- **Learn:** Retrieval pipelines, mastery models, full-stack source ingestion
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Use only after basic study habits work; trace one ingestion and retrieval path.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Buildermentor/README.md), [server.ts](../../geminiorganized/LLM_Generated_Buildermentor/apps/api/src/server.ts), [package.json](../../geminiorganized/LLM_Generated_Buildermentor/package.json).
- **Related versions/options:** [buildermentor](../../buildermentor). A corresponding learning option exists at buildermentor. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Buildsmallplates

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Buildsmallplates)

Small Plates mobile weightlifting log with workout progression and on-device storage.

- **Stack:** languages: TypeScript; frameworks: Expo; React; React Native; testing: Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** React Native, local SQLite, progression algorithms
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Test one progression rule and database migration with retained workouts.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Buildsmallplates/README.md), [App.tsx](../../geminiorganized/LLM_Generated_Buildsmallplates/App.tsx), [package.json](../../geminiorganized/LLM_Generated_Buildsmallplates/package.json).
- **Related versions/options:** [buildsmallplates](../../buildsmallplates). A corresponding learning option exists at buildsmallplates. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Buildwhiteboard

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Buildwhiteboard)

Collaborative Markdown editor using React, TypeScript, Yjs and WebSockets, with local document storage, preview, and presence.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: React; Vite; infrastructure: Docker; GitHub Actions; testing: Playwright.
- **Review:** Relevant implementation is present; runtime not verified. Local documentation: A React, Vite, TypeScript, Yjs, and WebSocket-powered collaborative Markdown editor with durable local document storage, sanitized Markdown preview, collaborator presence, document metadata APIs, import/export tooling, CI, and Docker scaffolding.
- **Learn:** Yjs, WebSockets, collaborative editing, persistence
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Demonstrate two-client convergence after disconnect/reconnect.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Buildwhiteboard/README.md), [App.tsx](../../geminiorganized/LLM_Generated_Buildwhiteboard/client/src/App.tsx), [README.md](../../geminiorganized/LLM_Generated_Buildwhiteboard/client/README.md).
- **Related versions/options:** [buildwhiteboard](../../buildwhiteboard). A corresponding learning option exists at buildwhiteboard. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Fablehelperv2

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Fablehelperv2)

CueDeck is a free, local-first conversation practice and disclosed-assistance coach for Windows.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Electron; React; Vite; testing: Playwright; Vitest.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Electron architecture, disclosed conversation coaching, streaming
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Trace one audio-to-response flow and compare recovery against finalcallhelp.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Fablehelperv2/cuedeck/README.md), [App.tsx](../../geminiorganized/LLM_Generated_Fablehelperv2/cuedeck/src/renderer/App.tsx), [package.json](../../geminiorganized/LLM_Generated_Fablehelperv2/cuedeck/package.json).
- **Related versions/options:** [fableaihelperv2](../../fableaihelperv2). A corresponding learning option exists at fableaihelperv2. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Fablehelperv3

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Fablehelperv3)

Push-to-record interview copilot for Windows.

- **Stack:** languages: CSS; HTML; JavaScript; TypeScript; frameworks: Electron; Vite; testing: Vitest; integrations: Anthropic API.
- **Review:** Static sample does not establish runtime readiness.
- **Learn:** Low-latency streaming, Electron bridges, cancellation
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Measure and explain one mocked stream/cancel path before provider integration.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Fablehelperv3/README.md), [preload.ts](../../geminiorganized/LLM_Generated_Fablehelperv3/src/preload.ts), [package.json](../../geminiorganized/LLM_Generated_Fablehelperv3/package.json).
- **Related versions/options:** [fableaihelperv3](../../fableaihelperv3). A corresponding learning option exists at fableaihelperv3. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Helper

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Helper)

A Windows desktop app (Electron) that helps you answer questions during your own live calls and interviews.

- **Stack:** languages: CSS; HTML; JavaScript; frameworks: Electron.
- **Review:** Static sample does not establish runtime readiness.
- **Learn:** Electron IPC, audio transcription, streamed responses
- **Before starting:** Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Next:** Explain preload isolation and handle one failed provider request.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Helper/README.md), [preload.js](../../geminiorganized/LLM_Generated_Helper/src/preload.js), [README.md](../../geminiorganized/LLM_Generated_Helper/docs/README.md).
- **Related versions/options:** [aihelper](../../aihelper). A corresponding learning option exists at aihelper. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/LLM_Generated_Rag

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/LLM_Generated_Rag)

NetAiOps is a AI-powered IT operations platform built as a phased learning project.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; PostgreSQL; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Relevant implementation is present; runtime not verified.
- **Learn:** Layered .NET, RBAC, operational data, retrieval and evaluation design.
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace one ticket request through UI/API/persistence, then implement one documented retrieval slice with a small evaluation set.
- **Evidence:** [README.md](../../geminiorganized/LLM_Generated_Rag/README.md), [Program.cs](../../geminiorganized/LLM_Generated_Rag/src/Api/Program.cs), [README.md](../../geminiorganized/LLM_Generated_Rag/docs2.0/README.md).
- **Related versions/options:** [netairag](../../netairag). A corresponding learning option exists at netairag. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

#### geminiorganized/OpenSource_Upskilling_Intercom

**Stage 7: Specializations. Related copy / alternative location.** [Open folder](../../geminiorganized/OpenSource_Upskilling_Intercom)

A two-sided live chat (Intercom-style): an embeddable visitor widget plus an agent inbox for support teams.

- **Stack:** languages: C#; CSS; HTML; TypeScript; frameworks: ASP.NET Core; React; Vite; data: Entity Framework Core; PostgreSQL; infrastructure: Docker; GitHub Actions; testing: xUnit.
- **Review:** Teaching/reference workspace; runtime not verified. Local documentation: Presence — in-memory PresenceTracker fed by hub connect/disconnect plus client activity heartbeats. Grace periods prevent flapping: 60s after a disconnect the agent still counts as online (page refreshes don't flicker); 5 min without activity degrades to Away. A background sweeper broadcasts transit
- **Learn:** Realtime rooms, visitor versus agent auth, routing, presence and SLA jobs.
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace visitor session to agent reply and verify conversation authorization plus reconnect behavior.
- **Evidence:** [README.md](../../geminiorganized/OpenSource_Upskilling_Intercom/README.md), [Program.cs](../../geminiorganized/OpenSource_Upskilling_Intercom/src/NetIntercom.Api/Program.cs), [README.md](../../geminiorganized/OpenSource_Upskilling_Intercom/docs/upskill/README.md).
- **Related versions/options:** [netintercom](../../netintercom). A corresponding learning option exists at netintercom. Select one location after comparing the versions; a matching sample does not establish full-tree equality.

## Nested-app details and supplemental review notes

The following 75 child applications sit inside three already-counted workspaces. They receive their own learning assignments here without increasing the 389 workspace/resource count.

### newcodecjs2/blockr

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodecjs2/blockr)

Page/block editor

- **Stack:** TypeScript; React; Next.js declared; Drizzle declared; Vitest.
- **Review:** Architecture reading scaffold with domain functions and route sketches over in-memory stores; root explicitly says installation/deployment wiring is incomplete.
- **Learn:** Recursive blocks, ordering and inherited page permissions
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Reject a page cycle and test inherited permission denial.
- **Evidence:** [README.md](../../newcodecjs2/blockr/README.md), [routes.ts](../../newcodecjs2/blockr/src/server/routes.ts), [package.json](../../newcodecjs2/blockr/package.json).

- **Variant guidance:** One of five related SaaS exercises; not five production-complete products.

### newcodecjs2/bookr

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodecjs2/bookr)

Scheduling

- **Stack:** TypeScript; React; Next.js declared; Drizzle declared; Vitest.
- **Review:** Architecture reading scaffold with domain functions and route sketches over in-memory stores; root explicitly says installation/deployment wiring is incomplete.
- **Learn:** Timezone availability, slot revalidation, locking and calendar gateways
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Test daylight-saving and two users booking the same slot.
- **Evidence:** [README.md](../../newcodecjs2/bookr/README.md), [routes.ts](../../newcodecjs2/bookr/src/server/routes.ts), [package.json](../../newcodecjs2/bookr/package.json).

- **Variant guidance:** One of five related SaaS exercises; not five production-complete products.

### newcodecjs2/payr

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodecjs2/payr)

Mock payments dashboard

- **Stack:** TypeScript; React; Next.js declared; Drizzle declared; Vitest.
- **Review:** Architecture reading scaffold with domain functions and route sketches over in-memory stores; root explicitly says installation/deployment wiring is incomplete.
- **Learn:** RBAC, idempotency, cursor pages, API keys and webhook logs
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Replay one payment mutation and prove permission checks precede state changes.
- **Evidence:** [README.md](../../newcodecjs2/payr/README.md), [routes.ts](../../newcodecjs2/payr/src/server/routes.ts), [package.json](../../newcodecjs2/payr/package.json).

- **Variant guidance:** One of five related SaaS exercises; not five production-complete products.

### newcodecjs2/planr

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodecjs2/planr)

Issue tracker

- **Stack:** TypeScript; React; Next.js declared; Drizzle declared; Vitest.
- **Review:** Architecture reading scaffold with domain functions and route sketches over in-memory stores; root explicitly says installation/deployment wiring is incomplete.
- **Learn:** Optimistic queues, rollback, filtering and workflow rules
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Trace one failed optimistic issue mutation and verify rollback.
- **Evidence:** [README.md](../../newcodecjs2/planr/README.md), [routes.ts](../../newcodecjs2/planr/src/server/routes.ts), [package.json](../../newcodecjs2/planr/package.json).

- **Variant guidance:** One of five related SaaS exercises; not five production-complete products.

### newcodecjs2/helpkit

**Stage 7: Specializations. optional targeted exercise.** [Open app folder](../../newcodecjs2/helpkit)

Support inbox/widget

- **Stack:** TypeScript; React; Next.js declared; Drizzle declared; Vitest.
- **Review:** Architecture reading scaffold with domain functions and route sketches over in-memory stores; root explicitly says installation/deployment wiring is incomplete.
- **Learn:** Tenant isolation, assignment routing, room events and email normalization
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace a widget message and prove room fanout cannot cross tenants.
- **Evidence:** [README.md](../../newcodecjs2/helpkit/README.md), [routes.ts](../../newcodecjs2/helpkit/src/server/routes.ts), [package.json](../../newcodecjs2/helpkit/package.json).

- **Variant guidance:** One of five related SaaS exercises; not five production-complete products.

### newcodex3/apps/16-blog-platform

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodex3/apps/16-blog-platform)

Multi-user blog

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** RBAC, editorial state transitions and comment moderation
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Trace one draft-to-published transition and reject an unauthorized editor action.
- **Evidence:** [README.md](../../newcodex3/apps/16-blog-platform/README.md), [service.ts](../../newcodex3/apps/16-blog-platform/server/src/comments/service.ts), [package.json](../../newcodex3/apps/16-blog-platform/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/16-blog-platform-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/16-blog-platform-net

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodex3/apps/16-blog-platform-net)

Multi-user blog (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** RBAC, editorial state transitions and comment moderation
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Trace one draft-to-published transition and reject an unauthorized editor action.
- **Evidence:** [README.md](../../newcodex3/apps/16-blog-platform-net/README.md), [Program.cs](../../newcodex3/apps/16-blog-platform-net/server/BlogPlatform.Api/Program.cs), [package.json](../../newcodex3/apps/16-blog-platform-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/16-blog-platform; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/31-multi-tenant-crm

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodex3/apps/31-multi-tenant-crm)

Multi-tenant CRM

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Learn:** Tenant scoping, ownership, soft-delete and audit trails
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Replace header-only tenant assumptions and test cross-tenant access.
- **Evidence:** [README.md](../../newcodex3/apps/31-multi-tenant-crm/README.md), [index.ts](../../newcodex3/apps/31-multi-tenant-crm/server/src/index.ts), [package.json](../../newcodex3/apps/31-multi-tenant-crm/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/31-multi-tenant-crm-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/31-multi-tenant-crm-net

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodex3/apps/31-multi-tenant-crm-net)

Multi-tenant CRM (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Tenant scoping, ownership, soft-delete and audit trails
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Replace header-only tenant assumptions and test cross-tenant access.
- **Evidence:** [README.md](../../newcodex3/apps/31-multi-tenant-crm-net/README.md), [Program.cs](../../newcodex3/apps/31-multi-tenant-crm-net/server/Program.cs), [package.json](../../newcodex3/apps/31-multi-tenant-crm-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/31-multi-tenant-crm; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/38-admin-settings-permissions-console

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodex3/apps/38-admin-settings-permissions-console)

Admin settings/permissions

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Learn:** Granular RBAC, versioned settings and auditable updates
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Reject a stale settings update and prove viewer roles cannot mutate billing/security settings.
- **Evidence:** [README.md](../../newcodex3/apps/38-admin-settings-permissions-console/README.md), [index.ts](../../newcodex3/apps/38-admin-settings-permissions-console/server/src/index.ts), [package.json](../../newcodex3/apps/38-admin-settings-permissions-console/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/38-admin-settings-permissions-console-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/38-admin-settings-permissions-console-net

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodex3/apps/38-admin-settings-permissions-console-net)

Admin settings/permissions (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Granular RBAC, versioned settings and auditable updates
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Reject a stale settings update and prove viewer roles cannot mutate billing/security settings.
- **Evidence:** [README.md](../../newcodex3/apps/38-admin-settings-permissions-console-net/README.md), [Program.cs](../../newcodex3/apps/38-admin-settings-permissions-console-net/server/Program.cs), [package.json](../../newcodex3/apps/38-admin-settings-permissions-console-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/38-admin-settings-permissions-console; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/17-kanban-board

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/17-kanban-board)

Kanban board

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Nested state, fractional ordering, membership and expiring invitations
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Verify reorder stability and one-time invitation acceptance.
- **Evidence:** [README.md](../../newcodex3/apps/17-kanban-board/README.md), [service.ts](../../newcodex3/apps/17-kanban-board/server/src/boards/service.ts), [package.json](../../newcodex3/apps/17-kanban-board/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/17-kanban-board-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/17-kanban-board-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/17-kanban-board-net)

Kanban board (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Nested state, fractional ordering, membership and expiring invitations
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Verify reorder stability and one-time invitation acceptance.
- **Evidence:** [README.md](../../newcodex3/apps/17-kanban-board-net/README.md), [Program.cs](../../newcodex3/apps/17-kanban-board-net/server/Program.cs), [package.json](../../newcodex3/apps/17-kanban-board-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/17-kanban-board; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/19-ecommerce-storefront

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/19-ecommerce-storefront)

Ecommerce storefront

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Guest carts, integer money, inventory transactions and idempotent webhooks
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Verify cart merge and duplicate payment-event handling using a fake provider.
- **Evidence:** [README.md](../../newcodex3/apps/19-ecommerce-storefront/README.md), [service.ts](../../newcodex3/apps/19-ecommerce-storefront/server/src/cart/service.ts), [package.json](../../newcodex3/apps/19-ecommerce-storefront/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/19-ecommerce-storefront-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/19-ecommerce-storefront-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/19-ecommerce-storefront-net)

Ecommerce storefront (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Guest carts, integer money, inventory transactions and idempotent webhooks
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Verify cart merge and duplicate payment-event handling using a fake provider.
- **Evidence:** [README.md](../../newcodex3/apps/19-ecommerce-storefront-net/README.md), [Program.cs](../../newcodex3/apps/19-ecommerce-storefront-net/server/Program.cs), [package.json](../../newcodex3/apps/19-ecommerce-storefront-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/19-ecommerce-storefront; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/20-event-booking

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/20-event-booking)

Event booking

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Capacity locks, ticket allocation, waitlists and deferred notification
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Prove two competing bookings cannot overbook the last seat.
- **Evidence:** [README.md](../../newcodex3/apps/20-event-booking/README.md), [service.ts](../../newcodex3/apps/20-event-booking/server/src/bookings/service.ts), [package.json](../../newcodex3/apps/20-event-booking/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/20-event-booking-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/20-event-booking-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/20-event-booking-net)

Event booking (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Capacity locks, ticket allocation, waitlists and deferred notification
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Prove two competing bookings cannot overbook the last seat.
- **Evidence:** [README.md](../../newcodex3/apps/20-event-booking-net/README.md), [Program.cs](../../newcodex3/apps/20-event-booking-net/server/Program.cs), [package.json](../../newcodex3/apps/20-event-booking-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/20-event-booking; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/21-invoicing-app

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/21-invoicing-app)

Invoicing

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Integer money/tax, invoice transitions, recurring jobs and PDF/email boundaries
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Test rounding, duplicate recurring generation and invalid invoice transitions.
- **Evidence:** [README.md](../../newcodex3/apps/21-invoicing-app/README.md), [service.ts](../../newcodex3/apps/21-invoicing-app/server/src/email/service.ts), [package.json](../../newcodex3/apps/21-invoicing-app/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/21-invoicing-app-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/21-invoicing-app-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/21-invoicing-app-net)

Invoicing (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Integer money/tax, invoice transitions, recurring jobs and PDF/email boundaries
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Test rounding, duplicate recurring generation and invalid invoice transitions.
- **Evidence:** [README.md](../../newcodex3/apps/21-invoicing-app-net/README.md), [Program.cs](../../newcodex3/apps/21-invoicing-app-net/server/Program.cs), [package.json](../../newcodex3/apps/21-invoicing-app-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/21-invoicing-app; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/22-team-wiki

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/22-team-wiki)

Team wiki

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Recursive trees, immutable revisions, restore and page permissions
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Reject a page cycle and prove restored content keeps its revision history.
- **Evidence:** [README.md](../../newcodex3/apps/22-team-wiki/README.md), [service.ts](../../newcodex3/apps/22-team-wiki/server/src/pages/service.ts), [package.json](../../newcodex3/apps/22-team-wiki/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/22-team-wiki-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/22-team-wiki-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/22-team-wiki-net)

Team wiki (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Recursive trees, immutable revisions, restore and page permissions
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Reject a page cycle and prove restored content keeps its revision history.
- **Evidence:** [README.md](../../newcodex3/apps/22-team-wiki-net/README.md), [Program.cs](../../newcodex3/apps/22-team-wiki-net/server/Program.cs), [package.json](../../newcodex3/apps/22-team-wiki-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/22-team-wiki; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/23-survey-form-builder

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/23-survey-form-builder)

Survey/form builder

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Versioned dynamic schemas, conditional logic, validation and analytics
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Validate a response against its published schema and reject hidden invalid inputs.
- **Evidence:** [README.md](../../newcodex3/apps/23-survey-form-builder/README.md), [service.ts](../../newcodex3/apps/23-survey-form-builder/server/src/forms/service.ts), [package.json](../../newcodex3/apps/23-survey-form-builder/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/23-survey-form-builder-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/23-survey-form-builder-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/23-survey-form-builder-net)

Survey/form builder (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Versioned dynamic schemas, conditional logic, validation and analytics
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Validate a response against its published schema and reject hidden invalid inputs.
- **Evidence:** [README.md](../../newcodex3/apps/23-survey-form-builder-net/README.md), [Program.cs](../../newcodex3/apps/23-survey-form-builder-net/server/Program.cs), [package.json](../../newcodex3/apps/23-survey-form-builder-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/23-survey-form-builder; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/25-discussion-forum

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/25-discussion-forum)

Discussion forum

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Comment trees, vote uniqueness, ranking and rate limits
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Prove one user cannot cast duplicate votes and test thread ordering.
- **Evidence:** [README.md](../../newcodex3/apps/25-discussion-forum/README.md), [service.ts](../../newcodex3/apps/25-discussion-forum/server/src/comments/service.ts), [package.json](../../newcodex3/apps/25-discussion-forum/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/25-discussion-forum-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/25-discussion-forum-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/25-discussion-forum-net)

Discussion forum (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Comment trees, vote uniqueness, ranking and rate limits
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Prove one user cannot cast duplicate votes and test thread ordering.
- **Evidence:** [README.md](../../newcodex3/apps/25-discussion-forum-net/README.md), [Program.cs](../../newcodex3/apps/25-discussion-forum-net/server/Program.cs), [package.json](../../newcodex3/apps/25-discussion-forum-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/25-discussion-forum; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/26-subscription-reminders

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/26-subscription-reminders)

Subscription reminders

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Local-calendar timezones, recurring queues and notification preferences
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Test one daylight-saving transition and duplicate reminder delivery.
- **Evidence:** [README.md](../../newcodex3/apps/26-subscription-reminders/README.md), [service.ts](../../newcodex3/apps/26-subscription-reminders/server/src/analytics/service.ts), [package.json](../../newcodex3/apps/26-subscription-reminders/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/26-subscription-reminders-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/26-subscription-reminders-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/26-subscription-reminders-net)

Subscription reminders (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Local-calendar timezones, recurring queues and notification preferences
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Test one daylight-saving transition and duplicate reminder delivery.
- **Evidence:** [README.md](../../newcodex3/apps/26-subscription-reminders-net/README.md), [Program.cs](../../newcodex3/apps/26-subscription-reminders-net/server/Program.cs), [package.json](../../newcodex3/apps/26-subscription-reminders-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/26-subscription-reminders; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/27-ats-lite

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/27-ats-lite)

Applicant tracking

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Multi-actor pipelines, file-scan states and interview conflict detection
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Reject overlapping interviews and unauthorized pipeline changes.
- **Evidence:** [README.md](../../newcodex3/apps/27-ats-lite/README.md), [service.ts](../../newcodex3/apps/27-ats-lite/server/src/applications/service.ts), [package.json](../../newcodex3/apps/27-ats-lite/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/27-ats-lite-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/27-ats-lite-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/27-ats-lite-net)

Applicant tracking (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Multi-actor pipelines, file-scan states and interview conflict detection
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Reject overlapping interviews and unauthorized pipeline changes.
- **Evidence:** [README.md](../../newcodex3/apps/27-ats-lite-net/README.md), [Program.cs](../../newcodex3/apps/27-ats-lite-net/server/Program.cs), [package.json](../../newcodex3/apps/27-ats-lite-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/27-ats-lite; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/28-restaurant-reservations

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/28-restaurant-reservations)

Restaurant reservations

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Resource intervals, table combinations, turn times and notification boundaries
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Verify overlapping table reservations and capacity edge cases.
- **Evidence:** [README.md](../../newcodex3/apps/28-restaurant-reservations/README.md), [service.ts](../../newcodex3/apps/28-restaurant-reservations/server/src/bookings/service.ts), [package.json](../../newcodex3/apps/28-restaurant-reservations/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/28-restaurant-reservations-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/28-restaurant-reservations-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/28-restaurant-reservations-net)

Restaurant reservations (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Resource intervals, table combinations, turn times and notification boundaries
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Verify overlapping table reservations and capacity edge cases.
- **Evidence:** [README.md](../../newcodex3/apps/28-restaurant-reservations-net/README.md), [Program.cs](../../newcodex3/apps/28-restaurant-reservations-net/server/Program.cs), [package.json](../../newcodex3/apps/28-restaurant-reservations-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/28-restaurant-reservations; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/29-personal-finance-dashboard

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/29-personal-finance-dashboard)

Personal-finance dashboard

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** CSV normalization, fingerprints, categorization rules and reporting
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Import the same sample twice and prove deterministic deduplication.
- **Evidence:** [README.md](../../newcodex3/apps/29-personal-finance-dashboard/README.md), [service.ts](../../newcodex3/apps/29-personal-finance-dashboard/server/src/budgets/service.ts), [package.json](../../newcodex3/apps/29-personal-finance-dashboard/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/29-personal-finance-dashboard-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/29-personal-finance-dashboard-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/29-personal-finance-dashboard-net)

Personal-finance dashboard (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** CSV normalization, fingerprints, categorization rules and reporting
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Import the same sample twice and prove deterministic deduplication.
- **Evidence:** [README.md](../../newcodex3/apps/29-personal-finance-dashboard-net/README.md), [Program.cs](../../newcodex3/apps/29-personal-finance-dashboard-net/server/Program.cs), [package.json](../../newcodex3/apps/29-personal-finance-dashboard-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/29-personal-finance-dashboard; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/32-helpdesk-ticketing

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/32-helpdesk-ticketing)

Helpdesk ticketing

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Learn:** Ticket lifecycle, internal/public comments and SLA jobs
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Prove internal notes stay private and a reopened ticket recomputes SLA correctly.
- **Evidence:** [README.md](../../newcodex3/apps/32-helpdesk-ticketing/README.md), [index.ts](../../newcodex3/apps/32-helpdesk-ticketing/server/src/index.ts), [package.json](../../newcodex3/apps/32-helpdesk-ticketing/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/32-helpdesk-ticketing-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/32-helpdesk-ticketing-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/32-helpdesk-ticketing-net)

Helpdesk ticketing (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Ticket lifecycle, internal/public comments and SLA jobs
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Prove internal notes stay private and a reopened ticket recomputes SLA correctly.
- **Evidence:** [README.md](../../newcodex3/apps/32-helpdesk-ticketing-net/README.md), [Program.cs](../../newcodex3/apps/32-helpdesk-ticketing-net/server/Program.cs), [package.json](../../newcodex3/apps/32-helpdesk-ticketing-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/32-helpdesk-ticketing; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/33-inventory-warehouse-manager

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/33-inventory-warehouse-manager)

Inventory/warehouse manager

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Learn:** Immutable stock movements, transfers and reconciliation
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Prove a transfer balances both locations and duplicate requests do not add stock.
- **Evidence:** [README.md](../../newcodex3/apps/33-inventory-warehouse-manager/README.md), [index.ts](../../newcodex3/apps/33-inventory-warehouse-manager/server/src/index.ts), [package.json](../../newcodex3/apps/33-inventory-warehouse-manager/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/33-inventory-warehouse-manager-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/33-inventory-warehouse-manager-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/33-inventory-warehouse-manager-net)

Inventory/warehouse manager (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Immutable stock movements, transfers and reconciliation
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Prove a transfer balances both locations and duplicate requests do not add stock.
- **Evidence:** [README.md](../../newcodex3/apps/33-inventory-warehouse-manager-net/README.md), [Program.cs](../../newcodex3/apps/33-inventory-warehouse-manager-net/server/Program.cs), [package.json](../../newcodex3/apps/33-inventory-warehouse-manager-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/33-inventory-warehouse-manager; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/35-analytics-reporting-dashboard

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/35-analytics-reporting-dashboard)

Analytics/reporting dashboard

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Learn:** Validated filters, aggregation, export jobs and permissions
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Verify report authorization and move one expensive export into a durable job.
- **Evidence:** [README.md](../../newcodex3/apps/35-analytics-reporting-dashboard/README.md), [index.ts](../../newcodex3/apps/35-analytics-reporting-dashboard/server/src/index.ts), [package.json](../../newcodex3/apps/35-analytics-reporting-dashboard/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/35-analytics-reporting-dashboard-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/35-analytics-reporting-dashboard-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/35-analytics-reporting-dashboard-net)

Analytics/reporting dashboard (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Validated filters, aggregation, export jobs and permissions
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Verify report authorization and move one expensive export into a durable job.
- **Evidence:** [README.md](../../newcodex3/apps/35-analytics-reporting-dashboard-net/README.md), [Program.cs](../../newcodex3/apps/35-analytics-reporting-dashboard-net/server/Program.cs), [package.json](../../newcodex3/apps/35-analytics-reporting-dashboard-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/35-analytics-reporting-dashboard; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/37-bulk-import-review-tool

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/37-bulk-import-review-tool)

Bulk import/review

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Learn:** Staging, mapping, row errors, approval, idempotent commit and rollback
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Commit an approved batch twice and prove rollback scope does not affect unrelated data.
- **Evidence:** [README.md](../../newcodex3/apps/37-bulk-import-review-tool/README.md), [index.ts](../../newcodex3/apps/37-bulk-import-review-tool/server/src/index.ts), [package.json](../../newcodex3/apps/37-bulk-import-review-tool/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/37-bulk-import-review-tool-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/37-bulk-import-review-tool-net

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodex3/apps/37-bulk-import-review-tool-net)

Bulk import/review (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Staging, mapping, row errors, approval, idempotent commit and rollback
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Commit an approved batch twice and prove rollback scope does not affect unrelated data.
- **Evidence:** [README.md](../../newcodex3/apps/37-bulk-import-review-tool-net/README.md), [Program.cs](../../newcodex3/apps/37-bulk-import-review-tool-net/server/Program.cs), [package.json](../../newcodex3/apps/37-bulk-import-review-tool-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/37-bulk-import-review-tool; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/24-file-sharing-app

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/24-file-sharing-app)

File sharing

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Object storage, quotas, upload sessions and expiring share tokens
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Trace upload finalization and verify ownership, quota and expired-share rejection.
- **Evidence:** [README.md](../../newcodex3/apps/24-file-sharing-app/README.md), [service.ts](../../newcodex3/apps/24-file-sharing-app/server/src/files/service.ts), [package.json](../../newcodex3/apps/24-file-sharing-app/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/24-file-sharing-app-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/24-file-sharing-app-net

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/24-file-sharing-app-net)

File sharing (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Object storage, quotas, upload sessions and expiring share tokens
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Trace upload finalization and verify ownership, quota and expired-share rejection.
- **Evidence:** [README.md](../../newcodex3/apps/24-file-sharing-app-net/README.md), [Program.cs](../../newcodex3/apps/24-file-sharing-app-net/server/Program.cs), [package.json](../../newcodex3/apps/24-file-sharing-app-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/24-file-sharing-app; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/30-headless-cms

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/30-headless-cms)

Headless CMS

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Schema-as-data, public API versioning, API keys and webhook retry
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Validate a content type end to end and test key isolation plus retry idempotency.
- **Evidence:** [README.md](../../newcodex3/apps/30-headless-cms/README.md), [service.ts](../../newcodex3/apps/30-headless-cms/server/src/api-keys/service.ts), [package.json](../../newcodex3/apps/30-headless-cms/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/30-headless-cms-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/30-headless-cms-net

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/30-headless-cms-net)

Headless CMS (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Schema-as-data, public API versioning, API keys and webhook retry
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Validate a content type end to end and test key isolation plus retry idempotency.
- **Evidence:** [README.md](../../newcodex3/apps/30-headless-cms-net/README.md), [Program.cs](../../newcodex3/apps/30-headless-cms-net/server/Program.cs), [package.json](../../newcodex3/apps/30-headless-cms-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/30-headless-cms; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/34-oauth-saas-identity-portal

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/34-oauth-saas-identity-portal)

OAuth/SaaS identity portal

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Learn:** Session lifecycle, refresh revocation, reset flows and audit events
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Trace identity proof and refresh replay rejection; replace any placeholder login behavior.
- **Evidence:** [README.md](../../newcodex3/apps/34-oauth-saas-identity-portal/README.md), [index.ts](../../newcodex3/apps/34-oauth-saas-identity-portal/server/src/index.ts), [package.json](../../newcodex3/apps/34-oauth-saas-identity-portal/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/34-oauth-saas-identity-portal-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/34-oauth-saas-identity-portal-net

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/34-oauth-saas-identity-portal-net)

OAuth/SaaS identity portal (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Session lifecycle, refresh revocation, reset flows and audit events
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Trace identity proof and refresh replay rejection; replace any placeholder login behavior.
- **Evidence:** [README.md](../../newcodex3/apps/34-oauth-saas-identity-portal-net/README.md), [Program.cs](../../newcodex3/apps/34-oauth-saas-identity-portal-net/server/Program.cs), [package.json](../../newcodex3/apps/34-oauth-saas-identity-portal-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/34-oauth-saas-identity-portal; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/36-feature-flag-management

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/36-feature-flag-management)

Feature flags

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Learn:** Deterministic bucketing, targeting, environment isolation and cache invalidation
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Prove rollout assignment is stable and isolated per environment.
- **Evidence:** [README.md](../../newcodex3/apps/36-feature-flag-management/README.md), [index.ts](../../newcodex3/apps/36-feature-flag-management/server/src/index.ts), [package.json](../../newcodex3/apps/36-feature-flag-management/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/36-feature-flag-management-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/36-feature-flag-management-net

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/36-feature-flag-management-net)

Feature flags (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Deterministic bucketing, targeting, environment isolation and cache invalidation
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Prove rollout assignment is stable and isolated per environment.
- **Evidence:** [README.md](../../newcodex3/apps/36-feature-flag-management-net/README.md), [Program.cs](../../newcodex3/apps/36-feature-flag-management-net/server/Program.cs), [package.json](../../newcodex3/apps/36-feature-flag-management-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/36-feature-flag-management; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/39-third-party-integration-sync-hub

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/39-third-party-integration-sync-hub)

Integration sync hub

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Learn:** Provider boundaries, cursor sync, webhooks, retry and conflict resolution
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Replay a failed page/webhook and prove cursor advancement does not lose or duplicate records.
- **Evidence:** [README.md](../../newcodex3/apps/39-third-party-integration-sync-hub/README.md), [index.ts](../../newcodex3/apps/39-third-party-integration-sync-hub/server/src/index.ts), [package.json](../../newcodex3/apps/39-third-party-integration-sync-hub/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/39-third-party-integration-sync-hub-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/39-third-party-integration-sync-hub-net

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/39-third-party-integration-sync-hub-net)

Integration sync hub (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Provider boundaries, cursor sync, webhooks, retry and conflict resolution
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Replay a failed page/webhook and prove cursor advancement does not lose or duplicate records.
- **Evidence:** [README.md](../../newcodex3/apps/39-third-party-integration-sync-hub-net/README.md), [Program.cs](../../newcodex3/apps/39-third-party-integration-sync-hub-net/server/Program.cs), [package.json](../../newcodex3/apps/39-third-party-integration-sync-hub-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/39-third-party-integration-sync-hub; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/40-observability-incident-dashboard

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/40-observability-incident-dashboard)

Observability/incident dashboard

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Learn:** Incident state, alerts, timelines and operations workflows
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Connect one real structured event to a reproducible incident timeline and recovery drill.
- **Evidence:** [README.md](../../newcodex3/apps/40-observability-incident-dashboard/README.md), [index.ts](../../newcodex3/apps/40-observability-incident-dashboard/server/src/index.ts), [package.json](../../newcodex3/apps/40-observability-incident-dashboard/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/40-observability-incident-dashboard-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/40-observability-incident-dashboard-net

**Stage 6: Architecture and advanced integrations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/40-observability-incident-dashboard-net)

Observability/incident dashboard (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Incident state, alerts, timelines and operations workflows
- **Before starting:** Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Next:** Connect one real structured event to a reproducible incident timeline and recovery drill.
- **Evidence:** [README.md](../../newcodex3/apps/40-observability-incident-dashboard-net/README.md), [Program.cs](../../newcodex3/apps/40-observability-incident-dashboard-net/server/Program.cs), [package.json](../../newcodex3/apps/40-observability-incident-dashboard-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/40-observability-incident-dashboard; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/18-team-chat

**Stage 7: Specializations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/18-team-chat)

Team chat

- **Stack:** TypeScript; Express; React; Vite; Prisma schema.
- **Review:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Learn:** Message cursors, optimistic reconciliation, presence and realtime transport
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace a message across reconnect and prevent duplicate delivery.
- **Evidence:** [README.md](../../newcodex3/apps/18-team-chat/README.md), [service.ts](../../newcodex3/apps/18-team-chat/server/src/messages/service.ts), [package.json](../../newcodex3/apps/18-team-chat/server/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/18-team-chat-net; study one first and use the other only for language/pattern comparison.

### newcodex3/apps/18-team-chat-net

**Stage 7: Specializations. optional targeted exercise.** [Open app folder](../../newcodex3/apps/18-team-chat-net)

Team chat (.NET variant)

- **Stack:** C#; ASP.NET Core minimal API; React; TypeScript; Vite.
- **Review:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Learn:** Message cursors, optimistic reconciliation, presence and realtime transport
- **Before starting:** Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Next:** Trace a message across reconnect and prevent duplicate delivery.
- **Evidence:** [README.md](../../newcodex3/apps/18-team-chat-net/README.md), [Program.cs](../../newcodex3/apps/18-team-chat-net/server/Program.cs), [package.json](../../newcodex3/apps/18-team-chat-net/client/package.json).

- **Variant guidance:** Paired language variant of newcodex3/apps/18-team-chat; study one first and use the other only for language/pattern comparison.

### newcodexJS/01-task-manager

**Stage 3: APIs and SQL. main-path candidate.** [Open app folder](../../newcodexJS/01-task-manager)

Task manager

- **Stack:** JavaScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified.
- **Learn:** Basic REST, validation, React state and SQL queries
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Build and explain one create/edit/filter/delete flow, including invalid input.
- **Evidence:** [README.md](../../newcodexJS/01-task-manager/README.md), [taskService.js](../../newcodexJS/01-task-manager/server/src/services/taskService.js), [package.json](../../newcodexJS/01-task-manager/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/02-contact-book

**Stage 3: APIs and SQL. optional targeted exercise.** [Open app folder](../../newcodexJS/02-contact-book)

Contact book

- **Stack:** JavaScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified.
- **Learn:** Many-to-many tags, pagination, debounced search and CSV
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Add a contact with tags and verify pagination plus malformed CSV handling.
- **Evidence:** [README.md](../../newcodexJS/02-contact-book/README.md), [contactService.js](../../newcodexJS/02-contact-book/server/src/services/contactService.js), [package.json](../../newcodexJS/02-contact-book/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/03-expense-tracker

**Stage 3: APIs and SQL. optional targeted exercise.** [Open app folder](../../newcodexJS/03-expense-tracker)

Expense tracker

- **Stack:** JavaScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified.
- **Learn:** SQL aggregation, category budgets, filters and charts
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Verify monthly totals and category boundaries with a small deterministic dataset.
- **Evidence:** [README.md](../../newcodexJS/03-expense-tracker/README.md), [expenseService.js](../../newcodexJS/03-expense-tracker/server/src/services/expenseService.js), [package.json](../../newcodexJS/03-expense-tracker/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/04-notes-app

**Stage 3: APIs and SQL. optional targeted exercise.** [Open app folder](../../newcodexJS/04-notes-app)

Notes app

- **Stack:** JavaScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Learn:** Generic CRUD with markdown/folder/tag/autosave learning goals
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Implement and verify one actual autosave or search behavior beyond the generic scaffold.
- **Evidence:** [README.md](../../newcodexJS/04-notes-app/README.md), [service.js](../../newcodexJS/04-notes-app/server/src/services/service.js), [package.json](../../newcodexJS/04-notes-app/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/06-bookmark-manager

**Stage 3: APIs and SQL. optional targeted exercise.** [Open app folder](../../newcodexJS/06-bookmark-manager)

Bookmark manager

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Learn:** Typed validation, URL metadata boundaries and API conventions
- **Before starting:** React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Next:** Implement one validated bookmark create flow and a safe metadata-fetch boundary.
- **Evidence:** [README.md](../../newcodexJS/06-bookmark-manager/README.md), [service.ts](../../newcodexJS/06-bookmark-manager/server/src/services/service.ts), [package.json](../../newcodexJS/06-bookmark-manager/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/05-recipe-manager

**Stage 4: Integrated full-stack workflows. main-path candidate.** [Open app folder](../../newcodexJS/05-recipe-manager)

Recipe manager with accounts

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified.
- **Learn:** JWT/refresh lifecycle, protected routes and nested Knex transactions
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Trace sign-in to recipe ownership and prove a failed nested write rolls back.
- **Evidence:** [README.md](../../newcodexJS/05-recipe-manager/README.md), [authService.ts](../../newcodexJS/05-recipe-manager/server/src/services/authService.ts), [package.json](../../newcodexJS/05-recipe-manager/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/07-blog-platform

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodexJS/07-blog-platform)

Blog platform

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Learn:** Content rendering, sanitization and publication workflow
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Verify rendered content safety and one authorized publish transition.
- **Evidence:** [README.md](../../newcodexJS/07-blog-platform/README.md), [service.ts](../../newcodexJS/07-blog-platform/server/src/services/service.ts), [package.json](../../newcodexJS/07-blog-platform/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/08-kanban-board

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodexJS/08-kanban-board)

Kanban board

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Learn:** Optimistic drag order and fractional ordering concepts
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Implement persistent reorder and verify two concurrent updates cannot silently lose a card.
- **Evidence:** [README.md](../../newcodexJS/08-kanban-board/README.md), [service.ts](../../newcodexJS/08-kanban-board/server/src/services/service.ts), [package.json](../../newcodexJS/08-kanban-board/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/09-job-application-tracker

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodexJS/09-job-application-tracker)

Job application tracker

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Learn:** Pipeline transitions, attachment boundaries and history
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Implement one status transition with an auditable history record.
- **Evidence:** [README.md](../../newcodexJS/09-job-application-tracker/README.md), [service.ts](../../newcodexJS/09-job-application-tracker/server/src/services/service.ts), [package.json](../../newcodexJS/09-job-application-tracker/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/10-inventory-management

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodexJS/10-inventory-management)

Inventory management

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Learn:** Stock movement ledger and purchase/sales workflow concepts
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Replace direct stock edits with a transaction-backed movement and test totals.
- **Evidence:** [README.md](../../newcodexJS/10-inventory-management/README.md), [service.ts](../../newcodexJS/10-inventory-management/server/src/services/service.ts), [package.json](../../newcodexJS/10-inventory-management/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/11-survey-builder

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodexJS/11-survey-builder)

Survey builder

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. README describes development/demo identity headers rather than completed authentication.
- **Learn:** Public response validation, nested questions and result aggregation
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Verify a response cannot target unpublished or foreign questions; replace demo identity for admin flows.
- **Evidence:** [README.md](../../newcodexJS/11-survey-builder/README.md), [surveyService.ts](../../newcodexJS/11-survey-builder/server/src/services/surveyService.ts), [package.json](../../newcodexJS/11-survey-builder/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/12-chat-polling

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodexJS/12-chat-polling)

HTTP-polling chat

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. README describes development/demo identity headers rather than completed authentication.
- **Learn:** Conversation membership, polling cursors and read state
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Test reconnect/poll overlap without duplicate messages and replace demo-user headers.
- **Evidence:** [README.md](../../newcodexJS/12-chat-polling/README.md), [chatService.ts](../../newcodexJS/12-chat-polling/server/src/services/chatService.ts), [package.json](../../newcodexJS/12-chat-polling/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/16-team-project-management

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodexJS/16-team-project-management)

Team-project management

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Shares a generic scoped CRUD/admin structure with 16-20; specialized title does not establish a complete domain engine.
- **Learn:** Generic scoped CRUD, saved views, comments, audit and bulk status
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Prove project scope and bulk-change auditing on one complete workflow.
- **Evidence:** [README.md](../../newcodexJS/16-team-project-management/README.md), [service.ts](../../newcodexJS/16-team-project-management/server/src/services/service.ts), [package.json](../../newcodexJS/16-team-project-management/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/17-support-ticket-system

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodexJS/17-support-ticket-system)

Support-ticket admin

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Shares a generic scoped CRUD/admin structure with 16-20; specialized title does not establish a complete domain engine.
- **Learn:** Generic ticket CRUD, priority/SLA metadata and audit
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Implement one real SLA deadline job and prove internal comments remain private.
- **Evidence:** [README.md](../../newcodexJS/17-support-ticket-system/README.md), [service.ts](../../newcodexJS/17-support-ticket-system/server/src/services/service.ts), [package.json](../../newcodexJS/17-support-ticket-system/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/18-learning-management-system

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodexJS/18-learning-management-system)

Learning-management admin

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Shares a generic scoped CRUD/admin structure with 16-20; specialized title does not establish a complete domain engine.
- **Learn:** Generic course catalog CRUD and publication lifecycle
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Implement one learner enrollment/progress behavior if choosing this domain.
- **Evidence:** [README.md](../../newcodexJS/18-learning-management-system/README.md), [service.ts](../../newcodexJS/18-learning-management-system/server/src/services/service.ts), [package.json](../../newcodexJS/18-learning-management-system/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/19-realtime-chat-platform

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodexJS/19-realtime-chat-platform)

Conversation administration

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Shares a generic scoped CRUD/admin structure with 16-20; specialized title does not establish a complete domain engine.
- **Learn:** Generic conversation CRUD, moderation metadata and audit; realtime transport not established
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Use the polling-chat app or netintercom for messaging, or add a tested transport to this scaffold.
- **Evidence:** [README.md](../../newcodexJS/19-realtime-chat-platform/README.md), [service.ts](../../newcodexJS/19-realtime-chat-platform/server/src/services/service.ts), [package.json](../../newcodexJS/19-realtime-chat-platform/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/20-marketplace-platform

**Stage 4: Integrated full-stack workflows. optional targeted exercise.** [Open app folder](../../newcodexJS/20-marketplace-platform)

Marketplace listing admin

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Shares a generic scoped CRUD/admin structure with 16-20; specialized title does not establish a complete domain engine.
- **Learn:** Generic vendor listing CRUD and moderation; payment/order marketplace engine not established
- **Before starting:** One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Next:** Implement vendor authorization and one meaningful listing moderation transition.
- **Evidence:** [README.md](../../newcodexJS/20-marketplace-platform/README.md), [service.ts](../../newcodexJS/20-marketplace-platform/server/src/services/service.ts), [package.json](../../newcodexJS/20-marketplace-platform/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/13-ecommerce-storefront

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodexJS/13-ecommerce-storefront)

Ecommerce storefront

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. README describes development/demo identity headers rather than completed authentication.
- **Learn:** Cart ownership, transactional checkout, reviews and admin flows
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Verify duplicate checkout/stock handling and replace demo identity before shared deployment.
- **Evidence:** [README.md](../../newcodexJS/13-ecommerce-storefront/README.md), [storeService.ts](../../newcodexJS/13-ecommerce-storefront/server/src/services/storeService.ts), [package.json](../../newcodexJS/13-ecommerce-storefront/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/14-appointment-booking

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodexJS/14-appointment-booking)

Appointment booking

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. README describes development/demo identity headers rather than completed authentication.
- **Learn:** Availability, timezone conversion and overlap detection
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Test last-slot concurrency and replace development identity/role headers.
- **Evidence:** [README.md](../../newcodexJS/14-appointment-booking/README.md), [serviceModel.ts](../../newcodexJS/14-appointment-booking/server/src/models/serviceModel.ts), [package.json](../../newcodexJS/14-appointment-booking/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### newcodexJS/15-api-tester

**Stage 5: Domain rules and reliability. optional targeted exercise.** [Open app folder](../../newcodexJS/15-api-tester)

REST API testing tool

- **Stack:** TypeScript; React; Vite; Express; Knex; PostgreSQL.
- **Review:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified.
- **Learn:** HTTP proxying, variable interpolation, request history and collections
- **Before starting:** A working full-stack app with authentication, authorization, relational data and tests.
- **Next:** Verify target restrictions, timeouts and response limits on the proxy endpoint.
- **Evidence:** [README.md](../../newcodexJS/15-api-tester/README.md), [collectionService.ts](../../newcodexJS/15-api-tester/server/src/services/collectionService.ts), [package.json](../../newcodexJS/15-api-tester/server/package.json).

- **Variant guidance:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.

### Coverage notes

**.nethris**

- **Status:** Empty project placeholder: only empty client directory.

**Amasterplan**

- **Status:** Empty directory.

**codexlearnp1**

- **Status:** Empty directory.


### Curriculum details

#### Csharptut

00-15 language/data/async; 16-21 I/O, HTTP, DI, EF Core, API and tests; 22 independent CRUD capstone; 23-24 study guidance.

#### Js1

Select from tiers rather than complete every clone: 11 vanilla apps; 9 React/Express apps; 8 TS/Postgres specialty apps; 10 richer JS apps; 10 TS/Postgres apps; 20 .NET/Postgres variants. Suggested selected progression: task-board, contact-book, focus-timer, issue-desk, secure-notes, invoice-studio, room-booking.


### Nested count

75

### Coverage notes

- newcodex3 contains 50 apps (16-40, TypeScript and .NET pairs), despite stale root five-app text.
- newcodexJS contains 20 apps despite stale 15-app opening line.
- newcodecjs2 contains five apps explicitly intended as architecture reading scaffolds.
- recipeweb/net contains planning documents only and is not counted as another implemented app.
- netsnapshot and netsnapshot1 snapshot copies are chronological learning material, not independently prioritized products.
- New folder is empty and excluded from project counts.

## Candidate copies and versions

These 56 groups come from the earlier multi-file sample comparison. They are retained as navigation and workload-reduction hints. This review does not authorize deletion or declare a canonical working copy. Compare the feature you need and its tests, then choose one directory for the assignment.

| Group | Locations with matching saved samples |
|---|---|
| 1 | [.netarchitectureproject](../../.netarchitectureproject); [geminiorganized/General_.Architectureproject](../../geminiorganized/General_.Architectureproject) |
| 2 | [.netopen2](../../.netopen2); [geminiorganized/General_.Open2](../../geminiorganized/General_.Open2) |
| 3 | [.netramp](../../.netramp); [geminiorganized/OpenSource_Upskilling_.Ramp](../../geminiorganized/OpenSource_Upskilling_.Ramp) |
| 4 | [.netstripe](../../.netstripe); [geminiorganized/OpenSource_Upskilling_.Stripe](../../geminiorganized/OpenSource_Upskilling_.Stripe) |
| 5 | [.nettodo](../../.nettodo); [geminiorganized/General_.Todo](../../geminiorganized/General_.Todo) |
| 6 | [aiapplybot](../../aiapplybot); [geminiorganized/LLM_Generated_Applybot](../../geminiorganized/LLM_Generated_Applybot) |
| 7 | [aihelper](../../aihelper); [geminiorganized/LLM_Generated_Helper](../../geminiorganized/LLM_Generated_Helper) |
| 8 | [AlanAndEliSoccer](../../AlanAndEliSoccer); [geminiorganized/General_Alanandelisoccer](../../geminiorganized/General_Alanandelisoccer) |
| 9 | [aral](../../aral); [geminiorganized/General_Aral](../../geminiorganized/General_Aral) |
| 10 | [borrowbox](../../borrowbox); [geminiorganized/General_Borrowbox](../../geminiorganized/General_Borrowbox) |
| 11 | [buildbusinesses](../../buildbusinesses); [geminiorganized/LLM_Generated_Buildbusinesses](../../geminiorganized/LLM_Generated_Buildbusinesses) |
| 12 | [buildermentor](../../buildermentor); [geminiorganized/LLM_Generated_Buildermentor](../../geminiorganized/LLM_Generated_Buildermentor) |
| 13 | [buildevent](../../buildevent); [geminiorganized/LLM_Generated_Buildevent](../../geminiorganized/LLM_Generated_Buildevent) |
| 14 | [buildreviewer](../../buildreviewer); [geminiorganized/LLM_Generated_Buildreviewer](../../geminiorganized/LLM_Generated_Buildreviewer) |
| 15 | [buildsmallplates](../../buildsmallplates); [geminiorganized/LLM_Generated_Buildsmallplates](../../geminiorganized/LLM_Generated_Buildsmallplates) |
| 16 | [buildwhiteboard](../../buildwhiteboard); [geminiorganized/LLM_Generated_Buildwhiteboard](../../geminiorganized/LLM_Generated_Buildwhiteboard) |
| 17 | [campusops](../../campusops); [geminiorganized/General_Campusops](../../geminiorganized/General_Campusops) |
| 18 | [csharptut](../../csharptut); [geminiorganized/General_Csharptut](../../geminiorganized/General_Csharptut) |
| 19 | [devdeck](../../devdeck); [geminiorganized/General_Devdeck](../../geminiorganized/General_Devdeck) |
| 20 | [fableaihelperv2](../../fableaihelperv2); [geminiorganized/LLM_Generated_Fablehelperv2](../../geminiorganized/LLM_Generated_Fablehelperv2) |
| 21 | [fableaihelperv3](../../fableaihelperv3); [geminiorganized/LLM_Generated_Fablehelperv3](../../geminiorganized/LLM_Generated_Fablehelperv3) |
| 22 | [finance-dashboard](../../finance-dashboard); [geminiorganized/General_Finance-Dashboard](../../geminiorganized/General_Finance-Dashboard) |
| 23 | [formforge](../../formforge); [geminiorganized/General_Formforge](../../geminiorganized/General_Formforge) |
| 24 | [geminiorganized/General_Cleanarch](../../geminiorganized/General_Cleanarch); [netcleanarch](../../netcleanarch) |
| 25 | [geminiorganized/General_Gitjira-App](../../geminiorganized/General_Gitjira-App); [gitjira-app](../../gitjira-app) |
| 26 | [geminiorganized/General_Globehire](../../geminiorganized/General_Globehire); [globehire](../../globehire) |
| 27 | [geminiorganized/General_Masternocu](../../geminiorganized/General_Masternocu); [masternocu](../../masternocu) |
| 28 | [geminiorganized/General_Masteroutline](../../geminiorganized/General_Masteroutline); [masteroutline](../../masteroutline) |
| 29 | [geminiorganized/General_Meterforge](../../geminiorganized/General_Meterforge); [meterforge](../../meterforge) |
| 30 | [geminiorganized/General_Missioncontrol](../../geminiorganized/General_Missioncontrol); [missioncontrol](../../missioncontrol) |
| 31 | [geminiorganized/General_Mobiletagalog](../../geminiorganized/General_Mobiletagalog); [mobiletagalog](../../mobiletagalog) |
| 32 | [geminiorganized/General_Newcodecjs2](../../geminiorganized/General_Newcodecjs2); [newcodecjs2](../../newcodecjs2) |
| 33 | [geminiorganized/General_Newcodex3](../../geminiorganized/General_Newcodex3); [newcodex3](../../newcodex3) |
| 34 | [geminiorganized/General_Newcodexjs](../../geminiorganized/General_Newcodexjs); [newcodexJS](../../newcodexJS) |
| 35 | [geminiorganized/General_Nopsolutions](../../geminiorganized/General_Nopsolutions); [nopsolutionsnet](../../nopsolutionsnet) |
| 36 | [geminiorganized/General_Open3](../../geminiorganized/General_Open3); [netopen3](../../netopen3) |
| 37 | [geminiorganized/General_Open5](../../geminiorganized/General_Open5); [netopen5](../../netopen5) |
| 38 | [geminiorganized/General_Perch](../../geminiorganized/General_Perch); [perch](../../perch) |
| 39 | [geminiorganized/General_Recipeview](../../geminiorganized/General_Recipeview); [recipeview](../../recipeview) |
| 40 | [geminiorganized/General_Recipeweb](../../geminiorganized/General_Recipeweb); [recipeweb](../../recipeweb) |
| 41 | [geminiorganized/General_Skillforgejs](../../geminiorganized/General_Skillforgejs); [skillforgejs](../../skillforgejs) |
| 42 | [geminiorganized/General_Spacegame](../../geminiorganized/General_Spacegame); [spacegame](../../spacegame) |
| 43 | [geminiorganized/LLM_Generated_Ecommerceproject](../../geminiorganized/LLM_Generated_Ecommerceproject); [grokbuildecommerceproject](../../grokbuildecommerceproject) |
| 44 | [geminiorganized/LLM_Generated_Grokjs](../../geminiorganized/LLM_Generated_Grokjs); [grokjs](../../grokjs) |
| 45 | [geminiorganized/LLM_Generated_Groktuts](../../geminiorganized/LLM_Generated_Groktuts); [groktuts](../../groktuts) |
| 46 | [geminiorganized/LLM_Generated_Js1](../../geminiorganized/LLM_Generated_Js1); [JS1](../../JS1) |
| 47 | [geminiorganized/LLM_Generated_Rag](../../geminiorganized/LLM_Generated_Rag); [netairag](../../netairag) |
| 48 | [geminiorganized/OpenSource_Upskilling_Auth](../../geminiorganized/OpenSource_Upskilling_Auth); [netauth](../../netauth) |
| 49 | [geminiorganized/OpenSource_Upskilling_Docu](../../geminiorganized/OpenSource_Upskilling_Docu); [netdocu](../../netdocu) |
| 50 | [geminiorganized/OpenSource_Upskilling_Drop](../../geminiorganized/OpenSource_Upskilling_Drop); [netdrop](../../netdrop) |
| 51 | [geminiorganized/OpenSource_Upskilling_Intercom](../../geminiorganized/OpenSource_Upskilling_Intercom); [netintercom](../../netintercom) |
| 52 | [geminiorganized/OpenSource_Upskilling_Linear](../../geminiorganized/OpenSource_Upskilling_Linear); [netlinear](../../netlinear) |
| 53 | [geminiorganized/OpenSource_Upskilling_Notion](../../geminiorganized/OpenSource_Upskilling_Notion); [netnotion](../../netnotion) |
| 54 | [geminiorganized/OpenSource_Upskilling_Shop](../../geminiorganized/OpenSource_Upskilling_Shop); [netshop](../../netshop) |
| 55 | [geminiorganized/OpenSource_Upskilling_Snapshot](../../geminiorganized/OpenSource_Upskilling_Snapshot); [netsnapshot](../../netsnapshot) |
| 56 | [geminiorganized/OpenSource_Upskilling_Snapshot1](../../geminiorganized/OpenSource_Upskilling_Snapshot1); [netsnapshot1](../../netsnapshot1) |

## Non-project folders and boundaries

`AstraOrganized`, `AstraOrganized2`, and `project-inventory` contain inventory/report artifacts; they are navigation references, not additional application assignments. Empty or container-only folders are tracked in the supplemental coverage notes above. `geminiorganized/General_.Hris` contains only an empty client folder, and `geminiorganized/General_Amasterplan` is empty in the current check. Shortcuts, OS metadata, dependencies, build outputs, agent state, secrets, and unrelated loose personal documents are outside the software-project learning catalog.

Project components such as an API, frontend, shared package, test project, or historical snapshot remain within their parent workspace. Independently versioned repositories under a container retain their own records. This report adds documentation only; source folders retain their locations.
