from uuid import uuid4

from ..repositories.crm_repository import CrmRepository
from ..security import hash_password, iso_now
from .auth_service import AuthService


class CrmService:
    def __init__(self) -> None:
        self.repository = CrmRepository()
        self.auth_service = AuthService()

    def get_bootstrap(self, tenant_id: str) -> dict:
        tenant = self.repository.get_tenant(tenant_id)
        return {
            "tenant": tenant,
            "users": self.repository.list_users(tenant_id),
            "tasks": self.repository.list_tasks(tenant_id),
            "agenda": self.repository.list_agenda(tenant_id),
            "automations": self.repository.list_automations(tenant_id),
            "activity": self.repository.list_activity(tenant_id),
            "invitations": self.repository.list_invitations(tenant_id),
            "roles": self.repository.list_roles(),
        }

    def list_leads(self, tenant_id: str) -> list[dict]:
        return self.repository.list_leads(tenant_id)

    def create_lead(self, tenant_id: str, owner_id: str | None, payload: dict) -> dict:
        lead = {
            "id": f"lead-{uuid4().hex[:8]}",
            "tenant_id": tenant_id,
            "owner_id": owner_id,
            "company": payload["company"],
            "name": payload["name"],
            "email": payload.get("email", ""),
            "phone": payload.get("phone", ""),
            "source": payload.get("source", "Manual"),
            "status": payload.get("status", "NEW"),
            "score": int(payload.get("score", 50)),
            "stage_id": payload.get("stageId", "stage-entry"),
            "tags": payload.get("tags", []),
            "last_interaction_at": iso_now(),
            "next_action": payload.get("nextAction", "Realizar primeiro contato"),
            "notes": payload.get("notes", ""),
            "created_at": iso_now(),
            "updated_at": iso_now(),
        }
        created = self.repository.create_lead(lead)
        self.repository.create_activity(
            {
                "id": f"activity-{uuid4().hex[:8]}",
                "tenant_id": tenant_id,
                "lead_id": created["id"],
                "type": "NOTE",
                "summary": "Lead criado manualmente no CRM.",
                "happened_at": iso_now(),
            }
        )
        return created

    def update_lead(self, tenant_id: str, lead_id: str, payload: dict) -> dict | None:
        updated = self.repository.update_lead(
            lead_id,
            tenant_id,
            {
                "status": payload.get("status"),
                "score": payload.get("score"),
                "stage_id": payload.get("stageId"),
                "next_action": payload.get("nextAction"),
                "notes": payload.get("notes"),
                "updated_at": iso_now(),
            },
        )
        if updated:
            self.repository.create_activity(
                {
                    "id": f"activity-{uuid4().hex[:8]}",
                    "tenant_id": tenant_id,
                    "lead_id": updated["id"],
                    "type": "STATUS_CHANGE",
                    "summary": f"Lead atualizado para {updated['status']} na etapa {updated['stage']}.",
                    "happened_at": iso_now(),
                }
            )
        return updated

    def get_pipeline(self, tenant_id: str) -> list[dict]:
        stages = self.repository.list_pipeline_stages(tenant_id)
        deals = self.repository.list_deals(tenant_id)
        items = []
        for stage in stages:
            stage_deals = [deal for deal in deals if deal["stage_id"] == stage["id"]]
            items.append(
                {
                    "id": stage["id"],
                    "pipelineId": stage["pipeline_id"],
                    "name": stage["name"],
                    "position": stage["position"],
                    "probability": stage["probability"],
                    "deals": [
                        {
                            **deal,
                            "expectedCloseAt": deal["expected_close_at"],
                        }
                        for deal in stage_deals
                    ],
                }
            )
        return items

    def update_deal(self, tenant_id: str, deal_id: str, payload: dict) -> dict | None:
        updated = self.repository.update_deal(
            deal_id,
            tenant_id,
            {
                "stage_id": payload.get("stageId"),
                "status": payload.get("status"),
                "updated_at": iso_now(),
            },
        )
        if updated:
            return {
                **updated,
                "expectedCloseAt": updated["expected_close_at"],
            }
        return None

    def list_tasks(self, tenant_id: str) -> list[dict]:
        return self.repository.list_tasks(tenant_id)

    def list_agenda(self, tenant_id: str) -> list[dict]:
        return [
            {
                **item,
                "startsAt": item["starts_at"],
                "endsAt": item["ends_at"],
            }
            for item in self.repository.list_agenda(tenant_id)
        ]

    def list_automations(self, tenant_id: str) -> list[dict]:
        return self.repository.list_automations(tenant_id)

    def list_team(self, tenant_id: str) -> dict:
        return {
            "users": self.repository.list_users(tenant_id),
            "teams": self.repository.list_teams(tenant_id),
            "invitations": self.repository.list_invitations(tenant_id),
            "roles": self.repository.list_roles(),
        }

    def list_invitations(self, tenant_id: str) -> list[dict]:
        return self.repository.list_invitations(tenant_id)

    def create_invitation(self, tenant_id: str, inviter_user_id: str, payload: dict) -> dict:
        roles = self.repository.list_roles()
        default_role = next((role for role in roles if role["name"] == "Vendedor"), roles[0])
        role_id = payload.get("roleId", default_role["id"])

        created = self.repository.create_invitation(
            {
                "id": f"invite-{uuid4().hex[:8]}",
                "tenant_id": tenant_id,
                "inviter_user_id": inviter_user_id,
                "email": payload["email"].strip().lower(),
                "role_id": role_id,
                "status": "PENDING",
                "invite_token": f"pulsecrm-{uuid4().hex[:16]}",
                "created_at": iso_now(),
                "accepted_at": None,
            }
        )
        return {
            **created,
            "accept_url": f"/?invite={created['invite_token']}",
        }

    def get_public_invitation(self, invite_token: str) -> dict | None:
        invitation = self.repository.find_invitation_by_token(invite_token)
        if not invitation:
            return None

        return {
            "id": invitation["id"],
            "email": invitation["email"],
            "status": invitation["status"],
            "inviteToken": invitation["invite_token"],
            "roleName": invitation["role_name"],
            "tenantName": invitation["tenant_name"],
            "inviterName": invitation["inviter_name"],
            "acceptedAt": invitation["accepted_at"],
        }

    def accept_invitation(self, invite_token: str, payload: dict) -> tuple[dict | None, str | None]:
        invitation = self.repository.find_invitation_by_token(invite_token)
        if not invitation:
            return None, "Invite nao encontrado."
        if invitation["status"] != "PENDING":
            return None, "Este convite ja foi utilizado ou expirou."

        email = invitation["email"]
        if self.repository.find_user_by_email(invitation["tenant_id"], email):
            return None, "Ja existe uma conta com este e-mail neste workspace."
        if not payload.get("name") or not payload.get("password"):
            return None, "Nome e senha sao obrigatorios para aceitar o convite."

        role_title = invitation["role_name"]
        self.repository.create_user(
            {
                "id": f"user-{uuid4().hex[:8]}",
                "tenant_id": invitation["tenant_id"],
                "team_id": None,
                "role_id": invitation["role_id"],
                "name": payload["name"].strip(),
                "email": email,
                "password_hash": hash_password(payload["password"]),
                "phone": payload.get("phone", ""),
                "title": role_title,
                "created_at": iso_now(),
            }
        )
        self.repository.accept_invitation(invitation["id"], iso_now())
        self.repository.create_activity(
            {
                "id": f"activity-{uuid4().hex[:8]}",
                "tenant_id": invitation["tenant_id"],
                "lead_id": None,
                "type": "NOTE",
                "summary": f"{payload['name'].strip()} entrou no workspace pelo convite de {invitation['inviter_name']}.",
                "happened_at": iso_now(),
            }
        )
        session = self.auth_service.login(email, payload["password"])
        return session, None
