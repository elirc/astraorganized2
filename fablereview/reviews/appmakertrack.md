# appmakertrack (kanban + time tracker) — Fable review

- **Path:** `_Organized Desktop/08 App And Product Projects/appmakertrack`  ·  **Wave:** 2  ·  **Stack:** Next 15.1.3 App Router / React 19 / TypeScript / Prisma + SQLite / `node:test` via tsx  ·  **Batch:** B13
- **Astra's change (one line):** Pulled all request parsing and write logic out of five API routes into four new `lib/` modules — a hand-written strict validator (`time-entry-validation.ts`), a timer service whose stop is a compare-and-set `updateMany({where:{id, endTime:null}})` and whose start wraps the running-check + create in `$transaction`, a board `moveTicket` that reads both sibling lists inside the transaction, rejects a target column from another project, clamps the insertion index and rewrites contiguous positions via temporary negative parking, plus `safeErrorResponse` so driver messages stop leaking into 500 bodies; 404/409 now distinguished from 400 everywhere.
- **Course size:** 6,198 words across 9 files (README 296 … 06-SOLUTIONS 2,362)  ·  **Tests claimed:** 13  ·  **Tests found on disk:** 13 `test(...)` in `tests/time-entry-validation.test.ts`, and the shipped log `astraupskill/evidence/luna-test-freeze-20260912.log` ends `# pass 13 / # fail 0`

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 4.9 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- Every defect fixed is a textbook CRUD defect, and the course names the original bug precisely. `03-WORKED-CHANGE.md:3` — "The original manual POST checked `!body.duration`, which rejected a valid zero" — is exactly what the backup contains (`backups/b7429e8bf71d/app/api/tickets/[ticketId]/time-entries/route.ts:35`, `if (!body.startTime || !body.endTime || !body.duration)`).
- The stop route went from read-then-blind-update to a real compare-and-set: `lib/time-entry-service.ts:11` `updateMany({ where: { id: entryId, endTime: null }, ... })` with `if (result.count !== 1) return { kind: "conflict" }`. The course explicitly teaches that the *initial read is not the guard* (`06-SOLUTIONS-AND-REVIEW.md` §3) — the single most valuable lesson in this batch.
- Omitted-vs-explicit-null is handled correctly and taught as such: `...(notes !== undefined && { notes })` in the service, and exercise 10 in `05-PRACTICE.md` is built around catching "accidental `body.notes || null` coercion".
- Tests are real seams, not "calls happened" assertions. They import the actual `parseManualEntry`, `stopRunningEntry`, `startTimer`, `moveTicket`, `createManualEntryHandler` and `createStartTimerHandler` and assert row state, Prisma argument shapes, and contiguous positions by ticket identity.
- Verification is unusually honest: raw `node:test` TAP logs, lint, typecheck, install, generate and Next build logs are all shipped under `astraupskill/evidence/` with a `results.json` scope string that explicitly says "no live database or browser". VERIFICATION.md also warns not to run `db:push`/`db:seed` because the seed resets `prisma/dev.db`, and notes that assigning `DATABASE_URL` will not override the literal URL in `schema.prisma` — a real, project-specific trap.
- Exercises are prediction-first and escalate: classify/predict (1–5), design a race (3), build a fixture and snapshot rows (6–7), then propose a harness and label it unproven (8). Solutions live in a separate file.

## Problems found (evidence required)
- **[D7]** No glossary. `02-CONCEPTS.md`/`03-WORKED-CHANGE.md` use "compare-and-set", "conditional write", "seam", "parking positions", "identity resolver" without ever defining them; a junior will need to look several up. The prose is also quite compressed (one idea per sentence, few examples per paragraph).
- **[D2, minor]** `parseInstant` (`lib/time-entry-validation.ts:11`) is a hand-rolled ISO regex capped at 3 fractional digits, so a legitimate client sending `2025-01-01T10:00:00.123456Z` gets a 400. This is a deliberate strictness choice but the course never lists it as a limit; `04`/`VERIFICATION` mention SQLite and identity limits but not this one.
- **[D2, minor]** `moveTicket` issues roughly 2×N row updates per move (`lib/board-service.ts:37-47`) where the original did 2–3 `updateMany` statements. Correctness improves, write amplification worsens; the course does not mention the trade-off. There is also no unique constraint on `(columnId, position)`, which VERIFICATION does disclose.
- **[D2, minor]** Behaviour change not flagged for API consumers: start-timer conflict moved from **400** to **409** and stop moved from 400 to 404/409. Nothing in the app currently reads those statuses (`grep -rn "TIMER_ALREADY" hooks lib components` only hits the handler itself), so no regression — but the course should say "if you had a client checking for 400, it breaks".
- **[D1, cosmetic]** `README.md` and `05-PRACTICE.md` begin with a UTF-8 BOM, which renders as a stray character before the `#` in some viewers.
- **[D2, cosmetic]** The lint cleanup changed `app/projects/[projectId]/page.tsx:16` to `const [, setSelectedTicketId] = useState<string|null>(null)`, leaving a setter whose value nothing reads. Correct for lint, but it is a dead-state smell the course could have used as a teaching moment instead of silently patching.

## Spot-checks performed
- README: "Next.js 15 App Router project" -> `package.json:24` `"next": "15.1.3"` -> **matches**.
- VERIFICATION: "records thirteen passing Node test cases, zero failures" -> `astraupskill/evidence/luna-test-freeze-20260912.log` tail `1..13 / # pass 13 / # fail 0`, and `grep -c "^test("` on `tests/time-entry-validation.test.ts` = 13 -> **matches**.
- 06-SOLUTIONS §2: "`notes: null` is included in the update data and clears notes" -> `lib/time-entry-service.ts:11` `...(notes !== undefined && { notes })` -> **matches**.
- 06-SOLUTIONS §6: "the route maps that result to status 400" for a foreign target column -> `app/api/tickets/[ticketId]/move/route.ts:16` `if (result.kind === "invalid-target") return ... { status: 400 }`, and `lib/board-service.ts:15` compares `target.projectId !== ticket.projectId` inside `$transaction` -> **matches**.
- 06-SOLUTIONS §4: "duration PATCH is 409 with `RUNNING_TIMER`" -> `app/api/time-entries/[entryId]/route.ts:17-18` returns `code: "RUNNING_TIMER"`, status 409, when `existing.endTime === null && body.duration !== undefined` -> **matches**.
- 03-WORKED-CHANGE's inlined `stopRunningEntry` code block -> byte-compared against `lib/time-entry-service.ts:4-15` -> **identical** (not paraphrased).
- VERIFICATION: "The lint command is eslint ." -> `package.json:10` `"lint": "eslint ."` (was `next lint` in the backup) -> **matches**; `lint:changed` exists but is described as a convenience, not a substitute.
- Delivery JSON `testResults`/`results.json` claim of a passing production build -> `evidence/root-build-final-01.log` ends with the Next route table -> **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Add a 15–20 term glossary section to `astraupskill/02-CONCEPTS.md` (compare-and-set, conditional update, zero-rows-as-conflict, transaction, seam, injected client, parking position, idempotency, 400 vs 404 vs 409). (effort: S)
2. Add a "known strictness and cost" paragraph to `VERIFICATION.md`: `parseInstant` rejects >3 fractional digits and offsets outside ±23:59; `moveTicket` performs ~2N updates; start/stop conflict statuses changed from 400 to 409/404. (effort: S)
3. Actually write exercise 8's temporary-SQLite harness as a second, skipped test file (`tests/board-service.integration.test.ts` guarded by an env flag) so the course's biggest stated gap becomes runnable instead of "proposed". (effort: M)
4. Extend the injected-client seam from `time-entry-handlers.ts` to the stop/PATCH/move route wrappers, as `03-WORKED-CHANGE.md` itself recommends, and add one response-level test per route. (effort: M)
5. Strip the UTF-8 BOM from `README.md` and `05-PRACTICE.md`. (effort: S)

## One-paragraph summary for the index
Do this one. It is the strongest course in batch B13 and a near-ideal CRUD lesson for a junior: five Next.js App Router routes are refactored from truthiness checks and blind updates into a validator, a timer service and a board service, and each fix maps to a named failure — zero durations rejected by `!body.duration`, a lost-update race on timer stop, a ticket moved into another project's column, and a Prisma error message leaking through a 500. Thirteen tests exercise the real functions with partial Prisma doubles, the raw test/lint/typecheck/build logs are shipped inside the course, and the limits (no live SQLite transaction proof, no identity model, global rather than per-user timer policy) are stated plainly rather than papered over. Every claim I spot-checked against the code matched, including a code block that is byte-identical to the file it quotes. Budget a few evenings: 6k words, eleven prediction-style exercises, and a separate solutions chapter that answers all of them.
