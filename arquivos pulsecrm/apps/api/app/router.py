from .controllers.auth_controller import AuthController
from .controllers.crm_controller import CrmController
from .http import send_json
from .services.auth_service import AuthService


class Router:
    def __init__(self) -> None:
        self.auth_controller = AuthController()
        self.crm_controller = CrmController()
        self.auth_service = AuthService()

    def _authenticate(self, handler) -> dict | None:
        context = self.auth_service.authenticate(handler.headers.get("Authorization"))
        if not context:
            send_json(handler, 401, {"error": "unauthorized", "message": "Sessao invalida ou expirada."})
            return None
        return context

    def dispatch(self, handler, method: str, path: str) -> bool:
        if method == "GET" and path == "/api/health":
            send_json(handler, 200, {"status": "ok", "service": "pulsecrm-api-python"})
            return True

        if method == "GET" and path == "/api/public/users":
            self.auth_controller.public_users(handler)
            return True

        if method == "GET" and path.startswith("/api/public/invitations/"):
            invite_token = path.rsplit("/", 1)[-1]
            self.crm_controller.public_invitation(handler, invite_token)
            return True

        if method == "POST" and path == "/api/auth/login":
            self.auth_controller.login(handler)
            return True

        if method == "POST" and path == "/api/public/accept-invitation":
            self.crm_controller.accept_invitation(handler)
            return True

        auth_context = None
        if path.startswith("/api/"):
            auth_context = self._authenticate(handler)
            if not auth_context:
                return True

        if method == "GET" and path == "/api/bootstrap":
            self.crm_controller.bootstrap(handler, auth_context)
            return True

        if method == "GET" and path == "/api/dashboard":
            self.crm_controller.dashboard(handler, auth_context)
            return True

        if method == "GET" and path == "/api/leads":
            self.crm_controller.list_leads(handler, auth_context)
            return True

        if method == "POST" and path == "/api/leads":
            self.crm_controller.create_lead(handler, auth_context)
            return True

        if method == "PATCH" and path.startswith("/api/leads/"):
            lead_id = path.rsplit("/", 1)[-1]
            self.crm_controller.update_lead(handler, auth_context, lead_id)
            return True

        if method == "GET" and path == "/api/pipeline":
            self.crm_controller.pipeline(handler, auth_context)
            return True

        if method == "PATCH" and path.startswith("/api/deals/"):
            deal_id = path.split("/")[3]
            self.crm_controller.update_deal(handler, auth_context, deal_id)
            return True

        if method == "GET" and path == "/api/tasks":
            self.crm_controller.tasks(handler, auth_context)
            return True

        if method == "GET" and path == "/api/agenda":
            self.crm_controller.agenda(handler, auth_context)
            return True

        if method == "GET" and path == "/api/automations":
            self.crm_controller.automations(handler, auth_context)
            return True

        if method == "GET" and path == "/api/team":
            self.crm_controller.team(handler, auth_context)
            return True

        if method == "GET" and path == "/api/invitations":
            self.crm_controller.invitations(handler, auth_context)
            return True

        if method == "POST" and path == "/api/invitations":
            self.crm_controller.create_invitation(handler, auth_context)
            return True

        return False
