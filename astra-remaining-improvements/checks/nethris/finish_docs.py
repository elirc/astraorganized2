from pathlib import Path
import os
import json
import hashlib

checks = Path(__file__).resolve().parent
stage = checks.parents[1] / 'stage/71e7b036865c'
baseline = json.loads((checks.parents[1] / 'baselines/71e7b036865c.json').read_text(encoding='utf-8'))['files']
for relative, digest in baseline.items():
    original = stage / 'docs/original' / (relative + '.txt')
    assert hashlib.sha256(original.read_bytes()).hexdigest() == digest, relative
count = 0
for relative in baseline:
    if relative.startswith('docs/') and relative.endswith('.md'):
        page = stage / relative
        link = os.path.relpath(stage / 'astraupskill/README.md', page.parent).replace('\\', '/')
        original = (stage / 'docs/original' / (relative + '.txt')).read_text(encoding='utf-8')
        page.write_text('> **Historical prototype documentation.** This page describes the original application or earlier proposals. Use the [current CRUD learning course](' + link + ') for the implemented workshop, setup, permissions and verification. The exact original is preserved under `docs/original`.\n\n' + original, encoding='utf-8')
        count += 1
(stage / 'README.md').write_text('''# Nethris — HRIS CRUD learning workshop

An employee directory, organization chart and time-off workflow built with React, TypeScript, .NET 10, EF Core and SQLite. The workshop is designed for junior-to-mid-level CRUD development practice.

**Start with the [nine-part learning course](astraupskill/README.md).** It includes source maps, worked changes, debugging traces, exercises, review guidance and [recorded verification](astraupskill/VERIFICATION.md).

## Run the packaged application

Prerequisites: .NET SDK 10.0.300 or a later 10.0.3xx patch (the verified SDK is 10.0.302), Node 22.16 through Node 22.x, and npm. Python is needed only for the HTTP/browser checks.

From this folder in PowerShell:

```powershell
.\\scripts\\package.ps1
.\\scripts\\start.ps1
```

Open http://127.0.0.1:5187. Create your first Admin account with a 12–128-character password. Optional fictional colleagues use that same workshop password: `employee@example.test`, `colleague@example.test`, `manager@example.test`, `hr@example.test` and `reviewer@example.test`. The application sends no email and connects to no external HR service.

The API creates `artifacts/App_Data/nethris-learning.sqlite`. Set `Hris__Database` to an absolute new path to use a separate practice database. Set `Hris__Urls` to another loopback HTTP URL if needed. Unknown existing database files are refused; original databases are not automatically migrated or reset. The package script replaces generated browser assets but does not delete the learning database.

The browser keeps its session in memory. Reloading requires sign-in. Sign out revokes the server session. An account's current role and active status are checked for every protected request.

## Develop and verify

For two-terminal development, run `dotnet run --project server/Nethris.Api --no-launch-profile`, then run `npm.cmd run dev` in `client`. Vite proxies `/api` to port 5187. The packaged application serves the same API and built assets together.

```powershell
dotnet test tests/Nethris.Tests/Nethris.Tests.csproj --no-restore
python scripts/check_api.py
python -m pip install -r scripts/requirements-browser.txt
python -m playwright install chromium
python scripts/check_browser.py
```

Both Python checks start an owned server with a fresh temporary database and stop it afterward. Results default to `.learning-results`. Build the package first. See [testing and debugging](astraupskill/04-TESTING-AND-DEBUGGING.md) for failure interpretation and optional browser executable configuration.

## Implemented behavior

- Employee, department and job-role CRUD with input validation, versions, case-insensitive uniqueness, active/archive choices and protected relationships.
- Separate Admin-only account creation, role/activity changes and password resets. HR employee editing cannot grant account privileges.
- PTO requests with quarter-hour units, bounded dates, balance reservations, overlap checks, pending edit/delete/cancel, captured-manager review and a different HR/Admin final reviewer.
- Atomic approval/balance/history writes, strong ETags, audit records and 24-hour operation receipts. The browser preserves stale drafts and supports exact retries after uncertain responses.
- Paginated lists, bounded organization traversal, role-sensitive balance/salary projections and responsive labeled forms.

This is a local single-organization workshop. It does not implement payroll, production hosting, account recovery, external notifications or approved-PTO refunds. The simplified PTO policy counts calendar dates, including weekends. See [verification and limits](astraupskill/VERIFICATION.md).

Original source and documentation are preserved as exact text in `docs/original`. Historical `docs/upskill` pages are labeled and retained for comparison; use `astraupskill` for current behavior.
''', encoding='utf-8')
ignore = (stage / '.gitignore').read_text(encoding='utf-8')
for entry in ['artifacts/', 'App_Data/', '*.sqlite', '*.sqlite-shm', '*.sqlite-wal', '.learning-results/', '__pycache__/', '*.pyc']:
    if entry not in ignore.splitlines():
        ignore += entry + '\n'
(stage / '.gitignore').write_text(ignore, encoding='utf-8')
print(json.dumps({'originalsVerified': len(baseline), 'historicalPagesMarked': count}))
