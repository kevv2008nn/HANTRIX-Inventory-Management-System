import os
from pathlib import Path
from urllib.parse import urlsplit

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = lambda: None

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{Path(__file__).resolve().parents[2] / 'smartlab.db'}"
)

if DATABASE_URL.startswith(("postgresql://", "postgresql+psycopg2://")):
    try:
        parsed_database_url = urlsplit(DATABASE_URL)
    except ValueError as error:
        raise RuntimeError(
            "Invalid DATABASE_URL: URL-encode special characters in the "
            "PostgreSQL username or password."
        ) from error

    if not parsed_database_url.hostname or "@" in parsed_database_url.hostname:
        raise RuntimeError(
            "Invalid DATABASE_URL: URL-encode special characters in the "
            "PostgreSQL password, for example @ as %40."
        )

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()