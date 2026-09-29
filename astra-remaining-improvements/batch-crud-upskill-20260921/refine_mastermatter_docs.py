from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/f5bd710b171f/astraupskill'
for f in P.glob('*.md'):
    t=f.read_text(encoding='utf-8-sig')
    t=t.replace('The old helper treated zero as success,','The old inline greater-than-one check allowed zero to fall through as success,')
    t=t.replace('the verification chapter records the unavailable tool.','the verification chapter distinguishes the historical launch failure, the source-method harness, and unexecuted native integration checks.')
    t=t.replace('The unavailable Go executable is a limitation, not a reason to claim execution.','The portable compiler enables a separate source-method harness; it does not establish that the native Mattermost package or database tests passed.')
    t=t.replace('python tests/crud-b02/run_channel_store_harness.py --go <portable-go>/go.exe','python mattermost/tests/crud-b02/run_channel_store_harness.py --go <path-to-go.exe>')
    t=t.replace('The portable source-method harness is:', 'From this project root, the portable source-method harness is:')
    t=t.replace('The current portable command is:', 'From this project root, the portable command is:')
    t=t.replace('A database driver reports the number of rows matched and changed.','The PostgreSQL update result reports an affected-row count; a successful SQL execution alone does not prove that a row existed.')
    if f.name=='02-CONCEPTS.md':
        t+='\nInspect [the supported-driver validation](../mattermost/server/public/model/config.go): SqlSettings.isValid accepts DatabaseDriverPostgres. Keep that repository fact separate from generic matched-versus-changed behavior in other database products. The harness provides RowsAffected values deliberately; it does not connect to PostgreSQL or validate driver behavior. A native integration case should update an existing channel with unchanged business fields as well as a missing id, and assert the returned resource and public projection state.\n'
    if f.name=='06-SOLUTIONS-AND-REVIEW.md':
        t+='\nThe delete extension has a policy-dependent answer: an idempotent delete can accept zero when the desired absence already holds, while a strict resource endpoint can report not-found. Neither policy justifies creating a public projection from a failed primary update. State the caller contract before transferring this rule to another CRUD operation. For grading, give full credit only when the answer distinguishes a source trace from an executed transaction test and names a concrete assertion for each.\n'
    f.write_text(t,encoding='utf-8')
