# astra2 — fix report (B17)

Fable, 2026-09-18.

## Done
- review#2 the fixture-gated late-game case moved to tests/late-game.fixture.test.ts, excluded from the default run and executed by npm run test:fixture; VERIFICATION restates 43 unconditional + 1 fixture-gated
- review#1 08 chapter: Express routes over the existing repository with If-Match/428 and a code-to-status table; review#3 01 note on innerHTML + exercise 6
- review#4 README time/hardware budget with the POSIX env line; review#5 evidence.json summary phrase reconciled with originalTextFilesPreserved

## Skipped
- (none)

## Verification
- npx vitest run via junctioned stage node_modules: 4 files, 43 passed (the fixture case is excluded by config); npm run test:fixture: 1 passed; npx tsc --noEmit exit 0; junction removed

## Course/code consistency check
- VERIFICATION headline now says 43 unconditional + 1 fixture-gated, matching the two runs; 08 status table uses the four VoyageError codes declared in voyages.ts; exercise 6 references voyageLibrary.ts and escape() which exist.

## Phase 3 addendum (glossary)

Added a `## Prerequisites and glossary` section to `astraupskill/README.md` with a prerequisites line and a 12-term table (record, snapshot, revision, expected revision, conflict, transaction boundary, validation, name key, typed error code, archive and restore, quota guard, origin), replacing the informal `## What you should know first` section, so there is one prerequisites section rather than two. Verified every term against the source before citing it: the files `src/voyages.ts`, `src/voyageLibrary.ts`, and the symbols and identifiers `Voyage`, `snapshots`, `snapshot(raw)`, `revision`, `VoyageRepository.write`, `edit`, `replace`, `delete`, `new VoyageError('conflict', ...)`, `this.db.transaction(['voyages', 'snapshots'], mode)`, `metadata(title, notes)`, `store.createIndex('nameKey', 'nameKey', { unique: true })`, `VoyageError`, `archive(id, revision, archived)`, `maxCheckpoints`, `maxBytes`.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 07. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **07** - src/voyages.ts (private write / revision check)

No source code was changed; only the chapter Markdown.
