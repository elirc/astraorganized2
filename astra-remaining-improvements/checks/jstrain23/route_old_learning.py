from pathlib import Path
import os
s=Path(__file__).resolve().parents[2]/'stage/58c5c289a8ce'
for p in (s/'_learning').rglob('*.md'):
    text=p.read_text(encoding='utf-8')
    assert not text.startswith('> Historical guide')
    current=os.path.relpath(s/'astraupskill/README.md',p.parent).replace('\\','/')
    original=os.path.relpath(s/'docs/original'/str(p.relative_to(s)).replace('\\','/'),p.parent).replace('\\','/')+'.txt'
    assert (p.parent/original).exists()
    p.write_text(f'> Historical guide for the original implementation. Start with the [current CRUD learning course]({current}) for the delivered code, setup and verified behavior. The [unaltered original guide]({original}) is preserved for comparison. Claims below about autosave, sharing or collaboration describe the earlier design and should not be used as current guarantees.\n\n'+text,encoding='utf-8')
(s/'_learning/README.md').write_text('''# Learning documentation entry point

The current detailed course is [astraupskill/README.md](../astraupskill/README.md). It covers the implemented request path, SQLite transactions, revision checks, draft recovery, conflict review, typed record CRUD, worked changes, tests and progressively harder exercises.

The other documents in this folder describe the original project. They remain useful for a before/after code review, but they are marked historical because the save lifecycle, API authorization, repository and database controls have changed. Exact original text is preserved in `docs/original`, including the original package and source files. Follow the comparison links at the top of each historical guide.

Start by tracing one accepted page rename in the current application, then compare the earlier autosave effect with the new session controller. Explain why a finished HTTP request does not necessarily mean the server accepted the latest draft. Use the current verification guide for evidence and limitations; do not treat original architecture descriptions as tested guarantees.
''',encoding='utf-8')
