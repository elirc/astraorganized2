# Section 2: Client apps, APIs and persistence

[Plan index](README.md)

Finish one client app, then one API-backed workflow. Keep the current stack; choose TypeScript/React/Node for the main route and defer the C# branch until after a capstone.

**Stage exit criterion:** Demonstrate a usable workflow, invalid input, loading/error states where applicable, and persistence across restart.

**Coverage:** 40 project/workspace/resource records and 5 nested teaching apps. Entries are grouped by original milestone and alphabetized within it; alphabetical position is not a mandatory execution order. Use the short route in the index.

All actions below are proposals based on the September 6–7 static reviews. Reproduce the baseline before claiming a defect or improvement. Existing tests and docs may already cover a proposed case; assess and strengthen them rather than duplicate them.

## Entries

- [_Organized Desktop/02 Build Projects/buildgum](#p024)
- [_Organized Desktop/02 Build Projects/buildsubbox](#p027)
- [_Organized Desktop/04 JavaScript Training/jstrain2.3](#p074)
- [_Organized Desktop/04 JavaScript Training/react](#p079)
- [_Organized Desktop/05 Numbered Experiments/g1](#p099)
- [_Organized Desktop/05 Numbered Experiments/X1](#p151)
- [_Organized Desktop/05 Numbered Experiments/z9](#p157)
- [_Organized Desktop/06 AI And Learning/claudeailab-temp](#p172)
- [_Organized Desktop/07 Anti Projects/antiinv](#p178)
- [_Organized Desktop/08 App And Product Projects/recipegen-app](#p187)
- [_Organized Desktop/08 App And Product Projects/recipegen-temp](#p188)
- [_Organized Desktop/12 Other Projects/3buildhyper](#p194)
- [_Organized Desktop/12 Other Projects/FinalJep](#p200)
- [_Organized Desktop/12 Other Projects/GlobGame](#p202)
- [_Organized Desktop/12 Other Projects/hypernova-inc-main](#p203)
- [AlanAndEliSoccer](#p213)
- [ankijs](#p214)
- [astra4.2](#p219)
- [buildbusinesses](#p222)
- [calendar+jobtrack](#p230)
- [formforge](#p239)
- [geminiorganized/General_Alanandelisoccer](#p244)
- [geminiorganized/General_Ankijs](#p245)
- [geminiorganized/General_Formforge](#p254)
- [geminiorganized/General_Recipeweb](#p277)
- [geminiorganized/LLM_Generated_Buildbusinesses](#p283)
- [jobtrack](#p350)
- [lucasrouter](#p356)
- [recipeweb](#p384)
- [_Organized Desktop/01 Net Workspaces/.netpastebin](#p009)
- [borrowbox](#p221)
- [geminiorganized/General_Borrowbox](#p247)
- [geminiorganized/General_Newcodexjs](#p269)
- [geminiorganized/General_Recipeview](#p276)
- [geminiorganized/OpenSource_Upskilling_Snapshot](#p316)
- [geminiorganized/OpenSource_Upskilling_Snapshot1](#p317)
- [netsnapshot](#p375)
- [netsnapshot1](#p376)
- [newcodexJS](#p379)
- [newcodexJS/01-task-manager](#p440)
- [newcodexJS/02-contact-book](#p441)
- [newcodexJS/03-expense-tracker](#p442)
- [newcodexJS/04-notes-app](#p443)
- [newcodexJS/06-bookmark-manager](#p445)
- [recipeview](#p383)

## Per-project improvement plans

<a id="p024"></a>
### _Organized Desktop/02 Build Projects/buildgum

Buildgum is a Gumroad-style creator commerce prototype built with Vite, React, TypeScript, and lucide-react.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Frontend commerce prototype; do not infer an operational payment/backend system from screens.
- **Recorded stack:** CSS, HTML, TypeScript, React, Vite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildgum/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to relational modeling, pricing, stock reservations, order state transitions.
- **2 — Improve the project/resource:** First scoped project change: Trace an order/reservation and test invalid transitions or repeated submissions. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildgum/README.md), [index.html](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildgum/index.html), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildgum/src/App.tsx).

---

<a id="p027"></a>
### _Organized Desktop/02 Build Projects/buildsubbox

ParcelPilot subscription-box UI prototype for subscriber preferences, billing, curation, and fulfillment.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Teaching implementation/prototype with an explicit limitation; runtime unverified. Limits: Frontend prototype with backend/API/testing work discussed as a next layer.
- **Recorded stack:** CSS, HTML, JavaScript, React, Vite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildsubbox/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of money units, state transitions and duplicate deliveries, an expected-state example and a guided-to-independent change exercise. Tie it to money arithmetic, idempotency, webhook processing, transaction boundaries.
- **2 — Improve the project/resource:** First scoped project change: Trace a charge or webhook and design a replay test that cannot double-apply it. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Use a fake provider and a fixed amount; repeat one financial event and verify one durable effect and an auditable rejection or replay result. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildsubbox/docs/upskill/README.md), [index.html](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildsubbox/index.html), [App.jsx](C:/Users/Owner/Desktop/_Organized%20Desktop/02%20Build%20Projects/buildsubbox/src/App.jsx).

---

<a id="p074"></a>
### _Organized Desktop/04 JavaScript Training/jstrain2.3

A Notion-style collaborative workspace built with Next.js (App Router), SQLite, Zustand, dnd-kit, and Fuse.js.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, Next.js, Node.js, React, Tailwind CSS, Prisma, SQLite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [package.json.guide.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.3/_learning/guides/package.json.guide.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of tree structure, revisions and inherited permissions, an expected-state example and a guided-to-independent change exercise. Tie it to content modeling, revisions, authorization, search, optimistic concurrency.
- **2 — Improve the project/resource:** First scoped project change: Trace an edit and test a stale revision or forbidden share. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.3/README.md), [page.js](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.3/src/app/page.js), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.3/package.json).

---

<a id="p079"></a>
### _Organized Desktop/04 JavaScript Training/react

Small browser-based Jeopardy game.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, HTML, JavaScript.
- **Learning content now:** No substantive guide verified. No populated entrypoint verified in the tutorial review.
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of server authority, timer ownership and command ordering, known stubs and one exercise targeting event/state modeling, real-time synchronization, validation, reconnect behavior. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Isolate a game/message state transition and specify duplicate-event/reconnect tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [data.js](C:/Users/Owner/Desktop/_Organized%20Desktop/04%20JavaScript%20Training/react/data.js).

---

<a id="p099"></a>
### _Organized Desktop/05 Numbered Experiments/g1

Bagel Atlas directory for exploring bagel shops and cities.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, SQL, TypeScript, Next.js, Node.js, React, Tailwind CSS, Drizzle, Anthropic API.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/g1/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting forms, client state, data transforms, search/filtering, API error states. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Build or explain one complete user interaction with empty/loading/error behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/g1/README.md), [env.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/g1/src/lib/env.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/g1/package.json).

---

<a id="p151"></a>
### _Organized Desktop/05 Numbered Experiments/X1

A TypeScript app for discovering, ranking, and operating bagel shop data across multiple cities.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, SQLite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [06-frontend-walkthrough.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/X1/bagel-intel-platform/docs/learning/06-frontend-walkthrough.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to forms, client state, data transforms, search/filtering, API error states.
- **2 — Improve the project/resource:** First scoped project change: Build or explain one complete user interaction with empty/loading/error behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/X1/bagel-intel-platform/README.md), [db.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/X1/bagel-intel-platform/src/lib/db.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/X1/bagel-intel-platform/package.json).

---

<a id="p157"></a>
### _Organized Desktop/05 Numbered Experiments/z9

Freelancer and agency operations portal.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Teaching implementation with documented simulated/demo boundaries; runtime unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Prisma, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [how-to-study-this-codebase.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z9/docs/learning/how-to-study-this-codebase.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to semantic HTML, component composition, forms, integration boundaries.
- **2 — Improve the project/resource:** First scoped project change: Review one page/form for keyboard use and predictable validation; isolate one integration. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z9/README.md), [service.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z9/src/modules/auth/service.ts), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/05%20Numbered%20Experiments/z9/package.json).

---

<a id="p172"></a>
### _Organized Desktop/06 AI And Learning/claudeailab-temp

Next.js starter retained alongside the AI-lab project; substantive app behavior was not established.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified. Limits: Generic Next.js starter.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Drizzle, SQLite.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab-temp/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting Next.js starter structure. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Prefer claudeailab for domain work; use this only for a clean scaffold comparison. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab-temp/README.md), [next.config.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab-temp/next.config.ts), [page.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab-temp/src/app/page.tsx).

---

<a id="p178"></a>
### _Organized Desktop/07 Anti Projects/antiinv

Frontend/backend starter with a generic sign-in screen; its intended inventory domain remains unverified.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified. Limits: Generic sign-in frontend/backend starter; the intended inventory domain is unverified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Tailwind CSS, Vite, Prisma, Redis, Docker, Vitest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antiinv/frontend/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of stock ownership, checkout and order transitions, known stubs and one exercise targeting frontend/backend contract exploration; domain clarification. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Establish the actual domain by reading schema and routes before expanding the starter. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Use a tiny stock fixture; verify one successful operation, one invalid transition and a repeated or competing mutation without inconsistent stock. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antiinv/frontend/README.md), [auth.routes.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antiinv/backend/src/modules/auth/auth.routes.ts), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/07%20Anti%20Projects/antiinv/frontend/src/App.tsx).

---

<a id="p187"></a>
### _Organized Desktop/08 App And Product Projects/recipegen-app

Weeknight recipe app that suggests dinner ideas from available ingredients.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Anthropic API.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting forms, client state, ingredient transforms, loading/error states. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace ingredients to suggestions and define empty-input and failed-request behavior. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app/README.md), [page.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app/app/page.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app/package.json).

---

<a id="p188"></a>
### _Organized Desktop/08 App And Product Projects/recipegen-temp

Next.js starter retained alongside the recipe app.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified. Limits: Generic Next.js starter.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-temp/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting Next.js starter structure. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Prefer recipegen-app for domain work; use this only for a scaffold comparison. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-temp/README.md), [next.config.ts](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-temp/next.config.ts), [page.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-temp/src/app/page.tsx).

---

<a id="p194"></a>
### _Organized Desktop/12 Other Projects/3buildhyper

HyperNova agency website with service pages, content tooling, and Amplify/HubSpot integration material.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, AWS SDK, GitHub Actions, Jest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/3buildhyper/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to React/Next page composition, accessibility, forms, content/integration boundaries.
- **2 — Improve the project/resource:** First scoped project change: Compare with hypernova-inc-main and complete one bounded page/form improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/3buildhyper/README.md), [services.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/3buildhyper/pages/services.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/3buildhyper/package.json).

---

<a id="p200"></a>
### _Organized Desktop/12 Other Projects/FinalJep

Convex/React app variants with chat components; a Jeopardy implementation was not established in the inspected samples.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified. Limits: Sampled components are chat-oriented; the name does not establish a Jeopardy implementation.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Vite.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/FinalJep/finaljep-app/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of server authority, timer ownership and command ordering, known stubs and one exercise targeting React/Convex workspace comparison and scope identification. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Compare the two app variants and locate actual game logic before selecting a build target. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/FinalJep/finaljep-app/README.md), [App.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/FinalJep/finaljep-app/src/App.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/FinalJep/finaljep-app/package.json).

---

<a id="p202"></a>
### _Organized Desktop/12 Other Projects/GlobGame

Globs is a daily hierarchical merge puzzle game built with Next.js, JavaScript, Prisma, and PostgreSQL.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, Next.js, Node.js, React, Tailwind CSS, Prisma.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/GlobGame/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of server authority, timer ownership and command ordering: ordered source files, one input-to-state trace, a diagram and one independent change targeting pure game rules, deterministic state transitions, persistence.
- **2 — Improve the project/resource:** First scoped project change: Extract and test a merge rule including invalid moves and repeat daily play. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Use a fake clock and replay one command or worker delivery; verify resources and completion effects are applied consistently once. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/GlobGame/README.md), [page.js](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/GlobGame/src/app/page.js), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/GlobGame/package.json).

---

<a id="p203"></a>
### _Organized Desktop/12 Other Projects/hypernova-inc-main

HyperNova agency website with service pages, content tooling, and Amplify/HubSpot integration material.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: Language fundamentals, HTML/CSS, DOM events, and basic debugging.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, GitHub Actions, Jest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/hypernova-inc-main/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, ordering and lifecycle transitions, an expected-state example and a guided-to-independent change exercise. Tie it to page composition, accessibility, content, forms/integration boundaries.
- **2 — Improve the project/resource:** First scoped project change: Compare with 3buildhyper and choose one canonical branch for a small page/form task. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/hypernova-inc-main/README.md), [services.tsx](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/hypernova-inc-main/pages/services.tsx), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/12%20Other%20Projects/hypernova-inc-main/package.json).

---

<a id="p213"></a>
### AlanAndEliSoccer

A Next.js learning app for the 17 Laws of Soccer, World Cup context, and practical match tools.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Recognizable content application; catalog found no tests. Treat sports content separately from code study. Static review only; not built, tested or run.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/AlanAndEliSoccer/soccer-laws-app/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of tree structure, revisions and inherited permissions, known stubs and one exercise targeting Next.js routes, content modeling, search, local UI state. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Add a tested saved-law or referee-tool interaction. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Alanandelisoccer](C:/Users/Owner/Desktop/geminiorganized/General_Alanandelisoccer). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/AlanAndEliSoccer/soccer-laws-app/README.md), [RefereeNotebook.tsx](C:/Users/Owner/Desktop/AlanAndEliSoccer/soccer-laws-app/src/components/tools/RefereeNotebook.tsx), [package.json](C:/Users/Owner/Desktop/AlanAndEliSoccer/soccer-laws-app/package.json).

---

<a id="p214"></a>
### ankijs

A , local-first spaced-repetition web app for the spare minutes in your day.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Substantial local-first flashcard app with tests; optional Supabase sync is separate from offline study. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, Python, SQL, TypeScript, React, Tailwind CSS, Vite, IndexedDB / Dexie, Supabase, GitHub Actions, Playwright, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/ankijs/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to Spaced repetition, IndexedDB, offline state, optional sync.
- **2 — Improve the project/resource:** First scoped project change: Use short daily recall sessions; study one scheduling or sync invariant. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/ankijs/README.md), [App.tsx](C:/Users/Owner/Desktop/ankijs/src/App.tsx), [package.json](C:/Users/Owner/Desktop/ankijs/package.json).

---

<a id="p219"></a>
### astra4.2

Hourly focus timer with fullscreen art breaks and custom reminders, packaged as a Chrome Manifest V3 extension with a local Node preview.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Partial implementation: timer state machine, extension background code and UI source are present. extension/assets is empty although app.js references artwork; generated extension/app.js and tests directory are absent. No build or runtime verification.
- **Recorded stack:** JavaScript, HTML, CSS, Chrome Extension Manifest V3, Node.js, Chrome storage / local browser state, esbuild, Node test script; referenced test directory absent, Chrome alarms.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/astra4.2/README.md).
- **1 — Improve the upskilling content:** Map timer states and extension events; document source-to-bundle steps and asset fallback behavior.
- **2 — Improve the project/resource:** Supply a fallback for missing artwork, add focus/pause/break state tests, and produce the referenced extension bundle from source.
- **3 — Prove completion:** Simulate pause/resume and a delayed alarm; confirm no skipped/double break and confirm the packaged extension resolves every referenced asset.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [package.json](C:/Users/Owner/Desktop/astra4.2/package.json), [manifest.json](C:/Users/Owner/Desktop/astra4.2/extension/manifest.json), [app.js](C:/Users/Owner/Desktop/astra4.2/src/app.js).

---

<a id="p222"></a>
### buildbusinesses

LocalOps Ledger for keeping daily operating records for small local businesses.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Small custom UI behind a stock Next.js README; backend durability is not established by the sample. Static review only; not built, tested or run.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/buildbusinesses/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to React forms, dashboard state, business record modeling.
- **2 — Improve the project/resource:** First scoped project change: Trace LocalOperationsApp state and add one validated record flow. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/LLM_Generated_Buildbusinesses](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildbusinesses). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/buildbusinesses/README.md), [page.tsx](C:/Users/Owner/Desktop/buildbusinesses/src/app/page.tsx), [package.json](C:/Users/Owner/Desktop/buildbusinesses/package.json).

---

<a id="p230"></a>
### calendar+jobtrack

A personal calendar and a gamified job-application tracker in one local-first app.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Local-only React app with test files; no account or backend by design. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, TypeScript, React, Tailwind CSS, Vite, Vitest.
- **Learning content now:** Developer explanation / brief orientation. Start at [README.md](C:/Users/Owner/Desktop/calendar%2Bjobtrack/README.md).
- **1 — Improve the upskilling content:** Expand the orientation into a 30–60 minute walkthrough of local persistence, replay and conflict resolution: ordered source files, one input-to-state trace, a diagram and one independent change targeting TypeScript, Zustand, calendar state, local persistence.
- **2 — Improve the project/resource:** First scoped project change: Add one calendar conflict or job-stage validation case with a test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/calendar%2Bjobtrack/README.md), [App.tsx](C:/Users/Owner/Desktop/calendar%2Bjobtrack/src/App.tsx), [package.json](C:/Users/Owner/Desktop/calendar%2Bjobtrack/package.json).

---

<a id="p239"></a>
### formforge

FormForge is a , schema-driven form builder and response analytics platform built as a fifteen-sprint React and TypeScript teaching repository.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Substantial teaching app and tests; API repository adapters include in-memory storage. Static review only; not built, tested or run.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Fastify, Node.js, React, Vite, GitHub Actions, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [0001-client-rendered-teaching-boundary.md](C:/Users/Owner/Desktop/formforge/docs/adr/0001-client-rendered-teaching-boundary.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for event identity, aggregation and reporting filters; make learners predict state before running it. Teach TypeScript schemas, React reducers, validation, branching, tests with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Follow the fifteen-sprint sequence; add one field type with validation tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Formforge](C:/Users/Owner/Desktop/geminiorganized/General_Formforge). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/formforge/README.md), [App.tsx](C:/Users/Owner/Desktop/formforge/apps/web/src/App.tsx), [package.json](C:/Users/Owner/Desktop/formforge/package.json).

---

<a id="p244"></a>
### geminiorganized/General_Alanandelisoccer

A Next.js learning app for the 17 Laws of Soccer, World Cup context, and practical match tools.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Alanandelisoccer/soccer-laws-app/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of tree structure, revisions and inherited permissions, known stubs and one exercise targeting Next.js routes, content modeling, search, local UI state. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Add a tested saved-law or referee-tool interaction. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Reject a recursive move or forbidden edit; verify a permitted edit/restore preserves coherent history. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [AlanAndEliSoccer](C:/Users/Owner/Desktop/AlanAndEliSoccer). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Alanandelisoccer/soccer-laws-app/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Alanandelisoccer/soccer-laws-app/package.json), [RefereeNotebook.tsx](C:/Users/Owner/Desktop/geminiorganized/General_Alanandelisoccer/soccer-laws-app/src/components/tools/RefereeNotebook.tsx).

---

<a id="p245"></a>
### geminiorganized/General_Ankijs

Recall is a local-first spaced-repetition PWA with quick capture, inbox triage, and offline study.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, SQL, TypeScript, React, Tailwind CSS, Vite, IndexedDB / Dexie, Supabase, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Ankijs/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of availability and local-time conversion, an expected-state example and a guided-to-independent change exercise. Tie it to Spaced repetition, IndexedDB, offline state, optional sync.
- **2 — Improve the project/resource:** First scoped project change: Use short daily recall sessions; study one scheduling or sync invariant. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Use a fixed clock and two competing requests for the last available resource; prove capacity and timezone rules hold. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [ankijs](C:/Users/Owner/Desktop/ankijs). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Ankijs/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Ankijs/net/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Ankijs/package.json).

---

<a id="p254"></a>
### geminiorganized/General_Formforge

FormForge is a , schema-driven form builder and response analytics platform built as a fifteen-sprint React and TypeScript teaching repository.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Relevant implementation is present; runtime not verified. Local documentation: API --> Data[@formforge/data\nrepository contracts + in-memory adapters]
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Fastify, Node.js, React, Vite, GitHub Actions, Vitest.
- **Learning content now:** Structured tutorial / exercises. Start at [0001-client-rendered-teaching-boundary.md](C:/Users/Owner/Desktop/geminiorganized/General_Formforge/docs/adr/0001-client-rendered-teaching-boundary.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for event identity, aggregation and reporting filters; make learners predict state before running it. Teach TypeScript schemas, React reducers, validation, branching, tests with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Follow the fifteen-sprint sequence; add one field type with validation tests. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [formforge](C:/Users/Owner/Desktop/formforge). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Formforge/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Formforge/package.json), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Formforge/apps/api/package.json).

---

<a id="p277"></a>
### geminiorganized/General_Recipeweb

A Filipino, Vietnamese, Thai & Spanish cookbook companion web app.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 2; prerequisites: JavaScript/TypeScript fundamentals, HTML/CSS and basic React.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, React, Vite, GitHub Actions.
- **Learning content now:** Codebase walkthrough / study pack. Start at [05-EXERCISES.md](C:/Users/Owner/Desktop/geminiorganized/General_Recipeweb/docs/05-EXERCISES.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Components, typed data, filters, context/local persistence and accessible list interactions..
- **2 — Improve the project/resource:** First scoped project change: Implement one shopping-list behavior and verify persistence/accessibility; use the net plan later as an API extension exercise. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [recipeweb](C:/Users/Owner/Desktop/recipeweb). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Recipeweb/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Recipeweb/package.json), [App.tsx](C:/Users/Owner/Desktop/geminiorganized/General_Recipeweb/src/App.tsx).

---

<a id="p283"></a>
### geminiorganized/LLM_Generated_Buildbusinesses

LocalOps Ledger for keeping daily operating records for small local businesses.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildbusinesses/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to React forms, dashboard state, business record modeling.
- **2 — Improve the project/resource:** First scoped project change: Trace LocalOperationsApp state and add one validated record flow. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [buildbusinesses](C:/Users/Owner/Desktop/buildbusinesses). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildbusinesses/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildbusinesses/docs/upskill/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/LLM_Generated_Buildbusinesses/package.json).

---

<a id="p350"></a>
### jobtrack

Daybook local-first calendar and job-application tracker.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Small Daybook app with tests; related concept to calendar+jobtrack but a separate implementation. Static review only; not built, tested or run.
- **Recorded stack:** HTML, JavaScript, React, Vite, Vitest.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/jobtrack/fabledocs/README.md).
- **1 — Improve the upskilling content:** Extend the Daybook cartography with import/export schema, storage ownership and migration examples.
- **2 — Improve the project/resource:** Make one import atomic and validate its schema; preserve the current local-first design.
- **3 — Prove completion:** Export, clear a disposable profile, and import to recover equivalent records; malformed input must leave existing data intact.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/jobtrack/README.md), [App.jsx](C:/Users/Owner/Desktop/jobtrack/src/App.jsx), [package.json](C:/Users/Owner/Desktop/jobtrack/package.json).

---

<a id="p356"></a>
### lucasrouter

Fleet and delivery-routing workspace with searchable stops, delivery status, and a driver interface.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 2; prerequisites: JavaScript fundamentals, basic HTML/CSS, modules and Git.
- **Baseline:** Substantial Next.js demo with tests; README says historical Lighthouse figures are not current measurements. Static review only; not built, tested or run.
- **Recorded stack:** CSS, JavaScript, TypeScript, Next.js, Node.js, React, Tailwind CSS, Vitest.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/lucasrouter/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of the documented workflow and its state boundary, known stubs and one exercise targeting Complex React state, maps, lazy loading, fleet UX. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace one stop status update and verify map/list/driver views agree. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** For the currently implemented client surface, exercise a valid action, invalid input and reload, plus keyboard use where interactive. Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. Use local fixtures if no server exists; a server is a later milestone.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/lucasrouter/README.md), [DriverRoutes.tsx](C:/Users/Owner/Desktop/lucasrouter/src/components/dispatch/DriverRoutes.tsx), [package.json](C:/Users/Owner/Desktop/lucasrouter/package.json).

---

<a id="p384"></a>
### recipeweb

A Filipino, Vietnamese, Thai & Spanish cookbook companion web app.

- **Use / order:** Primary route candidate; complete this milestone before adding an alternative. Original milestone 2; prerequisites: JavaScript/TypeScript fundamentals, HTML/CSS and basic React.
- **Baseline:** Static React cookbook with routing and shopping-list state. net/ contains planning documents for a .NET extension, not a backend implementation.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, React, Vite, GitHub Actions.
- **Learning content now:** Codebase walkthrough / study pack. Start at [01-ONBOARDING.md](C:/Users/Owner/Desktop/recipeweb/docs/01-ONBOARDING.md).
- **1 — Improve the upskilling content:** Connect onboarding to shopping-list state, persistence and keyboard interactions; keep the proposed .NET extension labeled as future work.
- **2 — Improve the project/resource:** Complete one shopping-list operation with persisted quantities and accessible controls.
- **3 — Prove completion:** Reload after changing a quantity; verify it survives and that the same operation works with keyboard input.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Recipeweb](C:/Users/Owner/Desktop/geminiorganized/General_Recipeweb). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/recipeweb/README.md), [App.tsx](C:/Users/Owner/Desktop/recipeweb/src/App.tsx), [HomePage.tsx](C:/Users/Owner/Desktop/recipeweb/src/pages/HomePage.tsx).

---

<a id="p009"></a>
### _Organized Desktop/01 Net Workspaces/.netpastebin

Small C#/ASP.NET Core paste-sharing API and UI learning project.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 3; prerequisites: Language fluency, HTTP/JSON, SQL CRUD, and asynchronous code.
- **Baseline:** Source implementation is indexed; runtime behavior remains unverified.
- **Recorded stack:** C#, CSS, HTML, JavaScript, TypeScript, ASP.NET Core, React, Vite.
- **Learning content now:** Codebase walkthrough / study pack. Start at [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netpastebin/docs/upskill/01-codebase-cartography/README.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to code navigation, contracts, validation, testing.
- **2 — Improve the project/resource:** First scoped project change: Trace one documented user flow from entry point to stored state and make one bounded improvement. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netpastebin/README.md), [Program.cs](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netpastebin/backend/Program.cs), [package.json](C:/Users/Owner/Desktop/_Organized%20Desktop/01%20Net%20Workspaces/.netpastebin/frontend/package.json).

---

<a id="p221"></a>
### borrowbox

BorrowBox is a beginner-friendly fifteen-sprint C#/.NET teaching repository for lending campus equipment such as laptops, cameras, calculators, and lab kits.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 3; prerequisites: Language basics, HTTP/JSON, simple relational data and Git.
- **Baseline:** Beginner-focused teaching repository with source/tests. Default API storage is non-durable; SQLite is an adapter exercise. X-Demo-Role is a teaching header, not production authentication. Static review only; not built, tested or run.
- **Recorded stack:** C#, SQL, ASP.NET Core, Entity Framework Core, SQLite, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/borrowbox/README.md).
- **1 — Improve the upskilling content:** Connect one borrowing-rule lesson to the API, domain checks and repository; explain X-Demo-Role and the optional SQLite adapter honestly.
- **2 — Improve the project/resource:** Add or strengthen a rule preventing the same equipment from being actively loaned twice. After that rule works, implement the SQLite adapter as a separate persistence milestone.
- **3 — Prove completion:** The first loan succeeds and a conflicting second loan fails without changing availability incorrectly. For the adapter milestone, restart the process and verify the loan remains recorded.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Borrowbox](C:/Users/Owner/Desktop/geminiorganized/General_Borrowbox). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/borrowbox/README.md), [Program.cs](C:/Users/Owner/Desktop/borrowbox/src/BorrowBox.Api/Program.cs), [BorrowBox.Api.csproj](C:/Users/Owner/Desktop/borrowbox/src/BorrowBox.Api/BorrowBox.Api.csproj).

---

<a id="p247"></a>
### geminiorganized/General_Borrowbox

BorrowBox is a beginner-friendly fifteen-sprint C#/.NET teaching repository for lending campus equipment such as laptops, cameras, calculators, and lab kits.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 3; prerequisites: Language basics, HTTP/JSON, simple relational data and Git.
- **Baseline:** Relevant implementation is present; runtime not verified. Local documentation: BorrowBox.Infrastructure in-memory and SQLite storage; OpenAPI is available at /openapi/v1.json in Development. Inventory reads and health endpoints are public. Mutating inventory uses the teaching header X-Demo-Role: Staff; borrowing accepts Student or Staff. This header is not production authentication.
- **Recorded stack:** C#, SQL, ASP.NET Core, Entity Framework Core, SQLite, GitHub Actions, xUnit.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Borrowbox/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for the documented workflow and its state boundary; make learners predict state before running it. Teach C# domain rules, minimal APIs, LINQ, DI, SQLite, tests with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Follow the fifteen sprints; independently add a borrowing rule and its test. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [borrowbox](C:/Users/Owner/Desktop/borrowbox). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Borrowbox/README.md), [BorrowBox.Api.csproj](C:/Users/Owner/Desktop/geminiorganized/General_Borrowbox/src/BorrowBox.Api/BorrowBox.Api.csproj), [BorrowBox.Core.csproj](C:/Users/Owner/Desktop/geminiorganized/General_Borrowbox/src/BorrowBox.Core/BorrowBox.Core.csproj).

---

<a id="p269"></a>
### geminiorganized/General_Newcodexjs

This workspace is organized around the Tier 1 web development curriculum: 15 self-contained full-stack apps for building junior-to-mid-level engineering patterns.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Vite, PostgreSQL.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/geminiorganized/General_Newcodexjs/01-task-manager/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, ordering and lifecycle transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Progressive REST/SQL/client integration, then auth and business workflows..
- **2 — Improve the project/resource:** First scoped project change: Begin 01-task-manager, then 05-recipe-manager; select one later domain challenge instead of completing all variants. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Newcodexjs/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Newcodexjs/04-notes-app/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Newcodexjs/package.json).

---

<a id="p276"></a>
### geminiorganized/General_Recipeview

Local-first cooking journal organized as Dish, Recipe, and Cook Log, with SQLite persistence and photo uploads.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** Relevant implementation is present; runtime not verified.
- **Recorded stack:** CSS, HTML, SQL, TypeScript, Express, Node.js, React, Vite.
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Recipeview/README.md).
- **1 — Improve the upskilling content:** Create a small codebase guide from implemented source: setup, ordered file map, one trace of local persistence, replay and conflict resolution, known stubs and one exercise targeting Relational modeling of dish/recipe/cook-log, SQL, file uploads and local-first UX.. Keep proposed architecture separate.
- **2 — Improve the project/resource:** First scoped project change: Trace creation of a recipe and cook log into SQLite, then test rollback and search-index consistency. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Save a change, reload, and replay its sync/import; verify no loss or duplicate state and an explicit conflict outcome. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [recipeview](C:/Users/Owner/Desktop/recipeview). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/General_Recipeview/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/General_Recipeview/package.json), [App.tsx](C:/Users/Owner/Desktop/geminiorganized/General_Recipeview/src/App.tsx).

---

<a id="p316"></a>
### geminiorganized/OpenSource_Upskilling_Snapshot

NetAiOps is a simulated full-stack AI-powered IT operations platform built as a 15-step teaching history for a junior engineer.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** Teaching/reference workspace; runtime not verified. Local documentation: NetAiOps is a simulated full-stack AI-powered IT operations platform built as a 15-step teaching history for a junior engineer. Browse snapshots/ in order; each folder contains a full copy of the codebase at that moment plus NOTES.md and CHANGES.md.
- **Recorded stack:** CSS, HTML, TypeScript, GitHub Actions.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Snapshot/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for tool or retrieval boundaries and explicit failure behavior; make learners predict state before running it. Teach How a walking skeleton becomes CRUD, auth, service layers, tests and operational features. with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Start snapshots/00-walking-skeleton/NOTES.md; predict each change, compare adjacent copies, and recreate one increment in your own branch. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed local fixture and mocked external responses; record expected output, an unavailable-tool case and a scored regression example. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [netsnapshot](C:/Users/Owner/Desktop/netsnapshot). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Snapshot/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Snapshot/snapshots/14-polish-and-docs/code/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Snapshot/snapshots/00-walking-skeleton/code/package.json).

---

<a id="p317"></a>
### geminiorganized/OpenSource_Upskilling_Snapshot1

Simulated fullstack teaching artifact for a TypeScript/Node backend and React frontend inspired by enterprise global workforce platforms.

- **Use / order:** Alternate copy; compare and choose a working baseline before investing. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** Teaching/reference workspace; runtime not verified. Local documentation: This repository is a simulated fullstack teaching artifact for a TypeScript/Node backend and React frontend inspired by enterprise global workforce platforms. Each folder under snapshots is a complete copy of the codebase at that moment in the project, not a diff, so a junior engineer can read the s
- **Recorded stack:** CSS, HTML, TypeScript.
- **Learning content now:** Codebase walkthrough / study pack. Start at [codebase-organization.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Snapshot1/snapshots/14-polish-docs/code/docs/codebase-organization.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of employee lifecycle, approval and tenant scope, an expected-state example and a guided-to-independent change exercise. Tie it to Incremental development, domain modeling, auth context and service refactoring..
- **2 — Improve the project/resource:** First scoped project change: Follow 00-walking-skeleton then implement one company workflow without copying its solution first. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [netsnapshot1](C:/Users/Owner/Desktop/netsnapshot1). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Snapshot1/README.md), [README.md](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Snapshot1/snapshots/14-polish-docs/code/README.md), [package.json](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Snapshot1/snapshots/00-walking-skeleton/code/package.json).

---

<a id="p375"></a>
### netsnapshot

NetAiOps is a simulated full-stack AI-powered IT operations platform built as a 15-step teaching history for a junior engineer.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** 15 full-copy chronological teaching snapshots of a simulated NetAiOps product. Sampled backend is TypeScript/Node and frontend React, despite .NET-sounding name.
- **Recorded stack:** TypeScript, Node.js, React, teaching snapshots.
- **Learning content now:** Structured tutorial / exercises. Start at [README.md](C:/Users/Owner/Desktop/netsnapshot/README.md).
- **1 — Improve the upskilling content:** Add a worked → partially guided → independent exercise for tool or retrieval boundaries and explicit failure behavior; make learners predict state before running it. Teach How a walking skeleton becomes CRUD, auth, service layers, tests and operational features. with a separate answer and rubric.
- **2 — Improve the project/resource:** First scoped project change: Start snapshots/00-walking-skeleton/NOTES.md; predict each change, compare adjacent copies, and recreate one increment in your own branch. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a fixed local fixture and mocked external responses; record expected output, an unavailable-tool case and a scored regression example. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/OpenSource_Upskilling_Snapshot](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Snapshot). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netsnapshot/README.md), [server.ts](C:/Users/Owner/Desktop/netsnapshot/snapshots/07-service-refactor/code/backend/src/server.ts), [App.tsx](C:/Users/Owner/Desktop/netsnapshot/snapshots/07-service-refactor/code/frontend/src/app/App.tsx).

---

<a id="p376"></a>
### netsnapshot1

Simulated fullstack teaching artifact for a TypeScript/Node backend and React frontend inspired by enterprise global workforce platforms.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** Chronological workforce-platform TypeScript/React teaching snapshots. Each snapshot is a full code copy, not a separate product to complete.
- **Recorded stack:** TypeScript, Node.js, React, teaching snapshots.
- **Learning content now:** Codebase walkthrough / study pack. Start at [codebase-organization.md](C:/Users/Owner/Desktop/netsnapshot1/snapshots/14-polish-docs/code/docs/codebase-organization.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of employee lifecycle, approval and tenant scope, an expected-state example and a guided-to-independent change exercise. Tie it to Incremental development, domain modeling, auth context and service refactoring..
- **2 — Improve the project/resource:** First scoped project change: Follow 00-walking-skeleton then implement one company workflow without copying its solution first. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use two fictional organizations; reject a cross-tenant or invalid lifecycle action and preserve the valid action’s audit history. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/OpenSource_Upskilling_Snapshot1](C:/Users/Owner/Desktop/geminiorganized/OpenSource_Upskilling_Snapshot1). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/netsnapshot1/README.md), [App.tsx](C:/Users/Owner/Desktop/netsnapshot1/snapshots/07-refactor-service-and-hooks/code/apps/web/src/App.tsx), [App.tsx](C:/Users/Owner/Desktop/netsnapshot1/snapshots/02-backend-crud/code/apps/web/src/App.tsx).

---

<a id="p379"></a>
### newcodexJS

Progressive React/Express/Knex/PostgreSQL learning workspace containing 20 child apps.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** 20 child React/Express/Knex/PostgreSQL apps. Maturity varies: 01 is small concrete CRUD; 05 includes JWT; several middle apps are generic scaffolds; 16-20 share admin CRUD patterns and titles overstate specialized capabilities.
- **Recorded stack:** CSS, HTML, JavaScript, TypeScript, Express, Node.js, React, Vite, PostgreSQL.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/01-task-manager/docs/FABLE.md).
- **1 — Improve the upskilling content:** Create a 20-app capability matrix: implemented source, teaching goals, known stubs and FABLE entrypoint.
- **2 — Improve the project/resource:** Standardize one selected child’s reproducible setup and fixtures; extend only that child’s actual workflow.
- **3 — Prove completion:** The matrix distinguishes generic CRUD from real domain behavior, and the chosen child passes its own completion criterion below.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Newcodexjs](C:/Users/Owner/Desktop/geminiorganized/General_Newcodexjs). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/README.md), [App.jsx](C:/Users/Owner/Desktop/newcodexJS/04-notes-app/client/src/App.jsx), [App.jsx](C:/Users/Owner/Desktop/newcodexJS/01-task-manager/client/src/App.jsx).

---

<a id="p440"></a>
### newcodexJS/01-task-manager

Task manager

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified.
- **Recorded stack:** JavaScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/01-task-manager/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of ownership, ordering and lifecycle transitions, an expected-state example and a guided-to-independent change exercise. Tie it to Basic REST, validation, React state and SQL queries.
- **2 — Improve the project/resource:** First scoped project change: Build and explain one create/edit/filter/delete flow, including invalid input. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Test a valid transition, an unauthorized actor and a stale or invalid update; verify stored state and displayed state agree. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/01-task-manager/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/01-task-manager/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/01-task-manager/client/package.json).

---

<a id="p441"></a>
### newcodexJS/02-contact-book

Contact book

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified.
- **Recorded stack:** JavaScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/02-contact-book/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Many-to-many tags, pagination, debounced search and CSV.
- **2 — Improve the project/resource:** First scoped project change: Add a contact with tags and verify pagination plus malformed CSV handling. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/02-contact-book/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/02-contact-book/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/02-contact-book/client/package.json).

---

<a id="p442"></a>
### newcodexJS/03-expense-tracker

Expense tracker

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified.
- **Recorded stack:** JavaScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/03-expense-tracker/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of event identity, aggregation and reporting filters, an expected-state example and a guided-to-independent change exercise. Tie it to SQL aggregation, category budgets, filters and charts.
- **2 — Improve the project/resource:** First scoped project change: Verify monthly totals and category boundaries with a small deterministic dataset. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Compare a report with a hand-calculated fixture containing duplicates and boundary values; verify permissions and deterministic totals. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/03-expense-tracker/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/03-expense-tracker/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/03-expense-tracker/client/package.json).

---

<a id="p443"></a>
### newcodexJS/04-notes-app

Notes app

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Recorded stack:** JavaScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/04-notes-app/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of the documented workflow and its state boundary, an expected-state example and a guided-to-independent change exercise. Tie it to Generic CRUD with markdown/folder/tag/autosave learning goals.
- **2 — Improve the project/resource:** First scoped project change: Implement and verify one actual autosave or search behavior beyond the generic scaffold. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Demonstrate the selected behavior with one valid input and one meaningful invalid or failure case; verify the resulting state and explain the exact code path. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/04-notes-app/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/04-notes-app/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/04-notes-app/client/package.json).

---

<a id="p445"></a>
### newcodexJS/06-bookmark-manager

Bookmark manager

- **Use / order:** Optional targeted exercise; choose one topic and one language variant. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** React/Express/Knex/PostgreSQL learning application; README, manifests and service source freshly inspected. Runtime and production readiness unverified. Sampled service is a generic CRUD scaffold; listed domain learning goals need implementation-depth checks.
- **Recorded stack:** TypeScript, React, Vite, Express, Knex, PostgreSQL.
- **Parent workspace:** [newcodexJS](C:/Users/Owner/Desktop/newcodexJS). Parent-level work does not replace this child’s task.
- **Learning content now:** Codebase walkthrough / study pack. Start at [FABLE.md](C:/Users/Owner/Desktop/newcodexJS/06-bookmark-manager/docs/FABLE.md).
- **1 — Improve the upskilling content:** Extend the existing walkthrough with a source-linked trace of outbound target validation, timeouts and response limits, an expected-state example and a guided-to-independent change exercise. Tie it to Typed validation, URL metadata boundaries and API conventions.
- **2 — Improve the project/resource:** First scoped project change: Implement one validated bookmark create flow and a safe metadata-fetch boundary. Confirm the present behavior; implement the missing case, or strengthen its regression coverage if already correct.
- **3 — Prove completion:** Use a controlled HTTP stub to verify one allowed request, a forbidden target, a redirect to a forbidden target, a timeout and an oversized response; rejected requests must not reach protected destinations. If persistence is implemented, verify state across process restart and a failed write.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Variant caveat:** Related curriculum exercise, not evidence of a separate unique architecture. Select by learning gap.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/newcodexJS/06-bookmark-manager/README.md), [package.json](C:/Users/Owner/Desktop/newcodexJS/06-bookmark-manager/server/package.json), [package.json](C:/Users/Owner/Desktop/newcodexJS/06-bookmark-manager/client/package.json).

---

<a id="p383"></a>
### recipeview

Local-first cooking journal organized as Dish, Recipe, and Cook Log, with SQLite persistence and photo uploads.

- **Use / order:** Alternative project; select for a measured skill gap, not as additional mandatory work. Original milestone 3; prerequisites: React state, HTTP/JSON, JavaScript/TypeScript or C# fundamentals and basic SQL.
- **Baseline:** Local-first Recipe Lab application with React and Express source. server/db.ts uses Node node:sqlite DatabaseSync, transaction helper and search indexing.
- **Recorded stack:** CSS, HTML, SQL, TypeScript, Express, Node.js, React, Vite, SQLite (node:sqlite).
- **Learning content now:** Plans, workflow, setup or reference only. Start at [README.md](C:/Users/Owner/Desktop/recipeview/README.md).
- **1 — Improve the upskilling content:** Diagram Dish → Recipe → Cook Log and the SQLite/photo/search write boundaries.
- **2 — Improve the project/resource:** Make one recipe-and-log update atomic and repair or explicitly handle search-index update failure.
- **3 — Prove completion:** Force a write failure; verify no half-created log, then verify search returns the committed recipe.
- **4 — Consolidate:** After the scoped change works, update the guide with actual commands/results and a short before/after explanation. Reuse the repository’s test tooling; do not migrate stacks just to standardize the collection.
- **Related locations to compare:** [geminiorganized/General_Recipeview](C:/Users/Owner/Desktop/geminiorganized/General_Recipeview). Similarity is not proof of identity; select the baseline using working setup, source and relevant tests.
- **Source-review evidence:** [README.md](C:/Users/Owner/Desktop/recipeview/README.md), [index.ts](C:/Users/Owner/Desktop/recipeview/server/index.ts), [App.tsx](C:/Users/Owner/Desktop/recipeview/src/App.tsx).

---
