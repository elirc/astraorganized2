# JS1/snippet-vault — Fable review

- **Path:** `JS1/snippet-vault`  ·  **Wave:** 1  ·  **Stack:** vanilla ES modules (store/dom/main split), localStorage, served over HTTP; node:test with a hand-rolled `localStorage` stub  ·  **Batch:** B02
- **Astra's change (one line):** Moves the store to write-then-publish (`commit(next)` sets `snippets` only after `localStorage.setItem` returns), makes `saveSnippet` throw on blank title/code and on an edit id that no longer exists, deduplicates tags case-insensitively while preserving the first-seen casing, catches those throws in `main.js` so the UI shows a message instead of half-updating, and makes `copyToClipboard` resolve `false` on a permission rejection instead of producing an unhandled rejection.
- **Course size:** 4,843 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 (`test/store.test.js`, ~12 assertions)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 3 | 3 | 3 | 4 | 4 | 4 | 3 | 3.6 |

**Verdict:** IMPROVE    **Path role:** elective

## What Astra did well
- The test fixture is clever and worth stealing: `test/store.test.js` imports the module with a cache-busting query (`await import(\`../src/store.js?case=${randomUUID()}\`)`) so each test gets a fresh module-level `snippets` array. That is the correct way to test a module that owns mutable state, and most juniors reach for a mock framework instead.
- Both the store-level and DOM-level halves of the failure path are covered. The first test throws from `setItem`, asserts `store.getSnippet(id).title` is still `'Test'` (in-memory not published) **and** that the serialized bytes are identical to before, for both a failed save and a failed delete.
- The clipboard fix is the kind of detail juniors miss: `navigator.clipboard.writeText` rejects when permission is denied, and the original `dom.js` awaited it bare, so a denied copy produced an unhandled rejection and the UI still said nothing. The test asserts `copyToClipboard` returns `false` on rejection and `true` plus the copied text on success.
- Tag normalization is tested with a fixture that exercises whitespace, case and empty entries in one string: `' Utility,utility, EVENTS, ,events '` -> `['Utility','EVENTS']`.

## Problems found (evidence required)
- **[D2] Encoding regression introduced by the delivery.** `src/store.js:1` now reads `// store.js â€” owns the data and every mutation. No DOM access lives here.` The backup at `batch02/backups/17/src/store.js:1` has the correct em dash. The UTF-8 bytes were read as cp1252 and re-encoded during the edit. I scanned all ten B02 projects for this pattern and **this is the only file affected**, so it is a one-off slip rather than a systemic problem — but it is a visible defect in the exact file the course tells the learner to open first, and it shipped with a verified `after_sha256`, which means the hash check confirmed the corruption rather than catching it.
- **[D2]** `main.js` catches the store's throws with bare `catch { ... }` (`main.js:44`, `main.js:73`) and replaces every error with one fixed message. A blank-title error and a "this snippet no longer exists" error are indistinguishable to the user, even though `store.js` raises two different, already-user-readable messages. The course's own `02-CONCEPTS.md` argues that feedback must identify the failure; the delivered UI does the opposite.
- **[D8]** Only **37%** of substantive words are unique to this project; `05-PRACTICE.md` and `04-TESTING-AND-DEBUGGING.md` are the shared batch template with one substituted prompt line per exercise.
- **[D6]** `VERIFICATION.md` carries the batch-wide "PostgreSQL tests used a separate local PostgreSQL 18.1 instance on port 55439" sentence; `batch02/checks.json` records only `node --test .../17/test/store.test.js` for this project.
- **[D4]** No HTTP, SQL, ownership or transactions. The module-boundary and write-then-publish lessons transfer; nothing else does.
- **[D5]** The README tells the learner to serve with `python -m http.server 8000`, i.e. a Python dependency in a JavaScript course. The project's own root README offers `npx serve` first; the course picked the other one. Also no `package-lock.json` (though this project has no dependencies, so the risk is low).

## Spot-checks performed
- Claim: excerpt "comes from src/store.js near line 59" -> `saveSnippet`'s body is at `store.js:59` and the fenced block is a verbatim substring -> **matches**.
- Claim (VERIFICATION): "Tags Utility,utility, EVENTS,events become Utility and EVENTS." -> `test/store.test.js` first test, `assert.deepEqual(first.tags, ['Utility','EVENTS'])` -> **matches**.
- Claim (report): "clipboard denial returns false so the UI can explain failure" -> `src/dom.js:57-65` now wraps the await in try/catch returning `false` -> **matches in `dom.js`, but `main.js` discards the distinction for store errors**.
- Claim (VERIFICATION): "Automated test cases: 2" -> `batch02/logs/17-tests.log` `# tests 2 / # pass 2` -> **matches**.
- Claim (VERIFICATION): "Chromium interaction Passed" -> `browser_checks.cjs:85-91` denies clipboard access via `addInitScript`, creates a snippet with duplicate tags, asserts two `.tag` elements, clicks Copy and waits for "Clipboard not available", then reloads -> **matches**.
- Claim: `src/store.js` is clean source a learner can read -> line 1 contains mojibake -> **does not match**.

## Improvements needed (ordered, concrete, actionable)
1. Fix the encoding of `src/store.js:1` — restore the em dash and re-save the file as UTF-8 (effort: S). Worth also adding a UTF-8 assertion to whatever tool applied the edit, since the delivery hash check confirmed the corrupted bytes.
2. Change the two bare `catch {}` blocks in `src/main.js` (lines 44 and 73) to `catch (error) { showMessage(error.message); }` so the store's two distinct messages reach the user, and add a test asserting the "no longer exists" message surfaces (effort: S).
3. Remove the PostgreSQL sentence from `astraupskill/VERIFICATION.md` (effort: S).
4. Change the README/VERIFICATION serve command to `npx serve .` to match the project's own root README and drop the Python dependency (effort: S).
5. Make `05-PRACTICE.md` exercises 3 and 4 concrete: "make the write fail only on the *second* save and prove the first snippet survives a reload"; "add a tag-rename operation and decide whether it should be case-preserving" (effort: M).

## One-paragraph summary for the index
A good small lesson on module boundaries and on publishing state only after persistence succeeds, with an unusually clever test fixture — it re-imports the module under a random query string so each test gets fresh module state, which is exactly how you test a module that owns a mutable array. The store change is right and the clipboard fix catches a real unhandled-rejection bug. Two things stop it being a clean keep: `src/store.js` line 1 was corrupted into mojibake during delivery (the only such file in the batch), and `main.js` swallows the store's two distinct, already user-readable error messages behind one generic string, which contradicts what the course itself teaches about feedback. Read it in an hour for the write-then-publish pattern; fix the two defects before handing it to anyone.
