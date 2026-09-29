# newcodexJS/20-marketplace-platform — Fable review

- **Path:** `newcodexJS/20-marketplace-platform`  ·  **Wave:** 1  ·  **Stack:** Node/TS, Express, Knex, PostgreSQL, React+Vite  ·  **Batch:** B08
- **Astra's change (one line):** Adds an additive `status_before_archive` migration plus a `lifecycleUpdate`/`statusFields` pair so archive remembers the prior workflow state, restore returns to it, repeats are no-ops, and bulk status edits dedupe IDs, lock all targets `FOR UPDATE` in ID order, reject the whole batch if any target is missing, and write real before/after audit rows; it also tightens payload validation, adds an `id` tie-breaker to list ordering, and adds a request-sequence guard in the React list.
- **Course size:** 8,377 words across 9 files  ·  **Tests claimed:** 4  ·  **Tests found on disk:** 4 (`test/crud.test.ts`, with harness `test/database.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 3 | 5 | 4 | 5 | 4 | 2 | 4.0 |

**Verdict:** IMPROVE    **Path role:** elective

## What Astra did well
- The code change is the real thing a junior needs to see: `server/src/models/model.ts:173` `lifecycleUpdate` takes `forUpdate()` on the row inside `db.transaction`, short-circuits on a repeated archive/restore, and writes activity + audit on the same `trx`. `bulkStatus` (model.ts:99+) locks `.whereIn("id", ids).orderBy("id").forUpdate()` and throws `NotFoundError` before any write if `beforeRows.length !== ids.length`.
- The migration is genuinely additive (`server/db/migrations/003_archive_status.ts` only adds a nullable column and has a working `down`), which is the correct teaching pattern for changing a lifecycle.
- The tests assert stored state, not just status codes: `test/crud.test.ts` counts `audit_log` rows before and after a repeated archive to prove idempotence, and re-reads the record after a rejected bulk update to prove nothing changed.
- Evidence is real and matches the claims: `batch04/checks.json` has 7 green checks for project 71, `logs/71-tests.log` ends `# pass 4 / # fail 0`, and `browser-checks.json` records 22 real API requests against an isolated server rather than a mock.

## Problems found (evidence required)
- **[D8]** The course is a noun-swap of its sibling clones. `diff 19-realtime-chat-platform/astraupskill/05-PRACTICE.md 20-marketplace-platform/astraupskill/05-PRACTICE.md` changes **1 line out of 47**; `02-CONCEPTS.md` differs in 3 lines, all of them "conversations/workspace_id/muted" to "listings/vendor_id/active". Identical but for the noun: *"Archive is a lifecycle operation with two related facts: a status and an archived timestamp… The statusFields helper synchronizes those fields whether the request came from an archive button, a form or a bulk command."*
- **[D3]** `07-TRACE-LAB.md` has six "Boundary N" sections that all repeat one paragraph verbatim: *"Find the relevant call in the source for this project, starting with server/src/models/model.ts and `lifecycleUpdate`."* (6 occurrences). `06-SOLUTIONS-AND-REVIEW.md` repeats *"Demonstrate an ordinary case and a case that would break a naive implementation…"* 4 times, once per exercise. The trace lab is the single biggest chapter (1,987 words) and much of it is this filler.
- **[D2]** `client/src/App.tsx:124` `runBulkStatus` has no `try/catch`, unlike `saveRecord` immediately above it. A rejected bulk status — exactly the new 404-on-missing-ID path the course teaches — produces an unhandled promise rejection and no visible error, which contradicts the course line "failed saves retain the draft and show an error" being presented as covering the mutation paths.
- **[D2]** Of the 36 files counted as changed, most differ only by Prettier reformatting (e.g. `server/db/migrations/002_enterprise_features.ts` shows only line-wrapping changes). A learner diffing backup vs. current must wade through that noise to find the ~150 meaningful lines.
- **[D5]** The documented command is `npm test` (root → `npm run test --workspace server` → `tsx --test ../test/*.test.ts`), but `batch04/checks.json` shows the check actually ran `tsx --test <absolute path to test/crud.test.ts>`. The documented glob-through-npm-script form was never exercised on this machine.

## Spot-checks performed
- Course: *"The excerpt below comes from server/src/models/model.ts near line 173"* -> `grep -n lifecycleUpdate server/src/models/model.ts` returns `173:async function lifecycleUpdate(` and the quoted body is byte-identical -> **matches**.
- Course: *"Bulk IDs are deduplicated"* -> `server/src/services/service.ts:199` `const ids = [...new Set(payload.ids.map((id) => parseId(String(id))))];` -> **matches**, and explains why the test's `[a.id, a.id]` returns one row instead of a 404.
- Course: *"List refreshes ignore stale responses"* -> `client/src/App.tsx:58,67,76` `const sequence = ++refreshSequence.current;` guarded by `if (sequence !== refreshSequence.current) return;` on both the success and catch paths -> **matches**.
- Course: *"failed saves retain the draft and show an error"* -> `client/src/App.tsx:98-107` `saveRecord` only calls `setForm(emptyForm)` after a successful await and sets `error` in `catch` -> **matches for saves**, does **not** hold for bulk actions.
- Course README: *"The root package.json is an npm workspace joining client and server"* -> root `package.json` is `"name": "astra-crud-workspace-71"` with `"workspaces": ["client","server"]` -> **matches**; note this root file was created by Astra and is absent from the backup.

## Improvements needed (ordered, concrete, actionable)
1. Rewrite `astraupskill/05-PRACTICE.md` and `02-CONCEPTS.md` around this marketplace domain (vendors, listings, flagged/paused moderation) instead of the shared text used by projects 16-20; at minimum exercises 0, 3 and 4 must name marketplace-specific invariants. (effort: M)
2. Collapse `07-TRACE-LAB.md` boundaries 1-6 into one instruction plus six one-line boundary descriptions, and point each boundary at the file that actually implements it (`routes/routes.ts` → `controllers/controller.ts` → `services/service.ts` → `models/model.ts`) rather than repeating `model.ts`/`lifecycleUpdate` six times. (effort: S)
3. Wrap `runBulkStatus` in `client/src/App.tsx` in the same `try/catch` + `setError` as `saveRecord`, and add one assertion or a note in `04-TESTING-AND-DEBUGGING.md` that the UI surfaces the bulk 404. (effort: S)
4. In `VERIFICATION.md`, say that a whole-repo Prettier reformat is part of the diff and tell the learner to read it with `git diff -w` so the behavioral change is visible. (effort: S)
5. Either fix the root `test` script so the documented `npm test` works on Windows, or document the exact per-file command that was actually verified. (effort: S)

## One-paragraph summary for the index
This is the best-engineered change in its clone family: archive/restore now preserves the previous workflow status through an additive migration, and bulk status edits lock every target row in ID order, reject the whole batch on a missing ID, and write truthful before/after audit rows — all covered by four tests that check stored rows rather than HTTP codes. The verification evidence is honest and reproducible if you have PostgreSQL and two disposable databases. The weakness is the prose, not the code: `05-PRACTICE.md` is one sentence away from being identical to the sibling chat-platform course, and the trace lab repeats the same paragraph six times. Do this course if you want row locks, atomic bulk edits and audit trails on Express+Knex+Postgres — but do only **one** of projects 16-20, because the other four teach the same lesson with the nouns swapped.
