from __future__ import annotations

from collections.abc import Generator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ApiToken, Membership, Organization, User
from app.permissions import ROLE_PERMISSIONS, allowed_permissions, has_permission
from app.security import Principal, hash_token, utcnow

bearer = HTTPBearer(auto_error=False)


def get_db(request: Request) -> Generator[Session, None, None]:
    session_factory = request.app.state.SessionLocal
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def get_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> Principal:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token_value = credentials.credentials
    token = db.scalar(
        select(ApiToken).where(
            ApiToken.token_hash == hash_token(token_value), ApiToken.is_active.is_(True)
        )
    )
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if token.expires_at and token.expires_at <= utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")

    if not db.get(Organization, token.organization_id) or token.role not in ROLE_PERMISSIONS:
        raise HTTPException(status_code=401, detail="Invalid token")
    known = set().union(*ROLE_PERMISSIONS.values())
    if not set(token.scopes or []) <= known:
        raise HTTPException(status_code=401, detail="Invalid token scopes")
    if token.token_type.value == "ingest" and (
        token.role != "service_account"
        or not token.scopes
        or not set(token.scopes) <= {"logs:write", "metrics:write", "traces:write"}
    ):
        raise HTTPException(
            status_code=401, detail="Legacy ingest token needs rotation to explicit write scopes"
        )
    user_email = None
    if token.user_id:
        user = db.get(User, token.user_id)
        membership = db.scalar(
            select(Membership).where(
                Membership.user_id == token.user_id,
                Membership.organization_id == token.organization_id,
            )
        )
        if (
            not user
            or not user.is_active
            or not membership
            or not allowed_permissions(token.role, token.scopes)
            <= allowed_permissions(membership.role)
        ):
            raise HTTPException(status_code=401, detail="User access changed; sign in again")
        user_email = user.email
    return Principal(
        token_id=token.id,
        organization_id=token.organization_id,
        user_id=token.user_id,
        role=token.role,
        token_type=token.token_type.value,
        scopes=token.scopes or [],
        email=user_email,
    )


def require_permission(module: str, action: str):
    permission = f"{module}:{action}"

    def dependency(principal: Principal = Depends(get_principal)) -> Principal:
        if not has_permission(principal.role, principal.scopes, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing permission {permission}"
            )
        return principal

    return dependency


def current_org(db: Session, principal: Principal) -> Organization:
    org = db.get(Organization, principal.organization_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return org


def membership_for_principal(db: Session, principal: Principal) -> Membership | None:
    if not principal.user_id:
        return None
    return db.scalar(
        select(Membership).where(
            Membership.user_id == principal.user_id,
            Membership.organization_id == principal.organization_id,
        )
    )


def permission_list(principal: Principal) -> list[str]:
    return sorted(allowed_permissions(principal.role, principal.scopes))
