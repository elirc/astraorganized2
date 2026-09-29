from pathlib import Path
import json
B=Path(__file__).resolve().parent;P=B/'stage/d9a27fa7f308'
p=P/'README.md';s=p.read_text(encoding='utf-8').replace('''1. creates the `data` directory if needed
2. opens the file
3. writes a small header comment
4. writes one expense per line''','''1. snapshots and validates the collection, then serializes every record
2. creates the destination directory if needed
3. writes the header and records to a temporary sibling file
4. atomically replaces the destination, or reports a save error without a non-atomic fallback
5. cleans up a leftover temporary file''')
s=s.replace('Reads the file line by line, skips blank lines and comments, converts lines into expenses, and returns the list.', 'Reads original record lines, skips blank lines and comments, rejects any malformed or duplicate record with an IOException, and returns only a completely validated list.')
s=s.replace('6. returns the loaded list to the manager','6. rejects the entire load on a malformed or duplicate record; otherwise returns the complete list to the manager')
p.write_text(s,encoding='utf-8')
spec={'changedFiles':['README.md','run.ps1','src/expensetracker/App.java','src/expensetracker/Expense.java','src/expensetracker/ExpenseManager.java','src/expensetracker/ExpenseFileStorage.java','test/expensetracker/RegressionTests.java'],
'summary':['Empty optional notes survive saved-file reload; malformed, invalid-precision and duplicate records reject the whole load without an exit-time overwrite.','Saving validates and serializes before writing a temporary sibling and atomically replacing the destination, with failed-move cleanup.','Complete CRUD adds immutable replacement updates and confirmed CLI deletion; failed commands preserve existing state and totals.','Shared domain precision/category validation, guarded ID allocation, snapshot loading and graceful EOF strengthen the foundational service boundaries.','A portable Java 17 runner and nine detailed learning documents cover actual source, failure traces, worked changes, regression reasoning and progressive CRUD web API exercises.'],
'checks':{'format':'json','resultsFile':'checks/j5/results.json','expectedTests':28,'command':'run.ps1 -Test; five separate-process CLI scenarios','environment':'Microsoft OpenJDK 17.0.10; --release 17 -Xlint:all; real temporary files; isolated project copy'},
'limits':['CLI only; HTTP, browser UI, database and authenticated owner scoping are proposed exercises.','Save-on-exit can lose unsaved edits after forced termination; no cross-process coordination or power-loss durability guarantee.','IDs can be reused after deleting the highest record and restarting; exhaustion does not wrap.','Atomic replacement is required; unsupported filesystems fail visibly. Strict loading requires manual repair of corrupt copies.','CLI diagnostics are printed; structured failure exit codes are not yet implemented.']}
(B/'specs/d9a27fa7f308.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
