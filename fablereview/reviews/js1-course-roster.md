# JS1/course-roster — Fable review

- **Path:** `JS1/course-roster`  ·  **Wave:** 1  ·  **Stack:** Node/Express (in-memory array) + React 18 (Vite, JSX)  ·  **Batch:** B03
- **Astra's change (one line):** `validateCourse` gained a real type gate (`isText` on code/title/instructor, `whole()` on capacity/enrolled), a closed level vocabulary, and a normalized-code uniqueness check that returns **409** while allowing a record to keep its own code on edit; plus a JSON-object body guard, `export const app` + a `pathToFileURL` listen guard so tests can import the app, and a genuinely missing client entry point (`client/src/main.jsx`) that finally mounts React.
- **Course size:** 5,824 words across 9 files  ·  **Tests claimed:** 2  ·  **Tests found on disk:** 2 in `test/api.test.js` (+ `test/http.js` harness)

## Scores

| D1 Accuracy | D2 Change quality | D3 Pedagogy | D4 CRUD relevance | D5 Reproducibility | D6 Verification honesty | D7 Junior fit | D8 Specificity | Avg |
|---|---|---|---|---|---|---|---|---|
| 4 | 4 | 3 | 5 | 4 | 4 | 4 | 2 | 3.8 |

**Verdict:** IMPROVE    **Path role:** core

## What Astra did well
- **The app was broken before and now works.** `backups/23/client/index.html` loaded `/src/App.jsx`, but `App.jsx` only does `export default function App()` — nothing ever called `createRoot`. Astra added `client/src/main.jsx` (`createRoot(document.getElementById("root")).render(<App />)`) and repointed the script tag. That is a real, verifiable fix, and it is honestly described in the report as the client mount being repaired.
- Correct HTTP semantics: duplicate resource -> `409`, bad shape -> `400` (`server/server.js:78-83`). Teaching a junior that "already exists" is not a 400 is worth the whole chapter.
- The uniqueness check is written so edit-in-place works: `courses.some(existing => existing.id !== req.params.id && existing.code === course.code)`. On POST `req.params.id` is `undefined`, so the guard degrades correctly.
- Tests hit real HTTP against the real Express app on an ephemeral port and assert both the normalized response (`made.data.code === 'ASTRA-101'`) and the 409 on a whitespace-padded equivalent (`test/api.test.js:7-9`). Test 2 loops seven distinct bad payloads including `{enrolled:null}` and `{capacity:1.5}`.
- `npm test` / `npm run build` scripts and `vite.config.js` were added, so the project is actually runnable and testable now.

## Problems found (evidence required)
- **[D8]** Heavy template reuse. Diffing this course against `JS1/event-admin/astraupskill` line-for-line: `04-TESTING-AND-DEBUGGING.md` differs on 3 of 64 lines, `README.md` on 3 of 63, `VERIFICATION.md` on 2 of 53, `05-PRACTICE.md` on 5 of 47. The "Review:" block under every exercise in `06-SOLUTIONS-AND-REVIEW.md` is one repeated paragraph.
- **[D2]** Dead code was injected. `realDate` is defined at `server/server.js:113` and never called anywhere in the file (a grep for call sites returns only the definition). It is the same copy-pasted helper trio dropped into all six Express projects in this batch.
- **[D2]** The pre-existing guards are now unreachable. `if (!course.code || !course.title || !course.instructor)` (`server/server.js:85`) can never fire, because `isText(value,1)` at line 78 already rejected those; same for `capacity < 1 || enrolled < 0` at line 89. The course never mentions that it left two layers of duplicated validation behind.
- **[D1/D6]** The report and `VERIFICATION.md` present "enrollment cannot exceed capacity" as part of the delivered change, but `if (course.enrolled > course.capacity)` already existed in `backups/23/server/server.js` — the diff does not add it. Credit for pre-existing behaviour.
- **[D2, ordering]** The 409 check runs before the capacity checks, so a request that is both a duplicate code *and* over capacity returns 409 rather than the validation error; not wrong, but undiscussed.
- **[D2]** `client/src/App.jsx` label fixes use opaque generated ids: `htmlFor="lesson-field-1"` … `lesson-field-6`. The association is correct, but `lesson-field-4` tells a reader nothing; `course-capacity` would.
- **[D5]** `package.json` pins every dependency as `"latest"` (pre-existing) and there is no lockfile, so `npm install` on a fresh machine is not reproducible. `VERIFICATION.md` admits "Dependency declarations using latest remain floating" but the README setup section does not warn the learner.

## Spot-checks performed
- "The excerpt below comes from server/server.js near line 77" -> `sed -n '77p'` = `function validateCourse(req, res, next) {`; the pasted excerpt matches the file verbatim -> matches.
- "Create astra-101 with capacity 4 and enrolled 2: the returned code is ASTRA-101. A second equivalent code returns 409." -> `normalizeCourse` does `.trim().toUpperCase()` (`server/server.js:102`) and `test/api.test.js:7-8` asserts exactly that pair -> matches.
- "2 passing regression cases, build passed" -> `logs/23-tests.log` shows `# tests 2 / # pass 2 / # fail 0`; `checks.json` has a build entry with `exit_code: 0` and a tests entry with `exit_code: 0` -> matches.
- "Chromium interaction passed" -> `browser-checks.json` records `{"project":"23","passed":true,"api":"actual isolated HTTP server"}` with `logs/23-browser.png` on disk. The JSON records no per-assertion detail, so the *content* of the browser check cannot be verified read-only — only that it ran and a screenshot exists. Partially verifiable.
- "Editing the original title succeeds" -> `test/api.test.js:9` PUTs a changed title and asserts 200 plus a stable id -> matches.

## Improvements needed (ordered, concrete, actionable)
1. Delete the unused `realDate` helper from `server/server.js:113`, and collapse the now-unreachable legacy guards at lines 85-95 into the single new guard — then add a paragraph to `03-WORKED-CHANGE.md` explaining why leaving two validation layers is a maintenance hazard. (effort: S)
2. Rewrite `05-PRACTICE.md` and `06-SOLUTIONS-AND-REVIEW.md` so the exercise bodies are roster-specific: e.g. "add a `PATCH /api/courses/:id/enroll` that must reject when `enrolled === capacity`, and write the test that proves two concurrent enrolments cannot both succeed against the in-memory array". The current bodies are one shared paragraph. (effort: M)
3. Correct the "Tested behavior" wording in `VERIFICATION.md` and `01-CODEBASE-MAP.md` to separate what the change added (uniqueness/409, type gate, level vocabulary) from what already existed (enrolled ≤ capacity). (effort: S)
4. Rename `lesson-field-1..6` in `client/src/App.jsx` to semantic ids (`course-code`, `course-title`, …) and mention label/`htmlFor` association in `02-CONCEPTS.md`. (effort: S)
5. Add a `package-lock.json` (or pin exact versions) and note in the README setup block that `latest` resolution can change under the learner. (effort: M)
6. Add one test for the in-memory persistence limit the course claims to teach: restart the app and show the course list resets. Nothing currently exercises "in-memory restart behavior" despite `VERIFICATION.md` citing it. (effort: S)

## One-paragraph summary for the index
This is the most useful kind of project in the batch: a small Express + React CRUD app where the change teaches three things a junior needs daily — validate types at the HTTP boundary before normalizing, return 409 (not 400) for a uniqueness conflict, and let a record keep its own unique value when it is edited. The two tests run against a real Express server over real HTTP, and Astra also fixed a genuine bug: the React client never mounted because `index.html` pointed at a component module with no `createRoot`. The costs are that the course's supporting chapters are near-identical to its siblings in this batch, and the server now carries an unused helper and two layers of duplicated validation. Do it early in the path, but read chapters 5 and 6 with low expectations.
