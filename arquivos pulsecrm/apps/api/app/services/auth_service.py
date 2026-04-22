from datetime import datetime

from ..repositories.auth_repository import AuthRepository
from ..security import create_session_token, hash_password, iso_after_session_ttl, iso_now


class AuthService:
    def __init__(self) -> None:
        self.repository = AuthRepository()

    def list_public_users(self) -> list[dict]:
        return self.repository.list_public_users()

    def login(self, email: str, password: str) -> dict | None:
        user = self.repository.find_user_by_email(email)
        if not user or user["password_hash"] != hash_password(password):
            return None

        token = create_session_token()
        created_at = iso_now()
        expires_at = iso_after_session_ttl()
        self.repository.create_session(token, user["id"], user["tenant_id"], created_at, expires_at)

        return {
            "token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "title": user["title"],
                "role": user["role_name"],
            },
            "tenant": {
                "id": user["tenant_id"],
                "name": user["tenant_name"],
                "slug": user["tenant_slug"],
                "timezone": user["tenant_timezone"],
                "plan": user["tenant_plan"],
            },
        }

    def authenticate(self, authorization_header: str | None) -> dict | None:
        if not authorization_header or not authorization_header.startswith("Bearer "):
            return None

        token = authorization_header.removeprefix("Bearer ").strip()
        session = self.repository.find_session(token)
        if not session:
            return None

        if datetime.fromisoformat(session["expires_at"]) <= datetime.fromisoformat(iso_now()):
            return None

        return {
            "token": session["token"],
            "tenant_id": session["tenant_id"],
            "user": {
                "id": session["user_id"],
                "name": session["user_name"],
                "email": session["user_email"],
                "title": session["user_title"],
                "role": session["role_name"],
            },
            "tenant": {
                "id": session["tenant_id"],
                "name": session["tenant_name"],
                "slug": session["tenant_slug"],
                "timezone": session["tenant_timezone"],
                "plan": session["tenant_plan"],
            },
        }
