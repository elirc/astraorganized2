# Brief for review agents

You are reviewing improvements that an agent called "Astra" made to many Desktop projects. Astra's goal was to
upskill a junior SWE in CRUD web development (JS, TypeScript, React, Node, Next.js, C#, .NET). Your job is to judge,
per project, how well the delivered course + code change actually serves that goal, and what must be improved.

## Where things are
- Projects live under `C:\Users\Owner\Desktop\`. Each assigned project has an `astraupskill/` folder (the course).
- Your batch file (`AstraOrganized2/fablereview/batches/Bxx.json`) lists each project with: `abs` (absolute path),
  `course`, `backup` (Astra's pre-change backup of the touched files, so `diff -r backup project` shows the change),
  and `evidence` (Astra's own delivery record: files touched with before/after hashes, test results, limits).
- Wave 1 (75 small CRUD apps): evidence in `AstraOrganized2/astrafinalplan/implementation/**/delivery-manifest.json`,
  per-batch `checks.json`, `browser-checks.json`, and `source-changes.diff` at the implementation root.
  Per-project detail is in `AstraOrganized2/astrdocs/NEXT_*_IMPLEMENTATION_REPORT.md`.
- Wave 2 (78 larger/varied projects): evidence in `AstraOrganized2/astra-remaining-improvements/deliveries/<id>.json`,
  spec in `specs/<id>.json`, prior reviews in `reviews/`, test logs in `checks/`.

## Method per project (budget ~10-15 minutes of reading each)
1. Read the course README, VERIFICATION, and skim all 9 files. Note word count (`wc -w`).
2. Diff backup vs. current for the touched files to see the actual code change. Read the new/changed tests.
3. Spot-check at least 3 concrete claims from the course against the code on disk (a quoted excerpt, a line
   reference, a command, a behavior). Record each spot-check.
4. Score with `fablereview/RUBRIC.md`. Fill `fablereview/REVIEW_TEMPLATE.md` exactly; write it to
   `fablereview/reviews/<slug>.md`.
5. Append a line to `fablereview/_work/<Bxx>.jsonl` with:
   `{"slug":..., "name":..., "wave":..., "stack":[...], "scores":{"D1":n,...,"D8":n}, "avg":n.n, "verdict":"KEEP|IMPROVE|REWORK", "role":"core|elective|reference|skip", "top_fix":"...", "summary":"..."}`

## Hard rules
- READ-ONLY. Do not run `npm install`, `dotnet restore`, builds, tests, or dev servers. Do not modify any project.
  Do not write anywhere except `fablereview/reviews/` and `fablereview/_work/`.
- Bash tool on this machine is Git Bash; paths with spaces must be quoted. Use `sed -n`, `grep -n`, `diff -r`, `wc -w`.
- Be skeptical of Astra's own reports. They are inputs, not truth. If VERIFICATION.md claims a browser check but
  the evidence JSON shows none, that is a D6 finding.
- Watch for template smell: if the same paragraph appears in several of your projects with only nouns swapped, say so
  with a quote and mark D8 low.
- Every score under 4 needs concrete evidence (file:line or short quote). No vague "could be better".
- Improvements must be actionable by an engineer in a follow-up session: say what file to change and what to add.
- When done with all projects in the batch, reply with a compact batch summary: per project one line
  (slug | avg | verdict | role | top fix), plus 3-5 cross-cutting observations for the batch.
