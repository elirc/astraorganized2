from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from threading import Lock

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from app.config import Settings, settings
from app.crud import build_crud_router
from app.db import build_engine, build_sessionmaker, init_db
from app.deps import current_org, get_db, get_principal, permission_list, require_permission
from app.errors import install_error_handlers
from app.http_boundary import LocalHTTPBoundary
from app.models import (
    AlertDelivery,
    AlertRule,
    ApiToken,
    Pipeline,
    PipelineRun,
)
from app.schemas import (
    BootstrapRequest,
    LoginRequest,
    LogsIngestRequest,
    MetricsIngestRequest,
    MetricsQueryRequest,
    OrgCreateRequest,
    PromQLRequest,
    SearchRequest,
    SQLQueryRequest,
    TokenCreateRequest,
    TokenResponse,
    TraceSearchRequest,
    TracesIngestRequest,
    UserCreateRequest,
)
from app.security import Principal
from app.services.alerts import run_alert
from app.services.auth import (
    bootstrap_platform,
    create_organization,
    create_token_for_org,
    create_user_in_org,
    login_user,
    revoke_token,
)
from app.services.ingestion import ingest_logs, ingest_metrics, ingest_traces
from app.services.pipelines import run_pipeline
from app.services.queries import (
    execute_log_sql,
    execute_metric_sql,
    query_metrics,
    query_metrics_promql,
    search_logs,
    search_traces,
    trace_detail,
)


def create_app(app_settings: Settings | None = None) -> FastAPI:
    cfg = app_settings or settings

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.settings = cfg
        app.state.engine = build_engine(cfg)
        app.state.SessionLocal = build_sessionmaker(app.state.engine)
        app.state.rate_limits = {}
        app.state.limiter_lock = Lock()
        try:
            init_db(app.state.engine)
            yield
        finally:
            app.state.engine.dispose()

    app = FastAPI(title="E14 Observability Platform", version="0.1.0", lifespan=lifespan)
    install_error_handlers(app)
    app.add_middleware(LocalHTTPBoundary, settings=cfg)
    web = Path(__file__).parent / "web"
    app.mount("/assets", StaticFiles(directory=web), name="assets")

    @app.get("/", include_in_schema=False)
    def workspace():
        return FileResponse(web / "index.html")

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.post("/api/v1/setup/bootstrap")
    def bootstrap(payload: BootstrapRequest, db=Depends(get_db)):
        try:
            org, user, token = bootstrap_platform(
                db,
                payload.org_name,
                payload.org_slug,
                payload.email,
                payload.password,
                payload.display_name,
                session_days=cfg.session_days,
            )
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return {
            "organization": {"id": org.id, "name": org.name, "slug": org.slug},
            "user": {"id": user.id, "email": user.email, "display_name": user.display_name},
            "token": token,
        }

    @app.post("/api/v1/auth/login")
    def login(payload: LoginRequest, db=Depends(get_db)):
        try:
            org, user, token, role = login_user(
                db, payload.email, payload.password, payload.org_slug, session_days=cfg.session_days
            )
        except ValueError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc
        except LookupError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except PermissionError as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from exc
        return {
            "organization": {"id": org.id, "name": org.name, "slug": org.slug},
            "user": {"id": user.id, "email": user.email, "display_name": user.display_name},
            "role": role,
            "token": token,
        }

    @app.post("/api/v1/auth/logout")
    def logout(principal: Principal = Depends(get_principal), db=Depends(get_db)):
        try:
            revoke_token(db, principal, principal.token_id)
        except LookupError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return {"revoked": True}

    @app.get("/api/v1/auth/me")
    def me(principal: Principal = Depends(get_principal), db=Depends(get_db)):
        org = current_org(db, principal)
        user = None
        if principal.user_id:
            from app.models import User

            user_model = db.get(User, principal.user_id)
            user = {
                "id": user_model.id,
                "email": user_model.email,
                "display_name": user_model.display_name,
            }
        return {
            "organization": {"id": org.id, "name": org.name, "slug": org.slug},
            "user": user,
            "role": principal.role,
            "scopes": principal.scopes,
            "permissions": permission_list(principal),
        }

    @app.get("/api/v1/orgs/current")
    def org_detail(principal: Principal = Depends(get_principal), db=Depends(get_db)):
        org = current_org(db, principal)
        return {"id": org.id, "name": org.name, "slug": org.slug}

    @app.post("/api/v1/orgs")
    def create_org(
        payload: OrgCreateRequest,
        principal: Principal = Depends(require_permission("iam", "write")),
        db=Depends(get_db),
    ):
        if principal.role != "org_admin" or not principal.user_id:
            raise HTTPException(
                status_code=403,
                detail="Organization provisioning requires a signed-in organization administrator",
            )
        org, user, token = create_organization(
            db,
            payload.org_name,
            payload.org_slug,
            payload.admin_email,
            payload.admin_password,
            payload.admin_display_name,
            session_days=cfg.session_days,
        )
        return {
            "organization": {"id": org.id, "name": org.name, "slug": org.slug},
            "user": {"id": user.id, "email": user.email, "display_name": user.display_name},
            "token": token,
        }

    @app.get("/api/v1/orgs/users")
    def list_users(
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0, le=10000),
        principal: Principal = Depends(require_permission("iam", "read")),
        db=Depends(get_db),
    ):
        from app.models import Membership, User

        rows = db.execute(
            select(User, Membership.role)
            .join(Membership, Membership.user_id == User.id)
            .where(Membership.organization_id == principal.organization_id)
            .order_by(User.id)
            .offset(offset)
            .limit(limit)
        ).all()
        return [
            {
                "id": user.id,
                "email": user.email,
                "display_name": user.display_name,
                "role": role,
                "is_active": user.is_active,
            }
            for user, role in rows
        ]

    @app.post("/api/v1/orgs/users")
    def create_user(
        payload: UserCreateRequest,
        principal: Principal = Depends(require_permission("iam", "write")),
        db=Depends(get_db),
    ):
        user = create_user_in_org(
            db, principal, payload.email, payload.password, payload.display_name, payload.role
        )
        return {"id": user.id, "email": user.email, "display_name": user.display_name}

    @app.get("/api/v1/tokens")
    def list_tokens(
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0, le=10000),
        principal: Principal = Depends(require_permission("iam", "read")),
        db=Depends(get_db),
    ):
        tokens = db.scalars(
            select(ApiToken)
            .where(ApiToken.organization_id == principal.organization_id)
            .order_by(ApiToken.id)
            .offset(offset)
            .limit(limit)
        ).all()
        return [
            {
                "id": token.id,
                "name": token.name,
                "token_prefix": token.token_prefix,
                "token_type": token.token_type.value,
                "role": token.role,
                "scopes": token.scopes,
                "created_at": token.created_at,
                "is_active": token.is_active,
            }
            for token in tokens
        ]

    @app.post("/api/v1/tokens")
    def create_token(
        payload: TokenCreateRequest,
        principal: Principal = Depends(require_permission("iam", "write")),
        db=Depends(get_db),
    ):
        token, plain = create_token_for_org(
            db,
            principal,
            payload.name,
            payload.token_type,
            payload.role,
            payload.scopes,
            payload.expires_in_days,
        )
        return TokenResponse(
            id=token.id,
            name=token.name,
            token_prefix=token.token_prefix,
            token_type=token.token_type.value,
            role=token.role,
            scopes=token.scopes,
            created_at=token.created_at,
            plain_token=plain,
        )

    @app.delete("/api/v1/tokens/{token_id}")
    def delete_token(
        token_id: int,
        principal: Principal = Depends(require_permission("iam", "write")),
        db=Depends(get_db),
    ):
        try:
            revoke_token(db, principal, token_id)
        except LookupError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return {"revoked": True}

    @app.post("/api/v1/ingest/logs/json")
    @app.post("/api/v1/otlp/logs")
    def ingest_logs_route(
        payload: LogsIngestRequest,
        request: Request,
        principal: Principal = Depends(require_permission("logs", "write")),
        db=Depends(get_db),
    ):
        return ingest_logs(
            db, request, principal, payload.stream, [event.model_dump() for event in payload.events]
        )

    @app.post("/api/v1/ingest/metrics")
    @app.post("/api/v1/otlp/metrics")
    def ingest_metrics_route(
        payload: MetricsIngestRequest,
        request: Request,
        principal: Principal = Depends(require_permission("metrics", "write")),
        db=Depends(get_db),
    ):
        return ingest_metrics(
            db, request, principal, payload.stream, [point.model_dump() for point in payload.points]
        )

    @app.post("/api/v1/ingest/traces")
    @app.post("/api/v1/otlp/traces")
    def ingest_traces_route(
        payload: TracesIngestRequest,
        request: Request,
        principal: Principal = Depends(require_permission("traces", "write")),
        db=Depends(get_db),
    ):
        return ingest_traces(
            db, request, principal, payload.stream, [span.model_dump() for span in payload.spans]
        )

    @app.post("/api/v1/logs/search")
    def logs_search(
        payload: SearchRequest,
        principal: Principal = Depends(require_permission("logs", "read")),
        db=Depends(get_db),
    ):
        return search_logs(db, principal, payload, cfg.query_scan_limit, cfg.query_row_limit)

    @app.post("/api/v1/logs/sql")
    def logs_sql(
        payload: SQLQueryRequest,
        principal: Principal = Depends(require_permission("logs", "read")),
        db=Depends(get_db),
    ):
        return execute_log_sql(
            db,
            principal,
            payload.start_time,
            payload.end_time,
            payload.query,
            payload.limit,
            cfg.query_scan_limit,
            cfg.query_row_limit,
            cfg.query_timeout_ms,
        )

    @app.post("/api/v1/metrics/query")
    def metrics_query(
        payload: MetricsQueryRequest,
        principal: Principal = Depends(require_permission("metrics", "read")),
        db=Depends(get_db),
    ):
        return query_metrics(db, principal, payload, cfg.query_scan_limit, cfg.query_row_limit)

    @app.post("/api/v1/metrics/sql")
    def metrics_sql(
        payload: SQLQueryRequest,
        principal: Principal = Depends(require_permission("metrics", "read")),
        db=Depends(get_db),
    ):
        return execute_metric_sql(
            db,
            principal,
            payload.start_time,
            payload.end_time,
            payload.query,
            payload.limit,
            cfg.query_scan_limit,
            cfg.query_row_limit,
            cfg.query_timeout_ms,
        )

    @app.post("/api/v1/metrics/promql")
    def metrics_promql(
        payload: PromQLRequest,
        principal: Principal = Depends(require_permission("metrics", "read")),
        db=Depends(get_db),
    ):
        return query_metrics_promql(
            db,
            principal,
            payload.start_time,
            payload.end_time,
            payload.query,
            payload.step_seconds,
            cfg.query_scan_limit,
            cfg.query_row_limit,
        )

    @app.post("/api/v1/traces/search")
    def traces_search(
        payload: TraceSearchRequest,
        principal: Principal = Depends(require_permission("traces", "read")),
        db=Depends(get_db),
    ):
        return search_traces(db, principal, payload, cfg.query_scan_limit, cfg.query_row_limit)

    @app.get("/api/v1/traces/{trace_id}")
    def traces_detail(
        trace_id: str,
        principal: Principal = Depends(require_permission("traces", "read")),
        db=Depends(get_db),
    ):
        return trace_detail(db, principal, trace_id)

    @app.post("/api/v1/alerts/{alert_id}/test")
    def alerts_test(
        alert_id: int,
        principal: Principal = Depends(require_permission("alerts", "write")),
        db=Depends(get_db),
    ):
        alert = db.get(AlertRule, alert_id)
        if not alert or alert.organization_id != principal.organization_id:
            raise HTTPException(status_code=404, detail="Alert not found")
        return run_alert(db, principal, alert, cfg)

    @app.post("/api/v1/alerts/evaluate")
    def alerts_evaluate(
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0, le=10000),
        principal: Principal = Depends(require_permission("alerts", "write")),
        db=Depends(get_db),
    ):
        alerts = db.scalars(
            select(AlertRule)
            .where(
                AlertRule.organization_id == principal.organization_id, AlertRule.enabled.is_(True)
            )
            .order_by(AlertRule.id)
            .offset(offset)
            .limit(limit)
        ).all()
        return [run_alert(db, principal, alert, cfg) for alert in alerts]

    @app.get("/api/v1/alerts/{alert_id}/deliveries")
    def alerts_deliveries(
        alert_id: int,
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0, le=10000),
        principal: Principal = Depends(require_permission("alerts", "read")),
        db=Depends(get_db),
    ):
        alert = db.get(AlertRule, alert_id)
        if not alert or alert.organization_id != principal.organization_id:
            raise HTTPException(status_code=404, detail="Alert not found")
        deliveries = db.scalars(
            select(AlertDelivery)
            .where(AlertDelivery.alert_rule_id == alert_id)
            .order_by(AlertDelivery.id.desc())
            .offset(offset)
            .limit(limit)
        ).all()
        return [
            {
                "id": delivery.id,
                "status": delivery.status,
                "destination": delivery.destination,
                "payload": delivery.payload,
                "fired_at": delivery.fired_at,
            }
            for delivery in deliveries
        ]

    @app.post("/api/v1/pipelines/{pipeline_id}/run")
    def pipelines_run(
        pipeline_id: int,
        payload: list[dict] | None = None,
        principal: Principal = Depends(require_permission("pipelines", "write")),
        db=Depends(get_db),
    ):
        return run_pipeline(db, principal, pipeline_id, payload)

    @app.get("/api/v1/pipelines/{pipeline_id}/runs")
    def pipelines_runs(
        pipeline_id: int,
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0, le=10000),
        principal: Principal = Depends(require_permission("pipelines", "read")),
        db=Depends(get_db),
    ):
        pipeline = db.get(Pipeline, pipeline_id)
        if not pipeline or pipeline.organization_id != principal.organization_id:
            raise HTTPException(status_code=404, detail="Pipeline not found")
        runs = db.scalars(
            select(PipelineRun)
            .where(PipelineRun.pipeline_id == pipeline_id)
            .order_by(PipelineRun.started_at.desc(), PipelineRun.id.desc())
            .offset(offset)
            .limit(limit)
        ).all()
        return [
            {
                "id": run.id,
                "status": run.status,
                "started_at": run.started_at,
                "finished_at": run.finished_at,
                "stats": run.stats,
                "error_message": run.error_message,
            }
            for run in runs
        ]

    app.include_router(build_crud_router())
    return app
