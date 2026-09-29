# newcodexJS/04-notes-app — Fable review

- **Path:** `newcodexJS/04-notes-app`  ·  **Wave:** 1  ·  **Stack:** Node + Express + Knex + PostgreSQL (server, CommonJS) and React (Vite) client  ·  **Batch:** B02
- **Astra's change (one line):** Replaces the model's `whereRaw("CAST(notes AS TEXT) ILIKE ?")` whole-row string match with a parameterised English full-text search over title+body (`to_tsvector('english', ...) @@ plainto_tsquery('english', ?)`), adds `folder` filtering and a deterministic `created_at, id` ordering, rewrites the service layer into real bounded validation with proper partial-update semantics (`PUT` no longer wipes omitted fields), serializes `tags` to JSON at the database boundary, and moves the client from client-side `JSON.stringify(record).includes(...)` filtering to a debounced server query with a request-version guard that discards stale responses.
- **Course size:** 5,220 words across 9 files  ·  **Tests claimed:** 1  ·  **Tests found on disk:** 1 test block (`server/test/search.test.cjs`) containing ~16 assertions against real PostgreSQL over real HTTP

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 4.5 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The bug being fixed is the most instructive one in the whole batch and it is a *correctness* bug with a security flavour. `backups/19/server/src/models/model.js` searched `CAST(notes AS TEXT) ILIKE '%term%'` — the whole serialized row — so a query matched on ids, timestamps, folder names and status values, and user-supplied `%` and `_` acted as wildcards. The test pins both halves: a note whose *folder* is `HiddenKeyword` must not match a content search for `HiddenKeyword`, and `?search=%` must return zero rows rather than everything.
- Partial updates are now genuinely partial. `sanitizePayload(payload, true)` skips undefined keys, and the test asserts that `PUT {body: 'A revised explanation'}` returns status 200 with `title` still `'Running notes'` and then re-reads the row directly from Knex to confirm the stored body. The old code would have failed the required-field check or blanked the title.
- Stemming is demonstrated rather than asserted abstractly: searching `run` matches "Running notes" because `to_tsvector('english', ...)` stems both. That single assertion is what separates full-text search from `LIKE` in a junior's head.
- The stale-response guard is implemented the right way and verified end-to-end. `client/src/App.jsx` increments `requestVersion.current` and drops any response whose version is stale, and the cleanup in the `useEffect` bumps the version on unmount/re-run. `batch02/browser_checks.cjs:108-115` makes the `old` query hang for 1200 ms, types `new`, waits for the new result, waits another 1500 ms and asserts the "Old response" heading **never appears** — a real race, not a mocked one.
- Validation bounds are explicit and tested at the edges: ids are rejected above 2147483647 (the int4 ceiling), a `?search[]=bad` array query returns 400, and `{tags: [{}]}` is rejected before any write.

## Problems found (evidence required)
- **[D6/D3]** `VERIFICATION.md` reports "Automated test cases: 1", which matches `batch02/logs/19-tests.log` (`# tests 1 / # pass 1`) but badly understates the evidence: that single `test()` block carries roughly sixteen assertions across create, search, filter, partial update and four validation rejections. A reader comparing "1 test" here against "4 tests" in the bookmark-manager course will draw exactly the wrong conclusion about coverage. The count is technically honest and pedagogically misleading.
- **[D2]** No GIN index accompanies the new `to_tsvector` predicate, so every search is a sequential scan with a per-row `to_tsvector` computation. `ALL_20_PROJECTS_REPORT.md` does state this ("Ranking and a GIN index remain future scaling work"), so it is disclosed — but the course teaches the query without ever showing an `EXPLAIN`, which is the natural next lesson and the reason juniors ship slow search.
- **[D8]** **37%** of substantive words are unique to this project. `01-CODEBASE-MAP.md` carries the same generic Mermaid flowchart as all nine sibling courses, and `05-PRACTICE.md` exercises 1-6 are the shared bodies with one substituted prompt line each.
- **[D6]** The shared "Environment and limits" paragraph is accurate *here* (this project genuinely used PostgreSQL 18.1), but it is the same text pasted into six B02 courses that have no database at all, which devalues it as evidence.
- **[D5]** The client and server must be installed separately and the README says so, but neither `server/package.json` nor the client has a committed lockfile.

## Spot-checks performed
- Claim: excerpt "comes from server/src/models/model.js near line 4" -> `listRecords` body is at `model.js:4` and the fenced block is a verbatim substring -> **matches**.
- Claim (VERIFICATION): "A note whose folder is HiddenKeyword does not match that content query." -> `server/test/search.test.cjs` creates note `b` with folder `'HiddenKeyword'` and asserts `GET /api/notes?search=HiddenKeyword` returns zero rows -> **matches**.
- Claim (report): "Payloads and filters are bounded, tags serialize correctly to JSON, and partial edits retain omitted fields." -> `service.js` `sanitizePayload(payload, true)`, `model.js` `databasePayload()` JSON-stringifying `tags`, and the `changed.body.data.title === 'Running notes'` assertion after a body-only `PUT` -> **matches**.
- Claim (README): "Tests require ASTRA_TEST_DATABASE_URL pointing at a dedicated astra_test_* database" -> `server/test/database.cjs` is imported and `server/package.json` has `"test": "node --test test/*.test.cjs"`; the course's `VERIFICATION.md` includes a PowerShell block setting the variable -> **matches**.
- Claim (VERIFICATION): "Chromium interaction Passed" -> `browser_checks.cjs:108-115` implements the delayed-`old` / fast-`new` race and asserts the stale heading count is 0 -> **matches**.
- Claim: `checks.json` records a client build -> `19/build` (`vite build`) exit 0 -> **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Split `server/test/search.test.cjs` into four named `test()` blocks (search semantics, filter composition, partial update, validation rejections) so the reported count reflects the coverage, and update "Automated test cases" in `astraupskill/VERIFICATION.md` (effort: S).
2. Add a migration creating `CREATE INDEX ... USING GIN (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,'')))` and a short `EXPLAIN` walkthrough in `04-TESTING-AND-DEBUGGING.md` showing the seq-scan before and the index scan after (effort: M).
3. Replace the generic Mermaid diagram in `01-CODEBASE-MAP.md` with the actual request path (client debounce -> `routes` -> `controller` -> `service.list` validation -> `model.listRecords` -> `tsquery`) (effort: S).
4. Add one test for the `ORDER BY created_at DESC, id DESC` tie-break using two notes inserted in the same transaction — the determinism fix on `model.js:4` is currently untested (effort: S).
5. Make `05-PRACTICE.md` exercises 2 and 4 concrete: "add `ts_rank` ordering and prove it changes result order for a two-word query"; "add a second language configuration and show what happens to stemming" (effort: M).

## One-paragraph summary for the index
The best pure-CRUD-API course in this batch, and the one whose original bug is most worth seeing. The old search cast the entire row to text and ran `ILIKE '%term%'` on it, so a search matched ids, timestamps and folder names, and a user typing `%` got everything back; the fix is a parameterised `to_tsvector`/`plainto_tsquery` predicate over title and body only, and the test proves both the stemming (searching `run` finds "Running notes") and the leak that is now closed. You also get real partial-update semantics — a `PUT` carrying only a body no longer blanks the title, verified by re-reading the row from Knex — and a client-side race fix where a slow earlier response can no longer overwrite a newer one, verified in Chromium with a deliberately delayed request. Two caveats: the whole suite is packed into one `test()` block, so the reported "1 test case" makes it look far thinner than it is, and no GIN index was added, so the new search is a sequential scan. Needs PostgreSQL and an `astra_test_*` database; budget half a day.
