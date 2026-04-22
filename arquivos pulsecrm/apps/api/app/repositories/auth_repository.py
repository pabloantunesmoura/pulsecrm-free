from ..db import get_connection


class AuthRepository:
    def list_public_users(self) -> list[dict]:
        query = """
        SELECT users.id, users.name, users.email, users.title, roles.name AS role
        FROM users
        JOIN roles ON roles.id = users.role_id
        ORDER BY users.name
        """
        with get_connection() as connection:
            rows = connection.execute(query).fetchall()
        return [dict(row) for row in rows]

    def find_user_by_email(self, email: str) -> dict | None:
        query = """
        SELECT users.*, roles.name AS role_name, tenants.name AS tenant_name, tenants.slug AS tenant_slug,
               tenants.timezone AS tenant_timezone, tenants.plan AS tenant_plan
        FROM users
        JOIN roles ON roles.id = users.role_id
        JOIN tenants ON tenants.id = users.tenant_id
        WHERE lower(users.email) = lower(?)
        """
        with get_connection() as connection:
            row = connection.execute(query, (email,)).fetchone()
        return dict(row) if row else None

    def create_session(self, token: str, user_id: str, tenant_id: str, created_at: str, expires_at: str) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO sessions (token, user_id, tenant_id, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (token, user_id, tenant_id, created_at, expires_at),
            )

    def find_session(self, token: str) -> dict | None:
        query = """
        SELECT sessions.token, sessions.user_id, sessions.tenant_id, sessions.created_at, sessions.expires_at,
               users.name AS user_name, users.email AS user_email, users.title AS user_title, roles.name AS role_name,
               tenants.name AS tenant_name, tenants.slug AS tenant_slug, tenants.timezone AS tenant_timezone, tenants.plan AS tenant_plan
        FROM sessions
        JOIN users ON users.id = sessions.user_id
        JOIN roles ON roles.id = users.role_id
        JOIN tenants ON tenants.id = sessions.tenant_id
        WHERE sessions.token = ?
        """
        with get_connection() as connection:
          row = connection.execute(query, (token,)).fetchone()
        return dict(row) if row else None
