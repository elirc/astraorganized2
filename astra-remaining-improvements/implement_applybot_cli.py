from pathlib import Path
s=Path('astra-remaining-improvements/stage/da9c28730758')
(s/'applybot/tracker.py').write_text('''"""SQLite tracking plus visible, explicitly imported legacy JSONL history."""
from __future__ import annotations

from pathlib import Path

from .application_store import ApplicationStore, StoreError
from .legacy_history import parse_legacy_history

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
HISTORY_FILE = DATA_DIR / "applications.jsonl"
DATABASE_FILE = DATA_DIR / "applications.sqlite3"


def log_application(url: str, company: str | None, title: str | None, status: str) -> None:
    ApplicationStore(DATABASE_FILE).create({"url": url, "company": company or "Unknown company", "title": title or "Untitled role", "status": status, "notes": ""})


def _as_history(row: dict) -> dict:
    return {**row, "timestamp": row["created_at"]}


def read_history(limit: int = 1000) -> list[dict]:
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 10000:
        raise StoreError("History limit must be between 1 and 10000.")
    records, imported = [], set()
    if DATABASE_FILE.exists():
        store = ApplicationStore(DATABASE_FILE)
        imported = store.imported_receipts()
        with store.connection() as db:
            records.extend(_as_history(dict(row)) for row in db.execute("SELECT * FROM applications ORDER BY created_at DESC,id LIMIT ?", (limit,)))
    if HISTORY_FILE.exists():
        records.extend({**record.data, "timestamp": record.timestamp, "legacy": True} for record in parse_legacy_history(HISTORY_FILE) if record.receipt not in imported)
    records.sort(key=lambda record: record["timestamp"], reverse=True)
    return records[:limit]


def prior_applications(url: str) -> list[dict]:
    records, imported = [], set()
    if DATABASE_FILE.exists():
        store = ApplicationStore(DATABASE_FILE)
        records.extend(_as_history(row) for row in store.find_by_url(url))
        imported = store.imported_receipts()
    if HISTORY_FILE.exists():
        records.extend({**record.data, "timestamp": record.timestamp} for record in parse_legacy_history(HISTORY_FILE) if record.receipt not in imported and record.data["url"] == url and record.data["status"] == "applied")
    return sorted(records, key=lambda record: record["timestamp"])


def print_history(limit: int = 200) -> None:
    records = read_history(limit)
    if not records:
        print("No applications logged yet.")
        return
    print(f"Showing up to {limit} most recent records (SQLite plus unimported legacy history).")
    print(f"{'When':<22} {'Status':<12} {'Company':<28} Title / URL")
    print("-" * 100)
    for record in records:
        when = record["timestamp"][:19].replace("T", " ")
        print(f"{when:<22} {record['status']:<12} {record['company'][:27]:<28} {record['title'][:60]}")
    if any(record.get("legacy") for record in records):
        print("Legacy rows are visible here. Use import-history to add them to the web dashboard.")
    print(f"{len(records)} records shown.")
''',encoding='utf-8')
p=s/'applybot/cli.py';t=p.read_text(encoding='utf-8').replace('from dotenv import load_dotenv\n','').replace('from . import llm, tracker','from . import tracker\nfrom .application_store import ApplicationStore, StoreError, application_input').replace('from .browser import Browser\n','').replace('from .profile import load_profile, profile_as_yaml\n','')
t=t.replace('def cmd_history(_: argparse.Namespace) -> None:\n    tracker.print_history()', 'def cmd_history(args: argparse.Namespace) -> None:\n    tracker.print_history(args.limit)')
t=t.replace('def cmd_apply(args: argparse.Namespace) -> None:\n    profile', '''def cmd_apply(args: argparse.Namespace) -> None:
    from . import llm
    from .browser import Browser
    from .profile import load_profile, profile_as_yaml

    application_input({"url": args.url, "company": "Unknown company", "title": "Untitled role", "status": "queued"})
    profile''')
t=t.replace('''    prior = [r for r in tracker.read_history()
             if r.get("url") == args.url and r.get("status") == "applied"]''','''    prior = tracker.prior_applications(args.url)''')
t=t.replace('''    except KeyboardInterrupt:
        print("\\nInterrupted.")
    finally:
        if not logged and (company or job_title):
            tracker.log_application(args.url, company, job_title, "incomplete")
        browser.close()''','''    except (KeyboardInterrupt, EOFError):
        print("\\nInput ended. The browser will close.")
    finally:
        try:
            if not logged and (company or job_title):
                tracker.log_application(args.url, company, job_title, "incomplete")
        finally:
            browser.close()''')
t=t.replace('    load_dotenv(PROJECT_ROOT / ".env")', '''    try:
        from dotenv import load_dotenv
    except ImportError:
        pass  # The tracker/dashboard only requires Python's standard library.
    else:
        load_dotenv(PROJECT_ROOT / ".env")''')
t=t.replace('    p_hist.set_defaults(func=cmd_history)', '''    p_hist.add_argument("--limit", type=int, default=200, help="Show up to 10000 recent records")
    p_hist.set_defaults(func=cmd_history)

    p_dashboard = sub.add_parser("dashboard", help="Open the local application-tracking web app")
    p_dashboard.add_argument("--data-dir", default=str(PROJECT_ROOT / "data"))
    p_dashboard.add_argument("--port", type=int, default=8421)
    p_dashboard.set_defaults(func=cmd_dashboard)

    p_import = sub.add_parser("import-history", help="Validate and explicitly import legacy JSONL history")
    p_import.add_argument("--file", default=str(PROJECT_ROOT / "data" / "applications.jsonl"))
    p_import.add_argument("--data-dir", default=str(PROJECT_ROOT / "data"))
    p_import.add_argument("--dry-run", action="store_true", help="Validate without opening or writing a database")
    p_import.set_defaults(func=cmd_import_history)

    p_backup = sub.add_parser("backup", help="Create a consistent SQLite backup in a new file")
    p_backup.add_argument("--data-dir", default=str(PROJECT_ROOT / "data"))
    p_backup.add_argument("--output", required=True)
    p_backup.set_defaults(func=cmd_backup)''')
t=t.replace('    args.func(args)', '''    try:
        args.func(args)
    except (StoreError, ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1) from None''')
a=t.index('def main(argv:');t=t[:a]+'''def cmd_dashboard(args: argparse.Namespace) -> None:
    from .dashboard import run_dashboard
    if not 0 <= args.port <= 65535:
        raise StoreError("Port must be between 0 and 65535.")
    run_dashboard(args.data_dir, args.port)


def cmd_import_history(args: argparse.Namespace) -> None:
    from .legacy_history import parse_legacy_history
    records = parse_legacy_history(args.file)
    if args.dry_run:
        print(f"Validated {len(records)} legacy records. No database was opened or changed; duplicate receipts are checked during import.")
        return
    result = ApplicationStore(Path(args.data_dir) / "applications.sqlite3").import_history(records)
    print(f"Imported {result['created']} records; skipped {result['skipped']} previously imported occurrences. Original JSONL was not changed.")


def cmd_backup(args: argparse.Namespace) -> None:
    path = Path(args.data_dir) / "applications.sqlite3"
    if not path.exists():
        raise StoreError("No tracker database exists at this data directory.")
    store = ApplicationStore(path)
    store.backup(args.output)
    print("Consistent tracker backup created in the requested new file.")


'''+t[a:];p.write_text(t,encoding='utf-8')
p=s/'applybot/application_store.py';t=p.read_text(encoding='utf-8');t+='''
    def backup(self, destination: str | Path) -> None:
        """Use SQLite backup so committed WAL contents are included."""
        import os
        target = Path(destination).resolve()
        descriptor = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(descriptor)
        try:
            with self.connection() as source:
                backup = sqlite3.connect(target)
                try:
                    source.backup(backup)
                finally:
                    backup.close()
        except BaseException:
            target.unlink(missing_ok=True)  # This call exclusively created this new file.
            raise
''';p.write_text(t,encoding='utf-8')
# Truthful handling of absent answers in the offline planner.
p=s/'applybot/llm.py';t=p.read_text(encoding='utf-8').replace('''                return act("check", "true")''','''                return act("skip", reason="certification or consent — review manually")''').replace('            if q.lower() in label:\n                value = str(a)', '            if q.lower() in label and a is not None and str(a).strip():\n                value = str(a)')
t=t.replace('''        if value is None:
            if ftype == "textarea"''','''        if value is None or not str(value).strip():
            if ftype == "textarea"''').replace('''        def yn(flag: object) -> str:
            return "Yes" if flag else "No"''','''        def yn(flag: object) -> str | None:
            if flag is True:
                return "Yes"
            if flag is False:
                return "No"
            return None''');p.write_text(t,encoding='utf-8')
# Release Playwright if persistent context creation fails.
p=s/'applybot/browser.py';t=p.read_text(encoding='utf-8');a=t.index('        self._pw = sync_playwright().start()');z=t.index('\n    def goto',a);old=t[a:z];body=old.replace('        self._pw = sync_playwright().start()','        self._pw = sync_playwright().start()');t=t[:a]+'''        self._pw = None
        self._ctx = None
        try:
'''+''.join('    '+line+'\n' for line in body.splitlines())+'''        except BaseException:
            self.close()
            raise
'''+t[z:];p.write_text(t,encoding='utf-8')
print('Integrated SQLite CLI tracking, explicit imports, consistent backup, lazy dependencies and browser cleanup')
