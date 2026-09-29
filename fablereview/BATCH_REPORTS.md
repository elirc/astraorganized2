# Batch reports (condensed)

Cross-cutting observations from each of the 18 reviewer batches, as reported back to Fable. Per-project scores are in `SCOREBOARD.md`;
per-project detail is in `reviews/`. Fable spot-checked the claims marked ✔ on disk.

## Wave 1

**B01 — JS1 01-03, finance-dashboard, recipeweb, jobtrack, newcodexJS 01-03, 05 (10 KEEP).** Every "near line N" excerpt verified exact.
Browser checks real (Playwright, projects 01-06; 07-10 correctly omit the row). jobtrack reports the inherited 90-test suite as its count
(Astra added 4). Courses ~80% one template: `02-CONCEPTS.md` differs in 4 of 41 lines between task-board and expense-tracker; the
"three variations" section gives none. newcodexJS 02 and 05 carry most of the CRUD value; all four Postgres courses need a DB with
`CREATE SCHEMA` rights and offer no container fallback.

**B02 — JS1 11-18, newcodexJS 04, 06 (4 KEEP, 6 IMPROVE).** 171 delivered files re-hashed, 0 mismatches. Only 33-45% of each course's
words are unique. "PostgreSQL 18.1 on port 55439" claimed in 7 of 10 projects that never touch Postgres. Six browser-only apps cap CRUD
relevance at 3. No lockfiles; `"latest"` everywhere. Test counts reported per `test()` block, so notes-app's ~16 assertions read as "1 test".

**B03 — JS1 21-30 (2 KEEP, 7 IMPROVE, 1 REWORK).** ✔ pulse-analytics fixture wrong in seven files including VERIFICATION. Five JSX clients
never mounted before Astra (index.html loaded `App.jsx`, no `createRoot`); Astra fixed it silently. Copy-pasted helper trio left dead code and
unreachable legacy guards in six servers. LF→CRLF on every touched file hides real diffs. Course-roster vs event-admin differ in 3 of 64 lines.

**B04 — JS1 31-40 (0 KEEP, 5 IMPROVE, 5 REWORK).** ✔ forum-search "Tested behavior" fabricated. Stages 36-40 are one course five times
(~40 changed lines of ~575). One 02-CONCEPTS paragraph appears verbatim in all 48 JS1 courses. Real seed bug fixed in asset-checkout
(`due_date` vs `dueDate`). Test files minified; BOM at line 2 of five servers; harness-only ids `lesson-field-1..5` in App.tsx.

**B05 — JS1 41-50 (6 KEEP → IMPROVE after normalization, 4 IMPROVE).** Two archetypes (TS/Postgres, JS/in-memory); scores identical within
each. 190 files re-hashed, 0 mismatches. TS variant: transaction + `FOR UPDATE` + audit on one client, `REPEATABLE READ READ ONLY` paging,
DATE OID parser. JS variant's best change (mounting the client) undocumented. Missing `CREATE DATABASE`/`pgcrypto`. Nothing teaches authz.

**B06 — JS1 51-57, newcodexJS 07-09 (2 KEEP, 8 IMPROVE).** 234 files re-hashed, 0 mismatches. ✔ "fractional cent is rejected" false in four
courses. All ten 04-TESTING files discuss Questboard/DevDeck/Live Chat. Trace-lab six-identical-boundaries pattern in all ten. Documented
`npm install && npm test` inside the project was never executed (checks ran from Astra's shared workspace). newcodex root package names
are Astra pipeline ids (`astra-crud-workspace-58`).

**B07 — newcodexJS 10-19 (6 KEEP, 1 IMPROVE, 3 REWORK).** 552 code lines extracted from course fenced blocks, 552 matched source. 16-20 are
95.9-99.8% identical (one changed sentence between 16 and 18). Real pre-existing bugs fixed in 12-15 (cart compared incremental quantity
while SQL added it; `activateEnvironment` cleared flags before checking existence). Trigger-injected rollback tests in 13 and 14. Root
`package.json` only declares `concurrently`; `pg`/`tsx` reach tests via workspace hoisting.

**B08 — newcodexJS 20, recipeview, calendar+jobtrack, devdeck, job track (1 KEEP, 4 IMPROVE).** Code better than prose. Trace-lab paragraph
repeated 6× in all five. Inherited suites reported as deliverable (92, 62). Prettier reformat conflicts with repo style in calendar+jobtrack.
Documented `npm test` commands differ from what checks ran (`tsx --test` by absolute path).

## Wave 2

**B09 — .NET workspaces (8 KEEP).** System.Text.Json, `Enum.IsDefined`, 428/412 details correct. ✔ netvg claims `checked` detects decimal
overflow (false). netgum baseline had literal Python syntax; fix described euphemistically. Only 3 of 8 have real xUnit; others use console
harnesses or Python. EF Core nearly absent (JSON files, dictionaries). buildjira live-singleton patch bug and netzen authz-after-pagination
are standout lessons. Opposite judgements on the same anti-pattern (netvg removes fabricated-success fallback, buildasana keeps it).

**B10 — meterforge, campusops, missioncontrol, borrowbox, Stripe, Ramp, master 6, jstrain2.3 (8 KEEP).** Counts perfect (29, 42, 10, 66, 51,
139, 29, 97). Snapshots ship but no exercise makes the learner see red. Only missioncontrol and Stripe run transactions against a database.
Exercises 5-7 are senior design with rubrics instead of answers. Ramp: `BoundedChannelFullMode.Wait` claim wrong.

**B11 — b1, d1, e13, e6, w24, ww17, ww27, ww37 (4 KEEP, 4 IMPROVE; ww27 → REWORK after normalization).** ✔ e13 archived test collected by
Vitest and reseeds `dev.db`. e13/ww17/ww27 have zero code blocks and doubled H1s; ww17 pastes one 57-word paragraph into all nine files.
w24 worked excerpt fabricated. ww17 dropped `.int()` on an `Int` column. Next.js claims otherwise correct (async `params`, `headers()` misuse fixed).
Test counts drift upward (e13 17 vs 11; ww27 10/11/12).

**B12 — ww39, ww5, z1, z3 ×2, z6, z7, z9 (4 KEEP, 4 IMPROVE).** ✔ z9 chapter files hold the next chapter's content. Zero code blocks in
ww39/z6/z9. Agent-process language in VERIFICATION ("the root agent applies the frozen manifest"). Evidence copied into the project is the
best predictor of score. z6 test is tautological (fake's own catch restores state). ww39 printed solution throws on its own tests.
Prisma/Next claims held up everywhere checked.

**B13 — zz8, appmakertrack, globgame, jdtrrain2.1, aiheartbeat, buildbusinesses, lucasrouter, buildcrmpyjs (6 KEEP, 2 IMPROVE).** Counts
reconciled (up to 505). globgame zero code blocks and a solutions file with no solutions; zz8 chapters offset. buildcrmpyjs: public register
accepted `SYSTEM_ADMIN`, 3-arg error handler never ran. Half the batch never touches a server. CRLF churn hides 4-line README edits.

**B14 — buildantigVG, master2/3/4/7, grokbuild ecommerce/hr/multitenant (8 KEEP).** ✔ master7 broken link. Grok projects run real disposable
Postgres + Chromium but ship no evidence in-repo; master* mock Prisma but ship snapshots/evidence. Serializable isolation claimed three times,
never demonstrated. Latent bugs: master4 reservation id collision, master2 tenant from untrusted headers.

**B15 — grokbuild order/ppm/team, e14, e15, aiapplybot, JSProjectLearn, buildgum (8 KEEP).** Counts exact. Not one course mentions Express,
Next, C#, EF Core or Zod outside tooling notes; three Python and two browser-only projects assert transfer and never show it. One correct
optimistic-concurrency lesson taught five ways (a feature). ppm README claims an untouched file was repaired. JSProjectLearn drifted after delivery.

**B16 — buildsubbox, jstrain3.0, react, j1, j2, j3, e12, e20 (8 KEEP).** Stack detection: j1/j2/j3 are Java 17 CLIs; "react" contains no
React (vanilla ES modules, honestly stated). Zero inflated counts; three projects volunteer failures. Delivered source unreadable in five
projects (20 tests in 26 lines). Same four-move pattern (bounded snapshot → compare → atomic replace → publish) in seven of eight; j3 inverts it.

**B17 — j4, j5, j7, job track ×3, andie, astra2 (4 KEEP, 4 IMPROVE).** ✔ Shopify token survives in Astra's backup of andie (live project clean).
Zero shared sentences across 28 course pairs. Four of eight are Java/Shopify tooling with 5/5 accuracy and 2-3 relevance. Windows-only
commands universal; j5/j7 document a `data/` fixture that does not exist. task-queue-system ran only 2 of 19 tests against pre-fix code.

**B18 — astra4.2, buildsmallplates, buildsql, buildwhiteboard, formforge, LLM_Generated_Helper (6 KEEP).** Counts exact including `it.each`
expansions. Zero template smell (one repeated shell line across 54 files). buildsql is a React app, not a SQL course. Helper: Astra built a
second, unrelated 800-line CRUD app inside the Electron project. Recurring: new return values nobody consumes; monolith files (1,098-line
App.tsx, 900-char JSX line). All CRUD-web payoff sits in unscaffolded practice tickets.
