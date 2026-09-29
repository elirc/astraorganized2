from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Dashboard, DashboardPanel
from app.security import Principal, utcnow
from app.services.common import write_audit_log


def upsert_dashboard(
    db: Session, principal: Principal, dashboard_id: int | None, payload: dict
) -> Dashboard:
    if dashboard_id is None:
        dashboard = Dashboard(
            organization_id=principal.organization_id,
            name=payload["name"],
            description=payload.get("description"),
            layout=payload.get("layout", {}),
            created_by=principal.user_id,
        )
        db.add(dashboard)
        db.flush()
    else:
        dashboard = db.get(Dashboard, dashboard_id)
        if not dashboard or dashboard.organization_id != principal.organization_id:
            raise HTTPException(status_code=404, detail="Dashboard not found")
        dashboard.name = payload["name"]
        dashboard.description = payload.get("description")
        dashboard.layout = payload.get("layout", {})
        dashboard.updated_at = utcnow()
        dashboard.panels.clear()

    for panel in payload.get("panels", []):
        dashboard.panels.append(
            DashboardPanel(
                title=panel["title"],
                panel_type=panel["panel_type"],
                position=panel.get("position", {}),
                query=panel.get("query", {}),
                visualization=panel.get("visualization", {}),
            )
        )
    write_audit_log(
        db,
        principal.organization_id,
        principal.user_id,
        "dashboard.upsert",
        "dashboard",
        str(dashboard.id or "new"),
        {"name": dashboard.name},
    )
    db.commit()
    db.refresh(dashboard)
    return dashboard


def serialize_dashboard(dashboard: Dashboard) -> dict:
    return {
        "id": dashboard.id,
        "name": dashboard.name,
        "description": dashboard.description,
        "layout": dashboard.layout,
        "created_at": dashboard.created_at,
        "updated_at": dashboard.updated_at,
        "panels": [
            {
                "id": panel.id,
                "title": panel.title,
                "panel_type": panel.panel_type,
                "position": panel.position,
                "query": panel.query,
                "visualization": panel.visualization,
            }
            for panel in dashboard.panels
        ],
    }
