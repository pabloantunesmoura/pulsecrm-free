import sqlite3
from contextlib import contextmanager

from .config import DATA_DIR, DATABASE_URL, DB_PATH, DB_PROVIDER, SCHEMA_PATH

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:  # pragma: no cover - optional in local sqlite mode
    psycopg = None
    dict_row = None


def _normalize_query(query: str) -> str:
    if DB_PROVIDER == "sqlite":
        return query

    parts = query.split("?")
    if len(parts) == 1:
        return query
    return "%s".join(parts)


def _split_statements(script: str) -> list[str]:
    return [statement.strip() for statement in script.split(";") if statement.strip()]


class ConnectionWrapper:
    def __init__(self, connection):
        self.connection = connection

    def execute(self, query: str, params=()):
        return self.connection.execute(_normalize_query(query), params)

    def executemany(self, query: str, params_seq):
        if DB_PROVIDER == "sqlite":
            return self.connection.executemany(query, params_seq)
        with self.connection.cursor() as cursor:
            cursor.executemany(_normalize_query(query), params_seq)
            return cursor

    def executescript(self, script: str):
        if DB_PROVIDER == "sqlite":
            return self.connection.executescript(script)
        with self.connection.cursor() as cursor:
            for statement in _split_statements(script):
                cursor.execute(statement)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


def connect():
    if DB_PROVIDER == "postgres":
        if psycopg is None:
            raise RuntimeError("psycopg nao esta instalado para o modo PostgreSQL.")
        connection = psycopg.connect(DATABASE_URL, row_factory=dict_row)
        return ConnectionWrapper(connection)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return ConnectionWrapper(connection)


@contextmanager
def get_connection():
    connection = connect()
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialize_schema() -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_connection() as connection:
        connection.executescript(schema)
