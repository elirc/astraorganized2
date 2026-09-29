# Remaining projects: review and proposed improvement order

Reviewed 2026-09-21. **132 project families are still pending in the campaign ledger; all 132 folders exist. This is a planning queue, not a claim that 132 projects are broken or untouched.** No project files were edited, no dependencies installed, and no project tests or servers were run in this review.

## What the current files show

- 107 campaign deliveries remain marked delivered; the earlier completed 14-project and 15-project batches stay excluded.
- The pending queue has no exact path overlap with the 153-project Fable registry. Existing enhancements found in pending folders must still be preserved; the registry alone does not establish who last changed every file.
- **108 families** have test-related filename indicators; **61 families** have recognized learning-document paths. These are discovery indicators, not passing-test or course-quality claims.
- `csbootcamp` illustrates the limit of filename counts: it has a custom `bootcamp/_lib/Check/Check.cs` assertion harness even though the conventional test-name scan finds no tests.
- `codehelper/ww20` is a separately queued child of `codehelper`. Do not improve both as independent copies of the same files. Its current package name is `multi-tenant-event-platform`; it needs its own scope decision.
- The review deliberately did not reinstall the dependencies removed during cleanup. Reinstall only what a selected future project needs.

## Recommended first batch: three concrete fixes

These findings are supported by reading the named source files. They have not been reproduced by running the applications. Add a failing regression first when implementation begins.

### 1. recipegen-app — validate request and provider data

Evidence: [API route](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app/app/api/recipes/route.ts) (lines 72–79 and 125 onward), [browser storage](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app/lib/storage.ts) (lines 21 and 55), and [submission flow](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app/app/HomeClient.tsx).
- A JSON `null` request parses successfully, then is destructured outside a guard at line 125. That bypasses the intended controlled validation response.
- Provider output validation checks only a few truthy fields and two arrays before casting to `Recipe`; field types, numeric bounds and nested entries are not validated.
- Saved history/favorites accept any valid JSON shape as an array; malformed-but-valid stored data can reach consumers.
**Proposed improvement:** explicit object/field validation at both boundaries, a mockable provider, defensive stored-data parsing, and useful storage-error behavior. **Acceptance cases:** null body, non-string ingredients, invalid servings, malformed recipe arrays, valid response, corrupt storage, and provider failure—all without a paid API call. No conventional test files were found.

### 2. AlanAndEliSoccer — make saved study progress resilient

Evidence: [LawProgressToggle.tsx](../../AlanAndEliSoccer/soccer-laws-app/src/components/law-page/LawProgressToggle.tsx) (lines 7–13, 19, and 31). The actual app root is `soccer-laws-app`, not the outer family directory.
- `readProgress()` returns parsed JSON without checking that it is an array of valid law numbers; stored `{}` or `null` can reach the `.includes()` call.
- The storage write is not caught, so storage-denied or quota failures throw after UI state has already changed.
**Proposed improvement:** extract a small validated persistence helper, retain usable in-memory state when saving fails, and add reload/toggle regressions. **Acceptance cases:** empty storage, malformed JSON, wrong JSON type, duplicates/out-of-range entries, unavailable storage and a normal reload. No conventional test files were found.

### 3. HNJOBTRACK — recover interrupted imports

Evidence: [scraper.py](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK/backend/app/services/scraper.py) (lines 38–59 and the batch-insert loop), and [admin pipeline](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK/backend/app/api/admin.py).
- The scraper inserts a `pending` thread before fetching comments. On another run, any existing thread is returned immediately regardless of status.
- If fetching or a later insertion batch fails, a retry can skip the missing comments and advance to parsing an incomplete import.
**Proposed improvement:** status-aware resumable import with idempotent comment writes and explicit failure/retry state. **Acceptance cases:** failure immediately after thread creation, failure after one insert batch, retry without duplicates, already-complete import and malformed input. Use fake HTTP/database adapters; do not send notifications. No conventional test files were found.

## Next: verify existing work before proposing more changes

| Project | Fresh evidence / proposed next check |
|---|---|
| [ww36](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww36) | Source already uses serializable reservation transactions, actor-scoped visibility, and lifecycle guards; tests and `docs/learning/testing-rationale.md` already exist. Verify their baseline; add a missing concurrent/repeated lifecycle case only if it adds coverage. Do not redo the existing safeguards. |
| [ww26](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww26) | The sampled release test mocks transactions and repositories and checks an already-released lease. A real database contention/stale-owner check is a proposed follow-up, not a confirmed missing implementation. Review the full suite first. |
| [.netcalendy](../../_Organized%20Desktop/01%20Net%20Workspaces/.netcalendy) | Existing application/domain/integration test files and extensive `docs/upskill` material. Verify booking-overlap and timezone-boundary coverage before expanding the course. |
| [ankijs](../../ankijs) | Existing scheduler, sync/outbox, repository and UI tests plus `docs/upskill`. Start with a coverage review of one offline/replay invariant; do not regenerate the existing curriculum. |
| [tagalog](../../tagalog) | Existing core lesson/session test files. Review guest-to-account progress replay and the package boundary first; no sync defect was established in this pass. |
| [ww43](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww43) | Current note-service, repository, route-auth and schema tests plus learning documents. Check stale revision and sharing coverage before adding another change. |

## Resolve variants and reference projects deliberately

- Choose a baseline within the audio-assistant families (`aicallhelper`, `aicallhelper2`, `fableaihelperv2`, `fableaihelperv3`, `finalcallhelp`) before repeating the same improvement. Similar purpose is not proof of identical files.
- Compare `spacegame` with `astraspacegameweb`, and `3buildhyper` with `hypernova-inc-main`, before selecting a copy to change.
- `FinalJep`, `jstrain3`, `antiinv`, and the `codehelper` parent/child boundary need scope clarification from their implementations rather than assumptions from folder names.
- Existing curricula, snapshot histories, and large upstream projects belong on a narrow exercise/contribution track. Do not rewrite whole courses, modify starter solutions wholesale, or treat upstream size as a reason to overhaul them.

## Full remaining-project review

All 132 queued families are listed below. Purpose and suggested workflow are carried forward from the September 6 source catalog unless specifically updated above. Current file/test/learning indicators come from the fresh September 21 inventory. “Test indicators” can include fixtures/configuration or vendored examples; “learning files” is a path-name heuristic. Neither measures executed coverage.

### 1 — Focused fixes first (3)

| Project | Files | Test indicators | Learning files | Proposed next action |
|---|---:|---:|---:|---|
| [_Organized Desktop/08 App And Product Projects/HNJOBTRACK](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/HNJOBTRACK) | 57 | 0 | 0 | Implement the focused regression-led fix described above. |
| [_Organized Desktop/08 App And Product Projects/recipegen-app](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/recipegen-app) | 40 | 0 | 0 | Implement the focused regression-led fix described above. |
| [AlanAndEliSoccer](../../AlanAndEliSoccer) | 61 | 0 | 0 | Implement the focused regression-led fix described above. |

### 2 — Choose scope/variant first (14)

| Project | Files | Test indicators | Learning files | Proposed next action |
|---|---:|---:|---:|---|
| [_Organized Desktop/04 JavaScript Training/jstrain3](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain3) | 162 | 0 | 0 | Compare deskpilot, deskpilot-app, and deskpilot-clean; select one implemented flow and replace demo identity only as a later exercise. |
| [_Organized Desktop/06 AI And Learning/codehelper](../../_Organized%20Desktop/06%20AI%20And%20Learning/codehelper) | 209 | 15 | 6 | Trace upload-to-code-view and test one malformed archive or failed provider response. |
| [_Organized Desktop/06 AI And Learning/codehelper/ww20](../../_Organized%20Desktop/06%20AI%20And%20Learning/codehelper/ww20) | 98 | 4 | 6 | Define the event-platform child boundary, then trace one event through gateway, service and consumer using existing tests. |
| [_Organized Desktop/07 Anti Projects/antiinv](../../_Organized%20Desktop/07%20Anti%20Projects/antiinv) | 61 | 0 | 0 | Establish the actual domain by reading schema and routes before expanding the starter. |
| [_Organized Desktop/12 Other Projects/3buildhyper](../../_Organized%20Desktop/12%20Other%20Projects/3buildhyper) | 702 | 11 | 0 | Compare with hypernova-inc-main and complete one bounded page/form improvement. |
| [_Organized Desktop/12 Other Projects/FinalJep](../../_Organized%20Desktop/12%20Other%20Projects/FinalJep) | 68 | 0 | 0 | Compare the two app variants and locate actual game logic before selecting a build target. |
| [_Organized Desktop/12 Other Projects/hypernova-inc-main](../../_Organized%20Desktop/12%20Other%20Projects/hypernova-inc-main) | 662 | 1 | 0 | Compare with 3buildhyper and choose one canonical branch for a small page/form task. |
| [aicallhelper](../../aicallhelper) | 6,272 | 18 | 0 | Trace recording cancellation and test event-order races. |
| [aicallhelper2](../../aicallhelper2) | 374 | 32 | 0 | Compare one recording flow with aicallhelper and choose one maintained variant. |
| [astraspacegameweb](../../astraspacegameweb) | 2,394 | 21 | 0 | Trace construction completion across database and worker boundaries. |
| [fableaihelperv2](../../fableaihelperv2) | 104 | 18 | 0 | Trace one audio-to-response flow and compare recovery against finalcallhelp. |
| [fableaihelperv3](../../fableaihelperv3) | 35 | 8 | 0 | Measure and explain one mocked stream/cancel path before provider integration. |
| [finalcallhelp](../../finalcallhelp) | 269 | 37 | 0 | Choose one CueDeck baseline after comparing tests and setup requirements. |
| [spacegame](../../spacegame) | 105 | 6 | 0 | Trace one build/combat timer from command to worker to client, including duplicate delivery. |

### 3 — Curriculum/upstream: narrow contribution (17)

| Project | Files | Test indicators | Learning files | Proposed next action |
|---|---:|---:|---:|---|
| [_Organized Desktop/01 Net Workspaces/csbootcamp](../../_Organized%20Desktop/01%20Net%20Workspaces/csbootcamp) | 104 | 0 | 0 | Read FLIGHTPLAN.md; study modules 01 language core, 02 methods/delegates, 03 collections/LINQ, 04 strings/time; solve prompts before solutions. |
| [_Organized Desktop/03 Master Projects/mastermatter](../../_Organized%20Desktop/03%20Master%20Projects/mastermatter) | 13,255 | 2890 | 0 | Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. |
| [_Organized Desktop/03 Master Projects/MasterStore](../../_Organized%20Desktop/03%20Master%20Projects/MasterStore) | 245 | 8 | 0 | Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. |
| [_Organized Desktop/05 Numbered Experiments/rn1](../../_Organized%20Desktop/05%20Numbered%20Experiments/rn1) | 2,695 | 31 | 0 | Choose one small feature or bug; trace its UI/API, domain, data, authorization and tests before attempting a contribution. |
| [_Organized Desktop/09 Grav And VG Projects/graveopenjspy](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/graveopenjspy) | 5,543 | 1081 | 20 | Trace one motion or vote across its API, data, authorization, and tests. |
| [_Organized Desktop/09 Grav And VG Projects/gravreviewboardjspy](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/gravreviewboardjspy) | 3,597 | 575 | 20 | Trace a review-request change and select one narrow bug or test contribution. |
| [_Organized Desktop/09 Grav And VG Projects/VGdemo](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/VGdemo) | 188 | 12 | 14 | Follow the structured globalhire-lite review and implement one small finding in an isolated copy later. |
| [_Organized Desktop/12 Other Projects/pyhealth](../../_Organized%20Desktop/12%20Other%20Projects/pyhealth) | 1,285 | 232 | 0 | Trace one incoming ping into check state and alert processing; select one bounded test or fix. |
| [geminiorganized/General_Newcodecjs2](../../geminiorganized/General_Newcodecjs2) | 173 | 21 | 0 | Choose one child by missing skill and turn one domain behavior into an independently verified vertical slice. |
| [geminiorganized/General_Newcodex3](../../geminiorganized/General_Newcodex3) | 707 | 0 | 0 | Choose one topic and one language implementation; document gaps between scaffold code and production notes before extending it. |
| [geminiorganized/LLM_Generated_Buildsql](../../geminiorganized/LLM_Generated_Buildsql) | 818 | 61 | 0 | Use missions for current curriculum gaps and produce code evidence. |
| [geminiorganized/LLM_Generated_Grokjs](../../geminiorganized/LLM_Generated_Grokjs) | 2,122 | 8 | 0 | Pick one language lab and one exercise matching a current gap. |
| [geminiorganized/LLM_Generated_Groktuts](../../geminiorganized/LLM_Generated_Groktuts) | 401 | 14 | 0 | Use one lab to close a measured fundamentals gap. |
| [geminiorganized/LLM_Generated_Jsprojectlearn](../../geminiorganized/LLM_Generated_Jsprojectlearn) | 610 | 66 | 0 | Compare an original/refactored example and implement the change independently. Compare this older curriculum with the current direct Desktop SkillForge Quest before choosing a course. |
| [geminiorganized/OpenSource_Upskilling_Snapshot](../../geminiorganized/OpenSource_Upskilling_Snapshot) | 851 | 24 | 0 | Start snapshots/00-walking-skeleton/NOTES.md; predict each change, compare adjacent copies, and recreate one increment in your own branch. |
| [geminiorganized/OpenSource_Upskilling_Snapshot1](../../geminiorganized/OpenSource_Upskilling_Snapshot1) | 768 | 36 | 0 | Follow 00-walking-skeleton then implement one company workflow without copying its solution first. |
| [jsharness/VTCode](../../jsharness/VTCode) | 2,840 | 160 | 3 | Trace one command from CLI parsing to tool execution and compare the TS port. |

### 4 — Existing learning material: verify gaps first (55)

| Project | Files | Test indicators | Learning files | Proposed next action |
|---|---:|---:|---:|---|
| [_Organized Desktop/01 Net Workspaces/.netcalendy](../../_Organized%20Desktop/01%20Net%20Workspaces/.netcalendy) | 187 | 14 | 40 | Verify existing work before edits. Test overlapping bookings and a daylight-saving boundary on one booking flow. |
| [_Organized Desktop/01 Net Workspaces/.netslack](../../_Organized%20Desktop/01%20Net%20Workspaces/.netslack) | 127 | 2 | 47 | Verify existing work before edits. Isolate a game/message state transition and specify duplicate-event/reconnect tests. |
| [_Organized Desktop/02 Build Projects/buildagenthelpdesk](../../_Organized%20Desktop/02%20Build%20Projects/buildagenthelpdesk) | 205 | 22 | 46 | Verify existing work before edits. Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/02 Build Projects/buildanalytics](../../_Organized%20Desktop/02%20Build%20Projects/buildanalytics) | 420 | 44 | 46 | Verify existing work before edits. Specify a workflow retry after a partial failure and add one focused recovery test. |
| [_Organized Desktop/02 Build Projects/buildecom](../../_Organized%20Desktop/02%20Build%20Projects/buildecom) | 124 | 5 | 46 | Verify existing work before edits. Trace an order/reservation and test invalid transitions or repeated submissions. |
| [_Organized Desktop/04 JavaScript Training/rewritepy2js](../../_Organized%20Desktop/04%20JavaScript%20Training/rewritepy2js) | 127 | 23 | 20 | Verify existing work before edits. Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/w21](../../_Organized%20Desktop/05%20Numbered%20Experiments/w21) | 95 | 4 | 6 | Verify existing work before edits. Follow one request across its boundary and test backward compatibility or cache invalidation. |
| [_Organized Desktop/05 Numbered Experiments/w22](../../_Organized%20Desktop/05%20Numbered%20Experiments/w22) | 88 | 4 | 6 | Verify existing work before edits. Read schema, permissions, paymentService, webhookService, reconciliationService in that order; test replayed creation and late provider events. |
| [_Organized Desktop/05 Numbered Experiments/w23](../../_Organized%20Desktop/05%20Numbered%20Experiments/w23) | 75 | 5 | 6 | Verify existing work before edits. Follow one request across its boundary and test backward compatibility or cache invalidation. |
| [_Organized Desktop/05 Numbered Experiments/w25](../../_Organized%20Desktop/05%20Numbered%20Experiments/w25) | 57 | 4 | 6 | Verify existing work before edits. Study acquire/renew/release invariants, then compare ww26 for actual Prisma-backed locking boundaries. |
| [_Organized Desktop/05 Numbered Experiments/ww1](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww1) | 68 | 4 | 6 | Verify existing work before edits. Specify a workflow retry after a partial failure and add one focused recovery test. |
| [_Organized Desktop/05 Numbered Experiments/ww10](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww10) | 80 | 4 | 6 | Verify existing work before edits. Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/ww11](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww11) | 71 | 4 | 6 | Verify existing work before edits. Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/ww12](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww12) | 88 | 4 | 6 | Verify existing work before edits. Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/ww13](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww13) | 91 | 5 | 6 | Verify existing work before edits. Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/ww15](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww15) | 82 | 6 | 6 | Verify existing work before edits. Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/ww16](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww16) | 83 | 4 | 6 | Verify existing work before edits. Trace a lead/deal transition and test tenant isolation plus invalid transitions. |
| [_Organized Desktop/05 Numbered Experiments/ww18](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww18) | 87 | 4 | 6 | Verify existing work before edits. Trace a lead/deal transition and test tenant isolation plus invalid transitions. |
| [_Organized Desktop/05 Numbered Experiments/ww19](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww19) | 95 | 4 | 6 | Verify existing work before edits. Specify a workflow retry after a partial failure and add one focused recovery test. |
| [_Organized Desktop/05 Numbered Experiments/ww26](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww26) | 61 | 4 | 6 | Verify existing work before edits. After w25, trace lockCoordinatorService through lockScopeRepository row locking and lockLeaseRepository; test stale ownership and contention. |
| [_Organized Desktop/05 Numbered Experiments/ww28](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww28) | 59 | 5 | 6 | Verify existing work before edits. Trace one upload through storage and processing; specify retry and access-denial cases. |
| [_Organized Desktop/05 Numbered Experiments/ww29](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww29) | 80 | 5 | 6 | Verify existing work before edits. Trace one event or check into a dashboard and test duplicate/missing/late data. |
| [_Organized Desktop/05 Numbered Experiments/ww3](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww3) | 97 | 8 | 6 | Verify existing work before edits. Trace one employee approval and test both cross-tenant access and invalid state changes. |
| [_Organized Desktop/05 Numbered Experiments/ww30](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww30) | 66 | 4 | 6 | Verify existing work before edits. Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/ww31](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww31) | 88 | 4 | 6 | Verify existing work before edits. Test deterministic targeting, rollback, and stale configuration behavior. |
| [_Organized Desktop/05 Numbered Experiments/ww32](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww32) | 98 | 4 | 6 | Verify existing work before edits. Isolate a game/message state transition and specify duplicate-event/reconnect tests. |
| [_Organized Desktop/05 Numbered Experiments/ww36](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww36) | 83 | 4 | 6 | Verify existing work before edits. Trace an order/reservation and test invalid transitions or repeated submissions. |
| [_Organized Desktop/05 Numbered Experiments/ww4](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww4) | 89 | 4 | 6 | Verify existing work before edits. Implement one board/task operation and test ordering plus permission boundaries. |
| [_Organized Desktop/05 Numbered Experiments/ww40](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww40) | 83 | 4 | 6 | Verify existing work before edits. Trace a create/update flow and test ownership, validation, and one invalid transition. |
| [_Organized Desktop/05 Numbered Experiments/ww43](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww43) | 90 | 6 | 6 | Verify existing work before edits. Trace an edit and test a stale revision or forbidden share. |
| [_Organized Desktop/05 Numbered Experiments/ww45](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww45) | 113 | 4 | 6 | Verify existing work before edits. Trace an edit and test a stale revision or forbidden share. |
| [_Organized Desktop/05 Numbered Experiments/ww46](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww46) | 90 | 4 | 6 | Verify existing work before edits. Trace one protected mutation and design cross-tenant read/write denial tests. |
| [_Organized Desktop/05 Numbered Experiments/ww47](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww47) | 116 | 4 | 6 | Verify existing work before edits. Validate one metric against a small hand-calculated dataset including duplicates. |
| [_Organized Desktop/05 Numbered Experiments/ww48](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww48) | 89 | 4 | 6 | Verify existing work before edits. Trace a lead/deal transition and test tenant isolation plus invalid transitions. |
| [_Organized Desktop/05 Numbered Experiments/ww6](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww6) | 75 | 4 | 6 | Verify existing work before edits. Validate one metric against a small hand-calculated dataset including duplicates. |
| [_Organized Desktop/05 Numbered Experiments/ww7](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww7) | 89 | 4 | 6 | Verify existing work before edits. Specify a workflow retry after a partial failure and add one focused recovery test. |
| [_Organized Desktop/05 Numbered Experiments/ww8](../../_Organized%20Desktop/05%20Numbered%20Experiments/ww8) | 86 | 4 | 6 | Verify existing work before edits. Trace one upload through storage and processing; specify retry and access-denial cases. |
| [_Organized Desktop/05 Numbered Experiments/X1](../../_Organized%20Desktop/05%20Numbered%20Experiments/X1) | 69 | 0 | 20 | Verify existing work before edits. Build or explain one complete user interaction with empty/loading/error behavior. |
| [_Organized Desktop/05 Numbered Experiments/z8](../../_Organized%20Desktop/05%20Numbered%20Experiments/z8) | 104 | 3 | 7 | Verify existing work before edits. Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/zz1](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz1) | 119 | 4 | 6 | Verify existing work before edits. Specify a workflow retry after a partial failure and add one focused recovery test. |
| [_Organized Desktop/05 Numbered Experiments/zz2](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz2) | 113 | 3 | 8 | Verify existing work before edits. Trace ticket creation to storage; test forbidden transitions and unauthorized access. |
| [_Organized Desktop/05 Numbered Experiments/zz3](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz3) | 109 | 6 | 7 | Verify existing work before edits. Trace ticket creation to storage; test forbidden transitions and unauthorized access. |
| [_Organized Desktop/05 Numbered Experiments/zz4](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz4) | 98 | 5 | 6 | Verify existing work before edits. Specify a workflow retry after a partial failure and add one focused recovery test. |
| [_Organized Desktop/05 Numbered Experiments/zz55](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz55) | 84 | 4 | 6 | Verify existing work before edits. Trace a charge or webhook and design a replay test that cannot double-apply it. |
| [_Organized Desktop/05 Numbered Experiments/zz7](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz7) | 110 | 5 | 7 | Verify existing work before edits. Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/zz9](../../_Organized%20Desktop/05%20Numbered%20Experiments/zz9) | 91 | 4 | 6 | Verify existing work before edits. Trace case assignment and test unauthorized queue access. |
| [_Organized Desktop/08 App And Product Projects/grouphelpdesk](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/grouphelpdesk) | 202 | 17 | 17 | Verify existing work before edits. Trace ticket creation and assignment through shared contracts; add an unauthorized transition test. |
| [_Organized Desktop/12 Other Projects/aaa1](../../_Organized%20Desktop/12%20Other%20Projects/aaa1) | 247 | 33 | 11 | Verify existing work before edits. Trace lead/deal mutation and test cross-tenant data access. |
| [_Organized Desktop/12 Other Projects/pp8](../../_Organized%20Desktop/12%20Other%20Projects/pp8) | 94 | 2 | 7 | Verify existing work before edits. Trace one HR use case and compare its validation/auth/data boundaries with the TypeScript version. |
| [ankijs](../../ankijs) | 4,656 | 57 | 46 | Verify existing work before edits. Use short daily recall sessions; study one scheduling or sync invariant. |
| [geminiorganized/OpenSource_Upskilling_Auth](../../geminiorganized/OpenSource_Upskilling_Auth) | 123 | 3 | 47 | Verify existing work before edits. Follow one authorization-code exchange and write a threat model plus negative tests around identity binding and replay. |
| [geminiorganized/OpenSource_Upskilling_Docu](../../geminiorganized/OpenSource_Upskilling_Docu) | 153 | 5 | 47 | Verify existing work before edits. Trace document creation to envelope completion; verify one unauthorized recipient and duplicate submission scenario. |
| [geminiorganized/OpenSource_Upskilling_Intercom](../../geminiorganized/OpenSource_Upskilling_Intercom) | 147 | 7 | 47 | Verify existing work before edits. Trace visitor session to agent reply and verify conversation authorization plus reconnect behavior. |
| [geminiorganized/OpenSource_Upskilling_Notion](../../geminiorganized/OpenSource_Upskilling_Notion) | 171 | 7 | 47 | Verify existing work before edits. Trace page sharing and version restore; add an inherited-permission regression and reject tree cycles. |
| [tagalog](../../tagalog) | 15,123 | 10 | 53 | Verify existing work before edits. Trace one lesson progress event through guest storage and authenticated sync; verify duplicate/offline replay handling. |

### 5 — Bounded workflow review (43)

| Project | Files | Test indicators | Learning files | Proposed next action |
|---|---:|---:|---:|---|
| [_Organized Desktop/02 Build Projects/buildaffiliate](../../_Organized%20Desktop/02%20Build%20Projects/buildaffiliate) | 444 | 73 | 0 | Validate one metric against a small hand-calculated dataset including duplicates. |
| [_Organized Desktop/02 Build Projects/buildagentteaching](../../_Organized%20Desktop/02%20Build%20Projects/buildagentteaching) | 505 | 39 | 0 | Trace one enrollment-to-completion flow and test an ineligible certification. |
| [_Organized Desktop/02 Build Projects/buildScedulingPYJS](../../_Organized%20Desktop/02%20Build%20Projects/buildScedulingPYJS) | 183 | 4 | 0 | Test overlapping bookings and a daylight-saving boundary on one booking flow. |
| [_Organized Desktop/03 Master Projects/master](../../_Organized%20Desktop/03%20Master%20Projects/master) | 128 | 1 | 0 | Specify a workflow retry after a partial failure and add one focused recovery test. |
| [_Organized Desktop/03 Master Projects/master1](../../_Organized%20Desktop/03%20Master%20Projects/master1) | 267 | 12 | 0 | Trace one employee approval and test both cross-tenant access and invalid state changes. |
| [_Organized Desktop/03 Master Projects/masterrnative](../../_Organized%20Desktop/03%20Master%20Projects/masterrnative) | 109 | 12 | 0 | Trace one feed/expense record through the mobile UI and storage; handle interrupted input and offline state. |
| [_Organized Desktop/04 JavaScript Training/jep vs code](../../_Organized%20Desktop/04%20JavaScript%20Training/jep%20vs%20code) | 253 | 0 | 0 | Isolate a game/message state transition and specify duplicate-event/reconnect tests. |
| [_Organized Desktop/04 JavaScript Training/jsdrill_sync_20260223_125137](../../_Organized%20Desktop/04%20JavaScript%20Training/jsdrill_sync_20260223_125137) | 117 | 0 | 0 | Validate one metric against a small hand-calculated dataset including duplicates. |
| [_Organized Desktop/04 JavaScript Training/jstrain1](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain1) | 83 | 0 | 0 | Trace one protected mutation and design cross-tenant read/write denial tests. |
| [_Organized Desktop/04 JavaScript Training/jstrain2](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2) | 228 | 14 | 0 | Specify a workflow retry after a partial failure and add one focused recovery test. |
| [_Organized Desktop/04 JavaScript Training/jstrain2.4](../../_Organized%20Desktop/04%20JavaScript%20Training/jstrain2.4) | 92 | 0 | 0 | Specify a workflow retry after a partial failure and add one focused recovery test. |
| [_Organized Desktop/05 Numbered Experiments/D2](../../_Organized%20Desktop/05%20Numbered%20Experiments/D2) | 50 | 0 | 0 | Use a deterministic provider fixture to specify success, cancellation, and failure behavior. |
| [_Organized Desktop/05 Numbered Experiments/D3](../../_Organized%20Desktop/05%20Numbered%20Experiments/D3) | 89 | 0 | 0 | Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/e11](../../_Organized%20Desktop/05%20Numbered%20Experiments/e11) | 51 | 4 | 0 | Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/e17](../../_Organized%20Desktop/05%20Numbered%20Experiments/e17) | 146 | 3 | 0 | Trace one documented user flow from entry point to stored state and make one bounded improvement. |
| [_Organized Desktop/05 Numbered Experiments/e3](../../_Organized%20Desktop/05%20Numbered%20Experiments/e3) | 102 | 2 | 0 | Validate one metric against a small hand-calculated dataset including duplicates. |
| [_Organized Desktop/05 Numbered Experiments/e4](../../_Organized%20Desktop/05%20Numbered%20Experiments/e4) | 132 | 2 | 0 | Trace an edit and test a stale revision or forbidden share. |
| [_Organized Desktop/05 Numbered Experiments/g1](../../_Organized%20Desktop/05%20Numbered%20Experiments/g1) | 66 | 0 | 0 | Build or explain one complete user interaction with empty/loading/error behavior. |
| [_Organized Desktop/06 AI And Learning/ai-observer-reference](../../_Organized%20Desktop/06%20AI%20And%20Learning/ai-observer-reference) | 245 | 14 | 0 | Trace a session event into usage metrics and test duplicate-event handling. |
| [_Organized Desktop/06 AI And Learning/aiapplybot](../../_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybot) | 138 | 8 | 0 | Map the six pipeline stages; isolate stage-six automation behind deterministic fixtures. |
| [_Organized Desktop/06 AI And Learning/aiapplybotjs](../../_Organized%20Desktop/06%20AI%20And%20Learning/aiapplybotjs) | 73 | 5 | 0 | Compare one pipeline stage to the Python version and test retry/cancellation behavior. |
| [_Organized Desktop/06 AI And Learning/claudeailab](../../_Organized%20Desktop/06%20AI%20And%20Learning/claudeailab) | 62 | 0 | 0 | Define one measurable experiment and trace how its result is stored and summarized. |
| [_Organized Desktop/06 AI And Learning/think](../../_Organized%20Desktop/06%20AI%20And%20Learning/think) | 64 | 4 | 0 | Trace one conversation import and design a repeat-import deduplication test. |
| [_Organized Desktop/07 Anti Projects/antiemponb](../../_Organized%20Desktop/07%20Anti%20Projects/antiemponb) | 144 | 2 | 0 | Trace one onboarding step and test invalid ordering and unauthorized completion. |
| [_Organized Desktop/07 Anti Projects/antihelpdesk](../../_Organized%20Desktop/07%20Anti%20Projects/antihelpdesk) | 132 | 0 | 0 | Trace one ticket transition and test both validation and authorization. |
| [_Organized Desktop/07 Anti Projects/antitestbuild](../../_Organized%20Desktop/07%20Anti%20Projects/antitestbuild) | 99 | 0 | 0 | Trace one cross-module employee workflow and test cross-tenant isolation. |
| [_Organized Desktop/08 App And Product Projects/eliapplybot](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot) | 136 | 18 | 0 | Use local form fixtures to test matching and filling while preserving user review. |
| [_Organized Desktop/08 App And Product Projects/eliapplybot-python](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/eliapplybot-python) | 86 | 5 | 0 | Compare form mappings with the extension and isolate browser effects behind fixtures. |
| [_Organized Desktop/08 App And Product Projects/hnrandom](../../_Organized%20Desktop/08%20App%20And%20Product%20Projects/hnrandom) | 118 | 0 | 0 | Trace one telemetry event and verify how duplicates and errors affect metrics. |
| [_Organized Desktop/09 Grav And VG Projects/vg](../../_Organized%20Desktop/09%20Grav%20And%20VG%20Projects/vg) | 250 | 0 | 0 | Trace one employee approval and test cross-tenant access denial. |
| [_Organized Desktop/12 Other Projects/appmaketrck](../../_Organized%20Desktop/12%20Other%20Projects/appmaketrck) | 244 | 8 | 0 | Trace one air-quality reading to the globe and handle unavailable/stale data. |
| [_Organized Desktop/12 Other Projects/cc](../../_Organized%20Desktop/12%20Other%20Projects/cc) | 135 | 0 | 0 | Establish one implemented content workflow and test validation and permission boundaries. |
| [_Organized Desktop/12 Other Projects/curse](../../_Organized%20Desktop/12%20Other%20Projects/curse) | 117 | 0 | 0 | Trace a game event and specify duplicate-event/reconnect behavior. |
| [_Organized Desktop/12 Other Projects/finaljepgame](../../_Organized%20Desktop/12%20Other%20Projects/finaljepgame) | 152 | 0 | 0 | Trace question creation into gameplay and test one invalid state transition. |
| [gitvg/agora-net](../../gitvg/agora-net) | 186 | 49 | 0 | Add one checkout failure or concurrent reservation test. |
| [gitvg/atlas-net](../../gitvg/atlas-net) | 119 | 42 | 0 | Compare one lifecycle slice with Atlas and choose one implementation to study. |
| [gitvg/bazaar-app](../../gitvg/bazaar-app) | 289 | 56 | 0 | Trace one return or fulfillment slice and test its permissions. |
| [gitvg/folio-app](../../gitvg/folio-app) | 227 | 43 | 0 | Trace a page edit through authorization and version history. |
| [gitvg/harbor-net](../../gitvg/harbor-net) | 174 | 48 | 0 | Test one SLA deadline and duplicate webhook delivery. |
| [gitvg/pulse-net](../../gitvg/pulse-net) | 138 | 34 | 0 | Test restart and replay of one captured event. |
| [gitvg/relay-app](../../gitvg/relay-app) | 274 | 53 | 0 | Replace one simulated action with a controlled adapter and contract test. |
| [gitvg/tracer-net](../../gitvg/tracer-net) | 190 | 46 | 0 | Test one invalid workflow transition and ordering edge case. |
| [jsharness/ctvodejs](../../jsharness/ctvodejs) | 185 | 45 | 0 | Port one bounded VTCode behavior and add a parity fixture. |

## Filename lists and review limits

- [Project names / Desktop-relative family paths](REMAINING_PROJECT_NAMES_2026-09-21.txt): 132 entries.
- [All inventoried filenames, with Desktop-relative paths](REMAINING_PROJECT_FILE_NAMES_2026-09-21.txt): **80,414 unique entries**. Full paths distinguish repeated names such as `README.md`.
- [Per-project files, manifests, package scripts, evidence checks and scan errors](REMAINING_PROJECT_REVIEW_INVENTORY_2026-09-21.json).
- [Original remaining queue](REMAINING_PROJECTS_TO_DO_2026-09-19.md) and [delivery ledger](../astra-remaining-improvements/progress.json) were not altered; reviewing is not delivery.
- Filename discovery used `rg --files --hidden --no-ignore` with explicit directory exclusions and no symlink-following flag. It includes source, docs, assets, configurations, snapshots and any generated files outside excluded folders. It is not a hand-certified list of authored source files.
- Excluded directory names: `node_modules`, `.git`, `.venv`, `venv`, `__pycache__`, `.next`, `.nuxt`, `.svelte-kit`, `.turbo`, `.cache`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.gradle`, `.pnpm-store`, `npm-cache`, `pip-cache`.
- Filesystem listing errors: 0. All 132 roots exist. Nested family entries can repeat in per-project inventories; the standalone filename list is deduplicated.
- Older catalog evidence paths missing today: 0; absence can mean a move or rename and is not itself a defect. See inventory `evidenceChecks`.
- No secret/environment-file contents were read. Their filenames may appear in the path inventory.
- This is a queue-wide static review with targeted source samples, not a line-by-line audit of 80,414 files. No build, test-pass, performance, security or runtime readiness claims are made.
