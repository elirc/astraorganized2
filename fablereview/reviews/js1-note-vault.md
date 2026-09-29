# JS1/note-vault — Fable review

- **Path:** `JS1/note-vault`  ·  **Wave:** 1  ·  **Stack:** Node 22 + Express 4 (ESM) + React (Vite) + JSON-file persistence  ·  **Batch:** B02
- **Astra's change (one line):** Extracts the inline JSON-file repository into `server/repository.js`, serializes every read-modify-write through a single promise queue, replaces whole-file `writeFile` with write-to-unique-temp + `rename` (with cleanup), validates and bounds request bodies/search, wraps every route so async failures reach one error handler, makes the app exportable/testable via `createApp(file)`, and fixes the client (React was never mounted — `index.html` loaded `App.jsx`, which only exports a component; a new `main.jsx` now calls `createRoot`).
- **Course size:** 5,385 words across 9 files  ·  **Tests claimed:** 3  ·  **Tests found on disk:** 3 (`test/persistence.test.js`, ~15 assertions)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 4 | 5 | 3 | 5 | 4 | 3 | 4.3 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- This is a real bug fix, not a demo. Before the change the client literally did not mount: `backups/14/client/index.html` pointed `<script type="module" src="/src/App.jsx">` at a file whose only export is `export default function App()` — nothing ever called `createRoot`. The fix adds `client/src/main.jsx` and repoints the script tag. A learner can reproduce the blank page from the backup.
- The concurrency fix is correct and worth studying. `server/repository.js` keeps a `tail` promise and wraps *every* exported method in `serial(...)` at the bottom of the factory, so the whole read-modify-write is inside the critical section rather than just the write. The test proves it: 12 concurrent `repo.create` calls yield 12 distinct ids and a *re-opened* repository reads 13 records — a lost-update bug would show 2.
- The atomic-write test is the best failure test in the batch. `test/persistence.test.js` injects a fake `io` whose `rename` throws once, asserts the file bytes are **byte-identical** to before, asserts the queue then recovers on retry, and finally writes `{bad` into the file and asserts the repository *refuses to reseed over corrupt data* (`await assert.rejects(createNoteRepository(file))` plus the bytes still being `{bad`). That last assertion targets exactly the destructive-recovery mistake juniors make.
- Verification is honest and specific. `VERIFICATION.md` describes the same fixture the test uses, and `astrdocs/ALL_20_PROJECTS_REPORT.md` explicitly states the boundary: "It does not provide multi-process locking or guaranteed power-loss durability." That limit is true of the code as written (the queue is per-instance, per-process) and is stated rather than hidden.

## Problems found (evidence required)
- **[D5]** Every dependency is `"latest"`: `package.json` lists `"vite": "latest"`, `"react": "latest"`, `"react-dom": "latest"`, `"express": "latest"`, `"@vitejs/plugin-react": "latest"`, and there is **no `package-lock.json`**. A junior running `npm install` months from now can get a React or Vite major that breaks the `npm run build` the course tells them to run. Astra added the `build` script but did not pin what it builds.
- **[D8]** Even the best course in this batch is only **41%** project-specific by substantive word count (measured across the 10 B02 courses). `01-CODEBASE-MAP.md` carries the same generic Mermaid diagram as all nine siblings, and `05-PRACTICE.md` exercises 1-6 are the shared template with one substituted prompt line each.
- **[D6]** `VERIFICATION.md` includes the batch-wide sentence "PostgreSQL tests used a separate local PostgreSQL 18.1 instance on port 55439 and uniquely named schemas in a dedicated test database." This project stores JSON on disk; no PostgreSQL check exists for project 14 in `batch02/checks.json`.
- **[D3]** The course does not walk the learner through the failure they can most easily reproduce — the pre-change blank page. `03-WORKED-CHANGE.md` excerpts `repository.js:6`, but the `main.jsx` mounting fix (the thing that makes the app run at all) gets one clause in the scope line.
- **[D7]** Promise-queue serialization and temp-file-plus-rename are genuinely mid-level topics. `02-CONCEPTS.md` explains them, but a junior who has not written async JS before will need the trace lab twice.

## Spot-checks performed
- Claim: excerpt "comes from server/repository.js near line 6" -> `createNoteRepository` is declared at `repository.js:6` and the fenced block is a verbatim substring of the file -> **matches**.
- Claim (VERIFICATION): "twelve concurrent creates leave thirteen records" -> `test/persistence.test.js` first test builds `Array.from({length:12}, ...)` then asserts `restarted.list({search:''})` has length 13 -> **matches**.
- Claim (report): "Writes use a unique sibling file and rename after writing succeeds." -> `repository.js` `writeAll` builds a temp name from `crypto.randomUUID()`, writes with `{ flag: "wx" }`, then renames -> **matches**.
- Claim (README): "the API defaults to port 4106. Run one port-4106 project at a time." -> `server/server.js` uses `Number(process.env.PORT || 4106)`, and `newcodexJS/06-bookmark-manager/client/src/services/api.ts` also defaults to `http://localhost:4106/api` -> **matches, and the warning is a genuinely useful catch**.
- Claim (VERIFICATION): "Automated test cases: 3" -> `batch02/logs/14-tests.log` shows `# tests 3 / # pass 3`; `checks.json` also records a passing `vite build` for project 14 -> **matches**.
- Claim: delivered bytes equal the manifest -> I re-hashed all 171 B02 delivered files against `delivery-manifest.json`; 0 mismatches -> **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Pin the toolchain: replace the seven `"latest"` entries in `package.json` with the exact versions the harness used and commit a `package-lock.json`; state the versions in `astraupskill/VERIFICATION.md` (effort: S).
2. Add a "reproduce the blank page" section to `03-WORKED-CHANGE.md`: revert `client/index.html` to point at `App.jsx`, load the page, read the empty console, then restore — the cheapest concrete lesson in the repo (effort: S).
3. Remove the PostgreSQL boilerplate sentence from `astraupskill/VERIFICATION.md` (effort: S).
4. Add a fourth test for `PUT /api/notes/:id` returning 404 on an unknown id and for the 128 kB `express.json` limit rejecting an oversized body — both are delivered behaviors with no coverage (effort: S).
5. In `05-PRACTICE.md`, make exercises 3 and 4 concrete to this repository: "make `writeFile` fail *after* the temp file exists but before `rename`, and prove no `.tmp` file is left behind"; "add a second process writing the same file and show the queue does not help" (effort: M).

## One-paragraph summary for the index
The strongest browser-plus-server exercise in B02 and a good early stop in the main sequence. It covers three things you will hit on any Node CRUD job: serializing read-modify-write so concurrent requests do not clobber each other, replacing a whole-file overwrite with write-temp-then-rename so a crash cannot truncate your data, and making an Express app exportable so you can test it over real HTTP without a running server. The tests are the best in this batch — one injects a failing `rename` and asserts the old bytes survive byte-for-byte, then asserts the app refuses to reseed over a corrupted file. Two caveats: every dependency is `"latest"` with no lockfile, so `npm install` is a gamble, and about 60% of the nine course files are template shared with nine sibling projects. Budget three to four hours and read `server/repository.js` next to `test/persistence.test.js`.
