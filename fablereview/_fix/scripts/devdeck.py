import sys, json, os, re
sys.path.insert(0, r'C:\Users\Owner\Desktop\AstraOrganized2\fablereview\_fix')
import fable_edit as fe
S = 'devdeck'
P = fe.REG[S]['abs']
os.chdir(P)
done = []

# --- review #3: consistent braces in the discount snippet, within the 12-line rule
def patch_cq(t):
    old = 'code: "function discount(user) {\\n  if (user) {\\n    if (user.isActive) {\\n      if (user.orders > 10) return 0.2;\\n      else return 0.05;\\n    } else {\\n      return 0;\\n    }\\n  } else {\\n    return 0;\\n  }\\n}",'
    new = 'code: "function discount(user) {\\n  if (user) {\\n    if (user.isActive) {\\n      if (user.orders > 10) { return 0.2; }\\n      else { return 0.05; }\\n    } else { return 0; }\\n  } else { return 0; }\\n}",'
    assert old in t, 'discount snippet not found'
    return t.replace(old, new, 1)
assert fe.rw('src/content/code-quality.ts', patch_cq)
done.append('review#3 discount(user) snippet now uses braces consistently (8 lines, within the 12-line content rule); the nesting the card teaches is unchanged')

# --- review #4: third delta test for the settings branch
def patch_test(t):
    add = '''
it("rejects a settings block whose enabled card types or deck ids are malformed", async () => {
  const { validateImport } = await import("./importValidation");
  const base = { exportedAt: Date.now(), states: [], logs: [], settings: { enabledCardTypes: ["concept"], enabledDeckIds: ["deck-1"] } } as any;
  expect(validateImport({ ...base, settings: { ...base.settings, enabledCardTypes: ["not-a-type"] } })).not.toBeNull();
  expect(validateImport({ ...base, settings: { ...base.settings, enabledDeckIds: [42] } })).not.toBeNull();
  expect(validateImport({ ...base, settings: { ...base.settings, enabledCardTypes: "concept" } })).not.toBeNull();
});
'''
    return t.rstrip('\n') + '\n' + add
assert fe.rw('src/importValidation.test.ts', patch_test)
done.append('review#4 third delta test covers the enabledCardTypes / enabledDeckIds settings branch of validateImport')

# --- review #5: transfer paragraph + README relabel
fe.append_section(S, '02', '## What this maps to on a server', """Everything in this course happens in the browser, but each idea has a one-to-one server equivalent that you will meet in the Express and .NET courses:

| here (DevDeck) | on a server |
|---|---|
| `validateImport` returning a message before any write | Zod (`validateBody`) or `parseItem` at the Express boundary, answering 400 before the handler |
| `db.transaction("rw", [...tables], fn)` in `src/db.ts` | `BEGIN ... COMMIT` / `ROLLBACK` around several statements (`withTransaction`, Knex `db.transaction`) |
| clearing progress then re-inserting inside one transaction | `DELETE` + `INSERT` in one transaction so a failure leaves the old rows |
| reading `states` after the import to render | re-fetching after a mutation instead of trusting the response |
| the missing piece: nobody else can write while you import | `SELECT ... FOR UPDATE` or a row lock, which IndexedDB gives you implicitly per transaction |

Treat this course as *runtime validation + client-side transactions*; the exercises transfer directly, the storage API does not.""")
fe.rw(fe.chapter(S, 'README'), lambda t: t.replace('# ', '# ', 1) if False else t.replace('\n## Reading and practice order', '\n**Learning-path label:** runtime validation + client-side transactions (an elective; the same shapes appear on the server in the Express and .NET courses, see chapter 2).\n\n## Reading and practice order', 1))
done.append('review#5 02 maps each idea to its server equivalent; README carries the learning-path label')

B = [
("the settings screen hands over a file",
 "`src/screens/Settings.tsx:128-136`: a hidden `<input type=\"file\" accept=\"application/json\">` whose `onChange` calls `onImportFile(file)` and immediately clears `e.target.value` so the same file can be chosen twice. Nothing is parsed here."),
("the store reads and parses the file",
 "`src/store.ts:292` `importBackup(file)`: `await file.text()`, then `JSON.parse(text) as ExportData`. The cast is a lie the compiler accepts; the real check is the next boundary. A file that is not JSON throws here and the UI shows the error."),
("the payload is validated before any write",
 "`src/importValidation.ts:3` `validateImport(payload)` checks `exportedAt`, every review state and log (types, ranges, duplicate card ids) and the `settings` block (`enabledCardTypes` against `ALL_CARD_TYPES`, `enabledDeckIds` as strings, lines 68-71). It returns a message or `null`; `importData` refuses to run when it is not `null`. The three tests in `src/importValidation.test.ts` exercise exactly this function."),
("the database applies the import in one transaction",
 "`src/db.ts:166` `importData(payload, now)` opens `db.transaction(\"rw\", [reviewStates, reviewLogs, ...], ...)` (Dexie), clears the progress tables, re-inserts the validated states and logs, and skips logs for unknown cards. A throw inside the callback aborts the whole transaction: exercise 3 forces that and checks the old rows survive."),
("the store re-reads and publishes",
 "Back in `importBackup`: `seedAndLoad(now)` re-reads the database (bundled cards plus restored states) and `set({ states, settings, meta })` publishes the new snapshot to React. The UI never sees the parsed file directly; it sees what the database committed."),
("the screen reports what happened",
 "`importBackup` returns `Restored progress for N cards.`; the Settings screen shows it, or the thrown error's message for a rejected file. Because the count comes from `importData`'s return value, it reflects rows written, not rows in the file."),
]
fe.set_boundaries(S, B); done.append('review#2 / 2.2 six distinct trace-lab boundaries (07)')

R = [
"the preview must call `validateImport` first and compute the three counts (restored = states whose card exists, ignored = logs for unknown cards, recreated = bundled cards with no state) without opening a transaction; a test asserts the counts for a fixture with one unknown card and that `importData` was not called.",
"the explanation must trace one scheduler field (`intervalDays`, `due` or `status`) through an existing test with a fixed clock, showing the before and after values for `Again` versus `Good`; it must reference the actual function in `src/scheduler.ts` and match the numbers the test asserts.",
"use a `Dexie` hook or an invalid operation inside `importData`'s callback to throw after the clear, then compare every affected table with the original export; the test must show the old rows are still there, and you must name the Dexie mechanism (transaction abort) that made it so.",
"the design must separate bundled cards from learner-created cards (a `source` field or a separate table), keep `seedAndLoad` from overwriting custom cards, give custom cards a stable id that survives export and import, and state how progress references a card that was later edited.",
]
fe.set_reviews(S, R); done.append('2.3 per-exercise review criteria (06)')

iv = open('src/importValidation.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
dbs = open('src/db.ts', encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
i0 = next(i for i, l in enumerate(dbs) if 'export async function importData' in l)
excerpt = '// src/importValidation.ts:3\n' + '\n'.join(iv[2:30]) + '\n\n// src/db.ts:' + str(i0 + 1) + '\n' + '\n'.join(dbs[i0:i0 + 26])
fe.set_excerpt(S, "The lines below are the ones Astra changed (compare `AstraOrganized2/astrafinalplan/implementation/batch04/backups/74/src` with `diff -r --strip-trailing-cr -w`): `validateImport` is the pure pre-replacement validator, and `importData` runs the clear-and-restore inside one Dexie transaction. The linked source is authoritative if you later edit the project.", excerpt, 'typescript'); done.append('2.4 excerpt shows validateImport and importData')

fe.set_variations(S, """**Normal variation — round trip.** Export progress, import the same file. Predict `Restored progress for N cards.` with N equal to the number of states in the file, and identical `due` values afterwards (read them in the Application tab, IndexedDB).

**Invalid variation — a duplicated card id.** Duplicate one entry in `states` in the exported file and import it. Predict the message from `validateImport` and that IndexedDB is unchanged (no transaction was opened). Then set `settings.enabledCardTypes` to `[\"nope\"]`: predict the new test's outcome.

**Boundary variation — a failure after the clear.** In a scratch copy, throw inside `importData` after the clear (or reproduce exercise 3). Predict: the old states are still present after the error, because Dexie aborted the transaction; then remove the transaction wrapper and repeat to see the progress vanish. Restore it."""); done.append('2.4 three concrete variations')
fe.rw(fe.chapter(S, 'VERIFICATION'), lambda t: t.replace("Automated test cases: **2 delivered by this change**", "Automated test cases: **2 delivered by this change** plus **1** added in the fix pass (settings branch)", 1))
json.dump(done, open(os.path.join(os.path.dirname(__file__), S + '.done.json'), 'w'))
print('\n'.join(done))
