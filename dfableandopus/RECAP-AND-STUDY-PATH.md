# Recap and study path

Fable, 2026-09-18. This is the single place to start. It covers what was reviewed, what was changed, what the new `dfableandopus/` folders are, and the order to study in.

Everything here refers to the 153 projects Astra changed. Each project has two learning folders:

- `<project>/astraupskill/` is the **course**: how the app works, the worked change, tests, practice, solutions, a trace lab.
- `<project>/dfableandopus/` is the **job and interview pack** for the same project (in progress, see section 3).

Supporting material lives in `AstraOrganized2/fablereview/`.

## 1. What was done, in order

| step | what | where |
|---|---|---|
| Review (2026-09-16) | Every project scored on 8 dimensions by 18 Opus reviewers under Fable's rubric. Verdicts: KEEP 89, IMPROVE 55, REWORK 9. | `fablereview/SUMMARY.md`, `SCOREBOARD.md`, `reviews/<slug>.md` |
| Fix pass (2026-09-17 to 18) | Every "Improvements needed" item applied to all 153 projects. Code changes verified by running each project's own tests. | `fablereview/_fix/FIX_REPORT.md`, `_fix/reports/<slug>.md` |
| Interview packs (2026-09-18, ongoing) | A seven-file `dfableandopus/` folder per project, written by Opus builders, reviewed by Fable. | `fablereview/_dfableandopus/STATUS.md` |

## 2. Improvements made in the fix pass

**Courses (all 153).**

- Wrong-project names and wrong-stack setup text removed from the 75 generated courses (68 affected, now 1, which is a project naming its own product).
- Every course now has real code blocks in chapters 03, 04, 06 and 07 (145 lacked them). The blocks are copied from the project's own source and tests, with file citations.
- Every bespoke course has a prerequisites and glossary section where each term points at a real file or symbol (77 lacked one).
- Generic "variations", review paragraphs and trace-lab boundaries replaced with project-specific ones in the 54 non-clone generated courses.
- Off-stack projects (Java, Python) gained a translation chapter mapping each mechanism to Express/Prisma and ASP.NET/EF Core.
- Agent-process language, byte-order marks and minified test files cleaned up. Dependency versions pinned.

**Code, each verified by tests.**

- Real defects fixed: master4 stock reservation double-counting duplicate SKUs; master3 asking for Serializable isolation with no retry; job-track live chat reading its "mark read" range outside the transaction; master-6 catching any error shaped like a unique violation; newcodexJS 05 treating a missing `isPublic` as public; JS1 secure-notes sessions that never expired; JS1 subscription-billing fractional cents; plus about twenty smaller ones listed in `FIX_REPORT.md`.
- New runnable material: a contacts CRUD module with tests in buildCRMPYJS; an HTTP plus SQLite starter service in astra4.2; buildsql's 1,098-line `App.tsx` split into views; integration tests against a real PostgreSQL for master2 and master3; the nethris dispatcher rewritten from 194 golfed lines into four readable files with identical behavior (28 xUnit and 28 black-box checks pass before and after).

**Known limits, stated honestly.**

- The 21 clone projects still share most of their generated prose. Skip them (list in section 4).
- The Shopify token found in an Astra backup was redacted in the file, but **you still need to revoke it in the Shopify admin**.

## 3. The `dfableandopus/` interview packs

Each pack has seven files, all grounded in that project's real code with `path:line` citations:

| file | use it for |
|---|---|
| `README.md` | the project pitch and a two-week prep plan |
| `01-INTERVIEW-QUESTIONS.md` | 24 to 30 questions with model answers: screening, deep-dive on the real bug, behavioral, interviewer follow-ups |
| `02-STORIES-AND-RESUME.md` | three STAR stories, five resume bullets, a 60-second spoken summary |
| `03-CODE-READING-DRILL.md` | explain-this-function, spot-the-bug, predict-the-status-code, review-this-diff, with hidden answers |
| `04-TAKE-HOME.md` | a 3 to 4 hour take-home on this codebase with a grading rubric |
| `05-SYSTEM-DESIGN-FOLLOWUPS.md` | "now scale it" questions answered from what the code does today |
| `06-FLASHCARDS.md` | 30 to 40 project-specific cards |

**Status: 34 of 153 complete.** Work stopped when the account hit its usage limit and resumes on request. Per-batch state is in `fablereview/_dfableandopus/STATUS.md`. Completed packs so far share 0 to 1 percent of their paragraphs with each other and average about 8,000 words.

## 4. Recommended study order

Do one project at a time. For each: read `astraupskill/` chapters 01, 03 and 07 closely, do one practice exercise, then work the `dfableandopus/` pack (questions aloud, one drill, the flashcards). Do the take-home only for the projects marked with a star.

### Stage 0: browser CRUD reasoning (2 short sessions)

1. `JS1/task-board`: save before you publish, undo that survives reload.
2. `JS1/note-vault`: the same ideas against an Express API.

### Stage 1: Express and PostgreSQL fundamentals (about 2 weeks)

3. `newcodexJS/01-task-manager`: validation, 400 versus 500, test harness.
4. `newcodexJS/02-contact-book`: CSV import, a transaction across three tables, stable pagination.
5. `newcodexJS/03-expense-tracker`: money validation, partial updates.
6. `newcodexJS/04-notes-app`: search that does not match ids and timestamps.
7. `newcodexJS/05-recipe-manager` ★: ownership, authentication versus authorization, row locks. This is the first project worth a take-home.

### Stage 2: TypeScript, transactions and concurrency (about 3 weeks)

8. `JS1/org-explorer`: closing a check-then-write race under a lock.
9. `JS1/room-booking`: overlap prevention with range types and an exclusion constraint.
10. `JS1/warehouse-ledger`: concurrent stock issue with an exact final balance.
11. `newcodexJS/13-ecommerce-storefront` ★: lock ordering, rollback tests.
12. `newcodexJS/14-appointment-booking`: the overlap rule inside the transaction.
13. `newcodexJS/11-survey-builder`: a capacity counter, Zod at the boundary.
14. `newcodexJS/07-blog-platform`: undefined versus null versus absent in PATCH. Do only this one of 07 to 10.
15. `newcodexJS/16-team-project-management`: archive, restore, bulk audit. Do only this one of 16 to 20.
16. `JS1/secure-notes`: token auth, now with session expiry.
17. `JS1/learning-paths`: one status transition, one transaction, one audit row.

### Stage 3: Prisma apps with tenancy and versioning (about 3 weeks)

18. `grokbuildorderproject`: optimistic concurrency with a conditional update.
19. `grokbuildteamproject` ★: compound foreign keys so the database rejects cross-tenant writes.
20. `grokbuildhrproject`: approval chains, advisory locks and their cost.
21. `master4`: stock reservation, now with the duplicate-SKU fix.
22. `buildCRMPYJS` ★: privilege escalation at registration, then the new contacts CRUD chapter.
23. `appmakertrack`: 409 semantics, ordered moves.
24. `master3`, then `master2`: Serializable with retry; webhooks, idempotency and why headers are not identity. Both now have real-database tests.

### Stage 4: Next.js (about 2 weeks)

25. `e6`, 26. `b1`, 27. `ww37`: authorization before pagination, membership checks, PATCH semantics and async `params`.
28. `z3/customer-feedback-board`, 29. `z3/founder-crm-lite`: server actions, SQLite write transactions, revalidation after commit.
30. `z7`, 31. `d1`, 32. `jdtrrain2.1`: what leaks into the client payload, atomic version bumps, Prisma with conditional updates.
33. `job track/restaurant-kitchen-display-system` ★: the best React app in the set. Its new exercise 7 (compare-and-set) is interview gold.

### Stage 5: C# and .NET (about 3 weeks)

34. `meterforge`: idempotent ingestion, Problem Details.
35. `borrowbox`, 36. `netgum`: domain rules, EF Core with real xUnit tests.
37. `nethris` ★: EF Core and SQLite transactions, ETag and If-Match, idempotency receipts. Read the rewritten `HrisApi*.cs` files.
38. `campusops`, 39. `missioncontrol`, 40. `netzen`, 41. `buildjira`: reservation with history, SQLite concurrency, authorization in the query, PATCH with omitted versus null.
42. `geminiorganized/OpenSource_Upskilling_.Stripe`: the capstone.

### Electives, by gap

- **Realtime and queues:** job track live-chat, job track task-queue, buildwhiteboard.
- **Browser-only but well taught:** buildsubbox, buildgum, JSProjectLearn, astra4.2 (now has a server port), buildsql (a React app, not a SQL course), JS1 kanban-flow and poll-studio.
- **Larger codebases for reading practice:** formforge, e20, e12, master7, master 6, grokbuildecommerceproject, grokbuildmultitenantproject, lucasrouter.
- **Off-stack reference (read the translation chapter):** j1, j2, j3, j4, j5, j7 (Java); e14, e15, aiapplybot (Python); andie; buildsmallplates.

### Skip

The 21 clones teach the same lesson as a project above: JS1 library-lending, gym-membership, campaign-planner, volunteer-coordinator, field-service, research-studies, travel-requests, vendor-contracts, quality-audits, grant-manager, incident-response, procurement-portal, property-rentals, patient-intake; newcodexJS 08, 09, 10, 17, 18, 19, 20. Also note that `04 JavaScript Training/react` is a vanilla-JS quiz board, not React.

## 5. Interview prep on top of the path

- **Two weeks before interviews:** pick five finished projects, one per stage from 1 to 5. For each, rehearse `02-STORIES-AND-RESUME.md` aloud and drill `06-FLASHCARDS.md` daily.
- **Screening rounds:** `01-INTERVIEW-QUESTIONS.md` screening and follow-up groups, then `03-CODE-READING-DRILL.md` with a timer.
- **Take-homes:** do the five starred ones under the stated time limit and grade yourself with the rubric before reading the reviewer notes.
- **System design:** read `05-SYSTEM-DESIGN-FOLLOWUPS.md` for the Stage 3 and Stage 5 projects. Those answers start from real code, which is what makes a junior's answer credible.
