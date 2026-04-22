import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .config import WEB_DIR


def read_json_body(handler) -> dict:
    length = int(handler.headers.get("Content-Length", "0"))
    raw = handler.rfile.read(length) if length else b""
    return json.loads(raw.decode("utf-8")) if raw else {}


def send_json(handler, status_code: int, payload: dict) -> None:
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status_code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def send_no_content(handler, status_code: int = 204) -> None:
    handler.send_response(status_code)
    handler.end_headers()


def parse_request_path(path: str) -> tuple[str, dict]:
    parsed = urlparse(path)
    return parsed.path, parse_qs(parsed.query)


def guess_content_type(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".css":
        return "text/css; charset=utf-8"
    if suffix == ".js":
        return "application/javascript; charset=utf-8"
    if suffix == ".json":
        return "application/json; charset=utf-8"
    if suffix == ".svg":
        return "image/svg+xml"
    return "text/html; charset=utf-8"


def serve_static(handler, path: str) -> bool:
    relative_path = "index.html" if path == "/" else path.lstrip("/")
    file_path = (WEB_DIR / relative_path).resolve()
    if not str(file_path).startswith(str(WEB_DIR.resolve())):
        return False
    if not file_path.exists() or not file_path.is_file():
        return False

    content = file_path.read_bytes()
    handler.send_response(200)
    handler.send_header("Content-Type", guess_content_type(file_path))
    handler.send_header("Content-Length", str(len(content)))
    handler.end_headers()
    handler.wfile.write(content)
    return True
