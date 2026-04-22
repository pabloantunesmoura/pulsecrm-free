import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
API_DIR = ROOT_DIR / "apps" / "api"
WEB_DIR = ROOT_DIR / "apps" / "web"
DATA_DIR = API_DIR / "data"
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
DB_PROVIDER = "postgres" if DATABASE_URL else "sqlite"
DB_PATH = Path(os.getenv("SQLITE_PATH", str(DATA_DIR / "pulsecrm.sqlite3")))
SCHEMA_PATH = API_DIR / ("schema_postgres.sql" if DB_PROVIDER == "postgres" else "schema.sql")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "3000"))
SESSION_TTL_HOURS = 12
