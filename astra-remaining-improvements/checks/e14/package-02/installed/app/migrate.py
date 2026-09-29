"""Explicit additive SQLite migration; always back up the stopped database first."""

from __future__ import annotations

import argparse
from pathlib import Path

from sqlalchemy import inspect
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db import INDEXES, VERSION_TABLES, build_engine


def migrate(engine):
    tables = set(inspect(engine).get_table_names())
    required = set(VERSION_TABLES) | {"users", "log_events", "metric_points"}
    if not required <= tables:
        raise ValueError("Not a recognized complete E14 schema; migration refused")
    with engine.connect() as connection:
        connection.exec_driver_sql("BEGIN IMMEDIATE")
        try:
            if connection.exec_driver_sql("PRAGMA foreign_key_check").first():
                raise ValueError("Resolve existing foreign-key inconsistencies before migration")
            if connection.exec_driver_sql(
                "SELECT lower(email) FROM users GROUP BY lower(email) HAVING count(*)>1 LIMIT 1"
            ).first():
                raise ValueError("Case-insensitive duplicate emails require explicit resolution")
            for table in ("log_events", "metric_points"):
                if connection.exec_driver_sql(
                    f"SELECT organization_id FROM {table} WHERE dedupe_key IS NOT NULL GROUP BY organization_id,dedupe_key HAVING count(*)>1 LIMIT 1"
                ).first():
                    raise ValueError(
                        f"Existing duplicate dedupe keys in {table}; migration preserves data and refuses to guess which row to keep"
                    )
            changed = []
            for table in VERSION_TABLES:
                columns = {
                    row[1] for row in connection.exec_driver_sql(f"PRAGMA table_info({table})")
                }
                if "version" not in columns:
                    connection.exec_driver_sql(
                        f"ALTER TABLE {table} ADD COLUMN version INTEGER NOT NULL DEFAULT 1"
                    )
                    changed.append(table)
            for sql in INDEXES.values():
                connection.exec_driver_sql(sql)
            connection.commit()
            return changed
        except BaseException:
            connection.rollback()
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", required=True)
    parser.parse_args()
    cfg = Settings.from_env()
    database = make_url(cfg.database_url).database
    if not database or database == ":memory:" or not Path(database).is_file():
        parser.error("Migration requires an existing database file; no empty database was created")
    engine = build_engine(cfg)
    try:
        print(
            "Migration accepted. Added version columns to: "
            + (", ".join(migrate(engine)) or "none (already current)")
        )
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
