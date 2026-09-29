# JS1/event-admin — Fable review

- **Path:** `JS1/event-admin`  ·  **Wave:** 1  ·  **Stack:** Node/Express (in-memory array) + React 18 (Vite, JSX)  ·  **Batch:** B03
- **Astra's change (one line):** `validateEvent` now rejects the request before normalization unless name/location are bounded strings, `date` is a *real* calendar day (regex + round-trip through `Date.toISOString().slice(0,10)`, so 2027-02-29 and 2028-04-31 fail) and capacity/registered are safe whole integers; plus a JSON-object body guard, a testable `export const app` with a `pathToFileURL` listen guard, and the missing React entry point `client/src/main.jsx`.
- **Course size:** 5,629 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 in `test/api.test.js` (+ `test/http.js`)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 4 | 4 | 3 | 5 | 4 | 4 | 4 | 2 | 3.8 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- `realDate` (`server/server.js:94`) is the genuinely instructive part of this batch. `Date.parse("2027-02-29T00:00:00Z")` does not throw — JS silently rolls over — so the helper round-trips the parsed date back to `YYYY-MM-DD` and compares strings. That is exactly the trick a junior gets wrong, and the course's chosen fixture (2028-02-29 valid, 2027-02-29 invalid) makes the leap-year rule concrete.
- The type gate runs *before* `normalizeEvent`, which is the right order: `normalizeEvent` coerces with `String(...)` and `Number(...)`, so validating after normalization would have turned `capacity: "bad"` into `NaN` and lost the reason.
- The body guard at `server/server.js:21-25` rejects arrays and non-objects on POST/PUT/PATCH before any handler sees them — a real defence, since `express.json()` happily accepts a top-level array.
- Same real mount fix as its siblings: `backups/24/client/index.html` pointed at `/src/App.jsx`, which has no `createRoot`; `client/src/main.jsx` is new and `index.html` now loads it.
- Tests are behavioural and use a real HTTP round trip on an ephemeral port.

## Problems found (evidence required)
- **[D8]** Template. Against `JS1/course-roster/astraupskill`, `04-TESTING-AND-DEBUGGING.md` differs on 3 of 64 lines, `README.md` on 3 of 63, `VERIFICATION.md` on 2 of 53. `05-PRACTICE.md` Exercises 0 and 5-6 plus the completion rubric are byte-identical across all ten projects in this batch.
- **[D8/D1]** `astraupskill/README.md` Prerequisites is the shared paragraph ("For API projects, review JSON, HTTP methods and promises, then learn the relevant SQL operations as you trace the request") — this project has no SQL at all. `VERIFICATION.md` Limits mentions "transaction scope"; there are no transactions here.
- **[D2]** Unreachable legacy code left behind. After the new guard at `server/server.js:67`, the block `if (!event.name || !event.location || !event.date)` (line 70) and `if (event.capacity < 1 || event.registered < 0 ...)` (line 73) can only ever be reached in states the new guard already excluded — except for `registered > capacity`, which is the only live branch. Two validation layers now disagree about who owns which rule and the course does not say so.
- **[D1/D6]** "Registered cannot exceed capacity" is listed in the report and in `VERIFICATION.md` as delivered behaviour, but `if (... event.registered > event.capacity)` is present unchanged in `backups/24/server/server.js`. It was not added by this change.
- **[D2]** `htmlFor="lesson-field-1"` … `lesson-field-6` in `client/src/App.jsx` — correct label association, meaningless ids.
- **[D5]** All dependencies are `"latest"` with no lockfile; the README setup block does not warn about it.
- **[D6]** `browser-checks.json` for project 24 records only `{"passed": true}` plus an api/persistence label. There is a screenshot (`logs/24-browser.png`) but no assertion list, so "Chromium interaction passed" cannot be independently checked read-only.

## Spot-checks performed
- "The excerpt below comes from server/server.js near line 66" -> `sed -n '66p'` = `function validateEvent(req, res, next) {`; pasted excerpt matches file -> matches.
- "2028-02-29 with capacity 3 and registered 3 succeeds. 2027-02-29, 2028-04-31 … fail" -> I traced `realDate` by hand: `2028-02-29` round-trips (2028 is a leap year); `2027-02-29` parses to 2027-03-01 whose slice is `2027-03-01 !== 2027-02-29`, so it is rejected. Logic matches the claim.
- "capacity 'bad' … fail without replacing a saved event" -> `whole("bad",1,100000)` -> `Number("bad")` is `NaN`, `Number.isSafeInteger(NaN)` is false -> 400 before `normalizeEvent` runs, so `events` is untouched -> matches.
- Test count claim of 2 -> `logs/24-tests.log` `# tests 2 / # pass 2 / # fail 0` -> matches.
- Build claim -> `checks.json` project 24 build entry, `exit_code: 0`, log `logs/24-build.log` -> matches.

## Improvements needed (ordered, concrete, actionable)
1. In `server/server.js`, delete lines 70-75 (the now-unreachable legacy string/number guards) and keep only the cross-field `registered > capacity` rule, so there is one validation layer. (effort: S)
2. Fix the provenance claim: in `VERIFICATION.md`, `01-CODEBASE-MAP.md` and `03-WORKED-CHANGE.md`, say that `registered <= capacity` pre-existed and that the change added the *type and calendar* gate in front of it. (effort: S)
3. `02-CONCEPTS.md` should show the failing case explicitly — print what `new Date("2027-02-29T00:00:00Z").toISOString()` returns — instead of only asserting that the helper works. This is the one place the course could teach something a junior will not find by guessing. (effort: S)
4. Replace the shared Prerequisites paragraph in `README.md` with the two real prerequisites: Express middleware order, and React controlled inputs. (effort: S)
5. Rewrite `05-PRACTICE.md` Exercises 1-4 with event-specific acceptance criteria (e.g. "reject an event whose date is in the past *only* when status is Open, and prove that changing status alone does not re-validate the date"). (effort: M)
6. Rename `lesson-field-N` ids to semantic ones and add a lockfile. (effort: S)

## One-paragraph summary for the index
A compact, well-chosen lesson in cross-field and calendar validation on an Express + React CRUD app. The best part is `realDate`: it shows why a regex plus `Date.parse` is not enough, because JavaScript quietly rolls 2027-02-29 forward to March 1, and the fix is a round-trip comparison. The change also puts the type gate ahead of normalization (so `capacity: "bad"` is rejected with a reason rather than becoming `NaN`) and repairs a React client that never actually mounted. The drawbacks: the server now has two overlapping validation layers where the older one is mostly dead, the course credits a pre-existing capacity rule as new work, and chapters 4-7 are shared boilerplate with a sibling project. Worth doing in the core path for the validation-ordering habit; skim the practice chapter.
