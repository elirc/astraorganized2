# Field Service — Fable review

- **Path:** `JS1/field-service`  ·  **Wave:** 1  ·  **Stack:** Node/Express + TypeScript + PostgreSQL (`pg`) + React/Vite  ·  **Batch:** B06
- **Astra's change (one line):** Identical treatment to `JS1/subscription-billing` applied to the `/api/visits` resource — list endpoint reads count+page inside one `REPEATABLE READ READ ONLY` transaction with an `id ASC` tie-break and clamped page, `PATCH /:id/status` takes `SELECT … FOR UPDATE` and no-ops (no audit row, no `updated_at` bump) when the status is unchanged, every route wrapped in `asyncRoute`, UUID `app.param` guard, full runtime body validation, `pg.types.setTypeParser(1082, v => v)` to stop DATE drift, and the `"dueDate"` seed-column fix in `server/db/schema.sql`.
- **Course size:** 8,396 words across 9 files  ·  **Tests claimed:** 4  ·  **Tests found on disk:** 4 (`test/workflow.test.ts`, harness `test/database.ts`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 3 | 5 | 3 | 5 | 4 | 5 | 4 | 2 | 3.9 |

**Verdict:** IMPROVE    **Path role:** skip

## What Astra did well
- The underlying code change is strong and identical in quality to subscription-billing: `withTransaction` + `SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY` for the list, `ORDER BY ${sort} ${direction}, id ASC`, `const page = Math.min(filters.page, totalPages)`, and `SELECT * FROM items WHERE id=$1 FOR UPDATE` before the status comparison.
- Route-level crash-proofing: an `asyncRoute` wrapper (`Promise.resolve(handler(...)).catch(next)`) now feeds every async route into the error middleware. Before the change a rejected promise inside `app.get("/api/visits", async …)` left the request hanging.
- `GET /:id/activity` and `POST /:id/activity` now check that the parent row exists and return 404 rather than an empty list / orphan insert, and activity ordering gained an `id ASC` tie-break.
- The domain vocabulary in the course is correct for *this* project: `01-CODEBASE-MAP.md:11` lists "Statuses are Requested, Scheduled, On Site, Complete, Cancelled. Categories are Install, Repair, Inspection, Training", which matches `server/src/index.ts:15-16` exactly.
- Verification is honest: `logs/53-tests.log` = `# tests 4 # pass 4 # fail 0`; build, typecheck and browser entries all present in the batch evidence; all 20 manifest `after_sha256` values match disk.

## Problems found (evidence required)
- **[D8]** This course is a mechanical clone. Against `JS1/research-studies`: `02-CONCEPTS.md` differs by **2 of 45 lines**, `05-PRACTICE.md` by **1 of 47**, `04-TESTING-AND-DEBUGGING.md` by **1 of 69**, `README.md` by **2 of 67**, `07-TRACE-LAB.md` by **4 of 114**. `test/workflow.test.ts` has the same four test names and the same assertions as both siblings. Nothing here teaches anything a learner would not have learned from subscription-billing.
- **[D1]** `02-CONCEPTS.md:9` claims "a **fractional cent is rejected** rather than silently rounded". There is no such check — `server/src/index.ts` `parseItem` only tests `!Number.isFinite(item.amount) || item.amount < 0 || item.amount > 9999999999.99`. The sentence continues "This scaffold does not perform external billing, legal work, **dispatch integration** or research compliance checks", which is the tell: one paragraph was written to cover four different projects at once.
- **[D3/D1]** `07-TRACE-LAB.md` has six "Boundary" sections with the **same paragraph repeated six times**, every one pointing at `server/src/index.ts` and `parseItem` — including boundaries 1 and 2, which describe the React client in `client/src/App.tsx`.
- **[D3]** `06-SOLUTIONS-AND-REVIEW.md` gives the same **Review:** paragraph for all four exercises.
- **[D8]** `04-TESTING-AND-DEBUGGING.md` still talks about other apps: "Questboard uses Vitest and simulated browser storage; DevDeck uses Vitest with fake-indexeddb… Live Chat also tests a real WebSocket and PostgreSQL notification."
- **[D5]** All dependencies are `"latest"` with no lockfile. `checks.json` shows the verified commands ran from Astra's shared `implementation/node_modules` against `stage/53`, so the documented `npm install && npm test` in this folder is unverified.
- **[D2, minor]** `test/workflow.test.ts` is a `.ts` file written as untyped JS (`let h;`), so `npm run typecheck` does not meaningfully cover it.

## Spot-checks performed
- "The excerpt below comes from `server/src/index.ts` near line 326" (`03-WORKED-CHANGE.md:19`) -> `grep -n "^function parseItem" server/src/index.ts` returns **326** -> matches exactly.
- "Statuses are Requested, Scheduled, On Site, Complete, Cancelled" -> `server/src/index.ts:15` `const STATUSES = ["Requested", "Scheduled", "On Site", "Complete", "Cancelled"];` -> matches.
- "a fractional cent is rejected rather than silently rounded" -> read `parseItem` amount branch -> **does not match**.
- "Every write locks the row before comparing the status" (worked change) -> `SELECT * FROM items WHERE id=$1 FOR UPDATE` then `if (current.rows[0].status === status) return current.rows[0];` -> matches.
- VERIFICATION "Automated test cases: 4" -> `batch04/logs/53-tests.log`: `# tests 4 # pass 4 # fail 0` -> matches.
- Template check: `diff JS1/field-service/astraupskill/02-CONCEPTS.md JS1/research-studies/astraupskill/02-CONCEPTS.md` -> 2 differing lines out of 45 -> confirms duplication.

## Improvements needed (ordered, concrete, actionable)
1. Drop this course from the learning path (keep `subscription-billing` as the representative of the trio), or repurpose it around a lesson the siblings do not cover. The obvious field-service-specific one: scheduling-window validation and double-booking a technician — add a `technician_id` + `scheduled_for` unique/exclusion constraint in `server/db/schema.sql`, enforce it in `parseItem`, and test two concurrent bookings of the same slot. That would make it a real second lesson instead of a re-read. (effort: L)
2. If it stays as-is, delete the fractional-cent sentence from `02-CONCEPTS.md`, `03-WORKED-CHANGE.md` and `07-TRACE-LAB.md` — this project has no money semantics worth the claim (its `amount` is a visit cost with no cent rule). (effort: S)
3. Rewrite `07-TRACE-LAB.md` boundaries 1–6 with real per-boundary targets (`client/src/App.tsx` submit -> `fetch` -> `app.param`/`parseItem` -> `withTransaction` -> `COMMIT` -> JSON mapper), deleting the five duplicate paragraphs. (effort: M)
4. Give per-exercise review criteria in `06-SOLUTIONS-AND-REVIEW.md` instead of one repeated paragraph. (effort: M)
5. Type `test/workflow.test.ts` (`let h: Awaited<ReturnType<typeof database>>`, typed `call` parameters) so `npm run typecheck` covers the suite. (effort: S)
6. Pin `package.json` versions from `batch04/dependency-versions.json` and commit a lockfile. (effort: S)

## One-paragraph summary for the index
Technically this is a good PostgreSQL CRUD hardening exercise — consistent count/page inside one `REPEATABLE READ` transaction, a `FOR UPDATE` idempotent status endpoint, an `asyncRoute` wrapper that stops rejected promises from hanging requests, and four tests including one that injects a failing trigger to prove rollback. The problem is that it is the same lesson, the same prose and the same four tests as `JS1/subscription-billing` and `JS1/research-studies`, with only the domain nouns changed (the concepts chapter differs from its sibling by two lines out of forty-five). The course also carries a false claim that fractional cents are rejected, and a trace lab that repeats one paragraph six times while pointing every boundary at the same server function. Skip it unless you specifically want a second rep; if you do want the rep, do it from the source and tests rather than the prose.
