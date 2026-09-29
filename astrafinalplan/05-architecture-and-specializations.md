# Section 5: Architecture and specializations

[Plan index](README.md)

Choose one advanced branch after reliable full-stack delivery. Large upstream repositories are bounded reading/contribution exercises; AI, realtime, games and mobile are optional specializations.

**Stage exit criterion:** Deliver one bounded architectural or specialist improvement, with a reproducible failure scenario, justified tradeoff, and relevant regression or evaluation evidence.

**Coverage:** 149 project/workspace/resource records and 15 nested teaching apps. Entries are grouped by original milestone and alphabetized within it; alphabetical position is not a mandatory execution order. Use the short route in the index.

All actions below are proposals based on the September 6–7 static reviews. Reproduce the baseline before claiming a defect or improvement. Existing tests and docs may already cover a proposed case; assess and strengthen them rather than duplicate them.

## Entries

- [.netarchitectureproject](#p001)
- [.netopen2](#p002)
- [_Organized Desktop/01 Net Workspaces/.netvg](#p012)
- [_Organized Desktop/02 Build Projects/buildagenthelpdesk](#p016)
- [_Organized Desktop/02 Build Projects/buildagentteachGEM](#p017)
- [_Organized Desktop/02 Build Projects/buildagentteaching](#p018)
- [_Organized Desktop/02 Build Projects/buildantigVG](#p020)
- [_Organized Desktop/03 Master Projects/master 6](#p029)
- [_Organized Desktop/03 Master Projects/master1](#p030)
- [_Organized Desktop/03 Master Projects/master2](#p031)
- [_Organized Desktop/03 Master Projects/master3](#p032)
- [_Organized Desktop/03 Master Projects/master4](#p033)
- [_Organized Desktop/03 Master Projects/master7](#p034)
- [_Organized Desktop/03 Master Projects/mastercal](#p035)
- [_Organized Desktop/03 Master Projects/masterdidy](#p036)
- [_Organized Desktop/03 Master Projects/masterdub](#p037)
- [_Organized Desktop/03 Master Projects/masterfinisc](#p038)
- [_Organized Desktop/03 Master Projects/masterflag](#p039)
- [_Organized Desktop/03 Master Projects/masterform](#p040)
- [_Organized Desktop/03 Master Projects/masterhop](#p041)
- [_Organized Desktop/03 Master Projects/masteridur](#p042)
- [_Organized Desktop/03 Master Projects/masterindicoPYJS](#p043)
- [_Organized Desktop/03 Master Projects/masterlink](#p044)
- [_Organized Desktop/03 Master Projects/mastermatter](#p045)
- [_Organized Desktop/03 Master Projects/mastermayan](#p046)
- [_Organized Desktop/03 Master Projects/mastermorphic](#p047)
- [_Organized Desktop/03 Master Projects/masternext](#p048)
- [_Organized Desktop/03 Master Projects/masternovu](#p049)
- [_Organized Desktop/03 Master Projects/masteropen](#p050)
- [_Organized Desktop/03 Master Projects/masteropenedxPYJS](#p051)
- [_Organized Desktop/03 Master Projects/masterpaper](#p052)
- [_Organized Desktop/03 Master Projects/masterplane](#p053)
- [_Organized Desktop/03 Master Projects/masterpload](#p054)
- [_Organized Desktop/03 Master Projects/masterpostiz](#p055)
- [_Organized Desktop/03 Master Projects/masterpre](#p056)
- [_Organized Desktop/03 Master Projects/mastersaleorPY](#p058)
- [_Organized Desktop/03 Master Projects/mastershadcn](#p059)
- [_Organized Desktop/03 Master Projects/MasterStore](#p060)
- [_Organized Desktop/03 Master Projects/mastersupa](#p061)
- [_Organized Desktop/03 Master Projects/mastertea](#p062)
- [_Organized Desktop/03 Master Projects/mastertool](#p063)
- [_Organized Desktop/03 Master Projects/mastertwenty](#p064)
- [_Organized Desktop/03 Master Projects/mastertypebot](#p065)
- [_Organized Desktop/03 Master Projects/masterumami](#p066)
- [_Organized Desktop/03 Master Projects/masterzulipPY](#p067)
- [_Organized Desktop/04 JavaScript Training/reactbullet](#p080)
- [_Organized Desktop/05 Numbered Experiments/e20](#p095)
- [_Organized Desktop/05 Numbered Experiments/rn1](#p106)
- [_Organized Desktop/05 Numbered Experiments/w21](#p107)
- [_Organized Desktop/05 Numbered Experiments/w23](#p109)
- [_Organized Desktop/05 Numbered Experiments/ww27](#p124)
- [_Organized Desktop/05 Numbered Experiments/ww3](#p127)
- [_Organized Desktop/07 Anti Projects/antitestbuild](#p179)
- [_Organized Desktop/09 Grav And VG Projects/grav1pretalx](#p189)
- [_Organized Desktop/09 Grav And VG Projects/graveopenjspy](#p190)
- [_Organized Desktop/09 Grav And VG Projects/gravreviewboardjspy](#p191)
- [_Organized Desktop/09 Grav And VG Projects/vg](#p192)
- [_Organized Desktop/09 Grav And VG Projects/VGdemo](#p193)
- [_Organized Desktop/12 Other Projects/andie](#p196)
- [_Organized Desktop/12 Other Projects/pp8](#p206)
- [_Organized Desktop/12 Other Projects/pyhealth](#p207)
- [astra1](#p217)
- [buildevent](#p224)
- [buildreviewer](#p225)
- [geminiorganized/General_.Architectureproject](#p241)
- [geminiorganized/General_.Open2](#p242)
- [geminiorganized/General_Cleanarch](#p250)
- [geminiorganized/General_Gitvg](#p257)
- [geminiorganized/General_Masternocu](#p261)
- [geminiorganized/General_Missioncontrol](#p265)
- [geminiorganized/General_Nopsolutions](#p270)
- [geminiorganized/General_Open1](#p271)
- [geminiorganized/General_Open3](#p272)
- [geminiorganized/LLM_Generated_Buildevent](#p285)
- [geminiorganized/LLM_Generated_Buildreviewer](#p286)
- [geminiorganized/OpenSource_Upskilling_Auth](#p309)
- [geminiorganized/OpenSource_Upskilling_Drop](#p311)
- [gitvg/bazaar](#p325)
- [gitvg/harbor-net](#p330)
- [gitvg/pulse](#p331)
- [gitvg/pulse-net](#p332)
- [gitvg/relay](#p333)
- [gitvg/relay-app](#p334)
- [masternocu](#p358)
- [missioncontrol](#p361)
- [netauth](#p364)
- [netcleanarch](#p365)
- [netdrop](#p367)
- [netopen1](#p371)
- [netopen3](#p372)
- [newcodex3/apps/24-file-sharing-app](#p406)
- [newcodex3/apps/24-file-sharing-app-net](#p407)
- [newcodex3/apps/30-headless-cms](#p418)
- [newcodex3/apps/30-headless-cms-net](#p419)
- [newcodex3/apps/34-oauth-saas-identity-portal](#p426)
- [newcodex3/apps/34-oauth-saas-identity-portal-net](#p427)
- [newcodex3/apps/36-feature-flag-management](#p430)
- [newcodex3/apps/36-feature-flag-management-net](#p431)
- [newcodex3/apps/39-third-party-integration-sync-hub](#p436)
- [newcodex3/apps/39-third-party-integration-sync-hub-net](#p437)
- [newcodex3/apps/40-observability-incident-dashboard](#p438)
- [newcodex3/apps/40-observability-incident-dashboard-net](#p439)
- [nopsolutionsnet](#p380)
- [_Organized Desktop/01 Net Workspaces/.netslack](#p010)
- [_Organized Desktop/03 Master Projects/masterrnative](#p057)
- [_Organized Desktop/04 JavaScript Training/jep vs code](#p068)
- [_Organized Desktop/05 Numbered Experiments/D2](#p085)
- [_Organized Desktop/05 Numbered Experiments/ww32](#p130)
- [_Organized Desktop/06 AI And Learning/aiapplybot](#p168)
- [_Organized Desktop/06 AI And Learning/aiapplybotjs](#p169)
- [_Organized Desktop/06 AI And Learning/codehelper](#p173)
- [_Organized Desktop/06 AI And Learning/think](#p175)
- [_Organized Desktop/08 App And Product Projects/eliapplybot](#p181)
- [_Organized Desktop/08 App And Product Projects/eliapplybot-python](#p182)
- [_Organized Desktop/12 Other Projects/appmaketrck](#p197)
- [_Organized Desktop/12 Other Projects/curse](#p199)
- [_Organized Desktop/12 Other Projects/finaljepgame](#p201)
- [aiapplybot](#p208)
- [aicallhelper](#p209)
- [aicallhelper2](#p210)
- [aiheartbeat](#p211)
- [aihelper](#p212)
- [aral](#p216)
- [astra2](#p218)
- [astraspacegameweb](#p220)
- [buildermentor](#p223)
- [buildsmallplates](#p226)
- [buildwhiteboard](#p228)
- [fableaihelperv2](#p235)
- [fableaihelperv3](#p236)
- [finalcallhelp](#p237)
- [geminiorganized/General_Aral](#p246)
- [geminiorganized/General_Jsharness](#p259)
- [geminiorganized/General_Masteroutline](#p262)
- [geminiorganized/General_Mobiletagalog](#p266)
- [geminiorganized/General_Open5](#p273)
- [geminiorganized/General_Spacegame](#p280)
- [geminiorganized/General_Tagalog](#p281)
- [geminiorganized/LLM_Generated_Applybot](#p282)
- [geminiorganized/LLM_Generated_Buildermentor](#p284)
- [geminiorganized/LLM_Generated_Buildsmallplates](#p287)
- [geminiorganized/LLM_Generated_Buildwhiteboard](#p289)
- [geminiorganized/LLM_Generated_Fablehelperv2](#p292)
- [geminiorganized/LLM_Generated_Fablehelperv3](#p293)
- [geminiorganized/LLM_Generated_Helper](#p297)
- [geminiorganized/LLM_Generated_Rag](#p304)
- [geminiorganized/OpenSource_Upskilling_Intercom](#p312)
- [gitvg/folio](#p327)
- [gitvg/folio-app](#p328)
- [gitvg/harbor](#p329)
- [gitvg/tracer](#p336)
- [jsharness/ctvodejs](#p352)
- [jsharness/VTCode](#p353)
- [masteroutline](#p359)
- [mobiletagalog](#p362)
- [netairag](#p363)
- [netintercom](#p368)
- [netopen5](#p373)
- [newcodecjs2/helpkit](#p462)
- [newcodex3/apps/18-team-chat](#p394)
- [newcodex3/apps/18-team-chat-net](#p395)
- [spacegame](#p387)
- [spacegamev2](#p388)
- [tagalog](#p389)

## Per-project improvement plans

<a id="p001"></a>
### .netarchitectureproject

Full Modular Monolith .NET application with Domain-Driven Design approach.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Large upstream reference with source and tests. The old catalog's unfinished/authentication caveat misquotes a discussion of OTHER examples. Static review only; not built, tested or run.
- **Recorded stack:** C#, HTML, SQL, ASP.NET Core, SQL Server, Docker, GitHub Actions.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/.netarchitectureproject/modular-monolith-with-ddd/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting DDD boundaries, domain events, modular monoliths. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace one meeting command across module boundaries and explain its transaction. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [geminiorganized/General_.Architectureproject](C:/Users/Owner/Desktop/geminiorganized/General_.Architectureproject). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/.netarchitectureproject/modular-monolith-with-ddd/README.md), [Program.cs](C:/Users/Owner/Desktop/.netarchitectureproject/modular-monolith-with-ddd/src/Database/DatabaseMigrator/Program.cs), [docker-compose.yml](C:/Users/Owner/Desktop/.netarchitectureproject/modular-monolith-with-ddd/docker-compose.yml).

---

<a id="p002"></a>
### .netopen2

Orchard Core is an open-source, modular, multi-tenant application framework and CMS for ASP.NET Core.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Large upstream Orchard Core checkout; useful after API fundamentals, not a beginner build target. Static review only; not built, tested or run.
- **Recorded stack:** C#, CSS, HTML, JavaScript, Razor, SCSS, TypeScript, ASP.NET Core, Vite, Vue, Docker, GitHub Actions, Moq, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/.netopen2/OrchardCore/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of content validation, publication and access boundaries, an expected-state example and a guided-to-independent change exercise. Tie it to Extensible CMS, tenants, dependency injection, mature code navigation.
- **2 — Improve the project/resource:** First scoped project change: Study one small module and propose one bounded fix. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Reject an unauthorized publish or invalid content payload; verify one permitted publication is rendered as intended.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_.Open2](C:/Users/Owner/Desktop/geminiorganized/General_.Open2). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/.netopen2/OrchardCore/README.md), [Program.cs](C:/Users/Owner/Desktop/.netopen2/OrchardCore/src/OrchardCore.Cms.Web/Program.cs), [package.json](C:/Users/Owner/Desktop/.netopen2/OrchardCore/package.json).

---

<a id="p012"></a>
### _Organized Desktop/01 Net Workspaces/.netvg

AtlasWork is a teaching application for global workforce hiring, payment, and employee/contractor management.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: README describes seeded in-memory read models and deterministic mock frontend fallback data.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, GitHub Actions, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netvg/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of employee lifecycle, approval and tenant scope, an expected-state example and a guided-to-independent change exercise. Tie it to tenant isolation, approval rules, audit history, module boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace one employee approval and test both cross-tenant access and invalid state changes. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** The Fable folder is a code-review pack; docs/upskill supplies the actual learning curriculum.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netvg/README.md), [Program.cs](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netvg/src/PeblClone.Api/Program.cs), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netvg/src/PeblClone.Web/package.json).

---

<a id="p016"></a>
### _Organized Desktop/02 Build Projects/buildagenthelpdesk

TypeScript modular monolith that emulates a mid-size internal enterprise platform.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Agent behavior uses deterministic local mocks.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Prisma, Docker, GitHub Actions, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagenthelpdesk/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagenthelpdesk/README.md), [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagenthelpdesk/apps/web/lib/auth.ts), [jobs.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagenthelpdesk/packages/domain/src/jobs.ts).

---

<a id="p017"></a>
### _Organized Desktop/02 Build Projects/buildagentteachGEM

A school operations cockpit built as a software engineering training laboratory.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Agent layer is documented as five deterministic mock-LLM analysts.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Prisma.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagentteachGEM/fabledocs/README.md).
- **1 — Improve the upskilling content:** Reconcile baseline gotchas with 04-what-changed.md; add an enrollment-to-certification trace against the selected revision.
- **2 — Improve the project/resource:** Enforce one certification eligibility rule at the domain boundary and show the rejection in the UI.
- **3 — Prove completion:** An ineligible learner cannot receive a certification through direct API use; the eligible case records completion once.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** The gotchas document describes an earlier baseline; check 04-what-changed.md before treating a listed issue as current.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagentteachGEM/README.md), [page.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagentteachGEM/src/app/page.tsx), [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagentteachGEM/src/packages/shared/auth.ts).

---

<a id="p018"></a>
### _Organized Desktop/02 Build Projects/buildagentteaching

Agentic Education Operations is a TypeScript modular-monolith learning project that emulates the start of a internal education operations and LMS platform.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Agent behavior uses deterministic local mocks.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Prisma, Docker, GitHub Actions, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagentteaching/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the codebase reading guide with a concrete enrollment-to-certification exercise and transaction map.
- **2 — Improve the project/resource:** Enforce one certification eligibility rule across the application and persistence boundary.
- **3 — Prove completion:** An ineligible learner is rejected; a valid completion and its recorded certification remain consistent after retry.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagentteaching/README.md), [handlers.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagentteaching/packages/application/src/jobs/handlers.ts), [job-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildagentteaching/packages/application/src/services/job-service.ts).

---

<a id="p020"></a>
### _Organized Desktop/02 Build Projects/buildantigVG

Multi-tenant Employer of Record teaching app; document uploads are simulated metadata updates.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Document upload is currently a simulated metadata update; storage integration is proposed work.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, NestJS, Node.js, React, Vite, Prisma, Docker, Jest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [08-learning-guide-for-junior-to-mid-level-engineers.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildantigVG/docs/08-learning-guide-for-junior-to-mid-level-engineers.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of employee lifecycle, approval and tenant scope, an expected-state example and a guided-to-independent change exercise. Tie it to tenant isolation, approval rules, audit history, module boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace one employee approval and test both cross-tenant access and invalid state changes. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildantigVG/README.md), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildantigVG/apps/web/src/App.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildantigVG/package.json).

---

<a id="p029"></a>
### _Organized Desktop/03 Master Projects/master 6

A enterprise learning management and certification platform built as a TypeScript modular monolith learning codebase.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, TypeScript, Express, Next.js, Node.js, React, Prisma, Redis, Docker, Vitest, BullMQ.
- **Learning content now:** Codebase walkthrough / study pack. Start at [important-files.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master%206/docs/code-walkthroughs/important-files.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of eligibility, progress and completion transitions, an expected-state example and a guided-to-independent change exercise. Tie it to enrollment/progress data, scoped permissions, policy rules, modular services.
- **2 — Improve the project/resource:** First scoped project change: Trace one enrollment-to-completion flow and test an ineligible certification. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an ineligible completion; repeat a valid progress event and verify progress and any certificate/review state remain consistent.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master%206/package.json), [auth.routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master%206/apps/api/src/routes/auth.routes.ts), [server.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master%206/apps/api/src/server.ts).

---

<a id="p030"></a>
### _Organized Desktop/03 Master Projects/master1

GlobalWork is a fictional Employer of Record SaaS platform built as a TypeScript modular monolith.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, NestJS, Next.js, Node.js, React, Prisma, Redis, AWS SDK, Docker, GitHub Actions, Jest, Playwright, Vitest, BullMQ.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master1/docs/code-walkthroughs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of employee lifecycle, approval and tenant scope, an expected-state example and a guided-to-independent change exercise. Tie it to tenant isolation, approval rules, audit history, module boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace one employee approval and test both cross-tenant access and invalid state changes. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master1/README.md), [auth.service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master1/apps/api/src/modules/auth/auth.service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master1/package.json).

---

<a id="p031"></a>
### _Organized Desktop/03 Master Projects/master2

A learning-oriented multi-tenant SaaS billing and subscription platform.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, TypeScript, Express, Node.js, React, Vite, Prisma, Redis, Docker, GitHub Actions, Vitest, BullMQ.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master2/docs/walkthroughs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of money units, state transitions and duplicate deliveries, an expected-state example and a guided-to-independent change exercise. Tie it to money arithmetic, idempotency, webhook processing, transaction boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace a charge or webhook and design a replay test that cannot double-apply it. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master2/README.md), [async-handler.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master2/apps/api/src/shared/async-handler.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master2/apps/web/src/App.tsx).

---

<a id="p032"></a>
### _Organized Desktop/03 Master Projects/master3

TypeScript support/CRM modular-monolith teaching app with demo header-based tenant/user resolution.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: README states x-tenant-slug/x-user-email resolve demo identity; the auth layer is not production authentication.
- **Recorded stack:** CSS, HTML, TypeScript, Express, Node.js, React, Vite, Prisma, Redis, Docker, GitHub Actions, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [important-files.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master3/docs/walkthrough/important-files.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ticket visibility, assignment and service deadlines, an expected-state example and a guided-to-independent change exercise. Tie it to route/service/repository boundaries, permissions, queue filters, workflow rules.
- **2 — Improve the project/resource:** First scoped project change: Trace ticket creation to storage; test forbidden transitions and unauthorized access. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master3/README.md), [health.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master3/apps/api/src/routes/health.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master3/apps/web/src/App.tsx).

---

<a id="p033"></a>
### _Organized Desktop/03 Master Projects/master4

Atlas Fulfillment is a TypeScript operations platform for warehouse and ecommerce inventory, orders, and fulfillment.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, TypeScript, Express, Node.js, React, Vite, Prisma, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [important-files.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master4/docs/walkthroughs/important-files.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to relational modeling, pricing, stock reservations, order state transitions.
- **2 — Improve the project/resource:** First scoped project change: Trace an order/reservation and test invalid transitions or repeated submissions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master4/README.md), [orders.service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master4/src/server/modules/orders/orders.service.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master4/src/App.tsx).

---

<a id="p034"></a>
### _Organized Desktop/03 Master Projects/master7

Teaching codebase for growing a enterprise learning management and certification platform through documented feature slices.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Redis, Docker, Playwright, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master7/docs/code-walkthroughs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of eligibility, progress and completion transitions, an expected-state example and a guided-to-independent change exercise. Tie it to enrollment/progress data, scoped permissions, policy rules, modular services.
- **2 — Improve the project/resource:** First scoped project change: Trace one enrollment-to-completion flow and test an ineligible certification. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an ineligible completion; repeat a valid progress event and verify progress and any certificate/review state remain consistent.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master7/README.md), [services.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master7/apps/api/src/services.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master7/package.json).

---

<a id="p035"></a>
### _Organized Desktop/03 Master Projects/mastercal

The community-driven, open-source scheduling platform.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, PHP, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Redis, Docker, GitHub Actions, Playwright, Vitest, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastercal/cal.diy/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to date/time modeling, interval conflicts, transactional booking, cancellation; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastercal/cal.diy/README.md), [server.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastercal/cal.diy/packages/i18n/server.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastercal/cal.diy/packages/app-store-cli/src/App.tsx).

---

<a id="p036"></a>
### _Organized Desktop/03 Master Projects/masterdidy

Dify LLM application platform with workflow, knowledge-retrieval, and agent components.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, PHP, Python, SQL, TypeScript, FastAPI, Flask, Hono, Next.js, Node.js, React, Tailwind CSS, Vite, MySQL, PostgreSQL, Redis, Supabase, AWS SDK, Docker, GitHub Actions, Playwright, Vitest, pytest, Anthropic API, Celery.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterdidy/dify/fable%20docs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of step state, retries and adapter contracts, an expected-state example and a guided-to-independent change exercise. Tie it to state machines, workers, retry policies, idempotency, execution logs; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterdidy/dify/README.md), [app.py](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterdidy/dify/api/controllers/web/app.py), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterdidy/dify/package.json).

---

<a id="p037"></a>
### _Organized Desktop/03 Master Projects/masterdub

The open-source link attribution platform.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Vite, MySQL, Prisma, Docker, GitHub Actions, Playwright, Vitest, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterdub/dub/fable%20docs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of event identity, aggregation and reporting filters, an expected-state example and a guided-to-independent change exercise. Tie it to event modeling, aggregation, reporting queries, deduplication; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterdub/dub/README.md), [use-click-handlers.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterdub/dub/packages/ui/src/hooks/use-click-handlers.ts), [server.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterdub/dub/apps/web/lib/axiom/server.ts).

---

<a id="p038"></a>
### _Organized Desktop/03 Master Projects/masterfinisc

The open-source secret management platform: Sync secrets/configs across your team/infrastructure and prevent secret leaks.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, Rust, TypeScript, Express, Fastify, Node.js, React, Tailwind CSS, Vite, MongoDB, MySQL, PostgreSQL, Redis, AWS SDK, Docker, GitHub Actions, Vitest, BullMQ, MCP.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterfinisc/infisical/fable-docs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterfinisc/infisical/README.md), [auth-dal.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterfinisc/infisical/backend/src/services/auth/auth-dal.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterfinisc/infisical/package.json).

---

<a id="p039"></a>
### _Organized Desktop/03 Master Projects/masterflag

Flagsmith feature-flag and remote-configuration platform.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, SCSS, SQL, TypeScript, Django, Express, Node.js, React, PostgreSQL, Redis, AWS SDK, Docker, GitHub Actions, Jest, Playwright, pytest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterflag/flagsmith/fable%20docs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of deterministic targeting and configuration versions, an expected-state example and a guided-to-independent change exercise. Tie it to rule evaluation, rollout consistency, cache invalidation, audit history; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Evaluate fixed subjects repeatedly across two environments; verify stable assignments, environment isolation and an explicit rollback result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterflag/flagsmith/README.md), [useRole.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterflag/flagsmith/frontend/common/services/useRole.ts), [Dockerfile](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterflag/flagsmith/Dockerfile).

---

<a id="p040"></a>
### _Organized Desktop/03 Master Projects/masterform

Formbricks survey and experience-management platform.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Vite, Prisma, Redis, AWS SDK, Azure SDK, Docker, GitHub Actions, Playwright, Vitest, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterform/formbricks/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of schema versions and response validation, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing; reading established code and bounded contributions. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Validate against a published schema; reject foreign, hidden-invalid or outdated inputs without partially saving a response.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterform/formbricks/README.md), [service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterform/formbricks/packages/cache/src/service.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterform/formbricks/apps/storybook/src/App.tsx).

---

<a id="p041"></a>
### _Organized Desktop/03 Master Projects/masterhop

Open Source API Development Ecosystem

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Recorded stack:** Go, HTML, JavaScript, Rust, SCSS, SQL, TypeScript, Vue, Express, NestJS, Node.js, Tailwind CSS, Vite, PostgreSQL, Prisma, Docker, GitHub Actions, Jest, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterhop/hoppscotch/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterhop/hoppscotch/README.md), [App.vue](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterhop/hoppscotch/packages/hoppscotch-agent/src/App.vue), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterhop/hoppscotch/package.json).

---

<a id="p042"></a>
### _Organized Desktop/03 Master Projects/masteridur

Open Source ERP / CRM Accounting Invoice Quote

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Express, Node.js, React, Vite, MongoDB, AWS SDK, GitHub Actions, OpenAI API.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteridur/idurar-erp-crm/fable%20docs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of money units, state transitions and duplicate deliveries, an expected-state example and a guided-to-independent change exercise. Tie it to relational data, lifecycle transitions, tenant-scoped queries, audit history; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteridur/idurar-erp-crm/README.md), [routes.jsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteridur/idurar-erp-crm/frontend/src/router/routes.jsx), [server.js](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteridur/idurar-erp-crm/backend/src/server.js).

---

<a id="p043"></a>
### _Organized Desktop/03 Master Projects/masterindicoPYJS

Indico event and conference management platform.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, SCSS, TypeScript, Flask, React, PostgreSQL, Redis, SQLAlchemy, GitHub Actions, Jest, Celery.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterindicoPYJS/indico/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach code navigation, contracts, validation, testing; reading established code and bounded contributions with a separate answer and rubric. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterindicoPYJS/indico/README.md), [controllers.py](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterindicoPYJS/indico/indico/modules/api/controllers.py), [app.py](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterindicoPYJS/indico/indico/web/flask/app.py).

---

<a id="p044"></a>
### _Organized Desktop/03 Master Projects/masterlink

Linkwarden bookmark collection and webpage-archiving reference application.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Expo, Next.js, Node.js, React, React Native, Tailwind CSS, Prisma, AWS SDK, Docker, GitHub Actions, Jest, Playwright, Vitest, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterlink/linkwarden/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterlink/linkwarden/README.md), [getUsers.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterlink/linkwarden/apps/web/lib/api/controllers/users/getUsers.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterlink/linkwarden/package.json).

---

<a id="p045"></a>
### _Organized Desktop/03 Master Projects/mastermatter

Mattermost team messaging and collaboration platform.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, Go, HTML, JavaScript, SCSS, SQL, TypeScript, Express, Node.js, React, PostgreSQL, Redis, AWS SDK, Docker, GitHub Actions, Cypress, Jest, Playwright.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermatter/mattermost/docs/mission-learning-path/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for membership, event identity and reconnect behavior; make learners predict state before running it. Teach event/state modeling, real-time synchronization, validation, reconnect behavior; reading established code and bounded contributions with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermatter/mattermost/README.md), [main.go](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermatter/mattermost/api/server/main.go), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermatter/mattermost/api/package.json).

---

<a id="p046"></a>
### _Organized Desktop/03 Master Projects/mastermayan

Mayan EDMS is a document management system.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, Redis, Docker, Celery.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermayan/Mayan-EDMS/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to file validation, access control, asynchronous processing, retries; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermayan/Mayan-EDMS/README.md), [handlers.py](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermayan/Mayan-EDMS/mayan/apps/ocr/handlers.py), [requirements.txt](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermayan/Mayan-EDMS/requirements.txt).

---

<a id="p047"></a>
### _Organized Desktop/03 Master Projects/mastermorphic

An AI-powered search engine with a generative UI.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Drizzle, Redis, Supabase, AWS SDK, Docker, GitHub Actions, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermorphic/morphic/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of tool or retrieval boundaries and explicit failure behavior, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Use a fixed local fixture and mocked external responses; record expected output, an unavailable-tool case and a scored regression example.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermorphic/morphic/README.md), [keyboard-shortcut-handler.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermorphic/morphic/components/keyboard-shortcut-handler.tsx), [server.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastermorphic/morphic/lib/supabase/server.ts).

---

<a id="p048"></a>
### _Organized Desktop/03 Master Projects/masternext

NextCRM is an open-source CRM built with Next.js 16, React 19, TypeScript, PostgreSQL (Prisma 7), and shadcn/ui.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, MongoDB, PostgreSQL, Prisma, AWS SDK, Docker, GitHub Actions, Jest, Playwright, MCP, OpenAI API.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masternext/nextcrm-app/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, ordering and lifecycle transitions, an expected-state example and a guided-to-independent change exercise. Tie it to relational data, lifecycle transitions, tenant-scoped queries, audit history; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masternext/nextcrm-app/README.md), [nav-user.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masternext/nextcrm-app/app/%5Blocale%5D/%28routes%29/components/nav-user.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masternext/nextcrm-app/package.json).

---

<a id="p049"></a>
### _Organized Desktop/03 Master Projects/masternovu

Novu notification infrastructure and in-app inbox platform.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, SQL, TypeScript, Express, NestJS, Next.js, Node.js, React, Tailwind CSS, Vite, MongoDB, Redis, AWS SDK, Azure SDK, Docker, GitHub Actions, Jest, Playwright, Vitest, BullMQ, Socket.IO.
- **Learning content now:** Codebase walkthrough / study pack. Start at [05-codebase-health.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masternovu/novu/docs/onboarding/senior/05-codebase-health.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masternovu/novu/README.md), [auth.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masternovu/novu/apps/dashboard/src/routes/auth.tsx), [user.service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masternovu/novu/playground/nestjs/src/user.service.ts).

---

<a id="p050"></a>
### _Organized Desktop/03 Master Projects/masteropen

The open-source status page and uptime monitoring platform.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, Go, JavaScript, SQL, TypeScript, Astro, Hono, Next.js, Node.js, React, Tailwind CSS, Drizzle, AWS SDK, Docker, GitHub Actions, Playwright, MCP, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteropen/openstatus/fabledocs3/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of event identity, aggregation and reporting filters, an expected-state example and a guided-to-independent change exercise. Tie it to event schemas, ingestion, aggregation, alerting, operational failure states; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Multiple Fable sets are listed; a higher suffix is not proof of a better starting point.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteropen/openstatus/README.md), [server.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteropen/openstatus/apps/server/src/routes/mcp/server.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteropen/openstatus/package.json).

---

<a id="p051"></a>
### _Organized Desktop/03 Master Projects/masteropenedxPYJS

Purpose The Open edX Platform enables the authoring and delivery of online learning at any scale.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, SCSS, TypeScript, Django, React, GitHub Actions, Jest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteropenedxPYJS/openedx-platform/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach code navigation, contracts, validation, testing; reading established code and bounded contributions with a separate answer and rubric. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Source-review evidence:** [README.rst](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteropenedxPYJS/openedx-platform/README.rst), [services.py](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteropenedxPYJS/openedx-platform/xmodule/services.py), [user_service.py](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masteropenedxPYJS/openedx-platform/common/djangoapps/xblock_django/user_service.py).

---

<a id="p052"></a>
### _Organized Desktop/03 Master Projects/masterpaper

Paperless-ngx is a document management system that transforms your physical documents into a searchable online archive so you can keep, well, less paper.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, SCSS, TypeScript, Angular, Django, Tailwind CSS, MySQL, PostgreSQL, Redis, Docker, GitHub Actions, Jest, Playwright, Celery, OpenAI API.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpaper/paperless-ngx/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to file validation, access control, asynchronous processing, retries; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpaper/paperless-ngx/README.md), [chat.service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpaper/paperless-ngx/src-ui/src/app/services/chat.service.ts), [Dockerfile](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpaper/paperless-ngx/Dockerfile).

---

<a id="p053"></a>
### _Organized Desktop/03 Master Projects/masterplane

Modern project management for all teams

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, TypeScript, Express, Node.js, React, Vite, Redis, Docker, GitHub Actions, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterplane/plane/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, ordering and lifecycle transitions, an expected-state example and a guided-to-independent change exercise. Tie it to relational CRUD, ordering, optimistic UI, project permissions; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterplane/plane/README.md), [user.service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterplane/plane/apps/live/src/services/user.service.ts), [server.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterplane/plane/apps/live/src/server.ts).

---

<a id="p054"></a>
### _Organized Desktop/03 Master Projects/masterpload

Payload TypeScript CMS and application framework.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SCSS, TypeScript, Express, Next.js, Node.js, React, Tailwind CSS, Drizzle, MongoDB, PostgreSQL, SQLite, AWS SDK, Azure SDK, Docker, GitHub Actions, Playwright, Vitest, MCP.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpload/payload/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of tree structure, revisions and inherited permissions, an expected-state example and a guided-to-independent change exercise. Tie it to content modeling, revisions, authorization, search, optimistic concurrency; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpload/payload/README.md), [index.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpload/payload/packages/next/src/routes/index.ts), [confirmOrder.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpload/payload/packages/plugin-ecommerce/src/endpoints/confirmOrder.ts).

---

<a id="p055"></a>
### _Organized Desktop/03 Master Projects/masterpostiz

Postiz social-media scheduling and publishing application.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SCSS, TypeScript, NestJS, Next.js, Node.js, React, Tailwind CSS, Vite, Prisma, Redis, AWS SDK, Docker, GitHub Actions, Jest, Vitest, MCP, OpenAI API, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpostiz/postiz-app/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to date/time modeling, interval conflicts, transactional booking, cancellation; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpostiz/postiz-app/README.md), [auth.service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpostiz/postiz-app/libraries/helpers/src/auth/auth.service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpostiz/postiz-app/package.json).

---

<a id="p056"></a>
### _Organized Desktop/03 Master Projects/masterpre

pretalx conference proposal, speaker, and schedule management.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, Vue, Django, Vite, Redis, GitHub Actions, pytest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpre/pretalx/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to date/time modeling, interval conflicts, transactional booking, cancellation; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.rst](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpre/pretalx/README.rst), [auth.py](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpre/pretalx/src/pretalx/api/auth.py), [App.vue](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterpre/pretalx/src/pretalx/frontend/schedule/src/App.vue).

---

<a id="p058"></a>
### _Organized Desktop/03 Master Projects/mastersaleorPY

Commerce that works with your language and stack

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** HTML, Python, Django, PostgreSQL, Redis, Docker, GitHub Actions, pytest, Celery, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastersaleorPY/saleor/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to relational modeling, pricing, stock reservations, order state transitions; reading established code and bounded contributions. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastersaleorPY/saleor/README.md), [asgi_handler.py](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastersaleorPY/saleor/saleor/asgi/asgi_handler.py), [app.py](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastersaleorPY/saleor/saleor/graphql/app/dataloaders/app.py).

---

<a id="p059"></a>
### _Organized Desktop/03 Master Projects/mastershadcn

A set of components that you can customize, extend, and build on.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Astro, Next.js, Node.js, React, Tailwind CSS, Vite, GitHub Actions, Vitest, MCP.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastershadcn/ui/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastershadcn/ui/README.md), [routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastershadcn/ui/templates/react-router-app/app/routes.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastershadcn/ui/templates/vite-app/src/App.tsx).

---

<a id="p060"></a>
### _Organized Desktop/03 Master Projects/MasterStore

A , headless ecommerce storefront for Spree Commerce, built with Next.js 16, React 19, and the Spree REST API.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, GitHub Actions, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/MasterStore/storefront/docs/mission-learning-path/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for availability and local-time conversion; make learners predict state before running it. Teach relational modeling, pricing, stock reservations, order state transitions; reading established code and bounded contributions with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/MasterStore/storefront/README.md), [handlers.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/MasterStore/storefront/src/lib/webhooks/handlers.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/MasterStore/storefront/package.json).

---

<a id="p061"></a>
### _Organized Desktop/03 Master Projects/mastersupa

Supabase is the Postgres development platform.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, Dart, HTML, JavaScript, Kotlin, SQL, TypeScript, Vue, Next.js, Node.js, Nuxt, React, Tailwind CSS, Vite, Supabase, AWS SDK, Docker, GitHub Actions, Playwright, Vitest, MCP, OpenAI API, Twilio.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastersupa/supabase/docs-codex-learning/react-typescript-next-tutorial/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastersupa/supabase/README.md), [routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastersupa/supabase/apps/lite-studio/app/routes.ts), [server.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastersupa/supabase/apps/ui-library/registry/default/clients/nextjs/lib/supabase/server.ts).

---

<a id="p062"></a>
### _Organized Desktop/03 Master Projects/mastertea

Manage Your Data & Connect Your Team Teable uses a simple, spreadsheet-like interface to create database applications.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Express, NestJS, Next.js, Node.js, React, Tailwind CSS, PostgreSQL, Prisma, Redis, AWS SDK, GitHub Actions, Playwright, Vitest, BullMQ.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertea/teable/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertea/teable/README.md), [UserLookupService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertea/teable/packages/v2/core/src/ports/UserLookupService.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertea/teable/apps/nextjs-app/src/features/app/blocks/App.tsx).

---

<a id="p063"></a>
### _Organized Desktop/03 Master Projects/mastertool

ToolJet is the open-source foundation of ToolJet AI - the AI-native platform for building and deploying internal tools, workflows and AI agents.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SCSS, TypeScript, NestJS, Node.js, React, Tailwind CSS, PostgreSQL, Redis, Docker, GitHub Actions, Terraform, Cypress, Jest, Anthropic API, BullMQ, Stripe.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertool/tooljet/docs2/mission-learning-path/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for step state, retries and adapter contracts; make learners predict state before running it. Teach state machines, workers, retry policies, idempotency, execution logs; reading established code and bounded contributions with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertool/tooljet/README.md), [AuthRoute.jsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertool/tooljet/frontend/src/Routes/AuthRoute.jsx), [App.jsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertool/tooljet/frontend/src/App/App.jsx).

---

<a id="p064"></a>
### _Organized Desktop/03 Master Projects/mastertwenty

Twenty open-source CRM with customer records, workflows, and team views.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, SQL, TypeScript, Electron, Express, Node.js, React, Vite, GitHub Actions, Terraform, Jest, Playwright, Vitest, Anthropic API, OpenAI API.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertwenty/twenty/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of step state, retries and adapter contracts, an expected-state example and a guided-to-independent change exercise. Tie it to state machines, workers, retry policies, idempotency, execution logs; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Multiple Fable sets are listed; a higher suffix is not proof of a better starting point.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertwenty/twenty/README.md), [AuthService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertwenty/twenty/packages/twenty-front/src/modules/auth/services/AuthService.ts), [server.js](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertwenty/twenty/packages/twenty-companion/src/server.js).

---

<a id="p065"></a>
### _Organized Desktop/03 Master Projects/mastertypebot

Typebot is a Fair Source chatbot builder.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, PHP, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Vite, Prisma, Redis, Docker, GitHub Actions, Playwright, OpenAI API, Stripe.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertypebot/typebot.io/docs/mission-learning-path/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for membership, event identity and reconnect behavior; make learners predict state before running it. Teach external API boundaries, streaming, deterministic evaluation, retries, human review; reading established code and bounded contributions with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertypebot/typebot.io/README.md), [index.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertypebot/typebot.io/apps/landing-page/src/routes/index.tsx), [getUsersHandler.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/mastertypebot/typebot.io/packages/forge/blocks/blink/src/handlers/getUsersHandler.ts).

---

<a id="p066"></a>
### _Organized Desktop/03 Master Projects/masterumami

Umami is a simple, fast, privacy-focused alternative to Google Analytics.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, PostgreSQL, Prisma, Redis, Docker, GitHub Actions, Cypress, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterumami/umami/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of event identity, aggregation and reporting filters, an expected-state example and a guided-to-independent change exercise. Tie it to event modeling, aggregation, reporting queries, deduplication; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterumami/umami/README.md), [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterumami/umami/src/lib/auth.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterumami/umami/src/app/%28main%29/App.tsx).

---

<a id="p067"></a>
### _Organized Desktop/03 Master Projects/masterzulipPY

Zulip is an open-source organized team chat app with unique [topic-based threading][why-zulip] that combines the best of email and chat to make remote work productive and delightful.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, Ruby, SQL, TypeScript, Astro, Django, Vite, Firebase, MongoDB, PostgreSQL, Redis, SQLAlchemy, AWS SDK, Docker, GitHub Actions, OpenAI API, Stripe.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterzulipPY/zulip/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for membership, event identity and reconnect behavior; make learners predict state before running it. Teach event/state modeling, real-time synchronization, validation, reconnect behavior; reading established code and bounded contributions with a separate answer and rubric. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterzulipPY/zulip/README.md), [click_handlers.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterzulipPY/zulip/web/src/click_handlers.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterzulipPY/zulip/package.json).

---

<a id="p080"></a>
### _Organized Desktop/04 JavaScript Training/reactbullet

A simple, scalable, and architecture for building production ready React applications.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Next.js, Node.js, React, Tailwind CSS, Vite, GitHub Actions, Playwright, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/reactbullet/bulletproof-react/fable-docs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing; reading established code and bounded contributions.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/reactbullet/bulletproof-react/README.md), [landing.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/reactbullet/bulletproof-react/apps/react-vite/src/app/routes/landing.tsx), [users.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/reactbullet/bulletproof-react/apps/react-vite/src/app/routes/app/users.tsx).

---

<a id="p095"></a>
### _Organized Desktop/05 Numbered Experiments/e20

Modular ERP MVP foundation for small-to-mid-sized businesses, built as a TypeScript/Fastify API with a shared master-data and document engine.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Teaching app with documented in-memory/mock persistence; database/schema claims do not establish durable storage. Runtime unverified. Limits: README explicitly says the in-memory store resets when the server restarts.
- **Recorded stack:** TypeScript, Fastify, Node.js, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e20/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to ERP domain modeling, document lifecycle, module contracts, transaction boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e20/README.md), [erp-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e20/src/domain/erp-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e20/package.json).

---

<a id="p106"></a>
### _Organized Desktop/05 Numbered Experiments/rn1

Bluesky social-app source workspace, including mobile/web client components.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, Go, HTML, JavaScript, Kotlin, Swift, TypeScript, Expo, Express, Node.js, React, React Native, Tailwind CSS, Vite, PostgreSQL, Redis, Docker, GitHub Actions, Jest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/rn1/social-app/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting code navigation, contracts, validation, testing; reading established code and bounded contributions. Keep proposed architecture separate. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/rn1/social-app/README.md), [routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/rn1/social-app/src/routes.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/rn1/social-app/package.json).

---

<a id="p107"></a>
### _Organized Desktop/05 Numbered Experiments/w21

PulseGate is a Next.js full-stack control plane and gateway runtime.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w21/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting API contracts, versioning, caching, indexing, service boundaries.
- **2 — Improve the project/resource:** First scoped project change: Follow one request across its boundary and test backward compatibility or cache invalidation. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w21/docs/architecture/README.md), [page.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w21/src/app/routes/page.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w21/package.json).

---

<a id="p109"></a>
### _Organized Desktop/05 Numbered Experiments/w23

Multi-tenant search and indexing system built with Next.js, TypeScript, Drizzle, PostgreSQL, Zod, and React Query.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Drizzle, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w23/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting API contracts, versioning, caching, indexing, service boundaries.
- **2 — Improve the project/resource:** First scoped project change: Follow one request across its boundary and test backward compatibility or cache invalidation. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w23/docs/architecture/README.md), [searchService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w23/src/services/searchService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w23/package.json).

---

<a id="p124"></a>
### _Organized Desktop/05 Numbered Experiments/ww27

Learning app for evolving a public REST API over time without freezing the system in place.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww27/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting API contracts, versioning, caching, indexing, service boundaries.
- **2 — Improve the project/resource:** First scoped project change: Follow one request across its boundary and test backward compatibility or cache invalidation. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww27/docs/architecture/README.md), [api-version-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww27/src/services/api-version-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww27/package.json).

---

<a id="p127"></a>
### _Organized Desktop/05 Numbered Experiments/ww3

Next.js + React + TypeScript learning build for employer-of-record operations.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww3/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of employee lifecycle, approval and tenant scope: ordered source files, one input-to-state trace, a diagram and one independent change targeting tenant isolation, approval rules, audit history, module boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace one employee approval and test both cross-tenant access and invalid state changes. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww3/docs/architecture/README.md), [jobService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww3/src/services/jobService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww3/package.json).

---

<a id="p179"></a>
### _Organized Desktop/07 Anti Projects/antitestbuild

GlobalWorkforce OS is a secure, multi-tenant Employer of Record (EOR) operations platform designed as a modular monolith.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, TypeScript, NestJS, Node.js, React, Vite, Prisma, Docker, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [08-learning-guide-for-junior-to-mid-level-engineers.md](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antitestbuild/docs/08-learning-guide-for-junior-to-mid-level-engineers.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of employee lifecycle, approval and tenant scope, an expected-state example and a guided-to-independent change exercise. Tie it to tenant isolation, workforce workflows, modular-monolith boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace one cross-module employee workflow and test cross-tenant isolation. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antitestbuild/README.md), [api.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antitestbuild/apps/web/src/services/api.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antitestbuild/apps/web/src/App.tsx).

---

<a id="p189"></a>
### _Organized Desktop/09 Grav And VG Projects/grav1pretalx

pretalx conference proposal, speaker, and schedule management.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, Vue, Django, Vite, Redis, GitHub Actions, pytest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/grav1pretalx/pretalx/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to Django domain modeling, proposal workflows, scheduling, established code navigation.
- **2 — Improve the project/resource:** First scoped project change: Compare its local contents with masterpre, then choose one bounded pretalx feature to trace. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.rst](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/grav1pretalx/pretalx/README.rst), [auth.py](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/grav1pretalx/pretalx/src/pretalx/api/auth.py), [App.vue](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/grav1pretalx/pretalx/src/pretalx/frontend/schedule/src/App.vue).

---

<a id="p190"></a>
### _Organized Desktop/09 Grav And VG Projects/graveopenjspy

OpenSlides is a free, web based presentation and assembly system for managing and projecting agenda, motions and elections of an assembly.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, Go, HTML, JavaScript, Python, SCSS, SQL, TypeScript, Docker, GitHub Actions.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/graveopenjspy/OpenSlides/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to assembly workflows, distributed service boundaries, permissions, event updates.
- **2 — Improve the project/resource:** First scoped project change: Trace one motion or vote across its API, data, authorization, and tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/graveopenjspy/OpenSlides/README.md), [main.go](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/graveopenjspy/OpenSlides/openslides-icc-service/main.go), [main.go](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/graveopenjspy/OpenSlides/openslides-manage-service/cmd/server/main.go).

---

<a id="p191"></a>
### _Organized Desktop/09 Grav And VG Projects/gravreviewboardjspy

Review Board is an open source, web-based code and document review tool built to help companies, open source projects, and other organizations keep their quality high and their bug count low.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** C, C++, CSS, HTML, JavaScript, Python, SQL, TypeScript, Django, MySQL, PostgreSQL, Docker.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/gravreviewboardjspy/reviewboard/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Django review workflows, diffs, access policy, extension points.
- **2 — Improve the project/resource:** First scoped project change: Trace a review-request change and select one narrow bug or test contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.rst](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/gravreviewboardjspy/reviewboard/README.rst), [services.py](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/gravreviewboardjspy/reviewboard/reviewboard/avatars/services.py), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/gravreviewboardjspy/reviewboard/package.json).

---

<a id="p192"></a>
### _Organized Desktop/09 Grav And VG Projects/vg

Employer-of-record (EOR) platform MVP built with Next.js, Node.js, and PostgreSQL.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Redis, Docker, BullMQ, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/vg/fable/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of employee lifecycle, approval and tenant scope, an expected-state example and a guided-to-independent change exercise. Tie it to multi-tenant workforce modeling, scoped APIs, approval workflows.
- **2 — Improve the project/resource:** First scoped project change: Trace one employee approval and test cross-tenant access denial. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/vg/README.md), [context.js](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/vg/src/services/context.js), [auth.service.js](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/vg/src/services/auth.service.js).

---

<a id="p193"></a>
### _Organized Desktop/09 Grav And VG Projects/VGdemo

This folder is a structured code review of the globalhire-lite codebase, written with a specific goal: take a junior software engineer and pull them toward mid/senior level for CRUD web-app development jobs.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** C#, CSS, HTML, JavaScript, TypeScript, ASP.NET Core, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Vitest, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/VGdemo/fable/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code-review practice, CRUD architecture, data/auth boundaries.
- **2 — Improve the project/resource:** First scoped project change: Follow the structured globalhire-lite review and implement one small finding in an isolated copy later. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/VGdemo/fable/README.md), [auth.routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/VGdemo/globalhire-lite/apps/api/src/modules/auth/auth.routes.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/VGdemo/globalhire-lite/apps/web/src/App.tsx).

---

<a id="p196"></a>
### _Organized Desktop/12 Other Projects/andie

Shopify-related scripting workspace, including a metaobject population utility.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** JavaScript.
- **Learning content now:** No substantive guide verified. No populated entrypoint verified in the tutorial review.
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting Shopify API scripting, data transformations, integration validation. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Inspect the metaobject utility inputs and design a dry-run plus idempotent update strategy. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [main.js](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/andie/.storybook/main.js).

---

<a id="p206"></a>
### _Organized Desktop/12 Other Projects/pp8

This repository recreates a unified HR platform in a Python-first stack so its backend architecture can be compared over time with a TypeScript-first version.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, Python, TypeScript, FastAPI, Next.js, Node.js, React, Tailwind CSS, PostgreSQL, SQLAlchemy, Docker, pytest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/pp8/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting Python-first HR architecture, service boundaries, comparison with TypeScript.
- **2 — Improve the project/resource:** First scoped project change: Trace one HR use case and compare its validation/auth/data boundaries with the TypeScript version. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/pp8/README.md), [main.py](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/pp8/backend/app/main.py), [docker-compose.yml](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/pp8/docker-compose.yml).

---

<a id="p207"></a>
### _Organized Desktop/12 Other Projects/pyhealth

Healthchecks is a cron job monitoring service.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: A tested full-stack app plus workflow/reliability practice; module boundaries and operations.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, Python, Django, PostgreSQL, Docker, GitHub Actions.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/pyhealth/healthchecks/docs/mission-learning-path/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Django scheduled-job monitoring, alert state, operations, established code reading with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace one incoming ping into check state and alert processing; select one bounded test or fix. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/pyhealth/healthchecks/README.md), [apps.py](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/pyhealth/healthchecks/hc/api/apps.py), [requirements.txt](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/pyhealth/healthchecks/requirements.txt).

---

<a id="p217"></a>
### astra1

A persistent station and enterprise operations simulation for practicing AI-assisted engineering.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Broad operations simulation with app and test code; simulated providers remain simulations. Static review only; not built, tested or run.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, PostgreSQL, Docker, GitHub Actions, Playwright.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/astra1/upskilling/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Operational workflows, telemetry, durable jobs, failure recovery with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Finish one incident-to-remediation slice and explain failure recovery. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/astra1/README.md), [instrumentation.ts](C:/Users/Owner/Desktop/astra1/src/instrumentation.ts), [package.json](C:/Users/Owner/Desktop/astra1/package.json).

---

<a id="p224"></a>
### buildevent

TypeScript monorepo for a ticketing platform with a Next.js frontend, Fastify API, Prisma/PostgreSQL data layer, Redis-backed jobs, Stripe checkout hooks, signed QR tickets, and mobile check-in.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Full-stack source with external service seams; only one cataloged test file, no integration runtime verification. Static review only; not built, tested or run.
- **Recorded stack:** CSS, JavaScript, TypeScript, Fastify, Next.js, Node.js, React, Tailwind CSS, Prisma, Redis, Docker, GitHub Actions, Vitest, BullMQ, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/buildevent/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of stock ownership, checkout and order transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Ticket inventory, checkout hooks, queues, signed QR check-in.
- **2 — Improve the project/resource:** First scoped project change: Test duplicate checkout and repeat check-in behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Buildevent](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildevent). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/buildevent/README.md), [server.ts](C:/Users/Owner/Desktop/buildevent/apps/api/src/server.ts), [package.json](C:/Users/Owner/Desktop/buildevent/package.json).

---

<a id="p225"></a>
### buildreviewer

A web-based code-review workspace for GitHub pull requests, inspired by ReviewFlow.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** NestJS/React review workspace with tests; GitHub publication integration unverified. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, NestJS, Node.js, React, Tailwind CSS, Vite, Prisma, Jest, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/buildreviewer/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting GitHub APIs, local drafts, transactional publishing, review UX.
- **2 — Improve the project/resource:** First scoped project change: Trace local draft persistence and implement a failed-publish recovery case. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Buildreviewer](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildreviewer). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/buildreviewer/README.md), [Review.tsx](C:/Users/Owner/Desktop/buildreviewer/apps/web/src/routes/Review.tsx), [package.json](C:/Users/Owner/Desktop/buildreviewer/package.json).

---

<a id="p241"></a>
### geminiorganized/General_.Architectureproject

Full Modular Monolith .NET application with Domain-Driven Design approach.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Teaching/reference workspace; runtime not verified.
- **Recorded stack:** C#, HTML, SQL, ASP.NET Core, SQL Server, Docker, GitHub Actions.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_.Architectureproject/modular-monolith-with-ddd/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting DDD boundaries, domain events, modular monoliths. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace one meeting command across module boundaries and explain its transaction. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [.netarchitectureproject](C:/Users/Owner/Desktop/.netarchitectureproject). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_.Architectureproject/modular-monolith-with-ddd/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_.Architectureproject/modular-monolith-with-ddd/docs/catalog-of-terms/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/General_.Architectureproject/modular-monolith-with-ddd/docker-compose.yml).

---

<a id="p242"></a>
### geminiorganized/General_.Open2

Orchard Core is an open-source, modular, multi-tenant application framework and CMS for ASP.NET Core.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** C#, CSS, HTML, JavaScript, Razor, SCSS, TypeScript, ASP.NET Core, Vite, Vue, Docker, GitHub Actions, Moq, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_.Open2/OrchardCore/fabledocs/upskill/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of content validation, publication and access boundaries, an expected-state example and a guided-to-independent change exercise. Tie it to Extensible CMS, tenants, dependency injection, mature code navigation.
- **2 — Improve the project/resource:** First scoped project change: Study one small module and propose one bounded fix. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an unauthorized publish or invalid content payload; verify one permitted publication is rendered as intended.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [.netopen2](C:/Users/Owner/Desktop/.netopen2). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_.Open2/OrchardCore/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_.Open2/OrchardCore/src/docs/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_.Open2/OrchardCore/package.json).

---

<a id="p250"></a>
### geminiorganized/General_Cleanarch

ASP.NET Core Clean Architecture starter/reference application.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** C#, HTML, JavaScript, SCSS, TypeScript, ASP.NET Core, Entity Framework Core, PostgreSQL, SQL Server, SQLite, GitHub Actions, Moq, NUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Cleanarch/CleanArchitecture/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Dependency boundaries, CQRS, integration testing, architecture tradeoffs..
- **2 — Improve the project/resource:** First scoped project change: Compare one simple endpoint and handler against your own completed CRUD app; adopt only a justified pattern. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Multiple Fable sets are listed; a higher suffix is not proof of a better starting point.
- **Related locations to compare:** [netcleanarch](C:/Users/Owner/Desktop/netcleanarch). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Cleanarch/CleanArchitecture/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Cleanarch/CleanArchitecture/fabledocs/README.md), [AppHost.csproj](C:/Users/Owner/Desktop/geminiorganized/General_Cleanarch/CleanArchitecture/src/AppHost/AppHost.csproj).

---

<a id="p257"></a>
### geminiorganized/General_Gitvg

Relay workflow-automation teaching platform with triggers, actions, connectors, and execution-engine exercises.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** C#, CSS, HTML, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Vite, Prisma, Redis, Docker, GitHub Actions, Playwright, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [LEARNER-GUIDE.md](C:/Users/Owner/Desktop/geminiorganized/General_Gitvg/agora/LEARNER-GUIDE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of step state, retries and adapter contracts, an expected-state example and a guided-to-independent change exercise. Tie it to Workflow engines, connectors, retries, durable execution.
- **2 — Improve the project/resource:** First scoped project change: Trace one failed workflow step and prove retry behavior is bounded. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [gitvg/relay](C:/Users/Owner/Desktop/gitvg/relay). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Gitvg/relay/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Gitvg/pulse/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Gitvg/bazaar/package.json).

---

<a id="p261"></a>
### geminiorganized/General_Masternocu

NocoBase extensible low-code application platform.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Static sample does not establish runtime readiness.
- **Recorded stack:** CSS, HTML, JavaScript, SCSS, SQL, TypeScript, React, MySQL, PostgreSQL, Docker, GitHub Actions, Vitest, LangChain.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Masternocu/nocobase/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Plugin architecture, schemas, permissions, large codebases. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Study one small plugin after owning a full-stack app. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [masternocu](C:/Users/Owner/Desktop/masternocu). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Masternocu/nocobase/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Masternocu/nocobase/docs/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Masternocu/nocobase/package.json).

---

<a id="p265"></a>
### geminiorganized/General_Missioncontrol

A self-hosted control plane for fleets of AI agents — a C# / .NET 10 recreation of builderz-labs/mission-control per the Fleet Command — C# / .NET Technical Specification.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** C#, CSS, Razor, ASP.NET Core, Entity Framework Core, SQLite, xUnit.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Missioncontrol/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of ownership, ordering and lifecycle transitions, known stubs and one exercise targeting Agent control-plane APIs, auth, EF Core, scheduling. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace task claim concurrency and test two workers claiming one task. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [missioncontrol](C:/Users/Owner/Desktop/missioncontrol). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Missioncontrol/README.md), [FleetCommand.Contracts.csproj](C:/Users/Owner/Desktop/geminiorganized/General_Missioncontrol/src/FleetCommand.Contracts/FleetCommand.Contracts.csproj), [FleetCommand.Domain.csproj](C:/Users/Owner/Desktop/geminiorganized/General_Missioncontrol/src/FleetCommand.Domain/FleetCommand.Domain.csproj).

---

<a id="p270"></a>
### geminiorganized/General_Nopsolutions

nopCommerce ecommerce application with storefront, administration, and plugins.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** C#, CSS, HTML, JavaScript, Razor, SQL, Express, PostgreSQL, SQL Server, Docker, GitHub Actions.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Nopsolutions/nopCommerce/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of stock ownership, checkout and order transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Large modular commerce application, plugin boundaries and order lifecycle..
- **2 — Improve the project/resource:** First scoped project change: Trace a single order service method and its callers/tests; compare it with the smaller netshop domain. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [nopsolutionsnet](C:/Users/Owner/Desktop/nopsolutionsnet). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Nopsolutions/nopCommerce/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Nopsolutions/nopCommerce/fabledocs/README.md), [Dockerfile](C:/Users/Owner/Desktop/geminiorganized/General_Nopsolutions/nopCommerce/Dockerfile).

---

<a id="p271"></a>
### geminiorganized/General_Open1

A reference .NET application implementing an e-commerce website using a services-based architecture using .NET Aspire.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** C#, CSS, HTML, JavaScript, Razor, TypeScript, ASP.NET Core, Blazor, Entity Framework Core, PostgreSQL, GitHub Actions, Playwright.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Open1/eShop/fabledoc2/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of stock ownership, checkout and order transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Service boundaries, distributed workflows, integration events and observability..
- **2 — Improve the project/resource:** First scoped project change: Follow checkout across services and diagram failure/retry boundaries after completing a monolith first. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Multiple Fable sets are listed; a higher suffix is not proof of a better starting point.
- **Related locations to compare:** [netopen1](C:/Users/Owner/Desktop/netopen1). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Open1/eShop/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Open1/eShop/tests/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Open1/eShop/package.json).

---

<a id="p272"></a>
### geminiorganized/General_Open3

Umbraco content management system and its administration interface.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Static sample does not establish runtime readiness.
- **Recorded stack:** C#, TypeScript, JavaScript, ASP.NET Core, Umbraco CMS, U, p, s, t, r, e, a, m,  , C, M, S, f, n, c, ;, o, d, l, i, g, ..
- **Learning content now:** Developer explanation / brief orientation. Start at [architecture.md](C:/Users/Owner/Desktop/geminiorganized/General_Open3/Umbraco-CMS/src/Umbraco.Web.UI.Client/docs/architecture.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting Large-repo navigation, extension architecture, management APIs, content caching and testing..
- **2 — Improve the project/resource:** First scoped project change: Select one management endpoint or backoffice component and trace its tests; scope a small contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [netopen3](C:/Users/Owner/Desktop/netopen3). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Open3/Umbraco-CMS/.github/README.md), [readme.md](C:/Users/Owner/Desktop/geminiorganized/General_Open3/Umbraco-CMS/templates/readme.md), [Dockerfile](C:/Users/Owner/Desktop/geminiorganized/General_Open3/Umbraco-CMS/.devcontainer/Dockerfile).

---

<a id="p285"></a>
### geminiorganized/LLM_Generated_Buildevent

TypeScript monorepo for a ticketing platform with a Next.js frontend, Fastify API, Prisma/PostgreSQL data layer, Redis-backed jobs, Stripe checkout hooks, signed QR tickets, and mobile check-in.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Fastify, Next.js, Node.js, React, Tailwind CSS, Prisma, Redis, Docker, GitHub Actions, Vitest, BullMQ, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildevent/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of stock ownership, checkout and order transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Ticket inventory, checkout hooks, queues, signed QR check-in.
- **2 — Improve the project/resource:** First scoped project change: Test duplicate checkout and repeat check-in behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [buildevent](C:/Users/Owner/Desktop/buildevent). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildevent/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildevent/docs/upskill/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildevent/package.json).

---

<a id="p286"></a>
### geminiorganized/LLM_Generated_Buildreviewer

A web-based code-review workspace for GitHub pull requests, inspired by ReviewFlow.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, NestJS, Node.js, React, Tailwind CSS, Vite, Prisma, Jest, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildreviewer/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting GitHub APIs, local drafts, transactional publishing, review UX.
- **2 — Improve the project/resource:** First scoped project change: Trace local draft persistence and implement a failed-publish recovery case. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [buildreviewer](C:/Users/Owner/Desktop/buildreviewer). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildreviewer/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildreviewer/package.json), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildreviewer/apps/api/package.json).

---

<a id="p309"></a>
### geminiorganized/OpenSource_Upskilling_Auth

Standalone identity provider for learning OAuth2/OIDC, JWT signing, refresh-token rotation, RBAC, MFA, and audit logging.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Teaching/reference workspace; runtime not verified. Local documentation: The current machine did not have the .NET SDK installed when this scaffold was created, so EF migration files were not generated locally. The infrastructure project includes a design-time AppDbContext factory; run the migration command in infra/postgres/README.md after installing .NET.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Auth/docs2/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for identity proof, session lifecycle and trust boundaries; make learners predict state before running it. Teach OAuth grants, PKCE, token rotation/replay, signing keys, resource authorization. with a separate answer and rubric. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Follow one authorization-code exchange and write a threat model plus negative tests around identity binding and replay. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Exercise the valid identity path and an expired, revoked or replayed credential; verify denial happens before protected state changes.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [netauth](C:/Users/Owner/Desktop/netauth). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Auth/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Auth/docs2/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Auth/docker-compose.yml).

---

<a id="p311"></a>
### geminiorganized/OpenSource_Upskilling_Drop

Personal/team cloud storage built with .NET 8 Web API, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Teaching/reference workspace; runtime not verified. Local documentation: - Background processing pipeline with queued scan jobs, retry/dead-letter state, simulated EICAR detection, text extraction, image thumbnail generation, quarantine, and janitor cleanup.
- **Recorded stack:** C#, CSS, HTML, JavaScript, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Drop/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, upload/finalization state and storage boundaries, an expected-state example and a guided-to-independent change exercise. Tie it to File metadata versus blobs, quotas, resumability, checksums, async processing.. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace an interrupted upload through resume, finalization and quota accounting; add failure/retry tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Try an unauthorized or expired operation and an interrupted retry; verify no orphaned committed state or double quota charge.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [netdrop](C:/Users/Owner/Desktop/netdrop). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Drop/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Drop/docs/upskill/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Drop/docker-compose.yml).

---

<a id="p325"></a>
### gitvg/bazaar

Bazaar is a Shopify-lite commerce platform and a fifteen-sprint systems-design course.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** TypeScript systems-design course with source/tests; in-memory fakes in tests do not establish live integration behavior. Static review only; not built, tested or run.
- **Recorded stack:** JavaScript, SQL, TypeScript, Fastify, Next.js, Node.js, React, GitHub Actions, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [sprint-01.md](C:/Users/Owner/Desktop/gitvg/bazaar/docs/curriculum/sprint-01.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for stock ownership, checkout and order transitions; make learners predict state before running it. Teach Cache coherence, inventory consistency, commerce systems design with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Explain stale storefront versus fresh merchant state and test invalidation. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/bazaar/README.md), [cart-service.ts](C:/Users/Owner/Desktop/gitvg/bazaar/apps/api/src/cart-service.ts), [package.json](C:/Users/Owner/Desktop/gitvg/bazaar/package.json).

---

<a id="p330"></a>
### gitvg/harbor-net

An Intercom-style customer-messaging platform — C#/.NET backend only.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Backend-only .NET support platform with test coverage files; integration behavior unverified. Static review only; not built, tested or run.
- **Recorded stack:** C#, ASP.NET Core, Entity Framework Core, SQLite, xUnit.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/gitvg/harbor-net/docs/adr/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ticket visibility, assignment and service deadlines: ordered source files, one input-to-state trace, a diagram and one independent change targeting SLA workflows, assignment, signed webhooks, outbox.
- **2 — Improve the project/resource:** First scoped project change: Test one SLA deadline and duplicate webhook delivery. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/harbor-net/README.md), [Program.cs](C:/Users/Owner/Desktop/gitvg/harbor-net/src/Harbor.Api/Program.cs), [Harbor.Api.csproj](C:/Users/Owner/Desktop/gitvg/harbor-net/src/Harbor.Api/Harbor.Api.csproj).

---

<a id="p331"></a>
### gitvg/pulse

Product-analytics learning project with event ingestion, consumers, jobs, and a web interface.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Substantial course source/tests; README says live DB/queue/stream wiring is not exercised by CI. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Fastify, Node.js, React, Vite, Prisma, Redis, Docker, GitHub Actions, Vitest, BullMQ.
- **Learning content now:** Structured tutorial / exercises. Start at [sprint-01.md](C:/Users/Owner/Desktop/gitvg/pulse/docs/curriculum/sprint-01.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for event identity, aggregation and reporting filters; make learners predict state before running it. Teach Event ingestion, analytics, identity merge, queues with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace one event through ingestion to query and test duplicate handling. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/pulse/README.md), [App.tsx](C:/Users/Owner/Desktop/gitvg/pulse/apps/web/src/App.tsx), [package.json](C:/Users/Owner/Desktop/gitvg/pulse/package.json).

---

<a id="p332"></a>
### gitvg/pulse-net

A PostHog/Mixpanel-style product-analytics platform — C#/.NET backend only.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Backend-only .NET analytics system with SQLite and worker tests. Static review only; not built, tested or run.
- **Recorded stack:** C#, ASP.NET Core, Entity Framework Core, SQLite, xUnit.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/gitvg/pulse-net/docs/adr/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of event identity, aggregation and reporting filters: ordered source files, one input-to-state trace, a diagram and one independent change targeting Durable ingestion, dead letters, analytics SQL, identity merge.
- **2 — Improve the project/resource:** First scoped project change: Test restart and replay of one captured event. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/pulse-net/README.md), [Program.cs](C:/Users/Owner/Desktop/gitvg/pulse-net/src/Pulse.Api/Program.cs), [Pulse.Api.csproj](C:/Users/Owner/Desktop/gitvg/pulse-net/src/Pulse.Api/Pulse.Api.csproj).

---

<a id="p333"></a>
### gitvg/relay

Workflow-automation teaching platform with triggers, actions, connectors, and durable-execution concepts across a fifteen-sprint curriculum.

- **Use / order:** Primary route candidate; complete this milestone before adding an alternative. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** TypeScript course implementation with API/web/source tests; external connector behavior unverified. Static review only; not built, tested or run.
- **Recorded stack:** JavaScript, TypeScript, Fastify, Next.js, Node.js, React, Prisma, Redis, GitHub Actions, Vitest, BullMQ.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/gitvg/relay/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for step state, retries and adapter contracts; make learners predict state before running it. Teach Workflow engines, connectors, retries, durable execution with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace one failed workflow step and prove retry behavior is bounded. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/relay/README.md), [server.ts](C:/Users/Owner/Desktop/gitvg/relay/apps/api/src/server.ts), [package.json](C:/Users/Owner/Desktop/gitvg/relay/package.json).

---

<a id="p334"></a>
### gitvg/relay-app

A Zapier-style integrations / connectors platform.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** .NET/React implementation explicitly simulates external actions in process. Static review only; not built, tested or run.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, SQLite, Vitest, xUnit.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/gitvg/relay-app/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of step state, retries and adapter contracts: ordered source files, one input-to-state trace, a diagram and one independent change targeting .NET workflow execution, logs, permissions, retries.
- **2 — Improve the project/resource:** First scoped project change: Replace one simulated action with a controlled adapter and contract test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/relay-app/README.md), [App.tsx](C:/Users/Owner/Desktop/gitvg/relay-app/client/src/App.tsx), [package.json](C:/Users/Owner/Desktop/gitvg/relay-app/client/package.json).

---

<a id="p358"></a>
### masternocu

NocoBase extensible low-code application platform.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** Large NocoBase upstream checkout with many tests; advanced reference despite old unknown label. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, SCSS, SQL, TypeScript, React, MySQL, PostgreSQL, Docker, GitHub Actions, Vitest, LangChain.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/masternocu/nocobase/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Plugin architecture, schemas, permissions, large codebases. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Study one small plugin after owning a full-stack app. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [geminiorganized/General_Masternocu](C:/Users/Owner/Desktop/geminiorganized/General_Masternocu). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/masternocu/nocobase/README.md), [server.ts](C:/Users/Owner/Desktop/masternocu/nocobase/packages/plugins/%40nocobase/plugin-error-handler/src/server/server.ts), [package.json](C:/Users/Owner/Desktop/masternocu/nocobase/package.json).

---

<a id="p361"></a>
### missioncontrol

A self-hosted control plane for fleets of AI agents — a C# / .NET 10 recreation of builderz-labs/mission-control per the Fleet Command — C# / .NET Technical Specification.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: Domain workflows, persistence, concurrency basics and operational debugging.
- **Baseline:** README states only roadmap phases 1-4 core of 8 are implemented; source is a partial control plane. Static review only; not built, tested or run.
- **Recorded stack:** C#, CSS, Razor, ASP.NET Core, Entity Framework Core, SQLite, xUnit.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/missioncontrol/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of ownership, ordering and lifecycle transitions, known stubs and one exercise targeting Agent control-plane APIs, auth, EF Core, scheduling. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace task claim concurrency and test two workers claiming one task. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Missioncontrol](C:/Users/Owner/Desktop/geminiorganized/General_Missioncontrol). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/missioncontrol/README.md), [Program.cs](C:/Users/Owner/Desktop/missioncontrol/src/FleetCommand.Host/Program.cs), [FleetCommand.Contracts.csproj](C:/Users/Owner/Desktop/missioncontrol/src/FleetCommand.Contracts/FleetCommand.Contracts.csproj).

---

<a id="p364"></a>
### netauth

Standalone identity provider for learning OAuth2/OIDC, JWT signing, refresh-token rotation, RBAC, MFA, and audit logging.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Educational identity-provider implementation with OAuth/OIDC controllers and MFA/session models. Authorize controller visibly accepts query user_id; authentication/consent safety needs focused review before treating this as an identity template.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/netauth/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for identity proof, session lifecycle and trust boundaries; make learners predict state before running it. Teach OAuth grants, PKCE, token rotation/replay, signing keys, resource authorization. with a separate answer and rubric. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Follow one authorization-code exchange and write a threat model plus negative tests around identity binding and replay. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Exercise the valid identity path and an expired, revoked or replayed credential; verify denial happens before protected state changes.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [geminiorganized/OpenSource_Upskilling_Auth](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Auth). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netauth/README.md), [AuthController.cs](C:/Users/Owner/Desktop/netauth/src/NetAuth0.Api/Controllers/AuthController.cs), [OAuthController.cs](C:/Users/Owner/Desktop/netauth/src/NetAuth0.Api/Controllers/OAuthController.cs).

---

<a id="p365"></a>
### netcleanarch

ASP.NET Core Clean Architecture starter/reference application.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Upstream Clean Architecture solution template; current local README targets .NET 10 and Aspire. User identity endpoint and multiple test-layer projects exist.
- **Recorded stack:** C#, HTML, JavaScript, SCSS, TypeScript, ASP.NET Core, Entity Framework Core, PostgreSQL, SQL Server, SQLite, GitHub Actions, Moq, NUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/netcleanarch/CleanArchitecture/fabledocs/README.md).
- **1 — Improve the upskilling content:** Add a side-by-side trace of one endpoint in this starter and the learner’s simpler finished app.
- **2 — Improve the project/resource:** Make one small handler change in a learning branch and record whether the architectural abstraction actually helps.
- **3 — Prove completion:** Existing relevant tests and one changed-behavior test pass; explain the extra boundary without copying it into unrelated projects.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Multiple Fable sets are listed; a higher suffix is not proof of a better starting point.
- **Related locations to compare:** [geminiorganized/General_Cleanarch](C:/Users/Owner/Desktop/geminiorganized/General_Cleanarch). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netcleanarch/CleanArchitecture/README.md), [Users.cs](C:/Users/Owner/Desktop/netcleanarch/CleanArchitecture/src/Web/Endpoints/Users.cs), [App.jsx](C:/Users/Owner/Desktop/netcleanarch/CleanArchitecture/src/Web/ClientApp-React/src/App.jsx).

---

<a id="p367"></a>
### netdrop

Personal/team cloud storage built with .NET 8 Web API, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Substantial cloud-storage learning app with owner-scoped file service and upload/storage abstractions. README describes resumable chunks, content hashing and queued scans; scanning is explicitly simulated.
- **Recorded stack:** C#, CSS, HTML, JavaScript, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/netdrop/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, upload/finalization state and storage boundaries, an expected-state example and a guided-to-independent change exercise. Tie it to File metadata versus blobs, quotas, resumability, checksums, async processing.. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace an interrupted upload through resume, finalization and quota accounting; add failure/retry tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Try an unauthorized or expired operation and an interrupted retry; verify no orphaned committed state or double quota charge.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [geminiorganized/OpenSource_Upskilling_Drop](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Drop). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netdrop/README.md), [AuthController.cs](C:/Users/Owner/Desktop/netdrop/src/NetDropbox.Api/Controllers/AuthController.cs), [FilesController.cs](C:/Users/Owner/Desktop/netdrop/src/NetDropbox.Api/Controllers/FilesController.cs).

---

<a id="p371"></a>
### netopen1

A reference .NET application implementing an e-commerce website using a services-based architecture using .NET Aspire.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Local upstream eShop reference application; README identifies .NET 9, Aspire and service-based commerce. Identity API and service/test roots are present.
- **Recorded stack:** C#, CSS, HTML, JavaScript, Python, Razor, TypeScript, ASP.NET Core, Blazor, Entity Framework Core, PostgreSQL, GitHub Actions, Playwright.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/netopen1/eShop/fabledoc2/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of stock ownership, checkout and order transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Service boundaries, distributed workflows, integration events and observability..
- **2 — Improve the project/resource:** First scoped project change: Follow checkout across services and diagram failure/retry boundaries after completing a monolith first. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Multiple Fable sets are listed; a higher suffix is not proof of a better starting point.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netopen1/eShop/README.md), [Program.cs](C:/Users/Owner/Desktop/netopen1/eShop/src/Identity.API/Program.cs), [Program.cs](C:/Users/Owner/Desktop/netopen1/eShop/src/Ordering.API/Program.cs).

---

<a id="p372"></a>
### netopen3

Umbraco content management system and its administration interface.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Substantial upstream Umbraco CMS source with .NET Management API and TypeScript web-component backoffice. Earlier catalog Next.js/unknown label is misleading for the core product.
- **Recorded stack:** C#, ASP.NET Core, TypeScript, web components, Vite, SQL Server/SQLite persistence projects, Playwright.
- **Learning content now:** Developer explanation / brief orientation. Start at [architecture.md](C:/Users/Owner/Desktop/netopen3/Umbraco-CMS/src/Umbraco.Web.UI.Client/docs/architecture.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting Large-repo navigation, extension architecture, management APIs, content caching and testing..
- **2 — Improve the project/resource:** First scoped project change: Select one management endpoint or backoffice component and trace its tests; scope a small contribution. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Open3](C:/Users/Owner/Desktop/geminiorganized/General_Open3). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netopen3/Umbraco-CMS/.github/README.md), [Umbraco.Cms.Api.Management.csproj](C:/Users/Owner/Desktop/netopen3/Umbraco-CMS/src/Umbraco.Cms.Api.Management/Umbraco.Cms.Api.Management.csproj), [package.json](C:/Users/Owner/Desktop/netopen3/Umbraco-CMS/src/Umbraco.Web.UI.Client/package.json).

---

<a id="p406"></a>
### newcodex3/apps/24-file-sharing-app

File sharing

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/24-file-sharing-app/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ownership, upload/finalization state and storage boundaries; make learners predict state before running it. Teach Object storage, quotas, upload sessions and expiring share tokens with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace upload finalization and verify ownership, quota and expired-share rejection. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Try an unauthorized or expired operation and an interrupted retry; verify no orphaned committed state or double quota charge.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/24-file-sharing-app-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/24-file-sharing-app/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/24-file-sharing-app/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/24-file-sharing-app/client/package.json).

---

<a id="p407"></a>
### newcodex3/apps/24-file-sharing-app-net

File sharing (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/24-file-sharing-app-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, upload/finalization state and storage boundaries: ordered source files, one input-to-state trace, a diagram and one independent change targeting Object storage, quotas, upload sessions and expiring share tokens.
- **2 — Improve the project/resource:** First scoped project change: Trace upload finalization and verify ownership, quota and expired-share rejection. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Try an unauthorized or expired operation and an interrupted retry; verify no orphaned committed state or double quota charge.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/24-file-sharing-app; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/24-file-sharing-app-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/24-file-sharing-app-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/24-file-sharing-app-net/server/Program.cs).

---

<a id="p418"></a>
### newcodex3/apps/30-headless-cms

Headless CMS

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/30-headless-cms/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for content validation, publication and access boundaries; make learners predict state before running it. Teach Schema-as-data, public API versioning, API keys and webhook retry with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Validate a content type end to end and test key isolation plus retry idempotency. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an unauthorized publish or invalid content payload; verify one permitted publication is rendered as intended.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/30-headless-cms-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/30-headless-cms/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/30-headless-cms/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/30-headless-cms/client/package.json).

---

<a id="p419"></a>
### newcodex3/apps/30-headless-cms-net

Headless CMS (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/30-headless-cms-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of content validation, publication and access boundaries: ordered source files, one input-to-state trace, a diagram and one independent change targeting Schema-as-data, public API versioning, API keys and webhook retry.
- **2 — Improve the project/resource:** First scoped project change: Validate a content type end to end and test key isolation plus retry idempotency. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an unauthorized publish or invalid content payload; verify one permitted publication is rendered as intended.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/30-headless-cms; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/30-headless-cms-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/30-headless-cms-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/30-headless-cms-net/server/Program.cs).

---

<a id="p426"></a>
### newcodex3/apps/34-oauth-saas-identity-portal

OAuth/SaaS identity portal

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/34-oauth-saas-identity-portal/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for identity proof, session lifecycle and trust boundaries; make learners predict state before running it. Teach Session lifecycle, refresh revocation, reset flows and audit events with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace identity proof and refresh replay rejection; replace any placeholder login behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Exercise the valid identity path and an expired, revoked or replayed credential; verify denial happens before protected state changes.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/34-oauth-saas-identity-portal-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/34-oauth-saas-identity-portal/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/34-oauth-saas-identity-portal/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/34-oauth-saas-identity-portal/client/package.json).

---

<a id="p427"></a>
### newcodex3/apps/34-oauth-saas-identity-portal-net

OAuth/SaaS identity portal (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/34-oauth-saas-identity-portal-net/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of identity proof, session lifecycle and trust boundaries, known stubs and one exercise targeting Session lifecycle, refresh revocation, reset flows and audit events. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace identity proof and refresh replay rejection; replace any placeholder login behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Exercise the valid identity path and an expired, revoked or replayed credential; verify denial happens before protected state changes.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/34-oauth-saas-identity-portal; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/34-oauth-saas-identity-portal-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/34-oauth-saas-identity-portal-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/34-oauth-saas-identity-portal-net/server/Program.cs).

---

<a id="p430"></a>
### newcodex3/apps/36-feature-flag-management

Feature flags

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/36-feature-flag-management/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for deterministic targeting and configuration versions; make learners predict state before running it. Teach Deterministic bucketing, targeting, environment isolation and cache invalidation with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Prove rollout assignment is stable and isolated per environment. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Evaluate fixed subjects repeatedly across two environments; verify stable assignments, environment isolation and an explicit rollback result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/36-feature-flag-management-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/36-feature-flag-management/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/36-feature-flag-management/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/36-feature-flag-management/client/package.json).

---

<a id="p431"></a>
### newcodex3/apps/36-feature-flag-management-net

Feature flags (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/36-feature-flag-management-net/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of deterministic targeting and configuration versions, known stubs and one exercise targeting Deterministic bucketing, targeting, environment isolation and cache invalidation. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Prove rollout assignment is stable and isolated per environment. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Evaluate fixed subjects repeatedly across two environments; verify stable assignments, environment isolation and an explicit rollback result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/36-feature-flag-management; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/36-feature-flag-management-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/36-feature-flag-management-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/36-feature-flag-management-net/server/Program.cs).

---

<a id="p436"></a>
### newcodex3/apps/39-third-party-integration-sync-hub

Integration sync hub

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/39-third-party-integration-sync-hub/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for step state, retries and adapter contracts; make learners predict state before running it. Teach Provider boundaries, cursor sync, webhooks, retry and conflict resolution with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Replay a failed page/webhook and prove cursor advancement does not lose or duplicate records. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/39-third-party-integration-sync-hub-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/39-third-party-integration-sync-hub/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/39-third-party-integration-sync-hub/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/39-third-party-integration-sync-hub/client/package.json).

---

<a id="p437"></a>
### newcodex3/apps/39-third-party-integration-sync-hub-net

Integration sync hub (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/39-third-party-integration-sync-hub-net/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of step state, retries and adapter contracts, known stubs and one exercise targeting Provider boundaries, cursor sync, webhooks, retry and conflict resolution. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Replay a failed page/webhook and prove cursor advancement does not lose or duplicate records. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/39-third-party-integration-sync-hub; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/39-third-party-integration-sync-hub-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/39-third-party-integration-sync-hub-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/39-third-party-integration-sync-hub-net/server/Program.cs).

---

<a id="p438"></a>
### newcodex3/apps/40-observability-incident-dashboard

Observability/incident dashboard

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/40-observability-incident-dashboard/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for event correlation, incident transitions and recovery evidence; make learners predict state before running it. Teach Incident state, alerts, timelines and operations workflows with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Connect one real structured event to a reproducible incident timeline and recovery drill. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Emit a controlled failure, find its correlated event and reconstruct the incident timeline; demonstrate the recovery action and record the changed observable state.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/40-observability-incident-dashboard-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/40-observability-incident-dashboard/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/40-observability-incident-dashboard/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/40-observability-incident-dashboard/client/package.json).

---

<a id="p439"></a>
### newcodex3/apps/40-observability-incident-dashboard-net

Observability/incident dashboard (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/40-observability-incident-dashboard-net/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of event correlation, incident transitions and recovery evidence, known stubs and one exercise targeting Incident state, alerts, timelines and operations workflows. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Connect one real structured event to a reproducible incident timeline and recovery drill. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Emit a controlled failure, find its correlated event and reconstruct the incident timeline; demonstrate the recovery action and record the changed observable state.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/40-observability-incident-dashboard; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/40-observability-incident-dashboard-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/40-observability-incident-dashboard-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/40-observability-incident-dashboard-net/server/Program.cs).

---

<a id="p380"></a>
### nopsolutionsnet

nopCommerce ecommerce application with storefront, administration, and plugins.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 6; prerequisites: Completed transactional workflow app; understand auth, tests, deployment and failure handling.
- **Baseline:** Local upstream nopCommerce source: ASP.NET Core storefront/admin with service libraries, plugins and tests. Local README describes .NET 9.
- **Recorded stack:** C#, CSS, HTML, JavaScript, Razor, SQL, Express, PostgreSQL, SQL Server, Docker, GitHub Actions.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/nopsolutionsnet/nopCommerce/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of stock ownership, checkout and order transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Large modular commerce application, plugin boundaries and order lifecycle..
- **2 — Improve the project/resource:** First scoped project change: Trace a single order service method and its callers/tests; compare it with the smaller netshop domain. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Nopsolutions](C:/Users/Owner/Desktop/geminiorganized/General_Nopsolutions). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/nopsolutionsnet/nopCommerce/README.md), [OrderService.cs](C:/Users/Owner/Desktop/nopsolutionsnet/nopCommerce/src/Libraries/Nop.Services/Orders/OrderService.cs), [Program.cs](C:/Users/Owner/Desktop/nopsolutionsnet/nopCommerce/src/Presentation/Nop.Web/Program.cs).

---

<a id="p010"></a>
### _Organized Desktop/01 Net Workspaces/.netslack

NetSlack is a Slack-style collaboration app built with ASP.NET Core, EF Core, SignalR, and React.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, SQLite, Docker, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netslack/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of server authority, timer ownership and command ordering, an expected-state example and a guided-to-independent change exercise. Tie it to event/state modeling, real-time synchronization, validation, reconnect behavior.
- **2 — Improve the project/resource:** First scoped project change: Isolate a game/message state transition and specify duplicate-event/reconnect tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netslack/README.md), [Program.cs](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netslack/src/NetSlack.Api/Program.cs), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netslack/client/src/App.tsx).

---

<a id="p057"></a>
### _Organized Desktop/03 Master Projects/masterrnative

Expo farm-batch tracker for feed, mortality, expenses, and sales.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** JavaScript, TypeScript, Expo, React, React Native, Playwright.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [01-feed-cost-allocation.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterrnative/docs/features/01-feed-cost-allocation.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of local persistence, replay and conflict resolution, known stubs and one exercise targeting Expo/React Native forms, farm-batch data, local/mobile persistence, mobile UX. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace one feed/expense record through the mobile UI and storage; handle interrupted input and offline state. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [storageService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterrnative/src/services/storageService.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterrnative/App.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/masterrnative/package.json).

---

<a id="p068"></a>
### _Organized Desktop/04 JavaScript Training/jep vs code

A full-stack Jeopardy game web application with a React frontend and Node.js/Express backend.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Express, Node.js, React, Vite, Prisma, Jest.
- **Learning content now:** Structured tutorial / exercises. Start at [TEACHING_INDEX.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jep%20vs%20code/Jeopardy-Game/TEACHING_INDEX.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for server authority, timer ownership and command ordering; make learners predict state before running it. Teach event/state modeling, real-time synchronization, validation, reconnect behavior with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Isolate a game/message state transition and specify duplicate-event/reconnect tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jep%20vs%20code/Jeopardy-Game/README.md), [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jep%20vs%20code/jeopardy-rebuild/backend/src/routes/auth.ts), [App.jsx](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jep%20vs%20code/Jeopardy-Game/frontend/src/App.jsx).

---

<a id="p085"></a>
### _Organized Desktop/05 Numbered Experiments/D2

This project implements a maintainable Next.js 14 application that runs structured AI code review in streaming mode.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, TypeScript, Next.js, Node.js, React, Drizzle, PostgreSQL, Anthropic API.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D2/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to external API boundaries, streaming, deterministic evaluation, retries, human review.
- **2 — Improve the project/resource:** First scoped project change: Use a deterministic provider fixture to specify success, cancellation, and failure behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D2/README.md), [page.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D2/src/app/page.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/D2/package.json).

---

<a id="p130"></a>
### _Organized Desktop/05 Numbered Experiments/ww32

Workspace Wire Slack-style messaging application with route, service, and repository boundaries; see the assessment for implementation limits.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest, Socket.IO.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww32/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of server authority, timer ownership and command ordering: ordered source files, one input-to-state trace, a diagram and one independent change targeting event/state modeling, real-time synchronization, validation, reconnect behavior.
- **2 — Improve the project/resource:** First scoped project change: Isolate a game/message state transition and specify duplicate-event/reconnect tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww32/docs/architecture/README.md), [routeHandler.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww32/src/lib/routeHandler.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww32/package.json).

---

<a id="p168"></a>
### _Organized Desktop/06 AI And Learning/aiapplybot

ApplyPilot-derived job-application automation workspace with a six-stage pipeline and an extended auto-apply stage.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** HTML, Python, GitHub Actions, Playwright, pytest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybot/ApplyPilot-main/docs/mission-learning-path/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Python CLI pipelines, browser automation, LLM boundaries, review checkpoints with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Map the six pipeline stages; isolate stage-six automation behind deterministic fixtures. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybot/ApplyPilot-main/README.md), [cli.py](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybot/ApplyPilot-main/src/applypilot/cli.py), [jobspy.py](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybot/ApplyPilot-main/src/applypilot/discovery/jobspy.py).

---

<a id="p169"></a>
### _Organized Desktop/06 AI And Learning/aiapplybotjs

TypeScript/Node CLI implementing a six-stage job-search and application pipeline.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** HTML, SQL, TypeScript, Drizzle, SQLite, Playwright, Vitest, Anthropic API, OpenAI API.
- **Learning content now:** Codebase walkthrough / study pack. Start at [SYSTEM_ARCHITECTURE.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybotjs/docs/intern/SYSTEM_ARCHITECTURE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to TypeScript CLI pipelines, async orchestration, provider adapters.
- **2 — Improve the project/resource:** First scoped project change: Compare one pipeline stage to the Python version and test retry/cancellation behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybotjs/README.md), [jobs.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybotjs/src/db/jobs.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybotjs/package.json).

---

<a id="p173"></a>
### _Organized Desktop/06 AI And Learning/codehelper

Coding-assistance workspace combining an editor and LLM chat with uploaded-codebase browsing and generated explanations.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Express, Fastify, Next.js, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Vitest, OpenAI API.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/codehelper/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, upload/finalization state and storage boundaries, an expected-state example and a guided-to-independent change exercise. Tie it to editor integration, code ingestion, API streaming, LLM error boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace upload-to-code-view and test one malformed archive or failed provider response. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Try an unauthorized or expired operation and an interrupted retry; verify no orphaned committed state or double quota charge.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/codehelper/README.md), [chat.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/codehelper/server/routes/chat.ts), [server.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/codehelper/ww20/services/gateway/src/server.ts).

---

<a id="p175"></a>
### _Organized Desktop/06 AI And Learning/think

TraceVault is a local-first trace platform for AI coding assistant conversations.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Fastify, Node.js, React, Vite, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/think/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of local persistence, replay and conflict resolution: ordered source files, one input-to-state trace, a diagram and one independent change targeting local trace ingestion, normalization, storage, search, privacy-aware tooling.
- **2 — Improve the project/resource:** First scoped project change: Trace one conversation import and design a repeat-import deduplication test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/think/README.md), [service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/think/packages/core/src/service.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/think/apps/web/src/App.tsx).

---

<a id="p181"></a>
### _Organized Desktop/08 App And Product Projects/eliapplybot

A local, personal Chrome extension that fills in the repetitive parts of job application forms — name, email, phone, links, education, work history — from a profile you control.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, React, Vite, GitHub Actions, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [01-codebase-overview.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot/fable/01-codebase-overview.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of time-driven state and browser lifecycle events, an expected-state example and a guided-to-independent change exercise. Tie it to browser extensions, DOM matching, content-script messaging, user-controlled profiles.
- **2 — Improve the project/resource:** First scoped project change: Use local form fixtures to test matching and filling while preserving user review. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a controllable clock; pause/resume and reload while verifying persisted state and no repeated completion event.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot/README.md), [serviceWorker.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot/src/background/serviceWorker.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot/package.json).

---

<a id="p182"></a>
### _Organized Desktop/08 App And Product Projects/eliapplybot-python

A local-first, review-first Python rebuild of the eli apply mate idea.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, Python, FastAPI, Playwright, pytest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot-python/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of local persistence, replay and conflict resolution, known stubs and one exercise targeting Python browser automation, profile models, adapters, explicit review flow. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Compare form mappings with the extension and isolate browser effects behind fixtures. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot-python/README.md), [main.py](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot-python/src/eliapplybot/main.py), [pyproject.toml](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot-python/pyproject.toml).

---

<a id="p197"></a>
### _Organized Desktop/12 Other Projects/appmaketrck

A real-time air quality monitoring web application with an interactive 3D globe visualization.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Playwright, Vitest, MCP.
- **Learning content now:** Developer explanation / brief orientation. Start at [ARCHITECTURE.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/appmaketrck/ARCHITECTURE.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of membership, event identity and reconnect behavior: ordered source files, one input-to-state trace, a diagram and one independent change targeting API-fed geospatial data, 3D visualization, client rendering performance.
- **2 — Improve the project/resource:** First scoped project change: Trace one air-quality reading to the globe and handle unavailable/stale data. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/appmaketrck/airwatch/README.md), [notes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/appmaketrck/obsidian-claude/packages/server/src/api/routes/notes.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/appmaketrck/airwatch/src/App.tsx).

---

<a id="p199"></a>
### _Organized Desktop/12 Other Projects/curse

A full-stack Jeopardy game web application with user accounts, friends system, game sharing, and real-time gameplay.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, Express, Node.js, React, Vite, Prisma, Jest.
- **Learning content now:** Structured tutorial / exercises. Start at [LEARNING_RESOURCES.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/curse/Jeopardy-Game/LEARNING_RESOURCES.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for server authority, timer ownership and command ordering; make learners predict state before running it. Teach Jeopardy game state, user/friend relations, real-time events with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace a game event and specify duplicate-event/reconnect behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/curse/Jeopardy-Game/README.md), [authRoutes.js](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/curse/Jeopardy-Game/backend/src/routes/authRoutes.js), [App.jsx](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/curse/Jeopardy-Game/frontend/src/App.jsx).

---

<a id="p201"></a>
### _Organized Desktop/12 Other Projects/finaljepgame

Jeopardy game builder and player workspace.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations; asynchronous workflows, error handling, and external API boundaries.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/finaljepgame/jeopardy-maker/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of server authority, timer ownership and command ordering, known stubs and one exercise targeting game-builder schemas, gameplay state, UI/server synchronization. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace question creation into gameplay and test one invalid state transition. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/finaljepgame/jeopardy-maker/README.md), [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/finaljepgame/jeopardy-maker/src/lib/auth.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/finaljepgame/jeopardy-maker/package.json).

---

<a id="p208"></a>
### aiapplybot

AI-assisted job application filler for company career sites (Greenhouse, Lever, Ashby, Workday, and custom forms).

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Small Python application with source; browser/provider integration remains unverified. Static review only; not built, tested or run.
- **Recorded stack:** Python, Playwright, Anthropic API, OpenAI API.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/aiapplybot/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting Python browser automation, form extraction, LLM integration.
- **2 — Improve the project/resource:** First scoped project change: Test mapping against a local synthetic form before live sites. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Applybot](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Applybot). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/aiapplybot/README.md), [ats.py](C:/Users/Owner/Desktop/aiapplybot/applybot/ats.py), [requirements.txt](C:/Users/Owner/Desktop/aiapplybot/requirements.txt).

---

<a id="p209"></a>
### aicallhelper

A push-to-record interview copilot for Windows.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Substantial desktop/UI source and test files; frontend mock bridge is not proof of native capture. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, Rust, TypeScript, React, Vite, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/aicallhelper/docs/learn/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Desktop audio streams, typed event bridges, UI state with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace recording cancellation and test event-order races. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/aicallhelper/README.md), [App.tsx](C:/Users/Owner/Desktop/aicallhelper/src/App.tsx), [package.json](C:/Users/Owner/Desktop/aicallhelper/package.json).

---

<a id="p210"></a>
### aicallhelper2

A push-to-record interview copilot for Windows.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Substantive implementation and tests despite old unknown label; native behavior unverified. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, Python, TypeScript, React, Vite, GitHub Actions, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/aicallhelper2/docs/learn/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Audio pipeline state, desktop IPC, recovery.
- **2 — Improve the project/resource:** First scoped project change: Compare one recording flow with aicallhelper and choose one maintained variant. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/aicallhelper2/README.md), [App.tsx](C:/Users/Owner/Desktop/aicallhelper2/frontend/src/App.tsx), [pyproject.toml](C:/Users/Owner/Desktop/aicallhelper2/pyproject.toml).

---

<a id="p211"></a>
### aiheartbeat

Pulse is a locally-run agentic loop.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Node daemon and dashboard source exist; requires its local agent CLI setup. Static review only; not built, tested or run.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/aiheartbeat/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ticket visibility, assignment and service deadlines: ordered source files, one input-to-state trace, a diagram and one independent change targeting Agent scheduling, ticket memory, SQLite, failure recovery. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace one ticket through daemon wakeup, execution, and recovery. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/aiheartbeat/README.md), [cli.ts](C:/Users/Owner/Desktop/aiheartbeat/packages/core/src/cli.ts), [package.json](C:/Users/Owner/Desktop/aiheartbeat/package.json).

---

<a id="p212"></a>
### aihelper

A Windows desktop app (Electron) that helps you answer questions during your own live calls and interviews.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Small Electron implementation with tests; service and native audio behavior unverified. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, Electron.
- **Learning content now:** Structured tutorial / exercises. Start at [ONBOARDING.md](C:/Users/Owner/Desktop/aihelper/docs/ONBOARDING.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Electron IPC, audio transcription, streamed responses with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Explain preload isolation and handle one failed provider request. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Helper](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Helper). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/aihelper/README.md), [preload.js](C:/Users/Owner/Desktop/aihelper/src/preload.js), [package.json](C:/Users/Owner/Desktop/aihelper/package.json).

---

<a id="p216"></a>
### aral

React PWA language-learning app with client-side SQLite, a progress-event log, and a thin synchronization backend.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** PWA/Capacitor monorepo with source and tests; sync service and mobile behavior unverified. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, Java, JavaScript, SQL, TypeScript, Hono, Node.js, React, Tailwind CSS, Vite, Drizzle, Vitest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/aral/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of local persistence, replay and conflict resolution, known stubs and one exercise targeting Offline SQLite, event logs, synchronization, shared schemas. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace one progress event from device storage to sync and rebuilt state. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Aral](C:/Users/Owner/Desktop/geminiorganized/General_Aral). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/aral/README.md), [App.tsx](C:/Users/Owner/Desktop/aral/packages/app/src/App.tsx), [package.json](C:/Users/Owner/Desktop/aral/package.json).

---

<a id="p218"></a>
### astra2

A playable 3D archipelago colony and maritime trade simulator, built with TypeScript, JavaScript, Three.js, Vite, HTML and CSS.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Local 3D simulator with substantive code; optional game specialization after web fundamentals. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Vite, Playwright, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [ARCHITECTURE.md](C:/Users/Owner/Desktop/astra2/ARCHITECTURE.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting Three.js, simulation state, persistence, rendering performance.
- **2 — Improve the project/resource:** First scoped project change: Modify one resource-production rule and verify save/reload behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/astra2/README.md), [data.ts](C:/Users/Owner/Desktop/astra2/src/data.ts), [package.json](C:/Users/Owner/Desktop/astra2/package.json).

---

<a id="p220"></a>
### astraspacegameweb

Persistent browser strategy game with construction, recruitment, scouting, battles, support, conquest, resource caravans, tribes, diplomacy, forums, private messages and rankings.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Broad Fastify/React strategy game; PostgreSQL, Redis and background jobs increase setup complexity. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Fastify, Node.js, React, Tailwind CSS, Vite, Drizzle, PostgreSQL, Redis, Docker, GitHub Actions, Playwright, Vitest, BullMQ.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/astraspacegameweb/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of server authority, timer ownership and command ordering: ordered source files, one input-to-state trace, a diagram and one independent change targeting Persistent multiplayer state, queues, strategy simulation.
- **2 — Improve the project/resource:** First scoped project change: Trace construction completion across database and worker boundaries. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/astraspacegameweb/README.md), [App.tsx](C:/Users/Owner/Desktop/astraspacegameweb/apps/web/src/App.tsx), [package.json](C:/Users/Owner/Desktop/astraspacegameweb/package.json).

---

<a id="p223"></a>
### buildermentor

A mastery-tracking study engine for junior software engineers leveling up to mid/senior and preparing for interviews.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Substantial Fastify/React/PostgreSQL app; E2E material includes scaffolding and AI integrations require setup. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Fastify, Node.js, React, Tailwind CSS, Vite, Drizzle, PostgreSQL, Docker, GitHub Actions, Playwright, Vitest, Anthropic API.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/buildermentor/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of tool or retrieval boundaries and explicit failure behavior: ordered source files, one input-to-state trace, a diagram and one independent change targeting Retrieval pipelines, mastery models, full-stack source ingestion.
- **2 — Improve the project/resource:** First scoped project change: Use only after basic study habits work; trace one ingestion and retrieval path. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed local fixture and mocked external responses; record expected output, an unavailable-tool case and a scored regression example.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Buildermentor](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildermentor). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/buildermentor/README.md), [server.ts](C:/Users/Owner/Desktop/buildermentor/apps/api/src/server.ts), [package.json](C:/Users/Owner/Desktop/buildermentor/package.json).

---

<a id="p226"></a>
### buildsmallplates

Small Plates mobile weightlifting log with workout progression and on-device storage.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Substantial local mobile app; purchase flow is explicitly a stubbed seam. Static review only; not built, tested or run.
- **Recorded stack:** TypeScript, Expo, React, React Native, Vitest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/buildsmallplates/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting React Native, local SQLite, progression algorithms. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Test one progression rule and database migration with retained workouts. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Buildsmallplates](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildsmallplates). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/buildsmallplates/README.md), [App.tsx](C:/Users/Owner/Desktop/buildsmallplates/App.tsx), [package.json](C:/Users/Owner/Desktop/buildsmallplates/package.json).

---

<a id="p228"></a>
### buildwhiteboard

Collaborative Markdown editor using React, TypeScript, Yjs and WebSockets, with local document storage, preview, and presence.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Small collaborative editor with source and one cataloged test file; runtime convergence unverified. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, React, Vite, Docker, GitHub Actions, Playwright.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/buildwhiteboard/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting Yjs, WebSockets, collaborative editing, persistence. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Demonstrate two-client convergence after disconnect/reconnect. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Buildwhiteboard](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildwhiteboard). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/buildwhiteboard/README.md), [App.tsx](C:/Users/Owner/Desktop/buildwhiteboard/client/src/App.tsx), [package.json](C:/Users/Owner/Desktop/buildwhiteboard/package.json).

---

<a id="p235"></a>
### fableaihelperv2

CueDeck is a free, local-first conversation practice and disclosed-assistance coach for Windows.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** CueDeck implementation with tests; part of a related desktop-assistant family. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Electron, React, Vite, Playwright, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/fableaihelperv2/cuedeck/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of local persistence, replay and conflict resolution: ordered source files, one input-to-state trace, a diagram and one independent change targeting Electron architecture, disclosed conversation coaching, streaming.
- **2 — Improve the project/resource:** First scoped project change: Trace one audio-to-response flow and compare recovery against finalcallhelp. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Fablehelperv2](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Fablehelperv2). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/fableaihelperv2/cuedeck/README.md), [App.tsx](C:/Users/Owner/Desktop/fableaihelperv2/cuedeck/src/renderer/App.tsx), [package.json](C:/Users/Owner/Desktop/fableaihelperv2/cuedeck/package.json).

---

<a id="p236"></a>
### fableaihelperv3

Push-to-record interview copilot for Windows.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** README calls this the v2 rewrite of aihelper despite folder name v3. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Electron, Vite, Vitest, Anthropic API.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/fableaihelperv3/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting Low-latency streaming, Electron bridges, cancellation.
- **2 — Improve the project/resource:** First scoped project change: Measure and explain one mocked stream/cancel path before provider integration. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Fablehelperv3](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Fablehelperv3). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/fableaihelperv3/README.md), [preload.ts](C:/Users/Owner/Desktop/fableaihelperv3/src/preload.ts), [package.json](C:/Users/Owner/Desktop/fableaihelperv3/package.json).

---

<a id="p237"></a>
### finalcallhelp

CueDeck desktop conversation-assistance and practice application.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Expanded CueDeck source with tests; folder name alone does not prove it is the canonical version. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Electron, React, Vite, Playwright, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/finalcallhelp/cuedeck/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting Desktop IPC, provider adapters, conversation practice.
- **2 — Improve the project/resource:** First scoped project change: Choose one CueDeck baseline after comparing tests and setup requirements. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/finalcallhelp/README.md), [App.tsx](C:/Users/Owner/Desktop/finalcallhelp/cuedeck/src/renderer/App.tsx), [package.json](C:/Users/Owner/Desktop/finalcallhelp/cuedeck/package.json).

---

<a id="p246"></a>
### geminiorganized/General_Aral

React PWA language-learning workspace with client-side SQLite, a progress-event log, and a thin synchronization backend.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, Java, JavaScript, SQL, TypeScript, Hono, Node.js, React, Tailwind CSS, Vite, Drizzle, Vitest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Aral/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of local persistence, replay and conflict resolution, known stubs and one exercise targeting Offline SQLite, event logs, synchronization, shared schemas. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace one progress event from device storage to sync and rebuilt state. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [aral](C:/Users/Owner/Desktop/aral). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Aral/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Aral/package.json), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Aral/content/package.json).

---

<a id="p259"></a>
### geminiorganized/General_Jsharness

VTCode Rust terminal coding-agent workspace.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Relevant implementation is present; runtime not verified. Local documentation: Scaffolds vtcode.toml, .vtcode/, and AGENTS.md in your project; vtcode init scaffold project config + AGENTS.md
- **Recorded stack:** JavaScript, Python, Ruby, Rust, TypeScript, Axum, GitHub Actions, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [ARCHITECTURE.md](C:/Users/Owner/Desktop/geminiorganized/General_Jsharness/VTCode/docs/ARCHITECTURE.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of tool or retrieval boundaries and explicit failure behavior: ordered source files, one input-to-state trace, a diagram and one independent change targeting Rust CLI architecture, tools, agent protocols, terminal UI.
- **2 — Improve the project/resource:** First scoped project change: Trace one command from CLI parsing to tool execution and compare the TS port. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed local fixture and mocked external responses; record expected output, an unavailable-tool case and a scored regression example.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [jsharness/VTCode](C:/Users/Owner/Desktop/jsharness/VTCode). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Jsharness/VTCode/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Jsharness/ctvodejs/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Jsharness/ctvodejs/package.json).

---

<a id="p262"></a>
### geminiorganized/General_Masteroutline

A fast, collaborative, knowledge base for your team built using React and Node.js.Try out Outline using our hosted version at www.getoutline.com.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** HTML, JavaScript, TypeScript, React, Vite, PostgreSQL, Redis, AWS SDK, Docker, GitHub Actions, Vitest, MCP, Socket.IO.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Masteroutline/outline/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Mature collaborative editor, Koa, PostgreSQL, Redis, policies.
- **2 — Improve the project/resource:** First scoped project change: Trace one document permission rule and its tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Multiple Fable sets are listed; a higher suffix is not proof of a better starting point.
- **Related locations to compare:** [masteroutline](C:/Users/Owner/Desktop/masteroutline). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Masteroutline/outline/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Masteroutline/outline/fabledocs/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Masteroutline/outline/package.json).

---

<a id="p266"></a>
### geminiorganized/General_Mobiletagalog

A Duolingo-style app teaching Tagalog to English speakers, built with React Native + Expo.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** JavaScript, TypeScript, Expo, React, React Native.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Mobiletagalog/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of local persistence, replay and conflict resolution: ordered source files, one input-to-state trace, a diagram and one independent change targeting Expo navigation, device SQLite, offline course content.
- **2 — Improve the project/resource:** First scoped project change: Test offline progress and one guest-to-account synchronization scenario. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [mobiletagalog](C:/Users/Owner/Desktop/mobiletagalog). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Mobiletagalog/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Mobiletagalog/package.json), [AuthScreen.tsx](C:/Users/Owner/Desktop/geminiorganized/General_Mobiletagalog/src/components/AuthScreen.tsx).

---

<a id="p273"></a>
### geminiorganized/General_Open5

Jellyfin The Free Software Media System

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** C#, CSS, HTML, ASP.NET Core, Entity Framework Core, SQLite, GitHub Actions.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Open5/jellyfin/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Media services, background libraries, API compatibility and large codebase maintenance..
- **2 — Improve the project/resource:** First scoped project change: Trace one user/library request into service and storage boundaries, then choose a narrow tested fix. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [netopen5](C:/Users/Owner/Desktop/netopen5). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Open5/jellyfin/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Open5/jellyfin/fuzz/README.md), [Emby.Naming.csproj](C:/Users/Owner/Desktop/geminiorganized/General_Open5/jellyfin/Emby.Naming/Emby.Naming.csproj).

---

<a id="p280"></a>
### geminiorganized/General_Spacegame

A server-authoritative, Tribal Wars-style multiplayer strategy game.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** JavaScript, SQL, TypeScript, Expo, Fastify, Node.js, React, React Native, Prisma, Redis, Docker, Vitest, BullMQ, Socket.IO.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Spacegame/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of server authority, timer ownership and command ordering, known stubs and one exercise targeting Deterministic simulation, concurrency, queues, reconciliation and mobile/realtime state.. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace one build/combat timer from command to worker to client, including duplicate delivery. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [spacegame](C:/Users/Owner/Desktop/spacegame). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Spacegame/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Spacegame/package.json), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/General_Spacegame/docker-compose.yml).

---

<a id="p281"></a>
### geminiorganized/General_Tagalog

A free Duolingo-style app teaching Tagalog to English speakers.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Expo, Fastify, Next.js, Node.js, React, React Native, Drizzle, Docker, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Tagalog/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of local persistence, replay and conflict resolution, an expected-state example and a guided-to-independent change exercise. Tie it to Shared domain core, content compiler, offline event sync, idempotency and cross-platform delivery..
- **2 — Improve the project/resource:** First scoped project change: Trace one lesson progress event through guest storage and authenticated sync; verify duplicate/offline replay handling. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [tagalog](C:/Users/Owner/Desktop/tagalog). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Tagalog/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Tagalog/docs/upskill/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Tagalog/package.json).

---

<a id="p282"></a>
### geminiorganized/LLM_Generated_Applybot

AI-assisted job application filler for company career sites (Greenhouse, Lever, Ashby, Workday, and custom forms).

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Static sample does not establish runtime readiness.
- **Recorded stack:** Python, Playwright, Anthropic API, OpenAI API.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Applybot/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting Python browser automation, form extraction, LLM integration.
- **2 — Improve the project/resource:** First scoped project change: Test mapping against a local synthetic form before live sites. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [aiapplybot](C:/Users/Owner/Desktop/aiapplybot). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Applybot/README.md), [requirements.txt](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Applybot/requirements.txt), [ats.py](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Applybot/applybot/ats.py).

---

<a id="p284"></a>
### geminiorganized/LLM_Generated_Buildermentor

A mastery-tracking study engine for junior software engineers leveling up to mid/senior and preparing for interviews.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Relevant implementation is present; runtime not verified. Local documentation: - E2E scaffold in e2e/ (Playwright): cd e2e && pnpm install && npx playwright install chromium && npx playwright test with the dev stack running.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Fastify, Node.js, React, Tailwind CSS, Vite, Drizzle, PostgreSQL, Docker, GitHub Actions, Playwright, Vitest, Anthropic API.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildermentor/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of tool or retrieval boundaries and explicit failure behavior: ordered source files, one input-to-state trace, a diagram and one independent change targeting Retrieval pipelines, mastery models, full-stack source ingestion.
- **2 — Improve the project/resource:** First scoped project change: Use only after basic study habits work; trace one ingestion and retrieval path. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed local fixture and mocked external responses; record expected output, an unavailable-tool case and a scored regression example.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [buildermentor](C:/Users/Owner/Desktop/buildermentor). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildermentor/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildermentor/package.json), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildermentor/docker-compose.yml).

---

<a id="p287"></a>
### geminiorganized/LLM_Generated_Buildsmallplates

Small Plates mobile weightlifting log with workout progression and on-device storage.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** TypeScript, Expo, React, React Native, Vitest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildsmallplates/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting React Native, local SQLite, progression algorithms. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Test one progression rule and database migration with retained workouts. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [buildsmallplates](C:/Users/Owner/Desktop/buildsmallplates). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildsmallplates/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildsmallplates/package.json), [App.tsx](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildsmallplates/App.tsx).

---

<a id="p289"></a>
### geminiorganized/LLM_Generated_Buildwhiteboard

Collaborative Markdown editor using React, TypeScript, Yjs and WebSockets, with local document storage, preview, and presence.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Relevant implementation is present; runtime not verified. Local documentation: A React, Vite, TypeScript, Yjs, and WebSocket-powered collaborative Markdown editor with durable local document storage, sanitized Markdown preview, collaborator presence, document metadata APIs, import/export tooling, CI, and Docker scaffolding.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, React, Vite, Docker, GitHub Actions, Playwright.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildwhiteboard/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting Yjs, WebSockets, collaborative editing, persistence. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Demonstrate two-client convergence after disconnect/reconnect. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [buildwhiteboard](C:/Users/Owner/Desktop/buildwhiteboard). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildwhiteboard/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildwhiteboard/client/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildwhiteboard/package.json).

---

<a id="p292"></a>
### geminiorganized/LLM_Generated_Fablehelperv2

CueDeck is a free, local-first conversation practice and disclosed-assistance coach for Windows.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Electron, React, Vite, Playwright, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Fablehelperv2/cuedeck/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of local persistence, replay and conflict resolution: ordered source files, one input-to-state trace, a diagram and one independent change targeting Electron architecture, disclosed conversation coaching, streaming.
- **2 — Improve the project/resource:** First scoped project change: Trace one audio-to-response flow and compare recovery against finalcallhelp. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [fableaihelperv2](C:/Users/Owner/Desktop/fableaihelperv2). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Fablehelperv2/cuedeck/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Fablehelperv2/cuedeck/package.json), [App.tsx](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Fablehelperv2/cuedeck/src/renderer/App.tsx).

---

<a id="p293"></a>
### geminiorganized/LLM_Generated_Fablehelperv3

Push-to-record interview copilot for Windows.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Static sample does not establish runtime readiness.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Electron, Vite, Vitest, Anthropic API.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Fablehelperv3/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting Low-latency streaming, Electron bridges, cancellation.
- **2 — Improve the project/resource:** First scoped project change: Measure and explain one mocked stream/cancel path before provider integration. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [fableaihelperv3](C:/Users/Owner/Desktop/fableaihelperv3). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Fablehelperv3/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Fablehelperv3/package.json), [preload.ts](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Fablehelperv3/src/preload.ts).

---

<a id="p297"></a>
### geminiorganized/LLM_Generated_Helper

A Windows desktop app (Electron) that helps you answer questions during your own live calls and interviews.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Static sample does not establish runtime readiness.
- **Recorded stack:** CSS, HTML, JavaScript, Electron.
- **Learning content now:** Structured tutorial / exercises. Start at [ONBOARDING.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Helper/docs/ONBOARDING.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Electron IPC, audio transcription, streamed responses with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Explain preload isolation and handle one failed provider request. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [aihelper](C:/Users/Owner/Desktop/aihelper). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Helper/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Helper/docs/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Helper/package.json).

---

<a id="p304"></a>
### geminiorganized/LLM_Generated_Rag

NetAiOps is a AI-powered IT operations platform built as a phased learning project.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Docker, GitHub Actions, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Rag/docs2.0/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of tool or retrieval boundaries and explicit failure behavior, an expected-state example and a guided-to-independent change exercise. Tie it to Layered .NET, RBAC, operational data, retrieval and evaluation design.. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace one ticket request through UI/API/persistence, then implement one documented retrieval slice with a small evaluation set. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed local fixture and mocked external responses; record expected output, an unavailable-tool case and a scored regression example.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [netairag](C:/Users/Owner/Desktop/netairag). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Rag/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Rag/docs2.0/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Rag/docker-compose.yml).

---

<a id="p312"></a>
### geminiorganized/OpenSource_Upskilling_Intercom

A two-sided live chat (Intercom-style): an embeddable visitor widget plus an agent inbox for support teams.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Teaching/reference workspace; runtime not verified. Local documentation: Presence — in-memory PresenceTracker fed by hub connect/disconnect plus client activity heartbeats. Grace periods prevent flapping: 60s after a disconnect the agent still counts as online (page refreshes don't flicker); 5 min without activity degrades to Away. A background sweeper broadcasts transit
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Docker, GitHub Actions, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Intercom/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of membership, event identity and reconnect behavior, an expected-state example and a guided-to-independent change exercise. Tie it to Realtime rooms, visitor versus agent auth, routing, presence and SLA jobs..
- **2 — Improve the project/resource:** First scoped project change: Trace visitor session to agent reply and verify conversation authorization plus reconnect behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [netintercom](C:/Users/Owner/Desktop/netintercom). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Intercom/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Intercom/docs/upskill/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Intercom/docker-compose.yml).

---

<a id="p327"></a>
### gitvg/folio

Collaborative document-editor teaching app covering blocks, concurrent editing, offline merge, comments, permissions, and version history.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Advanced course implementation with substantial source/tests; a stale scaffolding note conflicts with broader existing code. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Fastify, Node.js, React, Vite, Prisma, Redis, Docker, GitHub Actions, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/gitvg/folio/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for membership, event identity and reconnect behavior; make learners predict state before running it. Teach CRDTs, offline merge, permissions, collaborative editors with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Complete one two-client conflict scenario after simpler realtime exercises. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/folio/README.md), [App.tsx](C:/Users/Owner/Desktop/gitvg/folio/apps/web/src/App.tsx), [package.json](C:/Users/Owner/Desktop/gitvg/folio/package.json).

---

<a id="p328"></a>
### gitvg/folio-app

A Notion-style collaborative docs & knowledge base — full-stack monorepo.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Separate .NET/React document system; verify actual realtime semantics before equating it with Folio CRDT course. Static review only; not built, tested or run.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, SQLite, Vitest, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/gitvg/folio-app/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Block editing, document permissions, versions, .NET APIs.
- **2 — Improve the project/resource:** First scoped project change: Trace a page edit through authorization and version history. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/folio-app/README.md), [App.tsx](C:/Users/Owner/Desktop/gitvg/folio-app/client/src/App.tsx), [package.json](C:/Users/Owner/Desktop/gitvg/folio-app/client/package.json).

---

<a id="p329"></a>
### gitvg/harbor

Customer-messaging and support-inbox learning project with API, web, worker, and retrieval components.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Source and tests exist; CI intentionally uses fake infrastructure and mock models. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Fastify, Node.js, React, Vite, Prisma, GitHub Actions, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [LEARNER-GUIDE.md](C:/Users/Owner/Desktop/gitvg/harbor/docs/LEARNER-GUIDE.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for tool or retrieval boundaries and explicit failure behavior; make learners predict state before running it. Teach Support workflows, retrieval, evaluation, LLM cost controls with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Reproduce one failed answer evaluation with a mock model and improve it. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed local fixture and mocked external responses; record expected output, an unavailable-tool case and a scored regression example.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/harbor/README.md), [App.tsx](C:/Users/Owner/Desktop/gitvg/harbor/apps/web/src/App.tsx), [package.json](C:/Users/Owner/Desktop/gitvg/harbor/package.json).

---

<a id="p336"></a>
### gitvg/tracer

An offline-first, real-time issue tracker (a Linear-style clone) — and a 15-sprint upskilling curriculum built entirely as pull requests.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Advanced TypeScript issue-tracker course; frontend and sync source exist. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Fastify, Node.js, React, Vite, Prisma, Docker, GitHub Actions, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/gitvg/tracer/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for local persistence, replay and conflict resolution; make learners predict state before running it. Teach Offline synchronization, real-time presence, issue workflows with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: After gitjira-app, test conflicting offline edits and recovery. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/tracer/README.md), [App.tsx](C:/Users/Owner/Desktop/gitvg/tracer/apps/web/src/App.tsx), [package.json](C:/Users/Owner/Desktop/gitvg/tracer/package.json).

---

<a id="p352"></a>
### jsharness/ctvodejs

A TypeScript port of VTCode, built as a sequence of reviewable vertical slices.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Early TypeScript port explicitly not feature complete; substantial source and tests exist. Static review only; not built, tested or run.
- **Recorded stack:** JavaScript, TypeScript, GitHub Actions, Vitest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/jsharness/ctvodejs/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting TypeScript agent runtimes, event contracts, parity testing. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Port one bounded VTCode behavior and add a parity fixture. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/jsharness/ctvodejs/README.md), [index.ts](C:/Users/Owner/Desktop/jsharness/ctvodejs/apps/cli/src/index.ts), [package.json](C:/Users/Owner/Desktop/jsharness/ctvodejs/package.json).

---

<a id="p353"></a>
### jsharness/VTCode

VTCode Rust terminal coding-agent workspace.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Large Rust upstream coding-agent workspace; research-preview behavior and local runtime unverified. Static review only; not built, tested or run.
- **Recorded stack:** JavaScript, Python, Ruby, Rust, TypeScript, Axum, GitHub Actions.
- **Learning content now:** Developer explanation / brief orientation. Start at [ARCHITECTURE.md](C:/Users/Owner/Desktop/jsharness/VTCode/docs/ARCHITECTURE.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of tool or retrieval boundaries and explicit failure behavior: ordered source files, one input-to-state trace, a diagram and one independent change targeting Rust CLI architecture, tools, agent protocols, terminal UI.
- **2 — Improve the project/resource:** First scoped project change: Trace one command from CLI parsing to tool execution and compare the TS port. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Use a fixed local fixture and mocked external responses; record expected output, an unavailable-tool case and a scored regression example.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/jsharness/VTCode/README.md), [main.rs](C:/Users/Owner/Desktop/jsharness/VTCode/src/main.rs), [Cargo.toml](C:/Users/Owner/Desktop/jsharness/VTCode/Cargo.toml).

---

<a id="p359"></a>
### masteroutline

A fast, collaborative, knowledge base for your team built using React and Node.js.Try out Outline using our hosted version at www.getoutline.com.

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Large Outline upstream codebase; useful for bounded contribution after simpler collaboration projects. Static review only; not built, tested or run.
- **Recorded stack:** HTML, JavaScript, TypeScript, React, Vite, PostgreSQL, Redis, AWS SDK, Docker, GitHub Actions, Vitest, MCP, Socket.IO.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/masteroutline/outline/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Mature collaborative editor, Koa, PostgreSQL, Redis, policies.
- **2 — Improve the project/resource:** First scoped project change: Trace one document permission rule and its tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Multiple Fable sets are listed; a higher suffix is not proof of a better starting point.
- **Related locations to compare:** [geminiorganized/General_Masteroutline](C:/Users/Owner/Desktop/geminiorganized/General_Masteroutline). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/masteroutline/outline/README.md), [App.tsx](C:/Users/Owner/Desktop/masteroutline/outline/app/components/Sidebar/App.tsx), [package.json](C:/Users/Owner/Desktop/masteroutline/outline/package.json).

---

<a id="p362"></a>
### mobiletagalog

A Duolingo-style app teaching Tagalog to English speakers, built with React Native + Expo.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Reliable full-stack delivery plus the relevant specialization prerequisites.
- **Baseline:** Standalone port from tagalog; optional backend, no recorded audio clips yet, and no cataloged test files. Static review only; not built, tested or run.
- **Recorded stack:** JavaScript, TypeScript, Expo, React, React Native.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/mobiletagalog/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of local persistence, replay and conflict resolution: ordered source files, one input-to-state trace, a diagram and one independent change targeting Expo navigation, device SQLite, offline course content.
- **2 — Improve the project/resource:** First scoped project change: Test offline progress and one guest-to-account synchronization scenario. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Mobiletagalog](C:/Users/Owner/Desktop/geminiorganized/General_Mobiletagalog). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/mobiletagalog/README.md), [AuthScreen.tsx](C:/Users/Owner/Desktop/mobiletagalog/src/components/AuthScreen.tsx), [package.json](C:/Users/Owner/Desktop/mobiletagalog/package.json).

---

<a id="p363"></a>
### netairag

IT-operations learning platform with a .NET/React foundation and planned RAG, agent, mock integration and evaluation extensions.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Substantial .NET/React foundation and IT-operations CRUD; README and roadmap still reserve RAG, agents, MCP mocks and evaluation for future phases. Treat AI completion as unverified.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Docker, GitHub Actions, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/netairag/docs2.0/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of tool or retrieval boundaries and explicit failure behavior, an expected-state example and a guided-to-independent change exercise. Tie it to Layered .NET, RBAC, operational data, retrieval and evaluation design.. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace one ticket request through UI/API/persistence, then implement one documented retrieval slice with a small evaluation set. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed local fixture and mocked external responses; record expected output, an unavailable-tool case and a scored regression example.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Rag](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Rag). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netairag/README.md), [AuthController.cs](C:/Users/Owner/Desktop/netairag/src/Api/Controllers/AuthController.cs), [UsersController.cs](C:/Users/Owner/Desktop/netairag/src/Api/Controllers/UsersController.cs).

---

<a id="p368"></a>
### netintercom

A two-sided live chat (Intercom-style): an embeddable visitor widget plus an agent inbox for support teams.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Two React clients and .NET API with visitor-scoped widget endpoints, SignalR and Hangfire wiring; unit/integration project structure present. Runtime reliability unverified.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Docker, GitHub Actions, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/netintercom/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of membership, event identity and reconnect behavior, an expected-state example and a guided-to-independent change exercise. Tie it to Realtime rooms, visitor versus agent auth, routing, presence and SLA jobs..
- **2 — Improve the project/resource:** First scoped project change: Trace visitor session to agent reply and verify conversation authorization plus reconnect behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/OpenSource_Upskilling_Intercom](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Intercom). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netintercom/README.md), [AuthController.cs](C:/Users/Owner/Desktop/netintercom/src/NetIntercom.Api/Controllers/AuthController.cs), [WidgetController.cs](C:/Users/Owner/Desktop/netintercom/src/NetIntercom.Api/Controllers/WidgetController.cs).

---

<a id="p373"></a>
### netopen5

Jellyfin The Free Software Media System

- **Use / order:** Upstream/starter reference; choose a bounded study or contribution task. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Local upstream Jellyfin server source with C# API controllers, database and media-domain modules. Treat as advanced source-reading/contribution material.
- **Recorded stack:** C#, CSS, HTML, ASP.NET Core, Entity Framework Core, SQLite, GitHub Actions.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/netopen5/jellyfin/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Media services, background libraries, API compatibility and large codebase maintenance..
- **2 — Improve the project/resource:** First scoped project change: Trace one user/library request into service and storage boundaries, then choose a narrow tested fix. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct. Keep the change inside one upstream module or starter example and document its conventions.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Open5](C:/Users/Owner/Desktop/geminiorganized/General_Open5). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netopen5/jellyfin/README.md), [UserController.cs](C:/Users/Owner/Desktop/netopen5/jellyfin/Jellyfin.Api/Controllers/UserController.cs), [UserViewsController.cs](C:/Users/Owner/Desktop/netopen5/jellyfin/Jellyfin.Api/Controllers/UserViewsController.cs).

---

<a id="p462"></a>
### newcodecjs2/helpkit

Support inbox/widget

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Architecture reading scaffold with domain functions and route sketches over in-memory stores; root explicitly says installation/deployment wiring is incomplete.
- **Recorded stack:** TypeScript, React, Next.js declared, Drizzle declared, Vitest.
- **Parent workspace:** [newcodecjs2](C:/Users/Owner/Desktop/newcodecjs2). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodecjs2/helpkit/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of membership, event identity and reconnect behavior: ordered source files, one input-to-state trace, a diagram and one independent change targeting Tenant isolation, assignment routing, room events and email normalization.
- **2 — Improve the project/resource:** First scoped project change: Trace a widget message and prove room fanout cannot cross tenants. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** One of five related SaaS exercises; not five production-complete products.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodecjs2/helpkit/README.md), [package.json](C:/Users/Owner/Desktop/newcodecjs2/helpkit/package.json), [routes.ts](C:/Users/Owner/Desktop/newcodecjs2/helpkit/src/server/routes.ts).

---

<a id="p394"></a>
### newcodex3/apps/18-team-chat

Team chat

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/18-team-chat/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for membership, event identity and reconnect behavior; make learners predict state before running it. Teach Message cursors, optimistic reconciliation, presence and realtime transport with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace a message across reconnect and prevent duplicate delivery. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/18-team-chat-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/18-team-chat/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/18-team-chat/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/18-team-chat/client/package.json).

---

<a id="p395"></a>
### newcodex3/apps/18-team-chat-net

Team chat (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/18-team-chat-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of membership, event identity and reconnect behavior: ordered source files, one input-to-state trace, a diagram and one independent change targeting Message cursors, optimistic reconciliation, presence and realtime transport.
- **2 — Improve the project/resource:** First scoped project change: Trace a message across reconnect and prevent duplicate delivery. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Simulate two users and a reconnect; verify messages reach authorized members once and unauthorized recipients receive none.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/18-team-chat; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/18-team-chat-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/18-team-chat-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/18-team-chat-net/server/Program.cs).

---

<a id="p387"></a>
### spacegame

A server-authoritative, Tribal Wars-style multiplayer strategy game.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Server-authoritative multiplayer strategy code with Fastify API, Expo client, shared formulas, Prisma, BullMQ/Redis and Socket.IO. Runtime correctness unverified.
- **Recorded stack:** JavaScript, SQL, TypeScript, Expo, Fastify, Node.js, React, React Native, Prisma, Redis, Docker, Vitest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/spacegame/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of server authority, timer ownership and command ordering, known stubs and one exercise targeting Deterministic simulation, concurrency, queues, reconciliation and mobile/realtime state.. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace one build/combat timer from command to worker to client, including duplicate delivery. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Spacegame](C:/Users/Owner/Desktop/geminiorganized/General_Spacegame). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/spacegame/README.md), [auth.ts](C:/Users/Owner/Desktop/spacegame/apps/server/src/routes/auth.ts), [misc.ts](C:/Users/Owner/Desktop/spacegame/apps/server/src/routes/misc.ts).

---

<a id="p388"></a>
### spacegamev2

A server-authoritative, Tribal Wars-style multiplayer strategy game.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Warband variant nested at spacegamev2/spacegamev2. Fresh auth source differs from spacegame with session/logout/revocation imports; additional CI/E2E structure exists. Not established as a byte-for-byte duplicate or guaranteed better version.
- **Recorded stack:** JavaScript, SQL, TypeScript, Expo, Fastify, Node.js, React, React Native, Prisma, Redis, Docker, GitHub Actions, Playwright, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [readme.md](C:/Users/Owner/Desktop/spacegamev2/spacegamev2/fabledocs/readme.md).
- **1 — Improve the upskilling content:** Separate existing-build fabledocs from fabledocs2 rebuild specifications and fabledocs3 product onboarding; link each to its actual scope.
- **2 — Improve the project/resource:** Choose a baseline against spacegame, then protect one server-side game command against replay.
- **3 — Prove completion:** Deliver the same command twice and restart its worker; resources and completion effects must apply once.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** fabledocs describes the existing build; fabledocs2 is a rebuild specification; fabledocs3 is product onboarding. These are different purposes, not interchangeable editions. Multiple Fable sets are listed; a higher suffix is not proof of a better starting point.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/spacegamev2/spacegamev2/README.md), [auth.ts](C:/Users/Owner/Desktop/spacegamev2/spacegamev2/apps/server/src/routes/auth.ts), [misc.ts](C:/Users/Owner/Desktop/spacegamev2/spacegamev2/apps/server/src/routes/misc.ts).

---

<a id="p389"></a>
### tagalog

A free Duolingo-style app teaching Tagalog to English speakers.

- **Use / order:** Optional specialization after the capstone and reliability stage. Original milestone 7; prerequisites: Solid full-stack foundations plus architecture, concurrency, queues and observability basics.
- **Baseline:** Aral multi-client learning app with Next.js, Expo, Fastify, shared pure TS game engine and Drizzle/Postgres schema. README documents guest mode, mobile SQLite outbox and simplifications.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Expo, Fastify, Next.js, Node.js, React, React Native, Drizzle, Docker, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/tagalog/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of local persistence, replay and conflict resolution, an expected-state example and a guided-to-independent change exercise. Tie it to Shared domain core, content compiler, offline event sync, idempotency and cross-platform delivery..
- **2 — Improve the project/resource:** First scoped project change: Trace one lesson progress event through guest storage and authenticated sync; verify duplicate/offline replay handling. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/tagalog/README.md), [auth.ts](C:/Users/Owner/Desktop/tagalog/apps/api/src/routes/auth.ts), [me.ts](C:/Users/Owner/Desktop/tagalog/apps/api/src/routes/me.ts).

---
