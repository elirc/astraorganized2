from __future__ import annotations

import json
import math
import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import LogEvent, MetricPoint, TraceSpan
from app.permissions import has_permission
from app.schemas import MetricsQueryRequest, SearchRequest, TraceSearchRequest
from app.security import Principal
from app.services.common import get_stream_or_404, validate_time_range
from app.services.query_safety import bounded_rows, execute_subset

SQL_BLOCKLIST = re.compile(
    r"\b(insert|update|delete|drop|alter|attach|detach|pragma|create|replace)\b|;", re.IGNORECASE
)
PROMQL_RE = re.compile(
    r"^(?P<agg>sum|avg|min|max|count)\((?P<metric>[a-zA-Z_:][a-zA-Z0-9_:]*)(?:\{(?P<labels>[^}]*)\})?\)(?:\s+by\s+\((?P<groups>[^)]*)\))?$"
)


def _scan_guard(count: int, limit: int, scan_cap: int, row_cap: int) -> int:
    if count > scan_cap:
        raise HTTPException(
            status_code=400, detail=f"Query scan cap exceeded: {count} > {scan_cap}"
        )
    return min(limit, row_cap)


def search_logs(
    db: Session, principal: Principal, req: SearchRequest, scan_cap: int, row_cap: int
) -> dict[str, Any]:
    validate_time_range(req.start_time, req.end_time)
    query = select(LogEvent).where(
        LogEvent.organization_id == principal.organization_id,
        LogEvent.event_ts >= req.start_time,
        LogEvent.event_ts <= req.end_time,
    )
    if req.stream:
        stream = get_stream_or_404(db, principal.organization_id, req.stream, "logs")
        query = query.where(LogEvent.stream_id == stream.id)
    count = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    limit = _scan_guard(count, req.limit, scan_cap, row_cap)
    rows = bounded_rows(
        db.scalars(
            query.order_by(LogEvent.event_ts.desc(), LogEvent.id.desc()).limit(scan_cap)
        ).yield_per(100)
    )
    filtered = []
    for row in rows:
        if (
            req.text
            and req.text.lower() not in f"{row.message} {json.dumps(row.attributes)}".lower()
        ):
            continue
        matches = True
        for key, expected in req.filters.items():
            value = (
                getattr(row, key, None)
                if key in {"level", "message", "service", "trace_id", "span_id"}
                else None
            )
            if value is None:
                value = row.attributes.get(key)
            if value != expected:
                matches = False
                break
        if matches:
            filtered.append(row)
    matched_rows = len(filtered)
    filtered = filtered[:limit]
    histogram: dict[str, int] = defaultdict(int)
    fields: set[str] = set()
    for row in filtered:
        bucket = row.event_ts.replace(second=0, microsecond=0).isoformat()
        histogram[bucket] += 1
        fields.update(row.attributes.keys())
    return {
        "results": [
            {
                "id": row.id,
                "timestamp": row.event_ts,
                "level": row.level,
                "message": row.message,
                "service": row.service,
                "trace_id": row.trace_id,
                "span_id": row.span_id,
                "attributes": row.attributes,
            }
            for row in filtered
        ],
        "matched_rows": matched_rows,
        "histogram": [
            {"bucket": bucket, "count": count} for bucket, count in sorted(histogram.items())
        ],
        "fields": sorted(fields),
        "scanned_rows": count,
    }


def _build_sqlite_subset_log(rows: list[LogEvent]) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE log_events (
            id INTEGER,
            event_ts TEXT,
            level TEXT,
            message TEXT,
            service TEXT,
            trace_id TEXT,
            span_id TEXT,
            attributes_json TEXT
        )
        """
    )
    conn.executemany(
        "INSERT INTO log_events VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                row.id,
                row.event_ts.isoformat(),
                row.level,
                row.message,
                row.service,
                row.trace_id,
                row.span_id,
                json.dumps(row.attributes),
            )
            for row in rows
        ],
    )
    return conn


def _build_sqlite_subset_metrics(rows: list[MetricPoint]) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE metric_points (
            id INTEGER,
            ts TEXT,
            metric_name TEXT,
            value REAL,
            unit TEXT,
            labels_json TEXT
        )
        """
    )
    conn.executemany(
        "INSERT INTO metric_points VALUES (?, ?, ?, ?, ?, ?)",
        [
            (
                row.id,
                row.ts.isoformat(),
                row.metric_name,
                row.value,
                row.unit,
                json.dumps(row.labels),
            )
            for row in rows
        ],
    )
    return conn


def execute_log_sql(
    db: Session,
    principal: Principal,
    start_time: datetime,
    end_time: datetime,
    query: str,
    limit: int,
    scan_cap: int,
    row_cap: int,
    timeout_ms: int = 5000,
) -> dict[str, Any]:
    validate_time_range(start_time, end_time)
    scoped_query = select(LogEvent).where(
        LogEvent.organization_id == principal.organization_id,
        LogEvent.event_ts >= start_time,
        LogEvent.event_ts <= end_time,
    )
    count = db.scalar(select(func.count()).select_from(scoped_query.subquery())) or 0
    effective_limit = _scan_guard(count, limit, scan_cap, row_cap)
    rows = bounded_rows(db.scalars(scoped_query.limit(scan_cap)).yield_per(100))
    conn = _build_sqlite_subset_log(rows)
    columns, records = execute_subset(conn, "log_events", query, effective_limit, timeout_ms)
    return {"columns": columns, "rows": [list(record) for record in records], "scanned_rows": count}


def execute_metric_sql(
    db: Session,
    principal: Principal,
    start_time: datetime,
    end_time: datetime,
    query: str,
    limit: int,
    scan_cap: int,
    row_cap: int,
    timeout_ms: int = 5000,
) -> dict[str, Any]:
    validate_time_range(start_time, end_time)
    scoped_query = select(MetricPoint).where(
        MetricPoint.organization_id == principal.organization_id,
        MetricPoint.ts >= start_time,
        MetricPoint.ts <= end_time,
    )
    count = db.scalar(select(func.count()).select_from(scoped_query.subquery())) or 0
    effective_limit = _scan_guard(count, limit, scan_cap, row_cap)
    rows = bounded_rows(db.scalars(scoped_query.limit(scan_cap)).yield_per(100))
    conn = _build_sqlite_subset_metrics(rows)
    columns, records = execute_subset(conn, "metric_points", query, effective_limit, timeout_ms)
    return {"columns": columns, "rows": [list(record) for record in records], "scanned_rows": count}


def _matches_labels(labels: dict[str, Any], filters: dict[str, Any]) -> bool:
    return all(labels.get(key) == value for key, value in filters.items())


def query_metrics(
    db: Session, principal: Principal, req: MetricsQueryRequest, scan_cap: int, row_cap: int
) -> dict[str, Any]:
    validate_time_range(req.start_time, req.end_time)
    query = select(MetricPoint).where(
        MetricPoint.organization_id == principal.organization_id,
        MetricPoint.ts >= req.start_time,
        MetricPoint.ts <= req.end_time,
        MetricPoint.metric_name == req.metric_name,
    )
    count = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    limit = _scan_guard(count, req.limit, scan_cap, row_cap)
    rows = [
        row
        for row in bounded_rows(
            db.scalars(
                query.order_by(MetricPoint.ts.asc(), MetricPoint.id.asc()).limit(scan_cap)
            ).yield_per(100)
        )
        if _matches_labels(row.labels, req.filters)
    ]
    buckets: dict[tuple, list[float]] = defaultdict(list)
    step = max(req.step_seconds, 1)
    for row in rows:
        epoch = int(row.ts.timestamp())
        bucket_ts = datetime.fromtimestamp((epoch // step) * step, tz=timezone.utc).isoformat()
        group_values = tuple(
            json.dumps(row.labels.get(key), sort_keys=True, allow_nan=False) for key in req.group_by
        )
        buckets[(bucket_ts,) + group_values].append(row.value)
    series = []
    for bucket_key, values in sorted(buckets.items()):
        if req.aggregate == "sum":
            value = sum(values)
        elif req.aggregate == "avg":
            value = sum(values) / len(values)
        elif req.aggregate == "min":
            value = min(values)
        elif req.aggregate == "max":
            value = max(values)
        else:
            value = len(values)
        if not math.isfinite(value):
            raise HTTPException(
                status_code=400, detail="Aggregation exceeded the finite numeric range"
            )
        labels = {key: json.loads(bucket_key[index + 1]) for index, key in enumerate(req.group_by)}
        series.append({"timestamp": bucket_key[0], "value": value, "labels": labels})
    return {"series": series[-limit:], "scanned_rows": count}


def query_metrics_promql(
    db: Session,
    principal: Principal,
    start_time: datetime,
    end_time: datetime,
    query: str,
    step_seconds: int,
    scan_cap: int,
    row_cap: int,
) -> dict[str, Any]:
    match = PROMQL_RE.match(query.strip())
    if not match:
        raise HTTPException(status_code=400, detail="Unsupported PromQL-like query")
    labels = {}
    label_text = match.group("labels")
    if label_text:
        for pair in label_text.split(","):
            label = re.fullmatch(r'\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*("(?:[^"\\]|\\.)*")\s*', pair)
            if not label or label.group(1) in labels:
                raise HTTPException(
                    status_code=400, detail='Labels must be unique name="value" pairs'
                )
            try:
                labels[label.group(1)] = json.loads(label.group(2))
            except ValueError as exc:
                raise HTTPException(status_code=400, detail="Invalid label string") from exc
    group_by = [part.strip() for part in (match.group("groups") or "").split(",") if part.strip()]
    req = MetricsQueryRequest(
        start_time=start_time,
        end_time=end_time,
        metric_name=match.group("metric"),
        filters=labels,
        aggregate=match.group("agg"),
        group_by=group_by,
        step_seconds=step_seconds,
    )
    return query_metrics(db, principal, req, scan_cap, row_cap)


def search_traces(
    db: Session, principal: Principal, req: TraceSearchRequest, scan_cap: int, row_cap: int
) -> dict[str, Any]:
    validate_time_range(req.start_time, req.end_time)
    query = select(TraceSpan).where(
        TraceSpan.organization_id == principal.organization_id,
        TraceSpan.start_ts >= req.start_time,
        TraceSpan.start_ts <= req.end_time,
    )
    if req.stream:
        stream = get_stream_or_404(db, principal.organization_id, req.stream, "traces")
        query = query.where(TraceSpan.stream_id == stream.id)
    if req.service_name:
        query = query.where(TraceSpan.service_name == req.service_name)
    if req.operation_name:
        query = query.where(TraceSpan.operation_name == req.operation_name)
    if req.status:
        query = query.where(TraceSpan.status == req.status)
    if req.min_duration_ms is not None:
        query = query.where(TraceSpan.duration_ms >= req.min_duration_ms)
    if req.max_duration_ms is not None:
        query = query.where(TraceSpan.duration_ms <= req.max_duration_ms)
    count = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    limit = _scan_guard(count, req.limit, scan_cap, row_cap)
    rows = bounded_rows(
        db.scalars(
            query.order_by(TraceSpan.start_ts.desc(), TraceSpan.id.desc()).limit(scan_cap)
        ).yield_per(100)
    )
    filtered = []
    for row in rows:
        if all(row.attributes.get(key) == value for key, value in req.filters.items()):
            filtered.append(row)
    traces = defaultdict(list)
    for row in filtered:
        traces[row.trace_id].append(row)
    results = []
    for trace_id, spans in traces.items():
        root = min(spans, key=lambda item: item.start_ts)
        duration_ms = (
            max(span.end_ts for span in spans) - min(span.start_ts for span in spans)
        ).total_seconds() * 1000.0
        results.append(
            {
                "trace_id": trace_id,
                "root_service": root.service_name,
                "root_operation": root.operation_name,
                "span_count": len(spans),
                "start_ts": root.start_ts,
                "duration_ms": duration_ms,
                "status": "error" if any(span.status.lower() != "ok" for span in spans) else "ok",
            }
        )
    return {
        "results": results[:limit],
        "scanned_rows": count,
        "max_duration_ms": max((item["duration_ms"] for item in results), default=0.0),
        "span_scope": "Counts and durations describe spans matching the request filters and time window",
    }


def _build_trace_tree(spans: list[TraceSpan]) -> list[dict[str, Any]]:
    parents = {span.span_id: span.parent_span_id for span in spans}
    for start in parents:
        seen = set()
        node = start
        while node in parents:
            if node in seen or len(seen) >= 64:
                raise HTTPException(
                    status_code=400, detail="Stored trace contains a cycle or exceeds depth 64"
                )
            seen.add(node)
            node = parents[node]
    nodes = {
        span.span_id: {
            "span_id": span.span_id,
            "parent_span_id": span.parent_span_id,
            "service_name": span.service_name,
            "operation_name": span.operation_name,
            "status": span.status,
            "duration_ms": span.duration_ms,
            "start_ts": span.start_ts,
            "end_ts": span.end_ts,
            "attributes": span.attributes,
            "children": [],
        }
        for span in spans
    }
    roots = []
    for span in spans:
        if span.parent_span_id in nodes:
            nodes[span.parent_span_id]["children"].append(nodes[span.span_id])
        else:
            roots.append(nodes[span.span_id])
    return roots


def trace_detail(db: Session, principal: Principal, trace_id: str) -> dict[str, Any]:
    spans = bounded_rows(
        db.scalars(
            select(TraceSpan)
            .where(
                TraceSpan.organization_id == principal.organization_id,
                TraceSpan.trace_id == trace_id,
            )
            .order_by(TraceSpan.start_ts.asc(), TraceSpan.id.asc())
            .limit(1001)
        ).yield_per(100)
    )
    if len(spans) > 1000:
        raise HTTPException(status_code=400, detail="Stored trace exceeds 1000 spans")
    if not spans:
        raise HTTPException(status_code=404, detail="Trace not found")
    logs = (
        bounded_rows(
            db.scalars(
                select(LogEvent)
                .where(
                    LogEvent.organization_id == principal.organization_id,
                    LogEvent.trace_id == trace_id,
                )
                .order_by(LogEvent.event_ts.asc(), LogEvent.id.asc())
                .limit(1001)
            ).yield_per(100)
        )
        if has_permission(principal.role, principal.scopes, "logs:read")
        else []
    )
    service_edges = set()
    span_map = {span.span_id: span for span in spans}
    for span in spans:
        if span.parent_span_id and span.parent_span_id in span_map:
            parent = span_map[span.parent_span_id]
            if parent.service_name != span.service_name:
                service_edges.add((parent.service_name, span.service_name))
    return {
        "trace_id": trace_id,
        "correlated_logs_truncated": len(logs) > 1000,
        "correlated_logs_authorized": has_permission(principal.role, principal.scopes, "logs:read"),
        "span_tree": _build_trace_tree(spans),
        "timeline": [
            {
                "span_id": span.span_id,
                "service_name": span.service_name,
                "operation_name": span.operation_name,
                "start_ts": span.start_ts,
                "end_ts": span.end_ts,
                "duration_ms": span.duration_ms,
                "status": span.status,
            }
            for span in spans
        ],
        "service_map": [{"source": src, "target": dst} for src, dst in sorted(service_edges)],
        "correlated_logs": [
            {
                "timestamp": log.event_ts,
                "message": log.message,
                "service": log.service,
                "trace_id": log.trace_id,
                "span_id": log.span_id,
            }
            for log in logs[:1000]
        ],
    }
