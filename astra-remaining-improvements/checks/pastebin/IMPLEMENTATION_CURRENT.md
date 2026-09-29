# Paste workspace implementation checkpoint

Staged canonical project: `_Organized Desktop/01 Net Workspaces/.netpastebin`, id `d30d5dfdf243`. Original Desktop project is untouched. No delivery yet.

Current implementation includes the new PasteStore, WorkspaceDocument/PasteCommands/LegacyMigration, thin Program and Api/AppHost, net10.0 and global SDK pin, rewritten React entry and PasteWorkspace, paste-client helper, responsive CSS, Vite loopback configuration, pinned package manifest, updated root setup/recovery README, nine course chapters, four original snapshots and 48 historical documentation markers. The older store has been replaced in its original staged path; there is no WorkspaceFileStore.cs.

The API application compiled successfully. Backend build 01 failed only in test harness byte comparisons across await; fixed with EqualBytes. Backend build 02 passed. Backend build 03 passed with zero warnings/errors and includes the stronger mutation-failure fixture plus four capacity tests. The 30-scenario backend harness is now running in `checks/pastebin/backend-01`; require its process exit and complete results before claiming success.

Client tests 01: 15/15 passed, terminal exit 0. Evidence is client-tests-01.log and client-tests-01-execution.json. Python HTTP and browser verifier syntax compiled before the later output-directory guard addition; recompile final scripts as needed. HTTP verifier has 17 expected scenarios. Browser verifier has 14 expected scenarios and 9 planned screenshots. Neither has run yet.

Frontend lock-only installation is running; no frontend dependency installation/build/browser gate yet. Run npm ci after lock success, verify manifest/lock matching, then build. Prettier has not yet formatted the new frontend or course. Use the retained cached Prettier executable if helpful; avoid historical snapshots.

Spec `specs/d30d5dfdf243.json` currently lists 93 planned delivery files, 76 expected unique scenarios (30 backend +15 client +17 HTTP +14 browser). Nine course files initially total 5362 words, with an additional legacy-key compatibility paragraph added later. Existing 26 local course links passed an early check. Images are planned, not created. VERIFICATION.md explicitly remains pending and must be rewritten after actual outcomes. No aggregate results.json exists.

Final tasks: complete backend harness; run actual HTTP/CLI verification and fix failures; complete frontend lock/install/build; run browser checks and visually inspect all 9 screenshots; copy reviewed images into astraupskill/images and link them; update course verification, root commands if needed, aggregate evidence and spec; prepare/apply finite delivery only when all required gates genuinely pass; render central progress report. Do not count repeats as additional unique scenarios.

Compatibility finding: legacy key input is bounded to 6..256 characters. Original hashes do not reveal key length; longer historical keys remain stored but cannot authenticate through the revised contract. Root README and VERIFICATION now disclose this. Add this explicit limitation to final spec/report; do not silently replace hashes or imply all historical key lengths work.

API details: 127.0.0.1:5184 default; Vite 5185 and Development origin allowance. Default active file backend/App_Data/workspace-v1.json. Body cap512KiB, strict System.Text.Json unknown/duplicate/required/null policy, exact quoted If-Match, X-Paste-Key, X-Request-Id; no URL-key authorization. Create receipts survive deletion and return410 for expired/deleted replay. Read requests do not increment views or purge expired data. Rate default240/min one local bucket. CLI migrate source destination refuses an existing active workspace and preserves an exact original recovery copy. Production backend serves frontend/dist.

A critical earlier harness compilation error has been corrected. Do not reintroduce byte-array extension SequenceEqual with an awaited argument: .NET10 can select a span overload whose receiver cannot survive await. EqualBytes accepts completed arrays instead.


## Later verified outcomes

Backend run01 completed28/30: title control normalization accepted a trailing newline, and the Windows replacement test caught IOException but the platform returned UnauthorizedAccessException. The title now rejects controls before trimming; the test accepts either filesystem failure and still verifies unchanged bytes. Backend build04 and backend run02 passed30/30 with terminal exit0. HTTP run01 passed17/17 with terminal exit0. Client remains15/15. All62non-browser scenarios pass.

Frontend lock01 passed and manifest/lock dependencies/devDependencies/engines matched. npmci install01 passed19packages. Prettier format01 passed frontend source/tests/config/HTML/rootREADME/course. Frontend build01 underlying Vite process exited0; wrapper then failed to print a Unicode checkmark to CP1252. UTF-8 display recovery verified the saved exit0 and built index/assets without rerunning the build. Browser run01 now active with14expected checks,9screens.

Added verification/requirements-browser.txt pinnedPlaywright1.59.0 and standalone browser commands. Spec now94planned deliveryfiles; longlegacykey limitation is explicit. Course actualwordcount increased after compatibility paragraph/formatting; recalculate at final preparation.


## Browser follow-up

Browser01 completed only the empty landing check before Visibility selector timed out. Added explicit accessible labels to all four dropdowns; frontend build02 passed exit0. Browser verifier now brings the active page to front around the two-tab edit sequence. Browser02 is currently running with14expected scenarios. Only browser01 empty screenshot has been visually reviewed; all final9images remain required.


Browser02 passed landing/create/receipt, then clipboard comparison failed. A separate real Chromium diagnostic proved Windows normalized LF to CRLF; see clipboard-diagnostic.json. Raw/download bytes already matched exactly. The verifier now records clipboard-content.json and permits only CRLF-to-LF conversion for clipboard comparison. It retains byte equality for raw/download content. Browser03 is active. No application code change was needed for this platform behavior. The testing course now explains the distinction.
