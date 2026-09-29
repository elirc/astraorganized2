# Summary: how good is Astra's work at upskilling a junior CRUD web developer?

Fable, 2026-09-16. Based on 153 per-project reviews by 18 Opus agents plus Fable's own cross-course measurements and spot-checks.

## The verdict in one paragraph

Astra's **code changes are consistently real, correct and well-tested**, and its **verification evidence is honest**: reviewers re-hashed
hundreds of delivered files, recounted every claimed test against the files on disk, and found no inflated browser claims and only
a handful of miscounts. The **courses are the weaker half**. In wave 1 (the 75 small JS apps) they are one template rendered 75 times,
with a median 73% of paragraphs shared across projects, six-times-repeated trace-lab paragraphs, and templated sentences that are
false for the project they landed in. In wave 2 (the 78 larger projects) the courses are bespoke and accurate but often dense,
code-block-free, or aimed above a junior. The biggest structural gap for the stated goal is **ownership/authorization**: almost no
wave-1 course teaches it, and most wave-2 courses practise transactions and concurrency against in-memory stores rather than a database.
Used selectively (about 30 of the 153, see `LEARNING_PATH.md`), the material is a strong CRUD curriculum. Used as delivered, a
junior would spend many sessions on duplicates and template prose.

## Numbers

| | Wave 1 (75) | Wave 2 (78) | All (153) |
|---|---:|---:|---:|
| Mean score (1-5) | 3.95 | 4.46 | 4.21 |
| KEEP / IMPROVE / REWORK (final) | 27 / 40 / 8 | 62 / 15 / 1 | 89 / 55 / 9 |
| Path role core / elective / reference / skip | 36 / 28 / 0 / 11 | 48 / 22 / 8 / 0 | 84 / 50 / 8 / 11 |
| Shared paragraphs across courses (median) | 73% | 0% | |
| Course length (median words, 9 files) | 7,300 | 4,500 | |

Dimension means, wave 1 vs wave 2: accuracy 4.35 / 4.74, change quality 4.36 / 4.55, pedagogy 3.37 / 4.37, CRUD relevance 4.43 / 4.33,
reproducibility 4.11 / 4.40, verification honesty 4.63 / 4.77, junior fit 3.83 / 3.73, specificity 2.55 / 4.77.

Final verdicts apply the rubric thresholds as a floor on top of the reviewer's call; 7 verdicts were tightened (6 wave-1 KEEPs with a
specificity score of 2 became IMPROVE, and ww27 became REWORK for a verification-honesty score of 2).

## Two things that need action now (not course quality)

1. **Live Shopify admin token in Astra's backup.** The andie project itself was cleaned, but Astra's pre-change backup at
   `AstraOrganized2/astra-remaining-improvements/backups/cf8875344b43/scripts/populate-metaobjects.js` still contains a `shpat_` token.
   Revoke the token in Shopify, then delete that backup file. Nothing in this review touched it.
2. **e13 ships a test that reseeds the developer database.** `astraupskill/original/src/lib/commerce/commerce.test.ts` is collected by
   Vitest (no `exclude` in `vitest.config.ts`) and runs `npm run db:push` and `npm run db:seed` against the working `dev.db`.
   Add an exclude or rename the file to `.txt` before anyone runs `npm test` there.

## What Astra did well (verified)

- **Real bugs found and fixed**, not cosmetics. Examples confirmed against backups: six JS1 React clients never mounted (index.html loaded
  `App.jsx` with no `createRoot`); seed SQL selected `due_date` from JSON keyed `dueDate` so every seeded date was NULL (asset-checkout,
  subscription-billing); `CAST(table AS TEXT) ILIKE` search matching ids and timestamps (newcodexJS 07-09); a `DELETE FROM campaigns` in a
  catch block (task-queue-system); public `register` accepting `role: "SYSTEM_ADMIN"` plus a 3-arg Express error handler that never ran
  (buildcrmpyjs); forgeable base64 session cookies (z9); authorization applied after pagination (netzen); a live mutable singleton handed
  to a PATCH walker so a rejected request leaked a title into the next save (buildjira).
- **Tests that assert stored state**, including senior-grade techniques: PL/pgSQL `BEFORE INSERT` triggers as fault injection to prove
  rollback; `Promise.all` races asserting exactly one winner; a test harness that refuses any database not named `astra_test_*` and works in
  a throwaway schema. Optimistic concurrency via conditional `updateMany` on `(id, version)` is taught coherently across many projects.
- **Honest evidence.** Delivery manifests, TRX/TAP logs, screenshots and even failed intermediate runs are retained. Several VERIFICATION
  files pre-empt double counting ("reruns are retained as provenance, not added"). Reviewers found zero fabricated browser checks.
- **Correct framework detail** where it matters: System.Text.Json omitted-vs-null handling, `Enum.IsDefined` after `TryParse`, 428 vs 412
  for If-Match, Next 15 async `params`, `"use server"` with `revalidatePath` after the mutation, `React.cache` per-request sharing.

## What is wrong (verified)

**Wave 1 — the template.** One generator produced all 75 courses. Consequences found on disk:
- Paragraphs about *other* projects leaked in verbatim ("For Poll Studio and Kanban Flow, jsdom runs the actual app.js..." in 30 courses;
  "Questboard, DevDeck and Live Chat" in the batch04 testing chapters; PostgreSQL 18.1 cited in projects with no database).
- `07-TRACE-LAB.md` lists six differently named boundaries and then repeats the same paragraph six times, all pointing at one server function.
  `06-SOLUTIONS-AND-REVIEW.md` repeats one "Review:" paragraph under every exercise. `03-WORKED-CHANGE.md` promises "three variations" and gives none.
- Templated sentences that are false: "a fractional cent is rejected" in four billing-flavoured courses with no cent check; "empty role clears it"
  in 09-job-application-tracker where the schema returns 400; pulse-analytics repeats a fixture (10, 0, 20 → averages 10, 5, 10) in seven files
  while the test uses 10, 0, 30 and asserts 13.33; forum-search's "Tested behavior" describes six threads and a delete that the test never does.
- Clone families: JS1 36-40 are one course five times; JS1 41-50 are two archetypes; newcodexJS 07-10 and 16-20 are one lesson each.
  Eleven projects are marked `skip` for this reason alone.
- Mechanical noise: whole-file CRLF conversion and Prettier reformatting hide the real diff; minified test files (5-10 statements per line)
  in the very files the course tells juniors to read; helper trios (`isText`/`whole`/`realDate`) injected wholesale leaving dead code and
  unreachable legacy guards; a BOM left at line 2 of five servers; every `package.json` still on `"latest"` with no lockfile.
- Inherited test suites reported as the deliverable: jobtrack "90 tests" (Astra added 4), calendar+jobtrack "92" (added 2), devdeck "62" (added 2).

**Wave 2 — packaging and audience.**
- Zero code blocks in all nine chapters of e13, ww17, ww27, ww39, z6, z9 and globgame; transactions explained in prose only.
- Agent-process language addressed to the delivery reviewer, not the learner ("the root agent applies the frozen manifest").
- Chapter files shifted relative to their names in z9 (each file holds the next chapter's content) and zz8.
- Fabricated worked excerpt in w24 (functions that do not exist); a false C# claim in netvg (`checked` does not affect `decimal`);
  transaction placement described backwards in e13; a model solution in ww39 that would throw on the course's own tests.
- Only 3 of 8 .NET projects have real xUnit tests; the rest use bespoke console harnesses, so a junior finishes without writing a `[Fact]`.
- Off-stack projects (Java CLIs j1-j7, Python e14/e15/aiapplybot, browser-only buildsubbox/buildgum/JSProjectLearn/astra4.2) teach the
  right ideas but never demonstrate them on the target stack; each asserts "this transfers" and stops.
- Practice chapters routinely jump from junior exercises 1-3 to senior design tasks 5-7 with review heuristics instead of answers;
  no glossaries; snapshots of pre-change code ship but no exercise makes the learner run a red test first.

## How to use this folder

Read `LEARNING_PATH.md` for the sequence. Read `IMPROVEMENT_BACKLOG.md` if you plan to have an agent fix things; the wave-1 generator
sweeps are the highest-leverage work because one fix lands in 75 courses. Every per-project review in `reviews/` lists ordered,
file-specific fixes with effort estimates.

## Limits of this review

Reviewers read; they did not execute. Test counts and excerpts were verified by reading files on disk; claims that a given test fails
without the fix come from Astra's retained logs. Scores are calibrated within batches by one reviewer each, so a one-point difference
between batches is noise; the wave-level gaps (specificity, pedagogy) are not, and Fable's independent duplication measurement agrees with them.
