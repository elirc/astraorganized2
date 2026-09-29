# IPSKILL / buildsql implementation checkpoint

Canonical `buildsql`, id `0f3292fc93dc`. Original Desktop project has not been modified. Staged spec expects 50 finite delivery files including nine course guides and nine future final screenshots. No aggregate passing results or delivery manifest has been created.

Current implementation preserves all six original curriculum packs (310 lessons, 2155 missions) and adds a compact generated catalog, strict known-data contracts, explicit IndexedDB workspace persistence, transactional identity/revision comparisons, retained/exported drafts, reviewed imports and recovery snapshots. Original localStorage data is never deleted or overwritten by migration. Added a practice-project CRUD workflow, evidence/status constraints, versioned project operations, pagination, real archive filtering, bounded content loading, stale-response guards, lazy full-note rendering, accurate challenge/reward statistics and explicit self-review labeling.

Files: contracts.ts, progression.ts, storage.ts, useWorkspace.ts, PracticeView.tsx, WorkspaceSettings.tsx, LibraryView.tsx, content-loader.ts and catalog.json. Existing App/game/content entry points updated. Six earlier sources retained in docs/original as text. Only original non-content Markdown was root README; it was replaced with current setup and preserved as text. Existing curriculum prose remains unchanged. Authoring tools now produce new candidate outputs, reject incomplete/duplicate input and refuse overwrites. Further verification of authoring behavior may be warranted; no candidate has been published.

Nine astraupskill guides total roughly 5654 words before formatting/final verification. Verification guide remains explicitly pending. Unit/component/content test source defines 43 distinct scenarios (28 game/project, 4 practice interaction, 11 content including six actual packs); actual counts/outcomes must be checked. Browser verifier defines 19 scenarios and nine screenshots; syntax compilation passed, browser has not run. Planned total62, not yet a passing claim.

Dependency lock update passed exit0. npm ci completed its output with259packages in18minutes; verify the execution JSON and wrapper exit. Gate driver `checks/buildsql/run_gates.py` waits for that execution result, then sequentially formats sources/course/README, typechecks, runs Vitest JSON output, validates all content and builds Vite production. Driver stops at the first failed process and retains logs. Do not concurrently edit source while formatter is running. Installation/gates are slow under severe memory pressure; do not kill unrelated user processes.

Remaining: inspect gate results and fix actual failures; run production browser verification in fresh browser-01 output with retained Chromium executable; inspect all nine final screenshots; fix/recheck affected paths; copy screenshots into astraupskill/images; finalize VERIFICATION and exact counts; create checks/buildsql/results.json only after passing actual gates; verify unchanged curriculum hashes and source/baseline manifest; prepare/apply/render central report.

Known design limits are in the spec: whole-document conflicts,8MiB/100projects/10snapshots, no backend/accounts/cloud/automatic grading, known legacy validation only, manual recovery for corrupted active data, candidate generation does not publish, no claim of full accessibility/all browsers/power-loss durability. Backend/auth/booking examples are future exercises, not delivered features.

Central completion count is30/239 after Pastebin delivery. This project is not part of that completed count.

## Gate follow-up

npm ci finished exit0 with259packages in1140.48seconds. format01 passed exit0 in116.31seconds; it also formatted main.tsx, Markdown.tsx and test-setup.ts, now included in the53-file provisional spec. All eight original public/content files remain hash-identical, recorded in preserved-content-hashes.json. A baseline tsconfig.app.tsbuildinfo is generated output and intentionally not a delivery file.

Typecheck01 passed exit0 in225.59seconds. tests01 failed during Node-suite setup because the original shared test-setup.ts accessed window unconditionally. Its four component tests passed; game and content suites did not execute. Added a typeof-window guard; no application behavior changed. Pipeline typecheck02/tests02(default plus JSON reporters)/content01/build01 is running. Inspect actual results before proceeding. Browser verifier syntax passed; its19 scenarios and9 screenshots remain unrun.

## Latest gates

Typecheck03 exit0; tests03 all43 passed after guarding window in Node setup and setting a30second correctness timeout (previous41/43 failures were5second deadlines). Content01 exit0 across original archive. Build01 running. Authoring01 seven isolated CLI checks passed exit0; script added to finite delivery spec and guide. Total planned distinct checks now69 =43+7authoring+19browser. Browser remains unrun. No published content changed.

Final browser01 all19passed; browser02 screenshot refinement all19passed exit0. Nine final images inspected/copied, VERIFICATION finalized, aggregate69passed. Published8contentJSONfiles hash-identical. Ready for prepare/apply/render; original not yet modified until apply succeeds.
