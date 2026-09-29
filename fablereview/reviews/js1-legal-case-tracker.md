# Legal Case Tracker — Fable review

- **Path:** `JS1/legal-case-tracker`  ·  **Wave:** 1  ·  **Stack:** Node/Express + React (JSX, Vite), in-memory repository  ·  **Batch:** B06
- **Astra's change (one line):** Hardened the Express API — JSON-object body guard, runtime type/length/date validation, calendar-date checking (`2027-02-29` rejected), stable `id` tie-break in sort, page clamping to `totalPages`, and a genuinely idempotent `setStatus` that skips the write and the history row when the status is unchanged — plus `export const app` + conditional `listen` so tests can drive the real app over HTTP.
- **Course size:** 7,892 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/workflow.test.js`, helper `test/http.js`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 3 | 4 | 3 | 4 | 3 | 5 | 4 | 3 | 3.6 |

**Verdict:** IMPROVE    **Path role:** elective

## What Astra did well
- The change fixes a real latent bug, not a cosmetic one. In the backup, `setStatus` delegated to `update(id, {...existing, status})`, so *every* status call wrote an `"updated"` activity row and bumped `updatedAt`. The new `setStatus` (`server/server.js:~300`) compares `existing.status === status`, returns early, and otherwise writes a `"status"` entry naming the old and new value.
- Pagination is fixed at the right layer: `result.sort((a,b) => compareValues(...) || a.id.localeCompare(b.id))` plus `page = Math.min(page, totalPages)` inside `repository.query`, so totals stay truthful when a client asks for page 999.
- Tests assert *state*, not "a call happened": after two concurrent `PATCH .../status`, the suite asserts `entries.filter(x => x.kind === "status").length === 1`, and after six malformed PUTs it asserts `deepEqual` of the re-read record against the original.
- VERIFICATION.md is accurate. `batch04/logs/51-tests.log` shows `# tests 3 # pass 3 # fail 0`; `browser-checks.json` has a `{"project":"51","passed":true,"api":"actual isolated HTTP server","api_requests":6}` entry. All 19 manifest `after_sha256` values match the files on disk (I re-hashed all 234 files for stages 51–60: 0 mismatches).

## Problems found (evidence required)
- **[D1]** `astraupskill/02-CONCEPTS.md:9` claims "Amounts are bounded nonnegative currency values; a **fractional cent is rejected** rather than silently rounded." No such check exists. `server/server.js:146` is the only amount rule: `if (!Number.isFinite(input.amount) || input.amount < 0)`. `{"amount": 12.345}` is accepted and stored. The same sentence is copied into `03-WORKED-CHANGE.md` and `07-TRACE-LAB.md`, and into three sibling courses — it is template text that happens to be false here.
- **[D3/D1]** `07-TRACE-LAB.md` has six "Boundary" headings whose entire body is the **same paragraph six times**, and all six say "starting with [server/server.js](../server/server.js) and `createRepository`" — including Boundary 1 ("A React form, button or test sends a concrete operation") and Boundary 2 ("The client serializes editable values as an HTTP request"), which live in `client/src/App.jsx`. The lab does not actually trace anything.
- **[D3]** `06-SOLUTIONS-AND-REVIEW.md` repeats one identical **Review:** paragraph under all four exercises ("Demonstrate an ordinary case and a case that would break a naive implementation…"), so the "solutions" chapter gives no per-exercise review criteria.
- **[D5]** Every dependency in `package.json` is `"latest"` (pre-existing, but Astra added `test`/`build` scripts without pinning). VERIFICATION.md admits "Floating dependency declarations remain floating" — honest, but a junior on a fresh machine gets whatever npm resolves today, and there is no lockfile.
- **[D5/D6]** The documented commands were never the ones executed. `batch04/checks.json` for project 51 runs `node <implementation>/node_modules/vite/bin/vite.js build` and `node <implementation>/node_modules/tsx/dist/cli.mjs --test <stage>/51/test/workflow.test.js` from Astra's shared workspace. `npm install && npm test && npm run build` **inside this folder** was never run, and `"test": "node --test test/*.test.js"` relies on glob expansion that cmd.exe (npm's default Windows shell) does not perform.
- **[D8]** `04-TESTING-AND-DEBUGGING.md` discusses other projects: "Questboard uses Vitest and simulated browser storage; DevDeck uses Vitest with fake-indexeddb… Live Chat also tests a real WebSocket and PostgreSQL notification." None of that is in this repo.

## Spot-checks performed
- "The excerpt below comes from `server/server.js` near line 180" (`03-WORKED-CHANGE.md:19`) -> `grep -n "^function createRepository" server/server.js` returns **180** -> matches exactly.
- "Repeating a status leaves timestamps and history alone" (README Scope) -> read `setStatus`: early-returns `existing` unchanged when status matches, so `updatedAt` is untouched -> matches.
- "a fractional cent is rejected rather than silently rounded" (`02-CONCEPTS.md`) -> read `validateItem` + `normalizeItem`; only `Number.isFinite`/`>= 0` -> **does not match**.
- "Request page 999 after creating three matching rows with pageSize 2: the last page contains one row" -> `test/workflow.test.js` asserts `last.page === 2`, `last.items.length === 1`, and code has `page = Math.min(page, totalPages)` -> matches.
- VERIFICATION "Automated test cases: 3" -> `batch04/logs/51-tests.log`: `# tests 3 # pass 3` -> matches.

## Improvements needed (ordered, concrete, actionable)
1. Delete or make true the fractional-cent claim. Either strike the sentence from `astraupskill/02-CONCEPTS.md`, `03-WORKED-CHANGE.md` and `07-TRACE-LAB.md`, or add `if (Math.round(input.amount * 100) !== input.amount * 100) throw` to `validateItem` in `server/server.js` and a `{amount: 12.345} -> 400` case to `test/workflow.test.js`. (effort: S)
2. Rewrite `07-TRACE-LAB.md` boundaries 1–6 with the real per-boundary target: B1/B2 -> `client/src/App.jsx` submit handler and `client/src/api.js`; B3 -> `validateItem` (`server/server.js:105`); B4 -> `repository.update`/`setStatus`; B5 -> the array mutation in `createRepository`; B6 -> the JSON response. One sentence per boundary naming the actual function, not one paragraph repeated six times. (effort: M)
3. Give each exercise in `06-SOLUTIONS-AND-REVIEW.md` its own review criteria tied to the invariant it touches (e.g. for "status transition reason": "your test must show the reason is stored on the *status* activity only, and that a no-op repeat still writes nothing"). (effort: M)
4. Pin dependencies: replace `"latest"` in `package.json` with the versions recorded in `batch04/dependency-versions.json` and commit a lockfile, then update the Setup block in `astraupskill/README.md` to state the Node version actually used (22.16.0). (effort: S)
5. Make `npm test` work as documented on Windows: change the script to `node --test test/` (directory form, no shell glob) and add a line to VERIFICATION.md stating that the recorded evidence came from the isolated stage copy, not from `npm test` in this folder. (effort: S)
6. Replace the cross-project paragraph in `04-TESTING-AND-DEBUGGING.md` with a description of *this* harness (`test/http.js` boots the exported `app` on port 0 and closes it). (effort: S)

## One-paragraph summary for the index
A small Express + React case tracker where Astra fixed three genuine CRUD defects: a status endpoint that logged a history entry even when nothing changed, a pagination path that let `page=999` return an empty page with misleading totals, and request bodies that reached string/number operations untyped. The three regression tests are honest — they re-read the stored record after every rejected edit and count history rows after a repeated status command — and every verification claim matches the batch logs and file hashes. The weak part is the course furniture: the trace lab repeats one paragraph six times and points every "boundary" at the same server function, and the concepts chapter asserts a fractional-cent rule that this code does not implement. Worth doing if you want a fast, dependency-light introduction to validation/idempotency/pagination, but do it after `warehouse-ledger` and read the server source rather than the trace lab.
