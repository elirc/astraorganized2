from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, Request
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import AuditLog, LogEvent, MetricPoint, Organization, Stream, StreamType, TraceSpan
from app.security import Principal, utcnow


def validate_time_range(start_time: datetime, end_time: datetime) -> None:
    if end_time <= start_time:
        raise HTTPException(status_code=400, detail="Invalid time range")


def write_audit_log(
    db: Session,
    organization_id: int,
    actor_user_id: int | None,
    action: str,
    resource_type: str,
    resource_id: str,
    details: dict[str, Any] | None = None,
) -> None:
    db.add(
        AuditLog(
            organization_id=organization_id,
            actor_user_id=actor_user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
        )
    )


def ensure_default_streams(db: Session, org: Organization) -> None:
    for stream_type in StreamType:
        stream_name = f"{stream_type.value}-default"
        existing = db.scalar(
            select(Stream).where(Stream.organization_id == org.id, Stream.name == stream_name)
        )
        if not existing:
            db.add(
                Stream(
                    organization_id=org.id,
                    name=stream_name,
                    type=stream_type,
                    retention_days=14,
                    indexing_options={"default": True},
                )
            )


def get_stream_or_404(
    db: Session, organization_id: int, name: str, stream_type: str | None = None
) -> Stream:
    query = select(Stream).where(Stream.organization_id == organization_id, Stream.name == name)
    if stream_type:
        query = query.where(Stream.type == StreamType(stream_type))
    stream = db.scalar(query)
    if not stream:
        raise HTTPException(status_code=404, detail=f"Stream {name} not found")
    return stream


def enforce_rate_limit(request: Request, principal: Principal, stream_name: str) -> None:
    state = request.app.state
    now = utcnow()
    key = f"{principal.token_id}:{stream_name}"
    one_minute_ago = now - timedelta(minutes=1)
    with state.limiter_lock:
        state.rate_limits = {
            name: times
            for name, times in state.rate_limits.items()
            if times and times[-1] > one_minute_ago
        }
        if key not in state.rate_limits and len(state.rate_limits) >= 10000:
            raise HTTPException(status_code=429, detail="Too many active ingestion buckets")
        bucket = [ts for ts in state.rate_limits.get(key, []) if ts > one_minute_ago]
        if len(bucket) >= state.settings.rate_limit_per_minute:
            raise HTTPException(
                status_code=429, detail="Rate limit exceeded", headers={"Retry-After": "60"}
            )
        state.rate_limits[key] = [*bucket, now]


def validate_payload_size(payload: list[dict], max_bytes: int) -> None:
    size = len(json.dumps(payload, default=str).encode("utf-8"))
    if size > max_bytes:
        raise HTTPException(status_code=413, detail="Payload too large")


def maybe_enforce_retention(db: Session, request: Request, organization_id: int) -> None:
    now = utcnow()
    streams = db.scalars(select(Stream).where(Stream.organization_id == organization_id)).all()
    for stream in streams:
        cutoff = now - timedelta(days=stream.retention_days)
        if stream.type == StreamType.logs:
            db.execute(
                delete(LogEvent).where(LogEvent.stream_id == stream.id, LogEvent.event_ts < cutoff)
            )
        elif stream.type == StreamType.metrics:
            db.execute(
                delete(MetricPoint).where(
                    MetricPoint.stream_id == stream.id, MetricPoint.ts < cutoff
                )
            )
        else:
            db.execute(
                delete(TraceSpan).where(
                    TraceSpan.stream_id == stream.id, TraceSpan.start_ts < cutoff
                )
            )
