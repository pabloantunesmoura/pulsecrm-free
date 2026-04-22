from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .config import HOST, PORT
from .db import initialize_schema
from .http import parse_request_path, send_json, serve_static
from .router import Router
from .seed import seed_database


class PulseRequestHandler(BaseHTTPRequestHandler):
    router = Router()

    def do_GET(self) -> None:
        self._handle("GET")

    def do_POST(self) -> None:
        self._handle("POST")

    def do_PATCH(self) -> None:
        self._handle("PATCH")

    def log_message(self, format: str, *args) -> None:
        return

    def _handle(self, method: str) -> None:
        path, _query = parse_request_path(self.path)

        if self.router.dispatch(self, method, path):
            return

        if method == "GET" and serve_static(self, path):
            return

        send_json(self, 404, {"error": "not_found", "message": "Recurso nao encontrado."})


def bootstrap() -> None:
    initialize_schema()
    seed_database()
    server = ThreadingHTTPServer((HOST, PORT), PulseRequestHandler)
    print(f"PulseCRM rodando em http://{HOST}:{PORT}")
    server.serve_forever()
