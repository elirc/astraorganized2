# Property Rentals — Fable review

- **Path:** `JS1/property-rentals`  ·  **Wave:** 1  ·  **Stack:** JavaScript + Express (in-memory repository) + React/JSX/Vite  ·  **Batch:** B05
- **Astra's change (one line):** Added an object-shape guard for POST/PUT/PATCH bodies plus full type/length/date/priority validation at the Express boundary; made `repository.setStatus` repeat-safe (returns the existing record with no new history row when the status is unchanged) and made it write the record and its history entry together; clamped out-of-range page numbers after counting and added an `id` tie-breaker to sorting; exported `app` and guarded `app.listen` so tests can bind an ephemeral port; and created `client/src/main.jsx` plus repointed `client/index.html` at it so the React client actually mounts.
- **Course size:** 7306 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3, `test/workflow.test.js` (helper `test/http.js`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 3 | 4 | 3 | 4 | 5 | 5 | 4 | 2 | 3.8 |

**Verdict:** IMPROVE    **Path role:** reference

## What Astra did well
- It fixed a client that could not have worked. The backup `client/index.html` loaded `<script type="module" src="/src/App.jsx">`, and `App.jsx` only exports a component — nothing calls `createRoot`. Astra added `client/src/main.jsx` (`createRoot(document.getElementById("root")).render(<App />)`) and repointed `index.html` at it. That is the most consequential change in the project.
- The validation added to `server/server.js` is boundary validation done properly: an Express middleware rejects non-object JSON bodies on POST/PUT/PATCH, and the record validator checks types, a 200-character cap on `title`/`owner`, a real-calendar-date check (`2027-02-29` is rejected), the priority vocabulary and a 10000-character note cap — replacing the old `String(req.body.status || "")` coercion that turned any garbage into a string.
- `repository.setStatus` is now repeat-safe and writes state and history together: `if (existing.status === status) return existing;` then one synchronous update plus `activity.unshift(entry)`. The history text changed from `"Changed status to X"` to `"Changed status from A to B"`, which is what an audit trail should record.
- Tests observe behaviour, not calls. `test/workflow.test.js` loops six malformed PUT bodies and asserts 400 for each **and** `deepEqual`s the stored record afterwards; it asserts `page=999` clamps to page 2 with `total` still 3; and it fires two concurrent PATCHes and asserts exactly one `kind==='status'` entry.
- Reproducibility is genuinely easy: `npm install`, `npm run dev`, `npm test`, `npm run build` — no database, no external service. `logs/46-tests.log` shows `# tests 3 # pass 3 # fail 0`, and all 19 delivered files hash-match `delivery-manifest.json`.

## Problems found (evidence required)
- **[D1/D3]** The "Actual implementation excerpt" in `astraupskill/03-WORKED-CHANGE.md` does not show the implementation. It is a four-line tail of the handler — `const item = repository.setStatus(req.params.id, status);` / the 404 guard / `res.json(item);` / `});` — and those three statements are **unchanged** from the backup. The actual improvement, the `setStatus` equality guard and the paired history write, lives in the repository further down `server/server.js` and is never shown. The chapter's entire purpose is to show the worked change, and it shows code that was not changed.
- **[D1]** The client-mount fix is undocumented. `client/src/main.jsx` and `client/index.html` are both in the stage 46 `delivery-manifest.json`, but the Before/After paragraph in 03 never mentions them; `main.jsx` appears only as a bullet under "Source navigation" in `astraupskill/01-CODEBASE-MAP.md`. The most interesting change in the project is invisible to the learner.
- **[D8]** Severe cross-project templating. `astraupskill/02-CONCEPTS.md` is 45 lines and differs from the sibling course in `JS1/project-risks` in only 3 of them; `04-TESTING-AND-DEBUGGING.md` differs in 1 line; README in 2. Nouns are swapped and nothing else.
- **[D8/D1]** `astraupskill/04-TESTING-AND-DEBUGGING.md` carries a paragraph about other apps: *"For Poll Studio and Kanban Flow, jsdom runs the actual app.js against its HTML and fresh browser storage..."* — byte-identical across all 30 `JS1/*/astraupskill/04-TESTING-AND-DEBUGGING.md` files, and irrelevant here.
- **[D3]** All four exercises in `astraupskill/06-SOLUTIONS-AND-REVIEW.md` close with the identical "Review:" sentence (*"Demonstrate an ordinary case and a case that would break a naive implementation..."*), so the review criteria carry no per-exercise information.
- **[D4]** The lesson stops short of persistence. The repository is a module-level array; the course says so honestly (*"A server restart discards new records and history"*), but a junior gets no SQL, no transaction and no durability practice here, while 02-CONCEPTS still discusses transaction boundaries this project does not have.
- **[D7]** Heavy self-repetition: the fixture paragraph beginning *"Create \"One-bedroom courtyard unit\" ..."* appears in 01, 03, 04, 05, 06, 07 and VERIFICATION.

## Spot-checks performed
- Course says the excerpt "comes from `server/server.js` near line 37" -> line 37 of `JS1/property-rentals/server/server.js` is indeed `const item = repository.setStatus(req.params.id, status);`, but the handler begins at line 34 and the excerpt omits lines 34-36 (the status-vocabulary check) -> **line number matches, excerpt is misleadingly truncated**.
- 01-CODEBASE-MAP.md claims *"Statuses are Available, Application, Occupied, Maintenance."* -> `server/server.js` line 7 declares `const STATUSES = [Available, Application, Occupied, Maintenance]` in the same order -> **matches**.
- 07-TRACE-LAB.md drives `http://localhost:4226/api/units` -> `server/server.js` line 6 is `const port = Number(process.env.PORT || 4226)` and the routes are mounted at `/api/units` -> **matches**.
- VERIFICATION.md lists build / tests / Chromium and correctly **omits** typecheck (this project has no TypeScript), claiming 3 test cases -> `batch03/checks.json` has only `build` and `tests` rows for project 46, both `exit_code: 0`; `logs/46-tests.log` shows `# pass 3 # fail 0`; `browser-checks.json` records `"persistence": "fresh in-memory repository"` and both screenshots exist -> **matches, and the honest omission of typecheck counts in its favour**.
- README claims *"The shared toolbar now uses two flexible columns"* -> `client/src/styles.css` `.toolbar` is now `grid-template-columns: repeat(2, minmax(0, 1fr))` against the backup's `1fr 160px 160px 160px` -> **matches**.
- All 19 manifest `after_sha256` values for stage 46 re-hashed against disk -> **all match**.

## Improvements needed (ordered, concrete, actionable)
1. Replace the excerpt in `astraupskill/03-WORKED-CHANGE.md` with the actual changed code: the whole `app.patch("/api/units/:id/status")` handler **and** the `setStatus(id, status)` body from the repository in `server/server.js`, so the equality guard and the paired history write are on the page. (effort: S)
2. Add a "What else changed" section to 03 covering `client/src/main.jsx` and `client/index.html`: explain that a Vite entry module must call `createRoot(...).render(<App />)` and that pointing `index.html` at a component file yields a blank page with no console error. That is a high-value debugging lesson a junior will hit for real. (effort: S)
3. Delete the "Poll Studio and Kanban Flow" paragraph from 04 and describe only `test/http.js` and the ephemeral-port fixture. (effort: S)
4. De-duplicate: keep the fixture paragraph in 03 and link to it from the other six files; keep one copy of the setup block. (effort: S)
5. Add a break/observe/fix lab to 04: have the learner delete `if (existing.status === status) return existing;` from `server/server.js`, re-run `npm test`, and identify exactly which assertion fails and why. (effort: M)
6. Turn the persistence limitation into a scoped exercise instead of a disclaimer: swap the in-memory repository for a JSON-file or SQLite repository behind the same interface, and ask which existing assertions must still pass. That is the missing CRUD content here. (effort: L)

## One-paragraph summary for the index
A small Express plus React CRUD app whose useful lesson is boundary validation and repeat-safe status changes: the API now rejects malformed bodies and impossible calendar dates instead of coercing them, a repeated status request produces no duplicate audit entry, and out-of-range pages clamp after a real count. Astra also quietly repaired a client that never mounted (`index.html` pointed at `App.jsx` with no `createRoot`), which is the best debugging story in the project — but the course never mentions it, and the worked-change chapter excerpts three lines that were not changed. Setup is trivially reproducible: `npm install`, `npm test`, no database. Because everything lives in a module-level array you get no SQL, transaction or durability practice. Read it for validation and idempotency, then use a TypeScript/PostgreSQL sibling such as `JS1/learning-paths` for the persistence half.
