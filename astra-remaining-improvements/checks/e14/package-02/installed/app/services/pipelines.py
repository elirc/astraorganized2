from __future__ import annotations

import copy
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Pipeline, PipelineRun
from app.schemas import LogEventIn, MetricPointIn, TraceSpanIn
from app.security import Principal, utcnow
from app.services.common import get_stream_or_404


def _load_pipelines(db: Session, organization_id: int, source_type: str) -> list[Pipeline]:
    return db.scalars(
        select(Pipeline)
        .where(
            Pipeline.organization_id == organization_id,
            Pipeline.source_type == source_type,
            Pipeline.enabled.is_(True),
        )
        .order_by(Pipeline.id)
    ).all()


def _apply_steps(
    item: dict[str, Any], pipeline: Pipeline
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    current = copy.deepcopy(item)
    derived_metrics: list[dict[str, Any]] = []
    steps = pipeline.definition.get("steps", [])
    for step in steps:
        step_type = step.get("type")
        if step_type == "enrich":
            target = current.setdefault(
                "labels" if pipeline.source_type == "metrics" else "attributes", {}
            )
            target.update(step.get("fields", {}))
        elif step_type == "redact":
            fields = step.get("fields", [])
            for field in fields:
                if "attributes" in current and field in current["attributes"]:
                    current["attributes"][field] = "[REDACTED]"
                if "labels" in current and field in current["labels"]:
                    current["labels"][field] = "[REDACTED]"
        elif step_type == "filter_equals":
            field = step.get("field")
            expected = step.get("value")
            value = current.get(field)
            if value is None:
                value = current.get("attributes", {}).get(
                    field, current.get("labels", {}).get(field)
                )
            if value == expected:
                return None, derived_metrics
        elif step_type == "normalize_field":
            source = step.get("from")
            target = step.get("to")
            if "attributes" in current and source in current["attributes"]:
                current["attributes"][target] = current["attributes"].pop(source)
            if "labels" in current and source in current["labels"]:
                current["labels"][target] = current["labels"].pop(source)
        elif step_type == "route_stream":
            current["_stream_name"] = step.get("stream")
        elif step_type == "logs_to_metric":
            metric_name = step.get("metric_name")
            field = step.get("field")
            if field and "attributes" in current and field in current["attributes"]:
                derived_metrics.append(
                    {
                        "timestamp": current["timestamp"],
                        "metric_name": metric_name,
                        "value": float(current["attributes"][field]),
                        "labels": step.get("labels", {}),
                        "unit": step.get("unit"),
                    }
                )
        else:
            raise ValueError(f"Unsupported pipeline step {step_type}")
    return current, derived_metrics


def apply_pipelines(
    db: Session,
    organization_id: int,
    source_type: str,
    items: list[dict[str, Any]],
    *,
    selected: Pipeline | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    pipelines = (
        [selected] if selected is not None else _load_pipelines(db, organization_id, source_type)
    )
    if not pipelines:
        return items, []
    processed = items
    all_derived: list[dict[str, Any]] = []
    for pipeline in pipelines:
        run = PipelineRun(
            pipeline_id=pipeline.id, status="running", stats={"input": len(processed)}
        )
        db.add(run)
        db.flush()
        next_items: list[dict[str, Any]] = []
        dropped = 0
        pipeline_derived = []
        try:
            for item in processed:
                updated, derived = _apply_steps(item, pipeline)
                if updated is None:
                    dropped += 1
                    continue
                route = updated.pop("_stream_name", None)
                schema = {"logs": LogEventIn, "metrics": MetricPointIn, "traces": TraceSpanIn}[
                    source_type
                ]
                updated = schema.model_validate(updated).model_dump()
                if route:
                    get_stream_or_404(db, organization_id, route, source_type)
                    updated["_stream_name"] = route
                checked_derived = [
                    MetricPointIn.model_validate(metric).model_dump() for metric in derived
                ]
                if checked_derived:
                    get_stream_or_404(db, organization_id, "metrics-default", "metrics")
                next_items.append(updated)
                pipeline_derived.extend(checked_derived)
            run.status = "success"
            run.stats = {"input": len(processed), "output": len(next_items), "dropped": dropped}
            processed = next_items
            all_derived.extend(pipeline_derived)
        except (ValueError, TypeError, HTTPException):
            run.status = "failed"
            run.error_message = (
                "Transformation failed validation; this pipeline was skipped for the whole batch"
            )
            run.stats = {"input": len(processed), "output": len(processed), "failed_open": True}
        finally:
            run.finished_at = utcnow()
    return processed, all_derived


def run_pipeline(
    db: Session,
    principal: Principal,
    pipeline_id: int,
    sample_payload: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    pipeline = db.get(Pipeline, pipeline_id)
    if not pipeline or pipeline.organization_id != principal.organization_id:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    from fastapi.exceptions import RequestValidationError
    from pydantic import ValidationError

    items = sample_payload or []
    if len(items) > 1000:
        raise HTTPException(status_code=422, detail="At most 1000 sample items are allowed")
    schema = {"logs": LogEventIn, "metrics": MetricPointIn, "traces": TraceSpanIn}[
        pipeline.source_type
    ]
    try:
        items = [schema.model_validate(item).model_dump() for item in items]
    except ValidationError as exc:
        raise RequestValidationError(exc.errors()) from exc
    processed, derived = apply_pipelines(
        db, principal.organization_id, pipeline.source_type, items, selected=pipeline
    )
    db.commit()
    return {"processed": processed, "derived_metrics": derived}
