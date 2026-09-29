# Support Tickets — Fable review

- **Path:** `JS1/support-tickets`  ·  **Wave:** 1  ·  **Stack:** TypeScript + Express + PostgreSQL (`pg`) + React/Vite  ·  **Batch:** B04
- **Astra's change (one line):** Status and assignee PATCH routes now `SELECT ... FOR UPDATE` the ticket inside the existing transaction, return unchanged (no audit event) when the requested value already matches, validate UUIDs at the `app.param("id")` boundary and in `parseTicket`, funnel async route errors through one `asyncRoute` wrapper, and map PostgreSQL SQLSTATEs (`22P02/23503/23505/23514/22003`) to 400 instead of 500.
- **Course size:** 6,621 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/feature.test.ts`, helper `test/database.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 4 | 3 | 5 | 4 | 5 | 3 | 2 | 3.9 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- The code change is real, not cosmetic. `server/src/index.ts:175-178` reads the current row under `FOR UPDATE` and short-circuits (`if (currentRow.status === status) return true;`) before writing, so a repeated command produces no second audit row; the same pattern is applied to assignment at `:200-205`.
- The tests exercise the changed behaviour rather than "calls happened". `test/feature.test.ts` fires two concurrent `PATCH /status` calls via `Promise.all` and asserts `events.filter(x=>x.kind==='status').length === 1`; the third test installs a real PL/pgSQL `BEFORE INSERT` trigger on `ticket_events` to force the audit write to fail and asserts the ticket is unchanged afterwards. That is genuine fault injection against a real database.
- Course line references are exact. `03-WORKED-CHANGE.md:19` says "near line 171" and the quoted block is a character-for-character match of `server/src/index.ts:171`.
- VERIFICATION.md is unusually honest: it names harness versions, states that `latest` dependency ranges stay floating, says the browser check proxied to the real Express server rather than fabricated responses, and separates exercises from delivered work.

## Problems found (evidence required)
- **[D8]** The scaffolding is a shared template. The `02-CONCEPTS.md` paragraph "Validation rejects values the operation cannot accept…" appears verbatim in **all 48** `astraupskill/02-CONCEPTS.md` files under `Desktop/JS1`, as does "Before extracting a new abstraction, explain what repeated responsibility it would own." Only the central-idea heading, the scope sentence and one data-model paragraph are project-specific; `astraupskill/README.md` differs from `JS1/forum-search/astraupskill/README.md` by 6 lines out of 72.
- **[D8]** The same fixture sentence ("Create a ticket, resolve it twice, and read history…") is pasted unchanged into 01, 03, 04, 05, 06, 07 and VERIFICATION. Seven copies of one paragraph is filler, not reinforcement.
- **[D7]** The tests a junior is told to read are minified. `test/feature.test.ts:1` is `import {test,before,after} from 'node:test';import assert from 'node:assert/strict';import {randomUUID} from 'node:crypto';` and each test body is 2-3 physical lines holding several statements. `03-WORKED-CHANGE.md` instructs "Read each test as arrange → act → assert" over code formatted to make that hard.
- **[D3]** Exercise prompts are one-sentence stubs and the solution notes are boilerplate. `05-PRACTICE.md` Exercise 1 is the entire sentence "Disable the currently selected status action."; in `06-SOLUTIONS-AND-REVIEW.md` the **Review** paragraph ("Demonstrate an ordinary case and a case that would break a naive implementation…") is identical for Exercises 1, 2 and 3.
- **[D2]** Test scaffolding leaked into product code: `client/src/App.tsx:114-133` now carries `id="lesson-field-1"` … `id="lesson-field-4"`, names that exist only so `batch03/browser_checks.mts` can call `page.locator('#lesson-field-1')`. The `htmlFor`/`id` pairing is an accessibility win; the naming is harness debt a learner will copy.
- **[D5]** Every dependency in `package.json` is `"latest"` (`express`, `pg`, `react`, `typescript`, `vite`…) and no lockfile ships. VERIFICATION.md admits this, but a junior on a fresh machine can still get a different tree from the verified Node 22.16.0 / PostgreSQL 18.1 run.

## Spot-checks performed
- Claim "The excerpt below comes from server/src/index.ts near line 171" (`03-WORKED-CHANGE.md:19`) -> read `server/src/index.ts:171-190` -> **matches** exactly, including the `FOR UPDATE` query text.
- Claim "client/src/api.ts sends typed client data as untyped JSON over HTTP" (`01-CODEBASE-MAP.md:16`) -> listed `client/src` -> `api.ts` exists alongside `App.tsx`, `main.tsx`; **matches**.
- Claim VERIFICATION.md "Automated test cases: **3**" -> counted `test(` in `test/feature.test.ts` -> 3; **matches**.
- Claim VERIFICATION.md "Chromium interaction | Passed" -> `batch03/browser-checks.json` has `{"project":"31","passed":true,"api":"actual isolated HTTP server","persistence":"disposable PostgreSQL schema"}`, `batch03/logs/31-browser.png` exists, and `batch03/browser_checks.mts:21` launches real headless Chromium via Playwright; **matches**, not an unsupported claim.
- Independent check: `diff -rq batch03/stage/31 JS1/support-tickets` differs only by `client/dist` -> the code that was build/typecheck/test/browser-checked is byte-identical to what shipped; **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Reformat `test/feature.test.ts` and `test/database.ts` to one statement per line with blank-line arrange/act/assert sections, and re-paste the reformatted source into the second code block of `astraupskill/03-WORKED-CHANGE.md`. (effort: S)
2. Replace the generic halves of `astraupskill/02-CONCEPTS.md` (sections "Validation versus normalization", "Identity, representation and derived values", "Small design decisions deserve explanations") with ticket-specific material: what `ticket_labels` junction rows mean for a PUT that replaces the label set, and why `DELETE` + re-`INSERT` inside one transaction is safe here. (effort: M)
3. Expand `astraupskill/05-PRACTICE.md` Exercises 1-4 from one-liners into prompts with a stated starting state, an acceptance example and the file to edit; give each a distinct **Review** paragraph in `06-SOLUTIONS-AND-REVIEW.md`. (effort: M)
4. Rename `client/src/App.tsx` ids `lesson-field-1..4` to semantic ones (`ticket-subject`, `ticket-priority`, …) and update the selectors in `batch03/browser_checks.mts`. (effort: S)
5. Commit a `package-lock.json` or replace `"latest"` in `package.json` with the versions VERIFICATION.md says were tested, and add a known-good-versions table to the setup section of `astraupskill/README.md`. (effort: S)

## One-paragraph summary for the index
This is the strongest kind of CRUD lesson in the batch: a real concurrency bug (duplicate audit events from repeated status/assignment commands) fixed with `SELECT … FOR UPDATE` inside an existing transaction, plus UUID validation and PostgreSQL error-code mapping, backed by three tests that use concurrent requests and an injected `BEFORE INSERT` trigger to prove rollback. Everything the course says about the code is true — the line-171 excerpt is exact, the file map is right, and VERIFICATION.md matches the batch evidence including a real Playwright screenshot. The weakness is the wrapper: roughly two thirds of the prose is a template shared with 47 other courses, the exercises are one-sentence stubs, and the tests you are told to study are minified onto three lines. Do it for the transaction and audit-event material; skim chapter 2 and write your own exercises.
