# z3 / customer-feedback-board — fix report (B12)

## Done
- [review #1 / backlog 3.1] Added the four code blocks the review asked for, plus three more. The course had **one** fenced block in nine files; it now has blocks in six files:
  - `02-CONCEPTS.md` — the full `transact()` from `src/server/store.ts:38-58` under "Atomicity versus concurrency control", with a four-point read-along (why `BEGIN IMMEDIATE` locks before reading, why the callback must be synchronous, why `validateDatabase` runs before the write, what the `catch` rolls back); then `expected()` from `service.ts:41-48` **and** its real call site — the whole `editPost` branch, `service.ts:251-267` — under optimistic concurrency.
  - `01-CODEBASE-MAP.md` — the `"use server"` + post-commit `revalidatePath` block from `actions.ts:1-28`.
  - `04-TESTING-AND-DEBUGGING.md` — the stale-edit test from `tests/workflow.test.ts:258-272`, with the two habits worth copying (change exactly one field between the accepted and rejected call; re-read through `post()` instead of trusting the returned value).
  - `06-SOLUTIONS-AND-REVIEW.md` — the `service.ts:493-498` return shape, so the empty-state answer is a two-line decision rather than a paragraph.
  - `07-TRACE-LAB.md` — a fixed notebook shape for each hop, ending with separate `observed:` and `inferred:` lines.
- [review #2] Added "What the SQLite store replaced" to `01-CODEBASE-MAP.md`. `src/server/json-store.ts` is now a three-line tombstone, so I recovered the real retired implementation from `astra-remaining-improvements/backups/2f14585fed41/src/server/json-store.ts` and quoted `updateJsonFile`'s promise-per-path queue verbatim, followed by the three things wrong with it mapped one-to-one onto what the current store does: the `Map` lock lives in one process (→ `BEGIN IMMEDIATE`, and why `tests/worker.ts` races *processes*), `fs.writeFile` of a whole document can truncate (→ atomic `COMMIT`), and nothing validated the result (→ `validateDatabase`).
- [review #3] Added an effort table to the top of `05-PRACTICE.md`: exercise 1 one session, 2 one-to-two sessions, 3 and 4 explicitly **multi-day stretch tasks**, with a sentence saying it is reasonable to design 3 and 4 on paper and stop there.
- [review #4] Added the `revalidatePath` caveat to `01-CODEBASE-MAP.md`: it is synchronous cache-tag bookkeeping and will rarely throw, so the `try/catch` is a deliberately visible model of the general rule ("a side effect after the commit must never make the user retry the write"), not a failure mode to expect in logs — with the cases where that rule has real teeth (email, job enqueue, payment confirmation).
- [review #5] Replaced the dangling "older notes" reference with a link to the historical [build journal](../docs/learning/build-journal.md), which is where the retired files are actually listed (`docs/learning/build-journal.md:145` names `src/server/json-store.ts`), and put the retired implementation itself in the chapter.
- [backlog 3.4] Added a "Red-first: break it on purpose" section to `04-TESTING-AND-DEBUGGING.md`. This project ships no `.before` snapshots, so the drill uses the live code: comment out `expected(p, cmd.version)` and predict which assertion of the stale-edit test fails (the second one — the data-protection one); change `BEGIN IMMEDIATE` to `BEGIN` and run the cross-process test; remove the `instanceof Promise` guard and make a branch `async` to watch a test "pass" while committing nothing.
- [backlog 3.5] Added to `astraupskill/README.md`: a prerequisites paragraph, a per-chapter time-budget table (with the practice row carrying the effort split), and a 14-term glossary (Server Action, aggregate, transaction/`BEGIN IMMEDIATE`, atomicity, optimistic concurrency/captured version, 409, idempotency/desired state, projection, visibility, audit entry, reference-aware delete, merge/canonical target, revalidation, fixture).

## Skipped
- No source changes. Every review item was a course edit; the code scored 5/5 on accuracy and change quality and the review named no bug.
- backlog 3.2 (agent-process language): `grep -in "manifest|baseline|frozen|root agent|stage" astraupskill/*.md` finds nothing — this course never had it.
- backlog 3.3 (evidence in repo): already satisfied before I started. The four PNG captures are in `astraupskill/images/` and `VERIFICATION.md` links them relatively.
- backlog 3.11 (inline solutions in the practice chapter): does not apply; 05 states acceptance criteria, not answers, and 06 is deliberately reasoning rather than code.

## Verification
- `npm ci` then `npm test` (`tsx --test tests/*.test.ts`) → `# tests 43` / `# pass 43` / `# fail 0`, exit code 0 (133.9s). That is the backend half of the claimed 59 and it covers everything the edited chapters quote. The 16 Playwright scenarios were **not** re-run: `npm run verify` needs the dev server stopped and builds a fresh fixture, and the machine was running several other agents' installs at the time.
- Excerpt fidelity checked line by line against the source before pasting: `src/server/store.ts:38-64`, `src/modules/feedback/service.ts:41-48, 251-267, 493-498`, `src/modules/feedback/actions.ts:1-28`, `tests/workflow.test.ts:258-272`, and `backups/2f14585fed41/src/server/json-store.ts:26-41`.
- `grep -c '^```' astraupskill/*.md` → 4/6/2/2/0/2/2/0/0 (was 0/0/2/0/0/0/0/0/0).
- Every file in `astraupskill/` is CRLF; all edits were applied through a script that reads with `newline=""` and writes back with the file's own newline, and a post-edit check shows no file with mixed endings.

## Course/code consistency check
- `src/server/store.ts:28-70` re-read against the new 02 block and the red-first drill (the `BEGIN`/`BEGIN IMMEDIATE` and `instanceof Promise` steps both name real lines).
- `src/modules/feedback/service.ts` re-read at `41-48` (`expected`), `228-245` (`moderate`), `251-267` (`editPost`), `482` (pagination slice) and `493-498` (projection return) — the excerpts in 02 and 06 are verbatim with current line numbers.
- `src/modules/feedback/actions.ts:1-28` re-read against the new 01 block.
- `tests/workflow.test.ts:258-272` re-read against the new 04 block.
- `backups/2f14585fed41/src/server/json-store.ts` read in full; the quoted `updateJsonFile` is exact, and I verified the current `src/server/json-store.ts` really is only the tombstone before describing it as one.
- `docs/learning/build-journal.md` checked for the retired-file listing before linking it as "older notes".
