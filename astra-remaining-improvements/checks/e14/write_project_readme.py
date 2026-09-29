from pathlib import Path
S=Path(__file__).resolve().parents[2]/'stage/ca549816cdd1'
text=r'''# E14 observability workshop

A local FastAPI + SQLite application for learning mid-level CRUD engineering through logs, metrics, traces and configuration workflows. Start with the [detailed learning course](astraupskill/README.md).

## Run a separate learning workspace

Use Python 3.13 or newer and run these commands from this project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
$env:OBS_DATA_DIR = Join-Path $PWD 'learning-data'
.\.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`. Expand the first-run section to bootstrap the first organization, then use ordinary login for later sessions. Choose your own credentials. The browser keeps the token in memory and requires login after a reload. The interactive API reference remains at `/docs` and loads its documentation assets from its standard CDN.

Environment variables must be set in the shell that starts the app. `.env.example` is an example, not an automatically loaded configuration file. If `OBS_DATABASE_URL` is already set in your shell, it takes precedence over `OBS_DATA_DIR`; unset it or point it explicitly at the intended learning database.

## Implemented workflows

- Browser CRUD for streams, dashboards, alerts, pipelines and saved queries, with bounded lists and explicit conflict review.
- Organization-scoped authentication, role/scope checks, current membership validation, expiring login sessions, token creation and revocation.
- Strict request and nested configuration validation, local host/origin checks, raw body limits, finite JSON and safe validation errors.
- Version-protected updates and deletes using `If-Match`, database version predicates, atomic audits and reference guards.
- Log, metric and trace ingestion with retry deduplication, transactional pipeline history, whole-batch transform failure handling and organization-scoped retention.
- Filtered searches, UTC metric buckets, a small PromQL-like language, bounded isolated SQL, trace trees and exact-trace log correlation.
- Alert evaluation with simulated notifications by default, durable pending webhook intent when explicitly configured, and a separate operator delivery command.

Dashboards store panel/query configuration; this browser does not render a charting engine. Pipeline schedules are metadata, not an active scheduler. The `/otlp/*` aliases accept this project's JSON envelopes and are not OpenTelemetry wire-protocol endpoints. User and token management remain available through the API reference.

## Editing an existing record

GET a detail endpoint such as `/api/v1/dashboards/12`. The response includes `version` and an ETag such as `"v3"`. Send that ETag in `If-Match` for PUT or DELETE. A missing header returns 428, malformed syntax returns 400, and an outdated version returns 409. Reload and review your draft before retrying. A network failure does not prove that a write failed to commit.

Lists use `limit` and `offset`, with a default page size of 20 and maximum of 100. The five CRUD lists also return `X-Total-Count`. History and identity lists are bounded as well. Offset pagination is not a snapshot of a changing database.

## Existing database migration

Existing schemas require an explicit migration. Do not delete or reset data to bypass the check. Stop application/delivery processes, create and verify a private consistent backup, point `OBS_DATABASE_URL` at the intended file, then run:

```powershell
.\.venv\Scripts\python -m app.migrate --apply
```

The migration adds version columns and uniqueness indexes. It refuses incomplete schemas, broken references, duplicate case-insensitive emails and duplicate log/metric deduplication keys. It does not silently discard historical rows. See the [backup and migration walkthrough](astraupskill/04-TESTING-AND-DEBUGGING.md). Legacy naive timestamps are interpreted as UTC; previously lost offsets cannot be reconstructed automatically.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `OBS_DATA_DIR` | `./data` | Directory used to derive the default database path |
| `OBS_DATABASE_URL` | SQLite file under data directory | Explicit path overrides data directory |
| `OBS_QUERY_ROW_LIMIT` | 1000 | Returned query row cap |
| `OBS_QUERY_SCAN_LIMIT` | 50000 | Source row scan cap |
| `OBS_QUERY_TIMEOUT_MS` | 5000 | Isolated SQL execution budget |
| `OBS_INGEST_MAX_PAYLOAD_BYTES` | 1048576 | Per-ingestion batch limit, also constrained by the stream |
| `OBS_REQUEST_MAX_BYTES` | 2097152 | Raw HTTP request limit before parsing |
| `OBS_RATE_LIMIT_PER_MINUTE` | 600 | In-process ingestion limit per token/stream |
| `OBS_SESSION_DAYS` | 7 | New bootstrap/login session lifetime |
| `OBS_ALLOW_NOTIFICATIONS` | 0 | Enable queuing real webhook intent; evaluation still does not send |
| `OBS_WEBHOOK_HOSTS` | empty | Comma-separated exact allowed webhook hostnames |

Explicit API-created tokens default to 30 days and can specify their own allowed expiry. Existing tokens retain their stored expiry. Legacy ingest tokens with excessive permissions require rotation to explicit telemetry write scopes. Token last-use timestamps are historical fields and are not updated on each authenticated read.

## Notification outbox

Keep the default simulated mode for learning. With explicit opt-in and a hostname allowlist, evaluating a triggered webhook alert records a pending delivery. An operator may send one pending item with `python -m app.deliver --apply --delivery-id <id>`. This command makes a real external request; it is not necessary for the course.

The sender accepts HTTPS on port 443, rejects credentials/fragments, rejects non-public DNS results, connects to the checked address with hostname-validated TLS, does not follow redirects, and bounds the response. It claims the delivery before sending. Uncertain outcomes and crashed `sending` claims require investigation; they are not automatically retried. No real provider request was made during the recorded verification.

## Verify and learn

```powershell
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python -m ruff check app tests scripts
.\.venv\Scripts\python -m ruff format --check app tests scripts
.\.venv\Scripts\python -m playwright install chromium
.\.venv\Scripts\python scripts/check_browser.py --output browser-results-01
```

The browser output directory must be new. Tests use temporary databases. Read [verification and practical limits](astraupskill/VERIFICATION.md) for the recorded evidence. This is a local single-node learning application, without public deployment hardening, account recovery, distributed scheduling or a production message-delivery service.

The [original onboarding notes](docs/onboarding/01-reading-order.md) remain available with historical notices. Exact pre-change text is preserved under `docs/original/`; use the new course for current behavior.
'''
(S/'README.md').write_text(text,encoding='utf-8')
for p in (S/'docs/onboarding').rglob('*.md'):
    original=p.read_text(encoding='utf-8')
    assert not original.startswith('> Historical')
    relative='../'*(len(p.relative_to(S).parts)-1)+'astraupskill/README.md'
    p.write_text('> Historical onboarding note: this describes the original MVP. Read the [current learning course]('+relative+') for the revised CRUD, authorization, migration and transaction behavior. Exact original text is preserved under `docs/original/`.\n\n'+original,encoding='utf-8')
print('Updated README and marked nine original onboarding files as historical')
