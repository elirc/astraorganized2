# Next 30 projects: implementation details

Applied to original folders on September 8, 2026. **539 files**, **270 learning documents**, **207,577 words**, **89 regression cases passed**, plus **28 builds, 12 TypeScript checks and 30 Chromium interaction checks**. Read [the combined report](ALL_50_PROJECTS_REPORT.md) for all 50 courses and evidence, or [the concise summary](SUMMARY.md).

Each improvement below is implemented; the linked course's practice variations remain exercises. Existing tutorials are retained.

## 21. poll-studio

[Start the course](../../JS1/poll-studio/astraupskill/README.md) · [Verification](../../JS1/poll-studio/astraupskill/VERIFICATION.md)

**Changed:** Draft options carry stable ids. Surviving options retain their votes; new options start at zero. Blank or duplicate labels are rejected. Save, vote, reset and delete publish state only after storage succeeds.

**Learn:** identity in dynamic arrays and commit-before-publish. Remove Mobile app from the starter poll. Public API retains 7 votes and Dark mode retains 2, for 9 total. Duplicate labels API/api are rejected. A failed write preserves both the old poll and the current draft.

**Delivery:** 15 files; nine course files; 5,953 words; 3 passing regression cases. DOM/storage regressions and Chromium interaction passed.

## 22. kanban-flow

[Start the course](../../JS1/kanban-flow/astraupskill/README.md) · [Verification](../../JS1/kanban-flow/astraupskill/VERIFICATION.md)

**Changed:** Moves validate targets, ignore self-drops, calculate a candidate and renumber every column before saving. Failed moves preserve state. Column selects and move-up/down buttons support keyboard use and restore focus.

**Learn:** immutable movement, ordering invariants and keyboard access. Move A from todo [A,B] before C in doing. B becomes order 0; A/C become orders 0/1. A self-drop does nothing. Reject setItem and the previous card array remains identical.

**Delivery:** 14 files; nine course files; 5,722 words; 3 passing regression cases. DOM/storage regressions and Chromium interaction passed.

## 23. course-roster

[Start the course](../../JS1/course-roster/astraupskill/README.md) · [Verification](../../JS1/course-roster/astraupskill/VERIFICATION.md)

**Changed:** Codes and text are bounded and typed. Capacity/enrollment must be whole counts, enrollment cannot exceed capacity, levels are constrained, and normalized codes are unique across other records. Editing can retain its own code.

**Learn:** normalization, uniqueness and whole-number invariants. Create astra-101 with capacity 4 and enrolled 2: the returned code is ASTRA-101. A second equivalent code returns 409. Editing the original title succeeds. Capacity 1.5, enrollment 5 or null is rejected.

**Delivery:** 18 files; nine course files; 5,824 words; 2 passing regression cases. Build and integrated browser checks passed.

## 24. event-admin

[Start the course](../../JS1/event-admin/astraupskill/README.md) · [Verification](../../JS1/event-admin/astraupskill/VERIFICATION.md)

**Changed:** Events require bounded text, real YYYY-MM-DD dates and whole capacity/registration counts. Registered cannot exceed capacity. Invalid updates preserve the previous event.

**Learn:** calendar labels and cross-field validation. 2028-02-29 with capacity 3 and registered 3 succeeds. 2027-02-29, 2028-04-31, registered 4 and capacity "bad" fail without replacing a saved event.

**Delivery:** 18 files; nine course files; 5,629 words; 2 passing regression cases. Build and integrated browser checks passed.

## 25. job-pipeline

[Start the course](../../JS1/job-pipeline/astraupskill/README.md) · [Verification](../../JS1/job-pipeline/astraupskill/VERIFICATION.md)

**Changed:** Text fields are bounded and typed. Nonempty next-step dates must be real dates. Filtered results sort by date, place undated applications last, and use ids for ties.

**Learn:** optional values and stable chronological sorting. Dates March 10, March 1 and empty display as March 1, March 10, empty. An invalid follow-up edit returns 400 and leaves the original application identical.

**Delivery:** 18 files; nine course files; 5,680 words; 2 passing regression cases. Build and integrated browser checks passed.

## 26. stock-catalog

[Start the course](../../JS1/stock-catalog/astraupskill/README.md) · [Verification](../../JS1/stock-catalog/astraupskill/VERIFICATION.md)

**Changed:** Paging normalizes to bounded whole values. Sort ties use ids. Names/categories are bounded text, prices are finite and bounded, and stock is a nonnegative whole count. Existing last-page clamping has regression coverage.

**Learn:** filter-sort-slice order and numeric boundaries. Three same-price products at two per page give stable ids on page 1. Page 999 becomes page 2 with one item. Infinite/fractional page inputs use defaults; infinite prices and fractional stock are rejected.

**Delivery:** 18 files; nine course files; 5,775 words; 2 passing regression cases. Build and integrated browser checks passed.

## 27. recipe-studio

[Start the course](../../JS1/recipe-studio/astraupskill/README.md) · [Verification](../../JS1/recipe-studio/astraupskill/VERIFICATION.md)

**Changed:** Cooking minutes and servings are bounded whole numbers. Ingredients must be 1-100 nonempty bounded strings. Trimming and case-insensitive deduplication preserve first spelling. Invalid nested payloads are rejected before mutation.

**Learn:** array element validation and normalization. [" Salt ", "salt", "Water"] saves as ["Salt", "Water"]. Servings "4" becomes numeric 4 without changing id. Object ingredients, blanks, fractional servings and boolean cooking time fail.

**Delivery:** 18 files; nine course files; 5,715 words; 2 passing regression cases. Build and integrated browser checks passed.

## 28. org-explorer

[Start the course](../../JS1/org-explorer/astraupskill/README.md) · [Verification](../../JS1/org-explorer/astraupskill/VERIFICATION.md)

**Changed:** Moves validate UUIDs and parent existence, lock structural changes within a transaction, check the subtree under the lock, then update. A node cannot become its own ancestor.

**Learn:** recursive queries, structural invariants and concurrent tree moves. Create roots A and B. Race A-under-B with B-under-A. Exactly one succeeds; the rejected move leaves a readable acyclic tree. Moving A under its own descendant is rejected even without concurrency.

**Delivery:** 16 files; nine course files; 6,592 words; 3 passing regression cases. TypeScript, build and integrated browser checks passed.

## 29. mini-blog

[Start the course](../../JS1/mini-blog/astraupskill/README.md) · [Verification](../../JS1/mini-blog/astraupskill/VERIFICATION.md)

**Changed:** Posts and comments require bounded text before repository methods run. Tests verify existing parent-scoped deletion and cascade behavior. The client mount and static labels are repaired.

**Learn:** relationships and validated text boundaries. A comment under A cannot be deleted through B. Deleting A removes access to its comments. Object-valued text returns 400 and creates no comment.

**Delivery:** 18 files; nine course files; 5,677 words; 2 passing regression cases. Build and integrated browser checks passed.

## 30. pulse-analytics

[Start the course](../../JS1/pulse-analytics/astraupskill/README.md) · [Verification](../../JS1/pulse-analytics/astraupskill/VERIFICATION.md)

**Changed:** The series generates every requested calendar day, left-joins daily aggregates, fills missing values with zero and computes the moving average and cumulative total over those rows. Summary uses the same inclusive day window.

**Learn:** calendar buckets, window functions and derived data. For daily values 10, 0 and 20, the visible moving averages are 10, 5 and 10; cumulative totals are 10, 10 and 30. A seven-day request returns seven rows even if events exist on only two days.

**Delivery:** 16 files; nine course files; 6,596 words; 3 passing regression cases. TypeScript, build and integrated browser checks passed.

## 31. support-tickets

[Start the course](../../JS1/support-tickets/astraupskill/README.md) · [Verification](../../JS1/support-tickets/astraupskill/VERIFICATION.md)

**Changed:** Status and assignment read the current ticket under a row lock, return it unchanged for a repeated value, and record actual changes transactionally. Input and UUID validation reject malformed requests; failed related writes roll back.

**Learn:** row locks, atomic updates and meaningful audit events. Create a ticket, resolve it twice, and read history. There is one status event. Repeat assigning the same agent with the same expectation. Force a late related write to fail and verify that the earlier ticket changes did not commit.

**Delivery:** 16 files; nine course files; 6,621 words; 3 passing regression cases. TypeScript, build and integrated browser checks passed.

## 32. issue-desk

[Start the course](../../JS1/issue-desk/astraupskill/README.md) · [Verification](../../JS1/issue-desk/astraupskill/VERIFICATION.md)

**Changed:** Priority filtering composes with status and search in UI and API. Invalid priorities and malformed text return useful errors; updates preserve issue identity.

**Learn:** independent filter dimensions and runtime validation. High/Backlog, Low/Backlog and High/Done issues containing Astra produce one match for Astra + Backlog + High. Unknown priority returns 400; malformed title cannot overwrite a saved issue.

**Delivery:** 18 files; nine course files; 5,707 words; 2 passing regression cases. Build and integrated browser checks passed.

## 33. forum-search

[Start the course](../../JS1/forum-search/astraupskill/README.md) · [Verification](../../JS1/forum-search/astraupskill/VERIFICATION.md)

**Changed:** Search count and rows share a read-only repeatable-read transaction. Page numbers clamp to the available range, ordering has an id tie-breaker, and thread/tag inputs and author references are validated.

**Learn:** count/page consistency, stable ordering and bounded input. Create six threads matching a unique search, visit page two, delete its only item, then fetch page two again. The response reports the clamped first page with five rows and total five. Invalid author or malformed tag data is rejected.

**Delivery:** 16 files; nine course files; 6,696 words; 2 passing regression cases. TypeScript, build and integrated browser checks passed.

## 34. invoice-studio

[Start the course](../../JS1/invoice-studio/astraupskill/README.md) · [Verification](../../JS1/invoice-studio/astraupskill/VERIFICATION.md)

**Changed:** Invoices validate client UUIDs, real issue dates, bounded line arrays, whole positive quantities, two-decimal prices and tax from 0 to 100. Parent and line writes commit together, and a late line failure leaves no partial invoice change.

**Learn:** decimal input contracts and transactional parent/child writes. Create two units at 12.34, zero tax, issued 2028-02-29: total 24.68. Reject quantity [2], a three-decimal price and 2027-02-29. Force a replacement line insert to fail and verify the old invoice and lines remain intact.

**Delivery:** 16 files; nine course files; 6,606 words; 3 passing regression cases. TypeScript, build and integrated browser checks passed.

## 35. asset-checkout

[Start the course](../../JS1/asset-checkout/astraupskill/README.md) · [Verification](../../JS1/asset-checkout/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Status and audit writes use one row-locked transaction; count and rows share a repeatable-read snapshot. Seed dates map to the intended column. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** atomic status transitions, consistent pages and calendar dates. Create "Camera kit for field interviews" in Laptop with status Available, amount 12.50 and dueDate 2028-02-29. Request Checked Out twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item. A forced activity-insert failure leaves both the record and its prior history unchanged.

**Delivery:** 19 files; nine course files; 8,151 words; 4 passing regression cases. TypeScript, build and integrated browser checks passed.

## 36. equipment-maintenance

[Start the course](../../JS1/equipment-maintenance/astraupskill/README.md) · [Verification](../../JS1/equipment-maintenance/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Actual changes update the in-memory record and append one status event. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** repeat-safe workflow history and explicit input contracts. Create "Inspect west-wing ventilation" in HVAC with status Open, amount 12.50 and dueDate 2028-02-29. Request Scheduled twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item.

**Delivery:** 19 files; nine course files; 7,306 words; 3 passing regression cases. Build and integrated browser checks passed.

## 37. library-lending

[Start the course](../../JS1/library-lending/astraupskill/README.md) · [Verification](../../JS1/library-lending/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Actual changes update the in-memory record and append one status event. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** repeat-safe workflow history and explicit input contracts. Create "Loan a reference atlas" in Fiction with status Requested, amount 12.50 and dueDate 2028-02-29. Request Checked Out twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item.

**Delivery:** 19 files; nine course files; 7,347 words; 3 passing regression cases. Build and integrated browser checks passed.

## 38. gym-membership

[Start the course](../../JS1/gym-membership/astraupskill/README.md) · [Verification](../../JS1/gym-membership/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Actual changes update the in-memory record and append one status event. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** repeat-safe workflow history and explicit input contracts. Create "Beginner strength membership" in Strength with status Lead, amount 12.50 and dueDate 2028-02-29. Request Active twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item.

**Delivery:** 19 files; nine course files; 7,303 words; 3 passing regression cases. Build and integrated browser checks passed.

## 39. campaign-planner

[Start the course](../../JS1/campaign-planner/astraupskill/README.md) · [Verification](../../JS1/campaign-planner/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Actual changes update the in-memory record and append one status event. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** repeat-safe workflow history and explicit input contracts. Create "Autumn email welcome campaign" in Email with status Planning, amount 12.50 and dueDate 2028-02-29. Request Active twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item.

**Delivery:** 19 files; nine course files; 7,301 words; 3 passing regression cases. Build and integrated browser checks passed.

## 40. volunteer-coordinator

[Start the course](../../JS1/volunteer-coordinator/astraupskill/README.md) · [Verification](../../JS1/volunteer-coordinator/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Actual changes update the in-memory record and append one status event. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** repeat-safe workflow history and explicit input contracts. Create "Saturday food-bank shift" in Food Bank with status Draft, amount 12.50 and dueDate 2028-02-29. Request Open twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item.

**Delivery:** 19 files; nine course files; 7,292 words; 3 passing regression cases. Build and integrated browser checks passed.

## 41. learning-paths

[Start the course](../../JS1/learning-paths/astraupskill/README.md) · [Verification](../../JS1/learning-paths/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Status and audit writes use one row-locked transaction; count and rows share a repeatable-read snapshot. Seed dates map to the intended column. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** atomic status transitions, consistent pages and calendar dates. Create "Backend fundamentals with weekly review" in Frontend with status Planned, amount 12.50 and dueDate 2028-02-29. Request In Progress twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item. A forced activity-insert failure leaves both the record and its prior history unchanged.

**Delivery:** 19 files; nine course files; 8,158 words; 4 passing regression cases. TypeScript, build and integrated browser checks passed.

## 42. project-risks

[Start the course](../../JS1/project-risks/astraupskill/README.md) · [Verification](../../JS1/project-risks/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Actual changes update the in-memory record and append one status event. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** repeat-safe workflow history and explicit input contracts. Create "Supplier delay affects launch" in Schedule with status Identified, amount 12.50 and dueDate 2028-02-29. Request Mitigating twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item.

**Delivery:** 19 files; nine course files; 7,311 words; 3 passing regression cases. Build and integrated browser checks passed.

## 43. travel-requests

[Start the course](../../JS1/travel-requests/astraupskill/README.md) · [Verification](../../JS1/travel-requests/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Status and audit writes use one row-locked transaction; count and rows share a repeatable-read snapshot. Seed dates map to the intended column. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** atomic status transitions, consistent pages and calendar dates. Create "Training visit to the regional office" in Conference with status Draft, amount 12.50 and dueDate 2028-02-29. Request Submitted twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item. A forced activity-insert failure leaves both the record and its prior history unchanged.

**Delivery:** 19 files; nine course files; 8,151 words; 4 passing regression cases. TypeScript, build and integrated browser checks passed.

## 44. vendor-contracts

[Start the course](../../JS1/vendor-contracts/astraupskill/README.md) · [Verification](../../JS1/vendor-contracts/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Status and audit writes use one row-locked transaction; count and rows share a repeatable-read snapshot. Seed dates map to the intended column. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** atomic status transitions, consistent pages and calendar dates. Create "Annual monitoring software agreement" in SaaS with status Draft, amount 12.50 and dueDate 2028-02-29. Request Legal Review twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item. A forced activity-insert failure leaves both the record and its prior history unchanged.

**Delivery:** 19 files; nine course files; 8,146 words; 4 passing regression cases. TypeScript, build and integrated browser checks passed.

## 45. procurement-portal

[Start the course](../../JS1/procurement-portal/astraupskill/README.md) · [Verification](../../JS1/procurement-portal/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Actual changes update the in-memory record and append one status event. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** repeat-safe workflow history and explicit input contracts. Create "Developer workstation purchase" in Software with status Draft, amount 12.50 and dueDate 2028-02-29. Request Submitted twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item.

**Delivery:** 19 files; nine course files; 7,287 words; 3 passing regression cases. Build and integrated browser checks passed.

## 46. property-rentals

[Start the course](../../JS1/property-rentals/astraupskill/README.md) · [Verification](../../JS1/property-rentals/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Actual changes update the in-memory record and append one status event. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** repeat-safe workflow history and explicit input contracts. Create "One-bedroom courtyard unit" in Studio with status Available, amount 12.50 and dueDate 2028-02-29. Request Application twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item.

**Delivery:** 19 files; nine course files; 7,306 words; 3 passing regression cases. Build and integrated browser checks passed.

## 47. quality-audits

[Start the course](../../JS1/quality-audits/astraupskill/README.md) · [Verification](../../JS1/quality-audits/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Status and audit writes use one row-locked transaction; count and rows share a repeatable-read snapshot. Seed dates map to the intended column. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** atomic status transitions, consistent pages and calendar dates. Create "Quarterly access-control audit" in Process with status Planned, amount 12.50 and dueDate 2028-02-29. Request In Progress twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item. A forced activity-insert failure leaves both the record and its prior history unchanged.

**Delivery:** 19 files; nine course files; 8,142 words; 4 passing regression cases. TypeScript, build and integrated browser checks passed.

## 48. patient-intake

[Start the course](../../JS1/patient-intake/astraupskill/README.md) · [Verification](../../JS1/patient-intake/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Actual changes update the in-memory record and append one status event. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** repeat-safe workflow history and explicit input contracts. Create "Demo intake for a fictional learner" in Primary Care with status New, amount 12.50 and dueDate 2028-02-29. Request Reviewing twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item.

**Delivery:** 19 files; nine course files; 7,347 words; 3 passing regression cases. Build and integrated browser checks passed.

## 49. grant-manager

[Start the course](../../JS1/grant-manager/astraupskill/README.md) · [Verification](../../JS1/grant-manager/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Status and audit writes use one row-locked transaction; count and rows share a repeatable-read snapshot. Seed dates map to the intended column. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** atomic status transitions, consistent pages and calendar dates. Create "Community learning grant proposal" in Education with status Draft, amount 12.50 and dueDate 2028-02-29. Request Submitted twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item. A forced activity-insert failure leaves both the record and its prior history unchanged.

**Delivery:** 19 files; nine course files; 8,126 words; 4 passing regression cases. TypeScript, build and integrated browser checks passed.

## 50. incident-response

[Start the course](../../JS1/incident-response/astraupskill/README.md) · [Verification](../../JS1/incident-response/astraupskill/VERIFICATION.md)

**Changed:** Typed and bounded inputs protect edits, real calendar dates round-trip, page numbers clamp and equal sort values use an id tie-breaker. Repeating the current status creates no extra status history. Status and audit writes use one row-locked transaction; count and rows share a repeatable-read snapshot. Seed dates map to the intended column. The shared toolbar now uses two flexible columns so its search field remains readable beside the form and activity panels.

**Learn:** atomic status transitions, consistent pages and calendar dates. Create "Intermittent checkout latency" in Availability with status Open, amount 12.50 and dueDate 2028-02-29. Request Investigating twice: one status event is added. An edit with dueDate 2027-02-29 returns 400 and preserves the old record. With three matching records and pageSize 2, page 999 clamps to page 2 with one item. A forced activity-insert failure leaves both the record and its prior history unchanged.

**Delivery:** 19 files; nine course files; 8,110 words; 4 passing regression cases. TypeScript, build and integrated browser checks passed.

