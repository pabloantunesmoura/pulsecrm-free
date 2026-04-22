import json
from typing import Any

from ..db import get_connection


def _with_tags(row: dict) -> dict:
    hydrated = dict(row)
    hydrated["tags"] = json.loads(hydrated.get("tags") or "[]")
    return hydrated


class CrmRepository:
    def get_tenant(self, tenant_id: str) -> dict | None:
        with get_connection() as connection:
            row = connection.execute("SELECT * FROM tenants WHERE id = ?", (tenant_id,)).fetchone()
        return dict(row) if row else None

    def list_users(self, tenant_id: str) -> list[dict]:
        query = """
        SELECT users.id, users.name, users.email, users.title, users.team_id, roles.name AS role
        FROM users
        JOIN roles ON roles.id = users.role_id
        WHERE users.tenant_id = ?
        ORDER BY users.name
        """
        with get_connection() as connection:
            rows = connection.execute(query, (tenant_id,)).fetchall()
        return [dict(row) for row in rows]

    def list_teams(self, tenant_id: str) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute("SELECT * FROM teams WHERE tenant_id = ? ORDER BY name", (tenant_id,)).fetchall()
        return [dict(row) for row in rows]

    def list_roles(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute("SELECT * FROM roles ORDER BY name").fetchall()
        return [dict(row) for row in rows]

    def list_leads(self, tenant_id: str) -> list[dict]:
        query = """
        SELECT leads.*, users.name AS owner, pipeline_stages.name AS stage
        FROM leads
        LEFT JOIN users ON users.id = leads.owner_id
        LEFT JOIN pipeline_stages ON pipeline_stages.id = leads.stage_id
        WHERE leads.tenant_id = ?
        ORDER BY leads.updated_at DESC, leads.created_at DESC
        """
        with get_connection() as connection:
            rows = connection.execute(query, (tenant_id,)).fetchall()
        return [_with_tags(dict(row)) for row in rows]

    def create_lead(self, payload: dict) -> dict:
        query = """
        INSERT INTO leads (
          id, tenant_id, owner_id, company, name, email, phone, source, status, score,
          stage_id, tags, last_interaction_at, next_action, notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            payload["id"],
            payload["tenant_id"],
            payload["owner_id"],
            payload["company"],
            payload["name"],
            payload["email"],
            payload["phone"],
            payload["source"],
            payload["status"],
            payload["score"],
            payload["stage_id"],
            json.dumps(payload["tags"]),
            payload["last_interaction_at"],
            payload["next_action"],
            payload["notes"],
            payload["created_at"],
            payload["updated_at"],
        )
        with get_connection() as connection:
            connection.execute(query, params)
        return payload

    def update_lead(self, lead_id: str, tenant_id: str, updates: dict) -> dict | None:
        current = self.get_lead(lead_id, tenant_id)
        if not current:
            return None

        next_payload = {
            **current,
            "status": updates.get("status", current["status"]),
            "score": updates.get("score", current["score"]),
            "stage_id": updates.get("stage_id", current["stage_id"]),
            "next_action": updates.get("next_action", current["next_action"]),
            "notes": updates.get("notes", current["notes"]),
            "updated_at": updates.get("updated_at", current["updated_at"]),
        }
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE leads
                SET status = ?, score = ?, stage_id = ?, next_action = ?, notes = ?, updated_at = ?
                WHERE id = ? AND tenant_id = ?
                """,
                (
                    next_payload["status"],
                    next_payload["score"],
                    next_payload["stage_id"],
                    next_payload["next_action"],
                    next_payload["notes"],
                    next_payload["updated_at"],
                    lead_id,
                    tenant_id,
                ),
            )
        return self.get_lead(lead_id, tenant_id)

    def get_lead(self, lead_id: str, tenant_id: str) -> dict | None:
        query = """
        SELECT leads.*, users.name AS owner, pipeline_stages.name AS stage
        FROM leads
        LEFT JOIN users ON users.id = leads.owner_id
        LEFT JOIN pipeline_stages ON pipeline_stages.id = leads.stage_id
        WHERE leads.id = ? AND leads.tenant_id = ?
        """
        with get_connection() as connection:
            row = connection.execute(query, (lead_id, tenant_id)).fetchone()
        return _with_tags(dict(row)) if row else None

    def list_pipeline_stages(self, tenant_id: str) -> list[dict]:
        query = """
        SELECT pipeline_stages.id, pipeline_stages.pipeline_id, pipeline_stages.name, pipeline_stages.position, pipeline_stages.probability
        FROM pipeline_stages
        JOIN pipelines ON pipelines.id = pipeline_stages.pipeline_id
        WHERE pipelines.tenant_id = ?
        ORDER BY pipeline_stages.position
        """
        with get_connection() as connection:
            rows = connection.execute(query, (tenant_id,)).fetchall()
        return [dict(row) for row in rows]

    def list_deals(self, tenant_id: str) -> list[dict]:
        query = """
        SELECT deals.*, users.name AS owner
        FROM deals
        LEFT JOIN users ON users.id = deals.owner_id
        WHERE deals.tenant_id = ?
        ORDER BY deals.updated_at DESC
        """
        with get_connection() as connection:
            rows = connection.execute(query, (tenant_id,)).fetchall()
        return [dict(row) for row in rows]

    def update_deal(self, deal_id: str, tenant_id: str, updates: dict) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM deals WHERE id = ? AND tenant_id = ?",
                (deal_id, tenant_id),
            ).fetchone()
            if not row:
                return None
            current = dict(row)
            connection.execute(
                """
                UPDATE deals
                SET stage_id = ?, status = ?, updated_at = ?
                WHERE id = ? AND tenant_id = ?
                """,
                (
                    updates.get("stage_id", current["stage_id"]),
                    updates.get("status", current["status"]),
                    updates.get("updated_at", current["updated_at"]),
                    deal_id,
                    tenant_id,
                ),
            )
        return self.get_deal(deal_id, tenant_id)

    def get_deal(self, deal_id: str, tenant_id: str) -> dict | None:
        query = """
        SELECT deals.*, users.name AS owner
        FROM deals
        LEFT JOIN users ON users.id = deals.owner_id
        WHERE deals.id = ? AND deals.tenant_id = ?
        """
        with get_connection() as connection:
            row = connection.execute(query, (deal_id, tenant_id)).fetchone()
        return dict(row) if row else None

    def list_tasks(self, tenant_id: str) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT tasks.*, users.name AS owner
                FROM tasks
                LEFT JOIN users ON users.id = tasks.owner_id
                WHERE tasks.tenant_id = ?
                ORDER BY tasks.due_at ASC
                """,
                (tenant_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_agenda(self, tenant_id: str) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT calendar_events.*, users.name AS owner
                FROM calendar_events
                LEFT JOIN users ON users.id = calendar_events.owner_id
                WHERE calendar_events.tenant_id = ?
                ORDER BY calendar_events.starts_at ASC
                """,
                (tenant_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_automations(self, tenant_id: str) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM automations WHERE tenant_id = ? ORDER BY created_at DESC",
                (tenant_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_invitations(self, tenant_id: str) -> list[dict]:
        query = """
        SELECT invitations.*, users.name AS inviter_name, roles.name AS role_name
        FROM invitations
        JOIN users ON users.id = invitations.inviter_user_id
        JOIN roles ON roles.id = invitations.role_id
        WHERE invitations.tenant_id = ?
        ORDER BY invitations.created_at DESC
        """
        with get_connection() as connection:
            rows = connection.execute(query, (tenant_id,)).fetchall()
        return [dict(row) for row in rows]

    def find_invitation_by_token(self, invite_token: str) -> dict | None:
        query = """
        SELECT invitations.*, users.name AS inviter_name, roles.name AS role_name, tenants.name AS tenant_name
        FROM invitations
        JOIN users ON users.id = invitations.inviter_user_id
        JOIN roles ON roles.id = invitations.role_id
        JOIN tenants ON tenants.id = invitations.tenant_id
        WHERE invitations.invite_token = ?
        """
        with get_connection() as connection:
            row = connection.execute(query, (invite_token,)).fetchone()
        return dict(row) if row else None

    def create_invitation(self, payload: dict) -> dict:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO invitations (
                  id, tenant_id, inviter_user_id, email, role_id, status, invite_token, created_at, accepted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["id"],
                    payload["tenant_id"],
                    payload["inviter_user_id"],
                    payload["email"],
                    payload["role_id"],
                    payload["status"],
                    payload["invite_token"],
                    payload["created_at"],
                    payload["accepted_at"],
                ),
            )

        query = """
        SELECT invitations.*, users.name AS inviter_name, roles.name AS role_name
        FROM invitations
        JOIN users ON users.id = invitations.inviter_user_id
        JOIN roles ON roles.id = invitations.role_id
        WHERE invitations.id = ?
        """
        with get_connection() as connection:
            row = connection.execute(query, (payload["id"],)).fetchone()
        return dict(row)

    def find_user_by_email(self, tenant_id: str, email: str) -> dict | None:
        query = """
        SELECT users.*, roles.name AS role_name
        FROM users
        JOIN roles ON roles.id = users.role_id
        WHERE users.tenant_id = ? AND lower(users.email) = lower(?)
        """
        with get_connection() as connection:
            row = connection.execute(query, (tenant_id, email)).fetchone()
        return dict(row) if row else None

    def create_user(self, payload: dict) -> dict:
        query = """
        INSERT INTO users (
          id, tenant_id, team_id, role_id, name, email, password_hash, phone, title, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with get_connection() as connection:
            connection.execute(
                query,
                (
                    payload["id"],
                    payload["tenant_id"],
                    payload["team_id"],
                    payload["role_id"],
                    payload["name"],
                    payload["email"],
                    payload["password_hash"],
                    payload["phone"],
                    payload["title"],
                    payload["created_at"],
                ),
            )

        return self.find_user_by_email(payload["tenant_id"], payload["email"])

    def accept_invitation(self, invitation_id: str, accepted_at: str) -> dict | None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE invitations
                SET status = 'ACCEPTED', accepted_at = ?
                WHERE id = ?
                """,
                (accepted_at, invitation_id),
            )

        query = """
        SELECT invitations.*, users.name AS inviter_name, roles.name AS role_name, tenants.name AS tenant_name
        FROM invitations
        JOIN users ON users.id = invitations.inviter_user_id
        JOIN roles ON roles.id = invitations.role_id
        JOIN tenants ON tenants.id = invitations.tenant_id
        WHERE invitations.id = ?
        """
        with get_connection() as connection:
            row = connection.execute(query, (invitation_id,)).fetchone()
        return dict(row) if row else None

    def list_activity(self, tenant_id: str) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT * FROM activity_logs
                WHERE tenant_id = ?
                ORDER BY happened_at DESC
                """,
                (tenant_id,),
            ).fetchall()
        return [
            {
                **dict(row),
                "at": dict(row)["happened_at"],
            }
            for row in rows
        ]

    def create_activity(self, item: dict[str, Any]) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO activity_logs (id, tenant_id, lead_id, type, summary, happened_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    item["id"],
                    item["tenant_id"],
                    item.get("lead_id"),
                    item["type"],
                    item["summary"],
                    item["happened_at"],
                ),
            )
