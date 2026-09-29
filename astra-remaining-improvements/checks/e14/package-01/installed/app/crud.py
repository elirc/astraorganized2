"""Shared CRUD mechanics with explicit resource schemas and tenant boundaries."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response
from sqlalchemy import delete, func, select, text

from app.deps import get_db, get_principal
from app.models import (
    AlertDelivery,
    AlertRule,
    Dashboard,
    DashboardPanel,
    LogEvent,
    MetricPoint,
    Pipeline,
    PipelineRun,
    SavedQuery,
    Stream,
    TraceSpan,
)
from app.permissions import has_permission
from app.schemas import (
    AlertRequest,
    DashboardRequest,
    PipelineRequest,
    SavedQueryRequest,
    StreamCreateRequest,
)
from app.security import Principal, utcnow
from app.services.common import get_stream_or_404, write_audit_log
from app.services.dashboards import serialize_dashboard


@dataclass(frozen=True)
class Resource:
    path: str
    model: type
    schema: type
    permission: str
    fields: tuple[str, ...]


RESOURCES = (
    Resource(
        "streams",
        Stream,
        StreamCreateRequest,
        "streams",
        ("name", "type", "retention_days", "indexing_options", "max_payload_bytes"),
    ),
    Resource(
        "dashboards", Dashboard, DashboardRequest, "dashboards", ("name", "description", "layout")
    ),
    Resource(
        "alerts",
        AlertRule,
        AlertRequest,
        "alerts",
        ("name", "module", "condition", "notifications", "enabled", "dedupe_window_seconds"),
    ),
    Resource(
        "pipelines",
        Pipeline,
        PipelineRequest,
        "pipelines",
        ("name", "source_type", "schedule", "definition", "enabled"),
    ),
    Resource(
        "saved-queries",
        SavedQuery,
        SavedQueryRequest,
        "",
        ("module", "name", "query_text", "params"),
    ),
)


def permit(principal, module, action):
    if not has_permission(principal.role, principal.scopes, f"{module}:{action}"):
        raise HTTPException(status_code=403, detail=f"Missing permission {module}:{action}")


def scoped_record(db, principal, resource, record_id):
    record = db.scalar(
        select(resource.model).where(
            resource.model.id == record_id,
            resource.model.organization_id == principal.organization_id,
        )
    )
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


def check_revision(record, header):
    if header is None:
        raise HTTPException(
            status_code=428, detail="If-Match is required; load this record before changing it"
        )
    if not re.fullmatch(r'"v[1-9][0-9]{0,15}"', header):
        raise HTTPException(
            status_code=400, detail='If-Match must be a single version such as "v1"'
        )
    if header != f'"v{record.version}"':
        raise HTTPException(
            status_code=409,
            detail="This record changed. Reload it and review your draft before retrying",
        )


def serialize(resource, record):
    if resource.model is Dashboard:
        return {**serialize_dashboard(record), "version": record.version}
    result = {"id": record.id, "version": record.version}
    for name in resource.fields:
        value = getattr(record, name)
        result[name] = value.value if isinstance(value, Enum) else value
    return result


def validate_references(db, principal, resource, payload, existing=None):
    if resource.model is Pipeline:
        for step in payload.definition["steps"]:
            if step["type"] == "route_stream":
                get_stream_or_404(
                    db, principal.organization_id, step["stream"], payload.source_type
                )
    if resource.model is Stream:
        if existing is None:
            count = db.scalar(
                select(func.count())
                .select_from(Stream)
                .where(Stream.organization_id == principal.organization_id)
            )
            if count >= 1000:
                raise HTTPException(
                    status_code=409, detail="An organization may have at most 1000 streams"
                )
        elif payload.name != existing.name or payload.type != existing.type.value:
            assert_stream_unused(db, principal, existing)


def assert_stream_unused(db, principal, stream):
    if stream.name in {"logs-default", "metrics-default", "traces-default"}:
        raise HTTPException(
            status_code=409, detail="Default streams cannot be renamed, retyped or deleted"
        )
    for model in (LogEvent, MetricPoint, TraceSpan):
        if db.scalar(select(model.id).where(model.stream_id == stream.id).limit(1)) is not None:
            raise HTTPException(
                status_code=409,
                detail="Stream contains telemetry; retain it or change its retention policy",
            )
    pipelines = db.scalars(
        select(Pipeline).where(Pipeline.organization_id == principal.organization_id)
    )
    for pipeline in pipelines:
        if any(step.get("stream") == stream.name for step in pipeline.definition.get("steps", [])):
            raise HTTPException(
                status_code=409,
                detail="A pipeline references this stream; update the pipeline first",
            )


def apply_values(resource, record, payload):
    values = payload.model_dump(mode="json")
    for field in resource.fields:
        setattr(record, field, values[field])
    if resource.model is Dashboard:
        record.updated_at = utcnow()
        record.panels.clear()
        record.panels.extend(DashboardPanel(**panel) for panel in values["panels"])


def register_resource(router, resource):
    # Each closure captures one immutable Resource; no user input selects a model.
    path = "/api/v1/" + resource.path

    def list_records(
        response: Response,
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0, le=10000),
        principal: Principal = Depends(get_principal),
        db=Depends(get_db),
    ):
        query = select(resource.model).where(
            resource.model.organization_id == principal.organization_id
        )
        if resource.permission:
            permit(principal, resource.permission, "read")
        else:
            modules = [
                module
                for module in ("logs", "metrics", "traces")
                if has_permission(principal.role, principal.scopes, module + ":read")
            ]
            if not modules:
                raise HTTPException(status_code=403, detail="No telemetry read permission")
            query = query.where(SavedQuery.module.in_(modules))
        total = db.scalar(select(func.count()).select_from(query.subquery()))
        response.headers["X-Total-Count"] = str(total)
        response.headers["Cache-Control"] = "no-store"
        rows = db.scalars(query.order_by(resource.model.id).offset(offset).limit(limit)).all()
        return [serialize(resource, record) for record in rows]

    def get_record(
        record_id: int,
        response: Response,
        principal: Principal = Depends(get_principal),
        db=Depends(get_db),
    ):
        record = scoped_record(db, principal, resource, record_id)
        permit(principal, resource.permission or record.module, "read")
        response.headers["ETag"] = f'"v{record.version}"'
        response.headers["Cache-Control"] = "no-store"
        return serialize(resource, record)

    def create_record(
        payload,
        response: Response,
        principal: Principal = Depends(get_principal),
        db=Depends(get_db),
    ):
        permit(principal, resource.permission or payload.module, "write")
        db.execute(text("BEGIN IMMEDIATE"))
        validate_references(db, principal, resource, payload)
        record = resource.model(organization_id=principal.organization_id)
        if resource.model is Dashboard:
            record.created_by = principal.user_id
        apply_values(resource, record, payload)
        db.add(record)
        db.flush()
        write_audit_log(
            db,
            principal.organization_id,
            principal.user_id,
            resource.path + ".create",
            resource.path,
            str(record.id),
        )
        db.commit()
        response.headers["ETag"] = f'"v{record.version}"'
        return serialize(resource, record)

    def update_record(
        record_id: int,
        payload,
        response: Response,
        if_match: str | None = Header(None),
        principal: Principal = Depends(get_principal),
        db=Depends(get_db),
    ):
        db.execute(text("BEGIN IMMEDIATE"))
        record = scoped_record(db, principal, resource, record_id)
        permit(principal, resource.permission or record.module, "write")
        if resource.model is SavedQuery:
            permit(principal, payload.module, "write")
        check_revision(record, if_match)
        validate_references(db, principal, resource, payload, record)
        apply_values(resource, record, payload)
        # Advance even for equal-value writes and panel-only edits. SQLAlchemy's
        # version predicate also detects a competing commit after our read.
        record.version += 1
        write_audit_log(
            db,
            principal.organization_id,
            principal.user_id,
            resource.path + ".update",
            resource.path,
            str(record.id),
        )
        db.commit()
        response.headers["ETag"] = f'"v{record.version}"'
        return serialize(resource, record)

    def delete_record(
        record_id: int,
        if_match: str | None = Header(None),
        principal: Principal = Depends(get_principal),
        db=Depends(get_db),
    ):
        db.execute(text("BEGIN IMMEDIATE"))
        record = scoped_record(db, principal, resource, record_id)
        permit(principal, resource.permission or record.module, "write")
        check_revision(record, if_match)
        if resource.model is Stream:
            assert_stream_unused(db, principal, record)
        if resource.model is Pipeline:
            db.execute(delete(PipelineRun).where(PipelineRun.pipeline_id == record.id))
        if resource.model is AlertRule:
            unresolved = db.scalar(
                select(AlertDelivery.id)
                .where(
                    AlertDelivery.alert_rule_id == record.id,
                    AlertDelivery.status.in_(["pending", "sending", "uncertain"]),
                )
                .limit(1)
            )
            if unresolved is not None:
                raise HTTPException(
                    status_code=409,
                    detail="Resolve pending or uncertain deliveries before deleting this alert",
                )
            db.execute(delete(AlertDelivery).where(AlertDelivery.alert_rule_id == record.id))
        db.delete(record)
        write_audit_log(
            db,
            principal.organization_id,
            principal.user_id,
            resource.path + ".delete",
            resource.path,
            str(record.id),
        )
        db.commit()
        return {"deleted": True}

    # Bind the concrete request model before FastAPI inspects these endpoints.
    create_record.__annotations__["payload"] = resource.schema
    update_record.__annotations__["payload"] = resource.schema
    for suffix, method, handler in [
        ("", "GET", list_records),
        ("", "POST", create_record),
        ("/{record_id}", "GET", get_record),
        ("/{record_id}", "PUT", update_record),
        ("/{record_id}", "DELETE", delete_record),
    ]:
        router.add_api_route(
            path + suffix, handler, methods=[method], name=resource.path + "_" + handler.__name__
        )


def build_crud_router():
    router = APIRouter()
    for resource in RESOURCES:
        register_resource(router, resource)
    return router
