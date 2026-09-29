from pathlib import Path
s=Path('astra-remaining-improvements/stage/da9c28730758')
(s/'applybot/legacy_history.py').write_text('''"""Validate legacy JSONL without modifying or silently skipping its records."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .application_store import StoreError, application_input

MAX_HISTORY_BYTES = 10 * 1024 * 1024
MAX_HISTORY_RECORDS = 10000

@dataclass(frozen=True)
class LegacyRecord:
    receipt: str
    timestamp: str
    data: dict


def parse_legacy_history(path: str | Path) -> list[LegacyRecord]:
    with Path(path).open("rb") as source:
        raw = source.read(MAX_HISTORY_BYTES + 1)
    if len(raw) > MAX_HISTORY_BYTES:
        raise StoreError("Legacy history exceeds 10 MiB. Split a copy into smaller validated files.")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise StoreError("Legacy history must be UTF-8. The original file was not changed.") from None
    output, occurrences = [], Counter()
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        if len(line.encode("utf-8")) > 32768:
            raise StoreError(f"Legacy history line {number} exceeds 32 KiB.")
        try:
            value = json.loads(line)
            if not isinstance(value, dict) or set(value) != {"timestamp", "url", "company", "title", "status"}:
                raise StoreError("Expected timestamp, url, company, title and status.")
            if not isinstance(value["timestamp"], str):
                raise StoreError("Timestamp must be ISO text with a timezone.")
            timestamp = datetime.fromisoformat(value["timestamp"])
            if timestamp.tzinfo is None or not 1970 <= timestamp.year <= 2100:
                raise StoreError("Timestamp needs a timezone and a year between 1970 and 2100.")
            timestamp_text = timestamp.astimezone(timezone.utc).isoformat(timespec="microseconds")
            company, title = value["company"], value["title"]
            if not isinstance(company, str) or not isinstance(title, str):
                raise StoreError("Company and title must be text, including empty legacy values.")
            data = application_input({"url": value["url"], "company": company.strip() or "Unknown company", "title": title.strip() or "Untitled role", "status": value["status"], "notes": ""})
            canonical = json.dumps({"timestamp": timestamp_text, **data}, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
            fingerprint = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            occurrences[fingerprint] += 1
            receipt = f"{fingerprint}:{occurrences[fingerprint]}"
            output.append(LegacyRecord(receipt, timestamp_text, data))
            if len(output) > MAX_HISTORY_RECORDS:
                raise StoreError("History exceeds 10,000 records. Split a copy before importing.")
        except (ValueError, TypeError, OverflowError) as error:
            detail = str(error) if isinstance(error, StoreError) else "Invalid JSON or timestamp."
            raise StoreError(f"Legacy history line {number}: {detail} No records were imported.") from None
    return output
''',encoding='utf-8')
p=s/'applybot/application_store.py';t=p.read_text(encoding='utf-8');t+='''
    def import_history(self, records) -> dict:
        """Import a validated legacy batch atomically; retained receipts prevent resurrection."""
        from .legacy_history import LegacyRecord
        validated = []
        if len(records) > 10000:
            raise StoreError("Import is limited to 10,000 records.")
        for record in records:
            if not isinstance(record, LegacyRecord):
                raise StoreError("Import requires validated legacy records.")
            validated.append((record, application_input(record.data)))
        created = skipped = 0
        with self.transaction() as db:
            for record, data in validated:
                if db.execute("SELECT 1 FROM legacy_imports WHERE receipt=?", (record.receipt,)).fetchone():
                    skipped += 1
                    continue
                identity = str(uuid.uuid5(uuid.NAMESPACE_URL, "applybot-history:" + record.receipt))
                db.execute("""INSERT INTO applications(id,url,company,title,status,notes,created_at,updated_at)
                           VALUES(?,?,?,?,?,?,?,?)""", (identity, data["url"], data["company"], data["title"], data["status"], data["notes"], record.timestamp, record.timestamp))
                self._audit(db, identity, "IMPORT", 1)
                db.execute("INSERT INTO legacy_imports(receipt,application_id,imported_at) VALUES(?,?,?)", (record.receipt, identity, utc_now()))
                created += 1
        return {"created": created, "skipped": skipped, "total": len(records)}

    def imported_receipts(self) -> set[str]:
        with self.connection() as db:
            return {row[0] for row in db.execute("SELECT receipt FROM legacy_imports")}

    def find_by_url(self, url: str, status: str = "applied") -> list[dict]:
        with self.connection() as db:
            return [dict(row) for row in db.execute("SELECT * FROM applications WHERE url=? AND status=? ORDER BY created_at DESC,id LIMIT 20", (url, status))]
''';p.write_text(t,encoding='utf-8')
(s/'tests/test_legacy.py').write_text('''import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from applybot.application_store import ApplicationStore, StoreError
from applybot.legacy_history import parse_legacy_history


def legacy(**changes):
    return {"timestamp": "2026-09-09T12:00:00+00:00", "url": "https://jobs.example.test/1", "company": "Example", "title": "Engineer", "status": "applied", **changes}


class LegacyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "history.jsonl"
        self.store = ApplicationStore(Path(self.temp.name) / "tracker.sqlite3")

    def tearDown(self):
        self.temp.cleanup()

    def write(self, values):
        self.path.write_text("\\n".join(json.dumps(value) for value in values) + "\\n", encoding="utf-8")
        return parse_legacy_history(self.path)

    def test_import_repeat_and_appended_record_preserve_existing_rows(self):
        records = self.write([legacy(), legacy(title="Second role")])
        original = self.path.read_bytes()
        self.assertEqual(self.store.import_history(records)["created"], 2)
        rows = self.store.list()["items"]
        self.store.update(rows[0]["id"], 1, {key: ("Reviewed notes" if key == "notes" else rows[0][key]) for key in ("url", "company", "title", "status", "notes")})
        self.assertEqual(self.store.import_history(records)["skipped"], 2)
        appended = self.write([legacy(), legacy(title="Second role"), legacy(title="Third role")])
        self.assertEqual(self.store.import_history(appended), {"created": 1, "skipped": 2, "total": 3})
        self.assertTrue(any(row["notes"] == "Reviewed notes" for row in self.store.list()["items"]))
        self.assertTrue(self.path.read_bytes().startswith(original))

    def test_duplicate_legacy_occurrences_are_distinct_and_repeatable(self):
        records = self.write([legacy(), legacy()])
        self.assertNotEqual(records[0].receipt, records[1].receipt)
        self.assertEqual(self.store.import_history(records)["created"], 2)
        self.assertEqual(self.store.import_history(records)["skipped"], 2)

    def test_deleted_import_is_not_resurrected(self):
        records = self.write([legacy()])
        self.store.import_history(records)
        row = self.store.list()["items"][0]
        self.store.delete(row["id"], row["version"])
        self.assertEqual(self.store.import_history(records)["skipped"], 1)
        self.assertEqual(self.store.list()["total"], 0)

    def test_malformed_line_is_reported_without_skipping_or_mutating(self):
        self.path.write_text(json.dumps(legacy()) + "\\n{broken\\n", encoding="utf-8")
        before = self.path.read_bytes()
        with self.assertRaisesRegex(StoreError, "line 2"):
            parse_legacy_history(self.path)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.store.list()["total"], 0)

    def test_invalid_record_shapes_and_timestamps_fail(self):
        for value in [[], {**legacy(), "extra": 1}, legacy(timestamp="2026-09-09"), legacy(timestamp="not a date"), legacy(company=[]), legacy(status="probably sent")]:
            with self.subTest(kind=type(value).__name__):
                with self.assertRaises(StoreError):
                    self.write([value])

    def test_empty_legacy_labels_have_explicit_defaults(self):
        records = self.write([legacy(company="", title="")])
        self.assertEqual(records[0].data["company"], "Unknown company")
        self.assertEqual(records[0].data["title"], "Untitled role")

    def test_audit_failure_rolls_back_entire_import_and_receipts(self):
        records = self.write([legacy(), legacy(title="Second")])
        with self.store.connection() as db:
            db.execute("CREATE TRIGGER reject_import BEFORE INSERT ON application_audit BEGIN SELECT RAISE(ABORT,'injected'); END")
        with self.assertRaises(sqlite3.IntegrityError):
            self.store.import_history(records)
        self.assertEqual(self.store.list()["total"], 0)
        self.assertEqual(self.store.imported_receipts(), set())

    def test_invalid_utf8_and_oversized_file_are_rejected(self):
        self.path.write_bytes(b"\\xff")
        with self.assertRaisesRegex(StoreError, "UTF-8"):
            parse_legacy_history(self.path)
        self.path.write_bytes(b" " * (10 * 1024 * 1024 + 1))
        with self.assertRaisesRegex(StoreError, "10 MiB"):
            parse_legacy_history(self.path)
''',encoding='utf-8');print('Added explicit atomic legacy-history import with stable receipts and eight tests')
