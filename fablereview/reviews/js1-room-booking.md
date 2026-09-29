# JS1/room-booking — Fable review

- **Path:** `JS1/room-booking`  ·  **Wave:** 1  ·  **Stack:** TypeScript + React (Vite) + Express + node-postgres, PostgreSQL with a `btree_gist` exclusion constraint  ·  **Batch:** B02
- **Astra's change (one line):** Adds real editing in the UI (the `PUT` route already existed but nothing called it) with an in-flight guard and a stale-response guard; converts `datetime-local` values to explicit ISO instants before sending; replaces the server's untyped `date` day filter with validated `dayStart`/`dayEnd` browser-local boundaries (keeping `?date=` as an explicitly-UTC legacy path); and introduces `server/src/validation.ts` — UUID, real-date, ISO-timestamp-with-offset and bounded-text parsers — wired into every route via an async `wrap` helper.
- **Course size:** 5,563 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 (`test/booking.test.ts`, ~18 assertions, against a real PostgreSQL schema over real HTTP)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 5 | 5 | 4 | 5 | 4 | 5 | 3 | 4 | 4.4 |

**Verdict:** KEEP    **Path role:** core

## What Astra did well
- The concurrency test is the real thing, not a simulation. `test/booking.test.ts` fires two identical `POST`s with `Promise.all` and asserts `[201, 409]` — i.e. it proves the GiST exclusion constraint, not the application code, is the arbiter. It then books the *adjacent* 11:00-12:00 slot and asserts 201, which is the half-open-interval lesson stated as an executable claim.
- The failed-update postcondition is checked against the database, not the response. After a `PUT` that would create an overlap returns 409, the test queries `SELECT ends_at FROM bookings` through a separate admin client and asserts the old value survived. That is the distinction between "the API said no" and "the data is unchanged" that the rubric asks for.
- The test harness is unusually responsible for a teaching repo: it refuses to run unless `ASTRA_TEST_DATABASE_URL` points at a database named `astra_test_*`, creates a uniquely-named schema, and strips `DROP TABLE` out of `schema.sql` before applying it, with the comment "Never run the scaffold's DROP TABLE statements against a fallback namespace." A junior who copies this pattern will not nuke their dev database.
- The timezone lesson is precise and testable. `validation.ts` `timestamp()` requires an explicit `Z` or `±HH:MM` offset and normalizes via `new Date(value).toISOString()`; the second test asserts `2030-03-10T03:00:00-07:00` becomes `2030-03-10T10:00:00.000Z`. The Chromium check (`browser_checks.cjs:98-102`) separately proves that renaming a booking round-trips its seconds and milliseconds unchanged.
- `02-CONCEPTS.md` is honest about what the demo is not: "bookedBy is a human label, not authentication: this demo does not enforce ownership." That limit is repeated in `ALL_20_PROJECTS_REPORT.md`.

## Problems found (evidence required)
- **[D7]** This is the hardest project in the batch and the course does not staircase into it. `02-CONCEPTS.md` opens with "Half-open intervals include their start and exclude their end… the database constraint is the final arbiter" and assumes the reader already has `tstzrange`, GiST exclusion constraints, `btree_gist`, DST-variable day lengths and stale-request versioning. A junior meeting exclusion constraints for the first time needs a prerequisite page that this course does not supply.
- **[D2]** The edit flow depends on `<input type="datetime-local" step="0.001">` round-tripping milliseconds. That works in Chromium (which is what `browser_checks.cjs` verified) but sub-second `datetime-local` support is not uniform across browsers; if a browser normalizes the value, an edit that only changes the title will silently shift the stored instant. The course never names this as a browser dependency.
- **[D2]** `POST /api/bookings` is still hand-wrapped in its own `try/catch` (`server/src/index.ts`) while every other route was converted to the `wrap` helper — an inconsistency left behind by the refactor.
- **[D5]** `package.json` devDependencies are all `"latest"` (`typescript`, `vite`, `tsx`, `@types/*`) with no `package-lock.json`, so `npm run typecheck` and `npm run build` are not reproducible over time. The database side of setup is, by contrast, documented properly.
- **[D8]** Better than most of the batch but still templated: **41%** of substantive words are unique to this project. `01-CODEBASE-MAP.md` carries the same generic Mermaid flowchart as all nine siblings, and `05-PRACTICE.md` exercises 1-6 are the shared bodies with one substituted prompt line each.
- **[D6]** Minor: `VERIFICATION.md` states "Automated test cases: 2" where those two blocks hold roughly eighteen assertions. Undercounting is the safer direction, but it makes the suite look thinner than it is.

## Spot-checks performed
- Claim: excerpt "comes from server/src/validation.ts near line 16" -> `timestamp()` is declared at `validation.ts:16` and the fenced block is a verbatim substring -> **matches**.
- Claim (VERIFICATION): "Two requests for one room from 10:00 to 11:00 UTC yield one 201 and one 409. An adjacent 11:00-to-12:00 slot succeeds. Extending the first to 11:30 fails and preserves its old end." -> all three are assertions in `test/booking.test.ts` -> **matches**.
- Claim (report): "Day views send browser-local boundaries; a legacy date query explicitly means a UTC day." -> `client/src/api.ts` builds `dayStart`/`dayEnd` from `new Date(\`${date}T00:00\`)` (local), while `server/src/index.ts` maps `?date=` to `${date}T00:00:00.000Z` -> **matches**.
- Claim (README/VERIFICATION): "Tests use a separate astra_test_* database and run with `npm test` at the root." -> `package.json` has `"test": "tsx --test test/*.test.ts"`, and `test/booking.test.ts:7-8` throws unless the database name matches `/^astra_test_[a-z0-9_]+$/` -> **matches**.
- Claim (VERIFICATION): typecheck and build were run -> `batch02/checks.json` records `18/typecheck` (`tsc --noEmit`, exit 0) and `18/build` (`vite build`, exit 0) -> **matches**.
- Claim: delivered bytes equal the manifest -> re-hashed all 171 B02 delivered files against `delivery-manifest.json`; 0 mismatches -> **matches**.

## Improvements needed (ordered, concrete, actionable)
1. Add a prerequisite page (`00-PREREQS.md`, linked from `astraupskill/README.md`) covering `tstzrange`, `EXCLUDE USING gist`, why `btree_gist` is needed for the `room_id =` operand, and what a 23-hour day is — with a 10-line psql session the learner can paste (effort: M).
2. Document the `datetime-local step="0.001"` browser dependency in `02-CONCEPTS.md` and add a fallback: send `startsAt`/`endsAt` from component state rather than re-reading the input on save, so a normalizing browser cannot shift the instant (effort: M).
3. Convert `POST /api/bookings` in `server/src/index.ts` to use the same `wrap` helper as every other route (effort: S).
4. Pin `typescript`, `vite`, `tsx` and the `@types/*` packages in `package.json` and commit a lockfile; record the versions in `astraupskill/VERIFICATION.md` (effort: S).
5. Replace the generic Mermaid diagram in `01-CODEBASE-MAP.md` with a timeline of the two concurrent POSTs through Express, the pool and the constraint — the single most valuable picture this project could carry (effort: M).

## One-paragraph summary for the index
The most valuable project in B02 and the one closest to real backend work. It is the only course here where a *database constraint*, not application code, is the thing that keeps data correct, and the test proves it by racing two identical bookings and asserting one 201 and one 409. You also get the half-open-interval rule (adjacent meetings may share a boundary), a failed-update test that checks the surviving row directly in SQL rather than trusting the error response, and a careful treatment of converting browser-local `datetime-local` values into explicit ISO instants. Be warned that it is the hardest course in the batch: it assumes you already know `tstzrange` and GiST exclusion constraints, and it needs a real PostgreSQL with `btree_gist` plus an `astra_test_*` database before `npm test` will run at all. Do the note-vault course first, then budget a full day for this one.
