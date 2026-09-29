from pathlib import Path

S = Path(__file__).resolve().parents[2] / 'stage/4de416cd300b'
p = S / 'README.md'
t = p.read_text(encoding='utf-8')
t = t.replace('## Run', '## Learn CRUD engineering here\n\nStart with the [nine-part learning course](astraupskill/README.md). The voyage library demonstrates versioned records, atomic persistence, runtime validation, stale-edit recovery, archive/delete workflows, and meaningful regression tests in the existing game.\n\n## Run', 1)
a, b = t.index('## Saving'), t.index('## Verify')
t = t[:a] + '''## Saving and the voyage library

Saves live in browser IndexedDB, separately for each origin. Development port 5180 and preview port 5181 therefore have separate collections. Export and import game snapshots to move a voyage between origins or devices. Checkpoint titles and learning notes stay in the library; a game JSON export does not include that metadata.

Settings contains the manual slot, automatic slot, game import/export, seeded new-game creation, and the voyage library. The library pauses the simulation and lets you create named checkpoints, search titles/notes/seeds, edit details, replace a checkpoint's world, archive/restore, export, and permanently delete archived checkpoints. It holds up to 50 checkpoints including archived entries, with a 5 MB per-snapshot limit and a 50 MB aggregate snapshot limit. The browser may impose a lower practical quota.

Updates and deletions require the saved revision the editor read. A competing tab cannot silently overwrite that version. On conflict, keep your draft, review the latest entry, or preserve your active experiment as a separate checkpoint. Automatic and manual slots are protected from rename/archive/delete. Archived checkpoints retain their names and can be restored.

World changes from a manual load, a checkpoint load, an import, or a new game use an explicit confirmation. Replacement of the active world requires a committed automatic save first. Invalid imports and failed writes retain the active world. Loading the automatic slot explicitly also lets a tab review its latest stored version after a conflict.

Valid old localStorage slots are copied when their new slot is absent. Existing localStorage keys are never changed or deleted by this version. Damaged legacy data is left untouched and reported. If storage is unavailable, the game can still run and export; local saves are disabled.

Autosave runs every 30 seconds, with a best-effort attempt when the page becomes hidden. Wait for a saved status or export before relying on recent progress. An asynchronous database write is not guaranteed to finish during browser shutdown. Clearing browser data, browser eviction, device loss, or changing origins can make local records unavailable. Keep exported copies of important experiments.

''' + t[b:]
t = t.replace('npm run test:performance\n', 'npm run test:performance\n', 1)
t = t.replace('The browser helper uses installed Chrome/Chromium', '''The library regression script starts and stops its own production preview on an available loopback port. Build first, then run:

```sh
npm run build
npm run test:library
```

It uses isolated browser contexts and synthetic data. Set `TIDEBOUND_EVIDENCE_DIR` to choose a fresh evidence directory; its default is `artifacts/library`. It does not use your personal browser profile. Review the [current verification record](astraupskill/VERIFICATION.md) for checked behavior and remaining gates.

The browser helper uses installed Chrome/Chromium''')
p.write_text(t, encoding='utf-8')

p = S / 'ARCHITECTURE.md'
t = p.read_text(encoding='utf-8')
t = t.replace('`src/main.ts` owns DOM views, action routing, local save slots, exports/imports, notifications, keyboard controls and the fixed-step application loop.', '`src/main.ts` owns DOM views, action routing, versioned manual/automatic save integration, exports/imports, notifications, keyboard controls and the fixed-step application loop.')
t += '''
## Voyage library and current learning work

`src/voyages.ts` owns IndexedDB access. The `voyages` store holds bounded metadata and a unique normalized-title index. `snapshots` holds serialized worlds. A shared readwrite transaction compares the expected revision and commits metadata and payload changes together. Readonly transactions validate stored records and worlds before returning them. Slots are protected records; checkpoint archive and delete rules live in the repository.

`src/voyageLibrary.ts` owns the dialog, search/pagination state, selected revision, retained draft text, confirmation views and operation feedback. It uses a native modal dialog and escapes user text. It does not directly write browser storage. `src/voyages.css` defines its responsive layout and focus styles.

The main application serializes its own slot operations through a promise queue and invalidates old queued snapshots when the active world changes. Revision checks remain necessary because another page has a separate queue. Legacy localStorage keys are read for initial adoption and preserved. Storage failures and conflicts do not trigger unconditional retries or silent replacement of a draft.

The original release's coordination and performance sections above are historical context. The current improvement's learning path and verification are in `astraupskill/README.md` and `astraupskill/VERIFICATION.md`; original text snapshots are in `docs/original`.
'''
p.write_text(t, encoding='utf-8')

for name in ['VERIFICATION.md', 'PLAN.md', 'HANDOFF.md', 'DECISIONS.md', 'PROJECT_SPEC.md']:
    p = S / name
    t = p.read_text(encoding='utf-8')
    notice = '> Historical original-game document. Current voyage-library changes and their verification are documented in [the learning course](astraupskill/README.md) and [its verification record](astraupskill/VERIFICATION.md). The exact original version of this document is preserved in [docs/original/' + name + '](docs/original/' + name + ').\n\n'
    p.write_text(notice + t, encoding='utf-8')

p = S / 'scripts/browser-check.mjs'
t = p.read_text(encoding='utf-8')
load = " await page.locator('.save-slot').filter({hasText:'Captain’s save'}).getByRole('button',{name:'Load',exact:true}).click();"
t = t.replace(load, load + "\n await page.getByRole('button',{name:'Load saved voyage',exact:true}).click();")
save = " await page.locator('.save-slot').filter({hasText:'Captain’s save'}).getByRole('button',{name:'Save',exact:true}).click();"
t = t.replace(save, save + "\n await expect(page.locator('.toast').last()).toContainText('saved');\n" + load + "\n await page.getByRole('button',{name:'Load saved voyage',exact:true}).click();\n await expect(page.locator('.toast').last()).toContainText('Welcome back');\n await page.getByRole('button',{name:'Settings',exact:true}).click();")
line = " await expect(page.locator('.toast').last()).toContainText('arrived safely',{timeout:15000});"
t = t.replace(line, " await page.getByRole('button',{name:'Import this voyage',exact:true}).click();\n" + line)
p.write_text(t, encoding='utf-8')
p = S / 'scripts/performance-check.mjs'
t = p.read_text(encoding='utf-8')
t = t.replace(line, " await page.getByRole('button',{name:'Import this voyage',exact:true}).click();\n" + line)
p.write_text(t, encoding='utf-8')
print('Updated current documentation and existing browser scripts for confirmed loads/imports.')
