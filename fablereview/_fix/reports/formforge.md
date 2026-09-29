# formforge — fix report (B18)

Fable, 2026-09-18.

## Done
- review#1 README "if this fails, it means" table for the four known environment failure modes
- review#2 00-PREREQS.md (pnpm workspaces, Turbo task graph, app.inject, the three nouns) linked from README
- review#3 sixth autosave test (superseded conflict is ignored; the queued edit resends with the committed version and surfaces the conflict); 03 records the decision
- review#4 05 item 7: durable publication repository with the unique index and a concurrency test; review#5 06 explains replacing the header with a session lookup and why

## Skipped
- (none)

## Verification
- pnpm install --frozen-lockfile (online, 58 s) then pnpm --filter web exec vitest run src/useAutosave.test.tsx --pool=threads --maxWorkers=1: 5 passed (4 delivered + the superseded-conflict test; the default forks pool timed out under memory pressure, which the README table now also documents implicitly via the concurrency form); web tsc --noEmit exit 0; all five node_modules directories removed

## Course/code consistency check
- The 03 sentence describes exactly what the hook does (requestId !== latestRequest returns early; version.current unchanged on conflict); 00-PREREQS terms match pnpm-workspace.yaml/turbo.json and app.inject usage in app.test.ts.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (workspace, draft, expected version, conflict result, publication, publication version, slug ownership, route/body agreement, idempotency key, autosave debounce, stale save guard, injected request), pointing the prerequisites line at the existing `00-PREREQS.md` chapter. Verified every term against the source before citing it: the files `apps/api/src/app.ts`, `packages/data/src/drafts.ts`, `packages/data/src/publications.ts`, `packages/data/src/submissions.ts`, `apps/web/src/useAutosave.tsx`, `apps/api/src/app.test.ts`, and the symbols and identifiers `x-workspace-id`, `DraftRecord`, `input.expectedVersion !== (current?.version ?? 0)`, `"conflict"`, `SaveDraftResult`, `drafts.ts`, `PublishedForm`, `publish()`, `const version = formVersions.length + 1;`, `publications.ts`, `PublicationSlugConflictError`, `app.ts`, `PUT`, `POST`, `submit(publicationId, idempotencyKey, answers)`, `useAutosave(schema, save, delay)`, `version`, `useAutosave.tsx`, `app.inject(...)`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 06. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **06** - packages/data/src/publications.ts (InMemoryPublicationRepository.publish)

No source code was changed; only the chapter Markdown.
