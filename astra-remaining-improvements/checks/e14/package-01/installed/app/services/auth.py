from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.models import Organization, TokenType, User
from app.permissions import allowed_permissions
from app.security import Principal, create_api_token, hash_password, verify_password
from app.services.common import ensure_default_streams, write_audit_log


def bootstrap_platform(
    db: Session,
    org_name: str,
    org_slug: str,
    email: str,
    password: str,
    display_name: str,
    session_days: int = 7,
) -> tuple[Organization, User, str]:
    db.execute(text("BEGIN IMMEDIATE"))
    existing_orgs = db.scalar(select(func.count()).select_from(Organization))
    if existing_orgs:
        raise ValueError("Bootstrap already completed")
    return create_organization(
        db,
        org_name,
        org_slug,
        email,
        password,
        display_name,
        audit_action="bootstrap",
        session_days=session_days,
    )


def create_organization(
    db: Session,
    org_name: str,
    org_slug: str,
    email: str,
    password: str,
    display_name: str,
    audit_action: str = "organization.create",
    session_days: int = 7,
) -> tuple[Organization, User, str]:
    from app.models import Membership

    org = Organization(name=org_name, slug=org_slug)
    user = User(email=email, password_hash=hash_password(password), display_name=display_name)
    db.add_all([org, user])
    db.flush()
    db.add(Membership(user_id=user.id, organization_id=org.id, role="org_admin"))
    ensure_default_streams(db, org)
    token, plain = create_api_token(
        org.id, "org-admin", TokenType.user, "org_admin", [], user.id, expires_in_days=session_days
    )
    db.add(token)
    write_audit_log(
        db, org.id, user.id, audit_action, "organization", str(org.id), {"org_slug": org_slug}
    )
    db.commit()
    return org, user, plain


def login_user(
    db: Session, email: str, password: str, org_slug: str, session_days: int = 7
) -> tuple[Organization, User, str, str]:
    from app.models import Membership

    user = db.scalar(select(User).where(func.lower(User.email) == email.lower()))
    if not user or not user.is_active or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")
    org = db.scalar(select(Organization).where(Organization.slug == org_slug))
    if not org:
        raise ValueError("Invalid credentials")
    membership = db.scalar(
        select(Membership).where(
            Membership.user_id == user.id, Membership.organization_id == org.id
        )
    )
    if not membership:
        raise ValueError("Invalid credentials")
    token, plain = create_api_token(
        org.id,
        f"login-{user.email}",
        TokenType.user,
        membership.role,
        [],
        user.id,
        expires_in_days=session_days,
    )
    db.add(token)
    db.commit()
    return org, user, plain, membership.role


def create_user_in_org(
    db: Session,
    principal: Principal,
    email: str,
    password: str,
    display_name: str,
    role: str,
) -> User:
    from app.models import Membership

    if not allowed_permissions(role) <= allowed_permissions(principal.role, principal.scopes):
        raise HTTPException(status_code=403, detail="Cannot grant permissions you do not hold")
    user = User(email=email, password_hash=hash_password(password), display_name=display_name)
    db.add(user)
    db.flush()
    db.add(Membership(user_id=user.id, organization_id=principal.organization_id, role=role))
    write_audit_log(
        db,
        principal.organization_id,
        principal.user_id,
        "user.create",
        "user",
        str(user.id),
        {"role": role},
    )
    db.commit()
    return user


def create_token_for_org(
    db: Session,
    principal: Principal,
    name: str,
    token_type: str,
    role: str,
    scopes: list[str],
    expires_in_days: int | None,
):
    if not allowed_permissions(role, scopes) <= allowed_permissions(
        principal.role, principal.scopes
    ):
        raise HTTPException(status_code=403, detail="Cannot grant permissions you do not hold")
    if token_type == "user" and not principal.user_id:
        raise HTTPException(status_code=403, detail="A user token requires a signed-in user")
    token, plain = create_api_token(
        principal.organization_id,
        name,
        TokenType(token_type),
        role,
        scopes,
        user_id=principal.user_id if token_type == "user" else None,
        expires_in_days=expires_in_days,
    )
    db.add(token)
    db.flush()
    write_audit_log(
        db,
        principal.organization_id,
        principal.user_id,
        "token.create",
        "api_token",
        str(token.id),
        {"name": name, "type": token_type},
    )
    db.commit()
    db.refresh(token)
    return token, plain


def revoke_token(db: Session, principal: Principal, token_id: int) -> None:
    from app.models import ApiToken

    token = db.get(ApiToken, token_id)
    if not token or token.organization_id != principal.organization_id:
        raise LookupError("Token not found")
    token.is_active = False
    write_audit_log(
        db, principal.organization_id, principal.user_id, "token.revoke", "api_token", str(token_id)
    )
    db.commit()
