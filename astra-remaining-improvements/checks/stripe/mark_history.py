from pathlib import Path
from urllib.parse import quote
import os
root=Path(__file__).resolve().parents[2]/'stage/af19f6e32dba'
count=0
for folder in [root/'docs/upskill',root/'docs2']:
    for path in folder.rglob('*.md'):
        text=path.read_text(encoding='utf-8')
        if text.startswith('> Historical implementation notes.'):continue
        current=quote(os.path.relpath(root/'astraupskill/README.md',path.parent).replace('\\','/'),safe='/')
        original=quote(os.path.relpath(root/'docs/original'/(path.relative_to(root).as_posix()+'.txt'),path.parent).replace('\\','/'),safe='/')
        assert (root/'docs/original'/(path.relative_to(root).as_posix()+'.txt')).is_file()
        banner=f'> Historical implementation notes. This page describes the original in-memory, unauthenticated .NET 8 version; its commands, links and planned features may differ from the current application. Use the [current verified learning course]({current}) for executable guidance. [Exact original text]({original}).\n\n'
        path.write_text(banner+text,encoding='utf-8');count+=1
(root/'docs/original/README.md').write_text('''# Original project snapshot

The 125 original text files were copied byte-for-byte before implementation changes. Their relative paths are preserved and `.txt` is appended, so old source is available for comparison without being compiled.

Examples: [original README](README.md.txt), [original API](src/Billing.Api/Program.cs.txt), [original billing engine](src/Billing.Api/Infrastructure/BillingEngine.cs.txt), [original React screen](src/Billing.Web/src/App.tsx.txt).

These files describe an older .NET 8, in-memory, unauthenticated simulator. They are historical evidence, not current setup instructions. Start with the [current learning course](../../astraupskill/README.md).

No application database, dependency directory, live credentials or build output was included. The original configuration contained only the documented placeholder webhook secret. The delivered application generates a private secret per workspace.
''',encoding='utf-8')
print(f'Marked {count} historical pages and added the snapshot index.')
