from pathlib import Path

root=Path(__file__).parent/'stage/19110bf39fcf'
(root/'README.md').write_text(r'''# Help Desk: reliable CRUD learning project

A local FastAPI, SQLAlchemy, SQLite, and JavaScript help desk for practicing junior-to-mid-level web development. It includes ticket creation and versioned editing, public replies and private notes, bounded attachments, customer/configuration CRUD, scoped reporting, strict request contracts, preserved migration backups, and recoverable conflict handling.

Start with the [nine-part learning course](astraupskill/README.md). The [verification record](astraupskill/VERIFICATION.md) explains tested behavior and practical limits. Older onboarding notes are retained as historical explanations of the original implementation.

## Install on Windows

Python 3.13 was used for verification. The package requires Python 3.11 or newer; other interpreter/platform combinations have not all been tested.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
.\.venv\Scripts\python.exe -m pip install --no-deps -e .
```

The lock records the tested Windows dependency versions, including test and browser tools. It is a version lock, not a set of wheel hashes. Runtime requirements and optional development/browser groups also appear in `pyproject.toml`; use `pip install -e ".[dev,browser]"` when intentionally resolving a new environment instead of reproducing the recorded one. Review and test dependency upgrades before replacing the lock.

## Choose a data directory and explicitly create accounts

For a new disposable learning session, choose a new directory. Reuse the same environment value whenever starting that session's server or storage audit.

```powershell
$env:HELPDESK_DATA_DIR = Join-Path $env:LOCALAPPDATA 'HelpDeskLearning\session-01'
.\.venv\Scripts\python.exe -m app.setup demo --acknowledge-local-only
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`. Explicit demo setup creates `admin@example.com`, `manager@example.com`, `agent@example.com`, `lightagent@example.com`, `customer@example.com`, and `integration@example.com`, with the disposable password `changeme123`. The sample bot token is `integration-token-demo`. These are public fixtures for loopback learning; no live service is contacted.

For a new owner-controlled dataset, use a different new directory and owner setup instead:

```powershell
$env:HELPDESK_DATA_DIR = Join-Path $env:LOCALAPPDATA 'HelpDeskLearning\owner-01'
.\.venv\Scripts\python.exe -m app.setup owner --name 'Learning Owner' --email 'owner@example.invalid'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Owner setup prompts for a password without putting it in command-line history. It creates one administrator and default calendar/SLA, with no demo identities. Account setup refuses to overwrite existing users. Demo setup also refuses a nonempty dataset. Normal server startup never creates known logins.

If `HELPDESK_DATA_DIR` is omitted, the original paths remain `data/helpdesk.db` and `uploads/` beneath the project. If it is set, both the database and uploads live beneath that directory. Stop the server before moving or restoring a dataset; keep its database, upload directory, and backup history together.

## Explore a complete workflow

1. Sign in as the demo administrator and create a customer in Administration.
2. Open Staff workspace, select that customer, and create a ticket.
3. Edit the subject/status, send a public reply, and add an internal note with a small attachment.
4. Open a second editor on the same record to observe a stale-version conflict and retained-draft review.
5. Use the customer account in another browser context to compare public history with staff-only content.

Ticket and customer lists support pagination and literal search. The customer selector can search by name or email. Configuration forms support full create/read/update/delete; protected references and the required default policy prevent unsafe deletion. Ticket deletion hides active access while retaining stored conversation and receipt history.

## Important API behavior

- Existing-record changes require the reviewed `If-Match` version. A missing header returns 428; a stale version returns 409.
- Staff/public ticket creation requires an `Idempotency-Key` UUID4. Keep the same key for the same draft after a lost response. Changed content with the same key returns 409.
- Email/webhook intake uses its external message identifier and a payload fingerprint. Legacy receipts without a fingerprint are preserved but cannot be blindly replayed.
- Public intake does not verify identity or overwrite an existing customer profile. It returns a minimal receipt.
- Attach at most three files, each at most 5 MiB and at most 10 MiB combined. Files are authorized downloads; there is no malware-scanning service.
- Administration PUT replaces all editable fields. Ticket PATCH preserves fields omitted from its body.

## Tests and browser verification

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe verification\verify_browser.py
.\.venv\Scripts\python.exe verification\verify_rendering.py
```

Tests use temporary databases and uploads. Browser verification creates a new disposable dataset and local server, then writes logs, results, and screenshots to a new output directory. Set `HELPDESK_BROWSER_OUTPUT` or `HELPDESK_RENDER_OUTPUT` to another new path for subsequent runs. The scripts refuse to overwrite previous evidence.

## Migration and recovery

Startup recognizes the known legacy SQLite schema, creates a consistent pre-migration backup in `migration-backups`, then adds version/fingerprint columns in a transaction. Unsupported layouts or integrity problems stop startup for review; the application does not reset them. No real database is modified by the test suite.

Inspect attachment consistency without changing files:

```powershell
.\.venv\Scripts\python.exe -m app.storage_audit
```

Ordinary failed requests roll back database work and remove their newly tracked upload files. Abrupt process termination can leave unreferenced blobs. Review the audit and your backups before deciding on recovery; it intentionally performs no automatic deletion.

This remains a local learning application. It records intake and replies but does not deliver outbound email, schedule automation workers, invite accounts, reset passwords, or provide production hosting. Those are follow-on design exercises in the course, rather than implied capabilities.
''',encoding='utf-8')
print('Updated setup, API contracts, migration/recovery and learning entry point.')
