# fablereview — Fable's review of Astra's project improvements

**Question answered:** for each of the 153 Desktop projects that Astra changed (code + a 9-file `astraupskill/` course),
how good is the result at upskilling a junior SWE in CRUD web development on JS/TS/React/Node/Next and C#/.NET,
and what still needs improving?

**Method:** 18 Opus review agents (one per batch of 5-10 projects) did read-only, evidence-driven reviews against
a fixed rubric; Fable designed the rubric, measured cross-course duplication independently, spot-checked the
reviewers' most consequential claims on disk, normalized verdicts, and wrote the summary, path and backlog.
No project was installed, built, run or modified during the review (2026-09-16). The fix pass that followed (2026-09-18) did modify projects; see `_fix/FIX_REPORT.md`.

## Start here

| File | What it is |
|---|---|
| [_fix/FIX_REPORT.md](_fix/FIX_REPORT.md) | **Fix pass (2026-09-18):** every review item applied across all 153 projects, gates before/after, code changes verified by running each project's tests, per-project reports in `_fix/reports/`. |
| [SUMMARY.md](SUMMARY.md) | Fable's executive verdict: what Astra did well, what is wrong, the numbers, and the two items that need action now. |
| [LEARNING_PATH.md](LEARNING_PATH.md) | The curated sequence a junior should actually follow (about 30 of the 153 projects), with what each one teaches. |
| [IMPROVEMENT_BACKLOG.md](IMPROVEMENT_BACKLOG.md) | Prioritized, actionable fixes: cross-cutting sweeps first, then per-project top fixes grouped by verdict. |
| [SCOREBOARD.md](SCOREBOARD.md) | Every project with its 8 dimension scores, average, final verdict, path role, template-duplication %, word count and top fix. |
| [reviews/](reviews/) | One review per project (153 files), each with scores, evidence, spot-checks and ordered improvements. |
| [BATCH_REPORTS.md](BATCH_REPORTS.md) | Condensed cross-cutting observations from each of the 18 reviewer batches. |

## Supporting files

| File | What it is |
|---|---|
| [RUBRIC.md](RUBRIC.md) | The 8 dimensions (accuracy, change quality, pedagogy, CRUD relevance, reproducibility, verification honesty, junior fit, specificity), verdict thresholds and path roles. |
| [REVIEW_TEMPLATE.md](REVIEW_TEMPLATE.md) | Template every per-project review follows. |
| [AGENT_BRIEF.md](AGENT_BRIEF.md) | Brief given to the review agents (method, evidence locations, hard rules). |
| [registry.json](registry.json) | The 153 projects: name, absolute path, wave, detected stack, backup and evidence locations. |
| [batches/](batches/) | The 18 batch assignments (B01-B08 = wave 1, B09-B18 = wave 2). |
| [scoreboard.json](scoreboard.json) | Machine-readable scoreboard (reviewer verdict, rule verdict, final verdict, scores). |
| [_work/](_work/) | Reviewer JSONL output per batch, Fable's template-smell measurement, and the aggregation script. |

## Scope

- **Wave 1** (75 projects, delivered 2026-09-08): `JS1/*` (48), `newcodexJS/*` (20), plus finance-dashboard, recipeweb, jobtrack, recipeview, calendar+jobtrack, devdeck, and "08 App And Product Projects/job track". Evidence in `AstraOrganized2/astrafinalplan/implementation/`.
- **Wave 2** (78 projects, delivered 2026-09-09 to 2026-09-13): the larger and more varied projects (.NET workspaces, Next.js experiments, Prisma apps, grokbuild*, master*, Java/Python CLIs, browser-only apps). Evidence in `AstraOrganized2/astra-remaining-improvements/`.
- Two "prepared but not delivered" entries (ww55, e2) have no course and were not reviewed.

Re-run `python _work/aggregate.py` after editing any `_work/Bxx.jsonl` line to regenerate the scoreboard.
