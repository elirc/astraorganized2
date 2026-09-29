"""Resource limits for the intentionally small, isolated SQL query engine."""

import json
import re
import sqlite3
import time

from fastapi import HTTPException

MAX_RESULT_BYTES = 8 * 1024 * 1024
FUNCTIONS = {
    "abs",
    "avg",
    "coalesce",
    "count",
    "date",
    "datetime",
    "ifnull",
    "json_extract",
    "json_type",
    "length",
    "lower",
    "max",
    "min",
    "nullif",
    "round",
    "strftime",
    "substr",
    "substring",
    "sum",
    "total",
    "trim",
    "upper",
    "like",
    "glob",
    "typeof",
}


def bounded_rows(rows):
    result, size = [], 0
    for row in rows:
        values = {column.name: getattr(row, column.name) for column in row.__table__.columns}
        try:
            size += len(json.dumps(values, default=str, allow_nan=False).encode("utf-8"))
        except ValueError as exc:
            raise HTTPException(
                status_code=400, detail="Stored telemetry contains a non-finite value"
            ) from exc
        if size > MAX_RESULT_BYTES:
            raise HTTPException(
                status_code=400, detail="Query data exceeds 8 MiB; narrow the time window"
            )
        result.append(row)
    return result


def execute_subset(conn, table, query, limit, timeout_ms):
    try:
        if not re.match(r"^\s*select\b", query, re.IGNORECASE):
            raise HTTPException(status_code=400, detail="Only a bounded SELECT query is supported")
        conn.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 262144)
        conn.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 10000)
        conn.setlimit(sqlite3.SQLITE_LIMIT_COLUMN, 64)
        conn.setlimit(sqlite3.SQLITE_LIMIT_EXPR_DEPTH, 50)
        conn.setlimit(sqlite3.SQLITE_LIMIT_COMPOUND_SELECT, 10)
        conn.setlimit(sqlite3.SQLITE_LIMIT_VDBE_OP, 100000)
        conn.execute("PRAGMA query_only=ON")
        deadline = time.monotonic() + timeout_ms / 1000
        timed_out = False

        def progress():
            nonlocal timed_out
            timed_out = time.monotonic() >= deadline
            return int(timed_out)

        def authorize(action, arg1, arg2, _database, _trigger):
            if action == sqlite3.SQLITE_SELECT:
                return sqlite3.SQLITE_OK
            if action == sqlite3.SQLITE_READ and arg1 == table:
                return sqlite3.SQLITE_OK
            if action == sqlite3.SQLITE_FUNCTION and (arg2 or "").lower() in FUNCTIONS:
                return sqlite3.SQLITE_OK
            return sqlite3.SQLITE_DENY

        conn.set_authorizer(authorize)
        conn.set_progress_handler(progress, 1000)
        try:
            cursor = conn.execute(query)
            columns = [column[0] for column in cursor.description]
            records = [list(row) for row in cursor.fetchmany(limit)]
            if len(json.dumps(records, allow_nan=False).encode("utf-8")) > MAX_RESULT_BYTES:
                raise HTTPException(status_code=400, detail="SQL result exceeds 8 MiB")
            return columns, records
        except (sqlite3.Error, ValueError, TypeError, MemoryError) as exc:
            if timed_out:
                raise HTTPException(
                    status_code=408, detail="SQL query exceeded its time budget"
                ) from exc
            raise HTTPException(
                status_code=400,
                detail="Unsupported or invalid SQL query; use the documented SELECT subset",
            ) from exc
    finally:
        conn.close()
