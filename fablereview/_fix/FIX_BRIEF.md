# Brief for fix agents

You are implementing the improvements that a review fleet identified for "Astra"'s project courses. Read `PLAN.md` in this folder first.
Your batch file is `AstraOrganized2/fablereview/batches/<Bxx>.json` (fields: `abs` = project path, `slug`, `wave`, `backup`, `evidence`, `id`).

## Your inputs, per project
1. `AstraOrganized2/fablereview/reviews/<slug>.md` — read "Problems found" and "Improvements needed" (ordered, with effort). Do them all
   unless the plan's scope rules exclude the project or an item is genuinely unsafe; record any skip with a reason.
2. `AstraOrganized2/fablereview/IMPROVEMENT_BACKLOG.md` — do every row that names your project (P1, P3, P4) and every generic row that
   applies to its wave (P2 for wave 1, P3 for wave 2). The wave-1 structural sweep (backlog 2.1, 2.6, 2.7, 2.8 BOM/mojibake, 2.9, 2.10, 1.15)
   has ALREADY been applied by a script; do not redo it, do not undo it.
3. `AstraOrganized2/fablereview/RUBRIC.md` — the target. Your edits should raise accuracy, pedagogy, reproducibility, junior fit and
   specificity without lowering verification honesty.

## What "done" means for the common items
- **Trace lab (wave 1, backlog 2.2):** six *distinct* boundary paragraphs, each naming the real file and function for that boundary
  (client form/component → client serializer or fetch call → HTTP route → validator → repository/transaction → response/render). Cite line
  numbers you checked.
- **Solutions (2.3 / 3.11):** one specific review paragraph per exercise; move any inline answer out of `05-PRACTICE.md` into
  `06-SOLUTIONS-AND-REVIEW.md`; give real answers (code) for exercises that currently only have heuristics, at least for exercises 1-4.
- **Worked change (2.4):** the "Actual implementation excerpt" must contain changed lines (diff the backup to find them); write three concrete
  variations with expected results.
- **Ownership/authz exercise (2.5):** for every server project, add one guided exercise (with solution) that adds an owner/actor to the
  resource and rejects a cross-owner update with 403/404, plus a test. Prefer implementing it in the code when the project already has a
  user/actor concept; otherwise scaffold it as an exercise with a reference test.
- **Code blocks (3.1):** every chapter that explains code shows it; minimum one fenced block in 03, 04, 06, 07.
- **Agent-process language (3.2):** grep `manifest|baseline|frozen|root agent|stage` in `astraupskill/*.md`; rewrite for a learner.
- **Evidence in repo (3.3):** copy the cited logs/TRX/screenshots (not node_modules, not multi-MB binaries) into `astraupskill/evidence/` and fix the links.
- **Red-first exercise (3.4):** an explicit step: restore the snapshot, run the focused test, record the failure, restore the fix.
- **Glossary + prerequisites + time estimates (3.5):** add to README (or `00-START-HERE` section in README) — define every term a junior would not know.
- **08-TRANSLATION.md (3.6):** table: each enforced invariant → Express/Zod/Prisma equivalent → ASP.NET/EF Core equivalent, with a short code
  sample for each, and status-code mapping.
- **xUnit conversion (3.7):** add a real test project using `WebApplicationFactory<Program>` covering the harness's key checks; keep the harness.
  Verify with `dotnet test`.
- **Accuracy fixes (P1):** change the prose to match the code, or the code to match the prose when the prose describes the better behavior
  and the review says so; then re-verify.
- **Latent bugs (P4):** fix, add a regression test, run it, and add a sentence to the course explaining the bug.

## Hard rules
- Ownership: edit only your batch's project folders and `fablereview/_fix/reports/`, `fablereview/_fix/progress/`. Never touch another
  batch's project, Astra's evidence folders (`astrafinalplan/implementation`, `astra-remaining-improvements`), or `fablereview/reviews`.
- Work one project at a time. Install dependencies for one project at a time; see `PLAN.md` for the copy-from-stage trick and the Postgres
  check. Never claim a test passed unless you saw it pass; write the exact command and the observed summary line in the report.
- Keep Astra's accurate content; edit in place. Do not regenerate whole courses. Do not reformat files you did not otherwise change.
  Keep each file's existing line endings.
- Prettier on Windows treats file arguments as globs: pass forward-slash paths or it silently matches nothing and exits 2.
- Paths contain spaces: quote them. Git Bash for text work (`sed -n`, `grep -n`, `diff`); PowerShell for `npm.cmd`/`dotnet`.
- No git operations. No deletes outside files you created in this session.
- When a review item is wrong (you checked and the code already does it), say so in the report instead of editing.

## Report format — `fablereview/_fix/reports/<slug>.md`
```
# <name> — fix report (<Bxx>)
## Done
- [review #n / backlog x.y] <what changed> — files: ...
## Skipped
- [id] <why>
## Verification
- <command> → <observed summary line>
## Course/code consistency check
- <which chapters were re-read against the changed code>
```
Then append one JSON line to `fablereview/_fix/progress/<Bxx>.jsonl`:
`{"slug":"...","done":["review#1","2.2",...],"skipped":["3.7: reason"],"verified":"tests|syntax|none","notes":"..."}`

Finish with a compact batch summary in your reply: per project one line (slug | items done/skipped | verification), plus anything Fable must look at.
