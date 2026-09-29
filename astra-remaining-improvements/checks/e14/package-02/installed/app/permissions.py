from __future__ import annotations

ROLE_PERMISSIONS: dict[str, set[str]] = {
    "org_admin": {
        "logs:read",
        "logs:write",
        "metrics:read",
        "metrics:write",
        "traces:read",
        "traces:write",
        "dashboards:read",
        "dashboards:write",
        "alerts:read",
        "alerts:write",
        "pipelines:read",
        "pipelines:write",
        "iam:read",
        "iam:write",
        "streams:read",
        "streams:write",
    },
    "org_member": {
        "logs:read",
        "logs:write",
        "metrics:read",
        "metrics:write",
        "traces:read",
        "traces:write",
        "dashboards:read",
        "dashboards:write",
        "alerts:read",
        "alerts:write",
        "pipelines:read",
        "streams:read",
    },
    "viewer": {
        "logs:read",
        "metrics:read",
        "traces:read",
        "dashboards:read",
        "alerts:read",
        "pipelines:read",
        "streams:read",
    },
    "pipeline_admin": {
        "logs:read",
        "metrics:read",
        "traces:read",
        "dashboards:read",
        "alerts:read",
        "pipelines:read",
        "pipelines:write",
        "streams:read",
    },
    "service_account": set(),
}


def allowed_permissions(role: str, scopes: list[str] | None = None) -> set[str]:
    return set(ROLE_PERMISSIONS.get(role, set())) | set(scopes or [])


def has_permission(role: str, scopes: list[str] | None, permission: str) -> bool:
    return permission in allowed_permissions(role, scopes)
