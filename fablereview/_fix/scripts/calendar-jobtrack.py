import sys, json, os, re, subprocess
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'calendar-jobtrack'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# --- review #3: version paragraph + test for version 0
fe.append_section(S, '02', '## The version check: `!==`, not `>`', """`parseBackup` (`src/lib/backup.ts:61`) rejects any backup whose `version` is not exactly `BACKUP_VERSION`. The obvious alternative, `version > BACKUP_VERSION`, would accept older files, which sounds friendlier but is a promise this code cannot keep: an older file has an older shape, and `validateBackupRecords` only knows the current one. Two terms to keep apart: **backward compatibility** means a new build can read old files (it needs a migration path); **forward compatibility** means an old build can read new files (almost never true, which is why version 99 is rejected with a clear message). The strict check is the honest choice until a `migrateBackup(candidate)` exists, whose shape would be a switch on `candidate.version` that upgrades one step at a time (`0 -> 1`, `1 -> 2`) and then hands the result to the current validator. The new test pins the lower bound: a `version: 0` file is rejected, not silently accepted as \"older is fine\".""")
def patch_test(t):
    old = """  it("rejects a backup written by a newer version", () => {"""
    new = """  it("rejects a backup written by an older version (no migration path exists)", () => {
    const result = parseBackup(
      JSON.stringify({ ...validBackup(), version: 0 }),
    );
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.error).toMatch(/version 0/);
  });

  it("rejects a backup written by a newer version", () => {"""
    assert old in t
    return t.replace(old, new, 1)
assert fe.rw('src/lib/backup.test.ts', patch_test)
done.append('review#3 02 paragraph on the strict version check (forward vs backward compatibility, migrateBackup shape); new test for version 0')

# --- review #4: categoryId exercise
fe.add_exercise(S, 'referential check on categoryId',
"""`validateBackupRecords` (`src/lib/backupValidation.ts`) checks that every event's `categoryId` is text (line 63) but not that it names one of the categories in the same file. An imported event can therefore point at a category that does not exist, and the calendar renders it without a colour.

1. Decide the policy and write it down first: **reject** the file (`events[3].categoryId "abc" is not a category in this backup`), or **remap** dangling ids to a default category. Reject is simpler and keeps the file the source of truth; remap is friendlier but silently changes data.
2. Implement reject in `validateBackupRecords`: build a `Set` of `categories[].id` once, then check each event.
3. Add two tests to `src/lib/backup.test.ts`: a backup whose event references a missing category is rejected with the path in the message; a backup whose categories include it is accepted.
4. Write one sentence in `06` on why the check belongs in validation rather than in `replaceCalendar`.""",
"""Reference (reject policy):

```ts
const categoryIds = new Set(value.categories.map((c: { id: string }) => c.id));
for (const [i, e] of value.events.entries()) {
  if (!categoryIds.has(e.categoryId))
    return `events[${i}].categoryId ${JSON.stringify(e.categoryId)} is not a category in this backup.`;
}
```

Reference test skeleton: `parseBackup(JSON.stringify({ ...validBackup(), events: [{ ...makeEvent(), categoryId: "missing" }] }))` -> `ok === false` and `error` matches `/events\\[0\\]\\.categoryId/`.

Review: the check must run before any store is replaced (validation happens in `parseBackup`, the stores are touched only in `handleImport` after `result.ok`), and the message must carry the index so a user can find the row in a large file. If you chose remap instead, show where the default category comes from and prove the original file is not modified."""); done.append('review#4 exercise 7: categoryId referential check with policy trade-off and reference test (05, 06)')

B = [
("the settings page decides what to import",
 "`src/features/settings/SettingsPage.tsx:53` `handleImport(file)` reads the file as text and calls `parseBackup`. Nothing is touched before the result is `ok`; a failure becomes a toast with `result.error` and an 8 s ttl. There is no server: the whole write path is in the browser."),
("the file is parsed and shape-checked",
 "`src/lib/backup.ts:44` `parseBackup(raw)`: `JSON.parse` in a try/catch (non-JSON -> `ok: false`), then the app signature, then `typeof candidate.version === \"number\" && candidate.version === BACKUP_VERSION` (line 61), then the presence of `events`, `applications` and a non-empty `categories`. Each failure returns a specific message; no exception escapes."),
("every record is validated",
 "`src/lib/backupValidation.ts:4` `validateBackupRecords(value)` walks settings, categories, events and applications field by field (`text`, `stamp`, enum checks) and returns the first problem as a string or `null`. It is the runtime equivalent of the TypeScript types in `Backup`, which are erased at runtime; the categoryId referential check in exercise 7 belongs here."),
("the stores are replaced",
 "Back in `handleImport`: `replaceSettings({ ...DEFAULT_SETTINGS, ...backup.settings })`, `replaceCalendar({ events, categories })`, `replaceJobs(applications)`, three separate zustand `replaceAll` actions (`src/store/*.ts`). Each replaces its slice wholesale; there is no partial merge and no undo."),
("persistence happens per store, not atomically",
 "Each zustand store persists itself to `localStorage` under its own key on change. Three replacements mean three writes; if the second throws (quota), the first has already been persisted. That is the gap exercise 3 asks you to observe and exercise 4 asks you to close with a single transactional boundary (one versioned value, or one IndexedDB transaction)."),
("the UI reflects the committed state",
 "React re-renders from the stores; the toast reports `applications.length` and `events.length` from the parsed backup, not from the stores. After a reload the page shows whatever `localStorage` holds, which is the only durable truth in this app; compare the two after a simulated failure."),
]
fe.set_boundaries(S, B); done.append('review#5 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the summary must be computed from the parsed and validated backup (counts of events, applications, categories and `exportedAt`) and shown before any `replaceAll` call; a test renders the summary for a valid file and asserts no store changed until the confirm action runs.",
"the message must carry the collection index and field name (`events[2].recurrence.interval`) produced by `validateBackupRecords`, and must not include raw file contents; assert the exact path string in a test and show that a valid file still parses.",
"stub `localStorage.setItem` to throw on the second call, import a valid file, then read all three keys back: document exactly which stores changed and which did not; the test must not assert all-or-nothing, because the current code does not provide it.",
"the design must name the single boundary (one versioned `localStorage` value or one IndexedDB transaction), show that UI state is published only after the commit resolves, and include a migration plan for existing per-store keys.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')

src = open('src/lib/backup.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
p0 = next(i for i, l in enumerate(src) if 'export function parseBackup' in l)
excerpt = '// src/lib/backup.ts:' + str(p0 + 1) + '\n' + '\n'.join(src[p0:p0 + 52])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/73/src/lib/backup.ts` with `diff --strip-trailing-cr -w`): `parseBackup` now returns a discriminated `ParseResult` instead of throwing, checks the version strictly, and hands the candidate to `validateBackupRecords` before anything is replaced. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows parseBackup')

fe.set_variations(S, """**Normal variation — round trip.** Export a backup, import it unchanged. Predict: `ok: true`, the toast reports the same counts, and `localStorage` values are byte-identical to before the import. Compare with the browser devtools Application tab.

**Invalid variation — the wrong version.** Edit the file's `version` to `0`, then to `99`. Predict the two messages (`That backup is version 0, which this build cannot read.` and the same for 99) and that no store changed. Then remove `categories`: predict which check fires first.

**Boundary variation — a failure between stores.** In the console, wrap `localStorage.setItem` so the second call throws, import a valid file, reload. Predict which of settings, calendar and jobs survived; then read chapter 7 boundary 5 and exercise 3."""); done.append('2.4 three concrete variations')

# --- review #2: repo style for the two touched files (prettier, single quote, no semi)
fixdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = ['src/lib/backup.ts', 'src/lib/backupValidation.ts', 'src/lib/backup.test.ts']
res = subprocess.run(['npx.cmd', '--yes', 'prettier@3', '--single-quote', '--no-semi', '--end-of-line', 'auto', '--write'] + [P.replace('\\', '/') + '/' + f for f in files], cwd=fixdir, capture_output=True, text=True)
print(res.stdout.strip() or res.stderr.strip()[:300])
done.append("review#2 src/lib/backup.ts, backupValidation.ts and backup.test.ts reformatted to the repository's single-quote, no-semicolon style with Prettier")
fe.append_section(S, '01', '## Code style note', """The repository uses single quotes and no semicolons (see `src/App.tsx`); the files touched by this course were reformatted to match, so a `git diff` of `src/lib/backup.ts` shows behavior, not punctuation. There is no `.prettierrc`; if you add one, use `{ "singleQuote": true, "semi": false }`.""")
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
