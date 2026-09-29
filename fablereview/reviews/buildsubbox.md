# ParcelPilot (buildsubbox) — Fable review

- **Path:** `_Organized Desktop/02 Build Projects/buildsubbox`  ·  **Wave:** 2  ·  **Stack:** Node 22 + Vite 8 + React 19 (browser-only, localStorage persistence; no server/SQL)  ·  **Batch:** B16
- **Astra's change (one line):** Replaced a fake "reserve" button (which subtracted a hard-coded 1842 units from every selected item) with a real domain layer — `src/model.js` validation/reducer, `src/repository.js` Web-Locks + baseline-compare commit, versioned CRUD for items/plans/subscribers, quote snapshots, request-key replay, subscriber-month uniqueness and a Reserved→Packed→Shipped→Delivered/Cancelled lifecycle.
- **Course size:** 4,843 words across 9 files  ·  **Tests claimed:** 54 (36 unit + 18 browser)  ·  **Tests found on disk:** 36 `test(` cases in `test/model.test.mjs` (495 lines); 18 browser scenarios enumerated in `astra-remaining-improvements/checks/parcelpilot/browser-verified/results.json`

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 4 | 4 | 5 | 5 | 4 | 5 | 4.6 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The bug the course claims existed really existed: `backups/6e0808cd55b2/src/App.jsx:502` has `stock: Math.max(0, item.stock - 1842)`, and `:144` the matching "1,842 active subscribers queued" copy. The narrative is not invented.
- The replacement is a genuine domain model, not a cosmetic edit: `src/model.js` (572 lines) has `validateItem/validatePlan/validateSubscriber/validateState`, `quoteBox`, `fingerprint`, `replay`, `reduce`; `src/repository.js` serializes writes through `navigator.locks.request(STORAGE_KEY, ...)` and refuses to commit when `current.raw !== base.raw`.
- Two distinct duplicate-protections are implemented *and* taught separately (transport retry via `requestKey`+`fingerprint` in `replay`, business duplicate via subscriber-month uniqueness) — 02-CONCEPTS.md "Two identities prevent different duplicates" and 07-TRACE-LAB Lab C ask the learner to write one sentence about each.
- VERIFICATION.md is unusually honest: an explicit "Simulation boundary" section naming no auth, no SQL, no payments, no carrier, and a "Persistence boundary" naming the 4 MiB / 1000-item caps. These match `deliveries/6e0808cd55b2.json` `limits` verbatim in substance.

## Problems found (evidence required)
- **[D4]** Everything persists in `localStorage` (`src/repository.js:2 STORAGE_KEY = "parcelpilot-workspace-v1"`). The transferable ideas (optimistic concurrency, idempotency keys, snapshot lines) are exactly right, but the learner never writes a SQL statement, an HTTP handler or an auth check — that is deferred to Practice Exercise 5. For a junior whose goal is server CRUD this is one layer short.
- **[D3]** The practice ladder is design-heavy: all five exercises are "future work, not claims that the features already exist" (05-PRACTICE.md:3). There is no small guided edit with a red test to make green first; the first rung (Exercise 1, subscriber notes) already spans "editor, model, seed, import contract, and receipt display".
- **[D7]** Prose is dense and assumes comfort with terms like *aggregate*, *candidate*, *fingerprint*, *baseline* on first use. 02-CONCEPTS.md defines the ideas but there is no glossary, and sentences like 03-WORKED-CHANGE.md:19 ("The entire candidate is validated and encoded before storage replacement") land hard on a first reader.

## Spot-checks performed
- Course claims the old code "subtracted a hard-coded 1,842 units" → read `backups/6e0808cd55b2/src/App.jsx:502` → **matches**.
- README says open `http://127.0.0.1:5181` and that `npm run dev` binds it → `package.json` `"dev": "vite --host 127.0.0.1 --port 5181 --strictPort"` → **matches** (and `--strictPort` backs the "refuses an occupied port" claim).
- VERIFICATION says "36 domain and repository tests produce `.verification/unit-results.json`" → `grep -c "test("` on `test/model.test.mjs` = 36; `scripts/test.mjs:5,13,17` writes `.verification/unit.log` and `.verification/unit-results.json` → **matches**.
- 03-WORKED-CHANGE says quote "Lines are sorted by identifier to make their canonical order deterministic" → `src/model.js:409` `.sort((a, b) => (a.itemId < b.itemId ? -1 : ...))` → **matches**.
- Delivery claims 54 tests / 7 screenshots → `checks/parcelpilot/results.json` reports `total: 54, unitTests: 36, browserScenarios: 18, screenshotsReviewed: 7`, with 18 named scenarios in `browser-verified/results.json` and 7 PNGs in `astraupskill/images/` → **matches, no overclaim**.

## Improvements needed (ordered, concrete, actionable)
1. Add a rung 0 to `05-PRACTICE.md`: a 20-minute guided change with a failing test supplied (e.g. "add `validateItem` rejection for a negative `retailCents`; here is the test to paste into `test/model.test.mjs`; run `npm test`, watch it fail, then fix `src/model.js`"). Keeps the predict→run→fix loop concrete before the design essays. (effort: S)
2. Add a 15-term glossary to `02-CONCEPTS.md` (aggregate, candidate, baseline, fingerprint, request key, revision, version, snapshot/line, reducer, Web Lock) with a one-line definition and the `src/model.js` symbol that embodies each. (effort: S)
3. Promote Exercise 5 ("Move acceptance to SQL and HTTP") into a companion chapter with a concrete target: an Express + SQLite `POST /reservations` with `Idempotency-Key`, a `UNIQUE(subscriberId, cycle)` constraint and an `UPDATE items SET stock = stock - 1 WHERE id = ? AND stock > 0` compare-and-set, mapped line by line onto the existing `reduce`/`replay`. That is the missing server layer for the target stack. (effort: M)
4. In `01-CODEBASE-MAP.md`, add line anchors (e.g. `src/model.js:381 quoteBox`) so references survive a reader skimming a 572-line file. (effort: S)

## One-paragraph summary for the index
ParcelPilot is one of the strongest courses in this batch and is worth doing in full. Astra took a good-looking React prototype whose "reserve" button subtracted a hard-coded 1842 units and replaced it with a real domain model: validation, versioned records, an accepted-quote snapshot, an idempotency key with a fingerprint check, subscriber-month uniqueness, and a shipment lifecycle where stock is restored exactly once. The course explains *why* each of those exists rather than just what the code does, and the trace lab makes you reconcile stock and versions by hand. The one gap is that persistence is `localStorage`, not a database — you learn the transaction and idempotency reasoning but write no SQL or HTTP, so pair it with a server-side course afterwards.
