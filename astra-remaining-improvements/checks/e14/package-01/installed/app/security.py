from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.models import ApiToken, TokenType

PBKDF2_ROUNDS = 310_000


@dataclass(slots=True)
class Principal:
    token_id: int
    organization_id: int
    user_id: int | None
    role: str
    token_type: str
    scopes: list[str]
    email: str | None = None


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def hash_password(password: str, salt: str | None = None) -> str:
    salt_value = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt_value.encode("utf-8"), PBKDF2_ROUNDS
    )
    return f"pbkdf2_sha256${PBKDF2_ROUNDS}${salt_value}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, rounds, salt, digest = stored_hash.split("$", 3)
        iterations = int(rounds)
    except (AttributeError, TypeError, ValueError):
        return False
    if (
        algorithm != "pbkdf2_sha256"
        or not 100_000 <= iterations <= 1_000_000
        or not 1 <= len(salt) <= 128
        or len(digest) != 64
    ):
        return False
    check = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
    )
    return hmac.compare_digest(check.hex(), digest)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_token_value() -> str:
    return f"obs_{secrets.token_urlsafe(32)}"


def token_prefix(token: str) -> str:
    return token[:16]


def create_api_token(
    organization_id: int,
    name: str,
    token_type: TokenType,
    role: str,
    scopes: list[str],
    user_id: int | None = None,
    expires_in_days: int | None = 7,
) -> tuple[ApiToken, str]:
    plain = generate_token_value()
    expires_at = utcnow() + timedelta(days=expires_in_days) if expires_in_days else None
    token = ApiToken(
        organization_id=organization_id,
        user_id=user_id,
        name=name,
        token_hash=hash_token(plain),
        token_prefix=token_prefix(plain),
        token_type=token_type,
        role=role,
        scopes=scopes,
        expires_at=expires_at,
    )
    return token, plain
