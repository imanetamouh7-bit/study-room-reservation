import os
from pathlib import Path

import psycopg2
from dotenv import dotenv_values


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV = dotenv_values(PROJECT_ROOT / ".env")


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=5432,
        database=os.getenv("DB_NAME", ENV.get("POSTGRES_DB")),
        user=os.getenv("DB_USER", ENV.get("POSTGRES_USER")),
        password=os.getenv(
            "DB_PASSWORD",
            ENV.get("POSTGRES_PASSWORD"),
        ),
    )