from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.models import AlertDelivery, AlertRule
from app.permissions import has_permission
from app.schemas import MetricsQueryRequest, SearchRequest, TraceSearchRequest
from app.security import Principal, utcnow
from app.services.notification_outbox import validate_destination
from app.services.queries import query_metrics, search_logs, search_traces


def compare(operator: str, value: float, threshold: float) -> bool:
    return {
        "gt": value > threshold,
        "gte": value >= threshold,
        "lt": value < threshold,
        "lte": value <= threshold,
        "eq": value == threshold,
    }.get(operator, False)


def evaluate_alert_rule(db: Session, principal: Principal, alert: AlertRule, cfg=settings) -> dict:
    if not has_permission(principal.role, principal.scopes, alert.module + ":read"):
        raise HTTPException(
            status_code=403,
            detail="Alert evaluation requires read permission for its telemetry module",
        )
    from app.contracts import validate_alert_condition

    try:
        condition = validate_alert_condition(alert.module, alert.condition)
    except (ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=422, detail="Stored alert configuration needs repair before evaluation"
        ) from exc
    operator = condition.get("operator", "gte")
    threshold = float(condition.get("threshold", 1))
    if alert.module == "logs":
        req = SearchRequest(
            start_time=datetime.fromisoformat(condition["start_time"]),
            end_time=datetime.fromisoformat(condition["end_time"]),
            stream=condition.get("stream"),
            text=condition.get("text"),
            filters=condition.get("filters", {}),
            limit=condition.get("limit", 100),
        )
        result = search_logs(
            db, principal, req, scan_cap=cfg.query_scan_limit, row_cap=cfg.query_row_limit
        )
        value = float(result["matched_rows"])
    elif alert.module == "metrics":
        req = MetricsQueryRequest(
            start_time=datetime.fromisoformat(condition["start_time"]),
            end_time=datetime.fromisoformat(condition["end_time"]),
            metric_name=condition["metric_name"],
            filters=condition.get("filters", {}),
            aggregate=condition.get("aggregate", "avg"),
            group_by=condition.get("group_by", []),
            step_seconds=condition.get("step_seconds", 60),
            limit=condition.get("limit", 500),
        )
        result = query_metrics(
            db, principal, req, scan_cap=cfg.query_scan_limit, row_cap=cfg.query_row_limit
        )
        series = result["series"]
        value = float(series[-1]["value"] if series else 0.0)
    else:
        req = TraceSearchRequest(
            start_time=datetime.fromisoformat(condition["start_time"]),
            end_time=datetime.fromisoformat(condition["end_time"]),
            stream=condition.get("stream"),
            service_name=condition.get("service_name"),
            operation_name=condition.get("operation_name"),
            status=condition.get("status"),
            min_duration_ms=condition.get("min_duration_ms"),
            max_duration_ms=condition.get("max_duration_ms"),
            filters=condition.get("filters", {}),
            limit=condition.get("limit", 100),
        )
        result = search_traces(
            db, principal, req, scan_cap=cfg.query_scan_limit, row_cap=cfg.query_row_limit
        )
        value = result["max_duration_ms"]
    triggered = compare(operator, value, threshold)
    return {"triggered": triggered, "value": value, "threshold": threshold, "operator": operator}


def dispatch_notifications(db: Session, alert: AlertRule, evaluation: dict, cfg=settings) -> dict:
    fingerprint = hashlib.sha256(
        f"{alert.id}:{evaluation['value']}:{evaluation['threshold']}:{evaluation['operator']}".encode()
    ).hexdigest()
    now = utcnow()
    last_fired_at = alert.last_fired_at
    if last_fired_at and last_fired_at.tzinfo is None:
        last_fired_at = last_fired_at.replace(tzinfo=timezone.utc)
    if (
        alert.last_fired_fingerprint == fingerprint
        and last_fired_at
        and (now - last_fired_at).total_seconds() <= alert.dedupe_window_seconds
    ):
        return {"deduped": True, "deliveries": []}
    deliveries = []
    payload = {"alert": alert.name, "evaluation": evaluation, "fired_at": now.isoformat()}
    for channel in alert.notifications:
        destination = channel.get("target", "unknown")
        status_value = "simulated"
        channel_type = channel.get("type", "webhook")
        if cfg.allow_notifications and channel_type in {"webhook", "slack"}:
            try:
                validate_destination(destination, cfg)
            except ValueError as exc:
                raise HTTPException(status_code=422, detail=str(exc)) from exc
            status_value = "pending"
        delivery = AlertDelivery(
            alert_rule_id=alert.id,
            status=status_value,
            destination=destination,
            fingerprint=fingerprint,
            payload=payload,
        )
        db.add(delivery)
        deliveries.append({"destination": destination, "status": status_value})
    alert.last_fired_fingerprint = fingerprint
    alert.last_fired_at = now
    db.commit()
    return {"deduped": False, "deliveries": deliveries}


def run_alert(db: Session, principal: Principal, alert: AlertRule, cfg=settings) -> dict:
    if not alert.enabled:
        raise HTTPException(status_code=409, detail="Enable this alert before evaluating it")
    evaluation = evaluate_alert_rule(db, principal, alert, cfg)
    if not evaluation["triggered"]:
        return {"triggered": False, "evaluation": evaluation, "deliveries": []}
    notification_result = dispatch_notifications(db, alert, evaluation, cfg)
    return {"triggered": True, "evaluation": evaluation, **notification_result}
