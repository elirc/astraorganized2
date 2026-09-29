# Section 4: Domain rules and reliability

[Plan index](README.md)

Harden the capstone before starting another app. Select one focused project only when it teaches a missing invariant, transaction or recovery behavior.

**Stage exit criterion:** Show a domain rule holding through an invalid request and a relevant retry, concurrency or restart scenario; explain the failure and recovery path.

**Coverage:** 86 project/workspace/resource records and 37 nested teaching apps. Entries are grouped by original milestone and alphabetized within it; alphabetical position is not a mandatory execution order. Use the short route in the index.

All actions below are proposals based on the September 6–7 static reviews. Reproduce the baseline before claiming a defect or improvement. Existing tests and docs may already cover a proposed case; assess and strengthen them rather than duplicate them.

## Entries

- [.netstripe](#p004)
- [_Organized Desktop/01 Net Workspaces/.netcalendy](#p006)
- [_Organized Desktop/01 Net Workspaces/.netgum](#p007)
- [_Organized Desktop/02 Build Projects/buildaffiliate](#p015)
- [_Organized Desktop/02 Build Projects/buildanalytics](#p019)
- [_Organized Desktop/02 Build Projects/buildecom](#p023)
- [_Organized Desktop/02 Build Projects/buildScedulingPYJS](#p026)
- [_Organized Desktop/03 Master Projects/master](#p028)
- [_Organized Desktop/04 JavaScript Training/jsdrill_sync_20260223_125137](#p069)
- [_Organized Desktop/04 JavaScript Training/jstrain2](#p072)
- [_Organized Desktop/04 JavaScript Training/jstrain2.4](#p075)
- [_Organized Desktop/04 JavaScript Training/jstrain3](#p076)
- [_Organized Desktop/04 JavaScript Training/jstrain3.0](#p077)
- [_Organized Desktop/05 Numbered Experiments/B1](#p083)
- [_Organized Desktop/05 Numbered Experiments/e1](#p087)
- [_Organized Desktop/05 Numbered Experiments/e12](#p089)
- [_Organized Desktop/05 Numbered Experiments/e13](#p090)
- [_Organized Desktop/05 Numbered Experiments/e14](#p091)
- [_Organized Desktop/05 Numbered Experiments/e3](#p096)
- [_Organized Desktop/05 Numbered Experiments/w22](#p108)
- [_Organized Desktop/05 Numbered Experiments/w24](#p110)
- [_Organized Desktop/05 Numbered Experiments/w25](#p111)
- [_Organized Desktop/05 Numbered Experiments/ww1](#p112)
- [_Organized Desktop/05 Numbered Experiments/ww10](#p113)
- [_Organized Desktop/05 Numbered Experiments/ww11](#p114)
- [_Organized Desktop/05 Numbered Experiments/ww13](#p116)
- [_Organized Desktop/05 Numbered Experiments/ww14](#p117)
- [_Organized Desktop/05 Numbered Experiments/ww15](#p118)
- [_Organized Desktop/05 Numbered Experiments/ww18](#p121)
- [_Organized Desktop/05 Numbered Experiments/ww19](#p122)
- [_Organized Desktop/05 Numbered Experiments/ww26](#p123)
- [_Organized Desktop/05 Numbered Experiments/ww28](#p125)
- [_Organized Desktop/05 Numbered Experiments/ww29](#p126)
- [_Organized Desktop/05 Numbered Experiments/ww31](#p129)
- [_Organized Desktop/05 Numbered Experiments/ww34](#p131)
- [_Organized Desktop/05 Numbered Experiments/ww35](#p132)
- [_Organized Desktop/05 Numbered Experiments/ww36](#p133)
- [_Organized Desktop/05 Numbered Experiments/ww37](#p134)
- [_Organized Desktop/05 Numbered Experiments/ww39](#p135)
- [_Organized Desktop/05 Numbered Experiments/ww47](#p141)
- [_Organized Desktop/05 Numbered Experiments/ww49](#p143)
- [_Organized Desktop/05 Numbered Experiments/ww5](#p144)
- [_Organized Desktop/05 Numbered Experiments/ww6](#p147)
- [_Organized Desktop/05 Numbered Experiments/ww7](#p148)
- [_Organized Desktop/05 Numbered Experiments/ww8](#p149)
- [_Organized Desktop/05 Numbered Experiments/ww9](#p150)
- [_Organized Desktop/05 Numbered Experiments/z1](#p152)
- [_Organized Desktop/05 Numbered Experiments/zz1](#p158)
- [_Organized Desktop/05 Numbered Experiments/zz4](#p161)
- [_Organized Desktop/05 Numbered Experiments/zz55](#p162)
- [_Organized Desktop/05 Numbered Experiments/zz7](#p164)
- [_Organized Desktop/05 Numbered Experiments/zz8](#p165)
- [_Organized Desktop/06 AI And Learning/ai-observer-reference](#p167)
- [_Organized Desktop/07 Anti Projects/antiemponb](#p176)
- [_Organized Desktop/08 App And Product Projects/hnrandom](#p185)
- [campusops](#p231)
- [geminiorganized/General_Campusops](#p249)
- [geminiorganized/General_Globehire](#p258)
- [geminiorganized/General_Meterforge](#p264)
- [geminiorganized/General_Newcodecjs2](#p267)
- [geminiorganized/General_Newcodex3](#p268)
- [geminiorganized/General_Perch](#p274)
- [geminiorganized/General_Skillforgejs](#p279)
- [geminiorganized/LLM_Generated_Multitenantproject](#p301)
- [geminiorganized/LLM_Generated_Orderproject](#p302)
- [geminiorganized/OpenSource_Upskilling_.Stripe](#p308)
- [geminiorganized/OpenSource_Upskilling_Docu](#p310)
- [geminiorganized/OpenSource_Upskilling_Notion](#p314)
- [geminiorganized/OpenSource_Upskilling_Shop](#p315)
- [gitvg/agora](#p320)
- [gitvg/agora-net](#p321)
- [gitvg/atlas](#p323)
- [gitvg/atlas-net](#p324)
- [gitvg/bazaar-app](#p326)
- [gitvg/tracer-net](#p337)
- [globehire](#p338)
- [grokbuildmultitenantproject](#p342)
- [grokbuildorderproject](#p343)
- [meterforge](#p360)
- [netdocu](#p366)
- [netnotion](#p370)
- [netshop](#p374)
- [newcodecjs2](#p377)
- [newcodecjs2/blockr](#p460)
- [newcodecjs2/bookr](#p461)
- [newcodecjs2/payr](#p463)
- [newcodecjs2/planr](#p464)
- [newcodex3](#p378)
- [newcodex3/apps/17-kanban-board](#p392)
- [newcodex3/apps/17-kanban-board-net](#p393)
- [newcodex3/apps/19-ecommerce-storefront](#p396)
- [newcodex3/apps/19-ecommerce-storefront-net](#p397)
- [newcodex3/apps/20-event-booking](#p398)
- [newcodex3/apps/20-event-booking-net](#p399)
- [newcodex3/apps/21-invoicing-app](#p400)
- [newcodex3/apps/21-invoicing-app-net](#p401)
- [newcodex3/apps/22-team-wiki](#p402)
- [newcodex3/apps/22-team-wiki-net](#p403)
- [newcodex3/apps/23-survey-form-builder](#p404)
- [newcodex3/apps/23-survey-form-builder-net](#p405)
- [newcodex3/apps/25-discussion-forum](#p408)
- [newcodex3/apps/25-discussion-forum-net](#p409)
- [newcodex3/apps/26-subscription-reminders](#p410)
- [newcodex3/apps/26-subscription-reminders-net](#p411)
- [newcodex3/apps/27-ats-lite](#p412)
- [newcodex3/apps/27-ats-lite-net](#p413)
- [newcodex3/apps/28-restaurant-reservations](#p414)
- [newcodex3/apps/28-restaurant-reservations-net](#p415)
- [newcodex3/apps/29-personal-finance-dashboard](#p416)
- [newcodex3/apps/29-personal-finance-dashboard-net](#p417)
- [newcodex3/apps/32-helpdesk-ticketing](#p422)
- [newcodex3/apps/32-helpdesk-ticketing-net](#p423)
- [newcodex3/apps/33-inventory-warehouse-manager](#p424)
- [newcodex3/apps/33-inventory-warehouse-manager-net](#p425)
- [newcodex3/apps/35-analytics-reporting-dashboard](#p428)
- [newcodex3/apps/35-analytics-reporting-dashboard-net](#p429)
- [newcodex3/apps/37-bulk-import-review-tool](#p432)
- [newcodex3/apps/37-bulk-import-review-tool-net](#p433)
- [newcodexJS/13-ecommerce-storefront](#p452)
- [newcodexJS/14-appointment-booking](#p453)
- [newcodexJS/15-api-tester](#p454)
- [perch](#p381)
- [skillforgejs](#p386)

## Per-project improvement plans

<a id="p004"></a>
### .netstripe

A learning-oriented Stripe Billing / Chargebee style dashboard built with C#, .NET minimal APIs, and React.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Compact billing simulation; in-memory stores and workers are not durable payment infrastructure. Static review only; not built, tested or run.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/.netstripe/docs2/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of money units, state transitions and duplicate deliveries, an expected-state example and a guided-to-independent change exercise. Tie it to Money, idempotency, background payments, signed webhooks.
- **2 — Improve the project/resource:** First scoped project change: Test duplicate payment requests and then persist idempotency state. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/OpenSource_Upskilling_.Stripe](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_.Stripe). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/.netstripe/README.md), [Program.cs](C:/Users/Owner/Desktop/.netstripe/src/Billing.Api/Program.cs), [package.json](C:/Users/Owner/Desktop/.netstripe/src/Billing.Web/package.json).

---

<a id="p006"></a>
### _Organized Desktop/01 Net Workspaces/.netcalendy

A Calendly-style booking SaaS built with C# / .NET 9 and React.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Docker, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netcalendy/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to date/time modeling, interval conflicts, transactional booking, cancellation.
- **2 — Improve the project/resource:** First scoped project change: Test overlapping bookings and a daylight-saving boundary on one booking flow. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netcalendy/README.md), [Program.cs](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netcalendy/src/NetCalendy.Api/Program.cs), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netcalendy/web/src/App.tsx).

---

<a id="p007"></a>
### _Organized Desktop/01 Net Workspaces/.netgum

Netgum is a learning-oriented, clone of Gumroad built with C# and .NET 8.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** C#, ASP.NET Core, Entity Framework Core, SQL Server, Docker, GitHub Actions, xUnit.
- **Learning content now:** Developer explanation / brief orientation. Start at [architecture.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netgum/docs/architecture.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of availability and local-time conversion: ordered source files, one input-to-state trace, a diagram and one independent change targeting relational modeling, pricing, stock reservations, order state transitions.
- **2 — Improve the project/resource:** First scoped project change: Trace an order/reservation and test invalid transitions or repeated submissions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netgum/README.md), [Program.cs](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netgum/src/Netgum.Api/Program.cs), [Dockerfile](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netgum/src/Netgum.Api/Dockerfile).

---

<a id="p015"></a>
### _Organized Desktop/02 Build Projects/buildaffiliate

Multi-tenant platform connecting brands with affiliates: click tracking, attribution, commissions, fraud review, and payouts.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Fastify, Next.js, Node.js, React, Tailwind CSS, Prisma, Redis, Docker, GitHub Actions, Vitest, BullMQ.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildaffiliate/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of event identity, aggregation and reporting filters, an expected-state example and a guided-to-independent change exercise. Tie it to event modeling, aggregation, reporting queries, deduplication.
- **2 — Improve the project/resource:** First scoped project change: Validate one metric against a small hand-calculated dataset including duplicates. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildaffiliate/README.md), [error-handler.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildaffiliate/apps/api/src/lib/error-handler.ts), [server.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildaffiliate/apps/api/src/server.ts).

---

<a id="p019"></a>
### _Organized Desktop/02 Build Projects/buildanalytics

Full-stack internal dashboard platform for KPI tracking, operational analytics, audit visibility, monitoring dashboards, CSV exports, and role-aware internal operations workflows.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, SQL, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Redis, Docker, GitHub Actions, Playwright, Vitest, BullMQ.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildanalytics/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of step state, retries and adapter contracts, an expected-state example and a guided-to-independent change exercise. Tie it to state machines, workers, retry policies, idempotency, execution logs. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildanalytics/README.md), [auth.routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildanalytics/backend/src/modules/auth/auth.routes.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildanalytics/frontend/src/App.tsx).

---

<a id="p023"></a>
### _Organized Desktop/02 Build Projects/buildecom

MarketForge is a multi-vendor marketplace codebase.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Next.js, Node.js, React, Prisma, Redis, Playwright, Vitest, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildecom/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to relational modeling, pricing, stock reservations, order state transitions.
- **2 — Improve the project/resource:** First scoped project change: Trace an order/reservation and test invalid transitions or repeated submissions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildecom/README.md), [service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildecom/src/server/orders/service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildecom/package.json).

---

<a id="p026"></a>
### _Organized Desktop/02 Build Projects/buildScedulingPYJS

Full-stack scheduling platform scaffolded with React, TypeScript, Express, Prisma, PostgreSQL, Redis, BullMQ, JWT auth, RBAC, and scheduling-focused backend architecture.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, TypeScript, Express, Node.js, React, Vite, Prisma, Redis, Docker, GitHub Actions, Vitest, BullMQ.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FEATURE_WALKTHROUGHS.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildScedulingPYJS/FEATURE_WALKTHROUGHS.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to date/time modeling, interval conflicts, transactional booking, cancellation.
- **2 — Improve the project/resource:** First scoped project change: Test overlapping bookings and a daylight-saving boundary on one booking flow. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildScedulingPYJS/README.md), [auth.routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildScedulingPYJS/backend/src/modules/auth/auth.routes.ts), [server.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildScedulingPYJS/backend/src/server.ts).

---

<a id="p028"></a>
### _Organized Desktop/03 Master Projects/master

Personal planning app connecting areas, goals, projects, tasks, daily checklists, and time tracking.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, IndexedDB / Dexie, Prisma.
- **Learning content now:** Codebase walkthrough / study pack. Start at [prisma-seed.ts.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master/docs/intern/walkthroughs/prisma-seed.ts.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of step state, retries and adapter contracts, an expected-state example and a guided-to-independent change exercise. Tie it to state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master/README.md), [api.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master/src/lib/api.ts), [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/03%20Master%20Projects/master/src/lib/auth.ts).

---

<a id="p069"></a>
### _Organized Desktop/04 JavaScript Training/jsdrill_sync_20260223_125137

A Next.js app for deliberate JavaScript practice with spaced repetition, pattern tracking, and progress analytics.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Drizzle, SQLite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [01-schema.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jsdrill_sync_20260223_125137/training-docs/01-schema.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of event identity, aggregation and reporting filters, an expected-state example and a guided-to-independent change exercise. Tie it to event modeling, aggregation, reporting queries, deduplication.
- **2 — Improve the project/resource:** First scoped project change: Validate one metric against a small hand-calculated dataset including duplicates. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jsdrill_sync_20260223_125137/README.md), [fsrs.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jsdrill_sync_20260223_125137/src/lib/fsrs.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jsdrill_sync_20260223_125137/package.json).

---

<a id="p072"></a>
### _Organized Desktop/04 JavaScript Training/jstrain2

Workflow automation app with retries, queues, and execution logs; its README also documents an agent watchdog.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Drizzle, PostgreSQL, Redis, Docker, Playwright, Vitest, BullMQ.
- **Learning content now:** Codebase walkthrough / study pack. Start at [auth.ts.guide.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2/_learning/guides/src/auth.ts.guide.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of step state, retries and adapter contracts, an expected-state example and a guided-to-independent change exercise. Tie it to state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2/README.md), [route.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2/src/app/api/webhooks/incoming/%5BendpointId%5D/route.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2/package.json).

---

<a id="p075"></a>
### _Organized Desktop/04 JavaScript Training/jstrain2.4

Internal developer platform MVP inspired by Heroku/Vercel workflows.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, Next.js, Node.js, React, Tailwind CSS, Prisma.
- **Learning content now:** Codebase walkthrough / study pack. Start at [api.js.guide.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.4/_learning/guides/lib/api.js.guide.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of step state, retries and adapter contracts, an expected-state example and a guided-to-independent change exercise. Tie it to state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.4/README.md), [route.js](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.4/app/api/audit/route.js), [platform-service.js](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.4/lib/platform-service.js).

---

<a id="p076"></a>
### _Organized Desktop/04 JavaScript Training/jstrain3

Workspace with three DeskPilot variants; root README is a generic Next.js starter, so compare nested implementations before choosing one.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified. Limits: Fresh source check: root page is the default Next.js starter; deskpilot-clean auth selects a fixed seeded user, not a login session.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Redis, Docker.
- **Learning content now:** Codebase walkthrough / study pack. Start at [index.js.guide.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain3/deskpilot-clean/_learning/guides/worker/index.js.guide.md).
- **1 — Improve the upskilling content:** Replace generic root orientation with a comparison of deskpilot, deskpilot-app and deskpilot-clean; label fixed seeded identity.
- **2 — Improve the project/resource:** Choose one implemented variant and complete one flow there; replace demo identity only when introducing real user isolation.
- **3 — Prove completion:** Setup instructions open the chosen app rather than the default starter; its chosen flow works and identity limitations are explicit.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain3/README.md), [page.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain3/src/app/page.tsx), [auth.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain3/deskpilot-clean/src/lib/auth.ts).

---

<a id="p077"></a>
### _Organized Desktop/04 JavaScript Training/jstrain3.0

Ecommerce practice app with feature flags and experiments.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, Express, Node.js, React, Vite, SQLite.
- **Learning content now:** No substantive guide verified. No populated entrypoint verified in the tutorial review.
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of deterministic targeting and configuration versions, known stubs and one exercise targeting rule evaluation, rollout consistency, cache invalidation, audit history. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Test deterministic targeting, rollback, and stale configuration behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Evaluate fixed subjects repeatedly across two environments; verify stable assignments, environment isolation and an explicit rollback result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [auth.js](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain3.0/server/src/routes/auth.js), [App.jsx](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain3.0/client/src/App.jsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain3.0/package.json).

---

<a id="p083"></a>
### _Organized Desktop/05 Numbered Experiments/B1

Incident-response workspace with runbooks and incident-management components.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/B1/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of event identity, aggregation and reporting filters, known stubs and one exercise targeting event schemas, ingestion, aggregation, alerting, operational failure states. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace one event or check into a dashboard and test duplicate/missing/late data. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/B1/README.md), [http.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/B1/src/lib/http.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/B1/package.json).

---

<a id="p087"></a>
### _Organized Desktop/05 Numbered Experiments/e1

Pulseboard Scheduler is a dependency-light Next.js foundation for a Cal.com-style scheduling SaaS.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Teaching app with documented in-memory/mock persistence; database/schema claims do not establish durable storage. Runtime unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Redis, Docker.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e1/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to date/time modeling, interval conflicts, transactional booking, cancellation.
- **2 — Improve the project/resource:** First scoped project change: Test overlapping bookings and a daylight-saving boundary on one booking flow. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e1/README.md), [proxy.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e1/src/proxy.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e1/package.json).

---

<a id="p089"></a>
### _Organized Desktop/05 Numbered Experiments/e12

A dependency-light reference implementation of a multi-project feature flag platform.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e12/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of deterministic targeting and configuration versions, an expected-state example and a guided-to-independent change exercise. Tie it to rule evaluation, rollout consistency, cache invalidation, audit history.
- **2 — Improve the project/resource:** First scoped project change: Test deterministic targeting, rollback, and stale configuration behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Evaluate fixed subjects repeatedly across two environments; verify stable assignments, environment isolation and an explicit rollback result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e12/README.md), [services.js](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e12/src/server/services.js), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e12/package.json).

---

<a id="p090"></a>
### _Organized Desktop/05 Numbered Experiments/e13

Headless commerce practice platform with multiple sales-channel concepts.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, SQLite, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e13/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to relational modeling, pricing, stock reservations, order state transitions.
- **2 — Improve the project/resource:** First scoped project change: Trace an order/reservation and test invalid transitions or repeated submissions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e13/README.md), [env.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e13/src/lib/env.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e13/package.json).

---

<a id="p091"></a>
### _Organized Desktop/05 Numbered Experiments/e14

Single-node MVP for a multi-tenant observability platform covering logs, metrics, traces, dashboards, alerts, and pipelines.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Recorded stack:** Python, FastAPI, SQLAlchemy, pytest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e14/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of event identity, aggregation and reporting filters, an expected-state example and a guided-to-independent change exercise. Tie it to event schemas, ingestion, aggregation, alerting, operational failure states.
- **2 — Improve the project/resource:** First scoped project change: Trace one event or check into a dashboard and test duplicate/missing/late data. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e14/README.md), [auth.py](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e14/app/services/auth.py), [main.py](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e14/app/main.py).

---

<a id="p096"></a>
### _Organized Desktop/05 Numbered Experiments/e3

Signal Desk is a PostHog-style product analytics MVP built with Next.js, React, TypeScript, and Node-style server modules.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, TypeScript, Next.js, Node.js, React, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [00-codebase-map.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e3/docs/onboarding/00-codebase-map.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of event identity, aggregation and reporting filters, an expected-state example and a guided-to-independent change exercise. Tie it to event modeling, aggregation, reporting queries, deduplication.
- **2 — Improve the project/resource:** First scoped project change: Validate one metric against a small hand-calculated dataset including duplicates. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e3/README.md), [page.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e3/app/page.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/e3/package.json).

---

<a id="p108"></a>
### _Organized Desktop/05 Numbered Experiments/w22

Next.js App Router application that teaches payment-system correctness through a service and repository split.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w22/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of money units, state transitions and duplicate deliveries: ordered source files, one input-to-state trace, a diagram and one independent change targeting money arithmetic, idempotency, webhook processing, transaction boundaries.
- **2 — Improve the project/resource:** First scoped project change: Read schema, permissions, paymentService, webhookService, reconciliationService in that order; test replayed creation and late provider events. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w22/docs/architecture/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w22/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w22/package.json).

---

<a id="p110"></a>
### _Organized Desktop/05 Numbered Experiments/w24

Learning project for dynamic product behavior: versioned JSON configs, runtime rule evaluation, safe rollout, rollback, audit history, caching, and an admin UI that explains why a rule applied.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w24/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of deterministic targeting and configuration versions: ordered source files, one input-to-state trace, a diagram and one independent change targeting rule evaluation, rollout consistency, cache invalidation, audit history.
- **2 — Improve the project/resource:** First scoped project change: Test deterministic targeting, rollback, and stale configuration behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Evaluate fixed subjects repeatedly across two environments; verify stable assignments, environment isolation and an explicit rollback result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w24/README.md), [audit-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w24/src/services/audit-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w24/package.json).

---

<a id="p111"></a>
### _Organized Desktop/05 Numbered Experiments/w25

Backend-heavy Next.js application that teaches distributed locking through a web product shape.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Teaching implementation with documented simulated/demo boundaries; runtime unverified. Limits: Architecture explicitly uses mockStore and x-demo-user-id; Prisma schema describes the production-shaped model, not deployed persistence.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w25/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting concurrency, leases, ownership tokens, failure recovery.
- **2 — Improve the project/resource:** First scoped project change: Study acquire/renew/release invariants, then compare ww26 for actual Prisma-backed locking boundaries. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w25/docs/architecture/README.md), [lockService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w25/src/services/lockService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/w25/package.json).

---

<a id="p112"></a>
### _Organized Desktop/05 Numbered Experiments/ww1

Workforce Access Ops combines Employer of Record workflows with identity and entitlement management in one multi-tenant SaaS codebase.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww1/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of step state, retries and adapter contracts: ordered source files, one input-to-state trace, a diagram and one independent change targeting state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww1/docs/architecture/README.md), [workerService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww1/src/services/workerService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww1/package.json).

---

<a id="p113"></a>
### _Organized Desktop/05 Numbered Experiments/ww10

Loan origination and underwriting platform built with Next.js, TypeScript, PostgreSQL, Prisma, Tailwind, Zod, React Query, and REST APIs.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, PostgreSQL, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww10/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting code navigation, contracts, validation, testing; lifecycle transitions, scoped approvals and workflow invariants.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww10/README.md), [route-handler.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww10/src/lib/http/route-handler.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww10/package.json).

---

<a id="p114"></a>
### _Organized Desktop/05 Numbered Experiments/ww11

Next.js + TypeScript clinical trial participant tracking system with a backend-centered design.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww11/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting code navigation, contracts, validation, testing; lifecycle transitions, scoped approvals and workflow invariants.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww11/docs/architecture/README.md), [auditService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww11/src/services/auditService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww11/package.json).

---

<a id="p116"></a>
### _Organized Desktop/05 Numbered Experiments/ww13

FluxGrant is a grant and funding lifecycle management platform built as a learning artifact for backend-oriented product engineering.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Teaching app with documented in-memory/mock persistence; database/schema claims do not establish durable storage. Runtime unverified. Limits: README explicitly states Prisma/PostgreSQL/Zod/React Query were intentionally not installed; actual teaching implementation uses in-memory repositories and handwritten validation.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww13/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting code navigation, contracts, validation, testing; lifecycle transitions, scoped approvals and workflow invariants.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww13/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww13/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww13/package.json).

---

<a id="p117"></a>
### _Organized Desktop/05 Numbered Experiments/ww14

Multi-tenant learning management system focused on backend-oriented product engineering.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [guided-reading-path.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww14/docs/learning/guided-reading-path.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for eligibility, progress and completion transitions; make learners predict state before running it. Teach enrollment/progress data, scoped permissions, policy rules, modular services with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace one enrollment-to-completion flow and test an ineligible certification. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an ineligible completion; repeat a valid progress event and verify progress and any certificate/review state remain consistent.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww14/docs/architecture/README.md), [courseService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww14/src/services/courseService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww14/package.json).

---

<a id="p118"></a>
### _Organized Desktop/05 Numbered Experiments/ww15

ClosingHub is a Next.js App Router application for real estate transaction and deal management.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww15/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting code navigation, contracts, validation, testing; lifecycle transitions, scoped approvals and workflow invariants.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww15/docs/architecture/README.md), [listing-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww15/src/services/listing-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww15/package.json).

---

<a id="p121"></a>
### _Organized Desktop/05 Numbered Experiments/ww18

Tenant-aware quote-to-cash application built to teach backend product engineering.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww18/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, ordering and lifecycle transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting relational data, lifecycle transitions, tenant-scoped queries, audit history; lifecycle transitions, scoped approvals and workflow invariants.
- **2 — Improve the project/resource:** First scoped project change: Trace a lead/deal transition and test tenant isolation plus invalid transitions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww18/docs/architecture/README.md), [order-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww18/src/services/order-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww18/package.json).

---

<a id="p122"></a>
### _Organized Desktop/05 Numbered Experiments/ww19

Flowkeeper is a Temporal-lite orchestration app built as one Next.js codebase with a separate worker entrypoint.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww19/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of step state, retries and adapter contracts: ordered source files, one input-to-state trace, a diagram and one independent change targeting state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww19/docs/architecture/README.md), [auth-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww19/src/services/auth-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww19/package.json).

---

<a id="p123"></a>
### _Organized Desktop/05 Numbered Experiments/ww26

Locksmith Dashboard is a Next.js application that teaches distributed coordination with a database-backed lock manager, explicit RBAC, and an operational dashboard.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww26/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting concurrency, leases, ownership tokens, failure recovery.
- **2 — Improve the project/resource:** First scoped project change: After w25, trace lockCoordinatorService through lockScopeRepository row locking and lockLeaseRepository; test stale ownership and contention. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww26/docs/architecture/README.md), [dashboardService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww26/src/services/dashboardService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww26/package.json).

---

<a id="p125"></a>
### _Organized Desktop/05 Numbered Experiments/ww28

Learning scaffold for a distributed file storage system with tenant isolation, multipart uploads, retries, signed downloads, quota tracking, and duplicated chunk storage.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww28/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, upload/finalization state and storage boundaries: ordered source files, one input-to-state trace, a diagram and one independent change targeting file validation, access control, asynchronous processing, retries.
- **2 — Improve the project/resource:** First scoped project change: Trace one upload through storage and processing; specify retry and access-denial cases. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Try an unauthorized or expired operation and an interrupted retry; verify no orphaned committed state or double quota charge.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww28/docs/architecture/README.md), [fileService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww28/src/services/fileService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww28/package.json).

---

<a id="p126"></a>
### _Organized Desktop/05 Numbered Experiments/ww29

Next.js application for sending queued notifications over email, SMS, and push with retry logic, delivery history, user preferences, rate limiting, and an admin monitoring surface.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, PostgreSQL, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww29/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of event identity, aggregation and reporting filters: ordered source files, one input-to-state trace, a diagram and one independent change targeting event schemas, ingestion, aggregation, alerting, operational failure states.
- **2 — Improve the project/resource:** First scoped project change: Trace one event or check into a dashboard and test duplicate/missing/late data. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww29/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww29/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww29/package.json).

---

<a id="p129"></a>
### _Organized Desktop/05 Numbered Experiments/ww31

Flagship is a Next.js control plane for runtime feature rollout.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww31/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of deterministic targeting and configuration versions: ordered source files, one input-to-state trace, a diagram and one independent change targeting rule evaluation, rollout consistency, cache invalidation, audit history.
- **2 — Improve the project/resource:** First scoped project change: Test deterministic targeting, rollback, and stale configuration behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Evaluate fixed subjects repeatedly across two environments; verify stable assignments, environment isolation and an explicit rollback result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww31/docs/architecture/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww31/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww31/package.json).

---

<a id="p131"></a>
### _Organized Desktop/05 Numbered Experiments/ww34

StayBound is a Next.js App Router application for searching listings, requesting bookings, approving stays, capturing mock payments, applying cancellation policies, and creating post-stay reviews.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww34/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of availability and local-time conversion: ordered source files, one input-to-state trace, a diagram and one independent change targeting money arithmetic, idempotency, webhook processing, transaction boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace a charge or webhook and design a replay test that cannot double-apply it. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww34/docs/architecture/README.md), [reviewService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww34/src/services/reviewService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww34/package.json).

---

<a id="p132"></a>
### _Organized Desktop/05 Numbered Experiments/ww35

Appointment-booking application.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww35/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of availability and local-time conversion: ordered source files, one input-to-state trace, a diagram and one independent change targeting date/time modeling, interval conflicts, transactional booking, cancellation.
- **2 — Improve the project/resource:** First scoped project change: Test overlapping bookings and a daylight-saving boundary on one booking flow. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww35/docs/architecture/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww35/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww35/package.json).

---

<a id="p133"></a>
### _Organized Desktop/05 Numbered Experiments/ww36

Single-store inventory reservation app.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww36/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of availability and local-time conversion: ordered source files, one input-to-state trace, a diagram and one independent change targeting relational modeling, pricing, stock reservations, order state transitions.
- **2 — Improve the project/resource:** First scoped project change: Trace an order/reservation and test invalid transitions or repeated submissions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww36/docs/architecture/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww36/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww36/package.json).

---

<a id="p134"></a>
### _Organized Desktop/05 Numbered Experiments/ww37

This app is a small-store inventory reservation system built around three core workflows: create a hold, release a hold, and keep low-stock alerts in sync when inventory changes.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Teaching app with documented in-memory/mock persistence; database/schema claims do not establish durable storage. Runtime unverified. Limits: Fresh architecture review explicitly confirms mocked in-memory persistence and fake session headers. Use it for business rules; use a durable follow-on for concurrency claims.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww37/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of availability and local-time conversion: ordered source files, one input-to-state trace, a diagram and one independent change targeting relational modeling, pricing, stock reservations, order state transitions.
- **2 — Improve the project/resource:** First scoped project change: Test hold/release invariants in the small in-memory app; then compare ww36 or implement durable transactional storage. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww37/docs/architecture/README.md), [alertService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww37/src/services/alertService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww37/package.json).

---

<a id="p135"></a>
### _Organized Desktop/05 Numbered Experiments/ww39

Support-ticket workflow application with service and repository layers.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww39/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of step state, retries and adapter contracts: ordered source files, one input-to-state trace, a diagram and one independent change targeting state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww39/docs/architecture/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww39/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww39/package.json).

---

<a id="p141"></a>
### _Organized Desktop/05 Numbered Experiments/ww47

Next.js application for event ingestion, daily aggregation jobs, and protected analytics views.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww47/docs/mission-learning-path/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for event identity, aggregation and reporting filters; make learners predict state before running it. Teach event modeling, aggregation, reporting queries, deduplication with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Validate one metric against a small hand-calculated dataset including duplicates. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww47/README.md), [auth-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww47/src/services/auth-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww47/package.json).

---

<a id="p143"></a>
### _Organized Desktop/05 Numbered Experiments/ww49

Order-operations dashboard with coupons, fulfillment, refunds, and audit services.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww49/docs2/mission-learning-path/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for availability and local-time conversion; make learners predict state before running it. Teach relational modeling, pricing, stock reservations, order state transitions with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace an order/reservation and test invalid transitions or repeated submissions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww49/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww49/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww49/package.json).

---

<a id="p144"></a>
### _Organized Desktop/05 Numbered Experiments/ww5

Workday-like enterprise People + Operations platform with explicit backend boundaries for employees, org hierarchy, compensation workflow, approvals, tasks, reporting, audit logs, and admin settings.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww5/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of step state, retries and adapter contracts: ordered source files, one input-to-state trace, a diagram and one independent change targeting state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww5/docs/architecture/README.md), [taskService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww5/src/services/taskService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww5/package.json).

---

<a id="p147"></a>
### _Organized Desktop/05 Numbered Experiments/ww6

Cloud-cost allocation and chargeback dashboard.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww6/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of event identity, aggregation and reporting filters: ordered source files, one input-to-state trace, a diagram and one independent change targeting event modeling, aggregation, reporting queries, deduplication.
- **2 — Improve the project/resource:** First scoped project change: Validate one metric against a small hand-calculated dataset including duplicates. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww6/README.md), [budgetService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww6/src/services/budgetService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww6/package.json).

---

<a id="p148"></a>
### _Organized Desktop/05 Numbered Experiments/ww7

FlowForge is a learning project for workflow automation.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww7/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of step state, retries and adapter contracts: ordered source files, one input-to-state trace, a diagram and one independent change targeting state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww7/README.md), [auth-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww7/src/services/auth-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww7/package.json).

---

<a id="p149"></a>
### _Organized Desktop/05 Numbered Experiments/ww8

LedgerFlow is a document processing pipeline built with Next.js, TypeScript, Prisma, PostgreSQL, Zod, Tailwind, and React Query.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww8/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, upload/finalization state and storage boundaries: ordered source files, one input-to-state trace, a diagram and one independent change targeting file validation, access control, asynchronous processing, retries.
- **2 — Improve the project/resource:** First scoped project change: Trace one upload through storage and processing; specify retry and access-denial cases. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Try an unauthorized or expired operation and an interrupted retry; verify no orphaned committed state or double quota charge.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww8/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww8/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww8/package.json).

---

<a id="p150"></a>
### _Organized Desktop/05 Numbered Experiments/ww9

WW9 is a scheduling and booking engine built with Next.js, TypeScript, Prisma, PostgreSQL, React Query, Tailwind, and Zod.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww9/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of availability and local-time conversion: ordered source files, one input-to-state trace, a diagram and one independent change targeting date/time modeling, interval conflicts, transactional booking, cancellation.
- **2 — Improve the project/resource:** First scoped project change: Test overlapping bookings and a daylight-saving boundary on one booking flow. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww9/README.md), [bookingService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww9/src/services/bookingService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/ww9/package.json).

---

<a id="p152"></a>
### _Organized Desktop/05 Numbered Experiments/z1

Internal request-and-approval workflow application with mocked infrastructure.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Prisma.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z1/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of step state, retries and adapter contracts, an expected-state example and a guided-to-independent change exercise. Tie it to state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z1/README.md), [admin-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z1/src/lib/services/admin-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z1/package.json).

---

<a id="p158"></a>
### _Organized Desktop/05 Numbered Experiments/zz1

Multi-tenant CRM with deal workflows and service-layer authorization.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz1/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of step state, retries and adapter contracts: ordered source files, one input-to-state trace, a diagram and one independent change targeting state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz1/docs/architecture/README.md), [jobService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz1/src/services/jobService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz1/package.json).

---

<a id="p161"></a>
### _Organized Desktop/05 Numbered Experiments/zz4

A enterprise workflow app for access requests, purchase requests, onboarding requests, and policy exceptions.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, PostgreSQL, Prisma, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz4/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of step state, retries and adapter contracts, an expected-state example and a guided-to-independent change exercise. Tie it to state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz4/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz4/zz4/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz4/package.json).

---

<a id="p162"></a>
### _Organized Desktop/05 Numbered Experiments/zz55

OpsPilot is a learning project that combines subscription billing administration with employee onboarding operations.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz55/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of money units, state transitions and duplicate deliveries: ordered source files, one input-to-state trace, a diagram and one independent change targeting money arithmetic, idempotency, webhook processing, transaction boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace a charge or webhook and design a replay test that cannot double-apply it. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz55/README.md), [jobService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz55/src/services/jobService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz55/package.json).

---

<a id="p164"></a>
### _Organized Desktop/05 Numbered Experiments/zz7

Procurement dashboard for vendors, sourcing, purchase orders, and reporting.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz7/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of event identity, aggregation and reporting filters: ordered source files, one input-to-state trace, a diagram and one independent change targeting code navigation, contracts, validation, testing; lifecycle transitions, scoped approvals and workflow invariants.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz7/README.md), [authService.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz7/src/services/authService.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz7/package.json).

---

<a id="p165"></a>
### _Organized Desktop/05 Numbered Experiments/zz8

HRIS and employee-performance review workflows in one workspace.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, PostgreSQL, Prisma, Docker, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz8/docs/architecture/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of step state, retries and adapter contracts: ordered source files, one input-to-state trace, a diagram and one independent change targeting state machines, workers, retry policies, idempotency, execution logs.
- **2 — Improve the project/resource:** First scoped project change: Specify a workflow retry after a partial failure and add one focused recovery test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Inject a partial failure and retry with a fake adapter; verify completed effects are not repeated and retry attempts are bounded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz8/README.md), [review-service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz8/src/services/review-service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/zz8/package.json).

---

<a id="p167"></a>
### _Organized Desktop/06 AI And Learning/ai-observer-reference

Track token usage, costs, API latency, error rates, and session activity across all your AI coding assistants in one unified dashboard—with real-time updates and zero external dependencies.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, Go, HTML, JavaScript, TypeScript, React, Tailwind CSS, Vite, Docker, GitHub Actions, Vitest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/ai-observer-reference/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of event identity, aggregation and reporting filters, known stubs and one exercise targeting telemetry collection, event normalization, metrics, operational dashboards. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace a session event into usage metrics and test duplicate-event handling. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/ai-observer-reference/README.md), [routes.go](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/ai-observer-reference/backend/internal/server/routes.go), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/ai-observer-reference/frontend/src/App.tsx).

---

<a id="p176"></a>
### _Organized Desktop/07 Anti Projects/antiemponb

Welcome to the HRFlow Onboarding Platform Educational Lab.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, SQL, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Redis, Docker, Vitest, BullMQ.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antiemponb/docsclaude/04-architecture-and-patterns/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of employee lifecycle, approval and tenant scope: ordered source files, one input-to-state trace, a diagram and one independent change targeting onboarding workflows, authorization, module boundaries, audit history.
- **2 — Improve the project/resource:** First scoped project change: Trace one onboarding step and test invalid ordering and unauthorized completion. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antiemponb/docsclaude/README.md), [auth.routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antiemponb/backend/src/modules/auth/auth.routes.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antiemponb/frontend/src/App.tsx).

---

<a id="p185"></a>
### _Organized Desktop/08 App And Product Projects/hnrandom

AI Observer is a self-hosted observability backend and dashboard for AI coding workflows.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: One complete authenticated app; transactions, test isolation, and failure handling.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Docker, GitHub Actions, Vitest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/hnrandom/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of event identity, aggregation and reporting filters, known stubs and one exercise targeting observability ingestion, aggregation, diagnostics, dashboards. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace one telemetry event and verify how duplicates and errors affect metrics. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/hnrandom/README.md), [routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/hnrandom/backend/src/api/routes.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/hnrandom/frontend/src/App.tsx).

---

<a id="p231"></a>
### campusops

CampusOps is a fifteen-sprint teaching repository for learning business-heavy C#/.NET API development and React/TypeScript integration through a university facilities platform.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Fifteen-sprint .NET/React teaching repository. Default API storage is non-durable. X-Demo-Role and X-Demo-Campus are client-supplied teaching authentication headers; policy rejection is not proof of real identity. SQLite adapters are exercises. Static review only; not built, tested or run.
- **Recorded stack:** C#, CSS, HTML, SQL, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, SQLite, GitHub Actions, Vitest, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/campusops/README.md).
- **1 — Improve the upskilling content:** Turn one facilities request into a UI-to-domain-to-repository lesson; distinguish client-supplied demo campus/role headers from verified identity.
- **2 — Improve the project/resource:** Complete one facilities request approval flow with a persistent repository. Treat real session-based campus membership as a separate access-control milestone.
- **3 — Prove completion:** A valid approval is retained after restart and an invalid transition is rejected. For the identity milestone, prove a client cannot gain another campus by changing a header.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Campusops](C:/Users/Owner/Desktop/geminiorganized/General_Campusops). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/campusops/README.md), [Program.cs](C:/Users/Owner/Desktop/campusops/src/CampusOps.Api/Program.cs), [package.json](C:/Users/Owner/Desktop/campusops/web/CampusOps.Web/package.json).

---

<a id="p249"></a>
### geminiorganized/General_Campusops

CampusOps is a fifteen-sprint teaching repository for learning business-heavy C#/.NET API development and React/TypeScript integration through a university facilities platform.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Relevant implementation is present; runtime not verified. Local documentation: CampusOps.Infrastructure in-memory, SQLite, and integration adapters
- **Recorded stack:** C#, CSS, HTML, SQL, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, SQLite, GitHub Actions, Vitest, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Campusops/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Business API workflows, React integration, persistence, operations with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: After BorrowBox, implement one facilities workflow end to end with tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [campusops](C:/Users/Owner/Desktop/campusops). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Campusops/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Campusops/web/CampusOps.Web/package.json), [CampusOps.Api.csproj](C:/Users/Owner/Desktop/geminiorganized/General_Campusops/src/CampusOps.Api/CampusOps.Api.csproj).

---

<a id="p258"></a>
### geminiorganized/General_Globehire

GlobeHire is a fifteen-sprint C#/.NET teaching repository for a fictional global workforce and employer-of-record platform.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Relevant implementation is present; runtime not verified. Local documentation: Infrastructure adapters (in-memory teaching adapters today); Use the HTTP examples, inspect /openapi/v1.json in Development, and check /health/live and /health/ready. The readiness response intentionally discloses that storage is in-memory and non-durable.
- **Recorded stack:** C#, ASP.NET Core, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Globehire/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for employee lifecycle, approval and tenant scope; make learners predict state before running it. Teach Versioned rules, lifecycle changes, integration ports, API contracts with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: After CampusOps, change one fictional country rule without breaking API contracts. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [globehire](C:/Users/Owner/Desktop/globehire). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Globehire/README.md), [GlobeHire.Api.csproj](C:/Users/Owner/Desktop/geminiorganized/General_Globehire/src/GlobeHire.Api/GlobeHire.Api.csproj), [GlobeHire.Application.csproj](C:/Users/Owner/Desktop/geminiorganized/General_Globehire/src/GlobeHire.Application/GlobeHire.Application.csproj).

---

<a id="p264"></a>
### geminiorganized/General_Meterforge

MeterForge is a fifteen-sprint C#/.NET teaching repository for a fictional multi-tenant usage-based subscription billing platform.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Relevant implementation is present; runtime not verified. Local documentation: In-memory, PostgreSQL, and simulated provider adapters; OpenAPI is available at /openapi/v1.json in Development. Check /health/live and /health/ready; readiness explicitly reports that the default runtime uses non-durable in-memory adapters. docker compose up postgres starts the local database used by the PostgreSQL adapter exercise.
- **Recorded stack:** C#, SQL, ASP.NET Core, PostgreSQL, Docker, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Meterforge/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for money units, state transitions and duplicate deliveries; make learners predict state before running it. Teach Money invariants, idempotency, concurrency, outbox, integrations with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: After CampusOps, prove duplicate usage does not double bill, then use a durable adapter. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [meterforge](C:/Users/Owner/Desktop/meterforge). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Meterforge/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/General_Meterforge/docker-compose.yml), [MeterForge.Api.csproj](C:/Users/Owner/Desktop/geminiorganized/General_Meterforge/src/MeterForge.Api/MeterForge.Api.csproj).

---

<a id="p267"></a>
### geminiorganized/General_Newcodecjs2

This workspace contains five separate learning codebases generated from the pasted SaaS clone specs.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Static sample does not establish runtime readiness. Local documentation: Each project is intentionally scaffolded as a production-shaped TypeScript/React/Node app, but it is not wired for installation or deployment. The goal is reading, tracing, and modifying the architecture.
- **Recorded stack:** TypeScript, Next.js, Node.js, React, Vite, Drizzle, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Newcodecjs2/payr/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting Focused domain algorithms, policy checks, optimistic state and integration boundaries..
- **2 — Improve the project/resource:** First scoped project change: Choose one child by missing skill and turn one domain behavior into an independently verified vertical slice. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [newcodecjs2](C:/Users/Owner/Desktop/newcodecjs2). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Newcodecjs2/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Newcodecjs2/payr/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Newcodecjs2/blockr/package.json).

---

<a id="p268"></a>
### geminiorganized/General_Newcodex3

This workspace contains five learning projects built with JavaScript, React, TypeScript, and Node patterns.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** C#, CSS, HTML, TypeScript, Express, Node.js, React, Vite, Prisma, Redis, Vitest, Socket.IO.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/geminiorganized/General_Newcodex3/apps/27-ats-lite/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Compare equivalent domain patterns across TypeScript and C#; study one difficult invariant at a time. with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Choose one topic and one language implementation; document gaps between scaffold code and production notes before extending it. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Newcodex3/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Newcodex3/apps/27-ats-lite/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Newcodex3/package.json).

---

<a id="p274"></a>
### geminiorganized/General_Perch

Perch is a Greenhouse/Lever-style applicant tracking system and a teaching repository for junior engineers.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Static sample does not establish runtime readiness. Local documentation: Ports --> Memory[Deterministic in-memory adapters]; - packages/db: repository contracts, in-memory adapters, Prisma schema, demo seed.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Fastify, Node.js, React, Vite, Prisma, GitHub Actions, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [LEARNER-GUIDE.md](C:/Users/Owner/Desktop/geminiorganized/General_Perch/LEARNER-GUIDE.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ownership, ordering and lifecycle transitions; make learners predict state before running it. Teach Multi-actor workflow, object authorization, state machines, bulk actions, ports/adapters and test design. with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Follow one sprint playbook and implement a persistent repository adapter while retaining the authorization tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [perch](C:/Users/Owner/Desktop/perch). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Perch/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Perch/package.json), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Perch/apps/api/package.json).

---

<a id="p279"></a>
### geminiorganized/General_Skillforgejs

Skillforge is a web-first coding-skills learning platform built with Next.js App Router, TypeScript, Prisma/PostgreSQL, Auth.js, Tailwind, CodeMirror, server-side spaced repetition, and gamification.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Docker, GitHub Actions, Playwright, Vitest, Stripe.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Skillforgejs/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of eligibility, progress and completion transitions, an expected-state example and a guided-to-independent change exercise. Tie it to App Router/server boundaries, Prisma, content schema validation, pure scheduling logic and tests..
- **2 — Improve the project/resource:** First scoped project change: Trace lesson completion into review state and add a deterministic scheduler/transaction test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an ineligible completion; repeat a valid progress event and verify progress and any certificate/review state remain consistent.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [skillforgejs](C:/Users/Owner/Desktop/skillforgejs). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Skillforgejs/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Skillforgejs/docs/upskill/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Skillforgejs/package.json).

---

<a id="p301"></a>
### geminiorganized/LLM_Generated_Multitenantproject

A full-stack Multi-Tenant SaaS Starter built for educational purposes to upskill to mid/senior SWE level.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Vite, Prisma, Docker.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Multitenantproject/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Tenant isolation, organization roles, scoped queries with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Add a test proving one tenant cannot access another tenant's project. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [grokbuildmultitenantproject](C:/Users/Owner/Desktop/grokbuildmultitenantproject). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Multitenantproject/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Multitenantproject/docker-compose.yml), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Multitenantproject/backend/package.json).

---

<a id="p302"></a>
### geminiorganized/LLM_Generated_Orderproject

Full-stack Order Management / Operations Platform (Educational)

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Jest, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [JOURNAL.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Orderproject/JOURNAL.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for stock ownership, checkout and order transitions; make learners predict state before running it. Teach Inventory, order transitions, transactional integrity with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace one inventory update and test rollback on failure. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [grokbuildorderproject](C:/Users/Owner/Desktop/grokbuildorderproject). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Orderproject/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Orderproject/docker-compose.yml), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Orderproject/backend/package.json).

---

<a id="p308"></a>
### geminiorganized/OpenSource_Upskilling_.Stripe

A learning-oriented Stripe Billing / Chargebee style dashboard built with C#, .NET minimal APIs, and React.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Teaching/reference workspace; runtime not verified. Local documentation: The backend uses an in-memory store so the project stays dependency-free and easy to study. In a production system, the store boundary is where a relational database, durable job queue, distributed idempotency table, and transactional outbox would be added.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_.Stripe/docs2/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of money units, state transitions and duplicate deliveries, an expected-state example and a guided-to-independent change exercise. Tie it to Money, idempotency, background payments, signed webhooks.
- **2 — Improve the project/resource:** First scoped project change: Test duplicate payment requests and then persist idempotency state. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [.netstripe](C:/Users/Owner/Desktop/.netstripe). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_.Stripe/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_.Stripe/docs2/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_.Stripe/src/Billing.Web/package.json).

---

<a id="p310"></a>
### geminiorganized/OpenSource_Upskilling_Docu

NetDocu is a DocuSign-style signing workflow application with a .NET 8 clean-architecture API, PostgreSQL persistence, JWT/refresh-token auth, and a React + TypeScript signing workspace.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Teaching/reference workspace; runtime not verified. Local documentation: The initial test scaffold enforces core project reference direction:
- **Recorded stack:** C#, CSS, HTML, JavaScript, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Docu/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Document permissions, workflow state transitions, audit events, background processing. with a separate answer and rubric. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace document creation to envelope completion; verify one unauthorized recipient and duplicate submission scenario. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [netdocu](C:/Users/Owner/Desktop/netdocu). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Docu/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Docu/frontend/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Docu/docker-compose.yml).

---

<a id="p314"></a>
### geminiorganized/OpenSource_Upskilling_Notion

NetNotion is a Notion-style collaborative docs/wiki app built with .NET 8 Web API, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Teaching/reference workspace; runtime not verified.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Notion/docs/fable/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of tree structure, revisions and inherited permissions, an expected-state example and a guided-to-independent change exercise. Tie it to Recursive page trees, inherited permissions, block batching and immutable versions.. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace page sharing and version restore; add an inherited-permission regression and reject tree cycles. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file. docs/fable is substantive; the sampled docs/upskill README is explicitly unfilled.
- **Related locations to compare:** [netnotion](C:/Users/Owner/Desktop/netnotion). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Notion/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Notion/docs/fable/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Notion/docker-compose.yml).

---

<a id="p315"></a>
### geminiorganized/OpenSource_Upskilling_Shop

NetShopifyLite is a .NET 8 + React ecommerce admin and lightweight storefront scaffold.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Teaching/reference workspace; runtime not verified. Local documentation: NetShopifyLite is a .NET 8 + React ecommerce admin and lightweight storefront scaffold. It follows a layered architecture:
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Shop/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for stock ownership, checkout and order transitions; make learners predict state before running it. Teach Money modeling, transactional inventory, idempotent checkout/refunds and domain invariants. with a separate answer and rubric. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Prove duplicate checkout/refund behavior and stock consistency with a real persistence integration test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [netshop](C:/Users/Owner/Desktop/netshop). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Shop/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Shop/docs/upskill/README.md), [docker-compose.yml](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Shop/docker-compose.yml).

---

<a id="p320"></a>
### gitvg/agora

Single-store e-commerce teaching application with customer catalog/cart/checkout flows and an administrative back office.

- **Use / order:** Primary route candidate; complete this milestone before adding an alternative. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** C#/.NET plus React teaching repository; not simply the TypeScript version of agora-net. Static review only; not built, tested or run.
- **Recorded stack:** C#, CSS, HTML, JavaScript, TypeScript, ASP.NET Core, React, Tailwind CSS, Vite, Entity Framework Core, PostgreSQL, SQLite, Docker, GitHub Actions, Vitest, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [LEARNER-GUIDE.md](C:/Users/Owner/Desktop/gitvg/agora/LEARNER-GUIDE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to Commerce invariants, C# application layers, React, transactions.
- **2 — Improve the project/resource:** First scoped project change: Follow one checkout slice and add a stock-reservation test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/agora/README.md), [Program.cs](C:/Users/Owner/Desktop/gitvg/agora/src/Agora.Api/Program.cs), [docker-compose.yml](C:/Users/Owner/Desktop/gitvg/agora/docker-compose.yml).

---

<a id="p321"></a>
### gitvg/agora-net

C#/.NET e-commerce backend for catalog, inventory, carts, checkout reservations, and fulfillment-related rules.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Backend-only .NET commerce implementation with tests; no frontend implied. Static review only; not built, tested or run.
- **Recorded stack:** C#, ASP.NET Core, Entity Framework Core, SQLite, xUnit.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/gitvg/agora-net/docs/adr/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of availability and local-time conversion: ordered source files, one input-to-state trace, a diagram and one independent change targeting Backend checkout, inventory reservations, JWT, EF Core.
- **2 — Improve the project/resource:** First scoped project change: Add one checkout failure or concurrent reservation test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/agora-net/README.md), [Program.cs](C:/Users/Owner/Desktop/gitvg/agora-net/src/Agora.Api/Program.cs), [Agora.Api.csproj](C:/Users/Owner/Desktop/gitvg/agora-net/src/Agora.Api/Agora.Api.csproj).

---

<a id="p323"></a>
### gitvg/atlas

Employer-of-record teaching platform for hiring, onboarding, paying, and managing an international workforce.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Large C# teaching platform; domain examples are educational and runtime unverified. Static review only; not built, tested or run.
- **Recorded stack:** C#, ASP.NET Core, Entity Framework Core, PostgreSQL, SQLite, Docker, GitHub Actions, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [LEARNER-GUIDE.md](C:/Users/Owner/Desktop/gitvg/atlas/LEARNER-GUIDE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of employee lifecycle, approval and tenant scope, an expected-state example and a guided-to-independent change exercise. Tie it to Employment workflows, C# domain modeling, persistence.
- **2 — Improve the project/resource:** First scoped project change: Trace one onboarding-to-payroll workflow and test a rejected transition. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/atlas/README.md), [Program.cs](C:/Users/Owner/Desktop/gitvg/atlas/src/Atlas.Api/Program.cs), [docker-compose.yml](C:/Users/Owner/Desktop/gitvg/atlas/docker-compose.yml).

---

<a id="p324"></a>
### gitvg/atlas-net

An Employer-of-Record (EOR) platform backend, in the style of Velocity Global / Deel, built with C# and .NET 10.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Separate backend-focused .NET variant with tests, not an automatically redundant folder. Static review only; not built, tested or run.
- **Recorded stack:** C#, ASP.NET Core, Entity Framework Core, SQLite, xUnit.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/gitvg/atlas-net/docs/adr/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of employee lifecycle, approval and tenant scope: ordered source files, one input-to-state trace, a diagram and one independent change targeting Backend lifecycle modeling, client-scoped auth, payroll.
- **2 — Improve the project/resource:** First scoped project change: Compare one lifecycle slice with Atlas and choose one implementation to study. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/atlas-net/README.md), [Program.cs](C:/Users/Owner/Desktop/gitvg/atlas-net/src/Atlas.Api/Program.cs), [Atlas.Api.csproj](C:/Users/Owner/Desktop/gitvg/atlas-net/src/Atlas.Api/Atlas.Api.csproj).

---

<a id="p326"></a>
### gitvg/bazaar-app

Shopify-style e-commerce teaching app with a customer storefront and administrative catalog/order workflows.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Full-stack .NET variant; stack differs from gitvg/bazaar. Static review only; not built, tested or run.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, SQLite, Vitest, xUnit.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/gitvg/bazaar-app/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of stock ownership, checkout and order transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting .NET/React commerce, identity, fulfillment, EF Core.
- **2 — Improve the project/resource:** First scoped project change: Trace one return or fulfillment slice and test its permissions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/bazaar-app/README.md), [App.tsx](C:/Users/Owner/Desktop/gitvg/bazaar-app/client/src/App.tsx), [package.json](C:/Users/Owner/Desktop/gitvg/bazaar-app/client/package.json).

---

<a id="p337"></a>
### gitvg/tracer-net

A Linear-clone issue tracker backend built with C# / .NET 10 and ASP.NET Core.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Backend-only .NET issue tracker with substantial tests; choose as backend alternative to frontend-heavy courses. Static review only; not built, tested or run.
- **Recorded stack:** C#, ASP.NET Core, Entity Framework Core, SQLite, xUnit.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/gitvg/tracer-net/docs/adr/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, ordering and lifecycle transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting Issue state machines, ranking, search, EF Core.
- **2 — Improve the project/resource:** First scoped project change: Test one invalid workflow transition and ordering edge case. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/gitvg/tracer-net/README.md), [Program.cs](C:/Users/Owner/Desktop/gitvg/tracer-net/src/Tracer.Api/Program.cs), [Tracer.Api.csproj](C:/Users/Owner/Desktop/gitvg/tracer-net/src/Tracer.Api/Tracer.Api.csproj).

---

<a id="p338"></a>
### globehire

GlobeHire is a fifteen-sprint C#/.NET teaching repository for a fictional global workforce and employer-of-record platform.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Teaching system defaults to volatile in-memory storage and explicitly has no real authentication. Workforce rules are synthetic; curriculum completion does not mean deployable software. Static review only; not built, tested or run.
- **Recorded stack:** C#, ASP.NET Core, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/globehire/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for employee lifecycle, approval and tenant scope; make learners predict state before running it. Teach Versioned rules, lifecycle changes, integration ports, API contracts with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: After CampusOps, change one fictional country rule without breaking API contracts. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Globehire](C:/Users/Owner/Desktop/geminiorganized/General_Globehire). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/globehire/README.md), [Program.cs](C:/Users/Owner/Desktop/globehire/src/GlobeHire.Api/Program.cs), [GlobeHire.Api.csproj](C:/Users/Owner/Desktop/globehire/src/GlobeHire.Api/GlobeHire.Api.csproj).

---

<a id="p342"></a>
### grokbuildmultitenantproject

A full-stack Multi-Tenant SaaS Starter built for educational purposes to upskill to mid/senior SWE level.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Compact multi-tenant teaching implementation with only a few cataloged test files. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Vite, Prisma, Docker.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/grokbuildmultitenantproject/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Tenant isolation, organization roles, scoped queries with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Add a test proving one tenant cannot access another tenant's project. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/grokbuildmultitenantproject/README.md), [App.tsx](C:/Users/Owner/Desktop/grokbuildmultitenantproject/frontend/src/App.tsx), [docker-compose.yml](C:/Users/Owner/Desktop/grokbuildmultitenantproject/docker-compose.yml).

---

<a id="p343"></a>
### grokbuildorderproject

Full-stack Order Management / Operations Platform (Educational)

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Small educational order-system slice; verify workflow completeness from source before expanding it. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Docker, Jest, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [JOURNAL.md](C:/Users/Owner/Desktop/grokbuildorderproject/JOURNAL.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for stock ownership, checkout and order transitions; make learners predict state before running it. Teach Inventory, order transitions, transactional integrity with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Trace one inventory update and test rollback on failure. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/grokbuildorderproject/README.md), [App.tsx](C:/Users/Owner/Desktop/grokbuildorderproject/frontend/src/App.tsx), [docker-compose.yml](C:/Users/Owner/Desktop/grokbuildorderproject/docker-compose.yml).

---

<a id="p360"></a>
### meterforge

MeterForge is a fifteen-sprint C#/.NET teaching repository for a fictional multi-tenant usage-based subscription billing platform.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A completed full-stack slice, SQL transactions, authorization and meaningful tests.
- **Baseline:** Substantial fifteen-sprint source/tests. Default runtime uses non-durable in-memory adapters; README explicitly excludes production auth, migration runner, telemetry backend and operated restore. Static review only; not built, tested or run.
- **Recorded stack:** C#, SQL, ASP.NET Core, PostgreSQL, Docker, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/meterforge/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for money units, state transitions and duplicate deliveries; make learners predict state before running it. Teach Money invariants, idempotency, concurrency, outbox, integrations with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: After CampusOps, prove duplicate usage does not double bill, then use a durable adapter. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Meterforge](C:/Users/Owner/Desktop/geminiorganized/General_Meterforge). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/meterforge/README.md), [Program.cs](C:/Users/Owner/Desktop/meterforge/src/MeterForge.Api/Program.cs), [docker-compose.yml](C:/Users/Owner/Desktop/meterforge/docker-compose.yml).

---

<a id="p366"></a>
### netdocu

NetDocu is a DocuSign-style signing workflow application with a .NET 8 clean-architecture API, PostgreSQL persistence, JWT/refresh-token auth, and a React + TypeScript signing workspace.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Layered signing-workflow application with document/auth controllers, React workspace and test projects. Static inspection confirms application structure, not completed signing fidelity or deployed integrations.
- **Recorded stack:** C#, CSS, HTML, JavaScript, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/netdocu/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Document permissions, workflow state transitions, audit events, background processing. with a separate answer and rubric. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Trace document creation to envelope completion; verify one unauthorized recipient and duplicate submission scenario. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [geminiorganized/OpenSource_Upskilling_Docu](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Docu). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netdocu/README.md), [AuthController.cs](C:/Users/Owner/Desktop/netdocu/src/NetDocu.Api/Controllers/AuthController.cs), [DocumentsController.cs](C:/Users/Owner/Desktop/netdocu/src/NetDocu.Api/Controllers/DocumentsController.cs).

---

<a id="p370"></a>
### netnotion

NetNotion is a Notion-style collaborative docs/wiki app built with .NET 8 Web API, EF Core, PostgreSQL, React, TypeScript, Vite, and TanStack Query.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Collaborative-docs learning app with page/version/share controllers. README explicitly excludes realtime presence, templates and export stretch features.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/netnotion/docs/fable/README.md).
- **1 — Improve the upskilling content:** Use populated docs/fable as the start; label empty docs/upskill scaffolding and teach page permissions and revision history. Label the sampled placeholder chapters; complete only the chapter required by this exercise. Do not treat the empty alternative guide as a completed course.
- **2 — Improve the project/resource:** Protect a page move/restore operation against inherited-permission bypass and recursive tree cycles.
- **3 — Prove completion:** Reject a cycle and a forbidden inherited share; restore content while retaining a coherent revision history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file. docs/fable is substantive; the sampled docs/upskill README is explicitly unfilled.
- **Related locations to compare:** [geminiorganized/OpenSource_Upskilling_Notion](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Notion). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netnotion/README.md), [AuthController.cs](C:/Users/Owner/Desktop/netnotion/src/NetNotion.Api/Controllers/AuthController.cs), [PagesController.cs](C:/Users/Owner/Desktop/netnotion/src/NetNotion.Api/Controllers/PagesController.cs).

---

<a id="p374"></a>
### netshop

NetShopifyLite is a .NET 8 + React ecommerce admin and lightweight storefront scaffold.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Ecommerce learning scaffold with order/auth controllers, idempotency contracts and domain state transitions. Payment provider is fake; integration tests are described as a skeleton.
- **Recorded stack:** C#, CSS, HTML, TypeScript, ASP.NET Core, React, Vite, Entity Framework Core, PostgreSQL, Redis, Docker, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/netshop/docs/upskill/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for stock ownership, checkout and order transitions; make learners predict state before running it. Teach Money modeling, transactional inventory, idempotent checkout/refunds and domain invariants. with a separate answer and rubric. Label the sampled placeholder chapters; complete only the chapter required by this exercise.
- **2 — Improve the project/resource:** First scoped project change: Prove duplicate checkout/refund behavior and stock consistency with a real persistence integration test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Documentation caveats:** Some sampled documentation is empty/placeholder material; use the populated starting file.
- **Related locations to compare:** [geminiorganized/OpenSource_Upskilling_Shop](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Shop). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netshop/README.md), [AuthController.cs](C:/Users/Owner/Desktop/netshop/src/NetShopifyLite.Api/Controllers/AuthController.cs), [OrdersController.cs](C:/Users/Owner/Desktop/netshop/src/NetShopifyLite.Api/Controllers/OrdersController.cs).

---

<a id="p377"></a>
### newcodecjs2

Five focused SaaS architecture learning scaffolds: Planr, Bookr, Payr, Blockr and Helpkit.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Five architecture-oriented SaaS learning scaffolds. Root README explicitly says they are not wired for installation/deployment; sampled routes are plain functions over in-memory stores.
- **Recorded stack:** TypeScript, Next.js, Node.js, React, Vite, Drizzle, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodecjs2/payr/README.md).
- **1 — Improve the upskilling content:** Add a five-app skill map and identify each simulated integration and intended invariant.
- **2 — Improve the project/resource:** Select one of Planr, Bookr, Payr, Blockr or Helpkit and implement its smallest missing end-to-end slice.
- **3 — Prove completion:** Meet the selected child’s criterion below and record which integrations remain simulated.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Newcodecjs2](C:/Users/Owner/Desktop/geminiorganized/General_Newcodecjs2). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodecjs2/README.md), [routes.ts](C:/Users/Owner/Desktop/newcodecjs2/payr/src/server/routes.ts), [package.json](C:/Users/Owner/Desktop/newcodecjs2/blockr/package.json).

---

<a id="p460"></a>
### newcodecjs2/blockr

Page/block editor

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Architecture reading scaffold with domain functions and route sketches over in-memory stores; root explicitly says installation/deployment wiring is incomplete.
- **Recorded stack:** TypeScript, React, Next.js declared, Drizzle declared, Vitest.
- **Parent workspace:** [newcodecjs2](C:/Users/Owner/Desktop/newcodecjs2). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodecjs2/blockr/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of tree structure, revisions and inherited permissions: ordered source files, one input-to-state trace, a diagram and one independent change targeting Recursive blocks, ordering and inherited page permissions.
- **2 — Improve the project/resource:** First scoped project change: Reject a page cycle and test inherited permission denial. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** One of five related SaaS exercises; not five production-complete products.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodecjs2/blockr/README.md), [package.json](C:/Users/Owner/Desktop/newcodecjs2/blockr/package.json), [routes.ts](C:/Users/Owner/Desktop/newcodecjs2/blockr/src/server/routes.ts).

---

<a id="p461"></a>
### newcodecjs2/bookr

Scheduling

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Architecture reading scaffold with domain functions and route sketches over in-memory stores; root explicitly says installation/deployment wiring is incomplete.
- **Recorded stack:** TypeScript, React, Next.js declared, Drizzle declared, Vitest.
- **Parent workspace:** [newcodecjs2](C:/Users/Owner/Desktop/newcodecjs2). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodecjs2/bookr/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of availability and local-time conversion: ordered source files, one input-to-state trace, a diagram and one independent change targeting Timezone availability, slot revalidation, locking and calendar gateways.
- **2 — Improve the project/resource:** First scoped project change: Test daylight-saving and two users booking the same slot. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** One of five related SaaS exercises; not five production-complete products.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodecjs2/bookr/README.md), [package.json](C:/Users/Owner/Desktop/newcodecjs2/bookr/package.json), [routes.ts](C:/Users/Owner/Desktop/newcodecjs2/bookr/src/server/routes.ts).

---

<a id="p463"></a>
### newcodecjs2/payr

Mock payments dashboard

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Architecture reading scaffold with domain functions and route sketches over in-memory stores; root explicitly says installation/deployment wiring is incomplete.
- **Recorded stack:** TypeScript, React, Next.js declared, Drizzle declared, Vitest.
- **Parent workspace:** [newcodecjs2](C:/Users/Owner/Desktop/newcodecjs2). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodecjs2/payr/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of money units, state transitions and duplicate deliveries: ordered source files, one input-to-state trace, a diagram and one independent change targeting RBAC, idempotency, cursor pages, API keys and webhook logs.
- **2 — Improve the project/resource:** First scoped project change: Replay one payment mutation and prove permission checks precede state changes. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** One of five related SaaS exercises; not five production-complete products.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodecjs2/payr/README.md), [package.json](C:/Users/Owner/Desktop/newcodecjs2/payr/package.json), [routes.ts](C:/Users/Owner/Desktop/newcodecjs2/payr/src/server/routes.ts).

---

<a id="p464"></a>
### newcodecjs2/planr

Issue tracker

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Architecture reading scaffold with domain functions and route sketches over in-memory stores; root explicitly says installation/deployment wiring is incomplete.
- **Recorded stack:** TypeScript, React, Next.js declared, Drizzle declared, Vitest.
- **Parent workspace:** [newcodecjs2](C:/Users/Owner/Desktop/newcodecjs2). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodecjs2/planr/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of ownership, ordering and lifecycle transitions: ordered source files, one input-to-state trace, a diagram and one independent change targeting Optimistic queues, rollback, filtering and workflow rules.
- **2 — Improve the project/resource:** First scoped project change: Trace one failed optimistic issue mutation and verify rollback. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** One of five related SaaS exercises; not five production-complete products.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodecjs2/planr/README.md), [package.json](C:/Users/Owner/Desktop/newcodecjs2/planr/package.json), [routes.ts](C:/Users/Owner/Desktop/newcodecjs2/planr/src/server/routes.ts).

---

<a id="p378"></a>
### newcodex3

Learning workspace with 25 software topics numbered 16-40, each in TypeScript/React and .NET/React variants (50 child apps).

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** 50 child learning apps: 25 topics numbered 16-40 in TypeScript and .NET variants. Root five-project/title wording is stale. Many .NET and later TS versions use in-memory collections; architecture prose is not proof of durable services.
- **Recorded stack:** C#, CSS, HTML, TypeScript, Express, Node.js, React, Vite, Prisma, Redis, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/27-ats-lite/docs/upskill.md).
- **1 — Improve the upskilling content:** Index 25 topics and both language variants; explicitly distinguish in-memory C# samples from persistence plans.
- **2 — Improve the project/resource:** Choose one TypeScript child first; implement one missing domain rule before comparing its C# counterpart.
- **3 — Prove completion:** Demonstrate the chosen child independently; describe the implementations’ actual differences using code and behavior evidence.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Newcodex3](C:/Users/Owner/Desktop/geminiorganized/General_Newcodex3). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/README.md), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/27-ats-lite-net/server/Program.cs), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/18-team-chat-net/server/Program.cs).

---

<a id="p392"></a>
### newcodex3/apps/17-kanban-board

Kanban board

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/17-kanban-board/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ownership, ordering and lifecycle transitions; make learners predict state before running it. Teach Nested state, fractional ordering, membership and expiring invitations with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Verify reorder stability and one-time invitation acceptance. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/17-kanban-board-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/17-kanban-board/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/17-kanban-board/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/17-kanban-board/client/package.json).

---

<a id="p393"></a>
### newcodex3/apps/17-kanban-board-net

Kanban board (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/17-kanban-board-net/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of ownership, ordering and lifecycle transitions, known stubs and one exercise targeting Nested state, fractional ordering, membership and expiring invitations. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Verify reorder stability and one-time invitation acceptance. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/17-kanban-board; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/17-kanban-board-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/17-kanban-board-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/17-kanban-board-net/server/Program.cs).

---

<a id="p396"></a>
### newcodex3/apps/19-ecommerce-storefront

Ecommerce storefront

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/19-ecommerce-storefront/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for money units, state transitions and duplicate deliveries; make learners predict state before running it. Teach Guest carts, integer money, inventory transactions and idempotent webhooks with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Verify cart merge and duplicate payment-event handling using a fake provider. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/19-ecommerce-storefront-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/19-ecommerce-storefront/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/19-ecommerce-storefront/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/19-ecommerce-storefront/client/package.json).

---

<a id="p397"></a>
### newcodex3/apps/19-ecommerce-storefront-net

Ecommerce storefront (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/19-ecommerce-storefront-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of money units, state transitions and duplicate deliveries: ordered source files, one input-to-state trace, a diagram and one independent change targeting Guest carts, integer money, inventory transactions and idempotent webhooks.
- **2 — Improve the project/resource:** First scoped project change: Verify cart merge and duplicate payment-event handling using a fake provider. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/19-ecommerce-storefront; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/19-ecommerce-storefront-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/19-ecommerce-storefront-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/19-ecommerce-storefront-net/server/Program.cs).

---

<a id="p398"></a>
### newcodex3/apps/20-event-booking

Event booking

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/20-event-booking/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for availability and local-time conversion; make learners predict state before running it. Teach Capacity locks, ticket allocation, waitlists and deferred notification with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Prove two competing bookings cannot overbook the last seat. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/20-event-booking-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/20-event-booking/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/20-event-booking/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/20-event-booking/client/package.json).

---

<a id="p399"></a>
### newcodex3/apps/20-event-booking-net

Event booking (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/20-event-booking-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of availability and local-time conversion: ordered source files, one input-to-state trace, a diagram and one independent change targeting Capacity locks, ticket allocation, waitlists and deferred notification.
- **2 — Improve the project/resource:** First scoped project change: Prove two competing bookings cannot overbook the last seat. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/20-event-booking; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/20-event-booking-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/20-event-booking-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/20-event-booking-net/server/Program.cs).

---

<a id="p400"></a>
### newcodex3/apps/21-invoicing-app

Invoicing

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/21-invoicing-app/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for money units, state transitions and duplicate deliveries; make learners predict state before running it. Teach Integer money/tax, invoice transitions, recurring jobs and PDF/email boundaries with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Test rounding, duplicate recurring generation and invalid invoice transitions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/21-invoicing-app-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/21-invoicing-app/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/21-invoicing-app/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/21-invoicing-app/client/package.json).

---

<a id="p401"></a>
### newcodex3/apps/21-invoicing-app-net

Invoicing (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/21-invoicing-app-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of money units, state transitions and duplicate deliveries: ordered source files, one input-to-state trace, a diagram and one independent change targeting Integer money/tax, invoice transitions, recurring jobs and PDF/email boundaries.
- **2 — Improve the project/resource:** First scoped project change: Test rounding, duplicate recurring generation and invalid invoice transitions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/21-invoicing-app; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/21-invoicing-app-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/21-invoicing-app-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/21-invoicing-app-net/server/Program.cs).

---

<a id="p402"></a>
### newcodex3/apps/22-team-wiki

Team wiki

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/22-team-wiki/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for tree structure, revisions and inherited permissions; make learners predict state before running it. Teach Recursive trees, immutable revisions, restore and page permissions with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Reject a page cycle and prove restored content keeps its revision history. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/22-team-wiki-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/22-team-wiki/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/22-team-wiki/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/22-team-wiki/client/package.json).

---

<a id="p403"></a>
### newcodex3/apps/22-team-wiki-net

Team wiki (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/22-team-wiki-net/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for tree structure, revisions and inherited permissions; make learners predict state before running it. Teach Recursive trees, immutable revisions, restore and page permissions with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Reject a page cycle and prove restored content keeps its revision history. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/22-team-wiki; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/22-team-wiki-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/22-team-wiki-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/22-team-wiki-net/server/Program.cs).

---

<a id="p404"></a>
### newcodex3/apps/23-survey-form-builder

Survey/form builder

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/23-survey-form-builder/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for schema versions and response validation; make learners predict state before running it. Teach Versioned dynamic schemas, conditional logic, validation and analytics with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Validate a response against its published schema and reject hidden invalid inputs. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Validate against a published schema; reject foreign, hidden-invalid or outdated inputs without partially saving a response.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/23-survey-form-builder-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/23-survey-form-builder/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/23-survey-form-builder/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/23-survey-form-builder/client/package.json).

---

<a id="p405"></a>
### newcodex3/apps/23-survey-form-builder-net

Survey/form builder (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/23-survey-form-builder-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of schema versions and response validation: ordered source files, one input-to-state trace, a diagram and one independent change targeting Versioned dynamic schemas, conditional logic, validation and analytics.
- **2 — Improve the project/resource:** First scoped project change: Validate a response against its published schema and reject hidden invalid inputs. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Validate against a published schema; reject foreign, hidden-invalid or outdated inputs without partially saving a response.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/23-survey-form-builder; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/23-survey-form-builder-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/23-survey-form-builder-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/23-survey-form-builder-net/server/Program.cs).

---

<a id="p408"></a>
### newcodex3/apps/25-discussion-forum

Discussion forum

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/25-discussion-forum/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach Comment trees, vote uniqueness, ranking and rate limits with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Prove one user cannot cast duplicate votes and test thread ordering. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/25-discussion-forum-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/25-discussion-forum/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/25-discussion-forum/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/25-discussion-forum/client/package.json).

---

<a id="p409"></a>
### newcodex3/apps/25-discussion-forum-net

Discussion forum (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/25-discussion-forum-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of the documented workflow and its state boundary: ordered source files, one input-to-state trace, a diagram and one independent change targeting Comment trees, vote uniqueness, ranking and rate limits.
- **2 — Improve the project/resource:** First scoped project change: Prove one user cannot cast duplicate votes and test thread ordering. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/25-discussion-forum; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/25-discussion-forum-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/25-discussion-forum-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/25-discussion-forum-net/server/Program.cs).

---

<a id="p410"></a>
### newcodex3/apps/26-subscription-reminders

Subscription reminders

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/26-subscription-reminders/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for money units, state transitions and duplicate deliveries; make learners predict state before running it. Teach Local-calendar timezones, recurring queues and notification preferences with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Test one daylight-saving transition and duplicate reminder delivery. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/26-subscription-reminders-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/26-subscription-reminders/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/26-subscription-reminders/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/26-subscription-reminders/client/package.json).

---

<a id="p411"></a>
### newcodex3/apps/26-subscription-reminders-net

Subscription reminders (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/26-subscription-reminders-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of money units, state transitions and duplicate deliveries: ordered source files, one input-to-state trace, a diagram and one independent change targeting Local-calendar timezones, recurring queues and notification preferences.
- **2 — Improve the project/resource:** First scoped project change: Test one daylight-saving transition and duplicate reminder delivery. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/26-subscription-reminders; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/26-subscription-reminders-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/26-subscription-reminders-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/26-subscription-reminders-net/server/Program.cs).

---

<a id="p412"></a>
### newcodex3/apps/27-ats-lite

Applicant tracking

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/27-ats-lite/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for availability and local-time conversion; make learners predict state before running it. Teach Multi-actor pipelines, file-scan states and interview conflict detection with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Reject overlapping interviews and unauthorized pipeline changes. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/27-ats-lite-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/27-ats-lite/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/27-ats-lite/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/27-ats-lite/client/package.json).

---

<a id="p413"></a>
### newcodex3/apps/27-ats-lite-net

Applicant tracking (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/27-ats-lite-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of availability and local-time conversion: ordered source files, one input-to-state trace, a diagram and one independent change targeting Multi-actor pipelines, file-scan states and interview conflict detection.
- **2 — Improve the project/resource:** First scoped project change: Reject overlapping interviews and unauthorized pipeline changes. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/27-ats-lite; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/27-ats-lite-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/27-ats-lite-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/27-ats-lite-net/server/Program.cs).

---

<a id="p414"></a>
### newcodex3/apps/28-restaurant-reservations

Restaurant reservations

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/28-restaurant-reservations/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for availability and local-time conversion; make learners predict state before running it. Teach Resource intervals, table combinations, turn times and notification boundaries with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Verify overlapping table reservations and capacity edge cases. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/28-restaurant-reservations-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/28-restaurant-reservations/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/28-restaurant-reservations/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/28-restaurant-reservations/client/package.json).

---

<a id="p415"></a>
### newcodex3/apps/28-restaurant-reservations-net

Restaurant reservations (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/28-restaurant-reservations-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of availability and local-time conversion: ordered source files, one input-to-state trace, a diagram and one independent change targeting Resource intervals, table combinations, turn times and notification boundaries.
- **2 — Improve the project/resource:** First scoped project change: Verify overlapping table reservations and capacity edge cases. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/28-restaurant-reservations; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/28-restaurant-reservations-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/28-restaurant-reservations-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/28-restaurant-reservations-net/server/Program.cs).

---

<a id="p416"></a>
### newcodex3/apps/29-personal-finance-dashboard

Personal-finance dashboard

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** TypeScript/Express + React teaching reference with Prisma service code and manifests. It is intended for reading/extension; installation, integration behavior and test passing were not verified.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/29-personal-finance-dashboard/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for event identity, aggregation and reporting filters; make learners predict state before running it. Teach CSV normalization, fingerprints, categorization rules and reporting with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Import the same sample twice and prove deterministic deduplication. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/29-personal-finance-dashboard-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/29-personal-finance-dashboard/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/29-personal-finance-dashboard/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/29-personal-finance-dashboard/client/package.json).

---

<a id="p417"></a>
### newcodex3/apps/29-personal-finance-dashboard-net

Personal-finance dashboard (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/29-personal-finance-dashboard-net/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of event identity, aggregation and reporting filters: ordered source files, one input-to-state trace, a diagram and one independent change targeting CSV normalization, fingerprints, categorization rules and reporting.
- **2 — Improve the project/resource:** First scoped project change: Import the same sample twice and prove deterministic deduplication. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/29-personal-finance-dashboard; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/29-personal-finance-dashboard-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/29-personal-finance-dashboard-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/29-personal-finance-dashboard-net/server/Program.cs).

---

<a id="p422"></a>
### newcodex3/apps/32-helpdesk-ticketing

Helpdesk ticketing

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/32-helpdesk-ticketing/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ticket visibility, assignment and service deadlines; make learners predict state before running it. Teach Ticket lifecycle, internal/public comments and SLA jobs with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Prove internal notes stay private and a reopened ticket recomputes SLA correctly. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/32-helpdesk-ticketing-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/32-helpdesk-ticketing/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/32-helpdesk-ticketing/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/32-helpdesk-ticketing/client/package.json).

---

<a id="p423"></a>
### newcodex3/apps/32-helpdesk-ticketing-net

Helpdesk ticketing (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/32-helpdesk-ticketing-net/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of ticket visibility, assignment and service deadlines, known stubs and one exercise targeting Ticket lifecycle, internal/public comments and SLA jobs. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Prove internal notes stay private and a reopened ticket recomputes SLA correctly. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Verify private notes remain private and one assignment/reopen transition has the correct visible state and deadline.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/32-helpdesk-ticketing; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/32-helpdesk-ticketing-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/32-helpdesk-ticketing-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/32-helpdesk-ticketing-net/server/Program.cs).

---

<a id="p424"></a>
### newcodex3/apps/33-inventory-warehouse-manager

Inventory/warehouse manager

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/33-inventory-warehouse-manager/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for stock ownership, checkout and order transitions; make learners predict state before running it. Teach Immutable stock movements, transfers and reconciliation with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Prove a transfer balances both locations and duplicate requests do not add stock. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/33-inventory-warehouse-manager-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/33-inventory-warehouse-manager/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/33-inventory-warehouse-manager/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/33-inventory-warehouse-manager/client/package.json).

---

<a id="p425"></a>
### newcodex3/apps/33-inventory-warehouse-manager-net

Inventory/warehouse manager (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/33-inventory-warehouse-manager-net/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of stock ownership, checkout and order transitions, known stubs and one exercise targeting Immutable stock movements, transfers and reconciliation. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Prove a transfer balances both locations and duplicate requests do not add stock. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/33-inventory-warehouse-manager; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/33-inventory-warehouse-manager-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/33-inventory-warehouse-manager-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/33-inventory-warehouse-manager-net/server/Program.cs).

---

<a id="p428"></a>
### newcodex3/apps/35-analytics-reporting-dashboard

Analytics/reporting dashboard

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/35-analytics-reporting-dashboard/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for event identity, aggregation and reporting filters; make learners predict state before running it. Teach Validated filters, aggregation, export jobs and permissions with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Verify report authorization and move one expensive export into a durable job. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/35-analytics-reporting-dashboard-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/35-analytics-reporting-dashboard/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/35-analytics-reporting-dashboard/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/35-analytics-reporting-dashboard/client/package.json).

---

<a id="p429"></a>
### newcodex3/apps/35-analytics-reporting-dashboard-net

Analytics/reporting dashboard (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/35-analytics-reporting-dashboard-net/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of event identity, aggregation and reporting filters, known stubs and one exercise targeting Validated filters, aggregation, export jobs and permissions. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Verify report authorization and move one expensive export into a durable job. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/35-analytics-reporting-dashboard; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/35-analytics-reporting-dashboard-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/35-analytics-reporting-dashboard-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/35-analytics-reporting-dashboard-net/server/Program.cs).

---

<a id="p432"></a>
### newcodex3/apps/37-bulk-import-review-tool

Bulk import/review

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Compact TypeScript/Express + React teaching scaffold; sampled server uses in-memory arrays/records while Prisma schema describes the production data model.
- **Recorded stack:** TypeScript, Express, React, Vite, Prisma schema.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Structured tutorial / exercises. Start at [upskill.md](C:/Users/Owner/Desktop/newcodex3/apps/37-bulk-import-review-tool/docs/upskill.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for staging, approval and atomic batch commits; make learners predict state before running it. Teach Staging, mapping, row errors, approval, idempotent commit and rollback with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Commit an approved batch twice and prove rollback scope does not affect unrelated data. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Stage valid and invalid rows, reject commit before approval, then commit the approved batch twice; rollback must preserve unrelated records.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/37-bulk-import-review-tool-net; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/37-bulk-import-review-tool/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/37-bulk-import-review-tool/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/37-bulk-import-review-tool/client/package.json).

---

<a id="p433"></a>
### newcodex3/apps/37-bulk-import-review-tool-net

Bulk import/review (.NET variant)

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** C#/.NET + React teaching counterpart. Sampled minimal API uses in-memory collections; production persistence/integration descriptions are design guidance, not verified implementations.
- **Recorded stack:** C#, ASP.NET Core minimal API, React, TypeScript, Vite.
- **Parent workspace:** [newcodex3](C:/Users/Owner/Desktop/newcodex3). Parent-level work does not replace this child’s task.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/newcodex3/apps/37-bulk-import-review-tool-net/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of staging, approval and atomic batch commits, known stubs and one exercise targeting Staging, mapping, row errors, approval, idempotent commit and rollback. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Commit an approved batch twice and prove rollback scope does not affect unrelated data. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Stage valid and invalid rows, reject commit before approval, then commit the approved batch twice; rollback must preserve unrelated records.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Paired language variant of newcodex3/apps/37-bulk-import-review-tool; study one first and use the other only for language/pattern comparison.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodex3/apps/37-bulk-import-review-tool-net/README.md), [package.json](C:/Users/Owner/Desktop/newcodex3/apps/37-bulk-import-review-tool-net/client/package.json), [Program.cs](C:/Users/Owner/Desktop/newcodex3/apps/37-bulk-import-review-tool-net/server/Program.cs).

---

<a id="p452"></a>
### newcodexJS/13-ecommerce-storefront

Ecommerce storefront

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. README describes development/demo identity headers rather than completed authentication.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/13-ecommerce-storefront/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of stock ownership, checkout and order transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Cart ownership, transactional checkout, reviews and admin flows.
- **2 — Improve the project/resource:** First scoped project change: Verify duplicate checkout/stock handling and replace demo identity before shared deployment. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/13-ecommerce-storefront/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/13-ecommerce-storefront/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/13-ecommerce-storefront/client/package.json).

---

<a id="p453"></a>
### newcodexJS/14-appointment-booking

Appointment booking

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. README describes development/demo identity headers rather than completed authentication.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/14-appointment-booking/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to Availability, timezone conversion and overlap detection.
- **2 — Improve the project/resource:** First scoped project change: Test last-slot concurrency and replace development identity/role headers. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/14-appointment-booking/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/14-appointment-booking/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/14-appointment-booking/client/package.json).

---

<a id="p454"></a>
### newcodexJS/15-api-tester

REST API testing tool

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/15-api-tester/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of outbound target validation, timeouts and response limits, an expected-state example and a guided-to-independent change exercise. Tie it to HTTP proxying, variable interpolation, request history and collections.
- **2 — Improve the project/resource:** First scoped project change: Verify target restrictions, timeouts and response limits on the proxy endpoint. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a controlled HTTP stub to verify one allowed request, a forbidden target, a redirect to a forbidden target, a timeout and an oversized response; rejected requests must not reach protected destinations.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/15-api-tester/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/15-api-tester/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/15-api-tester/client/package.json).

---

<a id="p381"></a>
### perch

Perch is a Greenhouse/Lever-style applicant tracking system and a teaching repository for junior engineers.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Substantial teaching ATS with Fastify routes, React UI, pure domain tests and repository interfaces. Deterministic in-memory adapters are active; Prisma/Postgres production model and external provider intent boundaries remain separate.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Fastify, Node.js, React, Vite, Prisma, GitHub Actions, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [LEARNER-GUIDE.md](C:/Users/Owner/Desktop/perch/LEARNER-GUIDE.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for ownership, ordering and lifecycle transitions; make learners predict state before running it. Teach Multi-actor workflow, object authorization, state machines, bulk actions, ports/adapters and test design. with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Follow one sprint playbook and implement a persistent repository adapter while retaining the authorization tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Perch](C:/Users/Owner/Desktop/geminiorganized/General_Perch). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/perch/README.md), [app.ts](C:/Users/Owner/Desktop/perch/apps/api/src/app.ts), [index.ts](C:/Users/Owner/Desktop/perch/packages/db/src/index.ts).

---

<a id="p386"></a>
### skillforgejs

Skillforge is a web-first coding-skills learning platform built with Next.js App Router, TypeScript, Prisma/PostgreSQL, Auth.js, Tailwind, CodeMirror, server-side spaced repetition, and gamification.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 5; prerequisites: A working full-stack app with authentication, authorization, relational data and tests.
- **Baseline:** Substantial Next.js learning platform source with catalog server rendering, auth/data models, spaced-repetition modules, content validation and unit/E2E test configuration. Catalog content and runtime were not executed.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Docker, GitHub Actions, Playwright, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/skillforgejs/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of eligibility, progress and completion transitions, an expected-state example and a guided-to-independent change exercise. Tie it to App Router/server boundaries, Prisma, content schema validation, pure scheduling logic and tests..
- **2 — Improve the project/resource:** First scoped project change: Trace lesson completion into review state and add a deterministic scheduler/transaction test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Reject an ineligible completion; repeat a valid progress event and verify progress and any certificate/review state remain consistent.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Skillforgejs](C:/Users/Owner/Desktop/geminiorganized/General_Skillforgejs). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/skillforgejs/README.md), [page.tsx](C:/Users/Owner/Desktop/skillforgejs/src/app/page.tsx), [layout.tsx](C:/Users/Owner/Desktop/skillforgejs/src/app/layout.tsx).

---
