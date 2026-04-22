import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from .config import SESSION_TTL_HOURS


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat()


def iso_after_session_ttl() -> str:
    return (utc_now() + timedelta(hours=SESSION_TTL_HOURS)).isoformat()


def hash_password(raw_password: str) -> str:
    payload = f"pulsecrm-demo::{raw_password}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def create_session_token() -> str:
    return secrets.token_hex(24)
