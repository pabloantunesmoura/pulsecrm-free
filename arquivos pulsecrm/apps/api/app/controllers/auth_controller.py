from ..http import read_json_body, send_json
from ..services.auth_service import AuthService


class AuthController:
    def __init__(self) -> None:
        self.service = AuthService()

    def public_users(self, handler) -> None:
        send_json(handler, 200, {"items": self.service.list_public_users()})

    def login(self, handler) -> None:
        payload = read_json_body(handler)
        email = str(payload.get("email", "")).strip()
        password = str(payload.get("password", ""))

        if not email or not password:
            send_json(handler, 400, {"error": "bad_request", "message": "E-mail e senha sao obrigatorios."})
            return

        session = self.service.login(email, password)
        if not session:
            send_json(handler, 401, {"error": "unauthorized", "message": "Credenciais invalidas."})
            return

        send_json(handler, 200, session)
