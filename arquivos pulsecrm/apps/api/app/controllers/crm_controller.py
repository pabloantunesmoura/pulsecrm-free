from ..http import read_json_body, send_json
from ..services.crm_service import CrmService
from ..services.dashboard_service import DashboardService


class CrmController:
    def __init__(self) -> None:
        self.crm_service = CrmService()
        self.dashboard_service = DashboardService()

    def bootstrap(self, handler, auth_context: dict) -> None:
        tenant_id = auth_context["tenant_id"]
        payload = self.crm_service.get_bootstrap(tenant_id)
        payload["dashboard"] = self.dashboard_service.get_dashboard(tenant_id)
        payload["leads"] = self.crm_service.list_leads(tenant_id)
        payload["pipeline"] = self.crm_service.get_pipeline(tenant_id)
        send_json(handler, 200, payload)

    def dashboard(self, handler, auth_context: dict) -> None:
        send_json(handler, 200, self.dashboard_service.get_dashboard(auth_context["tenant_id"]))

    def list_leads(self, handler, auth_context: dict) -> None:
        send_json(handler, 200, {"items": self.crm_service.list_leads(auth_context["tenant_id"])})

    def create_lead(self, handler, auth_context: dict) -> None:
        payload = read_json_body(handler)
        if not payload.get("name") or not payload.get("company"):
            send_json(handler, 400, {"error": "bad_request", "message": "Os campos nome e empresa sao obrigatorios."})
            return

        created = self.crm_service.create_lead(
            auth_context["tenant_id"],
            auth_context["user"]["id"],
            payload,
        )
        send_json(handler, 201, {"item": created})

    def update_lead(self, handler, auth_context: dict, lead_id: str) -> None:
        payload = read_json_body(handler)
        item = self.crm_service.update_lead(auth_context["tenant_id"], lead_id, payload)
        if not item:
            send_json(handler, 404, {"error": "not_found", "message": "Lead nao encontrado."})
            return
        send_json(handler, 200, {"item": item})

    def pipeline(self, handler, auth_context: dict) -> None:
        send_json(handler, 200, {"items": self.crm_service.get_pipeline(auth_context["tenant_id"])})

    def update_deal(self, handler, auth_context: dict, deal_id: str) -> None:
        payload = read_json_body(handler)
        item = self.crm_service.update_deal(auth_context["tenant_id"], deal_id, payload)
        if not item:
            send_json(handler, 404, {"error": "not_found", "message": "Negocio nao encontrado."})
            return
        send_json(handler, 200, {"item": item})

    def tasks(self, handler, auth_context: dict) -> None:
        send_json(handler, 200, {"items": self.crm_service.list_tasks(auth_context["tenant_id"])})

    def agenda(self, handler, auth_context: dict) -> None:
        send_json(handler, 200, {"items": self.crm_service.list_agenda(auth_context["tenant_id"])})

    def automations(self, handler, auth_context: dict) -> None:
        send_json(handler, 200, {"items": self.crm_service.list_automations(auth_context["tenant_id"])})

    def team(self, handler, auth_context: dict) -> None:
        send_json(handler, 200, self.crm_service.list_team(auth_context["tenant_id"]))

    def invitations(self, handler, auth_context: dict) -> None:
        send_json(handler, 200, {"items": self.crm_service.list_invitations(auth_context["tenant_id"])})

    def create_invitation(self, handler, auth_context: dict) -> None:
        payload = read_json_body(handler)
        if not payload.get("email"):
            send_json(handler, 400, {"error": "bad_request", "message": "O e-mail do convidado e obrigatorio."})
            return

        item = self.crm_service.create_invitation(
            auth_context["tenant_id"],
            auth_context["user"]["id"],
            payload,
        )
        send_json(handler, 201, {"item": item})

    def public_invitation(self, handler, invite_token: str) -> None:
        item = self.crm_service.get_public_invitation(invite_token)
        if not item:
            send_json(handler, 404, {"error": "not_found", "message": "Convite nao encontrado."})
            return
        send_json(handler, 200, {"item": item})

    def accept_invitation(self, handler) -> None:
        payload = read_json_body(handler)
        invite_token = str(payload.get("inviteToken", "")).strip()
        if not invite_token:
            send_json(handler, 400, {"error": "bad_request", "message": "O token do convite e obrigatorio."})
            return

        session, error = self.crm_service.accept_invitation(invite_token, payload)
        if error:
            send_json(handler, 400, {"error": "bad_request", "message": error})
            return
        send_json(handler, 201, session)
