from __future__ import annotations

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models import LogEvent, MetricPoint, TraceSpan
from app.security import Principal
from app.services.common import (
    enforce_rate_limit,
    get_stream_or_404,
    maybe_enforce_retention,
    validate_payload_size,
)
from app.services.deduplication import unseen_items, validate_trace_graph
from app.services.pipelines import apply_pipelines


def ingest_logs(
    db: Session, request, principal: Principal, stream_name: str, events: list[dict]
) -> dict[str, int]:
    db.execute(text("BEGIN IMMEDIATE"))
    stream = get_stream_or_404(db, principal.organization_id, stream_name, "logs")
    enforce_rate_limit(request, principal, stream_name)
    validate_payload_size(
        events, min(stream.max_payload_bytes, request.app.state.settings.ingest_max_payload_bytes)
    )
    fresh, skipped = unseen_items(db, principal.organization_id, LogEvent, events)
    transformed, derived_metrics = apply_pipelines(db, principal.organization_id, "logs", fresh)
    accepted = 0
    for event in transformed:
        stream_to_use = (
            stream
            if not event.get("_stream_name")
            else get_stream_or_404(db, principal.organization_id, event["_stream_name"], "logs")
        )
        dedupe_key = event.get("dedupe_key")
        if dedupe_key and db.scalar(
            select(LogEvent.id).where(
                LogEvent.organization_id == principal.organization_id,
                LogEvent.dedupe_key == dedupe_key,
            )
        ):
            skipped += 1
            continue
        db.add(
            LogEvent(
                organization_id=principal.organization_id,
                stream_id=stream_to_use.id,
                event_ts=event["timestamp"],
                level=event.get("level"),
                message=event["message"],
                service=event.get("service"),
                trace_id=event.get("trace_id"),
                span_id=event.get("span_id"),
                dedupe_key=dedupe_key,
                attributes=event.get("attributes", {}),
            )
        )
        accepted += 1
    if derived_metrics:
        metrics_stream = get_stream_or_404(
            db, principal.organization_id, "metrics-default", "metrics"
        )
        for metric in derived_metrics:
            db.add(
                MetricPoint(
                    organization_id=principal.organization_id,
                    stream_id=metrics_stream.id,
                    ts=metric["timestamp"],
                    metric_name=metric["metric_name"],
                    value=metric["value"],
                    unit=metric.get("unit"),
                    labels=metric.get("labels", {}),
                )
            )
    db.flush()
    maybe_enforce_retention(db, request, principal.organization_id)
    db.commit()
    return {"accepted": accepted, "skipped": skipped, "derived_metrics": len(derived_metrics)}


def ingest_metrics(
    db: Session, request, principal: Principal, stream_name: str, points: list[dict]
) -> dict[str, int]:
    db.execute(text("BEGIN IMMEDIATE"))
    stream = get_stream_or_404(db, principal.organization_id, stream_name, "metrics")
    enforce_rate_limit(request, principal, stream_name)
    validate_payload_size(
        points, min(stream.max_payload_bytes, request.app.state.settings.ingest_max_payload_bytes)
    )
    fresh, skipped = unseen_items(db, principal.organization_id, MetricPoint, points)
    transformed, _ = apply_pipelines(db, principal.organization_id, "metrics", fresh)
    accepted = 0
    for point in transformed:
        stream_to_use = (
            stream
            if not point.get("_stream_name")
            else get_stream_or_404(db, principal.organization_id, point["_stream_name"], "metrics")
        )
        dedupe_key = point.get("dedupe_key")
        if dedupe_key and db.scalar(
            select(MetricPoint.id).where(
                MetricPoint.organization_id == principal.organization_id,
                MetricPoint.dedupe_key == dedupe_key,
            )
        ):
            skipped += 1
            continue
        db.add(
            MetricPoint(
                organization_id=principal.organization_id,
                stream_id=stream_to_use.id,
                ts=point["timestamp"],
                metric_name=point["metric_name"],
                value=point["value"],
                unit=point.get("unit"),
                dedupe_key=dedupe_key,
                labels=point.get("labels", {}),
            )
        )
        accepted += 1
    db.flush()
    maybe_enforce_retention(db, request, principal.organization_id)
    db.commit()
    return {"accepted": accepted, "skipped": skipped}


def ingest_traces(
    db: Session, request, principal: Principal, stream_name: str, spans: list[dict]
) -> dict[str, int]:
    db.execute(text("BEGIN IMMEDIATE"))
    stream = get_stream_or_404(db, principal.organization_id, stream_name, "traces")
    enforce_rate_limit(request, principal, stream_name)
    validate_payload_size(
        spans, min(stream.max_payload_bytes, request.app.state.settings.ingest_max_payload_bytes)
    )
    fresh, skipped = unseen_items(db, principal.organization_id, TraceSpan, spans)
    validate_trace_graph(db, principal.organization_id, fresh)
    transformed, _ = apply_pipelines(db, principal.organization_id, "traces", fresh)
    accepted = 0
    for span in transformed:
        exists = db.scalar(
            select(TraceSpan.id).where(
                TraceSpan.organization_id == principal.organization_id,
                TraceSpan.trace_id == span["trace_id"],
                TraceSpan.span_id == span["span_id"],
            )
        )
        if exists:
            skipped += 1
            continue
        stream_to_use = (
            stream
            if not span.get("_stream_name")
            else get_stream_or_404(db, principal.organization_id, span["_stream_name"], "traces")
        )
        duration_ms = max((span["end_ts"] - span["start_ts"]).total_seconds() * 1000.0, 0.0)
        db.add(
            TraceSpan(
                organization_id=principal.organization_id,
                stream_id=stream_to_use.id,
                trace_id=span["trace_id"],
                span_id=span["span_id"],
                parent_span_id=span.get("parent_span_id"),
                service_name=span["service_name"],
                operation_name=span["operation_name"],
                status=span.get("status", "ok"),
                duration_ms=duration_ms,
                start_ts=span["start_ts"],
                end_ts=span["end_ts"],
                dedupe_key=span.get("dedupe_key"),
                attributes=span.get("attributes", {}),
            )
        )
        accepted += 1
    db.flush()
    maybe_enforce_retention(db, request, principal.organization_id)
    db.commit()
    return {"accepted": accepted, "skipped": skipped}
