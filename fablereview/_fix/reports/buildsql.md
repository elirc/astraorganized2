# buildsql — fix report (B18)

Fable, 2026-09-18.

## Done
- review#1 src/App.tsx split: HomeView, WorldCard, JourneyView, MissionView, ReviewsView moved to src/views/<Name>.tsx and the shared helpers (worldTone, compactTitle, missionTitle, briefingCore, Loading, SectionTitle) to src/views/shared.tsx; App.tsx keeps routing and the workspace hook (449 lines)
- review#1 01 table points at App.tsx and src/views/; review#5 01 house-style note on multi-declarator constants
- review#3 02 ASCII chain form draft -> workspace draft -> accepted state with the function per transition
- review#4 root README first paragraph says what the project is (a React app displaying an archive, not a SQL course)
- review#2 08-BACKEND-TICKET.md scaffolds practice ticket 3 (schema with lowercased-email unique index and version, Express router with If-Match/409/428, reference 409 integration test)

## Skipped
- (none)

## Verification
- after the split: npx tsc -b exit 0, npx vitest run 3 files 43 passed, npx vite build ok (junctioned stage node_modules, removed afterwards); App.tsx is 449 lines with the five views and shared helpers in src/views/

## Course/code consistency check
- 01 table names the new files; 02 chain names putProject/useWorkspace/commit which exist; root README first paragraph added after the title.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (workspace, draft, revision, accepted data, conditional commit, conflict, validation, project status, evidence gate, self-review completion, catalog-derived count, export / import). Verified every term against the source before citing it: the files `src/contracts.ts`, `src/storage.ts`, `src/useWorkspace.ts`, `src/progression.ts`, `src/catalog.json`, `src/content-loader.ts`, and the symbols and identifiers `Workspace`, `newWorkspace`, `draft`, `useWorkspace`, `revision`, `commit`, `readWorkspace`, `commit(db, draft, expected)`, `ConflictError`, `validateWorkspace`, `validateProject`, `statuses`, `status`, `canComplete`, `completeMission`, `downloadText`, `importWorkspace`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 04, 06, 07. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **04** - src/game.test.ts (stale edits/deletes case)
- **06** - src/progression.ts (putProject)
- **07** - src/game.test.ts (due successful recall case)

No source code was changed; only the chapter Markdown.
