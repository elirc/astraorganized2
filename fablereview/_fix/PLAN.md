# Fix program plan — implement every improvement in the Fable review

Fable plans, orchestrates and reviews. Opus agents do the edits. Started 2026-09-17.
Input: `../IMPROVEMENT_BACKLOG.md` (P0-P4) and the "Improvements needed" section of every `../reviews/<slug>.md`.

## Phases

| Phase | Who | What | Gate |
|---|---|---|---|
| 0 | Fable | Redact the Shopify token in Astra's backup (done; the user still has to revoke it). Write this plan, `FIX_BRIEF.md`, verification script. | — |
| 1 | 1 Opus agent (S1) | **Wave-1 structural sweep**: one idempotent script over all 75 `astraupskill/` folders for the fixes that are identical everywhere (backlog 2.1, 2.6 de-minify, 2.7 pins, 2.8 BOM/mojibake, 2.9 diff note, 2.10 clone banners, 1.15 delta counts). Dry-run report first, then apply. | Fable reads the dry-run diff sample before apply; then verify.py "sweep" checks pass. |
| 2 | 18 Opus agents, max 6 concurrent | **Per-batch authoring + code fixes.** W01-W08 own wave-1 batches B01-B08; X09-X18 own wave-2 batches B09-B18. Each agent does every applicable backlog row and every review "Improvements needed" item for its projects, verifies code changes by running tests, and writes a change report per project. | Each report lists what was verified and how. |
| 3 | Fable (+ Opus QA sampling) | `verify.py` full run, template-smell re-measurement, chapter alignment, code-block counts, leaked-phrase scan; run a sample of test suites; spot-read reports; `FIX_REPORT.md` with before/after per project. Re-dispatch agents for anything that failed the gate. | All gate checks green or explicitly waived with reason. |

## Scope rules

- **Skip-role clones** (21 projects: JS1 library-lending, gym-membership, campaign-planner, volunteer-coordinator, field-service, research-studies,
  travel-requests, vendor-contracts, quality-audits, grant-manager, incident-response, procurement-portal, property-rentals, patient-intake;
  newcodexJS 08, 09, 10, 17, 18, 19, 20): sweep fixes + a "same lesson as X" banner + P1 accuracy fixes only. No new authoring.
  (Note: 09 and 10 and 20 are listed skip in LEARNING_PATH; treat 08/09/10 and 17-20 as clones of 07 and 16 respectively.)
- **Reference-role off-stack projects** (j1-j7, e14, e15, aiapplybot, andie, buildsmallplates): P1 fixes + `08-TRANSLATION.md` + glossary/prereqs. No code changes unless the review names a bug.
- Everything else: full treatment.
- Code changes must keep the course accurate (edit the chapter that describes the code in the same pass).
- No git commits, no pushes, no deletions of Astra's evidence folders.

## Concurrency and verification rules (from prior experience on this machine)

- At most 6 agents run at once. Each agent works one project at a time and installs dependencies for one project at a time.
- No project has `node_modules` installed. For wave 2, `AstraOrganized2/astra-remaining-improvements/stage/<id>/node_modules` often exists:
  **link it as a directory junction, never copy it** (C: had 3.5 GB free on 2026-09-17 and copies caused ENOSPC that truncated course
  files): PowerShell `New-Item -ItemType Junction -Path "<project>\node_modules" -Target "<stage>\node_modules"`; remove the junction
  afterwards with `Remove-Item "<project>\node_modules"` (removing a junction does not touch the target). Otherwise `npm ci` (or
  `npm install` when there is no lockfile) is allowed, one project at a time, with `--prefer-offline`, ONLY after checking
  `(Get-PSDrive C).Free/1GB` is above 2; delete the installed `node_modules` when done.
- Write course files via temp file + verify + replace so a failed write cannot truncate a chapter. Re-check any file you wrote for 0 bytes.
- .NET: `dotnet` 10.0.302 is on PATH; `dotnet test` is fine. Node is 22.16.0. Python 3.13.
- Postgres: check `netstat -an | findstr 5432 5433 5434 55439` before assuming a server. If a suite needs Postgres and none is reachable,
  say so in the report; never claim a pass that was not observed.
- Playwright browsers exist at `astra-remaining-improvements/playwright-browsers` (set `PLAYWRIGHT_BROWSERS_PATH`).
- After finishing a project, remove any `node_modules` you copied in **only if** the project had none before (keep the tree as you found it plus your edits).

## Deliverables

- `_fix/reports/<slug>.md` — one per project: items done (with backlog/review ids), items skipped and why, verification evidence (commands + observed result).
- `_fix/progress/<Bxx>.jsonl` — one line per project: `{"slug","done":[...],"skipped":[...],"verified":"tests|syntax|none","notes"}`.
- `_fix/FIX_REPORT.md` — Fable's final before/after report.
