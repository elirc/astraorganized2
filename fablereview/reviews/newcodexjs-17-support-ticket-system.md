# newcodexJS/17-support-ticket-system — Fable review

- **Path:** `newcodexJS/17-support-ticket-system`  ·  **Wave:** 1  ·  **Stack:** Node/Express + Knex/Postgres + React/Vite, TypeScript  ·  **Batch:** B07
- **Astra's change (one line):** Identical to stages 67/69/70/71 with `tickets`/`team_id` nouns — additive migration `003_archive_status.ts` adding `status_before_archive`, `lifecycleUpdate` locking the row and making repeat archive/restore no-ops, `bulkStatus` de-duplicating IDs, locking all targets in ID order, failing the whole batch with 404 on a missing target and writing real before/after audit rows, `sanitizePayload` gaining real field validation, and a React sequence-counter guard against stale list refreshes — **plus** one project-specific fix: the seed wrote a nonexistent `subject` column and now writes `title`.
- **Course size:** 8,425 words across 9 files  ·  **Tests claimed:** 4  ·  **Tests found on disk:** 4 (`test/crud.test.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 3 | 5 | 4 | 5 | 4 | 1 | 3.9 |

**Verdict:** REWORK    **Path role:** skip

## What Astra did well
- The underlying code change is genuinely good (see the 16-team-project-management review for the detailed assessment — the source files are line-identical). The archive/restore/bulk-audit work, the `FOR UPDATE` batch locking and the React stale-response guard are all real improvements over the backup.
- This is the one project in the family with a unique, verified defect fix. Diffing `backups/68/server/db/seeds/001_seed.ts` against the delivered seed shows `"subject": "Cannot access account"` etc. replaced with `title: "Cannot access account"` — the seed had been writing a column that does not exist in `001_init.ts`. The report flags it explicitly: "One support-ticket seed referenced a nonexistent `subject` column; it now uses the actual `title` column."
- The domain vocabulary is correctly threaded through the tests: `allowedStatuses` is `["open","pending","escalated","resolved","archived"]` (`server/src/services/service.ts:4-10`) and `test/crud.test.ts:38` creates the lifecycle fixture in `"pending"`, matching `VERIFICATION.md`'s "Create a record in pending… restore returns pending".
- All 69 substantive code lines in `03-WORKED-CHANGE.md` matched verbatim against the project's `.ts`/`.tsx` sources (69/69).

## Problems found (evidence required)
- **[D8 = 1]** The course is a noun-swapped copy. Against `newcodexJS/16-team-project-management/astraupskill`, character similarity is: README 98.7%, 01-CODEBASE-MAP 98.7%, 02-CONCEPTS 98.2%, 03-WORKED-CHANGE 98.6%, **04-TESTING-AND-DEBUGGING 99.7%**, **05-PRACTICE 99.5%**, 06-SOLUTIONS 98.3%, 07-TRACE-LAB 99.3%, VERIFICATION 99.0%. This is exactly the rubric's D1 description: "Boilerplate paragraphs copy-pasted across projects with the noun swapped." The same 8.4k words are also shipped as 18-learning-management-system, 19-realtime-chat-platform and 20-marketplace-platform.
- **[D8]** The report itself gives the game away: the stage 67, 68, 69, 70 and 71 "Implemented improvement" cells in `astrdocs/NEXT_25_IMPLEMENTATION_REPORT.md` are word-for-word identical apart from stage 68's single added sentence about the seed column, and the "Boundaries and next work" bullets differ only in `workspace_id` / `team_id` / `school_id` / `vendor_id`.
- **[D2]** The same dead code as the rest of the family: `restoreRecord` passes `{ archived_at: null, status: "active" }` into `lifecycleUpdate`, which unconditionally replaces it with `{ …, status: before.status_before_archive || "open" }` (`server/src/models/model.ts:188`). `"active"` is not a member of this project's `allowedStatuses`.
- **[D3]** `07-TRACE-LAB.md` "Trace the real call path" lists six differently-labelled boundaries and then repeats one byte-identical paragraph six times, all pointing at "starting with [server/src/models/model.ts](../server/src/models/model.ts) and `lifecycleUpdate`".
- **[D3]** All four exercise solutions in `06-SOLUTIONS-AND-REVIEW.md` carry the identical "**Review:** Demonstrate an ordinary case and a case that would break a naive implementation…" paragraph.
- **[D5]** Root `package.json` declares only `{"concurrently": "^9.1.2"}` while `test/database.ts` imports `pg`; the repeated "The root workspace also makes pg and tsx available to the root test directory" is true only via npm hoisting. No Node/Postgres version is pinned in `README.md`.

## Spot-checks performed
- Claim (`VERIFICATION.md`): "Create a record in pending, archive it twice and restore it twice… restore returns pending" -> read `test/crud.test.ts:38,47` (`create("Lifecycle","pending")`, `assert.equal(r.data.data.status, "pending")`) and `service.ts` `allowedStatuses` containing `"pending"` -> matches.
- Claim (report): "The sample seed uses the actual title column" -> diffed `backups/68/server/db/seeds/001_seed.ts` against the delivered file; three `"subject":` keys became `title:` -> matches, and `001_init.ts` confirms the column is `title`.
- Claim: "all targets are locked and checked before any change" -> read `model.ts` `bulkStatus`: `baseQuery(trx).whereIn("id", ids).orderBy("id").forUpdate()` then `if (beforeRows.length !== ids.length) throw new NotFoundError("One or more records were not found; no statuses changed.")` -> matches.
- Claim: "Automated test cases: 4" -> `batch04/logs/68-tests.log` shows `# tests 4 / # pass 4 / # fail 0`; `grep -c '^test('` returns 4 -> matches.
- Claim (VERIFICATION table): "Chromium interaction | Passed" -> `batch04/browser-checks.json` `{"project":"68","passed":true,"api":"actual isolated HTTP server","api_requests":22}` -> matches.
- Template check: `diff 16-team-project-management/astraupskill/04-TESTING-AND-DEBUGGING.md 18-.../04-TESTING-AND-DEBUGGING.md` returns a single changed sentence (`in_progress` → `review`). Confirmed the same pattern holds for this project.

## Improvements needed (ordered, concrete, actionable)
1. Drop `newcodexJS/17-support-ticket-system/astraupskill/` from the learning path and replace `README.md` with a three-line pointer to the 16-team-project-management course plus the one thing unique here (the `subject` → `title` seed bug). The code change stays; only the duplicated course leaves. (effort: S)
2. If it must remain a standalone course, rewrite 02, 04, 05 and 06 around support-desk invariants that the other four projects do not have: SLA clocks and `escalated` transitions, first-response vs resolution timestamps, requester-vs-agent visibility, and reopening a resolved ticket. Nothing in the current 8.4k words is ticket-specific except the status names. (effort: L)
3. Promote the seed-column bug into a taught lesson. "The seed wrote a column that does not exist" is an excellent 20-minute exercise (run the seed, read the Postgres error, find the migration, fix it) and it is currently a single sentence in the batch report. (effort: S)
4. Delete the dead `status: "active"` argument in `restoreRecord` (`server/src/models/model.ts`), or annotate it in `03-WORKED-CHANGE.md`. (effort: S)
5. Rewrite `07-TRACE-LAB.md` "Boundary 1..6" so each boundary names its own file rather than repeating the `lifecycleUpdate` pointer six times. (effort: S)

## One-paragraph summary for the index
The code change here is solid — archive now remembers the ticket's previous status in an additive migration, repeat archive/restore are no-ops, bulk status changes lock every target in ID order and fail the whole batch if one is missing, audit rows finally record real before/after values, and a seed that wrote a nonexistent `subject` column was fixed to use `title`. The course that explains it, however, is a 98–99% character-for-character copy of the team-project-management, learning-management, realtime-chat and marketplace courses with only the status names swapped; chapter 04 differs from its sibling by exactly one sentence. There is nothing support-desk-specific in it — no SLA clocks, no requester-vs-agent visibility, no reopen semantics. Read the 16-team-project-management course instead and skip this one, unless you want the twenty-minute exercise of reproducing the seed-column bug.
