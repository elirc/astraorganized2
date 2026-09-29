# Tidebound improvement checkpoint — not delivered

> Historical checkpoint, superseded by [DELIVERED.md](DELIVERED.md). Tidebound has now been applied and verified. All process handles mentioned below are terminal; do not restart any of them or rerun the one-time helpers.

Canonical family `4de416cd300b`, Desktop folder `astra2`. Stage: `astra-remaining-improvements/stage/4de416cd300b`. The original folder is untouched. The collection remains **39 of 239 eligible families delivered; 200 remain**. Previous goal turn made progress by creating and verifying completion reports; this turn is making code, course, and verification progress on the next family.

## Implemented in the isolated copy

- `src/voyages.ts`: IndexedDB metadata and snapshot stores, atomic writes/deletes, expected revisions, unique normalized checkpoint titles, validated reads/imports, protected manual/automatic slots, metadata edits, snapshot replacement, archive/restore/delete, 50-checkpoint / 5 MB snapshot / 50 MB aggregate bounds. No server or accounts.
- `src/voyageLibrary.ts` and `src/voyages.css`: native modal collection, create/edit, retained drafts, search, eight-record pages, archive/restore, explicit load/replace/delete confirmations, export, readable responsive cards and focus handling.
- `src/main.ts`: versioned slots, one-page operation queue plus cross-page revision checks, current-world generation invalidation, save-status sequence protection, commit-before-world replacement, confirmed loads/imports/new games, preserved legacy localStorage adoption, paused writes on conflicts, export fallback when storage cannot open, guarded pending loads, improved confirmation focus, reset simulation accumulator and reduced-motion class on load.
- `src/engine.ts`: demolition refunds clamp room to zero; paused warehouses do not subtract capacity twice; the final paused harbor remains protected.
- 18 new repository tests, three demolition tests, existing 23 simulation/progression tests retained. `vitest.config.ts` selects only current tests, one worker, bounded timeouts; progression keeps all simulation assertions with a 120-second wall-clock allowance.
- Nine course files drafted (initially 6,855 words, subsequently expanded with the verified demolition walkthrough), all 54 initial local links checked. Current course verification deliberately says unfinished.
- 42 exact original text snapshots in `docs/original`, with hash manifest. Original source, tests and historical artifacts there are reading/evidence material, not another test suite. Five original historical documents labeled at the current root; README/architecture updated for current saving behavior.
- Existing browser/performance scripts adapted to explicit load/import confirmations. New `scripts/library-check.mjs` owns its fresh preview and isolated browser contexts. Central `run_original_browser_checks.py` is ready but has NOT been executed.

Do not rerun `stage_projects.py`, `preserve_originals.py`, `integrate_saves.py`, `update_project_docs.py`, or `refine_load_controls.py` over this stage; they are one-time helpers and some expect the old source shape.

## Confirmed results

- `install-baseline`: npm 10.9.2 clean install succeeded, 66 packages.
- `engine-baseline`: FAILED, 18/23 tests passed and shutdown timed out. All five failed durations exceeded their original 5-second or progression 30-second limit. Do not claim an original domain assertion failure solely from the generic `STACK_TRACE_ERROR` JSON traces.
- `typecheck-01`: FAILED on a DOM focus union type; fixed.
- `npm-audit-01`: found Vitest/mocker advisory GHSA-82fw-gwwq-j7x9. Official patched target 4.1.11.
- `dependencies-01` and `dependency-lock-01`: npm 10 resolver crashed reading `edgesOut`, including a fresh package folder.
- `dependency-lock-02`: npx bootstrap of npm 11.19.1 FAILED due shared-cache EEXIST/ENOENT rename; no global cache cleanup attempted.
- `install_npm_cli.py`: fetched official npm 11.19.1 tarball directly, verified registry SHA-512, safely extracted to `checks/tidebound/tooling/npm-11.19.1`. Supports this Node 22.16.0. Metadata in `npm-cli-install.json`.
- `dependency-lock-03`: SUCCESS using that local npm 11.19.1 and private `checks/tidebound/npm-cache`, with normal peer checks. Final package and lock copied from `.dependency-refresh` to stage.
- `install-final-01`: SUCCESS using ordinary npm 10.9.2 `ci` against the final lockfile and private cache, 58 packages. Target path was verified inside this stage before package-managed replacement.
- `app-typecheck-02`: SUCCESS before the final small refinements; superseded by full build below.
- `tests-01`: **44/44 passed**, four current suites, process exit 0. Recorded under `tests-01-results.json`. Earned victory again at 3,190 simulation seconds; 101-building/six-ship 300-second benchmark took 716 ms in this run.
- `build-01`: SUCCESS, includes full `tsc --noEmit` for source/tests and Vite production build. Final game asset `game-CZhFWYNe.js` 658.72 kB, CSS `game-Cv-6ulJq.css` 38.05 kB. Expected >500 kB bundle notice, principally Three.js.
- `npm-audit-02`: SUCCESS, zero known advisories.
- `reproduce_demolition.mjs`: SUCCESS comparing original and current compiled source. Original wood 1,000 → 400; current 1,000 → 1,000. `demolition-comparison.json` records it. Its generated CommonJS folders are central evidence, not delivery files.

Pinned direct versions: Three 0.180.0, Vite 7.3.6, TypeScript 5.9.3, Vitest 4.1.11, fake-indexeddb 6.2.5, Playwright 1.63.0, @types/node 26.4.1, @types/three 0.180.0. Runtime Node 22.16.0. Browser runner currently explicitly uses installed `C:/Program Files/Google/Chrome/Application/chrome.exe` with a fresh profile; actual version still to record from passing browser output.

## Browser investigation in progress

`browser-library-01` exited 1 after six passing workflows: create/escaped notes, metadata edit, duplicate rejection/draft retention, search/empty state, exact snapshot export, and reload persistence. It timed out at script line 127: clicking the FIRST page's checkpoint Edit details after opening the second page's library. No page errors were recorded. Do not assume the database lost the record or that this is an application bug until inspecting both documents.

`scripts/library-check.mjs` now logs `TWO_TAB_STATE` (both dialog open flags, contents, current metadata) just before that action and captures every remaining page's screenshot/text on failure. No application code or built assets changed for this diagnostic rerun.

At checkpoint creation, unified exec handle **93240** is the live `browser-library-02` runner. Output directory `checks/tidebound/library-02`. Re-poll this handle and inspect its JSON/log; never restart just because a poll yields. A separate read-only log command handle **68235** may still need draining. All earlier handles are confirmed terminal. Do not launch another browser suite or mutate application code while browser-02 is running.

Likely next action: inspect diagnostic state and failure screenshots. If the browser workflow requires explicit tab activation, establish that with evidence rather than changing storage rules. The repository's two-connection stale-write tests already pass. Fix the actual UI/test problem, rerun necessary gates, and then run the existing 13 browser workflows, release checks, and performance script using the central owned-server runner. Review final desktop/narrow library and gameplay screenshots.

## Still required before delivery

Pass the complete real-browser workflows; validate the existing game/browser scripts with the new load confirmations; inspect screenshots; finalize course verification and root historical notes; preserve exact original hashes; create results/spec/finite manifest; apply through the existing guarded delivery tool; audit delivered files; regenerate the four central reports, including `astradocs/FINISHED_PROJECTS_SUMMARY.md`. Do not increment completion counts or mark the full goal complete now.

Known boundaries: origin-local browser storage, no cloud/account authorization, game-only JSON exports exclude learning metadata, no guaranteed unload save, original documented route reassignment teleport simplification retained. Earlier Nethris cleanup denials remain recorded elsewhere; do not retry those deletions. No cleanup approval rejection occurred in this Tidebound work; npm cache filesystem errors are separate from automatic approval review.
