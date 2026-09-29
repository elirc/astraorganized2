# Section 3: Full-stack workflows and a capstone

[Plan index](README.md)

Select one primary app with a useful domain. Own a complete workflow across interface, server and data, including permissions. Similar projects are alternatives.

**Stage exit criterion:** Reproduce setup from a clean checkout, demonstrate an authorized workflow and a denied action, and explain the code and data changes independently.

**Coverage:** 66 project/workspace/resource records and 18 nested teaching apps. Entries are grouped by original milestone and alphabetized within it; alphabetical position is not a mandatory execution order. Use the short route in the index.

All actions below are proposals based on the September 6–7 static reviews. Reproduce the baseline before claiming a defect or improvement. Existing tests and docs may already cover a proposed case; assess and strengthen them rather than duplicate them.

## Entries

- [.netramp](#p003)
- [.nettodo](#p005)
- [_Organized Desktop/01 Net Workspaces/.nethris](#p008)
- [_Organized Desktop/01 Net Workspaces/.nettrello](#p011)
- [_Organized Desktop/01 Net Workspaces/.netzen](#p013)
- [_Organized Desktop/02 Build Projects/buildasana](#p021)
- [_Organized Desktop/02 Build Projects/buildCRMPYJS](#p022)
- [_Organized Desktop/02 Build Projects/buildjira](#p025)
- [_Organized Desktop/04 JavaScript Training/jsdrillapp](#p070)
- [_Organized Desktop/04 JavaScript Training/jstrain1](#p071)
- [_Organized Desktop/04 JavaScript Training/jstrain5](#p078)
- [_Organized Desktop/04 JavaScript Training/rewritepy2js](#p081)
- [_Organized Desktop/05 Numbered Experiments/D1](#p084)
- [_Organized Desktop/05 Numbered Experiments/D3](#p086)
- [_Organized Desktop/05 Numbered Experiments/e11](#p088)
- [_Organized Desktop/05 Numbered Experiments/e15](#p092)
- [_Organized Desktop/05 Numbered Experiments/e17](#p093)
- [_Organized Desktop/05 Numbered Experiments/e2](#p094)
- [_Organized Desktop/05 Numbered Experiments/e4](#p097)
- [_Organized Desktop/05 Numbered Experiments/e6](#p098)
- [_Organized Desktop/05 Numbered Experiments/ww12](#p115)
- [_Organized Desktop/05 Numbered Experiments/ww16](#p119)
- [_Organized Desktop/05 Numbered Experiments/ww17](#p120)
- [_Organized Desktop/05 Numbered Experiments/ww30](#p128)
- [_Organized Desktop/05 Numbered Experiments/ww4](#p136)
- [_Organized Desktop/05 Numbered Experiments/ww40](#p137)
- [_Organized Desktop/05 Numbered Experiments/ww43](#p138)
- [_Organized Desktop/05 Numbered Experiments/ww45](#p139)
- [_Organized Desktop/05 Numbered Experiments/ww46](#p140)
- [_Organized Desktop/05 Numbered Experiments/ww48](#p142)
- [_Organized Desktop/05 Numbered Experiments/ww50](#p145)
- [_Organized Desktop/05 Numbered Experiments/ww55](#p146)
- [_Organized Desktop/05 Numbered Experiments/z3](#p153)
- [_Organized Desktop/05 Numbered Experiments/z6](#p154)
- [_Organized Desktop/05 Numbered Experiments/z7](#p155)
- [_Organized Desktop/05 Numbered Experiments/z8](#p156)
- [_Organized Desktop/05 Numbered Experiments/zz2](#p159)
- [_Organized Desktop/05 Numbered Experiments/zz3](#p160)
- [_Organized Desktop/05 Numbered Experiments/zz6](#p163)
- [_Organized Desktop/05 Numbered Experiments/zz9](#p166)
- [_Organized Desktop/06 AI And Learning/claudeailab](#p171)
- [_Organized Desktop/07 Anti Projects/antihelpdesk](#p177)
- [_Organized Desktop/08 App And Product Projects/appmakertrack](#p180)
- [_Organized Desktop/08 App And Product Projects/grouphelpdesk](#p183)
- [_Organized Desktop/08 App And Product Projects/HNJOBTRACK](#p184)
- [_Organized Desktop/08 App And Product Projects/job track](#p186)
- [_Organized Desktop/12 Other Projects/aaa1](#p195)
- [_Organized Desktop/12 Other Projects/cc](#p198)
- [_Organized Desktop/12 Other Projects/jdtrrain2.1](#p204)
- [geminiorganized/General_.Todo](#p243)
- [geminiorganized/General_Gitjira-App](#p256)
- [geminiorganized/LLM_Generated_Ecommerceproject](#p291)
- [geminiorganized/LLM_Generated_Hrproject](#p298)
- [geminiorganized/LLM_Generated_Ppmproject](#p303)
- [geminiorganized/LLM_Generated_Supportproject](#p305)
- [geminiorganized/LLM_Generated_Teamproject](#p306)
- [geminiorganized/OpenSource_Upskilling_.Ramp](#p307)
- [geminiorganized/OpenSource_Upskilling_Linear](#p313)
- [gitjira-app](#p319)
- [gitvg/storefront](#p335)
- [grokbuildecommerceproject](#p340)
- [grokbuildhrproject](#p341)
- [grokbuildppmproject](#p344)
- [grokbuildsupportproject](#p345)
- [grokbuildteamproject](#p346)
- [netlinear](#p369)
- [newcodex3/apps/16-blog-platform](#p390)
- [newcodex3/apps/16-blog-platform-net](#p391)
- [newcodex3/apps/31-multi-tenant-crm](#p420)
- [newcodex3/apps/31-multi-tenant-crm-net](#p421)
- [newcodex3/apps/38-admin-settings-permissions-console](#p434)
- [newcodex3/apps/38-admin-settings-permissions-console-net](#p435)
- [newcodexJS/05-recipe-manager](#p444)
- [newcodexJS/07-blog-platform](#p446)
- [newcodexJS/08-kanban-board](#p447)
- [newcodexJS/09-job-application-tracker](#p448)
- [newcodexJS/10-inventory-management](#p449)
- [newcodexJS/11-survey-builder](#p450)
- [newcodexJS/12-chat-polling](#p451)
- [newcodexJS/16-team-project-management](#p455)
- [newcodexJS/17-support-ticket-system](#p456)
- [newcodexJS/18-learning-management-system](#p457)
- [newcodexJS/19-realtime-chat-platform](#p458)
- [newcodexJS/20-marketplace-platform](#p459)

## Per-project improvement plans

<a id="p003"></a>
### .netramp

A learning-oriented clone of Ramp / Expensify / Brex expense workflows, built with ASP.NET Core (C#) and React.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Teaching application with in-memory storage and no cataloged tests; README says source was not compiled in its generation environment. Static review only; not built, tested or run.
- **Recorded stack:** C#, CSS, HTML, JavaScript, ASP.NET Core, React, Vite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/.netramp/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, upload/finalization state and storage boundaries, an expected-state example and a guided-to-independent change exercise. Tie it to Role-scoped expense workflows, state machines, uploads.
- **2 — Improve the project/resource:** First scoped project change: Persist one expense workflow and test approval transitions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Try an unauthorized or expired operation and an interrupted retry; verify no orphaned committed state or double quota charge.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/OpenSource_Upskilling_.Ramp](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_.Ramp). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/.netramp/README.md), [App.jsx](C:/Users/Owner/Desktop/.netramp/frontend/src/App.jsx), [package.json](C:/Users/Owner/Desktop/.netramp/frontend/package.json).

---

<a id="p005"></a>
### .nettodo

ASP.NET Core eShopOnWeb reference storefront demonstrating a monolithic web application.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** eShopOnWeb upstream reference, not a todo app; README identifies successor repositories. Static review only; not built, tested or run.
- **Recorded stack:** C#, CSS, JavaScript, Razor, SCSS, ASP.NET Core, Blazor, Entity Framework Core, SQL Server, Docker, GitHub Actions, MSTest, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/.nettodo/eShopOnWeb/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of stock ownership, checkout and order transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Layered ASP.NET application, EF Core, identity, storefronts.
- **2 — Improve the project/resource:** First scoped project change: Trace basket-to-order flow, then make one small tested change. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_.Todo](C:/Users/Owner/Desktop/geminiorganized/General_.Todo). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/.nettodo/eShopOnWeb/README.md), [Program.cs](C:/Users/Owner/Desktop/.nettodo/eShopOnWeb/src/Web/Program.cs), [docker-compose.yml](C:/Users/Owner/Desktop/.nettodo/eShopOnWeb/docker-compose.yml).

---

<a id="p008"></a>
### _Organized Desktop/01 Net Workspaces/.nethris

A compact HRIS / employee directory platform inspired by BambooHR and Rippling.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, SQLite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.nethris/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of employee lifecycle, approval and tenant scope, an expected-state example and a guided-to-independent change exercise. Tie it to tenant isolation, approval rules, audit history, module boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace one employee approval and test both cross-tenant access and invalid state changes. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.nethris/README.md), [Program.cs](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.nethris/server/Nethris.Api/Program.cs), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.nethris/client/src/App.tsx).

---

<a id="p011"></a>
### _Organized Desktop/01 Net Workspaces/.nettrello

NetTrello is a Trello-style kanban starter built with C#, ASP.NET Core, React, and TypeScript.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: README explicitly describes seeded in-memory persistence. Adding durable storage is a learning exercise.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Docker.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.nettrello/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, ordering and lifecycle transitions, an expected-state example and a guided-to-independent change exercise. Tie it to relational CRUD, ordering, optimistic UI, project permissions.
- **2 — Improve the project/resource:** First scoped project change: Implement one board/task operation and test ordering plus permission boundaries. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.nettrello/README.md), [Program.cs](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.nettrello/src/NetTrello.Api/Program.cs), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.nettrello/client/src/App.tsx).

---

<a id="p013"></a>
### _Organized Desktop/01 Net Workspaces/.netzen

A learning-oriented Zendesk/Intercom-style inbox built with C#, ASP.NET Core, SignalR, and React.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netzen/support-ticketing-app/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netzen/support-ticketing-app/README.md), [Program.cs](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netzen/support-ticketing-app/backend/SupportDesk.Api/Program.cs), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netzen/support-ticketing-app/frontend/src/App.tsx).

---

<a id="p021"></a>
### _Organized Desktop/02 Build Projects/buildasana

BuildAsana is an Asana-inspired work management system built for learning production-quality C#, .NET, and React patterns.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Recorded stack:** C#, CSS, HTML, JavaScript, TypeScript, ASP.NET Core, React, Vite, xUnit.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildasana/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, ordering and lifecycle transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting relational CRUD, ordering, optimistic UI, project permissions.
- **2 — Improve the project/resource:** First scoped project change: Implement one board/task operation and test ordering plus permission boundaries. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildasana/README.md), [Program.cs](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildasana/backend/src/BuildAsana.Api/Program.cs), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildasana/frontend/src/App.tsx).

---

<a id="p022"></a>
### _Organized Desktop/02 Build Projects/buildCRMPYJS

Full-stack internal CRM and sales-pipeline application.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Vite, Prisma, Redis, Docker, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildCRMPYJS/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, ordering and lifecycle transitions, an expected-state example and a guided-to-independent change exercise. Tie it to relational data, lifecycle transitions, tenant-scoped queries, audit history. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace a lead/deal transition and test tenant isolation plus invalid transitions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildCRMPYJS/README.md), [auth.routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildCRMPYJS/backend/src/modules/auth/auth.routes.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildCRMPYJS/frontend/src/App.tsx).

---

<a id="p025"></a>
### _Organized Desktop/02 Build Projects/buildjira

C#/React issue tracker; JavaScript predecessor is archived and current authentication uses demo actor impersonation.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: README states x-user-id impersonation/default seeded actor is a local-development identity model, not production authentication.
- **Recorded stack:** C#, CSS, HTML, JavaScript, TypeScript, ASP.NET Core, Docker.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildjira/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Separate the archived JavaScript predecessor from the current C#/React flow and explain demo actor impersonation.
- **2 — Improve the project/resource:** Complete one issue transition and replace demo actor selection with a verified session when adding shared-user operation.
- **3 — Prove completion:** A nonmember cannot mutate the issue; the valid transition updates the interface and stored issue consistently.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildjira/README.md), [health.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildjira/apps/api/src/routes/health.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildjira/apps/web/src/App.tsx).

---

<a id="p070"></a>
### _Organized Desktop/04 JavaScript Training/jsdrillapp

Reps coding-practice app for building programming fluency through repeated exercises.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Drizzle, SQLite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [01-schema.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jsdrillapp/reps/training-docs/01-schema.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jsdrillapp/reps/README.md), [fsrs.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jsdrillapp/reps/src/lib/fsrs.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jsdrillapp/reps/package.json).

---

<a id="p071"></a>
### _Organized Desktop/04 JavaScript Training/jstrain1

Full-stack JavaScript practice application for tenant-scoped administrative operations.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Express, Node.js, React, Vite, Prisma.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain1/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting sessions, tenant isolation, schemas, validation, authorization.
- **2 — Improve the project/resource:** First scoped project change: Trace one protected mutation and design cross-tenant read/write denial tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain1/README.md), [authRoutes.js](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain1/server/src/routes/authRoutes.js), [App.jsx](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain1/web/src/App.jsx).

---

<a id="p078"></a>
### _Organized Desktop/04 JavaScript Training/jstrain5

OpsForge is an internal operations dashboard for NovaCom (fictional telecom/SaaS company).

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Drizzle, PostgreSQL, Redis, Docker, BullMQ.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain5/fable-docs/README.md).
- **1 — Improve the upskilling content:** Connect the nine-chapter OpsForge Fable course to a concrete runbook trace and reconcile older per-file learning notes.
- **2 — Improve the project/resource:** Improve one runbook execution transition and make a failed step visible and recoverable.
- **3 — Prove completion:** A failed runbook step records its outcome; a retry follows the documented state transition without repeating completed side effects.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain5/README.md), [service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain5/src/lib/runbooks/service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain5/package.json).

---

<a id="p081"></a>
### _Organized Desktop/04 JavaScript Training/rewritepy2js

FastAPI codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the RealWorld spec and API.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** Python, SQL, TypeScript, Express, FastAPI, Node.js, PostgreSQL, Prisma, SQLAlchemy, Docker, Jest, pytest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/rewritepy2js/fastapi-realworld-example-app/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/rewritepy2js/fastapi-realworld-example-app/README.md), [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/rewritepy2js/fastapi-realworld-example-app/src/routes/auth.ts), [main.py](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/rewritepy2js/fastapi-realworld-example-app/app/main.py).

---

<a id="p084"></a>
### _Organized Desktop/05 Numbered Experiments/D1

Real-time kanban project-board application.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Drizzle, PostgreSQL, Redis, Socket.IO.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D1/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, ordering and lifecycle transitions, an expected-state example and a guided-to-independent change exercise. Tie it to relational CRUD, ordering, optimistic UI, project permissions.
- **2 — Improve the project/resource:** First scoped project change: Implement one board/task operation and test ordering plus permission boundaries. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D1/src/lib/services/auth.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D1/package.json), [server.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D1/server.ts).

---

<a id="p086"></a>
### _Organized Desktop/05 Numbered Experiments/D3

Scaffold with Next.js 14, TypeScript, Auth.js v5, PostgreSQL, Drizzle, Stripe, Resend, Zod, and Tailwind.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Drizzle, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D3/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D3/README.md), [audit.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D3/lib/services/audit.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D3/package.json).

---

<a id="p088"></a>
### _Organized Desktop/05 Numbered Experiments/e11

Roughflow visual board/editor application.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Vite, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e11/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e11/src/App.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e11/package.json).

---

<a id="p092"></a>
### _Organized Desktop/05 Numbered Experiments/e15

A pragmatic MVP for a multi-team support desk.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, FastAPI, SQLAlchemy, pytest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e15/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ticket visibility, assignment and service deadlines, an expected-state example and a guided-to-independent change exercise. Tie it to route/service/repository boundaries, permissions, queue filters, workflow rules.
- **2 — Improve the project/resource:** First scoped project change: Trace ticket creation to storage; test forbidden transitions and unauthorized access. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e15/README.md), [services.py](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e15/app/services.py), [main.py](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e15/app/main.py).

---

<a id="p093"></a>
### _Organized Desktop/05 Numbered Experiments/e17

Forum application with moderation, trust levels, and discussion threads.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, SQLite, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e17/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e17/README.md), [db.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e17/src/lib/db.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e17/package.json).

---

<a id="p094"></a>
### _Organized Desktop/05 Numbered Experiments/e2

Northstar CMS is a learning-oriented, Strapi-style headless CMS scaffold built with Next.js and TypeScript.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Teaching app with documented in-memory/mock persistence; database/schema claims do not establish durable storage. Runtime unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e2/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of tree structure, revisions and inherited permissions, an expected-state example and a guided-to-independent change exercise. Tie it to content modeling, revisions, authorization, search, optimistic concurrency.
- **2 — Improve the project/resource:** First scoped project change: Trace an edit and test a stale revision or forbidden share. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e2/README.md), [page.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e2/src/app/page.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e2/package.json).

---

<a id="p097"></a>
### _Organized Desktop/05 Numbered Experiments/e4

Northstar Publish is a production-oriented publication platform built with Next.js, React, TypeScript, Prisma, PostgreSQL, Stripe, and BullMQ.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Redis, AWS SDK, Playwright, Vitest, BullMQ, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e4/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of tree structure, revisions and inherited permissions, an expected-state example and a guided-to-independent change exercise. Tie it to content modeling, revisions, authorization, search, optimistic concurrency.
- **2 — Improve the project/resource:** First scoped project change: Trace an edit and test a stale revision or forbidden share. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e4/README.md), [service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e4/src/server/auth/service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e4/package.json).

---

<a id="p098"></a>
### _Organized Desktop/05 Numbered Experiments/e6

Multi-tenant team-workspace scaffold for full-stack practice.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Recorded stack:** CSS, TypeScript, Fastify, Next.js, Node.js, React, Prisma, Socket.IO.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e6/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to sessions, tenant isolation, schemas, validation, authorization.
- **2 — Improve the project/resource:** First scoped project change: Trace one protected mutation and design cross-tenant read/write denial tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e6/README.md), [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e6/apps/api/src/routes/auth.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e6/package.json).

---

<a id="p115"></a>
### _Organized Desktop/05 Numbered Experiments/ww12

Omnichannel customer communications platform built with Next.js, TypeScript, PostgreSQL, Prisma, Tailwind, Zod, React Query, and REST APIs.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Docker, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww12/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww12/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww12/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww12/package.json).

---

<a id="p119"></a>
### _Organized Desktop/05 Numbered Experiments/ww16

Channel Compass partner-relationship management scaffold with separated routes, validation, and business logic.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww16/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, ordering and lifecycle transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting relational data, lifecycle transitions, tenant-scoped queries, audit history.
- **2 — Improve the project/resource:** First scoped project change: Trace a lead/deal transition and test tenant isolation plus invalid transitions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww16/docs/architecture/README.md), [mdfService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww16/src/services/mdfService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww16/package.json).

---

<a id="p120"></a>
### _Organized Desktop/05 Numbered Experiments/ww17

SignalDesk is a learning-oriented customer success and health scoring platform built with Next.js, TypeScript, React Query, Zod, and Prisma-style repository boundaries.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww17/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, ordering and lifecycle transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting relational data, lifecycle transitions, tenant-scoped queries, audit history.
- **2 — Improve the project/resource:** First scoped project change: Trace a lead/deal transition and test tenant isolation plus invalid transitions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww17/README.md), [account-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww17/src/services/account-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww17/package.json).

---

<a id="p128"></a>
### _Organized Desktop/05 Numbered Experiments/ww30

QueryForge Workbench is a backend-first Next.js app for building safe dynamic queries over a constrained orders dataset.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww30/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww30/docs/architecture/README.md), [datasetService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww30/src/services/datasetService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww30/package.json).

---

<a id="p136"></a>
### _Organized Desktop/05 Numbered Experiments/ww4

WorkGrid is a Jira-like work management platform built to teach backend-oriented product engineering.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww4/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, ordering and lifecycle transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting relational CRUD, ordering, optimistic UI, project permissions.
- **2 — Improve the project/resource:** First scoped project change: Implement one board/task operation and test ordering plus permission boundaries. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww4/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww4/src/services/auth/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww4/package.json).

---

<a id="p137"></a>
### _Organized Desktop/05 Numbered Experiments/ww40

Single-platform job board admin dashboard built for backend-oriented CRUD learning.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww40/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting CRUD, filtering, authentication, validation, status transitions.
- **2 — Improve the project/resource:** First scoped project change: Trace a create/update flow and test ownership, validation, and one invalid transition. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww40/docs/architecture/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww40/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww40/package.json).

---

<a id="p138"></a>
### _Organized Desktop/05 Numbered Experiments/ww43

Notes application with version history, sharing, and conflict-aware saves.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww43/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of tree structure, revisions and inherited permissions: ordered source files, one input-to-state trace, a diagram and one independent change targeting content modeling, revisions, authorization, search, optimistic concurrency.
- **2 — Improve the project/resource:** First scoped project change: Trace an edit and test a stale revision or forbidden share. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww43/README.md), [auth-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww43/src/services/auth-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww43/package.json).

---

<a id="p139"></a>
### _Organized Desktop/05 Numbered Experiments/ww45

Internal knowledge base built with Next.js, TypeScript, Prisma, PostgreSQL, Zod, Tailwind, and React Query.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww45/docs2/mission-learning-path/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for tree structure, revisions and inherited permissions; make learners predict state before running it. Teach content modeling, revisions, authorization, search, optimistic concurrency with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace an edit and test a stale revision or forbidden share. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww45/README.md), [tagService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww45/src/services/tagService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww45/package.json).

---

<a id="p140"></a>
### _Organized Desktop/05 Numbered Experiments/ww46

Multi-tenant SaaS starter built with Next.js, TypeScript, Prisma, Tailwind, Zod, React Query, and REST APIs.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww46/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting sessions, tenant isolation, schemas, validation, authorization.
- **2 — Improve the project/resource:** First scoped project change: Trace one protected mutation and design cross-tenant read/write denial tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww46/README.md), [auth-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww46/src/services/auth-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww46/package.json).

---

<a id="p142"></a>
### _Organized Desktop/05 Numbered Experiments/ww48

CRM lead pipeline built with Next.js, TypeScript, PostgreSQL, Prisma, Zod, Tailwind, React Query, and REST APIs.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Docker, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww48/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, ordering and lifecycle transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting relational data, lifecycle transitions, tenant-scoped queries, audit history.
- **2 — Improve the project/resource:** First scoped project change: Trace a lead/deal transition and test tenant isolation plus invalid transitions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww48/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww48/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww48/package.json).

---

<a id="p145"></a>
### _Organized Desktop/05 Numbered Experiments/ww50

API key management portal built around explicit tenant boundaries, service-layer business rules, and auditability.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [codebase-improvements-and-major-issues.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww50/docs/codebase-improvements-and-major-issues.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww50/docs/architecture/README.md), [apiKeyService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww50/src/services/apiKeyService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww50/package.json).

---

<a id="p146"></a>
### _Organized Desktop/05 Numbered Experiments/ww55

Next.js admin dashboard for reviewing job postings, resolving moderation cases, and storing private saved searches.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww55/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting CRUD, filtering, authentication, validation, status transitions.
- **2 — Improve the project/resource:** First scoped project change: Trace a create/update flow and test ownership, validation, and one invalid transition. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww55/docs/architecture/README.md), [serviceDeps.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww55/src/services/serviceDeps.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww55/package.json).

---

<a id="p153"></a>
### _Organized Desktop/05 Numbered Experiments/z3

Two practice apps: a founder CRM and a customer-feedback board.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, TypeScript, Next.js, Node.js, React.
- **Learning content now:** Codebase walkthrough / study pack. Start at [CODEBASE-STUDY-PATH.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z3/CODEBASE-STUDY-PATH.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, ordering and lifecycle transitions, an expected-state example and a guided-to-independent change exercise. Tie it to relational data, lifecycle transitions, tenant-scoped queries, audit history. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace a lead/deal transition and test tenant isolation plus invalid transitions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z3/README.md), [service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z3/founder-crm-lite/src/modules/crm/service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z3/customer-feedback-board/package.json).

---

<a id="p154"></a>
### _Organized Desktop/05 Numbered Experiments/z6

Northstar Atlas is a internal team wiki / knowledge base built to be both usable software and a studyable codebase.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, SQL, TypeScript, Next.js, Node.js, React, Prisma, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [how-to-study-this-codebase.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z6/docs/learning/how-to-study-this-codebase.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of tree structure, revisions and inherited permissions, an expected-state example and a guided-to-independent change exercise. Tie it to content modeling, revisions, authorization, search, optimistic concurrency.
- **2 — Improve the project/resource:** First scoped project change: Trace an edit and test a stale revision or forbidden share. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z6/README.md), [service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z6/src/modules/knowledge-base/service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z6/package.json).

---

<a id="p155"></a>
### _Organized Desktop/05 Numbered Experiments/z7

Hiring-pipeline tracker.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z7/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to CRUD, filtering, authentication, validation, status transitions.
- **2 — Improve the project/resource:** First scoped project change: Trace a create/update flow and test ownership, validation, and one invalid transition. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z7/README.md), [hiring-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z7/src/features/shared/server/hiring-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z7/package.json).

---

<a id="p156"></a>
### _Organized Desktop/05 Numbered Experiments/z8

Event-operations dashboard.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Docker.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z8/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z8/README.md), [auth.service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z8/src/modules/auth/auth.service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z8/package.json).

---

<a id="p159"></a>
### _Organized Desktop/05 Numbered Experiments/zz2

A customer support ticketing system built to practice backend-heavy product engineering with Next.js, TypeScript, PostgreSQL, Prisma, Zod, React Query, and REST APIs.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Docker, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [how-to-study-this-codebase.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz2/docs/learning/how-to-study-this-codebase.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ticket visibility, assignment and service deadlines, an expected-state example and a guided-to-independent change exercise. Tie it to route/service/repository boundaries, permissions, queue filters, workflow rules.
- **2 — Improve the project/resource:** First scoped project change: Trace ticket creation to storage; test forbidden transitions and unauthorized access. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz2/README.md), [app-services.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz2/src/server/app-services.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz2/package.json).

---

<a id="p160"></a>
### _Organized Desktop/05 Numbered Experiments/zz3

Support Hub is a customer support ticketing and queue management application for a single company.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, PostgreSQL, Prisma, Docker, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz3/docs/learning/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ticket visibility, assignment and service deadlines: ordered source files, one input-to-state trace, a diagram and one independent change targeting route/service/repository boundaries, permissions, queue filters, workflow rules.
- **2 — Improve the project/resource:** First scoped project change: Trace ticket creation to storage; test forbidden transitions and unauthorized access. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz3/README.md), [sla-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz3/src/services/sla-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz3/package.json).

---

<a id="p163"></a>
### _Organized Desktop/05 Numbered Experiments/zz6

Policy-management and acknowledgment portal with exceptions and reporting.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz6/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of event identity, aggregation and reporting filters: ordered source files, one input-to-state trace, a diagram and one independent change targeting code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz6/README.md), [policy-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz6/src/services/policy-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz6/package.json).

---

<a id="p166"></a>
### _Organized Desktop/05 Numbered Experiments/zz9

Internal case-management application with team queues and audit trails.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz9/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting case lifecycles, permissions, queues, audit trails.
- **2 — Improve the project/resource:** First scoped project change: Trace case assignment and test unauthorized queue access. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz9/docs/architecture/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz9/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz9/package.json).

---

<a id="p171"></a>
### _Organized Desktop/06 AI And Learning/claudeailab

A personal experiment tracker and skill progression system for evaluating AI-assisted coding tools, workflows, and techniques.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Drizzle, SQLite.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting experiment data modeling, CRUD, progress tracking, evaluation criteria.
- **2 — Improve the project/resource:** First scoped project change: Define one measurable experiment and trace how its result is stored and summarized. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab/README.md), [seed.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab/src/db/seed.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab/package.json).

---

<a id="p177"></a>
### _Organized Desktop/07 Anti Projects/antihelpdesk

Enterprise SaaS helpdesk system for learning purposes.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antihelpdesk/docsclaude/02-frontend-deep-dive/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ticket visibility, assignment and service deadlines: ordered source files, one input-to-state trace, a diagram and one independent change targeting ticket CRUD, role rules, service boundaries, UI/server contracts.
- **2 — Improve the project/resource:** First scoped project change: Trace one ticket transition and test both validation and authorization. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antihelpdesk/README.md), [auth.routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antihelpdesk/backend/src/modules/auth/auth.routes.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antihelpdesk/frontend/src/App.tsx).

---

<a id="p180"></a>
### _Organized Desktop/08 App And Product Projects/appmakertrack

A single-user project management application with kanban boards, project-scoped team members, and time tracking.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/appmakertrack/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of ownership, ordering and lifecycle transitions, known stubs and one exercise targeting project/task modeling, kanban ordering, time tracking. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace a task move or time-entry save and test invalid project scope. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/appmakertrack/README.md), [page.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/appmakertrack/app/page.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/appmakertrack/package.json).

---

<a id="p183"></a>
### _Organized Desktop/08 App And Product Projects/grouphelpdesk

HelpDesk is a learning-focused full-stack internal support ticket system.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, GitHub Actions, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [git-workflow.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/grouphelpdesk/docs/guides/git-workflow.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ticket visibility, assignment and service deadlines, an expected-state example and a guided-to-independent change exercise. Tie it to React/Express TypeScript contracts, SQLite/Prisma, workflow validation, RBAC, Vitest/Supertest, logging.
- **2 — Improve the project/resource:** First scoped project change: Trace ticket creation and assignment through shared contracts; add an unauthorized transition test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/grouphelpdesk/README.md), [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/grouphelpdesk/packages/server/src/routes/auth.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/grouphelpdesk/packages/client/src/App.tsx).

---

<a id="p184"></a>
### _Organized Desktop/08 App And Product Projects/HNJOBTRACK

A full-stack job browser for Hacker News "Who's Hiring" threads.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, Python, SQL, TypeScript, FastAPI, Next.js, Node.js, React, Tailwind CSS, Supabase, OpenAI API.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting API ingestion, search/filtering, parsing, UI server-state.
- **2 — Improve the project/resource:** First scoped project change: Trace one imported posting and test malformed or repeated source records. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK/README.md), [main.py](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK/backend/app/main.py), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK/frontend/package.json).

---

<a id="p186"></a>
### _Organized Desktop/08 App And Product Projects/job track

Full-stack JavaScript app for tracking job applications with auth, protected routes, validation, CRUD, filtering/sorting, workflow transitions, and dashboard stats.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Vite, SQLite, Socket.IO.
- **Learning content now:** Developer explanation / brief orientation. Start at [ARCHITECTURE_DEEP_DIVE.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/job%20track/ARCHITECTURE_DEEP_DIVE.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting React/Express JavaScript, SQLite, JWT auth, validation, CRUD, workflow transitions.
- **2 — Improve the project/resource:** First scoped project change: Trace application creation then test ownership and an invalid status transition. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/job%20track/README.md), [App.jsx](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/job%20track/client/src/App.jsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/job%20track/package.json).

---

<a id="p195"></a>
### _Organized Desktop/12 Other Projects/aaa1

This is a multi-tenant CRM built with Next.js App Router, TypeScript, Prisma, PostgreSQL, Tailwind, Zod, React Query, and REST APIs.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/aaa1/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, ordering and lifecycle transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting tenant-aware CRM schemas, services, Zod validation, REST contracts.
- **2 — Improve the project/resource:** First scoped project change: Trace lead/deal mutation and test cross-tenant data access. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/aaa1/docs/architecture/README.md), [opsService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/aaa1/src/services/opsService.ts), [noteService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/aaa1/src/services/noteService.ts).

---

<a id="p198"></a>
### _Organized Desktop/12 Other Projects/cc

CMS web-application prototype.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma.
- **Learning content now:** No substantive guide verified. No populated entrypoint verified in the tutorial review.
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of tree structure, revisions and inherited permissions, known stubs and one exercise targeting CMS content modeling, edit workflows, API/UI separation. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Establish one implemented content workflow and test validation and permission boundaries. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [db.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/cc/src/lib/db.ts), [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/cc/src/lib/auth.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/cc/package.json).

---

<a id="p204"></a>
### _Organized Desktop/12 Other Projects/jdtrrain2.1

Full-stack JavaScript project management platform built with Next.js App Router, Prisma, SQLite, React Query, dnd-kit, and Recharts.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: API + SQL project; schema design, validation, sessions, and basic tests.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, Next.js, Node.js, React, Prisma.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/jdtrrain2.1/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of ownership, ordering and lifecycle transitions, known stubs and one exercise targeting Next.js CRUD, Prisma/SQLite, drag-and-drop, React Query, reporting. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace a task move into persistence and test ordering plus invalid project references. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/jdtrrain2.1/README.md), [cn.js](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/jdtrrain2.1/src/lib/cn.js), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/jdtrrain2.1/package.json).

---

<a id="p243"></a>
### geminiorganized/General_.Todo

ASP.NET Core eShopOnWeb reference storefront demonstrating a monolithic web application.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** C#, CSS, JavaScript, Razor, SCSS, ASP.NET Core, Blazor, Entity Framework Core, SQL Server, Docker, GitHub Actions, MSTest, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_.Todo/eShopOnWeb/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of stock ownership, checkout and order transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Layered ASP.NET application, EF Core, identity, storefronts.
- **2 — Improve the project/resource:** First scoped project change: Trace basket-to-order flow, then make one small tested change. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [.nettodo](C:/Users/Owner/Desktop/.nettodo). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_.Todo/eShopOnWeb/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_.Todo/eShopOnWeb/fabledocs/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/General_.Todo/eShopOnWeb/docker-compose.yml).

---

<a id="p256"></a>
### geminiorganized/General_Gitjira-App

A Jira-style issue tracker, built in public as a teaching codebase — 15 sprints, each landing as one reviewed pull request full of learning artifacts. v1.0.0 .

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Express, Node.js, React, Vite, Prisma, Redis, Docker, GitHub Actions, Playwright, Vitest, BullMQ, Socket.IO.
- **Learning content now:** Developer explanation / brief orientation. Start at [ARCHITECTURE.md](C:/Users/Owner/Desktop/geminiorganized/General_Gitjira-App/docs/ARCHITECTURE.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, ordering and lifecycle transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting Full-stack issue tracking, auth, relational data, reviewable delivery.
- **2 — Improve the project/resource:** First scoped project change: Trace one issue request, fix one bug, and ship one independently explained feature. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [gitjira-app](C:/Users/Owner/Desktop/gitjira-app). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Gitjira-App/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Gitjira-App/docs/adr/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Gitjira-App/package.json).

---

<a id="p291"></a>
### geminiorganized/LLM_Generated_Ecommerceproject

A full-stack E-commerce Platform built for educational purposes to upskill to mid/senior SWE level.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Ecommerceproject/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for stock ownership, checkout and order transitions; make learners predict state before running it. Teach React/API separation, cart/order rules, Prisma with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Complete and test one order flow before adding new domains. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [grokbuildecommerceproject](C:/Users/Owner/Desktop/grokbuildecommerceproject). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Ecommerceproject/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Ecommerceproject/docker-compose.yml), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Ecommerceproject/backend/package.json).

---

<a id="p298"></a>
### geminiorganized/LLM_Generated_Hrproject

Full-stack HR / People Operations Platform (Educational)

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Jest, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [JOURNAL.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Hrproject/JOURNAL.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for employee lifecycle, approval and tenant scope; make learners predict state before running it. Teach Employee data, leave workflows, pagination, RBAC with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace one leave request and test authorization. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [grokbuildhrproject](C:/Users/Owner/Desktop/grokbuildhrproject). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Hrproject/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Hrproject/docker-compose.yml), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Hrproject/backend/package.json).

---

<a id="p303"></a>
### geminiorganized/LLM_Generated_Ppmproject

Project-portfolio management practice app with portfolios, programs, projects, and tasks.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Ppmproject/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ownership, ordering and lifecycle transitions; make learners predict state before running it. Teach Hierarchical domain models, relationships, permissions with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Add one hierarchy constraint and test an invalid relationship. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [grokbuildppmproject](C:/Users/Owner/Desktop/grokbuildppmproject). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Ppmproject/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Ppmproject/docker-compose.yml), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Ppmproject/backend/package.json).

---

<a id="p305"></a>
### geminiorganized/LLM_Generated_Supportproject

Full-stack Customer Support Ticketing + Knowledge Base Platform

- **Use / order:** Supporting resource; improve only when using it with an active project. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Static sample does not establish runtime readiness. Local documentation: This project is designed for learning, not production. The comments, journal, and plans are the main value.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Supportproject/README.md).
- **1 — Improve the upskilling content:** Turn the material on Support domain modeling, API planning, ticket workflows into one active-project exercise: a prediction, an independent attempt, a worked answer and a reflection prompt. Start with: Use the specification only if choosing to build a support vertical slice.
- **2 — Improve the project/resource:** Improve this resource itself: add an index, intended audience, prerequisite milestone and links to the actual exercise/code evidence. Date historical claims and distinguish advice from observed behavior.
- **3 — Prove completion:** Complete one linked exercise in the active project, record the result and verify that a reader can find its prompt and evidence from this resource’s index.
- **4 — Consolidate:** Record one demonstrated skill and remove or label unsupported claims; do not invent an application feature for a reference-only folder.
- **Related locations to compare:** [grokbuildsupportproject](C:/Users/Owner/Desktop/grokbuildsupportproject). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Supportproject/README.md).

---

<a id="p306"></a>
### geminiorganized/LLM_Generated_Teamproject

A full-stack Team / Project Management application built for educational purposes.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Jest, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [JOURNAL.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Teamproject/JOURNAL.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ownership, ordering and lifecycle transitions; make learners predict state before running it. Teach Teams, project CRUD, JWT, validation, relational data with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Test one team-scoped API and its React loading/error states. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [grokbuildteamproject](C:/Users/Owner/Desktop/grokbuildteamproject). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Teamproject/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Teamproject/docker-compose.yml), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Teamproject/backend/package.json).

---

<a id="p307"></a>
### geminiorganized/OpenSource_Upskilling_.Ramp

A learning-oriented clone of Ramp / Expensify / Brex expense workflows, built with ASP.NET Core (C#) and React.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Teaching/reference workspace; runtime not verified. Local documentation: Storage/ In-memory DataStore (singleton) + demo seeding; background Channel, JSON) ships with the .NET SDK. Swapping the in-memory
- **Recorded stack:** C#, CSS, HTML, JavaScript, ASP.NET Core, React, Vite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_.Ramp/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, upload/finalization state and storage boundaries, an expected-state example and a guided-to-independent change exercise. Tie it to Role-scoped expense workflows, state machines, uploads.
- **2 — Improve the project/resource:** First scoped project change: Persist one expense workflow and test approval transitions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Try an unauthorized or expired operation and an interrupted retry; verify no orphaned committed state or double quota charge.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [.netramp](C:/Users/Owner/Desktop/.netramp). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_.Ramp/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_.Ramp/docs/upskill/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_.Ramp/frontend/package.json).

---

<a id="p313"></a>
### geminiorganized/OpenSource_Upskilling_Linear

NetLinear is a Linear/Jira-style issue tracker scaffold built with .NET 8, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** Teaching/reference workspace; runtime not verified. Local documentation: NetLinear is a Linear/Jira-style issue tracker scaffold built with .NET 8, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Linear/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ownership, ordering and lifecycle transitions; make learners predict state before running it. Teach REST, EF Core, filtered queries, optimistic mutations, xmin concurrency and workflow transitions. with a separate answer and rubric. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Complete an issue CRUD slice, then replace demo identity with authenticated users and prove stale-write conflict handling. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [netlinear](C:/Users/Owner/Desktop/netlinear). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Linear/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Linear/docs/upskill/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Linear/docker-compose.yml).

---

<a id="p319"></a>
### gitjira-app

A Jira-style issue tracker, built in public as a teaching codebase — 15 sprints, each landing as one reviewed pull request full of learning artifacts. v1.0.0 .

- **Use / order:** Primary route candidate; complete this milestone before adding an alternative. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Substantial Express/React teaching code and tests; README completion claim is not fresh runtime verification. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Express, Node.js, React, Vite, Prisma, Redis, Docker, GitHub Actions, Playwright, Vitest, BullMQ, Socket.IO.
- **Learning content now:** Developer explanation / brief orientation. Start at [ARCHITECTURE.md](C:/Users/Owner/Desktop/gitjira-app/docs/ARCHITECTURE.md).
- **1 — Improve the upskilling content:** Extend ARCHITECTURE.md with one issue-transition reading route and a guided exercise followed by an independent variation; link the relevant sprint material from gitjira.
- **2 — Improve the project/resource:** Make one issue transition preserve project membership and reject stale writes, using the existing model and version mechanism where present.
- **3 — Prove completion:** A project member completes the transition, a nonmember is denied, and two stale competing updates cannot silently overwrite each other; the interface explains the rejected change.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Gitjira-App](C:/Users/Owner/Desktop/geminiorganized/General_Gitjira-App). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitjira-app/README.md), [App.jsx](C:/Users/Owner/Desktop/gitjira-app/apps/web/src/App.jsx), [package.json](C:/Users/Owner/Desktop/gitjira-app/package.json).

---

<a id="p335"></a>
### gitvg/storefront

E-commerce teaching app with customer browsing/cart/order flows and seller product, inventory, order, and image management.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Compact Next.js/PostgreSQL teaching app with source and tests. Static review only; not built, tested or run.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Docker, GitHub Actions, Playwright, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/gitvg/storefront/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for stock ownership, checkout and order transitions; make learners predict state before running it. Teach Next.js full-stack boundaries, SQL, commerce, caching with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace product-to-order flow and add one access-control test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/storefront/README.md), [catalog.ts](C:/Users/Owner/Desktop/gitvg/storefront/server/services/catalog.ts), [package.json](C:/Users/Owner/Desktop/gitvg/storefront/package.json).

---

<a id="p340"></a>
### grokbuildecommerceproject

A full-stack E-commerce Platform built for educational purposes to upskill to mid/senior SWE level.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Compact educational commerce slice with a few test files; breadth in docs exceeds what a sample proves. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/grokbuildecommerceproject/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for stock ownership, checkout and order transitions; make learners predict state before running it. Teach React/API separation, cart/order rules, Prisma with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Complete and test one order flow before adding new domains. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Ecommerceproject](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Ecommerceproject). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/grokbuildecommerceproject/README.md), [App.tsx](C:/Users/Owner/Desktop/grokbuildecommerceproject/frontend/src/App.tsx), [docker-compose.yml](C:/Users/Owner/Desktop/grokbuildecommerceproject/docker-compose.yml).

---

<a id="p341"></a>
### grokbuildhrproject

Full-stack HR / People Operations Platform (Educational)

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Small Express/React/Prisma teaching implementation; advanced production claims are aspirational. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Jest, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [JOURNAL.md](C:/Users/Owner/Desktop/grokbuildhrproject/JOURNAL.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for employee lifecycle, approval and tenant scope; make learners predict state before running it. Teach Employee data, leave workflows, pagination, RBAC with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace one leave request and test authorization. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/grokbuildhrproject/README.md), [App.tsx](C:/Users/Owner/Desktop/grokbuildhrproject/frontend/src/App.tsx), [docker-compose.yml](C:/Users/Owner/Desktop/grokbuildhrproject/docker-compose.yml).

---

<a id="p344"></a>
### grokbuildppmproject

Project-portfolio management practice app with portfolios, programs, projects, and tasks.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Compact portfolio/project/task teaching app with tests; not a full enterprise PPM implementation. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/grokbuildppmproject/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ownership, ordering and lifecycle transitions; make learners predict state before running it. Teach Hierarchical domain models, relationships, permissions with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Add one hierarchy constraint and test an invalid relationship. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/grokbuildppmproject/README.md), [App.tsx](C:/Users/Owner/Desktop/grokbuildppmproject/frontend/src/App.tsx), [docker-compose.yml](C:/Users/Owner/Desktop/grokbuildppmproject/docker-compose.yml).

---

<a id="p345"></a>
### grokbuildsupportproject

Full-stack Customer Support Ticketing + Knowledge Base Platform

- **Use / order:** Supporting resource; improve only when using it with an active project. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Documentation-only in inventory: no source or test files, despite full-stack wording in README. Static review only; not built, tested or run.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/grokbuildsupportproject/README.md).
- **1 — Improve the upskilling content:** Turn the material on Support domain modeling, API planning, ticket workflows into one active-project exercise: a prediction, an independent attempt, a worked answer and a reflection prompt. Start with: Use the specification only if choosing to build a support vertical slice.
- **2 — Improve the project/resource:** Improve this resource itself: add an index, intended audience, prerequisite milestone and links to the actual exercise/code evidence. Date historical claims and distinguish advice from observed behavior.
- **3 — Prove completion:** Complete one linked exercise in the active project, record the result and verify that a reader can find its prompt and evidence from this resource’s index.
- **4 — Consolidate:** Record one demonstrated skill and remove or label unsupported claims; do not invent an application feature for a reference-only folder.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/grokbuildsupportproject/README.md).

---

<a id="p346"></a>
### grokbuildteamproject

A full-stack Team / Project Management application built for educational purposes.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: One local client app plus one API with persistence and basic tests.
- **Baseline:** Compact educational full-stack app; overlaps many issue/project trackers. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Jest, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [JOURNAL.md](C:/Users/Owner/Desktop/grokbuildteamproject/JOURNAL.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ownership, ordering and lifecycle transitions; make learners predict state before running it. Teach Teams, project CRUD, JWT, validation, relational data with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Test one team-scoped API and its React loading/error states. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/grokbuildteamproject/README.md), [App.tsx](C:/Users/Owner/Desktop/grokbuildteamproject/frontend/src/App.tsx), [docker-compose.yml](C:/Users/Owner/Desktop/grokbuildteamproject/docker-compose.yml).

---

<a id="p369"></a>
### netlinear

NetLinear is a Linear/Jira-style issue tracker scaffold built with .NET 8, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** Issue-tracker scaffold with workflow/concurrency code. Auth is explicitly a fixed demo-user dev-login endpoint; frontend obtains it automatically.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/netlinear/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ownership, ordering and lifecycle transitions; make learners predict state before running it. Teach REST, EF Core, filtered queries, optimistic mutations, xmin concurrency and workflow transitions. with a separate answer and rubric. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Complete an issue CRUD slice, then replace demo identity with authenticated users and prove stale-write conflict handling. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [geminiorganized/OpenSource_Upskilling_Linear](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Linear). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netlinear/README.md), [AuthController.cs](C:/Users/Owner/Desktop/netlinear/src/NetLinear.Api/Controllers/AuthController.cs), [IssuesController.cs](C:/Users/Owner/Desktop/netlinear/src/NetLinear.Api/Controllers/IssuesController.cs).

---

<a id="p390"></a>
### newcodex3/apps/16-blog-platform

Multi-user blog

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/16-blog-platform/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for content validation, publication and access boundaries; make learners predict state before running it. Teach RBAC, editorial state transitions and comment moderation with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace one draft-to-published transition and reject an unauthorized editor action. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an unauthorized publish or invalid content payload; verify one permitted publication is rendered as intended.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/16-blog-platform-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/16-blog-platform/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/16-blog-platform/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/16-blog-platform/client/package.json).

---

<a id="p391"></a>
### newcodex3/apps/16-blog-platform-net

Multi-user blog (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/16-blog-platform-net/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for content validation, publication and access boundaries; make learners predict state before running it. Teach RBAC, editorial state transitions and comment moderation with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace one draft-to-published transition and reject an unauthorized editor action. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an unauthorized publish or invalid content payload; verify one permitted publication is rendered as intended.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/16-blog-platform; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/16-blog-platform-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/16-blog-platform-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/16-blog-platform-net/server/BlogPlatform.Api/Program.cs).

---

<a id="p420"></a>
### newcodex3/apps/31-multi-tenant-crm

Multi-tenant CRM

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/31-multi-tenant-crm/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ownership, ordering and lifecycle transitions; make learners predict state before running it. Teach Tenant scoping, ownership, soft-delete and audit trails with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Replace header-only tenant assumptions and test cross-tenant access. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/31-multi-tenant-crm-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/31-multi-tenant-crm/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/31-multi-tenant-crm/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/31-multi-tenant-crm/client/package.json).

---

<a id="p421"></a>
### newcodex3/apps/31-multi-tenant-crm-net

Multi-tenant CRM (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/31-multi-tenant-crm-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, ordering and lifecycle transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting Tenant scoping, ownership, soft-delete and audit trails.
- **2 — Improve the project/resource:** First scoped project change: Replace header-only tenant assumptions and test cross-tenant access. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/31-multi-tenant-crm; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/31-multi-tenant-crm-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/31-multi-tenant-crm-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/31-multi-tenant-crm-net/server/Program.cs).

---

<a id="p434"></a>
### newcodex3/apps/38-admin-settings-permissions-console

Admin settings/permissions

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/38-admin-settings-permissions-console/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for settings versions, privilege boundaries and audit history; make learners predict state before running it. Teach Granular RBAC, versioned settings and auditable updates with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Reject a stale settings update and prove viewer roles cannot mutate billing/security settings. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a stale write and a viewer mutation; a permitted update must produce one coherent configuration revision and audit event.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/38-admin-settings-permissions-console-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/38-admin-settings-permissions-console/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/38-admin-settings-permissions-console/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/38-admin-settings-permissions-console/client/package.json).

---

<a id="p435"></a>
### newcodex3/apps/38-admin-settings-permissions-console-net

Admin settings/permissions (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/38-admin-settings-permissions-console-net/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for settings versions, privilege boundaries and audit history; make learners predict state before running it. Teach Granular RBAC, versioned settings and auditable updates with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Reject a stale settings update and prove viewer roles cannot mutate billing/security settings. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a stale write and a viewer mutation; a permitted update must produce one coherent configuration revision and audit event.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/38-admin-settings-permissions-console; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/38-admin-settings-permissions-console-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/38-admin-settings-permissions-console-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/38-admin-settings-permissions-console-net/server/Program.cs).

---

<a id="p444"></a>
### newcodexJS/05-recipe-manager

Recipe manager with accounts

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/05-recipe-manager/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to JWT/refresh lifecycle, protected routes and nested Knex transactions.
- **2 — Improve the project/resource:** First scoped project change: Trace sign-in to recipe ownership and prove a failed nested write rolls back. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/05-recipe-manager/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/05-recipe-manager/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/05-recipe-manager/client/package.json).

---

<a id="p446"></a>
### newcodexJS/07-blog-platform

Blog platform

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/07-blog-platform/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of content validation, publication and access boundaries, an expected-state example and a guided-to-independent change exercise. Tie it to Content rendering, sanitization and publication workflow.
- **2 — Improve the project/resource:** First scoped project change: Verify rendered content safety and one authorized publish transition. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an unauthorized publish or invalid content payload; verify one permitted publication is rendered as intended.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/07-blog-platform/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/07-blog-platform/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/07-blog-platform/client/package.json).

---

<a id="p447"></a>
### newcodexJS/08-kanban-board

Kanban board

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/08-kanban-board/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, ordering and lifecycle transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Optimistic drag order and fractional ordering concepts.
- **2 — Improve the project/resource:** First scoped project change: Implement persistent reorder and verify two concurrent updates cannot silently lose a card. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/08-kanban-board/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/08-kanban-board/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/08-kanban-board/client/package.json).

---

<a id="p448"></a>
### newcodexJS/09-job-application-tracker

Job application tracker

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/09-job-application-tracker/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Pipeline transitions, attachment boundaries and history.
- **2 — Improve the project/resource:** First scoped project change: Implement one status transition with an auditable history record. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/09-job-application-tracker/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/09-job-application-tracker/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/09-job-application-tracker/client/package.json).

---

<a id="p449"></a>
### newcodexJS/10-inventory-management

Inventory management

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/10-inventory-management/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of stock ownership, checkout and order transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Stock movement ledger and purchase/sales workflow concepts.
- **2 — Improve the project/resource:** First scoped project change: Replace direct stock edits with a transaction-backed movement and test totals. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/10-inventory-management/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/10-inventory-management/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/10-inventory-management/client/package.json).

---

<a id="p450"></a>
### newcodexJS/11-survey-builder

Survey builder

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. README describes development/demo identity headers rather than completed authentication.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/11-survey-builder/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of event identity, aggregation and reporting filters, an expected-state example and a guided-to-independent change exercise. Tie it to Public response validation, nested questions and result aggregation.
- **2 — Improve the project/resource:** First scoped project change: Verify a response cannot target unpublished or foreign questions; replace demo identity for admin flows. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/11-survey-builder/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/11-survey-builder/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/11-survey-builder/client/package.json).

---

<a id="p451"></a>
### newcodexJS/12-chat-polling

HTTP-polling chat

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. README describes development/demo identity headers rather than completed authentication.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/12-chat-polling/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of membership, event identity and reconnect behavior, an expected-state example and a guided-to-independent change exercise. Tie it to Conversation membership, polling cursors and read state.
- **2 — Improve the project/resource:** First scoped project change: Test reconnect/poll overlap without duplicate messages and replace demo-user headers. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/12-chat-polling/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/12-chat-polling/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/12-chat-polling/client/package.json).

---

<a id="p455"></a>
### newcodexJS/16-team-project-management

Team-project management

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Shares a generic scoped CRUD/admin structure with 16-20; specialized title does not establish a complete domain engine.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/16-team-project-management/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, ordering and lifecycle transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Generic scoped CRUD, saved views, comments, audit and bulk status.
- **2 — Improve the project/resource:** First scoped project change: Prove project scope and bulk-change auditing on one complete workflow. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/16-team-project-management/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/16-team-project-management/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/16-team-project-management/client/package.json).

---

<a id="p456"></a>
### newcodexJS/17-support-ticket-system

Support-ticket admin

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Shares a generic scoped CRUD/admin structure with 16-20; specialized title does not establish a complete domain engine.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/17-support-ticket-system/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ticket visibility, assignment and service deadlines, an expected-state example and a guided-to-independent change exercise. Tie it to Generic ticket CRUD, priority/SLA metadata and audit.
- **2 — Improve the project/resource:** First scoped project change: Implement one real SLA deadline job and prove internal comments remain private. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/17-support-ticket-system/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/17-support-ticket-system/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/17-support-ticket-system/client/package.json).

---

<a id="p457"></a>
### newcodexJS/18-learning-management-system

Learning-management admin

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Shares a generic scoped CRUD/admin structure with 16-20; specialized title does not establish a complete domain engine.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/18-learning-management-system/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of eligibility, progress and completion transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Generic course catalog CRUD and publication lifecycle.
- **2 — Improve the project/resource:** First scoped project change: Implement one learner enrollment/progress behavior if choosing this domain. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an ineligible completion; repeat a valid progress event and verify progress and any certificate/review state remain consistent.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/18-learning-management-system/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/18-learning-management-system/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/18-learning-management-system/client/package.json).

---

<a id="p458"></a>
### newcodexJS/19-realtime-chat-platform

Conversation administration

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Shares a generic scoped CRUD/admin structure with 16-20; specialized title does not establish a complete domain engine.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/19-realtime-chat-platform/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of membership, event identity and reconnect behavior, an expected-state example and a guided-to-independent change exercise. Tie it to Generic conversation CRUD, moderation metadata and audit; realtime transport not established.
- **2 — Improve the project/resource:** First scoped project change: Use the polling-chat app or netintercom for messaging, or add a tested transport to this scaffold. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/19-realtime-chat-platform/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/19-realtime-chat-platform/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/19-realtime-chat-platform/client/package.json).

---

<a id="p459"></a>
### newcodexJS/20-marketplace-platform

Marketplace listing admin

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 4; prerequisites: One complete CRUD API plus relational schema, React data fetching and basic test design.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Shares a generic scoped CRUD/admin structure with 16-20; specialized title does not establish a complete domain engine.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/20-marketplace-platform/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of money units, state transitions and duplicate deliveries, an expected-state example and a guided-to-independent change exercise. Tie it to Generic vendor listing CRUD and moderation; payment/order marketplace engine not established.
- **2 — Improve the project/resource:** First scoped project change: Implement vendor authorization and one meaningful listing moderation transition. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/20-marketplace-platform/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/20-marketplace-platform/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/20-marketplace-platform/client/package.json).

---
