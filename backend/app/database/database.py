import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured in .env"
    )


# ============================================================
# SUPABASE POSTGRES ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)


# ============================================================
# SESSION
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ============================================================
# SQLAlchemy BASE
# ============================================================

Base = declarative_base()


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# CONNECTION TEST
# ============================================================

def test_database_connection():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT 1")
        )

        return result.scalar() == 1